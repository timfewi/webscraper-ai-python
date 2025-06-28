"""
Test suite for the content_processor module.

Tests HTML content processing and text extraction functionality.
"""

from unittest.mock import Mock

from bs4 import BeautifulSoup
import requests

from src.content_processor import ContentProcessor


class TestContentProcessor:
    """Test cases for ContentProcessor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.processor = ContentProcessor()

    def test_process_basic_html(self):
        """Test processing of basic HTML content."""
        html = """<html>
        <head><title>Test Title</title></head>
        <body>
            <h1>Main Heading</h1>
            <p>This is a paragraph of text.</p>
            <p>Another paragraph with more content.</p>
        </body>
        </html>"""

        title, content = self.processor.process(html)

        assert title == "Test Title"
        assert "Main Heading" in content
        assert "This is a paragraph of text." in content
        assert "Another paragraph with more content." in content

    def test_process_html_with_excluded_tags(self):
        """Test that excluded tags are removed from content."""
        html = """<html>
        <head><title>Test Title</title></head>
        <body>
            <p>Visible content</p>
            <script>alert('hidden');</script>
            <style>body { color: red; }</style>
            <nav>Navigation menu</nav>
            <header>Header content</header>
            <footer>Footer content</footer>
            <aside>Sidebar content</aside>
            <noscript>No JS content</noscript>
            <form>Form content</form>
            <button>Button text</button>
            <p>More visible content</p>
        </body>
        </html>"""

        title, content = self.processor.process(html)

        assert title == "Test Title"
        assert "Visible content" in content
        assert "More visible content" in content
        # Excluded content should not be present
        assert "alert('hidden')" not in content
        assert "color: red" not in content
        assert "Navigation menu" not in content
        assert "Header content" not in content
        assert "Footer content" not in content
        assert "Sidebar content" not in content
        assert "No JS content" not in content
        assert "Form content" not in content
        assert "Button text" not in content

    def test_extract_title_priority(self):
        """Test title extraction priority order."""
        # Test with title tag (highest priority)
        html = """<html>
        <head>
            <title>Title Tag</title>
            <meta property="og:title" content="OG Title">
        </head>
        <body><h1>H1 Title</h1></body>
        </html>"""
        soup = BeautifulSoup(html, "html.parser")
        title = self.processor._extract_title(soup)
        assert title == "Title Tag"

        # Test with h1 fallback when no title tag
        html = """<html>
        <head><meta property="og:title" content="OG Title"></head>
        <body><h1>H1 Title</h1></body>
        </html>"""
        soup = BeautifulSoup(html, "html.parser")
        title = self.processor._extract_title(soup)
        assert title == "H1 Title"

        # Test with og:title when no title or h1
        html = """<html>
        <head><meta property="og:title" content="OG Title"></head>
        <body></body>
        </html>"""
        soup = BeautifulSoup(html, "html.parser")
        title = self.processor._extract_title(soup)
        assert title == "OG Title"

        # Test fallback when nothing is found
        html = "<html><head></head><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        title = self.processor._extract_title(soup)
        assert title == "No title found"

    def test_extract_main_content_semantic(self):
        """Test main content extraction from semantic HTML elements."""
        # Test with main tag
        html = """<html><body>
        <header>Header content</header>
        <main>
            <h1>Main Content Title</h1>
            <p>This is the main content of the page.</p>
        </main>
        <footer>Footer content</footer>
        </body></html>"""
        soup = BeautifulSoup(html, "html.parser")
        main_content = self.processor._extract_main_content(soup)
        assert "Main Content Title" in main_content
        assert "This is the main content" in main_content
        assert "Header content" not in main_content
        assert "Footer content" not in main_content

        # Test with article tag
        html = """<html><body>
        <nav>Navigation</nav>
        <article>
            <h2>Article Title</h2>
            <p>Article content goes here.</p>
        </article>
        </body></html>"""
        soup = BeautifulSoup(html, "html.parser")
        main_content = self.processor._extract_main_content(soup)
        assert "Article Title" in main_content
        assert "Article content goes here" in main_content
        assert "Navigation" not in main_content

        # Test with role="main"
        html = """<html><body>
        <div role="main">
            <h1>Main Role Content</h1>
            <p>Content with main role.</p>
        </div>
        </body></html>"""
        soup = BeautifulSoup(html, "html.parser")
        main_content = self.processor._extract_main_content(soup)
        assert "Main Role Content" in main_content
        assert "Content with main role" in main_content

    def test_extract_main_content_css_classes(self):
        """Test main content extraction using CSS classes."""
        html = """<html><body>
        <div class="sidebar">Sidebar content</div>
        <div class="main-content">
            <h1>Main Content</h1>
            <p>This is the main content area.</p>
        </div>
        </body></html>"""
        soup = BeautifulSoup(html, "html.parser")
        main_content = self.processor._extract_main_content(soup)
        assert "Main Content" in main_content
        assert "This is the main content area" in main_content
        assert "Sidebar content" not in main_content

    def test_clean_text_functionality(self):
        """Test text cleaning and normalization."""
        # Test with excessive whitespace
        text = """

        Line 1 with    multiple    spaces


        Line 2 with tabs	and	more	spaces


        Line 3 normal text


        """
        cleaned = self.processor._clean_text(text)
        assert (
            cleaned
            == "Line 1 with multiple spaces Line 2 with tabs and more spaces Line 3 normal text"
        )

        # Test with short/empty lines
        text = "Good line\n\n\na\n  \nAnother good line"
        cleaned = self.processor._clean_text(text)
        assert cleaned == "Good line Another good line"

        # Test empty text
        cleaned = self.processor._clean_text("")
        assert cleaned == ""

        # Test with whitespace only
        cleaned = self.processor._clean_text("   ")
        assert cleaned == ""

    def test_clean_text_length_limit(self):
        """Test that clean text respects length limits."""
        # Create very long text
        long_text = "A" * 15000
        cleaned = self.processor._clean_text(long_text)
        assert len(cleaned) <= 10003  # 10000 + "..." = 10003
        assert cleaned.endswith("...")

    def test_process_with_custom_session(self):
        """Test processor initialization with custom session."""
        custom_session = Mock(spec=requests.Session)
        processor = ContentProcessor(session=custom_session)
        assert processor.session == custom_session

    def test_process_error_handling(self):
        """Test error handling during content processing."""
        # Test with invalid HTML that might cause parsing errors
        invalid_html = "<<<invalid>>>html<<<"
        title, content = self.processor.process(invalid_html)

        # Should not crash and provide some output
        assert isinstance(title, str)
        assert isinstance(content, str)

    def test_process_empty_html(self):
        """Test processing of empty or minimal HTML."""
        # Test completely empty
        title, content = self.processor.process("")
        assert "No title found" in title
        assert content == ""

        # Test minimal HTML
        title, content = self.processor.process("<html></html>")
        assert title == "No title found"
        assert content == ""

    def test_extract_main_content_fallback(self):
        """Test main content extraction fallback behavior."""
        # HTML without semantic elements or recognized classes
        html = """<html><body>
        <div class="unknown-class">
            <p>Some content here</p>
            <p>More content here</p>
        </div>
        </body></html>"""
        soup = BeautifulSoup(html, "html.parser")

        # Should fall back to body content
        main_content = self.processor._extract_main_content(soup)
        assert main_content == ""  # No semantic elements found

        # But full processing should still work via body fallback
        title, content = self.processor.process(html)
        assert "Some content here" in content
        assert "More content here" in content

    def test_process_complex_html_structure(self):
        """Test processing of complex HTML with nested structures."""
        html = """<html>
        <head>
            <title>Complex Page</title>
            <style>/* CSS content */</style>
        </head>
        <body>
            <header>
                <nav>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/about">About</a></li>
                    </ul>
                </nav>
            </header>
            <main>
                <article>
                    <h1>Article Title</h1>
                    <div class="content">
                        <p>First paragraph of the article.</p>
                        <blockquote>
                            <p>This is a quote within the article.</p>
                        </blockquote>
                        <p>Second paragraph continues here.</p>
                        <ul>
                            <li>List item 1</li>
                            <li>List item 2</li>
                        </ul>
                    </div>
                </article>
                <aside class="sidebar">
                    <h3>Related Articles</h3>
                    <ul>
                        <li>Related article 1</li>
                        <li>Related article 2</li>
                    </ul>
                </aside>
            </main>
            <footer>
                <p>Copyright information</p>
            </footer>
            <script>
                console.log('This should be removed');
            </script>
        </body>
        </html>"""

        title, content = self.processor.process(html)

        assert title == "Complex Page"

        # Should include main content
        assert "Article Title" in content
        assert "First paragraph of the article" in content
        assert "This is a quote within the article" in content
        assert "Second paragraph continues here" in content
        assert "List item 1" in content
        assert "List item 2" in content

        # Should exclude navigation, footer, scripts, and sidebar
        assert "Home" not in content
        assert "About" not in content
        assert "Copyright information" not in content
        assert "console.log" not in content
        assert "Related Articles" not in content

    def test_whitespace_normalization(self):
        """Test proper whitespace normalization in content."""
        html = """<html><body>
        <p>Paragraph    with    extra    spaces</p>
        <p>
            Multi-line
            paragraph
            with breaks
        </p>
        <div>
            <span>Nested</span>
            <span>elements</span>
            <span>with</span>
            <span>spacing</span>
        </div>
        </body></html>"""

        title, content = self.processor.process(html)

        # Multiple spaces should be collapsed to single spaces
        assert "extra    spaces" not in content
        assert "Paragraph with extra spaces" in content

        # Line breaks should be normalized
        assert "Multi-line paragraph with breaks" in content

        # Nested elements should have proper spacing
        assert "Nested elements with spacing" in content
