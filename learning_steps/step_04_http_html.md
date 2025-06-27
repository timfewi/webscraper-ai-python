# Step 4: HTTP Requests & HTML Parsing

## 🎯 Learning Goals

- Make real HTTP requests using the requests library
- Parse HTML content with BeautifulSoup
- Handle headers, cookies, and sessions
- Extract data from real websites
- Understand HTML structure and CSS selectors

## 📖 Theory

### HTTP Requests in Web Scraping

HTTP (HyperText Transfer Protocol) is how web browsers communicate with websites:

- **GET**: Retrieve data from a webpage
- **POST**: Send data to a server (forms, logins)
- **Headers**: Metadata about requests (User-Agent, Accept, etc.)
- **Cookies**: Small data pieces for session management
- **Status Codes**: 200 (OK), 404 (Not Found), 429 (Rate Limited)

### HTML Structure

HTML is a tree-like structure:

```html
<html>
  <head>
    <title>Page Title</title>
  </head>
  <body>
    <div class="content">
      <h1 id="main-title">Welcome</h1>
      <p>Some text</p>
    </div>
  </body>
</html>
```

## 💻 Coding Exercises

### Exercise 1: Basic HTTP Requests
**File**: `examples/step04_http_basics.py`

```python
"""
Step 4: HTTP Requests and Response Handling
Learn to communicate with websites
"""

import requests
import time
from typing import Dict, Optional
import json

def make_basic_request(url: str) -> Optional[requests.Response]:
    """
    Make a basic HTTP GET request.

    Args:
        url: URL to request

    Returns:
        Response object or None if failed
    """
    try:
        print(f"🌐 Making request to: {url}")

        # Basic GET request
        response = requests.get(url, timeout=10)

        print(f"  Status Code: {response.status_code}")
        print(f"  Content Type: {response.headers.get('Content-Type', 'Unknown')}")
        print(f"  Content Length: {len(response.content)} bytes")

        # Check if request was successful
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes

        return response

    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {str(e)}")
        return None

def make_request_with_headers(url: str) -> Optional[requests.Response]:
    """
    Make HTTP request with custom headers to appear more like a real browser.

    Args:
        url: URL to request

    Returns:
        Response object or None if failed
    """
    # Common headers to make requests look more legitimate
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        print(f"🌐 Making request with headers to: {url}")

        response = requests.get(url, headers=headers, timeout=10)

        print(f"  Status Code: {response.status_code}")
        print(f"  Final URL: {response.url}")  # In case of redirects
        print(f"  Headers sent: {dict(response.request.headers)}")

        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {str(e)}")
        return None

def handle_different_status_codes(urls: list) -> Dict:
    """
    Demonstrate handling different HTTP status codes.

    Args:
        urls: List of URLs to test

    Returns:
        Summary of results
    """
    results = {
        'successful': [],
        'client_errors': [],  # 4xx
        'server_errors': [],  # 5xx
        'redirects': [],      # 3xx
        'other': []
    }

    for url in urls:
        try:
            response = requests.get(url, timeout=10, allow_redirects=True)

            if 200 <= response.status_code < 300:
                results['successful'].append({
                    'url': url,
                    'status_code': response.status_code,
                    'content_length': len(response.content)
                })
            elif 300 <= response.status_code < 400:
                results['redirects'].append({
                    'url': url,
                    'status_code': response.status_code,
                    'redirected_to': response.url
                })
            elif 400 <= response.status_code < 500:
                results['client_errors'].append({
                    'url': url,
                    'status_code': response.status_code,
                    'error': response.reason
                })
            elif 500 <= response.status_code < 600:
                results['server_errors'].append({
                    'url': url,
                    'status_code': response.status_code,
                    'error': response.reason
                })
            else:
                results['other'].append({
                    'url': url,
                    'status_code': response.status_code
                })

        except requests.exceptions.RequestException as e:
            results['client_errors'].append({
                'url': url,
                'status_code': 'N/A',
                'error': str(e)
            })

    return results

def explore_response_properties(url: str):
    """
    Explore all the properties of an HTTP response.

    Args:
        url: URL to analyze
    """
    try:
        response = requests.get(url, timeout=10)

        print(f"🔍 Response Analysis for: {url}")
        print("=" * 50)

        # Basic response info
        print(f"Status Code: {response.status_code} ({response.reason})")
        print(f"URL: {response.url}")
        print(f"Encoding: {response.encoding}")
        print(f"Content Type: {response.headers.get('Content-Type')}")

        # Response headers
        print(f"\n📋 Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")

        # Content analysis
        print(f"\n📄 Content Analysis:")
        print(f"  Raw content length: {len(response.content)} bytes")
        print(f"  Text content length: {len(response.text)} characters")
        print(f"  First 200 characters: {response.text[:200]}...")

        # Cookies
        if response.cookies:
            print(f"\n🍪 Cookies received:")
            for cookie in response.cookies:
                print(f"  {cookie.name}: {cookie.value}")

        # History (redirects)
        if response.history:
            print(f"\n🔄 Redirect History:")
            for i, hist_response in enumerate(response.history):
                print(f"  {i+1}. {hist_response.status_code} -> {hist_response.url}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to analyze {url}: {str(e)}")

def test_api_endpoints():
    """
    Test different types of API endpoints to understand JSON responses.
    """
    # HTTPBin provides testing endpoints
    test_endpoints = [
        "https://httpbin.org/json",          # Returns JSON
        "https://httpbin.org/xml",           # Returns XML
        "https://httpbin.org/html",          # Returns HTML
        "https://httpbin.org/user-agent",    # Returns your user agent
        "https://httpbin.org/headers",       # Returns your headers
        "https://httpbin.org/ip",            # Returns your IP
    ]

    print("🧪 Testing Different API Endpoints")
    print("=" * 40)

    for endpoint in test_endpoints:
        print(f"\n🎯 Testing: {endpoint}")

        try:
            response = requests.get(endpoint, timeout=10)

            # Try to parse as JSON
            try:
                json_data = response.json()
                print(f"  ✅ JSON Response: {json.dumps(json_data, indent=2)[:200]}...")
            except ValueError:
                # Not JSON, show first part of text
                print(f"  📄 Text Response: {response.text[:200]}...")

        except requests.exceptions.RequestException as e:
            print(f"  ❌ Failed: {str(e)}")

        # Be respectful - small delay between requests
        time.sleep(0.5)

# Example usage and demonstrations
if __name__ == "__main__":
    print("🚀 HTTP Requests Tutorial")
    print("=" * 30)

    # Test basic requests
    test_urls = [
        "https://httpbin.org/status/200",    # Success
        "https://httpbin.org/status/404",    # Not found
        "https://httpbin.org/status/500",    # Server error
        "https://example.com",               # Real website
    ]

    print("\n1. Basic Requests:")
    for url in test_urls[:2]:  # Test first 2
        make_basic_request(url)
        print()

    print("\n2. Requests with Headers:")
    make_request_with_headers("https://httpbin.org/headers")

    print("\n3. Status Code Handling:")
    results = handle_different_status_codes(test_urls)
    for category, items in results.items():
        if items:
            print(f"  {category.title()}: {len(items)} URLs")

    print("\n4. Response Analysis:")
    explore_response_properties("https://example.com")

    print("\n5. API Testing:")
    test_api_endpoints()
```

