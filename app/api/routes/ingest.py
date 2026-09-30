from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.ingest import IngestRequest, IngestResponse
from app.services.ingestion import IngestionService

router = APIRouter(prefix="", tags=["ingestion"])
service = IngestionService()


@router.post("/ingest", response_model=IngestResponse)
def ingest_memory(payload: IngestRequest, session: Session = Depends(get_session)) -> IngestResponse:
    try:
        memory = service.ingest_text(
            text=payload.text,
            source_label=payload.source_label,
            metadata=payload.metadata,
            session=session,
        )
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {exc}") from exc

    return IngestResponse(id=str(memory.id), category=memory.category.value, source_label=memory.source_label)
