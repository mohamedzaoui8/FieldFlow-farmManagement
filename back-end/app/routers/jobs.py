from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_owner
from app.database.database import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse, JobUpdate

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# CREATE
@router.post("/", response_model=JobResponse)
def create_job(
    job: JobCreate,
    current_user: User = Depends(require_owner),
    db: Session = Depends(get_db),
):
    existing_job = db.query(Job).filter(Job.name == job.name).first()

    existing_chef = (
        db.query(User).filter(User.id == job.chef_id, User.role == "chef").first()
    )

    if not existing_chef:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="المشرف غير موجود"
        )
    if existing_job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="إسم الوظيفة موجود مسبقًاٍ"
        )

    new_job = Job(
        name=job.name,
        daily_wage=job.daily_wage,
        payment_frequency=job.payment_frequency,
        chef_id=job.chef_id,
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# READ ALL
@router.get("/", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db) , current_user: User = Depends(require_owner)):
    jobs = db.query(Job).all()

    return jobs


# READ ONE
@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_owner)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="الوظيفة غير موجودة")

    return job


# UPDATE
@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user: User = Depends(require_owner),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الوظيفة غير موجودة"
        )

    update_data = job_data.model_dump(exclude_unset=True)

    if len(update_data) == 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="إنك تفوم يتغيير جميع خصائص الوظيفة، قم بإنشاء وظيفة جديدة"
        )
    if "name" in update_data:
        job.name = update_data["name"]

    if "daily_wage" in update_data:
        job.daily_wage = update_data["daily_wage"]

    if "payment_frequency" in update_data:
        job.payment_frequency = update_data["payment_frequency"]

    if "chef_id" in update_data:
        existing_chef = db.query(User).filter(
            User.id == update_data["chef_id"],
            User.role == "chef"
        ).first()

        if not existing_chef:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chef غير موجود"
            )

        job.chef_id = update_data["chef_id"]

    db.commit()
    db.refresh(job)

    return job

# DELETE SOFT
@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db) , current_user: User = Depends(require_owner)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="الوظيفة غير موجودة")

    job.is_active = False
    db.commit()
    return {"message": "تم إلغاء تفعيل الوظيفة بنجاح"}
