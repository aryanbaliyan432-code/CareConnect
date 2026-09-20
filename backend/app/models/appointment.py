from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class AppointmentCreate(BaseModel):
    doctor_id: str
    patient_name: str
    patient_village: str
    patient_age: int
    slot_time: str          # e.g. "3:30 PM"
    slot_date: str          # e.g. "2026-03-14"
    consult_type: Literal["video", "chat"] = "video"


class AppointmentOut(BaseModel):
    id: str
    doctor_id: str
    doctor_name: str
    doctor_specialization: str
    patient_id: str
    patient_name: str
    patient_village: str
    patient_age: int
    slot_time: str
    slot_date: str
    consult_type: str
    status: str             # scheduled | completed | cancelled
    fee: int
    created_at: datetime


class SlotQuery(BaseModel):
    doctor_id: str
    date: str               # YYYY-MM-DD
