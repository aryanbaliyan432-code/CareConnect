from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.user import UserRegister, UserLogin
from app.utils.auth import hash_password, verify_password, create_token
from app.utils.serializer import fmt
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(data: UserRegister):
    db = get_db()
    existing = await db.users.find_one({"phone": data.phone, "role": data.role})
    if existing:
        raise HTTPException(status_code=400, detail="Phone already registered. Please login instead.")

    doc = data.model_dump()
    doc["password"] = hash_password(data.password)
    doc["created_at"] = datetime.utcnow()

    result = await db.users.insert_one(doc)
    return {"message": "Registered successfully", "id": str(result.inserted_id)}


@router.post("/login")
async def login(data: UserLogin):
    db = get_db()
    user = await db.users.find_one({"phone": data.phone, "role": data.role})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": str(user["_id"]),
        "name": user["name"],
        "role": user["role"],
        "phone": user["phone"],
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "role": user["role"],
            "phone": user["phone"],
            "village": user.get("village"),
            "district": user.get("district"),
            "specialization": user.get("specialization"),
            "hospital": user.get("hospital"),
            "fee": user.get("fee"),
            "block": user.get("block"),
        }
    }


@router.delete("/clear-dev")
async def clear_dev_users():
    db = get_db()
    result = await db.users.delete_many({})
    return {"deleted": result.deleted_count}
