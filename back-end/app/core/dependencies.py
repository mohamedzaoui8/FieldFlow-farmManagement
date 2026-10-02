from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = decode_access_token(token)
    except ValueError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user


def require_owner(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="يتطلب صلاحيات المالك",
        )

    return current_user


def require_chef(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "chef":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chef access required",
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=401,
            detail="تم تعطيل المستخدم"
        )

    return current_user

def require_owner_or_chef(
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["owner", "chef"]:
        raise HTTPException(
            status_code=403,
            detail="لا تملك صلاحية الوصول إلى هذه الصفحة"
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=401,
            detail="تم تعطيل المستخدم"
        )

    return current_user