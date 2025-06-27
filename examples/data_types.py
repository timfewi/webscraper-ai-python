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

print("\nNumbers:")
print(f"Total pages: {total_pages}")
print(f"Current page: {current_page}")
print(f"Success rate: {success_rate}%")

# 3. Lists (collections of items)
urls_to_scrape = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com",
]

scraped_data = ["Title 1", "Title 2", "Title 3"]

print("\nLists:")
print(f"URLs to scrape: {urls_to_scrape}")
print(f"Scraped titles: {scraped_data}")

# 4. Dictionaries (key-value pairs, like JSON)
page_info = {
    "url": "https://example.com",
    "title": "Example Site",
    "status_code": 200,
    "content_length": 1500,
}

print("\nDictionary:")
print(f"Page info: {page_info}")
print(f"Just the title: {page_info['title']}")

# 5. Booleans (True/False values)
is_page_loaded = True
has_errors = False

print("\nBooleans:")
print(f"Page loaded: {is_page_loaded}")
print(f"Has errors: {has_errors}")
