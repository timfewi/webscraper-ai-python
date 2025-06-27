# Step 3: Functions, Modules & Error Handling

## 🎯 Learning Goals

- Create reusable functions for web scraping tasks
- Organize code into modules and packages
- Handle errors gracefully with try/except
- Work with files for data storage
- Understand Python imports and packages

## 📖 Theory

### Why Functions Matter for Web Scraping

- **Reusability**: Write once, use many times
- **Organization**: Break complex scraping into smaller tasks
- **Testing**: Easier to test individual components
- **Maintenance**: Fix bugs in one place

### Error Handling in Web Scraping

Web scraping is inherently unreliable:

- Network issues
- Website changes
- Rate limiting
- Invalid data

## 💻 Coding Exercises

### Exercise 1: Creating Scraping Functions
**File**: `examples/step03_functions.py`

```python
"""
Step 3: Functions for Web Scraping
Building reusable components
"""

import time
import random
from typing import List, Dict, Optional, Tuple

def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate if a URL is suitable for scraping.

    Args:
        url: The URL to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not url:
        return False, "URL cannot be empty"

    if not isinstance(url, str):
        return False, "URL must be a string"

    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"

    if len(url) < 10:
        return False, "URL appears to be too short"

    # Check for localhost or development URLs
    if any(pattern in url.lower() for pattern in ['localhost', '127.0.0.1', '.local']):
        return False, "Development URLs not allowed"

    return True, "URL is valid"

def extract_domain(url: str) -> Optional[str]:
    """
    Extract domain from URL.

    Args:
        url: Full URL

    Returns:
        Domain name or None if invalid
    """
    try:
        # Remove protocol
        if '://' in url:
            url = url.split('://', 1)[1]

        # Remove path
        domain = url.split('/')[0]

        # Remove port if present
        domain = domain.split(':')[0]

        return domain
    except (IndexError, AttributeError):
        return None

def simulate_http_request(url: str, timeout: int = 30) -> Dict:
    """
    Simulate an HTTP request with realistic outcomes.

    Args:
        url: URL to request
        timeout: Request timeout in seconds

    Returns:
        Dictionary with status_code, content, headers, etc.
    """
    # Simulate network delay
    time.sleep(random.uniform(0.1, 0.5))

    # Simulate different response scenarios
    scenarios = [
        {'status_code': 200, 'success': True, 'content': f'<html>Content from {url}</html>'},
        {'status_code': 404, 'success': False, 'content': 'Page not found'},
        {'status_code': 403, 'success': False, 'content': 'Access forbidden'},
        {'status_code': 500, 'success': False, 'content': 'Internal server error'},
        {'status_code': 429, 'success': False, 'content': 'Rate limited'}
    ]

    # 70% chance of success
    if random.random() < 0.7:
        response = scenarios[0]  # Success
    else:
        response = random.choice(scenarios[1:])  # Error

    return {
        'url': url,
        'status_code': response['status_code'],
        'success': response['success'],
        'content': response['content'],
        'headers': {'Content-Type': 'text/html'},
        'response_time': random.uniform(0.1, 2.0)
    }

def retry_request(url: str, max_retries: int = 3, delay: float = 1.0) -> Dict:
    """
    Make HTTP request with retry logic.

    Args:
        url: URL to request
        max_retries: Maximum number of retry attempts
        delay: Base delay between retries

    Returns:
        Response dictionary or error information
    """
    for attempt in range(max_retries + 1):
        print(f"  Attempt {attempt + 1}/{max_retries + 1} for {url}")

        response = simulate_http_request(url)

        if response['success']:
            response['attempts'] = attempt + 1
            return response

        # Don't retry on certain errors
        if response['status_code'] in [404, 403]:
            print(f"    ❌ Non-retryable error: {response['status_code']}")
            break

        # Wait before retry (exponential backoff)
        if attempt < max_retries:
            wait_time = delay * (2 ** attempt)
            print(f"    ⏳ Waiting {wait_time:.1f}s before retry...")
            time.sleep(wait_time)

    response['attempts'] = max_retries + 1
    return response

def scrape_url_safe(url: str) -> Dict:
    """
    Safely scrape a URL with validation and error handling.

    Args:
        url: URL to scrape

    Returns:
        Dictionary with scraping results
    """
    result = {
        'url': url,
        'success': False,
        'data': None,
        'error': None,
        'domain': None,
        'timestamp': time.time()
    }

    # Step 1: Validate URL
    is_valid, message = validate_url(url)
    if not is_valid:
        result['error'] = f"Invalid URL: {message}"
        return result

    # Step 2: Extract domain
    domain = extract_domain(url)
    if not domain:
        result['error'] = "Could not extract domain"
        return result

    result['domain'] = domain

    # Step 3: Make request with retries
    response = retry_request(url)

    if response['success']:
        result['success'] = True
        result['data'] = {
            'content': response['content'],
            'status_code': response['status_code'],
            'response_time': response['response_time'],
            'attempts': response['attempts']
        }
    else:
        result['error'] = f"HTTP {response['status_code']}: {response['content']}"

    return result

def batch_scrape_urls(urls: List[str], delay_between: float = 1.0) -> List[Dict]:
    """
    Scrape multiple URLs with rate limiting.

    Args:
        urls: List of URLs to scrape
        delay_between: Delay between requests in seconds

    Returns:
        List of scraping results
    """
    results = []
    total_urls = len(urls)

    print(f"🚀 Starting batch scrape of {total_urls} URLs")
    print("=" * 50)

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{total_urls}] Scraping: {url}")

        result = scrape_url_safe(url)
        results.append(result)

        if result['success']:
            print(f"  ✅ Success in {result['data']['attempts']} attempts")
        else:
            print(f"  ❌ Failed: {result['error']}")

        # Rate limiting (don't delay after last URL)
        if i < total_urls:
            print(f"  ⏳ Waiting {delay_between}s...")
            time.sleep(delay_between)

    return results

def summarize_results(results: List[Dict]) -> Dict:
    """
    Generate summary statistics from scraping results.

    Args:
        results: List of scraping results

    Returns:
        Summary statistics
    """
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    failed = total - successful

    # Analyze errors
    error_types = {}
    domains = set()

    for result in results:
        if result['domain']:
            domains.add(result['domain'])

        if not result['success'] and result['error']:
            error_key = result['error'].split(':')[0]  # Get error type
            error_types[error_key] = error_types.get(error_key, 0) + 1

    return {
        'total_urls': total,
        'successful': successful,
        'failed': failed,
        'success_rate': (successful / total * 100) if total > 0 else 0,
        'unique_domains': len(domains),
        'domains': list(domains),
        'error_types': error_types
    }

# Example usage
if __name__ == "__main__":
    # Test URLs
    test_urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://example.com",
        "https://github.com",
        "invalid-url",
        "https://httpbin.org/delay/1"
    ]

    # Scrape all URLs
    results = batch_scrape_urls(test_urls, delay_between=0.5)

    # Generate summary
    summary = summarize_results(results)

    print("\n" + "="*50)
    print("📊 SCRAPING SUMMARY")
    print("="*50)
    print(f"Total URLs: {summary['total_urls']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Unique Domains: {summary['unique_domains']}")
    print(f"Domains: {', '.join(summary['domains'])}")

    if summary['error_types']:
        print("\nError Types:")
        for error, count in summary['error_types'].items():
            print(f"  {error}: {count}")
```

### Exercise 2: Error Handling and Logging
**File**: `examples/step03_error_handling.py`

```python
"""
Step 3: Error Handling for Web Scraping
Graceful error management and logging
"""

import logging
import json
import time
from typing import Dict, List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ScrapingError(Exception):
    """Custom exception for scraping-related errors"""
    pass

class RateLimitError(ScrapingError):
    """Raised when rate limit is exceeded"""
    pass

class ValidationError(ScrapingError):
    """Raised when data validation fails"""
    pass

def safe_request(url: str) -> Dict:
    """
    Make a safe HTTP request with comprehensive error handling.

    Args:
        url: URL to request

    Returns:
        Response data or error information

    Raises:
        ScrapingError: For scraping-specific errors
        RateLimitError: When rate limited
    """
    try:
        logger.info(f"Making request to: {url}")

        # Simulate different error scenarios
        import random

        scenario = random.choice([
            'success',
            'network_error',
            'timeout',
            'rate_limit',
            'server_error',
            'invalid_response'
        ])

        if scenario == 'success':
            logger.info(f"✅ Successfully retrieved: {url}")
            return {
                'status': 'success',
                'data': f'<html>Content from {url}</html>',
                'status_code': 200,
                'url': url
            }

        elif scenario == 'network_error':
            logger.error(f"🌐 Network error for: {url}")
            raise ConnectionError("Network connection failed")

        elif scenario == 'timeout':
            logger.error(f"⏱️ Timeout for: {url}")
            raise TimeoutError("Request timed out")

        elif scenario == 'rate_limit':
            logger.warning(f"⏳ Rate limited: {url}")
            raise RateLimitError("Rate limit exceeded")

        elif scenario == 'server_error':
            logger.error(f"🚨 Server error for: {url}")
            return {
                'status': 'error',
                'error': 'Internal server error',
                'status_code': 500,
                'url': url
            }

        else:  # invalid_response
            logger.error(f"📄 Invalid response from: {url}")
            raise ValueError("Invalid response format")

    except Exception as e:
        logger.error(f"❌ Unexpected error for {url}: {str(e)}")
        raise

def scrape_with_error_handling(url: str, max_retries: int = 3) -> Optional[Dict]:
    """
    Scrape URL with comprehensive error handling.

    Args:
        url: URL to scrape
        max_retries: Maximum retry attempts

    Returns:
        Scraped data or None if failed
    """
    for attempt in range(max_retries):
        try:
            result = safe_request(url)

            if result['status'] == 'success':
                return result
            else:
                logger.warning(f"Non-success status: {result['status']}")
                if attempt < max_retries - 1:
                    continue
                else:
                    return None

        except RateLimitError:
            logger.warning(f"Rate limited, waiting 60s (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(5)  # Shortened for demo
                continue
            else:
                logger.error("Max retries exceeded due to rate limiting")
                return None

        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Network issue (attempt {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
                continue
            else:
                logger.error("Max retries exceeded due to network issues")
                return None

        except ValueError as e:
            logger.error(f"Data validation error: {str(e)}")
            # Don't retry for validation errors
            return None

        except Exception as e:
            logger.error(f"Unexpected error (attempt {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            else:
                logger.error("Max retries exceeded due to unexpected errors")
                return None

    return None

def validate_scraped_data(data: Dict) -> Dict:
    """
    Validate scraped data and clean it.

    Args:
        data: Raw scraped data

    Returns:
        Validated and cleaned data

    Raises:
        ValidationError: If data is invalid
    """
    try:
        if not isinstance(data, dict):
            raise ValidationError("Data must be a dictionary")

        if 'data' not in data:
            raise ValidationError("Data must contain 'data' field")

        content = data['data']
        if not content or len(content.strip()) < 10:
            raise ValidationError("Content is too short or empty")

        # Clean the data
        cleaned_data = {
            'url': data.get('url', '').strip(),
            'content': content.strip(),
            'status_code': data.get('status_code', 0),
            'scraped_at': time.time(),
            'content_length': len(content)
        }

        logger.info(f"✅ Data validation passed for: {cleaned_data['url']}")
        return cleaned_data

    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Validation failed: {str(e)}")

def save_data_safely(data: Dict, filename: str) -> bool:
    """
    Safely save data to file with error handling.

    Args:
        data: Data to save
        filename: Target filename

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        # Save with backup
        backup_filename = f"{filename}.backup"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Create backup
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 Data saved successfully to: {filename}")
        return True

    except PermissionError:
        logger.error(f"❌ Permission denied writing to: {filename}")
        return False
    except OSError as e:
        logger.error(f"❌ OS error saving {filename}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error saving {filename}: {str(e)}")
        return False

def robust_scraping_pipeline(urls: List[str]) -> Dict:
    """
    Complete scraping pipeline with error handling.

    Args:
        urls: List of URLs to scrape

    Returns:
        Summary of scraping results
    """
    results = {
        'successful': [],
        'failed': [],
        'errors': [],
        'total_processed': 0,
        'start_time': time.time()
    }

    logger.info(f"🚀 Starting scraping pipeline for {len(urls)} URLs")

    for i, url in enumerate(urls, 1):
        logger.info(f"[{i}/{len(urls)}] Processing: {url}")
        results['total_processed'] += 1

        try:
            # Step 1: Scrape with error handling
            scraped_data = scrape_with_error_handling(url)

            if scraped_data is None:
                results['failed'].append({
                    'url': url,
                    'error': 'Scraping failed after retries',
                    'timestamp': time.time()
                })
                continue

            # Step 2: Validate data
            validated_data = validate_scraped_data(scraped_data)

            # Step 3: Save data
            filename = f"data/{i:03d}_{url.replace('://', '_').replace('/', '_')}.json"
            if save_data_safely(validated_data, filename):
                results['successful'].append({
                    'url': url,
                    'filename': filename,
                    'content_length': validated_data['content_length'],
                    'timestamp': time.time()
                })
            else:
                results['failed'].append({
                    'url': url,
                    'error': 'Failed to save data',
                    'timestamp': time.time()
                })

        except ValidationError as e:
            error_msg = f"Validation error: {str(e)}"
            logger.error(f"❌ {error_msg} for: {url}")
            results['errors'].append({
                'url': url,
                'error': error_msg,
                'type': 'validation',
                'timestamp': time.time()
            })

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"❌ {error_msg} for: {url}")
            results['errors'].append({
                'url': url,
                'error': error_msg,
                'type': 'unexpected',
                'timestamp': time.time()
            })

    # Calculate summary statistics
    results['end_time'] = time.time()
    results['duration'] = results['end_time'] - results['start_time']
    results['success_rate'] = len(results['successful']) / len(urls) * 100

    logger.info(f"📊 Pipeline complete: {len(results['successful'])}/{len(urls)} successful")

    return results

# Example usage
if __name__ == "__main__":
    test_urls = [
        "https://httpbin.org/json",
        "https://httpbin.org/html",
        "https://httpbin.org/status/500",
        "https://example.com",
        "https://httpbin.org/delay/1"
    ]

    # Run the pipeline
    results = robust_scraping_pipeline(test_urls)

    # Print summary
    print("\n" + "="*60)
    print("📊 SCRAPING PIPELINE SUMMARY")
    print("="*60)
    print(f"Total URLs processed: {results['total_processed']}")
    print(f"Successful: {len(results['successful'])}")
    print(f"Failed: {len(results['failed'])}")
    print(f"Errors: {len(results['errors'])}")
    print(f"Success rate: {results['success_rate']:.1f}%")
    print(f"Duration: {results['duration']:.2f} seconds")

    if results['errors']:
        print("\nErrors encountered:")
        for error in results['errors']:
            print(f"  ❌ {error['url']}: {error['error']}")
```

### Exercise 3: Organizing Code into Modules
**File**: `src/scraper_utils.py`

```python
"""
Web Scraping Utility Functions
Organized into a reusable module
"""

import time
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)

class URLValidator:
    """URL validation utilities for web scraping"""

    ALLOWED_SCHEMES = ['http', 'https']
    BLOCKED_DOMAINS = ['localhost', '127.0.0.1', '0.0.0.0']

    @classmethod
    def is_valid(cls, url: str) -> Tuple[bool, str]:
        """
        Validate URL for scraping.

        Args:
            url: URL to validate

        Returns:
            Tuple of (is_valid, message)
        """
        if not url or not isinstance(url, str):
            return False, "URL must be a non-empty string"

        try:
            parsed = urlparse(url)

            if not parsed.scheme:
                return False, "URL must include scheme (http/https)"

            if parsed.scheme not in cls.ALLOWED_SCHEMES:
                return False, f"Scheme must be one of: {cls.ALLOWED_SCHEMES}"

            if not parsed.netloc:
                return False, "URL must include domain"

            # Check for blocked domains
            domain = parsed.netloc.split(':')[0].lower()
            if any(blocked in domain for blocked in cls.BLOCKED_DOMAINS):
                return False, f"Domain contains blocked pattern: {domain}"

            return True, "URL is valid"

        except Exception as e:
            return False, f"URL parsing error: {str(e)}"

    @staticmethod
    def extract_domain(url: str) -> Optional[str]:
        """Extract domain from URL"""
        try:
            return urlparse(url).netloc.split(':')[0].lower()
        except:
            return None

    @staticmethod
    def is_same_domain(url1: str, url2: str) -> bool:
        """Check if two URLs are from the same domain"""
        domain1 = URLValidator.extract_domain(url1)
        domain2 = URLValidator.extract_domain(url2)
        return domain1 == domain2 and domain1 is not None

class RateLimiter:
    """Rate limiting for respectful web scraping"""

    def __init__(self, requests_per_second: float = 1.0):
        self.delay = 1.0 / requests_per_second
        self.last_request_time = 0

    def wait_if_needed(self):
        """Wait if necessary to respect rate limit"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.delay:
            sleep_time = self.delay - time_since_last
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def set_rate(self, requests_per_second: float):
        """Update the rate limit"""
        self.delay = 1.0 / requests_per_second

class DataProcessor:
    """Process and clean scraped data"""

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean scraped text data"""
        if not text:
            return ""

        # Remove extra whitespace
        text = ' '.join(text.split())

        # Remove common HTML entities (basic)
        replacements = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&nbsp;': ' '
        }

        for entity, replacement in replacements.items():
            text = text.replace(entity, replacement)

        return text.strip()

    @staticmethod
    def extract_links(content: str, base_url: str) -> List[str]:
        """Extract and normalize links from content"""
        import re

        # Simple regex to find links (for demonstration)
        link_pattern = r'href=["\']([^"\']+)["\']'
        matches = re.findall(link_pattern, content)

        normalized_links = []
        for link in matches:
            # Convert relative URLs to absolute
            if link.startswith(('http://', 'https://')):
                normalized_links.append(link)
            else:
                absolute_url = urljoin(base_url, link)
                normalized_links.append(absolute_url)

        return list(set(normalized_links))  # Remove duplicates

    @staticmethod
    def calculate_content_stats(content: str) -> Dict:
        """Calculate statistics about scraped content"""
        if not content:
            return {'length': 0, 'words': 0, 'lines': 0}

        return {
            'length': len(content),
            'words': len(content.split()),
            'lines': len(content.splitlines()),
            'links_count': content.count('href='),
            'images_count': content.count('<img')
        }

def create_scraping_session(rate_limit: float = 1.0) -> Dict:
    """
    Create a configured scraping session.

    Args:
        rate_limit: Requests per second

    Returns:
        Session configuration dictionary
    """
    return {
        'rate_limiter': RateLimiter(rate_limit),
        'validator': URLValidator(),
        'processor': DataProcessor(),
        'start_time': time.time(),
        'request_count': 0,
        'success_count': 0,
        'error_count': 0
    }

def scrape_url(url: str, session: Dict) -> Optional[Dict]:
    """
    Scrape a single URL using the session configuration.

    Args:
        url: URL to scrape
        session: Session configuration

    Returns:
        Scraped data or None
    """
    session['request_count'] += 1

    # Validate URL
    is_valid, message = session['validator'].is_valid(url)
    if not is_valid:
        logger.error(f"Invalid URL {url}: {message}")
        session['error_count'] += 1
        return None

    # Apply rate limiting
    session['rate_limiter'].wait_if_needed()

    try:
        # Simulate scraping (replace with actual HTTP request)
        logger.info(f"Scraping: {url}")

        # Mock response
        content = f"<html><body>Content from {url}</body></html>"

        # Process the content
        cleaned_content = session['processor'].clean_text(content)
        stats = session['processor'].calculate_content_stats(content)

        session['success_count'] += 1

        return {
            'url': url,
            'domain': session['validator'].extract_domain(url),
            'content': cleaned_content,
            'stats': stats,
            'scraped_at': time.time()
        }

    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        session['error_count'] += 1
        return None
```

**File**: `src/__init__.py`

```python
"""
Web Scraper Package
Initialize the scraping modules
"""

from .scraper_utils import (
    URLValidator,
    RateLimiter,
    DataProcessor,
    create_scraping_session,
    scrape_url
)

__version__ = "0.1.0"
__all__ = [
    'URLValidator',
    'RateLimiter',
    'DataProcessor',
    'create_scraping_session',
    'scrape_url'
]
```

## 🔍 Key Concepts Learned

### 1. Function Definition and Documentation

```python
def function_name(param1: type, param2: type = default) -> return_type:
    """
    Function description.

    Args:
        param1: Description
        param2: Description with default

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception is raised
    """
    # Function body
    return result
```

### 2. Error Handling Patterns

```python
try:
    # Code that might fail
    result = risky_operation()
except SpecificError as e:
    # Handle specific error
    logger.error(f"Specific error: {e}")
except Exception as e:
    # Handle any other error
    logger.error(f"Unexpected error: {e}")
    raise  # Re-raise if needed
finally:
    # Always execute (cleanup)
    cleanup_resources()
```

### 3. Module Organization

```python
# In module file (utils.py)
def utility_function():
    pass

# In main file
from utils import utility_function
# or
import utils
utils.utility_function()
```

## 🧪 Practice Challenges

