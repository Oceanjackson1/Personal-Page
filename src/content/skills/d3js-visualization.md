---
title: "D3js Visualization"
description: "Creating interactive data visualisations using d3.js. This skill should be used when creating custom charts, graphs, network diagrams, geographic visualisations, or any complex SVG-based data visualisation that requires fine-grained control over v..."
category: "development"
source: "community"
author: "Community"
tags: ["d3js", "visualization"]
date: 2026-03-20
---

# D3.js Visualisation

## Overview

This skill provides guidance for creating sophisticated, interactive data visualisations using d3.js. D3.js (Data-Driven Documents) excels at binding data to DOM elements and applying data-driven transformations to create custom, publication-quality visualisations with precise control over every visual element. The techniques work across any JavaScript environment, including vanilla JavaScript, React, Vue, Svelte, and other frameworks.

## When to use d3.js

**Use d3.js for:**
- Custom visualisations requiring unique visual encodings or layouts
- Interactive explorations with complex pan, zoom, or brush behaviours
- Network/graph visualisations (force-directed layouts, tree diagrams, hierarchies, chord diagrams)
- Geographic visualisations with custom projections
- Visualisations requiring smooth, choreographed transitions
- Publication-quality graphics with fine-grained styling control
- Novel chart types not available in standard libraries

**Consider alternatives for:**
- 3D visualisations - use Three.js instead

## Core workflow

### 1. Set up d3.js

Import d3 at the top of your script:

```javascript
import * as d3 from 'd3';
```

Or use the CDN version (7.x):

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
```

All modules (scales, axes, shapes, transitions, etc.) are accessible through the `d3` namespace.

### 2. Choose the integration pattern

**Pattern A: Direct DOM manipulation (recommended for most cases)**
Use d3 to select DOM elements and manipulate them imperatively. This works in any JavaScript environment:

```javascript
function drawChart(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // Select by ID, class, or DOM element

  // Clear previous content
  svg.selectAll("*").remove();

  // Set up dimensions
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };

  // Create scales, axes, and draw visualisation
  // ... d3 code here ...
}

// Call when data changes
drawChart(myData);
```

**Pattern B: Declarative rendering (for frameworks with templating)**
Use d3 for data calculations (scales, layouts) but render elements via your framework:

```javascript
function getChartElements(data) {
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([0, 400]);

  return data.map((d, i) => ({
    x: 50,
    y: i * 30,
    width: xScale(d.value),
    height: 25
  }));
}

// In React: {getChartElements(data).map((d, i) => <rect key={i} {...d} fill="steelblue" />)}
// In Vue: v-for directive over the returned array
// In vanilla JS: Create elements manually from the returned data
```

Use Pattern A for complex visualisations with transitions, interactions, or when leveraging d3's full capabilities. Use Pattern B for simpler visualisations or when your framework prefers declarative rendering.

### 3. Structure the visualisation code

Follow this standard structure in your drawing function:

```javascript
function drawVisualization(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // Or pass a selector/element
  svg.selectAll("*").remove(); // Clear previous render

  // 1. Define dimensions
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 2. Create main group with margins
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 3. Create scales
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]); // Note: inverted for SVG coordinates

  // 4. Create and append axes
  const xAxis = d3.axisBottom(xScale);
  const yAxis = d3.axisLeft(yScale);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(xAxis);

  g.append("g")
    .call(yAxis);

  // 5. Bind data and create visual elements
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
}

// Call when data changes
drawVisualization(myData);
```

### 4. Implement responsive sizing

Make visualisations responsive to container size:

```javascript
function setupResponsiveChart(containerId, data) {
  const container = document.getElementById(containerId);
  const svg = d3.select(`#${containerId}`).append('svg');

  function updateChart() {
    const { width, height } = container.getBoundingClientRect();
    svg.attr('width', width).attr('height', height);

    // Redraw visualisation with new dimensions
    drawChart(data, svg, width, height);
  }

  // Update on initial load
  updateChart();

  // Update on window resize
  window.addEventListener('resize', updateChart);

  // Return cleanup function
  return () => window.removeEventListener('resize', updateChart);
}

// Usage:
// const cleanup = setupResponsiveChart('chart-container', myData);
// cleanup(); // Call when component unmounts or element removed
```

Or use ResizeObserver for more direct container monitoring:

```javascript
function setupResponsiveChartWithObserver(svgElement, data) {
  const observer = new ResizeObserver(() => {
    const { width, height } = svgElement.getBoundingClientRect();
    d3.select(svgElement)
      .attr('width', width)
      .attr('height', height);

    // Redraw visualisation
    drawChart(data, d3.select(svgElement), width, height);
  });

  observer.observe(svgElement.parentElement);
  return () => observer.disconnect();
}
```

## Common visualisation patterns

### Bar chart

```javascript
function drawBarChart(data, svgElement) {
  if (!data || data.length === 0) return;

  const svg = d3.select(svgElement);
  svg.selectAll("*").remove();

  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, innerWidth])
    .padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append("g")
    .call(d3.axisLeft(yScale));

  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.category))
    .attr("y", d => yScale(d.value))
    .attr("width", xScale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", "steelblue");
}

// Usage:
// drawBarChart(myData, document.getElementById('chart'));
```

### Line chart

```javascript
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX); // Smooth curve

g.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "steelblue")
  .attr("stroke-width", 2)
  .attr("d", line);
```

### Scatter plot

```javascript
g.selectAll("circle")
  .data(data)
  .join("circle")
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y))
  .attr("r", d => sizeScale(d.size)) // Optional: size encoding
  .attr("fill", d => colourScale(d.category)) // Optional: colour encoding
  .attr("opacity", 0.7);
