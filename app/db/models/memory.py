from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Column, DateTime, Enum as SqlEnum
from sqlmodel import Field, SQLModel

from app.core.config import settings


class MemoryCategory(str, Enum):
    IDENTITY = "identity"
    PREFERENCES = "preferences"
    EXPERIENCES = "experiences"
    BELIEFS_REASONING = "beliefs_reasoning"
    COMMUNICATION = "communication"


class PersonalMemory(SQLModel, table=True):
    __tablename__ = "personal_memories"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    category: MemoryCategory = Field(sa_column=Column(SqlEnum(MemoryCategory), nullable=False, index=True))
    source_text: str = Field(nullable=False)
    source_label: str = Field(default="unstructured_note", nullable=False)
    memory_metadata: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    embedding: list[float] = Field(sa_column=Column(Vector(settings.embedding_dimensions), nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
