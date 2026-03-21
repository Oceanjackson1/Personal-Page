---
title: "Scientific Visualization"
description: "Meta-skill for publication-ready figures. Use when creating journal submission figures requiring multi-panel layouts, significance annotations, error bars, colorblind-safe palettes, and specific journal formatting (Nature, Science, Cell). Orchestr..."
category: "research"
source: "community"
author: "Community"
tags: ["scientific", "visualization"]
date: 2026-03-20
---

# Scientific Visualization

## Overview

Scientific visualization transforms data into clear, accurate figures for publication. Create journal-ready plots with multi-panel layouts, error bars, significance markers, and colorblind-safe palettes. Export as PDF/EPS/TIFF using matplotlib, seaborn, and plotly for manuscripts.

## When to Use This Skill

This skill should be used when:
- Creating plots or visualizations for scientific manuscripts
- Preparing figures for journal submission (Nature, Science, Cell, PLOS, etc.)
- Ensuring figures are colorblind-friendly and accessible
- Making multi-panel figures with consistent styling
- Exporting figures at correct resolution and format
- Following specific publication guidelines
- Improving existing figures to meet publication standards
- Creating figures that need to work in both color and grayscale

## Quick Start Guide

### Basic Publication-Quality Figure

```python
import matplotlib.pyplot as plt
import numpy as np

# Apply publication style (from scripts/style_presets.py)
from style_presets import apply_publication_style
apply_publication_style('default')

# Create figure with appropriate size (single column = 3.5 inches)
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Plot data
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Proper labeling with units
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude (mV)')
ax.legend(frameon=False)

# Remove unnecessary spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Save in publication formats (from scripts/figure_export.py)
from figure_export import save_publication_figure
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
```

### Using Pre-configured Styles

Apply journal-specific styles using the matplotlib style files in `assets/`:

```python
import matplotlib.pyplot as plt

# Option 1: Use style file directly
plt.style.use('assets/nature.mplstyle')

# Option 2: Use style_presets.py helper
from style_presets import configure_for_journal
configure_for_journal('nature', figure_width='single')

# Now create figures - they'll automatically match Nature specifications
fig, ax = plt.subplots()
# ... your plotting code ...
```

### Quick Start with Seaborn

For statistical plots, use seaborn with publication styling:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from style_presets import apply_publication_style

# Apply publication style
apply_publication_style('default')
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
sns.set_palette('colorblind')

# Create statistical comparison figure
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x='treatment', y='response', 
            order=['Control', 'Low', 'High'], palette='Set2', ax=ax)
sns.stripplot(data=df, x='treatment', y='response',
              order=['Control', 'Low', 'High'], 
              color='black', alpha=0.3, size=3, ax=ax)
ax.set_ylabel('Response (μM)')
sns.despine()

# Save figure
from figure_export import save_publication_figure
save_publication_figure(fig, 'treatment_comparison', formats=['pdf', 'png'], dpi=300)
```

## Core Principles and Best Practices

### 1. Resolution and File Format

**Critical requirements** (detailed in `references/publication_guidelines.md`):
- **Raster images** (photos, microscopy): 300-600 DPI
- **Line art** (graphs, plots): 600-1200 DPI or vector format
- **Vector formats** (preferred): PDF, EPS, SVG
- **Raster formats**: TIFF, PNG (never JPEG for scientific data)

**Implementation:**
```python
# Use the figure_export.py script for correct settings
from figure_export import save_publication_figure

# Saves in multiple formats with proper DPI
save_publication_figure(fig, 'myfigure', formats=['pdf', 'png'], dpi=300)

# Or save for specific journal requirements
from figure_export import save_for_journal
save_for_journal(fig, 'figure1', journal='nature', figure_type='combination')
```

### 2. Color Selection - Colorblind Accessibility

**Always use colorblind-friendly palettes** (detailed in `references/color_palettes.md`):

**Recommended: Okabe-Ito palette** (distinguishable by all types of color blindness):
```python
# Option 1: Use assets/color_palettes.py
from color_palettes import OKABE_ITO_LIST, apply_palette
apply_palette('okabe_ito')

# Option 2: Manual specification
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=okabe_ito)
```

**For heatmaps/continuous data:**
- Use perceptually uniform colormaps: `viridis`, `plasma`, `cividis`
- Avoid red-green diverging maps (use `PuOr`, `RdBu`, `BrBG` instead)
- Never use `jet` or `rainbow` colormaps

**Always test figures in grayscale** to ensure interpretability.

### 3. Typography and Text

**Font guidelines** (detailed in `references/publication_guidelines.md`):
- Sans-serif fonts: Arial, Helvetica, Calibri
- Minimum sizes at **final print size**:
  - Axis labels: 7-9 pt
  - Tick labels: 6-8 pt
  - Panel labels: 8-12 pt (bold)
- Sentence case for labels: "Time (hours)" not "TIME (HOURS)"
- Always include units in parentheses

**Implementation:**
```python
# Set fonts globally
import matplotlib as mpl
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 9
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
```

### 4. Figure Dimensions

**Journal-specific widths** (detailed in `references/journal_requirements.md`):
- **Nature**: Single 89 mm, Double 183 mm
- **Science**: Single 55 mm, Double 175 mm
- **Cell**: Single 85 mm, Double 178 mm

**Check figure size compliance:**
```python
from figure_export import check_figure_size

fig = plt.figure(figsize=(3.5, 3))  # 89 mm for Nature
check_figure_size(fig, journal='nature')
```

### 5. Multi-Panel Figures

**Best practices:**
- Label panels with bold letters: **A**, **B**, **C** (uppercase for most journals, lowercase for Nature)
- Maintain consistent styling across all panels
- Align panels along edges where possible
- Use adequate white space between panels

**Example implementation** (see `references/matplotlib_examples.md` for complete code):
```python
from string import ascii_uppercase

fig = plt.figure(figsize=(7, 4))
gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
# ... create other panels ...

# Add panel labels
for i, ax in enumerate([ax1, ax2, ...]):
    ax.text(-0.15, 1.05, ascii_uppercase[i], transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='top')
```

## Common Tasks

### Task 1: Create a Publication-Ready Line Plot

See `references/matplotlib_examples.md` Example 1 for complete code.

**Key steps:**
1. Apply publication style
2. Set appropriate figure size for target journal
3. Use colorblind-friendly colors
4. Add error bars with correct representation (SEM, SD, or CI)
5. Label axes with units
6. Remove unnecessary spines
7. Save in vector format

**Using seaborn for automatic confidence intervals:**
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(data=timeseries, x='time', y='measurement',
             hue='treatment', errorbar=('ci', 95), 
             markers=True, ax=ax)
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Measurement (AU)')
sns.despine()
```

### Task 2: Create a Multi-Panel Figure

See `references/matplotlib_examples.md` Example 2 for complete code.

**Key steps:**
1. Use `GridSpec` for flexible layout
2. Ensure consistent styling across panels
3. Add bold panel labels (A, B, C, etc.)
4. Align related panels
5. Verify all text is readable at final size

### Task 3: Create a Heatmap with Proper Colormap

See `references/matplotlib_examples.md` Example 4 for complete code.

**Key steps:**
1. Use perceptually uniform colormap (`viridis`, `plasma`, `cividis`)
2. Include labeled colorbar
3. For diverging data, use colorblind-safe diverging map (`RdBu_r`, `PuOr`)
4. Set appropriate center value for diverging maps
5. Test appearance in grayscale

**Using seaborn for correlation matrices:**
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 4))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, square=True,
            linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
```

### Task 4: Prepare Figure for Specific Journal

**Workflow:**
1. Check journal requirements: `references/journal_requirements.md`
2. Configure matplotlib for journal:
   ```python
   from style_presets import configure_for_journal
   configure_for_journal('nature', figure_width='single')
   ```
3. Create figure (will auto-size correctly)
4. Export with journal specifications:
   ```python
   from figure_export import save_for_journal
   save_for_journal(fig, 'figure1', journal='nature', figure_type='line_art')
   ```

### Task 5: Fix an Existing Figure to Meet Publication Standards

**Checklist approach** (full checklist in `references/publication_guidelines.md`):

1. **Check resolution**: Verify DPI meets journal requirements
2. **Check file format**: Use vector for plots, TIFF/PNG for images
3. **Check colors**: Ensure colorblind-friendly
4. **Check fonts**: Minimum 6-7 pt at final size, sans-serif
5. **Check labels**: All axes labeled with units
6. **Check size**: Matches journal column width
7. **Test grayscale**: Figure interpretable without color
8. **Remove chart junk**: No unnecessary grids, 3D effects, shadows

### Task 6: Create Colorblind-Friendly Visualizations

**Strategy:**
1. Use approved palettes from `assets/color_palettes.py`
2. Add redundant encoding (line styles, markers, patterns)
3. Test with colorblind simulator
4. Ensure grayscale compatibility

**Example:**
```python
from color_palettes import apply_palette
import matplotlib.pyplot as plt