```

### Chord diagram

A chord diagram shows relationships between entities in a circular layout, with ribbons representing flows between them:

```javascript
function drawChordDiagram(data) {
  // data format: array of objects with source, target, and value
  // Example: [{ source: 'A', target: 'B', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 600;
  const height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 30;

  // Create matrix from data
  const nodes = Array.from(new Set(data.flatMap(d => [d.source, d.target])));
  const matrix = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));

  data.forEach(d => {
    const i = nodes.indexOf(d.source);
    const j = nodes.indexOf(d.target);
    matrix[i][j] += d.value;
    matrix[j][i] += d.value;
  });

  // Create chord layout
  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .source(d => d.source)
    .target(d => d.target);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10)
    .domain(nodes);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const chords = chord(matrix);

  // Draw ribbons
  g.append("g")
    .attr("fill-opacity", 0.67)
    .selectAll("path")
    .data(chords)
    .join("path")
    .attr("d", ribbon)
    .attr("fill", d => colourScale(nodes[d.source.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.source.index])).darker());

  // Draw groups (arcs)
  const group = g.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(nodes[d.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.index])).darker());

  // Add labels
  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .attr("dy", "0.31em")
    .attr("transform", d => `rotate(${(d.angle * 180 / Math.PI) - 90})translate(${outerRadius + 30})${d.angle > Math.PI ? "rotate(180)" : ""}`)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text((d, i) => nodes[i])
    .style("font-size", "12px");
}
```

### Heatmap

A heatmap uses colour to encode values in a two-dimensional grid, useful for showing patterns across categories:

```javascript
function drawHeatmap(data) {
  // data format: array of objects with row, column, and value
  // Example: [{ row: 'A', column: 'X', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 800;
  const height = 600;
  const margin = { top: 100, right: 30, bottom: 30, left: 100 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Get unique rows and columns
  const rows = Array.from(new Set(data.map(d => d.row)));
  const columns = Array.from(new Set(data.map(d => d.column)));

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Create scales
  const xScale = d3.scaleBand()
    .domain(columns)
    .range([0, innerWidth])
    .padding(0.01);

  const yScale = d3.scaleBand()
    .domain(rows)
    .range([0, innerHeight])
    .padding(0.01);

  // Colour scale for values
  const colourScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.value)]);

  // Draw rectangles
  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.column))
    .attr("y", d => yScale(d.row))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colourScale(d.value));

  // Add x-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(columns)
    .join("text")
    .attr("x", d => xScale(d) + xScale.bandwidth() / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text(d => d)
    .style("font-size", "12px");

  // Add y-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(rows)
    .join("text")
    .attr("x", -10)
    .attr("y", d => yScale(d) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text(d => d)
    .style("font-size", "12px");

  // Add colour legend
  const legendWidth = 20;
  const legendHeight = 200;
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 60},${margin.top})`);

  const legendScale = d3.scaleLinear()
    .domain(colourScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale)
    .ticks(5);

  // Draw colour gradient in legend
  for (let i = 0; i < legendHeight; i++) {
    legend.append("rect")
      .attr("y", i)
      .attr("width", legendWidth)
      .attr("height", 1)
      .attr("fill", colourScale(legendScale.invert(i)));
  }

  legend.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);
}
```

### Pie chart

```javascript
const pie = d3.pie()
  .value(d => d.value)
  .sort(null);

const arc = d3.arc()
  .innerRadius(0)
  .outerRadius(Math.min(width, height) / 2 - 20);

const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

const g = svg.append("g")
  .attr("transform", `translate(${width / 2},${height / 2})`);

g.selectAll("path")
  .data(pie(data))
  .join("path")
  .attr("d", arc)
  .attr("fill", (d, i) => colourScale(i))
  .attr("stroke", "white")
  .attr("stroke-width", 2);
```

### Force-directed network

```javascript
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(100))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(width / 2, height / 2));

const link = g.selectAll("line")
  .data(links)
  .join("line")
  .attr("stroke", "#999")
  .attr("stroke-width", 1);

const node = g.selectAll("circle")
  .data(nodes)
  .join("circle")
  .attr("r", 8)
  .attr("fill", "steelblue")
  .call(d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended));

simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);
  
  node
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);
});

function dragstarted(event) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  event.subject.fx = event.subject.x;
  event.subject.fy = event.subject.y;
}

function dragged(event) {
  event.subject.fx = event.x;
  event.subject.fy = event.y;
}

function dragended(event) {
  if (!event.active) simulation.alphaTarget(0);
  event.subject.fx = null;
  event.subject.fy = null;
}
```

## Adding interactivity

### Tooltips

```javascript
// Create tooltip div (outside SVG)
const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("position", "absolute")
  .style("visibility", "hidden")
  .style("background-color", "white")
  .style("border", "1px solid #ddd")
  .style("padding", "10px")
  .style("border-radius", "4px")
  .style("pointer-events", "none");

// Add to elements
circles
  .on("mouseover", function(event, d) {
    d3.select(this).attr("opacity", 1);
    tooltip
      .style("visibility", "visible")
      .html(`<strong>${d.label}</strong><br/>Value: ${d.value}`);
  })
  .on("mousemove", function(event) {
    tooltip
      .style("top", (event.pageY - 10) + "px")
      .style("left", (event.pageX + 10) + "px");
  })
  .on("mouseout", function() {
    d3.select(this).attr("opacity", 0.7);
    tooltip.style("visibility", "hidden");
  });
```

### Zoom and pan

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 10])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });

svg.call(zoom);
```

### Click interactions

```javascript
circles
  .on("click", function(event, d) {
    // Handle click (dispatch event, update app state, etc.)
    console.log("Clicked:", d);

    // Visual feedback
    d3.selectAll("circle").attr("fill", "steelblue");
    d3.select(this).attr("fill", "orange");

    // Optional: dispatch custom event for your framework/app to listen to
    // window.dispatchEvent(new CustomEvent('chartClick', { detail: d }));
  });
```

## Transitions and animations

Add smooth transitions to visual changes:

```javascript
// Basic transition
circles
  .transition()
  .duration(750)
  .attr("r", 10);

// Chained transitions
circles
  .transition()
  .duration(500)
  .attr("fill", "orange")
  .transition()
  .duration(500)
  .attr("r", 15);

// Staggered transitions
circles
  .transition()
  .delay((d, i) => i * 50)
  .duration(500)
  .attr("cy", d => yScale(d.value));

// Custom easing
circles
  .transition()
  .duration(1000)
  .ease(d3.easeBounceOut)
  .attr("r", 10);
```

## Scales reference

### Quantitative scales

```javascript
// Linear scale
const xScale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

// Log scale (for exponential data)
const logScale = d3.scaleLog()
  .domain([1, 1000])
  .range([0, 500]);

// Power scale
const powScale = d3.scalePow()
  .exponent(2)
  .domain([0, 100])
  .range([0, 500]);

// Time scale
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)])
  .range([0, 500]);
```

### Ordinal scales

```javascript
// Band scale (for bar charts)
const bandScale = d3.scaleBand()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.1);

// Point scale (for line/scatter categories)
const pointScale = d3.scalePoint()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400]);

// Ordinal scale (for colours)
const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
```

### Sequential scales

```javascript
// Sequential colour scale
const colourScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 100]);

// Diverging colour scale
const divScale = d3.scaleDiverging(d3.interpolateRdBu)
  .domain([-10, 0, 10]);
```

## Best practices

### Data preparation

Always validate and prepare data before visualisation:

```javascript
// Filter invalid values
const cleanData = data.filter(d => d.value != null && !isNaN(d.value));

// Sort data if order matters
const sortedData = [...data].sort((a, b) => b.value - a.value);

// Parse dates
const parsedData = data.map(d => ({
  ...d,
  date: d3.timeParse("%Y-%m-%d")(d.date)
}));
```

### Performance optimisation

For large datasets (>1000 elements):

```javascript
// Use canvas instead of SVG for many elements
// Use quadtree for collision detection
// Simplify paths with d3.line().curve(d3.curveStep)
// Implement virtual scrolling for large lists
// Use requestAnimationFrame for custom animations
```

### Accessibility

Make visualisations accessible:

```javascript
// Add ARIA labels
svg.attr("role", "img")
   .attr("aria-label", "Bar chart showing quarterly revenue");

// Add title and description
svg.append("title").text("Quarterly Revenue 2024");
svg.append("desc").text("Bar chart showing revenue growth across four quarters");

