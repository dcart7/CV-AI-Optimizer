from fastapi import FastAPI

from app.api.routes.analyze import router as analyze_router

app = FastAPI(title="Smart CV Optimizer API")

app.include_router(analyze_router, prefix="/analyze", tags=["analyze"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
