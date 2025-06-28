.PHONY: install format lint type-check test clean dev-install help

# Default target
help:
	@echo "Available commands:"
	@echo "  setup-dev        Setup development environment"
	@echo "  install          Install production dependencies"
	@echo "  format           Format code with Black"
	@echo "  lint             Lint code with Ruff"
	@echo "  type-check       Type check with MyPy"
	@echo "  check            Run all quality checks"
	@echo "  test             Run tests"
	@echo "  test-cov         Run tests with coverage"
	@echo "  security         Run security checks"
	@echo "  pre-commit-all   Run pre-commit on all files"
	@echo "  clean            Clean up cache files"
	@echo "  ci               Run full CI pipeline locally"

# Install production dependencies
install:
	pip install -e .

# Install development dependencies
dev-install:
	pip install -e ".[dev]"

# Setup development environment
setup-dev: dev-install
	pre-commit install
	@echo "Development environment setup complete!"
	@echo "Run 'make check' to verify everything is working."

# Format code with Black
format:
	black .

# Lint code with Ruff
lint:
	ruff check . --fix

# Type check with MyPy
type-check:
	mypy src/ --ignore-missing-imports

# Security check
security:
	pip install bandit[toml] safety
	bandit -r src/
	pip freeze | safety check --stdin

# Run all quality checks
check: lint type-check

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Clean up cache files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/

# Install pre-commit hooks
pre-commit-install:
	pre-commit install

# Run pre-commit on all files
pre-commit-all:
	pre-commit run --all-files

# Full CI pipeline (what runs in GitHub Actions)
ci: format check test-cov security
	@echo "All CI checks passed!"
