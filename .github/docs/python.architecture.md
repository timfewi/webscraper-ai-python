# Python Architecture Best Practices

## Project Structure

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── core/
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

## Design Principles

### SOLID Principles
- **Single Responsibility**: Each class/function has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Derived classes must be substitutable for base classes
- **Interface Segregation**: Clients shouldn't depend on unused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

### Clean Architecture
- Separate business logic from framework details
- Use dependency injection
- Implement repository pattern for data access
- Keep external dependencies at the edges

## Code Organization

### Modules and Packages
```python
# Good: Clear module structure
from src.models.user import User
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
```

### Configuration Management
```python
# Use environment variables and config files
import os
from dataclasses import dataclass

@dataclass
class Config:
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
```

## Error Handling

```python
# Custom exceptions
class BusinessLogicError(Exception):
    pass

class ValidationError(BusinessLogicError):
    pass

# Proper error handling
def process_user(user_data):
    try:
        validate_user_data(user_data)
        return create_user(user_data)
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise BusinessLogicError("User processing failed")
```

## Testing Strategy

### Unit Tests
```python
import pytest
from unittest.mock import Mock, patch

def test_user_service_create_user():
    # Arrange
    user_repo = Mock()
    user_service = UserService(user_repo)
    
    # Act
    result = user_service.create_user({"name": "John"})
    
    # Assert
    user_repo.save.assert_called_once()
```

### Integration Tests
- Test component interactions
- Use test databases
- Mock external services

## Performance Considerations

- Use generators for large datasets
- Implement caching strategies
- Profile critical code paths
- Use async/await for I/O operations

## Documentation

- Use docstrings for all public functions
- Follow PEP 257 conventions
- Include type hints
- Maintain README and API docs

## Dependencies

- Pin versions in requirements.txt
- Use virtual environments
- Separate dev/prod dependencies
- Regular security updates