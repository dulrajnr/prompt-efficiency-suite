.PHONY: install test lint clean run

install:
	pip install -e .

test:
	pytest tests/ --cov=prompt_efficiency_suite --cov-report=term-missing

lint:
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/
	mypy src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

run:
	uvicorn prompt_efficiency_suite.main:app --reload

help:
	@echo "Available commands:"
	@echo "  make install    - Install the package in development mode"
	@echo "  make test       - Run tests with coverage"
	@echo "  make lint       - Run linters (flake8, black, isort, mypy)"
	@echo "  make format     - Format code with black and isort"
	@echo "  make clean      - Clean up build artifacts and caches"
	@echo "  make run        - Run the FastAPI server in development mode"
	@echo "  make help       - Show this help message"
