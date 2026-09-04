import pandas as pd
import numpy as np
import joblib

# Load trained model
model = joblib.load("model/random_forest_model.pkl")

# Load feature names used during training
feature_names = joblib.load("model/feature_names.pkl")


def predict_threat(data):
    """
    Takes network traffic data and predicts the threat.
    """

    # Convert input into DataFrame
    df = pd.DataFrame([data])

    # Make sure all required features exist
    for feature in feature_names:
        if feature not in df.columns:
            df[feature] = 0

    # Keep only features used by the model
    df = df[feature_names]

    # Clean data
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)

    # Prediction
    prediction = model.predict(df)[0]

    # Probability/confidence
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities) * 100

    return prediction, confidence


# --------------------------------------------------
# TEST PREDICTION
# --------------------------------------------------

# Use a real row from our dataset
sample = pd.read_csv(
    "dataset/combined.csv",
    nrows=1
)

sample.columns = sample.columns.str.strip()

# Remove our label column
sample = sample.drop(columns=["Attack_Type"], errors="ignore")

# Keep numerical features
sample = sample.select_dtypes(include=[np.number])

# Convert first row to dictionary
sample_data = sample.iloc[0].to_dict()

prediction, confidence = predict_threat(sample_data)

print("\n==============================")
print("   UNIGUARD AI DETECTION")
print("==============================")

print("Threat:", prediction)
print("Confidence:", round(confidence, 2), "%")

if prediction == "BENIGN":
    print("Risk Level: LOW")
else:
    print("Risk Level: HIGH")