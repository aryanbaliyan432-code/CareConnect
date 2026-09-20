from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime
from app.models.prescription import PrescriptionCreate
from app.utils.auth import get_current_user, require_role
from app.utils.serializer import fmt
from app.database import get_db

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


def _rx_number(dt: datetime) -> str:
    return f"GST-{dt.strftime('%Y%m%d')}-{str(dt.microsecond)[:3].zfill(3)}"


@router.post("/", status_code=201)
async def create_prescription(data: PrescriptionCreate, user=Depends(require_role("doctor"))):
    db = get_db()
    appt = await db.appointments.find_one({"_id": ObjectId(data.appointment_id)})
    if not appt:
        raise HTTPException(404, "Appointment not found")

    doctor = await db.users.find_one({"_id": ObjectId(user["sub"])})
    now = datetime.utcnow()
    doc = {
        "rx_number": _rx_number(now),
        "appointment_id": data.appointment_id,
        "patient_id": data.patient_id,
        "patient_name": appt["patient_name"],
        "patient_age": appt["patient_age"],
        "patient_village": appt["patient_village"],
        "doctor_id": user["sub"],
        "doctor_name": user["name"],
        "doctor_registration": doctor.get("registration_no") if doctor else None,
        "medicines": [m.model_dump() for m in data.medicines],
        "advice": data.advice,
        "created_at": now,
    }
    result = await db.prescriptions.insert_one(doc)
    doc["_id"] = result.inserted_id
    await db.appointments.update_one(
        {"_id": ObjectId(data.appointment_id)},
        {"$set": {"status": "completed"}}
    )
    return {"message": "Prescription created", "prescription": fmt(doc)}


@router.get("/my")
async def my_prescriptions(user=Depends(require_role("patient"))):
    db = get_db()
    rxs = await db.prescriptions.find({"patient_id": user["sub"]}).sort("created_at", -1).to_list(20)
    return [fmt(r) for r in rxs]


@router.get("/{rx_id}")
async def get_prescription(rx_id: str, user=Depends(get_current_user)):
    db = get_db()
    rx = await db.prescriptions.find_one({"_id": ObjectId(rx_id)})
    if not rx:
        raise HTTPException(404, "Prescription not found")
    return fmt(rx)


@router.get("/appointment/{appt_id}")
async def prescription_by_appointment(appt_id: str, user=Depends(get_current_user)):
    db = get_db()
    rx = await db.prescriptions.find_one({"appointment_id": appt_id})
    if not rx:
        raise HTTPException(404, "No prescription for this appointment")
    return fmt(rx)
