from fastapi import APIRouter, Depends
from bson import ObjectId
from datetime import datetime
from app.models.symptom import SymptomSubmit, SymptomResult
from app.utils.auth import get_current_user
from app.utils.symptom_engine import analyze_symptoms
from app.utils.serializer import fmt
from app.database import get_db
import uuid

router = APIRouter(prefix="/symptoms", tags=["AI Symptom Check"])


READABLE = {
    "main_symptom": {
        "fever": "Fever / बुखार",
        "cough": "Cough / खांसी",
        "stomach_pain": "Stomach Pain / पेट दर्द",
        "headache": "Headache / सिरदर्द",
    },
    "duration": {
        "less_than_1_day": "Less than 1 day",
        "1_3_days": "1–3 days",
        "4_7_days": "4–7 days",
        "more_than_week": "More than a week",
    },
    "severity": {
        "mild": "Mild — I can manage",
        "moderate": "Moderate — affecting daily activities",
        "severe": "Severe — need help immediately",
    },
    "additional_symptoms": {
        "breathlessness": "Breathlessness / सांस लेने में दिक्कत",
        "vomiting": "Vomiting / उल्टी",
        "weakness": "Weakness / कमजोरी",
        "none": "None of the above",
    },
    "known_conditions": {
        "diabetes": "Diabetes / मधुमेह",
        "hypertension": "Hypertension / उच्च रक्तचाप",
        "asthma": "Asthma / दमा",
        "none": "No known conditions",
    },
}


@router.post("/analyze", response_model=SymptomResult)
async def analyze(data: SymptomSubmit, user=Depends(get_current_user)):
    db = get_db()
    raw = data.model_dump()
    result = analyze_symptoms(raw)
    assessment_id = str(uuid.uuid4())[:8].upper()

    # Store human-readable answers
    readable_answers = {
        "Q1 - Main Symptom":      READABLE["main_symptom"].get(raw["main_symptom"], raw["main_symptom"]),
        "Q2 - Duration":          READABLE["duration"].get(raw["duration"], raw["duration"]),
        "Q3 - Severity":          READABLE["severity"].get(raw["severity"], raw["severity"]),
        "Q4 - Additional Symptoms": READABLE["additional_symptoms"].get(raw["additional_symptoms"], raw["additional_symptoms"]),
        "Q5 - Known Conditions":  READABLE["known_conditions"].get(raw["known_conditions"], raw["known_conditions"]),
    }

    doc = {
        "assessment_id": assessment_id,
        "patient_id": user["sub"],
        "patient_name": user["name"],
        "appointment_id": data.appointment_id,
        "answers": readable_answers,
        "raw_inputs": raw,
        "result": result,
        "created_at": datetime.utcnow(),
    }
    await db.symptom_assessments.insert_one(doc)

    if data.appointment_id:
        await db.appointments.update_one(
            {"_id": ObjectId(data.appointment_id)},
            {"$set": {"symptom_assessment": result, "assessment_id": assessment_id}}
        )

    return SymptomResult(
        likely_diagnosis=result["diagnosis"],
        priority=result["priority"],
        priority_label=result["priority_label"],
        advice=result["advice"],
        sent_to_doctor=bool(data.appointment_id),
        assessment_id=assessment_id,
    )


@router.get("/my")
async def my_assessments(user=Depends(get_current_user)):
    db = get_db()
    records = await db.symptom_assessments.find(
        {"patient_id": user["sub"]}
    ).sort("created_at", -1).to_list(20)
    return [fmt(r) for r in records]
