import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


print("Loading dataset...")

data = pd.read_csv("dataset/combined.csv")

print("Dataset loaded!")
print("Total rows:", len(data))


# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

data.columns = data.columns.str.strip()


# ==========================================
# BALANCED DATASET
# ==========================================

target = "Attack_Type"

samples_per_class = 75000

selected_data = []

for attack_type in ["BENIGN", "DDoS", "PortScan"]:

    class_data = data[data[target] == attack_type]

    print(
        attack_type,
        "available:",
        len(class_data)
    )

    class_data = class_data.sample(
        min(samples_per_class, len(class_data)),
        random_state=42
    )

    selected_data.append(class_data)


train_data = pd.concat(
    selected_data,
    ignore_index=True
)


# ==========================================
# FEATURES
# ==========================================

X = train_data.drop(
    columns=[target]
)

y = train_data[target]


# Numerical features only
X = X.select_dtypes(
    include=[np.number]
)


# Clean infinite and missing values
X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)


print("\nTraining samples:", len(X))

print("\nClass distribution:")
print(y.value_counts())


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


# ==========================================
# RANDOM FOREST
# ==========================================

print("\nTraining Random Forest...")

model = RandomForestClassifier(

    n_estimators=75,

    max_depth=20,

    random_state=42,

    n_jobs=-1,

    min_samples_leaf=2
)


model.fit(
    X_train,
    y_train
)


print("Training completed!")


# ==========================================
# EVALUATE
# ==========================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n================================")
print("MODEL PERFORMANCE")
print("================================")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "model/random_forest_model.pkl"
)

joblib.dump(
    list(X.columns),
    "model/feature_names.pkl"
)


print("\n================================")
print("MODEL SAVED SUCCESSFULLY")
print("================================")