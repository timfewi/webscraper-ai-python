# Step 5: Dynamic Content & Complete Project

## 🎯 Learning Goals

- Handle JavaScript-rendered content with Selenium
- Work with APIs and JSON data
- Process data with pandas
- Build a complete web scraping project
- Implement the AI-powered categorization system

## 📖 Theory

### Dynamic Content Challenges

Modern websites often use JavaScript to load content dynamically:

- **Single Page Applications (SPAs)**: React, Vue, Angular apps
- **Infinite Scrolling**: Content loads as you scroll
- **AJAX Requests**: Data loaded after page load
- **Interactive Elements**: Dropdowns, modals, forms

### When to Use Selenium vs. Requests

**Use Requests + BeautifulSoup when:**
- Content is in initial HTML
- No JavaScript required
- Faster and more efficient
- API endpoints are available

**Use Selenium when:**
- Content is JavaScript-rendered
- Need to interact with page elements
- Infinite scrolling or dynamic loading
- Complex user interactions required

## 💻 Coding Exercises

### Exercise 1: Selenium for Dynamic Content
**File**: `examples/step05_selenium_basics.py`

```python
"""
Step 5: Selenium for Dynamic Content
Handle JavaScript-rendered websites
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from typing import List, Dict, Optional
import json

class SeleniumScraper:
    """Selenium-based scraper for dynamic content"""

    def __init__(self, headless: bool = True, timeout: int = 10):
        """
        Initialize Selenium scraper.

        Args:
            headless: Run browser in headless mode
            timeout: Default wait timeout
        """
        self.timeout = timeout
        self.driver = None
        self.setup_driver(headless)

    def setup_driver(self, headless: bool):
        """Setup Chrome WebDriver with options"""
        try:
            chrome_options = Options()

            if headless:
                chrome_options.add_argument('--headless')

            # Common options for stability
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')

            # User agent to appear more legitimate
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(self.timeout)

            print(f"✅ Chrome WebDriver initialized (headless: {headless})")

        except Exception as e:
            print(f"❌ Failed to initialize WebDriver: {str(e)}")
            print("Make sure ChromeDriver is installed and in PATH")
            raise

    def get_page(self, url: str) -> bool:
        """
        Navigate to a webpage.

        Args:
            url: URL to navigate to

        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"🌐 Navigating to: {url}")
            self.driver.get(url)

            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            print(f"✅ Page loaded: {self.driver.title}")
            return True

        except TimeoutException:
            print(f"❌ Timeout loading page: {url}")
            return False
        except Exception as e:
            print(f"❌ Error loading page: {str(e)}")
            return False

    def wait_for_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = None) -> Optional[object]:
        """
        Wait for an element to be present.

        Args:
            selector: Element selector
            by: Selection method (CSS_SELECTOR, ID, CLASS_NAME, etc.)
            timeout: Custom timeout

        Returns:
            WebElement or None
        """
        timeout = timeout or self.timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except TimeoutException:
            print(f"❌ Element not found: {selector}")
            return None

    def scroll_to_load_content(self, scroll_count: int = 3, delay: float = 2.0):
        """
        Scroll down to load dynamic content (infinite scrolling).

        Args:
            scroll_count: Number of scrolls
            delay: Delay between scrolls
        """
        print(f"📜 Scrolling to load content ({scroll_count} scrolls)")

        for i in range(scroll_count):
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"  Scroll {i+1}/{scroll_count}")
            time.sleep(delay)

        # Scroll back to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

    def click_element(self, selector: str, by: By = By.CSS_SELECTOR) -> bool:
        """
        Click an element.

        Args:
            selector: Element selector
            by: Selection method

        Returns:
            True if successful
        """
        try:
            element = self.wait_for_element(selector, by)
            if element:
                element.click()
                print(f"✅ Clicked element: {selector}")
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to click element {selector}: {str(e)}")
            return False

    def extract_dynamic_content(self, selectors: Dict[str, str]) -> Dict:
        """
        Extract content using multiple selectors.

        Args:
            selectors: Dictionary of {field_name: css_selector}

        Returns:
            Extracted data dictionary
        """
        data = {}

        for field_name, selector in selectors.items():
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

                if len(elements) == 1:
                    # Single element
                    data[field_name] = elements[0].text.strip()
                elif len(elements) > 1:
                    # Multiple elements
                    data[field_name] = [elem.text.strip() for elem in elements]
                else:
                    # No elements found
                    data[field_name] = None

            except Exception as e:
                print(f"❌ Error extracting {field_name}: {str(e)}")
                data[field_name] = None

        return data

    def scrape_spa_example(self, url: str) -> List[Dict]:
        """
        Example: Scrape a Single Page Application.

        Args:
            url: SPA URL to scrape

        Returns:
            List of scraped items
        """
        if not self.get_page(url):
            return []

        items = []

        # Wait for content to load
        time.sleep(3)

        # Example selectors (adjust based on actual site)
        selectors = {
            'title': 'h1, h2, .title',
            'content': 'p, .content, .description',
            'links': 'a[href]'
        }

        # Extract initial content
        initial_data = self.extract_dynamic_content(selectors)
        if any(initial_data.values()):
            items.append({
                'type': 'initial_content',
                'data': initial_data,
                'timestamp': time.time()
            })

        # Try to load more content (infinite scroll)
        self.scroll_to_load_content()

        # Extract content after scrolling
        after_scroll_data = self.extract_dynamic_content(selectors)
        if any(after_scroll_data.values()):
            items.append({
                'type': 'after_scroll',
                'data': after_scroll_data,
                'timestamp': time.time()
            })

        return items

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("✅ Browser closed")

def demo_selenium_vs_requests():
    """
    Demonstrate difference between Selenium and requests
    """
    import requests
    from bs4 import BeautifulSoup

    print("🆚 Selenium vs Requests Comparison")
    print("=" * 40)

    test_url = "https://httpbin.org/html"  # Simple static page

    # Method 1: Requests + BeautifulSoup
    print("1. Requests + BeautifulSoup:")
    try:
        start_time = time.time()
        response = requests.get(test_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        requests_time = time.time() - start_time

        title = soup.find('title')
        headings = soup.find_all(['h1', 'h2'])

        print(f"  ✅ Success in {requests_time:.2f}s")
        print(f"  Title: {title.get_text() if title else 'None'}")
        print(f"  Headings found: {len(headings)}")

    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")

    # Method 2: Selenium
    print("\n2. Selenium:")
    scraper = None
    try:
        start_time = time.time()
        scraper = SeleniumScraper(headless=True)
        success = scraper.get_page(test_url)
        selenium_time = time.time() - start_time

        if success:
            title = scraper.driver.title
            headings = scraper.driver.find_elements(By.CSS_SELECTOR, 'h1, h2')

            print(f"  ✅ Success in {selenium_time:.2f}s")
            print(f"  Title: {title}")
            print(f"  Headings found: {len(headings)}")

    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
    finally:
        if scraper:
            scraper.close()

    # Comparison summary
    if 'requests_time' in locals() and 'selenium_time' in locals():
        print(f"\n📊 Performance Comparison:")
        print(f"  Requests: {requests_time:.2f}s")
        print(f"  Selenium: {selenium_time:.2f}s")
        print(f"  Selenium is {selenium_time/requests_time:.1f}x slower")

# Example usage
if __name__ == "__main__":
    print("🚀 Selenium Tutorial")
    print("=" * 20)

    # Demonstrate selenium vs requests
    demo_selenium_vs_requests()

    print(f"\n{'='*50}")

    # Example of scraping dynamic content
    print("🔄 Dynamic Content Scraping Example")
    print("=" * 35)

    scraper = SeleniumScraper(headless=True)

    try:
        # Example with a simple page
        items = scraper.scrape_spa_example("https://httpbin.org/html")

        print(f"📊 Scraped {len(items)} content sections:")
        for item in items:
            print(f"  {item['type']}: {len(str(item['data']))} characters")

    finally:
        scraper.close()
```

