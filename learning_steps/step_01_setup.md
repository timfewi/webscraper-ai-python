# Step 1: Python Environment Setup & Hello World

## 🎯 Learning Goals
- Set up Python development environment
- Understand Python basics
- Write your first Python program
- Learn about Python syntax and indentation

## 📖 Theory

### What is Python?
Python is a high-level, interpreted programming language known for:
- **Readable syntax**: Code that looks almost like English
- **Versatility**: Used for web development, data science, AI, automation
- **Large ecosystem**: Thousands of libraries and frameworks
- **Beginner-friendly**: Great for learning programming concepts

### Why Python for Web Scraping?
- Excellent libraries (requests, BeautifulSoup, Selenium)
- Simple syntax for complex tasks
- Strong community support
- Great for data processing and analysis

## 🛠️ Setup Instructions

### 1. Check Python Installation
Open your terminal (PowerShell on Windows) and run:
```bash
python --version
```
You should see Python 3.9 or higher.

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\Activate.ps1

# Activate it (macOS/Linux)
source venv/bin/activate
```

### 3. Install Required Packages
```bash
pip install requests beautifulsoup4 lxml
```

## 💻 Coding Exercise

### Exercise 1: Hello World
Create your first Python file and write a simple program.

**File**: `examples/hello_world.py`

```python
# My first Python program
print("Hello, Web Scraping World!")
print("I'm learning Python step by step!")

# Variables and basic operations
name = "Python Learner"
age = 25
is_learning = True

print(f"My name is {name}")
print(f"I am {age} years old")
print(f"Am I learning Python? {is_learning}")

# Simple calculation
pages_to_scrape = 100
pages_completed = 25
progress = (pages_completed / pages_to_scrape) * 100

print(f"Scraping progress: {progress}%")
```

### Exercise 2: Basic Data Types
Explore Python's fundamental data types.

**File**: `examples/data_types.py`

```python
# Python Data Types - Essential for Web Scraping

# 1. Strings (text data from websites)
website_url = "https://example.com"
page_title = "Welcome to My Site"
html_content = "<h1>Hello World</h1>"

print("String examples:")
print(f"URL: {website_url}")
print(f"Title: {page_title}")
print(f"HTML: {html_content}")

# 2. Numbers (for counting, calculations)
total_pages = 50
current_page = 1
success_rate = 95.5

print(f"\nNumbers:")
print(f"Total pages: {total_pages}")
print(f"Current page: {current_page}")
print(f"Success rate: {success_rate}%")

# 3. Lists (collections of items)
urls_to_scrape = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
]

scraped_data = ["Title 1", "Title 2", "Title 3"]

print(f"\nLists:")
print(f"URLs to scrape: {urls_to_scrape}")
print(f"Scraped titles: {scraped_data}")

# 4. Dictionaries (key-value pairs, like JSON)
page_info = {
    "url": "https://example.com",
    "title": "Example Site",
    "status_code": 200,
    "content_length": 1500
}

print(f"\nDictionary:")
print(f"Page info: {page_info}")
print(f"Just the title: {page_info['title']}")

# 5. Booleans (True/False values)
is_page_loaded = True
has_errors = False

print(f"\nBooleans:")
print(f"Page loaded: {is_page_loaded}")
print(f"Has errors: {has_errors}")
```

## 🎯 Mini-Project: Website Info Collector

Create a simple program that collects information about websites you want to scrape.

**File**: `examples/website_collector.py`

```python
"""
Mini-Project: Website Information Collector
This program helps you organize websites you want to scrape later.
"""

def main():
    print("🕷️  Website Information Collector")
    print("=" * 40)

    # Initialize empty list to store website information
    websites = []

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a website")
        print("2. View all websites")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add_website(websites)
        elif choice == "2":
            view_websites(websites)
        elif choice == "3":
            print("Goodbye! Happy scraping! 🚀")
            break
        else:
            print("Invalid choice. Please try again.")

def add_website(websites):
    """Add a new website to our collection"""
    print("\n📝 Adding new website:")

    url = input("Enter website URL: ")
    name = input("Enter website name: ")
    category = input("Enter category (e.g., news, e-commerce, blog): ")

    # Create a dictionary to store website info
    website_info = {
        "url": url,
        "name": name,
        "category": category,
        "added_date": "2024-01-01"  # We'll learn about dates later
    }

    websites.append(website_info)
    print(f"✅ Added {name} to your collection!")

def view_websites(websites):
    """Display all collected websites"""
    if not websites:
        print("\n📭 No websites in your collection yet.")
        return

    print(f"\n📊 Your Website Collection ({len(websites)} sites):")
    print("-" * 50)

    for i, site in enumerate(websites, 1):
        print(f"{i}. {site['name']}")
        print(f"   URL: {site['url']}")
        print(f"   Category: {site['category']}")
        print()

# This is how we run the program
if __name__ == "__main__":
    main()
```

## 🔍 Key Concepts Learned

### 1. Variables
```python
name = "value"  # String
count = 42      # Integer
price = 19.99   # Float
is_active = True # Boolean
```

### 2. Data Types
- **Strings**: Text data (website content, URLs)
- **Numbers**: Integers and floats (page counts, prices)
- **Lists**: Ordered collections of items
- **Dictionaries**: Key-value pairs (structured data)
- **Booleans**: True/False values

### 3. f-strings (String Formatting)
```python
name = "Python"
print(f"I'm learning {name}!")  # Modern way
print("I'm learning {}!".format(name))  # Older way
```

### 4. Functions
```python
def function_name(parameter):
    """Function documentation"""
    # Function body
    return result
```

## 🧪 Testing Your Knowledge

### Quick Quiz
1. What data type would you use to store a list of URLs?
2. How do you access a value in a dictionary?
3. What's the difference between a list and a dictionary?

### Challenge Exercise
Modify the website collector to:
1. Ask for a description of what you want to scrape from each site
2. Add a priority level (1-5) for each website
3. Display websites sorted by priority when viewing

## 🎯 Next Steps

In Step 2, we'll learn about:
- Control structures (if/else, loops)
- Working with lists and dictionaries in detail
- Making decisions in your code
- Repeating tasks automatically

## 📝 Notes
- Save all your code in the `examples/` folder
- Try running each program to see how it works
- Don't worry about memorizing everything - focus on understanding
- Experiment and modify the code to see what happens!

---
**Completion Checklist:**
- [ ] Python environment is set up
- [ ] Created and ran hello_world.py
- [ ] Explored data types in data_types.py
- [ ] Built the website collector mini-project
- [ ] Understood variables, functions, and basic syntax

Ready for Step 2? Let's dive deeper into Python! 🚀
