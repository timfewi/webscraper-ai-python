# Step 2: Control Structures & Decision Making

## 🎯 Learning Goals
- Master if/else statements for conditional logic
- Learn loops (for, while) for repetitive tasks
- Understand list comprehensions
- Apply control structures to web scraping scenarios

## 📖 Theory

### Why Control Structures Matter for Web Scraping
- **Conditional Logic**: Check if a page loaded successfully
- **Loops**: Process multiple URLs or data items
- **Error Handling**: Decide what to do when scraping fails
- **Data Filtering**: Extract only the data you need

## 💻 Coding Exercises

### Exercise 1: Conditional Logic for Web Scraping
**File**: `examples/step02_conditionals.py`

```python
"""
Step 2: Conditional Logic for Web Scraping
Learn to make decisions in your code
"""

def check_url_validity(url):
    """Check if a URL is valid for scraping"""
    if not url:
        return False, "URL is empty"

    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"

    if len(url) < 10:
        return False, "URL seems too short"

    # Check for common invalid patterns
    invalid_patterns = ['.local', 'localhost', '127.0.0.1']
    for pattern in invalid_patterns:
        if pattern in url:
            return False, f"URL contains invalid pattern: {pattern}"

    return True, "URL is valid"

def categorize_website(url):
    """Categorize website based on URL patterns"""
    url_lower = url.lower()

    if 'shop' in url_lower or 'store' in url_lower or 'buy' in url_lower:
        return "E-commerce"
    elif 'news' in url_lower or 'blog' in url_lower:
        return "News/Blog"
    elif 'github.com' in url_lower:
        return "Code Repository"
    elif 'wikipedia.org' in url_lower:
        return "Reference"
    else:
        return "General"

def simulate_scraping_status():
    """Simulate different scraping scenarios"""
    import random

    scenarios = [
        (200, "Success"),
        (404, "Page not found"),
        (403, "Access forbidden"),
        (500, "Server error"),
        (429, "Rate limited")
    ]

    status_code, message = random.choice(scenarios)

    if status_code == 200:
        print(f"✅ {message} - Continue scraping")
        return True
    elif status_code == 429:
        print(f"⏳ {message} - Wait and retry")
        return False
    elif status_code in [403, 404]:
        print(f"❌ {message} - Skip this URL")
        return False
    else:
        print(f"⚠️  {message} - Log error and continue")
        return False

# Test the functions
if __name__ == "__main__":
    print("🔍 URL Validation Tests")
    print("=" * 30)

    test_urls = [
        "https://example.com",
        "http://shop.example.com",
        "https://news.site.com",
        "ftp://invalid.com",
        "https://localhost:8000",
        ""
    ]

    for url in test_urls:
        is_valid, message = check_url_validity(url)
        category = categorize_website(url) if is_valid else "N/A"
        print(f"URL: {url or 'Empty'}")
        print(f"  Valid: {is_valid} - {message}")
        print(f"  Category: {category}\n")

    print("🎲 Scraping Simulation")
    print("=" * 20)
    for i in range(5):
        print(f"Attempt {i+1}: ", end="")
        simulate_scraping_status()
```

### Exercise 2: Loops for Processing Multiple Items
**File**: `examples/step02_loops.py`

