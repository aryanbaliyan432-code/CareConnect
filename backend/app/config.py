import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "careconnect")
JWT_SECRET = os.getenv("JWT_SECRET", "careconnect_secret")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", 24))
PORT = int(os.getenv("PORT", 8000))
