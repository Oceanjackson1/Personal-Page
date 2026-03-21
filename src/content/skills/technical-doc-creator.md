---
title: "Technical Doc Creator"
description: "Create HTML technical documentation with code blocks, API workflows, system architecture diagrams, and syntax highlighting. Use when users request technical documentation, API docs, API references, code examples, or developer documentation."
category: "writing"
source: "community"
author: "Community"
tags: ["technical", "doc", "creator"]
date: 2026-03-20
---

# Technical Documentation Creator

Create comprehensive HTML technical documentation with code examples and API workflows.

## When to Use

- "Create API documentation for [endpoints]"
- "Generate technical docs for [system]"
- "Document API reference"
- "Create developer documentation"

## Components

1. **Overview**: purpose, key features, tech stack
2. **Getting Started**: installation, setup, quick start
3. **API Reference**: endpoints with request/response examples
4. **Code Examples**: syntax-highlighted code blocks
5. **Architecture**: system diagram (SVG)
6. **Workflows**: step-by-step processes

## HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>[API/System] Documentation</title>
  <style>
    body { font-family: system-ui; max-width: 1000px; margin: 0 auto; }
    pre { background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 4px; overflow-x: auto; }
    .endpoint { background: #f7fafc; padding: 15px; margin: 10px 0; border-left: 4px solid #4299e1; }
    code { background: #e2e8f0; padding: 2px 6px; border-radius: 3px; }
  </style>
</head>
<body>
  <h1>[System] Documentation</h1>
  <!-- Overview, Getting Started, API Reference, Examples -->
</body>
</html>
```

## API Endpoint Pattern

```html
<div class="endpoint">
  <h3><span style="color: #48bb78;">GET</span> /api/users/{id}</h3>
  <p>Retrieve user by ID</p>

  <h4>Request</h4>
  <pre><code>curl -X GET https://api.example.com/users/123</code></pre>

  <h4>Response</h4>
  <pre><code>{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}</code></pre>
</div>
```

## Code Block Pattern

```html
<pre><code>// Installation
npm install package-name

// Usage
import { feature } from 'package-name';
const result = feature.doSomething();</code></pre>
```

## Workflow

1. Extract API endpoints, methods, parameters
2. Create overview and getting started sections
3. Document each endpoint with examples
4. Add code snippets for common operations
5. Include architecture diagram if relevant
6. Write to `[system]-docs.html`

Use semantic colors for HTTP methods: GET (green), POST (blue), DELETE (red).

---

## Reference: Design_Patterns

# Design Patterns Reference

Complete design system guidelines for creating visually stunning HTML documentation.

## Color System

### Primary Palette

**Gradient Background:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
- Use for: Body background, primary branding elements
- Creates depth and visual interest

**Accent Colors:**
- Primary Purple-Blue: `#667eea`
- Secondary Purple: `#764ba2`
- Use for: Headings, borders, key UI elements

### Semantic Color Scales

#### Success / Confirmed / Positive
- **Base:** `#48bb78` (green)
- **Dark:** `#2f855a` (darker green, for strokes)
- **Light:** `#e6f4ea` (pale green, for backgrounds)
- Use for: Completed tasks, success messages, positive metrics

#### Warning / Uncertain / Attention
- **Base:** `#f59e0b` (amber)
- **Dark:** `#d97706` (darker amber, for strokes)
- **Light:** `#fffbeb` (pale amber, for backgrounds)
- Use for: In-progress items, warnings, items needing attention

#### Info / Primary / Standard
- **Base:** `#4299e1` (blue)
- **Dark:** `#2b6cb0` (darker blue, for strokes)
- **Light:** `#e6f2ff` (pale blue, for backgrounds)
- Use for: Standard information, primary actions, neutral states

#### Error / Critical / Negative
- **Base:** `#f56565` (red)
- **Dark:** `#c53030` (darker red, for strokes)
- **Light:** `#fff5f5` (pale red, for backgrounds)
- Use for: Errors, critical issues, failed states

#### Process / Action / Secondary
- **Base:** `#ed8936` (orange)
- **Dark:** `#c05621` (darker orange, for strokes)
- **Light:** `#fff5e6` (pale orange, for backgrounds)
- Use for: Processing states, secondary actions

#### Special / Highlight / Tertiary
- **Base:** `#9f7aea` (purple)
- **Dark:** `#6b46c1` (darker purple, for strokes)
- **Light:** `#f3e6ff` (pale purple, for backgrounds)
- Use for: Special features, highlights, premium items

### Neutral Palette

**Text Colors:**
- **Dark (Primary text):** `#2d3748` - Headings, important content
- **Medium (Secondary text):** `#718096` - Body text, labels
- **Light (Tertiary text):** `#a0aec0` - Captions, metadata

**UI Elements:**
- **Dark border:** `#cbd5e0`
- **Light border:** `#e2e8f0`
- **Dark background:** `#edf2f7`
- **Light background:** `#f7fafc`
- **White:** `#ffffff`

### Color Contrast Guidelines

**WCAG AA Compliance:**
- Minimum contrast ratio: 4.5:1 for normal text
- Large text (18pt+ or 14pt+ bold): 3:1 minimum
- Safe combinations:
  - Dark text (#2d3748) on light backgrounds (#f7fafc, #ffffff)
  - White text on colored backgrounds (all semantic base colors pass)
  - Medium text (#718096) on white only

## Typography

### Font Families

**Primary (Sans-serif):**
```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```
- Use for: All body text, headings, UI elements
- Fallback chain ensures availability across platforms

**Code (Monospace):**
```css
font-family: 'Courier New', monospace;
```
- Use for: Code blocks, technical data, fixed-width content

### Type Scale

**Display / Hero:**
- Size: `2.5em` (40px at 16px base)
- Weight: Bold (700)
- Use for: Page title (h1)
- Special effect: Gradient text clip

**Section Heading:**
- Size: `1.8em` (28.8px)
- Weight: Bold (700)
- Color: `#2d3748`
- Use for: Major sections (h2)
- Decoration: Bottom border `3px solid #667eea`

**Subsection:**
- Size: `1.4em` (22.4px)
- Weight: Bold (700)
- Color: `#2d3748`
- Use for: Subsections (h3)

**Body:**
- Size: `1em` (16px base)
- Weight: Normal (400)
- Line height: 1.6
- Color: `#2d3748` or `#4a5568`
- Use for: Paragraphs, general content

**Label / Caption:**
- Size: `0.9-0.95em` (14.4-15.2px)
- Weight: Normal (400) or Medium (500)
- Color: `#718096`
- Use for: Metric labels, chart labels, form labels

**Small / Meta:**
- Size: `0.85em` (13.6px)
- Weight: Normal (400)
- Color: `#a0aec0`
- Use for: Footnotes, timestamps, metadata

**SVG Text:**
- Small labels: `11-12px`
- Standard text: `13-14px`
- Emphasis: `15-16px`
- Large values: `18-24px`
- Metric displays: `48px+`

### Text Effects

**Gradient Text (for h1):**
```css
h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

**Code Highlighting:**
```css
.highlight {
    color: #fbbf24;  /* Amber highlight */
    font-weight: bold;
}
```

## Spacing & Layout

### Container Sizing

**Max Width:**
- Container: `1400px`
- Comfortable reading: `800-1000px`
- Full width sections: No max-width

**Padding:**
- Desktop container: `40px`
- Mobile container: `20px`
- Diagram containers: `30px`
- Content boxes: `20px`
- Metric cards: `25px`

**Margins:**
- Section bottom: `60px`
- Element groups: `30px`
- Individual elements: `20px`
- Small gaps: `10px`

### Grid Systems

**Metric Grid:**
```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
gap: 20px;
```
- Automatically responsive
- Minimum card width: 200px
- Equal width distribution

**Custom Grids:**
- 2-column: `grid-template-columns: 1fr 1fr;`
- 3-column: `grid-template-columns: repeat(3, 1fr);`
- Sidebar layout: `grid-template-columns: 300px 1fr;`

### Flexbox Patterns

**Horizontal Center:**
```css
display: flex;
justify-content: center;
align-items: center;
```

**Space Between:**
```css
display: flex;
justify-content: space-between;
align-items: center;
```

**Wrapped Row:**
```css
display: flex;
flex-wrap: wrap;
gap: 20px;
```

## Visual Effects

### Shadows

**Card Shadow:**
```css
box-shadow: 0 20px 60px rgba(0,0,0,0.3);
```
- Use for: Main container, elevated cards

**Metric Card Shadow:**
```css
box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
```
- Use for: Metric cards, smaller elevation

**Subtle Shadow:**
```css
box-shadow: 0 2px 8px rgba(0,0,0,0.1);
```
- Use for: Buttons, small cards, hover states

### Border Radius

**Large (Containers):**
- Container: `20px`
- Diagram containers: `15px`

**Medium (Cards & Boxes):**
- Metric cards: `15px`
- Content boxes: `10px`
- SVG shapes: `10px`

**Small (UI Elements):**
- Buttons: `8px`
- Small badges: `5px`

**Pills / Rounded:**
- Full rounded: `50%` (circles) or `9999px` (pills)
- Timeline progress bars: `20px`

### Opacity

**Overlays:**
- Light overlay: `0.3`
- Medium overlay: `0.5-0.6`
- Strong overlay: `0.8-0.9`

**Hover States:**
- Slight fade: `0.9`
- Clear fade: `0.7-0.8`

**Disabled:**
- `0.5-0.6`

## Responsive Breakpoints

### Mobile First Strategy

**Breakpoints:**
```css
/* Mobile: default styles, no media query needed */

/* Tablet */
@media (min-width: 768px) { ... }

/* Desktop */
@media (min-width: 1024px) { ... }

/* Large Desktop */
@media (min-width: 1440px) { ... }
```

**Common Pattern (Desktop First):**
```css
@media (max-width: 768px) {
    .container { padding: 20px; }
    h1 { font-size: 1.8em; }
    .section-title { font-size: 1.4em; }
    .metric-grid { grid-template-columns: 1fr; }
}
```

### Responsive Typography

**Desktop:**
- h1: `2.5em`
- h2: `1.8em`
- h3: `1.4em`
- body: `1em`

**Mobile (max-width: 768px):**
- h1: `1.8em`
- h2: `1.4em`
- h3: `1.2em`
- body: `0.95em`

**SVG Text Scaling:**
- Use `viewBox` for automatic scaling
- Font sizes in px remain constant
- Increase viewBox dimensions rather than reducing font sizes

## Component Patterns

### Metric Cards

**Standard Pattern:**
```html
<div class="metric-card">
    <div class="metric-value">[LARGE NUMBER]</div>
    <div class="metric-label">[DESCRIPTION]</div>
</div>
```

**With Custom Color:**
```html
<div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
    <div class="metric-value">✓ [NUMBER]</div>
    <div class="metric-label">[DESCRIPTION]</div>
</div>
```

### Code Blocks

**Standard:**
```html
<div class="code-block">
<span class="highlight">Key term:</span> Regular code text
    Indented content
</div>
```

**CSS:**
```css
.code-block {
    background: #2d3748;
    color: #e2e8f0;
    padding: 20px;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    overflow-x: auto;
    line-height: 1.6;
}
```

### Example Boxes

**Pattern:**
```html
<div class="example-box">
    <div class="example-title">[TITLE]</div>
    <p>[CONTENT]</p>
</div>
```

**CSS:**
```css
.example-box {
    background: #fff;
    border: 2px solid #667eea;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}
```

### Legends

**Pattern:**
```html
<div class="legend">
    <div class="legend-item">
        <div class="legend-box" style="background: #4299e1;"></div>
        <span>[DESCRIPTION]</span>
    </div>
    <!-- More items -->
</div>
```

**CSS:**
```css
.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
    background: #edf2f7;
    border-radius: 10px;
}
```

## SVG Styling

### Default SVG Styles

**Container:**
```css
svg {
    width: 100%;
    height: auto;
}
```

**Text:**
```css
svg text {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
```

### Common Stroke/Fill Combinations

**Primary Box:**
- Fill: `#4299e1`
- Stroke: `#2b6cb0`
- Stroke-width: `3`

**Success Box:**
- Fill: `#48bb78`
- Stroke: `#2f855a`
- Stroke-width: `3`

**Warning Box:**
- Fill: `#f59e0b`
- Stroke: `#d97706`
- Stroke-width: `3`

**Neutral/Pending:**
- Fill: `#cbd5e0`
- Stroke: `#a0aec0`
- Stroke-width: `2-3`

### ViewBox Guidelines

**Common Aspect Ratios:**
- Wide: `viewBox="0 0 1200 400"` (3:1)
- Standard: `viewBox="0 0 1200 600"` (2:1)
- Balanced: `viewBox="0 0 1200 800"` (3:2)
- Square: `viewBox="0 0 600 600"` (1:1)
- Portrait: `viewBox="0 0 800 1000"` (4:5)

**Coordinate System:**
- Origin: Top-left (0, 0)
- X increases rightward
- Y increases downward
- Units are relative to viewBox

## Accessibility

### Color Blindness

**Safe Patterns:**
- Don't rely on color alone (use icons, labels, patterns)
- Use both fill and stroke for differentiation
- Ensure shapes differ (circle vs square vs diamond)
- Add text labels to all visual elements

**Color Combinations to Avoid:**
- Red/green alone (common color blindness)
- Blue/purple alone (hard to distinguish)
- Low contrast combinations

### Screen Readers

**HTML Structure:**
- Use semantic tags: `<section>`, `<article>`, `<header>`, `<footer>`
- Proper heading hierarchy: h1 → h2 → h3
- Descriptive text around SVG diagrams

**ARIA (if needed):**
```html
<svg aria-labelledby="chart-title" role="img">
    <title id="chart-title">Process Flow Diagram</title>
    <!-- SVG content -->
</svg>
```

### Keyboard Navigation

- Ensure all interactive elements are focusable
- Visible focus indicators
- Logical tab order

## Animation (Optional)

### Subtle Transitions

**Hover Effects:**
```css
.metric-card {
    transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}
```

**Fade In:**
```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.section {
    animation: fadeIn 0.5s ease-in;
}
```

**Note:** Keep animations subtle and optional - avoid distracting from content.

---

## Reference: Svg_Library

# SVG Component Library

Comprehensive reference for SVG shapes, patterns, and techniques for creating stunning diagrams.

## SVG Fundamentals

### Basic Structure

```xml
<svg viewBox="0 0 1200 800" style="width: 100%; height: auto;">
    <defs>
        <!-- Reusable definitions (markers, gradients, patterns) -->
    </defs>

    <g id="group-name">
        <!-- Grouped elements -->
    </g>

    <!-- Direct elements -->
</svg>
```

### ViewBox Explained

**Format:** `viewBox="min-x min-y width height"`
**Example:** `viewBox="0 0 1200 800"`

- **min-x, min-y:** Usually `0 0` (top-left origin)
- **width, height:** Virtual coordinate system dimensions
- SVG scales to fit container while maintaining aspect ratio
- Larger viewBox = more space for content

**Common Sizes:**
```xml
<!-- Wide flowchart -->
<svg viewBox="0 0 1200 400">

<!-- Standard diagram -->
<svg viewBox="0 0 1200 600">

<!-- Detailed flowchart -->
<svg viewBox="0 0 1200 800">

<!-- Square chart -->
<svg viewBox="0 0 600 600">

<!-- Vertical timeline -->
<svg viewBox="0 0 800 1000">
```

### Coordinate System

- **X-axis:** Left (0) to right (positive)
- **Y-axis:** Top (0) to bottom (positive)
- **Center of 1200×800 viewBox:** `(600, 400)`
- **Units:** Relative to viewBox (not pixels)

## Basic Shapes

### Rectangle

**Standard Rectangle:**
```xml
<rect x="100" y="100" width="200" height="100"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
```

**Rounded Rectangle:**
```xml
<rect x="100" y="100" width="200" height="100" rx="10"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
```
- `rx`: Horizontal corner radius
- `ry`: Vertical corner radius (defaults to `rx` if omitted)

**Process Box with Text:**
```xml
<rect x="50" y="50" width="200" height="100" rx="10"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
<text x="150" y="95" text-anchor="middle" fill="white"
      font-size="16" font-weight="bold">
    Process Name
</text>
<text x="150" y="115" text-anchor="middle" fill="white" font-size="12">
    Subtitle
</text>
```

**Position Calculation:**
- Text X: `rect.x + (rect.width / 2)` for center
- Text Y: `rect.y + (rect.height / 2)` for vertical center (approximately)
- Baseline adjustment: Add `5-10px` to Y for visual centering

### Circle

**Basic Circle:**
```xml
<circle cx="300" cy="200" r="50"
        fill="#48bb78" stroke="#2f855a" stroke-width="3"/>
```
- `cx, cy`: Center coordinates
- `r`: Radius

**Circle with Text (Start/End Node):**
```xml
<circle cx="300" cy="200" r="50"
        fill="#48bb78" stroke="#2f855a" stroke-width="3"/>
<text x="300" y="205" text-anchor="middle" fill="white"
      font-size="16" font-weight="bold">
    START
</text>
```

**Small Marker Circle:**
```xml
<circle cx="300" cy="200" r="15"
        fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
```

### Ellipse

```xml
<ellipse cx="400" cy="200" rx="120" ry="60"
         fill="#9f7aea" stroke="#6b46c1" stroke-width="3"/>
```
- `rx`: Horizontal radius
- `ry`: Vertical radius

## Path Shapes

### Diamond (Decision Node)

**Diamond Formula:**
```
Top:    (center-x, top-y)
Right:  (right-x, center-y)
Bottom: (center-x, bottom-y)
Left:   (left-x, center-y)
```

**Example (100px wide, 100px tall, centered at 600, 150):**
```xml
<path d="M 600 100 L 650 150 L 600 200 L 550 150 Z"
      fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
<text x="600" y="155" text-anchor="middle" font-size="14" font-weight="bold">
    Decision?
</text>
```

**Larger Diamond (200×100):**
```xml
<path d="M 600 130 L 700 130 L 750 180 L 700 230 L 500 230 L 450 180 Z"
      fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
```

### Hexagon (Preparation)

**Horizontal Hexagon:**
```xml
<path d="M 900 75 L 1050 75 L 1100 100 L 1050 125 L 900 125 L 850 100 Z"
      fill="#9f7aea" stroke="#6b46c1" stroke-width="3"/>
```

**Pattern:**
```
M [left-mid-x] [top-y]          (start left of top edge)
L [right-mid-x] [top-y]         (top edge)
L [right-x] [center-y]          (top-right slope)
L [right-mid-x] [bottom-y]      (bottom edge)
L [left-mid-x] [bottom-y]       (bottom edge)
L [left-x] [center-y]           (top-left slope)
Z                                (close path)
```

### Parallelogram

```xml
<path d="M 100 100 L 280 100 L 250 150 L 70 150 Z"
      fill="#ed8936" stroke="#c05621" stroke-width="3"/>
```

### Custom Polygons

**Triangle:**
```xml
<path d="M 500 100 L 600 200 L 400 200 Z"
      fill="#f56565" stroke="#c53030" stroke-width="3"/>
```

**Pentagon:**
```xml
<path d="M 500 100 L 580 150 L 550 230 L 450 230 L 420 150 Z"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>
```

## Lines & Arrows

### Straight Lines

**Horizontal:**
```xml
<line x1="100" y1="200" x2="300" y2="200"
      stroke="#2d3748" stroke-width="3"/>
```

**Vertical:**
```xml
<line x1="200" y1="100" x2="200" y2="300"
      stroke="#2d3748" stroke-width="3"/>
```

**Diagonal:**
```xml
<line x1="100" y1="100" x2="300" y2="300"
      stroke="#2d3748" stroke-width="3"/>
```

**Dashed Line:**
```xml
<line x1="100" y1="200" x2="300" y2="200"
      stroke="#cbd5e0" stroke-width="2" stroke-dasharray="5,5"/>
```
- `stroke-dasharray="dash,gap"`: Pattern of dashes and gaps
- Common patterns: `"5,5"` (small), `"10,5"` (medium), `"20,10"` (large)

### Path-based Lines

**Straight line with path:**
```xml
<path d="M 100 200 L 300 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```
- `fill="none"`: Prevents filling (required for non-closed paths used as lines)

**L-shaped connector:**
```xml
<path d="M 250 100 L 400 100 L 400 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```

**Multi-segment:**
```xml
<path d="M 100 100 L 200 100 L 200 200 L 300 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```

### Arrow Markers

**Standard Arrowhead Definition:**
```xml
<defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#2d3748"/>
    </marker>
</defs>
```
- `markerWidth/Height`: Size of marker viewport
- `refX/refY`: Anchor point (where arrow attaches to line)
- `orient="auto"`: Rotates to match line angle

**Colored Arrows:**
```xml
<defs>
    <marker id="arrowhead-success" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#48bb78"/>
    </marker>

    <marker id="arrowhead-error" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#f56565"/>
    </marker>
</defs>
```

**Using Arrows:**
```xml
<!-- Arrow at end -->
<path d="M 100 200 L 300 200" stroke="#2d3748" stroke-width="3"
      fill="none" marker-end="url(#arrowhead)"/>

<!-- Arrow at start -->
<path d="M 100 200 L 300 200" stroke="#2d3748" stroke-width="3"
      fill="none" marker-start="url(#arrowhead)"/>

<!-- Arrows at both ends -->
<path d="M 100 200 L 300 200" stroke="#2d3748" stroke-width="3"
      fill="none" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)"/>
```

### Curved Lines (Bezier Curves)

**Quadratic Bezier (Q):**
```xml
<path d="M 100 200 Q 200 100 300 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```
- Format: `Q control-x control-y end-x end-y`
- One control point

**Cubic Bezier (C):**
```xml
<path d="M 100 200 C 150 100, 250 100, 300 200"
      stroke="#2d3748" stroke-width="3" fill="none"/>
```
- Format: `C control1-x control1-y control2-x control2-y end-x end-y`
- Two control points (more control)

**Smooth Curve Through Points:**
```xml
<path d="M 100 200 Q 150 150 200 200 T 300 200"
      stroke="#4299e1" stroke-width="3" fill="none"/>
```
- `T`: Smooth continuation of quadratic curve

## Text Elements

### Basic Text

```xml
<text x="100" y="100" font-size="16" fill="#2d3748">
    Simple Text
</text>
```

### Text Anchoring

**Horizontal Alignment:**
```xml
<!-- Left-aligned (default) -->
<text x="100" y="100" text-anchor="start">Left</text>

<!-- Center-aligned -->
<text x="100" y="100" text-anchor="middle">Center</text>

<!-- Right-aligned -->
<text x="100" y="100" text-anchor="end">Right</text>
```

**Vertical Alignment:**
```xml
<!-- Baseline (default) -->
<text x="100" y="100" dominant-baseline="auto">Baseline</text>

<!-- Middle -->
<text x="100" y="100" dominant-baseline="middle">Middle</text>

<!-- Hanging (top) -->
<text x="100" y="100" dominant-baseline="hanging">Top</text>
```

**Note:** For reliable vertical centering, calculate Y position manually rather than relying on dominant-baseline (browser support varies).

### Text Styling

```xml
<text x="100" y="100"
      font-size="18"
      font-weight="bold"
      font-style="italic"
      fill="#2d3748"
      opacity="0.8">
    Styled Text
</text>
```

**Font Families in SVG:**
```xml
<text x="100" y="100" font-family="'Segoe UI', sans-serif">
    Custom Font
</text>
```

### Multi-line Text

**Using Multiple <text> Elements:**
```xml
<text x="150" y="90" text-anchor="middle" fill="white" font-size="16" font-weight="bold">
    Line 1
</text>
<text x="150" y="110" text-anchor="middle" fill="white" font-size="12">
    Line 2
</text>
<text x="150" y="125" text-anchor="middle" fill="white" font-size="11">
    Line 3
</text>
```

**Line Spacing:** Typically 15-25px between lines depending on font size

### Text on Path

```xml
<defs>
    <path id="curve" d="M 100 200 Q 300 100 500 200" fill="none"/>
</defs>

<text font-size="16" fill="#2d3748">
    <textPath href="#curve">
        Text following the curve
    </textPath>
</text>
```

## Gradients

### Linear Gradient

```xml
<defs>
    <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#4299e1;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#2b6cb0;stop-opacity:1" />
    </linearGradient>
</defs>

<rect x="100" y="100" width="200" height="100" fill="url(#blueGradient)"/>
```

**Gradient Directions:**
- Horizontal: `x1="0%" y1="0%" x2="100%" y2="0%"`
- Vertical: `x1="0%" y1="0%" x2="0%" y2="100%"`
- Diagonal: `x1="0%" y1="0%" x2="100%" y2="100%"`

### Radial Gradient

```xml
<defs>
    <radialGradient id="radialGlow">
        <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#764ba2;stop-opacity:0.5" />
    </radialGradient>
</defs>

<circle cx="300" cy="200" r="80" fill="url(#radialGlow)"/>
```

### Multi-stop Gradients

```xml
<linearGradient id="multiColor" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" style="stop-color:#48bb78" />
    <stop offset="50%" style="stop-color:#f59e0b" />
    <stop offset="100%" style="stop-color:#f56565" />
</linearGradient>
```

## Grouping & Reuse

### Groups (<g>)

```xml
<g id="icon-group" transform="translate(100, 100)">
    <circle r="30" fill="#4299e1"/>
    <text y="5" text-anchor="middle" fill="white" font-weight="bold">✓</text>
</g>
```

**Benefits:**
- Apply transformations to multiple elements
- Organize related elements
- Apply styles to all children

### Use Element

**Define once:**
```xml
<defs>
    <g id="status-icon">
        <circle r="15" fill="#48bb78" stroke="#2f855a" stroke-width="2"/>
        <text text-anchor="middle" fill="white" font-size="12" font-weight="bold">✓</text>
    </g>
</defs>
```

**Reuse multiple times:**
```xml
<use href="#status-icon" x="100" y="100"/>
<use href="#status-icon" x="300" y="100"/>
<use href="#status-icon" x="500" y="100"/>
```

### Symbol Element

```xml
<defs>
    <symbol id="check-icon" viewBox="0 0 30 30">
        <circle cx="15" cy="15" r="15" fill="#48bb78"/>
        <path d="M 8 15 L 13 20 L 22 10" stroke="white" stroke-width="3"
              fill="none" stroke-linecap="round"/>
    </symbol>
</defs>

<use href="#check-icon" x="100" y="100" width="30" height="30"/>
<use href="#check-icon" x="200" y="100" width="50" height="50"/>
```

**Symbol vs Group:**
- Symbol has its own viewBox (scalable)
- Symbol not rendered unless used
- Better for reusable icons

## Transformations

### Translate (Move)

```xml
<rect x="0" y="0" width="100" height="50" fill="#4299e1"
      transform="translate(200, 100)"/>
```
- Moves shape to new position
- Original x, y still apply (total position = original + translate)

### Rotate

```xml
<rect x="100" y="100" width="100" height="50" fill="#4299e1"
      transform="rotate(45 150 125)"/>
```
- Format: `rotate(angle center-x center-y)`
- Angle in degrees
- Rotates around specified center point

### Scale

```xml
<circle cx="200" cy="200" r="30" fill="#48bb78"
        transform="scale(1.5)"/>
```
- `scale(factor)`: Uniform scaling
- `scale(x-factor, y-factor)`: Non-uniform scaling

### Combined Transformations

```xml
<rect x="0" y="0" width="100" height="50" fill="#4299e1"
      transform="translate(200, 100) rotate(15) scale(1.2)"/>
```
- Applied right to left: scale → rotate → translate

## Advanced Patterns

### Rounded Progress Bar

```xml
<!-- Background -->
<rect x="150" y="80" width="800" height="40" rx="20" fill="#e2e8f0"/>

<!-- Progress (60%) -->
<rect x="150" y="80" width="480" height="40" rx="20" fill="#48bb78"/>
```

### Donut Chart (Simplified)

```xml
<circle cx="300" cy="300" r="150" fill="none"
        stroke="#4299e1" stroke-width="80"/>
```

**Multi-segment Donut:**
```xml
<!-- Segment 1 (50% of circle = 471 units out of 942 total circumference) -->
<circle cx="300" cy="300" r="150" fill="none"
        stroke="#4299e1" stroke-width="80"
        stroke-dasharray="471 471"
        transform="rotate(-90 300 300)"/>

<!-- Segment 2 (30%) -->
<circle cx="300" cy="300" r="150" fill="none"
        stroke="#48bb78" stroke-width="80"
        stroke-dasharray="283 659"
        stroke-dashoffset="-471"
        transform="rotate(-90 300 300)"/>
```

**Circumference Formula:** `2 × π × radius = 2 × 3.14159 × 150 ≈ 942`

### Drop Shadow Filter

```xml
<defs>
    <filter id="drop-shadow">
        <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
        <feOffset dx="2" dy="2" result="offsetblur"/>
        <feMerge>
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
</defs>

<rect x="100" y="100" width="200" height="100" rx="10"
      fill="#4299e1" filter="url(#drop-shadow)"/>
```

### Clipping Path

```xml
<defs>
    <clipPath id="rounded-clip">
        <rect x="100" y="100" width="200" height="150" rx="15"/>
    </clipPath>
</defs>

<image x="100" y="100" width="200" height="150"
       href="image.jpg" clip-path="url(#rounded-clip)"/>
```

## Chart Components

### Bar Chart Bar

```xml
<rect x="200" y="150" width="150" height="200" rx="5"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="2"/>
<text x="275" y="260" text-anchor="middle" fill="white"
      font-size="24" font-weight="bold">
    456
</text>
```

### Axis Lines

```xml
<!-- X-axis -->
<line x1="100" y1="350" x2="1100" y2="350"
      stroke="#2d3748" stroke-width="2"/>

<!-- Y-axis -->
<line x1="100" y1="350" x2="100" y2="80"
      stroke="#2d3748" stroke-width="2"/>

<!-- Grid lines -->
<line x1="100" y1="280" x2="1100" y2="280"
      stroke="#e2e8f0" stroke-width="1" opacity="0.5"/>
```

### Data Point Marker

```xml
<circle cx="300" cy="200" r="6" fill="#4299e1"
        stroke="white" stroke-width="2"/>
```

## Best Practices

### Coordinate Calculation

**Center Text in Rectangle:**
```javascript
textX = rectX + (rectWidth / 2)
textY = rectY + (rectHeight / 2) + (fontSize * 0.35)
```

**Position Diamond Points:**
```javascript
centerX = 600, centerY = 180
halfWidth = 100, halfHeight = 50

top:    (centerX, centerY - halfHeight)
right:  (centerX + halfWidth, centerY)
bottom: (centerX, centerY + halfHeight)
left:   (centerX - halfWidth, centerY)
```

### Performance Tips

- Limit total SVG elements per diagram to ~500-1000
- Use `<use>` for repeated elements
- Avoid overly complex paths
- Minimize filter usage (shadows, blurs)
- Group related elements

### Readability Guidelines

- Minimum stroke-width: 2px for visibility
- Minimum font-size: 11px for labels, 14px for emphasis
- Minimum touch target: 30×30px for interactive elements
- White space: 20-30px between major elements
- Contrast: Stroke should be darker than fill

### Debugging SVG

**Visible Boundaries:**
```xml
<!-- Temporary: shows viewBox boundary -->
<rect x="0" y="0" width="1200" height="800"
      fill="none" stroke="red" stroke-width="1"/>
```

**Grid Overlay:**
```xml
<!-- Shows 100px grid -->
<line x1="0" y1="100" x2="1200" y2="100" stroke="pink" stroke-width="1"/>
<line x1="0" y1="200" x2="1200" y2="200" stroke="pink" stroke-width="1"/>
<!-- ... repeat for debugging ... -->
```

## Icon Library

### Checkmark

```xml
<path d="M 8 15 L 13 20 L 22 10"
      stroke="#48bb78" stroke-width="3" fill="none"
      stroke-linecap="round" stroke-linejoin="round"/>
```

### X (Close)

```xml
<path d="M 10 10 L 20 20 M 20 10 L 10 20"
      stroke="#f56565" stroke-width="3"
      stroke-linecap="round"/>
```

### Warning Triangle

```xml
<path d="M 15 5 L 25 23 L 5 23 Z"
      fill="#f59e0b" stroke="#d97706" stroke-width="2"/>
<text x="15" y="20" text-anchor="middle" fill="white"
      font-weight="bold" font-size="14">!</text>
```

### Info Circle

```xml
<circle cx="15" cy="15" r="12" fill="#4299e1" stroke="#2b6cb0" stroke-width="2"/>
<text x="15" y="20" text-anchor="middle" fill="white"
      font-weight="bold" font-size="16">i</text>
```
