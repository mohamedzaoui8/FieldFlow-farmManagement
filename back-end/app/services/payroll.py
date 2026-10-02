from calendar import monthrange
from datetime import datetime, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.job import Job
from app.models.worker import Worker
from app.schemas.payroll import PayrollResponse, PayrollWorkerResponse


def calculate_payroll(
    db: Session,
    period: str,
    chef_id: int | None = None,
) -> PayrollResponse:
    today = datetime.now(
        ZoneInfo("Africa/Algiers")
    ).date()

    # تحديد الفترة
    if period == "weekly":
        days_since_saturday = (today.weekday() - 5) % 7

        start_date = today - timedelta(
            days=days_since_saturday
        )

        # Saturday -> Thursday
        end_date = start_date + timedelta(days=5)

    elif period == "monthly":
        start_date = today.replace(day=1)

        last_day = monthrange(
            today.year,
            today.month
        )[1]

        end_date = today.replace(day=last_day)

    else:
        raise ValueError("نظام الدفع غير صالح")

    # العمال النشطون
    query = db.query(Worker).filter(
        Worker.is_active.is_(True)
    )

    # إذا كان المستخدم Chef، نعرض عماله فقط
    if chef_id is not None:
        query = query.filter(
            Worker.chef_id == chef_id
        )

    workers = query.all()

    payroll_workers = []

    total_present_days = 0
    total_possible_days = 0

    # حساب راتب كل عامل
    for worker in workers:

        job = (
            db.query(Job)
            .filter(Job.id == worker.job_id)
            .first()
        )

        if not job:
            continue

        # عدد أيام الحضور
        days_present = (
            db.query(Attendance)
            .filter(
                Attendance.worker_id == worker.id,
                Attendance.date >= start_date,
                Attendance.date <= end_date,
                Attendance.status == "present",
            )
            .count()
        )

        # عدد أيام العمل في الفترة
        if period == "weekly":
            possible_days = 6

        else:
            possible_days = sum(
                1
                for day_offset in range(
                    (end_date - start_date).days + 1
                )
                if (
                    start_date
                    + timedelta(days=day_offset)
                ).weekday() != 4
            )

        daily_wage = job.daily_wage

        total_wage = days_present * daily_wage

        # نسبة حضور العامل
        attendance_percentage = (
            (days_present / possible_days) * 100
            if possible_days > 0
            else 0
        )

        total_present_days += days_present
        total_possible_days += possible_days

        payroll_workers.append(
            PayrollWorkerResponse(
                worker_id=worker.id,
                worker_name=worker.name,
                job_name=job.name,
                days_present=days_present,
                daily_wage=daily_wage,
                total_wage=total_wage,
                attendance_percentage=round(
                    attendance_percentage,
                    2
                ),
            )
        )

    # مجموع الرواتب
    total = sum(
        (
            worker.total_wage
            for worker in payroll_workers
        ),
        Decimal(0),
    )

    # نسبة الحضور الإجمالية
    attendance_percentage = (
        (
            total_present_days
            / total_possible_days
        ) * 100
        if total_possible_days > 0
        else 0
    )

    return PayrollResponse(
        period=period,
        start_date=start_date,
        end_date=end_date,
        workers=payroll_workers,
        total=total,
        attendance_percentage=round(
            attendance_percentage,
            2
        ),
    )

