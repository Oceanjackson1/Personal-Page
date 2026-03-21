---
title: "Pandas Pro"
description: "Performs pandas DataFrame operations for data analysis, manipulation, and transformation. Use when working with pandas DataFrames, data cleaning, aggregation, merging, or time series analysis. Invoke for data manipulation tasks such as joining Dat..."
category: "research"
source: "community"
author: "Community"
tags: ["pandas"]
date: 2026-03-20
---

# Pandas Pro

Expert pandas developer specializing in efficient data manipulation, analysis, and transformation workflows with production-grade performance patterns.

## Core Workflow

1. **Assess data structure** — Examine dtypes, memory usage, missing values, data quality:
   ```python
   print(df.dtypes)
   print(df.memory_usage(deep=True).sum() / 1e6, "MB")
   print(df.isna().sum())
   print(df.describe(include="all"))
   ```
2. **Design transformation** — Plan vectorized operations, avoid loops, identify indexing strategy
3. **Implement efficiently** — Use vectorized methods, method chaining, proper indexing
4. **Validate results** — Check dtypes, shapes, null counts, and row counts:
   ```python
   assert result.shape[0] == expected_rows, f"Row count mismatch: {result.shape[0]}"
   assert result.isna().sum().sum() == 0, "Unexpected nulls after transform"
   assert set(result.columns) == expected_cols
   ```
5. **Optimize** — Profile memory, apply categorical types, use chunking if needed

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| DataFrame Operations | `references/dataframe-operations.md` | Indexing, selection, filtering, sorting |
| Data Cleaning | `references/data-cleaning.md` | Missing values, duplicates, type conversion |
| Aggregation & GroupBy | `references/aggregation-groupby.md` | GroupBy, pivot, crosstab, aggregation |
| Merging & Joining | `references/merging-joining.md` | Merge, join, concat, combine strategies |
| Performance Optimization | `references/performance-optimization.md` | Memory usage, vectorization, chunking |

## Code Patterns

### Vectorized Operations (before/after)

```python
# ❌ AVOID: row-by-row iteration
for i, row in df.iterrows():
    df.at[i, 'tax'] = row['price'] * 0.2

# ✅ USE: vectorized assignment
df['tax'] = df['price'] * 0.2
```

### Safe Subsetting with `.copy()`

```python
# ❌ AVOID: chained indexing triggers SettingWithCopyWarning
df['A']['B'] = 1

# ✅ USE: .loc[] with explicit copy when mutating a subset
subset = df.loc[df['status'] == 'active', :].copy()
subset['score'] = subset['score'].fillna(0)
```

### GroupBy Aggregation

```python
summary = (
    df.groupby(['region', 'category'], observed=True)
    .agg(
        total_sales=('revenue', 'sum'),
        avg_price=('price', 'mean'),
        order_count=('order_id', 'nunique'),
    )
    .reset_index()
)
```

### Merge with Validation

```python
merged = pd.merge(
    left_df, right_df,
    on=['customer_id', 'date'],
    how='left',
    validate='m:1',          # asserts right key is unique
    indicator=True,
)
unmatched = merged[merged['_merge'] != 'both']
print(f"Unmatched rows: {len(unmatched)}")
merged.drop(columns=['_merge'], inplace=True)
```

### Missing Value Handling

```python
# Forward-fill then interpolate numeric gaps
df['price'] = df['price'].ffill().interpolate(method='linear')

# Fill categoricals with mode, numerics with median
for col in df.select_dtypes(include='object'):
    df[col] = df[col].fillna(df[col].mode()[0])
for col in df.select_dtypes(include='number'):
    df[col] = df[col].fillna(df[col].median())
```

### Time Series Resampling

```python
daily = (
    df.set_index('timestamp')
    .resample('D')
    .agg({'revenue': 'sum', 'sessions': 'count'})
    .fillna(0)
)
```

### Pivot Table

```python
pivot = df.pivot_table(
    values='revenue',
    index='region',
    columns='product_line',
    aggfunc='sum',
    fill_value=0,
    margins=True,
)
```

### Memory Optimization

```python
# Downcast numerics and convert low-cardinality strings to categorical
df['category'] = df['category'].astype('category')
df['count'] = pd.to_numeric(df['count'], downcast='integer')
df['score'] = pd.to_numeric(df['score'], downcast='float')
print(df.memory_usage(deep=True).sum() / 1e6, "MB after optimization")
```

## Constraints

### MUST DO
- Use vectorized operations instead of loops
- Set appropriate dtypes (categorical for low-cardinality strings)
- Check memory usage with `.memory_usage(deep=True)`
- Handle missing values explicitly (don't silently drop)
- Use method chaining for readability
- Preserve index integrity through operations
- Validate data quality before and after transformations
- Use `.copy()` when modifying subsets to avoid SettingWithCopyWarning

### MUST NOT DO
- Iterate over DataFrame rows with `.iterrows()` unless absolutely necessary
- Use chained indexing (`df['A']['B']`) — use `.loc[]` or `.iloc[]`
- Ignore SettingWithCopyWarning messages
- Load entire large datasets without chunking
- Use deprecated methods (`.ix`, `.append()` — use `pd.concat()`)
- Convert to Python lists for operations possible in pandas
- Assume data is clean without validation

## Output Templates

When implementing pandas solutions, provide:
1. Code with vectorized operations and proper indexing
2. Comments explaining complex transformations
3. Memory/performance considerations if dataset is large
4. Data validation checks (dtypes, nulls, shapes)

---

## Reference: Aggregation Groupby

# Aggregation and GroupBy

---

## Overview

Aggregation transforms data from individual records to summary statistics. This reference covers GroupBy, pivot tables, crosstab, and advanced aggregation patterns with pandas 2.0+.

---

## GroupBy Fundamentals

### Basic GroupBy

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'department': ['Eng', 'Eng', 'Sales', 'Sales', 'Eng', 'HR'],
    'team': ['Backend', 'Frontend', 'East', 'West', 'Backend', 'Recruit'],
    'employee': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
    'salary': [80000, 75000, 65000, 70000, 85000, 60000],
    'years': [5, 3, 7, 4, 6, 2]
})

# Single column groupby with single aggregation
avg_salary = df.groupby('department')['salary'].mean()

# Multiple aggregations
stats = df.groupby('department')['salary'].agg(['mean', 'min', 'max', 'count'])

# GroupBy multiple columns
grouped = df.groupby(['department', 'team'])['salary'].mean()

# Reset index to get DataFrame instead of Series
grouped = df.groupby('department')['salary'].mean().reset_index()
```

### Multiple Columns, Multiple Aggregations

```python
# Named aggregation (pandas 2.0+ preferred)
result = df.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    total_years=('years', 'sum'),
    headcount=('employee', 'count'),
)

# Dictionary syntax (traditional)
result = df.groupby('department').agg({
    'salary': ['mean', 'max', 'std'],
    'years': ['sum', 'mean'],
})

# Flatten multi-level column names
result.columns = ['_'.join(col).strip() for col in result.columns.values]
```

### Custom Aggregation Functions

```python
# Lambda functions
result = df.groupby('department').agg({
    'salary': lambda x: x.max() - x.min(),  # Range
    'years': lambda x: x.quantile(0.75),    # 75th percentile
})

# Named functions for clarity
def salary_range(x):
    return x.max() - x.min()

def coefficient_of_variation(x):
    return x.std() / x.mean() if x.mean() != 0 else 0

result = df.groupby('department').agg(
    salary_range=('salary', salary_range),
    salary_cv=('salary', coefficient_of_variation),
)

# Multiple custom functions
result = df.groupby('department')['salary'].agg([
    ('range', lambda x: x.max() - x.min()),
    ('iqr', lambda x: x.quantile(0.75) - x.quantile(0.25)),
    ('median', 'median'),
])
```

---

## Transform and Apply

### Transform - Returns Same Shape

```python
# Transform returns Series with same index as original
# Useful for adding aggregated values back to original DataFrame

# Add group mean as new column
df['dept_avg_salary'] = df.groupby('department')['salary'].transform('mean')

