from fastapi import FastAPI

from app.api.routes.ingest import router as ingest_router
from app.db.session import create_db_and_tables

app = FastAPI(title="Personal Digital Twin API", version="0.1.0")
app.include_router(ingest_router)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
