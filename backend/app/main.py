from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import predict, auth
from app.routes import checks
from app.routes import favorites
from app.routes import reports
from app.admin import router as admin_router
from app.database import engine, Base
import app.models.user
import app.models.token
import app.models.check
import app.models.favorite
import app.models.report
import app.models.audit_log

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crypto Scam Token Detection API",
    description="API for detecting scam cryptocurrency tokens",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(checks.router)
app.include_router(favorites.router)
app.include_router(reports.router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Crypto Scam Detector API is running"}