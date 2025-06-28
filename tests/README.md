# Testing Documentation

This document describes the testing strategy and how to run tests for the webscraper project.

## Test Structure

The test suite is organized into several categories:

### 1. Basic Tests (`test_basic.py`)
- Package import verification
- Basic functionality validation
- Dependency availability checks

### 2. Unit Tests
- `test_models.py` - Data model tests
- `test_validators.py` - URL validation tests
- `test_categorizer.py` - Content categorization tests
- `test_metadata_extractor.py` - Metadata extraction tests
- `test_content_processor.py` - HTML processing tests
- `test_exporters.py` - Data export tests
- `test_scraper.py` - Main scraper functionality tests

### 3. Integration Tests (`test_integration.py`)
- End-to-end workflow tests
- Component interaction tests
- Real dependency integration tests

## Running Tests

### Quick Start
Run all tests:
```bash
cd tests
python run_tests.py
```

### Using pytest directly
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run only unit tests (fast)
pytest tests/ -m "not integration" -v

# Run only integration tests
pytest tests/ -m "integration" -v
```

### Using the test runner script
```bash
# Run all tests with coverage
python tests/run_tests.py

# Run only unit tests
python tests/run_tests.py --unit-only

# Run only integration tests
python tests/run_tests.py --integration-only

# Run code quality checks
python tests/run_tests.py --lint

# Run everything (tests + linting)
python tests/run_tests.py --all
```

## Test Categories

Tests are marked with pytest markers:

- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Slower integration tests
- `@pytest.mark.slow` - Tests that take significant time

## Test Coverage

The test suite aims for:
- **80%+ code coverage** minimum
- **100% coverage** for critical paths
- **All public APIs** tested
- **Error conditions** tested

### Coverage Report
After running tests with coverage, view the HTML report:
```bash
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

## Test Fixtures

Common test fixtures are defined in `conftest.py`:
- `sample_html` - Sample HTML for testing
- `sample_urls` - Valid URLs for testing
- `invalid_urls` - Invalid URLs for testing

## Mocking Strategy

Tests use unittest.mock for:
- **HTTP requests** - Mock `requests.Session.get`
- **File operations** - Mock file I/O operations
- **External dependencies** - Mock third-party services
- **Time-dependent operations** - Mock `time.sleep`

## Testing Best Practices

### 1. Test Isolation
- Each test is independent
- No shared state between tests
- Use fixtures for test data

### 2. Clear Test Names
```python
def test_validator_rejects_blocked_domains():
    """Test that validator rejects social media domains."""
```

### 3. Arrange-Act-Assert Pattern
```python
def test_scraper_handles_valid_url():
    # Arrange
    scraper = WebScraper()
    url = "https://example.com"

    # Act
    result = scraper.scrape_url(url)

    # Assert
    assert result.success is True
```

### 4. Test Edge Cases
- Empty inputs
- Invalid inputs
- Network failures
- Malformed HTML
- Large data sets

### 5. Error Testing
```python
def test_scraper_handles_network_error():
    with patch('requests.Session.get', side_effect=ConnectionError):
        result = scraper.scrape_url("https://example.com")
        assert result.success is False
```

## Continuous Integration

Tests should be run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    python -m pytest tests/ --cov=src --cov-fail-under=80
```

## Test Data

### Sample HTML
```html
<html>
    <head>
        <title>Test Page</title>
        <meta name="description" content="Test description">
    </head>
    <body>
        <main>
            <h1>Main Content</h1>
            <p>Test content</p>
        </main>
    </body>
</html>
```

### Sample URLs
- Valid: `https://example.com`
- E-commerce: `https://shop.example.com`
- News: `https://news.example.com`
- Invalid: `not-a-url`
- Blocked: `https://facebook.com`

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure `src/` is in Python path
   - Check `conftest.py` configuration

2. **Mock Issues**
   - Verify mock paths match actual imports
   - Use `spec` parameter for better mocking

3. **Coverage Issues**
   - Check for unreachable code
   - Add tests for error conditions

4. **Slow Tests**
   - Use mocks instead of real HTTP requests
   - Mark slow tests with `@pytest.mark.slow`

### Debugging Tests
```bash
# Run with pdb on failure
pytest tests/ --pdb

# Verbose output
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -l

# Run specific test with debugging
pytest tests/test_models.py::TestScrapedData::test_creation -v -s
```

## Adding New Tests

When adding new functionality:

1. **Write tests first** (TDD approach)
2. **Test both success and failure cases**
3. **Add appropriate markers** (`@pytest.mark.unit`, etc.)
4. **Update fixtures** if needed
5. **Maintain coverage** above 80%

Example test template:
```python
class TestNewFeature:
    """Test cases for new feature."""

    def setup_method(self):
        """Set up test fixtures."""
        self.feature = NewFeature()

    def test_feature_success_case(self):
        """Test successful operation."""
        # Arrange
        input_data = "test input"

        # Act
        result = self.feature.process(input_data)

        # Assert
        assert result is not None
        assert result.success is True

    def test_feature_error_case(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            self.feature.process(None)
```
