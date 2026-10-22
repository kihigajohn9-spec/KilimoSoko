from fastapi import FastAPI
from app.core.config import settings
from app.core.data_base import engine, Base
from app.models import User, Farmer, Buyer, Product, Order,Farm
from app.api.authetication import router as auth_router
from app.api.farmers import router as farmer_router
from app.api.products import router as product_router
from app.api.orders import router as orders_router
from app.api.farm import router as farm_router
# Create the database tables
Base.metadata.create_all(bind=engine)



app = FastAPI(
    title=settings.APP_NAME,
    description="Digital platform which connects famers and buyers",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(farmer_router)
app.include_router(product_router)
app.include_router(orders_router)
app.include_router(farm_router)

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
