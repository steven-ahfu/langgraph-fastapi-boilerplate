# Repository Guidelines

Use this guide to navigate the repository, run the project locally, and
contribute changes that match the current structure and conventions.

## Project structure and module organization

The repository is organized around LangGraph workflows and FastAPI serving.
Core Python code lives in top-level packages rather than a `src/` directory.

- `app/` holds the FastAPI app and routers.
- `graphs/` contains LangGraph workflow definitions.
- `schemas/` defines Pydantic models for structured outputs.
- `prompts/` stores prompt templates, including `prompts/evals/`.
- `datasets/` and `evals/` provide LangSmith dataset and evaluation scripts.
- `notebooks/` contains exploratory notebooks and sample data.
- `settings.py` and `logger.py` centralize configuration and logging.

## Build, test, and development commands

Use `uv` for dependency management and local runs.

- `uv sync` installs dependencies into the environment.
- `fastapi dev` starts the local API server.
- `uv sync && docker compose up --watch --build` runs the Docker workflow.
- `uv run python -m datasets.candidate_cv` builds a LangSmith dataset.
- `uv run python -m evals.candidate_scores` runs an evaluation pipeline.

## Coding style and naming conventions

Python code uses 4-space indentation and follows standard module naming.
Ruff is configured in `pyproject.toml` with a 120-character line length.

- Use `snake_case` for files and functions.
- Keep Pydantic models in `schemas/` and graph logic in `graphs/`.
- Run `uv run ruff check .` to lint when working on Python code.

## Testing guidelines

There are no automated tests in the repository today. If you add tests,
place them under `tests/` and name files like `test_graphs.py`, then run
`uv run pytest` after adding `pytest` to the dev dependency group.

## Commit and pull request guidelines

Recent commit messages are short, lowercase summaries such as `update readme`.
Keep messages concise and action-oriented.

For pull requests, include a short summary, a list of key changes, and the
commands you ran. If you changed prompts, datasets, or evaluations, call out
those files explicitly.

## Security and configuration tips

Secrets live in a local `.env` file and must not be committed. Required keys
include `OPENAI_COMPAT_API_KEY` and `LANGSMITH_API_KEY`. Set
`OPENAI_COMPAT_BASE_URL` to the provider base URL. Review `settings.py` for
expected configuration values before running workflows.
