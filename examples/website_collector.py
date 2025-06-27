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
        "added_date": "2024-01-01",  # We'll learn about dates later
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
