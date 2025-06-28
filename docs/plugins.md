# Plugin Development Guide

This guide provides comprehensive instructions for extending the AI-Powered Web Scraper framework through custom plugins and components.

## Table of Contents

- [Overview](#overview)
- [Plugin Architecture](#plugin-architecture)
- [Creating Custom Components](#creating-custom-components)
- [Plugin Types](#plugin-types)
- [Development Workflow](#development-workflow)
- [Best Practices](#best-practices)
- [Testing Plugins](#testing-plugins)
- [Publishing Plugins](#publishing-plugins)

## Overview

The AI-Powered Web Scraper framework is designed with extensibility in mind. Through its interface-based architecture and dependency injection pattern, you can easily create custom components to extend functionality without modifying the core framework.

### Extension Points

The framework provides several extension points:

- **Content Processors**: Custom content extraction and cleaning
- **Categorizers**: Custom content categorization algorithms
- **Metadata Extractors**: Custom metadata extraction logic
- **URL Validators**: Custom URL validation rules
- **Data Exporters**: Custom export formats and destinations
- **AI Analyzers**: Custom AI-powered content analysis
- **Rate Limiters**: Custom rate limiting strategies

## Plugin Architecture

### Interface-Based Design

All plugins implement specific interfaces that define contracts for functionality:

```python
from abc import ABC, abstractmethod
from typing import Protocol

# Example: Content Processor Interface
class IContentProcessor(Protocol):
    def process_content(self, html: str) -> str:
        """Process HTML content and return cleaned text."""
        ...

# Example: Categorizer Interface
class IContentCategorizer(Protocol):
    def categorize(self, content: str) -> str:
        """Categorize content and return category name."""
        ...

    def get_category_confidence(self, content: str) -> Dict[str, float]:
        """Get confidence scores for all categories."""
        ...
```

### Plugin Registration

Plugins are registered through dependency injection or factory patterns:

```python
# Method 1: Direct injection
custom_processor = MyCustomProcessor()
scraper = WebScraper(content_processor=custom_processor)

# Method 2: Factory registration
DataExporterFactory.register('custom_format', MyCustomExporter)

# Method 3: Plugin manager (future enhancement)
plugin_manager.register_plugin('processor', MyCustomProcessor)
```

## Creating Custom Components

### 1. Custom Content Processor

Create a content processor that extracts article text using advanced algorithms:

```python
from typing import Optional
from bs4 import BeautifulSoup, Tag
import re
from src.interfaces import IContentProcessor

class AdvancedContentProcessor(IContentProcessor):
    """Advanced content processor using readability algorithms."""

    def __init__(self, min_text_length: int = 100):
        self.min_text_length = min_text_length
        self.content_indicators = [
            'article', 'main', 'content', 'post', 'entry',
            'story', 'body-text', 'article-body'
        ]

    def process_content(self, html: str) -> str:
        """Process HTML using advanced content extraction."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unwanted elements
        self._remove_noise_elements(soup)

        # Find main content using multiple strategies
        main_content = self._extract_main_content(soup)

        if main_content:
            text = self._clean_text(main_content.get_text())
            return text if len(text) >= self.min_text_length else ""

        return ""

    def _remove_noise_elements(self, soup: BeautifulSoup) -> None:
        """Remove navigation, ads, and other noise elements."""
        noise_selectors = [
            'nav', 'header', 'footer', 'aside',
            '.navigation', '.menu', '.sidebar',
            '.advertisement', '.ad', '.popup',
            'script', 'style', 'noscript'
        ]

        for selector in noise_selectors:
            for element in soup.select(selector):
                element.decompose()

    def _extract_main_content(self, soup: BeautifulSoup) -> Optional[Tag]:
        """Extract main content using various strategies."""
        # Strategy 1: Look for semantic HTML5 elements
        for tag in ['article', 'main']:
            element = soup.find(tag)
            if element and self._is_content_rich(element):
                return element

        # Strategy 2: Look for content indicators in class/id names
        for indicator in self.content_indicators:
            for attr in ['class', 'id']:
                element = soup.find(attrs={attr: re.compile(indicator, re.I)})
                if element and self._is_content_rich(element):
                    return element

        # Strategy 3: Find element with most text content
        candidates = soup.find_all(['div', 'section', 'article'])
        if candidates:
            best_candidate = max(candidates, key=lambda x: len(x.get_text()))
            if self._is_content_rich(best_candidate):
                return best_candidate

        # Fallback: use body
        return soup.find('body')

    def _is_content_rich(self, element: Tag) -> bool:
        """Check if element contains substantial content."""
        text = element.get_text()

        # Basic checks
        if len(text) < self.min_text_length:
            return False

        # Check for reasonable text-to-HTML ratio
        html_length = len(str(element))
        text_ratio = len(text) / html_length if html_length > 0 else 0

        return text_ratio > 0.1  # At least 10% text content

    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove common web artifacts
        text = re.sub(r'\b(skip to|jump to|click here|read more)\b', '', text, flags=re.I)

        return text.strip()

# Usage
advanced_processor = AdvancedContentProcessor(min_text_length=200)
scraper = WebScraper(content_processor=advanced_processor)
```

### 2. Custom Machine Learning Categorizer

Create a categorizer using a pre-trained machine learning model:

```python
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict
from src.interfaces import IContentCategorizer

class MLContentCategorizer(IContentCategorizer):
    """Machine learning-based content categorizer."""

    def __init__(self, model_path: str, vectorizer_path: str):
        """Initialize with pre-trained model and vectorizer."""
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)

        self.categories = [
            'technology', 'business', 'health', 'sports',
            'entertainment', 'politics', 'science', 'other'
        ]

    def categorize(self, content: str) -> str:
        """Categorize content using ML model."""
        if not content.strip():
            return 'other'

        # Vectorize content
        features = self.vectorizer.transform([content])

        # Predict category
        prediction = self.model.predict(features)[0]

        return self.categories[prediction] if prediction < len(self.categories) else 'other'

    def get_category_confidence(self, content: str) -> Dict[str, float]:
        """Get confidence scores for all categories."""
        if not content.strip():
            return {category: 0.0 for category in self.categories}

        # Vectorize content
        features = self.vectorizer.transform([content])

        # Get probability scores
        probabilities = self.model.predict_proba(features)[0]

        return {
            category: float(prob)
            for category, prob in zip(self.categories, probabilities)
        }

    def train_model(self, training_data: List[tuple]) -> None:
        """Train the model with new data."""
        texts, labels = zip(*training_data)

        # Re-fit vectorizer
        self.vectorizer.fit(texts)
        features = self.vectorizer.transform(texts)

        # Train model
        self.model.fit(features, labels)

    def save_model(self, model_path: str, vectorizer_path: str) -> None:
        """Save trained model and vectorizer."""
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)

        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)

# Usage
ml_categorizer = MLContentCategorizer(
    model_path='models/content_classifier.pkl',
    vectorizer_path='models/tfidf_vectorizer.pkl'
)
scraper = WebScraper(categorizer=ml_categorizer)
```

### 3. Custom Database Exporter

Create an exporter that saves data to a database:

```python
import sqlite3
import json
from typing import List
from datetime import datetime
from src.interfaces import IDataExporter
from src.models import ScrapedData

class DatabaseExporter(IDataExporter):
    """Export scraped data to SQLite database."""

    def __init__(self, database_path: str, table_name: str = 'scraped_data'):
        self.database_path = database_path
        self.table_name = table_name
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Create database table if it doesn't exist."""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    title TEXT,
                    content TEXT,
                    category TEXT,
                    metadata TEXT,
                    quality_score REAL,
                    status_code INTEGER,
                    timestamp TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create indexes for better performance
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_url ON {self.table_name}(url)')
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_category ON {self.table_name}(category)')
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_timestamp ON {self.table_name}(timestamp)')

    def export(self, data: List[ScrapedData], filename: str) -> None:
        """Export data to database."""
        with sqlite3.connect(self.database_path) as conn:
            for item in data:
                # Serialize metadata to JSON
                metadata_json = json.dumps(item.metadata) if item.metadata else None

                # Convert timestamp to string
                timestamp_str = item.timestamp.isoformat() if item.timestamp else None

                conn.execute(f'''
                    INSERT INTO {self.table_name}
                    (url, title, content, category, metadata, quality_score, status_code, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.url,
                    item.title,
                    item.content,
                    item.category,
                    metadata_json,
                    item.quality_score,
                    item.status_code,
                    timestamp_str
                ))

    def query_data(self,
                   category: str = None,
                   min_quality: float = None,
                   start_date: datetime = None,
                   end_date: datetime = None) -> List[ScrapedData]:
        """Query data from database with filters."""
        query = f'SELECT * FROM {self.table_name} WHERE 1=1'
        params = []

        if category:
            query += ' AND category = ?'
            params.append(category)

        if min_quality is not None:
            query += ' AND quality_score >= ?'
            params.append(min_quality)

        if start_date:
            query += ' AND timestamp >= ?'
            params.append(start_date.isoformat())

        if end_date:
            query += ' AND timestamp <= ?'
            params.append(end_date.isoformat())

        with sqlite3.connect(self.database_path) as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.execute(query, params)

            results = []
            for row in cursor.fetchall():
                # Deserialize metadata
                metadata = json.loads(row['metadata']) if row['metadata'] else {}

                # Parse timestamp
                timestamp = datetime.fromisoformat(row['timestamp']) if row['timestamp'] else None

                data = ScrapedData(
                    url=row['url'],
                    title=row['title'],
                    content=row['content'],
                    category=row['category'],
                    metadata=metadata,
                    quality_score=row['quality_score'],
                    status_code=row['status_code'],
                    timestamp=timestamp
                )
                results.append(data)

            return results

# Register with factory
DataExporterFactory.register('database', DatabaseExporter)

# Usage
db_exporter = DatabaseExporter('scraped_data.db')
scraper = WebScraper()

# Scrape data
results = scraper.scrape_multiple_urls(['https://example.com'])
successful_data = [r.data for r in results if r.success and r.data]

# Export to database
db_exporter.export(successful_data, 'scraped_data.db')

# Query data
high_quality_tech = db_exporter.query_data(
    category='technology',
    min_quality=80.0
)
```

### 4. Custom Rate Limiter

Create a sophisticated rate limiter with multiple strategies:

```python
import time
import threading
from collections import defaultdict, deque
from typing import Dict, Optional
from urllib.parse import urlparse

class AdaptiveRateLimiter:
    """Adaptive rate limiter that adjusts based on server responses."""

    def __init__(self, default_delay: float = 1.0):
        self.default_delay = default_delay
        self.domain_delays: Dict[str, float] = defaultdict(lambda: default_delay)
        self.last_request_times: Dict[str, float] = {}
        self.request_counts: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.lock = threading.Lock()

    def wait_if_needed(self, url: str) -> None:
        """Wait if necessary before making request."""
        domain = self._extract_domain(url)

        with self.lock:
            current_time = time.time()
            last_request = self.last_request_times.get(domain, 0)
            required_delay = self.domain_delays[domain]

            elapsed = current_time - last_request
            if elapsed < required_delay:
                wait_time = required_delay - elapsed
                time.sleep(wait_time)

            self.last_request_times[domain] = time.time()
            self.request_counts[domain].append(time.time())

    def record_response(self, url: str, status_code: int, response_time: float) -> None:
        """Record response to adjust rate limiting."""
        domain = self._extract_domain(url)

        with self.lock:
            if status_code == 429:  # Too Many Requests
                self._handle_rate_limit_error(domain)
            elif status_code >= 500:  # Server error
                self._handle_server_error(domain)
            elif 200 <= status_code < 300:  # Success
                self._handle_success(domain, response_time)

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        return urlparse(url).netloc

    def _handle_rate_limit_error(self, domain: str) -> None:
        """Handle rate limiting by increasing delay."""
        current_delay = self.domain_delays[domain]
        new_delay = min(current_delay * 2, 10.0)  # Cap at 10 seconds
        self.domain_delays[domain] = new_delay
        self.error_counts[domain] += 1

        print(f"Rate limited on {domain}, increasing delay to {new_delay:.2f}s")

    def _handle_server_error(self, domain: str) -> None:
        """Handle server errors by slightly increasing delay."""
        current_delay = self.domain_delays[domain]
        new_delay = min(current_delay * 1.5, 5.0)  # Cap at 5 seconds
        self.domain_delays[domain] = new_delay
        self.error_counts[domain] += 1

    def _handle_success(self, domain: str, response_time: float) -> None:
        """Handle successful responses by potentially reducing delay."""
        current_delay = self.domain_delays[domain]

        # Calculate recent success rate
        recent_requests = self.request_counts[domain]
        if len(recent_requests) >= 10:  # Have enough data
            success_rate = self._calculate_success_rate(domain)

            if success_rate > 0.95 and response_time < 2.0:  # High success, fast response
                new_delay = max(current_delay * 0.9, 0.1)  # Decrease delay, minimum 0.1s
                self.domain_delays[domain] = new_delay

        # Reset error count on success
        if domain in self.error_counts:
            self.error_counts[domain] = max(0, self.error_counts[domain] - 1)

    def _calculate_success_rate(self, domain: str) -> float:
        """Calculate recent success rate for domain."""
        recent_requests = len(self.request_counts[domain])
        recent_errors = min(self.error_counts[domain], recent_requests)
        return (recent_requests - recent_errors) / recent_requests if recent_requests > 0 else 0.0

    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """Get rate limiting statistics."""
        stats = {}
        for domain in self.domain_delays:
            stats[domain] = {
                'current_delay': self.domain_delays[domain],
                'error_count': self.error_counts[domain],
                'success_rate': self._calculate_success_rate(domain),
                'requests_count': len(self.request_counts[domain])
            }
        return stats

# Integration with scraper
class RateLimitedScraper(WebScraper):
    """Scraper with adaptive rate limiting."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate_limiter = AdaptiveRateLimiter()

    def scrape_url(self, url: str) -> ScrapingResult:
        """Scrape URL with adaptive rate limiting."""
        self.rate_limiter.wait_if_needed(url)

        start_time = time.time()
        result = super().scrape_url(url)
        response_time = time.time() - start_time

        # Record response for rate limiter
        status_code = result.data.status_code if result.data else 0
        self.rate_limiter.record_response(url, status_code, response_time)

        return result
```

### 5. Custom AI Analyzer

Create an AI-powered content analyzer using OpenAI API:

```python
import openai
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from src.models import ContentAnalysis

@dataclass
class OpenAIConfig:
    api_key: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.1
    max_tokens: int = 1000

class OpenAIContentAnalyzer:
    """AI-powered content analyzer using OpenAI API."""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        openai.api_key = config.api_key

        self.analysis_prompt = """
        Analyze the following web content and provide a JSON response with:
        1. category: Main topic category (technology, business, health, sports, entertainment, politics, science, other)
        2. confidence: Confidence score (0.0-1.0) for the category
        3. quality_score: Content quality score (0-100) based on writing quality, informativeness, and clarity
        4. key_topics: List of 3-5 main topics/keywords
        5. sentiment: Overall sentiment (positive, negative, neutral)
        6. readability_score: Estimated readability score (0-100, higher = more readable)
        7. summary: Brief 1-2 sentence summary

        Content to analyze:
        {content}

        Respond only with valid JSON:
        """

    def analyze_content(self, content: str) -> ContentAnalysis:
        """Analyze content using OpenAI API."""
        if not content.strip():
            return self._default_analysis()

        try:
            # Truncate content if too long
            max_content_length = 3000
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."

            # Make API request
            response = openai.ChatCompletion.create(
                model=self.config.model,
                messages=[
                    {"role": "user", "content": self.analysis_prompt.format(content=content)}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )

            # Parse response
            response_text = response.choices[0].message.content
            analysis_data = json.loads(response_text)

            return ContentAnalysis(
                category=analysis_data.get('category', 'other'),
                confidence=analysis_data.get('confidence', 0.0),
                quality_score=analysis_data.get('quality_score', 0.0),
                key_topics=analysis_data.get('key_topics', []),
                sentiment=analysis_data.get('sentiment', 'neutral'),
                word_count=len(content.split()),
                readability_score=analysis_data.get('readability_score', 0.0),
                summary=analysis_data.get('summary', '')
            )

        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._default_analysis()

    def _default_analysis(self) -> ContentAnalysis:
        """Return default analysis for errors or empty content."""
        return ContentAnalysis(
            category='other',
            confidence=0.0,
            quality_score=0.0,
            key_topics=[],
            sentiment='neutral',
            word_count=0,
            readability_score=0.0,
            summary=''
        )

    def batch_analyze(self, contents: List[str]) -> List[ContentAnalysis]:
        """Analyze multiple contents in batch for efficiency."""
        results = []

        # Process in smaller batches to avoid API limits
        batch_size = 5
        for i in range(0, len(contents), batch_size):
            batch = contents[i:i + batch_size]

            for content in batch:
                analysis = self.analyze_content(content)
                results.append(analysis)

                # Add small delay to respect rate limits
                time.sleep(0.1)

        return results

# Integration with AI Enhanced Scraper
class OpenAIEnhancedScraper(AIEnhancedWebScraper):
    """Scraper enhanced with OpenAI analysis."""

    def __init__(self, openai_config: OpenAIConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai_analyzer = OpenAIContentAnalyzer(openai_config)

    def scrape_with_ai_analysis(self, url: str) -> ScrapingResult:
        """Scrape URL with OpenAI-powered analysis."""
        # First perform standard scraping
        result = super().scrape_url(url)

        if result.success and result.data and result.data.content:
            # Perform AI analysis
            ai_analysis = self.ai_analyzer.analyze_content(result.data.content)

            # Update result with AI insights
            result.data.category = ai_analysis.category
            result.data.quality_score = ai_analysis.quality_score

            # Add AI analysis to metadata
            if not result.data.metadata:
                result.data.metadata = {}

            result.data.metadata['ai_analysis'] = {
                'category': ai_analysis.category,
                'confidence': ai_analysis.confidence,
                'quality_score': ai_analysis.quality_score,
                'key_topics': ai_analysis.key_topics,
                'sentiment': ai_analysis.sentiment,
                'readability_score': ai_analysis.readability_score,
                'summary': ai_analysis.summary
            }

        return result

# Usage
openai_config = OpenAIConfig(api_key="your-openai-api-key")
ai_scraper = OpenAIEnhancedScraper(openai_config)

result = ai_scraper.scrape_with_ai_analysis("https://example.com")
if result.success:
    ai_data = result.data.metadata['ai_analysis']
    print(f"Category: {ai_data['category']}")
    print(f"Quality: {ai_data['quality_score']}")
    print(f"Summary: {ai_data['summary']}")
```

## Plugin Types

### Content Processing Plugins

- **HTML Parsers**: Custom parsing for specific website structures
- **Text Cleaners**: Advanced text cleaning and normalization
- **Content Extractors**: Specialized extraction for articles, products, etc.
- **Format Converters**: Convert between different content formats

### Analysis Plugins

- **Categorizers**: ML models, rule-based systems, AI-powered categorization
- **Quality Assessors**: Content quality scoring algorithms
- **Sentiment Analyzers**: Emotion and sentiment detection
- **Topic Extractors**: Keyword and topic identification

### Data Processing Plugins

- **Validators**: Custom validation rules for different data types
- **Transformers**: Data transformation and normalization
- **Enrichers**: Add additional information to scraped data
- **Filters**: Filter data based on custom criteria

### Export Plugins

- **Database Exporters**: Various database systems (MySQL, PostgreSQL, MongoDB)
- **API Exporters**: REST APIs, GraphQL endpoints
- **Cloud Storage**: AWS S3, Google Cloud Storage, Azure Blob
- **Message Queues**: RabbitMQ, Apache Kafka, Redis

### Integration Plugins

- **Authentication**: OAuth, API keys, session management
- **Monitoring**: Custom metrics and alerting
- **Caching**: Redis, Memcached, custom cache backends
- **Proxy Management**: Proxy rotation and management

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone the framework
git clone https://github.com/timfewi/webscraper-ai-python.git
cd webscraper-ai-python

# Create plugin development workspace
mkdir plugins/my-plugin
cd plugins/my-plugin

# Create plugin structure
mkdir src tests docs
touch src/__init__.py
touch src/my_plugin.py
touch tests/test_my_plugin.py
touch setup.py
touch README.md
```

### 2. Plugin Template

```python
# src/my_plugin.py
from typing import Any, Dict
from src.interfaces import IContentProcessor

class MyCustomPlugin(IContentProcessor):
    """Custom plugin template."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize plugin with configuration."""
        self.config = config or {}
        self._initialize()

    def _initialize(self) -> None:
        """Initialize plugin resources."""
        # Load models, connect to services, etc.
        pass

    def process_content(self, html: str) -> str:
        """Main plugin functionality."""
        # Your implementation here
        return html

    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        # Close connections, save state, etc.
        pass

# Plugin metadata
PLUGIN_INFO = {
    'name': 'My Custom Plugin',
    'version': '1.0.0',
    'description': 'Description of plugin functionality',
    'author': 'Your Name',
    'license': 'MIT',
    'dependencies': ['beautifulsoup4', 'requests'],
    'interfaces': ['IContentProcessor']
}

# Plugin factory function
def create_plugin(config: Dict[str, Any] = None) -> MyCustomPlugin:
    """Factory function to create plugin instance."""
    return MyCustomPlugin(config)
```

### 3. Plugin Configuration

```python
# config.py
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class PluginConfig:
    """Configuration for custom plugin."""

    # Plugin-specific settings
    enabled: bool = True
    api_key: Optional[str] = None
    timeout: int = 30
    custom_settings: Dict[str, Any] = None

    def __post_init__(self):
        if self.custom_settings is None:
            self.custom_settings = {}

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'PluginConfig':
        """Create config from dictionary."""
        return cls(**config_dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'enabled': self.enabled,
            'api_key': self.api_key,
            'timeout': self.timeout,
            'custom_settings': self.custom_settings
        }
```

### 4. Plugin Testing

```python
# tests/test_my_plugin.py
import pytest
from unittest.mock import Mock, patch
from src.my_plugin import MyCustomPlugin, create_plugin

class TestMyCustomPlugin:
    """Test suite for custom plugin."""

    def setup_method(self):
        """Setup test fixtures."""
        self.config = {'enabled': True, 'timeout': 30}
        self.plugin = create_plugin(self.config)

    def test_plugin_initialization(self):
        """Test plugin initializes correctly."""
        assert self.plugin.config['enabled'] is True
        assert self.plugin.config['timeout'] == 30

    def test_process_content_success(self):
        """Test successful content processing."""
        html = "<html><body><p>Test content</p></body></html>"
        result = self.plugin.process_content(html)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_process_content_empty_input(self):
        """Test handling of empty input."""
        result = self.plugin.process_content("")
        assert result == ""

    @patch('requests.get')
    def test_external_api_integration(self, mock_get):
        """Test integration with external APIs."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {'result': 'success'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test API integration
        result = self.plugin.call_external_api("test_data")
        assert result == {'result': 'success'}

    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            self.plugin.process_content(None)

    def teardown_method(self):
        """Cleanup after tests."""
        self.plugin.cleanup()

# Performance tests
class TestPluginPerformance:
    """Performance tests for plugin."""

    def test_processing_speed(self):
        """Test processing speed with large content."""
        import time

        plugin = create_plugin()
        large_html = "<html><body>" + "<p>Test content</p>" * 1000 + "</body></html>"

        start_time = time.time()
        result = plugin.process_content(large_html)
        processing_time = time.time() - start_time

        assert processing_time < 1.0  # Should process in under 1 second
        assert len(result) > 0

    def test_memory_usage(self):
        """Test memory efficiency."""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        plugin = create_plugin()

        # Process multiple large documents
        for _ in range(100):
            html = "<html><body>" + "<p>Test content</p>" * 100 + "</body></html>"
            plugin.process_content(html)

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024
```

### 5. Plugin Packaging

```python
# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="webscraper-my-plugin",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Custom plugin for AI-Powered Web Scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/webscraper-my-plugin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "webscraper-ai-python>=2.0.0",
        "beautifulsoup4>=4.9.0",
        "requests>=2.25.0",
        # Add your dependencies here
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "webscraper.plugins": [
            "my_plugin = my_plugin.src.my_plugin:create_plugin",
        ],
    },
)
```

## Best Practices

### Code Quality

1. **Follow PEP 8**: Use consistent code formatting
2. **Type Hints**: Add type hints for better IDE support
3. **Documentation**: Write comprehensive docstrings
4. **Error Handling**: Implement robust error handling
5. **Logging**: Add appropriate logging for debugging

### Performance

1. **Efficient Algorithms**: Use appropriate data structures and algorithms
2. **Memory Management**: Clean up resources properly
3. **Caching**: Cache expensive operations when possible
4. **Async Support**: Consider async implementation for I/O operations
5. **Profiling**: Profile your plugin for bottlenecks

### Compatibility

1. **Interface Compliance**: Strictly follow interface contracts
2. **Version Compatibility**: Test with different framework versions
3. **Dependency Management**: Pin dependency versions appropriately
4. **Graceful Degradation**: Handle missing dependencies gracefully

### Security

1. **Input Validation**: Validate all inputs thoroughly
2. **Sanitization**: Sanitize data to prevent injection attacks
3. **Authentication**: Secure API keys and credentials
4. **Rate Limiting**: Implement appropriate rate limiting

### Testing

1. **Unit Tests**: Test individual components thoroughly
2. **Integration Tests**: Test plugin integration with framework
3. **Performance Tests**: Test with realistic data volumes
4. **Error Cases**: Test error handling and edge cases

## Testing Plugins

### Unit Testing Framework

```python
# conftest.py (pytest configuration)
import pytest
from src.my_plugin import create_plugin

@pytest.fixture
def plugin():
    """Create plugin instance for testing."""
    return create_plugin({'enabled': True})

@pytest.fixture
def sample_html():
    """Sample HTML for testing."""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <article>
                <h1>Test Article</h1>
                <p>This is test content for plugin testing.</p>
                <p>Additional paragraph with more content.</p>
            </article>
        </body>
    </html>
    """

@pytest.fixture
def large_html():
    """Large HTML for performance testing."""
    content = "<p>Test paragraph content.</p>" * 1000
    return f"<html><body><article>{content}</article></body></html>"
```

### Integration Testing

```python
# tests/test_integration.py
import pytest
from src import WebScraper, ScrapingConfig
from src.my_plugin import create_plugin

class TestPluginIntegration:
    """Test plugin integration with the main framework."""

    def test_plugin_with_webscraper(self):
        """Test plugin works with WebScraper."""
        plugin = create_plugin()
        config = ScrapingConfig()
        scraper = WebScraper(
            config=config,
            content_processor=plugin
        )

        # Mock URL to avoid actual network requests
        with patch('requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.text = "<html><body><p>Test content</p></body></html>"
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            result = scraper.scrape_url("https://example.com")

            assert result.success
            assert result.data is not None
            assert len(result.data.content) > 0

    def test_plugin_error_handling_in_scraper(self):
        """Test plugin error handling within scraper context."""
        # Create plugin that raises exception
        faulty_plugin = Mock()
        faulty_plugin.process_content.side_effect = Exception("Plugin error")

        scraper = WebScraper(content_processor=faulty_plugin)

        with patch('requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.text = "<html><body><p>Test</p></body></html>"
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            result = scraper.scrape_url("https://example.com")

            # Should handle plugin error gracefully
            assert not result.success
            assert "Plugin error" in result.error
```

## Publishing Plugins

### Documentation Requirements

Create comprehensive documentation:

```markdown
# My Custom Plugin

## Overview
Brief description of what the plugin does.

## Installation
```bash
pip install webscraper-my-plugin
```

## Usage
```python
from webscraper_my_plugin import create_plugin
from src import WebScraper

plugin = create_plugin({'enabled': True})
scraper = WebScraper(content_processor=plugin)
```

## Configuration
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | True | Enable/disable plugin |
| timeout | int | 30 | Request timeout in seconds |

## API Reference
Detailed API documentation...

## Examples
Complete usage examples...

## License
MIT License
```

### Distribution

1. **PyPI Publishing**:
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

2. **GitHub Releases**: Create tagged releases with changelogs

3. **Documentation**: Host documentation on GitHub Pages or Read the Docs

### Community Guidelines

1. **Code of Conduct**: Follow project code of conduct
2. **Contributing**: Provide clear contributing guidelines
3. **Issue Templates**: Use issue and PR templates
4. **Versioning**: Follow semantic versioning (SemVer)
5. **Changelog**: Maintain a detailed changelog

---

This plugin development guide provides everything you need to create, test, and publish custom extensions for the AI-Powered Web Scraper framework. The modular architecture makes it easy to add new functionality while maintaining compatibility and performance.