apply_palette('okabe_ito')

# Add redundant encoding beyond color
line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', '^', 'v']

for i, (data, label) in enumerate(datasets):
    plt.plot(x, data, linestyle=line_styles[i % 4],
             marker=markers[i % 4], label=label)
```

## Statistical Rigor

**Always include:**
- Error bars (SD, SEM, or CI - specify which in caption)
- Sample size (n) in figure or caption
- Statistical significance markers (*, **, ***)
- Individual data points when possible (not just summary statistics)

**Example with statistics:**
```python
# Show individual points with summary statistics
ax.scatter(x_jittered, individual_points, alpha=0.4, s=8)
ax.errorbar(x, means, yerr=sems, fmt='o', capsize=3)

# Mark significance
ax.text(1.5, max_y * 1.1, '***', ha='center', fontsize=8)
```

## Working with Different Plotting Libraries

### Matplotlib
- Most control over publication details
- Best for complex multi-panel figures
- Use provided style files for consistent formatting
- See `references/matplotlib_examples.md` for extensive examples

### Seaborn

Seaborn provides a high-level, dataset-oriented interface for statistical graphics, built on matplotlib. It excels at creating publication-quality statistical visualizations with minimal code while maintaining full compatibility with matplotlib customization.

**Key advantages for scientific visualization:**
- Automatic statistical estimation and confidence intervals
- Built-in support for multi-panel figures (faceting)
- Colorblind-friendly palettes by default
- Dataset-oriented API using pandas DataFrames
- Semantic mapping of variables to visual properties

#### Quick Start with Publication Style

Always apply matplotlib publication styles first, then configure seaborn:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from style_presets import apply_publication_style

# Apply publication style
apply_publication_style('default')

# Configure seaborn for publication
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
sns.set_palette('colorblind')  # Use colorblind-safe palette

# Create figure
fig, ax = plt.subplots(figsize=(3.5, 2.5))
sns.scatterplot(data=df, x='time', y='response', 
                hue='treatment', style='condition', ax=ax)
sns.despine()  # Remove top and right spines
```

#### Common Plot Types for Publications

**Statistical comparisons:**
```python
# Box plot with individual points for transparency
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x='treatment', y='response', 
            order=['Control', 'Low', 'High'], palette='Set2', ax=ax)
sns.stripplot(data=df, x='treatment', y='response',
              order=['Control', 'Low', 'High'], 
              color='black', alpha=0.3, size=3, ax=ax)
ax.set_ylabel('Response (μM)')
sns.despine()
```

**Distribution analysis:**
```python
# Violin plot with split comparison
fig, ax = plt.subplots(figsize=(4, 3))
sns.violinplot(data=df, x='timepoint', y='expression',
               hue='treatment', split=True, inner='quartile', ax=ax)
ax.set_ylabel('Gene Expression (AU)')
sns.despine()
```

**Correlation matrices:**
```python
# Heatmap with proper colormap and annotations
fig, ax = plt.subplots(figsize=(5, 4))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))  # Show only lower triangle
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, square=True,
            linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
plt.tight_layout()
```

**Time series with confidence bands:**
```python
# Line plot with automatic CI calculation
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(data=timeseries, x='time', y='measurement',
             hue='treatment', style='replicate',
             errorbar=('ci', 95), markers=True, dashes=False, ax=ax)
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Measurement (AU)')
sns.despine()
```

#### Multi-Panel Figures with Seaborn

**Using FacetGrid for automatic faceting:**
```python
# Create faceted plot
g = sns.relplot(data=df, x='dose', y='response',
                hue='treatment', col='cell_line', row='timepoint',
                kind='line', height=2.5, aspect=1.2,
                errorbar=('ci', 95), markers=True)
g.set_axis_labels('Dose (μM)', 'Response (AU)')
g.set_titles('{row_name} | {col_name}')
sns.despine()

# Save with correct DPI
from figure_export import save_publication_figure
save_publication_figure(g.figure, 'figure_facets', 
                       formats=['pdf', 'png'], dpi=300)
```

**Combining seaborn with matplotlib subplots:**
```python
# Create custom multi-panel layout
fig, axes = plt.subplots(2, 2, figsize=(7, 6))

# Panel A: Scatter with regression
sns.regplot(data=df, x='predictor', y='response', ax=axes[0, 0])
axes[0, 0].text(-0.15, 1.05, 'A', transform=axes[0, 0].transAxes,
                fontsize=10, fontweight='bold')

# Panel B: Distribution comparison
sns.violinplot(data=df, x='group', y='value', ax=axes[0, 1])
axes[0, 1].text(-0.15, 1.05, 'B', transform=axes[0, 1].transAxes,
                fontsize=10, fontweight='bold')

# Panel C: Heatmap
sns.heatmap(correlation_data, cmap='viridis', ax=axes[1, 0])
axes[1, 0].text(-0.15, 1.05, 'C', transform=axes[1, 0].transAxes,
                fontsize=10, fontweight='bold')

# Panel D: Time series
sns.lineplot(data=timeseries, x='time', y='signal', 
             hue='condition', ax=axes[1, 1])
axes[1, 1].text(-0.15, 1.05, 'D', transform=axes[1, 1].transAxes,
                fontsize=10, fontweight='bold')

plt.tight_layout()
sns.despine()
```

#### Color Palettes for Publications

Seaborn includes several colorblind-safe palettes:

```python
# Use built-in colorblind palette (recommended)
sns.set_palette('colorblind')

# Or specify custom colorblind-safe colors (Okabe-Ito)
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
sns.set_palette(okabe_ito)

# For heatmaps and continuous data
sns.heatmap(data, cmap='viridis')  # Perceptually uniform
sns.heatmap(corr, cmap='RdBu_r', center=0)  # Diverging, centered
```

#### Choosing Between Axes-Level and Figure-Level Functions

**Axes-level functions** (e.g., `scatterplot`, `boxplot`, `heatmap`):
- Use when building custom multi-panel layouts
- Accept `ax=` parameter for precise placement
- Better integration with matplotlib subplots
- More control over figure composition

```python
fig, ax = plt.subplots(figsize=(3.5, 2.5))
sns.scatterplot(data=df, x='x', y='y', hue='group', ax=ax)
```

**Figure-level functions** (e.g., `relplot`, `catplot`, `displot`):
- Use for automatic faceting by categorical variables
- Create complete figures with consistent styling
- Great for exploratory analysis
- Use `height` and `aspect` for sizing

```python
g = sns.relplot(data=df, x='x', y='y', col='category', kind='scatter')
```

#### Statistical Rigor with Seaborn

Seaborn automatically computes and displays uncertainty:

```python
# Line plot: shows mean ± 95% CI by default
sns.lineplot(data=df, x='time', y='value', hue='treatment',
             errorbar=('ci', 95))  # Can change to 'sd', 'se', etc.

# Bar plot: shows mean with bootstrapped CI
sns.barplot(data=df, x='treatment', y='response',
            errorbar=('ci', 95), capsize=0.1)

# Always specify error type in figure caption:
# "Error bars represent 95% confidence intervals"
```

#### Best Practices for Publication-Ready Seaborn Figures

1. **Always set publication theme first:**
   ```python
   sns.set_theme(style='ticks', context='paper', font_scale=1.1)
   ```

2. **Use colorblind-safe palettes:**
   ```python
   sns.set_palette('colorblind')
   ```

3. **Remove unnecessary elements:**
   ```python
   sns.despine()  # Remove top and right spines
   ```

4. **Control figure size appropriately:**
   ```python
   # Axes-level: use matplotlib figsize
   fig, ax = plt.subplots(figsize=(3.5, 2.5))
   
   # Figure-level: use height and aspect
   g = sns.relplot(..., height=3, aspect=1.2)
   ```

5. **Show individual data points when possible:**
   ```python
   sns.boxplot(...)  # Summary statistics
   sns.stripplot(..., alpha=0.3)  # Individual points
   ```

6. **Include proper labels with units:**
   ```python
   ax.set_xlabel('Time (hours)')
   ax.set_ylabel('Expression (AU)')
   ```

7. **Export at correct resolution:**
   ```python
   from figure_export import save_publication_figure
   save_publication_figure(fig, 'figure_name', 
                          formats=['pdf', 'png'], dpi=300)
   ```

#### Advanced Seaborn Techniques

**Pairwise relationships for exploratory analysis:**
```python
# Quick overview of all relationships
g = sns.pairplot(data=df, hue='condition', 
                 vars=['gene1', 'gene2', 'gene3'],
                 corner=True, diag_kind='kde', height=2)
```