### Exercise 2: HTML Parsing with BeautifulSoup
**File**: `examples/step04_html_parsing.py`

```python
"""
Step 4: HTML Parsing with BeautifulSoup
Extract data from HTML content
"""

import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional
import re

def get_soup(url: str) -> Optional[BeautifulSoup]:
    """
    Get BeautifulSoup object from URL.

    Args:
        url: URL to scrape

    Returns:
        BeautifulSoup object or None if failed
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Create BeautifulSoup object
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Failed to parse HTML: {str(e)}")
        return None

def demonstrate_basic_selectors(html_content: str):
    """
    Demonstrate basic CSS selectors and element finding.

    Args:
        html_content: HTML string to parse
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    print("🔍 Basic HTML Parsing Demonstration")
    print("=" * 40)

    # 1. Find by tag
    print("1. Finding by tag:")
    titles = soup.find_all('h1')
    for title in titles:
        print(f"  H1: {title.get_text().strip()}")

    # 2. Find by class
    print("\n2. Finding by class:")
    content_divs = soup.find_all('div', class_='content')
    for div in content_divs:
        print(f"  Content div: {div.get_text().strip()[:50]}...")

    # 3. Find by ID
    print("\n3. Finding by ID:")
    main_content = soup.find('div', id='main')
    if main_content:
        print(f"  Main content: {main_content.get_text().strip()[:50]}...")

    # 4. CSS selectors
    print("\n4. CSS Selectors:")

    # Class selector
    products = soup.select('.product')
    print(f"  Products found: {len(products)}")

    # ID selector
    header = soup.select('#header')
    print(f"  Header found: {len(header)}")

    # Descendant selector
    product_names = soup.select('.product .name')
    for name in product_names:
        print(f"  Product name: {name.get_text().strip()}")

    # Attribute selector
    links = soup.select('a[href]')
    print(f"  Links with href: {len(links)}")

def extract_product_data(soup: BeautifulSoup) -> List[Dict]:
    """
    Extract product information from an e-commerce-like page.

    Args:
        soup: BeautifulSoup object

    Returns:
        List of product dictionaries
    """
    products = []

    # Find all product containers
    product_elements = soup.find_all('div', class_='product')

    for product_elem in product_elements:
        product_data = {}

        # Extract product name
        name_elem = product_elem.find('h3', class_='name') or product_elem.find('h2', class_='title')
        if name_elem:
            product_data['name'] = name_elem.get_text().strip()

        # Extract price
        price_elem = product_elem.find(class_='price') or product_elem.find(text=re.compile(r'\$\d+'))
        if price_elem:
            if isinstance(price_elem, Tag):
                price_text = price_elem.get_text()
            else:
                price_text = str(price_elem)

            # Extract numeric price
            price_match = re.search(r'\$?(\d+(?:\.\d{2})?)', price_text)
            if price_match:
                product_data['price'] = float(price_match.group(1))

        # Extract description
        desc_elem = product_elem.find('p', class_='description') or product_elem.find('div', class_='desc')
        if desc_elem:
            product_data['description'] = desc_elem.get_text().strip()

        # Extract image URL
        img_elem = product_elem.find('img')
        if img_elem:
            product_data['image'] = img_elem.get('src') or img_elem.get('data-src')

        # Extract product URL
        link_elem = product_elem.find('a')
        if link_elem:
            product_data['url'] = link_elem.get('href')

        # Only add if we found at least a name
        if 'name' in product_data:
            products.append(product_data)

    return products

def extract_article_data(soup: BeautifulSoup) -> Dict:
    """
    Extract article/blog post information.

    Args:
        soup: BeautifulSoup object

    Returns:
        Article data dictionary
    """
    article_data = {}

    # Extract title
    title_selectors = ['h1', 'h1.title', '.article-title', 'title']
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem and title_elem.get_text().strip():
            article_data['title'] = title_elem.get_text().strip()
            break

    # Extract author
    author_selectors = ['.author', '.byline', '[rel="author"]', '.post-author']
    for selector in author_selectors:
        author_elem = soup.select_one(selector)
        if author_elem:
            article_data['author'] = author_elem.get_text().strip()
            break

    # Extract publication date
    date_selectors = ['time', '.date', '.published', '.post-date']
    for selector in date_selectors:
        date_elem = soup.select_one(selector)
        if date_elem:
            # Try to get datetime attribute first, then text
            date_text = date_elem.get('datetime') or date_elem.get_text().strip()
            if date_text:
                article_data['date'] = date_text
                break

    # Extract article content
    content_selectors = ['.article-content', '.post-content', '.content', 'article']
    for selector in content_selectors:
        content_elem = soup.select_one(selector)
        if content_elem:
            # Get text content, removing extra whitespace
            content_text = content_elem.get_text(separator=' ', strip=True)
            article_data['content'] = content_text
            article_data['content_length'] = len(content_text)
            break

    # Extract tags/categories
    tag_selectors = ['.tags a', '.categories a', '.tag', '.category']
    tags = []
    for selector in tag_selectors:
        tag_elements = soup.select(selector)
        for tag_elem in tag_elements:
            tag_text = tag_elem.get_text().strip()
            if tag_text and tag_text not in tags:
                tags.append(tag_text)

    if tags:
        article_data['tags'] = tags

    return article_data

def extract_links_and_navigation(soup: BeautifulSoup, base_url: str) -> Dict:
    """
    Extract all links and navigation information.

    Args:
        soup: BeautifulSoup object
        base_url: Base URL for resolving relative links

    Returns:
        Dictionary with categorized links
    """
    from urllib.parse import urljoin, urlparse

    link_data = {
        'internal_links': [],
        'external_links': [],
        'navigation_links': [],
        'social_links': [],
        'email_links': []
    }

    base_domain = urlparse(base_url).netloc

    # Find all links
    all_links = soup.find_all('a', href=True)

    for link in all_links:
        href = link.get('href')
        text = link.get_text().strip()

        # Skip empty or javascript links
        if not href or href.startswith(('javascript:', '#')):
            continue

        # Resolve relative URLs
        full_url = urljoin(base_url, href)
        link_domain = urlparse(full_url).netloc

        link_info = {
            'url': full_url,
            'text': text,
            'title': link.get('title', ''),
            'classes': link.get('class', [])
        }

        # Categorize links
        if href.startswith('mailto:'):
            link_data['email_links'].append(link_info)
        elif link_domain == base_domain:
            # Check if it's navigation
            if any(nav_class in str(link.get('class', [])) for nav_class in ['nav', 'menu', 'navigation']):
                link_data['navigation_links'].append(link_info)
            else:
                link_data['internal_links'].append(link_info)
        else:
            # Check if it's social media
            social_domains = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 'youtube.com']
            if any(social in link_domain for social in social_domains):
                link_data['social_links'].append(link_info)
            else:
                link_data['external_links'].append(link_info)

    return link_data

def scrape_real_website_example():
    """
    Example of scraping a real website (using httpbin for demonstration).
    """
    print("🌐 Real Website Scraping Example")
    print("=" * 35)

    # Use httpbin HTML page for demonstration
    url = "https://httpbin.org/html"
    soup = get_soup(url)

    if not soup:
        print("❌ Failed to get webpage")
        return

    print(f"✅ Successfully loaded: {url}")

    # Extract basic information
    title = soup.find('title')
    if title:
        print(f"📄 Page Title: {title.get_text()}")

    # Find all headings
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if headings:
        print(f"\n📋 Headings found: {len(headings)}")
        for heading in headings[:5]:  # Show first 5
            print(f"  {heading.name.upper()}: {heading.get_text().strip()}")

    # Find all paragraphs
    paragraphs = soup.find_all('p')
    if paragraphs:
        print(f"\n📝 Paragraphs found: {len(paragraphs)}")
        for i, p in enumerate(paragraphs[:3]):  # Show first 3
            text = p.get_text().strip()
            print(f"  {i+1}. {text[:100]}{'...' if len(text) > 100 else ''}")

    # Find all links
    links = soup.find_all('a', href=True)
    if links:
        print(f"\n🔗 Links found: {len(links)}")
        for link in links[:5]:  # Show first 5
            print(f"  {link.get_text().strip()} -> {link.get('href')}")

# Example usage
if __name__ == "__main__":
    # Create sample HTML for demonstration
    sample_html = """
    <html>
    <head><title>Sample E-commerce Site</title></head>
    <body>
        <div id="header">
            <h1>My Store</h1>
            <nav class="navigation">
                <a href="/home">Home</a>
                <a href="/products">Products</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>

        <div id="main">
            <div class="product">
                <h3 class="name">Laptop Computer</h3>
                <p class="price">$999.99</p>
                <p class="description">High-performance laptop for work and gaming.</p>
                <img src="/images/laptop.jpg" alt="Laptop">
                <a href="/product/laptop">View Details</a>
            </div>

            <div class="product">
                <h3 class="name">Wireless Mouse</h3>
                <p class="price">$29.99</p>
                <p class="description">Ergonomic wireless mouse with long battery life.</p>
                <img src="/images/mouse.jpg" alt="Mouse">
                <a href="/product/mouse">View Details</a>
            </div>
        </div>
    </body>
    </html>
    """

    print("🧪 HTML Parsing Tutorial")
    print("=" * 25)

    # Demonstrate basic selectors
    demonstrate_basic_selectors(sample_html)

    # Extract product data
    soup = BeautifulSoup(sample_html, 'html.parser')
    products = extract_product_data(soup)

    print(f"\n🛍️ Extracted Products: {len(products)}")
    for i, product in enumerate(products, 1):
        print(f"  {i}. {product.get('name', 'Unknown')}")
        print(f"     Price: ${product.get('price', 'N/A')}")
        print(f"     Description: {product.get('description', 'N/A')[:50]}...")

    # Scrape real website
    print(f"\n{'='*50}")
    scrape_real_website_example()
```

