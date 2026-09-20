# CareConnect — Backend

FastAPI + MongoDB backend for the CareConnect frontend.

## Setup

### 1. Install Python
Download from https://python.org (3.11+ recommended). Make sure to check "Add to PATH".

### 2. Install MongoDB
- **Local:** Download from https://www.mongodb.com/try/download/community
- **Atlas (cloud):** Update `MONGO_URI` in `.env` with your Atlas connection string

### 3. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment
Edit `.env` if needed:
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=careconnect
JWT_SECRET=careconnect_super_secret_key_change_in_production
JWT_EXPIRE_HOURS=24
PORT=8000
```

### 5. Run the server
```bash
cd backend
python run.py
```

Server starts at: http://localhost:8000  
API docs at: http://localhost:8000/docs

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/register | Register patient/doctor/health_worker |
| POST | /auth/login | Login and get JWT token |
| GET | /doctors/ | List doctors (filter by specialization) |
| GET | /doctors/{id}/slots | Available time slots |
| POST | /appointments/ | Book appointment |
| GET | /appointments/my | My appointments |
| GET | /appointments/doctor/queue | Doctor's today queue |
| POST | /symptoms/analyze | AI symptom analysis |
| POST | /prescriptions/ | Create prescription (doctor only) |
| GET | /prescriptions/my | Patient's prescriptions |
| POST | /health-worker/patients | Register patient offline |
| POST | /health-worker/sync | Sync offline records |
| GET | /stats/ | Platform stats |

---

## MongoDB Collections

- `users` — patients, doctors, health workers
- `appointments` — all bookings
- `symptom_assessments` — AI symptom results
- `prescriptions` — digital prescriptions
- `hw_patients` — health worker offline patient records
