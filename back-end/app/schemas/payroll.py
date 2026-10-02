from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class PayrollWorkerResponse(BaseModel):
    worker_id: int
    worker_name: str
    job_name: str
    days_present: int
    daily_wage: Decimal
    total_wage: Decimal
    attendance_percentage: float


class PayrollResponse(BaseModel):
    period: str
    start_date: date
    end_date: date
    workers: list[PayrollWorkerResponse]
    total: Decimal
    attendance_percentage: float