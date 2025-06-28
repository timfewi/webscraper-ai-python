"""
Core data models for the web scraper.

This module defines the data structures used throughout the application,
following the Single Responsibility Principle.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class ScrapedData:
    """Data structure for scraped content."""

    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    status_code: int = 0
    quality_score: float = 0.0

    def __post_init__(self) -> None:
        """Initialize default values after creation."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ScrapingConfig:
    """Configuration settings for the web scraper."""

    delay_min: float = 1.0
    delay_max: float = 3.0
    timeout: int = 30
    max_retries: int = 3
    user_agent: str = field(
        default_factory=lambda: (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    )
    max_content_length: int = 5000
    rate_limit_enabled: bool = True


@dataclass
class ScrapingResult:
    """Result of a scraping operation."""

    success: bool
    data: Optional[ScrapedData] = None
    error_message: Optional[str] = None
    retry_count: int = 0