### Exercise 3: Advanced Scraping Techniques
**File**: `examples/step04_advanced_scraping.py`

```python
"""
Step 4: Advanced Scraping Techniques
Sessions, cookies, forms, and dynamic content
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List, Optional
import json

class WebScraper:
    """Advanced web scraper with session management and error handling"""

    def __init__(self, delay: float = 1.0):
        self.session = requests.Session()
        self.delay = delay
        self.last_request_time = 0

        # Set default headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def wait_for_rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.delay:
            sleep_time = self.delay - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def get_page(self, url: str, params: Dict = None) -> Optional[BeautifulSoup]:
        """
        Get a webpage with session management and rate limiting.

        Args:
            url: URL to fetch
            params: Query parameters

        Returns:
            BeautifulSoup object or None
        """
        self.wait_for_rate_limit()

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            return BeautifulSoup(response.content, 'html.parser')

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch {url}: {str(e)}")
            return None

    def post_form(self, url: str, form_data: Dict) -> Optional[BeautifulSoup]:
        """
        Submit a form using POST request.

        Args:
            url: Form action URL
            form_data: Form data dictionary

        Returns:
            BeautifulSoup object or None
        """
        self.wait_for_rate_limit()

        try:
            response = self.session.post(url, data=form_data, timeout=10)
            response.raise_for_status()

            return BeautifulSoup(response.content, 'html.parser')

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to submit form to {url}: {str(e)}")
            return None

    def handle_cookies_example(self):
        """Demonstrate cookie handling"""
        print("🍪 Cookie Handling Example")
        print("=" * 30)

        # Visit a page that sets cookies
        url = "https://httpbin.org/cookies/set/session_id/ABC123"

        response = self.session.get(url)

        print(f"Cookies after visiting {url}:")
        for cookie in self.session.cookies:
            print(f"  {cookie.name}: {cookie.value}")

        # Visit a page that shows cookies
        cookie_url = "https://httpbin.org/cookies"
        response = self.session.get(cookie_url)

        try:
            cookie_data = response.json()
            print(f"Server sees these cookies: {cookie_data['cookies']}")
        except:
            print("Could not parse cookie response")

    def scrape_with_pagination(self, base_url: str, max_pages: int = 5) -> List[Dict]:
        """
        Scrape multiple pages with pagination.

        Args:
            base_url: Base URL with pagination parameter
            max_pages: Maximum pages to scrape

        Returns:
            List of scraped data from all pages
        """
        all_data = []

        for page_num in range(1, max_pages + 1):
            print(f"📄 Scraping page {page_num}/{max_pages}")

            # Example pagination URL
            page_url = f"{base_url}?page={page_num}"
            soup = self.get_page(page_url)

            if not soup:
                print(f"❌ Failed to load page {page_num}")
                continue

            # Extract data from current page
            page_data = self.extract_page_data(soup, page_num)
            all_data.extend(page_data)

            # Check if there's a next page
            if not self.has_next_page(soup):
                print(f"✅ Reached last page at page {page_num}")
                break

        return all_data

    def extract_page_data(self, soup: BeautifulSoup, page_num: int) -> List[Dict]:
        """
        Extract data from a single page.

        Args:
            soup: BeautifulSoup object
            page_num: Current page number

        Returns:
            List of data items from the page
        """
        # This is a mock implementation
        # In real scraping, you'd extract actual content

        items = []

        # Look for common content patterns
        content_elements = soup.find_all(['article', 'div', 'section'])

        for i, element in enumerate(content_elements[:5]):  # Limit to 5 per page
            text_content = element.get_text(strip=True)
            if len(text_content) > 50:  # Only meaningful content
                items.append({
                    'page': page_num,
                    'item_id': f"page_{page_num}_item_{i}",
                    'content': text_content[:200],  # First 200 chars
                    'length': len(text_content),
                    'scraped_at': time.time()
                })

        return items

    def has_next_page(self, soup: BeautifulSoup) -> bool:
        """
        Check if there's a next page available.

        Args:
            soup: BeautifulSoup object

        Returns:
            True if next page exists
        """
        # Look for common "next page" indicators
        next_indicators = [
            soup.find('a', text=re.compile(r'next', re.I)),
            soup.find('a', {'class': re.compile(r'next', re.I)}),
            soup.find('a', {'rel': 'next'}),
            soup.find(text=re.compile(r'next page', re.I))
        ]

        return any(indicator for indicator in next_indicators)

    def extract_all_images(self, url: str) -> List[Dict]:
        """
        Extract all images from a webpage.

        Args:
            url: URL to scrape images from

        Returns:
            List of image information
        """
        soup = self.get_page(url)
        if not soup:
            return []

        images = []
        img_elements = soup.find_all('img')

        for img in img_elements:
            img_data = {
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', ''),
                'width': img.get('width', ''),
                'height': img.get('height', ''),
                'class': img.get('class', [])
            }

            # Convert relative URLs to absolute
            if img_data['src'] and not img_data['src'].startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                img_data['src'] = urljoin(url, img_data['src'])

            images.append(img_data)

        return images

    def close(self):
        """Close the session"""
        self.session.close()

def demonstrate_form_handling():
    """Demonstrate handling of web forms"""
    print("📝 Form Handling Example")
    print("=" * 25)

    scraper = WebScraper()

    # Example: Get a form page
    form_url = "https://httpbin.org/forms/post"
    soup = scraper.get_page(form_url)

    if soup:
        # Find the form
        form = soup.find('form')
        if form:
            print(f"Found form with action: {form.get('action')}")
            print(f"Form method: {form.get('method', 'GET')}")

            # Find all input fields
            inputs = form.find_all(['input', 'select', 'textarea'])
            print(f"Form has {len(inputs)} input fields:")

            for inp in inputs:
                input_type = inp.get('type', inp.name)
                input_name = inp.get('name', 'unnamed')
                print(f"  {input_type}: {input_name}")

    # Example: Submit form data
    form_data = {
        'custname': 'John Doe',
        'custtel': '555-1234',
        'custemail': 'john@example.com',
        'size': 'large',
        'delivery': '1'
    }

    result_soup = scraper.post_form("https://httpbin.org/post", form_data)
    if result_soup:
        print("✅ Form submitted successfully")

    scraper.close()

def scrape_quotes_example():
    """Example scraping a quotes website"""
    print("📚 Quotes Scraping Example")
    print("=" * 30)

    scraper = WebScraper(delay=0.5)

    # Note: This is a hypothetical example
    # In practice, you'd use a real quotes website
    base_url = "https://httpbin.org/html"  # Using httpbin for demo

    quotes = []

    # Scrape multiple pages
    for page in range(1, 4):  # 3 pages
        print(f"Scraping page {page}...")

        soup = scraper.get_page(base_url)
        if soup:
            # In a real scenario, you'd extract quotes like this:
            # quote_elements = soup.find_all('div', class_='quote')
            # for quote_elem in quote_elements:
            #     quote_text = quote_elem.find('span', class_='text').get_text()
            #     author = quote_elem.find('small', class_='author').get_text()
            #     tags = [tag.get_text() for tag in quote_elem.find_all('a', class_='tag')]

            # For demo, we'll create mock data
            for i in range(3):  # 3 quotes per page
                quotes.append({
                    'text': f"This is quote {len(quotes) + 1} from page {page}",
                    'author': f"Author {(len(quotes) % 5) + 1}",
                    'tags': ['inspiration', 'wisdom'],
                    'page': page
                })

    print(f"✅ Scraped {len(quotes)} quotes total")
    for quote in quotes[:5]:  # Show first 5
        print(f"  \"{quote['text']}\" - {quote['author']}")

    scraper.close()
    return quotes

# Example usage
if __name__ == "__main__":
    print("🚀 Advanced Scraping Techniques")
    print("=" * 35)

    # Demonstrate cookie handling
    scraper = WebScraper()
    scraper.handle_cookies_example()

    print(f"\n{'='*50}")

    # Demonstrate form handling
    demonstrate_form_handling()

    print(f"\n{'='*50}")

    # Demonstrate pagination scraping
    quotes = scrape_quotes_example()

    print(f"\n{'='*50}")

    # Image extraction example
    print("🖼️ Image Extraction Example")
    print("=" * 30)

    images = scraper.extract_all_images("https://httpbin.org/html")
    print(f"Found {len(images)} images")
    for img in images[:3]:  # Show first 3
        print(f"  {img['src']} (alt: {img['alt']})")

    scraper.close()
```

