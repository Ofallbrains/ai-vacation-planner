from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlmodel import Session

from app.dependencies.db import get_session

from app.schemas.auth import (UserLogin, UserRegister, Token)

from app.core.security import create_access_token

from app.services.auth_service import (create_user, authenticate_user)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# register

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    session: Session = Depends(get_session)
):
    user = create_user(
        session,
        user_data
    )
    
    if not user: 
        raise HTTPException(
            status_code=400,
            detail="Email alrealy registered"
        )
        
    return {
        "message": "User registered successfully"
    }
    
# login

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    
    user = authenticate_user(
        session,
        user_data.email,
        user_data.password
    ) 
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }