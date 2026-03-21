---
title: "Plotly"
description: "Interactive visualization library. Use when you need hover info, zoom, pan, or web-embeddable charts. Best for dashboards, exploratory analysis, and presentations. For static publication figures use matplotlib or scientific-visualization."
category: "research"
source: "community"
author: "Community"
tags: ["plotly"]
date: 2026-03-20
---

# Plotly

Python graphing library for creating interactive, publication-quality visualizations with 40+ chart types.

## Quick Start

Install Plotly:
```bash
uv pip install plotly
```

Basic usage with Plotly Express (high-level API):
```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13]
})

fig = px.scatter(df, x='x', y='y', title='My First Plot')
fig.show()
```

## Choosing Between APIs

### Use Plotly Express (px)
For quick, standard visualizations with sensible defaults:
- Working with pandas DataFrames
- Creating common chart types (scatter, line, bar, histogram, etc.)
- Need automatic color encoding and legends
- Want minimal code (1-5 lines)

See [reference/plotly-express.md](reference/plotly-express.md) for complete guide.

### Use Graph Objects (go)
For fine-grained control and custom visualizations:
- Chart types not in Plotly Express (3D mesh, isosurface, complex financial charts)
- Building complex multi-trace figures from scratch
- Need precise control over individual components
- Creating specialized visualizations with custom shapes and annotations

See [reference/graph-objects.md](reference/graph-objects.md) for complete guide.

**Note:** Plotly Express returns graph objects Figure, so you can combine approaches:
```python
fig = px.scatter(df, x='x', y='y')
fig.update_layout(title='Custom Title')  # Use go methods on px figure
fig.add_hline(y=10)                     # Add shapes
```

## Core Capabilities

### 1. Chart Types

Plotly supports 40+ chart types organized into categories:

**Basic Charts:** scatter, line, bar, pie, area, bubble

**Statistical Charts:** histogram, box plot, violin, distribution, error bars

**Scientific Charts:** heatmap, contour, ternary, image display

**Financial Charts:** candlestick, OHLC, waterfall, funnel, time series

**Maps:** scatter maps, choropleth, density maps (geographic visualization)

**3D Charts:** scatter3d, surface, mesh, cone, volume

**Specialized:** sunburst, treemap, sankey, parallel coordinates, gauge

For detailed examples and usage of all chart types, see [reference/chart-types.md](reference/chart-types.md).

### 2. Layouts and Styling

**Subplots:** Create multi-plot figures with shared axes:
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=2, cols=2, subplot_titles=('A', 'B', 'C', 'D'))
fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4]), row=1, col=1)
```

**Templates:** Apply coordinated styling:
```python
fig = px.scatter(df, x='x', y='y', template='plotly_dark')
# Built-in: plotly_white, plotly_dark, ggplot2, seaborn, simple_white
```

**Customization:** Control every aspect of appearance:
- Colors (discrete sequences, continuous scales)
- Fonts and text
- Axes (ranges, ticks, grids)
- Legends
- Margins and sizing
- Annotations and shapes

For complete layout and styling options, see [reference/layouts-styling.md](reference/layouts-styling.md).

### 3. Interactivity

Built-in interactive features:
- Hover tooltips with customizable data
- Pan and zoom
- Legend toggling
- Box/lasso selection
- Rangesliders for time series
- Buttons and dropdowns
- Animations

```python
# Custom hover template
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
)

# Add rangeslider
fig.update_xaxes(rangeslider_visible=True)

# Animations
fig = px.scatter(df, x='x', y='y', animation_frame='year')
```

For complete interactivity guide, see [reference/export-interactivity.md](reference/export-interactivity.md).

### 4. Export Options

**Interactive HTML:**
```python
fig.write_html('chart.html')                       # Full standalone
fig.write_html('chart.html', include_plotlyjs='cdn')  # Smaller file
```

**Static Images (requires kaleido):**
```bash
uv pip install kaleido
```

```python
fig.write_image('chart.png')   # PNG
fig.write_image('chart.pdf')   # PDF
fig.write_image('chart.svg')   # SVG
```

For complete export options, see [reference/export-interactivity.md](reference/export-interactivity.md).

## Common Workflows

### Scientific Data Visualization

```python
import plotly.express as px

# Scatter plot with trendline
fig = px.scatter(df, x='temperature', y='yield', trendline='ols')

# Heatmap from matrix
fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='RdBu')

# 3D surface plot
import plotly.graph_objects as go
fig = go.Figure(data=[go.Surface(z=z_data, x=x_data, y=y_data)])
```

### Statistical Analysis

```python
# Distribution comparison
fig = px.histogram(df, x='values', color='group', marginal='box', nbins=30)

# Box plot with all points
fig = px.box(df, x='category', y='value', points='all')

# Violin plot
fig = px.violin(df, x='group', y='measurement', box=True)
```

### Time Series and Financial

```python
# Time series with rangeslider
fig = px.line(df, x='date', y='price')
fig.update_xaxes(rangeslider_visible=True)

# Candlestick chart
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
```

### Multi-Plot Dashboards

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Scatter', 'Bar', 'Histogram', 'Box'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'histogram'}, {'type': 'box'}]]
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=['A', 'B'], y=[1, 2]), row=1, col=2)
fig.add_trace(go.Histogram(x=data), row=2, col=1)
fig.add_trace(go.Box(y=data), row=2, col=2)

fig.update_layout(height=800, showlegend=False)
```

## Integration with Dash