// Ensure sufficient colour contrast
// Provide keyboard navigation for interactive elements
// Include data table alternative
```

### Styling

Use consistent, professional styling:

```javascript
// Define colour palettes upfront
const colours = {
  primary: '#4A90E2',
  secondary: '#7B68EE',
  background: '#F5F7FA',
  text: '#333333',
  gridLines: '#E0E0E0'
};

// Apply consistent typography
svg.selectAll("text")
  .style("font-family", "Inter, sans-serif")
  .style("font-size", "12px");

// Use subtle grid lines
g.selectAll(".tick line")
  .attr("stroke", colours.gridLines)
  .attr("stroke-dasharray", "2,2");
```

## Common issues and solutions

**Issue**: Axes not appearing
- Ensure scales have valid domains (check for NaN values)
- Verify axis is appended to correct group
- Check transform translations are correct

**Issue**: Transitions not working
- Call `.transition()` before attribute changes
- Ensure elements have unique keys for proper data binding
- Check that useEffect dependencies include all changing data

**Issue**: Responsive sizing not working
- Use ResizeObserver or window resize listener
- Update dimensions in state to trigger re-render
- Ensure SVG has width/height attributes or viewBox

**Issue**: Performance problems
- Limit number of DOM elements (consider canvas for >1000 items)
- Debounce resize handlers
- Use `.join()` instead of separate enter/update/exit selections
- Avoid unnecessary re-renders by checking dependencies

## Resources

### references/
Contains detailed reference materials:
- `d3-patterns.md` - Comprehensive collection of visualisation patterns and code examples
- `scale-reference.md` - Complete guide to d3 scales with examples
- `colour-schemes.md` - D3 colour schemes and palette recommendations

### assets/

Contains boilerplate templates:

- `chart-template.js` - Starter template for basic chart
- `interactive-template.js` - Template with tooltips, zoom, and interactions
- `sample-data.json` - Example datasets for testing

These templates work with vanilla JavaScript, React, Vue, Svelte, or any other JavaScript environment. Adapt them as needed for your specific framework.

To use these resources, read the relevant files when detailed guidance is needed for specific visualisation types or patterns.

---

## Reference: Colour Schemes

# D3.js Colour Schemes and Palette Recommendations

Comprehensive guide to colour selection in data visualisation with d3.js.

## Built-in categorical colour schemes

### Category10 (default)

```javascript
d3.schemeCategory10
// ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
//  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
```

**Characteristics:**
- 10 distinct colours
- Good colour-blind accessibility
- Default choice for most categorical data
- Balanced saturation and brightness

**Use cases:** General purpose categorical encoding, legend items, multiple data series

### Tableau10

```javascript
d3.schemeTableau10
```

**Characteristics:**
- 10 colours optimised for data visualisation
- Professional appearance
- Excellent distinguishability

**Use cases:** Business dashboards, professional reports, presentations

### Accent

```javascript
d3.schemeAccent
// 8 colours with high saturation
```

**Characteristics:**
- Bright, vibrant colours
- High contrast
- Modern aesthetic

**Use cases:** Highlighting important categories, modern web applications

### Dark2

```javascript
d3.schemeDark2
// 8 darker, muted colours
```

**Characteristics:**
- Subdued palette
- Professional appearance
- Good for dark backgrounds

**Use cases:** Dark mode visualisations, professional contexts

### Paired

```javascript
d3.schemePaired
// 12 colours in pairs of similar hues
```

**Characteristics:**
- Pairs of light and dark variants
- Useful for nested categories
- 12 distinct colours

**Use cases:** Grouped bar charts, hierarchical categories, before/after comparisons

### Pastel1 & Pastel2

```javascript
d3.schemePastel1 // 9 colours
d3.schemePastel2 // 8 colours
```

**Characteristics:**
- Soft, low-saturation colours
- Gentle appearance
- Good for large areas

**Use cases:** Background colours, subtle categorisation, calming visualisations

### Set1, Set2, Set3

```javascript
d3.schemeSet1 // 9 colours - vivid
d3.schemeSet2 // 8 colours - muted
d3.schemeSet3 // 12 colours - pastel
```

**Characteristics:**
- Set1: High saturation, maximum distinction
- Set2: Professional, balanced
- Set3: Subtle, many categories

**Use cases:** Varied based on visual hierarchy needs

## Sequential colour schemes

Sequential schemes map continuous data from low to high values using a single hue or gradient.

### Single-hue sequential

**Blues:**
```javascript
d3.interpolateBlues
d3.schemeBlues[9] // 9-step discrete version
```

**Other single-hue options:**
- `d3.interpolateGreens` / `d3.schemeGreens`
- `d3.interpolateOranges` / `d3.schemeOranges`
- `d3.interpolatePurples` / `d3.schemePurples`
- `d3.interpolateReds` / `d3.schemeReds`
- `d3.interpolateGreys` / `d3.schemeGreys`

**Use cases:**
- Simple heat maps
- Choropleth maps
- Density plots
- Single-metric visualisations

### Multi-hue sequential

**Viridis (recommended):**
```javascript
d3.interpolateViridis
```

**Characteristics:**
- Perceptually uniform
- Colour-blind friendly
- Print-safe
- No visual dead zones
- Monotonically increasing perceived lightness

**Other perceptually-uniform options:**
- `d3.interpolatePlasma` - Purple to yellow
- `d3.interpolateInferno` - Black to white through red/orange
- `d3.interpolateMagma` - Black to white through purple
- `d3.interpolateCividis` - Colour-blind optimised

**Colour-blind accessible:**
```javascript
d3.interpolateTurbo // Rainbow-like but perceptually uniform
d3.interpolateCool  // Cyan to magenta
d3.interpolateWarm  // Orange to yellow
```

**Use cases:**
- Scientific visualisation
- Medical imaging
- Any high-precision data visualisation
- Accessible visualisations

### Traditional sequential

**Yellow-Orange-Red:**
```javascript
d3.interpolateYlOrRd
d3.schemeYlOrRd[9]
```

**Yellow-Green-Blue:**
```javascript
d3.interpolateYlGnBu
d3.schemeYlGnBu[9]
```

**Other multi-hue:**
- `d3.interpolateBuGn` - Blue to green
- `d3.interpolateBuPu` - Blue to purple
- `d3.interpolateGnBu` - Green to blue
- `d3.interpolateOrRd` - Orange to red
- `d3.interpolatePuBu` - Purple to blue
- `d3.interpolatePuBuGn` - Purple to blue-green
- `d3.interpolatePuRd` - Purple to red
- `d3.interpolateRdPu` - Red to purple
- `d3.interpolateYlGn` - Yellow to green
- `d3.interpolateYlOrBr` - Yellow to orange-brown

**Use cases:** Traditional data visualisation, familiar colour associations (temperature, vegetation, water)

## Diverging colour schemes

Diverging schemes highlight deviations from a central value using two distinct hues.

### Red-Blue (temperature)

```javascript
d3.interpolateRdBu
d3.schemeRdBu[11]
```

**Characteristics:**
- Intuitive temperature metaphor
- Strong contrast
- Clear positive/negative distinction

**Use cases:** Temperature, profit/loss, above/below average, correlation

### Red-Yellow-Blue

```javascript
d3.interpolateRdYlBu
d3.schemeRdYlBu[11]
```

**Characteristics:**
- Three-colour gradient
- Softer transition through yellow
- More visual steps

**Use cases:** When extreme values need emphasis and middle needs visibility

### Other diverging schemes

**Traffic light:**
```javascript
d3.interpolateRdYlGn // Red (bad) to green (good)
```

**Spectral (rainbow):**
```javascript
d3.interpolateSpectral // Full spectrum
```

**Other options:**
- `d3.interpolateBrBG` - Brown to blue-green
- `d3.interpolatePiYG` - Pink to yellow-green
- `d3.interpolatePRGn` - Purple to green
- `d3.interpolatePuOr` - Purple to orange
- `d3.interpolateRdGy` - Red to grey

**Use cases:** Choose based on semantic meaning and accessibility needs

## Colour-blind friendly palettes

### General guidelines

1. **Avoid red-green combinations** (most common colour blindness)
2. **Use blue-orange diverging** instead of red-green
3. **Add texture or patterns** as redundant encoding
4. **Test with simulation tools**

### Recommended colour-blind safe schemes

**Categorical:**
```javascript
// Okabe-Ito palette (colour-blind safe)
const okabePalette = [
  '#E69F00', // Orange
  '#56B4E9', // Sky blue
  '#009E73', // Bluish green
  '#F0E442', // Yellow
  '#0072B2', // Blue
  '#D55E00', // Vermillion
  '#CC79A7', // Reddish purple
  '#000000'  // Black
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(okabePalette);
```

**Sequential:**
```javascript
// Use Viridis, Cividis, or Blues
d3.interpolateViridis  // Best overall
d3.interpolateCividis  // Optimised for CVD
d3.interpolateBlues    // Simple, safe
```

**Diverging:**
```javascript
// Use blue-orange instead of red-green
d3.interpolateBrBG
d3.interpolatePuOr
```

## Custom colour palettes

### Creating custom sequential

```javascript
const customSequential = d3.scaleLinear()
  .domain([0, 100])
  .range(['#e8f4f8', '#006d9c']) // Light to dark blue
  .interpolate(d3.interpolateLab); // Perceptually uniform
```

### Creating custom diverging

```javascript
const customDiverging = d3.scaleLinear()
  .domain([0, 50, 100])
  .range(['#ca0020', '#f7f7f7', '#0571b0']) // Red, grey, blue
  .interpolate(d3.interpolateLab);
```

### Creating custom categorical

```javascript
// Brand colours
const brandPalette = [
  '#FF6B6B', // Primary red
  '#4ECDC4', // Secondary teal
  '#45B7D1', // Tertiary blue
  '#FFA07A', // Accent coral
  '#98D8C8'  // Accent mint
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(brandPalette);
```

## Semantic colour associations

### Universal colour meanings

**Red:**
- Danger, error, negative
- High temperature
- Debt, loss

**Green:**
- Success, positive
- Growth, vegetation
- Profit, gain

**Blue:**
- Trust, calm
- Water, cold
- Information, neutral

**Yellow/Orange:**
- Warning, caution
- Energy, warmth
- Attention

**Grey:**
- Neutral, inactive
- Missing data
- Background

### Context-specific palettes

**Financial:**
```javascript
const financialColours = {
  profit: '#27ae60',
  loss: '#e74c3c',
  neutral: '#95a5a6',
  highlight: '#3498db'
};
```

**Temperature:**
```javascript
const temperatureScale = d3.scaleSequential(d3.interpolateRdYlBu)
  .domain([40, -10]); // Hot to cold (reversed)
```

**Traffic/Status:**
```javascript
const statusColours = {
  success: '#27ae60',
  warning: '#f39c12',
  error: '#e74c3c',
  info: '#3498db',
  neutral: '#95a5a6'
};
```

## Accessibility best practices

### Contrast ratios

Ensure sufficient contrast between colours and backgrounds:

```javascript
// Good contrast example
const highContrast = {
  background: '#ffffff',
  text: '#2c3e50',
  primary: '#3498db',
  secondary: '#e74c3c'
};
```

**WCAG guidelines:**
- Normal text: 4.5:1 minimum
- Large text: 3:1 minimum
- UI components: 3:1 minimum

### Redundant encoding

Never rely solely on colour to convey information:

```javascript
// Add patterns or shapes
const symbols = ['circle', 'square', 'triangle', 'diamond'];

// Add text labels
// Use line styles (solid, dashed, dotted)
// Use size encoding
```

### Testing

Test visualisations for colour blindness:
- Chrome DevTools (Rendering > Emulate vision deficiencies)
- Colour Oracle (free desktop application)
- Coblis (online simulator)

## Professional colour recommendations

### Data journalism

```javascript
// Guardian style
const guardianPalette = [
  '#005689', // Guardian blue
  '#c70000', // Guardian red
  '#7d0068', // Guardian pink
  '#951c75', // Guardian purple
];

// FT style
const ftPalette = [
  '#0f5499', // FT blue
  '#990f3d', // FT red
  '#593380', // FT purple
  '#262a33', // FT black
];
```

### Academic/Scientific

```javascript
// Nature journal style
const naturePalette = [
  '#0071b2', // Blue
  '#d55e00', // Vermillion
  '#009e73', // Green
  '#f0e442', // Yellow
];

// Use Viridis for continuous data
const scientificScale = d3.scaleSequential(d3.interpolateViridis);
```

### Corporate/Business

```javascript
// Professional, conservative
const corporatePalette = [
  '#003f5c', // Dark blue
  '#58508d', // Purple
  '#bc5090', // Magenta
  '#ff6361', // Coral
  '#ffa600'  // Orange
];
```

## Dynamic colour selection

### Based on data range

```javascript
function selectColourScheme(data) {
  const extent = d3.extent(data);
  const hasNegative = extent[0] < 0;
  const hasPositive = extent[1] > 0;
  
  if (hasNegative && hasPositive) {
    // Diverging: data crosses zero
    return d3.scaleSequentialSymlog(d3.interpolateRdBu)
      .domain([extent[0], 0, extent[1]]);
  } else {
    // Sequential: all positive or all negative
    return d3.scaleSequential(d3.interpolateViridis)
      .domain(extent);
  }
}
```

### Based on category count

```javascript
function selectCategoricalScheme(categories) {
  const n = categories.length;
  
  if (n <= 10) {
    return d3.scaleOrdinal(d3.schemeTableau10);
  } else if (n <= 12) {
    return d3.scaleOrdinal(d3.schemePaired);
  } else {
    // For many categories, use sequential with quantize
    return d3.scaleQuantize()
      .domain([0, n - 1])
      .range(d3.quantize(d3.interpolateRainbow, n));
  }
}
```

## Common colour mistakes to avoid

1. **Rainbow gradients for sequential data**
   - Problem: Not perceptually uniform, hard to read
   - Solution: Use Viridis, Blues, or other uniform schemes

2. **Red-green for diverging (colour blindness)**
   - Problem: 8% of males can't distinguish
   - Solution: Use blue-orange or purple-green

3. **Too many categorical colours**
   - Problem: Hard to distinguish and remember
   - Solution: Limit to 5-8 categories, use grouping

4. **Insufficient contrast**
   - Problem: Poor readability
   - Solution: Test contrast ratios, use darker colours on light backgrounds

5. **Culturally inconsistent colours**
   - Problem: Confusing semantic meaning
   - Solution: Research colour associations for target audience

6. **Inverted temperature scales**
   - Problem: Counterintuitive (red = cold)
   - Solution: Red/orange = hot, blue = cold

## Quick reference guide

**Need to show...**

- **Categories (≤10):** `d3.schemeCategory10` or `d3.schemeTableau10`
- **Categories (>10):** `d3.schemePaired` or group categories
- **Sequential (general):** `d3.interpolateViridis`
- **Sequential (scientific):** `d3.interpolateViridis` or `d3.interpolatePlasma`
- **Sequential (temperature):** `d3.interpolateRdYlBu` (inverted)
- **Diverging (zero):** `d3.interpolateRdBu` or `d3.interpolateBrBG`
- **Diverging (good/bad):** `d3.interpolateRdYlGn` (inverted)
- **Colour-blind safe (categorical):** Okabe-Ito palette (shown above)
- **Colour-blind safe (sequential):** `d3.interpolateCividis` or `d3.interpolateBlues`
- **Colour-blind safe (diverging):** `d3.interpolatePuOr` or `d3.interpolateBrBG`

**Always remember:**
1. Test for colour-blindness
2. Ensure sufficient contrast
3. Use semantic colours appropriately
4. Add redundant encoding (patterns, labels)
5. Keep it simple (fewer colours = clearer visualisation)

---

## Reference: D3 Patterns

# D3.js Visualisation Patterns

This reference provides detailed code patterns for common d3.js visualisation types.

## Hierarchical visualisations

### Tree diagram

```javascript
useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const tree = d3.tree().size([height - 100, width - 200]);
  
  const root = d3.hierarchy(data);
  tree(root);
  
  const g = svg.append("g")
    .attr("transform", "translate(100,50)");
  
  // Links
  g.selectAll("path")
    .data(root.links())
    .join("path")
    .attr("d", d3.linkHorizontal()
      .x(d => d.y)
      .y(d => d.x))
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-width", 2);
  
  // Nodes
  const node = g.selectAll("g")
    .data(root.descendants())
    .join("g")
    .attr("transform", d => `translate(${d.y},${d.x})`);
  
  node.append("circle")
    .attr("r", 6)
    .attr("fill", d => d.children ? "#555" : "#999");
  
  node.append("text")
    .attr("dy", "0.31em")
    .attr("x", d => d.children ? -8 : 8)
    .attr("text-anchor", d => d.children ? "end" : "start")
    .text(d => d.data.name)
    .style("font-size", "12px");
    
}, [data]);
```

### Treemap

```javascript
useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);
  
  d3.treemap()
    .size([width, height])
    .padding(2)
    .round(true)(root);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const cell = svg.selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr("transform", d => `translate(${d.x0},${d.y0})`);
  
  cell.append("rect")
    .attr("width", d => d.x1 - d.x0)
    .attr("height", d => d.y1 - d.y0)
    .attr("fill", d => colourScale(d.parent.data.name))
    .attr("stroke", "white")
    .attr("stroke-width", 2);
  
  cell.append("text")
    .attr("x", 4)
    .attr("y", 16)
    .text(d => d.data.name)
    .style("font-size", "12px")
    .style("fill", "white");
    
}, [data]);
```

### Sunburst diagram

```javascript
useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 600;
  const height = 600;
  const radius = Math.min(width, height) / 2;
  
  const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);
  
  const partition = d3.partition()
    .size([2 * Math.PI, radius]);
  
  partition(root);
  
  const arc = d3.arc()
    .startAngle(d => d.x0)
    .endAngle(d => d.x1)
    .innerRadius(d => d.y0)
    .outerRadius(d => d.y1);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);
  
  g.selectAll("path")
    .data(root.descendants())
    .join("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(d.depth))
    .attr("stroke", "white")
    .attr("stroke-width", 1);
    
}, [data]);
```

### Chord diagram

```javascript
function drawChordDiagram(data) {
  // data format: array of objects with source, target, and value
  // Example: [{ source: 'A', target: 'B', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 600;
  const height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 30;

  // Create matrix from data
  const nodes = Array.from(new Set(data.flatMap(d => [d.source, d.target])));
  const matrix = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));

  data.forEach(d => {
    const i = nodes.indexOf(d.source);
    const j = nodes.indexOf(d.target);
    matrix[i][j] += d.value;
    matrix[j][i] += d.value;
  });

  // Create chord layout
  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .source(d => d.source)
    .target(d => d.target);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10)
    .domain(nodes);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const chords = chord(matrix);

  // Draw ribbons
  g.append("g")
    .attr("fill-opacity", 0.67)
    .selectAll("path")
    .data(chords)
    .join("path")
    .attr("d", ribbon)
    .attr("fill", d => colourScale(nodes[d.source.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.source.index])).darker());

  // Draw groups (arcs)
  const group = g.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(nodes[d.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.index])).darker());

  // Add labels
  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .attr("dy", "0.31em")
    .attr("transform", d => `rotate(${(d.angle * 180 / Math.PI) - 90})translate(${outerRadius + 30})${d.angle > Math.PI ? "rotate(180)" : ""}`)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text((d, i) => nodes[i])
    .style("font-size", "12px");
}

