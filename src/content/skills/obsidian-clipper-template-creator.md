---
title: "Obsidian Clipper Template Creator"
description: "Guide for creating templates for the Obsidian Web Clipper. Use when you want to create a new clipping template, understand available variables, or format clipped content."
category: "other"
source: "community"
author: "Community"
tags: ["obsidian", "clipper", "template", "creator"]
date: 2026-03-20
---

# Obsidian Web Clipper Template Creator

This skill helps you create importable JSON templates for the Obsidian Web Clipper.

## Workflow

1. **Identify User Intent:** specific site (YouTube), specific type (Recipe), or general clipping?
2. **Check Existing Bases:** The user likely has a "Base" schema defined in `Bases/`.
    - **Action:** Read `Bases/*.base` to find a matching category (e.g., `Recipes.base`).
    - **Action:** Use the properties defined in the Base to structure the Clipper template properties.
    - See [references/bases-workflow.md](references/bases-workflow.md) for details.
3. **Fetch & Analyze Reference URL:** Validate variables against a real page.
    - **Action:** Ask the user for a sample URL of the content they want to clip (if not provided).
    - **Action (REQUIRED):** Use **WebFetch** to retrieve page content; if WebFetch is not available, use a browser DOM snapshot. See [references/analysis-workflow.md](references/analysis-workflow.md).
    - **Action:** Analyze the HTML for Schema.org JSON, Meta tags, and CSS selectors.
    - **Action (REQUIRED):** Verify each selector against the fetched content. Do not guess selectors.
    - See [references/analysis-workflow.md](references/analysis-workflow.md) for analysis techniques.
4. **Draft the JSON:** Create a valid JSON object following the schema.
    - See [references/json-schema.md](references/json-schema.md).
5. **Consider template logic:** Use conditionals for optional blocks (e.g. show nutrition only if present), loops for list data, variable assignment to avoid repeating expressions, and fallbacks for missing variables. Use logic only when it improves the template; keep simple templates simple. See [references/logic.md](references/logic.md).
6. **Verify Variables:** Ensure the chosen variables (Preset, Schema, Selector) exist in your analysis.
    - **Action (REQUIRED):** If a selector cannot be verified from the fetched content, state that explicitly and ask for another URL.
    - See [references/variables.md](references/variables.md).

## Selector Verification Rules

- **Always verify selectors** against live page content before responding.
- **Never guess selectors.** If the DOM cannot be accessed or the element is missing, ask for another URL or a screenshot.
- **Prefer stable selectors** (data attributes, semantic roles, unique IDs) over fragile class chains.
- **Document the target element** in your reasoning (e.g., "About sidebar paragraph") to reduce mismatch.

## Output Format

**ALWAYS** output the final result as a JSON code block that the user can copy and import.