```python
"""
Step 2: Loops for Web Scraping
Process multiple URLs and data efficiently
"""

def process_url_list(urls):
    """Process a list of URLs with different loop types"""
    print("🔄 Processing URLs with different loop methods\n")

    # Method 1: Basic for loop
    print("Method 1: Basic for loop")
    for url in urls:
        print(f"  Processing: {url}")

    print("\nMethod 2: Loop with index")
    for i, url in enumerate(urls):
        print(f"  {i+1}. Processing: {url}")

    print("\nMethod 3: Loop with condition")
    for url in urls:
        if not url.startswith('https://'):
            print(f"  ⚠️  Skipping insecure URL: {url}")
            continue
        print(f"  ✅ Processing secure URL: {url}")

def simulate_batch_scraping(urls, max_retries=3):
    """Simulate scraping multiple URLs with retry logic"""
    import random
    import time

    results = []

    for url in urls:
        print(f"\n🌐 Scraping: {url}")

        # Retry loop
        retry_count = 0
        success = False

        while retry_count < max_retries and not success:
            # Simulate scraping (random success/failure)
            if random.random() > 0.3:  # 70% success rate
                print(f"  ✅ Success on attempt {retry_count + 1}")
                results.append({
                    'url': url,
                    'status': 'success',
                    'attempts': retry_count + 1,
                    'data': f"Sample data from {url}"
                })
                success = True
            else:
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = retry_count * 2  # Exponential backoff
                    print(f"  ❌ Failed attempt {retry_count}, waiting {wait_time}s...")
                    time.sleep(1)  # Simulate wait (shortened for demo)
                else:
                    print(f"  ❌ Failed after {max_retries} attempts")
                    results.append({
                        'url': url,
                        'status': 'failed',
                        'attempts': max_retries,
                        'data': None
                    })

    return results

def filter_and_transform_data(raw_data):
    """Use list comprehensions to filter and transform data"""
    print("\n🔍 Filtering and Transforming Data")
    print("=" * 35)

    # List comprehension examples
    successful_urls = [item['url'] for item in raw_data if item['status'] == 'success']
    failed_urls = [item['url'] for item in raw_data if item['status'] == 'failed']

    # Transform data
    url_lengths = [len(item['url']) for item in raw_data]
    domains = [item['url'].split('//')[1].split('/')[0] for item in raw_data if item['status'] == 'success']

    print(f"Successful URLs ({len(successful_urls)}):")
    for url in successful_urls:
        print(f"  ✅ {url}")

    print(f"\nFailed URLs ({len(failed_urls)}):")
    for url in failed_urls:
        print(f"  ❌ {url}")

    print(f"\nDomains extracted: {domains}")
    print(f"Average URL length: {sum(url_lengths) / len(url_lengths):.1f} characters")

# Main execution
if __name__ == "__main__":
    # Sample URLs for testing
    test_urls = [
        "https://example.com",
        "https://github.com/python",
        "http://insecure-site.com",
        "https://news.example.com",
        "https://shop.example.com"
    ]

    print("🚀 Web Scraping Loop Examples")
    print("=" * 35)

    # Process URLs
    process_url_list(test_urls)

    # Simulate batch scraping
    print("\n" + "="*50)
    print("🔄 Batch Scraping Simulation")
    print("="*50)

    results = simulate_batch_scraping(test_urls[:3])  # Test with first 3 URLs

    # Filter and analyze results
    filter_and_transform_data(results)
```

### Exercise 3: Advanced Control Flow
**File**: `examples/step02_advanced_control.py`

```python
"""
Step 2: Advanced Control Flow for Web Scraping
Complex decision making and flow control
"""

class ScrapingController:
    """A class to demonstrate advanced control flow in web scraping"""

    def __init__(self):
        self.scraped_count = 0
        self.error_count = 0
        self.rate_limit_hits = 0
        self.max_errors = 5
        self.max_rate_limits = 3

    def should_continue_scraping(self):
        """Decide whether to continue scraping based on current state"""
        if self.error_count >= self.max_errors:
            print(f"❌ Too many errors ({self.error_count}), stopping...")
            return False

        if self.rate_limit_hits >= self.max_rate_limits:
            print(f"⏳ Too many rate limits ({self.rate_limit_hits}), stopping...")
            return False

        return True

    def process_url_with_conditions(self, url, priority="normal"):
        """Process URL with complex conditional logic"""
        print(f"\n🌐 Processing: {url} (Priority: {priority})")

        # Nested conditions for different scenarios
        if priority == "high":
            # High priority URLs get special treatment
            if not self.should_continue_scraping():
                print("  ⚠️  Forcing high priority URL despite errors")

            # Try multiple strategies for high priority
            strategies = ["direct", "proxy", "headless_browser"]
            for strategy in strategies:
                print(f"  🔄 Trying {strategy} strategy...")
                success = self.simulate_scraping_attempt(strategy)
                if success:
                    break
            else:
                print("  ❌ All strategies failed for high priority URL")

        elif priority == "low":
            # Low priority URLs - skip if any issues
            if not self.should_continue_scraping():
                print("  ⏭️  Skipping low priority URL due to errors")
                return False

            # Single attempt for low priority
            success = self.simulate_scraping_attempt("direct")

        else:  # Normal priority
            if not self.should_continue_scraping():
                return False

            # Standard retry logic
            for attempt in range(3):
                success = self.simulate_scraping_attempt("direct")
                if success:
                    break
                elif attempt < 2:
                    print(f"    Retry {attempt + 1}/2...")
            else:
                print("  ❌ Failed after retries")

        return True

    def simulate_scraping_attempt(self, strategy):
        """Simulate a scraping attempt with different outcomes"""
        import random

        # Different success rates for different strategies
        success_rates = {
            "direct": 0.7,
            "proxy": 0.8,
            "headless_browser": 0.9
        }

        if random.random() < success_rates.get(strategy, 0.7):
            self.scraped_count += 1
            print(f"    ✅ Success with {strategy} strategy")
            return True
        else:
            # Simulate different types of failures
            failure_type = random.choice(["error", "rate_limit", "timeout"])

            if failure_type == "error":
                self.error_count += 1
                print(f"    ❌ Error occurred (total errors: {self.error_count})")
            elif failure_type == "rate_limit":
                self.rate_limit_hits += 1
                print(f"    ⏳ Rate limited (total: {self.rate_limit_hits})")
            else:
                print(f"    ⏱️  Timeout occurred")

            return False

    def smart_url_processing(self, urls):
        """Process URLs with intelligent prioritization and flow control"""
        print("🧠 Smart URL Processing")
        print("=" * 25)

        # Categorize URLs by priority
        prioritized_urls = []

        for url in urls:
            if "important" in url or "critical" in url:
                priority = "high"
            elif "optional" in url or "extra" in url:
                priority = "low"
            else:
                priority = "normal"

            prioritized_urls.append((url, priority))

        # Sort by priority (high first, then normal, then low)
        priority_order = {"high": 0, "normal": 1, "low": 2}
        prioritized_urls.sort(key=lambda x: priority_order[x[1]])

        # Process URLs
        for url, priority in prioritized_urls:
            if not self.process_url_with_conditions(url, priority):
                print("⛔ Stopping processing due to excessive errors")
                break

        # Summary
        print(f"\n📊 Summary:")
        print(f"  ✅ Successfully scraped: {self.scraped_count}")
        print(f"  ❌ Errors encountered: {self.error_count}")
        print(f"  ⏳ Rate limits hit: {self.rate_limit_hits}")

# Main execution
if __name__ == "__main__":
    # Test URLs with different priorities
    test_urls = [
        "https://example.com/normal-page",
        "https://example.com/important-data",
        "https://example.com/optional-info",
        "https://example.com/critical-content",
        "https://example.com/extra-details",
        "https://example.com/regular-content"
    ]

    # Create and run the scraping controller
    controller = ScrapingController()
    controller.smart_url_processing(test_urls)
```