For interactive web applications, use Dash (Plotly's web app framework):

```bash
uv pip install dash
```

```python
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

fig = px.scatter(df, x='x', y='y')

app.layout = html.Div([
    html.H1('Dashboard'),
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)
```

## Reference Files

- **[plotly-express.md](reference/plotly-express.md)** - High-level API for quick visualizations
- **[graph-objects.md](reference/graph-objects.md)** - Low-level API for fine-grained control
- **[chart-types.md](reference/chart-types.md)** - Complete catalog of 40+ chart types with examples
- **[layouts-styling.md](reference/layouts-styling.md)** - Subplots, templates, colors, customization
- **[export-interactivity.md](reference/export-interactivity.md)** - Export options and interactive features

## Additional Resources

- Official documentation: https://plotly.com/python/
- API reference: https://plotly.com/python-api-reference/
- Community forum: https://community.plotly.com/

---

## Reference: Chart Types

# Plotly Chart Types

Comprehensive guide to chart types organized by category.

## Basic Charts

### Scatter Plots

```python
import plotly.express as px
fig = px.scatter(df, x='x', y='y', color='category', size='size')

# With trendlines
fig = px.scatter(df, x='x', y='y', trendline='ols')
```

### Line Charts

```python
fig = px.line(df, x='date', y='value', color='group')

# Multiple lines from wide-form data
fig = px.line(df, x='date', y=['metric1', 'metric2', 'metric3'])
```

### Bar Charts

```python
# Vertical bars
fig = px.bar(df, x='category', y='value', color='group')

# Horizontal bars
fig = px.bar(df, x='value', y='category', orientation='h')

# Stacked bars
fig = px.bar(df, x='category', y='value', color='group', barmode='stack')

# Grouped bars
fig = px.bar(df, x='category', y='value', color='group', barmode='group')
```

### Pie Charts

```python
fig = px.pie(df, names='category', values='count')

# Donut chart
fig = px.pie(df, names='category', values='count', hole=0.4)
```

### Area Charts

```python
fig = px.area(df, x='date', y='value', color='category')
```

## Statistical Charts

### Histograms

```python
# Basic histogram
fig = px.histogram(df, x='values', nbins=30)

# With marginal plot
fig = px.histogram(df, x='values', marginal='box')  # or 'violin', 'rug'

# 2D histogram
fig = px.density_heatmap(df, x='x', y='y', nbinsx=20, nbinsy=20)
```

### Box Plots

```python
fig = px.box(df, x='category', y='value', color='group')

# Notched box plot
fig = px.box(df, x='category', y='value', notched=True)

# Show all points
fig = px.box(df, x='category', y='value', points='all')
```

### Violin Plots

```python
fig = px.violin(df, x='category', y='value', color='group', box=True, points='all')
```

### Strip/Dot Plots

```python
fig = px.strip(df, x='category', y='value', color='group')
```

### Distribution Plots

```python
# Empirical cumulative distribution
fig = px.ecdf(df, x='value', color='group')

# Marginal distribution
fig = px.scatter(df, x='x', y='y', marginal_x='histogram', marginal_y='box')
```

### Error Bars

```python
fig = px.scatter(df, x='x', y='y', error_y='error', error_x='x_error')

# Using graph_objects for custom error bars
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[1, 2, 3],
    y=[5, 10, 15],
    error_y=dict(
        type='data',
        array=[1, 2, 3],
        visible=True
    )
))
```

## Scientific Charts

### Heatmaps

```python
# From matrix data
fig = px.imshow(z_matrix, color_continuous_scale='Viridis')

# With graph_objects
fig = go.Figure(data=go.Heatmap(
    z=z_matrix,
    x=x_labels,
    y=y_labels,
    colorscale='RdBu'
))
```

### Contour Plots

```python
# 2D contour
fig = px.density_contour(df, x='x', y='y')

# Filled contour
fig = go.Figure(data=go.Contour(
    z=z_matrix,
    contours=dict(
        coloring='heatmap',
        showlabels=True
    )
))
```

### Ternary Plots

```python
fig = px.scatter_ternary(df, a='component_a', b='component_b', c='component_c')
```

### Log Scales

```python
fig = px.scatter(df, x='x', y='y', log_x=True, log_y=True)
```

### Image Display

```python
import plotly.express as px
fig = px.imshow(img_array)  # img_array from PIL, numpy, etc.
```

## Financial Charts

### Candlestick Charts

```python
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
```

### OHLC Charts

```python
fig = go.Figure(data=[go.Ohlc(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
```

### Waterfall Charts

```python
fig = go.Figure(go.Waterfall(
    x=categories,
    y=values,
    measure=['relative', 'relative', 'total', 'relative', 'total']
))
```

### Funnel Charts

```python
fig = px.funnel(df, x='count', y='stage')

# Or with graph_objects
fig = go.Figure(go.Funnel(
    y=['Stage 1', 'Stage 2', 'Stage 3'],
    x=[100, 60, 40]
))
```

### Time Series

```python
fig = px.line(df, x='date', y='price')

# With rangeslider
fig.update_xaxes(rangeslider_visible=True)

# With range selector buttons
fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label='1m', step='month', stepmode='backward'),
            dict(count=6, label='6m', step='month', stepmode='backward'),
            dict(count=1, label='YTD', step='year', stepmode='todate'),
            dict(count=1, label='1y', step='year', stepmode='backward'),
            dict(step='all')
        ])
    )
)
```

## Maps and Geographic

### Scatter Maps

```python
# Geographic projection
fig = px.scatter_geo(df, lat='lat', lon='lon', color='value', size='size')

# Mapbox (requires token for some styles)
fig = px.scatter_mapbox(
    df, lat='lat', lon='lon',
    color='value',
    zoom=10,
    mapbox_style='open-street-map'  # or 'carto-positron', 'carto-darkmatter'
)
```

### Choropleth Maps

```python
# Country-level
fig = px.choropleth(
    df,
    locations='iso_alpha',
    color='value',
    hover_name='country',
    color_continuous_scale='Viridis'
)

# US States
fig = px.choropleth(
    df,
    locations='state_code',
    locationmode='USA-states',
    color='value',
    scope='usa'
)
```

### Density Maps

```python
fig = px.density_mapbox(
    df, lat='lat', lon='lon', z='value',
    radius=10,
    zoom=10,
    mapbox_style='open-street-map'
)
```

## 3D Charts

### 3D Scatter

```python
fig = px.scatter_3d(df, x='x', y='y', z='z', color='category', size='size')
```

### 3D Line

```python
fig = px.line_3d(df, x='x', y='y', z='z', color='group')
```

### 3D Surface

```python
import plotly.graph_objects as go
fig = go.Figure(data=[go.Surface(z=z_matrix, x=x_array, y=y_array)])

fig.update_layout(scene=dict(
    xaxis_title='X',
    yaxis_title='Y',
    zaxis_title='Z'
))
```

### 3D Mesh

```python
fig = go.Figure(data=[go.Mesh3d(
    x=x_coords,
    y=y_coords,
    z=z_coords,
    i=i_indices,
    j=j_indices,
    k=k_indices,
    intensity=intensity_values,
    colorscale='Viridis'
)]
```

### 3D Cone (Vector Field)

```python
fig = go.Figure(data=go.Cone(
    x=x, y=y, z=z,
    u=u, v=v, w=w,
    colorscale='Blues',
    sizemode='absolute',
    sizeref=0.5
))
```

## Hierarchical Charts

### Sunburst

```python
fig = px.sunburst(
    df,
    path=['continent', 'country', 'city'],
    values='population',
    color='value'
)
```

### Treemap

```python
fig = px.treemap(
    df,
    path=['category', 'subcategory', 'item'],
    values='count',
    color='value',
    color_continuous_scale='RdBu'
)
```

### Sankey Diagram

```python
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=['A', 'B', 'C', 'D', 'E'],
        color='blue'
    ),
    link=dict(
        source=[0, 1, 0, 2, 3],
        target=[2, 3, 3, 4, 4],
        value=[8, 4, 2, 8, 4]
    )
)])
```

## Specialized Charts

### Parallel Coordinates

```python
fig = px.parallel_coordinates(
    df,
    dimensions=['dim1', 'dim2', 'dim3', 'dim4'],
    color='target',
    color_continuous_scale='Viridis'
)
```

### Parallel Categories

```python
fig = px.parallel_categories(
    df,
    dimensions=['cat1', 'cat2', 'cat3'],
    color='value'
)
```

### Scatter Matrix (SPLOM)

```python
fig = px.scatter_matrix(
    df,
    dimensions=['col1', 'col2', 'col3', 'col4'],
    color='category'
)
```

### Indicator/Gauge

```python
fig = go.Figure(go.Indicator(
    mode='gauge+number+delta',
    value=75,
    delta={'reference': 60},
    gauge={'axis': {'range': [None, 100]},
           'bar': {'color': 'darkblue'},
           'steps': [
               {'range': [0, 50], 'color': 'lightgray'},
               {'range': [50, 100], 'color': 'gray'}
           ],
           'threshold': {'line': {'color': 'red', 'width': 4},
                        'thickness': 0.75,
                        'value': 90}
    }
))
```

### Table

```python
fig = go.Figure(data=[go.Table(
    header=dict(values=['A', 'B', 'C']),
    cells=dict(values=[col_a, col_b, col_c])
)])
```

## Bioinformatics

### Dendrogram

```python
from plotly.figure_factory import create_dendrogram
fig = create_dendrogram(data_matrix)
```

### Annotated Heatmap

```python
from plotly.figure_factory import create_annotated_heatmap
fig = create_annotated_heatmap(z_matrix, x=x_labels, y=y_labels)
```

### Volcano Plot

```python
# Typically built with scatter plot
fig = px.scatter(
    df,
    x='log2_fold_change',
    y='neg_log10_pvalue',
    color='significant',
    hover_data=['gene_name']
)
fig.add_hline(y=-np.log10(0.05), line_dash='dash')
fig.add_vline(x=-1, line_dash='dash')
fig.add_vline(x=1, line_dash='dash')
```

---

## Reference: Export Interactivity

# Export and Interactivity

## Static Image Export

### Installation

Static image export requires Kaleido:

```bash
uv pip install kaleido
```

Kaleido v1+ requires Chrome/Chromium on your system.

### Supported Formats

- **Raster**: PNG, JPEG, WebP
- **Vector**: SVG, PDF

### Writing to File

```python
import plotly.express as px

fig = px.scatter(df, x='x', y='y')

# Format inferred from extension
fig.write_image('chart.png')
fig.write_image('chart.pdf')
fig.write_image('chart.svg')

# Explicit format
fig.write_image('chart', format='png')
```

### Converting to Bytes

```python
# Get image as bytes
img_bytes = fig.to_image(format='png')

# Display in Jupyter
from IPython.display import Image
Image(img_bytes)

# Save to file manually
with open('chart.png', 'wb') as f:
    f.write(img_bytes)
```

### Customizing Export

```python
fig.write_image(
    'chart.png',
    format='png',
    width=1200,
    height=800,
    scale=2  # Higher resolution
)
```

### Setting Export Defaults

```python
import plotly.io as pio

pio.kaleido.scope.default_format = 'png'
pio.kaleido.scope.default_width = 800
pio.kaleido.scope.default_height = 600
pio.kaleido.scope.default_scale = 2
```

### Exporting Multiple Figures

```python
import plotly.io as pio

# Kaleido v1+ only
pio.write_images(
    fig=[fig1, fig2, fig3],
    file=['chart1.png', 'chart2.png', 'chart3.png']
)
```

## Interactive HTML Export

### Basic Export

```python
# Full standalone HTML
fig.write_html('interactive_chart.html')

# Open in browser
fig.show()
```

### File Size Control

```python
# Full library embedded (~5MB file)
fig.write_html('chart.html', include_plotlyjs=True)

# CDN reference (~2KB file, requires internet)
fig.write_html('chart.html', include_plotlyjs='cdn')

# Local reference (requires plotly.min.js in same directory)
fig.write_html('chart.html', include_plotlyjs='directory')

# No library (for embedding in existing HTML with Plotly.js)
fig.write_html('chart.html', include_plotlyjs=False)
```

### HTML Configuration

```python
fig.write_html(
    'chart.html',
    config={
        'displayModeBar': True,
        'displaylogo': False,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'custom_image',
            'height': 800,
            'width': 1200,
            'scale': 2
        }
    }
)
```

### Embedding in Templates

```python
# Get only the div (no full HTML structure)
html_div = fig.to_html(
    full_html=False,
    include_plotlyjs='cdn',
    div_id='my-plot'
)

# Use in Jinja2 template
template = """
<html>
<body>
    <h1>My Dashboard</h1>
    {{ plot_div | safe }}
</body>
</html>
"""
```

## Interactivity Features

### Built-in Interactions

Plotly figures automatically support:

- **Hover tooltips** - Display data on hover
- **Pan and zoom** - Click and drag to pan, scroll to zoom
- **Box/lasso select** - Select multiple points
- **Legend toggling** - Click to hide/show traces
- **Double-click** - Reset axes

### Hover Customization

```python
# Hover mode
fig.update_layout(
    hovermode='closest'  # 'x', 'y', 'closest', 'x unified', False
)

# Custom hover template
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>' +
                  'Value: %{y:.2f}<br>' +
                  'Extra: %{customdata[0]}<br>' +
                  '<extra></extra>'
)

# Hover data in Plotly Express
fig = px.scatter(
    df, x='x', y='y',
    hover_data={
        'extra_col': True,     # Show column
        'x': ':.2f',           # Format column
        'hidden': False        # Hide column
    },
    hover_name='name_column'   # Bold title
)
```

### Click Events (Dash/FigureWidget)

For web applications, use Dash or FigureWidget for click handling:

```python
# With FigureWidget in Jupyter
import plotly.graph_objects as go

fig = go.FigureWidget(data=[go.Scatter(x=[1, 2, 3], y=[4, 5, 6])])

def on_click(trace, points, selector):
    print(f'Clicked on points: {points.point_inds}')

fig.data[0].on_click(on_click)
fig
```

### Zoom and Pan

```python
# Disable zoom/pan
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)

# Set initial zoom
fig.update_xaxes(range=[0, 10])
fig.update_yaxes(range=[0, 100])

# Constrain zoom
fig.update_xaxes(
    range=[0, 10],
    constrain='domain'
)
```

### Rangeslider (Time Series)

```python
fig = px.line(df, x='date', y='value')

# Add rangeslider
fig.update_xaxes(rangeslider_visible=True)

# Customize rangeslider
fig.update_xaxes(
    rangeslider=dict(
        visible=True,
        thickness=0.05,
        bgcolor='lightgray'
    )
)
```

### Range Selector Buttons

```python
fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label='1m', step='month', stepmode='backward'),
            dict(count=6, label='6m', step='month', stepmode='backward'),
            dict(count=1, label='YTD', step='year', stepmode='todate'),
            dict(count=1, label='1y', step='year', stepmode='backward'),
            dict(step='all', label='All')
        ]),
        x=0.0,
        y=1.0,
        xanchor='left',
        yanchor='top'
    )
)
```

### Buttons and Dropdowns

```python
fig.update_layout(
    updatemenus=[
        dict(
            type='buttons',
            direction='left',
            buttons=list([
                dict(
                    args=[{'type': 'scatter'}],
                    label='Scatter',
                    method='restyle'
                ),
                dict(
                    args=[{'type': 'bar'}],
                    label='Bar',
                    method='restyle'
                )
            ]),
            x=0.1,
            y=1.15
        )
    ]
)
```

### Sliders

```python
fig.update_layout(
    sliders=[
        dict(
            active=0,
            steps=[
                dict(
                    method='update',
                    args=[{'visible': [True, False]},
                          {'title': 'Dataset 1'}],
                    label='Dataset 1'
                ),
                dict(
                    method='update',
                    args=[{'visible': [False, True]},
                          {'title': 'Dataset 2'}],
                    label='Dataset 2'
                )
            ],
            x=0.1,
            y=0,
            len=0.9
        )
    ]
)
```

## Animations

### Using Plotly Express

```python
fig = px.scatter(
    df, x='gdp', y='life_exp',
    animation_frame='year',     # Animate over this column
    animation_group='country',  # Group animated elements
    size='population',
    color='continent',
    hover_name='country',
    log_x=True,
    range_x=[100, 100000],
    range_y=[25, 90]
)

# Customize animation speed
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
```

### Using Graph Objects

```python
import plotly.graph_objects as go

fig = go.Figure(
    data=[go.Scatter(x=[1, 2], y=[1, 2])],
    layout=go.Layout(
        updatemenus=[dict(
            type='buttons',
            buttons=[dict(label='Play',
                         method='animate',
                         args=[None])]
        )]
    ),
    frames=[
        go.Frame(data=[go.Scatter(x=[1, 2], y=[1, 2])]),
        go.Frame(data=[go.Scatter(x=[1, 2], y=[2, 3])]),
        go.Frame(data=[go.Scatter(x=[1, 2], y=[3, 4])])
    ]
)
```

## Displaying Figures

### In Jupyter

```python
# Default renderer
fig.show()

# Specific renderer
fig.show(renderer='notebook')  # or 'jupyterlab', 'colab', 'kaggle'
```

### In Web Browser

```python
fig.show()  # Opens in default browser
```

### In Dash Applications

```python
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

fig = px.scatter(df, x='x', y='y')

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)
```

### Saving and Loading

```python
# Save as JSON
fig.write_json('figure.json')

# Load from JSON
import plotly.io as pio
fig = pio.read_json('figure.json')

# Save as HTML
fig.write_html('figure.html')
```

## Configuration Options

### Display Config

```python
config = {
    'displayModeBar': True,      # Show toolbar
    'displaylogo': False,        # Hide Plotly logo
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],  # Remove buttons
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'custom_image',
        'height': 500,
        'width': 700,
        'scale': 1
    },
    'scrollZoom': True,          # Enable scroll zoom
    'editable': True,            # Enable editing
    'responsive': True           # Responsive sizing
}

fig.show(config=config)
fig.write_html('chart.html', config=config)
```

### Available Config Options

- `displayModeBar`: Show/hide toolbar ('hover', True, False)
- `displaylogo`: Show Plotly logo
- `modeBarButtonsToRemove`: List of buttons to hide
- `modeBarButtonsToAdd`: Custom buttons
- `scrollZoom`: Enable scroll to zoom
- `doubleClick`: Double-click behavior ('reset', 'autosize', 'reset+autosize', False)
- `showAxisDragHandles`: Show axis drag handles
- `editable`: Allow editing
- `responsive`: Responsive sizing

---

## Reference: Graph Objects

# Graph Objects - Low-Level API

The `plotly.graph_objects` module provides fine-grained control over figure construction through Python classes representing Plotly components.

## Core Classes

- **`go.Figure`** - Main figure container
- **`go.FigureWidget`** - Jupyter-compatible interactive widget
- **Trace types** - 40+ chart types (Scatter, Bar, Heatmap, etc.)
- **Layout components** - Axes, annotations, shapes, etc.

## Key Advantages

1. **Data validation** - Helpful error messages for invalid properties
2. **Built-in documentation** - Accessible via docstrings
3. **Flexible syntax** - Dictionary or attribute access
4. **Convenience methods** - `.add_trace()`, `.update_layout()`, etc.
5. **Magic underscore notation** - Compact nested property access
6. **Integrated I/O** - `.show()`, `.write_html()`, `.write_image()`

## Basic Figure Construction

### Creating Empty Figure

```python
import plotly.graph_objects as go

fig = go.Figure()
```

### Adding Traces

```python
# Method 1: Add traces one at a time
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], name='Line 1'))
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[2, 3, 4], name='Line 2'))

# Method 2: Pass data to constructor
fig = go.Figure(data=[
    go.Scatter(x=[1, 2, 3], y=[4, 5, 6], name='Line 1'),
    go.Scatter(x=[1, 2, 3], y=[2, 3, 4], name='Line 2')
])
```

## Common Trace Types

### Scatter (Lines and Markers)

```python
fig.add_trace(go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='lines+markers',  # 'lines', 'markers', 'lines+markers', 'text'
    name='Trace 1',
    line=dict(color='red', width=2, dash='dash'),
    marker=dict(size=10, color='blue', symbol='circle')
))
```

### Bar

```python
fig.add_trace(go.Bar(
    x=['A', 'B', 'C'],
    y=[1, 3, 2],
    name='Bar Chart',
    marker=dict(color='lightblue'),
    text=[1, 3, 2],
    textposition='auto'
))
```

### Heatmap

```python
fig.add_trace(go.Heatmap(
    z=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    x=['A', 'B', 'C'],
    y=['X', 'Y', 'Z'],
    colorscale='Viridis'
))
```

### 3D Scatter

```python
fig.add_trace(go.Scatter3d(
    x=[1, 2, 3],
    y=[4, 5, 6],
    z=[7, 8, 9],
    mode='markers',
    marker=dict(size=5, color='red')
))
```

## Layout Configuration

### Update Layout

```python
fig.update_layout(
    title='Figure Title',
    title_font_size=20,
    xaxis_title='X Axis',
    yaxis_title='Y Axis',
    width=800,
    height=600,
    template='plotly_white',
    showlegend=True,
    hovermode='closest'  # 'x', 'y', 'closest', 'x unified', False
)
```

### Magic Underscore Notation

Compact way to set nested properties:

```python
# Instead of:
fig.update_layout(title=dict(text='Title', font=dict(size=20)))

# Use underscores:
fig.update_layout(
    title_text='Title',
    title_font_size=20
)
```

### Axis Configuration

```python
fig.update_xaxes(
    title='X Axis',
    range=[0, 10],
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    type='log',  # 'linear', 'log', 'date', 'category'
    tickformat='.2f',
    dtick=1  # Tick spacing
)

fig.update_yaxes(
    title='Y Axis',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='black'
)
```

## Updating Traces

```python
# Update all traces
fig.update_traces(
    marker=dict(size=10, opacity=0.7)
)

# Update specific trace
fig.update_traces(
    marker=dict(color='red'),
    selector=dict(name='Line 1')
)

# Update by position
fig.data[0].marker.size = 15
```

## Adding Annotations

```python
fig.add_annotation(
    x=2, y=5,
    text='Important Point',
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor='red',
    ax=40,  # Arrow x offset
    ay=-40  # Arrow y offset
)
```

## Adding Shapes

```python
# Rectangle
fig.add_shape(
    type='rect',
    x0=1, y0=2, x1=3, y1=4,
    line=dict(color='red', width=2),
    fillcolor='lightblue',
    opacity=0.3
)

# Line
fig.add_shape(
    type='line',
    x0=0, y0=0, x1=5, y1=5,
    line=dict(color='green', width=2, dash='dash')
)

# Convenience methods for horizontal/vertical lines
fig.add_hline(y=5, line_dash='dash', line_color='red')
fig.add_vline(x=3, line_dash='dot', line_color='blue')
```

## Figure Structure

Figures follow a tree hierarchy:

```python
fig = go.Figure(data=[trace1, trace2], layout=go.Layout(...))

# Access via dictionary syntax
fig['layout']['title'] = 'New Title'
fig['data'][0]['marker']['color'] = 'red'

# Or attribute syntax
fig.layout.title = 'New Title'
fig.data[0].marker.color = 'red'
```

## Complex Chart Types

### Candlestick

```python
fig.add_trace(go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Stock Price'
))
```

### Sankey Diagram

```python
fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=['A', 'B', 'C', 'D'],
        color='blue'
    ),
    link=dict(
        source=[0, 1, 0, 2],
        target=[2, 3, 3, 3],
        value=[8, 4, 2, 8]
    )
)])
```

### Surface (3D)

```python
fig = go.Figure(data=[go.Surface(
    z=z_data,  # 2D array
    x=x_data,
    y=y_data,
    colorscale='Viridis'
)])
```

## Working with DataFrames

Build traces from pandas DataFrames:

```python
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13]
})

fig = go.Figure()
for group_name, group_df in df.groupby('category'):
    fig.add_trace(go.Scatter(
        x=group_df['x'],
        y=group_df['y'],
        name=group_name,
        mode='lines+markers'
    ))
```

## When to Use Graph Objects

Use graph_objects when:
- Creating chart types not available in Plotly Express
- Building complex multi-trace figures from scratch
- Need precise control over individual components
- Creating specialized visualizations (3D mesh, isosurface, custom shapes)
- Building subplots with mixed chart types

Use Plotly Express when:
- Creating standard charts quickly
- Working with tidy DataFrame data
- Want automatic styling and legends

---

## Reference: Layouts Styling

# Layouts, Styling, and Customization

## Subplots

### Creating Subplots

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Basic grid
fig = make_subplots(rows=2, cols=2)

# Add traces to specific positions
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[1, 3, 2]), row=1, col=2)
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[2, 3, 4]), row=2, col=1)
```

### Subplot Options

```python
fig = make_subplots(
    rows=2, cols=2,

    # Titles
    subplot_titles=('Plot 1', 'Plot 2', 'Plot 3', 'Plot 4'),

    # Custom dimensions
    column_widths=[0.7, 0.3],
    row_heights=[0.4, 0.6],

    # Spacing
    horizontal_spacing=0.1,
    vertical_spacing=0.15,

    # Shared axes
    shared_xaxes=True,  # or 'columns', 'rows', 'all'
    shared_yaxes=False,

    # Trace types (optional, for mixed types)
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'surface'}, {'type': 'table'}]]
)
```

### Mixed Subplot Types

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# 2D and 3D subplots
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'scatter'}, {'type': 'scatter3d'}]]
)

fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4]), row=1, col=1)
fig.add_trace(go.Scatter3d(x=[1, 2], y=[3, 4], z=[5, 6]), row=1, col=2)
```

