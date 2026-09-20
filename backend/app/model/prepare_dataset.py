import pandas as pd
import os

data_dir = os.path.join(os.path.dirname(__file__), "raw_data")

dataset = pd.read_csv(os.path.join(data_dir, "dataset.csv"))

# Strip whitespace from all string columns
dataset = dataset.map(lambda x: x.strip() if isinstance(x, str) else x)

# Symptoms a patient can reasonably self-report (no tests needed)
mapped_symptoms = [
    "cough", "high_fever", "mild_fever", "headache", "stomach_pain",
    "vomiting", "breathlessness", "fatigue", "chills", "joint_pain",
    "nausea", "diarrhoea", "skin_rash", "chest_pain", "dizziness",
    "weight_loss", "muscle_pain", "throat_irritation", "runny_nose", "loss_of_appetite",
]

symptom_cols = [c for c in dataset.columns if c.startswith("Symptom_")]

# Build binary columns: 1 if that symptom appears in any of the Symptom_1..17 columns
rows = []
for _, row in dataset.iterrows():
    present = set(str(v).strip().lower() for v in row[symptom_cols] if pd.notna(v) and str(v).strip() != "")
    entry = {"disease": row["Disease"]}
    for s in mapped_symptoms:
        entry[s] = 1 if s in present else 0
    rows.append(entry)

df = pd.DataFrame(rows)

# Drop rows where none of our mapped symptoms are present (useless for our model)
has_any = df[mapped_symptoms].sum(axis=1) > 0
df = df[has_any].reset_index(drop=True)

print(f"Rows after filtering: {len(df)} (dropped {has_any.shape[0] - len(df)} rows with no mapped symptoms)\n")

print("Disease class distribution:")
counts = df["disease"].value_counts()
for disease, count in counts.items():
    print(f"  {disease}: {count}")

out_path = os.path.join(os.path.dirname(__file__), "training_data.csv")
df.to_csv(out_path, index=False)
print(f"\nSaved {len(df)} rows to training_data.csv")
