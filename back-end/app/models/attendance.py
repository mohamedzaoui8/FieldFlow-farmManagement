# app/models/attendance.py
from sqlalchemy import Column, Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False, default="present")
    worker = relationship("Worker" , back_populates="attendance")

    __table_args__ = (
        UniqueConstraint("worker_id", "date", name="uq_worker_date"),
    )