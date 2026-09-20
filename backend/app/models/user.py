from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime


class UserRegister(BaseModel):
    name: str
    phone: str
    password: str
    role: Literal["patient", "doctor", "health_worker"]
    village: Optional[str] = None
    district: Optional[str] = None
    # Doctor-specific
    specialization: Optional[str] = None
    hospital: Optional[str] = None
    registration_no: Optional[str] = None
    fee: Optional[int] = None
    # Health worker specific
    block: Optional[str] = None


class UserLogin(BaseModel):
    phone: str
    password: str
    role: Literal["patient", "doctor", "health_worker"]


class UserOut(BaseModel):
    id: str
    name: str
    phone: str
    role: str
    village: Optional[str] = None
    district: Optional[str] = None
    specialization: Optional[str] = None
    hospital: Optional[str] = None
    fee: Optional[int] = None
    block: Optional[str] = None
    created_at: datetime
