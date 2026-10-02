from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_owner, require_owner_or_chef
from app.database.database import get_db
from app.models.user import User
from app.models.worker import Worker
from app.schemas.worker import ReassignWorkers, WorkerCreate, WorkerResponse

router = APIRouter(prefix="/workers", tags=["Workers"])


# CREATE
@router.post("/", response_model=WorkerResponse)
def create_worker(
    worker: WorkerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner_or_chef),
):

    if current_user.role == "owner":
        chef_exist = (
            db.query(User)
            .filter(User.id == worker.chef_id, User.role == "chef")
            .first()
        )

        if not chef_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="خطأ في الطلب"
            )
        if not chef_exist.job or chef_exist.job.id != worker.job_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="خطأ في الطلب"
            )
        new_worker = Worker(
            name=worker.name, chef_id=worker.chef_id, job_id=worker.job_id
        )
    if current_user.role == "chef":
        new_worker = Worker(
            name=worker.name, chef_id=current_user.id, job_id=current_user.job.id
        )

    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)

    return new_worker


# READ ALL
@router.get("/", response_model=list[WorkerResponse])
def get_workers(
    db: Session = Depends(get_db), current_user: User = Depends(require_owner_or_chef)
):
    if current_user.role == "chef":
        workers = (
            db.query(Worker)
            .filter(Worker.chef_id == current_user.id, Worker.is_active == True)
            .all()
        )
    else:
        workers = db.query(Worker).filter(Worker.is_active == True).all()

    return workers


# ------------------------------------------------------------------------------
# # READ ONE
# @router.get("/{worker_id}", response_model=WorkerResponse)
# def get_worker(
#     worker_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_owner_or_chef),
# ):
#     worker = db.query(Worker).filter(Worker.id == worker_id).first()

#     if not worker:
#         raise HTTPException(status_code=404, detail="العامل غير موجود")

#     return worker
# ------------------------------------------------------------------------------


# UPDATE
@router.put("/{worker_id}", response_model=WorkerResponse)
def update_worker(
    worker_id: int,
    worker_data: WorkerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner_or_chef),
):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()

    if not worker:
        raise HTTPException(status_code=404, detail="العامل غير موجود")

    worker.name = worker_data.name
    worker.chef_id = worker_data.chef_id
    worker.job_id = worker_data.job_id

    db.commit()
    db.refresh(worker)

    return worker


# DELETE SOFT
@router.delete("/{worker_id}")
def delete_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner_or_chef),
):
    if current_user.role == "owner":
        worker = (
            db.query(Worker)
            .filter(Worker.id == worker_id, Worker.is_active == True)
            .first()
        )
    else:
        worker = (
            db.query(Worker)
            .filter(
                Worker.id == worker_id,
                Worker.is_active == True,
                Worker.chef_id == current_user.id,
            )
            .first()
        )

    if not worker:
        raise HTTPException(status_code=404, detail="العامل غير موجود")

    worker.is_active = False
    db.commit()

    return {"message": "تم إلغاء تفعيل العامل بنجاح"}


# DEACTIVATE CHEF WITH HIS WORKERS
@router.patch("/ByChef/{chef_id}/deactivate")
def deactivate_workers_by_chef(
    chef_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    chef = db.query(User).filter(User.id == chef_id, User.role == "chef").first()

    if not chef:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="المشرف غير موجود"
        )

    # Deactivate all workers associated with the chef
    for worker in chef.workers:
        worker.is_active = False

    db.commit()

    return {
        "message": f"تم إلغاء تفعيل جميع العمال المرتبطين بالمشرف {chef.name} بنجاح"
    }


# REASSIGN WORKER
@router.put("/reassignByChef")
def reassign_worker(
    data: ReassignWorkers,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    old_chef = (
        db.query(User).filter(User.id == data.from_chef_id, User.role == "chef").first()
    )
    new_chef = (
        db.query(User).filter(User.id == data.to_chef_id, User.role == "chef").first()
    )

    if not old_chef or not new_chef:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="المشرف غير موجود"
        )
    if not new_chef.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="المشرف الجديد غير نشط"
        )
    if not new_chef.job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="المشرف الجديد ليس لديه وظيفة محددة",
        )
    for worker in old_chef.workers:
        worker.chef_id = new_chef.id
        worker.job_id = new_chef.job.id

    db.commit()
    return {
        "message": f"تم إعادة تعيين جميع العمال من المشرف {old_chef.name} إلى المشرف {new_chef.name} بنجاح"
    }