// Data format example:
// const data = [
//   { source: 'Category A', target: 'Category B', value: 100 },
//   { source: 'Category A', target: 'Category C', value: 50 },
//   { source: 'Category B', target: 'Category C', value: 75 }
// ];
// drawChordDiagram(data);
```

## Advanced chart types

### Heatmap

```javascript
function drawHeatmap(data) {
  // data format: array of objects with row, column, and value
  // Example: [{ row: 'A', column: 'X', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 800;
  const height = 600;
  const margin = { top: 100, right: 30, bottom: 30, left: 100 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Get unique rows and columns
  const rows = Array.from(new Set(data.map(d => d.row)));
  const columns = Array.from(new Set(data.map(d => d.column)));

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Create scales
  const xScale = d3.scaleBand()
    .domain(columns)
    .range([0, innerWidth])
    .padding(0.01);

  const yScale = d3.scaleBand()
    .domain(rows)
    .range([0, innerHeight])
    .padding(0.01);

  // Colour scale for values (sequential from light to dark red)
  const colourScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.value)]);

  // Draw rectangles
  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.column))
    .attr("y", d => yScale(d.row))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colourScale(d.value));

  // Add x-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(columns)
    .join("text")
    .attr("x", d => xScale(d) + xScale.bandwidth() / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text(d => d)
    .style("font-size", "12px");

  // Add y-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(rows)
    .join("text")
    .attr("x", -10)
    .attr("y", d => yScale(d) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text(d => d)
    .style("font-size", "12px");

  // Add colour legend
  const legendWidth = 20;
  const legendHeight = 200;
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 60},${margin.top})`);

  const legendScale = d3.scaleLinear()
    .domain(colourScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale).ticks(5);

  // Draw colour gradient in legend
  for (let i = 0; i < legendHeight; i++) {
    legend.append("rect")
      .attr("y", i)
      .attr("width", legendWidth)
      .attr("height", 1)
      .attr("fill", colourScale(legendScale.invert(i)));
  }

  legend.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);
}

// Data format example:
// const data = [
//   { row: 'Monday', column: 'Morning', value: 42 },
//   { row: 'Monday', column: 'Afternoon', value: 78 },
//   { row: 'Tuesday', column: 'Morning', value: 65 },
//   { row: 'Tuesday', column: 'Afternoon', value: 55 }
// ];
// drawHeatmap(data);
```

