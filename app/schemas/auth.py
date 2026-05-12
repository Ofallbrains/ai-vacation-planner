from pydantic import BaseModel, EmailStr

# registering schema
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    
# login schema

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# token response
class Token(BaseModel):
    access_token: str
    token_type: str