### Exercise 2: API Integration and Data Processing
**File**: `examples/step05_api_data_processing.py`

```python
"""
Step 5: API Integration and Data Processing
Work with APIs and process data with pandas
"""

import requests
import pandas as pd
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIDataProcessor:
    """Process and analyze scraped data using APIs and pandas"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Python Data Processor 1.0'
        })

    def fetch_api_data(self, url: str, params: Dict = None) -> Optional[Dict]:
        """
        Fetch data from API endpoint.

        Args:
            url: API endpoint URL
            params: Query parameters

        Returns:
            JSON data or None
        """
        try:
            logger.info(f"Fetching data from API: {url}")

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {str(e)}")
            return None

    def process_scraped_data_with_pandas(self, scraped_data: List[Dict]) -> pd.DataFrame:
        """
        Process scraped data using pandas.

        Args:
            scraped_data: List of scraped data dictionaries

        Returns:
            Processed pandas DataFrame
        """
        logger.info(f"Processing {len(scraped_data)} scraped items with pandas")

        # Create DataFrame
        df = pd.DataFrame(scraped_data)

        if df.empty:
            logger.warning("No data to process")
            return df

        # Data cleaning and processing
        print("📊 Data Processing Steps:")
        print(f"  Original shape: {df.shape}")

        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        print(f"  After removing duplicates: {len(df)} (removed {initial_count - len(df)})")

        # Handle missing values
        missing_counts = df.isnull().sum()
        if missing_counts.any():
            print(f"  Missing values found:")
            for col, count in missing_counts.items():
                if count > 0:
                    print(f"    {col}: {count}")

        # Add timestamp if not present
        if 'scraped_at' not in df.columns:
            df['scraped_at'] = datetime.now()

        # Convert timestamp to datetime if it's numeric
        if 'scraped_at' in df.columns:
            if df['scraped_at'].dtype in ['int64', 'float64']:
                df['scraped_at'] = pd.to_datetime(df['scraped_at'], unit='s')

        # Add processing metadata
        df['processed_at'] = datetime.now()
        df['data_quality_score'] = self.calculate_data_quality_score(df)

        print(f"  Final shape: {df.shape}")
        print(f"  Data types:\n{df.dtypes}")

        return df

    def calculate_data_quality_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate data quality score for each row.

        Args:
            df: DataFrame to analyze

        Returns:
            Series with quality scores (0-100)
        """
        scores = []

        for _, row in df.iterrows():
            score = 100  # Start with perfect score

            # Penalize missing values
            missing_ratio = row.isnull().sum() / len(row)
            score -= missing_ratio * 30

            # Check content quality (if content column exists)
            if 'content' in row and pd.notna(row['content']):
                content_length = len(str(row['content']))
                if content_length < 50:
                    score -= 20  # Very short content
                elif content_length < 100:
                    score -= 10  # Short content

            # Check URL validity (if url column exists)
            if 'url' in row and pd.notna(row['url']):
                url = str(row['url'])
                if not url.startswith(('http://', 'https://')):
                    score -= 15

            scores.append(max(0, score))  # Ensure non-negative

        return pd.Series(scores)

    def analyze_scraped_content(self, df: pd.DataFrame) -> Dict:
        """
        Perform analysis on scraped content.

        Args:
            df: DataFrame with scraped data

        Returns:
            Analysis results dictionary
        """
        if df.empty:
            return {'error': 'No data to analyze'}

        analysis = {
            'total_items': len(df),
            'date_range': {
                'start': df['scraped_at'].min() if 'scraped_at' in df.columns else None,
                'end': df['scraped_at'].max() if 'scraped_at' in df.columns else None
            },
            'data_quality': {
                'average_score': df['data_quality_score'].mean() if 'data_quality_score' in df.columns else None,
                'high_quality_items': len(df[df['data_quality_score'] >= 80]) if 'data_quality_score' in df.columns else None
            }
        }

        # Content analysis
        if 'content' in df.columns:
            content_lengths = df['content'].astype(str).str.len()
            analysis['content_analysis'] = {
                'average_length': content_lengths.mean(),
                'median_length': content_lengths.median(),
                'min_length': content_lengths.min(),
                'max_length': content_lengths.max()
            }

        # Domain analysis
        if 'url' in df.columns:
            domains = df['url'].astype(str).str.extract(r'https?://([^/]+)')[0]
            domain_counts = domains.value_counts()
            analysis['domain_analysis'] = {
                'unique_domains': len(domain_counts),
                'top_domains': domain_counts.head().to_dict()
            }

        return analysis

    def categorize_content_with_keywords(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Simple keyword-based content categorization.

        Args:
            df: DataFrame with content to categorize

        Returns:
            DataFrame with added category column
        """
        if 'content' not in df.columns:
            logger.warning("No content column found for categorization")
            return df

        # Define category keywords
        category_keywords = {
            'technology': ['tech', 'software', 'computer', 'digital', 'AI', 'machine learning', 'programming'],
            'business': ['business', 'market', 'company', 'financial', 'profit', 'investment', 'economy'],
            'health': ['health', 'medical', 'doctor', 'hospital', 'medicine', 'treatment', 'wellness'],
            'education': ['education', 'school', 'university', 'learning', 'student', 'teacher', 'course'],
            'entertainment': ['movie', 'music', 'game', 'entertainment', 'celebrity', 'show', 'film'],
            'sports': ['sports', 'football', 'basketball', 'soccer', 'athlete', 'team', 'game', 'championship'],
            'news': ['news', 'breaking', 'report', 'journalist', 'media', 'press', 'update']
        }

        def categorize_text(text):
            """Categorize single text based on keywords"""
            if pd.isna(text):
                return 'unknown'

            text_lower = str(text).lower()
            category_scores = {}

            for category, keywords in category_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    category_scores[category] = score

            if category_scores:
                return max(category_scores.items(), key=lambda x: x[1])[0]
            else:
                return 'general'

        # Apply categorization
        logger.info("Categorizing content based on keywords...")
        df['category'] = df['content'].apply(categorize_text)

        # Category distribution
        category_counts = df['category'].value_counts()
        logger.info(f"Category distribution:\n{category_counts}")

        return df

    def enrich_data_with_external_apis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich scraped data with external API data.

        Args:
            df: DataFrame to enrich

        Returns:
            Enriched DataFrame
        """
        logger.info("Enriching data with external APIs...")

        # Example: Add timezone information based on domains
        if 'url' in df.columns:
            # Extract domains
            domains = df['url'].astype(str).str.extract(r'https?://([^/]+)')[0]

            # Mock API data (in real scenario, you'd call actual APIs)
            domain_info = {}
            unique_domains = domains.dropna().unique()

            for domain in unique_domains[:5]:  # Limit to 5 for demo
                # Simulate API call delay
                time.sleep(0.1)

                # Mock data (replace with real API calls)
                domain_info[domain] = {
                    'country': 'US' if '.com' in domain else 'Unknown',
                    'is_commercial': '.com' in domain,
                    'estimated_traffic': 'high' if domain in ['google.com', 'facebook.com'] else 'medium'
                }

            # Add enriched data to DataFrame
            df['domain'] = domains
            df['domain_country'] = df['domain'].map(lambda x: domain_info.get(x, {}).get('country', 'Unknown'))
            df['is_commercial'] = df['domain'].map(lambda x: domain_info.get(x, {}).get('is_commercial', False))

        return df

    def generate_insights_report(self, df: pd.DataFrame) -> str:
        """
        Generate insights report from processed data.

        Args:
            df: Processed DataFrame

        Returns:
            Formatted report string
        """
        if df.empty:
            return "No data available for report generation."

        analysis = self.analyze_scraped_content(df)

        report = f"""
📊 WEB SCRAPING INSIGHTS REPORT
{'='*50}

📈 OVERVIEW
Total items scraped: {analysis['total_items']}
Data quality average: {analysis['data_quality'].get('average_score', 'N/A'):.1f}/100
High quality items: {analysis['data_quality'].get('high_quality_items', 'N/A')}

"""

        # Content analysis
        if 'content_analysis' in analysis:
            content = analysis['content_analysis']
            report += f"""
📄 CONTENT ANALYSIS
Average content length: {content['average_length']:.0f} characters
Content length range: {content['min_length']:.0f} - {content['max_length']:.0f}
Median content length: {content['median_length']:.0f} characters

"""

        # Domain analysis
        if 'domain_analysis' in analysis:
            domain = analysis['domain_analysis']
            report += f"""
🌐 DOMAIN ANALYSIS
Unique domains: {domain['unique_domains']}
Top domains:
"""
            for domain_name, count in domain['top_domains'].items():
                report += f"  {domain_name}: {count} items\n"

        # Category analysis
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            report += f"""
🏷️ CATEGORY ANALYSIS
Categories found: {len(category_counts)}
Distribution:
"""
            for category, count in category_counts.items():
                percentage = (count / len(df)) * 100
                report += f"  {category}: {count} ({percentage:.1f}%)\n"

        return report

def create_sample_scraped_data() -> List[Dict]:
    """Create sample scraped data for demonstration"""
    return [
        {
            'url': 'https://techcrunch.com/article1',
            'title': 'New AI Breakthrough in Machine Learning',
            'content': 'Researchers have developed a new machine learning algorithm that can process natural language with unprecedented accuracy.',
            'scraped_at': time.time() - 3600
        },
        {
            'url': 'https://businessinsider.com/article2',
            'title': 'Stock Market Reaches New Heights',
            'content': 'The stock market continues to grow as investors show confidence in the economic recovery.',
            'scraped_at': time.time() - 1800
        },
        {
            'url': 'https://healthline.com/article3',
            'title': 'Benefits of Regular Exercise',
            'content': 'New study shows that regular exercise can significantly improve mental health and cognitive function.',
            'scraped_at': time.time() - 900
        },
        {
            'url': 'https://espn.com/article4',
            'title': 'Championship Game Highlights',
            'content': 'Last nights championship game was filled with incredible plays and outstanding athletic performance.',
            'scraped_at': time.time() - 600
        },
        {
            'url': 'https://example.com/article5',
            'title': 'Local Community Event',
            'content': 'The annual community festival brought together families for a day of fun and celebration.',
            'scraped_at': time.time() - 300
        }
    ]

# Example usage
if __name__ == "__main__":
    print("🚀 API Integration & Data Processing Tutorial")
    print("=" * 50)

    # Create processor
    processor = APIDataProcessor()

    # Get sample data
    sample_data = create_sample_scraped_data()
    print(f"📥 Created {len(sample_data)} sample items")

    # Process with pandas
    df = processor.process_scraped_data_with_pandas(sample_data)

    # Categorize content
    df = processor.categorize_content_with_keywords(df)

    # Enrich with external data
    df = processor.enrich_data_with_external_apis(df)

    # Generate insights
    report = processor.generate_insights_report(df)
    print(report)

    # Save processed data
    output_file = 'data/processed_scraped_data.csv'
    df.to_csv(output_file, index=False)
    print(f"💾 Processed data saved to: {output_file}")
```