### Area chart with gradient

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // Define gradient
  const defs = svg.append("defs");
  const gradient = defs.append("linearGradient")
    .attr("id", "areaGradient")
    .attr("x1", "0%")
    .attr("x2", "0%")
    .attr("y1", "0%")
    .attr("y2", "100%");
  
  gradient.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", "steelblue")
    .attr("stop-opacity", 0.8);
  
  gradient.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", "steelblue")
    .attr("stop-opacity", 0.1);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);
  
  const area = d3.area()
    .x(d => xScale(d.date))
    .y0(innerHeight)
    .y1(d => yScale(d.value))
    .curve(d3.curveMonotoneX);
  
  g.append("path")
    .datum(data)
    .attr("fill", "url(#areaGradient)")
    .attr("d", area);
  
  const line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value))
    .curve(d3.curveMonotoneX);
  
  g.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2)
    .attr("d", line);
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### Stacked bar chart

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const categories = Object.keys(data[0]).filter(k => k !== 'group');
  const stackedData = d3.stack().keys(categories)(data);
  
  const xScale = d3.scaleBand()
    .domain(data.map(d => d.group))
    .range([0, innerWidth])
    .padding(0.1);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(stackedData[stackedData.length - 1], d => d[1])])
    .range([innerHeight, 0]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  g.selectAll("g")
    .data(stackedData)
    .join("g")
    .attr("fill", (d, i) => colourScale(i))
    .selectAll("rect")
    .data(d => d)
    .join("rect")
    .attr("x", d => xScale(d.data.group))
    .attr("y", d => yScale(d[1]))
    .attr("height", d => yScale(d[0]) - yScale(d[1]))
    .attr("width", xScale.bandwidth());
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### Grouped bar chart

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const categories = Object.keys(data[0]).filter(k => k !== 'group');
  
  const x0Scale = d3.scaleBand()
    .domain(data.map(d => d.group))
    .range([0, innerWidth])
    .padding(0.1);
  
  const x1Scale = d3.scaleBand()
    .domain(categories)
    .range([0, x0Scale.bandwidth()])
    .padding(0.05);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => Math.max(...categories.map(c => d[c])))])
    .range([innerHeight, 0]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const group = g.selectAll("g")
    .data(data)
    .join("g")
    .attr("transform", d => `translate(${x0Scale(d.group)},0)`);
  
  group.selectAll("rect")
    .data(d => categories.map(key => ({ key, value: d[key] })))
    .join("rect")
    .attr("x", d => x1Scale(d.key))
    .attr("y", d => yScale(d.value))
    .attr("width", x1Scale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", d => colourScale(d.key));
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x0Scale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### Bubble chart

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]);
  
  const sizeScale = d3.scaleSqrt()
    .domain([0, d3.max(data, d => d.size)])
    .range([0, 50]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", d => sizeScale(d.size))
    .attr("fill", d => colourScale(d.category))
    .attr("opacity", 0.6)
    .attr("stroke", "white")
    .attr("stroke-width", 2);
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

## Geographic visualisations

### Basic map with points

```javascript
useEffect(() => {
  if (!geoData || !pointData) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const projection = d3.geoMercator()
    .fitSize([width, height], geoData);
  
  const pathGenerator = d3.geoPath().projection(projection);
  
  // Draw map
  svg.selectAll("path")
    .data(geoData.features)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", "#e0e0e0")
    .attr("stroke", "#999")
    .attr("stroke-width", 0.5);
  
  // Draw points
  svg.selectAll("circle")
    .data(pointData)
    .join("circle")
    .attr("cx", d => projection([d.longitude, d.latitude])[0])
    .attr("cy", d => projection([d.longitude, d.latitude])[1])
    .attr("r", 5)
    .attr("fill", "steelblue")
    .attr("opacity", 0.7);
    
}, [geoData, pointData]);
```

### Choropleth map

```javascript
useEffect(() => {
  if (!geoData || !valueData) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const projection = d3.geoMercator()
    .fitSize([width, height], geoData);
  
  const pathGenerator = d3.geoPath().projection(projection);
  
  // Create value lookup
  const valueLookup = new Map(valueData.map(d => [d.id, d.value]));
  
  // Colour scale
  const colourScale = d3.scaleSequential(d3.interpolateBlues)
    .domain([0, d3.max(valueData, d => d.value)]);
  
  svg.selectAll("path")
    .data(geoData.features)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", d => {
      const value = valueLookup.get(d.id);
      return value ? colourScale(value) : "#e0e0e0";
    })
    .attr("stroke", "#999")
    .attr("stroke-width", 0.5);
    
}, [geoData, valueData]);
```

## Advanced interactions

### Brush and zoom

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const circles = g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
  
  // Add brush
  const brush = d3.brush()
    .extent([[0, 0], [innerWidth, innerHeight]])
    .on("start brush", (event) => {
      if (!event.selection) return;
      
      const [[x0, y0], [x1, y1]] = event.selection;
      
      circles.attr("fill", d => {
        const cx = xScale(d.x);
        const cy = yScale(d.y);
        return (cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1) 
          ? "orange" 
          : "steelblue";
      });
    });
  
  g.append("g")
    .attr("class", "brush")
    .call(brush);
    
}, [data]);
```

### Linked brushing between charts

```javascript
function LinkedCharts({ data }) {
  const [selectedPoints, setSelectedPoints] = useState(new Set());
  const svg1Ref = useRef();
  const svg2Ref = useRef();
  
  useEffect(() => {
    // Chart 1: Scatter plot
    const svg1 = d3.select(svg1Ref.current);
    svg1.selectAll("*").remove();
    
    // ... create first chart ...
    
    const circles1 = svg1.selectAll("circle")
      .data(data)
      .join("circle")
      .attr("fill", d => selectedPoints.has(d.id) ? "orange" : "steelblue");
    
    // Chart 2: Bar chart
    const svg2 = d3.select(svg2Ref.current);
    svg2.selectAll("*").remove();
    
    // ... create second chart ...
    
    const bars = svg2.selectAll("rect")
      .data(data)
      .join("rect")
      .attr("fill", d => selectedPoints.has(d.id) ? "orange" : "steelblue");
    
    // Add brush to first chart
    const brush = d3.brush()
      .on("start brush end", (event) => {
        if (!event.selection) {
          setSelectedPoints(new Set());
          return;
        }
        
        const [[x0, y0], [x1, y1]] = event.selection;
        const selected = new Set();
        
        data.forEach(d => {
          const x = xScale(d.x);
          const y = yScale(d.y);
          if (x >= x0 && x <= x1 && y >= y0 && y <= y1) {
            selected.add(d.id);
          }
        });
        
        setSelectedPoints(selected);
      });
    
    svg1.append("g").call(brush);
    
  }, [data, selectedPoints]);
  
  return (
    <div>
      <svg ref={svg1Ref} width="400" height="300" />
      <svg ref={svg2Ref} width="400" height="300" />
    </div>
  );
}
```

## Animation patterns

### Enter, update, exit with transitions

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  
  const circles = svg.selectAll("circle")
    .data(data, d => d.id); // Key function for object constancy
  
  // EXIT: Remove old elements
  circles.exit()
    .transition()
    .duration(500)
    .attr("r", 0)
    .remove();
  
  // UPDATE: Modify existing elements
  circles
    .transition()
    .duration(500)
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("fill", "steelblue");
  
  // ENTER: Add new elements
  circles.enter()
    .append("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 0)
    .attr("fill", "steelblue")
    .transition()
    .duration(500)
    .attr("r", 5);
    
}, [data]);
```

