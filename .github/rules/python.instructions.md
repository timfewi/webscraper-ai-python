# PEP 8 Style Guide - Quick Reference

## Introduction

This document provides essential coding conventions for Python code. These guidelines improve code readability and consistency across Python projects.

**Key Principle**: Code is read much more often than it is written - prioritize readability.

## Code Layout

### Indentation
- Use 4 spaces per indentation level
- Never mix tabs and spaces
- Continuation lines should align vertically or use hanging indent

### Line Length
- Limit lines to 79 characters maximum
- Docstrings/comments limited to 72 characters
- Use parentheses for line continuation (preferred over backslashes)

### Blank Lines
- 2 blank lines around top-level function and class definitions
- 1 blank line around method definitions inside classes
- Use blank lines sparingly within functions to separate logical sections

### Imports
- Put imports at top of file after module docstring
- Group imports: standard library → third party → local application
- One import per line (except `from module import name1, name2`)
- Use absolute imports when possible

```python
import os
import sys

import requests
from bs4 import BeautifulSoup

from mypackage import mymodule
```

## Whitespace

### Avoid Extra Whitespace
- Inside parentheses: `spam(ham[1], {eggs: 2})`
- Before commas/semicolons: `if x == 4: print(x, y)`
- Before function call parentheses: `spam(1)`

### Use Single Spaces Around
- Assignment operators: `x = 1`
- Comparisons: `x == y`, `x < y`, `x is None`
- Booleans: `x and y`

### Function Arguments
- No spaces around `=` for keyword arguments: `func(arg=value)`
- Spaces around `=` for annotated defaults: `func(arg: str = 'default')`

## String Quotes
- Be consistent with single or double quotes
- Use triple double quotes for docstrings: `"""Docstring"""`

## Comments and Docstrings
- Comments should be complete sentences
- Block comments start with `#` and single space
- Inline comments separated by at least 2 spaces
- Write docstrings for all public modules, functions, classes, methods

## Naming Conventions

### Styles
- `lowercase` or `lower_case_with_underscores` - functions, variables, modules
- `UPPER_CASE_WITH_UNDERSCORES` - constants
- `CapWords` - classes, exceptions (add "Error" suffix for exceptions)
- `_single_leading_underscore` - internal use
- `__double_leading_underscore` - name mangling in classes

### Specific Rules
- Function/variable names: `function_name`, `variable_name`
- Class names: `ClassName`
- Constants: `MAX_SIZE`, `DEFAULT_TIMEOUT`
- Methods: always use `self` for instance, `cls` for class methods
- Avoid single characters: `l`, `O`, `I` (look like numbers)

## Programming Recommendations

### Comparisons
- Use `is`/`is not` for singletons like `None`: `if x is not None:`
- Use `isinstance()` instead of `type()`: `isinstance(obj, str)`

### Sequences
- Use truthiness for empty sequences: `if not seq:` instead of `if len(seq) == 0:`

### Exception Handling
- Be specific with exceptions: `except ValueError:` not bare `except:`
- Use `try` blocks for minimal code only
- Derive custom exceptions from `Exception`

### Functions
- Use `def` statements, not lambda assignments
- Be consistent with return statements (all return values or all return None)

### Best Practices
- Use `''.startswith()` and `''.endswith()` for string prefixes/suffixes
- Use context managers (`with` statements) for resource management
- Don't compare booleans with `==`: use `if flag:` not `if flag == True:`

## Type Hints (Modern Python)
- Use type hints for function parameters and return values
- Format: `def function(param: str) -> int:`
- Space after colon, spaces around arrow: ` -> `

## Quick Checklist
- ✅ 4-space indentation, no tabs
- ✅ Lines ≤ 79 characters
- ✅ Proper import grouping and placement
- ✅ Consistent string quote style
- ✅ Descriptive variable/function names in snake_case
- ✅ Class names in CapWords
- ✅ Constants in UPPER_CASE
- ✅ Docstrings for public APIs
- ✅ Specific exception handling
- ✅ Type hints where helpful

---

*This is a condensed version of PEP 8. For complete details, see the full specification.*