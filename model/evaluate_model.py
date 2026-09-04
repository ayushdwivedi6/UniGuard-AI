import pandas as pd
import numpy as np
import joblib


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(
    "model/random_forest_model.pkl"
)

feature_names = joblib.load(
    "model/feature_names.pkl"
)


# ==========================================
# FILES TO TEST
# ==========================================

files = {

    "BENIGN": "dataset/Monday-WorkingHours.pcap_ISCX.csv",

    "DDoS": "dataset/Friday-WorkingHours-Afternoon-DDoS.pcap_ISCX.csv",

    "PortScan": "dataset/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"

}


# ==========================================
# TEST EACH DATASET
# ==========================================

for expected, filename in files.items():

    print("\n====================================")
    print("Testing:", expected)
    print("====================================")

    data = pd.read_csv(filename)

    data.columns = data.columns.str.strip()


    # Select numerical features
    features = data.select_dtypes(
        include=[np.number]
    )


    # Add missing features
    for feature in feature_names:

        if feature not in features.columns:

            features[feature] = 0


    # Keep correct order
    features = features[feature_names]


    # Clean values
    features = features.replace(
        [np.inf, -np.inf],
        np.nan
    )

    features = features.fillna(0)


    # Predict
    predictions = model.predict(features)


    # Count predictions
    counts = pd.Series(
        predictions
    ).value_counts()


    total = len(predictions)


    benign = int(
        counts.get("BENIGN", 0)
    )

    ddos = int(
        counts.get("DDoS", 0)
    )

    portscan = int(
        counts.get("PortScan", 0)
    )


    print("Total:", total)

    print(
        "BENIGN:",
        benign,
        f"({benign / total * 100:.2f}%)"
    )

    print(
        "DDoS:",
        ddos,
        f"({ddos / total * 100:.2f}%)"
    )

    print(
        "PortScan:",
        portscan,
        f"({portscan / total * 100:.2f}%)"
    )