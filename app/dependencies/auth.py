from fastapi import(Depends, HTTPException, status)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlmodel import Session, select
from app.dependencies.db import get_session
from app.models.user import User
from app.core.security import verify_token

# token extraction
oauth2_scheme = HTTPBearer()

# get current user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )
    
    try:
        token = credentials.credentials

        payload = verify_token(token)
        
        if payload is None:
            raise credentials_exception
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    user = session.exec(select(User).where(User.email == email)).first()
    
    if user is None:
        raise credentials_exception
    
    return user