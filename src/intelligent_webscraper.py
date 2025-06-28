"""
Main WebScraper class - Core functionality for intelligent web scraping.

This module implements the main scraping logic with AI-powered categorization
as outlined in the Product Requirements Document.
"""

from dataclasses import dataclass
from datetime import datetime
import json
import logging
from pathlib import Path
import random
import time
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class ScrapedData:
    """Data structure for scraped content."""

    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    status_code: int = 0

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


class WebScraperConfig:
    """Configuration settings for the web scraper."""

    def __init__(
        self,
        delay_min: float = 1.0,
        delay_max: float = 3.0,
        timeout: int = 30,
        max_retries: int = 3,
        user_agent: Optional[str] = None,
    ):
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.timeout = timeout
        self.max_retries = max_retries
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )


class IntelligentWebScraper:
    """
    AI-Powered Intelligent Web Scraper.

    This class implements the core functionality for intelligently scraping
    and categorizing web content as specified in the PRD.
    """

    def __init__(self, config: Optional[WebScraperConfig] = None):
        """Initialize the web scraper with configuration."""
        self.config = config or WebScraperConfig()
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.config.user_agent})
        self.scraped_data: List[ScrapedData] = []

        logger.info("IntelligentWebScraper initialized")

    def validate_url(self, url: str) -> Tuple[bool, str]:
        """
        Validate if a URL is suitable for scraping.

        Args:
            url: The URL to validate

        Returns:
            Tuple of (is_valid, message)
        """
        if not url:
            return False, "URL is empty"

        if not url.startswith(("http://", "https://")):
            return False, "URL must start with http:// or https://"

        if len(url) < 10:
            return False, "URL appears to be too short"

        # Check for localhost or development URLs
        invalid_patterns = ["localhost", "127.0.0.1", ".local"]
        if any(pattern in url.lower() for pattern in invalid_patterns):
            return False, "Development URLs not allowed"

        return True, "URL is valid"

    def categorize_website(self, url: str, content: Optional[str] = None) -> str:
        """
        Intelligently categorize a website based on URL and content.

        This is a simplified version of AI categorization.
        In the full implementation, this would use ML models.

        Args:
            url: The website URL
            content: Optional content to analyze

        Returns:
            Category string
        """
        url_lower = url.lower()

        # E-commerce indicators
        ecommerce_keywords = [
            "shop",
            "store",
            "buy",
            "cart",
            "product",
            "amazon",
            "ebay",
        ]
        if any(keyword in url_lower for keyword in ecommerce_keywords):
            return "E-commerce"

        # News/Blog indicators
        news_keywords = ["news", "blog", "article", "post", "medium", "wordpress"]
        if any(keyword in url_lower for keyword in news_keywords):
            return "News/Blog"

        # Technical/Development
        tech_keywords = ["github", "stackoverflow", "docs", "api"]
        if any(keyword in url_lower for keyword in tech_keywords):
            return "Technical"

        # Social Media
        social_keywords = ["facebook", "twitter", "linkedin", "instagram", "social"]
        if any(keyword in url_lower for keyword in social_keywords):
            return "Social Media"

        # Reference/Educational
        ref_keywords = ["wikipedia", "edu", "reference", "wiki"]
        if any(keyword in url_lower for keyword in ref_keywords):
            return "Reference"

        # If content is available, analyze it too
        if content:
            content_lower = content.lower()
            if "price" in content_lower and (
                "buy" in content_lower or "cart" in content_lower
            ):
                return "E-commerce"
            elif (
                len(
                    [
                        word
                        for word in ["article", "blog", "post", "news"]
                        if word in content_lower
                    ]
                )
                >= 2
            ):
                return "News/Blog"

        return "General"

    def extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """
        Extract metadata from the parsed HTML.

        Args:
            soup: BeautifulSoup object
            url: Original URL

        Returns:
            Dictionary with metadata
        """
        metadata = {
            "url": url,
            "domain": url.split("/")[2] if len(url.split("/")) > 2 else "",
            "links_count": len(soup.find_all("a")),
            "images_count": len(soup.find_all("img")),
            "has_forms": len(soup.find_all("form")) > 0,
        }

        # Extract meta description
        import bs4  # Ensure bs4 is imported for type checking

        try:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            # Ensure meta_desc is a Tag before calling .get
            if isinstance(meta_desc, bs4.element.Tag):
                content_val = meta_desc.get("content")
                if content_val:
                    metadata["description"] = str(content_val)
        except (AttributeError, TypeError):
            pass

        # Extract meta keywords
        try:
            meta_keywords = soup.find("meta", attrs={"name": "keywords"})
            # Ensure meta_keywords is a Tag before calling .get
            if isinstance(meta_keywords, bs4.element.Tag):
                content_val = meta_keywords.get("content")
                if content_val:
                    metadata["keywords"] = str(content_val)
        except (AttributeError, TypeError):
            pass

        # Check for common frameworks/technologies
        page_text = str(soup).lower()
        technologies = []
        tech_indicators = {
            "react": "react",
            "vue": "vue.js",
            "angular": "angular",
            "bootstrap": "bootstrap",
            "jquery": "jquery",
        }

        for indicator, tech in tech_indicators.items():
            if indicator in page_text:
                technologies.append(tech)

        metadata["technologies"] = technologies

        return metadata

    def scrape_url(self, url: str) -> Optional[ScrapedData]:
        """
        Scrape a single URL and return structured data.

        Args:
            url: The URL to scrape

        Returns:
            ScrapedData object or None if failed
        """
        # Validate URL
        is_valid, message = self.validate_url(url)
        if not is_valid:
            logger.warning(f"Invalid URL {url}: {message}")
            return None

        # Rate limiting - respectful delay
        delay = random.uniform(self.config.delay_min, self.config.delay_max)
        time.sleep(delay)

        try:
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title_tag = soup.find("title")
            title = title_tag.get_text().strip() if title_tag else None

            # Extract main content (simplified)
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            content = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            content = " ".join(chunk for chunk in chunks if chunk)

            # Limit content length
            if len(content) > 5000:
                content = content[:5000] + "..."

            # Extract metadata
            metadata = self.extract_metadata(soup, url)

            # Categorize website
            category = self.categorize_website(url, content)

            # Create structured data
            scraped_data = ScrapedData(
                url=url,
                title=title,
                content=content,
                category=category,
                metadata=metadata,
                status_code=response.status_code,
            )

            self.scraped_data.append(scraped_data)
            logger.info(f"Successfully scraped {url} - Category: {category}")

            return scraped_data

        except requests.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None

    def scrape_multiple_urls(self, urls: List[str]) -> List[ScrapedData]:
        """
        Scrape multiple URLs with error handling and progress tracking.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of successfully scraped data
        """
        successful_scrapes = []

        logger.info(f"Starting batch scraping of {len(urls)} URLs")

        for i, url in enumerate(urls, 1):
            logger.info(f"Progress: {i}/{len(urls)} - {url}")

            scraped_data = self.scrape_url(url)
            if scraped_data:
                successful_scrapes.append(scraped_data)

            # Progress update every 5 URLs
            if i % 5 == 0:
                success_rate = len(successful_scrapes) / i * 100
                logger.info(
                    f"Completed {i}/{len(urls)} URLs - Success rate: {success_rate:.1f}%"
                )

        final_success_rate = len(successful_scrapes) / len(urls) * 100
        logger.info(
            f"Batch scraping completed: {len(successful_scrapes)}/{len(urls)} successful ({final_success_rate:.1f}%)"
        )

        return successful_scrapes

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about scraped data.

        Returns:
            Dictionary with various statistics
        """
        if not self.scraped_data:
            return {"message": "No data scraped yet"}

        # Category distribution
        categories = [data.category for data in self.scraped_data if data.category]
        category_counts = pd.Series(categories).value_counts().to_dict()
        # Convert numpy int64 to native Python int for JSON serialization
        category_counts = {k: int(v) for k, v in category_counts.items()}

        # Status code distribution
        status_codes = [data.status_code for data in self.scraped_data]
        status_counts = pd.Series(status_codes).value_counts().to_dict()
        # Convert numpy int64 to native Python int for JSON serialization
        status_counts = {k: int(v) for k, v in status_counts.items()}

        # Content length statistics
        content_lengths = [
            len(data.content) if data.content else 0 for data in self.scraped_data
        ]

        # Convert numpy types to native Python types for JSON serialization
        content_stats = {
            "avg_length": float(np.mean(content_lengths)),
            "min_length": int(np.min(content_lengths)),
            "max_length": int(np.max(content_lengths)),
        }

        stats = {
            "total_scraped": len(self.scraped_data),
            "categories": category_counts,
            "status_codes": status_counts,
            "content_stats": content_stats,
            "domains": len(
                {(data.metadata or {}).get("domain", "") for data in self.scraped_data}
            ),
        }

        return stats

    def _create_export_directory(self) -> Path:
        """
        Create organized directory structure for exports.

        Returns:
            Path to the export directory
        """
        # Create main exports directory
        base_dir = Path("exports")

        # Create date-based subdirectory (YYYY/MM/DD format)
        today = datetime.now()
        date_dir = (
            base_dir / f"{today.year}" / f"{today.month:02d}" / f"{today.day:02d}"
        )

        # Create category subdirectories
        categories = ["json", "csv", "reports", "logs"]
        for category in categories:
            category_dir = date_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Created export directory structure: {date_dir}")
        return date_dir

    def export_to_json(
        self, filename: Optional[str] = None, export_dir: Optional[Path] = None
    ) -> str:
        """
        Export scraped data to JSON file in organized directory structure.

        Args:
            filename: Optional filename, defaults to timestamp-based name
            export_dir: Optional export directory, defaults to organized structure

        Returns:
            Full path of exported file
        """
        # Create export directory if not provided
        if export_dir is None:
            export_dir = self._create_export_directory()

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}.json"

        # Ensure filename has .json extension
        if not filename.endswith(".json"):
            filename += ".json"

        # Create full file path in json subdirectory
        json_dir = export_dir / "json"
        json_dir.mkdir(parents=True, exist_ok=True)
        file_path = json_dir / filename

        # Convert to serializable format
        export_data = []
        for data in self.scraped_data:
            export_data.append(
                {
                    "url": data.url,
                    "title": data.title,
                    "content": data.content,
                    "category": data.category,
                    "metadata": data.metadata,
                    "timestamp": data.timestamp.isoformat() if data.timestamp else None,
                    "status_code": data.status_code,
                }
            )

        # Add export metadata
        export_metadata = {
            "export_info": {
                "export_timestamp": datetime.now().isoformat(),
                "total_records": len(export_data),
                "scraper_version": "1.0.0",
                "export_format": "json",
            },
            "data": export_data,
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(export_metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(export_data)} records to {file_path}")
        return str(file_path)

    def export_to_csv(
        self, filename: Optional[str] = None, export_dir: Optional[Path] = None
    ) -> str:
        """
        Export scraped data to CSV file in organized directory structure.

        Args:
            filename: Optional filename, defaults to timestamp-based name
            export_dir: Optional export directory, defaults to organized structure

        Returns:
            Full path of exported file
        """
        # Create export directory if not provided
        if export_dir is None:
            export_dir = self._create_export_directory()

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}.csv"

        # Ensure filename has .csv extension
        if not filename.endswith(".csv"):
            filename += ".csv"

        # Create full file path in csv subdirectory
        csv_dir = export_dir / "csv"
        csv_dir.mkdir(parents=True, exist_ok=True)
        file_path = csv_dir / filename

        # Convert to DataFrame
        data_list = []
        for data in self.scraped_data:
            metadata = data.metadata or {}
            row = {
                "url": data.url,
                "title": data.title,
                "category": data.category,
                "timestamp": data.timestamp.isoformat() if data.timestamp else None,
                "status_code": data.status_code,
                "domain": metadata.get("domain", ""),
                "links_count": metadata.get("links_count", 0),
                "images_count": metadata.get("images_count", 0),
                "has_forms": metadata.get("has_forms", False),
                "content_length": len(data.content) if data.content else 0,
                "technologies": ", ".join(metadata.get("technologies", [])),
                "description": metadata.get("description", ""),
                "keywords": metadata.get("keywords", ""),
            }
            data_list.append(row)

        scraped_data_df = pd.DataFrame(data_list)
        scraped_data_df.to_csv(file_path, index=False, encoding="utf-8")

        logger.info(f"Exported {len(data_list)} records to {file_path}")
        return str(file_path)

    def export_summary_report(self, export_dir: Optional[Path] = None) -> str:
        """
        Generate and export a summary report of the scraping session.

        Args:
            export_dir: Optional export directory, defaults to organized structure

        Returns:
            Full path of exported report file
        """
        # Create export directory if not provided
        if export_dir is None:
            export_dir = self._create_export_directory()

        # Create report filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scraping_report_{timestamp}.txt"

        # Create full file path in reports subdirectory
        reports_dir = export_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        file_path = reports_dir / filename

        # Generate report content
        stats = self.get_statistics()

        report_content = f"""
