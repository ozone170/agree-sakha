# backend/train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "crop_dataset.csv")  # put your dataset here
MODEL_OUT = os.path.join(BASE_DIR, "crop_model.pkl")
LE_OUT = os.path.join(BASE_DIR, "label_encoder.pkl")

def load_and_prepare(csv_path):
    df = pd.read_csv(csv_path)
    # Expected columns: Nitrogen_N, phosphorus_P, Potassium_K, pH, Temperature, Humidity, Rainfall(cm), Crops
    required = ["Nitrogen_N","phosphorus_P","Potassium_K","pH","Temperature","Humidity","Rainfall(cm)","Crops"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")
    X = df[["Nitrogen_N","phosphorus_P","Potassium_K","pH","Temperature","Humidity","Rainfall(cm)"]].values
    y = df["Crops"].values
    return X, y

def train_and_save():
    X, y = load_and_prepare(CSV_PATH)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f"Test Accuracy: {acc:.4f}")

    joblib.dump(model, MODEL_OUT)
    joblib.dump(le, LE_OUT)
    print(f"Saved model -> {MODEL_OUT} and encoder -> {LE_OUT}")

if __name__ == "__main__":
    train_and_save()
