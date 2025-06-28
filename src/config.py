"""
Configuration management for the webscraper project.

Handles environment variables and API key management.
"""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for application settings."""

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_ORG_ID: Optional[str] = os.getenv("OPENAI_ORG_ID")

    # Web Scraping Configuration
    DEFAULT_USER_AGENT: str = os.getenv(
        "USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    DEFAULT_DELAY_MIN: float = float(os.getenv("DEFAULT_DELAY_MIN", "1.0"))
    DEFAULT_DELAY_MAX: float = float(os.getenv("DEFAULT_DELAY_MAX", "3.0"))
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30"))

    @classmethod
    def get_openai_api_key(cls) -> str:
        """
        Get OpenAI API key with validation.

        Returns:
            OpenAI API key

        Raises:
            ValueError: If API key is not set
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file."
            )
        return cls.OPENAI_API_KEY

    @classmethod
    def validate_required_env_vars(cls) -> None:
        """
        Validate that all required environment variables are set.

        Raises:
            ValueError: If required environment variables are missing
        """
        missing_vars = []

        if not cls.OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Please check your .env file."
            )
