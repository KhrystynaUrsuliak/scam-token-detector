from fastapi import FastAPI

app = FastAPI(
    title="Crypto Scam Token Detection API",
    description="API for detecting scam cryptocurrency tokens",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Crypto Scam Detector API is running"}