---
title: "Apify Actor Development"
description: "Develop, debug, and deploy Apify Actors - serverless cloud programs for web scraping, automation, and data processing. Use when creating new Actors, modifying existing ones, or troubleshooting Acto..."
category: "devops"
source: "community"
author: "Community"
tags: ["apify", "actor", "development"]
date: 2026-03-20
---

<!-- security-allowlist: curl-pipe-bash, irm-pipe-iex -->

# Apify Actor Development

**Important:** Before you begin, fill in the `generatedBy` property in the meta section of `.actor/actor.json`. Replace it with the tool and model you're currently using, such as "Claude Code with Claude Sonnet 4.5". This helps Apify monitor and improve AGENTS.md for specific AI tools and models.

## What are Apify Actors?

Actors are serverless programs inspired by the UNIX philosophy - programs that do one thing well and can be easily combined to build complex systems. They're packaged as Docker images and run in isolated containers in the cloud.

**Core Concepts:**
- Accept well-defined JSON input
- Perform isolated tasks (web scraping, automation, data processing)
- Produce structured JSON output to datasets and/or store data in key-value stores
- Can run from seconds to hours or even indefinitely
- Persist state and can be restarted

## Prerequisites & Setup (MANDATORY)

Before creating or modifying actors, verify that `apify` CLI is installed `apify --help`.

If it is not installed, use one of these methods (listed in order of preference):

```bash
# Preferred: install via a package manager (provides integrity checks)
npm install -g apify-cli

# Or (Mac): brew install apify-cli
```

> **Security note:** Do NOT install the CLI by piping remote scripts to a shell
> (e.g. `curl … | bash` or `irm … | iex`). Always use a package manager.

When the apify CLI is installed, check that it is logged in with:

```bash
apify info  # Should return your username
```