**Hierarchical clustering heatmap:**
```python
# Cluster samples and features
g = sns.clustermap(expression_data, method='ward', 
                   metric='euclidean', z_score=0,
                   cmap='RdBu_r', center=0, 
                   figsize=(10, 8), 
                   row_colors=condition_colors,
                   cbar_kws={'label': 'Z-score'})
```

**Joint distributions with marginals:**
```python
# Bivariate distribution with context
g = sns.jointplot(data=df, x='gene1', y='gene2',
                  hue='treatment', kind='scatter',
                  height=6, ratio=4, marginal_kws={'kde': True})
```

#### Common Seaborn Issues and Solutions

**Issue: Legend outside plot area**
```python
g = sns.relplot(...)
g._legend.set_bbox_to_anchor((0.9, 0.5))
```

**Issue: Overlapping labels**
```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

**Issue: Text too small at final size**
```python
sns.set_context('paper', font_scale=1.2)  # Increase if needed
```

#### Additional Resources

For more detailed seaborn information, see:
- `scientific-packages/seaborn/SKILL.md` - Comprehensive seaborn documentation
- `scientific-packages/seaborn/references/examples.md` - Practical use cases
- `scientific-packages/seaborn/references/function_reference.md` - Complete API reference
- `scientific-packages/seaborn/references/objects_interface.md` - Modern declarative API

### Plotly
- Interactive figures for exploration
- Export static images for publication
- Configure for publication quality:
```python
fig.update_layout(
    font=dict(family='Arial, sans-serif', size=10),
    plot_bgcolor='white',
    # ... see matplotlib_examples.md Example 8
)
fig.write_image('figure.png', scale=3)  # scale=3 gives ~300 DPI
```

## Resources

### References Directory

**Load these as needed for detailed information:**

- **`publication_guidelines.md`**: Comprehensive best practices
  - Resolution and file format requirements
  - Typography guidelines
  - Layout and composition rules
  - Statistical rigor requirements
  - Complete publication checklist

- **`color_palettes.md`**: Color usage guide
  - Colorblind-friendly palette specifications with RGB values
  - Sequential and diverging colormap recommendations
  - Testing procedures for accessibility
  - Domain-specific palettes (genomics, microscopy)

- **`journal_requirements.md`**: Journal-specific specifications
  - Technical requirements by publisher
  - File format and DPI specifications
  - Figure dimension requirements
  - Quick reference table

- **`matplotlib_examples.md`**: Practical code examples
  - 10 complete working examples
  - Line plots, bar plots, heatmaps, multi-panel figures
  - Journal-specific figure examples
  - Tips for each library (matplotlib, seaborn, plotly)

### Scripts Directory

**Use these helper scripts for automation:**

- **`figure_export.py`**: Export utilities
  - `save_publication_figure()`: Save in multiple formats with correct DPI
  - `save_for_journal()`: Use journal-specific requirements automatically
  - `check_figure_size()`: Verify dimensions meet journal specs
  - Run directly: `python scripts/figure_export.py` for examples

- **`style_presets.py`**: Pre-configured styles
  - `apply_publication_style()`: Apply preset styles (default, nature, science, cell)
  - `set_color_palette()`: Quick palette switching
  - `configure_for_journal()`: One-command journal configuration
  - Run directly: `python scripts/style_presets.py` to see examples

### Assets Directory

**Use these files in figures:**

- **`color_palettes.py`**: Importable color definitions
  - All recommended palettes as Python constants
  - `apply_palette()` helper function
  - Can be imported directly into notebooks/scripts

- **Matplotlib style files**: Use with `plt.style.use()`
  - `publication.mplstyle`: General publication quality
  - `nature.mplstyle`: Nature journal specifications
  - `presentation.mplstyle`: Larger fonts for posters/slides

## Workflow Summary

**Recommended workflow for creating publication figures:**

1. **Plan**: Determine target journal, figure type, and content
2. **Configure**: Apply appropriate style for journal
   ```python
   from style_presets import configure_for_journal
   configure_for_journal('nature', 'single')
   ```
3. **Create**: Build figure with proper labels, colors, statistics
4. **Verify**: Check size, fonts, colors, accessibility
   ```python
   from figure_export import check_figure_size
   check_figure_size(fig, journal='nature')
   ```
5. **Export**: Save in required formats
   ```python
   from figure_export import save_for_journal
   save_for_journal(fig, 'figure1', 'nature', 'combination')
   ```
6. **Review**: View at final size in manuscript context

## Common Pitfalls to Avoid

1. **Font too small**: Text unreadable when printed at final size
2. **JPEG format**: Never use JPEG for graphs/plots (creates artifacts)
3. **Red-green colors**: ~8% of males cannot distinguish
4. **Low resolution**: Pixelated figures in publication
5. **Missing units**: Always label axes with units
6. **3D effects**: Distorts perception, avoid completely
7. **Chart junk**: Remove unnecessary gridlines, decorations
8. **Truncated axes**: Start bar charts at zero unless scientifically justified
9. **Inconsistent styling**: Different fonts/colors across figures in same manuscript
10. **No error bars**: Always show uncertainty

## Final Checklist

Before submitting figures, verify:

- [ ] Resolution meets journal requirements (300+ DPI)
- [ ] File format is correct (vector for plots, TIFF for images)
- [ ] Figure size matches journal specifications
- [ ] All text readable at final size (≥6 pt)
- [ ] Colors are colorblind-friendly
- [ ] Figure works in grayscale
- [ ] All axes labeled with units
- [ ] Error bars present with definition in caption
- [ ] Panel labels present and consistent
- [ ] No chart junk or 3D effects
- [ ] Fonts consistent across all figures
- [ ] Statistical significance clearly marked
- [ ] Legend is clear and complete

Use this skill to ensure scientific figures meet the highest publication standards while remaining accessible to all readers.

---

## Reference: Color_Palettes

# Scientific Color Palettes and Guidelines

## Overview

Color choice in scientific visualization is critical for accessibility, clarity, and accurate data representation. This reference provides colorblind-friendly palettes and best practices for color usage.

## Colorblind-Friendly Palettes

### Okabe-Ito Palette (Recommended for Categories)

The Okabe-Ito palette is specifically designed to be distinguishable by people with all forms of color blindness.

```python
# Okabe-Ito colors (RGB values)
okabe_ito = {
    'orange': '#E69F00',      # RGB: (230, 159, 0)
    'sky_blue': '#56B4E9',    # RGB: (86, 180, 233)
    'bluish_green': '#009E73', # RGB: (0, 158, 115)
    'yellow': '#F0E442',      # RGB: (240, 228, 66)
    'blue': '#0072B2',        # RGB: (0, 114, 178)
    'vermillion': '#D55E00',  # RGB: (213, 94, 0)
    'reddish_purple': '#CC79A7', # RGB: (204, 121, 167)
    'black': '#000000'        # RGB: (0, 0, 0)
}
```

**Usage in Matplotlib:**
```python
import matplotlib.pyplot as plt

colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
          '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
```

**Usage in Seaborn:**
```python
import seaborn as sns

okabe_ito_palette = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                      '#0072B2', '#D55E00', '#CC79A7']
sns.set_palette(okabe_ito_palette)
```

**Usage in Plotly:**
```python
import plotly.graph_objects as go

okabe_ito_plotly = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                     '#0072B2', '#D55E00', '#CC79A7']
fig = go.Figure()
# Apply to discrete color scale
```

### Wong Palette (Alternative for Categories)

Another excellent colorblind-friendly palette by Bang Wong (Nature Methods).

```python
wong_palette = {
    'black': '#000000',
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermillion': '#D55E00',
    'purple': '#CC79A7'
}
```

### Paul Tol Palettes

Paul Tol has designed multiple scientifically-optimized palettes for different use cases.

**Bright Palette (up to 7 categories):**
```python
tol_bright = ['#4477AA', '#EE6677', '#228833', '#CCBB44',
              '#66CCEE', '#AA3377', '#BBBBBB']
```

**Muted Palette (up to 9 categories):**
```python
tol_muted = ['#332288', '#88CCEE', '#44AA99', '#117733',
             '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499']
