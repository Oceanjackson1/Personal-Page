---
title: "Debug & Optimize LCP"
description: "使用 Chrome DevTools 调试和优化最大内容绘制 (LCP) 性能指标"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Chrome DevTools MCP"
tags: ["performance", "lcp", "core-web-vitals", "optimization"]
date: 2026-03-20
---

## What is LCP and why it matters

Largest Contentful Paint (LCP) measures how quickly a page's main content becomes visible. It's the time from navigation start until the largest image or text block renders in the viewport.

- **Good**: 2.5 seconds or less
- **Needs improvement**: 2.5–4.0 seconds
- **Poor**: greater than 4.0 seconds

LCP is a Core Web Vital that directly affects user experience and search ranking. On 73% of mobile pages, the LCP element is an image.

## LCP Subparts Breakdown

Every page's LCP breaks down into four sequential subparts with no gaps or overlaps. Understanding which subpart is the bottleneck is the key to effective optimization.

| Subpart                       | Ideal % of LCP | What it measures                               |
| ----------------------------- | -------------- | ---------------------------------------------- |
| **Time to First Byte (TTFB)** | ~40%           | Navigation start → first byte of HTML received |
| **Resource load delay**       | <10%           | TTFB → browser starts loading the LCP resource |
| **Resource load duration**    | ~40%           | Time to download the LCP resource              |
| **Element render delay**      | <10%           | LCP resource downloaded → LCP element rendered |

The "delay" subparts should be as close to zero as possible. If either delay subpart is large relative to the total LCP, that's the first place to optimize.

**Common Pitfall**: Optimizing one subpart (like compressing an image to reduce load duration) without checking others. If render delay is the real bottleneck, a smaller image won't help — the saved time just shifts to render delay.

## Debugging Workflow

Follow these steps in order. Each step builds on the previous one.

### Step 1: Record a Performance Trace

Navigate to the page, then record a trace with reload to capture the full page load including LCP:

1. `navigate_page` to the target URL.
2. `performance_start_trace` with `reload: true` and `autoStop: true`.

The trace results will include LCP timing and available insight sets. Note the insight set IDs from the output — you'll need them in the next step.

### Step 2: Analyze LCP Insights

Use `performance_analyze_insight` to drill into LCP-specific insights. Look for these insight names in the trace results:

- **LCPBreakdown** — Shows the four LCP subparts with timing for each.
- **DocumentLatency** — Server response time issues affecting TTFB.
- **RenderBlocking** — Resources blocking the LCP element from rendering.
- **LCPDiscovery** — Whether the LCP resource was discoverable early.

Call `performance_analyze_insight` with the insight name and the insight set ID from the trace results.

### Step 3: Identify the LCP Element

Use `evaluate_script` with the **"Identify LCP Element" snippet** found in [references/lcp-snippets.md](references/lcp-snippets.md) to reveal the LCP element's tag, resource URL, and raw timing data.

The `url` field tells you what resource to look for in the network waterfall. If `url` is empty, the LCP element is text-based (no resource to load).

### Step 4: Check the Network Waterfall

Use `list_network_requests` to see when the LCP resource loaded relative to other resources:

- Call `list_network_requests` filtered by `resourceTypes: ["Image", "Font"]` (adjust based on Step 3).
- Then use `get_network_request` with the LCP resource's request ID for full details.

**Key Checks:**

- **Start Time**: Compare against the HTML document and the first resource. If the LCP resource starts much later than the first resource, there's resource load delay to eliminate.
- **Duration**: A large resource load duration suggests the file is too big or the server is slow.

### Step 5: Inspect HTML for Common Issues

Use `evaluate_script` with the **"Audit Common Issues" snippet** found in [references/lcp-snippets.md](references/lcp-snippets.md) to check for lazy-loaded images in the viewport, missing fetchpriority, and render-blocking scripts.

## Optimization Strategies

After identifying the bottleneck subpart, apply these prioritized fixes.

### 1. Eliminate Resource Load Delay (target: <10%)

The most common bottleneck. The LCP resource should start loading immediately.

- **Root Cause**: LCP image loaded via JS/CSS, `data-src` usage, or `loading="lazy"`.
- **Fix**: Use standard `<img>` with `src`. **Never** lazy-load the LCP image.
- **Fix**: Add `<link rel="preload" fetchpriority="high">` if the image isn't discoverable in HTML.
- **Fix**: Add `fetchpriority="high"` to the LCP `<img>` tag.