### Exercise 3: Complete AI-Powered Web Scraper Project
**File**: `src/ai_web_scraper.py`

```python
"""
Complete AI-Powered Web Scraper
Bringing together all concepts learned
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import re
from dataclasses import dataclass, asdict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ScrapedItem:
    """Data class for scraped items"""
    url: str
    title: str = ""
    content: str = ""
    category: str = "unknown"
    scraped_at: datetime = None
    quality_score: float = 0.0

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()

class AIWebScraper:
    """
    Complete AI-powered web scraper implementation
    """

    def __init__(self, config: Dict = None):
        """
        Initialize the AI web scraper.

        Args:
            config: Configuration dictionary
        """
        self.config = config or self.get_default_config()
        self.session = requests.Session()
        self.setup_session()
        self.scraped_data = []

        # Create output directory
        Path(self.config['output_dir']).mkdir(parents=True, exist_ok=True)

        logger.info("AI Web Scraper initialized")

    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'delay_between_requests': 1.0,
            'timeout': 10,
            'max_retries': 3,
            'output_dir': 'data',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'respect_robots_txt': True,
            'categorization_enabled': True
        }

    def setup_session(self):
        """Setup HTTP session with headers"""
        self.session.headers.update({
            'User-Agent': self.config['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def validate_url(self, url: str) -> Tuple[bool, str]:
        """
        Validate URL for scraping.

        Args:
            url: URL to validate

        Returns:
            Tuple of (is_valid, message)
        """
        if not url or not isinstance(url, str):
            return False, "URL must be a non-empty string"

        if not url.startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"

        # Basic URL pattern validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(url):
            return False, "URL format is invalid"

        return True, "URL is valid"

    def make_request(self, url: str) -> Optional[requests.Response]:
        """
        Make HTTP request with error handling and retries.

        Args:
            url: URL to request

        Returns:
            Response object or None
        """
        for attempt in range(self.config['max_retries']):
            try:
                logger.debug(f"Making request to {url} (attempt {attempt + 1})")

                response = self.session.get(
                    url,
                    timeout=self.config['timeout'],
                    allow_redirects=True
                )
                response.raise_for_status()

                # Rate limiting
                time.sleep(self.config['delay_between_requests'])

                return response

            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}): {str(e)}")
                if attempt < self.config['max_retries'] - 1:
                    time.sleep((attempt + 1) * 2)  # Exponential backoff
                else:
                    logger.error(f"All retry attempts failed for {url}")

        return None

    def extract_content(self, response: requests.Response) -> Dict:
        """
        Extract content from HTTP response.

        Args:
            response: HTTP response object

        Returns:
            Extracted content dictionary
        """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title_element = soup.find('title')
            title = title_element.get_text().strip() if title_element else ""

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract main content
            content = ""

            # Try common content selectors
            content_selectors = [
                'article',
                '.content',
                '.main-content',
                '.post-content',
                '.article-content',
                'main',
                '#content',
                '.entry-content'
            ]

            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    content = content_element.get_text(separator=' ', strip=True)
                    break

            # If no specific content area found, use body
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text(separator=' ', strip=True)

            # Extract metadata
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description.get('content', '') if meta_description else ''

            return {
                'title': title,
                'content': content,
                'description': description,
                'content_length': len(content),
                'word_count': len(content.split()) if content else 0
            }

        except Exception as e:
            logger.error(f"Content extraction failed: {str(e)}")
            return {
                'title': '',
                'content': '',
                'description': '',
                'content_length': 0,
                'word_count': 0
            }

    def categorize_content(self, content: str, title: str = "") -> str:
        """
        AI-powered content categorization using keyword analysis.

        Args:
            content: Text content to categorize
            title: Page title

        Returns:
            Category string
        """
        if not self.config['categorization_enabled']:
            return 'uncategorized'

        # Combine title and content for analysis
        text = f"{title} {content}".lower()

        # Category keywords (simplified AI categorization)
        categories = {
            'technology': [
                'technology', 'software', 'computer', 'programming', 'coding',
                'artificial intelligence', 'ai', 'machine learning', 'data science',
                'blockchain', 'cryptocurrency', 'app', 'mobile', 'web development'
            ],
            'business': [
                'business', 'company', 'corporate', 'enterprise', 'startup',
                'market', 'finance', 'investment', 'economy', 'profit',
                'revenue', 'sales', 'marketing', 'strategy'
            ],
            'health': [
                'health', 'medical', 'healthcare', 'medicine', 'doctor',
                'hospital', 'treatment', 'disease', 'wellness', 'fitness',
                'nutrition', 'mental health', 'therapy'
            ],
            'science': [
                'science', 'research', 'study', 'experiment', 'discovery',
                'biology', 'chemistry', 'physics', 'astronomy', 'climate',
                'environment', 'nature'
            ],
            'education': [
                'education', 'school', 'university', 'college', 'learning',
                'student', 'teacher', 'course', 'training', 'academic',
                'degree', 'curriculum'
            ],
            'entertainment': [
                'entertainment', 'movie', 'film', 'music', 'game', 'gaming',
                'celebrity', 'show', 'television', 'streaming', 'media',
                'culture', 'art'
            ],
            'sports': [
                'sports', 'football', 'basketball', 'soccer', 'baseball',
                'athlete', 'team', 'game', 'championship', 'league',
                'fitness', 'exercise'
            ],
            'news': [
                'news', 'breaking', 'report', 'journalist', 'press',
                'politics', 'government', 'election', 'policy', 'world'
            ]
        }

        # Calculate category scores
        category_scores = {}
        for category, keywords in categories.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Weight by keyword importance and frequency
                    frequency = text.count(keyword)
                    importance = 2 if keyword in title.lower() else 1
                    score += frequency * importance

            if score > 0:
                category_scores[category] = score

        # Return category with highest score
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])[0]
            logger.debug(f"Categorized as '{best_category}' with scores: {category_scores}")
            return best_category

        return 'general'

    def calculate_quality_score(self, extracted_data: Dict) -> float:
        """
        Calculate quality score for scraped content.

        Args:
            extracted_data: Extracted content data

        Returns:
            Quality score (0-100)
        """
        score = 100.0

        # Title quality
        title = extracted_data.get('title', '')
        if not title:
            score -= 20
        elif len(title) < 10:
            score -= 10

        # Content quality
        content = extracted_data.get('content', '')
        word_count = extracted_data.get('word_count', 0)

        if not content:
            score -= 40
        elif word_count < 50:
            score -= 30
        elif word_count < 100:
            score -= 15

        # Content/title ratio
        if title and content:
            if len(title) > len(content) / 2:
                score -= 10  # Title too long relative to content

        return max(0.0, score)

    def scrape_url(self, url: str) -> Optional[ScrapedItem]:
        """
        Scrape a single URL.

        Args:
            url: URL to scrape

        Returns:
            ScrapedItem or None if failed
        """
        # Validate URL
        is_valid, message = self.validate_url(url)
        if not is_valid:
            logger.error(f"Invalid URL {url}: {message}")
            return None

        logger.info(f"Scraping: {url}")

        # Make request
        response = self.make_request(url)
        if not response:
            logger.error(f"Failed to fetch {url}")
            return None

        # Extract content
        extracted_data = self.extract_content(response)

        # Categorize content
        category = self.categorize_content(
            extracted_data['content'],
            extracted_data['title']
        )

        # Calculate quality score
        quality_score = self.calculate_quality_score(extracted_data)

        # Create scraped item
        item = ScrapedItem(
            url=url,
            title=extracted_data['title'],
            content=extracted_data['content'],
            category=category,
            quality_score=quality_score
        )

        logger.info(f"✅ Scraped {url} - Category: {category}, Quality: {quality_score:.1f}")

        return item

    def scrape_urls(self, urls: List[str]) -> List[ScrapedItem]:
        """
        Scrape multiple URLs.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of successfully scraped items
        """
        logger.info(f"Starting batch scrape of {len(urls)} URLs")

        scraped_items = []

        for i, url in enumerate(urls, 1):
            logger.info(f"Processing {i}/{len(urls)}: {url}")

            item = self.scrape_url(url)
            if item:
                scraped_items.append(item)
                self.scraped_data.append(item)

        logger.info(f"Batch scrape complete: {len(scraped_items)}/{len(urls)} successful")

        return scraped_items

    def save_data(self, filename: str = None) -> str:
        """
        Save scraped data to file.

        Args:
            filename: Output filename (optional)

        Returns:
            Path to saved file
        """
        if not self.scraped_data:
            logger.warning("No data to save")
            return ""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}.json"

        filepath = Path(self.config['output_dir']) / filename

        # Convert to dictionaries for JSON serialization
        data_dicts = []
        for item in self.scraped_data:
            item_dict = asdict(item)
            item_dict['scraped_at'] = item_dict['scraped_at'].isoformat()
            data_dicts.append(item_dict)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_dicts, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 Data saved to: {filepath}")
        return str(filepath)

    def generate_report(self) -> Dict:
        """
        Generate analysis report of scraped data.

        Returns:
            Report dictionary
        """
        if not self.scraped_data:
            return {'error': 'No data available'}

        # Convert to DataFrame for analysis
        df = pd.DataFrame([asdict(item) for item in self.scraped_data])

        # Category analysis
        category_counts = df['category'].value_counts().to_dict()

        # Quality analysis
        avg_quality = df['quality_score'].mean()
        high_quality_count = len(df[df['quality_score'] >= 80])

        # Content analysis
        avg_content_length = df['content'].str.len().mean()

        report = {
            'summary': {
                'total_items': len(self.scraped_data),
                'average_quality_score': round(avg_quality, 2),
                'high_quality_items': high_quality_count,
                'average_content_length': round(avg_content_length, 0)
            },
            'categories': category_counts,
            'quality_distribution': {
                'excellent (90+)': len(df[df['quality_score'] >= 90]),
                'good (80-89)': len(df[(df['quality_score'] >= 80) & (df['quality_score'] < 90)]),
                'fair (70-79)': len(df[(df['quality_score'] >= 70) & (df['quality_score'] < 80)]),
                'poor (<70)': len(df[df['quality_score'] < 70])
            }
        }

        return report

# Example usage and demonstration
if __name__ == "__main__":
    print("🤖 AI-Powered Web Scraper Demo")
    print("=" * 40)

    # Test URLs for demonstration
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html",
        # Add more URLs as needed for testing
    ]

    # Create and configure scraper
    config = {
        'delay_between_requests': 0.5,  # Faster for demo
        'categorization_enabled': True,
        'output_dir': 'data'
    }

    scraper = AIWebScraper(config)

    # Scrape URLs
    scraped_items = scraper.scrape_urls(test_urls)

    # Generate and display report
    report = scraper.generate_report()

    print("\n📊 SCRAPING REPORT")
    print("=" * 30)
    print(f"Total items: {report['summary']['total_items']}")
    print(f"Average quality: {report['summary']['average_quality_score']}")
    print(f"High quality items: {report['summary']['high_quality_items']}")

    print("\n🏷️ Categories:")
    for category, count in report['categories'].items():
        print(f"  {category}: {count}")

    print("\n⭐ Quality Distribution:")
    for quality_range, count in report['quality_distribution'].items():
        print(f"  {quality_range}: {count}")

    # Save data
    saved_file = scraper.save_data()
    print(f"\n💾 Data saved to: {saved_file}")
```