The Clipper template editor validates template syntax.
If you use template logic (conditionals, loops, variable assignment), ensure it follows the syntax in [references/logic.md](references/logic.md) and the official [Logic](https://help.obsidian.md/web-clipper/logic) docs so the template passes validation.

```json
{
  "schemaVersion": "0.1.0",
  "name": "My Template",
  ...
}
```

## Resources

- [references/variables.md](references/variables.md) - Available data variables.
- [references/filters.md](references/filters.md) - Formatting filters.
- [references/json-schema.md](references/json-schema.md) - JSON structure documentation.
- [references/logic.md](references/logic.md) - Template logic.
- [references/bases-workflow.md](references/bases-workflow.md) - How to map Bases to Templates.
- [references/analysis-workflow.md](references/analysis-workflow.md) - How to validate page data.

### Official Documentation

- [Variables](https://help.obsidian.md/web-clipper/variables)
- [Filters](https://help.obsidian.md/web-clipper/filters)
- [Logic](https://help.obsidian.md/web-clipper/logic)
- [Templates](https://help.obsidian.md/web-clipper/templates)

## Examples

See [assets/](assets/) for JSON examples.

---

## Reference: Analysis Workflow

# Analysis Workflow: Validating Variables

To ensure your template works correctly, you must validate that the target page actually contains the data you want to extract.

## 1. Fetch the Page

Use the `WebFetch` tool or a browser DOM snapshot to retrieve the content of a representative URL provided by the user.

```text
WebFetch(url="https://example.com/recipe/chocolate-cake")
```

## 2. Analyze the Output

### Check for Schema.org (Recommended)

Look for `<script type="application/ld+json">`. This contains structured data which is the most reliable way to extract info.

**Example Found in HTML:**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Chocolate Cake",
  "author": {
    "@type": "Person",
    "name": "John Doe"
  }
}
```

**Conclusion:**

- `{{schema:Recipe:name}}` is valid.
- `{{schema:Recipe:author.name}}` is valid.
- **Tip:** You can use `schema:Recipe` in the `triggers` array to automatically select this template for any page with this schema.

### Check for Meta Tags

Look for `<meta>` tags in the `<head>` section.

**Example Found in HTML:**

```html
<meta property="og:title" content="The Best Chocolate Cake" />
<meta name="description" content="A rich, moist chocolate cake recipe." />
```

**Conclusion:**

- `{{meta:og:title}}` is valid.
- `{{meta:description}}` is valid.

### Check for CSS Selectors (Verified)

If Schema and Meta tags are missing, look for HTML structure (classes and IDs) to use with `{{selector:...}}`.
Selectors must be verified against the fetched HTML or DOM snapshot. Do not guess selectors.

**Example Found in HTML:**

```html
<div class="article-body">
  <h1 id="main-title">Chocolate Cake</h1>
  <span class="author-name">By John Doe</span>
</div>
```

**Conclusion:**

- `{{selector:h1#main-title}}` or `{{selector:h1}}` can extract the title.
- `{{selector:.author-name}}` can extract the author.

## 3. Verify Against Base

Compare the available data from your analysis with the properties required by the user's Base (see [bases-workflow.md](bases-workflow.md)).

- If the Base requires `ingredients` but the page has no Schema or clear list structure, warn the user that this field might need manual entry or a prompt variable.

---

## Reference: Bases Workflow

# Working with Obsidian Bases

The user maintains "Bases" in `Bases/*.base` which define the schema and properties for different types of notes (e.g., Recipes, Clippings, People).

## Workflow

1.  **Identify the Category:** Determine the type of content the user wants to clip (e.g., a Recipe, a News Article, a YouTube video).
2.  **Find the Base:** Search `Bases/` for a matching `.base` file.
    *   Example: For a recipe, look for `Bases/Recipes.base`.
    *   Example: For a generic article, look for `Bases/Clippings.base`.
3.  **Read the Base:** Read the content of the `.base` file to understand the required properties.

## Interpreting .base Files

Base files use a YAML-like structure. Look for the `properties` section.

```yaml
properties:
  file.name:
    displayName: name
  note.author:
    displayName: author
  note.type:
    displayName: type
  note.ingredients:
    displayName: ingredients
```

*   `note.X` corresponds to a property name `X` in the frontmatter.
*   `displayName` helps understand the intent, but the property key (e.g., `author`, `type`, `ingredients`) is what matters for the template.

## Mapping to Clipper Properties

When creating the JSON for the Web Clipper, map the Base properties to the `properties` array in the JSON.

| Base Property | Clipper JSON Property Name | Value Strategy |
| :--- | :--- | :--- |
| `note.author` | `author` | `{{author}}` or `{{schema:author.name}}` |
| `note.source` | `source` | `{{url}}` |
| `note.published` | `published` | `{{published}}` |
| `note.ingredients` | `ingredients` | `{{schema:Recipe:recipeIngredient}}` |
| `note.type` | `type` | Constant (e.g., `Recipe`) or empty |

**Crucial Step:** Ask the user which properties should be automatically filled, which should be hardcoded (e.g., `type: Recipe`), and which should be left empty for manual entry.

---

## Reference: Filters

# Obsidian Web Clipper Filters

**Official Docs:** [help.obsidian.md/web-clipper/filters](https://help.obsidian.md/web-clipper/filters)

Use filters to format variables: `{{variable|filter}}`.

## Text Formatting
- `markdown`: Convert HTML to Markdown.
- `strip_tags`: Remove HTML tags.
- `trim`: Remove whitespace.
- `upper`: Convert to uppercase.
- `lower`: Convert to lowercase.
- `title`: Title Case.
- `capitalize`: Capitalize first letter.
- `camel`: CamelCase.
- `kebab`: kebab-case.
- `snake`: snake_case.
- `pascal`: PascalCase.
- `replace:"old","new"`: Replace text.
- `safe_name`: Make safe for filenames.
- `blockquote`: Format as blockquote.
- `link`: Create markdown link.
- `wikilink`: Create [[wikilink]].
- `list`: Format array as list.
- `table`: Format array as table.
- `callout`: Format as callout block.

## Dates
- `date:"format"`: Format date (e.g., `YYYY-MM-DD`).
- `date_modify:"+1 day"`: Modify date.
- `duration`: Format duration.

## Numbers
- `calc`: Perform calculations.
- `length`: Get length of string/array.
- `round`: Round numbers.

## HTML Processing
- `remove_html`: Remove HTML tags.
- `remove_attr`: Remove attributes.
- `strip_attr`: Strip specific attributes.

## Arrays and Objects
- `map`: Transform array items (e.g., `map:item =>> item.text`).
- `join:"separator"`: Join array items.
- `split:"separator"`: Split string into array.
- `first`: First item.
- `last`: Last item.
- `slice:start,end`: Slice array.
- `unique`: Unique items.
- `template:"format"`: Format items using a template string.

---

## Reference: Json Schema

# Obsidian Web Clipper JSON Schema

The Obsidian Web Clipper imports templates via JSON files.

## Root Structure

```json
{
	"schemaVersion": "0.1.0",
	"name": "Template Name",
	"behavior": "create",
	"noteContentFormat": "Markdown content here...",
	"properties": [],
	"triggers": [],
	"noteNameFormat": "{{title}}",
	"path": "Inbox/"
}
```

### Fields

*   **`schemaVersion`**: Always "0.1.0".
*   **`name`**: The display name of the template in the Clipper.
*   **`behavior`**: How the note is created.
    *   `create`: Create a new note.
    *   `append-specific`: Append to a specific note (requires `path` to be a full file path).
    *   `append-daily`: Append to the daily note.
*   **`noteContentFormat`**: The body of the note.
    *   Use `\n` for newlines.
    *   Can use all variables (e.g., `{{content}}`, `{{selection}}`).
    *   Supports **template logic** (conditionals, loops, variable assignment) as documented in [logic.md](logic.md).
*   **`noteNameFormat`**: The filename pattern (e.g., `{{date}} - {{title}}`).
*   **`path`**: The location to save the note.
    *   For `create` behavior: The *folder* to save the note in (e.g., `Clippings/` or `Recipes/`).
    *   For `append-specific` behavior: The *full file path* of the note to append to (e.g., `Databases/Recipes.md`).
*   **`triggers`**: Array of strings to automatically select this template.
    *   **URL Patterns**: `["https://www.youtube.com/watch"]` (Simple string or Regex).
    *   **Schema Types**: `["schema:Recipe"]` (Triggers if the page contains this Schema.org type).

## Properties

The `properties` array defines the YAML frontmatter of the note.

```json
"properties": [
    {
        "name": "category",
        "value": "Recipes",
        "type": "text"
    },
    {
        "name": "published",
        "value": "{{published}}",
        "type": "datetime"
    }
]
```

### Property Types

*   **`text`**: Simple text string.
*   **`multitext`**: List of text strings (for tags/aliases).
*   **`number`**: Numeric value.
*   **`checkbox`**: Boolean true/false.
*   **`date`**: Date string (YYYY-MM-DD).
*   **`datetime`**: Date and time string.

### Property Object Structure

*   **`name`**: The key in the YAML frontmatter.
*   **`value`**: The value to populate. Can contain variables and the same **template logic** (conditionals, loops, variable assignment) as `noteContentFormat`; see [logic.md](logic.md).
*   **`type`**: One of the types listed above.

## Template validation

The Clipper template editor checks template syntax. 
Invalid logic in `noteContentFormat` or property `value` fields will be reported in the editor; use valid syntax as described in the [Logic](https://help.obsidian.md/web-clipper/logic) documentation.

---

## Reference: Logic

# Obsidian Web Clipper Template Logic

**Official docs:** [Logic - Obsidian Help](https://help.obsidian.md/web-clipper/logic)

As of **Obsidian Web Clipper 1.0.0**, templates support logic in `noteContentFormat` and in property `value` fields: conditionals, loops, variable assignment, and fallbacks. This page describes how each works. For authoritative syntax and delimiters, use the official documentation link above.

---

## When to use logic

- **Conditionals:** Show optional sections only when data exists (e.g. nutrition block only if `{{schema:Recipe:nutrition}}` is present).
- **Variable assignment:** Assign a value once and reuse it in the template to avoid repeating long expressions.
- **Fallbacks:** Provide a default when a variable is empty so the note still looks correct.
- **Loops:** Iterate over arrays (ingredients, steps, tags) to format each item; combine with filters for list/table output.

Keep simple templates simple; add logic only when it improves the result or avoids broken output for missing data.

---

## Conditionals

Conditionals include or exclude blocks based on whether a value exists or meets a condition.

- **Comparison operators:** Compare two values (e.g. equals, not equals, greater than, less than). Exact operators are defined in the official Logic page.
- **Logical operators:** Combine or negate conditions (e.g. and, or, not; or symbol forms like `&&`, `||`, `!`). Use these to build compound conditions.
- **Truthiness:** Values are evaluated in a JavaScript-like way for conditions. Empty strings, empty arrays, and missing variables are typically falsy; non-empty values are truthy. See the official docs for the full rules.
- **Typical use:** Wrap optional sections (e.g. author, nutrition, image) in a conditional so they only render when the variable has a value.

---

## Assign a variable

You can assign a variable once and reuse it in the same template. Use this to avoid repeating long variable or filter chains (e.g. the same schema path or selector used in multiple places). The assigned variable is available for the rest of the template in that scope. Exact syntax (e.g. assignment block format and scope) is in the official Logic documentation.

---

## Fallbacks

Fallbacks supply a default when a variable is empty.

- **Default when missing:** Provide a fallback value so the template still produces readable output when the primary variable is empty.
- **Chaining fallbacks:** You can chain multiple fallbacks (e.g. try variable A, then B, then a literal default). The first non-empty value is used.
- **With filters:** Fallbacks can be used together with filters. The evaluation order (variable → fallback → filter, or other) is defined in the official docs under "With filters" and "Evaluation order."

---

## Loops

Loops iterate over array values (e.g. ingredients, instructions, tags).

- **Loop sources:** The array to iterate over—typically a variable that returns a list (e.g. `{{schema:Recipe:recipeIngredient}}`, `{{schema:Recipe:recipeInstructions}}`).
- **Loop variables:** Inside the loop you get a variable for the current item; you may also get an index or other loop metadata. Names and behavior are described in the official "Loop variables" and "Accessing array items by index" sections.
- **Accessing array items by index:** When you need the nth item of an array outside a loop, or need the current index inside a loop, the syntax is defined in the official documentation.
- **Nested loops:** Loops can be nested when you have arrays of structured data (e.g. steps each with sub-steps).
- **Combine logic:** Loops and conditionals can be combined (e.g. loop over items and show a subsection only when a field exists, or conditionally include a loop).

---

## Evaluation order and combining logic

The order in which variables, filters, fallbacks, conditionals, and loops are evaluated is defined in the official documentation. When you combine logic (e.g. conditionals inside loops, or variables used in both conditionals and output), follow the official "Evaluation order" and "Combine logic" sections so behavior matches expectations.

---

## Template validation

The Obsidian Web Clipper template editor **validates template syntax**. Invalid logic (e.g. malformed conditionals or loops) will be reported in the editor. When generating templates, use only logic constructs and syntax described on the official Logic page so that the template passes validation.

---

## Reference: Variables

# Obsidian Web Clipper Variables

**Official Docs:** [help.obsidian.md/web-clipper/variables](https://help.obsidian.md/web-clipper/variables)

## Preset Variables
Automatically extracted from the page.

- `{{content}}`: Main article content (markdown).
- `{{contentHtml}}`: Main article content (HTML).
- `{{title}}`: Page title.
- `{{url}}`: Page URL.
- `{{author}}`: Author name.
- `{{date}}`: Current date.
- `{{published}}`: Publication date (if detected).
- `{{site}}`: Site name.
- `{{description}}`: Meta description.
- `{{highlights}}`: Highlighted text (if any).
- `{{selection}}`: Selected text.
- `{{fullHtml}}`: Full page HTML.
- `{{favicon}}`: Favicon URL.
- `{{image}}`: Social share image URL.
- `{{words}}`: Word count.
- `{{domain}}`: Domain name.

## Prompt Variables (AI)
Use `{{"Your prompt here"}}` to ask the AI Interpreter to extract or summarize info.
*Requires Interpreter to be enabled.*

Examples:
- `{{"Summarize in 3 bullet points"}}`
- `{{"Extract the ingredients list"}}`
- `{{"Translate to English"}}`

## Selector Variables
Extract content using CSS selectors.
Syntax: `{{selector:css-selector}}` or `{{selector:css-selector?attribute}}`

Examples:
- `{{selector:h1}}`: Text of H1 tag.
- `{{selector:img.hero?src}}`: Source of image with class 'hero'.
- `{{selector:.author}}`: Text of element with class 'author'.
- `{{selectorHtml:body|markdown}}`: Full HTML converted to markdown.

## Meta Variables
Extract data from meta tags.
Syntax: `{{meta:name}}` or `{{meta:property}}`

Examples:
- `{{meta:description}}`
- `{{meta:og:title}}`

## Schema.org Variables
Extract structured data.
Syntax: `{{schema:Property}}` or `{{schema:@Type:Property}}`

Examples:
- `{{schema:Recipe:recipeIngredient}}`
- `{{schema:author.name}}`
- `{{schema:Article:headline}}`

## Fallbacks
When a variable is empty, you can supply a default value (fallback). 
Fallbacks can be chained (try variable A, then B, then a literal default) and used with filters. 
For syntax and evaluation order, see [logic.md](logic.md).
