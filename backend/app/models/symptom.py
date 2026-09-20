from pydantic import BaseModel
from typing import Optional, Literal


class SymptomSubmit(BaseModel):
    main_symptom: Literal["fever", "cough", "stomach_pain", "headache"]
    duration: Literal["less_than_1_day", "1_3_days", "4_7_days", "more_than_week"]
    severity: Literal["mild", "moderate", "severe"]
    additional_symptoms: Literal["breathlessness", "vomiting", "weakness", "none"]
    known_conditions: Literal["diabetes", "hypertension", "asthma", "none"]
    appointment_id: Optional[str] = None


class SymptomResult(BaseModel):
    likely_diagnosis: str
    priority: Literal["low", "moderate", "high", "emergency"]
    priority_label: str
    advice: str
    sent_to_doctor: bool
    assessment_id: str