# Normalize within group
df['salary_zscore'] = df.groupby('department')['salary'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Rank within group
df['salary_rank'] = df.groupby('department')['salary'].transform('rank', ascending=False)

# Percentage of group total
df['salary_pct'] = df.groupby('department')['salary'].transform(
    lambda x: x / x.sum() * 100
)

# Fill missing with group mean
df['salary'] = df.groupby('department')['salary'].transform(
    lambda x: x.fillna(x.mean())
)
```

### Apply - Flexible Operations

```python
# Apply runs function on each group DataFrame
def top_n_by_salary(group, n=2):
    return group.nlargest(n, 'salary')

top_earners = df.groupby('department').apply(top_n_by_salary, n=2)

# Reset index after apply
top_earners = df.groupby('department', group_keys=False).apply(
    top_n_by_salary, n=2
).reset_index(drop=True)

# Complex group operations
def group_summary(group):
    return pd.Series({
        'headcount': len(group),
        'avg_salary': group['salary'].mean(),
        'top_earner': group.loc[group['salary'].idxmax(), 'employee'],
        'avg_tenure': group['years'].mean(),
    })

summary = df.groupby('department').apply(group_summary)
```

### Filter - Keep/Remove Groups

```python
# Keep only groups meeting a condition
# Groups with average salary > 70000
filtered = df.groupby('department').filter(lambda x: x['salary'].mean() > 70000)

# Groups with more than 2 members
filtered = df.groupby('department').filter(lambda x: len(x) > 2)

# Combined conditions
filtered = df.groupby('department').filter(
    lambda x: (len(x) >= 2) and (x['salary'].mean() > 65000)
)
```

---

## Pivot Tables

### Basic Pivot Table

```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=6),
    'product': ['A', 'B', 'A', 'B', 'A', 'B'],
    'region': ['East', 'East', 'West', 'West', 'East', 'West'],
    'sales': [100, 150, 120, 180, 90, 200],
    'quantity': [10, 15, 12, 18, 9, 20],
})

# Simple pivot
pivot = df.pivot_table(
    values='sales',
    index='product',
    columns='region',
    aggfunc='sum'
)

# Multiple values
pivot = df.pivot_table(
    values=['sales', 'quantity'],
    index='product',
    columns='region',
    aggfunc='sum'
)

# Multiple aggregation functions
pivot = df.pivot_table(
    values='sales',
    index='product',
    columns='region',
    aggfunc=['sum', 'mean', 'count']
)
```

### Advanced Pivot Table Options

```python
# Fill missing values
pivot = df.pivot_table(
    values='sales',
    index='product',
    columns='region',
    aggfunc='sum',
    fill_value=0
)

# Add margins (totals)
pivot = df.pivot_table(
    values='sales',
    index='product',
    columns='region',
    aggfunc='sum',
    margins=True,
    margins_name='Total'
)

# Multiple index levels
pivot = df.pivot_table(
    values='sales',
    index=['product', df['date'].dt.month],
    columns='region',
    aggfunc='sum'
)

# Observed categories only (for categorical data)
pivot = df.pivot_table(
    values='sales',
    index='product',
    columns='region',
    aggfunc='sum',
    observed=True  # pandas 2.0+ default changed
)
```

### Unpivoting (Melt)

```python
# Wide to long format
wide_df = pd.DataFrame({
    'product': ['A', 'B'],
    'Q1_sales': [100, 150],
    'Q2_sales': [120, 180],
    'Q3_sales': [90, 200],
})

# Melt to long format
long_df = pd.melt(
    wide_df,
    id_vars=['product'],
    value_vars=['Q1_sales', 'Q2_sales', 'Q3_sales'],
    var_name='quarter',
    value_name='sales'
)

# Clean quarter column
long_df['quarter'] = long_df['quarter'].str.replace('_sales', '')
```

---

## Crosstab

### Basic Crosstab

```python
df = pd.DataFrame({
    'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'M'],
    'department': ['Eng', 'Eng', 'Sales', 'Sales', 'Eng', 'HR', 'HR', 'Eng'],
    'level': ['Senior', 'Junior', 'Senior', 'Senior', 'Junior', 'Junior', 'Senior', 'Junior'],
})

# Simple crosstab (counts)
ct = pd.crosstab(df['gender'], df['department'])

# Normalized crosstab
ct_pct = pd.crosstab(df['gender'], df['department'], normalize='all')  # Total
ct_pct = pd.crosstab(df['gender'], df['department'], normalize='index')  # Row
ct_pct = pd.crosstab(df['gender'], df['department'], normalize='columns')  # Column

# With margins
ct = pd.crosstab(df['gender'], df['department'], margins=True)

# Multiple levels
ct = pd.crosstab(
    [df['gender'], df['level']],
    df['department']
)
```

### Crosstab with Aggregation

```python
df['salary'] = [80000, 75000, 65000, 70000, 85000, 60000, 72000, 78000]

# Crosstab with values and aggregation
ct = pd.crosstab(
    df['gender'],
    df['department'],
    values=df['salary'],
    aggfunc='mean'
)

# Multiple aggregations
ct = pd.crosstab(
    df['gender'],
    df['department'],
    values=df['salary'],
    aggfunc=['mean', 'sum', 'count']
)
```

---

## Window Functions with GroupBy

### Rolling Aggregations

```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10),
    'product': ['A', 'B'] * 5,
    'sales': [100, 150, 110, 160, 120, 170, 130, 180, 140, 190],
})

# Rolling mean within groups
df['rolling_avg'] = df.groupby('product')['sales'].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean()
)

# Expanding aggregations
df['cumulative_sales'] = df.groupby('product')['sales'].transform('cumsum')

df['expanding_avg'] = df.groupby('product')['sales'].transform(
    lambda x: x.expanding().mean()
)

# Rank within groups
df['sales_rank'] = df.groupby('product')['sales'].rank(method='dense')
```

### Shift and Diff

```python
# Previous value within group
df['prev_sales'] = df.groupby('product')['sales'].shift(1)

# Next value
df['next_sales'] = df.groupby('product')['sales'].shift(-1)

# Period-over-period change
df['sales_change'] = df.groupby('product')['sales'].diff()

# Percentage change
df['sales_pct_change'] = df.groupby('product')['sales'].pct_change()
```

---

## Common Aggregation Patterns

### Summary Statistics

```python
# Comprehensive summary by group
def full_summary(group):
    return pd.Series({
        'count': len(group),
        'mean': group['salary'].mean(),
        'std': group['salary'].std(),
        'min': group['salary'].min(),
        'q25': group['salary'].quantile(0.25),
        'median': group['salary'].median(),
        'q75': group['salary'].quantile(0.75),
        'max': group['salary'].max(),
        'sum': group['salary'].sum(),
    })

summary = df.groupby('department').apply(full_summary)
```

### Top N Per Group

```python
# Top 2 salaries per department
top_2 = df.groupby('department', group_keys=False).apply(
    lambda x: x.nlargest(2, 'salary')
)

# Using head after sorting
top_2 = df.sort_values('salary', ascending=False).groupby(
    'department', group_keys=False
).head(2)

# Bottom N
bottom_2 = df.groupby('department', group_keys=False).apply(
    lambda x: x.nsmallest(2, 'salary')
)
```

### First/Last Per Group

```python
# First row per group
first = df.groupby('department').first()

# Last row per group
last = df.groupby('department').last()

# First row after sorting
first_by_salary = df.sort_values('salary', ascending=False).groupby(
    'department'
).first()

# Nth row
nth = df.groupby('department').nth(1)  # Second row (0-indexed)
```

### Cumulative Operations

```python
# Cumulative sum
df['cum_sales'] = df.groupby('department')['salary'].cumsum()

# Cumulative max/min
df['cum_max'] = df.groupby('department')['salary'].cummax()
df['cum_min'] = df.groupby('department')['salary'].cummin()

# Cumulative count
df['cum_count'] = df.groupby('department').cumcount() + 1

# Running percentage of total
df['running_pct'] = df.groupby('department')['salary'].transform(
    lambda x: x.cumsum() / x.sum() * 100
)
```

---

## Performance Tips for GroupBy

### Efficient GroupBy Operations

```python
# Pre-sort for faster groupby operations
df = df.sort_values('department')
grouped = df.groupby('department', sort=False)  # Already sorted

# Use observed=True for categorical columns (pandas 2.0+ default)
df['department'] = df['department'].astype('category')
grouped = df.groupby('department', observed=True)['salary'].mean()

# Avoid apply when possible - use built-in aggregations
# SLOWER:
result = df.groupby('department')['salary'].apply(lambda x: x.sum())
# FASTER:
result = df.groupby('department')['salary'].sum()

# Use numba for custom aggregations (if available)
@numba.jit(nopython=True)
def custom_agg(values):
    return values.sum() / len(values)
```

### Memory-Efficient Aggregation

```python
# For large DataFrames, compute aggregations separately
groups = df.groupby('department')

means = groups['salary'].mean()
sums = groups['salary'].sum()
counts = groups.size()

result = pd.DataFrame({
    'mean': means,
    'sum': sums,
    'count': counts
})

# Avoid creating intermediate large DataFrames
# BAD: Creates full transformed DataFrame
df['z_score'] = (df['salary'] - df.groupby('department')['salary'].transform('mean')) / df.groupby('department')['salary'].transform('std')

# BETTER: Compute once
group_stats = df.groupby('department')['salary'].agg(['mean', 'std'])
df = df.merge(group_stats, on='department')
df['z_score'] = (df['salary'] - df['mean']) / df['std']
```

---

## Best Practices Summary

1. **Use named aggregation** - Clearer than dictionary syntax
2. **Choose transform vs apply wisely** - Transform for same-shape, apply for flexible
3. **Pre-sort for performance** - Use `sort=False` after sorting
4. **Prefer built-in aggregations** - Faster than lambda/apply
5. **Use observed=True** - Especially for categorical data
6. **Reset index when needed** - Keep DataFrames easier to work with
7. **Validate group counts** - Check for unexpected groups

---

## Anti-Patterns to Avoid

```python
# BAD: Iterating over groups manually
for name, group in df.groupby('department'):
    # process group
    pass

