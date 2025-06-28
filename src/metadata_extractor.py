"""
Metadata extraction implementation.

This module handles extraction of metadata from web pages,
following the Single Responsibility Principle.
"""

import json
import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup, Tag

from .interfaces import IMetadataExtractor


class MetadataExtractor(IMetadataExtractor):
    """Extracts metadata from HTML content."""

    def extract(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """
        Extract metadata from parsed HTML.

        Args:
            soup: BeautifulSoup object
            url: Original URL

        Returns:
            Dictionary with metadata
        """
        metadata = {
            "url": url,
            "title": self._extract_title(soup),
            "description": self._extract_description(soup),
            "keywords": self._extract_keywords(soup),
            "author": self._extract_author(soup),
            "language": self._extract_language(soup),
            "og_data": self._extract_open_graph(soup),
            "twitter_data": self._extract_twitter_cards(soup),
            "canonical_url": self._extract_canonical_url(soup),
            "links": self._extract_links(soup, url),
            "images": self._extract_images(soup, url),
            "schema_data": self._extract_schema_org(soup),
        }

        return metadata

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        # Try multiple sources for title
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            if title:
                return str(title)

        og_title = soup.find("meta", {"property": "og:title"})
        if isinstance(og_title, Tag) and og_title.get("content"):
            content = og_title.get("content")
            if isinstance(content, str):
                return str(content).strip()

        twitter_title = soup.find("meta", {"name": "twitter:title"})
        if isinstance(twitter_title, Tag) and twitter_title.get("content"):
            content = twitter_title.get("content")
            if isinstance(content, str):
                return str(content).strip()

        h1_tag = soup.find("h1")
        if h1_tag:
            h1_text = h1_tag.get_text(strip=True)
            if h1_text:
                return str(h1_text)

        return "No title found"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description."""
        description_sources = [
            soup.find("meta", {"name": "description"}),
            soup.find("meta", {"property": "og:description"}),
            soup.find("meta", {"name": "twitter:description"}),
        ]

        for source in description_sources:
            if isinstance(source, Tag) and source.get("content"):
                content = source.get("content")
                if isinstance(content, str) and content.strip():
                    return content.strip()

        return ""

    def _extract_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Extract keywords from meta tags."""
        keywords_tag = soup.find("meta", {"name": "keywords"})
        if isinstance(keywords_tag, Tag) and keywords_tag.get("content"):
            content = keywords_tag.get("content")
            if isinstance(content, str):
                keywords = content.split(",")
                return [kw.strip() for kw in keywords if kw.strip()]
        return []

    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract author information."""
        author_sources = [
            soup.find("meta", {"name": "author"}),
            soup.find("meta", {"property": "article:author"}),
            soup.find("meta", {"name": "twitter:creator"}),
        ]

        for source in author_sources:
            if isinstance(source, Tag) and source.get("content"):
                content = source.get("content")
                if isinstance(content, str):
                    return content.strip()

        return ""

    def _extract_language(self, soup: BeautifulSoup) -> str:
        """Extract page language."""
        html_tag = soup.find("html")
        if isinstance(html_tag, Tag) and html_tag.get("lang"):
            lang = html_tag.get("lang")
            if isinstance(lang, str):
                return lang

        lang_meta = soup.find("meta", {"http-equiv": "content-language"})
        if isinstance(lang_meta, Tag) and lang_meta.get("content"):
            content = lang_meta.get("content")
            if isinstance(content, str):
                return content

        return "en"  # Default to English

    def _extract_open_graph(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract Open Graph metadata."""
        og_data = {}
        og_tags = soup.find_all("meta", {"property": re.compile(r"^og:")})

        for tag in og_tags:
            if isinstance(tag, Tag):
                property_name = tag.get("property")
                content = tag.get("content")
                if isinstance(property_name, str) and isinstance(content, str):
                    og_data[property_name] = content

        return og_data

    def _extract_twitter_cards(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract Twitter Card metadata."""
        twitter_data = {}
        twitter_tags = soup.find_all("meta", {"name": re.compile(r"^twitter:")})

        for tag in twitter_tags:
            if isinstance(tag, Tag):
                name = tag.get("name")
                content = tag.get("content")
                if isinstance(name, str) and isinstance(content, str):
                    twitter_data[name] = content

        return twitter_data

    def _extract_canonical_url(self, soup: BeautifulSoup) -> str:
        """Extract canonical URL."""
        canonical_link = soup.find("link", {"rel": "canonical"})
        if isinstance(canonical_link, Tag) and canonical_link.get("href"):
            href = canonical_link.get("href")
            if isinstance(href, str):
                return href
        return ""

    def _extract_links(
        self, soup: BeautifulSoup, base_url: str
    ) -> List[Dict[str, str]]:
        """Extract all links from the page."""
        links = []
        for link in soup.find_all("a", href=True):
            if isinstance(link, Tag):
                href = link.get("href")
                if isinstance(href, str):
                    text = link.get_text(strip=True)
                    title = link.get("title")
                    title_str = title if isinstance(title, str) else ""

                    links.append({"url": href, "text": text, "title": title_str})

        return links[:50]  # Limit to first 50 links

    def _extract_images(
        self, soup: BeautifulSoup, base_url: str
    ) -> List[Dict[str, str]]:
        """Extract image information."""
        images = []
        for img in soup.find_all("img", src=True):
            if isinstance(img, Tag):
                src = img.get("src")
                if isinstance(src, str):
                    alt = img.get("alt")
                    title = img.get("title")

                    alt_str = alt if isinstance(alt, str) else ""
                    title_str = title if isinstance(title, str) else ""

                    images.append({"src": src, "alt": alt_str, "title": title_str})

        return images[:20]  # Limit to first 20 images

    def _extract_schema_org(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract Schema.org structured data."""
        schema_data = []

        # Look for JSON-LD structured data
        json_ld_scripts = soup.find_all("script", {"type": "application/ld+json"})
        for script in json_ld_scripts:
            if isinstance(script, Tag) and script.string:
                try:
                    data = json.loads(script.string)
                    schema_data.append(data)
                except (json.JSONDecodeError, AttributeError):
                    continue

        # Look for microdata
        microdata_items = soup.find_all(attrs={"itemtype": True})
        for item in microdata_items[:5]:  # Limit to first 5 items
            if isinstance(item, Tag):
                itemtype = item.get("itemtype")
                if isinstance(itemtype, str):
                    item_data: Dict[str, Any] = {"type": itemtype, "properties": {}}

                    # Extract itemprop values
                    for prop in item.find_all(attrs={"itemprop": True}):
                        if isinstance(prop, Tag):
                            prop_name = prop.get("itemprop")
                            prop_content = prop.get("content")
                            prop_text = prop.get_text(strip=True)

                            if isinstance(prop_name, str):
                                if isinstance(prop_content, str):
                                    prop_value = prop_content
                                elif prop_text:
                                    prop_value = prop_text
                                else:
                                    continue

                                item_data["properties"][prop_name] = prop_value

                    if item_data["properties"]:
                        schema_data.append(item_data)

        return schema_data
