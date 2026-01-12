from pydantic import BaseModel, EmailStr

from src.models.users import UserRole


class UserSend(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.PATIENT

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
      from_attributes: True
