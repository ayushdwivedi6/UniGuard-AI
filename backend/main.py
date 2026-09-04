from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import numpy as np
import joblib
import os
import tempfile


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="UniGuard AI",
    description="AI-Based Cyber Threat Detection System",
    version="1.0"
)


# ==========================================
# ALLOW FRONTEND TO CONNECT
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://uni-guard-ai-rho.vercel.app"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# LOAD AI MODEL
# ==========================================

MODEL_PATH = "model/random_forest_model.pkl"
FEATURE_PATH = "model/feature_names.pkl"

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_PATH)


# ==========================================
# BASIC ROUTE
# ==========================================

@app.get("/")
def home():

    return {
        "status": "online",
        "system": "UniGuard AI",
        "message": "Cyber Threat Detection API is running"
    }


# ==========================================
# MODEL INFORMATION
# ==========================================

@app.get("/model-info")
def model_info():

    return {
        "model": "Random Forest",
        "features": len(feature_names),
        "classes": ["BENIGN", "DDoS", "PortScan"]
    }


# ==========================================
# CSV ANALYSIS
# ==========================================

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    # ======================================
    # CHECK FILE TYPE
    # ======================================

    if not file.filename.lower().endswith(".csv"):

        return {
            "error": "Please upload a CSV file."
        }


    # ======================================
    # CREATE TEMPORARY FILE
    # ======================================

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    ) as temp:

        temp.write(contents)
        temp_path = temp.name


    try:

        # ======================================
        # READ CSV
        # ======================================

        data = pd.read_csv(temp_path)

        data.columns = data.columns.str.strip()


        # ======================================
        # KEEP NUMERICAL FEATURES
        # ======================================

        features = data.select_dtypes(
            include=[np.number]
        )


        # ======================================
        # ADD MISSING FEATURES
        # ======================================

        for feature in feature_names:

            if feature not in features.columns:

                features[feature] = 0


        # ======================================
        # KEEP MODEL FEATURES
        # ======================================

        features = features[feature_names]


        # ======================================
        # CLEAN VALUES
        # ======================================

        features = features.replace(
            [np.inf, -np.inf],
            np.nan
        )

        features = features.fillna(0)


        # ======================================
        # AI PREDICTION
        # ======================================

        predictions = model.predict(features)


        # ======================================
        # COUNT RESULTS
        # ======================================

        counts = pd.Series(
            predictions
        ).value_counts()


        benign = int(
            counts.get("BENIGN", 0)
        )

        ddos = int(
            counts.get("DDoS", 0)
        )

        portscan = int(
            counts.get("PortScan", 0)
        )


        # Total threats

        threats = ddos + portscan


        # ======================================
        # TOTAL FLOWS
        # ======================================

        total = len(predictions)


        # ======================================
        # THREAT PERCENTAGE
        # ======================================

        if total > 0:

            threat_percentage = (
                threats / total
            ) * 100

        else:

            threat_percentage = 0


        # ======================================
        # RISK SCORE
        # ======================================

        if total > 0:

            threat_ratio = (
                threats / total
            )

        else:

            threat_ratio = 0


        risk_score = int(
            threat_ratio * 100
        )


        # Keep score between 0 and 100

        risk_score = min(
            max(risk_score, 0),
            100
        )


        # ======================================
        # SEVERITY
        # ======================================

        if risk_score <= 10:

            severity = "LOW"

        elif risk_score <= 30:

            severity = "MEDIUM"

        elif risk_score <= 60:

            severity = "HIGH"

        else:

            severity = "CRITICAL"


        # ======================================
        # AI CONFIDENCE
        # ======================================

        if total > 0:

            probabilities = model.predict_proba(
                features
            )

            confidence = (
                probabilities.max(axis=1).mean()
            ) * 100

        else:

            confidence = 0


        # ======================================
        # RESPONSE
        # ======================================

        return {

            "filename": file.filename,

            "total_flows": total,

            "benign": benign,

            "ddos": ddos,

            "portscan": portscan,

            "threats": threats,

            "threat_percentage": round(
                threat_percentage,
                2
            ),

            "risk_score": risk_score,

            "severity": severity,

            "confidence": round(
                confidence,
                2
            )
        }


    finally:

        # ======================================
        # REMOVE TEMPORARY FILE
        # ======================================

        if os.path.exists(temp_path):

            os.remove(temp_path)