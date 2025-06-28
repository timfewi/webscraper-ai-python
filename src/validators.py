"""
URL validation implementation.

This module handles URL validation and safety checks,
following the Single Responsibility Principle.
"""

import re
from typing import Tuple
from urllib.parse import urlparse

from .interfaces import IURLValidator


class URLValidator(IURLValidator):
    """Validates URLs for scraping suitability."""

    MAX_URL_LENGTH = 2048  # Maximum allowed URL length

    def __init__(self) -> None:
        """Initialize the URL validator with blocked domains."""
        self.blocked_domains = {
            "facebook.com",
            "instagram.com",
            "twitter.com",
            "linkedin.com",
            "youtube.com",
            "tiktok.com",
            "pinterest.com",
            "snapchat.com",
        }

        # Pattern for valid URL structure
        self.url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

    def validate(self, url: str) -> Tuple[bool, str]:
        """
        Validate if a URL is suitable for scraping.

        Args:
            url: The URL to validate

        Returns:
            Tuple of (is_valid, message)
        """
        if not url or not isinstance(url, str):
            return False, "URL must be a non-empty string"

        url = url.strip()

        # Check for maximum URL length
        if len(url) > self.MAX_URL_LENGTH:
            return False, "URL exceeds maximum allowed length"

        # Check basic URL format
        if not self.url_pattern.match(url):
            return False, "Invalid URL format"

        try:
            parsed = urlparse(url)

            # Check if scheme is supported
            if parsed.scheme not in ("http", "https"):
                return False, "Only HTTP and HTTPS URLs are supported"

            # Normalize domain by stripping 'www.' prefix if present
            domain = parsed.netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]

            # Check if domain or its subdomain is blocked
            if any(
                domain == blocked or domain.endswith(f".{blocked}")
                for blocked in self.blocked_domains
            ):
                return False, f"Domain {parsed.netloc} is blocked for scraping"

            # Check for suspicious patterns
            if self._has_suspicious_patterns(url):
                return False, "URL contains suspicious patterns"

            return True, "URL is valid for scraping"

        except Exception as e:
            return False, f"URL parsing error: {str(e)}"

    def _has_suspicious_patterns(self, url: str) -> bool:
        """
        Check for suspicious patterns in URL.

        Args:
            url: URL to check

        Returns:
            True if suspicious patterns found
        """
        suspicious_patterns = [
            r"login",
            r"auth",
            r"admin",
            r"private",
            r"\.exe$",
            r"\.zip$",
            r"\.pdf$",
        ]

        url_lower = url.lower()
        return any(re.search(pattern, url_lower) for pattern in suspicious_patterns)
