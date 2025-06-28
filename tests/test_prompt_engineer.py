"""
Test suite for the prompt_engineer module.

Tests OpenAI prompt engineering functionality including categorization,
content analysis, and sentiment scoring.
"""

from typing import List, Optional, Tuple
from unittest.mock import Mock, patch

import pytest

from src.prompt_engineer import (
    CategoryDefinition,
    ContentAnalysis,
    PromptConfig,
    PromptEngineer,
)


class TestPromptConfig:
    """Test cases for PromptConfig dataclass."""

    def test_prompt_config_defaults(self):
        """Test PromptConfig default values."""
        config = PromptConfig()

        assert config.model == "gpt-4.1-nano"
        assert config.max_tokens == 1000
        assert config.temperature == 0.7
        assert config.top_p == 0.9
        assert config.frequency_penalty == 0.0
        assert config.presence_penalty == 0.0

    def test_prompt_config_custom_values(self):
        """Test PromptConfig with custom values."""
        config = PromptConfig(
            model="gpt-4.1-nano", max_tokens=500, temperature=0.5, top_p=0.8
        )

        assert config.model == "gpt-4.1-nano"
        assert config.max_tokens == 500
        assert config.temperature == 0.5
        assert config.top_p == 0.8


class TestContentAnalysis:
    """Test cases for ContentAnalysis dataclass."""

    def test_content_analysis_creation(self):
        """Test ContentAnalysis creation."""
        analysis = ContentAnalysis(
            category="Technical",
            confidence=0.95,
            reasoning="Strong technical indicators found",
            keywords=["code", "api", "programming"],
            sentiment="neutral",
            quality_score=0.85,
            metadata={"domain_analysis": "tech blog"},
        )

        assert analysis.category == "Technical"
        assert analysis.confidence == 0.95
        assert analysis.reasoning == "Strong technical indicators found"
        assert analysis.keywords == ["code", "api", "programming"]
        assert analysis.sentiment == "neutral"
        assert analysis.quality_score == 0.85
        assert analysis.metadata["domain_analysis"] == "tech blog"


class TestCategoryDefinition:
    """Test cases for CategoryDefinition dataclass."""

    def test_category_definition_creation(self):
        """Test CategoryDefinition creation."""
        category = CategoryDefinition(
            name="E-commerce",
            description="Online shopping and product sales",
            indicators=["buy", "cart", "price", "product"],
            examples=["Amazon product page", "Online store"],
        )

        assert category.name == "E-commerce"
        assert category.description == "Online shopping and product sales"
        assert "buy" in category.indicators
        assert "Amazon product page" in category.examples


