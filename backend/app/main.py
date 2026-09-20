from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from app.database import connect_db, close_db
from app.routes import auth, doctors, appointments, symptoms, prescriptions, health_worker, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="CareConnect API",
    description="Backend API for CareConnect — Connected Telehealth Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend HTML file
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "CARE_CONNECT.html")
if not os.path.exists(FRONTEND_PATH):
    FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "gramseva_teleclinic (2).html")

@app.get("/app", include_in_schema=False)
async def serve_frontend():
    return FileResponse(os.path.abspath(FRONTEND_PATH))

app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(symptoms.router)
app.include_router(prescriptions.router)
app.include_router(health_worker.router)
app.include_router(stats.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "CareConnect API is running"}
