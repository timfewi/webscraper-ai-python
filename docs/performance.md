# Performance Tuning

This guide provides optimization techniques and best practices for maximizing the performance of the AI-Powered Web Scraper framework.

## Table of Contents

- [Overview](#overview)
- [Performance Metrics](#performance-metrics)
- [Optimization Strategies](#optimization-strategies)
- [Configuration Tuning](#configuration-tuning)
- [Memory Management](#memory-management)
- [Concurrency Optimization](#concurrency-optimization)
- [Caching Strategies](#caching-strategies)
- [Monitoring and Profiling](#monitoring-and-profiling)
- [Best Practices](#best-practices)

## Overview

Performance optimization in web scraping involves balancing several factors:

- **Throughput**: Number of pages scraped per unit time
- **Resource Efficiency**: CPU, memory, and network usage
- **Quality**: Accuracy and completeness of extracted data
- **Reliability**: Error rate and system stability
- **Compliance**: Respecting rate limits and server resources

## Performance Metrics

### Key Performance Indicators (KPIs)

#### Throughput Metrics

- **Pages per Second (PPS)**: Total pages scraped / time
- **Successful Scrapes per Minute**: Successful operations / time
- **Data Volume per Hour**: Amount of data extracted / time

#### Efficiency Metrics

- **Memory Usage per Page**: RAM consumption / page
- **CPU Utilization**: Processor usage during scraping
- **Network Bandwidth**: Data transferred / time
- **Success Rate**: Successful scrapes / total attempts

#### Quality Metrics

- **Content Completeness**: Percentage of expected data extracted
- **Categorization Accuracy**: Correct categories / total categorizations
- **Data Quality Score**: Average quality score of extracted content

### Measurement Tools

```python
import time
import psutil
import memory_profiler
from typing import Dict, Any

class PerformanceMonitor:
    """Monitor scraping performance metrics."""

    def __init__(self):
        self.start_time = None
        self.metrics = {}

    def start_monitoring(self):
        """Start performance monitoring."""
        self.start_time = time.time()
        self.metrics = {
            'start_memory': psutil.virtual_memory().used,
            'start_cpu': psutil.cpu_percent(),
            'pages_scraped': 0,
            'successful_scrapes': 0,
            'errors': 0
        }

    def record_scrape(self, success: bool, data_size: int = 0):
        """Record a scraping operation."""
        self.metrics['pages_scraped'] += 1
        if success:
            self.metrics['successful_scrapes'] += 1
            self.metrics.setdefault('total_data_size', 0)
            self.metrics['total_data_size'] += data_size
        else:
            self.metrics['errors'] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        elapsed_time = time.time() - self.start_time
        current_memory = psutil.virtual_memory().used

        return {
            'elapsed_time': elapsed_time,
            'pages_per_second': self.metrics['pages_scraped'] / elapsed_time,
            'success_rate': self.metrics['successful_scrapes'] / max(1, self.metrics['pages_scraped']),
            'memory_usage_mb': (current_memory - self.metrics['start_memory']) / 1024 / 1024,
            'total_pages': self.metrics['pages_scraped'],
            'total_errors': self.metrics['errors']
        }

# Usage example
monitor = PerformanceMonitor()
monitor.start_monitoring()

# ... scraping operations ...
monitor.record_scrape(success=True, data_size=1024)

print(monitor.get_metrics())
```

## Optimization Strategies

### 1. Request Optimization

#### Connection Pooling

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OptimizedScraper:
    def __init__(self):
        self.session = requests.Session()

        # Configure connection pooling
        adapter = HTTPAdapter(
            pool_connections=20,  # Number of connection pools
            pool_maxsize=20,      # Maximum connections per pool
            max_retries=Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=[500, 502, 503, 504]
            )
        )

        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        # Keep connections alive
        self.session.headers.update({'Connection': 'keep-alive'})
```

#### Request Compression

```python
class CompressedScraper:
    def __init__(self):
        self.session = requests.Session()

        # Enable compression
        self.session.headers.update({
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })

    def scrape_url(self, url: str) -> ScrapingResult:
        try:
            response = self.session.get(url, stream=True)

            # Check content size before loading
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
                return ScrapingResult(
                    success=False,
                    error="Content too large"
                )

            # Load content with size limit
            content = ""
            size = 0
            for chunk in response.iter_content(chunk_size=8192, decode_unicode=True):
                content += chunk
                size += len(chunk)
                if size > 10 * 1024 * 1024:  # 10MB limit
                    break

            return self.process_content(content, url)

        except Exception as e:
            return ScrapingResult(success=False, error=str(e))
```

### 2. Content Processing Optimization

#### Streaming Processing

```python
from io import StringIO
import xml.etree.ElementTree as ET

class StreamingProcessor:
    """Process large HTML documents efficiently."""

    def process_large_html(self, html: str) -> str:
        """Process HTML in chunks to reduce memory usage."""
        if len(html) < 1024 * 1024:  # 1MB threshold
            return self.process_small_html(html)

        # Process in chunks for large documents
        return self.process_html_chunks(html)

    def process_html_chunks(self, html: str) -> str:
        """Process HTML in manageable chunks."""
        chunk_size = 64 * 1024  # 64KB chunks
        text_parts = []

        soup = BeautifulSoup(html, 'lxml')

        # Extract text from major content containers
        for container in soup.find_all(['article', 'main', 'div'],
                                      class_=lambda x: x and 'content' in x.lower()):
            text = container.get_text(separator=' ', strip=True)
            if len(text) > 100:  # Filter short text
                text_parts.append(text)

        # If no content containers found, process body
        if not text_parts:
            body = soup.find('body')
            if body:
                # Remove noise elements
                for element in body(['script', 'style', 'nav', 'header', 'footer']):
                    element.decompose()

                text_parts.append(body.get_text(separator=' ', strip=True))

        return ' '.join(text_parts)
```

#### Selective Parsing

```python
class SelectiveParser:
    """Parse only relevant parts of HTML documents."""

    def __init__(self):
        self.content_selectors = [
            'article',
            'main',
            '[role="main"]',
            '.content',
            '#content',
            '.post-content',
            '.entry-content'
        ]

    def extract_content(self, html: str) -> str:
        """Extract content using selective parsing."""
        soup = BeautifulSoup(html, 'lxml')

        # Try content selectors in order of priority
        for selector in self.content_selectors:
            elements = soup.select(selector)
            if elements:
                # Use the largest content element
                largest = max(elements, key=lambda e: len(e.get_text()))
                return self.clean_text(largest.get_text())

        # Fallback to body content
        body = soup.find('body')
        if body:
            return self.clean_text(body.get_text())

        return ""

    def clean_text(self, text: str) -> str:
        """Clean extracted text efficiently."""
        # Use regex for fast cleaning
        import re

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove common noise patterns
        noise_patterns = [
            r'\b(click here|read more|continue reading)\b',
            r'\b(advertisement|sponsored)\b',
            r'\b(share|tweet|like|follow)\b'
        ]

        for pattern in noise_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        return text.strip()
```

### 3. AI Processing Optimization

#### Batch Processing

```python
class BatchCategorizer:
    """Process multiple documents in batches for efficiency."""

    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.pending_documents = []

    def add_document(self, content: str, callback=None):
        """Add document to processing queue."""
        self.pending_documents.append((content, callback))

        if len(self.pending_documents) >= self.batch_size:
            self.process_batch()

    def process_batch(self):
        """Process accumulated documents in batch."""
        if not self.pending_documents:
            return

        contents = [doc[0] for doc in self.pending_documents]
        callbacks = [doc[1] for doc in self.pending_documents]

        # Batch categorization (more efficient than individual calls)
        categories = self.categorize_batch(contents)

        # Execute callbacks with results
        for category, callback in zip(categories, callbacks):
            if callback:
                callback(category)

        self.pending_documents.clear()

    def categorize_batch(self, contents: List[str]) -> List[str]:
        """Categorize multiple documents efficiently."""
        # Use vectorized operations for ML models
        from sklearn.feature_extraction.text import TfidfVectorizer

        # Vectorize all documents at once
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        features = vectorizer.fit_transform(contents)

        # Batch prediction
        predictions = self.model.predict(features)

        return [self.decode_category(pred) for pred in predictions]
```

#### Model Caching

```python
from functools import lru_cache
import hashlib
import pickle
import os

class CachedCategorizer:
    """Categorizer with intelligent caching."""

    def __init__(self, cache_size: int = 1000):
        self.cache_size = cache_size
        self.disk_cache_dir = "cache/categorizer"
        os.makedirs(self.disk_cache_dir, exist_ok=True)

    @lru_cache(maxsize=1000)
    def categorize_cached(self, content_hash: str, content: str) -> str:
        """Categorize with in-memory caching."""
        # Check disk cache first
        cache_file = os.path.join(self.disk_cache_dir, f"{content_hash}.pkl")
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        # Perform categorization
        category = self.categorize_impl(content)

        # Save to disk cache
        with open(cache_file, 'wb') as f:
            pickle.dump(category, f)

        return category

    def categorize(self, content: str) -> str:
        """Main categorization method with caching."""
        # Create content hash for caching
        content_hash = hashlib.md5(content[:1000].encode()).hexdigest()
        return self.categorize_cached(content_hash, content)

    def categorize_impl(self, content: str) -> str:
        """Actual categorization implementation."""
        # Your ML model inference here
        pass
```

## Configuration Tuning

### Optimal Configuration Values

```python
@dataclass
class PerformanceConfig:
    """Optimized configuration for different scenarios."""

    # High-throughput configuration
    @classmethod
    def high_throughput(cls) -> 'PerformanceConfig':
        return cls(
            delay_min=0.1,
            delay_max=0.5,
            timeout=15,
            max_retries=2,
            max_concurrent_requests=20,
            content_size_limit=1024 * 1024,  # 1MB
            enable_compression=True,
            connection_pool_size=25
        )

    # Memory-efficient configuration
    @classmethod
    def memory_efficient(cls) -> 'PerformanceConfig':
        return cls(
            delay_min=1.0,
            delay_max=2.0,
            timeout=30,
            max_retries=3,
            max_concurrent_requests=5,
            content_size_limit=512 * 1024,  # 512KB
            enable_streaming=True,
            chunk_size=8192
        )

    # Quality-focused configuration
    @classmethod
    def high_quality(cls) -> 'PerformanceConfig':
        return cls(
            delay_min=2.0,
            delay_max=5.0,
            timeout=60,
            max_retries=5,
            max_concurrent_requests=3,
            enable_ai_analysis=True,
            quality_threshold=80.0,
            enable_content_validation=True
        )
```

### Dynamic Configuration

```python
class AdaptiveConfiguration:
    """Dynamically adjust configuration based on performance."""

    def __init__(self):
        self.config = ScrapingConfig()
        self.performance_history = []
        self.adjustment_threshold = 10  # Adjust after 10 samples

    def update_config(self, performance_metrics: Dict[str, float]):
        """Update configuration based on performance."""
        self.performance_history.append(performance_metrics)

        if len(self.performance_history) >= self.adjustment_threshold:
            self.adjust_config()
            self.performance_history = []

    def adjust_config(self):
        """Adjust configuration based on performance history."""
        avg_success_rate = sum(m['success_rate'] for m in self.performance_history) / len(self.performance_history)
        avg_response_time = sum(m.get('response_time', 1.0) for m in self.performance_history) / len(self.performance_history)

        # Adjust delays based on success rate
        if avg_success_rate < 0.8:  # Low success rate
            self.config.delay_min *= 1.5
            self.config.delay_max *= 1.5
            self.config.timeout += 10
        elif avg_success_rate > 0.95:  # High success rate
            self.config.delay_min *= 0.8
            self.config.delay_max *= 0.8

        # Adjust timeouts based on response time
        if avg_response_time > 30:
            self.config.timeout = max(60, avg_response_time * 2)
        elif avg_response_time < 5:
            self.config.timeout = max(15, self.config.timeout * 0.8)
```

## Memory Management

### Memory Profiling

```python
import tracemalloc
import gc
from typing import Generator

class MemoryProfiler:
    """Profile memory usage during scraping."""

    def __init__(self):
        self.snapshots = []

    def start_profiling(self):
        """Start memory profiling."""
        tracemalloc.start()
        self.snapshots = [tracemalloc.take_snapshot()]

    def checkpoint(self, label: str):
        """Create a memory checkpoint."""
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append((label, snapshot))

        # Compare with previous snapshot
        if len(self.snapshots) > 1:
            prev_snapshot = self.snapshots[-2]
            if isinstance(prev_snapshot, tuple):
                prev_snapshot = prev_snapshot[1]

            top_stats = snapshot.compare_to(prev_snapshot, 'lineno')

            print(f"Memory changes since last checkpoint ({label}):")
            for stat in top_stats[:5]:
                print(f"  {stat}")

    def get_current_usage(self) -> float:
        """Get current memory usage in MB."""
        snapshot = tracemalloc.take_snapshot()
        return sum(stat.size for stat in snapshot.statistics('filename')) / 1024 / 1024

# Memory-efficient scraping
class MemoryEfficientScraper:
    def __init__(self):
        self.profiler = MemoryProfiler()

    def scrape_with_memory_management(self, urls: List[str]) -> Generator[ScrapingResult, None, None]:
        """Scrape URLs with memory management."""
        self.profiler.start_profiling()

        for i, url in enumerate(urls):
            # Periodic garbage collection
            if i % 100 == 0:
                gc.collect()
                self.profiler.checkpoint(f"URL {i}")

            # Check memory usage
            memory_usage = self.profiler.get_current_usage()
            if memory_usage > 500:  # 500MB threshold
                print(f"High memory usage: {memory_usage:.1f}MB, forcing GC")
                gc.collect()

            result = self.scrape_url(url)
            yield result

            # Clear large objects immediately
            del result
```

### Memory Optimization Techniques

```python
class OptimizedDataProcessor:
    """Process data with minimal memory footprint."""

    def __init__(self):
        self.chunk_size = 1024 * 1024  # 1MB chunks

    def process_large_dataset(self, data_source) -> Generator[ScrapedData, None, None]:
        """Process large datasets in chunks."""
        buffer = []

        for item in data_source:
            buffer.append(item)

            if len(buffer) >= 100:  # Process in batches of 100
                yield from self.process_batch(buffer)
                buffer.clear()  # Explicit clear

        # Process remaining items
        if buffer:
            yield from self.process_batch(buffer)

    def process_batch(self, items: List[Any]) -> Generator[ScrapedData, None, None]:
        """Process a batch of items efficiently."""
        for item in items:
            processed = self.process_item(item)
            if processed:
                yield processed
                # Help garbage collector
                del processed
```

## Concurrency Optimization

### Thread Pool Optimization

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from queue import Queue

class OptimizedConcurrentScraper:
    """Optimized concurrent scraping with thread pooling."""

    def __init__(self, max_workers: int = None):
        # Calculate optimal worker count
        if max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) + 4)

        self.max_workers = max_workers
        self.rate_limiter = Queue(maxsize=max_workers * 2)
        self.session_pool = self.create_session_pool()

    def create_session_pool(self) -> Queue:
        """Create a pool of HTTP sessions."""
        pool = Queue()
        for _ in range(self.max_workers):
            session = requests.Session()
            # Configure session for performance
            adapter = HTTPAdapter(
                pool_connections=1,
                pool_maxsize=1,
                max_retries=3
            )
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            pool.put(session)
        return pool

    def scrape_urls_concurrent(self, urls: List[str]) -> List[ScrapingResult]:
        """Scrape URLs with optimized concurrency."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_url = {
                executor.submit(self.scrape_with_session, url): url
                for url in urls
            }

            # Collect results as they complete
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(ScrapingResult(
                        success=False,
                        error=f"Future error for {url}: {str(e)}"
                    ))

        return results

    def scrape_with_session(self, url: str) -> ScrapingResult:
        """Scrape URL using pooled session."""
        session = self.session_pool.get()
        try:
            # Rate limiting
            time.sleep(0.1)  # Minimum delay

            response = session.get(url, timeout=30)
            result = self.process_response(response, url)

        except Exception as e:
            result = ScrapingResult(success=False, error=str(e))
        finally:
            self.session_pool.put(session)

        return result
```

### Async Implementation

```python
import asyncio
import aiohttp
from typing import AsyncGenerator

class AsyncScraper:
    """Asynchronous scraper for high-performance scraping."""

    def __init__(self, max_concurrent: int = 20):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def scrape_urls_async(self, urls: List[str]) -> List[ScrapingResult]:
        """Scrape URLs asynchronously."""
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=20,
            keepalive_timeout=30
        )

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            tasks = [self.scrape_url_async(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Convert exceptions to error results
            processed_results = []
            for result in results:
                if isinstance(result, Exception):
                    processed_results.append(
                        ScrapingResult(success=False, error=str(result))
                    )
                else:
                    processed_results.append(result)

            return processed_results

    async def scrape_url_async(self, session: aiohttp.ClientSession, url: str) -> ScrapingResult:
        """Scrape single URL asynchronously."""
        async with self.semaphore:  # Rate limiting
            try:
                async with session.get(url) as response:
                    content = await response.text()
                    return await self.process_content_async(content, url)

            except Exception as e:
                return ScrapingResult(success=False, error=str(e))

    async def process_content_async(self, content: str, url: str) -> ScrapingResult:
        """Process content asynchronously."""
        # Run CPU-intensive processing in thread pool
        loop = asyncio.get_event_loop()

        # Process content in executor to avoid blocking
        processed_content = await loop.run_in_executor(
            None, self.process_content_sync, content
        )

        return ScrapingResult(
            success=True,
            data=ScrapedData(
                url=url,
                content=processed_content,
                timestamp=datetime.now()
            )
        )
```

## Caching Strategies

### Multi-Level Caching

```python
import redis
from functools import wraps
import pickle

class MultiLevelCache:
    """Implement multi-level caching for web scraping."""

    def __init__(self):
        # Level 1: In-memory cache (fastest)
        self.memory_cache = {}
        self.memory_cache_max_size = 1000

        # Level 2: Redis cache (medium speed)
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
            self.redis_available = True
        except:
            self.redis_available = False

        # Level 3: Disk cache (slowest but persistent)
        self.disk_cache_dir = "cache/pages"
        os.makedirs(self.disk_cache_dir, exist_ok=True)

    def get(self, key: str) -> Any:
        """Get value from cache (checks all levels)."""
        # Level 1: Memory cache
        if key in self.memory_cache:
            return self.memory_cache[key]

        # Level 2: Redis cache
        if self.redis_available:
            try:
                value = self.redis_client.get(key)
                if value:
                    # Deserialize and promote to memory cache
                    deserialized = pickle.loads(value)
                    self.set_memory_cache(key, deserialized)
                    return deserialized
            except:
                pass

        # Level 3: Disk cache
        disk_path = os.path.join(self.disk_cache_dir, f"{key}.pkl")
        if os.path.exists(disk_path):
            try:
                with open(disk_path, 'rb') as f:
                    value = pickle.load(f)
                    # Promote to higher levels
                    self.set_memory_cache(key, value)
                    if self.redis_available:
                        self.redis_client.setex(key, 3600, pickle.dumps(value))
                    return value
            except:
                pass

        return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in all cache levels."""
        # Memory cache
        self.set_memory_cache(key, value)

        # Redis cache
        if self.redis_available:
            try:
                self.redis_client.setex(key, ttl, pickle.dumps(value))
            except:
                pass

        # Disk cache
        disk_path = os.path.join(self.disk_cache_dir, f"{key}.pkl")
        try:
            with open(disk_path, 'wb') as f:
                pickle.dump(value, f)
        except:
            pass

    def set_memory_cache(self, key: str, value: Any):
        """Set value in memory cache with size limit."""
        if len(self.memory_cache) >= self.memory_cache_max_size:
            # Remove oldest entry (simple LRU)
            oldest_key = next(iter(self.memory_cache))
            del self.memory_cache[oldest_key]

        self.memory_cache[key] = value

# Cache decorator for scraping functions
def cached_scrape(cache_duration: int = 3600):
    """Decorator to cache scraping results."""
    cache = MultiLevelCache()

    def decorator(func):
        @wraps(func)
        def wrapper(url: str, *args, **kwargs):
            # Create cache key
            cache_key = f"scrape:{hashlib.md5(url.encode()).hexdigest()}"

            # Check cache first
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result

            # Perform scraping
            result = func(url, *args, **kwargs)

            # Cache successful results
            if result.success:
                cache.set(cache_key, result, cache_duration)

            return result
        return wrapper
    return decorator

# Usage
class CachedScraper:
    @cached_scrape(cache_duration=7200)  # 2 hours
    def scrape_url(self, url: str) -> ScrapingResult:
        # Your scraping logic here
        pass
```

## Monitoring and Profiling

### Real-time Performance Dashboard

```python
import matplotlib.pyplot as plt
from collections import deque
import threading
import time

class PerformanceDashboard:
    """Real-time performance monitoring dashboard."""

    def __init__(self, max_points: int = 100):
        self.max_points = max_points
        self.timestamps = deque(maxlen=max_points)
        self.throughput = deque(maxlen=max_points)
        self.memory_usage = deque(maxlen=max_points)
        self.success_rate = deque(maxlen=max_points)

        self.monitoring = False
        self.monitor_thread = None

    def start_monitoring(self, scraper):
        """Start real-time monitoring."""
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(scraper,)
        )
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()

    def _monitor_loop(self, scraper):
        """Monitoring loop."""
        while self.monitoring:
            timestamp = time.time()
            metrics = scraper.get_performance_metrics()

            self.timestamps.append(timestamp)
            self.throughput.append(metrics.get('pages_per_second', 0))
            self.memory_usage.append(metrics.get('memory_usage_mb', 0))
            self.success_rate.append(metrics.get('success_rate', 0))

            # Update dashboard every 5 seconds
            time.sleep(5)

    def plot_dashboard(self):
        """Create real-time dashboard plot."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Convert timestamps to relative time
        if self.timestamps:
            start_time = self.timestamps[0]
            times = [(t - start_time) / 60 for t in self.timestamps]  # Minutes

            # Throughput plot
            ax1.plot(times, self.throughput, 'b-', linewidth=2)
            ax1.set_title('Throughput (Pages/Second)')
            ax1.set_xlabel('Time (minutes)')
            ax1.grid(True)

            # Memory usage plot
            ax2.plot(times, self.memory_usage, 'r-', linewidth=2)
            ax2.set_title('Memory Usage (MB)')
            ax2.set_xlabel('Time (minutes)')
            ax2.grid(True)

            # Success rate plot
            ax3.plot(times, self.success_rate, 'g-', linewidth=2)
            ax3.set_title('Success Rate (%)')
            ax3.set_xlabel('Time (minutes)')
            ax3.set_ylim(0, 1)
            ax3.grid(True)

            # Statistics
            if self.throughput:
                avg_throughput = sum(self.throughput) / len(self.throughput)
                max_memory = max(self.memory_usage) if self.memory_usage else 0
                avg_success = sum(self.success_rate) / len(self.success_rate) if self.success_rate else 0

                stats_text = f"""Performance Statistics:
Average Throughput: {avg_throughput:.2f} pages/sec
Peak Memory Usage: {max_memory:.1f} MB
Average Success Rate: {avg_success:.1%}
Monitoring Duration: {times[-1]:.1f} minutes"""

                ax4.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center')
                ax4.set_title('Statistics')
                ax4.axis('off')

        plt.tight_layout()
        return fig
```

### Profiling Tools

```python
import cProfile
import pstats
from typing import Callable

class ScrapingProfiler:
    """Profile scraping operations to identify bottlenecks."""

    def __init__(self):
        self.profiler = cProfile.Profile()
        self.stats = None

    def profile_function(self, func: Callable, *args, **kwargs):
        """Profile a specific function."""
        self.profiler.enable()
        try:
            result = func(*args, **kwargs)
        finally:
            self.profiler.disable()

        return result

    def get_stats(self, sort_by: str = 'cumulative') -> pstats.Stats:
        """Get profiling statistics."""
        if self.stats is None:
            self.stats = pstats.Stats(self.profiler)

        return self.stats.sort_stats(sort_by)

    def print_stats(self, lines: int = 20):
        """Print top profiling results."""
        stats = self.get_stats()
        stats.print_stats(lines)

    def get_bottlenecks(self, threshold: float = 0.1) -> List[str]:
        """Identify performance bottlenecks."""
        stats = self.get_stats()
        bottlenecks = []

        for func_info, (cc, nc, tt, ct, callers) in stats.stats.items():
            if ct > threshold:  # Functions taking more than threshold seconds
                filename, line, func_name = func_info
                bottlenecks.append(f"{func_name} ({filename}:{line}): {ct:.3f}s")

        return sorted(bottlenecks, key=lambda x: float(x.split(': ')[1][:-1]), reverse=True)

# Usage example
profiler = ScrapingProfiler()
scraper = WebScraper()

# Profile scraping operation
result = profiler.profile_function(scraper.scrape_url, "https://example.com")

# Analyze results
profiler.print_stats()
bottlenecks = profiler.get_bottlenecks()
print("Performance bottlenecks:")
for bottleneck in bottlenecks[:5]:
    print(f"  {bottleneck}")
```

## Best Practices

### Performance Checklist

#### Before Scraping

- [ ] **Analyze target websites** for optimal scraping patterns
- [ ] **Set appropriate rate limits** to avoid overwhelming servers
- [ ] **Configure connection pooling** for better resource utilization
- [ ] **Enable compression** to reduce bandwidth usage
- [ ] **Set reasonable timeouts** based on target site performance

#### During Development

- [ ] **Profile your code** to identify bottlenecks
- [ ] **Use caching** for repeated operations
- [ ] **Implement streaming** for large content processing
- [ ] **Monitor memory usage** and implement cleanup
- [ ] **Test with realistic data volumes**

#### Production Deployment

- [ ] **Monitor performance metrics** continuously
- [ ] **Implement health checks** for system components
- [ ] **Set up alerts** for performance degradation
- [ ] **Plan for scaling** based on load requirements
- [ ] **Regular performance tuning** based on metrics

### Common Performance Pitfalls

#### 1. Excessive DOM Parsing

```python
# BAD: Parse entire document for small extraction
soup = BeautifulSoup(html, 'html.parser')
title = soup.find('title').text

# GOOD: Use targeted parsing
title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
title = title_match.group(1) if title_match else ""
```

#### 2. Memory Leaks in Loops

```python
# BAD: Accumulating objects without cleanup
results = []
for url in large_url_list:
    result = scrape_url(url)
    results.append(result)  # Memory grows continuously

# GOOD: Process in batches with cleanup
def process_urls_efficiently(urls):
    batch_size = 100
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        batch_results = process_batch(batch)

        # Process results immediately
        export_results(batch_results)

        # Clear memory
        del batch_results
        gc.collect()
```

#### 3. Inefficient String Operations

```python
# BAD: Repeated string concatenation
text = ""
for chunk in text_chunks:
    text += chunk  # O(n²) complexity

# GOOD: Use list and join
text_parts = []
for chunk in text_chunks:
    text_parts.append(chunk)
text = ''.join(text_parts)  # O(n) complexity
```

#### 4. Blocking Operations in Async Code

```python
# BAD: Blocking operation in async function
async def scrape_async(url):
    response = await fetch_url(url)
    # This blocks the event loop
    result = cpu_intensive_processing(response.text)
    return result

# GOOD: Use executor for CPU-intensive tasks
async def scrape_async(url):
    response = await fetch_url(url)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, cpu_intensive_processing, response.text
    )
    return result
```

### Performance Testing

```python
import time
import statistics
from typing import List

class PerformanceTester:
    """Test scraper performance under various conditions."""

    def __init__(self, scraper):
        self.scraper = scraper

    def benchmark_throughput(self, urls: List[str], iterations: int = 3) -> Dict[str, float]:
        """Benchmark scraping throughput."""
        times = []

        for i in range(iterations):
            start_time = time.time()

            results = self.scraper.scrape_multiple_urls(urls)
            successful = sum(1 for r in results if r.success)

            elapsed = time.time() - start_time
            times.append(elapsed)

            print(f"Iteration {i+1}: {successful}/{len(urls)} successful in {elapsed:.2f}s")

        avg_time = statistics.mean(times)
        pages_per_second = len(urls) / avg_time

        return {
            'average_time': avg_time,
            'pages_per_second': pages_per_second,
            'std_deviation': statistics.stdev(times) if len(times) > 1 else 0
        }

    def stress_test(self, url: str, concurrent_requests: List[int]) -> Dict[int, Dict[str, float]]:
        """Test performance under different concurrency levels."""
        results = {}

        for concurrency in concurrent_requests:
            print(f"Testing with {concurrency} concurrent requests...")

            # Create URL list for testing
            test_urls = [url] * concurrency

            start_time = time.time()
            scraping_results = self.scraper.scrape_multiple_urls(test_urls)
            elapsed = time.time() - start_time

            successful = sum(1 for r in scraping_results if r.success)

            results[concurrency] = {
                'elapsed_time': elapsed,
                'success_rate': successful / len(test_urls),
                'requests_per_second': len(test_urls) / elapsed
            }

        return results

# Example usage
scraper = WebScraper()
tester = PerformanceTester(scraper)

# Benchmark throughput
urls = ["https://example.com"] * 50
benchmark_results = tester.benchmark_throughput(urls)
print(f"Average throughput: {benchmark_results['pages_per_second']:.2f} pages/second")

# Stress test
stress_results = tester.stress_test("https://example.com", [1, 5, 10, 20])
for concurrency, metrics in stress_results.items():
    print(f"Concurrency {concurrency}: {metrics['requests_per_second']:.2f} req/s, "
          f"{metrics['success_rate']:.1%} success rate")
```

---

By following these performance optimization techniques and best practices, you can significantly improve the efficiency and scalability of your web scraping operations. Remember to always profile your specific use case and adjust configurations based on your requirements and target websites' characteristics.