## 🔍 Key Concepts Learned

### 1. Conditional Statements
```python
# Basic if/else
if condition:
    # do something
elif other_condition:
    # do something else
else:
    # default action

# Inline conditions
result = "success" if status_code == 200 else "failed"
```

### 2. Loops
```python
# For loops
for item in list:
    process(item)

# While loops
while condition:
    # do something
    # make sure to update condition!

# Loop control
for item in items:
    if skip_condition:
        continue  # Skip to next iteration
    if stop_condition:
        break     # Exit loop completely
```

### 3. List Comprehensions
```python
# Filter items
valid_urls = [url for url in urls if url.startswith('https://')]

# Transform items
domains = [url.split('//')[1] for url in urls]

# Filter and transform
secure_domains = [url.split('//')[1] for url in urls if url.startswith('https://')]
```

## 🧪 Practice Challenges

### Challenge 1: URL Validator
Create a function that validates URLs and categorizes them:
```python
def validate_and_categorize_urls(urls):
    """
    Validate a list of URLs and categorize them
    Return: dict with 'valid', 'invalid', 'categories'
    """
    # Your code here
    pass
```

### Challenge 2: Smart Retry Logic
Implement a retry system that:
- Tries up to 3 times
- Waits longer between each retry (1s, 2s, 4s)
- Gives up on certain error types immediately
- Returns success/failure with attempt count

### Challenge 3: Batch Processor
Create a function that processes URLs in batches:
- Process 5 URLs at a time
- If 3+ URLs in a batch fail, pause for 10 seconds
- Track overall success rate
- Stop if success rate drops below 50%

## 🎯 Next Steps

In Step 3, we'll learn about:
- Functions and modules (organizing your code)
- Error handling (try/except)
- Working with files (saving scraped data)
- Introduction to external libraries

## 📝 Notes
- Practice all the examples by running them
- Try modifying the conditions and see what happens
- Think about how these patterns apply to web scraping
- Control structures are the foundation of all programming logic

---
**Completion Checklist:**
- [ ] Understand if/else statements
- [ ] Can write for and while loops
- [ ] Know when to use continue vs break
- [ ] Comfortable with list comprehensions
- [ ] Completed all coding exercises
- [ ] Attempted at least one practice challenge

Ready for Step 3? Let's organize our code better! 🚀