# GOOD: Use vectorized operations
df.groupby('department').agg(...)

# BAD: Multiple groupby calls
df.groupby('dept')['salary'].mean()
df.groupby('dept')['salary'].sum()
df.groupby('dept')['salary'].count()

# GOOD: Single groupby, multiple aggs
df.groupby('dept')['salary'].agg(['mean', 'sum', 'count'])

# BAD: Apply for simple aggregations
df.groupby('dept')['salary'].apply(np.mean)

# GOOD: Built-in method
df.groupby('dept')['salary'].mean()
```

---

## Related References

- `dataframe-operations.md` - Filtering before aggregation
- `merging-joining.md` - Join aggregated results back
- `performance-optimization.md` - Optimize large-scale aggregations

---

## Reference: Data Cleaning

# Data Cleaning

---

## Overview

Data cleaning is critical for reliable analysis. This reference covers handling missing values, duplicates, type conversion, and data validation with pandas 2.0+ patterns.

---

## Missing Values

### Detecting Missing Values

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', None, 'Diana'],
    'age': [25, np.nan, 35, 28],
    'salary': [50000, 60000, np.nan, np.nan],
    'department': ['Eng', '', 'Eng', 'Sales']
})

# Check for any missing values
df.isna().any()  # Per column
df.isna().any().any()  # Entire DataFrame

# Count missing values
df.isna().sum()  # Per column
df.isna().sum().sum()  # Total

# Percentage of missing values
(df.isna().sum() / len(df) * 100).round(2)

# Rows with any missing values
df[df.isna().any(axis=1)]

# Rows with all values present
df[df.notna().all(axis=1)]

# Missing value heatmap info
missing_info = pd.DataFrame({
    'missing': df.isna().sum(),
    'percent': (df.isna().sum() / len(df) * 100).round(2),
    'dtype': df.dtypes
})
```

### Handling Missing Values - Dropping

```python
# Drop rows with any missing value
df_clean = df.dropna()

# Drop rows where specific columns have missing values
df_clean = df.dropna(subset=['name', 'age'])

# Drop rows where ALL values are missing
df_clean = df.dropna(how='all')

# Drop rows with minimum non-null values
df_clean = df.dropna(thresh=3)  # Keep rows with at least 3 non-null

# Drop columns with missing values
df_clean = df.dropna(axis=1)

# Drop columns with more than 50% missing
threshold = len(df) * 0.5
df_clean = df.dropna(axis=1, thresh=threshold)
```

### Handling Missing Values - Filling

```python
# Fill with constant value
df['age'] = df['age'].fillna(0)

# Fill with column mean/median/mode
df['age'] = df['age'].fillna(df['age'].mean())
df['salary'] = df['salary'].fillna(df['salary'].median())
df['department'] = df['department'].fillna(df['department'].mode()[0])

# Forward fill (use previous value)
df['salary'] = df['salary'].ffill()

# Backward fill (use next value)
df['salary'] = df['salary'].bfill()

# Fill with different values per column
fill_values = {'age': 0, 'salary': df['salary'].median(), 'name': 'Unknown'}
df = df.fillna(fill_values)

# Fill with interpolation (numeric data)
df['salary'] = df['salary'].interpolate(method='linear')

# Group-specific fill (fill with group mean)
df['salary'] = df.groupby('department')['salary'].transform(
    lambda x: x.fillna(x.mean())
)
```

### Handling Empty Strings vs NaN

```python
# Empty strings are NOT detected as NaN
df['department'].isna().sum()  # Won't count ''

# Replace empty strings with NaN
df['department'] = df['department'].replace('', np.nan)
# Or
df['department'] = df['department'].replace(r'^\s*$', np.nan, regex=True)

# Replace multiple values with NaN
df = df.replace(['', 'N/A', 'null', 'None', '-'], np.nan)

# Using na_values when reading files
df = pd.read_csv('file.csv', na_values=['', 'N/A', 'null', 'None', '-'])
```

---

## Handling Duplicates

### Detecting Duplicates

```python
df = pd.DataFrame({
    'id': [1, 2, 2, 3, 4, 4],
    'name': ['Alice', 'Bob', 'Bob', 'Charlie', 'Diana', 'Diana'],
    'email': ['a@x.com', 'b@x.com', 'b@x.com', 'c@x.com', 'd@x.com', 'd2@x.com']
})

# Check for duplicate rows (all columns)
df.duplicated().sum()

# Check specific columns
df.duplicated(subset=['id']).sum()
df.duplicated(subset=['name', 'email']).sum()

# View duplicate rows
df[df.duplicated(keep=False)]  # All duplicates
df[df.duplicated(keep='first')]  # Duplicates except first occurrence
df[df.duplicated(keep='last')]  # Duplicates except last occurrence

# Count duplicates per key
df.groupby('id').size().loc[lambda x: x > 1]
```

### Removing Duplicates

```python
# Remove duplicate rows (keep first)
df_clean = df.drop_duplicates()

# Keep last occurrence
df_clean = df.drop_duplicates(keep='last')

# Remove all duplicates (keep none)
df_clean = df.drop_duplicates(keep=False)

# Based on specific columns
df_clean = df.drop_duplicates(subset=['id'])
df_clean = df.drop_duplicates(subset=['name', 'email'], keep='last')

# In-place modification
df.drop_duplicates(inplace=True)
```

### Handling Duplicates with Aggregation

```python
# Instead of dropping, aggregate duplicates
df_agg = df.groupby('id').agg({
    'name': 'first',
    'email': lambda x: ', '.join(x.unique())
}).reset_index()

# Keep row with max/min value
df_best = df.loc[df.groupby('id')['score'].idxmax()]

# Rank duplicates
df['rank'] = df.groupby('id').cumcount() + 1
```

---

## Type Conversion

### Checking and Converting Types

```python
# Check current types
df.dtypes
df.info()

# Convert to specific type
df['age'] = df['age'].astype(int)
df['salary'] = df['salary'].astype(float)
df['name'] = df['name'].astype(str)

# Safe conversion with errors handling
df['age'] = pd.to_numeric(df['age'], errors='coerce')  # Invalid -> NaN
df['age'] = pd.to_numeric(df['age'], errors='ignore')  # Keep original if invalid

# Convert multiple columns
df = df.astype({'age': 'int64', 'salary': 'float64'})

# Convert object to string (pandas 2.0+ StringDtype)
df['name'] = df['name'].astype('string')  # Nullable string type
```

### Datetime Conversion

```python
df = pd.DataFrame({
    'date_str': ['2024-01-15', '2024-02-20', 'invalid', '2024-03-10'],
    'timestamp': [1705276800, 1708387200, 1710028800, 1710028800]
})

# String to datetime
df['date'] = pd.to_datetime(df['date_str'], errors='coerce')

# Specify format for faster parsing
df['date'] = pd.to_datetime(df['date_str'], format='%Y-%m-%d', errors='coerce')

# Unix timestamp to datetime
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

# Extract components
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.day_name()

# Handle mixed formats
df['date'] = pd.to_datetime(df['date_str'], format='mixed', dayfirst=False)
```

### Categorical Conversion

```python
# Convert to categorical (memory efficient for low cardinality)
df['department'] = df['department'].astype('category')

# Ordered categorical
df['size'] = pd.Categorical(
    df['size'],
    categories=['Small', 'Medium', 'Large'],
    ordered=True
)

# Check memory savings
print(f"Object: {df['department'].nbytes}")
df['department'] = df['department'].astype('category')
print(f"Category: {df['department'].nbytes}")
```

### Nullable Integer Types (pandas 2.0+)

```python
# Standard int doesn't support NaN
# Use nullable integer types
df['age'] = df['age'].astype('Int64')  # Note capital I

# All nullable types
df = df.astype({
    'count': 'Int64',      # Nullable integer
    'price': 'Float64',    # Nullable float
    'flag': 'boolean',     # Nullable boolean
    'name': 'string',      # Nullable string
})

# Convert with NA handling
df['age'] = pd.array([1, 2, None, 4], dtype='Int64')
```

---

## String Cleaning

### Common String Operations

```python
df = pd.DataFrame({
    'name': ['  Alice  ', 'BOB', 'charlie', None, 'Diana Smith'],
    'email': ['ALICE@EXAMPLE.COM', 'bob@test', 'invalid', None, 'diana@example.com']
})

# Strip whitespace
df['name'] = df['name'].str.strip()

# Case normalization
df['name'] = df['name'].str.lower()
df['name'] = df['name'].str.upper()
df['name'] = df['name'].str.title()  # Title Case

# Replace patterns
df['name'] = df['name'].str.replace(r'\s+', ' ', regex=True)  # Multiple spaces to one
df['phone'] = df['phone'].str.replace(r'[^0-9]', '', regex=True)  # Keep only digits

# Extract with regex
df['domain'] = df['email'].str.extract(r'@(.+)$')
df['first_name'] = df['name'].str.extract(r'^(\w+)')

# Split strings
df[['first', 'last']] = df['name'].str.split(' ', n=1, expand=True)
```