```

**High Contrast (3 categories only):**
```python
tol_high_contrast = ['#004488', '#DDAA33', '#BB5566']
```

## Sequential Colormaps (Continuous Data)

Sequential colormaps represent data from low to high values with a single hue.

### Perceptually Uniform Colormaps

These colormaps have uniform perceptual change across the color scale.

**Viridis (default in Matplotlib):**
- Colorblind-friendly
- Prints well in grayscale
- Perceptually uniform
```python
plt.imshow(data, cmap='viridis')
```

**Cividis:**
- Optimized for colorblind viewers
- Designed specifically for deuteranopia/protanopia
```python
plt.imshow(data, cmap='cividis')
```

**Plasma, Inferno, Magma:**
- Perceptually uniform alternatives to viridis
- Good for different aesthetic preferences
```python
plt.imshow(data, cmap='plasma')
```

### When to Use Sequential Maps
- Heatmaps showing intensity
- Geographic elevation data
- Probability distributions
- Any single-variable continuous data (low → high)

## Diverging Colormaps (Negative to Positive)

Diverging colormaps have a neutral middle color with two contrasting colors at extremes.

### Colorblind-Safe Diverging Maps

**RdYlBu (Red-Yellow-Blue):**
```python
plt.imshow(data, cmap='RdYlBu_r')  # _r reverses: blue (low) to red (high)
```

**PuOr (Purple-Orange):**
- Excellent for colorblind viewers
```python
plt.imshow(data, cmap='PuOr')
```

**BrBG (Brown-Blue-Green):**
- Good colorblind accessibility
```python
plt.imshow(data, cmap='BrBG')
```

### Avoid These Diverging Maps
- **RdGn (Red-Green)**: Problematic for red-green colorblindness
- **RdYlGn (Red-Yellow-Green)**: Same issue

### When to Use Diverging Maps
- Correlation matrices
- Change/difference data (positive vs. negative)
- Deviation from a central value
- Temperature anomalies

## Special Purpose Palettes

### For Genomics/Bioinformatics

**Sequence type identification:**
```python
# DNA/RNA bases
nucleotide_colors = {
    'A': '#00CC00',  # Green
    'C': '#0000CC',  # Blue
    'G': '#FFB300',  # Orange
    'T': '#CC0000',  # Red
    'U': '#CC0000'   # Red (RNA)
}
```

**Gene expression:**
- Use sequential colormaps (viridis, YlOrRd) for expression levels
- Use diverging colormaps (RdBu) for log2 fold change

### For Microscopy

**Fluorescence channels:**
```python
# Traditional fluorophore colors (use with caution)
fluorophore_colors = {
    'DAPI': '#0000FF',      # Blue - DNA
    'GFP': '#00FF00',       # Green (problematic for colorblind)
    'RFP': '#FF0000',       # Red
    'Cy5': '#FF00FF'        # Magenta
}

# Colorblind-friendly alternatives
fluorophore_alt = {
    'Channel1': '#0072B2',  # Blue
    'Channel2': '#E69F00',  # Orange (instead of green)
    'Channel3': '#D55E00',  # Vermillion
    'Channel4': '#CC79A7'   # Magenta
}
```

## Color Usage Best Practices

### Categorical Data (Qualitative Color Schemes)

**Do:**
- Use distinct, saturated colors from Okabe-Ito or Wong palette
- Limit to 7-8 categories max in one plot
- Use consistent colors for same categories across figures
- Add patterns/markers when colors alone might be insufficient

**Don't:**
- Use red/green combinations
- Use rainbow (jet) colormap for categories
- Use similar hues that are hard to distinguish

### Continuous Data (Sequential/Diverging Schemes)

**Do:**
- Use perceptually uniform colormaps (viridis, plasma, cividis)
- Choose diverging maps when data has meaningful center point
- Include colorbar with labeled ticks
- Test appearance in grayscale

**Don't:**
- Use rainbow (jet) colormap - not perceptually uniform
- Use red-green diverging maps
- Omit colorbar on heatmaps

## Testing for Colorblind Accessibility

### Online Simulators
- **Coblis**: https://www.color-blindness.com/coblis-color-blindness-simulator/
- **Color Oracle**: Free downloadable tool for Windows/Mac/Linux
- **Sim Daltonism**: Mac application

### Types of Color Vision Deficiency
- **Deuteranopia** (~5% of males): Cannot distinguish green
- **Protanopia** (~2% of males): Cannot distinguish red
- **Tritanopia** (<1%): Cannot distinguish blue (rare)

### Python Tools
```python
# Using colorspacious to simulate colorblind vision
from colorspacious import cspace_convert

def simulate_deuteranopia(image_rgb):
    from colorspacious import cspace_convert
    # Convert to colorblind simulation
    # (Implementation would require colorspacious library)
    pass
```

## Implementation Examples

### Setting Global Matplotlib Style
```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set Okabe-Ito as default color cycle
okabe_ito_colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                     '#0072B2', '#D55E00', '#CC79A7']
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=okabe_ito_colors)

# Set default colormap to viridis
mpl.rcParams['image.cmap'] = 'viridis'
```

### Seaborn with Custom Palette
```python
import seaborn as sns

# Set Paul Tol muted palette
tol_muted = ['#332288', '#88CCEE', '#44AA99', '#117733',
             '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499']
sns.set_palette(tol_muted)

# For heatmaps
sns.heatmap(data, cmap='viridis', annot=True)
```

### Plotly with Discrete Colors
```python
import plotly.express as px

# Use Okabe-Ito for categorical data
okabe_ito_plotly = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                     '#0072B2', '#D55E00', '#CC79A7']

fig = px.scatter(df, x='x', y='y', color='category',
                 color_discrete_sequence=okabe_ito_plotly)
```

## Grayscale Compatibility

All figures should remain interpretable in grayscale. Test by converting to grayscale:

```python
# Convert figure to grayscale for testing
fig.savefig('figure_gray.png', dpi=300, colormap='gray')
```

**Strategies for grayscale compatibility:**
1. Use different line styles (solid, dashed, dotted)
2. Use different marker shapes (circles, squares, triangles)
3. Add hatching patterns to bars
4. Ensure sufficient luminance contrast between colors

## Color Spaces

### RGB vs CMYK
- **RGB** (Red, Green, Blue): For digital/screen display
- **CMYK** (Cyan, Magenta, Yellow, Black): For print

**Important:** Colors appear different in print vs. screen. When preparing for print:
1. Convert to CMYK color space
2. Check color appearance in CMYK preview
3. Ensure sufficient contrast remains

### Matplotlib Color Spaces
```python
# Save for print (CMYK)
# Note: Direct CMYK support limited; use PDF and let publisher convert
fig.savefig('figure.pdf', dpi=300)

# For RGB (digital)
fig.savefig('figure.png', dpi=300)
```

## Common Mistakes

1. **Using jet/rainbow colormap**: Not perceptually uniform; avoid
2. **Red-green combinations**: ~8% of males cannot distinguish
3. **Too many colors**: More than 7-8 becomes difficult to distinguish
4. **Inconsistent color meaning**: Same color should mean same thing across figures
5. **Missing colorbar**: Always include for continuous data
6. **Low contrast**: Ensure colors differ sufficiently
7. **Relying solely on color**: Add texture, patterns, or markers

## Resources

- **ColorBrewer**: http://colorbrewer2.org/ - Choose palettes by colorblind-safe option
- **Paul Tol's palettes**: https://personal.sron.nl/~pault/
- **Okabe-Ito palette origin**: "Color Universal Design" (Okabe & Ito, 2008)
- **Matplotlib colormaps**: https://matplotlib.org/stable/tutorials/colors/colormaps.html
- **Seaborn palettes**: https://seaborn.pydata.org/tutorial/color_palettes.html

---

## Reference: Journal_Requirements

# Journal-Specific Figure Requirements

## Overview

Different journals have specific technical requirements for figures. This reference compiles common requirements from major scientific publishers. **Always check the specific journal's author guidelines for the most current requirements.**

## Nature Portfolio (Nature, Nature Methods, etc.)

### Technical Specifications
- **File formats**:
  - Vector: PDF, EPS, AI (preferred for graphs)
  - Raster: TIFF, PNG (for images)
  - Never: PowerPoint, Word, JPEG

- **Resolution**:
  - Line art: 1000-1200 DPI
  - Combination (line art + images): 600 DPI
  - Photographs/microscopy: 300 DPI minimum

- **Color space**: RGB (Nature is digital-first)

- **Dimensions**:
  - Single column: 89 mm (3.5 inches)
  - 1.5 column: 120 mm (4.7 inches)
  - Double column: 183 mm (7.2 inches)
  - Maximum height: 247 mm (9.7 inches)

- **Fonts**:
  - Arial or Helvetica (or similar sans-serif)
  - Minimum 5-7 pt at final size
  - Embed all fonts in PDF/EPS

### Nature Specific Guidelines
- Panel labels: a, b, c (lowercase, bold) in top-left corner
- Scale bars required for microscopy images
- Gel images: Include molecular weight markers
- Cropping: Indicate with line breaks
- Statistics: Mark significance; define symbols in legend
- Source data: Required for all graphs

### File Naming
Format: `FirstAuthorLastName_FigureNumber.ext`
Example: `Smith_Fig1.pdf`

## Science (AAAS)

### Technical Specifications
- **File formats**:
  - Vector: EPS, PDF (preferred)
  - Raster: TIFF
  - Acceptable: AI, PSD (Photoshop)

- **Resolution**:
  - Line art: 1000 DPI minimum
  - Photographs: 300 DPI minimum
  - Combination: 600 DPI minimum

- **Color space**: RGB

- **Dimensions**:
  - Single column: 5.5 cm (2.17 inches)
  - 1.5 column: 12 cm (4.72 inches)
  - Full width: 17.5 cm (6.89 inches)
  - Maximum height: 23.3 cm (9.17 inches)

- **Fonts**:
  - Helvetica (or Arial)
  - 6-8 pt minimum at final size
  - Consistent across all figures

### Science Specific Guidelines
- Panel labels: (A), (B), (C) in parentheses
- Minimal text within figures (details in caption)
- High contrast for web and print
- Error bars required; define in caption
- Avoid excessive whitespace

### File Naming
Format: `Manuscript#_Fig#.ext`
Example: `abn1234_Fig1.eps`

