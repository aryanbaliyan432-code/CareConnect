"""
Seed script — populates MongoDB with sample data for all 3 roles.
Run: python seed_data.py  (from the backend folder)
"""
import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI, DB_NAME
from app.utils.auth import hash_password

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


async def seed():
    print("Clearing old data...")
    await db.users.delete_many({})
    await db.appointments.delete_many({})
    await db.symptom_assessments.delete_many({})
    await db.prescriptions.delete_many({})
    await db.hw_patients.delete_many({})

    # ── USERS ──
    print("Seeding users...")
    users = [
        # Patients
        {
            "name": "Ramesh Kumar",
            "phone": "9876543210",
            "password": hash_password("pass123"),
            "role": "patient",
            "village": "Rampur",
            "district": "Sultanpur",
            "created_at": datetime.utcnow(),
        },
        {
            "name": "Sunita Devi",
            "phone": "9876543211",
            "password": hash_password("pass123"),
            "role": "patient",
            "village": "Khajuriyapur",
            "district": "Sultanpur",
            "created_at": datetime.utcnow(),
        },
        {
            "name": "Mohan Lal",
            "phone": "9876543212",
            "password": hash_password("pass123"),
            "role": "patient",
            "village": "Raipur",
            "district": "Sultanpur",
            "created_at": datetime.utcnow(),
        },
        # Doctors
        {
            "name": "Dr. Priya Sharma",
            "phone": "9000000001",
            "password": hash_password("doc123"),
            "role": "doctor",
            "specialization": "General Medicine",
            "hospital": "KGMU, Lucknow",
            "registration_no": "UP-24-7892",
            "fee": 150,
            "created_at": datetime.utcnow(),
        },
        {
            "name": "Dr. Vikram Singh",
            "phone": "9000000002",
            "password": hash_password("doc123"),
            "role": "doctor",
            "specialization": "Cardiology",
            "hospital": "BHU, Varanasi",
            "registration_no": "UP-18-4421",
            "fee": 200,
            "created_at": datetime.utcnow(),
        },
        {
            "name": "Dr. Rekha Gupta",
            "phone": "9000000003",
            "password": hash_password("doc123"),
            "role": "doctor",
            "specialization": "Pediatrics",
            "hospital": "SGPGI, Lucknow",
            "registration_no": "UP-20-3310",
            "fee": 150,
            "created_at": datetime.utcnow(),
        },
        # Health Worker
        {
            "name": "Seema Yadav",
            "phone": "8000000001",
            "password": hash_password("asha123"),
            "role": "health_worker",
            "block": "Kadipur",
            "district": "Sultanpur",
            "created_at": datetime.utcnow(),
        },
    ]
    result = await db.users.insert_many(users)
    user_ids = result.inserted_ids

    patient1_id = str(user_ids[0])
    patient2_id = str(user_ids[1])
    patient3_id = str(user_ids[2])
    doctor1_id  = str(user_ids[3])
    doctor2_id  = str(user_ids[4])
    hw_id       = str(user_ids[6])

    today = datetime.utcnow().strftime("%Y-%m-%d")
    tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")

    # ── APPOINTMENTS ──
    print("Seeding appointments...")
    appointments = [
        {
            "doctor_id": doctor1_id,
            "doctor_name": "Dr. Priya Sharma",
            "doctor_specialization": "General Medicine",
            "patient_id": patient1_id,
            "patient_name": "Ramesh Kumar",
            "patient_village": "Rampur, Sultanpur",
            "patient_age": 42,
            "slot_time": "3:30 PM",
            "slot_date": today,
            "consult_type": "video",
            "status": "scheduled",
            "fee": 150,
            "created_at": datetime.utcnow(),
        },
        {
            "doctor_id": doctor2_id,
            "doctor_name": "Dr. Vikram Singh",
            "doctor_specialization": "Cardiology",
            "patient_id": patient1_id,
            "patient_name": "Ramesh Kumar",
            "patient_village": "Rampur, Sultanpur",
            "patient_age": 42,
            "slot_time": "11:00 AM",
            "slot_date": tomorrow,
            "consult_type": "chat",
            "status": "scheduled",
            "fee": 200,
            "created_at": datetime.utcnow(),
        },
        {
            "doctor_id": doctor1_id,
            "doctor_name": "Dr. Priya Sharma",
            "doctor_specialization": "General Medicine",
            "patient_id": patient2_id,
            "patient_name": "Sunita Devi",
            "patient_village": "Khajuriyapur, Sultanpur",
            "patient_age": 55,
            "slot_time": "4:00 PM",
            "slot_date": today,
            "consult_type": "video",
            "status": "scheduled",
            "fee": 150,
            "created_at": datetime.utcnow(),
        },
    ]
    appt_result = await db.appointments.insert_many(appointments)
    appt1_id = str(appt_result.inserted_ids[0])

    # ── SYMPTOM ASSESSMENTS ──
    print("Seeding symptom assessments...")
    assessments = [
        {
            "assessment_id": "A1B2C3D4",
            "patient_id": patient1_id,
            "patient_name": "Ramesh Kumar",
            "appointment_id": appt1_id,
            "answers": {
                "Q1 - Main Symptom": "Fever / बुखार",
                "Q2 - Duration": "1–3 days",
                "Q3 - Severity": "Moderate — affecting daily activities",
                "Q4 - Additional Symptoms": "Weakness / कमजोरी",
                "Q5 - Known Conditions": "No known conditions",
            },
            "raw_inputs": {
                "main_symptom": "fever",
                "duration": "1_3_days",
                "severity": "moderate",
                "additional_symptoms": "weakness",
                "known_conditions": "none",
            },
            "result": {
                "diagnosis": "Viral Fever with Respiratory Symptoms",
                "priority": "moderate",
                "priority_label": "⚠ Moderate Priority",
                "advice": "Rest for 3-4 days. Drink ORS and fluids. Take Paracetamol if needed.",
            },
            "created_at": datetime.utcnow(),
        },
        {
            "assessment_id": "E5F6G7H8",
            "patient_id": patient2_id,
            "patient_name": "Sunita Devi",
            "appointment_id": None,
            "answers": {
                "Q1 - Main Symptom": "Headache / सिरदर्द",
                "Q2 - Duration": "4–7 days",
                "Q3 - Severity": "Mild — I can manage",
                "Q4 - Additional Symptoms": "None of the above",
                "Q5 - Known Conditions": "Hypertension / उच्च रक्तचाप",
            },
            "raw_inputs": {
                "main_symptom": "headache",
                "duration": "4_7_days",
                "severity": "mild",
                "additional_symptoms": "none",
                "known_conditions": "hypertension",
            },
            "result": {
                "diagnosis": "Headache with Hypertension",
                "priority": "high",
                "priority_label": "🔴 High Priority",
                "advice": "Monitor BP. Take prescribed medication. Avoid stress and salt.",
            },
            "created_at": datetime.utcnow(),
        },
    ]
    await db.symptom_assessments.insert_many(assessments)

    # ── PRESCRIPTIONS ──
    print("Seeding prescriptions...")
    prescriptions = [
        {
            "rx_number": "GST-20260414-001",
            "appointment_id": appt1_id,
            "patient_id": patient1_id,
            "patient_name": "Ramesh Kumar",
            "patient_age": 42,
            "patient_village": "Rampur, Sultanpur",
            "doctor_id": doctor1_id,
            "doctor_name": "Dr. Priya Sharma",
            "doctor_registration": "UP-24-7892",
            "medicines": [
                {"name": "Paracetamol 500mg", "dosage": "1 tablet", "instructions": "Every 6 hours for 3 days · After food"},
                {"name": "Cetirizine 10mg",   "dosage": "1 tablet", "instructions": "At bedtime for 5 days"},
                {"name": "ORS Sachets",        "dosage": "1 sachet", "instructions": "In 1L water, 2-3 times daily"},
            ],
            "advice": "Rest for 3-4 days. Drink plenty of fluids. If fever crosses 103°F visit nearest PHC.",
            "created_at": datetime.utcnow(),
        }
    ]
    await db.prescriptions.insert_many(prescriptions)

    # ── HEALTH WORKER PATIENTS ──
    print("Seeding health worker patient records...")
    hw_patients = [
        {
            "name": "Ramesh Kumar",
            "age": 42, "gender": "male",
            "village": "Rampur", "phone": "9876543210",
            "chief_complaint": "Fever and cough since 3 days",
            "temperature": "102°F", "blood_pressure": "130/85",
            "spo2": "98%", "weight": "68",
            "health_worker_id": hw_id,
            "health_worker_name": "Seema Yadav",
            "synced": False,
            "created_at": datetime.utcnow(),
        },
        {
            "name": "Sunita Devi",
            "age": 55, "gender": "female",
            "village": "Khajuriyapur", "phone": "9876543211",
            "chief_complaint": "Diabetes follow-up",
            "temperature": "98.6°F", "blood_pressure": "140/90",
            "spo2": "97%", "weight": "62",
            "health_worker_id": hw_id,
            "health_worker_name": "Seema Yadav",
            "synced": False,
            "created_at": datetime.utcnow(),
        },
        {
            "name": "Mohan Lal",
            "age": 60, "gender": "male",
            "village": "Raipur", "phone": "9876543212",
            "chief_complaint": "Hypertension checkup",
            "temperature": "98.4°F", "blood_pressure": "150/95",
            "spo2": "96%", "weight": "75",
            "health_worker_id": hw_id,
            "health_worker_name": "Seema Yadav",
            "synced": True,
            "created_at": datetime.utcnow(),
        },
    ]
    await db.hw_patients.insert_many(hw_patients)

    print("\n✅ Seed complete! Use these credentials:\n")
    print("  PATIENT:       phone=9876543210  password=pass123")
    print("  PATIENT 2:     phone=9876543211  password=pass123")
    print("  DOCTOR:        phone=9000000001  password=doc123")
    print("  HEALTH WORKER: phone=8000000001  password=asha123")

    client.close()


asyncio.run(seed())
