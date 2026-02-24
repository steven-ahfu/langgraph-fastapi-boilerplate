# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A boilerplate for building LLM-powered applications using LangGraph (workflow engine) + FastAPI (API layer) + LangSmith (observability/evaluation). The included CV-scoring workflow is the reference implementation—replace or extend it to build your own workflows.

## Commands

```bash
# Install dependencies
uv sync

# Run dev server (hot reload at http://localhost:8000)
fastapi dev

# Docker with file watch (rebuilds on pyproject.toml/uv.lock changes)
uv sync && docker compose up --watch --build

# Lint
ruff check . --fix

# Upload dataset examples to LangSmith
uv run python -m datasets.candidate_cv

# Run LLM-as-judge evaluation against LangSmith dataset
uv run python -m evals.candidate_scores
```

There is no test suite — evaluation is done via LangSmith experiments (`evals/`).

## Architecture

### Request Flow

```
HTTP Request → app/routers/*.py → graphs/*.py (LangGraph) → LLM → Pydantic schema → Response
```

Routers are thin: they validate input, call a compiled graph, and return the result. Business logic lives in `graphs/`.

### LangGraph Pattern

Every workflow in `graphs/` follows this structure:

1. **Two TypedDicts**: `State` (data flowing between nodes) and `ContextSchema` (runtime config like model name and prompt)
2. **Async node functions** that receive `(state: State, runtime: Runtime[ContextSchema])` — access `runtime.context` for config, `state` for data
3. **`compile_*()`** function that builds and returns the graph
4. **Invocation** passes state inputs and a `context=` dict at call time

```python
result = await graph.ainvoke(
    {"your_input": value},
    context={"model_name": "gpt-4o", "prompt": PROMPT_TEMPLATE}
)
```

This separation means the same graph can run different models/prompts without code changes.

### Structured Outputs

Node functions use `llm.with_structured_output(PydanticModel).ainvoke(prompt)` to get typed LLM responses. Pydantic models live in `schemas/` and are shared between graphs and API routers.

### Models

Pre-configured in `settings.py` as a `MODELS` dict. Keys: `"gpt-3.5-turbo"`, `"gpt-4o-mini"`, `"gpt-4o"` (temp=0), `"o3-mini"`. Add new models there.

### LangSmith

Tracing is **automatically enabled** when `LANGSMITH_API_KEY` and `LANGSMITH_PROJECT` are set in `.env`. No code changes needed. Evaluation experiments (`evals/`) run your compiled graph against a stored dataset and score outputs with an LLM judge via `openevals`.

### ChromaDB

Optional vector store. The `vectors` router initializes an async client on first request via FastAPI `Depends()`. Requires `CHROMA_*` env vars.

## Adding a New Workflow

1. **Schema** — Add a Pydantic model in `schemas/your_feature.py`
2. **Prompt** — Add a prompt template string in `prompts/your_feature.py`
3. **Graph** — Add `graphs/your_feature.py` following the `State`/`ContextSchema`/`compile_*()` pattern
4. **Router** — Add `app/routers/your_feature.py` and include it in `app/main.py`
5. **Dataset** (optional) — Add `datasets/your_feature.py` for LangSmith dataset management
6. **Eval** (optional) — Add `evals/your_feature.py` for evaluation pipelines

## Integrating Into Another Project

To pull a workflow into an existing project, you need:

- The `graphs/your_workflow.py` file (and its imports: schema, prompt, settings)
- `settings.py` for `MODELS` dict and env var loading
- Dependencies: `langgraph`, `langchain-openai`, `pydantic`, `python-dotenv`

Call the compiled graph directly without FastAPI:

```python
from graphs.candidate_scores import compile_candidate_scores
from prompts.candidate_scores import PROMPT

graph = compile_candidate_scores()
result = await graph.ainvoke(
    {"cv_text": "..."},
    context={"model_name": "gpt-4o", "prompt": PROMPT}
)
scores = result["candidate_scores"]  # CandidateScores Pydantic instance
```

The graph functions are framework-agnostic — they don't depend on FastAPI and can be called from any async Python context.

## Environment Setup

Copy `.env.example` to `.env` and fill in:

```bash
OPENAI_API_KEY=       # Required
LANGSMITH_API_KEY=    # Required for tracing and evals
LANGSMITH_PROJECT=    # Required for tracing and evals
CHROMA_HOST=api.trychroma.com  # Optional, for vector storage
CHROMA_TENANT=
CHROMA_DATABASE=
CHROMA_TOKEN=
LOG_LEVEL=INFO        # Optional, default INFO
```
