# C:\Users\tassili\Downloads\sersou-project\back-end\app\models/payroll.py
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    week_start = Column(Date, nullable=False)
    week_end = Column(Date, nullable=False)
    is_paid = Column(Boolean, default=False, nullable=False)
    days_worked = Column(Integer, nullable=False)
    daily_wage = Column(Numeric(10, 2), nullable=False)
    worker = relationship("Worker", back_populates="payrolls")


    __table_args__ = (
        UniqueConstraint(
            "worker_id",
            "week_start",
            name="uq_worker_week",
        ),
    )