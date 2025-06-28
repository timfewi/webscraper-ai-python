# test_imports.py
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    print("Testing individual imports...")

    # Test 1: Models
    from src.models import ScrapedData

    assert ScrapedData is not None
    assert (
        ScrapedData.__name__ == "ScrapedData"
    )  # Ensure the class is correctly imported
    assert hasattr(ScrapedData, "url")  # Check if the class has the

    print("✅ ScrapedData imported successfully")

    # Test 2: Intelligent WebScraper
    from src.intelligent_webscraper import IntelligentWebScraper, WebScraperConfig

    assert IntelligentWebScraper is not None
    assert WebScraperConfig is not None

    print("✅ IntelligentWebScraper imported successfully")

    # Test 3: PromptEngineer (this is likely where it fails)
    from src.prompt_engineer import ContentAnalysis, PromptConfig, PromptEngineer

    assert ContentAnalysis is not None
    assert PromptConfig is not None
    assert PromptEngineer is not None

    print("✅ PromptEngineer imported successfully")

    # Test 4: AI Enhanced Scraper
    from src.ai_enhanced_scraper import AIEnhancedWebScraper

    assert AIEnhancedWebScraper is not None

    print("✅ AIEnhancedWebScraper imported successfully")

    print("🎉 All imports successful!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Error occurred in: {e.name if hasattr(e, 'name') else 'unknown module'}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