### String Validation

```python
# Check patterns
df['valid_email'] = df['email'].str.match(r'^[\w.]+@[\w.]+\.\w+$', na=False)

# String length
df['name_length'] = df['name'].str.len()
df['valid_length'] = df['name'].str.len().between(2, 50)

# Contains check
df['has_domain'] = df['email'].str.contains('@', na=False)
```

---

## Data Validation

### Validation Functions

```python
def validate_dataframe(df: pd.DataFrame) -> dict:
    """Comprehensive DataFrame validation."""
    report = {
        'rows': len(df),
        'columns': len(df.columns),
        'duplicates': df.duplicated().sum(),
        'missing_by_column': df.isna().sum().to_dict(),
        'dtypes': df.dtypes.astype(str).to_dict(),
    }
    return report

# Range validation
def validate_range(series: pd.Series, min_val, max_val) -> pd.Series:
    """Return boolean mask for values in range."""
    return series.between(min_val, max_val)

df['valid_age'] = validate_range(df['age'], 0, 120)

# Custom validation
def validate_email(series: pd.Series) -> pd.Series:
    """Validate email format."""
    pattern = r'^[\w.+-]+@[\w-]+\.[\w.-]+$'
    return series.str.match(pattern, na=False)

df['valid_email'] = validate_email(df['email'])
```

### Schema Validation with pandera

```python
# Using pandera for schema validation (recommended for production)
import pandera as pa
from pandera import Column, Check

schema = pa.DataFrameSchema({
    'name': Column(str, Check.str_length(min_value=1, max_value=100)),
    'age': Column(int, Check.in_range(0, 120)),
    'email': Column(str, Check.str_matches(r'^[\w.+-]+@[\w-]+\.[\w.-]+$')),
    'salary': Column(float, Check.greater_than(0), nullable=True),
})

# Validate DataFrame
try:
    schema.validate(df)
except pa.errors.SchemaError as e:
    print(f"Validation failed: {e}")
```

---

## Data Cleaning Pipeline

### Method Chaining Pattern

```python
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Complete data cleaning pipeline using method chaining."""
    return (
        df
        # Make a copy
        .copy()
        # Standardize column names
        .rename(columns=lambda x: x.lower().strip().replace(' ', '_'))
        # Drop fully empty rows
        .dropna(how='all')
        # Clean string columns
        .assign(
            name=lambda x: x['name'].str.strip().str.title(),
            email=lambda x: x['email'].str.lower().str.strip(),
        )
        # Handle missing values
        .fillna({'department': 'Unknown'})
        # Convert types
        .astype({'age': 'Int64', 'department': 'category'})
        # Remove duplicates
        .drop_duplicates(subset=['email'])
        # Reset index
        .reset_index(drop=True)
    )

df_clean = clean_dataframe(df)
```

### Pipeline with Validation

```python
def clean_and_validate(
    df: pd.DataFrame,
    required_columns: list[str],
    unique_columns: list[str] | None = None,
) -> tuple[pd.DataFrame, dict]:
    """Clean DataFrame and return validation report."""

    # Validate required columns exist
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Track cleaning stats
    stats = {
        'initial_rows': len(df),
        'dropped_empty': 0,
        'dropped_duplicates': 0,
        'filled_missing': {},
    }

    # Clean
    df = df.copy()

    # Drop empty rows
    before = len(df)
    df = df.dropna(how='all')
    stats['dropped_empty'] = before - len(df)

    # Handle duplicates
    if unique_columns:
        before = len(df)
        df = df.drop_duplicates(subset=unique_columns)
        stats['dropped_duplicates'] = before - len(df)

    stats['final_rows'] = len(df)

    return df, stats
```

---

## Best Practices Summary

1. **Always check data quality first** - Use `.info()`, `.describe()`, and missing value analysis
2. **Document cleaning decisions** - Track what was dropped/filled and why
3. **Use nullable types** - `Int64`, `string`, `boolean` for proper NA handling
4. **Validate after cleaning** - Ensure data meets expectations
5. **Use method chaining** - Readable, maintainable cleaning pipelines
6. **Copy before modifying** - Avoid SettingWithCopyWarning
7. **Handle edge cases** - Empty strings, whitespace, invalid formats

---

## Anti-Patterns to Avoid

```python
# BAD: Dropping NaN without understanding impact
df = df.dropna()  # May lose significant data

# GOOD: Investigate first, then decide
print(f"Missing values: {df.isna().sum()}")
print(f"Rows affected: {df.isna().any(axis=1).sum()}")
# Then make informed decision

# BAD: Filling without domain knowledge
df['age'] = df['age'].fillna(0)  # Age 0 is not valid

# GOOD: Use appropriate fill strategy
df['age'] = df['age'].fillna(df['age'].median())

# BAD: Type conversion without error handling
df['id'] = df['id'].astype(int)  # Will fail on NaN or invalid

# GOOD: Safe conversion
df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
```

---

## Related References

- `dataframe-operations.md` - Selection and filtering for targeted cleaning
- `aggregation-groupby.md` - Aggregate duplicates instead of dropping
- `performance-optimization.md` - Efficient cleaning of large datasets

---

## Reference: Dataframe Operations

# DataFrame Operations

---

## Overview

DataFrame operations form the foundation of pandas work. This reference covers indexing, selection, filtering, and sorting with pandas 2.0+ best practices.

---

## Indexing and Selection

### Label-Based Selection with `.loc[]`

Use `.loc[]` for label-based indexing. Always preferred over chained indexing.

```python
import pandas as pd
import numpy as np

# Sample DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'age': [25, 30, 35, 28],
    'salary': [50000, 60000, 70000, 55000],
    'department': ['Engineering', 'Sales', 'Engineering', 'Marketing']
}, index=['a', 'b', 'c', 'd'])

# Single value
value = df.loc['a', 'name']  # 'Alice'

# Single row (returns Series)
row = df.loc['a']

# Multiple rows
rows = df.loc[['a', 'c']]

# Row and column slices (inclusive on both ends)
subset = df.loc['a':'c', 'name':'salary']

# Boolean indexing with .loc
adults = df.loc[df['age'] >= 30]

# Boolean indexing with column selection
adults_names = df.loc[df['age'] >= 30, 'name']

# Multiple conditions
engineering_seniors = df.loc[
    (df['department'] == 'Engineering') & (df['age'] >= 30),
    ['name', 'salary']
]
```

### Position-Based Selection with `.iloc[]`

Use `.iloc[]` for integer position-based indexing.

```python
# Single value by position
value = df.iloc[0, 0]  # First row, first column

# Single row by position
first_row = df.iloc[0]

# Slice rows (exclusive end, like Python)
first_three = df.iloc[:3]

# Specific rows and columns by position
subset = df.iloc[[0, 2], [0, 2]]  # Rows 0,2 and columns 0,2

# Range selection
block = df.iloc[1:3, 0:2]  # Rows 1-2, columns 0-1
```

### When to Use `.loc[]` vs `.iloc[]`

| Scenario | Use | Example |
|----------|-----|---------|
| Known column names | `.loc[]` | `df.loc[:, 'name']` |
| Filter by condition | `.loc[]` | `df.loc[df['age'] > 25]` |
| First/last N rows | `.iloc[]` | `df.iloc[:5]` or `df.iloc[-5:]` |
| Specific row positions | `.iloc[]` | `df.iloc[[0, 5, 10]]` |
| Unknown column order | `.iloc[]` | `df.iloc[:, 0]` |

---

## Filtering DataFrames

### Boolean Masks

```python
# Single condition
mask = df['age'] > 25
filtered = df[mask]

# Multiple conditions (use parentheses!)
mask = (df['age'] > 25) & (df['salary'] < 65000)
filtered = df[mask]

# OR conditions
mask = (df['department'] == 'Engineering') | (df['department'] == 'Sales')
filtered = df[mask]

# NOT condition
mask = ~(df['department'] == 'Marketing')
filtered = df[mask]
```

### Using `.query()` for Readable Filters

```python
# Simple query - more readable for complex conditions
result = df.query('age > 25 and salary < 65000')

# Using variables with @
min_age = 25
result = df.query('age > @min_age')

# String comparisons
result = df.query('department == "Engineering"')

# In-list filtering
depts = ['Engineering', 'Sales']
result = df.query('department in @depts')

# Complex expressions
result = df.query('(age > 25) and (department != "Marketing")')
```

### Using `.isin()` for Multiple Values