## Cell Press (Cell, Neuron, Molecular Cell, etc.)

### Technical Specifications
- **File formats**:
  - Vector: PDF, EPS (preferred for graphs/diagrams)
  - Raster: TIFF (for photographs)

- **Resolution**:
  - Line art: 1000 DPI
  - Photographs: 300 DPI
  - Combination: 600 DPI

- **Color space**: RGB

- **Dimensions**:
  - Single column: 85 mm (3.35 inches)
  - Double column: 178 mm (7.01 inches)
  - Maximum height: 230 mm (9.06 inches)

- **Fonts**:
  - Arial or Helvetica only
  - 8-12 pt for axis labels
  - 6-8 pt for tick labels

### Cell Press Specific Guidelines
- Panel labels: (A), (B), (C) or A, B, C in top-left
- Related panels should match in size
- Scale bars mandatory for microscopy
- Western blots: Include molecular weight markers
- Arrows/arrowheads: 2 pt minimum width
- Line widths: 1-2 pt for data

## PLOS (Public Library of Science)

### Technical Specifications
- **File formats**:
  - Vector: EPS, PDF (preferred)
  - Raster: TIFF, PNG
  - TIFF with LZW compression acceptable

- **Resolution**:
  - Minimum 300 DPI at final size (all figure types)
  - 600 DPI preferred for line art

- **Color space**: RGB

- **Dimensions**:
  - Single column: 8.3 cm (3.27 inches)
  - 1.5 column: 11.4 cm (4.49 inches)
  - Double column: 17.3 cm (6.81 inches)
  - Maximum height: 23.3 cm (9.17 inches)

- **Fonts**:
  - Sans-serif preferred (Arial, Helvetica)
  - 8-12 pt for labels at final size

### PLOS Specific Guidelines
- Figures should be understandable without caption
- Color required only if adding information
- All figures convertible to grayscale
- Panel labels optional but recommended
- Open access: Figures must be CC-BY licensed
- Source data files encouraged

## ACS (American Chemical Society)

### Technical Specifications
- **File formats**:
  - Preferred: TIFF, PDF, EPS
  - Application files: AI, CDX (ChemDraw), CDL
  - Acceptable: PNG (not for publication)

- **Resolution**:
  - Minimum 300 DPI at final size
  - 600 DPI for line art and chemical structures
  - 1200 DPI for detailed structures

- **Color space**: RGB or CMYK (check specific journal)

- **Dimensions**:
  - Single column: 3.25 inches (8.25 cm)
  - Double column: 7 inches (17.78 cm)

- **Fonts**:
  - Embedded fonts required
  - Consistent sizing across figures

### ACS Specific Guidelines
- Chemical structures: Use ChemDraw or equivalent
- Atom labels: 10-12 pt
- Bond thickness: 2 pt
- Panel labels: Lowercase bold (a, b, c)
- High contrast required (many ACS journals grayscale print)

## Elsevier Journals (varies by journal)

### Technical Specifications
- **File formats**:
  - Vector: EPS, PDF
  - Raster: TIFF, JPEG (only for photographs)

- **Resolution**:
  - Line art: 1000 DPI minimum
  - Photographs: 300 DPI minimum
  - Combination: 600 DPI minimum

- **Color space**: RGB (for online); CMYK (for print journals)

- **Dimensions**: Vary by journal
  - Common single column: 90 mm
  - Common double column: 190 mm

- **Fonts**:
  - Preferred: Arial, Times, Symbol
  - Minimum 6 pt at final size

### Elsevier Specific Guidelines
- Check individual journal guidelines (highly variable)
- Some journals charge for color in print
- Panel labels typically (A), (B), (C) or A, B, C
- Graphical abstract often required (separate from figures)

## IEEE (Engineering/Computer Science)

### Technical Specifications
- **File formats**:
  - Vector: PDF, EPS (preferred)
  - Raster: TIFF, PNG

- **Resolution**:
  - Photographs/graphics: 300 DPI minimum at final size
  - Line art: 600 DPI minimum

- **Color space**: RGB (online); CMYK (print)

- **Dimensions**:
  - Single column: 3.5 inches (8.9 cm)
  - Double column: 7.16 inches (18.2 cm)

- **Fonts**:
  - Sans-serif preferred
  - Minimum 8-10 pt at final size

### IEEE Specific Guidelines
- Figures should be readable in black and white
- Color figures incur no charge (online publication)
- Panel labels: (a), (b), (c) in lowercase
- Captions below figures (not on separate page)
- Use IEEE graphics checker tool before submission

## BMC (BioMed Central) - Open Access

### Technical Specifications
- **File formats**:
  - Any standard format accepted
  - Preferred: TIFF, PDF, EPS, PNG

- **Resolution**:
  - Minimum 600 DPI for line art
  - Minimum 300 DPI for photographs

- **Color space**: RGB

- **Dimensions**:
  - Flexible, but consider readability
  - Maximum width typically 140 mm

- **Fonts**:
  - Embedded and readable

### BMC Specific Guidelines
- Open access: CC-BY license required
- Figure files uploaded separately
- Panel labels as appropriate for field
- Source data encouraged
- Accessibility important (colorblind-friendly)

## Common Requirements Across Journals

### Universal Best Practices
1. **Never use JPEG for graphs/plots**: Compression artifacts
2. **Embed all fonts**: In PDF/EPS files
3. **Layer structure**: Flatten images (merge layers in Photoshop)
4. **RGB vs CMYK**: Most journals now RGB (digital-first)
5. **High resolution**: Always better to start high, reduce if needed
6. **Consistency**: Same style across all figures in manuscript
7. **File size**: Balance quality with reasonable file sizes (typically <10 MB per figure)

### Submitting Figures
- **Initial submission**: Lower resolution often acceptable (for review)
- **Revision/acceptance**: High-resolution required
- **Separate files**: Each figure as separate file
- **File naming**: Clear, systematic naming
- **Supporting information**: May have different requirements

## Quick Reference Table

| Publisher | Single Column | Double Column | Min DPI (photos) | Min DPI (line art) | Preferred Format |
|-----------|---------------|---------------|------------------|-------------------|------------------|
| Nature | 89 mm | 183 mm | 300 | 1000 | EPS, PDF |
| Science | 5.5 cm | 17.5 cm | 300 | 1000 | EPS, PDF |
| Cell Press | 85 mm | 178 mm | 300 | 1000 | EPS, PDF |
| PLOS | 8.3 cm | 17.3 cm | 300 | 600 | EPS, TIFF |
| ACS | 3.25 in | 7 in | 300 | 600 | TIFF, EPS |

## Checking Requirements

### Before Submission Checklist
1. Read journal's author guidelines (figure section)
2. Check file format requirements
3. Verify resolution requirements
4. Confirm size specifications (width × height)
5. Check font requirements
6. Verify color space (RGB vs CMYK)
7. Check panel labeling style
8. Review supplementary materials requirements
9. Confirm file naming conventions
10. Check file size limits

### Useful Tools
- **ImageJ/Fiji**: Check/adjust DPI
- **Adobe Acrobat**: Verify embedded fonts, check PDF properties
- **GIMP**: Free alternative to Photoshop for raster editing
- **Inkscape**: Free vector graphics editor

## Resources

- **Journal websites**: Always check "Author Guidelines" or "Instructions for Authors"
- **Publisher resources**: Many provide templates and tools
- **Format conversion**: Use reputable tools; check output quality
- **Help desks**: Contact journal staff if unclear

## Notes

- Requirements change periodically - always verify current guidelines
- Preprint servers (bioRxiv, arXiv) often have different requirements
- Conference proceedings may have separate requirements
- Some journals offer figure preparation services (often paid)
- Supplementary figures may have relaxed requirements compared to main text figures

---

## Reference: Matplotlib_Examples

