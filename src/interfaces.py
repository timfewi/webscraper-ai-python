"""
Core interfaces and abstract base classes.

This module defines the contracts for different components,
following the Interface Segregation and Dependency Inversion principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup

from .models import ScrapedData, ScrapingResult


class IURLValidator(ABC):
    """Interface for URL validation."""

    @abstractmethod
    def validate(self, url: str) -> Tuple[bool, str]:
        """
        Validate if a URL is suitable for scraping.

        Args:
            url: The URL to validate

        Returns:
            Tuple of (is_valid, message)
        """
        pass


class IContentCategorizer(ABC):
    """Interface for content categorization."""

    @abstractmethod
    def categorize(self, url: str, content: Optional[str] = None) -> str:
        """
        Categorize website content.

        Args:
            url: The website URL
            content: Optional content to analyze

        Returns:
            Category string
        """
        pass


class IMetadataExtractor(ABC):
    """Interface for metadata extraction."""

    @abstractmethod
    def extract(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """
        Extract metadata from parsed HTML.

        Args:
            soup: BeautifulSoup object
            url: Original URL

        Returns:
            Dictionary with metadata
        """
        pass


class IContentProcessor(ABC):
    """Interface for content processing."""

    @abstractmethod
    def process(self, html_content: str) -> Tuple[str, str]:
        """
        Process HTML content to extract title and clean text.

        Args:
            html_content: Raw HTML content

        Returns:
            Tuple of (title, clean_content)
        """
        pass


class IDataExporter(ABC):
    """Interface for data export."""

    @abstractmethod
    def export(self, data: List[ScrapedData], filename: str) -> str:
        """
        Export scraped data to file.

        Args:
            data: List of scraped data
            filename: Output filename

        Returns:
            Path to exported file
        """
        pass


class IScraper(ABC):
    """Main scraper interface."""

    @abstractmethod
    def scrape_url(self, url: str) -> ScrapingResult:
        """
        Scrape a single URL.

        Args:
            url: URL to scrape

        Returns:
            ScrapingResult object
        """
        pass

    @abstractmethod
    def scrape_multiple_urls(self, urls: List[str]) -> List[ScrapingResult]:
        """
        Scrape multiple URLs.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of ScrapingResult objects
        """
        pass