## 🔍 Key Concepts Learned

### 1. Selenium WebDriver

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Navigate and wait
driver.get(url)
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "selector"))
)
```

### 2. Data Processing with Pandas

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame(data)

# Data cleaning
df = df.drop_duplicates()
df = df.dropna()

# Analysis
df.describe()
df.groupby('category').size()
df['column'].value_counts()
```

### 3. API Integration

```python
import requests

# GET request
response = requests.get(api_url, params=params)
data = response.json()

# POST request
response = requests.post(api_url, json=payload)
```

## 🧪 Practice Challenges

### Challenge 1: E-commerce Price Monitor

Build a complete system that:

- Monitors product prices across multiple sites
- Detects price changes
- Sends notifications
- Stores historical data
- Generates price trend reports

### Challenge 2: News Aggregator

Create an AI-powered news aggregator that:

- Scrapes multiple news sources
- Categorizes articles by topic
- Detects duplicate stories
- Ranks articles by importance
- Generates daily summaries

### Challenge 3: Social Media Sentiment Analyzer

Develop a tool that:

- Collects social media posts about brands
- Analyzes sentiment using AI
- Tracks trending topics
- Generates brand reputation reports
- Monitors competitor mentions

## 🎯 Project Extension Ideas

### Add Machine Learning

