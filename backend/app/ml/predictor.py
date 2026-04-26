import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "scam_token_detector.pkl"

model = joblib.load(MODEL_PATH)

def predict_token(name: str, url: str):
    slug = url.rstrip("/").split("/")[-1]
    text_input = f"{name} {slug}"

    prediction = model.predict([text_input])[0]

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba([text_input])[0][1])

    risk_score = round(probability * 100, 2) if probability is not None else None

    label = "SCAM" if prediction == 1 else "LEGIT"

    if risk_score is not None:
        if risk_score >= 70:
            explanation = "High scam risk detected based on token name and URL patterns."
        elif risk_score >= 40:
            explanation = "Moderate scam risk detected. Additional verification is recommended."
        else:
            explanation = "Low scam risk detected based on the available data."
    else:
        explanation = "Prediction generated successfully."

    return {
        "name": name,
        "url": url,
        "slug": slug,
        "prediction": label,
        "probability": probability,
        "risk_score": risk_score,
        "explanation": explanation
    }