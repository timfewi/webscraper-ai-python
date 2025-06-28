# Development commands for webscraper project
# Usage: .\dev.ps1 <command>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Command = "help",
    [switch]$VerboseOutput
)

function Show-Help {
    Write-Host "🤖 AI-Powered Web Scraper Development Tools" -ForegroundColor Cyan
    Write-Host "===========================================" -ForegroundColor Cyan
    Write-Host ""
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
    Write-Host "  status           Show project status"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\dev.ps1 setup-dev    # First time setup"
    Write-Host "  .\dev.ps1 ci           # Full CI pipeline"
    Write-Host "  .\dev.ps1 test-cov     # Tests with coverage"
    Write-Host ""
    Write-Host "Use -VerboseOutput for detailed output" -ForegroundColor Yellow
}

function Write-Status {
    param([string]$Message, [string]$Color = "Blue")
    Write-Host "🔧 $Message" -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Show-Status {
    Write-Host "📊 Project Status" -ForegroundColor Cyan
    Write-Host "=================" -ForegroundColor Cyan

    # Python version
    try {
        $pythonVersion = python --version 2>$null
        Write-Host "Python: $pythonVersion" -ForegroundColor White
    }
    catch {
        Write-Host "Python: ❌ Not found" -ForegroundColor Red
    }

    # Check if virtual environment is active
    if ($env:VIRTUAL_ENV) {
        Write-Host "Virtual Environment: ✅ Active ($env:VIRTUAL_ENV)" -ForegroundColor Green
    }
    else {
        Write-Host "Virtual Environment: ⚠️ Not active" -ForegroundColor Yellow
    }

    # Check if packages are installed
    try {
        pip show webscraper | Out-Null 2>&1
        Write-Host "Package Installation: ✅ Installed" -ForegroundColor Green
    }
    catch {
        Write-Host "Package Installation: ❌ Not installed (run .\dev.ps1 setup-dev)" -ForegroundColor Red
    }

    # Check test coverage
    if (Test-Path "htmlcov/index.html") {
        Write-Host "Test Coverage: ✅ Available (open htmlcov/index.html)" -ForegroundColor Green
    }
    else {
        Write-Host "Test Coverage: ⚠️ No recent coverage report" -ForegroundColor Yellow
    }

    # Git status
    try {
        $gitStatus = git status --porcelain 2>$null
        if ($gitStatus) {
            Write-Host "Git Status: ⚠️ Uncommitted changes" -ForegroundColor Yellow
        }
        else {
            Write-Host "Git Status: ✅ Clean working directory" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Git Status: ℹ️ Not a git repository" -ForegroundColor Gray
    }
}

function Install-Production {
    Write-Status "Installing production dependencies..."
    try {
        pip install -e .
        Write-Success "Production dependencies installed"
    }
    catch {
        Write-Error "Failed to install production dependencies"
        throw
    }
}

function Install-Dev {
    Write-Status "Installing development dependencies..."
    try {
        pip install -e ".[dev]"
        Write-Success "Development dependencies installed"
    }
    catch {
        Write-Error "Failed to install development dependencies"
        throw
    }
}

function Setup-Dev {
    Write-Status "Setting up development environment..."

    try {
        Install-Dev

        Write-Status "Installing pre-commit hooks..."
        pre-commit install

        Write-Success "Development environment setup complete!"
        Write-Host ""
        Write-Host "🚀 Quick Start:" -ForegroundColor Cyan
        Write-Host "  .\dev.ps1 status    # Check project status"
        Write-Host "  .\dev.ps1 test      # Run tests"
        Write-Host "  .\dev.ps1 ci        # Full CI pipeline"
    }
    catch {
        Write-Error "Setup failed. Please check the error messages above."
        throw
    }
}

function Format-Code {
    Write-Status "Formatting code with Black..."
    try {
        black .
        Write-Success "Code formatting complete"
    }
    catch {
        Write-Error "Code formatting failed"
        throw
    }
}

function Lint-Code {
    Write-Status "Linting code with Ruff..."
    try {
        ruff check . --fix
        Write-Success "Code linting complete"
    }
    catch {
        Write-Error "Code linting failed"
        throw
    }
}

function Type-Check {
    Write-Status "Type checking with MyPy..."
    try {
        mypy src/ --ignore-missing-imports
        Write-Success "Type checking complete"
    }
    catch {
        Write-Error "Type checking failed"
        throw
    }
}

function Security-Check {
    Write-Status "Running security checks..."
    try {
        Write-Status "Installing security tools..."
        pip install bandit[toml] safety

        Write-Status "Running Bandit security scan..."
        bandit -r src/

        Write-Status "Checking for vulnerable dependencies..."
        pip freeze | safety check --stdin

        Write-Success "Security checks complete"
    }
    catch {
        Write-Error "Security checks failed"
        throw
    }
}

function Run-Check {
    Write-Status "Running all quality checks..."
    try {
        Lint-Code
        Type-Check
        Write-Success "All quality checks passed"
    }
    catch {
        Write-Error "Quality checks failed"
        throw
    }
}

function Run-Tests {
    Write-Status "Running tests..."
    try {
        pytest tests/ -v
        Write-Success "Tests complete"
    }
    catch {
        Write-Error "Tests failed"
        throw
    }
}

function Run-Tests-Coverage {
    Write-Status "Running tests with coverage..."
    try {
        pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
        Write-Success "Tests with coverage complete"

        if (Test-Path "htmlcov/index.html") {
            Write-Host "📊 Coverage report: htmlcov/index.html" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Error "Tests with coverage failed"
        throw
    }
}

function Clean-Cache {
    Write-Status "Cleaning cache files..."

    $cleanItems = @(
        "*.pyc",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        "*.egg-info"
    )

    foreach ($pattern in $cleanItems) {
        Get-ChildItem -Path . -Recurse -Name $pattern -Force 2>$null | ForEach-Object {
            $fullPath = Join-Path $PWD $_
            if (Test-Path $fullPath) {
                if ($VerboseOutput) {
                    Write-Host "Removing: $fullPath" -ForegroundColor Gray
                }
                Remove-Item -Path $fullPath -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }

    # Clean specific directories
    $directories = @("build", "dist", "htmlcov")
    foreach ($dir in $directories) {
        if (Test-Path $dir) {
            if ($VerboseOutput) {
                Write-Host "Removing directory: $dir" -ForegroundColor Gray
            }
            Remove-Item -Path $dir -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    # Clean specific files
    if (Test-Path ".coverage") {
        if ($VerboseOutput) {
            Write-Host "Removing: .coverage" -ForegroundColor Gray
        }
        Remove-Item -Path ".coverage" -Force -ErrorAction SilentlyContinue
    }

    Write-Success "Cache cleanup complete"
}

function Pre-Commit-All {
    Write-Status "Running pre-commit on all files..."
    try {
        pre-commit run --all-files
        Write-Success "Pre-commit checks complete"
    }
    catch {
        Write-Error "Pre-commit checks failed"
        throw
    }
}

function Run-CI {
    Write-Status "Running full CI pipeline..."
    Write-Host "🔄 CI Pipeline Steps:" -ForegroundColor Cyan
    Write-Host "  1. Code formatting"
    Write-Host "  2. Quality checks (lint + type)"
    Write-Host "  3. Tests with coverage"
    Write-Host "  4. Security scanning"
    Write-Host ""

    try {
        Format-Code
        Run-Check
        Run-Tests-Coverage
        Security-Check
        Write-Success "🎉 All CI checks passed!"
        Write-Host "Your code is ready for production! 🚀" -ForegroundColor Green
    }
    catch {
        Write-Error "CI pipeline failed. Please fix the issues and try again."
        exit 1
    }
}

# Main command dispatcher
try {
    switch ($Command.ToLower()) {
        "help" { Show-Help }
        "status" { Show-Status }
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
            Write-Error "Unknown command: $Command"
            Write-Host ""
            Show-Help
            exit 1
        }
    }
}
catch {
    Write-Error "Command failed: $_"
    exit 1
}
