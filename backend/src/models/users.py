import enum

from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    PATIENT = 'patient'

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.PATIENT)

    def __repr__(self):
        return f"User {self.email} ({self.role})"
