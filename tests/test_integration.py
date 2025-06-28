"""
Integration tests for the webscraper package.

These tests verify that all components work together correctly.
"""

from unittest.mock import Mock, patch

import pytest

from src import ScraperBuilder, WebScraper


@pytest.mark.integration
class TestWebScraperIntegration:
    """Integration tests for WebScraper with real components."""

    def test_scraper_with_real_dependencies(self):
        """Test scraper using real dependency instances."""
        scraper = WebScraper()

        # Verify all dependencies are properly instantiated
        assert scraper.url_validator is not None
        assert scraper.categorizer is not None
        assert scraper.metadata_extractor is not None
        assert scraper.content_processor is not None
        assert scraper.session is not None

    @patch("requests.Session.get")
    def test_complete_scraping_workflow(self, mock_get):
        """Test complete workflow from URL validation to data export."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head>
                <title>E-commerce Product Page</title>
                <meta name="description" content="Amazing product for sale">
                <meta property="og:title" content="Best Product Ever">
            </head>
            <body>
                <main>
                    <h1>Product Title</h1>
                    <p>This is an amazing product that you can buy now!</p>
                    <button>Add to Cart</button>
                </main>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        # Create scraper
        scraper = WebScraper()

        # Test scraping
        result = scraper.scrape_url("https://shop.example.com/product/123")

        # Verify successful scraping
        assert result.success is True
        assert result.data is not None

        # Verify data content
        data = result.data
        assert data.url == "https://shop.example.com/product/123"
        assert data.title is not None
        assert "Product" in data.title or "E-commerce" in data.title
        assert data.content is not None
        assert "amazing product" in data.content.lower()
        assert data.category == "ecommerce"  # Should be categorized correctly
        assert isinstance(data.metadata, dict)
        assert data.timestamp is not None

    @patch("requests.Session.get")
    def test_multiple_url_scraping_with_categorization(self, mock_get):
        """Test scraping multiple URLs with different categories."""

        # Setup different mock responses for different URL types
        def mock_response_factory(url, **kwargs):
            response = Mock()
            response.status_code = 200

            if "news" in url:
                response.text = """
                <html><head><title>Breaking News</title></head>
                <body><article><h1>News Article</h1><p>Latest news story here.</p></article></body></html>
                """
            elif "shop" in url:
                response.text = """
                <html><head><title>Product Store</title></head>
                <body><main><h1>Product</h1><p>Buy this product now!</p></main></body></html>
                """
            elif "tech" in url:
                response.text = """
                <html><head><title>Tech Blog</title></head>
                <body><article><h1>Programming Tutorial</h1><p>Learn to code with this guide.</p></article></body></html>
                """
            else:
                response.text = """
                <html><head><title>General Page</title></head>
                <body><p>General content here.</p></body></html>
                """

            return response

        mock_get.side_effect = mock_response_factory

        # Test URLs
        urls = [
            "https://news.example.com/article",
            "https://shop.example.com/product",
            "https://tech.example.com/tutorial",
            "https://example.com/page",
        ]

        scraper = WebScraper()
        results = scraper.scrape_multiple_urls(urls)

        # Verify all succeeded
        assert len(results) == 4
        assert all(result.success for result in results)

        # Verify categorization
        categories = [result.data.category for result in results if result.data]
        assert "news" in categories
        assert "ecommerce" in categories
        assert "technology" in categories
        assert "general" in categories

    def test_scraper_builder_integration(self):
        """Test ScraperBuilder creates properly configured scraper."""
        scraper = (
            ScraperBuilder()
            .with_user_agent("Test Integration Bot/1.0")
            .with_delay_range(0.1, 0.2)
            .with_timeout(10)
            .with_max_retries(1)
            .build()
        )

        # Verify configuration
        assert scraper.config.user_agent == "Test Integration Bot/1.0"
        assert scraper.config.delay_min == 0.1
        assert scraper.config.delay_max == 0.2
        assert scraper.config.timeout == 10
        assert scraper.config.max_retries == 1

        # Verify session is configured
        assert scraper.session.headers["User-Agent"] == "Test Integration Bot/1.0"

    @patch("requests.Session.get")
    def test_data_export_integration(self, mock_get):
        """Test complete workflow including data export."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Test Article</title></head>
            <body><p>Test content for export.</p></body>
        </html>
        """
        mock_get.return_value = mock_response

        scraper = WebScraper()

        # Scrape data
        result = scraper.scrape_url("https://example.com/article")
        assert result.success is True

        # Test export functionality
        data_list = [result.data] if result.data else []

        with patch("src.scraper.DataExporterFactory.create_exporter") as mock_factory:
            mock_exporter = Mock()
            mock_exporter.export.return_value = "/path/to/output.json"
            mock_factory.return_value = mock_exporter

            export_path = scraper.export_data(data_list, "test_output.json", "json")

            assert export_path == "/path/to/output.json"
            mock_factory.assert_called_once_with("json")
            mock_exporter.export.assert_called_once_with(data_list, "test_output.json")

    def test_error_handling_integration(self):
        """Test error handling across the entire system."""
        scraper = WebScraper()

        # Test with blocked domain
        result = scraper.scrape_url("https://facebook.com/page")
        assert result.success is False
        assert result.error_message is not None
        assert "blocked" in result.error_message.lower()

        # Test with invalid URL
        result = scraper.scrape_url("not-a-url")
        assert result.success is False
        assert result.error_message is not None

        # Test with suspicious pattern
        result = scraper.scrape_url("https://example.com/login")
        assert result.success is False
        assert result.error_message is not None

    @patch("requests.Session.get")
    def test_metadata_extraction_integration(self, mock_get):
        """Test that metadata extraction works with real HTML."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html lang="en">
            <head>
                <title>Comprehensive Test Page</title>
                <meta name="description" content="A comprehensive test page with all metadata">
                <meta name="keywords" content="test, integration, metadata">
                <meta name="author" content="Test Author">
                <meta property="og:title" content="OG Test Page">
                <meta property="og:description" content="OpenGraph description">
                <meta name="twitter:card" content="summary">
                <link rel="canonical" href="https://example.com/canonical">
            </head>
            <body>
                <h1>Main Title</h1>
                <p>Content with <a href="https://link.example.com">external link</a></p>
                <img src="test.jpg" alt="Test image">
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        scraper = WebScraper()
        result = scraper.scrape_url("https://example.com/test")

        assert result.success is True
        assert result.data is not None

        metadata = result.data.metadata
        assert isinstance(metadata, dict)
        assert metadata["title"] == "Comprehensive Test Page"
        assert metadata["description"] == "A comprehensive test page with all metadata"
        assert metadata["keywords"] == ["test", "integration", "metadata"]
        assert metadata["author"] == "Test Author"
        assert metadata["language"] == "en"
        assert "og:title" in metadata["og_data"]
        assert "twitter:card" in metadata["twitter_data"]
        assert metadata["canonical_url"] == "https://example.com/canonical"
        assert len(metadata["links"]) > 0
        assert len(metadata["images"]) > 0


