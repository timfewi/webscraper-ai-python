"""
Test suite for the scraper module.

Tests the main web scraper functionality and builder pattern.
"""

from unittest.mock import Mock, patch

import requests

from src.interfaces import (
    IContentCategorizer,
    IContentProcessor,
    IDataExporter,
    IMetadataExtractor,
    IURLValidator,
)
from src.models import ScrapedData, ScrapingConfig
from src.scraper import ScraperBuilder, WebScraper


class TestWebScraper:
    """Test cases for WebScraper class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_validator = Mock(spec=IURLValidator)
        self.mock_categorizer = Mock(spec=IContentCategorizer)
        self.mock_metadata_extractor = Mock(spec=IMetadataExtractor)
        self.mock_content_processor = Mock(spec=IContentProcessor)
        self.mock_session = Mock()
        self.mock_session.headers = {}  # Add headers dict to mock
        self.scraper = WebScraper(
            url_validator=self.mock_validator,
            categorizer=self.mock_categorizer,
            metadata_extractor=self.mock_metadata_extractor,
            content_processor=self.mock_content_processor,
            session=self.mock_session,
        )

    def test_scraper_initialization_with_defaults(self):
        """Test scraper initialization with default dependencies."""
        scraper = WebScraper()

        assert scraper.config is not None
        assert scraper.url_validator is not None
        assert scraper.categorizer is not None
        assert scraper.metadata_extractor is not None
        assert scraper.content_processor is not None
        assert scraper.session is not None

    def test_scraper_initialization_with_custom_config(self):
        """Test scraper initialization with custom configuration."""
        config = ScrapingConfig(delay_min=0.5, delay_max=2.0, timeout=60, max_retries=5)
        scraper = WebScraper(config=config)

        assert scraper.config == config
        assert scraper.config.delay_min == 0.5
        assert scraper.config.delay_max == 2.0
        assert scraper.config.timeout == 60
        assert scraper.config.max_retries == 5

    def test_scrape_url_success(self):
        """Test successful URL scraping."""
        url = "https://example.com"
        mock_response = Mock()
        mock_response.text = (
            "<html><head><title>Test</title></head><body>Content</body></html>"
        )
        mock_response.status_code = 200

        # Setup mocks
        self.mock_validator.validate.return_value = (True, "Valid URL")
        self.mock_session.get.return_value = mock_response
        self.mock_content_processor.process.return_value = (
            "Test Title",
            "Clean content",
        )
        self.mock_metadata_extractor.extract.return_value = {"meta": "data"}
        self.mock_categorizer.categorize.return_value = "news"

        result = self.scraper.scrape_url(url)

        assert result.success is True
        assert result.error_message is None
        assert result.data is not None
        assert result.data.url == url
        assert result.data.title == "Test Title"
        assert result.data.content == "Clean content"
        assert result.data.category == "news"
        assert result.data.metadata == {"meta": "data"}

        # Verify method calls
        self.mock_validator.validate.assert_called_once_with(url)
        self.mock_session.get.assert_called_once()
        self.mock_content_processor.process.assert_called_once()
        self.mock_metadata_extractor.extract.assert_called_once()
        self.mock_categorizer.categorize.assert_called_once()

    def test_scrape_url_validation_failure(self):
        """Test URL scraping with validation failure."""
        url = "invalid-url"
        self.mock_validator.validate.return_value = (False, "Invalid URL format")

        result = self.scraper.scrape_url(url)

        assert result.success is False
        assert result.error_message is not None
        assert "URL validation failed" in result.error_message
        assert result.data is None

        # Should not make HTTP request if validation fails
        self.mock_session.get.assert_not_called()

    def test_scrape_url_http_failure(self):
        """Test URL scraping with HTTP request failure."""
        url = "https://example.com"
        self.mock_validator.validate.return_value = (True, "Valid URL")

        # Mock HTTP failure
        with patch.object(self.scraper, "_make_request", return_value=None):
            result = self.scraper.scrape_url(url)

            assert result.success is False
            assert result.error_message is not None
            assert "Failed to fetch URL" in result.error_message
            assert result.data is None

    def test_scrape_url_processing_exception(self):
        """Test URL scraping with processing exception."""
        url = "https://example.com"
        mock_response = Mock()
        mock_response.text = "<html>Valid HTML</html>"
        mock_response.status_code = 200

        self.mock_validator.validate.return_value = (True, "Valid URL")
        self.mock_session.get.return_value = mock_response
        self.mock_content_processor.process.side_effect = Exception("Processing error")

        result = self.scraper.scrape_url(url)

        assert result.success is False
        assert result.error_message is not None
        assert "Scraping error" in result.error_message
        assert result.data is None

    @patch("time.sleep")
    def test_scrape_multiple_urls(self, mock_sleep):
        """Test scraping multiple URLs with rate limiting."""
        urls = ["https://example1.com", "https://example2.com", "https://example3.com"]

        # Mock successful responses
        mock_response = Mock()
        mock_response.text = "<html><title>Test</title><body>Content</body></html>"
        mock_response.status_code = 200

        self.mock_validator.validate.return_value = (True, "Valid URL")
        self.mock_session.get.return_value = mock_response
        self.mock_content_processor.process.return_value = ("Title", "Content")
        self.mock_metadata_extractor.extract.return_value = {}
        self.mock_categorizer.categorize.return_value = "general"

        results = self.scraper.scrape_multiple_urls(urls)

        assert len(results) == 3
        assert all(result.success for result in results)

        # Should have called sleep between requests (not before first)
        assert mock_sleep.call_count == 2

        # Verify all URLs were processed
        assert self.mock_validator.validate.call_count == 3
        assert self.mock_session.get.call_count == 3

    def test_export_data(self):
        """Test data export functionality."""
        data = [ScrapedData(url="https://example.com", title="Test", content="Content")]

        mock_exporter = Mock(spec=IDataExporter)
        mock_exporter.export.return_value = "/path/to/exported/file.json"

        with patch(
            "src.scraper.DataExporterFactory.create_exporter",
            return_value=mock_exporter,
        ):
            result_path = self.scraper.export_data(data, "output.json", "json")

            assert result_path == "/path/to/exported/file.json"
            mock_exporter.export.assert_called_once_with(data, "output.json")

    def test_make_request_success(self):
        """Test successful HTTP request."""
        url = "https://example.com"
        mock_response = Mock()
        mock_response.status_code = 200

        self.mock_session.get.return_value = mock_response

        response = self.scraper._make_request(url)

        assert response == mock_response
        self.mock_session.get.assert_called_once_with(
            url, timeout=30, allow_redirects=True
        )

    @patch("time.sleep")
    def test_make_request_with_retries(self, mock_sleep):
        """Test HTTP request with retries on failure."""
        url = "https://example.com"

        # Mock first two attempts to fail, third to succeed
        mock_response_fail = Mock()
        mock_response_fail.status_code = 500
        mock_response_success = Mock()
        mock_response_success.status_code = 200

        self.mock_session.get.side_effect = [
            mock_response_fail,
            mock_response_fail,
            mock_response_success,
        ]

        response = self.scraper._make_request(url)

        assert response == mock_response_success
        assert self.mock_session.get.call_count == 3
        assert mock_sleep.call_count == 2  # Sleep between retries

    @patch("time.sleep")
    def test_make_request_rate_limit_handling(self, mock_sleep):
        """Test HTTP request handling of rate limits (429 status)."""
        url = "https://example.com"

        # Mock rate limit response followed by success
        mock_response_rate_limit = Mock()
        mock_response_rate_limit.status_code = 429
        mock_response_success = Mock()
        mock_response_success.status_code = 200

        self.mock_session.get.side_effect = [
            mock_response_rate_limit,
            mock_response_success,
        ]

        response = self.scraper._make_request(url)

        assert response == mock_response_success
        assert self.mock_session.get.call_count == 2
        mock_sleep.assert_called_once()  # Exponential backoff sleep

    def test_make_request_max_retries_exceeded(self):
        """Test HTTP request when max retries are exceeded."""
        url = "https://example.com"

        # Mock all attempts to fail
        self.mock_session.get.side_effect = requests.exceptions.ConnectionError(
            "Connection failed"
        )

        with patch("time.sleep"):
            response = self.scraper._make_request(url)

            assert response is None
            assert self.mock_session.get.call_count == 3  # Default max_retries

    def test_session_configuration(self):
        """Test that session is properly configured with user agent."""
        config = ScrapingConfig(user_agent="Custom Bot/1.0")
        scraper = WebScraper(config=config)

        assert scraper.session.headers["User-Agent"] == "Custom Bot/1.0"


class TestScraperBuilder:
    """Test cases for ScraperBuilder class."""

    def test_builder_initialization(self):
        """Test builder initialization with defaults."""
        builder = ScraperBuilder()

        assert builder._config is not None
        assert isinstance(builder._config, ScrapingConfig)
        assert builder._url_validator is None
        assert builder._categorizer is None
        assert builder._metadata_extractor is None
        assert builder._content_processor is None
        assert builder._session is None

    def test_builder_with_config(self):
        """Test builder with custom configuration."""
        custom_config = ScrapingConfig(timeout=60)
        builder = ScraperBuilder()

        result_builder = builder.with_config(custom_config)

        assert result_builder == builder  # Should return self for chaining
        assert builder._config == custom_config

    def test_builder_with_user_agent(self):
        """Test builder user agent configuration."""
        builder = ScraperBuilder()
        user_agent = "Custom Bot/2.0"

        result_builder = builder.with_user_agent(user_agent)

        assert result_builder == builder
        assert builder._config.user_agent == user_agent

    def test_builder_with_delay_range(self):
        """Test builder delay range configuration."""
        builder = ScraperBuilder()

        result_builder = builder.with_delay_range(0.5, 2.5)

        assert result_builder == builder
        assert builder._config.delay_min == 0.5
        assert builder._config.delay_max == 2.5

    def test_builder_with_timeout(self):
        """Test builder timeout configuration."""
        builder = ScraperBuilder()

        result_builder = builder.with_timeout(45)

        assert result_builder == builder
        assert builder._config.timeout == 45

    def test_builder_with_max_retries(self):
        """Test builder max retries configuration."""
        builder = ScraperBuilder()

        result_builder = builder.with_max_retries(5)

        assert result_builder == builder
        assert builder._config.max_retries == 5

    def test_builder_with_custom_dependencies(self):
        """Test builder with custom dependency injection."""
        builder = ScraperBuilder()
        mock_validator = Mock(spec=IURLValidator)
        mock_categorizer = Mock(spec=IContentCategorizer)
        mock_extractor = Mock(spec=IMetadataExtractor)
        mock_processor = Mock(spec=IContentProcessor)
        mock_session = Mock(spec=requests.Session)

        result_builder = (
            builder.with_url_validator(mock_validator)
            .with_categorizer(mock_categorizer)
            .with_metadata_extractor(mock_extractor)
            .with_content_processor(mock_processor)
            .with_session(mock_session)
        )

        assert result_builder == builder
        assert builder._url_validator == mock_validator
        assert builder._categorizer == mock_categorizer
        assert builder._metadata_extractor == mock_extractor
        assert builder._content_processor == mock_processor
        assert builder._session == mock_session

    def test_builder_build_with_defaults(self):
        """Test building scraper with default dependencies."""
        builder = ScraperBuilder()
        scraper = builder.build()

        assert isinstance(scraper, WebScraper)
        assert scraper.config == builder._config
        assert scraper.url_validator is not None  # Should use default
        assert scraper.categorizer is not None
        assert scraper.metadata_extractor is not None
        assert scraper.content_processor is not None
        assert scraper.session is not None

    def test_builder_build_with_custom_dependencies(self):
        """Test building scraper with custom dependencies."""
        builder = ScraperBuilder()
        mock_validator = Mock(spec=IURLValidator)
        mock_categorizer = Mock(spec=IContentCategorizer)

        scraper = (
            builder.with_url_validator(mock_validator)
            .with_categorizer(mock_categorizer)
            .build()
        )

        assert isinstance(scraper, WebScraper)
        assert scraper.url_validator == mock_validator
        assert scraper.categorizer == mock_categorizer

    def test_builder_method_chaining(self):
        """Test that all builder methods can be chained."""
        builder = ScraperBuilder()

        result = (
            builder.with_user_agent("Test Bot")
            .with_delay_range(0.1, 0.5)
            .with_timeout(30)
            .with_max_retries(2)
        )

        assert result == builder
        assert builder._config.user_agent == "Test Bot"
        assert builder._config.delay_min == 0.1
        assert builder._config.delay_max == 0.5
        assert builder._config.timeout == 30
        assert builder._config.max_retries == 2

    def test_builder_fluent_interface_complete_example(self):
        """Test complete builder usage with fluent interface."""
        scraper = (
            ScraperBuilder()
            .with_user_agent("Integration Test Bot/1.0")
            .with_delay_range(0.5, 1.5)
            .with_timeout(45)
            .with_max_retries(2)
            .build()
        )

        assert isinstance(scraper, WebScraper)
        assert scraper.config.user_agent == "Integration Test Bot/1.0"
        assert scraper.config.delay_min == 0.5
        assert scraper.config.delay_max == 1.5
        assert scraper.config.timeout == 45
        assert scraper.config.max_retries == 2


class TestScraperIntegration:
    """Integration tests for scraper functionality."""

    @patch("requests.Session.get")
    def test_end_to_end_scraping_flow(self, mock_get):
        """Test complete scraping flow from URL to result."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head>
                <title>Test News Article</title>
                <meta name="description" content="Test article description">
            </head>
            <body>
                <article>
                    <h1>Breaking News</h1>
                    <p>This is the content of the news article.</p>
                </article>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        # Create scraper with real dependencies
        scraper = WebScraper()

        # Test scraping
        result = scraper.scrape_url("https://news.example.com/article")

        assert result.success is True
        assert result.data is not None
        assert result.data.url == "https://news.example.com/article"
        assert result.data.title is not None
        assert "Test News Article" in result.data.title
        assert result.data.content is not None
        assert (
            "Breaking News" in result.data.content
            or "news article" in result.data.content
        )
        assert result.data.category == "news"  # Should be categorized as news
        assert isinstance(result.data.metadata, dict)

    def test_scraper_with_invalid_urls(self):
        """Test scraper behavior with various invalid URLs."""
        scraper = WebScraper()

        invalid_urls = [
            "",
            "not-a-url",
            "https://facebook.com",  # Blocked domain
            "https://example.com/login",  # Suspicious pattern
        ]

        for url in invalid_urls:
            result = scraper.scrape_url(url)
            assert result.success is False
            assert result.data is None
            assert result.error_message is not None
