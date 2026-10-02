from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_owner
from app.database.database import get_db
from app.models.user import User
from app.schemas.payroll import PayrollResponse
from app.services.payroll import calculate_payroll

router = APIRouter(
    prefix="/payroll",
    tags=["Payroll"],
)


@router.get("/", response_model=PayrollResponse)
def get_payroll(
    period: str = Query(
        ...,
        pattern="^(weekly|monthly)$",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chef_id = None

    # إذا كان المستخدم Chef
    if current_user.role == "chef":
        chef_id = current_user.id

    return calculate_payroll(
        db=db,
        period=period,
        chef_id=chef_id,
    )

@router.post("/is-payed", response_model=PayrollResponse)
 
    


