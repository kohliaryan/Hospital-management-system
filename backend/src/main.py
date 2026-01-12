from fastapi import FastAPI
from src.routers.app import router as base_router

from src.core.database import engine, Base
from contextlib import asynccontextmanager
from src.models.users import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Because we imported 'User' above, Base now knows about it!
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# ... rest of your code ...


app = FastAPI(title="Hospital Management System", lifespan=lifespan)
@app.get("/")
def read_root():
    return {"msg": "Hello Aryan!"}

# 2. Plug in the router
app.include_router(base_router)

# Now the app knows about all the routes defined in the router file!