### Customizing Subplot Axes

```python
# Update specific subplot axes
fig.update_xaxes(title_text='X Label', row=1, col=1)
fig.update_yaxes(title_text='Y Label', range=[0, 100], row=2, col=1)

# Update all x-axes
fig.update_xaxes(showgrid=True, gridcolor='lightgray')
```

### Shared Colorscale

```python
fig = make_subplots(rows=1, cols=2)
fig.add_trace(go.Bar(x=['A', 'B'], y=[1, 2],
                     marker=dict(color=[1, 2], coloraxis='coloraxis')),
              row=1, col=1)
fig.add_trace(go.Bar(x=['C', 'D'], y=[3, 4],
                     marker=dict(color=[3, 4], coloraxis='coloraxis')),
              row=1, col=2)

fig.update_layout(coloraxis=dict(colorscale='Viridis'))
```

## Templates and Themes

### Built-in Templates

```python
import plotly.express as px
import plotly.io as pio

# Available templates
templates = [
    'plotly',          # Default
    'plotly_white',    # White background
    'plotly_dark',     # Dark theme
    'ggplot2',         # ggplot2 style
    'seaborn',         # Seaborn style
    'simple_white',    # Minimal white
    'presentation',    # For presentations
    'xgridoff',        # No x grid
    'ygridoff',        # No y grid
    'gridon',          # Grid on
    'none'             # No styling
]

# Use in Plotly Express
fig = px.scatter(df, x='x', y='y', template='plotly_dark')

# Use in graph_objects
fig.update_layout(template='seaborn')

# Set default template for session
pio.templates.default = 'plotly_white'
```

