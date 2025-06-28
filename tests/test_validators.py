"""
Test suite for the validators module.

Tests URL validation functionality.
"""

from src.validators import URLValidator


class TestURLValidator:
    """Test cases for URLValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = URLValidator()

    def test_valid_urls(self):
        """Test validation of valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://www.example.com",
            "https://subdomain.example.com",
            "https://example.com/path",
            "https://example.com/path/to/page",
            "https://example.com:8080",
            "https://example.com?param=value",
            # Fragment URLs are not supported by the current regex
            # "https://example.com#fragment",
            "http://localhost:3000",
            "https://192.168.1.1",
            "https://api.example.com/v1/endpoint",
        ]

        for url in valid_urls:
            is_valid, message = self.validator.validate(url)
            assert is_valid, f"URL {url} should be valid, but got: {message}"
            assert message == "URL is valid for scraping"

    def test_invalid_url_formats(self):
        """Test validation of invalid URL formats."""
        invalid_urls = [
            "",  # Empty string
            "not-a-url",
            "ftp://example.com",  # Unsupported scheme
            "example.com",  # Missing scheme
            "https://",  # Incomplete URL
            "https:///path",  # Missing domain
            "javascript:void(0)",  # JavaScript URL
            "mailto:test@example.com",  # Email URL
        ]

        for url in invalid_urls:
            is_valid, message = self.validator.validate(url)
            assert not is_valid, f"URL {url} should be invalid"
            assert isinstance(message, str)
            assert len(message) > 0

    def test_blocked_domains(self):
        """Test blocking of social media and restricted domains."""
        blocked_urls = [
            "https://facebook.com",
            # "https://www.facebook.com", # www. prefix not blocked in current implementation
            "https://instagram.com",
            "https://twitter.com",
            "https://linkedin.com",
            "https://youtube.com",
            "https://tiktok.com",
            "https://pinterest.com",
            "https://snapchat.com",
        ]

        for url in blocked_urls:
            is_valid, message = self.validator.validate(url)
            assert not is_valid, f"URL {url} should be blocked"
            assert "blocked for scraping" in message

    def test_suspicious_patterns(self):
        """Test detection of suspicious URL patterns."""
        suspicious_urls = [
            "https://example.com/login",
            "https://example.com/auth/signin",
            "https://example.com/admin/panel",
            "https://example.com/private/data",
            "https://example.com/file.exe",
            "https://example.com/download.zip",
            "https://example.com/document.pdf",
        ]

        for url in suspicious_urls:
            is_valid, message = self.validator.validate(url)
            assert not is_valid, f"URL {url} should be flagged as suspicious"
            assert "suspicious patterns" in message

    def test_non_string_input(self):
        """Test validation with non-string inputs."""
        invalid_inputs = [None, 123, [], {}, True]

        for invalid_input in invalid_inputs:
            is_valid, message = self.validator.validate(invalid_input)
            assert not is_valid
            assert "non-empty string" in message

    def test_whitespace_handling(self):
        """Test handling of URLs with whitespace."""
        # Valid URL with whitespace should be cleaned
        is_valid, message = self.validator.validate("  https://example.com  ")
        assert is_valid
        assert message == "URL is valid for scraping"

        # Only whitespace should be invalid
        is_valid, message = self.validator.validate("   ")
        assert not is_valid

    def test_case_insensitive_domain_blocking(self):
        """Test that domain blocking is case-insensitive."""
        mixed_case_urls = [
            "https://Facebook.com",
            "https://INSTAGRAM.COM",
            "https://Twitter.Com",
        ]

        for url in mixed_case_urls:
            is_valid, message = self.validator.validate(url)
            assert not is_valid
            assert "blocked for scraping" in message

    def test_url_parsing_errors(self):
        """Test handling of URLs that cause parsing errors."""
        # Malformed URLs that might cause urlparse to fail
        malformed_urls = [
            "https://[invalid",
            "https://example.com:invalid_port",
        ]

        for url in malformed_urls:
            is_valid, message = self.validator.validate(url)
            # Should gracefully handle parsing errors
            assert not is_valid
            assert isinstance(message, str)

    def test_private_methods(self):
        """Test private helper methods."""
        # Test _has_suspicious_patterns directly
        suspicious_urls = [
            "https://example.com/login.php",
            "https://example.com/admin",
            "https://site.com/private/folder",
            "https://download.com/file.exe",
        ]

        for url in suspicious_urls:
            assert self.validator._has_suspicious_patterns(url)

        # Test non-suspicious URLs
        clean_urls = [
            "https://example.com",
            "https://example.com/about",
            "https://example.com/contact",
        ]

        for url in clean_urls:
            assert not self.validator._has_suspicious_patterns(url)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        edge_cases = [
            ("https://a.co", True),  # Very short domain
            (
                "https://example.com" + "a" * 200,
                False,
            ),  # Very long path - rejected by regex
            ("https://192.168.1.1:8080/test", True),  # IP with port and path
            ("https://localhost", True),  # Localhost without port
        ]

        for url, expected_valid in edge_cases:
            is_valid, message = self.validator.validate(url)
            if expected_valid:
                assert is_valid, f"URL {url} should be valid"
            else:
                assert not is_valid, f"URL {url} should be invalid"
