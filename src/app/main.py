from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routes import health, items


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="ai-app", lifespan=lifespan)
app.include_router(health.router)
app.include_router(items.router)
