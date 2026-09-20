from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class PatientRecord(BaseModel):
    name: str
    age: int
    gender: Literal["male", "female", "other"]
    village: str
    phone: str
    chief_complaint: str
    # Vitals (optional)
    temperature: Optional[str] = None
    blood_pressure: Optional[str] = None
    spo2: Optional[str] = None
    weight: Optional[str] = None


class PatientRecordOut(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    village: str
    phone: str
    chief_complaint: str
    temperature: Optional[str]
    blood_pressure: Optional[str]
    spo2: Optional[str]
    weight: Optional[str]
    health_worker_id: str
    synced: bool
    created_at: datetime


class SyncRequest(BaseModel):
    record_ids: list[str]