### Path morphing

```javascript
useEffect(() => {
  if (!data1 || !data2) return;
  
  const svg = d3.select(svgRef.current);
  
  const line = d3.line()
    .x(d => xScale(d.x))
    .y(d => yScale(d.y))
    .curve(d3.curveMonotoneX);
  
  const path = svg.select("path");
  
  // Morph from data1 to data2
  path
    .datum(data1)
    .attr("d", line)
    .transition()
    .duration(1000)
    .attrTween("d", function() {
      const previous = d3.select(this).attr("d");
      const current = line(data2);
      return d3.interpolatePath(previous, current);
    });
    
}, [data1, data2]);
```

---

## Reference: Scale Reference

# D3.js Scale Reference

Comprehensive guide to all d3 scale types with examples and use cases.

## Continuous scales

### Linear scale

Maps continuous input domain to continuous output range with linear interpolation.

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

scale(50);  // Returns 250
scale(0);   // Returns 0
scale(100); // Returns 500

// Invert scale (get input from output)
scale.invert(250); // Returns 50
```

**Use cases:**
- Most common scale for quantitative data
- Axes, bar lengths, position encoding
- Temperature, prices, counts, measurements

**Methods:**
- `.domain([min, max])` - Set input domain
- `.range([min, max])` - Set output range
- `.invert(value)` - Get domain value from range value
- `.clamp(true)` - Restrict output to range bounds
- `.nice()` - Extend domain to nice round values

### Power scale

Maps continuous input to continuous output with exponential transformation.

```javascript
const sqrtScale = d3.scalePow()
  .exponent(0.5)  // Square root
  .domain([0, 100])
  .range([0, 500]);

