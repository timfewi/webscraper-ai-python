"""
Step 2: Conditional Logic for Web Scraping
Learn to make decisions in your code
"""

from typing import Tuple


def check_url_validity(url: str) -> Tuple[bool, str]:
    """Check if a URL is valid for scraping"""
    if not url:
        return False, "URL is empty"

    if not url.startswith(("http://", "https://")):
        return False, "URL must start with http:// or https://"

    if len(url) < 10:
        return False, "URL seems too short"

    # Check for common invalid patterns
    invalid_patterns = [".local", "localhost", "127.0.0.1"]
    for pattern in invalid_patterns:
        if pattern in url:
            return False, f"URL contains invalid pattern: {pattern}"

    return True, "URL is valid"


def categorize_website(url: str) -> str:
    """Categorize website based on URL patterns"""
    url_lower = url.lower()

    if "shop" in url_lower or "store" in url_lower or "buy" in url_lower:
        return "E-commerce"
    elif "news" in url_lower or "blog" in url_lower:
        return "News/Blog"
    elif "github.com" in url_lower:
        return "Code Repository"
    elif "wikipedia.org" in url_lower:
        return "Reference"
    else:
        return "General"


def simulate_scraping_status() -> bool:
    """Simulate different scraping scenarios"""
    import random

    scenarios = [
        (200, "Success"),
        (404, "Page not found"),
        (403, "Access forbidden"),
        (500, "Server error"),
        (429, "Rate limited"),
    ]

    status_code, message = random.choice(scenarios)

    if status_code == 200:
        print(f"✅ {message} - Continue scraping")
        return True
    elif status_code == 429:
        print(f"⏳ {message} - Wait and retry")
        return False
    elif status_code in [403, 404]:
        print(f"❌ {message} - Skip this URL")
        return False
    else:
        print(f"⚠️  {message} - Log error and continue")
        return False


# Test the functions
if __name__ == "__main__":
    print("🔍 URL Validation Tests")
    print("=" * 30)

    test_urls = [
        "https://example.com",
        "http://shop.example.com",
        "https://news.site.com",
        "ftp://invalid.com",
        "https://localhost:8000",
        "",
    ]

    for url in test_urls:
        is_valid, message = check_url_validity(url)
        category = categorize_website(url) if is_valid else "N/A"
        print(f"URL: {url or 'Empty'}")
        print(f"  Valid: {is_valid} - {message}")
        print(f"  Category: {category}\n")

    print("🎲 Scraping Simulation")
    print("=" * 20)
    for i in range(5):
        print(f"Attempt {i+1}: ", end="")
        simulate_scraping_status()
