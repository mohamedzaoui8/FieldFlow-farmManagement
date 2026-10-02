# app/models/job.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    daily_wage = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    chef_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    payment_frequency = Column(String(20), nullable=False)
    workers = relationship("Worker", back_populates="job")
    chef = relationship("User", back_populates="job")
