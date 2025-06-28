"""
Content processing implementation.

This module handles HTML content processing and text extraction,
following the Single Responsibility Principle.
"""

from typing import Optional, Tuple

from bs4 import BeautifulSoup, Tag
import requests

from .interfaces import IContentProcessor


class ContentProcessor(IContentProcessor):
    """Processes HTML content to extract clean text and titles."""

    def __init__(self, session: Optional[requests.Session] = None):
        """
        Initialize the content processor.

        Args:
            session: Optional requests session for consistent configuration
        """
        self.session = session or requests.Session()

        # Tags to exclude from text extraction
        self.excluded_tags = {
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "noscript",
            "form",
            "button",
        }

    def process(self, html_content: str) -> Tuple[str, str]:
        """
        Process HTML content to extract title and clean text.

        Args:
            html_content: Raw HTML content

        Returns:
            Tuple of (title, clean_content)
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            title = self._extract_title(soup)
            clean_text = self._extract_clean_text(soup)

            return title, clean_text

        except Exception as e:
            return f"Error processing content: {str(e)}", ""

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """
        Extract the page title from BeautifulSoup object.

        Args:
            soup: BeautifulSoup parsed HTML

        Returns:
            Page title string
        """
        # Try title tag first
        title_tag = soup.find("title")
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            if title_text:
                return str(title_text)

        # Try h1 as fallback
        h1_tag = soup.find("h1")
        if h1_tag:
            h1_text = h1_tag.get_text(strip=True)
            if h1_text:
                return str(h1_text)

        # Try meta og:title
        og_title = soup.find("meta", property="og:title")
        if isinstance(og_title, Tag):
            content = og_title.get("content")
            if isinstance(content, str):
                return content.strip()

        return "No title found"

    def _extract_clean_text(self, soup: BeautifulSoup) -> str:
        """
        Extract clean text content from BeautifulSoup object.

        Args:
            soup: BeautifulSoup parsed HTML

        Returns:
            Clean text content
        """
        # Remove unwanted tags
        for tag in soup.find_all(self.excluded_tags):
            tag.decompose()

        # Extract text from main content areas first
        main_content = self._extract_main_content(soup)
        if main_content:
            return main_content

        # Fallback to body text
        body = soup.find("body")
        if body:
            return self._clean_text(body.get_text())

        # Final fallback to all text
        return self._clean_text(soup.get_text())

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Try to extract main content from semantic HTML elements.

        Args:
            soup: BeautifulSoup parsed HTML

        Returns:
            Main content text or empty string
        """
        # Priority order for content extraction
        content_selectors = [
            "main",
            "article",
            '[role="main"]',
            ".main-content",
            ".content",
            ".post-content",
            ".entry-content",
            "#main-content",
            "#content",
        ]

        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                return self._clean_text(element.get_text())

        return ""

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Split into lines and clean each
        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            # Strip whitespace
            line = line.strip()

            # Skip empty lines and lines with only special characters
            if line and len(line) > 2 and not line.isspace():
                cleaned_lines.append(line)

        # Join lines with single space
        cleaned_text = " ".join(cleaned_lines)

        # Remove excessive whitespace
        cleaned_text = " ".join(cleaned_text.split())

        # Limit length to prevent memory issues
        if len(cleaned_text) > 10000:
            cleaned_text = cleaned_text[:10000] + "..."

        return cleaned_text