# Publication-Ready Matplotlib Examples

## Overview

This reference provides practical code examples for creating publication-ready scientific figures using Matplotlib, Seaborn, and Plotly. All examples follow best practices from `publication_guidelines.md` and use colorblind-friendly palettes from `color_palettes.md`.

## Setup and Configuration

### Publication-Quality Matplotlib Configuration

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Set publication quality parameters
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.size'] = 8
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
mpl.rcParams['axes.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 9
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
mpl.rcParams['legend.fontsize'] = 7
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['lines.linewidth'] = 1.5

# Use colorblind-friendly colors (Okabe-Ito palette)
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=okabe_ito)

# Use perceptually uniform colormap
mpl.rcParams['image.cmap'] = 'viridis'
```

### Helper Function for Saving

```python
def save_publication_figure(fig, filename, formats=['pdf', 'png'], dpi=300):
    """
    Save figure in multiple formats for publication.

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure to save
    filename : str
        Base filename (without extension)
    formats : list
        List of file formats to save ['pdf', 'png', 'eps', 'svg']
    dpi : int
        Resolution for raster formats
    """
    for fmt in formats:
        output_file = f"{filename}.{fmt}"
        fig.savefig(output_file, dpi=dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none',
                   transparent=False, format=fmt)
        print(f"Saved: {output_file}")
```

## Example 1: Line Plot with Error Bars

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
x = np.linspace(0, 10, 50)
y1 = 2 * x + 1 + np.random.normal(0, 1, 50)
y2 = 1.5 * x + 2 + np.random.normal(0, 1.2, 50)

# Calculate means and standard errors for binned data
bins = np.linspace(0, 10, 11)
y1_mean = [y1[(x >= bins[i]) & (x < bins[i+1])].mean() for i in range(len(bins)-1)]
y1_sem = [y1[(x >= bins[i]) & (x < bins[i+1])].std() /
          np.sqrt(len(y1[(x >= bins[i]) & (x < bins[i+1])]))
          for i in range(len(bins)-1)]
x_binned = (bins[:-1] + bins[1:]) / 2

# Create figure with appropriate size (single column width = 3.5 inches)
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Plot with error bars
ax.errorbar(x_binned, y1_mean, yerr=y1_sem,
            marker='o', markersize=4, capsize=3, capthick=0.5,
            label='Condition A', linewidth=1.5)

# Add labels with units
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Fluorescence intensity (a.u.)')

# Add legend
ax.legend(frameon=False, loc='upper left')

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Tight layout
fig.tight_layout()

# Save
save_publication_figure(fig, 'line_plot_with_errors')
plt.show()
```

## Example 2: Multi-Panel Figure

```python
import matplotlib.pyplot as plt
import numpy as np
from string import ascii_uppercase

# Create figure with multiple panels (double column width = 7 inches)
fig = plt.figure(figsize=(7, 4))

# Define grid for panels
gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.4,
                      left=0.08, right=0.98, top=0.95, bottom=0.08)

# Panel A: Line plot
ax_a = fig.add_subplot(gs[0, :2])
x = np.linspace(0, 10, 100)
for i, offset in enumerate([0, 0.5, 1.0]):
    ax_a.plot(x, np.sin(x) + offset, label=f'Dataset {i+1}')
ax_a.set_xlabel('Time (s)')
ax_a.set_ylabel('Amplitude (V)')
ax_a.legend(frameon=False, fontsize=6)
ax_a.spines['top'].set_visible(False)
ax_a.spines['right'].set_visible(False)

# Panel B: Bar plot
ax_b = fig.add_subplot(gs[0, 2])
categories = ['Control', 'Treatment\nA', 'Treatment\nB']
values = [100, 125, 140]
errors = [5, 8, 6]
ax_b.bar(categories, values, yerr=errors, capsize=3,
         color=['#0072B2', '#E69F00', '#009E73'], alpha=0.8)
ax_b.set_ylabel('Response (%)')
ax_b.spines['top'].set_visible(False)
ax_b.spines['right'].set_visible(False)
ax_b.set_ylim(0, 160)

# Panel C: Scatter plot
ax_c = fig.add_subplot(gs[1, 0])
x = np.random.randn(100)
y = 2*x + np.random.randn(100)
ax_c.scatter(x, y, s=10, alpha=0.6, color='#0072B2')
ax_c.set_xlabel('Variable X')
ax_c.set_ylabel('Variable Y')
ax_c.spines['top'].set_visible(False)
ax_c.spines['right'].set_visible(False)

# Panel D: Heatmap
ax_d = fig.add_subplot(gs[1, 1:])
data = np.random.randn(10, 20)
im = ax_d.imshow(data, cmap='viridis', aspect='auto')
ax_d.set_xlabel('Sample number')
ax_d.set_ylabel('Feature')
cbar = plt.colorbar(im, ax=ax_d, fraction=0.046, pad=0.04)
cbar.set_label('Intensity (a.u.)', rotation=270, labelpad=12)

# Add panel labels
panels = [ax_a, ax_b, ax_c, ax_d]
for i, ax in enumerate(panels):
    ax.text(-0.15, 1.05, ascii_uppercase[i], transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='top')

save_publication_figure(fig, 'multi_panel_figure')
plt.show()
```

## Example 3: Box Plot with Individual Points

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
np.random.seed(42)
data = [np.random.normal(100, 15, 30),
        np.random.normal(120, 20, 30),
        np.random.normal(140, 18, 30),
        np.random.normal(110, 22, 30)]

fig, ax = plt.subplots(figsize=(3.5, 3))

# Create box plot
bp = ax.boxplot(data, widths=0.5, patch_artist=True,
                showfliers=False,  # We'll add points manually
                boxprops=dict(facecolor='lightgray', edgecolor='black', linewidth=0.8),
                medianprops=dict(color='black', linewidth=1.5),
                whiskerprops=dict(linewidth=0.8),
                capprops=dict(linewidth=0.8))

# Overlay individual points
colors = ['#0072B2', '#E69F00', '#009E73', '#D55E00']
for i, (d, color) in enumerate(zip(data, colors)):
    # Add jitter to x positions
    x = np.random.normal(i+1, 0.04, size=len(d))
    ax.scatter(x, d, alpha=0.4, s=8, color=color)

# Customize
ax.set_xticklabels(['Control', 'Treatment A', 'Treatment B', 'Treatment C'])
ax.set_ylabel('Cell count')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(50, 200)

fig.tight_layout()
save_publication_figure(fig, 'boxplot_with_points')
plt.show()
```

## Example 4: Heatmap with Colorbar

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate correlation matrix
np.random.seed(42)
n = 10
A = np.random.randn(n, n)
corr_matrix = np.corrcoef(A)

# Create figure
fig, ax = plt.subplots(figsize=(4, 3.5))

# Plot heatmap
im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')

# Add colorbar
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Correlation coefficient', rotation=270, labelpad=15)

# Set ticks and labels
gene_names = [f'Gene{i+1}' for i in range(n)]
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(gene_names, rotation=45, ha='right')
ax.set_yticklabels(gene_names)

# Add grid
ax.set_xticks(np.arange(n)-.5, minor=True)
ax.set_yticks(np.arange(n)-.5, minor=True)
ax.grid(which='minor', color='white', linestyle='-', linewidth=0.5)

fig.tight_layout()
save_publication_figure(fig, 'correlation_heatmap')
plt.show()
```

## Example 5: Seaborn Violin Plot

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Generate sample data
np.random.seed(42)
data = pd.DataFrame({
    'condition': np.repeat(['Control', 'Drug A', 'Drug B'], 50),
    'value': np.concatenate([
        np.random.normal(100, 15, 50),
        np.random.normal(120, 20, 50),
        np.random.normal(140, 18, 50)
    ])
})

# Set style
sns.set_style('ticks')
sns.set_palette(['#0072B2', '#E69F00', '#009E73'])

fig, ax = plt.subplots(figsize=(3.5, 3))

# Create violin plot
sns.violinplot(data=data, x='condition', y='value', ax=ax,
               inner='box', linewidth=0.8)

# Add strip plot
sns.stripplot(data=data, x='condition', y='value', ax=ax,
              size=2, alpha=0.3, color='black')

