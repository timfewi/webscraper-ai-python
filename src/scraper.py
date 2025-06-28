"""
Main scraper implementation.

This module provides the main scraper class that orchestrates
all components using dependency injection, following SOLID principles.
"""

import random
import time
from typing import List, Optional

from bs4 import BeautifulSoup
import requests

from .categorizer import ContentCategorizer
from .content_processor import ContentProcessor
from .exporters import DataExporterFactory
from .interfaces import (
    IContentCategorizer,
    IContentProcessor,
    IMetadataExtractor,
    IScraper,
    IURLValidator,
)
from .metadata_extractor import MetadataExtractor
from .models import ScrapedData, ScrapingConfig, ScrapingResult
from .validators import URLValidator


class WebScraper(IScraper):
    """
    Main web scraper that orchestrates all scraping components.

    Uses dependency injection to follow SOLID principles.
    """

    def __init__(
        self,
        config: Optional[ScrapingConfig] = None,
        url_validator: Optional[IURLValidator] = None,
        categorizer: Optional[IContentCategorizer] = None,
        metadata_extractor: Optional[IMetadataExtractor] = None,
        content_processor: Optional[IContentProcessor] = None,
        session: Optional[requests.Session] = None,
    ):
        """
        Initialize the web scraper with dependencies.

        Args:
            config: Scraping configuration
            url_validator: URL validation component
            categorizer: Content categorization component
            metadata_extractor: Metadata extraction component
            content_processor: Content processing component
            session: HTTP session for requests
        """
        self.config = config or ScrapingConfig()

        # Inject dependencies or use defaults
        self.url_validator = url_validator or URLValidator()
        self.categorizer = categorizer or ContentCategorizer()
        self.metadata_extractor = metadata_extractor or MetadataExtractor()
        self.content_processor = content_processor or ContentProcessor()

        # Setup HTTP session
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": self.config.user_agent})
        # Note: requests.Session doesn't have a timeout attribute,
        # we'll pass timeout to individual requests

    def scrape_url(self, url: str) -> ScrapingResult:
        """
        Scrape a single URL.

        Args:
            url: URL to scrape

        Returns:
            ScrapingResult object
        """
        try:
            # Validate URL
            is_valid, message = self.url_validator.validate(url)
            if not is_valid:
                return ScrapingResult(
                    success=False,
                    error_message=f"URL validation failed: {message}",
                    data=None,
                )

            # Make HTTP request
            response = self._make_request(url)
            if not response:
                return ScrapingResult(
                    success=False, error_message="Failed to fetch URL", data=None
                )

            # Process content
            soup = BeautifulSoup(response.text, "html.parser")
            title, clean_content = self.content_processor.process(response.text)

            # Extract metadata
            metadata = self.metadata_extractor.extract(soup, url)

            # Categorize content
            category = self.categorizer.categorize(url, clean_content)

            # Create scraped data object
            scraped_data = ScrapedData(
                url=url,
                title=title,
                content=clean_content,
                category=category,
                metadata=metadata,
            )

            return ScrapingResult(success=True, error_message=None, data=scraped_data)

        except Exception as e:
            return ScrapingResult(
                success=False, error_message=f"Scraping error: {str(e)}", data=None
            )

    def scrape_multiple_urls(self, urls: List[str]) -> List[ScrapingResult]:
        """
        Scrape multiple URLs with rate limiting.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of ScrapingResult objects
        """
        results = []

        for i, url in enumerate(urls):
            # Apply rate limiting with random delay
            if i > 0:
                delay = random.uniform(self.config.delay_min, self.config.delay_max)
                time.sleep(delay)

            result = self.scrape_url(url)
            results.append(result)

            # Respect max URLs limit (if specified in future config)
            # For now, we'll process all URLs provided

        return results

    def export_data(
        self, data: List[ScrapedData], filename: str, format_type: str = "json"
    ) -> str:
        """
        Export scraped data to file.

        Args:
            data: List of scraped data
            filename: Output filename
            format_type: Export format ('json', 'csv', 'xml')

        Returns:
            Path to exported file

        Raises:
            ValueError: If format is not supported
        """
        exporter = DataExporterFactory.create_exporter(format_type)
        return exporter.export(data, filename)

    def _make_request(self, url: str) -> Optional[requests.Response]:
        """
        Make HTTP request with error handling and retries.

        Args:
            url: URL to request

        Returns:
            Response object or None if failed
        """
        for attempt in range(self.config.max_retries):
            try:
                response = self.session.get(
                    url, timeout=self.config.timeout, allow_redirects=True
                )

                # Check if response is successful
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limited
                    wait_time = self.config.delay_min * (
                        2**attempt
                    )  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                else:
                    # Other HTTP errors
                    if attempt == self.config.max_retries - 1:
                        return None
                    time.sleep(self.config.delay_min)

            except requests.exceptions.RequestException:
                if attempt == self.config.max_retries - 1:
                    return None
                time.sleep(self.config.delay_min)

        return None


class ScraperBuilder:
    """
    Builder pattern for creating configured scraper instances.

    Allows flexible configuration of scraper components.
    """

    def __init__(self) -> None:
        """Initialize builder with default values."""
        self._config = ScrapingConfig()
        self._url_validator: Optional[IURLValidator] = None
        self._categorizer: Optional[IContentCategorizer] = None
        self._metadata_extractor: Optional[IMetadataExtractor] = None
        self._content_processor: Optional[IContentProcessor] = None
        self._session: Optional[requests.Session] = None

    def with_config(self, config: ScrapingConfig) -> "ScraperBuilder":
        """Set scraping configuration."""
        self._config = config
        return self

    def with_user_agent(self, user_agent: str) -> "ScraperBuilder":
        """Set custom user agent."""
        self._config.user_agent = user_agent
        return self

    def with_delay_range(self, min_delay: float, max_delay: float) -> "ScraperBuilder":
        """Set delay range between requests."""
        self._config.delay_min = min_delay
        self._config.delay_max = max_delay
        return self

    def with_timeout(self, timeout: int) -> "ScraperBuilder":
        """Set request timeout."""
        self._config.timeout = timeout
        return self

    def with_max_retries(self, max_retries: int) -> "ScraperBuilder":
        """Set maximum retry attempts."""
        self._config.max_retries = max_retries
        return self

    def with_url_validator(self, validator: IURLValidator) -> "ScraperBuilder":
        """Set custom URL validator."""
        self._url_validator = validator
        return self

    def with_categorizer(self, categorizer: IContentCategorizer) -> "ScraperBuilder":
        """Set custom content categorizer."""
        self._categorizer = categorizer
        return self

    def with_metadata_extractor(
        self, extractor: IMetadataExtractor
    ) -> "ScraperBuilder":
        """Set custom metadata extractor."""
        self._metadata_extractor = extractor
        return self

    def with_content_processor(self, processor: IContentProcessor) -> "ScraperBuilder":
        """Set custom content processor."""
        self._content_processor = processor
        return self

    def with_session(self, session: requests.Session) -> "ScraperBuilder":
        """Set custom HTTP session."""
        self._session = session
        return self

    def build(self) -> WebScraper:
        """
        Build the configured scraper instance.

        Returns:
            Configured WebScraper instance
        """
        return WebScraper(
            config=self._config,
            url_validator=self._url_validator,
            categorizer=self._categorizer,
            metadata_extractor=self._metadata_extractor,
            content_processor=self._content_processor,
            session=self._session,
        )
