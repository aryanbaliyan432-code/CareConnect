from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime
from app.models.appointment import AppointmentCreate
from app.utils.auth import get_current_user, require_role
from app.utils.serializer import fmt
from app.database import get_db

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", status_code=201)
async def book_appointment(
    data: AppointmentCreate,
    user=Depends(require_role("patient", "health_worker"))
):
    db = get_db()

    conflict = await db.appointments.find_one({
        "doctor_id": data.doctor_id,
        "slot_date": data.slot_date,
        "slot_time": data.slot_time,
        "status": {"$ne": "cancelled"}
    })
    if conflict:
        raise HTTPException(400, "This slot is already booked")

    doctor = await db.users.find_one({"_id": ObjectId(data.doctor_id)})
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    doc = {
        "doctor_id": data.doctor_id,
        "doctor_name": doctor["name"],
        "doctor_specialization": doctor.get("specialization", ""),
        "patient_id": user["sub"],
        "patient_name": data.patient_name,
        "patient_village": data.patient_village,
        "patient_age": data.patient_age,
        "slot_time": data.slot_time,
        "slot_date": data.slot_date,
        "consult_type": data.consult_type,
        "status": "scheduled",
        "fee": doctor.get("fee", 150),
        "created_at": datetime.utcnow(),
    }
    result = await db.appointments.insert_one(doc)
    doc["_id"] = result.inserted_id
    return {"message": "Appointment booked", "appointment": fmt(doc)}


@router.get("/my")
async def my_appointments(user=Depends(get_current_user)):
    db = get_db()
    role = user["role"]
    if role == "doctor":
        query = {"doctor_id": user["sub"]}
    else:
        query = {"patient_id": user["sub"]}
    appts = await db.appointments.find(query).sort("slot_date", 1).to_list(50)
    return [fmt(a) for a in appts]


@router.get("/doctor/queue")
async def doctor_queue(user=Depends(require_role("doctor"))):
    db = get_db()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    appts = await db.appointments.find(
        {"doctor_id": user["sub"], "slot_date": today}
    ).sort("slot_time", 1).to_list(50)
    return [fmt(a) for a in appts]


@router.patch("/{appt_id}/status")
async def update_status(appt_id: str, status: str, user=Depends(require_role("doctor"))):
    db = get_db()
    await db.appointments.update_one(
        {"_id": ObjectId(appt_id)},
        {"$set": {"status": status}}
    )
    return {"message": "Status updated"}


@router.delete("/{appt_id}")
async def cancel_appointment(appt_id: str, user=Depends(require_role("patient"))):
    db = get_db()
    await db.appointments.update_one(
        {"_id": ObjectId(appt_id), "patient_id": user["sub"]},
        {"$set": {"status": "cancelled"}}
    )
    return {"message": "Appointment cancelled"}
