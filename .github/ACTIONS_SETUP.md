# GitHub Actions CI/CD Setup

This document explains the GitHub Actions workflows configured for this webscraper project.

## Workflows Overview

### Main Workflow: `ci.yml`

The main CI/CD pipeline runs on every push and pull request to `main` and `develop` branches.

#### Jobs:

1. **Code Quality** - Tests code formatting, linting, type checking, and runs tests
2. **Security** - Scans for security vulnerabilities in code
3. **Dependency Check** - Checks dependencies for known vulnerabilities
4. **Pre-commit** - Runs all pre-commit hooks

#### Matrix Testing

The workflow tests against multiple Python versions:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.13

## Local Development

### Setup Development Environment

```bash
# Setup everything needed for development
make setup-dev

# Or manually:
pip install -e ".[dev]"
pre-commit install
```

### Daily Workflow

```bash
# Before committing code
make check          # Run linting and type checking
make test-cov      # Run tests with coverage
make format        # Format code

# Run full CI pipeline locally
make ci
```

### Available Make Commands

- `make setup-dev` - Setup development environment
- `make format` - Format code with Black
- `make lint` - Lint code with Ruff (auto-fix enabled)
- `make type-check` - Type check with MyPy
- `make check` - Run lint + type check
- `make test` - Run tests
- `make test-cov` - Run tests with coverage report
- `make security` - Run security scans
- `make clean` - Clean cache files
- `make ci` - Run full CI pipeline locally

## Workflow Details

### Code Quality Checks

1. **Black Formatting**
   - Ensures consistent code formatting
   - Configuration in `pyproject.toml`
   - Line length: 88 characters

2. **Ruff Linting**
   - Fast Python linter replacing flake8, isort, and others
   - Includes import sorting and code quality checks
   - Auto-fixes many issues

3. **MyPy Type Checking**
   - Static type checking for Python
   - Helps catch type-related bugs early
   - Currently set to non-blocking (continues on errors)

4. **Pytest Testing**
   - Runs all tests in `tests/` directory
   - Generates coverage reports
   - Minimum coverage requirement: 70%

### Security Scanning

1. **Bandit Security Scan**
   - Scans for common security issues in Python code
   - Generates JSON reports uploaded as artifacts

2. **Safety Dependency Check**
   - Checks installed packages against known vulnerability database
   - Fails CI if vulnerable packages found

### Pre-commit Integration

The workflow also runs all pre-commit hooks to ensure consistency with local development.

## Artifacts and Reports

### Coverage Reports
- Coverage reports uploaded to Codecov
- HTML coverage reports available as artifacts
- Minimum coverage threshold: 70%

### Security Reports
- Bandit security scan results uploaded as JSON artifacts
- Available for download from GitHub Actions runs

## Status Badges

Add these badges to your README to show build status:

```markdown
![CI Status](https://github.com/timfewi/webscraper-ai-python/workflows/Code%20Quality%20&%20Tests/badge.svg)
![Coverage](https://codecov.io/gh/timfewi/webscraper-ai-python/branch/main/graph/badge.svg)
```

## Troubleshooting

### Common CI Failures

1. **Black formatting issues**
   ```bash
   make format  # Fix locally then commit
   ```

2. **Ruff linting errors**
   ```bash
   make lint    # Auto-fix many issues
   ```

3. **Test failures**
   ```bash
   make test    # Run tests locally to debug
   ```

4. **Type checking errors**
   ```bash
   make type-check  # Check types locally
   ```

### Local vs CI Differences

If CI fails but local checks pass:
1. Ensure you're using the same Python version
2. Make sure all dependencies are up to date
3. Run `make ci` to simulate the full pipeline locally

### Branch Protection

Consider enabling branch protection rules in GitHub:
1. Require status checks to pass before merging
2. Require branches to be up to date before merging
3. Require pull request reviews before merging

## Configuration Files

- `.github/workflows/ci.yml` - Main CI/CD workflow
- `pyproject.toml` - Tool configurations (Black, Ruff, MyPy, Pytest)
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `Makefile` - Local development commands
- `.vscode/settings.json` - VS Code integration settings

## Next Steps

1. **Enable branch protection** on main branch
2. **Set up Codecov** for coverage tracking
3. **Add more comprehensive tests** as you develop features
4. **Consider adding deployment workflows** for releases
5. **Set up dependency updates** with Dependabot
