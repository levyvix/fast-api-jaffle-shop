

run-dev:
	uv run fastapi dev

run:
	uv run run.py

lint:
	uv run ruff check . --exclude packages/dlt_plus/dlt_plus/transformations/dataframes/templates
	uv run ruff format --check . --exclude packages/dlt_plus/dlt_plus/transformations/dataframes/templates

format:
	uv run ruff format . --exclude packages/dlt_plus/dlt_plus/transformations/dataframes/templates


test:
	uv run pytest

test-fast:
	uv run pytest tests/test_routers.py -v -m "not slow"

freeze-requirements:
	uv sync --no-dev
	uv pip freeze > requirements.txt
