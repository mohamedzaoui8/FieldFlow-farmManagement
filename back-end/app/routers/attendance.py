# header: back-end/app/routers/attendance.py
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import require_chef
from app.database.database import get_db
from app.models.attendance import Attendance
from app.models.user import User
from app.models.worker import Worker
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceUpdate,
)

router = APIRouter(prefix="/attendance", tags=["Attendance"])


# CREATE
@router.post("/", response_model=AttendanceResponse)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_chef),
):
    worker = db.query(Worker).filter(Worker.id == attendance.worker_id).first()
    today = date.today()
    if not worker:
        raise HTTPException(status_code=404, detail="العامل غير موجود")

    if worker.chef_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="ليس لديك إذن لتسجيل حضور هذا العامل"
        )
    existing = (
        db.query(Attendance)
        .filter(
            Attendance.worker_id == attendance.worker_id,
            Attendance.date == today
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="تم تسجيل حضور هذا العامل في هذا اليوم مسبقًا"
        )

    new_attendance = Attendance(
        worker_id=attendance.worker_id, date=today, status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


# READ ALL
@router.get(
    "/",
    response_model=list[AttendanceResponse],
)
def get_attendance(
    db: Session = Depends(get_db), current_user: User = Depends(require_chef)
):
    records = (
        db.query(Attendance)
        .join(Worker)
        .filter(Worker.chef_id == current_user.id)
        .all()
    )
    return records


# READ ONE
@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance_record(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_chef),
):
    record = (
        db.query(Attendance)
        .join(Worker)
        .filter(Attendance.id == attendance_id, Worker.chef_id == current_user.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="سجل الحضور غير موجود")

    return record


# UPDATE
@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_chef),
):

    record = (
        db.query(Attendance)
        .join(Worker)
        .filter(Attendance.id == attendance_id, Worker.chef_id == current_user.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="سجل الحضور غير موجود")

    if record.date != date.today():
        raise HTTPException(
            status_code=403, detail="لا يمكن تعديل الحضور إلا في نفس اليوم"
        )
    record.status = attendance_data.status

    db.commit()
    db.refresh(record)

    return record


# DELETE
@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_chef),
):
    record = (
        db.query(Attendance)
        .join(Worker)
        .filter(Attendance.id == attendance_id, Worker.chef_id == current_user.id)
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="سجل الحضور غير موجود")

    db.delete(record)
    db.commit()

    return {"message": "تم حذف سجل الحضور بنجاح"}
