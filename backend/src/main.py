from fastapi import FastAPI
from src.routers.app import router as base_router# 1. Initialize the main App
app = FastAPI(title="Hospital Management System")

# 2. Plug in the router
app.include_router(base_router)

# Now the app knows about all the routes defined in the router file!