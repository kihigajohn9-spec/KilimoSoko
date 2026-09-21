from fastapi import FastAPI
from app.core.config import settings
app = FastAPI(
    title=settings.APP_NAME,
    description="Digital platform which connects famers to buyers",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "Welcome to KILIMOSOKO ",
    "status": "running"
    }
    
@app.get("/health")
def health_check():
    return{
        "status": "healthy"
    }