### Custom Templates

```python
import plotly.graph_objects as go
import plotly.io as pio

# Create custom template
custom_template = go.layout.Template(
    layout=go.Layout(
        font=dict(family='Arial', size=14),
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='white',
        colorway=['#1f77b4', '#ff7f0e', '#2ca02c'],
        title_font_size=20
    )
)

# Register template
pio.templates['custom'] = custom_template

# Use it
fig = px.scatter(df, x='x', y='y', template='custom')
```

## Styling with Plotly Express

### Built-in Arguments

```python
fig = px.scatter(
    df, x='x', y='y',

    # Dimensions
    width=800,
    height=600,

    # Title
    title='Figure Title',

    # Labels
    labels={'x': 'X Axis Label', 'y': 'Y Axis Label'},

    # Colors
    color='category',
    color_discrete_sequence=px.colors.qualitative.Set2,
    color_discrete_map={'A': 'red', 'B': 'blue'},
    color_continuous_scale='Viridis',

    # Ordering
    category_orders={'category': ['A', 'B', 'C']},

    # Template
    template='plotly_white'
)
```

### Setting Defaults

```python
import plotly.express as px

# Session-wide defaults
px.defaults.template = 'plotly_white'
px.defaults.width = 800
px.defaults.height = 600
px.defaults.color_continuous_scale = 'Viridis'
```