```python
# Filter by multiple values
departments = ['Engineering', 'Sales']
filtered = df[df['department'].isin(departments)]

# Negation
filtered = df[~df['department'].isin(departments)]

# Multiple columns
conditions = {
    'department': ['Engineering', 'Sales'],
    'age': [25, 30, 35]
}
# Filter where department is in list AND age is in list
mask = df['department'].isin(conditions['department']) & df['age'].isin(conditions['age'])
```

### String Filtering with `.str` Accessor

```python
df = pd.DataFrame({
    'email': ['alice@example.com', 'bob@test.org', 'charlie@example.com'],
    'name': ['Alice Smith', 'Bob Jones', 'Charlie Brown']
})

# Contains
mask = df['email'].str.contains('example')

# Starts/ends with
mask = df['email'].str.endswith('.com')
mask = df['name'].str.startswith('A')

# Regex matching
mask = df['email'].str.match(r'^[a-z]+@example\.com$')

# Case-insensitive
mask = df['name'].str.lower().str.contains('alice')
# Or with case parameter
mask = df['name'].str.contains('alice', case=False)

# Handle NaN in string columns
mask = df['email'].str.contains('example', na=False)
```

---

## Sorting

### Basic Sorting

```python
# Sort by single column (ascending)
sorted_df = df.sort_values('age')

# Sort descending
sorted_df = df.sort_values('age', ascending=False)

# Sort by multiple columns
sorted_df = df.sort_values(['department', 'salary'], ascending=[True, False])

# Sort by index
sorted_df = df.sort_index()
sorted_df = df.sort_index(ascending=False)
```

### Advanced Sorting

```python
# Sort with NaN handling
df_with_nan = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'score': [85.0, np.nan, 90.0]
})

# NaN at end (default)
sorted_df = df_with_nan.sort_values('score', na_position='last')

# NaN at beginning
sorted_df = df_with_nan.sort_values('score', na_position='first')

# Custom sort order using Categorical
order = ['Marketing', 'Sales', 'Engineering']
df['department'] = pd.Categorical(df['department'], categories=order, ordered=True)
sorted_df = df.sort_values('department')

# Sort by computed values without adding column
sorted_df = df.iloc[df['name'].str.len().argsort()]
```

### In-Place Sorting

```python
# Modify DataFrame in place
df.sort_values('age', inplace=True)

# Reset index after sorting
df.sort_values('age', inplace=True)
df.reset_index(drop=True, inplace=True)

# Or chain
df = df.sort_values('age').reset_index(drop=True)
```

---

## Column Operations

### Adding and Modifying Columns

```python
# Add new column
df['bonus'] = df['salary'] * 0.1

# Conditional column with np.where
df['seniority'] = np.where(df['age'] >= 30, 'Senior', 'Junior')

# Multiple conditions with np.select
conditions = [
    df['age'] < 25,
    df['age'] < 35,
    df['age'] >= 35
]
choices = ['Junior', 'Mid', 'Senior']
df['level'] = np.select(conditions, choices, default='Unknown')

# Using .assign() for method chaining (returns new DataFrame)
df_new = df.assign(
    bonus=lambda x: x['salary'] * 0.1,
    total_comp=lambda x: x['salary'] + x['salary'] * 0.1
)
```

### Renaming Columns

```python
# Rename specific columns
df = df.rename(columns={'name': 'full_name', 'age': 'years'})

# Rename all columns with function
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Using rename with function
df = df.rename(columns=str.upper)
```

### Dropping Columns

```python
# Drop single column
df = df.drop('bonus', axis=1)
# Or
df = df.drop(columns=['bonus'])

# Drop multiple columns
df = df.drop(columns=['bonus', 'level'])

# Drop columns by condition
cols_to_drop = [col for col in df.columns if col.startswith('temp_')]
df = df.drop(columns=cols_to_drop)
```

### Reordering Columns

```python
# Explicit order
new_order = ['name', 'department', 'age', 'salary']
df = df[new_order]

# Move specific column to front
cols = ['salary'] + [c for c in df.columns if c != 'salary']
df = df[cols]

# Using .reindex()
df = df.reindex(columns=['name', 'age', 'salary', 'department'])
```

---

## Index Operations

### Setting and Resetting Index

```python
# Set column as index
df = df.set_index('name')

# Reset index back to column
df = df.reset_index()

# Drop index completely
df = df.reset_index(drop=True)

# Set multiple columns as index (MultiIndex)
df = df.set_index(['department', 'name'])
```

### Working with MultiIndex

```python
# Create MultiIndex DataFrame
df = pd.DataFrame({
    'department': ['Eng', 'Eng', 'Sales', 'Sales'],
    'team': ['Backend', 'Frontend', 'East', 'West'],
    'headcount': [10, 8, 15, 12]
}).set_index(['department', 'team'])

# Select from MultiIndex
df.loc['Eng']  # All Eng rows
df.loc[('Eng', 'Backend')]  # Specific row

# Cross-section with .xs()
df.xs('Backend', level='team')  # All Backend teams

# Reset specific level
df.reset_index(level='team')
```

---

## Copying DataFrames

### When to Use `.copy()`

```python
# ALWAYS copy when modifying a subset
subset = df[df['age'] > 25].copy()
subset['new_col'] = 100  # Safe, no SettingWithCopyWarning

# Without copy - may raise warning or fail silently
# BAD:
# subset = df[df['age'] > 25]
# subset['new_col'] = 100  # SettingWithCopyWarning!

# Deep copy (default) - copies data
df_copy = df.copy()  # or df.copy(deep=True)

# Shallow copy - shares data, only copies structure
df_shallow = df.copy(deep=False)
```

---

## Best Practices Summary

1. **Use `.loc[]` and `.iloc[]`** - Never use chained indexing
2. **Parenthesize conditions** - `(cond1) & (cond2)` not `cond1 & cond2`
3. **Use `.query()` for readability** - Especially with complex filters
4. **Copy before modifying subsets** - Always use `.copy()`
5. **Use vectorized operations** - Avoid row iteration for filtering
6. **Handle NaN explicitly** - Use `na=False` in string operations
7. **Prefer method chaining** - Use `.assign()` for column creation

---

## Anti-Patterns to Avoid

```python
# BAD: Chained indexing
df['A']['B'] = value  # May not work, raises warning

# GOOD: Use .loc
df.loc[:, ('A', 'B')] = value
# Or for row selection then assignment:
df.loc[df['A'] > 0, 'B'] = value

# BAD: Iterating for filtering
result = []
for idx, row in df.iterrows():
    if row['age'] > 25:
        result.append(row)

# GOOD: Boolean indexing
result = df[df['age'] > 25]

# BAD: Multiple separate assignments
df = df[df['age'] > 25]
df = df[df['salary'] > 50000]

# GOOD: Combined filter
df = df[(df['age'] > 25) & (df['salary'] > 50000)]
```

---

## Related References

- `data-cleaning.md` - After selection, clean the data
- `aggregation-groupby.md` - Group and aggregate filtered data
- `performance-optimization.md` - Optimize filtering on large datasets

---

## Reference: Merging Joining

# Merging and Joining

---

## Overview

Combining DataFrames is essential for working with relational data. This reference covers merge, join, concat, and advanced combination strategies with pandas 2.0+.

---

## Merge (SQL-Style Joins)

### Basic Merge

```python
import pandas as pd
import numpy as np

# Sample DataFrames
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'dept_id': [101, 102, 101, 103, 102],
})

departments = pd.DataFrame({
    'dept_id': [101, 102, 104],
    'dept_name': ['Engineering', 'Sales', 'Marketing'],
})

# Inner join (default) - only matching rows
result = pd.merge(employees, departments, on='dept_id')

# Explicit how parameter
result = pd.merge(employees, departments, on='dept_id', how='inner')
```

### Join Types

```python
# Inner join - only matching rows from both
inner = pd.merge(employees, departments, on='dept_id', how='inner')
# Result: 4 rows (emp_id 4 has dept_id 103 which doesn't exist in departments)

# Left join - all rows from left, matching from right
left = pd.merge(employees, departments, on='dept_id', how='left')
# Result: 5 rows (Diana has NaN for dept_name)

# Right join - all rows from right, matching from left
right = pd.merge(employees, departments, on='dept_id', how='right')
# Result: 4 rows (Marketing has no employees, but is included)

# Outer join - all rows from both
outer = pd.merge(employees, departments, on='dept_id', how='outer')
# Result: 6 rows (includes unmatched from both sides)

# Cross join - cartesian product
cross = pd.merge(employees, departments, how='cross')
# Result: 15 rows (5 employees x 3 departments)
```

### Merging on Different Column Names

```python
employees = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': [101, 102, 101],
})

departments = pd.DataFrame({
    'id': [101, 102],
    'dept_name': ['Engineering', 'Sales'],
})

# Different column names
result = pd.merge(
    employees,
    departments,
    left_on='department',
    right_on='id'
)

# Drop duplicate column after merge
result = result.drop('id', axis=1)
```

