"""
Content categorization implementation.

This module handles website content categorization,
following the Single Responsibility Principle.
"""

import re
from typing import Optional
from urllib.parse import urlparse

from .interfaces import IContentCategorizer


class ContentCategorizer(IContentCategorizer):
    """Categorizes website content based on URL and content analysis."""

    def __init__(self) -> None:
        """Initialize the categorizer with domain patterns."""
        self.category_patterns = {
            "ecommerce": [
                r"shop",
                r"store",
                r"cart",
                r"buy",
                r"product",
                r"amazon",
                r"ebay",
                r"etsy",
                r"alibaba",
            ],
            "news": [
                r"news",
                r"article",
                r"blog",
                r"post",
                r"story",
                r"cnn",
                r"bbc",
                r"reuters",
                r"nytimes",
            ],
            "education": [
                r"edu",
                r"learn",
                r"course",
                r"tutorial",
                r"academic",
                r"university",
                r"college",
                r"school",
            ],
            "social": [
                r"social",
                r"community",
                r"forum",
                r"discussion",
                r"reddit",
                r"stackoverflow",
                r"quora",
                r"facebook",
                r"twitter",
                r"instagram",
                r"linkedin",
            ],
            "business": [
                r"corp",
                r"company",
                r"business",
                r"enterprise",
                r"corporate",
                r"services",
            ],
            "technology": [
                r"tech",
                r"software",
                r"app",
                r"api",
                r"github",
                r"developer",
                r"programming",
                r"code",
            ],
            "health": [
                r"health",
                r"medical",
                r"doctor",
                r"hospital",
                r"medicine",
                r"wellness",
            ],
            "finance": [
                r"bank",
                r"finance",
                r"money",
                r"investment",
                r"crypto",
                r"trading",
                r"stock",
            ],
        }

    def categorize(self, url: str, content: Optional[str] = None) -> str:
        """
        Categorize website content.

        Args:
            url: The website URL
            content: Optional content to analyze

        Returns:
            Category string
        """
        if not url:
            return "unknown"

        # Parse URL for domain analysis
        try:
            parsed = urlparse(url.lower())
            domain = parsed.netloc
            path = parsed.path
        except Exception:
            domain = url.lower()
            path = ""

        # First, check domain-specific patterns (higher priority)
        for category, patterns in self.category_patterns.items():
            if any(re.search(pattern, domain) for pattern in patterns):
                return category

        # Then check path patterns
        for category, patterns in self.category_patterns.items():
            if any(re.search(pattern, path) for pattern in patterns):
                return category

        # If content is provided, analyze it too
        if content:
            content_category = self._analyze_content(content)
            if content_category != "unknown":
                return content_category

        return "general"

    def _analyze_content(self, content: str) -> str:
        """
        Analyze content text for categorization clues.

        Args:
            content: Text content to analyze

        Returns:
            Category string or 'unknown'
        """
        if not content:
            return "unknown"

        content_lower = content.lower()

        # Count keyword occurrences for each category
        category_scores = {}

        for category, patterns in self.category_patterns.items():
            score = sum(len(re.findall(pattern, content_lower)) for pattern in patterns)
            if score > 0:
                category_scores[category] = score

        # Return category with highest score
        if category_scores:
            return max(category_scores.keys(), key=lambda k: category_scores[k])

        return "unknown"