const squareScale = d3.scalePow()
  .exponent(2)  // Square
  .domain([0, 100])
  .range([0, 500]);

// Shorthand for square root
const sqrtScale2 = d3.scaleSqrt()
  .domain([0, 100])
  .range([0, 500]);
```

**Use cases:**
- Perceptual scaling (human perception is non-linear)
- Area encoding (use square root to map values to circle radii)
- Emphasising differences in small or large values

### Logarithmic scale

Maps continuous input to continuous output with logarithmic transformation.

```javascript
const logScale = d3.scaleLog()
  .domain([1, 1000])  // Must be positive
  .range([0, 500]);

logScale(1);    // Returns 0
logScale(10);   // Returns ~167
logScale(100);  // Returns ~333
logScale(1000); // Returns 500
```

**Use cases:**
- Data spanning multiple orders of magnitude
- Population, GDP, wealth distributions
- Logarithmic axes
- Exponential growth visualisations

**Important:** Domain values must be strictly positive (>0).

### Time scale

Specialised linear scale for temporal data.

```javascript
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)])
  .range([0, 800]);

timeScale(new Date(2022, 0, 1)); // Returns 400

// Invert to get date
timeScale.invert(400); // Returns Date object for mid-2022
```

**Use cases:**
- Time series visualisations
- Timeline axes
- Temporal animations
- Date-based interactions

**Methods:**
- `.nice()` - Extend domain to nice time intervals
- `.ticks(count)` - Generate nicely-spaced tick values
- All linear scale methods apply

### Quantize scale

Maps continuous input to discrete output buckets.

```javascript
const quantizeScale = d3.scaleQuantize()
  .domain([0, 100])
  .range(['low', 'medium', 'high']);

quantizeScale(25);  // Returns 'low'
quantizeScale(50);  // Returns 'medium'
quantizeScale(75);  // Returns 'high'

// Get the threshold values
quantizeScale.thresholds(); // Returns [33.33, 66.67]
```

**Use cases:**
- Binning continuous data
- Heat map colours
- Risk categories (low/medium/high)
- Age groups, income brackets

### Quantile scale

Maps continuous input to discrete output based on quantiles.

```javascript
const quantileScale = d3.scaleQuantile()
  .domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20, 24]) // Sample data
  .range(['low', 'medium', 'high']);

quantileScale(8);  // Returns based on quantile position
quantileScale.quantiles(); // Returns quantile thresholds
```

**Use cases:**
- Equal-size groups regardless of distribution
- Percentile-based categorisation
- Handling skewed distributions

### Threshold scale

Maps continuous input to discrete output with custom thresholds.

```javascript
const thresholdScale = d3.scaleThreshold()
  .domain([0, 10, 20])
  .range(['freezing', 'cold', 'warm', 'hot']);

thresholdScale(-5);  // Returns 'freezing'
thresholdScale(5);   // Returns 'cold'
thresholdScale(15);  // Returns 'warm'
thresholdScale(25);  // Returns 'hot'
```

**Use cases:**
- Custom breakpoints
- Grade boundaries (A, B, C, D, F)
- Temperature categories
- Air quality indices

## Sequential scales

### Sequential colour scale

Maps continuous input to continuous colour gradient.

```javascript
const colourScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 100]);

colourScale(0);   // Returns lightest blue
colourScale(50);  // Returns mid blue
colourScale(100); // Returns darkest blue
```

**Available interpolators:**

**Single hue:**
- `d3.interpolateBlues`, `d3.interpolateGreens`, `d3.interpolateReds`
- `d3.interpolateOranges`, `d3.interpolatePurples`, `d3.interpolateGreys`

**Multi-hue:**
- `d3.interpolateViridis`, `d3.interpolateInferno`, `d3.interpolateMagma`
- `d3.interpolatePlasma`, `d3.interpolateWarm`, `d3.interpolateCool`
- `d3.interpolateCubehelixDefault`, `d3.interpolateTurbo`

**Use cases:**
- Heat maps, choropleth maps
- Continuous data visualisation
- Temperature, elevation, density

### Diverging colour scale

Maps continuous input to diverging colour gradient with a midpoint.

```javascript
const divergingScale = d3.scaleDiverging(d3.interpolateRdBu)
  .domain([-10, 0, 10]);