### Merging on Multiple Columns

```python
sales = pd.DataFrame({
    'region': ['East', 'East', 'West', 'West'],
    'product': ['A', 'B', 'A', 'B'],
    'sales': [100, 150, 120, 180],
})

targets = pd.DataFrame({
    'region': ['East', 'East', 'West'],
    'product': ['A', 'B', 'A'],
    'target': [90, 140, 110],
})

# Merge on multiple columns
result = pd.merge(sales, targets, on=['region', 'product'], how='left')
```

### Merging on Index

```python
# Set index before merge
employees_idx = employees.set_index('emp_id')
salaries = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'salary': [80000, 75000, 70000, 65000],
}).set_index('emp_id')

# Merge on index
result = pd.merge(employees_idx, salaries, left_index=True, right_index=True)

# Mix of column and index
result = pd.merge(
    employees,
    salaries,
    left_on='emp_id',
    right_index=True
)
```

---

## Handling Duplicate Columns

### Suffixes

```python
df1 = pd.DataFrame({
    'id': [1, 2, 3],
    'value': [10, 20, 30],
    'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
})

df2 = pd.DataFrame({
    'id': [1, 2, 3],
    'value': [100, 200, 300],
    'date': ['2024-02-01', '2024-02-02', '2024-02-03'],
})

# Default suffixes
result = pd.merge(df1, df2, on='id')
# Columns: id, value_x, date_x, value_y, date_y

# Custom suffixes
result = pd.merge(df1, df2, on='id', suffixes=('_jan', '_feb'))
# Columns: id, value_jan, date_jan, value_feb, date_feb
```

### Validate Merge Cardinality

```python
# Validate merge relationships (pandas 2.0+)
# Raises MergeError if validation fails

# One-to-one: each key appears at most once in both DataFrames
result = pd.merge(df1, df2, on='id', validate='one_to_one')  # or '1:1'

# One-to-many: keys unique in left only
result = pd.merge(employees, salaries, on='emp_id', validate='one_to_many')  # or '1:m'

# Many-to-one: keys unique in right only
result = pd.merge(salaries, employees, on='emp_id', validate='many_to_one')  # or 'm:1'

# Many-to-many: no uniqueness requirement (default)
result = pd.merge(df1, df2, on='id', validate='many_to_many')  # or 'm:m'
```

### Indicator Column

```python
# Add indicator column showing source of each row
result = pd.merge(
    employees,
    departments,
    on='dept_id',
    how='outer',
    indicator=True
)
# _merge column values: 'left_only', 'right_only', 'both'

# Custom indicator name
result = pd.merge(
    employees,
    departments,
    on='dept_id',
    how='outer',
    indicator='source'
)

# Filter by indicator
left_only = result[result['_merge'] == 'left_only']
both = result[result['_merge'] == 'both']
```

---

## Join (Index-Based)

### DataFrame.join()

```python
# join() is for index-based joining (simpler syntax)
employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'dept_id': [101, 102, 101],
}, index=[1, 2, 3])

salaries = pd.DataFrame({
    'salary': [80000, 75000, 70000],
    'bonus': [5000, 4000, 3500],
}, index=[1, 2, 3])

# Join on index
result = employees.join(salaries)

# Join types (same as merge)
result = employees.join(salaries, how='left')
result = employees.join(salaries, how='outer')
```

### Join on Column to Index

```python
employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'dept_id': [101, 102, 101],
})

departments = pd.DataFrame({
    'dept_name': ['Engineering', 'Sales'],
}, index=[101, 102])

# Join left column to right index
result = employees.join(departments, on='dept_id')
```

### Join Multiple DataFrames

```python
df1 = pd.DataFrame({'a': [1, 2]}, index=['x', 'y'])
df2 = pd.DataFrame({'b': [3, 4]}, index=['x', 'y'])
df3 = pd.DataFrame({'c': [5, 6]}, index=['x', 'y'])

# Join multiple at once
result = df1.join([df2, df3])

# With suffixes for duplicate columns
result = df1.join([df2, df3], lsuffix='_1', rsuffix='_2')
```

---

## Concat (Stacking DataFrames)

### Vertical Concatenation (Row-wise)

```python
# Stack DataFrames vertically
df1 = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [25, 30],
})

df2 = pd.DataFrame({
    'name': ['Charlie', 'Diana'],
    'age': [35, 28],
})

# Basic concat (axis=0 is default)
result = pd.concat([df1, df2])

# Reset index
result = pd.concat([df1, df2], ignore_index=True)

# Keep track of source
result = pd.concat([df1, df2], keys=['source1', 'source2'])
# Creates MultiIndex
```

### Horizontal Concatenation (Column-wise)

```python
names = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie']})
ages = pd.DataFrame({'age': [25, 30, 35]})
salaries = pd.DataFrame({'salary': [50000, 60000, 70000]})

# Concat columns (axis=1)
result = pd.concat([names, ages, salaries], axis=1)
```

### Handling Mismatched Columns

```python
df1 = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [25, 30],
})

df2 = pd.DataFrame({
    'name': ['Charlie', 'Diana'],
    'salary': [70000, 65000],
})

# Outer join (default) - include all columns
result = pd.concat([df1, df2])
# age and salary columns have NaN where not present

# Inner join - only common columns
result = pd.concat([df1, df2], join='inner')
# Only 'name' column
```

### Concat with Verification

```python
# Verify no index overlap
try:
    result = pd.concat([df1, df2], verify_integrity=True)
except ValueError as e:
    print(f"Index overlap detected: {e}")

# Alternative: use ignore_index
result = pd.concat([df1, df2], ignore_index=True)
```

---

## Combine and Update

### combine_first() - Fill Gaps

```python
# Fill NaN values from another DataFrame
df1 = pd.DataFrame({
    'A': [1, np.nan, 3],
    'B': [np.nan, 2, 3],
}, index=['a', 'b', 'c'])

df2 = pd.DataFrame({
    'A': [10, 20, 30],
    'B': [10, 20, 30],
}, index=['a', 'b', 'c'])

# Fill NaN in df1 with values from df2
result = df1.combine_first(df2)
# A: [1, 20, 3], B: [10, 2, 3]
```

### update() - In-Place Update

```python
df1 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
}, index=['a', 'b', 'c'])

df2 = pd.DataFrame({
    'A': [10, 20],
    'B': [40, 50],
}, index=['a', 'b'])

# Update df1 with values from df2 (in-place)
df1.update(df2)
# df1 now has A: [10, 20, 3], B: [40, 50, 6]

# Only update where df2 has non-NaN
df1.update(df2, overwrite=False)  # Don't overwrite existing values
```

---

## Advanced Merge Patterns

### Merge with Aggregation

```python
# Merge and aggregate in one operation
orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4],
    'customer_id': [101, 102, 101, 103],
    'amount': [100, 200, 150, 300],
})

customers = pd.DataFrame({
    'customer_id': [101, 102, 103],
    'name': ['Alice', 'Bob', 'Charlie'],
})

# Get customer summary
customer_summary = orders.groupby('customer_id').agg(
    total_orders=('order_id', 'count'),
    total_amount=('amount', 'sum'),
).reset_index()

# Merge with customer info
result = pd.merge(customers, customer_summary, on='customer_id')
```

### Merge Asof (Nearest Match)

```python
# Merge on nearest key (useful for time series)
trades = pd.DataFrame({
    'time': pd.to_datetime(['2024-01-01 10:00:01', '2024-01-01 10:00:03', '2024-01-01 10:00:05']),
    'ticker': ['AAPL', 'AAPL', 'AAPL'],
    'price': [150.0, 151.0, 150.5],
})

quotes = pd.DataFrame({
    'time': pd.to_datetime(['2024-01-01 10:00:00', '2024-01-01 10:00:02', '2024-01-01 10:00:04']),
    'ticker': ['AAPL', 'AAPL', 'AAPL'],
    'bid': [149.5, 150.5, 150.0],
    'ask': [150.5, 151.5, 151.0],
})

# Merge asof - find nearest quote for each trade
result = pd.merge_asof(
    trades.sort_values('time'),
    quotes.sort_values('time'),
    on='time',
    by='ticker',
    direction='backward'  # Use most recent quote
)
```

### Conditional Merge

```python
# Merge with conditions beyond key equality
# First merge, then filter

products = pd.DataFrame({
    'product_id': [1, 2, 3],
    'name': ['Widget', 'Gadget', 'Gizmo'],
    'category': ['A', 'B', 'A'],
})

discounts = pd.DataFrame({
    'category': ['A', 'A', 'B'],
    'min_qty': [10, 50, 20],
    'discount': [0.05, 0.10, 0.08],
})

# Cross merge then filter
merged = pd.merge(products, discounts, on='category')
# Then apply quantity-based filtering as needed
```

---

## Performance Considerations

### Pre-sorting for Merge

