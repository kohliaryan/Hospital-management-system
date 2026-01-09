from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import engine, Base
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    print("Shutdown: Closing database connection...")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return "Server is running!"

