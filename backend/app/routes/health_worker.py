from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime
from app.models.health_worker import PatientRecord, SyncRequest
from app.utils.auth import require_role
from app.utils.serializer import fmt
from app.database import get_db

router = APIRouter(prefix="/health-worker", tags=["Health Worker"])


@router.post("/patients", status_code=201)
async def register_patient(data: PatientRecord, user=Depends(require_role("health_worker"))):
    db = get_db()
    doc = data.model_dump()
    doc["health_worker_id"] = user["sub"]
    doc["health_worker_name"] = user["name"]
    doc["synced"] = False
    doc["created_at"] = datetime.utcnow()
    result = await db.hw_patients.insert_one(doc)
    return {"message": "Patient registered", "id": str(result.inserted_id)}


@router.get("/patients")
async def list_patients(user=Depends(require_role("health_worker"))):
    db = get_db()
    patients = await db.hw_patients.find(
        {"health_worker_id": user["sub"]}
    ).sort("created_at", -1).to_list(100)
    return [fmt(p) for p in patients]


@router.get("/patients/{patient_id}")
async def get_patient(patient_id: str, user=Depends(require_role("health_worker"))):
    db = get_db()
    p = await db.hw_patients.find_one({
        "_id": ObjectId(patient_id),
        "health_worker_id": user["sub"]
    })
    if not p:
        raise HTTPException(404, "Patient not found")
    return fmt(p)


@router.post("/sync")
async def sync_records(data: SyncRequest, user=Depends(require_role("health_worker"))):
    db = get_db()
    ids = [ObjectId(rid) for rid in data.record_ids]
    result = await db.hw_patients.update_many(
        {"_id": {"$in": ids}, "health_worker_id": user["sub"]},
        {"$set": {"synced": True, "synced_at": datetime.utcnow()}}
    )
    return {"message": f"{result.modified_count} records synced", "synced_count": result.modified_count}


@router.get("/sync/pending")
async def pending_sync(user=Depends(require_role("health_worker"))):
    db = get_db()
    count = await db.hw_patients.count_documents({"health_worker_id": user["sub"], "synced": False})
    return {"pending_count": count}


@router.get("/stats")
async def worker_stats(user=Depends(require_role("health_worker"))):
    db = get_db()
    total = await db.hw_patients.count_documents({"health_worker_id": user["sub"]})
    pending = await db.hw_patients.count_documents({"health_worker_id": user["sub"], "synced": False})
    return {"total_patients": total, "pending_sync": pending}
