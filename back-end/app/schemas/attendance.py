from datetime import date
from typing import Literal

from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    worker_id: int
    status: Literal["present", "absent"]


class AttendanceUpdate(BaseModel):
    status: Literal["present", "absent"]


class AttendanceResponse(BaseModel):
    id: int
    worker_id: int
    date: date
    status: Literal["present", "absent"]

    class Config:
        from_attributes = True