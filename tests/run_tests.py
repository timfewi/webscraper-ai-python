"""
Comprehensive test runner for the webscraper project.

This script runs all tests with proper coverage reporting and formatting.
"""

import importlib.util
from pathlib import Path
import subprocess
import sys


def run_tests():
    """Run all tests with coverage and proper formatting."""
    # Base pytest command
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--strict-config",  # Strict config checking
        "--durations=10",  # Show 10 slowest tests
    ]

    # Add coverage if available
    if importlib.util.find_spec("coverage") is not None:
        cmd.extend(
            [
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
                "--cov-fail-under=60",
            ]
        )
        print("Running tests with coverage reporting...")
    else:
        print("Coverage not available, running tests without coverage...")

    # Add parallel execution if pytest-xdist is available
    if importlib.util.find_spec("xdist") is not None:
        cmd.extend(["-n", "auto"])
        print("Running tests in parallel...")

    # Run the tests
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def run_unit_tests_only():
    """Run only unit tests (fast execution)."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",
        "-m",
        "not integration and not slow",
        "--tb=short",
    ]

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error running unit tests: {e}")
        return 1


def run_integration_tests_only():
    """Run only integration tests."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",
        "-m",
        "integration",
        "--tb=short",
    ]

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error running integration tests: {e}")
        return 1


def type_check():
    """Run mypy type checking."""
    print("Running type checking...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "mypy", "src/", "tests/"],
            check=False,
        )
        if result.returncode == 0:
            print("✓ MyPy type checking passed")
        else:
            print("✗ MyPy type checking failed")
        return result.returncode
    except FileNotFoundError:
        print("MyPy not available, skipping type checking...")
        return 0


def lint_code():
    """Run code linting and formatting checks."""
    print("Running code quality checks...")
    exit_code = 0

    # Run ruff if available (preferred)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "src/", "tests/"],
            check=False,
        )
        if result.returncode == 0:
            print("✓ Ruff linting passed")
        else:
            print("✗ Ruff linting failed")
            exit_code = max(exit_code, result.returncode)
    except FileNotFoundError:
        # Fallback to flake8 if ruff not available
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "flake8",
                    "src/",
                    "tests/",
                    "--max-line-length=88",
                    "--extend-ignore=E203,W503",
                ],
                check=False,
            )
            if result.returncode == 0:
                print("✓ Flake8 linting passed")
            else:
                print("✗ Flake8 linting failed")
                exit_code = max(exit_code, result.returncode)
        except FileNotFoundError:
            print("Neither ruff nor flake8 available, skipping linting...")

    # Run black formatting check if available
    try:
        result = subprocess.run(
            [sys.executable, "-m", "black", "--check", "--diff", "src/", "tests/"],
            check=False,
        )
        if result.returncode == 0:
            print("✓ Black formatting check passed")
        else:
            print("✗ Black formatting check failed")
            exit_code = max(exit_code, result.returncode)
    except FileNotFoundError:
        print("Black not available, skipping formatting check...")

    return exit_code


def security_check():
    """Run security checks."""
    print("Running security checks...")
    exit_code = 0

    # Run bandit for security issues
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "bandit",
                "-r",
                "src/",
                "-f",
                "json",
                "-o",
                "bandit-report.json",
            ],
            check=False,
            capture_output=True,
        )
        if result.returncode == 0:
            print("✓ Bandit security check passed")
        else:
            print("✗ Bandit security check found issues")
            exit_code = max(exit_code, result.returncode)
    except FileNotFoundError:
        print("Bandit not available, skipping security check...")

    # Run safety for dependency vulnerabilities
    try:
        result = subprocess.run(
            [sys.executable, "-m", "safety", "check", "--json"],
            check=False,
            capture_output=True,
        )
        if result.returncode == 0:
            print("✓ Safety dependency check passed")
        else:
            print("✗ Safety found vulnerable dependencies")
            exit_code = max(exit_code, result.returncode)
    except FileNotFoundError:
        print("Safety not available, skipping dependency check...")

    return exit_code


def validate_markers():
    """Validate that all pytest markers are properly defined."""
    print("Validating pytest markers...")

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("⚠ pyproject.toml not found, cannot validate markers")
        return 0

    # This is a basic check - in a real implementation you might parse the TOML
    # and check for marker definitions
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--markers"],
            check=False,
            capture_output=True,
            text=True,
        )
        if "integration" not in result.stdout:
            print("⚠ 'integration' marker not properly defined in pyproject.toml")
            return 1
        print("✓ Pytest markers validation passed")
        return 0
    except Exception as e:
        print(f"Error validating markers: {e}")
        return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run webscraper tests")
    parser.add_argument("--unit-only", action="store_true", help="Run only unit tests")
    parser.add_argument(
        "--integration-only", action="store_true", help="Run only integration tests"
    )
    parser.add_argument("--lint", action="store_true", help="Run code quality checks")
    parser.add_argument("--type-check", action="store_true", help="Run type checking")
    parser.add_argument("--security", action="store_true", help="Run security checks")
    parser.add_argument(
        "--validate-markers", action="store_true", help="Validate pytest markers"
    )
    parser.add_argument(
        "--all", action="store_true", help="Run all tests and quality checks"
    )
    parser.add_argument(
        "--ci", action="store_true", help="Run full CI pipeline (all checks)"
    )

    args = parser.parse_args()

    exit_code = 0

    if args.validate_markers or args.all or args.ci:
        exit_code = max(exit_code, validate_markers())

    if args.lint or args.all or args.ci:
        exit_code = max(exit_code, lint_code())

    if args.type_check or args.all or args.ci:
        exit_code = max(exit_code, type_check())

    if args.security or args.all or args.ci:
        exit_code = max(exit_code, security_check())

    if args.unit_only:
        exit_code = max(exit_code, run_unit_tests_only())
    elif args.integration_only:
        exit_code = max(exit_code, run_integration_tests_only())
    elif (
        args.all
        or args.ci
        or not any(
            [
                args.unit_only,
                args.integration_only,
                args.lint,
                args.type_check,
                args.security,
                args.validate_markers,
            ]
        )
    ):
        exit_code = max(exit_code, run_tests())

    if exit_code == 0:
        print("\n✓ All checks passed!")
    else:
        print(f"\n✗ Some checks failed (exit code: {exit_code})")

    sys.exit(exit_code)
