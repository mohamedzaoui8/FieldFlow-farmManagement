from pydantic import BaseModel


class DashboardTeam(BaseModel):
    chef_name: str
    initials: str
    total_workers: int
    present: int
    attendance_percentage: int


class DashboardResponse(BaseModel):
    total_workers: int
    total_chefs: int
    present_today: int
    absent_today: int
    attendance_percentage: int
    weekly_payroll: float
    teams: list[DashboardTeam]