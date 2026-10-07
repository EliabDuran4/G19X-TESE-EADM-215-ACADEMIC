from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.config import settings
from app.routers import documents
from app.core.telemetry import setup_telemetry 


app = FastAPI(title=settings.app_name)

setup_telemetry(app)

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(documents.router, prefix="/documents", tags=["Documentos"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": settings.app_name}


@app.get("/health")
def health_check():
    return {"status": "healthy"}