## Color Scales

### Discrete Colors

```python
import plotly.express as px

# Named color sequences
color_sequences = [
    px.colors.qualitative.Plotly,
    px.colors.qualitative.D3,
    px.colors.qualitative.G10,
    px.colors.qualitative.Set1,
    px.colors.qualitative.Pastel,
    px.colors.qualitative.Dark2,
]

fig = px.scatter(df, x='x', y='y', color='category',
                color_discrete_sequence=px.colors.qualitative.Set2)
```

### Continuous Colors

```python
# Named continuous scales
continuous_scales = [
    'Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis',  # Perceptually uniform
    'Blues', 'Greens', 'Reds', 'YlOrRd', 'YlGnBu',       # Sequential
    'RdBu', 'RdYlGn', 'Spectral', 'Picnic',              # Diverging
]

fig = px.scatter(df, x='x', y='y', color='value',
                color_continuous_scale='Viridis')

# Reverse scale
fig = px.scatter(df, x='x', y='y', color='value',
                color_continuous_scale='Viridis_r')

# Custom scale
fig = px.scatter(df, x='x', y='y', color='value',
                color_continuous_scale=['blue', 'white', 'red'])
```

### Colorbar Customization

```python
fig.update_coloraxes(
    colorbar=dict(
        title='Value',
        tickmode='linear',
        tick0=0,
        dtick=10,
        len=0.7,           # Length relative to plot
        thickness=20,
        x=1.02             # Position
    )
)
```

