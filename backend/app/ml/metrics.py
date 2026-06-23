import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

MODEL_PATH = Path(__file__).parent / "scam_token_detector.pkl"

_DEFAULT_DATASET_LOCATIONS = [
    Path(__file__).parent.parent.parent / "data" / "Crypto_enhanced_dataset.csv",
    Path(__file__).parent.parent.parent / "data" / "Crypto_final_labeled.csv",
]


def compute_model_metrics():
    dataset_path = os.getenv("DATASET_PATH")
    if dataset_path:
        path = Path(dataset_path)
    else:
        path = next((p for p in _DEFAULT_DATASET_LOCATIONS if p.exists()), None)

    if path is None or not path.exists():
        checked = [str(p) for p in _DEFAULT_DATASET_LOCATIONS]
        return None, f"Dataset not found. Place it at one of: {checked}, or set DATASET_PATH env var."

    model = joblib.load(MODEL_PATH)

    df = pd.read_csv(path)
    df["url_slug"] = df["url"].fillna("").apply(lambda u: u.rstrip("/").split("/")[-1])
    df["text_feature"] = (df["name"].fillna("") + " " + df["url_slug"]).astype(str)

    X = df["text_feature"]
    y = df["is_scam"]

    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred).tolist()

    proba_distribution = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_test)[:, 1]
        buckets = [0] * 10
        for p in proba:
            buckets[min(int(p * 10), 9)] += 1
        proba_distribution = {
            "labels": ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%",
                       "50-60%", "60-70%", "70-80%", "80-90%", "90-100%"],
            "values": buckets,
        }

    return {
        "accuracy": round(report["accuracy"], 4),
        "precision": round(report["weighted avg"]["precision"], 4),
        "recall": round(report["weighted avg"]["recall"], 4),
        "f1_score": round(report["weighted avg"]["f1-score"], 4),
        "confusion_matrix": cm,
        "class_report": {
            "legit": {
                "precision": round(report["0"]["precision"], 4),
                "recall": round(report["0"]["recall"], 4),
                "f1": round(report["0"]["f1-score"], 4),
                "support": int(report["0"]["support"]),
            },
            "scam": {
                "precision": round(report["1"]["precision"], 4),
                "recall": round(report["1"]["recall"], 4),
                "f1": round(report["1"]["f1-score"], 4),
                "support": int(report["1"]["support"]),
            },
        },
        "probability_distribution": proba_distribution,
        "test_size": len(y_test),
    }, None