### 2. Eliminate Element Render Delay (target: <10%)

The element should render immediately after loading.

- **Root Cause**: Large stylesheets, synchronous scripts in `<head>`, or main thread blocking.
- **Fix**: Inline critical CSS, defer non-critical CSS/JS.
- **Fix**: Break up long tasks blocking the main thread.
- **Fix**: Use Server-Side Rendering (SSR) so the element exists in initial HTML.

### 3. Reduce Resource Load Duration (target: ~40%)

Make the resource smaller or faster to deliver.

- **Fix**: Use modern formats (WebP, AVIF) and responsive images (`srcset`).
- **Fix**: Serve from a CDN.
- **Fix**: Set `Cache-Control` headers.
- **Fix**: Use `font-display: swap` if LCP is text blocked by a web font.

### 4. Reduce TTFB (target: ~40%)

The HTML document itself takes too long to arrive.

- **Fix**: Minimize redirects and optimize server response time.
- **Fix**: Cache HTML at the edge (CDN).
- **Fix**: Ensure pages are eligible for back/forward cache (bfcache).

## Verifying Fixes & Emulation

- **Verification**: Re-run the trace (`performance_start_trace` with `reload: true`) and compare the new subpart breakdown. The bottleneck should shrink.
- **Emulation**: Lab measurements differ from real-world experience. Use `emulate` to test under constraints:
  - `emulate` with `networkConditions: "Fast 3G"` and `cpuThrottlingRate: 4`.
  - This surfaces issues visible only on slower connections/devices.

---

## Reference: Elements And Size

# Elements and Size for LCP

## What Elements are Considered?

The types of elements considered for Largest Contentful Paint (LCP) are:

- **`<img>` elements**: The first frame presentation time is used for animated content like GIFs.
- **`<image>` elements** inside an `<svg>` element.
- **`<video>` elements**: The poster image load time or first frame presentation time, whichever is earlier.
- **Background images**: Elements with a background image loaded using `url()`.
- **Block-level elements**: Containing text nodes or other inline-level text element children.

## Heuristics to Exclude Non-Contentful Elements

Chromium-based browsers use heuristics to exclude:

- Elements with **opacity of 0**.
- Elements that **cover the full viewport** (likely background).
- **Placeholder images** or low-entropy images.

## How is an Element's Size Determined?

- **Visible Area**: Typically the size visible within the viewport. Extending outside, clipped, or overflow portions don't count.
- **Image Elements**: Either the visible size or the intrinsic size, whichever is smaller.
- **Text Elements**: The smallest rectangle containing all text nodes.
- **Exclusions**: Margin, padding, and borders are not considered toward the size.
- **Containment**: Every text node belongs to its closest block-level ancestor element.

---

## Reference: Lcp Breakdown

# Largest Contentful Paint (LCP) Breakdown

LCP measures the time from when the user initiates loading the page until the largest image or text block is rendered within the viewport. To provide a good user experience, sites should strive to have an LCP of 2.5 seconds or less for at least 75% of page visits.

## The Four Subparts of LCP

Every page's LCP consists of these four subcategories. There's no gap or overlap between them, and they add up to the full LCP time.

| LCP subpart                   | % of LCP (Optimal) | Description                                                                                                                                                              |
| ----------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Time to First Byte (TTFB)** | ~40%               | The time from when the user initiates loading the page until the browser receives the first byte of the HTML document response.                                          |
| **Resource load delay**       | <10%               | The time between TTFB and when the browser starts loading the LCP resource. If the LCP element doesn't require a resource load (e.g., system font text), this time is 0. |
| **Resource load duration**    | ~40%               | The duration of time it takes to load the LCP resource itself. If the LCP element doesn't require a resource load, this time is 0.                                       |
| **Element render delay**      | <10%               | The time between when the LCP resource finishes loading and the LCP element rendering fully.                                                                             |

## Why the Breakdown Matters

Optimizing for LCP requires identifying which of these subparts is the bottleneck:

- **Large delta between TTFB and FCP**: Indicates the browser needs to download a lot of render-blocking assets or complete a lot of work (e.g., client-side rendering).
- **Large delta between FCP and LCP**: Indicates the LCP resource is not immediately available for the browser to prioritize or the browser is completing other work before it can display the LCP content.
- **Large resource load delay**: Indicates the resource is not discoverable early or is deprioritized.
- **Large element render delay**: Indicates rendering is blocked by stylesheets, scripts, or long tasks.