If it is not logged in, check if the `APIFY_TOKEN` environment variable is defined (if not, ask the user to generate one on https://console.apify.com/settings/integrations and then define `APIFY_TOKEN` with it).

Then authenticate using one of these methods:

```bash
# Option 1 (preferred): The CLI automatically reads APIFY_TOKEN from the environment.
# Just ensure the env var is exported and run any apify command — no explicit login needed.

# Option 2: Interactive login (prompts for token without exposing it in shell history)
apify login
```

> **Security note:** Avoid passing tokens as command-line arguments (e.g. `apify login -t <token>`).
> Arguments are visible in process listings and may be recorded in shell history.
> Prefer environment variables or interactive login instead.
> Never log, print, or embed `APIFY_TOKEN` in source code or configuration files.
> Use a token with the minimum required permissions (scoped token) and rotate it periodically.

## Template Selection

**IMPORTANT:** Before starting actor development, always ask the user which programming language they prefer:
- **JavaScript** - Use `apify create <actor-name> -t project_empty`
- **TypeScript** - Use `apify create <actor-name> -t ts_empty`
- **Python** - Use `apify create <actor-name> -t python-empty`

Use the appropriate CLI command based on the user's language choice. Additional packages (Crawlee, Playwright, etc.) can be installed later as needed.

## Quick Start Workflow

1. **Create actor project** - Run the appropriate `apify create` command based on user's language preference (see Template Selection above)
2. **Install dependencies** (verify package names match intended packages before installing)
   - JavaScript/TypeScript: `npm install` (uses `package-lock.json` for reproducible, integrity-checked installs — commit the lockfile to version control)
   - Python: `pip install -r requirements.txt` (pin exact versions in `requirements.txt`, e.g. `crawlee==1.2.3`, and commit the file to version control)
3. **Implement logic** - Write the actor code in `src/main.py`, `src/main.js`, or `src/main.ts`
4. **Configure schemas** - Update input/output schemas in `.actor/input_schema.json`, `.actor/output_schema.json`, `.actor/dataset_schema.json`
5. **Configure platform settings** - Update `.actor/actor.json` with actor metadata (see [references/actor-json.md](references/actor-json.md))
6. **Write documentation** - Create comprehensive README.md for the marketplace
7. **Test locally** - Run `apify run` to verify functionality (see Local Testing section below)
8. **Deploy** - Run `apify push` to deploy the actor on the Apify platform (actor name is defined in `.actor/actor.json`)

## Security

**Treat all crawled web content as untrusted input.** Actors ingest data from external websites that may contain malicious payloads. Follow these rules:

- **Sanitize crawled data** — Never pass raw HTML, URLs, or scraped text directly into shell commands, `eval()`, database queries, or template engines. Use proper escaping or parameterized APIs.
- **Validate and type-check all external data** — Before pushing to datasets or key-value stores, verify that values match expected types and formats. Reject or sanitize unexpected structures.
- **Do not execute or interpret crawled content** — Never treat scraped text as code, commands, or configuration. Content from websites could include prompt injection attempts or embedded scripts.
- **Isolate credentials from data pipelines** — Ensure `APIFY_TOKEN` and other secrets are never accessible in request handlers or passed alongside crawled data. Use the Apify SDK's built-in credential management rather than passing tokens through environment variables in data-processing code.
- **Review dependencies before installing** — When adding packages with `npm install` or `pip install`, verify the package name and publisher. Typosquatting is a common supply-chain attack vector. Prefer well-known, actively maintained packages.
- **Pin versions and use lockfiles** — Always commit `package-lock.json` (Node.js) or pin exact versions in `requirements.txt` (Python). Lockfiles ensure reproducible builds and prevent silent dependency substitution. Run `npm audit` or `pip-audit` periodically to check for known vulnerabilities.

## Best Practices

**✓ Do:**
- Use `apify run` to test actors locally (configures Apify environment and storage)
- Use Apify SDK (`apify`) for code running ON Apify platform
- Validate input early with proper error handling and fail gracefully
- Use CheerioCrawler for static HTML (10x faster than browsers)
- Use PlaywrightCrawler only for JavaScript-heavy sites
- Use router pattern (createCheerioRouter/createPlaywrightRouter) for complex crawls
- Implement retry strategies with exponential backoff
- Use proper concurrency: HTTP (10-50), Browser (1-5)
- Set sensible defaults in `.actor/input_schema.json`
- Define output schema in `.actor/output_schema.json`
- Clean and validate data before pushing to dataset
- Use semantic CSS selectors with fallback strategies
- Respect robots.txt, ToS, and implement rate limiting
- **Always use `apify/log` package** — censors sensitive data (API keys, tokens, credentials)
- Implement readiness probe handler (required if your Actor uses standby mode)

**✗ Don't:**
- Use `npm start`, `npm run start`, `npx apify run`, or similar commands to run actors (use `apify run` instead)
- Assume local storage from `apify run` is pushed to or visible in the Apify Console — it is local-only; deploy with `apify push` and run on the platform to see results in the Console
- Rely on `Dataset.getInfo()` for final counts on Cloud
- Use browser crawlers when HTTP/Cheerio works
- Hard code values that should be in input schema or environment variables
- Skip input validation or error handling
- Overload servers - use appropriate concurrency and delays
- Scrape prohibited content or ignore Terms of Service
- Store personal/sensitive data unless explicitly permitted
- Use deprecated options like `requestHandlerTimeoutMillis` on CheerioCrawler (v3.x)
- Use `additionalHttpHeaders` - use `preNavigationHooks` instead
- Pass raw crawled content into shell commands, `eval()`, or code-generation functions
- Use `console.log()` or `print()` instead of the Apify logger — these bypass credential censoring
- Disable standby mode without explicit permission

## Logging

See [references/logging.md](references/logging.md) for complete logging documentation including available log levels and best practices for JavaScript/TypeScript and Python.

Check `usesStandbyMode` in `.actor/actor.json` - only implement if set to `true`.

## Commands

```bash
apify run          # Run Actor locally
apify login        # Authenticate account
apify push         # Deploy to Apify platform (uses name from .actor/actor.json)
apify help         # List all commands
```

**IMPORTANT:** Always use `apify run` to test actors locally. Do not use `npm run start`, `npm start`, `yarn start`, or other package manager commands - these will not properly configure the Apify environment and storage.

## Local Testing

When testing an actor locally with `apify run`, provide input data by creating a JSON file at:

```
storage/key_value_stores/default/INPUT.json
```

This file should contain the input parameters defined in your `.actor/input_schema.json`. The actor will read this input when running locally, mirroring how it receives input on the Apify platform.

**IMPORTANT - Local storage is NOT synced to the Apify Console:**
- Running `apify run` stores all data (datasets, key-value stores, request queues) **only on your local filesystem** in the `storage/` directory.
- This data is **never** automatically uploaded or pushed to the Apify platform. It exists only on your machine.
- To verify results on the Apify Console, you must deploy the Actor with `apify push` and then run it on the platform.
- Do **not** rely on checking the Apify Console to verify results from local runs — instead, inspect the local `storage/` directory or check the Actor's log output.

## Standby Mode

See [references/standby-mode.md](references/standby-mode.md) for complete standby mode documentation including readiness probe implementation for JavaScript/TypeScript and Python.

## Project Structure

```
.actor/
├── actor.json           # Actor config: name, version, env vars, runtime
├── input_schema.json    # Input validation & Console form definition
└── output_schema.json   # Output storage and display templates
src/
└── main.js/ts/py       # Actor entry point
storage/                # Local-only storage (NOT synced to Apify Console)
├── datasets/           # Output items (JSON objects)
├── key_value_stores/   # Files, config, INPUT
└── request_queues/     # Pending crawl requests
Dockerfile              # Container image definition
```

## Actor Configuration

See [references/actor-json.md](references/actor-json.md) for complete actor.json structure and configuration options.

## Input Schema

See [references/input-schema.md](references/input-schema.md) for input schema structure and examples.

## Output Schema

See [references/output-schema.md](references/output-schema.md) for output schema structure, examples, and template variables.

## Dataset Schema

See [references/dataset-schema.md](references/dataset-schema.md) for dataset schema structure, configuration, and display properties.

## Key-Value Store Schema

See [references/key-value-store-schema.md](references/key-value-store-schema.md) for key-value store schema structure, collections, and configuration.


## Apify MCP Tools

If MCP server is configured, use these tools for documentation:

- `search-apify-docs` - Search documentation
- `fetch-apify-docs` - Get full doc pages

Otherwise, the MCP Server url: `https://mcp.apify.com/?tools=docs`.

## Resources

- [docs.apify.com/llms.txt](https://docs.apify.com/llms.txt) - Apify quick reference documentation
- [docs.apify.com/llms-full.txt](https://docs.apify.com/llms-full.txt) - Apify complete documentation
- [https://crawlee.dev/llms.txt](https://crawlee.dev/llms.txt) - Crawlee quick reference documentation
- [https://crawlee.dev/llms-full.txt](https://crawlee.dev/llms-full.txt) - Crawlee complete documentation
- [whitepaper.actor](https://raw.githubusercontent.com/apify/actor-whitepaper/refs/heads/master/README.md) - Complete Actor specification

---

## Reference: Actor Json

# Actor Configuration (actor.json)

The `.actor/actor.json` file contains the Actor's configuration including metadata, schema references, and platform settings.

## Structure

```json
{
    "actorSpecification": 1,
    "name": "project-name",
    "title": "Project Title",
    "description": "Actor description",
    "version": "0.0",
    "meta": {
        "templateId": "template-id",
        "generatedBy": "<FILL-IN-TOOL-AND-MODEL>"
    },
    "input": "./input_schema.json",
    "output": "./output_schema.json",
    "storages": {
        "dataset": "./dataset_schema.json"
    },
    "dockerfile": "../Dockerfile"
}
```

## Example

```json
{
    "actorSpecification": 1,
    "name": "project-cheerio-crawler-javascript",
    "title": "Project Cheerio Crawler Javascript",
    "description": "Crawlee and Cheerio project in javascript.",
    "version": "0.0",
    "meta": {
        "templateId": "js-crawlee-cheerio",
        "generatedBy": "Claude Code with Claude Sonnet 4.5"
    },
    "input": "./input_schema.json",
    "output": "./output_schema.json",
    "storages": {
        "dataset": "./dataset_schema.json"
    },
    "dockerfile": "../Dockerfile"
}
```

## Properties

- `actorSpecification` (integer, required) - Version of actor specification (currently 1)
- `name` (string, required) - Actor identifier (lowercase, hyphens allowed)
- `title` (string, required) - Human-readable title displayed in UI
- `description` (string, optional) - Actor description for marketplace
- `version` (string, required) - Semantic version number
- `meta` (object, optional) - Metadata about actor generation
  - `templateId` (string) - ID of template used to create the actor
  - `generatedBy` (string) - Tool and model name that generated/modified the actor (e.g., "Claude Code with Claude Sonnet 4.5")
- `input` (string, optional) - Path to input schema file
- `output` (string, optional) - Path to output schema file
- `storages` (object, optional) - Storage schema references
  - `dataset` (string) - Path to dataset schema file
  - `keyValueStore` (string) - Path to key-value store schema file
- `dockerfile` (string, optional) - Path to Dockerfile

**Important:** Always fill in the `generatedBy` property with the tool and model you're currently using (e.g., "Claude Code with Claude Sonnet 4.5") to help Apify improve documentation.

---

## Reference: Dataset Schema

# Dataset Schema Reference

The dataset schema defines how your Actor's output data is structured, transformed, and displayed in the Output tab in the Apify Console.

## Examples

### JavaScript and TypeScript

Consider an example Actor that calls `Actor.pushData()` to store data into dataset:

```javascript
import { Actor } from 'apify';
// Initialize the JavaScript SDK
await Actor.init();

/**
 * Actor code
 */
await Actor.pushData({
    numericField: 10,
    pictureUrl: 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png',
    linkUrl: 'https://google.com',
    textField: 'Google',
    booleanField: true,
    dateField: new Date(),
    arrayField: ['#hello', '#world'],
    objectField: {},
});

// Exit successfully
await Actor.exit();
```

### Python

Consider an example Actor that calls `Actor.push_data()` to store data into dataset:

```python
# Dataset push example (Python)
import asyncio
from datetime import datetime
from apify import Actor

async def main():
    await Actor.init()

    # Actor code
    await Actor.push_data({
        'numericField': 10,
        'pictureUrl': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png',
        'linkUrl': 'https://google.com',
        'textField': 'Google',
        'booleanField': True,
        'dateField': datetime.now().isoformat(),
        'arrayField': ['#hello', '#world'],
        'objectField': {},
    })

    # Exit successfully
    await Actor.exit()

if __name__ == '__main__':
    asyncio.run(main())
```

## Configuration

To set up the Actor's output tab UI, reference a dataset schema file in `.actor/actor.json`:

```json
{
    "actorSpecification": 1,
    "name": "book-library-scraper",
    "title": "Book Library Scraper",
    "version": "1.0.0",
    "storages": {
        "dataset": "./dataset_schema.json"
    }
}
```

Then create the dataset schema in `.actor/dataset_schema.json`:

```json
{
    "actorSpecification": 1,
    "fields": {},
    "views": {
        "overview": {
            "title": "Overview",
            "transformation": {
                "fields": [
                    "pictureUrl",
                    "linkUrl",
                    "textField",
                    "booleanField",
                    "arrayField",
                    "objectField",
                    "dateField",
                    "numericField"
                ]
            },
            "display": {
                "component": "table",
                "properties": {
                    "pictureUrl": {
                        "label": "Image",
                        "format": "image"
                    },
                    "linkUrl": {
                        "label": "Link",
                        "format": "link"
                    },
                    "textField": {
                        "label": "Text",
                        "format": "text"
                    },
                    "booleanField": {
                        "label": "Boolean",
                        "format": "boolean"
                    },
                    "arrayField": {
                        "label": "Array",
                        "format": "array"
                    },
                    "objectField": {
                        "label": "Object",
                        "format": "object"
                    },
                    "dateField": {
                        "label": "Date",
                        "format": "date"
                    },
                    "numericField": {
                        "label": "Number",
                        "format": "number"
                    }
                }
            }
        }
    }
}
```

## Structure

```json
{
    "actorSpecification": 1,
    "fields": {},
    "views": {
        "<VIEW_NAME>": {
            "title": "string (required)",
            "description": "string (optional)",
            "transformation": {
                "fields": ["string (required)"],
                "unwind": ["string (optional)"],
                "flatten": ["string (optional)"],
                "omit": ["string (optional)"],
                "limit": "integer (optional)",
                "desc": "boolean (optional)"
            },
            "display": {
                "component": "table (required)",
                "properties": {
                    "<FIELD_NAME>": {
                        "label": "string (optional)",
                        "format": "text|number|date|link|boolean|image|array|object (optional)"
                    }
                }
            }
        }
    }
}
```

## Properties

### Dataset Schema Properties

- `actorSpecification` (integer, required) - Specifies the version of dataset schema structure document (currently only version 1)
- `fields` (JSONSchema object, required) - Schema of one dataset object (use JsonSchema Draft 2020-12 or compatible)
- `views` (DatasetView object, required) - Object with API and UI views description

### DatasetView Properties

- `title` (string, required) - Visible in UI Output tab and API
- `description` (string, optional) - Only available in API response
- `transformation` (ViewTransformation object, required) - Data transformation applied when loading from Dataset API
- `display` (ViewDisplay object, required) - Output tab UI visualization definition

### ViewTransformation Properties

- `fields` (string[], required) - Fields to present in output (order matches column order)
- `unwind` (string[], optional) - Deconstructs nested children into parent object
- `flatten` (string[], optional) - Transforms nested object into flat structure
- `omit` (string[], optional) - Removes specified fields from output
- `limit` (integer, optional) - Maximum number of results (default: all)
- `desc` (boolean, optional) - Sort order (true = newest first)

### ViewDisplay Properties

- `component` (string, required) - Only `table` is available
- `properties` (Object, optional) - Keys matching `transformation.fields` with ViewDisplayProperty values

### ViewDisplayProperty Properties

- `label` (string, optional) - Table column header
- `format` (string, optional) - One of: `text`, `number`, `date`, `link`, `boolean`, `image`, `array`, `object`

---

## Reference: Input Schema

# Input Schema Reference

The input schema defines the input parameters for an Actor. It's a JSON object comprising various field types supported by the Apify platform.

## Structure

```json
{
    "title": "<INPUT-SCHEMA-TITLE>",
    "type": "object",
    "schemaVersion": 1,
    "properties": {
        /* define input fields here */
    },
    "required": []
}
```

## Example

```json
{
    "title": "E-commerce Product Scraper Input",
    "type": "object",
    "schemaVersion": 1,
    "properties": {
        "startUrls": {
            "title": "Start URLs",
            "type": "array",
            "description": "URLs to start scraping from (category pages or product pages)",
            "editor": "requestListSources",
            "default": [{ "url": "https://example.com/category" }],
            "prefill": [{ "url": "https://example.com/category" }]
        },
        "followVariants": {
            "title": "Follow Product Variants",
            "type": "boolean",
            "description": "Whether to scrape product variants (different colors, sizes)",
            "default": true
        },
        "maxRequestsPerCrawl": {
            "title": "Max Requests per Crawl",
            "type": "integer",
            "description": "Maximum number of pages to scrape (0 = unlimited)",
            "default": 1000,
            "minimum": 0
        },
        "proxyConfiguration": {
            "title": "Proxy Configuration",
            "type": "object",
            "description": "Proxy settings for anti-bot protection",
            "editor": "proxy",
            "default": { "useApifyProxy": false }
        },
        "locale": {
            "title": "Locale",
            "type": "string",
            "description": "Language/country code for localized content",
            "default": "cs",
            "enum": ["cs", "en", "de", "sk"],
            "enumTitles": ["Czech", "English", "German", "Slovak"]
        }
    },
    "required": ["startUrls"]
}
```

---

## Reference: Key Value Store Schema

# Key-Value Store Schema Reference

The key-value store schema organizes keys into logical groups called collections for easier data management.

## Examples

### JavaScript and TypeScript

Consider an example Actor that calls `Actor.setValue()` to save records into the key-value store:

```javascript
import { Actor } from 'apify';
// Initialize the JavaScript SDK
await Actor.init();

/**
 * Actor code
 */
await Actor.setValue('document-1', 'my text data', { contentType: 'text/plain' });

await Actor.setValue(`image-${imageID}`, imageBuffer, { contentType: 'image/jpeg' });

// Exit successfully
await Actor.exit();
```

### Python

Consider an example Actor that calls `Actor.set_value()` to save records into the key-value store:

```python
# Key-Value Store set example (Python)
import asyncio
from apify import Actor

async def main():
    await Actor.init()

    # Actor code
    await Actor.set_value('document-1', 'my text data', content_type='text/plain')

    image_id = '123'          # example placeholder
    image_buffer = b'...'     # bytes buffer with image data
    await Actor.set_value(f'image-{image_id}', image_buffer, content_type='image/jpeg')

    # Exit successfully
    await Actor.exit()

if __name__ == '__main__':
    asyncio.run(main())
```

## Configuration

To configure the key-value store schema, reference a schema file in `.actor/actor.json`:

```json
{
    "actorSpecification": 1,
    "name": "data-collector",
    "title": "Data Collector",
    "version": "1.0.0",
    "storages": {
        "keyValueStore": "./key_value_store_schema.json"
    }
}
```

Then create the key-value store schema in `.actor/key_value_store_schema.json`:

```json
{
    "actorKeyValueStoreSchemaVersion": 1,
    "title": "Key-Value Store Schema",
    "collections": {
        "documents": {
            "title": "Documents",
            "description": "Text documents stored by the Actor",
            "keyPrefix": "document-"
        },
        "images": {
            "title": "Images",
            "description": "Images stored by the Actor",
            "keyPrefix": "image-",
            "contentTypes": ["image/jpeg"]
        }
    }
}
```

## Structure

```json
{
    "actorKeyValueStoreSchemaVersion": 1,
    "title": "string (required)",
    "description": "string (optional)",
    "collections": {
        "<COLLECTION_NAME>": {
            "title": "string (required)",
            "description": "string (optional)",
            "key": "string (conditional - use key OR keyPrefix)",
            "keyPrefix": "string (conditional - use key OR keyPrefix)",
            "contentTypes": ["string (optional)"],
            "jsonSchema": "object (optional)"
        }
    }
}
```

## Properties

### Key-Value Store Schema Properties

- `actorKeyValueStoreSchemaVersion` (integer, required) - Version of key-value store schema structure document (currently only version 1)
- `title` (string, required) - Title of the schema
- `description` (string, optional) - Description of the schema
- `collections` (Object, required) - Object where each key is a collection ID and value is a Collection object

### Collection Properties

- `title` (string, required) - Collection title shown in UI tabs
- `description` (string, optional) - Description appearing in UI tooltips
- `key` (string, conditional) - Single specific key for this collection
- `keyPrefix` (string, conditional) - Prefix for keys included in this collection
- `contentTypes` (string[], optional) - Allowed content types for validation
- `jsonSchema` (object, optional) - JSON Schema Draft 07 format for `application/json` content type validation

Either `key` or `keyPrefix` must be specified for each collection, but not both.

---

## Reference: Logging

# Actor Logging Reference

## JavaScript and TypeScript

**ALWAYS use the `apify/log` package for logging** - This package contains critical security logic including censoring sensitive data (Apify tokens, API keys, credentials) to prevent accidental exposure in logs.

### Available Log Levels in `apify/log`

The Apify log package provides the following methods for logging:

- `log.debug()` - Debug level logs (detailed diagnostic information)
- `log.info()` - Info level logs (general informational messages)
- `log.warning()` - Warning level logs (warning messages for potentially problematic situations)
- `log.warningOnce()` - Warning level logs (same warning message logged only once)
- `log.error()` - Error level logs (error messages for failures)
- `log.exception()` - Exception level logs (for exceptions with stack traces)
- `log.perf()` - Performance level logs (performance metrics and timing information)
- `log.deprecated()` - Deprecation level logs (warnings about deprecated code)
- `log.softFail()` - Soft failure logs (non-critical failures that don't stop execution, e.g., input validation errors, skipped items)
- `log.internal()` - Internal level logs (internal/system messages)

### Best Practices

- Use `log.debug()` for detailed operation-level diagnostics (inside functions)
- Use `log.info()` for general informational messages (API requests, successful operations)
- Use `log.warning()` for potentially problematic situations (validation failures, unexpected states)
- Use `log.error()` for actual errors and failures
- Use `log.exception()` for caught exceptions with stack traces

## Python

**ALWAYS use `Actor.log` for logging** - This logger contains critical security logic including censoring sensitive data (Apify tokens, API keys, credentials) to prevent accidental exposure in logs.

### Available Log Levels

The Apify Actor logger provides the following methods for logging:

- `Actor.log.debug()` - Debug level logs (detailed diagnostic information)
- `Actor.log.info()` - Info level logs (general informational messages)
- `Actor.log.warning()` - Warning level logs (warning messages for potentially problematic situations)
- `Actor.log.error()` - Error level logs (error messages for failures)
- `Actor.log.exception()` - Exception level logs (for exceptions with stack traces)

### Best Practices

- Use `Actor.log.debug()` for detailed operation-level diagnostics (inside functions)
- Use `Actor.log.info()` for general informational messages (API requests, successful operations)
- Use `Actor.log.warning()` for potentially problematic situations (validation failures, unexpected states)
- Use `Actor.log.error()` for actual errors and failures
- Use `Actor.log.exception()` for caught exceptions with stack traces

---

## Reference: Output Schema

# Output Schema Reference

The Actor output schema builds upon the schemas for the dataset and key-value store. It specifies where an Actor stores its output and defines templates for accessing that output. Apify Console uses these output definitions to display run results.

## Structure

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "<OUTPUT-SCHEMA-TITLE>",
    "properties": {
        /* define your outputs here */
    }
}
```

## Example

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "Output schema of the files scraper",
    "properties": {
        "files": {
            "type": "string",
            "title": "Files",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys"
        },
        "dataset": {
            "type": "string",
            "title": "Dataset",
            "template": "{{links.apiDefaultDatasetUrl}}/items"
        }
    }
}
```

## Output Schema Template Variables

- `links` (object) - Contains quick links to most commonly used URLs
- `links.publicRunUrl` (string) - Public run url in format `https://console.apify.com/view/runs/:runId`
- `links.consoleRunUrl` (string) - Console run url in format `https://console.apify.com/actors/runs/:runId`
- `links.apiRunUrl` (string) - API run url in format `https://api.apify.com/v2/actor-runs/:runId`
- `links.apiDefaultDatasetUrl` (string) - API url of default dataset in format `https://api.apify.com/v2/datasets/:defaultDatasetId`
- `links.apiDefaultKeyValueStoreUrl` (string) - API url of default key-value store in format `https://api.apify.com/v2/key-value-stores/:defaultKeyValueStoreId`
- `links.containerRunUrl` (string) - URL of a webserver running inside the run in format `https://<containerId>.runs.apify.net/`
- `run` (object) - Contains information about the run same as it is returned from the `GET Run` API endpoint
- `run.defaultDatasetId` (string) - ID of the default dataset
- `run.defaultKeyValueStoreId` (string) - ID of the default key-value store

---

## Reference: Standby Mode

# Actor Standby Mode Reference

## JavaScript and TypeScript

- **NEVER disable standby mode (`usesStandbyMode: false`) in `.actor/actor.json` without explicit permission** - Actor Standby mode solves this problem by letting you have the Actor ready in the background, waiting for the incoming HTTP requests. In a sense, the Actor behaves like a real-time web server or standard API server instead of running the logic once to process everything in batch. Always keep `usesStandbyMode: true` unless there is a specific documented reason to disable it
- **ALWAYS implement readiness probe handler for standby Actors** - Handle the `x-apify-container-server-readiness-probe` header at GET / endpoint to ensure proper Actor lifecycle management

You can recognize a standby Actor by checking the `usesStandbyMode` property in `.actor/actor.json`. Only implement the readiness probe if this property is set to `true`.

### Readiness Probe Implementation Example

```javascript
// Apify standby readiness probe at root path
app.get('/', (req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    if (req.headers['x-apify-container-server-readiness-probe']) {
        res.end('Readiness probe OK\n');
    } else {
        res.end('Actor is ready\n');
    }
});
```

Key points:

- Detect the `x-apify-container-server-readiness-probe` header in incoming requests
- Respond with HTTP 200 status code for both readiness probe and normal requests
- This enables proper Actor lifecycle management in standby mode

## Python

- **NEVER disable standby mode (`usesStandbyMode: false`) in `.actor/actor.json` without explicit permission** - Actor Standby mode solves this problem by letting you have the Actor ready in the background, waiting for the incoming HTTP requests. In a sense, the Actor behaves like a real-time web server or standard API server instead of running the logic once to process everything in batch. Always keep `usesStandbyMode: true` unless there is a specific documented reason to disable it
- **ALWAYS implement readiness probe handler for standby Actors** - Handle the `x-apify-container-server-readiness-probe` header at GET / endpoint to ensure proper Actor lifecycle management

You can recognize a standby Actor by checking the `usesStandbyMode` property in `.actor/actor.json`. Only implement the readiness probe if this property is set to `true`.

### Readiness Probe Implementation Example

```python
# Apify standby readiness probe
from http.server import SimpleHTTPRequestHandler

class GetHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle Apify standby readiness probe
        if 'x-apify-container-server-readiness-probe' in self.headers:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Readiness probe OK')
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Actor is ready')
```

Key points:

- Detect the `x-apify-container-server-readiness-probe` header in incoming requests
- Respond with HTTP 200 status code for both readiness probe and normal requests
- This enables proper Actor lifecycle management in standby mode
