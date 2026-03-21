---
title: "Web Scraper"
description: "Web scraping inteligente multi-estrategia. Extrai dados estruturados de paginas web (tabelas, listas, precos). Paginacao, monitoramento e export CSV/JSON."
category: "development"
source: "community"
author: "Community"
tags: ["web", "scraper"]
date: 2026-03-20
---

# Web Scraper

## Overview

Web scraping inteligente multi-estrategia. Extrai dados estruturados de paginas web (tabelas, listas, precos). Paginacao, monitoramento e export CSV/JSON.

## When to Use This Skill

- When the user mentions "scraper" or related topics
- When the user mentions "scraping" or related topics
- When the user mentions "extrair dados web" or related topics
- When the user mentions "web scraping" or related topics
- When the user mentions "raspar dados" or related topics
- When the user mentions "coletar dados site" or related topics

## Do Not Use This Skill When

- The task is unrelated to web scraper
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Execute phases in strict order. Each phase feeds the next.

```
1. CLARIFY  ->  2. RECON  ->  3. STRATEGY  ->  4. EXTRACT  ->  5. TRANSFORM  ->  6. VALIDATE  ->  7. FORMAT
```

Never skip Phase 1 or Phase 2. They prevent wasted effort and failed extractions.

**Fast path**: If user provides URL + clear data target + the request is simple
(single page, one data type), compress Phases 1-3 into a single action:
fetch, classify, and extract in one WebFetch call. Still validate and format.

---

## Capabilities

- **Multi-strategy**: WebFetch (static), Browser automation (JS-rendered), Bash/curl (APIs), WebSearch (discovery)
- **Extraction modes**: table, list, article, product, contact, FAQ, pricing, events, jobs, custom
- **Output formats**: Markdown tables (default), JSON, CSV
- **Pagination**: auto-detect and follow (page numbers, infinite scroll, load-more)
- **Multi-URL**: extract same structure across sources with comparison and diff
- **Validation**: confidence ratings (HIGH/MEDIUM/LOW) on every extraction
- **Auto-escalation**: WebFetch fails silently -> automatic Browser fallback
- **Data transforms**: cleaning, normalization, deduplication, enrichment
- **Differential mode**: detect changes between scraping runs

## Web Scraper

Multi-strategy web data extraction with intelligent approach selection,
automatic fallback escalation, data transformation, and structured output.

## Phase 1: Clarify

Establish extraction parameters before touching any URL.

## Required Parameters

| Parameter     | Resolve                              | Default        |
|:--------------|:-------------------------------------|:---------------|
| Target URL(s) | Which page(s) to scrape?             | *(required)*   |
| Data Target   | What specific data to extract?       | *(required)*   |
| Output Format | Markdown table, JSON, CSV, or text?  | Markdown table |
| Scope         | Single page, paginated, or multi-URL?| Single page    |

## Optional Parameters

| Parameter     | Resolve                                | Default      |
|:--------------|:---------------------------------------|:-------------|
| Pagination    | Follow pagination? Max pages?          | No, 1 page   |
| Max Items     | Maximum number of items to collect?    | Unlimited    |
| Filters       | Data to exclude or include?            | None         |
| Sort Order    | How to sort results?                   | Source order  |
| Save Path     | Save to file? Which path?              | Display only |
| Language      | Respond in which language?             | User's lang  |
| Diff Mode     | Compare with previous run?             | No           |

## Clarification Rules

- If user provides a URL and clear data target, proceed directly to Phase 2.
  Do NOT ask unnecessary questions.
- If request is ambiguous (e.g. "scrape this site"), ask ONLY:
  "What specific data do you want me to extract from this page?"
- Default to Markdown table output. Mention alternatives only if relevant.
- Accept requests in any language. Always respond in the user's language.
- If user says "everything" or "all data", perform recon first, then present
  what's available and let user choose.

## Discovery Mode

When user has a topic but no specific URL:
1. Use WebSearch to find the most relevant pages
2. Present top 3-5 URLs with descriptions
3. Let user choose which to scrape, or scrape all
4. Proceed to Phase 2 with selected URL(s)

Example: "find and extract pricing data for CRM tools"
-> WebSearch("CRM tools pricing comparison 2026")
-> Present top results -> User selects -> Extract

---

## Phase 2: Reconnaissance

Analyze the target page before extraction.

## Step 2.1: Initial Fetch

Use WebFetch to retrieve and analyze the page structure:

```
WebFetch(
  url = TARGET_URL,
  prompt = "Analyze this page structure and report:
    1. Page type: article, product listing, search results, data table,
       directory, dashboard, API docs, FAQ, pricing page, job board, events, or other
    2. Main content structure: tables, ordered/unordered lists, card grid, free-form text,
       accordion/collapsible sections, tabs
    3. Approximate number of distinct data items visible
    4. JavaScript rendering indicators: empty containers, loading spinners,
       SPA framework markers (React root, Vue app, Angular), minimal HTML with heavy JS
    5. Pagination: next/prev links, page numbers, load-more buttons,
       infinite scroll indicators, total results count
    6. Data density: how much structured, extractable data exists
    7. List the main data fields/columns available for extraction
    8. Embedded structured data: JSON-LD, microdata, OpenGraph tags
    9. Available download links: CSV, Excel, PDF, API endpoints"
)
```

## Step 2.2: Evaluate Fetch Quality

| Signal                                      | Interpretation                    | Action                    |
|:--------------------------------------------|:----------------------------------|:--------------------------|
| Rich content with data clearly visible      | Static page                       | Strategy A (WebFetch)     |
| Empty containers, "loading...", minimal text | JS-rendered                       | Strategy B (Browser)      |
| Login wall, CAPTCHA, 403/401 response       | Blocked                           | Report to user            |
| Content present but poorly structured       | Needs precision                   | Strategy B (Browser)      |
| JSON or XML response body                   | API endpoint                      | Strategy C (Bash/curl)    |
| Download links for CSV/Excel available      | Direct data file                  | Strategy C (download)     |

## Step 2.3: Content Classification

Classify into an extraction mode:

| Mode       | Indicators                                 | Examples                          |
|:-----------|:-------------------------------------------|:----------------------------------|
| `table`    | HTML `<table>`, grid layout with headers   | Price comparison, statistics, specs|
| `list`     | Repeated similar elements, card grids      | Search results, product listings  |
| `article`  | Long-form text with headings/paragraphs    | Blog post, news article, docs     |
| `product`  | Product name, price, specs, images, rating | E-commerce product page           |
| `contact`  | Names, emails, phones, addresses, roles    | Team page, staff directory        |
| `faq`      | Question-answer pairs, accordions          | FAQ page, help center             |
| `pricing`  | Plan names, prices, features, tiers        | SaaS pricing page                 |
| `events`   | Dates, locations, titles, descriptions     | Event listings, conferences       |
| `jobs`     | Titles, companies, locations, salaries     | Job boards, career pages          |
| `custom`   | User specified CSS selectors or fields     | Anything not matching above       |

Record: **page type**, **extraction mode**, **JS rendering needed (yes/no)**,
**available fields**, **structured data present (JSON-LD etc.)**.

If user asked for "everything", present the available fields and let them choose.

---

## Phase 3: Strategy Selection

Choose the extraction approach based on recon results.

## Decision Tree

```
Structured data (JSON-LD, microdata) has what we need?
 |
 +-- YES --> STRATEGY E: Extract structured data directly
 |
 +-- NO: Content fully visible in WebFetch?
      |
      +-- YES: Need precise element targeting?
      |    |
      |    +-- NO  --> STRATEGY A: WebFetch + AI extraction
      |    +-- YES --> STRATEGY B: Browser automation
      |
      +-- NO: JavaScript rendering detected?
           |
           +-- YES --> STRATEGY B: Browser automation
           +-- NO:  API/JSON/XML endpoint or download link?
                |
                +-- YES --> STRATEGY C: Bash (curl + jq)
                +-- NO  --> Report access issue to user
```

## Strategy A: Webfetch With Ai Extraction

**Best for**: Static pages, articles, simple tables, well-structured HTML.

Use WebFetch with a targeted extraction prompt tailored to the mode:

```
WebFetch(
  url = URL,
  prompt = "Extract [DATA_TARGET] from this page.
    Return ONLY the extracted data as [FORMAT] with these columns/fields: [FIELDS].
    Rules:
    - If a value is missing or unclear, use 'N/A'
    - Do not include navigation, ads, footers, or unrelated content
    - Preserve original values exactly (numbers, currencies, dates)
    - Include ALL matching items, not just the first few
    - For each item, also extract the URL/link if available"
)
```

**Auto-escalation**: If WebFetch returns suspiciously few items (less than
50% of expected from recon), or mostly empty fields, automatically escalate
to Strategy B without asking user. Log the escalation in notes.

## Strategy B: Browser Automation

**Best for**: JS-rendered pages, SPAs, interactive content, lazy-loaded data.

Sequence:
1. Get tab context: `tabs_context_mcp(createIfEmpty=true)` -> get tabId
2. Navigate to URL: `navigate(url=TARGET_URL, tabId=TAB)`
3. Wait for content to load: `computer(action="wait", duration=3, tabId=TAB)`
4. Check for cookie/consent banners: `find(query="cookie consent or accept button", tabId=TAB)`
   - If found, dismiss it (prefer privacy-preserving option)
5. Read page structure: `read_page(tabId=TAB)` or `get_page_text(tabId=TAB)`
6. Locate target elements: `find(query="[DESCRIPTION]", tabId=TAB)`
7. Extract with JavaScript for precise data via `javascript_tool`

```javascript
// Table extraction
const rows = document.querySelectorAll('TABLE_SELECTOR tr');
const data = Array.from(rows).map(row => {
  const cells = row.querySelectorAll('td, th');
  return Array.from(cells).map(c => c.textContent.trim());
});
JSON.stringify(data);
```

```javascript
// List/card extraction
const items = document.querySelectorAll('ITEM_SELECTOR');
const data = Array.from(items).map(item => ({
  field1: item.querySelector('FIELD1_SELECTOR')?.textContent?.trim() || null,
  field2: item.querySelector('FIELD2_SELECTOR')?.textContent?.trim() || null,
  link: item.querySelector('a')?.href || null,
}));
JSON.stringify(data);
```

8. For lazy-loaded content, scroll and re-extract:
   `computer(action="scroll", scroll_direction="down", tabId=TAB)`
   then `computer(action="wait", duration=2, tabId=TAB)`

## Strategy C: Bash (Curl + Jq)

**Best for**: REST APIs, JSON endpoints, XML feeds, CSV/Excel downloads.

```bash

## Json Api

curl -s "API_URL" | jq '[.items[] | {field1: .key1, field2: .key2}]'

## Csv Download

curl -s "CSV_URL" -o /tmp/scraped_data.csv

## Xml Parsing

curl -s "XML_URL" | python3 -c "
import xml.etree.ElementTree as ET, json, sys
tree = ET.parse(sys.stdin)

## ... Parse And Output Json

"
```

## Strategy D: Hybrid

When a single strategy is insufficient, combine:
1. WebSearch to discover relevant URLs
2. WebFetch for initial content assessment
3. Browser automation for JS-heavy sections
4. Bash for post-processing (jq, python for data cleaning)

## Strategy E: Structured Data Extraction

When JSON-LD, microdata, or OpenGraph is present:
1. Use Browser `javascript_tool` to extract structured data:
```javascript
const scripts = document.querySelectorAll('script[type="application/ld+json"]');
const data = Array.from(scripts).map(s => {
  try { return JSON.parse(s.textContent); } catch { return null; }
}).filter(Boolean);
JSON.stringify(data);
```
2. This often provides cleaner, more reliable data than DOM scraping
3. Fall back to DOM extraction only for fields not in structured data

## Pagination Handling

When pagination is detected and user wants multiple pages:

**Page-number pagination (any strategy):**
1. Extract data from current page
2. Identify URL pattern (e.g. `?page=N`, `/page/N`, `&offset=N`)
3. Iterate through pages up to user's max (default: 5 pages)
4. Show progress: "Extracting page 2/5..."
5. Concatenate all results, deduplicate if needed

**Infinite scroll (Browser only):**
1. Extract currently visible data
2. Record item count
3. Scroll down: `computer(action="scroll", scroll_direction="down", tabId=TAB)`
4. Wait: `computer(action="wait", duration=2, tabId=TAB)`
5. Extract newly loaded data
6. Compare count - if no new items after 2 scrolls, stop
7. Repeat until no new content or max iterations (default: 5)

**"Load More" button (Browser only):**
1. Extract currently visible data
2. Find button: `find(query="load more button", tabId=TAB)`
3. Click it: `computer(action="left_click", ref=REF, tabId=TAB)`
4. Wait and extract new content
5. Repeat until button disappears or max iterations reached

---

## Phase 4: Extract

Execute the selected strategy using mode-specific patterns.
See [references/extraction-patterns.md](references/extraction-patterns.md)
for CSS selectors and JavaScript snippets.

## Table Mode

WebFetch prompt:
```
"Extract ALL rows from the table(s) on this page.
Return as a markdown table with exact column headers.
Include every row - do not truncate or summarize.
Preserve numeric precision, currencies, and units."
```

## List Mode

WebFetch prompt:
```
"Extract each [ITEM_TYPE] from this page.
For each item, extract: [FIELD_LIST].
Return as a JSON array of objects with these keys: [KEY_LIST].
Include ALL items, not just the first few. Include link/URL for each item if available."
```

## Article Mode

WebFetch prompt:
```
"Extract article metadata:
- title, author, date, tags/categories, word count estimate
- Key factual data points, statistics, and named entities
Return as structured markdown. Summarize the content; do not reproduce full text."
```

## Product Mode

WebFetch prompt:
```
"Extract product data with these exact fields:
- name, brand, price, currency, originalPrice (if discounted),
  availability, description (first 200 chars), rating, reviewCount,
  specifications (as key-value pairs), productUrl, imageUrl
Return as JSON. Use null for missing fields."
```

Also check for JSON-LD `Product` schema (Strategy E) first.

## Contact Mode

WebFetch prompt:
```
"Extract contact information for each person/entity:
- name, title, role, email, phone, address, organization, website, linkedinUrl
Return as a markdown table. Only extract real contacts visible on the page."
```

## Faq Mode

WebFetch prompt:
```
"Extract all question-answer pairs from this page.
For each FAQ item extract:
- question: the exact question text
- answer: the answer text (first 300 chars if long)
- category: the section/category if grouped
Return as a JSON array of objects."
```

## Pricing Mode

WebFetch prompt:
```
"Extract all pricing plans/tiers from this page.
For each plan extract:
- planName, monthlyPrice, annualPrice, currency
- features (array of included features)
- limitations (array of limits or excluded features)
- ctaText (call-to-action button text)
- highlighted (true if marked as recommended/popular)
Return as JSON. Use null for missing fields."
```

## Events Mode

WebFetch prompt:
```
"Extract all events/sessions from this page.
For each event extract:
- title, date, time, endTime, location, description (first 200 chars)
- speakers (array of names), category, registrationUrl
Return as JSON. Use null for missing fields."
```

## Jobs Mode

WebFetch prompt:
```
"Extract all job listings from this page.
For each job extract:
- title, company, location, salary, salaryRange, type (full-time/part-time/contract)
- postedDate, description (first 200 chars), applyUrl, tags
Return as JSON. Use null for missing fields."
```

## Custom Mode

When user provides specific selectors or field descriptions:
- Use Browser automation with `javascript_tool` and user's CSS selectors
- Or use WebFetch with a prompt built from user's field descriptions
- Always confirm extracted schema with user before proceeding to multi-URL

## Multi-Url Extraction

When extracting from multiple URLs:
1. Extract from the **first URL** to establish the data schema
2. Show user the first results and confirm the schema is correct
3. Extract from remaining URLs using the same schema
4. Add a `source` column/field to every record with the origin URL
5. Combine all results into a single output
6. Show progress: "Extracting 3/7 URLs..."

---

## Phase 5: Transform

Clean, normalize, and enrich extracted data before validation.
See [references/data-transforms.md](references/data-transforms.md) for patterns.