# Customize
ax.set_xlabel('')
ax.set_ylabel('Expression level (AU)')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.tight_layout()
save_publication_figure(fig, 'violin_plot')
plt.show()
```

## Example 6: Scientific Scatter with Regression

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Generate data with correlation
np.random.seed(42)
x = np.random.randn(100)
y = 2.5 * x + np.random.randn(100) * 0.8

# Calculate regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# Create figure
fig, ax = plt.subplots(figsize=(3.5, 3.5))

# Scatter plot
ax.scatter(x, y, s=15, alpha=0.6, color='#0072B2', edgecolors='none')

# Regression line
x_line = np.array([x.min(), x.max()])
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, 'r-', linewidth=1.5, label=f'y = {slope:.2f}x + {intercept:.2f}')

# Add statistics text
stats_text = f'$R^2$ = {r_value**2:.3f}\n$p$ < 0.001' if p_value < 0.001 else f'$R^2$ = {r_value**2:.3f}\n$p$ = {p_value:.3f}'
ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
        verticalalignment='top', fontsize=7,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray', linewidth=0.5))

# Customize
ax.set_xlabel('Predictor variable')
ax.set_ylabel('Response variable')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.tight_layout()
save_publication_figure(fig, 'scatter_regression')
plt.show()
```

## Example 7: Time Series with Shaded Error

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate time series data
np.random.seed(42)
time = np.linspace(0, 24, 100)
n_replicates = 5

# Simulate multiple replicates
data = np.array([10 * np.exp(-time/10) + np.random.normal(0, 0.5, 100)
                 for _ in range(n_replicates)])

# Calculate mean and SEM
mean = data.mean(axis=0)
sem = data.std(axis=0) / np.sqrt(n_replicates)

# Create figure
fig, ax = plt.subplots(figsize=(4, 2.5))

# Plot mean line
ax.plot(time, mean, linewidth=1.5, color='#0072B2', label='Mean ± SEM')

# Add shaded error region
ax.fill_between(time, mean - sem, mean + sem,
                alpha=0.3, color='#0072B2', linewidth=0)

# Customize
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Concentration (μM)')
ax.legend(frameon=False, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, 24)
ax.set_ylim(0, 12)

fig.tight_layout()
save_publication_figure(fig, 'timeseries_shaded')
plt.show()
```

## Example 8: Plotly Interactive Figure

```python
import plotly.graph_objects as go
import numpy as np

# Generate data
np.random.seed(42)
x = np.random.randn(100)
y = 2*x + np.random.randn(100)
colors = np.random.choice(['Group A', 'Group B'], 100)

# Okabe-Ito colors for Plotly
okabe_ito_plotly = ['#E69F00', '#56B4E9']

# Create figure
fig = go.Figure()

for group, color in zip(['Group A', 'Group B'], okabe_ito_plotly):
    mask = colors == group
    fig.add_trace(go.Scatter(
        x=x[mask], y=y[mask],
        mode='markers',
        name=group,
        marker=dict(size=6, color=color, opacity=0.6)
    ))

# Update layout for publication quality
fig.update_layout(
    width=500,
    height=400,
    font=dict(family='Arial, sans-serif', size=10),
    plot_bgcolor='white',
    xaxis=dict(
        title='Variable X',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=False
    ),
    yaxis=dict(
        title='Variable Y',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=False
    ),
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=0.5
    )
)

# Save as static image (requires kaleido)
fig.write_image('plotly_scatter.png', width=500, height=400, scale=3)  # scale=3 gives ~300 DPI
fig.write_html('plotly_scatter.html')  # Interactive version

fig.show()
```

## Example 9: Grouped Bar Plot with Significance

```python
import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['WT', 'Mutant A', 'Mutant B']
control_means = [100, 85, 70]
control_sem = [5, 6, 5]
treatment_means = [100, 120, 140]
treatment_sem = [6, 8, 9]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(3.5, 3))

# Create bars
bars1 = ax.bar(x - width/2, control_means, width, yerr=control_sem,
               capsize=3, label='Control', color='#0072B2', alpha=0.8)
bars2 = ax.bar(x + width/2, treatment_means, width, yerr=treatment_sem,
               capsize=3, label='Treatment', color='#E69F00', alpha=0.8)

# Add significance markers
def add_significance_bar(ax, x1, x2, y, h, text):
    """Add significance bar between two bars"""
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], linewidth=0.8, c='black')
    ax.text((x1+x2)/2, y+h, text, ha='center', va='bottom', fontsize=7)

# Mark significant differences
add_significance_bar(ax, x[1]-width/2, x[1]+width/2, 135, 3, '***')
add_significance_bar(ax, x[2]-width/2, x[2]+width/2, 155, 3, '***')

# Customize
ax.set_ylabel('Activity (% of WT control)')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(frameon=False, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 180)

# Add note about significance
ax.text(0.98, 0.02, '*** p < 0.001', transform=ax.transAxes,
        ha='right', va='bottom', fontsize=6)

fig.tight_layout()
save_publication_figure(fig, 'grouped_bar_significance')
plt.show()
```

## Example 10: Publication-Ready Figure for Nature

```python
import matplotlib.pyplot as plt
import numpy as np
from string import ascii_lowercase

# Nature specifications: 89mm single column
inch_per_mm = 0.0393701
width_mm = 89
height_mm = 110
figsize = (width_mm * inch_per_mm, height_mm * inch_per_mm)

fig = plt.figure(figsize=figsize)
gs = fig.add_gridspec(3, 2, hspace=0.5, wspace=0.4,
                      left=0.12, right=0.95, top=0.96, bottom=0.08)

# Panel a: Time course
ax_a = fig.add_subplot(gs[0, :])
time = np.linspace(0, 48, 100)
for i, label in enumerate(['Control', 'Treatment']):
    y = (1 + i*0.5) * np.exp(-time/20) * (1 + 0.3*np.sin(time/5))
    ax_a.plot(time, y, linewidth=1.2, label=label)
ax_a.set_xlabel('Time (h)', fontsize=7)
ax_a.set_ylabel('Growth (OD$_{600}$)', fontsize=7)
ax_a.legend(frameon=False, fontsize=6)
ax_a.tick_params(labelsize=6)
ax_a.spines['top'].set_visible(False)
ax_a.spines['right'].set_visible(False)

# Panel b: Bar plot
ax_b = fig.add_subplot(gs[1, 0])
categories = ['A', 'B', 'C']
values = [1.0, 1.5, 2.2]
errors = [0.1, 0.15, 0.2]
ax_b.bar(categories, values, yerr=errors, capsize=2, width=0.6,
         color='#0072B2', alpha=0.8)
ax_b.set_ylabel('Fold change', fontsize=7)
ax_b.tick_params(labelsize=6)
ax_b.spines['top'].set_visible(False)
ax_b.spines['right'].set_visible(False)

# Panel c: Heatmap
ax_c = fig.add_subplot(gs[1, 1])
data = np.random.randn(8, 6)
im = ax_c.imshow(data, cmap='viridis', aspect='auto')
ax_c.set_xlabel('Sample', fontsize=7)
ax_c.set_ylabel('Gene', fontsize=7)
ax_c.tick_params(labelsize=6)

# Panel d: Scatter
ax_d = fig.add_subplot(gs[2, :])
x = np.random.randn(50)
y = 2*x + np.random.randn(50)*0.5
ax_d.scatter(x, y, s=8, alpha=0.6, color='#E69F00')
ax_d.set_xlabel('Expression gene X', fontsize=7)
ax_d.set_ylabel('Expression gene Y', fontsize=7)
ax_d.tick_params(labelsize=6)
ax_d.spines['top'].set_visible(False)
ax_d.spines['right'].set_visible(False)

# Add lowercase panel labels (Nature style)
for i, ax in enumerate([ax_a, ax_b, ax_c, ax_d]):
    ax.text(-0.2, 1.1, f'{ascii_lowercase[i]}', transform=ax.transAxes,
            fontsize=9, fontweight='bold', va='top')

# Save in Nature-preferred format
fig.savefig('nature_figure.pdf', dpi=1000, bbox_inches='tight',
           facecolor='white', edgecolor='none')