@pytest.mark.integration
class TestComponentIntegration:
    """Test integration between individual components."""

    def test_validator_categorizer_integration(self):
        """Test that validator and categorizer work together."""
        from src.categorizer import ContentCategorizer
        from src.validators import URLValidator

        validator = URLValidator()
        categorizer = ContentCategorizer()

        # Test valid ecommerce URL
        url = "https://shop.example.com/product"
        is_valid, message = validator.validate(url)
        assert is_valid

        category = categorizer.categorize(url)
        assert category == "ecommerce"

        # Test invalid URL (should fail validation before categorization)
        invalid_url = "https://facebook.com"
        is_valid, message = validator.validate(invalid_url)
        assert not is_valid
        # Should still be able to categorize (though URL would be rejected)
        category = categorizer.categorize(invalid_url)
        assert category == "social"

    def test_processor_extractor_integration(self):
        """Test content processor and metadata extractor together."""
        from bs4 import BeautifulSoup

        from src.content_processor import ContentProcessor
        from src.metadata_extractor import MetadataExtractor

        processor = ContentProcessor()
        extractor = MetadataExtractor()

        html = """
        <html>
            <head>
                <title>Integration Test</title>
                <meta name="description" content="Testing integration">
            </head>
            <body>
                <main>
                    <h1>Main Content</h1>
                    <p>This is the main content for testing.</p>
                </main>
                <aside>Sidebar content to be excluded</aside>
            </body>
        </html>
        """

        # Process content
        title, content = processor.process(html)
        assert title == "Integration Test"
        assert "Main Content" in content
        assert "Sidebar content" not in content

        # Extract metadata
        soup = BeautifulSoup(html, "html.parser")
        metadata = extractor.extract(soup, "https://example.com")
        assert metadata["title"] == "Integration Test"
        assert metadata["description"] == "Testing integration"
        assert metadata["url"] == "https://example.com"