```python
# Sort keys before merge for better performance
df1 = df1.sort_values('key')
df2 = df2.sort_values('key')

# Merge sorted DataFrames
result = pd.merge(df1, df2, on='key')
```

### Index Alignment

```python
# Using index for merge is often faster than columns
df1 = df1.set_index('key')
df2 = df2.set_index('key')

# Join on index
result = df1.join(df2)
```

### Memory-Efficient Merge

```python
# For large DataFrames, reduce memory before merge
# Convert to appropriate types
df1['key'] = df1['key'].astype('int32')  # Instead of int64
df1['category'] = df1['category'].astype('category')

# Select only needed columns
cols_needed = ['key', 'value1', 'value2']
result = pd.merge(df1[cols_needed], df2[cols_needed], on='key')
```

---

## Common Merge Patterns

### Left Join with Null Check

```python
# Find unmatched rows after left join
result = pd.merge(employees, departments, on='dept_id', how='left')
unmatched = result[result['dept_name'].isna()]
```

### Anti-Join (Rows Not in Other)

```python
# Find employees NOT in a specific department list
dept_list = [101, 102]

# Method 1: Using isin
not_in_depts = employees[~employees['dept_id'].isin(dept_list)]

# Method 2: Using merge with indicator
merged = pd.merge(
    employees,
    pd.DataFrame({'dept_id': dept_list}),
    on='dept_id',
    how='left',
    indicator=True
)
not_in_depts = merged[merged['_merge'] == 'left_only']
```

### Self-Join

```python
# Find pairs within same department
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'dept_id': [101, 101, 102, 101],
})

# Self-join to find pairs
pairs = pd.merge(
    employees,
    employees,
    on='dept_id',
    suffixes=('_1', '_2')
)
# Remove self-pairs and duplicates
pairs = pairs[pairs['emp_id_1'] < pairs['emp_id_2']]
```

---

## Best Practices Summary

1. **Choose the right join type** - Default inner may drop data
2. **Validate cardinality** - Use `validate` parameter
3. **Use indicator** - Debug unexpected results
4. **Handle duplicates** - Use meaningful suffixes
5. **Pre-sort for performance** - Especially for large DataFrames
6. **Reset index after operations** - Keep DataFrames usable
7. **Check for NaN after join** - Understand unmatched rows

---

## Anti-Patterns to Avoid

```python
# BAD: Merge without understanding cardinality
result = pd.merge(df1, df2, on='key')  # May explode row count

# GOOD: Validate relationship
result = pd.merge(df1, df2, on='key', validate='one_to_one')

# BAD: Repeated merges
result = pd.merge(df1, df2, on='key')
result = pd.merge(result, df3, on='key')
result = pd.merge(result, df4, on='key')

# GOOD: Chain or use reduce
from functools import reduce
dfs = [df1, df2, df3, df4]
result = reduce(lambda left, right: pd.merge(left, right, on='key'), dfs)

# BAD: Ignoring merge indicators
result = pd.merge(df1, df2, on='key', how='outer')

# GOOD: Check merge results
result = pd.merge(df1, df2, on='key', how='outer', indicator=True)
print(result['_merge'].value_counts())
```

---

## Related References

- `dataframe-operations.md` - Filter before/after merge
- `aggregation-groupby.md` - Aggregate before merging
- `performance-optimization.md` - Optimize large merges

---

## Reference: Performance Optimization

# Performance Optimization

---

## Overview

Optimizing pandas performance is critical for production workflows. This reference covers memory optimization, vectorization, chunking, and profiling with pandas 2.0+.

---

## Memory Analysis

### Checking Memory Usage

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'id': range(1_000_000),
    'name': ['user_' + str(i) for i in range(1_000_000)],
    'category': np.random.choice(['A', 'B', 'C', 'D'], 1_000_000),
    'value': np.random.randn(1_000_000),
    'count': np.random.randint(0, 100, 1_000_000),
})

# Basic memory info
print(df.info(memory_usage='deep'))

# Detailed memory by column
memory_usage = df.memory_usage(deep=True)
print(memory_usage)
print(f"Total: {memory_usage.sum() / 1e6:.2f} MB")

# Memory as percentage of total
memory_pct = (memory_usage / memory_usage.sum() * 100).round(2)
print(memory_pct)
```

### Memory Profiling Function

```python
def memory_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Profile memory usage by column with optimization suggestions."""
    memory_bytes = df.memory_usage(deep=True)

    profile = pd.DataFrame({
        'dtype': df.dtypes,
        'non_null': df.count(),
        'null_count': df.isna().sum(),
        'unique': df.nunique(),
        'memory_mb': (memory_bytes / 1e6).round(3),
    })

    # Add optimization suggestions
    suggestions = []
    for col in df.columns:
        dtype = df[col].dtype
        nunique = df[col].nunique()

        if dtype == 'object':
            if nunique / len(df) < 0.5:  # Less than 50% unique
                suggestions.append(f"Convert to category (only {nunique} unique)")
            else:
                suggestions.append("Consider string dtype")
        elif dtype == 'int64':
            if df[col].max() < 2**31 and df[col].min() >= -2**31:
                suggestions.append("Downcast to int32")
            if df[col].max() < 2**15 and df[col].min() >= -2**15:
                suggestions.append("Downcast to int16")
        elif dtype == 'float64':
            suggestions.append("Consider float32 if precision allows")
        else:
            suggestions.append("OK")

    profile['suggestion'] = suggestions
    return profile

print(memory_profile(df))
```

---

## Memory Optimization Techniques

### Downcasting Numeric Types

```python
# Automatic downcasting for integers
df['count'] = pd.to_numeric(df['count'], downcast='integer')

# Automatic downcasting for floats
df['value'] = pd.to_numeric(df['value'], downcast='float')

# Manual downcasting function
def downcast_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce memory by downcasting numeric types."""
    df = df.copy()

    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')

    return df

