import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import json
import os

# Create sample data for crop prediction
np.random.seed(42)
n_samples = 1000

# Generate synthetic soil data
data = {
    'N': np.random.uniform(0, 140, n_samples),
    'P': np.random.uniform(0, 145, n_samples),
    'K': np.random.uniform(0, 205, n_samples),
    'temperature': np.random.uniform(8, 43, n_samples),
    'humidity': np.random.uniform(14, 99, n_samples),
    'ph': np.random.uniform(3.5, 9.9, n_samples),
    'rainfall': np.random.uniform(20, 298, n_samples)
}

# Define crops and their typical ranges
crops = ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate', 'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee']

# Create labels based on typical crop conditions
def assign_crop(row):
    if row['temperature'] > 30 and row['humidity'] > 60:
        return np.random.choice(['rice', 'banana', 'coconut', 'papaya'])
    elif row['temperature'] > 25 and row['rainfall'] > 100:
        return np.random.choice(['maize', 'mango', 'orange'])
    elif row['N'] > 80 and row['P'] > 60:
        return np.random.choice(['chickpea', 'kidneybeans', 'pigeonpeas'])
    elif row['ph'] < 6.5 and row['rainfall'] < 100:
        return np.random.choice(['mothbeans', 'mungbean', 'blackgram', 'lentil'])
    elif row['temperature'] < 25 and row['rainfall'] > 150:
        return np.random.choice(['apple', 'grapes', 'pomegranate'])
    else:
        return np.random.choice(['watermelon', 'muskmelon', 'cotton', 'jute', 'coffee'])

df = pd.DataFrame(data)
df['crop'] = df.apply(assign_crop, axis=1)

# Train model
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['crop']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Label encoder
encoder = LabelEncoder()
encoder.fit(y)

# Save model and encoder
os.makedirs('backend', exist_ok=True)
joblib.dump(model, 'backend/crop_model.pkl')
joblib.dump(encoder, 'backend/label_encoder.pkl')

print('Model and encoder saved successfully')