fig.savefig('nature_figure.png', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')

plt.show()
```

## Tips for Each Library

### Matplotlib
- Use `fig.tight_layout()` or `constrained_layout=True` to prevent overlapping
- Set DPI to 300-600 for publication
- Use vector formats (PDF, EPS) for line plots
- Embed fonts in PDF/EPS files

### Seaborn
- Built on matplotlib, so all matplotlib customizations work
- Use `sns.set_style('ticks')` or `'whitegrid'` for clean looks
- `sns.despine()` removes top and right spines
- Set custom palette with `sns.set_palette()`

### Plotly
- Great for interactive exploratory analysis
- Export static images with `fig.write_image()` (requires kaleido package)
- Use `scale` parameter to control DPI (scale=3 ≈ 300 DPI)
- Update layout extensively for publication quality

## Common Workflow

1. **Explore with default settings**
2. **Apply publication configuration** (see Setup section)
3. **Create plot with appropriate size** (check journal requirements)
4. **Customize colors** (use colorblind-friendly palettes)
5. **Adjust fonts and line widths** (readable at final size)
6. **Remove chart junk** (top/right spines, excessive grid)
7. **Add clear labels with units**
8. **Test in grayscale**
9. **Save in multiple formats** (PDF for vector, PNG for raster)
10. **Verify in final context** (import into manuscript to check size)

## Resources

- Matplotlib documentation: https://matplotlib.org/
- Seaborn gallery: https://seaborn.pydata.org/examples/index.html
- Plotly documentation: https://plotly.com/python/
- Nature Methods Points of View: Data visualization column archive

---

## Reference: Publication_Guidelines

# Publication-Ready Figure Guidelines

## Core Principles

Scientific figures must be clear, accurate, and accessible. Publication-ready figures follow these fundamental principles:

1. **Clarity**: Information should be immediately understandable
2. **Accuracy**: Data representation must be truthful and unmanipulated
3. **Accessibility**: Figures should be interpretable by all readers, including those with visual impairments
4. **Professional**: Clean, polished appearance suitable for peer-reviewed journals

## Resolution and File Format

### Resolution Requirements
- **Raster images (photos, microscopy)**: 300-600 DPI at final print size
- **Line art and graphs**: 600-1200 DPI (or vector format)
- **Combined figures**: 300-600 DPI

### File Formats
- **Vector formats (preferred for graphs/plots)**: PDF, EPS, SVG
  - Infinitely scalable without quality loss
  - Smaller file sizes for line art
  - Best for: plots, diagrams, schematics

- **Raster formats**: TIFF, PNG (never JPEG for scientific data)
  - Use for: photographs, microscopy, images with continuous tone
  - TIFF: Lossless, widely accepted
  - PNG: Lossless, good for web and supplementary materials
  - **Never use JPEG**: Lossy compression introduces artifacts

### Size Specifications
- **Single column**: 85-90 mm (3.35-3.54 inches) width
- **1.5 column**: 114-120 mm (4.49-4.72 inches) width
- **Double column**: 174-180 mm (6.85-7.08 inches) width
- **Maximum height**: Usually 230-240 mm (9-9.5 inches)

## Typography

### Font Guidelines
- **Font family**: Sans-serif fonts (Arial, Helvetica, Calibri) for most journals
  - Some journals prefer specific fonts (check guidelines)
  - Consistency across all figures in manuscript

- **Font sizes at final print size**:
  - Axis labels: 7-9 pt minimum
  - Tick labels: 6-8 pt minimum
  - Legends: 6-8 pt
  - Panel labels (A, B, C): 8-12 pt, bold
  - Title: Generally avoided in multi-panel figures

- **Font weight**: Regular weight for most text; bold for panel labels only

### Text Best Practices
- Use sentence case for axis labels ("Time (hours)" not "TIME (HOURS)")
- Include units in parentheses
- Avoid abbreviations unless space-constrained (define in caption)
- No text smaller than 5-6 pt at final size

## Color Usage

### Color Selection Principles
1. **Colorblind-friendly**: ~8% of males have color vision deficiency
   - Avoid red/green combinations
   - Use blue/orange, blue/yellow, or add texture/pattern
   - Test with colorblindness simulators

2. **Purposeful color**: Color should convey meaning, not just aesthetics
   - Use color to distinguish categories or highlight key data
   - Maintain consistency across figures (same treatment = same color)

3. **Print considerations**:
   - Colors may appear different in print vs. screen
   - Use CMYK color space for print, RGB for digital
   - Ensure sufficient contrast (especially for grayscale conversion)

### Recommended Color Palettes
- **Qualitative (categories)**: ColorBrewer, Okabe-Ito palette
- **Sequential (low to high)**: Viridis, Cividis, Blues, Oranges
- **Diverging (negative to positive)**: RdBu, PuOr, BrBG (ensure colorblind-safe)

### Grayscale Compatibility
- All figures should be interpretable in grayscale
- Use different line styles (solid, dashed, dotted) and markers
- Add patterns/hatching to bars and areas

## Layout and Composition

### Multi-Panel Figures
- **Panel labels**: Use bold uppercase letters (A, B, C) in top-left corner
- **Spacing**: Adequate white space between panels
- **Alignment**: Align panels along edges or axes where possible
- **Sizing**: Related panels should have consistent sizes
- **Arrangement**: Logical flow (left-to-right, top-to-bottom)

### Plot Elements

#### Axes
- **Axis lines**: 0.5-1 pt thickness
- **Tick marks**: Point inward or outward consistently
- **Tick frequency**: Enough to read values, not cluttered (typically 4-7 major ticks)
- **Axis labels**: Required on all plots; state units
- **Axis ranges**: Start from zero for bar charts (unless scientifically inappropriate)

#### Lines and Markers
- **Line width**: 1-2 pt for data lines; 0.5-1 pt for reference lines
- **Marker size**: 3-6 pt, larger than line width
- **Marker types**: Differentiate when multiple series (circles, squares, triangles)
- **Error bars**: 0.5-1 pt width; include caps if appropriate

#### Legends
- **Position**: Inside plot area if space permits, outside otherwise
- **Frame**: Optional; if used, thin line (0.5 pt)
- **Order**: Match order of data appearance (top to bottom or left to right)
- **Content**: Concise descriptions; full details in caption

### White Space and Margins
- Remove unnecessary white space around plots
- Maintain consistent margins
- `tight_layout()` or `constrained_layout=True` in matplotlib

## Data Representation Best Practices

### Statistical Rigor
- **Error bars**: Always show uncertainty (SD, SEM, CI) and state which in caption
- **Sample size**: Indicate n in figure or caption
- **Significance**: Mark statistical significance clearly (*, **, ***)
- **Replicates**: Show individual data points when possible, not just summary statistics

### Appropriate Chart Types
- **Bar plots**: Comparing discrete categories; always start y-axis at zero
- **Line plots**: Time series or continuous relationships
- **Scatter plots**: Correlation between variables; add regression line if appropriate
- **Box plots**: Distribution comparisons; show outliers
- **Heatmaps**: Matrix data, correlations, expression patterns
- **Violin plots**: Distribution shape comparison (better than box plots for bimodal data)

### Avoiding Distortion
- **No 3D effects**: Distorts perception of values
- **No unnecessary decorations**: No gradients, shadows, or chart junk
- **Consistent scales**: Use same scale for comparable panels
- **No truncated axes**: Unless clearly indicated and scientifically justified
- **Linear vs. log scales**: Choose appropriate scale; always label clearly

## Accessibility

### Colorblind Considerations
- Test with online simulators (e.g., Coblis, Color Oracle)
- Use patterns/textures in addition to color
- Provide alternative representations in supplementary materials if needed

### Visual Impairment
- High contrast between elements
- Thick enough lines (minimum 0.5 pt)
- Clear, uncluttered layouts

### Data Availability
- Include data tables in supplementary materials
- Provide source data files for graphs
- Consider interactive figures for online supplementary materials

## Common Mistakes to Avoid

1. **Font too small**: Text unreadable at final print size
2. **Low resolution**: Pixelated or blurry images
3. **Chart junk**: Unnecessary grid lines, 3D effects, decorations
4. **Poor color choices**: Red/green combinations, low contrast
5. **Missing elements**: No axis labels, no units, no error bars
6. **Inconsistent styling**: Different fonts/sizes within figure or between figures
7. **Data distortion**: Truncated axes, inappropriate scales, 3D effects
8. **JPEG compression**: Artifacts around text and lines
9. **Too much information**: Cramming too many data series into one plot
10. **Inaccessible legends**: Legends outside the figure boundary after export

## Figure Checklist

Before submission, verify:

- [ ] Resolution meets journal requirements (300+ DPI for raster)
- [ ] File format is acceptable (vector for plots, TIFF/PNG for images)
- [ ] Figure dimensions match journal specifications
- [ ] All text is readable at final size (minimum 6-7 pt)
- [ ] Fonts are consistent and embedded (for PDF/EPS)
- [ ] Colors are colorblind-friendly
- [ ] Figure is interpretable in grayscale
- [ ] All axes are labeled with units
- [ ] Error bars or uncertainty indicators are present
- [ ] Statistical significance is marked if applicable
- [ ] Panel labels are present and consistent (A, B, C)
- [ ] Legend is clear and complete
- [ ] No chart junk or unnecessary elements
- [ ] File naming follows journal conventions
- [ ] Figure caption is comprehensive
- [ ] Source data is available

## Journal-Specific Considerations

Always consult the specific journal's author guidelines. Common variations include:

- **Nature journals**: RGB, 300 DPI minimum, specific size requirements
- **Science**: EPS or high-res TIFF, specific font requirements
- **Cell Press**: PDF or EPS preferred, Arial or Helvetica fonts
- **PLOS**: TIFF or EPS, specific color space requirements
- **ACS journals**: Application files (AI, EPS) or high-res TIFF

See `journal_requirements.md` for detailed specifications from major publishers.