## Automatic Transforms (Always Apply)

| Transform              | Action                                               |
|:-----------------------|:-----------------------------------------------------|
| Whitespace cleanup     | Trim, collapse multiple spaces, remove `\n` in cells |
| HTML entity decode     | `&amp;` -> `&`, `&lt;` -> `<`, `&#39;` -> `'`       |
| Unicode normalization  | NFKC normalization for consistent characters          |
| Empty string to null   | `""` -> `null` (for JSON), `""` -> `N/A` (for tables)|

## Conditional Transforms (Apply When Relevant)

| Transform             | When                         | Action                                  |
|:----------------------|:-----------------------------|:----------------------------------------|
| Price normalization   | Product/pricing modes        | Extract numeric value + currency symbol |
| Date normalization    | Any dates found              | Normalize to ISO-8601 (YYYY-MM-DD)      |
| URL resolution        | Relative URLs extracted      | Convert to absolute URLs                |
| Phone normalization   | Contact mode                 | Standardize to E.164 format if possible |
| Deduplication         | Multi-page or multi-URL      | Remove exact duplicate rows             |
| Sorting               | User requested or natural    | Sort by user-specified field            |

## Data Enrichment (Only When Useful)

| Enrichment             | When                         | Action                                |
|:-----------------------|:-----------------------------|:--------------------------------------|
| Currency conversion    | User asks for single currency| Note original + convert (approximate) |
| Domain extraction      | URLs in data                 | Add domain column from full URLs      |
| Word count             | Article mode                 | Count words in extracted text         |
| Relative dates         | Dates present                | Add "X days ago" column if useful     |

## Deduplication Strategy

When combining data from multiple pages or URLs:
1. Exact match: rows with identical values in all fields -> keep first
2. Near match: rows with same key fields (name+source) but different details
   -> keep most complete (fewer nulls), flag in notes
3. Report: "Removed N duplicate rows" in delivery notes

---

## Phase 6: Validate

Verify extraction quality before delivering results.

## Validation Checks

| Check                | Action                                              |
|:---------------------|:----------------------------------------------------|
| Item count           | Compare extracted count to expected count from recon |
| Empty fields         | Count N/A or null values per field                   |
| Data type consistency| Numbers should be numeric, dates parseable           |
| Duplicates           | Flag exact duplicate rows (post-dedup)               |
| Encoding             | Check for HTML entities, garbled characters           |
| Completeness         | All user-requested fields present in output          |
| Truncation           | Verify data wasn't cut off (check last items)        |
| Outliers             | Flag values that seem anomalous (e.g. $0.00 price)  |

## Confidence Rating

Assign to every extraction:

| Rating     | Criteria                                                        |
|:-----------|:----------------------------------------------------------------|
| **HIGH**   | All fields populated, count matches expected, no anomalies      |
| **MEDIUM** | Minor gaps (<10% empty fields) or count slightly differs        |
| **LOW**    | Significant gaps (>10% empty), structural issues, partial data  |

Always report confidence with specifics:
> Confidence: **HIGH** - 47 items extracted, all 6 fields populated,
> matches expected count from page analysis.

## Auto-Recovery (Try Before Reporting Issues)

| Issue              | Auto-Recovery Action                                  |
|:-------------------|:------------------------------------------------------|
| Missing data       | Re-attempt with Browser if WebFetch was used          |
| Encoding problems  | Apply HTML entity decode + unicode normalization      |
| Incomplete results | Check for pagination or lazy-loading, fetch more      |
| Count mismatch     | Scroll/paginate to find remaining items               |
| All fields empty   | Page likely JS-rendered, switch to Browser strategy   |
| Partial fields     | Try JSON-LD extraction as supplement                  |

Log all recovery attempts in delivery notes.
Inform user of any irrecoverable gaps with specific details.

---

## Phase 7: Format And Deliver

Structure results according to user preference.
See [references/output-templates.md](references/output-templates.md)
for complete formatting templates.

## Delivery Envelope

ALWAYS wrap results with this metadata header:

```markdown

## Extraction Results

**Source:** [Page Title](http://example.com)
**Date:** YYYY-MM-DD HH:MM UTC
**Items:** N records (M fields each)
**Confidence:** HIGH | MEDIUM | LOW
**Strategy:** A (WebFetch) | B (Browser) | C (API) | E (Structured Data)
**Format:** Markdown Table | JSON | CSV

---

[DATA HERE]

---

**Notes:**
- [Any gaps, issues, or observations]
- [Transforms applied: deduplication, normalization, etc.]
- [Pages scraped if paginated: "Pages 1-5 of 12"]
- [Auto-escalation if it occurred: "Escalated from WebFetch to Browser"]
```

## Markdown Table Rules

- Left-align text columns (`:---`), right-align numbers (`---:`)
- Consistent column widths for readability
- Include summary row for numeric data when useful (totals, averages)
- Maximum 10 columns per table; split wider data into multiple tables
  or suggest JSON format
- Truncate long cell values to 60 chars with `...` indicator
- Use `N/A` for missing values, never leave cells empty
- For multi-page results, show combined table (not per-page)

## Json Rules

- Use camelCase for keys (e.g. `productName`, `unitPrice`)
- Wrap in metadata envelope:
  ```json
  {
    "metadata": {
      "source": "URL",
      "title": "Page Title",
      "extractedAt": "ISO-8601",
      "itemCount": 47,
      "fieldCount": 6,
      "confidence": "HIGH",
      "strategy": "A",
      "transforms": ["deduplication", "priceNormalization"],
      "notes": []
    },
    "data": [ ... ]
  }
  ```
- Pretty-print with 2-space indentation
- Numbers as numbers (not strings), booleans as booleans
- null for missing values (not empty strings)

## Csv Rules

- First row is always headers
- Quote any field containing commas, quotes, or newlines
- UTF-8 encoding with BOM for Excel compatibility
- Use `,` as delimiter (standard)
- Include metadata as comments: `# Source: URL`

## File Output

When user requests file save:
- Markdown: `.md` extension
- JSON: `.json` extension
- CSV: `.csv` extension
- Confirm path before writing
- Report full file path and item count after saving

## Multi-Url Comparison Format

When comparing data across multiple sources:
- Add `Source` as the first column/field
- Use short identifiers for sources (domain name or user label)
- Group by source or interleave based on user preference
- Highlight differences if user asks for comparison
- Include summary: "Best price: $X at store-b.com"

## Differential Output

When user requests change detection (diff mode):
- Compare current extraction with previous run
- Mark new items with `[NEW]`
- Mark removed items with `[REMOVED]`
- Mark changed values with `[WAS: old_value]`
- Include summary: "Changes since last run: +5 new, -2 removed, 3 modified"

---

## Rate Limiting

- Maximum 1 request per 2 seconds for sequential page fetches
- For multi-URL jobs, process sequentially with pauses
- If a site returns 429 (Too Many Requests), stop and report to user

## Access Respect

- If a page blocks access (403, CAPTCHA, login wall), report to user
- Do NOT attempt to bypass bot detection, CAPTCHAs, or access controls
- Do NOT scrape behind authentication unless user explicitly provides access
- Respect robots.txt directives when known

## Copyright

- Do NOT reproduce large blocks of copyrighted article text
- For articles: extract factual data, statistics, and structured info;
  summarize narrative content
