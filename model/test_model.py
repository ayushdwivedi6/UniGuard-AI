import pandas as pd
import numpy as np
import joblib

# Load model
model = joblib.load("model/random_forest_model.pkl")
feature_names = joblib.load("model/feature_names.pkl")


def predict(row):

    # Keep only numerical features
    row = row.select_dtypes(include=[np.number])

    # Add missing features
    for feature in feature_names:
        if feature not in row.columns:
            row[feature] = 0

    # Keep the same feature order used during training
    row = row[feature_names]

    # Clean data
    row = row.replace([np.inf, -np.inf], np.nan)
    row = row.fillna(0)

    prediction = model.predict(row)[0]

    probabilities = model.predict_proba(row)[0]
    confidence = max(probabilities) * 100

    return prediction, confidence


# Load one sample from each file
files = {
    "BENIGN": "dataset/Monday-WorkingHours.pcap_ISCX.csv",
    "DDoS": "dataset/Friday-WorkingHours-Afternoon-DDoS.pcap_ISCX.csv",
    "PortScan": "dataset/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
}


print("\n======================================")
print("       UNIGUARD AI - MODEL TEST")
print("======================================\n")


for actual_type, file in files.items():

    print("Testing:", actual_type)

    data = pd.read_csv(file, nrows=1)

    data.columns = data.columns.str.strip()

    prediction, confidence = predict(data)

    print("Actual:     ", actual_type)
    print("Predicted:  ", prediction)
    print("Confidence: ", round(confidence, 2), "%")

    if prediction == actual_type:
        print("Result:      ✅ CORRECT")
    else:
        print("Result:      ❌ INCORRECT")

    print("--------------------------------------")