🕷️ Web Scraping Summary Report
{'=' * 50}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total URLs Scraped: {stats.get('total_scraped', 0)}
Unique Domains: {stats.get('domains', 0)}

📊 Category Distribution:
{'-' * 30}
"""

        # Add category statistics
        categories = stats.get("categories", {})
        for category, count in categories.items():
            percentage = (count / stats.get("total_scraped", 1)) * 100
            report_content += f"  {category}: {count} ({percentage:.1f}%)\n"

        report_content += f"""
🌐 Status Code Distribution:
{'-' * 30}
"""

        # Add status code statistics
        status_codes = stats.get("status_codes", {})
        for status, count in status_codes.items():
            percentage = (count / stats.get("total_scraped", 1)) * 100
            report_content += f"  HTTP {status}: {count} ({percentage:.1f}%)\n"

        # Add content statistics
        content_stats = stats.get("content_stats", {})
        report_content += f"""
📝 Content Statistics:
{'-' * 30}
  Average Length: {content_stats.get('avg_length', 0):.0f} characters
  Minimum Length: {content_stats.get('min_length', 0)} characters
  Maximum Length: {content_stats.get('max_length', 0)} characters

📁 Scraped URLs:
{'-' * 30}
"""

        # Add list of scraped URLs with their categories
        for i, data in enumerate(self.scraped_data, 1):
            report_content += f"  {i}. {data.url}\n"
            report_content += f"     Category: {data.category}\n"
            report_content += f"     Title: {data.title or 'N/A'}\n"
            report_content += f"     Status: {data.status_code}\n"
            report_content += f"     Content Length: {len(data.content) if data.content else 0} chars\n\n"

        report_content += f"""
{'=' * 50}
Report generated by AI-Powered Intelligent Web Scraper v1.0.0
"""

        # Write report to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        logger.info(f"Generated summary report: {file_path}")
        return str(file_path)

    def export_all(self, base_filename: Optional[str] = None) -> Dict[str, str]:
        """
        Export all data in multiple formats with organized folder structure.

        Args:
            base_filename: Optional base filename (timestamp will be added if not provided)

        Returns:
            Dictionary with paths to all exported files
        """
        # Create export directory
        export_dir = self._create_export_directory()

        # Generate base filename if not provided
        if base_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"scraped_data_{timestamp}"

        # Export in all formats
        export_paths = {}

        try:
            # Export JSON
            json_path = self.export_to_json(f"{base_filename}.json", export_dir)
            export_paths["json"] = json_path

            # Export CSV
            csv_path = self.export_to_csv(f"{base_filename}.csv", export_dir)
            export_paths["csv"] = csv_path

            # Export summary report
            report_path = self.export_summary_report(export_dir)
            export_paths["report"] = report_path

            # Create index file
            index_path = self._create_index_file(export_dir, export_paths)
            export_paths["index"] = index_path

            logger.info(f"Successfully exported all data to {export_dir}")

        except Exception as e:
            logger.error(f"Error during export: {e}")
            raise

        return export_paths

    def _create_index_file(self, export_dir: Path, export_paths: Dict[str, str]) -> str:
        """
        Create an index file listing all exports.

        Args:
            export_dir: Export directory path
            export_paths: Dictionary of export file paths

        Returns:
            Path to index file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        index_filename = f"export_index_{timestamp}.md"
        index_path = export_dir / index_filename

        # Get statistics
        stats = self.get_statistics()

        # Create index content
        index_content = (
            f"# Web Scraping Export Index\n\n"
            f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**Total Records:** {stats.get('total_scraped', 0)}\n"
            f"**Unique Domains:** {stats.get('domains', 0)}\n\n"
            "## 📁 Exported Files\n\n"
            "| Format | File Path | Description |\n"
            "|--------|-----------|-------------|\n"
            f"| JSON | `{Path(export_paths.get('json', '')).name}` | Complete data with metadata |\n"
            f"| CSV | `{Path(export_paths.get('csv', '')).name}` | Tabular data for analysis |\n"
            f"| Report | `{Path(export_paths.get('report', '')).name}` | Human-readable summary |\n\n"
            "## 📊 Quick Statistics\n\n"
            "### Categories\n"
        )

        # Add category breakdown
        categories = stats.get("categories", {})
        for category, count in categories.items():
            percentage = (count / stats.get("total_scraped", 1)) * 100
            index_content += f"- **{category}:** {count} ({percentage:.1f}%)\n"

        index_content += "\n### Status Codes\n"

        # Add status code breakdown
        status_codes = stats.get("status_codes", {})
        for status, count in status_codes.items():
            percentage = (count / stats.get("total_scraped", 1)) * 100
            index_content += f"- **HTTP {status}:** {count} ({percentage:.1f}%)\n"

        index_content += f"""
## 🗂️ Directory Structure

```
{export_dir.name}/
├── json/           # JSON exports with full data
├── csv/            # CSV exports for spreadsheet analysis
├── reports/        # Human-readable summary reports
└── logs/           # Processing logs (if any)
```

## 🔍 Data Fields

### JSON Export Fields
- `url`: Original URL scraped
- `title`: Page title
- `content`: Extracted text content
- `category`: AI-assigned category
- `metadata`: Technical metadata (links, images, etc.)
- `timestamp`: When the page was scraped
- `status_code`: HTTP response code

### CSV Export Fields
- Basic fields plus flattened metadata for easy analysis
- Additional computed fields like content_length
- Technology detection results

---
*Generated by AI-Powered Intelligent Web Scraper v1.0.0*
"""

        # Write index file
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)

        logger.info(f"Created export index: {index_path}")
        return str(index_path)