## 🔍 Key Concepts Learned

### 1. HTTP Request Methods

```python
import requests

# GET request (retrieve data)
response = requests.get(url, headers=headers, params=params)

# POST request (send data)
response = requests.post(url, data=form_data, json=json_data)

# Session for persistent cookies
session = requests.Session()
response = session.get(url)
```

### 2. BeautifulSoup Selectors

```python
from bs4 import BeautifulSoup

# Find methods
soup.find('tag')                    # First matching tag
soup.find_all('tag')                # All matching tags
soup.find('tag', class_='name')     # By class
soup.find('tag', id='name')         # By ID

# CSS selectors
soup.select('tag')                  # All tags
soup.select('.class')               # By class
soup.select('#id')                  # By ID
soup.select('tag.class')            # Tag with class
soup.select('parent > child')       # Direct child
soup.select('ancestor descendant')  # Any descendant
```

### 3. Data Extraction Patterns

```python
# Text content
element.get_text()                  # All text content
element.get_text(strip=True)        # Remove extra whitespace
element.string                      # Direct text only

# Attributes
element.get('href')                 # Get attribute value
element['href']                     # Alternative syntax
element.attrs                       # All attributes

# Navigation
element.parent                      # Parent element
element.find_next_sibling()         # Next sibling
element.find_all('tag')             # Children
```

