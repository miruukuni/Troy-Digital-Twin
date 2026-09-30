# Troy-Digital-Twin

Personal Digital Twin backend scaffold for Milestones 1 and 2.

## Project structure

```text
app/
  api/
    routes/
      ingest.py          # FastAPI ingestion route
  core/
    config.py            # Environment/config settings
  db/
    models/
      memory.py          # Personal memory schema + pgvector embedding field
    session.py           # Engine/session setup + DB bootstrap
  schemas/
    ingest.py            # Request/response schemas
  services/
    ingestion.py         # Categorization + embedding + persistence logic
  main.py                # FastAPI app entrypoint
```

## Personal memory categories

- `identity`: basic facts, education, career, interests
- `preferences`: technology, work style, entertainment
- `experiences`: projects, accomplishments, failures
- `beliefs_reasoning`: principles, tradeoffs, decision patterns
- `communication`: vocabulary, tone, formatting habits

## Quickstart

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment:
   ```bash
   cp .env.example .env
   # then set OPENAI_API_KEY
   ```
3. Start API:
   ```bash
   uvicorn app.main:app --reload
   ```

## Ingest endpoint

`POST /ingest`

Example request:

```json
{
  "text": "I prefer concise pull request reviews and Python for backend work.",
  "source_label": "old_email",
  "metadata": {
    "author": "troy",
    "timestamp": "2025-10-08"
  }
}
```

Behavior:
- Classifies input into one of the five memory buckets
- Creates OpenAI embedding
- Stores text, metadata, category, and vector in PostgreSQL with pgvector
