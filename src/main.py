import contextlib

from fastapi import FastAPI

from src import database


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = FastAPI(
    title="URL Shortener",
    description="Web application to get shorten URL",
    lifespan=lifespan,
    version="0.1.0",
)
