from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Worker(Base):
    __tablename__ = "workers"

    id =Column(Integer , primary_key=True , index=True)
    name=Column(String(50) ,nullable=False)
    chef_id=Column(Integer , ForeignKey("users.id"), nullable=False)
    job_id=Column(Integer , ForeignKey("jobs.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    chef=relationship("User",back_populates="workers")
    job=relationship("Job" ,back_populates="workers")
    payrolls = relationship("Payroll", back_populates="worker")
    attendance = relationship("Attendance",back_populates="worker")
