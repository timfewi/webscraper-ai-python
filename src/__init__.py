"""
Intelligent Web Scraper Package

A modular, SOLID-principles-based web scraper built with dependency injection.
Provides flexible components for URL validation, content processing, categorization,
metadata extraction, and data export.

Example:
    Basic usage:
    ```python
    from src import WebScraper, ScraperBuilder

    # Simple usage
    scraper = WebScraper()
    result = scraper.scrape_url("https://example.com")

    # Advanced configuration with builder
    scraper = (ScraperBuilder()
               .with_delay_range(1.0, 3.0)
               .with_timeout(60)
               .with_user_agent("Custom Bot/1.0")
               .build())

    results = scraper.scrape_multiple_urls(["https://site1.com", "https://site2.com"])

    # Export data
    successful_data = [r.data for r in results if r.success and r.data]
    scraper.export_data(successful_data, "output.json", "json")
    ```

Components:
    - WebScraper: Main scraper orchestrator
    - ScraperBuilder: Builder pattern for configuration
    - ScrapedData: Data structure for scraped content
    - ScrapingConfig: Configuration settings
    - ScrapingResult: Operation result wrapper

Interfaces (for custom implementations):
    - IScraper: Main scraper interface
    - IURLValidator: URL validation interface
    - IContentCategorizer: Content categorization interface
    - IMetadataExtractor: Metadata extraction interface
    - IContentProcessor: Content processing interface
    - IDataExporter: Data export interface

Individual Components (for advanced usage):
    - URLValidator: Default URL validation
    - ContentCategorizer: Default content categorization
    - MetadataExtractor: Default metadata extraction
    - ContentProcessor: Default content processing
    - DataExporterFactory: Factory for data exporters
"""

from .ai_enhanced_scraper import AIEnhancedWebScraper
from .categorizer import ContentCategorizer
from .config import Config
from .content_processor import ContentProcessor
from .exporters import CSVExporter, DataExporterFactory, JSONExporter, XMLExporter
from .intelligent_webscraper import IntelligentWebScraper, WebScraperConfig

# Interfaces (for dependency injection and custom implementations)
from .interfaces import (
    IContentCategorizer,
    IContentProcessor,
    IDataExporter,
    IMetadataExtractor,
    IScraper,
    IURLValidator,
)
from .metadata_extractor import MetadataExtractor

# Data models
from .models import ScrapedData, ScrapingConfig, ScrapingResult
from .prompt_engineer import ContentAnalysis, PromptConfig, PromptEngineer

# Main scraper components
from .scraper import ScraperBuilder, WebScraper

# Individual components (for advanced usage)
from .validators import URLValidator

# Enhanced imports for AI-powered scraping

__version__ = "2.0.0"
__all__ = [
    # Main components
    "WebScraper",
    "ScraperBuilder",
    # AI-Enhanced components
    "AIEnhancedWebScraper",
    "IntelligentWebScraper",
    "PromptEngineer",
    # Configuration
    "Config",
    "WebScraperConfig",
    "PromptConfig",
    # Data models
    "ScrapedData",
    "ScrapingConfig",
    "ScrapingResult",
    "ContentAnalysis",
    # Interfaces
    "IScraper",
    "IURLValidator",
    "IContentCategorizer",
    "IMetadataExtractor",
    "IContentProcessor",
    "IDataExporter",
    # Individual components
    "URLValidator",
    "ContentCategorizer",
    "MetadataExtractor",
    "ContentProcessor",
    "DataExporterFactory",
    "CSVExporter",
    "JSONExporter",
    "XMLExporter",
]
