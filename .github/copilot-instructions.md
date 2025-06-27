# GitHub Copilot Instructions Guide

This guide provides best practices and instructions for effectively using GitHub Copilot in our Python webscraper project to maximize productivity and code quality.

## Getting Started with Copilot

### Prerequisites

- GitHub Copilot subscription (Individual, Business, or Enterprise)
- VS Code with GitHub Copilot extension installed
- Python development environment configured

### Initial Setup

1. Install the GitHub Copilot extension in VS Code
2. Sign in with your GitHub account
3. Enable Copilot in your workspace settings
4. Familiarize yourself with keyboard shortcuts:
   - `Tab` to accept suggestions
   - `Esc` to dismiss suggestions
   - `Alt + ]` / `Alt + [` to cycle through suggestions
   - `Ctrl + Enter` to open Copilot suggestions panel

## Effective Prompting Techniques

### Context is Key

Provide clear context through comments, function names, and variable names. Copilot uses surrounding code to generate better suggestions.

```python
# Good: Clear context and intent
def scrape_product_data(url: str, headers: dict) -> dict:
    """
    Scrape product information from e-commerce website.
    Extract: title, price, description, availability
    """
    # Copilot will generate appropriate scraping logic here

# Better: Even more specific context
class AmazonProductScraper:
    def __init__(self, session: requests.Session):
        self.session = session
        self.base_url = "https://amazon.com"

    def extract_product_title(self, soup: BeautifulSoup) -> str:
        # Extract product title from Amazon product page
        # Look for element with id 'productTitle'
```

### Use Descriptive Comments

Write comments that describe what you want to achieve, not how to do it.

```python
# Good: Describes the intent
# Parse the JSON response and extract error messages if any
response_data = json.loads(response.text)

# Better: More specific about expected structure
# Extract error messages from API response
# Expected format: {"errors": [{"message": "...", "code": "..."}]}
```

### Function and Variable Naming

Use descriptive names that help Copilot understand the context and purpose.

```python
# Good naming helps Copilot generate better code
def validate_scraped_product_data(product_info: dict) -> bool:
    # Copilot understands this should validate product data

def clean_extracted_price_text(raw_price_string: str) -> float:
    # Copilot knows to clean and convert price text to float
```

## Code Generation Best Practices

### Start with Structure

Define the structure and let Copilot fill in the implementation details.

```python
class WebScraperBase:
    def __init__(self, base_url: str, headers: dict = None):
        # Copilot will suggest appropriate initialization

    def make_request(self, url: str) -> requests.Response:
        # Copilot will suggest request handling with error handling

    def parse_response(self, response: requests.Response) -> BeautifulSoup:
        # Copilot will suggest HTML parsing logic

    def extract_data(self, soup: BeautifulSoup) -> dict:
        # Copilot will suggest data extraction methods
```

### Use Type Hints

Type hints help Copilot generate more accurate suggestions.

```python
from typing import List, Dict, Optional, Union
import requests
from bs4 import BeautifulSoup

def scrape_multiple_pages(
    urls: List[str],
    headers: Dict[str, str],
    delay: float = 1.0
) -> List[Dict[str, any]]:
    # Copilot will generate appropriate logic for multiple page scraping
```

### Leverage Existing Imports

Import the libraries you plan to use at the top of the file to give Copilot context.

```python
import requests
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin, urlparse
import logging

# Now Copilot knows which libraries are available and will suggest accordingly
```

## Common Patterns and Templates

### Web Scraping Session Management

```python
class ScrapingSession:
    def __init__(self, headers: dict = None, proxy: dict = None):
        # Initialize session with headers and proxy configuration

    def __enter__(self):
        # Setup session context manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup session resources
```

### Rate Limiting and Retry Logic

```python
def make_request_with_retry(
    url: str,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0
) -> requests.Response:
    # Implement exponential backoff retry logic
```

### Data Validation and Cleaning

```python
def validate_scraped_data(data: dict, required_fields: List[str]) -> bool:
    # Validate that all required fields are present and not empty

def clean_text_data(raw_text: str) -> str:
    # Remove extra whitespace, HTML entities, and normalize text
```

## Integration with Development Workflow

### Code Review Guidelines

1. **Always review Copilot suggestions** before accepting
2. **Test generated code** thoroughly, especially error handling
3. **Verify security implications** of generated code
4. **Check for proper error handling** and edge cases
5. **Ensure code follows project style guide**

### Testing with Copilot

