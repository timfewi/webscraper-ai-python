"""
OpenAI Prompt Engineering Module for Intelligent Web Scraping.

This module implements advanced prompt engineering techniques to enhance
the AI-powered categorization and content analysis capabilities.
"""

from dataclasses import dataclass
import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
import openai

from . import config

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class PromptConfig:
    """Configuration for OpenAI prompt engineering."""

    model: str = config.Config.OPENAI_MODEL
    max_tokens: int = config.Config.OPENAI_MAX_TOKENS
    temperature: float = config.Config.OPENAI_TEMPERATURE
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


@dataclass
class ContentAnalysis:
    """Structured result from AI content analysis."""

    category: str
    confidence: float
    reasoning: str
    keywords: List[str]
    sentiment: str
    quality_score: float
    metadata: Dict[str, Any]


@dataclass
class ScrapedContent:
    """Structured representation of scraped web content."""

    url: str
    title: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CategoryDefinition:
    """Definition of content categories for AI classification."""

    name: str
    description: str
    indicators: List[str]
    examples: List[str]


class PromptEngineer:
    """
    Advanced prompt engineering for web scraping AI tasks.

    This class implements modern prompt engineering best practices including:
    - Structured prompting with clear role definitions
    - Chain-of-thought reasoning
    - Few-shot learning examples
    - Output format specification
    - Error handling and validation
    """

    def __init__(self, config: Optional[PromptConfig] = None) -> None:
        """Initialize the prompt engineer with OpenAI configuration."""
        self.config = config or PromptConfig()

        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = openai.OpenAI(api_key=api_key)

        # Define category system
        self.categories = self._initialize_categories()

        logger.info("PromptEngineer initialized with OpenAI client")

    def _initialize_categories(self) -> List[CategoryDefinition]:
        """Initialize the content categorization system."""
        return [
            CategoryDefinition(
                name="E-commerce",
                description="Online shopping, product sales, marketplace websites",
                indicators=[
                    "price",
                    "buy",
                    "cart",
                    "product",
                    "shop",
                    "store",
                    "payment",
                ],
                examples=["Amazon product page", "Online store", "Shopping cart"],
            ),
            CategoryDefinition(
                name="News/Blog",
                description="News articles, blog posts, journalistic content",
                indicators=["article", "news", "blog", "post", "author", "published"],
                examples=["News website", "Personal blog", "Magazine article"],
            ),
            CategoryDefinition(
                name="Technical",
                description="Programming, documentation, technical resources",
                indicators=["code", "api", "documentation", "tutorial", "github"],
                examples=[
                    "API documentation",
                    "Programming tutorial",
                    "Code repository",
                ],
            ),
            CategoryDefinition(
                name="Social Media",
                description="Social networking platforms and user-generated content",
                indicators=["social", "share", "like", "follow", "comment", "post"],
                examples=["Facebook page", "Twitter profile", "LinkedIn post"],
            ),
            CategoryDefinition(
                name="Reference",
                description="Educational content, wikis, reference materials",
                indicators=["wikipedia", "reference", "definition", "encyclopedia"],
                examples=[
                    "Wikipedia article",
                    "Dictionary entry",
                    "Educational resource",
                ],
            ),
            CategoryDefinition(
                name="Business",
                description="Corporate websites, business services, professional content",
                indicators=[
                    "company",
                    "business",
                    "service",
                    "corporate",
                    "professional",
                ],
                examples=["Company homepage", "Business directory", "Service page"],
            ),
            CategoryDefinition(
                name="Entertainment",
                description="Media, games, entertainment content",
                indicators=[
                    "game",
                    "movie",
                    "music",
                    "entertainment",
                    "video",
                    "media",
                ],
                examples=["Movie review", "Game website", "Entertainment news"],
            ),
            CategoryDefinition(
                name="General",
                description="Content that doesn't fit specific categories",
                indicators=[],
                examples=["Generic website", "Mixed content", "Uncategorizable"],
            ),
        ]

    def _build_categorization_prompt(self, url: str, title: str, content: str) -> str:
        """
        Build a comprehensive prompt for content categorization using modern techniques.

        Args:
            url: Website URL
            title: Page title
            content: Page content

        Returns:
            Structured prompt string
        """

        # Create category definitions for the prompt
        category_definitions = "\n".join(
            [
                f"**{cat.name}**: {cat.description}\n"
                f"   Indicators: {', '.join(cat.indicators[:5])}\n"
                f"   Examples: {', '.join(cat.examples[:2])}"
                for cat in self.categories
            ]
        )

        prompt = f"""# Role & Objective
You are a Content Categorization Specialist. Your goal is to accurately classify web content into predefined categories and provide detailed analysis with high confidence and reasoning.

# Instructions
Follow these steps to analyze and categorize the provided web content:

1. **Content Analysis**: Examine the URL, title, and content thoroughly
2. **Category Matching**: Compare content against category definitions below
3. **Confidence Assessment**: Evaluate how certain you are about the classification
4. **Keyword Extraction**: Identify the most relevant keywords
5. **Quality Assessment**: Rate the content quality and usefulness

## Category Definitions
{category_definitions}

# Reasoning Steps
Think step by step:
1. Analyze URL structure and domain patterns
2. Examine title for category indicators
3. Scan content for category-specific keywords and patterns
4. Consider context and overall content theme
5. Assign confidence score based on evidence strength
6. Extract most relevant keywords (5-10 words)
7. Assess content sentiment and quality

# Output Format
Provide your analysis in this exact JSON structure:
```json
{{
    "category": "category_name",
    "confidence": 0.95,
    "reasoning": "Detailed explanation of classification decision",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "sentiment": "positive|neutral|negative",
    "quality_score": 0.85,
    "metadata": {{
        "primary_indicators": ["indicator1", "indicator2"],
        "secondary_signals": ["signal1", "signal2"],
        "domain_analysis": "brief domain assessment"
    }}
}}
```

# Content to Analyze
**URL**: {url}
**Title**: {title or 'No title available'}
**Content Preview**: {content[:2000]}{"..." if len(content) > 2000 else ""}

Analyze this content step by step and provide the JSON response only.
"""

        return prompt

    def _build_content_enhancement_prompt(self, content: str, category: str) -> str:
        """
        Build prompt for enhancing content analysis based on category.

        Args:
            content: Raw content to enhance
            category: Determined category

        Returns:
            Structured prompt for content enhancement
        """

        prompt = f"""# Role & Objective
You are a Content Enhancement Specialist. Your goal is to extract structured, valuable information from web content based on its category type.

# Instructions
Process the provided {category} content and extract relevant structured data:

1. **Key Information Extraction**: Identify the most important facts and data points
2. **Entity Recognition**: Extract names, dates, locations, organizations
3. **Content Summarization**: Create concise summary of main points
4. **Action Items**: Identify any actionable information or next steps
5. **Data Validation**: Verify information consistency and flag any issues

# Category-Specific Focus
For {category} content, pay special attention to:
{self._get_category_focus(category)}

# Reasoning Steps
Think step by step:
1. Identify content structure and main sections
2. Extract category-relevant entities and data
3. Summarize key points in order of importance
4. Identify actionable items or calls-to-action
5. Assess data quality and completeness

# Output Format
Provide enhanced analysis in this JSON structure:
```json
{{
    "summary": "Concise 2-3 sentence summary",
    "key_points": ["point1", "point2", "point3"],
    "entities": {{
        "people": ["person1", "person2"],
        "organizations": ["org1", "org2"],
        "locations": ["location1", "location2"],
        "dates": ["date1", "date2"]
    }},
    "action_items": ["action1", "action2"],
    "data_quality": {{
        "completeness": 0.85,
        "accuracy_confidence": 0.90,
        "freshness": "recent|moderate|outdated"
    }},
    "category_specific": {{
        {self._get_category_specific_fields(category)}
    }}
}}
```

# Content to Enhance
{content[:3000]}{"..." if len(content) > 3000 else ""}

Process this content and provide the enhanced JSON analysis.
"""

        return prompt

    def _get_category_focus(self, category: str) -> str:
        """Get category-specific focus instructions."""
        focus_map = {
            "E-commerce": "Product details, pricing, availability, reviews, specifications",
            "News/Blog": "Headlines, publication dates, authors, sources, key events",
            "Technical": "Code examples, API endpoints, version numbers, dependencies",
            "Social Media": "User engagement, hashtags, mentions, viral content",
            "Reference": "Definitions, citations, accuracy, educational value",
            "Business": "Contact information, services, company details, credentials",
            "Entertainment": "Release dates, ratings, cast/crew, genre information",
            "General": "Main topics, purpose, target audience, key messages",
        }
        return focus_map.get(category, "General content analysis and key information")

    def _get_category_specific_fields(self, category: str) -> str:
        """Get category-specific fields for enhanced analysis."""
        fields_map = {
            "E-commerce": '"products": [], "prices": [], "availability": "", "reviews_summary": ""',
            "News/Blog": '"headline": "", "author": "", "publication_date": "", "sources": []',
            "Technical": '"technologies": [], "code_snippets": [], "apis": [], "difficulty": ""',
            "Social Media": '"platform": "", "engagement_metrics": {}, "trending_topics": []',
            "Reference": '"topic": "", "credibility": "", "citations": [], "educational_level": ""',
            "Business": '"company_name": "", "services": [], "contact_info": {}, "industry": ""',
            "Entertainment": '"title": "", "genre": "", "rating": "", "release_info": ""',
            "General": '"main_topic": "", "target_audience": "", "content_type": ""',
        }
        return fields_map.get(category, '"content_type": "", "main_focus": ""')

    def categorize_content(
        self, url: str, title: Optional[str] = None, content: Optional[str] = None
    ) -> ContentAnalysis:
        """
        Categorize web content using advanced AI analysis.

        Args:
            url: Website URL
            title: Page title
            content: Page content

        Returns:
            ContentAnalysis object with detailed results
        """

        if not content:
            content = "No content available"

        if not title:
            title = "No title available"

        try:
            # Build and execute categorization prompt
            prompt = self._build_categorization_prompt(url, title, content)

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content categorization AI. Always respond with valid JSON only.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
            )

            # Parse response
            response_content = response.choices[0].message.content
            if not response_content:
                raise ValueError("Empty response from OpenAI")

            response_text = response_content.strip()

            # Clean JSON if wrapped in code blocks
            if response_text.startswith("```json"):
                response_text = (
                    response_text.replace("```json", "").replace("```", "").strip()
                )

            result_data = json.loads(response_text)

            # Create ContentAnalysis object
            analysis = ContentAnalysis(
                category=result_data.get("category", "General"),
                confidence=float(result_data.get("confidence", 0.5)),
                reasoning=result_data.get("reasoning", "No reasoning provided"),
                keywords=result_data.get("keywords", []),
                sentiment=result_data.get("sentiment", "neutral"),
                quality_score=float(result_data.get("quality_score", 0.5)),
                metadata=result_data.get("metadata", {}),
            )

            logger.info(
                f"Successfully categorized content: {analysis.category} (confidence: {analysis.confidence})"
            )
            return analysis

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            # Return fallback analysis
            return self._create_fallback_analysis(url, title, content)

        except Exception as e:
            logger.error(f"Error in AI categorization: {e}")
            return self._create_fallback_analysis(url, title, content)

    def enhance_content_analysis(self, content: str, category: str) -> Dict[str, Any]:
        """
        Enhance content analysis with category-specific insights.

        Args:
            content: Content to analyze
            category: Content category

        Returns:
            Dictionary with enhanced analysis
        """

        try:
            prompt = self._build_content_enhancement_prompt(content, category)

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content analyst. Provide detailed structured analysis in valid JSON format only.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.config.max_tokens,
                temperature=0.1,  # Lower temperature for factual analysis
                top_p=0.9,
            )

            response_content = response.choices[0].message.content
            if not response_content:
                raise ValueError("Empty response from OpenAI")

            response_text = response_content.strip()

            # Clean JSON if wrapped in code blocks
            if response_text.startswith("```json"):
                response_text = (
                    response_text.replace("```json", "").replace("```", "").strip()
                )

            enhanced_data = json.loads(response_text)

            # Ensure we return a dictionary as expected
            if isinstance(enhanced_data, dict):
                logger.info(f"Successfully enhanced {category} content analysis")
                return enhanced_data
            else:
                logger.warning(
                    f"Unexpected response format for {category} content analysis"
                )
                return {
                    "summary": "Content analysis unavailable - invalid format",
                    "key_points": [],
                    "entities": {},
                    "action_items": [],
                    "data_quality": {"completeness": 0.0, "accuracy_confidence": 0.0},
                    "category_specific": {},
                }

        except Exception as e:
            logger.error(f"Error in content enhancement: {e}")
            return {
                "summary": "Content analysis unavailable",
                "key_points": [],
                "entities": {},
                "action_items": [],
                "data_quality": {"completeness": 0.0, "accuracy_confidence": 0.0},
                "category_specific": {},
            }

    def _create_fallback_analysis(
        self, url: str, title: Optional[str], content: Optional[str]
    ) -> ContentAnalysis:
        """Create fallback analysis when AI fails."""

        # Simple keyword-based categorization as fallback
        if content:
            content_lower = content.lower()
            url_lower = url.lower()

            # Check for obvious patterns
            if any(
                word in content_lower or word in url_lower
                for word in ["shop", "buy", "price", "cart"]
            ):
                category = "E-commerce"
            elif any(
                word in content_lower or word in url_lower
                for word in ["news", "article", "blog"]
            ):
                category = "News/Blog"
            elif any(
                word in content_lower or word in url_lower
                for word in ["code", "api", "github"]
            ):
                category = "Technical"
            else:
                category = "General"
        else:
            category = "General"

        return ContentAnalysis(
            category=category,
            confidence=0.3,  # Low confidence for fallback
            reasoning="Fallback categorization due to AI analysis failure",
            keywords=[],
            sentiment="neutral",
            quality_score=0.5,
            metadata={"fallback": True, "ai_failure": True},
        )

    def analyze_batch_content(
        self, content_items: List[Tuple[str, Optional[str], Optional[str]]]
    ) -> List[ContentAnalysis]:
        """
        Analyze multiple content items in batch for efficiency.

        Args:
            content_items: List of (url, title, content) tuples

        Returns:
            List of ContentAnalysis objects
        """

        results = []
        total_items = len(content_items)

        logger.info(f"Starting batch analysis of {total_items} items")

        for i, (url, title, content) in enumerate(content_items, 1):
            try:
                analysis = self.categorize_content(url, title, content)
                results.append(analysis)

                # Log progress every 10 items
                if i % 10 == 0:
                    logger.info(f"Batch progress: {i}/{total_items} completed")

            except Exception as e:
                logger.error(f"Failed to analyze item {i}: {e}")
                # Add fallback result
                fallback = self._create_fallback_analysis(url, title, content)
                results.append(fallback)

        logger.info(
            f"Batch analysis completed: {len(results)}/{total_items} successful"
        )
        return results

    def get_category_statistics(
        self, analyses: List[ContentAnalysis]
    ) -> Dict[str, Any]:
        """
        Generate statistics from content analyses.

        Args:
            analyses: List of ContentAnalysis objects

        Returns:
            Statistics dictionary
        """

        if not analyses:
            return {"message": "No analyses provided"}

        # Category distribution
        categories = [analysis.category for analysis in analyses]
        category_counts: Dict[str, int] = {}
        for category in categories:
            category_counts[category] = category_counts.get(category, 0) + 1

        # Confidence statistics
        confidences = [analysis.confidence for analysis in analyses]
        avg_confidence = sum(confidences) / len(confidences)

        # Quality statistics
        quality_scores = [analysis.quality_score for analysis in analyses]
        avg_quality = sum(quality_scores) / len(quality_scores)

        # Sentiment distribution
        sentiments = [analysis.sentiment for analysis in analyses]
        sentiment_counts: Dict[str, int] = {}
        for sentiment in sentiments:
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1

        return {
            "total_analyzed": len(analyses),
            "category_distribution": category_counts,
            "average_confidence": round(avg_confidence, 3),
            "average_quality": round(avg_quality, 3),
            "sentiment_distribution": sentiment_counts,
            "high_confidence_items": sum(1 for c in confidences if c > 0.8),
            "low_confidence_items": sum(1 for c in confidences if c < 0.5),
        }


# Example usage and testing
if __name__ == "__main__":
    # Test the prompt engineer
    engineer = PromptEngineer()

    # Test categorization
    test_url = "https://example.com/blog/post"
    test_title = "How to Build Better Web Applications"
    test_content = """
    This article discusses best practices for building modern web applications.
    We'll cover topics like responsive design, performance optimization,
    and user experience principles. The content includes code examples
    and practical tips for developers.
    """

    print("🤖 Testing AI Prompt Engineering")
    print("=" * 50)

    # Analyze content
    analysis = engineer.categorize_content(test_url, test_title, test_content)

    print(f"Category: {analysis.category}")
    print(f"Confidence: {analysis.confidence}")
    print(f"Reasoning: {analysis.reasoning}")
    print(f"Keywords: {analysis.keywords}")
    print(f"Sentiment: {analysis.sentiment}")
    print(f"Quality Score: {analysis.quality_score}")

    # Test enhancement
    enhanced = engineer.enhance_content_analysis(test_content, analysis.category)
    print("\nEnhanced Analysis:")
    print(json.dumps(enhanced, indent=2))