# Example usage and testing
if __name__ == "__main__":
    # Create scraper instance
    config = WebScraperConfig(delay_min=0.5, delay_max=1.5)
    scraper = IntelligentWebScraper(config)

    # Test URLs from different categories
    test_urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://example.com",
    ]

    print("🕷️  AI-Powered Intelligent Web Scraper")
    print("=" * 50)

    # Scrape test URLs
    results = scraper.scrape_multiple_urls(test_urls)

    # Show statistics
    stats = scraper.get_statistics()
    print("\n📊 Scraping Statistics:")
    print(json.dumps(stats, indent=2))

    # Export data with organized folder structure
    print("\n💾 Exporting data...")
    export_paths = scraper.export_all()

    print("\n📁 Data exported to organized directory structure:")
    for export_type, file_path in export_paths.items():
        file_path_obj = Path(file_path)
        # Show relative path from the exports directory
        try:
            relative_path = file_path_obj.relative_to(Path.cwd())
        except ValueError:
            # If relative path fails, just show the file path
            relative_path = file_path_obj
        print(f"  - {export_type.upper()}: {relative_path}")

    print(
        f"\n🗂️  All exports organized in: exports/{datetime.now().year}/{datetime.now().month:02d}/{datetime.now().day:02d}/"
    )
    print("   📄 Check the index file for complete export summary!")