## Layout Customization

### Title and Fonts

```python
fig.update_layout(
    title=dict(
        text='Main Title',
        font=dict(size=24, family='Arial', color='darkblue'),
        x=0.5,              # Center title
        xanchor='center'
    ),

    font=dict(
        family='Arial',
        size=14,
        color='black'
    )
)
```

### Margins and Size

```python
fig.update_layout(
    width=1000,
    height=600,

    margin=dict(
        l=50,    # left
        r=50,    # right
        t=100,   # top
        b=50,    # bottom
        pad=10   # padding
    ),

    autosize=True  # Auto-resize to container
)
```

### Background Colors

```python
fig.update_layout(
    plot_bgcolor='#f0f0f0',   # Plot area
    paper_bgcolor='white'      # Figure background
)
```

### Legend

```python
fig.update_layout(
    showlegend=True,

    legend=dict(
        title='Legend Title',
        orientation='h',           # 'h' or 'v'
        x=0.5,                     # Position
        y=-0.2,
        xanchor='center',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=12)
    )
)
```

### Axes

```python
fig.update_xaxes(
    title='X Axis Title',
    title_font=dict(size=16, family='Arial'),

    # Range
    range=[0, 10],
    autorange=True,  # Auto range

    # Grid
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',

    # Ticks
    showticklabels=True,
    tickmode='linear',
    tick0=0,
    dtick=1,
    tickformat='.2f',
    tickangle=-45,

    # Zero line
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='black',

    # Scale
    type='linear',  # 'linear', 'log', 'date', 'category'
)

fig.update_yaxes(
    title='Y Axis Title',
    # ... same options as xaxes
)
```

