# AI-Powered Web Scraper 🤖🕷️

**A professional-grade web scraping framework with intelligent content categorization and data processing capabilities.**

[![CI](https://github.com/timfewi/webscraper-ai-python/workflows/Code%20Quality%20&%20Tests/badge.svg)](https://github.com/timfewi/webscraper-ai-python/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/timfewi/webscraper-ai-python)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🚀 Features

- **Intelligent Content Extraction**: Automatically extracts structured data from web pages
- **AI-Powered Categorization**: Uses machine learning to categorize scraped content
- **Dynamic Content Support**: Handles JavaScript-rendered content with Selenium
- **Quality Assessment**: Scores and validates scraped content quality
- **Multiple Export Formats**: JSON, CSV, XML data export options
- **Robust Error Handling**: Graceful handling of network issues and malformed data
- **Rate Limiting**: Respects website resources with configurable delays
- **Modular Architecture**: Clean, maintainable code with dependency injection

## 🛠️ Tech Stack

- **Python 3.8+** - Core programming language
- **requests** - HTTP client for web requests
- **BeautifulSoup4** - HTML parsing and data extraction
- **Selenium** - Dynamic content and browser automation
- **pandas** - Data manipulation and analysis
- **scikit-learn** - Machine learning for content categorization
- **pytest** - Testing framework with 100% coverage

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Chrome/Chromium browser (for Selenium)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/timfewi/webscraper-ai-python.git
cd webscraper-ai-python

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Development Setup

```bash
# Setup development environment
make setup-dev

# Verify installation
make check
make test
```

## 🎯 Quick Usage

### Basic Web Scraping

```python
from src import WebScraper, ScrapingConfig

# Configure the scraper
config = ScrapingConfig(
    delay_between_requests=1.0,
    max_retries=3,
    timeout=30
)

# Create scraper instance
scraper = WebScraper(config)

# Scrape a URL
result = scraper.scrape_url("https://example.com")

if result.success:
    print(f"Title: {result.data.title}")
    print(f"Content: {result.data.content[:100]}...")
    print(f"Category: {result.data.category}")
```

### AI-Powered Intelligent Scraping

```python
from src import IntelligentWebScraper

# Create intelligent scraper with AI categorization
scraper = IntelligentWebScraper({
    'categorization_enabled': True,
    'quality_threshold': 70,
    'output_format': 'json'
})

# Scrape multiple URLs
urls = [
    "https://example.com/tech-article",
    "https://example.com/business-news",
    "https://example.com/health-tips"
]

results = scraper.scrape_urls(urls)

# Generate insights report
report = scraper.generate_report()
print(f"Scraped {report['total_items']} items")
print(f"Categories: {report['categories']}")
```

### Data Export

```python
from src import DataExporterFactory

# Export to different formats
exporter = DataExporterFactory.create_exporter('json')
exporter.export(scraped_data, 'output.json')

# Export to CSV
csv_exporter = DataExporterFactory.create_exporter('csv')
csv_exporter.export(scraped_data, 'output.csv')
```

## 📊 Project Structure

```
webscraper-ai-python/
├── src/                           # Source code
│   ├── __init__.py               # Package initialization
│   ├── scraper.py                # Core scraping logic
│   ├── intelligent_webscraper.py # AI-powered scraper
│   ├── models.py                 # Data models
│   ├── categorizer.py            # Content categorization
│   ├── validators.py             # URL validation
│   ├── exporters.py              # Data export utilities
│   └── config.py                 # Configuration management
├── tests/                         # Test suite (100% coverage)
├── learning_steps/               # Step-by-step tutorials
├── examples/                     # Usage examples
├── docs/                         # Documentation
└── Makefile                      # Development commands
```

## 🔧 Development

### Available Commands

```ps1
# Show available commands
.\dev.ps1 help

# Setup development environment
.\dev.ps1 setup-dev

# Code quality
.\dev.ps1 format
.\dev.ps1 lint
.\dev.ps1 type-check
.\dev.ps1 check

# Testing
.\dev.ps1 test
.\dev.ps1 test-cov

# Maintenance
.\dev.ps1 clean
.\dev.ps1 security
.\dev.ps1 pre-commit-all

# Full CI pipeline
.\dev.ps1 ci
```

### Code Quality

This project maintains high code quality standards:

- **100% Test Coverage** - Comprehensive test suite
- **Type Hints** - Full type annotation coverage
- **Linting** - Ruff for code quality (600+ rules)
- **Formatting** - Black for consistent code style
- **Security** - Bandit for security vulnerability scanning

## 📚 Learning Resources

New to web scraping or Python? Check out our comprehensive learning path:

- **[Step 1: Python Setup & Basics](learning_steps/step_01_setup.md)** - Environment setup and Python fundamentals
- **[Step 2: Control Structures](learning_steps/step_02_control_structures.md)** - Loops, conditionals, and logic
- **[Step 3: Functions & Modules](learning_steps/step_03_functions_modules.md)** - Code organization and error handling
- **[Step 4: Web Scraping Basics](learning_steps/step_04_http_html.md)** - HTTP requests and HTML parsing
- **[Step 5: Complete Project](learning_steps/step_05_complete_project.md)** - AI integration and advanced features

## 🤝 Contributing

Contributions are welcome! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `make ci`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern Python best practices
- Inspired by the need for intelligent web scraping solutions
- Designed for both learning and production use

---

**Ready to start scraping intelligently?** 🚀

[Get Started](learning_steps/step_01_setup.md) | [View Examples](examples/) | [API Documentation](docs/)
