.PHONY: setup data run app test figures lint

setup:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

data:
	.venv/bin/python scripts/download_data.py

run:
	.venv/bin/python -m nilm.model
	.venv/bin/python scripts/make_figures.py

app:
	streamlit run app/app.py

test:
	.venv/bin/pytest -q

figures:
	.venv/bin/python scripts/make_figures.py

lint:
	.venv/bin/ruff check src tests
	.venv/bin/ruff format --check src tests
