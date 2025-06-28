#!/usr/bin/env python3
"""
Demonstration script for AI-Enhanced Web Scraping with Prompt Engineering.

This script showcases the advanced AI capabilities integrated into the web scraper,
including OpenAI-powered content categorization, sentiment analysis, and quality scoring.
"""

import logging
import os
from pathlib import Path
import sys

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import after path setup - these need to be after sys.path modification
# ruff: noqa: E402
from src.ai_enhanced_scraper import AIEnhancedWebScraper
from src.intelligent_webscraper import WebScraperConfig
from src.prompt_engineer import PromptConfig, PromptEngineer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Demonstrate AI-enhanced web scraping capabilities."""

    print("🤖 AI-Enhanced Web Scraper Demonstration")
    print("=" * 60)

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   Please set your OpenAI API key in the .env file")
        return

    print("✅ OpenAI API key found")

    # Configuration
    scraper_config = WebScraperConfig(
        delay_min=0.5, delay_max=1.5, timeout=30, max_retries=3
    )

    prompt_config = PromptConfig(
        model="gpt-4.1-nano",  # Using GPT-4.1-nano for best results
        max_tokens=1000,
        temperature=0.1,  # Low temperature for consistent categorization
        top_p=0.9,
    )

    # Create AI-enhanced scraper
    print("\n🔧 Initializing AI-Enhanced Web Scraper...")
    scraper = AIEnhancedWebScraper(
        scraper_config=scraper_config,
        prompt_config=prompt_config,
        enable_ai_analysis=True,
    )

    if not scraper.enable_ai_analysis:
        print(
            "⚠️  AI analysis failed to initialize. Running with basic categorization."
        )
    else:
        print("✅ AI analysis initialized successfully")

    # Test URLs representing different content categories
    test_urls = [
        "https://example.com/tech-article",
        # Golang docs:
        "https://go.dev/doc/",
    ]

    print(f"\n📡 Scraping {len(test_urls)} test URLs...")
    print("   This may take a few moments with AI analysis enabled...")

    # Scrape URLs with AI enhancement
    results = scraper.scrape_multiple_urls(test_urls)

    print(f"\n✅ Scraping completed! Successfully scraped {len(results)} URLs")

    # Show basic statistics
    print("\n📊 Basic Statistics:")
    basic_stats = scraper.get_statistics()
    for key, value in basic_stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")

    # Show AI-enhanced statistics if available
    if scraper.enable_ai_analysis and scraper.ai_analyses:
        print("\n🤖 AI Analysis Results:")
        ai_stats = scraper.get_ai_statistics()

        print(f"  Total AI Analyses: {ai_stats.get('total_analyzed', 0)}")
        print(f"  Average Confidence: {ai_stats.get('average_confidence', 0):.3f}")
        print(f"  Average Quality: {ai_stats.get('average_quality', 0):.3f}")

        print("\n  Category Distribution:")
        category_dist = ai_stats.get("category_distribution", {})
        for category, count in category_dist.items():
            print(f"    {category}: {count}")

        print("\n  Sentiment Distribution:")
        sentiment_dist = ai_stats.get("sentiment_distribution", {})
        for sentiment, count in sentiment_dist.items():
            emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}.get(
                sentiment, "🤔"
            )
            print(f"    {emoji} {sentiment}: {count}")

        # Show detailed analysis for each URL
        print("\n🔍 Detailed AI Analysis:")
        for i, analysis in enumerate(scraper.ai_analyses, 1):
            # Find corresponding scraped data
            scraped_item = None
            for item in scraper.scraped_data:
                if hasattr(item, "metadata") and item.metadata:
                    ai_data = item.metadata.get("ai_analysis", {})
                    if ai_data.get("confidence") == analysis.confidence:
                        scraped_item = item
                        break

            print(f"\n  Analysis {i}:")
            if scraped_item:
                print(f"    URL: {scraped_item.url}")
                print(f"    Title: {scraped_item.title or 'No title'}")
                print(f"    Category: {analysis.category}")
                print(f"    Confidence: {analysis.confidence:.3f}")
                print(f"    Quality Score: {analysis.quality_score:.3f}")
                print(f"    Sentiment: {analysis.sentiment}")
                print(f"    Keywords: {', '.join(analysis.keywords[:5])}")
                print(f"    Reasoning: {analysis.reasoning[:200]}...")

    # Export enhanced data
    print("\n💾 Exporting enhanced data...")
    export_paths = scraper.export_all_enhanced()

    print("\n📁 Exported files:")
    for export_type, file_path in export_paths.items():
        file_path_obj = Path(file_path)
        try:
            relative_path = file_path_obj.relative_to(Path.cwd())
        except ValueError:
            relative_path = file_path_obj
        print(f"  - {export_type.upper()}: {relative_path}")

    # Show prompt engineering demonstration
    if scraper.enable_ai_analysis and scraper.prompt_engineer:
        print("\n🧠 Prompt Engineering Demonstration:")
        print("   Testing standalone prompt engineering features...")

        # Test categorization with custom content
        test_content = """
        Welcome to our online electronics store! We offer the latest smartphones,
        laptops, tablets, and accessories at competitive prices. Shop now and
        get free shipping on orders over $50. Add items to your cart and checkout
        securely with our payment system.
        """

        analysis = scraper.prompt_engineer.categorize_content(
            url="https://example-electronics-store.com",
            title="Best Electronics Store - Shop Online",
            content=test_content,
        )

        print("\n  Test Content Analysis:")
        print(f"    Category: {analysis.category}")
        print(f"    Confidence: {analysis.confidence:.3f}")
        print(f"    Keywords: {', '.join(analysis.keywords)}")
        print(f"    Sentiment: {analysis.sentiment}")
        print(f"    Quality: {analysis.quality_score:.3f}")
        print(f"    Reasoning: {analysis.reasoning}")

        # Test enhanced content analysis
        enhanced = scraper.prompt_engineer.enhance_content_analysis(
            content=test_content, category=analysis.category
        )

        print("\n  Enhanced Analysis:")
        print(f"    Summary: {enhanced.get('summary', 'N/A')}")
        print(f"    Key Points: {enhanced.get('key_points', [])}")
        print(f"    Category-Specific Data: {enhanced.get('category_specific', {})}")

    print("\n🎉 AI-Enhanced Web Scraping Demonstration Complete!")
    print("\nKey Features Demonstrated:")
    print("  ✅ OpenAI-powered content categorization")
    print("  ✅ Advanced prompt engineering techniques")
    print("  ✅ Sentiment analysis and quality scoring")
    print("  ✅ Enhanced data export with AI insights")
    print("  ✅ Comprehensive statistics and reporting")

    if scraper.enable_ai_analysis and export_paths.get("ai_insights"):
        print("\n📋 Check the AI insights report for detailed analysis:")
        print(f"   {export_paths['ai_insights']}")


def demonstrate_prompt_engineering() -> None:
    """Demonstrate standalone prompt engineering capabilities."""

    print("\n" + "=" * 60)
    print("🎯 Standalone Prompt Engineering Demonstration")
    print("=" * 60)

    try:
        # Initialize prompt engineer
        config = PromptConfig(model="gpt-4o", temperature=0.1)
        engineer = PromptEngineer(config)

        # Test cases with different content types
        test_cases = [
            {
                "url": "https://tech-blog.example.com/ai-tutorial",
                "title": "Building AI Applications with Python",
                "content": """
                In this comprehensive tutorial, we'll explore how to build AI applications
                using Python. We'll cover machine learning libraries like scikit-learn,
                TensorFlow, and PyTorch. The tutorial includes code examples, best practices,
                and deployment strategies. Perfect for developers looking to get started
                with AI development.
                """,
                "expected_category": "Technical",
            },
            {
                "url": "https://news.example.com/breaking-news",
                "title": "Breaking: Major Technology Breakthrough Announced",
                "content": """
                Scientists at a leading research institution have announced a major
                breakthrough in quantum computing technology. The development could
                revolutionize how we approach complex computational problems.
                The research was published today in the journal Nature.
                """,
                "expected_category": "News/Blog",
            },
            {
                "url": "https://shop.example.com/products/laptop",
                "title": "Premium Gaming Laptop - On Sale Now!",
                "content": """
                Discover our high-performance gaming laptop featuring the latest GPU,
                16GB RAM, and ultra-fast SSD storage. Perfect for gaming, content creation,
                and professional work. Price: $1,299.99 (was $1,599.99). Free shipping
                available. Add to cart now and save 25%!
                """,
                "expected_category": "E-commerce",
            },
        ]

        print("\n📝 Testing AI categorization with different content types:\n")

        for i, test_case in enumerate(test_cases, 1):
            print(f"Test Case {i}: {test_case['expected_category']}")
            print(f"URL: {test_case['url']}")
            print(f"Title: {test_case['title']}")

            # Analyze content
            analysis = engineer.categorize_content(
                url=test_case["url"],
                title=test_case["title"],
                content=test_case["content"],
            )

            # Check if categorization matches expected
            correct = analysis.category == test_case["expected_category"]
            status = "✅" if correct else "❌"

            print(f"Result: {status}")
            print(f"  Predicted: {analysis.category}")
            print(f"  Expected: {test_case['expected_category']}")
            print(f"  Confidence: {analysis.confidence:.3f}")
            print(f"  Quality: {analysis.quality_score:.3f}")
            print(f"  Keywords: {', '.join(analysis.keywords[:3])}")
            print(f"  Reasoning: {analysis.reasoning[:150]}...")
            print()

        print("🎯 Prompt Engineering Features Demonstrated:")
        print("  ✅ Structured prompt templates")
        print("  ✅ Category-specific analysis")
        print("  ✅ Confidence scoring")
        print("  ✅ Keyword extraction")
        print("  ✅ Quality assessment")
        print("  ✅ Chain-of-thought reasoning")

    except Exception as e:
        print(f"❌ Prompt engineering demonstration failed: {e}")
        print(
            "   Make sure your OpenAI API key is valid and you have sufficient credits"
        )


if __name__ == "__main__":
    try:
        # Run main demonstration
        main()

        # Run standalone prompt engineering demo
        demonstrate_prompt_engineering()

    except KeyboardInterrupt:
        print("\n\n⏹️  Demonstration interrupted by user")
    except Exception as e:
        logger.error(f"Demonstration failed: {e}")
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your OpenAI API key in .env file")
        print("  2. Ensure you have sufficient OpenAI credits")
        print("  3. Check your internet connection")
        print("  4. Verify all dependencies are installed")
    finally:
        print("\n👋 Thank you for trying the AI-Enhanced Web Scraper!")
