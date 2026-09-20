import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os
import numpy as np

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "training_data.csv"))

features = [c for c in df.columns if c != "disease"]
target = "disease"

label_encoder = LabelEncoder()
df[target] = label_encoder.fit_transform(df[target])

X = df[features]
y = df[target]

# duplicate symptom patterns in the underlying dataset caused data leakage with a normal random split.
groups = df[features].apply(tuple, axis=1)

gkf = GroupKFold(n_splits=5)
fold_accuracies = []
tested_classes = set()

print("Running 5-fold GroupKFold Cross-Validation...")
for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups=groups), 1):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    tested_classes.update(y_test.unique())
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    fold_accuracies.append(acc)
    
    print(f"Fold {fold}: Accuracy = {acc:.4f} (Train rows: {len(train_idx)}, Test rows: {len(test_idx)})")

print(f"\nAverage Accuracy: {np.mean(fold_accuracies):.4f}")
print(f"Total disease classes with test coverage in at least one fold: {len(tested_classes)} / {len(label_encoder.classes_)}\n")

print("Training final model on all data...")
final_model = RandomForestClassifier(n_estimators=100, random_state=42)
final_model.fit(X, y)

model_dir = os.path.dirname(__file__)
joblib.dump(final_model, os.path.join(model_dir, "symptom_model.pkl"))
joblib.dump(label_encoder, os.path.join(model_dir, "label_encoder.pkl"))

print("Saved: symptom_model.pkl, label_encoder.pkl")