class TestPromptEngineer:
    """Test cases for PromptEngineer class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.config = PromptConfig(model="gpt-4.1-nano", temperature=0.1)

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_prompt_engineer_initialization_success(self, mock_getenv, mock_openai):
        """Test successful PromptEngineer initialization."""
        mock_getenv.return_value = "test-api-key"
        mock_openai.return_value = self.mock_client

        engineer = PromptEngineer(self.config)

        assert engineer.config == self.config
        assert engineer.client == self.mock_client
        assert len(engineer.categories) == 8  # Expected number of categories
        mock_openai.assert_called_once_with(api_key="test-api-key")

    @patch("src.prompt_engineer.os.getenv")
    def test_prompt_engineer_initialization_no_api_key(self, mock_getenv):
        """Test PromptEngineer initialization fails without API key."""
        mock_getenv.return_value = None

        with pytest.raises(
            ValueError, match="OPENAI_API_KEY environment variable is required"
        ):
            PromptEngineer(self.config)

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_initialize_categories(self, mock_getenv, mock_openai):
        """Test category initialization."""
        mock_getenv.return_value = "test-api-key"
        mock_openai.return_value = self.mock_client

        engineer = PromptEngineer(self.config)
        categories = engineer._initialize_categories()

        # Check all expected categories are present
        category_names = [cat.name for cat in categories]
        expected_categories = [
            "E-commerce",
            "News/Blog",
            "Technical",
            "Social Media",
            "Reference",
            "Business",
            "Entertainment",
            "General",
        ]

        for expected in expected_categories:
            assert expected in category_names

        # Check category structure
        ecommerce_cat = next(cat for cat in categories if cat.name == "E-commerce")
        assert "price" in ecommerce_cat.indicators
        assert len(ecommerce_cat.examples) > 0

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_build_categorization_prompt(self, mock_getenv, mock_openai):
        """Test categorization prompt building."""
        mock_getenv.return_value = "test-api-key"
        mock_openai.return_value = self.mock_client

        engineer = PromptEngineer(self.config)

        url = "https://shop.example.com/products"
        title = "Premium Products Store"
        content = "Buy our amazing products with great prices and fast shipping."

        prompt = engineer._build_categorization_prompt(url, title, content)

        # Check prompt structure
        assert "# Role & Objective" in prompt
        assert "Content Categorization Specialist" in prompt
        assert "# Instructions" in prompt
        assert "# Reasoning Steps" in prompt
        assert "# Output Format" in prompt
        assert "# Content to Analyze" in prompt

        # Check content is included
        assert url in prompt
        assert title in prompt
        assert content[:2000] in prompt

        # Check JSON format specification
        assert "```json" in prompt
        assert '"category":' in prompt
        assert '"confidence":' in prompt

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_categorize_content_success(self, mock_getenv, mock_openai):
        """Test successful content categorization."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client

        # Mock OpenAI response
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = """```json
        {
            "category": "E-commerce",
            "confidence": 0.95,
            "reasoning": "Contains shopping keywords and product references",
            "keywords": ["buy", "product", "price", "cart"],
            "sentiment": "positive",
            "quality_score": 0.85,
            "metadata": {
                "primary_indicators": ["buy", "product"],
                "secondary_signals": ["price", "shopping"],
                "domain_analysis": "commercial website"
            }
        }
        ```"""
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        engineer = PromptEngineer(self.config)

        result = engineer.categorize_content(
            url="https://shop.example.com",
            title="Online Store",
            content="Buy products online with great prices and fast shipping.",
        )

        assert isinstance(result, ContentAnalysis)
        assert result.category == "E-commerce"
        assert result.confidence == 0.95
        assert result.reasoning == "Contains shopping keywords and product references"
        assert "buy" in result.keywords
        assert result.sentiment == "positive"
        assert result.quality_score == 0.85
        assert result.metadata["domain_analysis"] == "commercial website"

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_categorize_content_json_error(self, mock_getenv, mock_openai):
        """Test content categorization with JSON parsing error."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client

        # Mock invalid JSON response
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Invalid JSON response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        engineer = PromptEngineer(self.config)

        result = engineer.categorize_content(
            url="https://example.com", title="Test", content="Test content"
        )

        # Should return fallback analysis
        assert isinstance(result, ContentAnalysis)
        assert result.category in ["E-commerce", "News/Blog", "Technical", "General"]
        assert result.confidence == 0.3  # Low confidence for fallback
        assert result.metadata.get("fallback") is True

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_categorize_content_api_error(self, mock_getenv, mock_openai):
        """Test content categorization with API error."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client

        # Mock API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        engineer = PromptEngineer(self.config)

        result = engineer.categorize_content(
            url="https://example.com", title="Test", content="Test content"
        )

        # Should return fallback analysis
        assert isinstance(result, ContentAnalysis)
        assert result.metadata.get("ai_failure") is True

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_enhance_content_analysis_success(self, mock_getenv, mock_openai):
        """Test successful content enhancement analysis."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client

        # Mock OpenAI response
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = """```json
        {
            "summary": "Article about machine learning applications",
            "key_points": ["AI algorithms", "Data processing", "Model training"],
            "entities": {
                "people": ["John Doe"],
                "organizations": ["TechCorp"],
                "locations": ["Silicon Valley"],
                "dates": ["2024"]
            },
            "action_items": ["Implement ML pipeline", "Train model"],
            "data_quality": {
                "completeness": 0.9,
                "accuracy_confidence": 0.85,
                "freshness": "recent"
            },
            "category_specific": {
                "technologies": ["Python", "TensorFlow"],
                "code_snippets": [],
                "apis": ["REST API"],
                "difficulty": "intermediate"
            }
        }
        ```"""
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        engineer = PromptEngineer(self.config)

        result = engineer.enhance_content_analysis(
            content="Machine learning article content...", category="Technical"
        )

        assert result["summary"] == "Article about machine learning applications"
        assert "AI algorithms" in result["key_points"]
        assert result["entities"]["people"] == ["John Doe"]
        assert result["data_quality"]["completeness"] == 0.9
        assert "Python" in result["category_specific"]["technologies"]

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_create_fallback_analysis(self, mock_getenv, mock_openai):
        """Test fallback analysis creation."""
        mock_getenv.return_value = "test-api-key"
        mock_openai.return_value = self.mock_client

        engineer = PromptEngineer(self.config)

        # Test e-commerce detection
        result = engineer._create_fallback_analysis(
            url="https://shop.example.com",
            title="Buy Products",
            content="Shop now and buy amazing products with great prices",
        )

        assert result.category == "E-commerce"
        assert result.confidence == 0.3
        assert result.metadata["fallback"] is True

        # Test technical content detection
        result = engineer._create_fallback_analysis(
            url="https://github.com/user/repo",
            title="Code Repository",
            content="API documentation and code examples",
        )

        assert result.category == "Technical"

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_analyze_batch_content(self, mock_getenv, mock_openai):
        """Test batch content analysis."""
        mock_getenv.return_value = "test-api-key"
        mock_client = Mock()
        mock_openai.return_value = mock_client

        # Mock successful response
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = """```json
        {
            "category": "General",
            "confidence": 0.7,
            "reasoning": "Generic content",
            "keywords": ["test"],
            "sentiment": "neutral",
            "quality_score": 0.6,
            "metadata": {}
        }
        ```"""
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        engineer = PromptEngineer(self.config)

        content_items: List[Tuple[str, Optional[str], Optional[str]]] = [
            ("https://example1.com", "Title 1", "Content 1"),
            ("https://example2.com", "Title 2", "Content 2"),
            ("https://example3.com", "Title 3", "Content 3"),
        ]

        results = engineer.analyze_batch_content(content_items)

        assert len(results) == 3
        for result in results:
            assert isinstance(result, ContentAnalysis)
            assert result.category == "General"

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_get_category_statistics(self, mock_getenv, mock_openai):
        """Test category statistics generation."""
        mock_getenv.return_value = "test-api-key"
        mock_openai.return_value = self.mock_client

        engineer = PromptEngineer(self.config)

        # Create test analyses
        analyses = [
            ContentAnalysis("E-commerce", 0.9, "reason1", ["buy"], "positive", 0.8, {}),
            ContentAnalysis(
                "E-commerce", 0.8, "reason2", ["shop"], "positive", 0.7, {}
            ),
            ContentAnalysis("Technical", 0.95, "reason3", ["code"], "neutral", 0.9, {}),
            ContentAnalysis("News/Blog", 0.7, "reason4", ["news"], "negative", 0.6, {}),
        ]

        stats = engineer.get_category_statistics(analyses)

        assert stats["total_analyzed"] == 4
        assert stats["category_distribution"]["E-commerce"] == 2
        assert stats["category_distribution"]["Technical"] == 1
        assert stats["category_distribution"]["News/Blog"] == 1
        assert stats["average_confidence"] == 0.838  # (0.9 + 0.8 + 0.95 + 0.7) / 4
        assert stats["average_quality"] == 0.75  # (0.8 + 0.7 + 0.9 + 0.6) / 4
        assert stats["sentiment_distribution"]["positive"] == 2
        assert stats["sentiment_distribution"]["neutral"] == 1
        assert stats["sentiment_distribution"]["negative"] == 1
        assert stats["high_confidence_items"] == 2  # > 0.8 (0.9, 0.95)
        assert stats["low_confidence_items"] == 0  # < 0.5 (none)

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_get_category_focus(self, mock_getenv, mock_openai):
        """Test category-specific focus instructions."""
        mock_getenv.return_value = "test-api-key"
        mock_openai.return_value = self.mock_client

        engineer = PromptEngineer(self.config)

        # Test different categories
        ecommerce_focus = engineer._get_category_focus("E-commerce")
        assert "Product details" in ecommerce_focus
        assert "pricing" in ecommerce_focus

        technical_focus = engineer._get_category_focus("Technical")
        assert "Code examples" in technical_focus
        assert "API endpoints" in technical_focus

        unknown_focus = engineer._get_category_focus("Unknown")
        assert "General content analysis" in unknown_focus

    @patch("src.prompt_engineer.openai.OpenAI")
    @patch("src.prompt_engineer.os.getenv")
    def test_get_category_specific_fields(self, mock_getenv, mock_openai):
        """Test category-specific field definitions."""
        mock_getenv.return_value = "test-api-key"
        mock_openai.return_value = self.mock_client

        engineer = PromptEngineer(self.config)

        # Test e-commerce fields
        ecommerce_fields = engineer._get_category_specific_fields("E-commerce")
        assert '"products":' in ecommerce_fields
        assert '"prices":' in ecommerce_fields

        # Test technical fields
        technical_fields = engineer._get_category_specific_fields("Technical")
        assert '"technologies":' in technical_fields
        assert '"code_snippets":' in technical_fields

        # Test unknown category
        unknown_fields = engineer._get_category_specific_fields("Unknown")
        assert '"content_type":' in unknown_fields


@pytest.mark.integration
class TestPromptEngineerIntegration:
    """Integration tests for PromptEngineer."""

    @pytest.mark.skip(reason="Integration tests require manual setup")
    def test_real_openai_integration(self):
        """Test with real OpenAI API (requires valid API key)."""
        # This test requires a real API key and should be run manually
        # when testing with actual OpenAI services
        pass

    def test_prompt_engineer_with_various_content_types(self):
        """Test prompt engineer with different types of content."""
        # This would be implemented as a comprehensive integration test
        # testing various content types and ensuring consistent categorization
        pass


# Test fixtures for PromptEngineer tests
@pytest.fixture
def sample_openai_response():
    """Sample OpenAI API response for testing."""
    return {
        "category": "Technical",
        "confidence": 0.92,
        "reasoning": "Content contains programming terminology and code examples",
        "keywords": ["python", "api", "programming", "development"],
        "sentiment": "neutral",
        "quality_score": 0.85,
        "metadata": {
            "primary_indicators": ["code", "api"],
            "secondary_signals": ["programming", "python"],
            "domain_analysis": "technical blog",
        },
    }


@pytest.fixture
def sample_content_analysis():
    """Sample ContentAnalysis for testing."""
    return ContentAnalysis(
        category="Technical",
        confidence=0.92,
        reasoning="Content contains programming terminology",
        keywords=["python", "api", "programming"],
        sentiment="neutral",
        quality_score=0.85,
        metadata={"domain_analysis": "technical blog"},
    )
