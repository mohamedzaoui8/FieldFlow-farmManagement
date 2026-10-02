# C:\Users\tassili\Downloads\sersou-project\back-end\app\routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_owner
from app.core.security import hash_password
from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserCreateResponse, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


# CREATE USER CHEF
@router.post(
    "/", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role="chef",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "تم إنشاء المشرف بنجاح", "user": new_user}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# READ ALL CHEF
@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db), current_user: User = Depends(require_owner)
):
    users = db.query(User).all()

    return users


# READ ONE
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


# UPDATE
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="المستخدم غير موجود"
        )  # must try in postman 9999

    if user_data.name is not None:
        user.name = user_data.name

    if user_data.email is not None:
        existing_user = (
            db.query(User)
            .filter(User.email == user_data.email, User.id != user_id)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="البريد الإلكتروني مسجل مسبقاً",
            )  # must try in postman
        user.email = user_data.email

    if user_data.password is not None:
        user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)

    return user


# DELETE_SOFTLY
@router.patch("/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="المستخدم غير موجود"
        )

    if user.role != "chef":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="يمكن تعطيل المشرفين فقط"
        )

    # Check if the Chef has workers
    if user.workers:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"لا يمكن تعطيل هذا المشرف. "
                f"لديه {len(user.workers)} عامل مرتبط به. "
            ),
        )

    user.is_active = False
    db.commit()

    return {"message": "تم تعطيل المستخدم"}
