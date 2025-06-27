Prefer using NumPy for numerical computations.
Use vectorized operations instead of loops where possible.
Import NumPy using the alias 'np'.
Include comments explaining complex mathematical operations.<!-- filepath: z:\code-python\webscraper\.github\rules\numpy.instructions.md -->

# NumPy Style Guide - Quick Reference

## Introduction

Essential NumPy coding conventions for numerical computing in Python projects. These guidelines optimize performance, readability, and maintainability when working with numerical data.

**Key Principle**: Vectorization over loops - leverage NumPy's optimized C implementations for better performance.

## Import Conventions

### Standard Imports

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, optimize
```

### Avoid Star Imports

- Use `import numpy as np` - never `from numpy import *`
- Keeps namespace clean and code readable

## Array Creation

### Prefer Specific Constructors

```python
# Correct - explicit and efficient
zeros_arr = np.zeros((10, 10))
ones_arr = np.ones(100)
range_arr = np.arange(0, 10, 0.1)
linspace_arr = np.linspace(0, 1, 50)

# Less optimal
empty_arr = np.array([0] * 100)  # Slower than np.zeros()
```

### Specify Data Types

```python
# Memory efficient and precise
int_arr = np.array([1, 2, 3], dtype=np.int32)
float_arr = np.array([1.0, 2.0], dtype=np.float64)
bool_arr = np.array([True, False], dtype=np.bool_)
```

## Vectorization Best Practices

### Use Vectorized Operations

```python
# Correct - vectorized (fast)
arr = np.array([1, 2, 3, 4, 5])
result = arr * 2 + 1

# Wrong - explicit loops (slow)
result = [x * 2 + 1 for x in arr]
```

### Leverage Broadcasting

```python
# Broadcasting for different shaped arrays
matrix = np.random.rand(100, 10)
row_means = np.mean(matrix, axis=0)  # Shape: (10,)
centered = matrix - row_means        # Broadcasting (100,10) - (10,)
```

## Array Indexing

### Boolean Indexing

```python
arr = np.array([1, -2, 3, -4, 5])
positive = arr[arr > 0]              # Preferred
negative_mask = arr < 0
arr[negative_mask] = 0
```

### Advanced Indexing

```python
# Use fancy indexing appropriately
data = np.random.rand(1000, 5)
indices = [0, 2, 4]
selected_cols = data[:, indices]     # Select specific columns
```

## Performance Optimization

### Avoid Unnecessary Copies

```python
# Creates view (fast, shares memory)
view = arr[::2]
slice_view = arr[1:4]

# Creates copy (slower, new memory)
copy = arr.copy()
fancy_copy = arr[[0, 2, 4]]         # Fancy indexing creates copy
```

### Use In-Place Operations

```python
# In-place operations (memory efficient)
arr += 1                            # Instead of arr = arr + 1
arr *= 2                            # Instead of arr = arr * 2
np.sqrt(arr, out=arr)              # In-place square root
```

## Mathematical Operations

### Use NumPy Functions

```python
# Correct - NumPy functions (vectorized)
sqrt_arr = np.sqrt(arr)
max_val = np.max(arr)
sum_val = np.sum(arr)

# Wrong - Python built-ins on arrays
sqrt_arr = [math.sqrt(x) for x in arr]
```

### Axis-Aware Operations

```python
matrix = np.random.rand(100, 50)
row_sums = np.sum(matrix, axis=1)      # Sum across columns
col_means = np.mean(matrix, axis=0)    # Mean of each column
total_sum = np.sum(matrix)             # Sum all elements
```

## Memory Management

### Pre-allocate Arrays

```python
# Correct - pre-allocate
n = 10000
result = np.empty(n)
for i in range(n):
    result[i] = expensive_computation(i)

# Wrong - growing arrays (very slow!)
result = np.array([])
for i in range(n):
    result = np.append(result, expensive_computation(i))
