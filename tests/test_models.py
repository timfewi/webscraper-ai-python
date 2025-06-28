"""
Test suite for the models module.

Tests the core data structures used throughout the application.
"""

from datetime import datetime

from src.models import ScrapedData, ScrapingConfig, ScrapingResult


class TestScrapedData:
    """Test cases for ScrapedData dataclass."""

    def test_scraped_data_creation(self):
        """Test basic ScrapedData creation."""
        data = ScrapedData(url="https://example.com")

        assert data.url == "https://example.com"
        assert data.title is None
        assert data.content is None
        assert data.category is None
        assert data.metadata == {}
        assert isinstance(data.timestamp, datetime)
        assert data.status_code == 0
        assert data.quality_score == 0.0

    def test_scraped_data_with_all_fields(self):
        """Test ScrapedData with all fields populated."""
        test_time = datetime.now()
        metadata = {"key": "value"}

        data = ScrapedData(
            url="https://test.com",
            title="Test Title",
            content="Test content",
            category="news",
            metadata=metadata,
            timestamp=test_time,
            status_code=200,
            quality_score=0.95,
        )

        assert data.url == "https://test.com"
        assert data.title == "Test Title"
        assert data.content == "Test content"
        assert data.category == "news"
        assert data.metadata == metadata
        assert data.timestamp == test_time
        assert data.status_code == 200
        assert data.quality_score == 0.95

    def test_scraped_data_post_init(self):
        """Test __post_init__ method behavior."""
        # Test timestamp auto-generation
        data1 = ScrapedData(url="https://example.com")
        assert data1.timestamp is not None
        assert isinstance(data1.timestamp, datetime)

        # Test metadata initialization
        data2 = ScrapedData(url="https://example.com", metadata=None)
        assert data2.metadata == {}

        # Test existing values are preserved
        test_time = datetime(2023, 1, 1)
        test_metadata = {"existing": "data"}
        data3 = ScrapedData(
            url="https://example.com", timestamp=test_time, metadata=test_metadata
        )
        assert data3.timestamp == test_time
        assert data3.metadata == test_metadata


class TestScrapingConfig:
    """Test cases for ScrapingConfig dataclass."""

    def test_scraping_config_defaults(self):
        """Test default configuration values."""
        config = ScrapingConfig()

        assert config.delay_min == 1.0
        assert config.delay_max == 3.0
        assert config.timeout == 30
        assert config.max_retries == 3
        assert "Mozilla/5.0" in config.user_agent
        assert config.max_content_length == 5000
        assert config.rate_limit_enabled is True

    def test_scraping_config_custom_values(self):
        """Test configuration with custom values."""
        config = ScrapingConfig(
            delay_min=0.5,
            delay_max=2.0,
            timeout=60,
            max_retries=5,
            user_agent="Custom Bot/1.0",
            max_content_length=10000,
            rate_limit_enabled=False,
        )

        assert config.delay_min == 0.5
        assert config.delay_max == 2.0
        assert config.timeout == 60
        assert config.max_retries == 5
        assert config.user_agent == "Custom Bot/1.0"
        assert config.max_content_length == 10000
        assert config.rate_limit_enabled is False

    def test_scraping_config_user_agent_factory(self):
        """Test user agent factory function."""
        config1 = ScrapingConfig()
        config2 = ScrapingConfig()

        # Both should have the same default user agent
        assert config1.user_agent == config2.user_agent
        assert "Chrome" in config1.user_agent


class TestScrapingResult:
    """Test cases for ScrapingResult dataclass."""

    def test_scraping_result_success(self):
        """Test successful scraping result."""
        data = ScrapedData(url="https://example.com", title="Test")
        result = ScrapingResult(
            success=True, data=data, error_message=None, retry_count=0
        )

        assert result.success is True
        assert result.data == data
        assert result.error_message is None
        assert result.retry_count == 0

    def test_scraping_result_failure(self):
        """Test failed scraping result."""
        result = ScrapingResult(
            success=False, data=None, error_message="Connection timeout", retry_count=3
        )

        assert result.success is False
        assert result.data is None
        assert result.error_message == "Connection timeout"
        assert result.retry_count == 3

    def test_scraping_result_defaults(self):
        """Test default values for ScrapingResult."""
        result = ScrapingResult(success=True)

        assert result.success is True
        assert result.data is None
        assert result.error_message is None
        assert result.retry_count == 0

    def test_scraping_result_with_retry(self):
        """Test scraping result with retry information."""
        data = ScrapedData(url="https://example.com")
        result = ScrapingResult(success=True, data=data, retry_count=2)

        assert result.success is True
        assert result.data == data
        assert result.retry_count == 2
        assert result.error_message is None
