from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId
from app.utils.serializer import fmt
from app.database import get_db

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("/")
async def list_doctors(specialization: str = Query(None)):
    db = get_db()
    query = {"role": "doctor"}
    if specialization:
        query["specialization"] = {"$regex": specialization, "$options": "i"}
    doctors = await db.users.find(query).to_list(100)
    result = []
    for d in doctors:
        d.pop("password", None)
        result.append(fmt(d))
    return result


@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str):
    db = get_db()
    doc = await db.users.find_one({"_id": ObjectId(doctor_id), "role": "doctor"})
    if not doc:
        raise HTTPException(404, "Doctor not found")
    doc.pop("password", None)
    return fmt(doc)


@router.get("/{doctor_id}/slots")
async def get_slots(doctor_id: str, date: str = Query(...)):
    db = get_db()
    booked = await db.appointments.find(
        {"doctor_id": doctor_id, "slot_date": date, "status": {"$ne": "cancelled"}}
    ).to_list(100)
    booked_times = {a["slot_time"] for a in booked}
    all_slots = [
        "9:00 AM", "10:00 AM", "11:00 AM", "11:30 AM",
        "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM"
    ]
    return [{"time": s, "available": s not in booked_times} for s in all_slots]
