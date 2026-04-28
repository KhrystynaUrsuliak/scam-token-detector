from fastapi import FastAPI
from app.routes import predict, auth
from app.routes import checks
from app.routes import favorites
from admin import router as admin_router

app = FastAPI(
    title="Crypto Scam Token Detection API",
    description="API for detecting scam cryptocurrency tokens",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(checks.router)
app.include_router(favorites.router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Crypto Scam Detector API is running"}