---

## Reference: Lcp Snippets

# LCP Debugging Snippets

Use these JavaScript snippets with the `evaluate_script` tool to extract deep insights from the page.

## 1. Identify LCP Element

Use this snippet to identify the LCP element and get raw timing data from the Performance API.

```javascript
async () => {
  return await new Promise(resolve => {
    new PerformanceObserver(list => {
      const entries = list.getEntries();
      const last = entries[entries.length - 1];
      resolve({
        element: last.element?.tagName,
        id: last.element?.id,
        className: last.element?.className,
        url: last.url,
        startTime: last.startTime,
        renderTime: last.renderTime,
        loadTime: last.loadTime,
        size: last.size,
      });
    }).observe({type: 'largest-contentful-paint', buffered: true});
  });
};
```

## 2. Audit Common Issues

Use this snippet to check for common DOM-based LCP issues (lazy loading, priority).

```javascript
() => {
  const issues = [];

  // Check for lazy-loaded images in viewport
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    const rect = img.getBoundingClientRect();
    if (rect.top < window.innerHeight) {
      issues.push({
        issue: 'lazy-loaded image in viewport',
        element: img.outerHTML.substring(0, 200),
        fix: 'Remove loading="lazy" from this image — it is in the initial viewport and may be the LCP element',
      });
    }
  });

  // Check for LCP-candidate images missing fetchpriority
  document.querySelectorAll('img:not([fetchpriority])').forEach(img => {
    const rect = img.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.width * rect.height > 50000) {
      issues.push({
        issue: 'large viewport image without fetchpriority',
        element: img.outerHTML.substring(0, 200),
        fix: 'Add fetchpriority="high" to this image — it is large and visible in the initial viewport',
      });
    }
  });

  // Check for render-blocking scripts in head
  document
    .querySelectorAll(
      'head script:not([async]):not([defer]):not([type="module"])',
    )
    .forEach(script => {
      if (script.src) {
        issues.push({
          issue: 'render-blocking script in head',
          element: script.outerHTML.substring(0, 200),
          fix: 'Add async or defer attribute, or move to end of body',
        });
      }
    });

  return {issueCount: issues.length, issues};
};
```

---

## Reference: Optimization Strategies

# LCP Optimization Strategies

## 1. Eliminate Resource Load Delay

**Goal**: Ensure the LCP resource starts loading as early as possible.

- **Early Discovery**: Ensure the LCP resource is discoverable in the initial HTML document response (not dynamically added by JS or hidden in `data-src`).
- **Preload**: Use `<link rel="preload">` with `fetchpriority="high"` for critical images or fonts.
- **Avoid Lazy Loading**: Never set `loading="lazy"` on the LCP image.
- **Fetch Priority**: Use `fetchpriority="high"` on the `<img>` tag.
- **Same Origin**: Host critical resources on the same origin or use `<link rel="preconnect">`.

## 2. Eliminate Element Render Delay

**Goal**: Ensure the LCP element can render immediately after its resource has finished loading.

- **Minimize Render-Blocking CSS**: Inline critical CSS and defer non-critical CSS. Ensure the stylesheet is smaller than the LCP resource.
- **Minimize Render-Blocking JS**: Avoid synchronous scripts in the `<head>`. Inline very small scripts.
- **Server-Side Rendering (SSR)**: Deliver the full HTML markup from the server so image resources are discoverable immediately.
- **Break Up Long Tasks**: Prevent large JavaScript tasks from blocking the main thread during rendering.

## 3. Reduce Resource Load Duration

**Goal**: Reduce the time spent transferring the bytes of the resource.

- **Optimize Resource Size**: Serve optimal image sizes, use modern formats (AVIF, WebP), and compress images/fonts.
- **Geographic Proximity (CDN)**: Use a Content Delivery Network to get servers closer to users.
- **Reduce Contention**: Use `fetchpriority="high"` to prevent lower-priority resources from competing for bandwidth.
- **Caching**: Use efficient `Cache-Control` policies.

## 4. Reduce Time to First Byte (TTFB)

**Goal**: Deliver the initial HTML as quickly as possible.

- **Minimize Redirects**: Avoid multiple redirects from advertisements or shortened links.
- **CDN Caching**: Cache static HTML documents at the edge.
- **Edge Computing**: Move dynamic logic to the edge to avoid trips to the origin server.
- **Back/Forward Cache**: Ensure pages are eligible for bfcache.