```

### Use Appropriate Data Types

```python
# Choose precision based on needs
prices = np.array(price_list, dtype=np.float32)      # Usually sufficient
counts = np.array(count_list, dtype=np.int32)        # Memory efficient
timestamps = np.array(time_list, dtype=np.int64)     # For large timestamps
```

## Web Scraping Applications

### Data Cleaning

```python
# Clean scraped numerical data
raw_prices = np.array(scraped_price_strings)
numeric_prices = pd.to_numeric(raw_prices, errors='coerce')
clean_prices = numeric_prices[~np.isnan(numeric_prices)]

# Statistical analysis
price_stats = {
    'mean': np.mean(clean_prices),
    'median': np.median(clean_prices),
    'std': np.std(clean_prices),
    'percentiles': np.percentile(clean_prices, [25, 75])
}
```

### Time Series Processing

```python
# Handle time-based scraped data
timestamps = np.array(timestamp_list, dtype='datetime64[s]')
values = np.array(value_list, dtype=np.float64)

# Sort by timestamp
sort_indices = np.argsort(timestamps)
sorted_times = timestamps[sort_indices]
sorted_values = values[sort_indices]
```

## Error Handling

### Input Validation

```python
def process_scraped_data(data):
    """Process numerical data from web scraping."""
    # Convert to numpy array with validation
    arr = np.asarray(data, dtype=np.float64)

    # Check for valid shape
    if arr.ndim != 1:
        raise ValueError("Expected 1D array")

    # Remove infinite values
    finite_mask = np.isfinite(arr)
    return arr[finite_mask]
```

### Handle Missing Data

```python
# Use NaN for missing floating-point data
data = np.array([1.0, 2.0, np.nan, 4.0])
valid_data = data[~np.isnan(data)]

# Use masked arrays for complex patterns
masked_data = np.ma.masked_invalid(data)
result = np.ma.mean(masked_data)
```

## Documentation

### Document Array Shapes

```python
def analyze_price_data(prices: np.ndarray) -> dict:
    """
    Analyze price data from web scraping.

    Parameters
    ----------
    prices : np.ndarray, shape (n,), dtype float
        Array of price values scraped from website

    Returns
    -------
    dict
        Statistical summary with keys: mean, std, min, max
    """
    # Ensure input is proper numpy array
    prices = np.asarray(prices, dtype=np.float64)

    # Remove invalid values (NaN, inf)
    valid_prices = prices[np.isfinite(prices)]

    return {
        'mean': np.mean(valid_prices),
        'std': np.std(valid_prices),
        'min': np.min(valid_prices),
        'max': np.max(valid_prices)
    }
```

### Comment Complex Operations

```python
def normalize_scraped_features(features):
    """Normalize features using z-score normalization."""
    # Calculate mean and std along feature axis (axis=0)
    # Shape: features (n_samples, n_features)
    feature_means = np.mean(features, axis=0, keepdims=True)
    feature_stds = np.std(features, axis=0, keepdims=True)

    # Avoid division by zero for constant features
    feature_stds = np.maximum(feature_stds, np.finfo(float).eps)

    # Broadcasting: (n_samples, n_features) - (1, n_features)
    normalized = (features - feature_means) / feature_stds

    return normalized
```

## Quick Checklist

### Performance

- ✅ Use vectorized operations instead of loops
- ✅ Pre-allocate arrays when size is known
- ✅ Choose appropriate data types (int32 vs int64, float32 vs float64)
- ✅ Use in-place operations when possible
- ✅ Leverage broadcasting for element-wise operations

### Memory Efficiency

- ✅ Understand when operations create views vs copies
- ✅ Use `keepdims=True` for dimension-preserving reductions
- ✅ Avoid repeatedly appending to arrays
- ✅ Use appropriate dtypes for data range

### Code Quality

- ✅ Import numpy as `np`
- ✅ Document array shapes and dtypes in docstrings
- ✅ Validate inputs with `np.asarray()`
- ✅ Handle NaN and infinite values appropriately
- ✅ Use axis parameter for reductions
- ✅ Comment complex mathematical operations

---

\*Prefer using NumPy for numerical computations. Use vectorized operations instead of loops where possible. Import NumPy using the alias 'np'. Include comments