df_optimized = downcast_dtypes(df)
print(f"Before: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
print(f"After: {df_optimized.memory_usage(deep=True).sum() / 1e6:.2f} MB")
```

### Using Categorical Type

```python
# Convert low-cardinality string columns to category
# Especially effective when unique values << total rows

# Before
print(f"Object dtype: {df['category'].memory_usage(deep=True) / 1e6:.2f} MB")

# After
df['category'] = df['category'].astype('category')
print(f"Category dtype: {df['category'].memory_usage(deep=True) / 1e6:.2f} MB")

# Automatic conversion for low-cardinality columns
def optimize_categories(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Convert object columns to category if unique ratio < threshold."""
    df = df.copy()

    for col in df.select_dtypes(include=['object']).columns:
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio < threshold:
            df[col] = df[col].astype('category')

    return df
```

### Sparse Data Types

```python
# For data with many repeated values (especially zeros/NaN)
sparse_series = pd.arrays.SparseArray([0, 0, 1, 0, 0, 0, 2, 0, 0, 0])

# Create sparse DataFrame
df_sparse = pd.DataFrame({
    'sparse_col': pd.arrays.SparseArray([0] * 9000 + [1] * 1000),
    'dense_col': [0] * 9000 + [1] * 1000,
})

print(f"Sparse: {df_sparse['sparse_col'].memory_usage() / 1e6:.4f} MB")
print(f"Dense: {df_sparse['dense_col'].memory_usage() / 1e6:.4f} MB")
```

### Nullable Types (pandas 2.0+)

```python
# Use nullable types for proper NA handling with memory efficiency
df = df.astype({
    'id': 'Int32',          # Nullable int32
    'count': 'Int16',       # Nullable int16
    'value': 'Float32',     # Nullable float32
    'name': 'string',       # Nullable string (more memory efficient)
    'category': 'category', # Categorical
})

# Arrow-backed types for even better memory (pandas 2.0+)
df['name'] = df['name'].astype('string[pyarrow]')
df['category'] = df['category'].astype('category')
```

---

## Vectorization

### Replace Loops with Vectorized Operations

```python
# BAD: Row iteration (extremely slow)
result = []
for idx, row in df.iterrows():
    if row['value'] > 0:
        result.append(row['value'] * 2)
    else:
        result.append(0)
df['result'] = result

# GOOD: Vectorized with np.where
df['result'] = np.where(df['value'] > 0, df['value'] * 2, 0)

# GOOD: Vectorized with boolean indexing
df['result'] = 0
df.loc[df['value'] > 0, 'result'] = df.loc[df['value'] > 0, 'value'] * 2
```

### Multiple Conditions with np.select

```python
# BAD: Nested if-else in apply
def categorize(row):
    if row['value'] < -1:
        return 'very_low'
    elif row['value'] < 0:
        return 'low'
    elif row['value'] < 1:
        return 'medium'
    else:
        return 'high'

df['category'] = df.apply(categorize, axis=1)  # SLOW!

# GOOD: Vectorized with np.select
conditions = [
    df['value'] < -1,
    df['value'] < 0,
    df['value'] < 1,
]
choices = ['very_low', 'low', 'medium']
df['category'] = np.select(conditions, choices, default='high')
```

### String Operations - Vectorized

```python
# BAD: Apply for string operations
df['upper_name'] = df['name'].apply(lambda x: x.upper())

# GOOD: Vectorized string methods
df['upper_name'] = df['name'].str.upper()

# Combine multiple string operations
df['processed'] = (
    df['name']
    .str.strip()
    .str.lower()
    .str.replace(r'\s+', '_', regex=True)
)
```

### Avoid apply() When Possible

```python
# BAD: apply for row-wise calculation
df['total'] = df.apply(lambda row: row['a'] + row['b'] + row['c'], axis=1)

# GOOD: Direct vectorized operation
df['total'] = df['a'] + df['b'] + df['c']

# BAD: apply for element-wise operation
df['squared'] = df['value'].apply(lambda x: x ** 2)

# GOOD: Vectorized
df['squared'] = df['value'] ** 2

# When apply IS appropriate: complex custom logic
def complex_calculation(row):
    # Multiple dependencies and conditional logic
    if row['type'] == 'A':
        return row['value'] * row['multiplier'] + row['offset']
    else:
        return row['value'] / row['divisor'] - row['adjustment']

# Consider rewriting as vectorized if performance critical
```

---

## Chunked Processing

### Reading Large Files in Chunks

```python
# Read CSV in chunks
chunk_size = 100_000
chunks = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    processed = chunk[chunk['value'] > 0]  # Filter
    processed = processed.groupby('category')['value'].sum()  # Aggregate
    chunks.append(processed)

# Combine results
result = pd.concat(chunks).groupby(level=0).sum()
```

### Chunked Processing Function

```python
def process_large_csv(
    filepath: str,
    chunk_size: int = 100_000,
    filter_func=None,
    agg_func=None,
) -> pd.DataFrame:
    """Process large CSV files in chunks."""
    results = []

    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        # Apply filter if provided
        if filter_func:
            chunk = filter_func(chunk)

        # Apply aggregation if provided
        if agg_func:
            chunk = agg_func(chunk)

        results.append(chunk)

    # Combine results
    combined = pd.concat(results, ignore_index=True)

    # Re-aggregate if needed
    if agg_func:
        combined = agg_func(combined)

    return combined

# Usage
result = process_large_csv(
    'large_file.csv',
    chunk_size=50_000,
    filter_func=lambda df: df[df['value'] > 0],
    agg_func=lambda df: df.groupby('category').agg({'value': 'sum'}),
)
```

### Memory-Efficient Iteration

```python
# When you must iterate, use itertuples (not iterrows)
# itertuples is 10-100x faster than iterrows

# BAD: iterrows
for idx, row in df.iterrows():
    process(row['name'], row['value'])

# BETTER: itertuples
for row in df.itertuples():
    process(row.name, row.value)  # Access as attributes

# BEST: Vectorized operations (avoid iteration entirely)
```

---

## Query Optimization

### Efficient Filtering

```python
# Order matters - filter early, compute late
# BAD: Compute on all rows, then filter
df['expensive_calc'] = df['a'] * df['b'] + np.sin(df['c'])
result = df[df['category'] == 'A']

# GOOD: Filter first, compute on subset
mask = df['category'] == 'A'
result = df[mask].copy()
result['expensive_calc'] = result['a'] * result['b'] + np.sin(result['c'])
```

### Using query() for Performance

```python
# query() can be faster for large DataFrames (uses numexpr)
# Traditional boolean indexing
result = df[(df['value'] > 0) & (df['category'] == 'A')]

# query() syntax (faster for large data)
result = df.query('value > 0 and category == "A"')

# With variables
threshold = 0
cat = 'A'
result = df.query('value > @threshold and category == @cat')
```

### eval() for Complex Expressions

```python
# eval() uses numexpr for faster computation
# Standard pandas
df['result'] = df['a'] + df['b'] * df['c'] - df['d']

# Using eval (faster for large DataFrames)
df['result'] = pd.eval('df.a + df.b * df.c - df.d')

# In-place with inplace parameter
df.eval('result = a + b * c - d', inplace=True)
```

---

## GroupBy Optimization

### Pre-sort for Faster GroupBy

```python
# Sort by groupby column first
df = df.sort_values('category')

# Use sort=False since already sorted
result = df.groupby('category', sort=False)['value'].mean()
```

### Use Built-in Aggregations

```python
# BAD: Custom function via apply
result = df.groupby('category')['value'].apply(lambda x: x.mean())

# GOOD: Built-in aggregation
result = df.groupby('category')['value'].mean()

# Built-in aggregations available:
# sum, mean, median, min, max, std, var, count, first, last, nth
# size, sem, prod, cumsum, cummax, cummin, cumprod
```

### Observed Categories

```python
# For categorical columns, use observed=True (pandas 2.0+ default)
df['category'] = df['category'].astype('category')

# Avoid computing for unobserved categories
result = df.groupby('category', observed=True)['value'].mean()
```

---

## I/O Optimization

### Efficient File Formats

```python
# Parquet - best for analytical workloads
df.to_parquet('data.parquet', compression='snappy')
df = pd.read_parquet('data.parquet')

# Feather - best for pandas interchange
df.to_feather('data.feather')
df = pd.read_feather('data.feather')

# CSV with optimizations
df.to_csv('data.csv', index=False)
df = pd.read_csv(
    'data.csv',
    dtype={'category': 'category', 'count': 'int32'},
    usecols=['id', 'category', 'value'],  # Only needed columns
    nrows=10000,  # Limit rows for testing
)
```

### Specify dtypes When Reading

```python
# Specify dtypes upfront to avoid inference overhead
dtypes = {
    'id': 'int32',
    'name': 'string',
    'category': 'category',
    'value': 'float32',
    'count': 'int16',
}

df = pd.read_csv('data.csv', dtype=dtypes)

# Parse dates efficiently
df = pd.read_csv(
    'data.csv',
    dtype=dtypes,
    parse_dates=['date_column'],
    date_format='%Y-%m-%d',  # Explicit format is faster
)
```

---

## Profiling and Benchmarking

### Timing Operations

```python
import time

# Simple timing
start = time.time()
result = df.groupby('category')['value'].mean()
elapsed = time.time() - start
print(f"Elapsed: {elapsed:.4f} seconds")

# Using %%timeit in Jupyter
# %%timeit
# df.groupby('category')['value'].mean()
```

### Memory Profiling

```python
# Track memory before/after
import tracemalloc

tracemalloc.start()

# Your operation
df_result = df.groupby('category').agg({'value': 'sum'})

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1e6:.2f} MB")
print(f"Peak memory: {peak / 1e6:.2f} MB")

tracemalloc.stop()
```

### Comparison Template

```python
def benchmark_operations(df: pd.DataFrame, operations: dict, n_runs: int = 5):
    """Benchmark multiple operations."""
    results = {}

    for name, func in operations.items():
        times = []
        for _ in range(n_runs):
            start = time.time()
            func(df)
            times.append(time.time() - start)

        results[name] = {
            'mean': np.mean(times),
            'std': np.std(times),
            'min': np.min(times),
        }

    return pd.DataFrame(results).T

# Usage
operations = {
    'iterrows': lambda df: [row['value'] for _, row in df.iterrows()],
    'itertuples': lambda df: [row.value for row in df.itertuples()],
    'vectorized': lambda df: df['value'].tolist(),
}

benchmark_results = benchmark_operations(df.head(10000), operations)
print(benchmark_results)
```

---

## Best Practices Summary

1. **Profile first** - Identify actual bottlenecks before optimizing
2. **Use appropriate dtypes** - int32/float32/category save memory
3. **Vectorize everything** - Avoid loops and apply when possible
4. **Filter early** - Reduce data before expensive operations
5. **Chunk large files** - Process in manageable pieces
6. **Use efficient file formats** - Parquet/Feather over CSV
7. **Leverage built-in methods** - Faster than custom functions

---

## Performance Checklist

Before deploying pandas code:

- [ ] Memory profiled with `memory_usage(deep=True)`
- [ ] Dtypes optimized (downcast, categorical)
- [ ] No iterrows/itertuples in hot paths
- [ ] GroupBy uses built-in aggregations
- [ ] Large files processed in chunks
- [ ] Filters applied before computations
- [ ] Appropriate file format used
- [ ] Benchmarked with representative data size

---

## Anti-Patterns Summary

| Anti-Pattern | Alternative |
|--------------|-------------|
| `iterrows()` for computation | Vectorized operations |
| `apply(lambda)` for simple ops | Built-in methods |
| Loading entire large file | Chunked reading |
| String columns with low cardinality | Category dtype |
| int64 for small integers | int32/int16 |
| Multiple separate filters | Combined boolean mask |
| Repeated groupby calls | Single groupby with multiple aggs |

---

## Related References

- `dataframe-operations.md` - Efficient indexing and filtering
- `aggregation-groupby.md` - Optimized aggregation patterns
- `merging-joining.md` - Efficient merge strategies
