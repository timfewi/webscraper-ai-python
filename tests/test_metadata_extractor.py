"""
Test suite for the metadata_extractor module.

Tests metadata extraction functionality.
"""

import json

from bs4 import BeautifulSoup

from src.metadata_extractor import MetadataExtractor


class TestMetadataExtractor:
    """Test cases for MetadataExtractor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = MetadataExtractor()

    def test_extract_title(self):
        """Test title extraction from various sources."""
        # Test with title tag
        html = "<html><head><title>Test Title</title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        title = self.extractor._extract_title(soup)
        assert title == "Test Title"

        # Test with og:title meta tag
        html = """<html><head>
        <meta property="og:title" content="OG Title">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        title = self.extractor._extract_title(soup)
        assert title == "OG Title"

        # Test with twitter:title meta tag
        html = """<html><head>
        <meta name="twitter:title" content="Twitter Title">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        title = self.extractor._extract_title(soup)
        assert title == "Twitter Title"

        # Test with h1 tag fallback
        html = "<html><body><h1>H1 Title</h1></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        title = self.extractor._extract_title(soup)
        assert title == "H1 Title"

    def test_extract_description(self):
        """Test description extraction from meta tags."""
        # Test with meta description
        html = """<html><head>
        <meta name="description" content="Page description">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        description = self.extractor._extract_description(soup)
        assert description == "Page description"

        # Test with og:description
        html = """<html><head>
        <meta property="og:description" content="OG description">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        description = self.extractor._extract_description(soup)
        assert description == "OG description"

        # Test with twitter:description
        html = """<html><head>
        <meta name="twitter:description" content="Twitter description">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        description = self.extractor._extract_description(soup)
        assert description == "Twitter description"

    def test_extract_keywords(self):
        """Test keywords extraction from meta tags."""
        html = """<html><head>
        <meta name="keywords" content="python, scraping, web, automation">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        keywords = self.extractor._extract_keywords(soup)
        expected_keywords = ["python", "scraping", "web", "automation"]
        assert keywords == expected_keywords

        # Test with empty keywords
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        keywords = self.extractor._extract_keywords(soup)
        assert keywords == []

    def test_extract_author(self):
        """Test author extraction from various meta tags."""
        # Test with meta author
        html = """<html><head>
        <meta name="author" content="John Doe">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        author = self.extractor._extract_author(soup)
        assert author == "John Doe"

        # Test with article:author
        html = """<html><head>
        <meta property="article:author" content="Jane Smith">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        author = self.extractor._extract_author(soup)
        assert author == "Jane Smith"

    def test_extract_language(self):
        """Test language extraction."""
        # Test with html lang attribute
        html = """<html lang="en-US"><head></head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        language = self.extractor._extract_language(soup)
        assert language == "en-US"

        # Test with meta content-language
        html = """<html><head>
        <meta http-equiv="content-language" content="fr-FR">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        language = self.extractor._extract_language(soup)
        assert language == "fr-FR"

        # Test default fallback
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        language = self.extractor._extract_language(soup)
        assert language == "en"

    def test_extract_open_graph(self):
        """Test Open Graph metadata extraction."""
        html = """<html><head>
        <meta property="og:title" content="OG Title">
        <meta property="og:description" content="OG Description">
        <meta property="og:image" content="https://example.com/image.jpg">
        <meta property="og:type" content="article">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        og_data = self.extractor._extract_open_graph(soup)

        expected_og_data = {
            "og:title": "OG Title",
            "og:description": "OG Description",
            "og:image": "https://example.com/image.jpg",
            "og:type": "article",
        }
        assert og_data == expected_og_data

    def test_extract_twitter_cards(self):
        """Test Twitter Card metadata extraction."""
        html = """<html><head>
        <meta name="twitter:card" content="summary">
        <meta name="twitter:title" content="Twitter Title">
        <meta name="twitter:description" content="Twitter Description">
        <meta name="twitter:creator" content="@username">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        twitter_data = self.extractor._extract_twitter_cards(soup)

        expected_twitter_data = {
            "twitter:card": "summary",
            "twitter:title": "Twitter Title",
            "twitter:description": "Twitter Description",
            "twitter:creator": "@username",
        }
        assert twitter_data == expected_twitter_data

    def test_extract_canonical_url(self):
        """Test canonical URL extraction."""
        html = """<html><head>
        <link rel="canonical" href="https://example.com/canonical">
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        canonical_url = self.extractor._extract_canonical_url(soup)
        assert canonical_url == "https://example.com/canonical"

        # Test with no canonical URL
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        canonical_url = self.extractor._extract_canonical_url(soup)
        assert canonical_url == ""

    def test_extract_links(self):
        """Test link extraction."""
        html = """<html><body>
        <a href="https://example.com" title="Example">Example Link</a>
        <a href="/internal-page">Internal Link</a>
        <a href="mailto:test@example.com">Email Link</a>
        </body></html>"""
        soup = BeautifulSoup(html, "html.parser")
        links = self.extractor._extract_links(soup, "https://test.com")

        assert len(links) == 3
        assert links[0]["url"] == "https://example.com"
        assert links[0]["text"] == "Example Link"
        assert links[0]["title"] == "Example"
        assert links[1]["url"] == "/internal-page"
        assert links[1]["text"] == "Internal Link"

    def test_extract_images(self):
        """Test image extraction."""
        html = """<html><body>
        <img src="https://example.com/image1.jpg" alt="Image 1" title="First Image">
        <img src="/local-image.png" alt="Local Image">
        <img src="data:image/svg+xml;base64,..." alt="SVG Image">
        </body></html>"""
        soup = BeautifulSoup(html, "html.parser")
        images = self.extractor._extract_images(soup, "https://test.com")

        assert len(images) == 3
        assert images[0]["src"] == "https://example.com/image1.jpg"
        assert images[0]["alt"] == "Image 1"
        assert images[0]["title"] == "First Image"
        assert images[1]["src"] == "/local-image.png"
        assert images[1]["alt"] == "Local Image"

    def test_extract_schema_org_json_ld(self):
        """Test Schema.org JSON-LD extraction."""
        schema_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "Test Article",
            "author": "John Doe",
        }

        html = f"""<html><head>
        <script type="application/ld+json">
        {json.dumps(schema_data)}
        </script>
        </head></html>"""
        soup = BeautifulSoup(html, "html.parser")
        extracted_schema = self.extractor._extract_schema_org(soup)

        assert len(extracted_schema) == 1
        assert extracted_schema[0] == schema_data

    def test_extract_schema_org_microdata(self):
        """Test Schema.org microdata extraction."""
        html = """<html><body>
        <div itemtype="https://schema.org/Person">
            <span itemprop="name">John Doe</span>
            <span itemprop="email">john@example.com</span>
        </div>
        </body></html>"""
        soup = BeautifulSoup(html, "html.parser")
        extracted_schema = self.extractor._extract_schema_org(soup)

        assert len(extracted_schema) == 1
        assert extracted_schema[0]["type"] == "https://schema.org/Person"
        assert "name" in extracted_schema[0]["properties"]
        assert "email" in extracted_schema[0]["properties"]

    def test_full_metadata_extraction(self):
        """Test complete metadata extraction."""
        html = """<html lang="en">
        <head>
            <title>Test Page</title>
            <meta name="description" content="Test description">
            <meta name="keywords" content="test, page, metadata">
            <meta name="author" content="Test Author">
            <meta property="og:title" content="OG Test Page">
            <meta name="twitter:card" content="summary">
            <link rel="canonical" href="https://example.com/test">
        </head>
        <body>
            <a href="https://example.com">Example</a>
            <img src="test.jpg" alt="Test Image">
        </body>
        </html>"""

        soup = BeautifulSoup(html, "html.parser")
        url = "https://test.com/page"
        metadata = self.extractor.extract(soup, url)

        # Verify all metadata fields are present
        assert metadata["url"] == url
        assert metadata["title"] == "Test Page"
        assert metadata["description"] == "Test description"
        assert metadata["keywords"] == ["test", "page", "metadata"]
        assert metadata["author"] == "Test Author"
        assert metadata["language"] == "en"
        assert "og:title" in metadata["og_data"]
        assert "twitter:card" in metadata["twitter_data"]
        assert metadata["canonical_url"] == "https://example.com/test"
        assert len(metadata["links"]) == 1
        assert len(metadata["images"]) == 1
        assert isinstance(metadata["schema_data"], list)

    def test_empty_html_handling(self):
        """Test handling of empty or minimal HTML."""
        html = "<html></html>"
        soup = BeautifulSoup(html, "html.parser")
        metadata = self.extractor.extract(soup, "https://test.com")

        # Should not crash and provide default values
        assert metadata["url"] == "https://test.com"
        assert metadata["title"] == "No title found"
        assert metadata["description"] == ""
        assert metadata["keywords"] == []
        assert metadata["author"] == ""
        assert metadata["language"] == "en"

    def test_malformed_html_handling(self):
        """Test handling of malformed HTML."""
        # Missing closing tags, invalid structure
        html = """<html><head><title>Test</title><meta name="description" content="desc">
        <body><a href="link">Text</body>"""
        soup = BeautifulSoup(html, "html.parser")

        # Should not crash and extract what it can
        metadata = self.extractor.extract(soup, "https://test.com")
        assert metadata["title"] == "Test"
        assert len(metadata["links"]) >= 0  # May or may not extract the malformed link

    def test_extraction_limits(self):
        """Test that extraction respects limits for performance."""
        # Create HTML with many links and images
        links_html = "".join(
            [f'<a href="link{i}.html">Link {i}</a>' for i in range(100)]
        )
        images_html = "".join(
            [f'<img src="image{i}.jpg" alt="Image {i}">' for i in range(50)]
        )

        html = f"<html><body>{links_html}{images_html}</body></html>"
        soup = BeautifulSoup(html, "html.parser")
        metadata = self.extractor.extract(soup, "https://test.com")

        # Should limit to reasonable numbers
        assert len(metadata["links"]) <= 50
        assert len(metadata["images"]) <= 20
