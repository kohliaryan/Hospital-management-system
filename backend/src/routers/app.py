from fastapi import APIRouter
# from src.core.database import engine # Keep your DB imports if needed

# 1. Create a Router (Think of it as a "Mini App")
router = APIRouter()

# 2. Use @router instead of @app
@router.get("/")
async def root():
    return {"message": "Hello from the Router!"}

@router.get("/health")
async def health_check():
    return {"status": "ok"}