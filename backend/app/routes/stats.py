from fastapi import APIRouter
from app.database import get_db

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/")
async def platform_stats():
    """Public stats shown on the home screen."""
    db = get_db()
    consultations = await db.appointments.count_documents({"status": "completed"})
    doctors = await db.users.count_documents({"role": "doctor"})
    villages = await db.hw_patients.distinct("village")

    return {
        "consultations": consultations,
        "doctors": doctors,
        "villages": len(villages),
    }
