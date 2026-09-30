from openai import OpenAI
from sqlmodel import Session

from app.core.config import settings
from app.db.models.memory import MemoryCategory, PersonalMemory

_CATEGORY_DESCRIPTIONS = {
    MemoryCategory.IDENTITY: "basic facts, education, career, interests",
    MemoryCategory.PREFERENCES: "technology, work style, entertainment preferences",
    MemoryCategory.EXPERIENCES: "projects, accomplishments, failures, lessons learned",
    MemoryCategory.BELIEFS_REASONING: "principles, decision criteria, tradeoff thinking",
    MemoryCategory.COMMUNICATION: "tone, vocabulary, formatting, communication habits",
}


class IngestionService:
    @staticmethod
    def _get_client() -> OpenAI:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        return OpenAI(api_key=settings.openai_api_key)

    def _classify_memory(self, text: str) -> MemoryCategory:
        prompt = (
            "Classify the provided text into exactly one of these labels: "
            f"{', '.join(category.value for category in MemoryCategory)}. "
            "Return only the label.\n\n"
            "Label definitions:\n"
            + "\n".join(f"- {key.value}: {value}" for key, value in _CATEGORY_DESCRIPTIONS.items())
            + f"\n\nText:\n{text}"
        )

        client = self._get_client()
        response = client.responses.create(
            model=settings.openai_classifier_model,
            input=prompt,
            temperature=0,
            max_output_tokens=16,
        )
        classification = (response.output_text or "").strip().lower()
        try:
            return MemoryCategory(classification)
        except ValueError:
            return MemoryCategory.EXPERIENCES

    def _embed(self, text: str) -> list[float]:
        client = self._get_client()
        embedding_response = client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text,
            dimensions=settings.embedding_dimensions,
        )
        return embedding_response.data[0].embedding

    def ingest_text(self, *, text: str, source_label: str, metadata: dict, session: Session) -> PersonalMemory:
        category = self._classify_memory(text)
        embedding = self._embed(text)

        memory = PersonalMemory(
            category=category,
            source_text=text,
            source_label=source_label,
            memory_metadata=metadata,
            embedding=embedding,
        )
        session.add(memory)
        session.commit()
        session.refresh(memory)
        return memory
