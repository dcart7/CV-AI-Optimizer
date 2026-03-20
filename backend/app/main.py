from fastapi import FastAPI

from app.api.routes.analyze import router as analyze_router
from app.db.init_db import init_db

app = FastAPI(title="Smart CV Optimizer API")

app.include_router(analyze_router, prefix="/analyze", tags=["analyze"])


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