### Hover Behavior

```python
fig.update_layout(
    hovermode='closest',  # 'x', 'y', 'closest', 'x unified', False
)

# Customize hover template
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
)
```

### Annotations

```python
fig.add_annotation(
    text='Important Note',
    x=2,
    y=5,
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor='red',
    ax=40,  # Arrow x offset
    ay=-40, # Arrow y offset
    font=dict(size=14, color='black'),
    bgcolor='yellow',
    opacity=0.8
)
```

### Shapes

```python
# Rectangle
fig.add_shape(
    type='rect',
    x0=1, y0=2, x1=3, y1=4,
    line=dict(color='red', width=2),
    fillcolor='lightblue',
    opacity=0.3
)

# Circle
fig.add_shape(
    type='circle',
    x0=0, y0=0, x1=1, y1=1,
    line_color='purple'
)

# Convenience methods
fig.add_hline(y=5, line_dash='dash', line_color='red',
              annotation_text='Threshold')
fig.add_vline(x=3, line_dash='dot')
fig.add_vrect(x0=1, x1=2, fillcolor='green', opacity=0.2)
fig.add_hrect(y0=4, y1=6, fillcolor='red', opacity=0.2)
```

## Update Methods

### Update Layout

```python
fig.update_layout(
    title='New Title',
    xaxis_title='X',
    yaxis_title='Y'
)
```

### Update Traces

```python
# Update all traces
fig.update_traces(marker=dict(size=10, opacity=0.7))

# Update with selector
fig.update_traces(
    marker=dict(color='red'),
    selector=dict(mode='markers', name='Series 1')
)
```