```python
import pytest
from unittest.mock import Mock, patch

class TestProductScraper:
    def test_extract_product_title(self):
        # Test successful title extraction

    def test_extract_product_title_missing_element(self):
        # Test handling when title element is missing

    def test_price_parsing_various_formats(self):
        # Test price parsing with different currency formats
```

### Documentation with Copilot

```python
def scrape_product_listings(base_url: str, max_pages: int = 10) -> List[dict]:
    """
    Scrape product listings from multiple pages.

    This function iterates through pagination and extracts product data
    from each page. It includes rate limiting and error handling.

    Args:
        base_url: The base URL of the product listing page
        max_pages: Maximum number of pages to scrape (default: 10)

    Returns:
        List of dictionaries containing product information

    Raises:
        requests.RequestException: If HTTP request fails
        ValueError: If URL is invalid or response is malformed

    Example:
        >>> products = scrape_product_listings('https://example.com/products')
        >>> len(products)
        50
    """
    # Copilot will generate implementation based on docstring
```

## Security and Ethics Considerations

### Responsible Scraping Practices

```python
# Always check robots.txt before scraping
def check_robots_txt(base_url: str) -> bool:
    # Check if scraping is allowed according to robots.txt

# Implement proper delays between requests
def respectful_delay(last_request_time: float, min_delay: float = 1.0):
    # Calculate and implement appropriate delay between requests

# Handle rate limiting gracefully
def handle_rate_limit(response: requests.Response) -> bool:
    # Check for rate limiting status codes and headers
```

### Data Privacy and Security

```python
# Sanitize sensitive data from logs
def sanitize_url_for_logging(url: str) -> str:
    # Remove sensitive parameters from URL before logging

# Secure credential handling
def load_credentials_from_env() -> dict:
    # Load API keys and credentials from environment variables
```

## Troubleshooting Common Issues

### When Copilot Suggestions Are Not Helpful

1. **Add more context** through comments and variable names
2. **Break down complex tasks** into smaller, specific functions
3. **Use more descriptive function and variable names**
4. **Add type hints** to clarify expected data types
5. **Include example data structures** in comments

### Improving Code Quality

```python
# Instead of accepting the first suggestion, consider:
# 1. Error handling completeness
# 2. Edge case coverage
# 3. Performance implications
# 4. Code maintainability
# 5. Security considerations

def robust_data_extraction(html_content: str) -> Optional[dict]:
    """
    Extract data with comprehensive error handling.
    Handle cases: malformed HTML, missing elements, encoding issues
    """
    # Copilot will generate more robust code with this context
```

### Performance Optimization

```python
# Use specific comments to guide performance optimizations
def optimize_bulk_scraping(urls: List[str]) -> List[dict]:
    # Use asyncio for concurrent requests to improve performance
    # Implement connection pooling for better resource utilization
    # Add caching to avoid duplicate requests
```

## Best Practices Summary

### Do's

- ✅ Provide clear, descriptive context through comments
- ✅ Use meaningful function and variable names
- ✅ Add type hints for better suggestions
- ✅ Review and test all generated code
- ✅ Break complex tasks into smaller functions
- ✅ Use docstrings to guide implementation
- ✅ Import relevant libraries at the top of files

### Don'ts

- ❌ Accept suggestions without review
- ❌ Use vague or generic comments
- ❌ Ignore security implications
- ❌ Skip testing generated code
- ❌ Use generated code without understanding it
- ❌ Rely solely on Copilot for architecture decisions

## Advanced Tips

### Custom Instructions

You can create inline instructions for specific patterns:

```python
# COPILOT: Generate a retry decorator with exponential backoff
# Pattern: @retry(max_attempts=3, delay=1.0, backoff=2.0)
def retry_decorator(max_attempts: int, delay: float, backoff: float):
    # Copilot will generate decorator implementation
```

### Context-Aware Generation

```python
# Set up context for the entire file
"""
This module handles web scraping for e-commerce websites.
Focus on: error handling, rate limiting, data validation
Libraries: requests, BeautifulSoup, selenium
Pattern: session management with context managers
"""

# Now all suggestions in this file will be influenced by this context
```

## Conclusion

GitHub Copilot is a powerful tool that can significantly enhance your Python development productivity when used effectively. The key to success is providing clear context, reviewing suggestions carefully, and maintaining good coding practices. Remember that Copilot is an assistant, not a replacement for thoughtful software engineering.

Always prioritize code quality, security, and maintainability over speed of development.
