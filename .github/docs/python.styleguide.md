# Python Style Guide

This document outlines coding standards and best practices for Python development to ensure consistency, readability, and maintainability.

## Code Formatting

### PEP 8 Compliance
- Follow [PEP 8](https://peps.python.org/pep-0008/) as the baseline style guide
- Use tools like `black`, `flake8`, or `ruff` for automatic formatting and linting

### Line Length
- Maximum line length: 88 characters (Black's default)
- Break long lines using parentheses, not backslashes

### Indentation
- Use 4 spaces per indentation level
- Never mix tabs and spaces

### Imports
- Group imports in this order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library imports
- Use absolute imports when possible
- One import per line for `from` imports

```python
# Good
import os
import sys

import requests
from django.conf import settings

from .models import User
from .utils import helper_function
```

## Naming Conventions

### Variables and Functions
- Use `snake_case` for variables and functions
- Use descriptive names that explain purpose

```python
# Good
user_count = get_active_users()
calculate_monthly_revenue()

# Avoid
n = get_users()
calc()
```

### Classes
- Use `PascalCase` for class names
- Use nouns that describe what the class represents

```python
class UserManager:
    pass

class DatabaseConnection:
    pass
```

### Constants
- Use `UPPER_SNAKE_CASE` for constants
- Define at module level

```python
MAX_RETRY_ATTEMPTS = 3
DATABASE_URL = "postgresql://localhost/mydb"
```

### Private Members
- Use single leading underscore for internal use
- Use double leading underscore for name mangling (rare cases)

```python
class MyClass:
    def __init__(self):
        self.public_attr = "public"
        self._internal_attr = "internal"
        self.__private_attr = "private"
```

## Documentation

### Docstrings
- Use triple quotes for all docstrings
- Follow Google or NumPy docstring conventions
- Document all public functions, classes, and modules

```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculate the discounted price.

    Args:
        price: The original price of the item.
        discount_rate: The discount rate as a decimal (0.1 for 10%).

    Returns:
        The discounted price.

    Raises:
        ValueError: If price is negative or discount_rate is not between 0 and 1.
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")

    return price * (1 - discount_rate)
```

### Comments
- Use comments sparingly to explain "why", not "what"
- Keep comments up-to-date with code changes
- Use TODO comments for temporary code

```python
# TODO: Optimize this query for better performance
# We use a simple linear search here because the dataset is small,
# but this should be replaced with a hash lookup for larger datasets
```

## Type Hints

### Always Use Type Hints
- Add type hints to all function signatures
- Use type hints for class attributes when not obvious
- Import types from `typing` module when needed

```python
from typing import List, Dict, Optional, Union

def process_users(users: List[Dict[str, str]]) -> Optional[str]:
    """Process a list of user dictionaries."""
    if not users:
        return None
    return users[0].get("name")

class UserService:
    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
        self.cache: Dict[str, Any] = {}
```

## Error Handling

### Exception Handling
- Be specific with exception types
- Always handle exceptions at the appropriate level
- Use `finally` blocks for cleanup when necessary

```python
# Good
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logger.error(f"Failed to fetch data from {url}: {e}")
    raise

# Avoid
try:
    response = requests.get(url)
except:  # Too broad
    pass  # Silent failure
```

### Custom Exceptions
- Create custom exceptions for domain-specific errors
- Inherit from appropriate built-in exceptions

```python
class ValidationError(ValueError):
    """Raised when data validation fails."""
    pass

class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    pass
```

## Code Organization

### Function Design
- Keep functions small and focused (single responsibility)
- Limit function parameters (max 5-7 parameters)
- Return early to reduce nesting

```python
def validate_user_data(user_data: Dict[str, Any]) -> None:
    """Validate user data dictionary."""
    if not user_data:
        raise ValidationError("User data cannot be empty")

    if "email" not in user_data:
        raise ValidationError("Email is required")

    if not is_valid_email(user_data["email"]):
        raise ValidationError("Invalid email format")
```

### Class Design
- Follow single responsibility principle
- Use composition over inheritance when possible
- Implement `__str__` and `__repr__` methods for debugging

```python
class User:
    def __init__(self, email: str, name: str) -> None:
        self.email = email
        self.name = name

    def __str__(self) -> str:
        return f"User(name={self.name})"

    def __repr__(self) -> str:
        return f"User(email={self.email!r}, name={self.name!r})"
```

## Best Practices

### General Guidelines
1. **DRY (Don't Repeat Yourself)**: Extract common code into functions or classes
2. **KISS (Keep It Simple, Stupid)**: Prefer simple solutions over complex ones
3. **YAGNI (You Aren't Gonna Need It)**: Don't add functionality until it's needed
4. **Use context managers**: Always use `with` statements for file operations and resource management
5. **Validate inputs**: Check function parameters and raise appropriate exceptions
6. **Use logging**: Replace print statements with proper logging
7. **Test your code**: Write unit tests for all public functions

### Performance Considerations
- Use list comprehensions and generator expressions when appropriate
- Prefer `enumerate()` over manual indexing
- Use `dict.get()` instead of checking key existence
- Consider using `dataclasses` for simple data containers

```python
# Good
active_users = [user for user in users if user.is_active]
for index, item in enumerate(items):
    process_item(index, item)

value = config.get("setting", default_value)

@dataclass
class Point:
    x: float
    y: float
```

### Security
- Never commit secrets or API keys to version control
- Use environment variables for configuration
- Validate and sanitize all user inputs
- Use parameterized queries for database operations

## Tools and Automation

### Recommended Tools
- **Formatter**: `black` for code formatting
- **Linter**: `ruff` or `flake8` for code quality
- **Type Checker**: `mypy` for static type checking
- **Import Sorting**: `isort` for organizing imports
- **Security**: `bandit` for security linting

### Pre-commit Hooks
Set up pre-commit hooks to automatically run these tools before each commit.

## Conclusion

Following these guidelines will lead to:
- More readable and maintainable code
- Easier collaboration with team members
- Fewer bugs and easier debugging
- Better development experience overall

Remember: Consistency is key. When in doubt, prioritize readability and maintainability over cleverness.
