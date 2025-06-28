# API Reference

This document provides comprehensive API documentation for the AI-Powered Web Scraper framework.

## Table of Contents

- [Core Classes](#core-classes)
  - [WebScraper](#webscraper)
  - [AIEnhancedWebScraper](#aienhancedwebscraper)
  - [IntelligentWebScraper](#intelligentwebscraper)
- [Configuration](#configuration)
  - [ScrapingConfig](#scrapingconfig)
  - [WebScraperConfig](#webscraperconfig)
  - [PromptConfig](#promptconfig)
- [Data Models](#data-models)
  - [ScrapedData](#scrapeddata)
  - [ScrapingResult](#scrapingresult)
  - [ContentAnalysis](#contentanalysis)
- [Components](#components)
  - [ContentProcessor](#contentprocessor)
  - [ContentCategorizer](#contentcategorizer)
  - [MetadataExtractor](#metadataextractor)
  - [URLValidator](#urlvalidator)
  - [PromptEngineer](#promptengineer)
- [Exporters](#exporters)
  - [DataExporterFactory](#dataexporterfactory)
  - [JSONExporter](#jsonexporter)
  - [CSVExporter](#csvexporter)
  - [XMLExporter](#xmlexporter)
- [Interfaces](#interfaces)

## Core Classes

### WebScraper

The main scraper class that orchestrates all scraping components using dependency injection.

```python
class WebScraper(IScraper):
    def __init__(
        self,
        config: Optional[ScrapingConfig] = None,
        url_validator: Optional[IURLValidator] = None,
        categorizer: Optional[IContentCategorizer] = None,
        metadata_extractor: Optional[IMetadataExtractor] = None,
        content_processor: Optional[IContentProcessor] = None,
        session: Optional[requests.Session] = None,
    )
```

#### Methods

##### scrape_url(url: str) -> ScrapingResult

Scrapes a single URL and returns the result.

**Parameters:**
- `url` (str): The URL to scrape

**Returns:**
- `ScrapingResult`: Contains success status, scraped data, and any errors

**Example:**
```python
from src import WebScraper, ScrapingConfig

config = ScrapingConfig(delay_min=1.0, delay_max=2.0)
scraper = WebScraper(config)
result = scraper.scrape_url("https://example.com")

if result.success:
    print(f"Title: {result.data.title}")
    print(f"Category: {result.data.category}")
```

##### scrape_multiple_urls(urls: List[str]) -> List[ScrapingResult]

Scrapes multiple URLs with rate limiting.

**Parameters:**
- `urls` (List[str]): List of URLs to scrape

**Returns:**
- `List[ScrapingResult]`: List of scraping results for each URL

##### export_data(data: List[ScrapedData], filename: str, format: str) -> None

Exports scraped data to various formats.

**Parameters:**
- `data` (List[ScrapedData]): List of scraped data objects
- `filename` (str): Output filename
- `format` (str): Export format ('json', 'csv', 'xml')

### AIEnhancedWebScraper

Advanced scraper with AI-powered content analysis and categorization.

```python
class AIEnhancedWebScraper:
    def __init__(
        self,
        config: Optional[ScrapingConfig] = None,
        prompt_config: Optional[PromptConfig] = None
    )
```

#### Methods

##### analyze_content(content: str) -> ContentAnalysis

Analyzes content using AI-powered prompt engineering.

**Parameters:**
- `content` (str): Text content to analyze

**Returns:**
- `ContentAnalysis`: AI analysis results including category, quality score, and insights

##### scrape_with_analysis(url: str) -> ScrapingResult

Scrapes URL and performs AI analysis on the content.

**Parameters:**
- `url` (str): The URL to scrape

**Returns:**
- `ScrapingResult`: Enhanced result with AI analysis

### IntelligentWebScraper

High-level intelligent scraper with advanced features.

```python
class IntelligentWebScraper:
    def __init__(self, config: Dict[str, Any])
```

#### Methods

##### scrape_urls(urls: List[str]) -> List[ScrapingResult]

Scrapes multiple URLs with intelligent processing.

##### generate_report() -> Dict[str, Any]

Generates comprehensive analytics report from scraped data.

**Returns:**
- `Dict[str, Any]`: Report with statistics, categories, and insights

## Configuration

### ScrapingConfig

Basic configuration for scraping operations.

```python
@dataclass
class ScrapingConfig:
    delay_min: float = 1.0
    delay_max: float = 3.0
    timeout: int = 30
    max_retries: int = 3
    user_agent: str = "Mozilla/5.0..."
    max_content_length: int = 5000
    rate_limit_enabled: bool = True
```

**Attributes:**
- `delay_min` (float): Minimum delay between requests (seconds)
- `delay_max` (float): Maximum delay between requests (seconds)
- `timeout` (int): Request timeout in seconds
- `max_retries` (int): Maximum number of retry attempts
- `user_agent` (str): User agent string for requests
- `max_content_length` (int): Maximum content length to process
- `rate_limit_enabled` (bool): Enable rate limiting

### WebScraperConfig

Advanced configuration for intelligent scraping.

```python
@dataclass
class WebScraperConfig:
    categorization_enabled: bool = True
    quality_threshold: float = 70.0
    max_concurrent_requests: int = 5
    output_format: str = 'json'
    enable_content_analysis: bool = True
    extract_metadata: bool = True
```

### PromptConfig

Configuration for AI prompt engineering.

```python
@dataclass
class PromptConfig:
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.1
    max_tokens: int = 1000
    enable_categorization: bool = True
    enable_quality_scoring: bool = True
```

## Data Models

### ScrapedData

Data structure for scraped content.

```python
@dataclass
class ScrapedData:
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    status_code: int = 0
    quality_score: float = 0.0
```

**Attributes:**
- `url` (str): The scraped URL
- `title` (Optional[str]): Page title
- `content` (Optional[str]): Main content text
- `category` (Optional[str]): Content category
- `metadata` (Optional[Dict]): Additional metadata
- `timestamp` (Optional[datetime]): Scraping timestamp
- `status_code` (int): HTTP status code
- `quality_score` (float): Content quality score (0-100)

### ScrapingResult

Wrapper for scraping operation results.

```python
@dataclass
class ScrapingResult:
    success: bool
    data: Optional[ScrapedData] = None
    error: Optional[str] = None
    status_code: int = 0
```

### ContentAnalysis

AI analysis results for content.

```python
@dataclass
class ContentAnalysis:
    category: str
    confidence: float
    quality_score: float
    key_topics: List[str]
    sentiment: str
    word_count: int
    readability_score: float
```

## Components

### ContentProcessor

Processes and cleans scraped content.

```python
class ContentProcessor(IContentProcessor):
    def process_content(self, html: str) -> str
    def extract_text(self, soup: BeautifulSoup) -> str
    def clean_text(self, text: str) -> str
```

#### Methods

##### process_content(html: str) -> str

Processes HTML content and extracts clean text.

**Parameters:**
- `html` (str): Raw HTML content

**Returns:**
- `str`: Cleaned text content

### ContentCategorizer

Categorizes content using machine learning.

```python
class ContentCategorizer(IContentCategorizer):
    def categorize(self, content: str) -> str
    def get_category_confidence(self, content: str) -> Dict[str, float]
```

#### Methods

##### categorize(content: str) -> str

Categorizes content into predefined categories.

**Parameters:**
- `content` (str): Text content to categorize

**Returns:**
- `str`: Category name (e.g., "technology", "business", "health")

### MetadataExtractor

Extracts metadata from web pages.

```python
class MetadataExtractor(IMetadataExtractor):
    def extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]
    def extract_title(self, soup: BeautifulSoup) -> Optional[str]
    def extract_description(self, soup: BeautifulSoup) -> Optional[str]
```

#### Methods

##### extract_metadata(soup: BeautifulSoup, url: str) -> Dict[str, Any]

Extracts comprehensive metadata from a parsed HTML document.

**Parameters:**
- `soup` (BeautifulSoup): Parsed HTML document
- `url` (str): Page URL

**Returns:**
- `Dict[str, Any]`: Metadata dictionary with title, description, keywords, etc.

### URLValidator

Validates URLs before scraping.

```python
class URLValidator(IURLValidator):
    def is_valid(self, url: str) -> bool
    def normalize_url(self, url: str) -> str
```

#### Methods

##### is_valid(url: str) -> bool

Validates if a URL is properly formatted and accessible.

**Parameters:**
- `url` (str): URL to validate

**Returns:**
- `bool`: True if valid, False otherwise

### PromptEngineer

Optimizes AI prompts for content analysis.

```python
class PromptEngineer:
    def __init__(self, config: PromptConfig)
    def create_categorization_prompt(self, content: str) -> str
    def create_quality_assessment_prompt(self, content: str) -> str
    def analyze_content(self, content: str) -> ContentAnalysis
```

## Exporters

### DataExporterFactory

Factory for creating data exporters.

```python
class DataExporterFactory:
    @staticmethod
    def create_exporter(format_type: str) -> IDataExporter
```

#### Methods

##### create_exporter(format_type: str) -> IDataExporter

Creates an exporter for the specified format.

**Parameters:**
- `format_type` (str): Export format ('json', 'csv', 'xml')

**Returns:**
- `IDataExporter`: Exporter instance

### JSONExporter

Exports data to JSON format.

```python
class JSONExporter(IDataExporter):
    def export(self, data: List[ScrapedData], filename: str) -> None
```

### CSVExporter

Exports data to CSV format.

```python
class CSVExporter(IDataExporter):
    def export(self, data: List[ScrapedData], filename: str) -> None
```

### XMLExporter

Exports data to XML format.

```python
class XMLExporter(IDataExporter):
    def export(self, data: List[ScrapedData], filename: str) -> None
```

## Interfaces

The framework uses interfaces to enable dependency injection and custom implementations.

### IScraper

Main scraper interface.

```python
class IScraper(Protocol):
    def scrape_url(self, url: str) -> ScrapingResult: ...
```

### IURLValidator

URL validation interface.

```python
class IURLValidator(Protocol):
    def is_valid(self, url: str) -> bool: ...
```

### IContentCategorizer

Content categorization interface.

```python
class IContentCategorizer(Protocol):
    def categorize(self, content: str) -> str: ...
```

### IMetadataExtractor

Metadata extraction interface.

```python
class IMetadataExtractor(Protocol):
    def extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]: ...
```

### IContentProcessor

Content processing interface.

```python
class IContentProcessor(Protocol):
    def process_content(self, html: str) -> str: ...
```

### IDataExporter

Data export interface.

```python
class IDataExporter(Protocol):
    def export(self, data: List[ScrapedData], filename: str) -> None: ...
```

## Usage Examples

### Basic Scraping

```python
from src import WebScraper, ScrapingConfig

# Create configuration
config = ScrapingConfig(
    delay_min=1.0,
    delay_max=2.0,
    timeout=30
)

# Create scraper
scraper = WebScraper(config)

# Scrape single URL
result = scraper.scrape_url("https://example.com")
if result.success:
    print(f"Title: {result.data.title}")
    print(f"Category: {result.data.category}")
```

### AI-Enhanced Scraping

```python
from src import AIEnhancedWebScraper, PromptConfig

# Configure AI analysis
prompt_config = PromptConfig(
    enable_categorization=True,
    enable_quality_scoring=True
)

# Create AI-enhanced scraper
scraper = AIEnhancedWebScraper(prompt_config=prompt_config)

# Scrape with AI analysis
result = scraper.scrape_with_analysis("https://news.example.com")
if result.success:
    analysis = result.data.metadata.get('ai_analysis')
    print(f"Category: {analysis.category}")
    print(f"Quality: {analysis.quality_score}")
    print(f"Topics: {analysis.key_topics}")
```

### Batch Processing

```python
from src import IntelligentWebScraper

# Configure intelligent scraper
scraper = IntelligentWebScraper({
    'categorization_enabled': True,
    'quality_threshold': 70,
    'max_concurrent_requests': 5
})

# Batch scraping
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]
results = scraper.scrape_urls(urls)

# Generate report
report = scraper.generate_report()
print(f"Total items: {report['summary']['total_items']}")
print(f"Categories found: {len(report['categories'])}")
```

### Data Export

```python
from src import DataExporterFactory

# Get successful results
successful_data = [r.data for r in results if r.success and r.data]

# Export to different formats
json_exporter = DataExporterFactory.create_exporter('json')
csv_exporter = DataExporterFactory.create_exporter('csv')

json_exporter.export(successful_data, 'results.json')
csv_exporter.export(successful_data, 'results.csv')
```

## Error Handling

All methods follow consistent error handling patterns:

- **Return Values**: Methods return `ScrapingResult` objects with success/error status
- **Exceptions**: Framework-specific exceptions are defined in `exceptions.py`
- **Logging**: Comprehensive logging at all levels (DEBUG, INFO, WARNING, ERROR)

### Common Error Scenarios

1. **Network Errors**: Connection timeouts, DNS failures
2. **HTTP Errors**: 404, 500, rate limiting (429)
3. **Content Errors**: Invalid HTML, empty content
4. **Configuration Errors**: Invalid settings, missing dependencies

### Best Practices

1. **Always check `result.success`** before accessing data
2. **Handle rate limiting** by using appropriate delays
3. **Validate URLs** before scraping
4. **Use appropriate timeouts** for your use case
5. **Monitor quality scores** to filter low-quality content

---

*For more examples and advanced usage patterns, see the [examples directory](../tests/) and [learning steps](../learning_steps/).*