- Always include source attribution (http://example.com) in output

## Data Scope

- Extract ONLY what the user explicitly requested
- Warn user before collecting potentially sensitive data at scale
  (emails, phone numbers, personal information)
- Do not store or transmit extracted data beyond what the user sees

## Failure Protocol

When extraction fails or is blocked:
1. Explain the specific reason (JS rendering, bot detection, login, etc.)
2. Suggest alternatives (different URL, API if available, manual approach)
3. Never retry aggressively or escalate access attempts

---

## Quick Reference: Mode Cheat Sheet

| User Says...                         | Mode      | Strategy  | Output Default   |
|:-------------------------------------|:----------|:----------|:-----------------|
| "extract the table"                  | table     | A or B    | Markdown table   |
| "get all products/prices"            | product   | E then A  | Markdown table   |
| "scrape the listings"                | list      | A or B    | Markdown table   |
| "extract contact info / team page"   | contact   | A         | Markdown table   |
| "get the article data"               | article   | A         | Markdown text    |
| "extract the FAQ"                    | faq       | A or B    | JSON             |
| "get pricing plans"                  | pricing   | A or B    | Markdown table   |
| "scrape job listings"                | jobs      | A or B    | Markdown table   |
| "get event schedule"                 | events    | A or B    | Markdown table   |
| "find and extract [topic]"           | discovery | WebSearch | Markdown table   |
| "compare prices across sites"        | multi-URL | A or B    | Comparison table |
| "what changed since last time"       | diff      | any       | Diff format      |

---

## References

- **Extraction patterns**: [references/extraction-patterns.md](references/extraction-patterns.md)
  CSS selectors, JavaScript snippets, JSON-LD parsing, domain tips.

- **Output templates**: [references/output-templates.md](references/output-templates.md)
  Markdown, JSON, CSV templates with complete examples.

- **Data transforms**: [references/data-transforms.md](references/data-transforms.md)
  Cleaning, normalization, deduplication, enrichment patterns.

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

---

## Reference: Data Transforms

# Data Transforms Reference

Patterns for cleaning, normalizing, deduplicating, and enriching
extracted web data. Apply these transforms in Phase 5 (Transform)
between extraction and validation.

---

## Automatic Transforms

Always apply these to every extraction result.

### Whitespace Cleanup

```python
# Remove leading/trailing whitespace, collapse internal whitespace
value = ' '.join(value.split())

# Remove zero-width characters
import re
value = re.sub(r'[\u200b\u200c\u200d\ufeff\u00a0]', ' ', value).strip()
```

Patterns to handle:
- `\n`, `\r`, `\t` inside cell values -> single space
- Multiple consecutive spaces -> single space
- Non-breaking spaces (`&nbsp;`, `\u00a0`) -> regular space
- Zero-width characters -> remove

### HTML Entity Decode

| Entity      | Character | Entity     | Character |
|:------------|:----------|:-----------|:----------|
| `&amp;`     | `&`       | `&quot;`   | `"`       |
| `&lt;`      | `<`       | `&apos;`   | `'`       |
| `&gt;`      | `>`       | `&#39;`    | `'`       |
| `&nbsp;`    | ` `       | `&#8217;`  | (curly ')  |
| `&mdash;`   | `--`      | `&#8212;`  | `--`      |

```python
import html
value = html.unescape(value)
```

### Unicode Normalization

```python
import unicodedata
value = unicodedata.normalize('NFKC', value)
```

This handles:
- Fancy quotes -> standard quotes
- Ligatures -> separate characters (e.g. `ﬁ` -> `fi`)
- Full-width characters -> standard (e.g. `Ａ` -> `A`)
- Superscript/subscript numbers -> regular numbers

### Empty Value Standardization

| Input                   | Markdown Output | JSON Output |
|:------------------------|:----------------|:------------|
| `""` (empty string)     | `N/A`           | `null`      |
| `"-"` or `"--"`         | `N/A`           | `null`      |
| `"N/A"`, `"n/a"`, `"NA"`| `N/A`           | `null`      |
| `"None"`, `"null"`      | `N/A`           | `null`      |
| `"TBD"`, `"TBA"`        | `TBD`           | `"TBD"`     |

---

## Price Normalization

Apply when extracting product, pricing, or financial data.

### Extraction Pattern

```python
import re

def normalize_price(raw):
    if not raw:
        return None
    # Remove currency words
    cleaned = re.sub(r'(?i)(USD|EUR|GBP|BRL|R\$|US\$)', '', raw)
    # Extract numeric value (handles 1,234.56 and 1.234,56 formats)
    match = re.search(r'[\d.,]+', cleaned)
    if not match:
        return None
    num_str = match.group()
    # Detect format: if last separator is comma with 2 digits after, it's decimal
    if re.search(r',\d{2}$', num_str):
        num_str = num_str.replace('.', '').replace(',', '.')
    else:
        num_str = num_str.replace(',', '')
    return float(num_str)
```

### Currency Detection

| Symbol/Code | Currency | Symbol/Code | Currency |
|:------------|:---------|:------------|:---------|
| `$`, `US$`, `USD` | US Dollar | `R$`, `BRL` | Brazilian Real |
| `€`, `EUR` | Euro     | `£`, `GBP`  | British Pound |
| `¥`, `JPY` | Yen      | `₹`, `INR`  | Indian Rupee  |
| `C$`, `CAD` | Canadian Dollar | `A$`, `AUD` | Australian Dollar |

### Output Format

```json
{
  "price": 29.99,
  "currency": "USD",
  "rawPrice": "$29.99"
}
```

For Markdown, show formatted: `$29.99` (right-aligned in table).

---

## Date Normalization

Normalize all dates to ISO-8601 format.

### Common Formats to Handle

| Input Format            | Example              | Normalized         |
|:------------------------|:---------------------|:-------------------|
| Full text               | February 25, 2026    | 2026-02-25         |
| Short text              | Feb 25, 2026         | 2026-02-25         |
| US numeric              | 02/25/2026           | 2026-02-25         |
| EU numeric              | 25/02/2026           | 2026-02-25         |
| ISO already             | 2026-02-25           | 2026-02-25         |
| Relative                | 3 days ago           | (compute from now) |
| Relative                | Yesterday            | (compute from now) |
| Timestamp               | 1740441600           | 2025-02-25         |
| With time               | 2026-02-25T14:30:00Z | 2026-02-25 14:30   |

### Ambiguous Dates

When format is ambiguous (e.g. `03/04/2026`):
- Default to US format (MM/DD/YYYY) unless site is clearly non-US
- Check page `lang` attribute or URL TLD for locale hints
- Note ambiguity in delivery notes

### Relative Date Resolution

```python
from datetime import datetime, timedelta
import re

def resolve_relative_date(text):
    text = text.lower().strip()
    today = datetime.now()

    if 'today' in text: return today.strftime('%Y-%m-%d')
    if 'yesterday' in text: return (today - timedelta(days=1)).strftime('%Y-%m-%d')

    match = re.search(r'(\d+)\s*(hour|day|week|month|year)s?\s*ago', text)
    if match:
        n, unit = int(match.group(1)), match.group(2)
        deltas = {'hour': 0, 'day': n, 'week': n*7, 'month': n*30, 'year': n*365}
        return (today - timedelta(days=deltas.get(unit, 0))).strftime('%Y-%m-%d')

    return text  # Return as-is if can't parse
```

---

## URL Resolution

Convert relative URLs to absolute.

### Patterns

| Input                    | Base URL                    | Resolved                              |
|:-------------------------|:----------------------------|:--------------------------------------|
| `/products/item-1`       | `https://example.com/shop`  | `https://example.com/products/item-1` |
| `item-1`                 | `https://example.com/shop/` | `https://example.com/shop/item-1`     |
| `//cdn.example.com/img`  | `https://example.com`       | `https://cdn.example.com/img`         |
| `https://other.com/page` | (any)                       | `https://other.com/page` (absolute)   |

### JavaScript Resolution

```javascript
function resolveUrl(relative, base) {
  try { return new URL(relative, base || window.location.href).href; }
  catch { return relative; }
}
```

---

## Phone Normalization

For contact mode extraction.

### Pattern

```python
import re

def normalize_phone(raw):
    if not raw:
        return None
    # Remove all non-digit chars except leading +
    digits = re.sub(r'[^\d+]', '', raw)
    if not digits or len(digits) < 7:
        return None
    # Add + prefix if looks international
    if len(digits) >= 11 and not digits.startswith('+'):
        digits = '+' + digits
    return digits
```

### Format by Context

| Context          | Format Example       |
|:-----------------|:---------------------|
| JSON output      | `"+5511999998888"`   |
| Markdown table   | `+55 11 99999-8888`  |
| CSV output       | `"+5511999998888"`   |

---

## Deduplication

### Exact Deduplication

```python
def deduplicate(records, key_fields=None):
    """Remove exact duplicate records.
    If key_fields provided, deduplicate by those fields only.
    """
    seen = set()
    unique = []
    for record in records:
        if key_fields:
            key = tuple(record.get(f) for f in key_fields)
        else:
            key = tuple(sorted(record.items()))
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique, len(records) - len(unique)  # returns (unique_list, removed_count)
```

### Near-Duplicate Detection

When records share key fields but differ in details:
1. Group by key fields (e.g. product name + source)
2. For each group, keep the record with fewest null values
3. If tie, keep the first occurrence
4. Report in notes: "Merged N near-duplicate records"

### Dedup Key Selection by Mode

| Mode     | Key Fields                        |
|:---------|:----------------------------------|
| product  | name + source (or name + brand)   |
| contact  | name + email (or name + org)      |
| jobs     | title + company + location        |
| events   | title + date + location           |
| table    | all fields (exact match)          |
| list     | first 2-3 identifying fields      |

---

## Text Cleaning

### Remove Noise

Common noise patterns to strip from extracted text:

| Pattern                            | Action                    |
|:-----------------------------------|:--------------------------|
| `\[edit\]`, `\[citation needed\]`  | Remove (Wikipedia)        |
| `Read more...`, `See more`         | Remove (truncation markers)|
| `Sponsored`, `Ad`, `Promoted`      | Remove or flag            |
| Cookie consent text                | Remove                    |
| Navigation breadcrumbs             | Remove                    |
| Footer boilerplate                 | Remove                    |

### Sentence Case Normalization

When extracting ALL-CAPS or inconsistent-case text:

```python
def normalize_case(text):
    if text.isupper() and len(text) > 3:
        return text.title()  # ALL CAPS -> Title Case
    return text
```

Only apply when: field is clearly ALL-CAPS input (common in older sites),
user requests it, or data looks better normalized.

---

## Data Type Coercion

### Automatic Type Detection

| Raw Value     | Detected Type | Coerced Value     |
|:--------------|:--------------|:------------------|
| `"123"`       | integer       | `123`             |
| `"12.99"`     | float         | `12.99`           |
| `"true"`      | boolean       | `true`            |
| `"false"`     | boolean       | `false`           |
| `"2026-02-25"`| date string   | `"2026-02-25"`    |
| `"$29.99"`    | price         | `29.99` + currency|
| `"4.5/5"`     | rating        | `4.5`             |
| `"1,234"`     | integer       | `1234`            |

### Rating Normalization

```python
import re

def normalize_rating(raw):
    if not raw:
        return None
    match = re.search(r'([\d.]+)\s*(?:/\s*([\d.]+))?', str(raw))
    if match:
        score = float(match.group(1))
        max_score = float(match.group(2)) if match.group(2) else 5.0
        return round(score / max_score * 5, 1)  # Normalize to /5 scale
    return None
```

---

## Enrichment Patterns

### Domain Extraction

Add domain from full URLs:
```python
from urllib.parse import urlparse

def extract_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        return domain
    except:
        return None
```

### Word Count

For article mode:
```python
def word_count(text):
    return len(text.split()) if text else 0
```

### Relative Time

Add human-readable time since date:
```python
def time_since(date_str):
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(date_str)
        delta = datetime.now() - dt
        if delta.days == 0: return "Today"
        if delta.days == 1: return "Yesterday"
        if delta.days < 7: return f"{delta.days} days ago"
        if delta.days < 30: return f"{delta.days // 7} weeks ago"
        if delta.days < 365: return f"{delta.days // 30} months ago"
        return f"{delta.days // 365} years ago"
    except:
        return None
```

---

## Transform Pipeline Order

Apply transforms in this sequence:

1. **HTML entity decode** - raw text cleanup
2. **Unicode normalization** - character standardization
3. **Whitespace cleanup** - spacing normalization
4. **Empty value standardization** - null/N/A handling
5. **URL resolution** - relative to absolute
6. **Data type coercion** - strings to numbers/dates
7. **Price normalization** - if applicable
8. **Date normalization** - if applicable
9. **Phone normalization** - if applicable
10. **Text cleaning** - noise removal
11. **Deduplication** - remove duplicates
12. **Sorting** - user-requested order
13. **Enrichment** - domain, word count, etc.

Not all steps apply to every extraction. Apply only what's relevant
to the data type and extraction mode.

---

## Reference: Extraction Patterns

# Extraction Patterns Reference

CSS selectors, JavaScript snippets, and domain-specific tips for
common web scraping scenarios.

---

## CSS Selector Patterns

### Tables

```css
/* Standard HTML tables */
table                               /* All tables */
table.data-table                    /* Class-based */
table[id*="result"]                 /* ID contains "result" */
table thead th                      /* Header cells */
table tbody tr                      /* Data rows */
table tbody tr td                   /* Data cells */
table tbody tr td:nth-child(2)      /* Specific column (2nd) */

/* Grid layouts acting as tables */
[role="table"]                      /* ARIA table role */
[role="row"]                        /* ARIA row */
[role="gridcell"]                   /* ARIA grid cell */
.table-responsive table             /* Bootstrap responsive wrapper */
```

### Product Listings

```css
/* E-commerce product grids */
.product-card, .product-item, .product-tile
[data-product-id]                   /* Data attribute markers */
.product-name, .product-title, h2.title
.price, .product-price, [data-price]
.price--sale, .price--original      /* Sale vs original price */
.rating, .stars, [data-rating]
.availability, .stock-status
.product-image img, .product-thumb img

/* Common e-commerce patterns */
.search-results .result-item
.catalog-grid .catalog-item
.listing .listing-item
```

### Search Results

```css
/* Generic search result patterns */
.search-result, .result-item, .search-entry
.result-title a, .result-link
.result-snippet, .result-description
.result-url, .result-source
.result-date, .result-timestamp
.pagination a, .page-numbers a, [aria-label="Next"]
```

### Contact / Directory

```css
/* People and contact cards */
.team-member, .staff-card, .person, .contact-card
.member-name, .person-name, h3.name
.member-title, .job-title, .role
.member-email a[href^="mailto:"]
.member-phone a[href^="tel:"]
.member-bio, .person-description
.vcard                              /* hCard microformat */
```

### FAQ / Accordion

```css
/* FAQ and accordion patterns */
.faq-item, .accordion-item, [itemtype*="FAQPage"] [itemprop="mainEntity"]
.faq-question, .accordion-header, [itemprop="name"], summary
.faq-answer, .accordion-body, .accordion-content, [itemprop="acceptedAnswer"]
details, details > summary          /* Native HTML accordion */
[role="tabpanel"]                   /* Tab-based FAQ */
```

### Pricing Tables

```css
/* SaaS pricing page patterns */
.pricing-table, .pricing-card, .plan-card, .pricing-tier
.plan-name, .tier-name, .pricing-title
.plan-price, .pricing-amount, .price-value
.plan-period, .billing-cycle        /* monthly/annually */
.plan-features li, .feature-list li
.plan-cta, .pricing-button
[class*="popular"], [class*="recommended"], [class*="featured"]  /* highlighted plan */
```

### Job Listings

```css
/* Job board patterns */
.job-listing, .job-card, .job-posting, [itemtype*="JobPosting"]
.job-title, [itemprop="title"]
.company-name, [itemprop="hiringOrganization"]
.job-location, [itemprop="jobLocation"]
.job-salary, [itemprop="baseSalary"]
.job-type, .employment-type
.job-date, [itemprop="datePosted"]
```

### Events

```css
/* Event listing patterns */
.event-card, .event-item, [itemtype*="Event"]
.event-title, [itemprop="name"]
.event-date, [itemprop="startDate"], time[datetime]
.event-location, [itemprop="location"]
.event-description, [itemprop="description"]
.event-speaker, .speaker-name
```

### Navigation / Pagination

```css
/* Pagination controls */
.pagination, .pager, nav[aria-label*="pagination"]
.pagination .next, a[rel="next"]
.pagination .prev, a[rel="prev"]
.page-numbers, .page-link
button[data-page], a[data-page]
.load-more, button.show-more
```

### Articles / Blog Posts

```css
/* Article content */
article, .post, .entry, .article-content
article h1, .post-title, .entry-title
.author, .byline, [rel="author"]
time, .date, .published, .post-date
.post-content, .entry-content, .article-body
.tags a, .categories a, .post-tags a
```

---

## JavaScript Extraction Snippets

### Generic Table Extractor

```javascript
function extractTable(selector) {
  const table = document.querySelector(selector || 'table');
  if (!table) return { error: 'No table found' };

  const headers = Array.from(
    table.querySelectorAll('thead th, tr:first-child th, tr:first-child td')
  ).map(el => el.textContent.trim());

  const rows = Array.from(table.querySelectorAll('tbody tr, tr:not(:first-child)'))
    .map(tr => {
      const cells = Array.from(tr.querySelectorAll('td'))
        .map(td => td.textContent.trim());
      return cells.length > 0 ? cells : null;
    })
    .filter(Boolean);

  return { headers, rows, rowCount: rows.length };
}
JSON.stringify(extractTable());
```

### Multi-Table Extractor

```javascript
function extractAllTables() {
  const tables = document.querySelectorAll('table');
  return Array.from(tables).map((table, idx) => {
    const caption = table.querySelector('caption')?.textContent?.trim()
      || table.getAttribute('aria-label') || `Table ${idx + 1}`;
    const headers = Array.from(
      table.querySelectorAll('thead th, tr:first-child th')
    ).map(el => el.textContent.trim());
    const rows = Array.from(table.querySelectorAll('tbody tr'))
      .map(tr => Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim()))
      .filter(r => r.length > 0);
    return { caption, headers, rows, rowCount: rows.length };
  });
}
JSON.stringify(extractAllTables());
```

### Generic List Extractor

```javascript
function extractList(containerSelector, itemSelector, fieldMap) {
  // fieldMap: { fieldName: { selector: 'CSS', attr: 'href'|'src'|null } }
  const container = document.querySelector(containerSelector);
  if (!container) return { error: 'Container not found' };

  const items = Array.from(container.querySelectorAll(itemSelector));
  const data = items.map(item => {
    const record = {};
    for (const [key, config] of Object.entries(fieldMap)) {
      const sel = typeof config === 'string' ? config : config.selector;
      const attr = typeof config === 'object' ? config.attr : null;
      const el = item.querySelector(sel);
      if (!el) { record[key] = null; continue; }
      record[key] = attr ? el.getAttribute(attr) : el.textContent.trim();
    }
    return record;
  });
  return { data, itemCount: data.length };
}

// Example usage:
JSON.stringify(extractList('.results', '.result-item', {
  title: '.result-title',
  description: '.result-snippet',
  url: { selector: '.result-title a', attr: 'href' },
  date: '.result-date'
}));
```

### JSON-LD Structured Data Extractor

Many pages embed structured data that's easier to parse than DOM:

```javascript
function extractJsonLd(targetType) {
  const scripts = document.querySelectorAll('script[type="application/ld+json"]');
  const allData = Array.from(scripts).map(s => {
    try { return JSON.parse(s.textContent); } catch { return null; }
  }).filter(Boolean);

  // Flatten @graph arrays
  const flat = allData.flatMap(d => d['@graph'] || [d]);

  if (targetType) {
    return flat.filter(d =>
      d['@type'] === targetType ||
      (Array.isArray(d['@type']) && d['@type'].includes(targetType))
    );
  }
  return flat;
}
// Extract products: extractJsonLd('Product')
// Extract articles: extractJsonLd('Article')
// Extract all: extractJsonLd()
JSON.stringify(extractJsonLd());
```

Common JSON-LD types and their useful fields:
- `Product`: name, offers.price, offers.priceCurrency, aggregateRating, brand.name
- `Article`: headline, author.name, datePublished, description, wordCount
- `Organization`: name, address, telephone, email, url
- `BreadcrumbList`: itemListElement[].name (navigation path)
- `FAQPage`: mainEntity[].name (question), mainEntity[].acceptedAnswer.text
- `JobPosting`: title, hiringOrganization.name, jobLocation, baseSalary
- `Event`: name, startDate, endDate, location, performer

### OpenGraph / Meta Tag Extractor

```javascript
function extractMeta() {
  const meta = {};
  document.querySelectorAll('meta[property^="og:"], meta[name^="twitter:"]')
    .forEach(el => {
      const key = el.getAttribute('property') || el.getAttribute('name');
      meta[key] = el.getAttribute('content');
    });
  meta.title = document.title;
  meta.description = document.querySelector('meta[name="description"]')
    ?.getAttribute('content');
  meta.canonical = document.querySelector('link[rel="canonical"]')
    ?.getAttribute('href');
  return meta;
}
JSON.stringify(extractMeta());
```

### Pricing Plan Extractor

```javascript
function extractPricingPlans() {
  const cards = document.querySelectorAll(
    '.pricing-card, .plan-card, .pricing-tier, [class*="pricing"] [class*="card"]'
  );
  return Array.from(cards).map(card => ({
    name: card.querySelector('[class*="name"], [class*="title"], h2, h3')
      ?.textContent?.trim() || null,
    price: card.querySelector('[class*="price"], [class*="amount"]')
      ?.textContent?.trim() || null,
    period: card.querySelector('[class*="period"], [class*="billing"]')
      ?.textContent?.trim() || null,
    features: Array.from(card.querySelectorAll('[class*="feature"] li, ul li'))
      .map(li => li.textContent.trim()),
    highlighted: card.matches('[class*="popular"], [class*="recommended"], [class*="featured"]'),
    ctaText: card.querySelector('a, button')?.textContent?.trim() || null,
    ctaUrl: card.querySelector('a')?.href || null,
  }));
}
JSON.stringify(extractPricingPlans());
```

### FAQ Extractor

```javascript
function extractFAQ() {
  // Try JSON-LD first
  const ldFaq = extractJsonLd('FAQPage');
  if (ldFaq.length > 0 && ldFaq[0].mainEntity) {
    return ldFaq[0].mainEntity.map(q => ({
      question: q.name,
      answer: q.acceptedAnswer?.text || null
    }));
  }

  // Try <details>/<summary> pattern
  const details = document.querySelectorAll('details');
  if (details.length > 0) {
    return Array.from(details).map(d => ({
      question: d.querySelector('summary')?.textContent?.trim() || null,
      answer: Array.from(d.children).filter(c => c.tagName !== 'SUMMARY')
        .map(c => c.textContent.trim()).join(' ')
    }));
  }

  // Try accordion pattern
  const items = document.querySelectorAll(
    '.faq-item, .accordion-item, [class*="faq"] [class*="item"]'
  );
  return Array.from(items).map(item => ({
    question: item.querySelector(
      '[class*="question"], [class*="header"], [class*="title"], h3, h4'
    )?.textContent?.trim() || null,
    answer: item.querySelector(
      '[class*="answer"], [class*="body"], [class*="content"], p'
    )?.textContent?.trim() || null
  }));
}
JSON.stringify(extractFAQ());
```

### Link Extractor

```javascript
function extractLinks(scope) {
  const container = scope ? document.querySelector(scope) : document;
  const links = Array.from(container.querySelectorAll('a[href]'))
    .map(a => ({
      text: a.textContent.trim(),
      href: a.href,
      title: a.title || null
    }))
    .filter(l => l.text && l.href && !l.href.startsWith('javascript:'));
  return { links, count: links.length };
}
JSON.stringify(extractLinks());
```

### Image Extractor

```javascript
function extractImages(scope) {
  const container = scope ? document.querySelector(scope) : document;
  const images = Array.from(container.querySelectorAll('img'))
    .map(img => ({
      src: img.src,
      alt: img.alt || null,
      width: img.naturalWidth,
      height: img.naturalHeight
    }))
    .filter(i => i.src && !i.src.includes('data:image/gif'));
  return { images, count: images.length };
}
JSON.stringify(extractImages());
```

### Scroll-and-Collect Pattern

For pages with lazy-loaded content, use this pattern with Browser automation:

```javascript
// Count items before scroll
function countItems(selector) {
  return document.querySelectorAll(selector).length;
}
```

Then in the workflow:
1. `javascript_tool`: `countItems('.item')` -> get initial count
2. `computer(action="scroll", scroll_direction="down")`
3. `computer(action="wait", duration=2)`
4. `javascript_tool`: `countItems('.item')` -> get new count
5. If new count > old count, repeat from step 2
6. If count unchanged after 2 scrolls, all items loaded
7. Extract all items at once

---

## Domain-Specific Tips

### E-Commerce Sites
- Check for JSON-LD `Product` schema first - often has cleaner data than DOM
- Prices may have hidden original/sale price elements
- Availability often encoded in data attributes (`data-available="true"`)
- Product variants (size, color) may require click interactions
- Review data often loaded lazily - scroll to reviews section first
- Many sites have internal APIs at `/api/products` - check Network tab

### Wikipedia
- Tables use class `.wikitable` - always prefer this selector
- Infoboxes use class `.infobox`
- References in `<sup class="reference">` - exclude from text extraction
- Table cells may contain complex nested HTML - use `.textContent.trim()`
- Sortable tables have class `.sortable` with sort buttons in headers

### News Sites
- Article body often in `<article>` or `[itemprop="articleBody"]`
- Paywall indicators: `.paywall`, `.subscribe-wall`, truncated with "Read more"
- Publication date in `<time>` element or `[itemprop="datePublished"]`
- Author in `[itemprop="author"]` or `.byline`
- JSON-LD `NewsArticle` often has complete metadata

### Government / Data Portals
- Often use HTML tables without JavaScript
- May have download links for CSV/Excel - check for `.csv`, `.xlsx` links
- Data dictionaries may be on separate pages
- Look for API endpoints in page source (`/api/`, `.json` links)
- CORS may block direct API access; use Bash curl instead

### Social Media (Public Profiles)
- Content is almost always JS-rendered - use Browser automation
- Rate limiting is aggressive - keep requests minimal
- Infinite scroll is the norm - set clear item limits
- Structure changes frequently - prefer text extraction over selectors

### SaaS Pricing Pages
- Pricing often changes dynamically (monthly vs annual toggle)
- May need to click "Annual" toggle to see annual prices
- Feature comparison tables often use checkmarks (Unicode or SVG)
- Check for hidden elements toggled by billing period selector

### Job Boards
- Most use JSON-LD `JobPosting` schema
- Salary ranges often hidden behind "View salary" buttons
- Location may include remote/hybrid indicators
- Filters are URL-parameter based - useful for pagination

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Better Approach |
|:-------------|:-------------|:----------------|
| Selectors with generated hashes (`.css-1a2b3c`) | Change on every deploy | Use semantic selectors, ARIA roles, data attributes |
| Deeply nested paths (`div > div > div > span`) | Fragile on layout changes | Use closest meaningful class or attribute |
| Index-based (`:nth-child(3)`) for dynamic lists | Order may change | Use content-based identification |
| Selecting by inline styles | Presentation, not semantics | Use classes, IDs, or data attributes |
| Hardcoded wait times for JS content | Too short or too long | Check for content presence in a loop |
| Single selector for variant pages | Different pages differ | Test selector on multiple pages first |

## Robust Selector Priority

Prefer selectors in this order (most stable to least):

1. `[data-testid="..."]`, `[data-id="..."]` - test/data attributes
2. `#unique-id` - unique IDs
3. `[role="..."]`, `[aria-label="..."]` - ARIA attributes
4. `[itemprop="..."]`, `[itemtype="..."]` - microdata / schema.org
5. `.semantic-class` - meaningful class names
6. `tag.class` - element type + class
7. Structural selectors - last resort

---

## Reference: Output Templates

# Output Templates Reference

Complete formatting templates for all supported output formats.
Every output must be wrapped in a delivery envelope with metadata.

---

## Delivery Envelope (Required)

Every extraction result MUST include this metadata wrapper,
regardless of output format:

```markdown
## Extraction Results

**Source:** [Page Title](https://example.com/page)
**Date:** 2026-02-25 14:30 UTC
**Items:** 47 records
**Confidence:** HIGH
**Format:** Markdown Table

---

[DATA GOES HERE]

---

**Notes:**
- Any gaps, anomalies, or observations
- Filters or sorts applied
- Pages scraped (if paginated)
```

---

## Markdown Table Format

### Standard Table

```markdown
| Name           | Price    | Rating | Availability |
|:---------------|---------:|:------:|:-------------|
| Product Alpha  |   $29.99 |  4.5   | In Stock     |
| Product Beta   |   $49.99 |  4.2   | In Stock     |
| Product Gamma  |  $119.00 |  4.8   | Pre-order    |
| Product Delta  |   $15.50 |  3.9   | Out of Stock |
```

### Alignment Rules

| Data Type    | Alignment | Markdown Syntax |
|:-------------|:----------|:----------------|
| Text         | Left      | `:---`          |
| Numbers      | Right     | `---:`          |
| Centered     | Center    | `:---:`         |
| Mixed/Status | Left      | `:---`          |

### Table with Summary Row

```markdown
| Product        | Units Sold | Revenue    |
|:---------------|----------:|-----------:|
| Widget A       |     1,234 |  $12,340   |
| Widget B       |       567 |   $8,505   |
| Widget C       |     2,890 |  $57,800   |
| **Total**      | **4,691** | **$78,645**|
```

### Wide Data (Split Tables)

When data has more than 10 columns, split into logical groups:

```markdown
### Basic Information

| Name    | Category | Brand   | SKU      |
|:--------|:---------|:--------|:---------|
| Item A  | Tools    | Acme    | ACM-001  |

### Pricing and Availability

| Name    | Price   | Sale Price | Stock | Ships In |
|:--------|--------:|-----------:|:------|:---------|
| Item A  | $49.99  |    $39.99  | 142   | 2 days   |
```

### Multi-URL Comparison Table

```markdown
| Source       | Product    | Price   | Rating |
|:-------------|:-----------|--------:|:------:|
| store-a.com  | Laptop X   | $999    |  4.3   |
| store-b.com  | Laptop X   | $949    |  4.5   |
| store-c.com  | Laptop X   | $1,029  |  4.1   |
```

### Truncation Rules

For values exceeding 60 characters:
```markdown
| Title                                                       | Author  |
|:------------------------------------------------------------|:--------|
| Introduction to Advanced Machine Learning Techni...         | J. Smith|
```

---

## JSON Format

### Standard JSON Output

```json
{
  "metadata": {
    "source": "https://example.com/products",
    "title": "Product Catalog - Example Store",
    "extractedAt": "2026-02-25T14:30:00Z",
    "itemCount": 3,
    "confidence": "HIGH",
    "fields": ["name", "price", "rating", "availability"],
    "notes": []
  },
  "data": [
    {
      "name": "Product Alpha",
      "price": 29.99,
      "currency": "USD",
      "rating": 4.5,
      "availability": "In Stock"
    },
    {
      "name": "Product Beta",
      "price": 49.99,
      "currency": "USD",
      "rating": 4.2,
      "availability": "In Stock"
    },
    {
      "name": "Product Gamma",
      "price": 119.00,
      "currency": "USD",
      "rating": 4.8,
      "availability": "Pre-order"
    }
  ]
}
```

### JSON Key Naming

| Rule                   | Example                           |
|:-----------------------|:----------------------------------|
| camelCase              | `productName`, `unitPrice`        |
| Numbers stay numeric   | `29.99` not `"29.99"`             |
| Booleans stay boolean  | `true` not `"true"`               |
| Missing = null         | `null` not `""` or `"N/A"`        |
| Arrays for multiples   | `"tags": ["sale", "new"]`         |
| ISO-8601 for dates     | `"2026-02-25T14:30:00Z"`         |

### Nested JSON (Product with Details)

```json
{
  "metadata": { "..." : "..." },
  "data": [
    {
      "name": "Laptop Pro X",
      "brand": "TechCo",
      "pricing": {
        "current": 999.99,
        "original": 1299.99,
        "currency": "USD",
        "discount": "23%"
      },
      "rating": {
        "score": 4.5,
        "count": 1234
      },
      "specifications": {
        "processor": "M3 Pro",
        "ram": "16 GB",
        "storage": "512 GB SSD",
        "display": "14.2 inch Retina"
      },
      "availability": {
        "inStock": true,
        "shipsIn": "2-3 business days"
      }
    }
  ]
}
```

### Multi-URL JSON

```json
{
  "metadata": {
    "sources": [
      "https://store-a.com/laptop-x",
      "https://store-b.com/laptop-x"
    ],
    "extractedAt": "2026-02-25T14:30:00Z",
    "itemCount": 2,
    "confidence": "HIGH"
  },
  "data": [
    {
      "source": "store-a.com",
      "name": "Laptop X",
      "price": 999,
      "currency": "USD",
      "rating": 4.3
    },
    {
      "source": "store-b.com",
      "name": "Laptop X",
      "price": 949,
      "currency": "USD",
      "rating": 4.5
    }
  ]
}
```

---

## CSV Format

### Standard CSV

```csv
# Source: https://example.com/products
# Extracted: 2026-02-25 14:30 UTC
# Items: 3 | Confidence: HIGH
name,price,currency,rating,availability
"Product Alpha",29.99,USD,4.5,"In Stock"
"Product Beta",49.99,USD,4.2,"In Stock"
"Product Gamma",119.00,USD,4.8,"Pre-order"
```

### CSV Rules

| Rule                                 | Example                        |
|:-------------------------------------|:-------------------------------|
| Always include header row            | `name,price,rating`            |
| Quote fields with commas             | `"Smith, John"`                |
| Quote fields with quotes (escape)    | `"He said ""hello"""`          |
| Quote fields with newlines           | `"Line 1\nLine 2"`            |
| UTF-8 encoding with BOM             | `\xEF\xBB\xBF` prefix         |
| Comma delimiter (standard)           | `,`                            |
| Metadata as comments (# prefix)      | `# Source: URL`                |
| null/missing as empty field          | `field1,,field3`               |

### Multi-URL CSV

```csv
# Sources: store-a.com, store-b.com
# Extracted: 2026-02-25 14:30 UTC
source,name,price,currency,rating
"store-a.com","Laptop X",999,USD,4.3
"store-b.com","Laptop X",949,USD,4.5
```

---

## Summary Statistics Template

When extracted data contains numeric fields, include a summary block:

```markdown
### Summary Statistics

| Metric    | Price     | Rating |
|:----------|----------:|-------:|
| Count     |        47 |     47 |
| Min       |    $12.99 |    2.1 |
| Max       |   $299.99 |    5.0 |
| Average   |    $67.42 |    4.1 |
| Median    |    $54.99 |    4.3 |
```

Include only when:
- Data has numeric columns
- More than 5 items extracted
- User would likely benefit from aggregate view (prices, ratings, quantities)

---

## Contact Data Template

```markdown
| Name           | Title              | Email                | Phone          |
|:---------------|:-------------------|:---------------------|:---------------|
| Jane Smith     | CEO                | jane@example.com     | +1-555-0101    |
| John Doe       | CTO                | john@example.com     | +1-555-0102    |
| Alice Johnson  | VP Engineering     | alice@example.com    | N/A            |
```

---

## Article Extraction Template

```markdown
## Article: [Title]

**Author:** Author Name
**Published:** YYYY-MM-DD
**Source:** [Site Name](URL)

### Summary
[2-3 sentence summary of the article content]

### Key Data Points
- [Factual data point 1]
- [Factual data point 2]
- [Statistical finding]

### Tags
`tag1` `tag2` `tag3`
```

Note: Summarize article content. Do not reproduce full article text
due to copyright.

---

## FAQ Extraction Template

```markdown
### FAQ: [Page Title]

**Source:** [Site Name](URL)
**Items:** 12 questions

| # | Question | Answer (excerpt) |
|--:|:---------|:-----------------|
| 1 | How do I reset my password? | Navigate to Settings > Security and click "Reset..." |
| 2 | What payment methods do you accept? | We accept Visa, Mastercard, PayPal, and bank transfer... |
```

Or as JSON (default for FAQ mode):
```json
{
  "metadata": { "source": "URL", "itemCount": 12, "confidence": "HIGH" },
  "data": [
    { "question": "How do I reset my password?", "answer": "Navigate to...", "category": "Account" },
    { "question": "What payment methods?", "answer": "We accept...", "category": "Billing" }
  ]
}
```

---

## Pricing Plans Template

```markdown
### Pricing: [Product Name]

**Source:** [Site Name](URL)
**Plans:** 3 tiers

| Plan        | Monthly   | Annual    | Highlighted |
|:------------|----------:|----------:|:-----------:|
| Starter     |    $9/mo  |   $7/mo   |             |
| Pro         |   $29/mo  |  $24/mo   |     *       |
| Enterprise  |  Custom   |  Custom   |             |

#### Feature Comparison

| Feature               | Starter | Pro | Enterprise |
|:----------------------|:-------:|:---:|:----------:|
| Users                 | 1       | 10  | Unlimited  |
| Storage               | 5 GB    | 50 GB | Unlimited |
| API Access            | N/A     | Yes | Yes        |
| Priority Support      | N/A     | N/A | Yes        |
```

---

## Job Listings Template

```markdown
| Title              | Company     | Location       | Salary          | Type      | Posted     |
|:-------------------|:------------|:---------------|:----------------|:----------|:-----------|
| Senior Engineer    | TechCo      | Remote, US     | $150k - $200k   | Full-time | 2026-02-20 |
| Product Manager    | StartupXYZ  | San Francisco  | $130k - $160k   | Full-time | 2026-02-18 |
| Data Analyst       | DataCorp    | London, UK     | GBP 55k - 70k   | Contract  | 2026-02-22 |
```

---

## Events Template

```markdown
| Event                  | Date       | Time    | Location          | Speakers       |
|:-----------------------|:-----------|:--------|:------------------|:---------------|
| Opening Keynote        | 2026-03-15 | 09:00   | Main Hall         | J. Smith       |
| Workshop: AI Basics    | 2026-03-15 | 14:00   | Room 201          | A. Johnson     |
| Networking Reception   | 2026-03-15 | 18:00   | Rooftop Lounge    | N/A            |
```

---

## Differential (Diff) Output Template

When comparing current extraction with a previous run:

```markdown
## Extraction Results (Diff)

**Source:** [Page Title](URL)
**Date:** 2026-02-25 14:30 UTC
**Compared to:** 2026-02-20 10:00 UTC
**Changes:** +5 new, -2 removed, 3 modified

---

### New Items (+5)

| Name           | Price    | Rating |
|:---------------|--------:|:------:|
| Product Eta    |  $39.99 |  4.6   |
| Product Theta  |  $24.99 |  4.1   |
| ...            |         |        |

### Removed Items (-2)

| Name           | Price    | Rating |
|:---------------|--------:|:------:|
| ~~Product Alpha~~ | ~~$29.99~~ | ~~4.5~~ |
| ~~Product Beta~~  | ~~$49.99~~ | ~~4.2~~ |

### Modified Items (3)

| Name           | Field   | Was        | Now        |
|:---------------|:--------|:-----------|:-----------|
| Product Gamma  | Price   | $119.00    | $109.00    |
| Product Gamma  | Rating  | 4.8        | 4.9        |
| Product Delta  | Stock   | Out of Stock | In Stock |

---

**Summary:**
- 5 new products added since last extraction
- 2 products removed (possibly discontinued)
- Product Gamma had a price drop of $10 and rating increase
- Product Delta is back in stock
```

---

## Error / Partial Result Template

When extraction partially fails:

```markdown
## Extraction Results (Partial)

**Source:** [Page Title](URL)
**Date:** 2026-02-25 14:30 UTC
**Items:** 23 of ~50 expected records
**Confidence:** LOW
**Strategy:** A (WebFetch) -> escalated to B (Browser)

---

[PARTIAL DATA]

---

**Issues:**
- 27 items could not be extracted (content behind JS rendering)
- Price field missing for 5 items (marked N/A)
- Auto-escalation from WebFetch to Browser recovered 15 additional items

**Suggestions:**
- Re-run with explicit Browser automation for complete results
- Check if site has an API endpoint for direct data access
- Try at a different time if rate-limited
```
