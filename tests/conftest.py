"""
Test configuration and utilities for the webscraper project.
"""

from pathlib import Path
import sys

import pytest

# Add project root to Python path for testing
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Also add to PYTHONPATH environment variable
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (deselect with '-m \"not unit\"')"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests (deselect with '-m \"not integration\"')",
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


# Common test fixtures
@pytest.fixture
def sample_html():
    """Provide sample HTML for testing."""
    return """
    <html>
        <head>
            <title>Sample Page</title>
            <meta name="description" content="This is a sample page for testing">
            <meta name="keywords" content="test, sample, html">
            <meta property="og:title" content="OG Sample Page">
        </head>
        <body>
            <header>
                <nav>
                    <a href="/home">Home</a>
                    <a href="/about">About</a>
                </nav>
            </header>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content of the page.</p>
                <p>It contains multiple paragraphs for testing.</p>
            </main>
            <footer>
                <p>Footer content</p>
            </footer>
        </body>
    </html>
    """


@pytest.fixture
def sample_urls():
    """Provide sample URLs for testing."""
    return [
        "https://example.com",
        "https://news.example.com/article",
        "https://shop.example.com/product",
        "https://tech.example.com/blog",
        "https://health.example.com/guide",
    ]


@pytest.fixture
def invalid_urls():
    """Provide invalid URLs for testing."""
    return [
        "",
        "not-a-url",
        "ftp://example.com",
        "https://facebook.com",
        "https://example.com/login",
        "https://example.com/file.exe",
    ]
