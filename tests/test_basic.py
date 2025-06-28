"""
Basic functionality tests for the webscraper project.

These tests verify that the package can be imported and basic functionality works.
"""

import pytest


def test_basic_functionality():
    """Test that basic Python functionality works."""
    assert 1 + 1 == 2


def test_import_statements():
    """Test that required packages can be imported."""
    try:
        import bs4  # noqa: F401
        import numpy as np  # noqa: F401
        import pandas as pd  # noqa: F401
        import requests  # noqa: F401

        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required package: {e}")


def test_src_package_import():
    """Test that the src package can be imported."""
    try:
        import src

        assert hasattr(src, "WebScraper")
        assert hasattr(src, "ScraperBuilder")
        assert hasattr(src, "ScrapedData")
        assert hasattr(src, "ScrapingConfig")
        assert hasattr(src, "ScrapingResult")
    except ImportError as e:
        pytest.fail(f"Failed to import src package: {e}")


def test_individual_modules_import():
    """Test that individual modules can be imported."""
    modules_to_test = [
        "src.models",
        "src.interfaces",
        "src.validators",
        "src.categorizer",
        "src.metadata_extractor",
        "src.content_processor",
        "src.exporters",
        "src.scraper",
    ]

    for module_name in modules_to_test:
        try:
            __import__(module_name)
        except ImportError as e:
            pytest.fail(f"Failed to import {module_name}: {e}")


def test_package_version():
    """Test that package version is accessible."""
    try:
        import src

        assert hasattr(src, "__version__")
        assert isinstance(src.__version__, str)
        assert len(src.__version__) > 0
    except ImportError as e:
        pytest.fail(f"Failed to access package version: {e}")


class TestBasicWebscraperFunctionality:
    """Basic functionality tests for webscraper components."""

    def test_scraper_instantiation(self):
        """Test that WebScraper can be instantiated."""
        from src import WebScraper

        scraper = WebScraper()
        assert scraper is not None
        assert hasattr(scraper, "scrape_url")
        assert hasattr(scraper, "scrape_multiple_urls")
        assert hasattr(scraper, "export_data")

    def test_builder_instantiation(self):
        """Test that ScraperBuilder can be instantiated."""
        from src import ScraperBuilder

        builder = ScraperBuilder()
        assert builder is not None
        assert hasattr(builder, "build")
        assert hasattr(builder, "with_user_agent")
        assert hasattr(builder, "with_timeout")

    def test_data_models_instantiation(self):
        """Test that data models can be instantiated."""
        from src import ScrapedData, ScrapingConfig, ScrapingResult

        # Test ScrapedData
        data = ScrapedData(url="https://example.com")
        assert data.url == "https://example.com"

        # Test ScrapingConfig
        config = ScrapingConfig()
        assert config.timeout > 0
        assert config.max_retries > 0

        # Test ScrapingResult
        result = ScrapingResult(success=True)
        assert result.success is True

    def test_validators_basic_functionality(self):
        """Test basic validator functionality."""
        from src import URLValidator

        validator = URLValidator()

        # Test valid URL
        is_valid, message = validator.validate("https://example.com")
        assert isinstance(is_valid, bool)
        assert isinstance(message, str)

        # Test invalid URL
        is_valid, message = validator.validate("not-a-url")
        assert is_valid is False
        assert len(message) > 0

    def test_categorizer_basic_functionality(self):
        """Test basic categorizer functionality."""
        from src import ContentCategorizer

        categorizer = ContentCategorizer()

        # Test categorization
        category = categorizer.categorize("https://shop.example.com")
        assert isinstance(category, str)
        assert len(category) > 0

    def test_exporters_basic_functionality(self):
        """Test basic exporter functionality."""
        from src import DataExporterFactory

        # Test supported formats
        formats = DataExporterFactory.get_supported_formats()
        assert isinstance(formats, list)
        assert len(formats) > 0
        assert "json" in formats

        # Test exporter creation
        exporter = DataExporterFactory.create_exporter("json")
        assert exporter is not None
        assert hasattr(exporter, "export")

    def test_string_operations(self):
        """Test basic string operations that might be used in scraping."""
        test_html = "<title>Test Title</title>"
        assert "Test Title" in test_html
        assert test_html.startswith("<title>")
        assert test_html.endswith("</title>")

    def test_beautifulsoup_basic_functionality(self):
        """Test that BeautifulSoup works as expected."""
        from bs4 import BeautifulSoup

        html = (
            "<html><head><title>Test</title></head><body><p>Content</p></body></html>"
        )
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("title")
        assert title is not None
        assert title.get_text() == "Test"

        p_tag = soup.find("p")
        assert p_tag is not None
        assert p_tag.get_text() == "Content"

    def test_requests_mock_functionality(self):
        """Test that requests functionality works for testing."""
        from unittest.mock import Mock

        # Test that we can mock requests
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>Mock content</html>"

        assert mock_response.status_code == 200
        assert "Mock content" in mock_response.text
