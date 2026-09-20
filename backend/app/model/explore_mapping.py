import pandas as pd
import os

data_dir = os.path.join(os.path.dirname(__file__), "raw_data")

severity_df = pd.read_csv(os.path.join(data_dir, "Symptom-severity.csv"))
dataset_df = pd.read_csv(os.path.join(data_dir, "dataset.csv"))

# All 133 symptom names from the severity file
all_symptoms = severity_df["Symptom"].str.strip().tolist()

print("=" * 60)
print(f"All {len(all_symptoms)} symptoms in Symptom-severity.csv:")
print("=" * 60)
for s in sorted(all_symptoms):
    print(f"  {s}")

# Our app's symptom fields and their values
our_main_symptoms = ["fever", "cough", "stomach_pain", "headache"]
our_additional = ["breathlessness", "vomiting", "weakness", "none"]

all_symptoms_lower = [s.lower() for s in all_symptoms]


def find_matches(term):
    # exact match first, then partial
    exact = [s for s in all_symptoms if s.lower() == term.lower()]
    partial = [s for s in all_symptoms if term.lower() in s.lower() and s not in exact]
    return exact, partial


print("\n" + "=" * 60)
print("Mapping: our main_symptom values → dataset symptoms")
print("=" * 60)
for term in our_main_symptoms:
    exact, partial = find_matches(term)
    print(f"\n  '{term}'")
    print(f"    Exact matches : {exact if exact else 'none'}")
    print(f"    Partial matches: {partial if partial else 'none'}")

print("\n" + "=" * 60)
print("Mapping: our additional_symptoms values → dataset symptoms")
print("=" * 60)
for term in our_additional:
    exact, partial = find_matches(term)
    print(f"\n  '{term}'")
    print(f"    Exact matches : {exact if exact else 'none'}")
    print(f"    Partial matches: {partial if partial else 'none'}")

# Also show which diseases appear in the dataset, useful context
print("\n" + "=" * 60)
print(f"Diseases in dataset.csv ({dataset_df['Disease'].nunique()} unique):")
print("=" * 60)
for d in sorted(dataset_df["Disease"].unique()):
    print(f"  {d}")