divergingScale(-10); // Returns red
divergingScale(0);   // Returns white/neutral
divergingScale(10);  // Returns blue
```

**Available interpolators:**
- `d3.interpolateRdBu` - Red to blue
- `d3.interpolateRdYlBu` - Red, yellow, blue
- `d3.interpolateRdYlGn` - Red, yellow, green
- `d3.interpolatePiYG` - Pink, yellow, green
- `d3.interpolateBrBG` - Brown, blue-green
- `d3.interpolatePRGn` - Purple, green
- `d3.interpolatePuOr` - Purple, orange
- `d3.interpolateRdGy` - Red, grey
- `d3.interpolateSpectral` - Rainbow spectrum

**Use cases:**
- Data with meaningful midpoint (zero, average, neutral)
- Positive/negative values
- Above/below comparisons
- Correlation matrices

### Sequential quantile scale

Combines sequential colour with quantile mapping.

```javascript
const sequentialQuantileScale = d3.scaleSequentialQuantile(d3.interpolateBlues)
  .domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20, 24]);

// Maps based on quantile position
```

**Use cases:**
- Perceptually uniform binning
- Handling outliers
- Skewed distributions

## Ordinal scales

### Band scale

Maps discrete input to continuous bands (rectangles) with optional padding.

```javascript
const bandScale = d3.scaleBand()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.1);

bandScale('A');           // Returns start position (e.g., 0)
bandScale('B');           // Returns start position (e.g., 110)
bandScale.bandwidth();    // Returns width of each band (e.g., 95)
bandScale.step();         // Returns total step including padding
bandScale.paddingInner(); // Returns inner padding (between bands)
bandScale.paddingOuter(); // Returns outer padding (at edges)
```

**Use cases:**
- Bar charts (most common use case)
- Grouped elements
- Categorical axes
- Heat map cells

**Padding options:**
- `.padding(value)` - Sets both inner and outer padding (0-1)
- `.paddingInner(value)` - Padding between bands (0-1)
- `.paddingOuter(value)` - Padding at edges (0-1)
- `.align(value)` - Alignment of bands (0-1, default 0.5)

### Point scale

Maps discrete input to continuous points (no width).

```javascript
const pointScale = d3.scalePoint()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.5);

pointScale('A'); // Returns position (e.g., 50)
pointScale('B'); // Returns position (e.g., 150)
pointScale('C'); // Returns position (e.g., 250)
pointScale('D'); // Returns position (e.g., 350)
pointScale.step(); // Returns distance between points
```

**Use cases:**
- Line chart categorical x-axis
- Scatter plot with categorical axis
- Node positions in network graphs
- Any point positioning for categories

### Ordinal colour scale

Maps discrete input to discrete output (colours, shapes, etc.).

```javascript
const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

colourScale('apples');  // Returns first colour
colourScale('oranges'); // Returns second colour
colourScale('apples');  // Returns same first colour (consistent)

// Custom range
const customScale = d3.scaleOrdinal()
  .domain(['cat1', 'cat2', 'cat3'])
  .range(['#FF6B6B', '#4ECDC4', '#45B7D1']);
```

**Built-in colour schemes:**

**Categorical:**
- `d3.schemeCategory10` - 10 colours
- `d3.schemeAccent` - 8 colours
- `d3.schemeDark2` - 8 colours
- `d3.schemePaired` - 12 colours
- `d3.schemePastel1` - 9 colours
- `d3.schemePastel2` - 8 colours
- `d3.schemeSet1` - 9 colours
- `d3.schemeSet2` - 8 colours
- `d3.schemeSet3` - 12 colours
- `d3.schemeTableau10` - 10 colours

**Use cases:**
- Category colours
- Legend items
- Multi-series charts
- Network node types

## Scale utilities

### Nice domain

Extend domain to nice round values.

```javascript
const scale = d3.scaleLinear()
  .domain([0.201, 0.996])
  .nice();

scale.domain(); // Returns [0.2, 1.0]

// With count (approximate tick count)
const scale2 = d3.scaleLinear()
  .domain([0.201, 0.996])
  .nice(5);
```

### Clamping

Restrict output to range bounds.

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500])
  .clamp(true);

scale(-10); // Returns 0 (clamped)
scale(150); // Returns 500 (clamped)
```

### Copy scales

Create independent copies.

```javascript
const scale1 = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

const scale2 = scale1.copy();
// scale2 is independent of scale1
```

### Tick generation

Generate nice tick values for axes.

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

scale.ticks(10);        // Generate ~10 ticks
scale.tickFormat(10);   // Get format function for ticks
scale.tickFormat(10, ".2f"); // Custom format (2 decimal places)

// Time scale ticks
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)]);

timeScale.ticks(d3.timeYear);      // Yearly ticks
timeScale.ticks(d3.timeMonth, 3);  // Every 3 months
timeScale.tickFormat(5, "%Y-%m");  // Format as year-month
```

## Colour spaces and interpolation

### RGB interpolation

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"]);
// Default: RGB interpolation
```

### HSL interpolation

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateHsl);
// Smoother colour transitions
```

### Lab interpolation

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateLab);
// Perceptually uniform
```

### HCL interpolation

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateHcl);
// Perceptually uniform with hue
```

## Common patterns

### Diverging scale with custom midpoint

```javascript
const scale = d3.scaleLinear()
  .domain([min, midpoint, max])
  .range(["red", "white", "blue"])
  .interpolate(d3.interpolateHcl);
```

### Multi-stop gradient scale

```javascript
const scale = d3.scaleLinear()
  .domain([0, 25, 50, 75, 100])
  .range(["#d53e4f", "#fc8d59", "#fee08b", "#e6f598", "#66c2a5"]);
```

### Radius scale for circles (perceptual)

```javascript
const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, 50]);

// Use with circles
circle.attr("r", d => radiusScale(d.value));
```

### Adaptive scale based on data range

```javascript
function createAdaptiveScale(data) {
  const extent = d3.extent(data);
  const range = extent[1] - extent[0];
  
  // Use log scale if data spans >2 orders of magnitude
  if (extent[1] / extent[0] > 100) {
    return d3.scaleLog()
      .domain(extent)
      .range([0, width]);
  }
  
  // Otherwise use linear
  return d3.scaleLinear()
    .domain(extent)
    .range([0, width]);
}
```

### Colour scale with explicit categories

```javascript
const colourScale = d3.scaleOrdinal()
  .domain(['Low Risk', 'Medium Risk', 'High Risk'])
  .range(['#2ecc71', '#f39c12', '#e74c3c'])
  .unknown('#95a5a6'); // Fallback for unknown values
```