- Use scikit-learn for better categorization
- Implement text similarity detection
- Add sentiment analysis
- Create recommendation systems

### Scale the System

- Add database storage (SQLite, PostgreSQL)
- Implement distributed scraping
- Add web dashboard with Flask/Django
- Create REST API for data access

### Advanced Features

- Add image recognition and processing
- Implement real-time scraping
- Add data visualization with matplotlib/plotly
- Create automated reporting system

## 📝 Notes

- Combine Selenium and requests based on needs
- Use pandas for efficient data processing
- Implement proper error handling and logging
- Respect rate limits and robots.txt
- Consider ethical and legal implications

---

**Completion Checklist:**
- [ ] Understood when to use Selenium vs requests
- [ ] Can handle JavaScript-rendered content
- [ ] Processed data with pandas
- [ ] Integrated external APIs
- [ ] Built complete scraping project
- [ ] Implemented AI-powered categorization
- [ ] Generated insights and reports
- [ ] Completed all coding exercises

🎉 **Congratulations!** You've built a complete AI-powered web scraper and learned Python fundamentals through practical application!

## 🚀 Next Steps

Continue your Python journey by exploring:

- **Web Development**: Flask, Django, FastAPI
- **Data Science**: NumPy, SciPy, matplotlib, seaborn
- **Machine Learning**: scikit-learn, TensorFlow, PyTorch
- **Automation**: pytest, CI/CD, deployment
- **Advanced Topics**: Async programming, microservices, cloud computing
