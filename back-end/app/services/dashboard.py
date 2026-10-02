from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.user import User
from app.models.worker import Worker


def get_dashboard_data(db: Session):

    today = date.today()

    # =========================
    # الأسبوع: السبت → الخميس
    # =========================

    # Python weekday:
    # Monday = 0
    # Tuesday = 1
    # Wednesday = 2
    # Thursday = 3
    # Friday = 4
    # Saturday = 5
    # Sunday = 6

    days_since_saturday = (today.weekday() - 5) % 7

    week_start = today - timedelta(days=days_since_saturday)
    week_end = week_start + timedelta(days=5)

    # =========================
    # العمال
    # =========================

    workers = (
        db.query(Worker)
        .filter(Worker.status == "active")
        .all()
    )

    total_workers = len(workers)

    # =========================
    # المشرفون
    # =========================

    total_chefs = (
        db.query(User)
        .filter(User.role == "chef")
        .count()
    )

    # =========================
    # حضور اليوم
    # =========================

    present_today = (
        db.query(Attendance)
        .join(Worker)
        .filter(
            Attendance.date == today,
            Attendance.status == "present",
            Worker.status == "active"
        )
        .count()
    )

    absent_today = (
        db.query(Attendance)
        .join(Worker)
        .filter(
            Attendance.date == today,
            Attendance.status == "absent",
            Worker.status == "active"
        )
        .count()
    )

    attendance_percentage = (
        round((present_today / total_workers) * 100)
        if total_workers > 0
        else 0
    )

    # =========================
    # أجور الأسبوع
    # =========================

    weekly_payroll = 0

    for worker in workers:

        worked_days = (
            db.query(Attendance)
            .filter(
                Attendance.worker_id == worker.id,
                Attendance.date >= week_start,
                Attendance.date <= week_end,
                Attendance.status == "present"
            )
            .count()
        )

        if worker.job:
            weekly_payroll += worked_days * float(worker.job.daily_wage)

    # =========================
    # إحصائيات كل مشرف
    # =========================

    teams = []

    chefs = (
        db.query(User)
        .filter(User.role == "chef")
        .all()
    )

    for chef in chefs:

        team = [
            worker
            for worker in workers
            if worker.chef_id == chef.id
        ]

        total_team_workers = len(team)

        present_team = (
            db.query(Attendance)
            .filter(
                Attendance.date == today,
                Attendance.status == "present",
                Attendance.worker_id.in_(
                    [worker.id for worker in team]
                )
            )
            .count()
            if team
            else 0
        )

        team_percentage = (
            round(
                (present_team / total_team_workers) * 100
            )
            if total_team_workers > 0
            else 0
        )

        initials = "".join(
            word[0]
            for word in chef.name.split()
        )[:2].upper()

        teams.append(
            {
                "chef_name": chef.name,
                "initials": initials,
                "total_workers": total_team_workers,
                "present": present_team,
                "attendance_percentage": team_percentage,
            }
        )

    # =========================
    # النتيجة النهائية
    # =========================

    return {
        "total_workers": total_workers,
        "total_chefs": total_chefs,
        "present_today": present_today,
        "absent_today": absent_today,
        "attendance_percentage": attendance_percentage,
        "weekly_payroll": weekly_payroll,
        "teams": teams,
    }