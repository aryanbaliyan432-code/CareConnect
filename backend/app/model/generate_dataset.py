import random
import csv
import os

# All possible values for each field
main_symptoms = ["fever", "cough", "stomach_pain", "headache"]
durations = ["less_than_1_day", "1_3_days", "4_7_days", "more_than_week"]
severities = ["mild", "moderate", "severe"]
additional_symptoms_opts = ["breathlessness", "vomiting", "weakness", "none"]
known_conditions_opts = ["diabetes", "hypertension", "asthma", "none"]

# Same rule logic as symptom_engine.py, just priority labels extracted
DIAGNOSIS_RULES = [
    {"conditions": {"main_symptom": "fever", "additional_symptoms": "breathlessness", "severity": "severe"}, "priority": "emergency"},
    {"conditions": {"main_symptom": "fever", "known_conditions": "diabetes"}, "priority": "high"},
    {"conditions": {"main_symptom": "fever", "additional_symptoms": "breathlessness"}, "priority": "high"},
    {"conditions": {"main_symptom": "fever", "duration": "more_than_week"}, "priority": "high"},
    {"conditions": {"main_symptom": "fever", "severity": "moderate"}, "priority": "moderate"},
    {"conditions": {"main_symptom": "cough", "duration": "more_than_week", "known_conditions": "asthma"}, "priority": "high"},
    {"conditions": {"main_symptom": "cough", "additional_symptoms": "breathlessness"}, "priority": "high"},
    {"conditions": {"main_symptom": "cough", "duration": "more_than_week"}, "priority": "moderate"},
    {"conditions": {"main_symptom": "stomach_pain", "additional_symptoms": "vomiting", "severity": "severe"}, "priority": "emergency"},
    {"conditions": {"main_symptom": "stomach_pain", "additional_symptoms": "vomiting"}, "priority": "moderate"},
    {"conditions": {"main_symptom": "stomach_pain", "known_conditions": "diabetes"}, "priority": "high"},
    {"conditions": {"main_symptom": "headache", "known_conditions": "hypertension", "severity": "severe"}, "priority": "emergency"},
    {"conditions": {"main_symptom": "headache", "known_conditions": "hypertension"}, "priority": "high"},
    {"conditions": {"main_symptom": "headache", "severity": "severe"}, "priority": "moderate"},
]

DEFAULTS = {
    "fever": "low",
    "cough": "low",
    "stomach_pain": "low",
    "headache": "low",
}


def get_priority(row):
    best_match = None
    best_score = 0
    for rule in DIAGNOSIS_RULES:
        score = 0
        matched = True
        for key, val in rule["conditions"].items():
            if row[key] == val:
                score += 1
            else:
                matched = False
                break
        if matched and score > best_score:
            best_score = score
            best_match = rule
    if best_match:
        return best_match["priority"]
    return DEFAULTS[row["main_symptom"]]


all_priorities = ["low", "moderate", "high", "emergency"]

# Down-weight severe to keep emergency combos rare (~5%)
severity_weights = [0.45, 0.40, 0.15]  # mild, moderate, severe

rows = []
for _ in range(3000):
    row = {
        "main_symptom": random.choice(main_symptoms),
        "duration": random.choice(durations),
        "severity": random.choices(severities, weights=severity_weights)[0],
        "additional_symptoms": random.choice(additional_symptoms_opts),
        "known_conditions": random.choice(known_conditions_opts),
    }
    row["priority"] = get_priority(row)
    rows.append(row)

# Flip ~6% of labels to simulate noise, but only ~1% for emergency
# (real data wouldn't mislabel true emergencies nearly as often)
noise_alternatives = {
    "low": ["moderate", "high"],
    "moderate": ["low", "high"],
    "high": ["moderate", "emergency"],
    "emergency": ["high"],
}
for row in rows:
    flip_rate = 0.01 if row["priority"] == "emergency" else 0.06
    if random.random() < flip_rate:
        row["priority"] = random.choice(noise_alternatives[row["priority"]])

# Print class balance check
counts = {}
for row in rows:
    counts[row["priority"]] = counts.get(row["priority"], 0) + 1
total = len(rows)
print("Class distribution:")
for p in all_priorities:
    n = counts.get(p, 0)
    print(f"  {p}: {n} ({100 * n / total:.1f}%)")

out_path = os.path.join(os.path.dirname(__file__), "symptom_dataset.csv")
with open(out_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["main_symptom", "duration", "severity", "additional_symptoms", "known_conditions", "priority"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {total} rows to symptom_dataset.csv")
