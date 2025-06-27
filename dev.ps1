# Development commands for webscraper project
# Usage: .\dev.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Green
    Write-Host "  setup-dev        Setup development environment"
    Write-Host "  install          Install production dependencies"
    Write-Host "  format           Format code with Black"
    Write-Host "  lint             Lint code with Ruff"
    Write-Host "  type-check       Type check with MyPy"
    Write-Host "  check            Run all quality checks"
    Write-Host "  test             Run tests"
    Write-Host "  test-cov         Run tests with coverage"
    Write-Host "  security         Run security checks"
    Write-Host "  pre-commit-all   Run pre-commit on all files"
    Write-Host "  clean            Clean up cache files"
    Write-Host "  ci               Run full CI pipeline locally"
}

function Install-Production {
    Write-Host "Installing production dependencies..." -ForegroundColor Blue
    pip install -e .
}

function Install-Dev {
    Write-Host "Installing development dependencies..." -ForegroundColor Blue
    pip install -e ".[dev]"
}

function Setup-Dev {
    Write-Host "Setting up development environment..." -ForegroundColor Blue
    Install-Dev
    pre-commit install
    Write-Host "Development environment setup complete!" -ForegroundColor Green
    Write-Host "Run '.\dev.ps1 check' to verify everything is working."
}

function Format-Code {
    Write-Host "Formatting code with Black..." -ForegroundColor Blue
    black .
}

function Lint-Code {
    Write-Host "Linting code with Ruff..." -ForegroundColor Blue
    ruff check . --fix
}

function Type-Check {
    Write-Host "Type checking with MyPy..." -ForegroundColor Blue
    mypy src/
}

function Security-Check {
    Write-Host "Running security checks..." -ForegroundColor Blue
    pip install bandit[toml] safety
    bandit -r src/
    pip freeze | safety check --stdin
}

function Run-Check {
    Write-Host "Running all quality checks..." -ForegroundColor Blue
    Lint-Code
    Type-Check
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Blue
    pytest tests/ -v
}

function Run-Tests-Coverage {
    Write-Host "Running tests with coverage..." -ForegroundColor Blue
    pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
}

function Clean-Cache {
    Write-Host "Cleaning cache files..." -ForegroundColor Blue
    Get-ChildItem -Path . -Recurse -Name "*.pyc" | Remove-Item -Force
    Get-ChildItem -Path . -Recurse -Name "__pycache__" -Directory | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Recurse -Name ".mypy_cache" -Directory | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Recurse -Name ".pytest_cache" -Directory | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Recurse -Name "*.egg-info" -Directory | Remove-Item -Recurse -Force
    if (Test-Path "build") { Remove-Item -Path "build" -Recurse -Force }
    if (Test-Path "dist") { Remove-Item -Path "dist" -Recurse -Force }
    if (Test-Path ".coverage") { Remove-Item -Path ".coverage" -Force }
    if (Test-Path "htmlcov") { Remove-Item -Path "htmlcov" -Recurse -Force }
}

function Pre-Commit-All {
    Write-Host "Running pre-commit on all files..." -ForegroundColor Blue
    pre-commit run --all-files
}

function Run-CI {
    Write-Host "Running full CI pipeline..." -ForegroundColor Blue
    Format-Code
    Run-Check
    Run-Tests-Coverage
    Security-Check
    Write-Host "All CI checks passed!" -ForegroundColor Green
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Production }
    "dev-install" { Install-Dev }
    "setup-dev" { Setup-Dev }
    "format" { Format-Code }
    "lint" { Lint-Code }
    "type-check" { Type-Check }
    "check" { Run-Check }
    "test" { Run-Tests }
    "test-cov" { Run-Tests-Coverage }
    "security" { Security-Check }
    "clean" { Clean-Cache }
    "pre-commit-all" { Pre-Commit-All }
    "ci" { Run-CI }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help
    }
}
