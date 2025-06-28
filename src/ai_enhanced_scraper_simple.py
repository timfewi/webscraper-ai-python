# Create src/ai_enhanced_scraper_simple.py
import logging
from typing import Any, Dict, List, Optional

from .intelligent_webscraper import IntelligentWebScraper, WebScraperConfig

logger = logging.getLogger(__name__)


class AIEnhancedWebScraper(IntelligentWebScraper):
    """Simplified AI-Enhanced Web Scraper without OpenAI dependencies."""

    def __init__(
        self, scraper_config: Optional[WebScraperConfig] = None, **kwargs: Any
    ) -> None:
        super().__init__(scraper_config)
        self.enable_ai_analysis = False
        self.ai_analyses: List[Any] = []
        logger.warning("AI features disabled - OpenAI dependencies not available")

    def get_ai_statistics(self) -> Dict[str, Any]:
        return {
            "message": "AI analysis disabled",
            "total_analyzed": 0,
            "ai_enabled": False,
        }

    def export_all_enhanced(
        self, base_filename: Optional[str] = None
    ) -> Dict[str, str]:
        return super().export_all(base_filename)