### Challenge 1: Create a Scraping Config Module

Create `src/config.py` with:

- Configuration class for scraping settings
- Environment variable loading
- Validation of configuration values
- Default settings for different scraping scenarios

### Challenge 2: Build a Robust Downloader

Create a function that:

- Downloads content from URLs
- Handles different content types
- Implements exponential backoff
- Saves files with proper naming
- Creates progress reports

### Challenge 3: Data Validation System

Build a system that:

- Validates scraped data against schemas
- Cleans and normalizes data
- Detects duplicate content
- Generates data quality reports

## 🎯 Next Steps

In Step 4, we'll learn about:

- Working with real HTTP requests (requests library)
- Parsing HTML with BeautifulSoup
- Handling forms and cookies
- Basic web scraping patterns

## 📝 Notes

- Functions are the building blocks of larger programs
- Error handling is crucial for reliable web scraping
- Good organization makes code maintainable
- Type hints improve code clarity and catch errors early

---

**Completion Checklist:**
- [ ] Created reusable functions for scraping tasks
- [ ] Implemented proper error handling with try/except
- [ ] Organized code into modules with imports
- [ ] Used logging for debugging and monitoring
- [ ] Completed all coding exercises
- [ ] Attempted at least one practice challenge

Ready for Step 4? Let's start making real HTTP requests! 🌐
