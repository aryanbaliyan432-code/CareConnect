from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Medicine(BaseModel):
    name: str
    dosage: str
    instructions: str


class PrescriptionCreate(BaseModel):
    appointment_id: str
    patient_id: str
    medicines: List[Medicine]
    advice: str


class PrescriptionOut(BaseModel):
    id: str
    rx_number: str
    appointment_id: str
    patient_id: str
    patient_name: str
    patient_age: int
    patient_village: str
    doctor_id: str
    doctor_name: str
    doctor_registration: Optional[str]
    medicines: List[Medicine]
    advice: str
    created_at: datetime
