from sqlmodel import Session, select

from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import(
    hash_password,
    verify_password
)

# create a user

def create_user(
    session: Session,
    user_data: UserRegister
):
    existing_user = session.exec(
        select(User).where(
            User.email == user_data.email
        )
    ).first()
    
    if existing_user:
        return None
    
    user = User(
        email=user_data.email,
        hashed_password=hash_password(
            user_data.password
        )
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

# authenticate user

def authenticate_user(
    session: Session,
    email: str,
    password: str
):
    
    user = session.exec(
        select(User).where(
            User.email == email
        )
    ).first()
    
    if not user:
        return None
    if not verify_password(
        password,
        user.hashed_password
    ):
        return None
    
    return user