### Update Axes

```python
fig.update_xaxes(showgrid=True, gridcolor='lightgray')
fig.update_yaxes(type='log')
```

## Responsive Design

```python
# Auto-resize to container
fig.update_layout(autosize=True)

# Responsive in HTML
fig.write_html('plot.html', config={'responsive': True})
```

---

## Reference: Plotly Express

# Plotly Express - High-Level API

Plotly Express (px) is a high-level interface for creating data visualizations with minimal code (typically 1-5 lines).

## Installation

```bash
uv pip install plotly
```

## Key Advantages

- Concise syntax for common chart types
- Automatic color encoding and legends
- Works seamlessly with pandas DataFrames
- Smart defaults for layout and styling
- Returns graph_objects.Figure for further customization

## Basic Usage Pattern

```python
import plotly.express as px
import pandas as pd

# Most functions follow this pattern
fig = px.chart_type(
    data_frame=df,
    x="column_x",
    y="column_y",
    color="category_column",  # Auto-color by category
    size="size_column",        # Size by values
    title="Chart Title"
)
fig.show()
```

## 40+ Chart Types

### Basic Charts
- `px.scatter()` - Scatter plots with optional trendlines
- `px.line()` - Line charts for time series
- `px.bar()` - Bar charts (vertical/horizontal)
- `px.area()` - Area charts
- `px.pie()` - Pie charts

### Statistical Charts
- `px.histogram()` - Histograms with automatic binning
- `px.box()` - Box plots for distributions
- `px.violin()` - Violin plots
- `px.strip()` - Strip plots
- `px.ecdf()` - Empirical cumulative distribution

### Maps
- `px.scatter_geo()` - Geographic scatter plots
- `px.choropleth()` - Choropleth maps
- `px.scatter_mapbox()` - Mapbox scatter plots
- `px.density_mapbox()` - Density heatmaps on maps

### Specialized
- `px.sunburst()` - Hierarchical sunburst charts
- `px.treemap()` - Treemap visualizations
- `px.funnel()` - Funnel charts
- `px.parallel_coordinates()` - Parallel coordinates
- `px.scatter_matrix()` - Scatter matrix (SPLOM)
- `px.density_heatmap()` - 2D density heatmaps
- `px.density_contour()` - Density contours

### 3D Charts
- `px.scatter_3d()` - 3D scatter plots
- `px.line_3d()` - 3D line plots

## Common Parameters

All Plotly Express functions support these styling parameters:

```python
fig = px.scatter(
    df, x="x", y="y",
    # Dimensions
    width=800,
    height=600,

    # Labels
    title="Figure Title",
    labels={"x": "X Axis", "y": "Y Axis"},

    # Colors
    color="category",
    color_discrete_map={"A": "red", "B": "blue"},
    color_continuous_scale="Viridis",

    # Ordering
    category_orders={"category": ["A", "B", "C"]},

    # Theming
    template="plotly_dark"  # or "simple_white", "seaborn", "ggplot2"
)
```

## Data Format

Plotly Express works with:
- **Long-form data** (tidy): One row per observation
- **Wide-form data**: Multiple columns as separate traces

```python
# Long-form (preferred)
df_long = pd.DataFrame({
    'fruit': ['apple', 'orange', 'apple', 'orange'],
    'contestant': ['A', 'A', 'B', 'B'],
    'count': [1, 3, 2, 4]
})
fig = px.bar(df_long, x='fruit', y='count', color='contestant')

# Wide-form
df_wide = pd.DataFrame({
    'fruit': ['apple', 'orange'],
    'A': [1, 3],
    'B': [2, 4]
})
fig = px.bar(df_wide, x='fruit', y=['A', 'B'])
```

## Trendlines

Add statistical trendlines to scatter plots:

```python
fig = px.scatter(
    df, x="x", y="y",
    trendline="ols",  # "ols", "lowess", "rolling", "ewm", "expanding"
    trendline_options=dict(log_x=True)  # Additional options
)
```

## Faceting (Subplots)

Create faceted plots automatically:

```python
fig = px.scatter(
    df, x="x", y="y",
    facet_row="category_1",    # Separate rows
    facet_col="category_2",    # Separate columns
    facet_col_wrap=3           # Wrap columns
)
```

## Animation

Create animated visualizations:

```python
fig = px.scatter(
    df, x="gdp", y="life_exp",
    animation_frame="year",     # Animate over this column
    animation_group="country",  # Group animated elements
    size="population",
    color="continent",
    hover_name="country"
)
```

## Hover Data

Customize hover tooltips:

```python
fig = px.scatter(
    df, x="x", y="y",
    hover_data={
        "extra_col": True,      # Add column
        "x": ":.2f",            # Format existing
        "hidden_col": False     # Hide column
    },
    hover_name="name_column"    # Bold title in hover
)
```

## Further Customization

Plotly Express returns a `graph_objects.Figure` that can be further customized:

```python
fig = px.scatter(df, x="x", y="y")

# Use graph_objects methods
fig.update_layout(
    title="Custom Title",
    xaxis_title="X Axis",
    font=dict(size=14)
)

fig.update_traces(
    marker=dict(size=10, opacity=0.7)
)

fig.add_hline(y=0, line_dash="dash")
```

## When to Use Plotly Express

Use Plotly Express when:
- Creating standard chart types quickly
- Working with pandas DataFrames
- Need automatic color/size encoding
- Want sensible defaults with minimal code

Use graph_objects when:
- Building custom chart types not in px
- Need fine-grained control over every element
- Creating complex multi-trace figures
- Building specialized visualizations