## 🧪 Practice Challenges

### Challenge 1: News Article Scraper

Create a scraper that:

- Extracts article headlines from a news website
- Gets publication dates and authors
- Follows links to full articles
- Saves data in structured format

### Challenge 2: Product Price Monitor

Build a scraper that:

- Monitors product prices on e-commerce sites
- Tracks price changes over time
- Handles different page layouts
- Deals with anti-bot measures

### Challenge 3: Social Media Link Extractor

Create a tool that:

- Finds all social media links on websites
- Categorizes links by platform
- Extracts profile information
- Generates a report of social presence

## 🎯 Next Steps

In Step 5, we'll learn about:

- Handling JavaScript-rendered content (Selenium)
- Working with APIs and JSON data
- Advanced data processing with pandas
- Building a complete scraping project

## 📝 Notes

- Always respect robots.txt and rate limits
- Use appropriate headers to avoid blocking
- Handle errors gracefully
- Session management is crucial for complex sites
- BeautifulSoup is powerful but not suitable for JavaScript-heavy sites

---

**Completion Checklist:**
- [ ] Made successful HTTP requests with requests library
- [ ] Parsed HTML content with BeautifulSoup
- [ ] Used CSS selectors and find methods
- [ ] Extracted structured data from web pages
- [ ] Handled sessions, cookies, and forms
- [ ] Completed all coding exercises
- [ ] Attempted at least one practice challenge

Ready for Step 5? Let's handle dynamic content and build a complete project! 🚀
