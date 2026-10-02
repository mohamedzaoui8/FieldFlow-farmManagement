from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    daily_wage: Decimal = Field(gt=0)
    payment_frequency: Literal["weekly", "monthly"] = "weekly"
    chef_id: int


class JobUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)

    daily_wage: Decimal | None = Field(default=None, gt=0)

    payment_frequency: Literal["weekly", "monthly"] | None = Field(default=None)


class JobResponse(BaseModel):
    id: int
    name: str
    daily_wage: Decimal
    payment_frequency: Literal["weekly", "monthly"]

    class Config:
        from_attributes = True
