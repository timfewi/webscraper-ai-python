"""
AI-Enhanced Intelligent Web Scraper with Advanced Prompt Engineering.

This module integrates the base IntelligentWebScraper with the PromptEngineer
to provide advanced AI-powered content analysis and categorization.
"""

from datetime import datetime
import json
import logging
from pathlib import Path
import random
import time
from typing import Any, Dict, List, Optional

import config

from .intelligent_webscraper import IntelligentWebScraper, ScrapedData, WebScraperConfig
from .prompt_engineer import ContentAnalysis, PromptConfig, PromptEngineer

logger = logging.getLogger(__name__)


class AIEnhancedWebScraper(IntelligentWebScraper):
    """
    Enhanced web scraper with advanced AI capabilities.

    This class extends the base IntelligentWebScraper with:
    - OpenAI-powered content categorization
    - Advanced content analysis
    - Structured data extraction
    - Sentiment analysis
    - Quality scoring
    """

    def __init__(
        self,
        scraper_config: Optional[WebScraperConfig] = None,
        prompt_config: Optional[PromptConfig] = None,
        enable_ai_analysis: bool = True,
    ):
        """
        Initialize the AI-enhanced web scraper.

        Args:
            scraper_config: Configuration for the base scraper
            prompt_config: Configuration for AI prompt engineering
            enable_ai_analysis: Whether to enable AI-powered analysis
        """
        super().__init__(scraper_config)

        self.enable_ai_analysis = enable_ai_analysis
        self.ai_analyses: List[ContentAnalysis] = []
        self.prompt_engineer: Optional[PromptEngineer] = None

        if self.enable_ai_analysis:
            try:
                self.prompt_engineer = PromptEngineer(prompt_config)
                logger.info(
                    "AI-enhanced web scraper initialized with OpenAI integration"
                )

                # Validate AI components
                if not self._validate_ai_components():
                    logger.warning(
                        "AI component validation failed, disabling AI analysis"
                    )
                    self.enable_ai_analysis = False

            except Exception as e:
                logger.warning(
                    f"Failed to initialize AI components: {e}. Falling back to basic categorization."
                )
                self.enable_ai_analysis = False
        else:
            logger.info("AI-enhanced web scraper initialized without AI components")

    def _validate_ai_components(self) -> bool:
        """Validate that AI components are properly initialized."""
        if not self.enable_ai_analysis:
            return False

        if not hasattr(self, "prompt_engineer") or self.prompt_engineer is None:
            logger.warning("PromptEngineer not initialized")
            return False

        # For now, just check if the prompt_engineer exists
        # We could add a test API call here, but it might be expensive
        return True

    def categorize_website(self, url: str, content: Optional[str] = None) -> str:
        """
        Enhanced website categorization using AI when available.

        Args:
            url: The website URL
            content: Optional content to analyze

        Returns:
            Category string
        """
        if self.enable_ai_analysis and self.prompt_engineer and content:
            try:
                # Use AI categorization
                analysis = self.prompt_engineer.categorize_content(
                    url=url,
                    title=None,  # We'll extract title separately
                    content=content,
                )

                # Store the analysis for later use
                self.ai_analyses.append(analysis)

                logger.info(
                    f"AI categorized {url} as {analysis.category} (confidence: {analysis.confidence})"
                )
                return analysis.category

            except Exception as e:
                logger.warning(
                    f"AI categorization failed for {url}: {e}. Using fallback."
                )

        # Fallback to basic categorization
        return super().categorize_website(url, content)

    def scrape_url(self, url: str) -> Optional[ScrapedData]:
        """
        Enhanced URL scraping with AI-powered analysis.

        Args:
            url: The URL to scrape

        Returns:
            Enhanced ScrapedData object or None if failed
        """
        # Get basic scraped data
        scraped_data = super().scrape_url(url)

        if not scraped_data:
            return None

        # Enhance with AI analysis if enabled
        if self.enable_ai_analysis and self.prompt_engineer and scraped_data.content:
            try:
                # Get detailed AI analysis
                ai_analysis = self.prompt_engineer.categorize_content(
                    url=scraped_data.url,
                    title=scraped_data.title,
                    content=scraped_data.content,
                )

                # Update category with AI result
                scraped_data.category = ai_analysis.category

                # Add AI analysis to metadata
                if not scraped_data.metadata:
                    scraped_data.metadata = {}

                scraped_data.metadata.update(
                    {
                        "ai_analysis": {
                            "confidence": ai_analysis.confidence,
                            "reasoning": ai_analysis.reasoning,
                            "keywords": ai_analysis.keywords,
                            "sentiment": ai_analysis.sentiment,
                            "quality_score": ai_analysis.quality_score,
                            "ai_metadata": ai_analysis.metadata,
                        }
                    }
                )

                # Get enhanced content analysis
                try:
                    enhanced_analysis = self.prompt_engineer.enhance_content_analysis(
                        scraped_data.content, ai_analysis.category
                    )

                    scraped_data.metadata["enhanced_analysis"] = enhanced_analysis

                except Exception as e:
                    logger.warning(f"Enhanced analysis failed for {url}: {e}")

                # Store AI analysis
                self.ai_analyses.append(ai_analysis)

                logger.info(f"Enhanced scraping completed for {url} with AI analysis")

            except Exception as e:
                logger.warning(f"AI enhancement failed for {url}: {e}")

        return scraped_data

    def scrape_multiple_urls(self, urls: List[str]) -> List[ScrapedData]:
        """
        Enhanced multiple URL scraping with AI analysis for each URL.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of enhanced ScrapedData objects
        """
        results = []
        total_urls = len(urls)

        logger.info(f"Starting AI-enhanced scraping of {total_urls} URLs")

        for i, url in enumerate(urls, 1):
            try:
                result = self.scrape_url(url)  # This will use our AI-enhanced method
                if result:
                    results.append(result)
                    logger.info(
                        f"Progress: {i}/{total_urls} - Successfully scraped {url}"
                    )
                else:
                    logger.warning(
                        f"Progress: {i}/{total_urls} - Failed to scrape {url}"
                    )

            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")

            # Add delay between requests (from config)
            if i < total_urls and hasattr(self.config, "delay_min"):
                delay = random.uniform(self.config.delay_min, self.config.delay_max)
                time.sleep(delay)

        logger.info(f"Completed scraping: {len(results)}/{total_urls} successful")
        return results

    def get_ai_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about AI analysis results.

        Returns:
            Dictionary with AI-specific statistics
        """
        if not self.enable_ai_analysis:
            return {
                "message": "AI analysis is disabled",
                "total_analyzed": 0,
                "ai_enabled": False,
                "category_distribution": {},
                "average_confidence": 0.0,
                "average_quality": 0.0,
                "sentiment_distribution": {},
            }

        if not self.ai_analyses:
            return {
                "message": "No AI analyses available yet",
                "total_analyzed": 0,
                "ai_enabled": True,
                "category_distribution": {},
                "average_confidence": 0.0,
                "average_quality": 0.0,
                "sentiment_distribution": {},
            }

        if not self.prompt_engineer:
            return {
                "message": "PromptEngineer not available",
                "total_analyzed": len(self.ai_analyses),
                "ai_enabled": False,
                "category_distribution": {},
                "average_confidence": 0.0,
                "average_quality": 0.0,
                "sentiment_distribution": {},
            }

        try:
            return self.prompt_engineer.get_category_statistics(self.ai_analyses)
        except Exception as e:
            logger.error(f"Error getting AI statistics: {e}")
            return {
                "message": f"Error retrieving statistics: {e}",
                "total_analyzed": len(self.ai_analyses),
                "ai_enabled": True,
                "category_distribution": {},
                "average_confidence": 0.0,
                "average_quality": 0.0,
                "sentiment_distribution": {},
            }

    def get_enhanced_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics including both basic and AI metrics.

        Returns:
            Enhanced statistics dictionary
        """
        # Get basic statistics
        basic_stats = super().get_statistics()

        # Add AI statistics if available
        if self.enable_ai_analysis and self.ai_analyses:
            ai_stats = self.get_ai_statistics()

            # Combine statistics
            enhanced_stats = {
                **basic_stats,
                "ai_analysis": ai_stats,
                "ai_enabled": True,
                "total_ai_analyses": len(self.ai_analyses),
            }

            # Add quality metrics
            if self.ai_analyses:
                quality_scores = [
                    analysis.quality_score for analysis in self.ai_analyses
                ]
                confidence_scores = [
                    analysis.confidence for analysis in self.ai_analyses
                ]

                enhanced_stats["quality_metrics"] = {
                    "average_quality": sum(quality_scores) / len(quality_scores),
                    "average_confidence": sum(confidence_scores)
                    / len(confidence_scores),
                    "high_quality_content": sum(
                        1 for score in quality_scores if score > 0.7
                    ),
                    "high_confidence_predictions": sum(
                        1 for score in confidence_scores if score > 0.8
                    ),
                }

            return enhanced_stats
        else:
            return {**basic_stats, "ai_enabled": False}

    def export_ai_insights_report(self, export_dir: Optional[Path] = None) -> str:
        """
        Generate and export a detailed AI insights report.

        Args:
            export_dir: Optional export directory

        Returns:
            Path to insights report
        """
        if not self.enable_ai_analysis or not self.ai_analyses:
            logger.warning("No AI analysis data available for insights report")
            return ""

        # Create export directory if not provided
        if export_dir is None:
            export_dir = self._create_export_directory()

        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_insights_report_{timestamp}.md"

        # Create full file path in reports subdirectory
        reports_dir = export_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        file_path = reports_dir / filename

        # Get statistics
        ai_stats = self.get_ai_statistics()

        # Generate report content
        report_content = f"""# 🤖 AI-Enhanced Web Scraping Insights Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total URLs Analyzed:** {ai_stats.get('total_analyzed', 0)}
**AI Analysis Enabled:** ✅

## 🎯 Category Analysis

"""

        # Add category distribution
        category_dist = ai_stats.get("category_distribution", {})
        total_analyzed = ai_stats.get("total_analyzed", 1)

        for category, count in category_dist.items():
            percentage = (count / total_analyzed) * 100
            report_content += f"- **{category}:** {count} items ({percentage:.1f}%)\n"

        report_content += f"""

## 📊 Quality Metrics

- **Average Confidence:** {ai_stats.get('average_confidence', 0):.3f}
- **Average Quality Score:** {ai_stats.get('average_quality', 0):.3f}
- **High Confidence Items:** {ai_stats.get('high_confidence_items', 0)}
- **Low Confidence Items:** {ai_stats.get('low_confidence_items', 0)}

## 😊 Sentiment Analysis

"""

        # Add sentiment distribution
        sentiment_dist = ai_stats.get("sentiment_distribution", {})
        for sentiment, count in sentiment_dist.items():
            percentage = (count / total_analyzed) * 100
            emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}.get(
                sentiment, "🤔"
            )
            report_content += f"- **{emoji} {sentiment.title()}:** {count} items ({percentage:.1f}%)\n"

        report_content += """

---
*Generated by AI-Enhanced Intelligent Web Scraper with OpenAI GPT-4*
"""

        # Write report to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        logger.info(f"AI insights report generated: {file_path}")
        return str(file_path)

    def export_all_enhanced(
        self, base_filename: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Export all data with AI enhancements in multiple formats.

        Args:
            base_filename: Optional base filename

        Returns:
            Dictionary with paths to all exported files
        """
        # Get basic exports
        export_paths = super().export_all(base_filename)

        # Add AI-specific exports if available
        if self.enable_ai_analysis and self.ai_analyses:
            try:
                # Create AI insights report
                export_dir = Path(
                    export_paths["json"]
                ).parent.parent  # Go up to date directory
                insights_path = self.export_ai_insights_report(export_dir)
                export_paths["ai_insights"] = insights_path

                logger.info("AI-enhanced exports completed successfully")

            except Exception as e:
                logger.error(f"Failed to create AI-enhanced exports: {e}")

        return export_paths


# Example usage and testing
if __name__ == "__main__":
    # Create enhanced scraper instance
    scraper_config = WebScraperConfig(delay_min=0.5, delay_max=1.5)
    prompt_config = PromptConfig(
        model=config.Config.OPENAI_MODEL, temperature=config.Config.OPENAI_TEMPERATURE
    )  # Fixed model name

    scraper = AIEnhancedWebScraper(
        scraper_config=scraper_config,
        prompt_config=prompt_config,
        enable_ai_analysis=True,
    )

    # Test URLs from different categories
    test_urls = [
        "https://go.dev/doc/",
        "https://go.dev/doc/tutorial/getting-started",
    ]

    print("🤖 AI-Enhanced Intelligent Web Scraper")
    print("=" * 50)

    # Scrape test URLs
    results = scraper.scrape_multiple_urls(test_urls)

    # Show enhanced statistics
    stats = scraper.get_enhanced_statistics()
    print("\n📊 Enhanced Scraping Statistics:")
    print(json.dumps(stats, indent=2))

    # Export data with AI enhancements
    print("\n💾 Exporting enhanced data...")
    export_paths = scraper.export_all_enhanced()

    print("\n📁 Enhanced data exported:")
    for export_type, file_path in export_paths.items():
        file_path_obj = Path(file_path)
        try:
            relative_path = file_path_obj.relative_to(Path.cwd())
        except ValueError:
            relative_path = file_path_obj
        print(f"  - {export_type.upper()}: {relative_path}")

    print("\n🚀 AI-enhanced scraping completed!")
    if scraper.enable_ai_analysis:
        print(f"   🤖 AI analyses: {len(scraper.ai_analyses)}")
        print("   📋 Check the AI insights report for detailed analysis!")
    else:
        print("   ⚠️  AI analysis was disabled or failed to initialize")
