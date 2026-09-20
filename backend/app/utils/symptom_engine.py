"""
Rule-based AI symptom analysis engine.
Maps symptom combinations to likely diagnoses and priority levels.
"""

DIAGNOSIS_RULES = [
    {
        "conditions": {
            "main_symptom": "fever",
            "additional_symptoms": "breathlessness",
            "severity": "severe",
        },
        "diagnosis": "Possible Pneumonia / Severe Respiratory Infection",
        "priority": "emergency",
        "advice": "Seek immediate medical attention. Visit nearest PHC or hospital right away.",
    },
    {
        "conditions": {
            "main_symptom": "fever",
            "known_conditions": "diabetes",
        },
        "diagnosis": "Viral Fever with Diabetic Risk",
        "priority": "high",
        "advice": "Monitor blood sugar closely. Consult doctor immediately. Stay hydrated.",
    },
    {
        "conditions": {
            "main_symptom": "fever",
            "additional_symptoms": "breathlessness",
        },
        "diagnosis": "Viral Fever with Respiratory Symptoms",
        "priority": "high",
        "advice": "Rest and stay hydrated. If breathing worsens, visit PHC immediately.",
    },
    {
        "conditions": {
            "main_symptom": "fever",
            "duration": "more_than_week",
        },
        "diagnosis": "Prolonged Fever — Possible Typhoid / Malaria",
        "priority": "high",
        "advice": "Get blood tests done. Avoid self-medication. Consult doctor urgently.",
    },
    {
        "conditions": {
            "main_symptom": "fever",
            "severity": "moderate",
        },
        "diagnosis": "Viral Fever with Respiratory Symptoms",
        "priority": "moderate",
        "advice": "Rest for 3-4 days. Drink ORS and fluids. Take Paracetamol if needed.",
    },
    {
        "conditions": {
            "main_symptom": "cough",
            "duration": "more_than_week",
            "known_conditions": "asthma",
        },
        "diagnosis": "Asthma Exacerbation / Chronic Cough",
        "priority": "high",
        "advice": "Use your inhaler. Avoid dust and cold air. Consult doctor immediately.",
    },
    {
        "conditions": {
            "main_symptom": "cough",
            "additional_symptoms": "breathlessness",
        },
        "diagnosis": "Respiratory Infection with Breathlessness",
        "priority": "high",
        "advice": "Avoid cold air. Rest well. Visit doctor if breathing difficulty increases.",
    },
    {
        "conditions": {
            "main_symptom": "cough",
            "duration": "more_than_week",
        },
        "diagnosis": "Chronic Cough — Possible TB Screening Needed",
        "priority": "moderate",
        "advice": "Get TB screening done at nearest PHC. Avoid smoking. Stay hydrated.",
    },
    {
        "conditions": {
            "main_symptom": "stomach_pain",
            "additional_symptoms": "vomiting",
            "severity": "severe",
        },
        "diagnosis": "Acute Gastroenteritis / Possible Appendicitis",
        "priority": "emergency",
        "advice": "Visit hospital immediately. Do not eat anything. Stay hydrated with ORS.",
    },
    {
        "conditions": {
            "main_symptom": "stomach_pain",
            "additional_symptoms": "vomiting",
        },
        "diagnosis": "Gastroenteritis / Food Poisoning",
        "priority": "moderate",
        "advice": "Take ORS frequently. Avoid solid food for 6 hours. Rest well.",
    },
    {
        "conditions": {
            "main_symptom": "stomach_pain",
            "known_conditions": "diabetes",
        },
        "diagnosis": "Abdominal Pain with Diabetic Risk",
        "priority": "high",
        "advice": "Check blood sugar. Consult doctor. Avoid spicy food.",
    },
    {
        "conditions": {
            "main_symptom": "headache",
            "known_conditions": "hypertension",
            "severity": "severe",
        },
        "diagnosis": "Hypertensive Headache — Possible BP Crisis",
        "priority": "emergency",
        "advice": "Check BP immediately. Visit hospital if BP is very high. Take prescribed BP medicine.",
    },
    {
        "conditions": {
            "main_symptom": "headache",
            "known_conditions": "hypertension",
        },
        "diagnosis": "Headache with Hypertension",
        "priority": "high",
        "advice": "Monitor BP. Take prescribed medication. Avoid stress and salt.",
    },
    {
        "conditions": {
            "main_symptom": "headache",
            "severity": "severe",
        },
        "diagnosis": "Severe Headache — Migraine / Tension Headache",
        "priority": "moderate",
        "advice": "Rest in a dark quiet room. Stay hydrated. Consult doctor if recurring.",
    },
]

# Default fallback rules per main symptom
DEFAULTS = {
    "fever": {
        "diagnosis": "Mild Viral Fever",
        "priority": "low",
        "advice": "Rest well, drink plenty of fluids. Take Paracetamol if needed. Monitor temperature.",
    },
    "cough": {
        "diagnosis": "Common Cold / Mild Cough",
        "priority": "low",
        "advice": "Stay warm, drink warm water with honey. Avoid cold drinks.",
    },
    "stomach_pain": {
        "diagnosis": "Mild Indigestion / Gastric Issue",
        "priority": "low",
        "advice": "Avoid spicy food. Drink warm water. Take antacid if needed.",
    },
    "headache": {
        "diagnosis": "Tension Headache",
        "priority": "low",
        "advice": "Rest, stay hydrated, avoid screen time. Take Paracetamol if needed.",
    },
}

PRIORITY_LABELS = {
    "low": "✅ Low Priority",
    "moderate": "⚠ Moderate Priority",
    "high": "🔴 High Priority",
    "emergency": "🚨 Emergency — Seek Immediate Care",
}


def analyze_symptoms(data: dict) -> dict:
    """
    Match symptom data against rules (most specific first).
    Returns diagnosis, priority, advice.
    """
    best_match = None
    best_score = 0

    for rule in DIAGNOSIS_RULES:
        score = 0
        matched = True
        for key, val in rule["conditions"].items():
            if data.get(key) == val:
                score += 1
            else:
                matched = False
                break
        if matched and score > best_score:
            best_score = score
            best_match = rule

    if best_match:
        return {
            "diagnosis": best_match["diagnosis"],
            "priority": best_match["priority"],
            "priority_label": PRIORITY_LABELS[best_match["priority"]],
            "advice": best_match["advice"],
        }

    # Fallback to default for main symptom
    default = DEFAULTS.get(data.get("main_symptom", "fever"), DEFAULTS["fever"])
    return {
        "diagnosis": default["diagnosis"],
        "priority": default["priority"],
        "priority_label": PRIORITY_LABELS[default["priority"]],
        "advice": default["advice"],
    }
