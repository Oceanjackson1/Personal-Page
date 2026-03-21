---
title: "MCP Developer"
description: "Use when building, debugging, or extending MCP servers or clients that connect AI systems with external tools and data sources. Invoke to implement tool handlers, configure resource providers, set up stdio/HTTP/SSE transport layers, validate schem..."
category: "development"
source: "community"
author: "Community"
tags: ["mcp", "developer"]
date: 2026-03-20
---

# MCP Developer

Senior MCP (Model Context Protocol) developer with deep expertise in building servers and clients that connect AI systems with external tools and data sources.

## Core Workflow

1. **Analyze requirements** — Identify data sources, tools needed, and client apps
2. **Initialize project** — `npx @modelcontextprotocol/create-server my-server` (TypeScript) or `pip install mcp` + scaffold (Python)
3. **Design protocol** — Define resource URIs, tool schemas (Zod/Pydantic), and prompt templates
4. **Implement** — Register tools and resource handlers; configure transport (stdio/SSE/HTTP)
5. **Test** — Run `npx @modelcontextprotocol/inspector` to verify protocol compliance interactively; confirm tools appear, schemas accept valid inputs, and error responses are well-formed JSON-RPC 2.0. **Feedback loop:** if schema validation fails → inspect Zod/Pydantic error output → fix schema definition → re-run inspector. If a tool call returns a malformed response → check transport serialisation → fix handler → re-test.
6. **Deploy** — Package, add auth/rate-limiting, configure env vars, monitor

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Protocol | `references/protocol.md` | Message types, lifecycle, JSON-RPC 2.0 |
| TypeScript SDK | `references/typescript-sdk.md` | Building servers/clients in Node.js |
| Python SDK | `references/python-sdk.md` | Building servers/clients in Python |
| Tools | `references/tools.md` | Tool definitions, schemas, execution |
| Resources | `references/resources.md` | Resource providers, URIs, templates |

## Minimal Working Example

### TypeScript — Tool with Zod Validation

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-server", version: "1.1.0" });

// Register a tool with validated input schema
server.tool(
  "get_weather",
  "Fetch current weather for a location",
  {
    location: z.string().min(1).describe("City name or coordinates"),
    units: z.enum(["celsius", "fahrenheit"]).default("celsius"),
  },
  async ({ location, units }) => {
    // Implementation: call external API, transform response
    const data = await fetchWeather(location, units); // your fetch logic
    return {
      content: [{ type: "text", text: JSON.stringify(data) }],
    };
  }
);

// Register a resource provider
server.resource(
  "config://app",
  "Application configuration",
  async (uri) => ({
    contents: [{ uri: uri.href, text: JSON.stringify(getConfig()), mimeType: "application/json" }],
  })
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python — Tool with Pydantic Validation

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("my-server")

class WeatherInput(BaseModel):
    location: str = Field(..., min_length=1, description="City name or coordinates")
    units: str = Field("celsius", pattern="^(celsius|fahrenheit)$")

@mcp.tool()
async def get_weather(location: str, units: str = "celsius") -> str:
    """Fetch current weather for a location."""
    data = await fetch_weather(location, units)  # your fetch logic
    return str(data)

@mcp.resource("config://app")
async def app_config() -> str:
    """Expose application configuration as a resource."""
    return json.dumps(get_config())

if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport
```

**Expected tool call flow:**
```
Client → { "method": "tools/call", "params": { "name": "get_weather", "arguments": { "location": "Berlin" } } }
Server → { "result": { "content": [{ "type": "text", "text": "{\"temp\": 18, \"units\": \"celsius\"}" }] } }
```

## Constraints

### MUST DO
- Implement JSON-RPC 2.0 protocol correctly
- Validate all inputs with schemas (Zod/Pydantic)
- Use proper transport mechanisms (stdio/HTTP/SSE)
- Implement comprehensive error handling
- Add authentication and authorization
- Log protocol messages for debugging
- Test protocol compliance thoroughly
- Document server capabilities

### MUST NOT DO
- Skip input validation on tool inputs
- Expose sensitive data in resource content
- Ignore protocol version compatibility
- Mix synchronous code with async transports
- Hardcode credentials or secrets
- Return unstructured errors to clients
- Deploy without rate limiting
- Skip security controls

## Output Templates

When implementing MCP features, provide:
1. Server/client implementation file
2. Schema definitions (tools, resources, prompts)
3. Configuration file (transport, auth, etc.)
4. Brief explanation of design decisions

---

## Reference: Protocol

# MCP Protocol Specification

## Protocol Overview

MCP is built on JSON-RPC 2.0 and enables bidirectional communication between clients (like Claude Desktop) and servers that provide resources, tools, and prompts.

## Message Types

### Request/Response

```typescript
// Request format
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}

// Success response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "description": "Get weather for a location",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": { "type": "string" }
          },
          "required": ["location"]
        }
      }
    ]
  }
}

// Error response
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": { "details": "location is required" }
  }
}
```

### Notifications

```typescript
// Server sends notification (no response expected)
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "uri": "file:///project/data.json"
  }
}
```

## Connection Lifecycle

```
1. Client initiates connection (stdio/HTTP/SSE)
2. Client sends initialize request
   → Server responds with capabilities
3. Client sends initialized notification
4. Normal operation (requests/notifications)
5. Client/server can ping for keepalive
6. Client sends shutdown request
7. Connection closes
```

### Initialize Handshake

```typescript
// Client initialize request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": { "listChanged": true },
      "sampling": {}
    },
    "clientInfo": {
      "name": "claude-desktop",
      "version": "1.0.0"
    }
  }
}

// Server response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "resources": { "subscribe": true, "listChanged": true },
      "tools": { "listChanged": true },
      "prompts": { "listChanged": true }
    },
    "serverInfo": {
      "name": "my-mcp-server",
      "version": "1.0.0"
    }
  }
}

// Client sends initialized notification
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

## Core Methods

### Resources

```typescript
// List available resources
resources/list → { resources: Resource[] }

// Read resource content
resources/read { uri: string } → { contents: ResourceContent[] }

// Subscribe to resource updates (if supported)
resources/subscribe { uri: string } → {}

// Unsubscribe
resources/unsubscribe { uri: string } → {}

// Server notifies of changes
notifications/resources/list_changed → {}
notifications/resources/updated { uri: string } → {}
```

### Tools

```typescript
// List available tools
tools/list → { tools: Tool[] }

// Execute tool
tools/call {
  name: string,
  arguments: object
} → { content: ToolResponse[] }

// Server notifies of tool changes
notifications/tools/list_changed → {}
```

### Prompts

```typescript
// List available prompts
prompts/list → { prompts: Prompt[] }

// Get prompt with arguments
prompts/get {
  name: string,
  arguments?: object
} → { messages: PromptMessage[] }

// Server notifies of prompt changes
notifications/prompts/list_changed → {}
```

## Error Codes

Standard JSON-RPC 2.0 codes plus MCP-specific:

```typescript
const ERROR_CODES = {
  // JSON-RPC 2.0 standard
  PARSE_ERROR: -32700,
  INVALID_REQUEST: -32600,
  METHOD_NOT_FOUND: -32601,
  INVALID_PARAMS: -32602,
  INTERNAL_ERROR: -32603,

  // MCP-specific (implementation defined)
  RESOURCE_NOT_FOUND: -32001,
  TOOL_EXECUTION_ERROR: -32002,
  UNAUTHORIZED: -32003,
  RATE_LIMIT_EXCEEDED: -32004
};
```

## Transport Mechanisms

### stdio (Standard Input/Output)

```typescript
// Server reads from stdin, writes to stdout
// Each message is newline-delimited JSON
// Used for local integration (Claude Desktop default)
```

### HTTP with SSE (Server-Sent Events)

```typescript
// Client POSTs JSON-RPC requests to endpoint
// Server streams responses and notifications via SSE
// Used for remote servers

POST /mcp HTTP/1.1
Content-Type: application/json

{"jsonrpc":"2.0","id":1,"method":"tools/list"}

// SSE response
GET /mcp/sse HTTP/1.1

event: message
data: {"jsonrpc":"2.0","id":1,"result":{...}}
```

## Protocol Versions

Current version: `2024-11-05`

Servers must declare supported version in initialize response. Clients should verify compatibility.

## Best Practices

1. **Validation**: Always validate params with JSON Schema
2. **Error handling**: Return structured errors with helpful messages
3. **Versioning**: Check protocol version in initialize
4. **Timeouts**: Implement request timeouts (30s recommended)
5. **Logging**: Log all protocol messages for debugging
6. **Stateless**: Design tools/resources to be stateless
7. **Idempotency**: Make tool calls idempotent when possible
8. **Notifications**: Use notifications for real-time updates

---

## Reference: Python Sdk

# Python SDK Implementation

## Installation

```bash
pip install mcp pydantic
```

## Basic Server Setup

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolRequest,
    ListToolsRequest,
)
from pydantic import BaseModel, Field
import asyncio

# Create server instance
app = Server("example-server")

# Define tool input schema
class WeatherArgs(BaseModel):
    location: str = Field(..., description="City name or zip code")
    units: str = Field(default="celsius", pattern="^(celsius|fahrenheit)$")

# List available tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a location",
            inputSchema=WeatherArgs.model_json_schema(),
        )
    ]

# Handle tool execution
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather":
        # Validate arguments
        args = WeatherArgs(**arguments)

        # Execute tool logic
        weather_data = await fetch_weather(args.location, args.units)

        return [
            TextContent(
                type="text",
                text=f"Weather in {args.location}: {weather_data['temp']}°{
                    'C' if args.units == 'celsius' else 'F'
                }",
            )
        ]

    raise ValueError(f"Unknown tool: {name}")

# Run server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## Resource Provider

```python
from mcp.types import (
    Resource,
    ResourceTemplate,
    TextResourceContents,
    ListResourcesRequest,
    ReadResourceRequest,
)
import json

@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="file:///config/settings.json",
            name="Application Settings",
            description="Current application configuration",
            mimeType="application/json",
        ),
        Resource(
            uri="db://users/schema",
            name="User Schema",
            description="Database schema for users table",
            mimeType="text/plain",
        ),
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "file:///config/settings.json":
        settings = await load_settings()
        return json.dumps(settings, indent=2)

    if uri.startswith("db://users/"):
        schema = await get_database_schema("users")
        return schema

    raise ValueError(f"Resource not found: {uri}")
```

## Resource Templates (Dynamic URIs)

```python
@app.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    return [
        ResourceTemplate(
            uriTemplate="user://{user_id}/profile",
            name="User Profile",
            description="Get user profile by ID",
            mimeType="application/json",
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    # Parse template URI
    if uri.startswith("user://"):
        user_id = uri.split("/")[2]
        profile = await get_user_profile(user_id)
        return json.dumps(profile, indent=2)

    raise ValueError(f"Unknown resource: {uri}")
```

## Prompt Templates

```python
from mcp.types import (
    Prompt,
    PromptArgument,
    PromptMessage,
    GetPromptRequest,
)

@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name="code_review",
            description="Generate code review comments",
            arguments=[
                PromptArgument(
                    name="language",
                    description="Programming language",
                    required=True,
                ),
                PromptArgument(
                    name="code",
                    description="Code to review",
                    required=True,
                ),
            ],
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    if name == "code_review":
        language = arguments["language"]
        code = arguments["code"]

        return [
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"Review this {language} code and provide feedback:\n\n{code}",
                ),
            )
        ]

    raise ValueError(f"Unknown prompt: {name}")
```

## Input Validation with Pydantic

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class WeatherArgs(BaseModel):
    location: str = Field(..., min_length=1, description="City name")
    units: Literal["celsius", "fahrenheit"] = Field(default="celsius")

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Location cannot be empty")
        return v.strip()

class DatabaseQueryArgs(BaseModel):
    table: str = Field(..., pattern="^[a-zA-Z_][a-zA-Z0-9_]*$")
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "query_database":
        # Pydantic validation happens here
        args = DatabaseQueryArgs(**arguments)

        results = await execute_query(args.table, args.limit, args.offset)
        return [TextContent(type="text", text=json.dumps(results))]

    raise ValueError(f"Unknown tool: {name}")
```

## Error Handling

```python
from mcp.types import McpError, INTERNAL_ERROR, INVALID_PARAMS

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "get_weather":
            args = WeatherArgs(**arguments)
            result = await fetch_weather(args.location, args.units)
            return [TextContent(type="text", text=str(result))]

        raise ValueError(f"Unknown tool: {name}")

    except ValueError as e:
        # Validation or tool not found
        raise McpError(INVALID_PARAMS, str(e))

    except Exception as e:
        # Unexpected errors
        raise McpError(INTERNAL_ERROR, f"Tool execution failed: {e}")
```

## Logging

```python
import logging
import sys

# Configure logging to stderr (stdout is used for protocol)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)

logger = logging.getLogger("mcp-server")

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    logger.info(f"Tool called: {name} with args: {arguments}")

    try:
        result = await execute_tool(name, arguments)
        logger.info(f"Tool {name} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}", exc_info=True)
        raise
```

## Context Managers and Cleanup

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_connection():
    """Manage database connection lifecycle"""
    db = await connect_to_database()
    try:
        yield db
    finally:
        await db.close()

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "query_database":
        async with database_connection() as db:
            result = await db.execute(arguments["query"])
            return [TextContent(type="text", text=str(result))]

    raise ValueError(f"Unknown tool: {name}")
```

## Basic Client Setup

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a tool
            result = await session.call_tool(
                "get_weather",
                arguments={"location": "San Francisco"},
            )
            print(f"Result: {result.content}")

if __name__ == "__main__":
    asyncio.run(run_client())
```

## Notifications

```python
from mcp.types import ResourceUpdatedNotification

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "update_config":
        # Update configuration
        await save_config(arguments["config"])

        # Notify clients of resource update
        await app.request_context.session.send_resource_updated(
            uri="file:///config/settings.json"
        )

        return [TextContent(type="text", text="Configuration updated")]

    raise ValueError(f"Unknown tool: {name}")
```

## Best Practices

1. **Type Safety**: Use Pydantic for all schemas
2. **Async/Await**: All handlers must be async
3. **Validation**: Validate inputs early with Pydantic
4. **Logging**: Log to stderr, never stdout
5. **Error Handling**: Wrap errors in McpError
6. **Resource Cleanup**: Use context managers
7. **Testing**: Use pytest-asyncio for async tests
8. **Performance**: Cache expensive operations
9. **Security**: Sanitize all inputs and outputs
10. **Documentation**: Include docstrings and type hints

---

## Reference: Resources

# MCP Resources Reference

## Resource Basics

Resources represent data or content that can be read by AI assistants. They use URI schemes to identify content.

```typescript
{
  "uri": "file:///path/to/resource",
  "name": "Human-readable name",
  "description": "What this resource contains",
  "mimeType": "application/json"
}
```

## Common URI Schemes

### File URIs

```typescript
{
  "uri": "file:///config/settings.json",
  "name": "Application Settings",
  "mimeType": "application/json"
}

{
  "uri": "file:///docs/README.md",
  "name": "README Documentation",
  "mimeType": "text/markdown"
}
```

### Custom Schemes

```typescript
// Database resources
{
  "uri": "db://users/schema",
  "name": "Users Table Schema",
  "mimeType": "text/plain"
}

// API resources
{
  "uri": "api://v1/status",
  "name": "API Status",
  "mimeType": "application/json"
}

// Git resources
{
  "uri": "git://main/commits",
  "name": "Recent Commits",
  "mimeType": "text/plain"
}
```

## Resource Templates

Templates allow dynamic URIs with parameters.

```typescript
// TypeScript
server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => {
  return {
    resourceTemplates: [
      {
        uriTemplate: "user://{user_id}/profile",
        name: "User Profile",
        description: "Get user profile by ID",
        mimeType: "application/json",
      },
      {
        uriTemplate: "repo://{owner}/{repo}/issues",
        name: "GitHub Issues",
        description: "List issues for a repository",
        mimeType: "application/json",
      },
    ],
  };
});

// Handle templated URIs in read_resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  // Parse user profile URI
  const userMatch = uri.match(/^user:\/\/([^/]+)\/profile$/);
  if (userMatch) {
    const userId = userMatch[1];
    const profile = await getUserProfile(userId);
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(profile, null, 2),
        },
      ],
    };
  }

  // Parse GitHub issues URI
  const repoMatch = uri.match(/^repo:\/\/([^/]+)\/([^/]+)\/issues$/);
  if (repoMatch) {
    const [, owner, repo] = repoMatch;
    const issues = await fetchGitHubIssues(owner, repo);
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(issues, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

```python
# Python
@app.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    return [
        ResourceTemplate(
            uriTemplate="user://{user_id}/profile",
            name="User Profile",
            description="Get user profile by ID",
            mimeType="application/json",
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    # Parse template URI
    import re

    match = re.match(r'^user://([^/]+)/profile$', uri)
    if match:
        user_id = match.group(1)
        profile = await get_user_profile(user_id)
        return json.dumps(profile, indent=2)

    raise ValueError(f"Unknown resource: {uri}")
```

## Content Types

### Text Content

```typescript
{
  "uri": "file:///data.txt",
  "mimeType": "text/plain",
  "text": "The content of the file"
}
```

### JSON Content

```typescript
{
  "uri": "api://status",
  "mimeType": "application/json",
  "text": JSON.stringify({
    "status": "ok",
    "uptime": 12345
  }, null, 2)
}
```

### Binary Content (Base64)

```typescript
{
  "uri": "file:///image.png",
  "mimeType": "image/png",
  "blob": "base64-encoded-data-here"
}
```

### Markdown Content

```typescript
{
  "uri": "docs://api-reference",
  "mimeType": "text/markdown",
  "text": "# API Reference\n\n## Endpoints\n..."
}
```

## Implementation Patterns

### File System Resources

```typescript
import * as fs from "fs/promises";
import * as path from "path";

const ALLOWED_DIR = "/path/to/allowed/directory";

server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const files = await fs.readdir(ALLOWED_DIR);

  return {
    resources: files.map((file) => ({
      uri: `file:///${file}`,
      name: file,
      description: `File: ${file}`,
      mimeType: getMimeType(file),
    })),
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri.startsWith("file:///")) {
    const filename = uri.slice(8); // Remove "file:///"
    const safePath = path.resolve(ALLOWED_DIR, filename);

    // Security: ensure path is within allowed directory
    if (!safePath.startsWith(ALLOWED_DIR)) {
      throw new McpError(ErrorCode.InvalidParams, "Access denied");
    }

    const content = await fs.readFile(safePath, "utf-8");

    return {
      contents: [
        {
          uri,
          mimeType: getMimeType(filename),
          text: content,
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

### Database Resources

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    tables = await db.get_tables()

    return [
        Resource(
            uri=f"db://{table}/schema",
            name=f"{table} Schema",
            description=f"Schema for {table} table",
            mimeType="text/plain",
        )
        for table in tables
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri.startswith("db://"):
        parts = uri[5:].split("/")
        table = parts[0]
        resource_type = parts[1] if len(parts) > 1 else "data"

        if resource_type == "schema":
            schema = await db.get_schema(table)
            return schema

        if resource_type == "data":
            rows = await db.query(f"SELECT * FROM {table} LIMIT 100")
            return json.dumps(rows, indent=2)

    raise ValueError(f"Unknown resource: {uri}")
```

### API Resources

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "api://v1/status",
        name: "API Status",
        mimeType: "application/json",
      },
      {
        uri: "api://v1/metrics",
        name: "API Metrics",
        mimeType: "application/json",
      },
    ],
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri === "api://v1/status") {
    const status = await checkApiStatus();
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(status, null, 2),
        },
      ],
    };
  }

  if (uri === "api://v1/metrics") {
    const metrics = await collectMetrics();
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(metrics, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

### Git Repository Resources

```python
import git

@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="git://log",
            name="Git Log",
            description="Recent commits",
            mimeType="text/plain",
        ),
        Resource(
            uri="git://status",
            name="Git Status",
            description="Working tree status",
            mimeType="text/plain",
        ),
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    repo = git.Repo(".")

    if uri == "git://log":
        log = repo.git.log("--oneline", "-n", "10")
        return log

    if uri == "git://status":
        status = repo.git.status()
        return status

    raise ValueError(f"Unknown resource: {uri}")
```

## Resource Subscriptions

Allow clients to subscribe to resource updates.

```typescript
// Declare subscription capability
const server = new Server(
  { name: "example", version: "1.0.0" },
  {
    capabilities: {
      resources: {
        subscribe: true,
        listChanged: true,
      },
    },
  }
);

// Track subscriptions
const subscriptions = new Set<string>();

server.setRequestHandler(SubscribeRequestSchema, async (request) => {
  subscriptions.add(request.params.uri);
  return {};
});

server.setRequestHandler(UnsubscribeRequestSchema, async (request) => {
  subscriptions.delete(request.params.uri);
  return {};
});

// Notify subscribers when resource changes
async function notifyResourceUpdate(uri: string) {
  if (subscriptions.has(uri)) {
    await server.notification({
      method: "notifications/resources/updated",
      params: { uri },
    });
  }
}

// Example: file watcher
const watcher = fs.watch(WATCHED_DIR, async (event, filename) => {
  if (event === "change") {
    const uri = `file:///${filename}`;
    await notifyResourceUpdate(uri);
  }
});
```

## Best Practices

### 1. URI Design

```typescript
// Good: Hierarchical and descriptive
"db://users/schema"
"db://users/data"
"api://v1/endpoints/users"
"file:///config/app.json"

// Bad: Flat and ambiguous
"db1"
"data"
"config"
```

### 2. MIME Types

```typescript
function getMimeType(filename: string): string {
  const ext = filename.split(".").pop()?.toLowerCase();

  const mimeTypes: Record<string, string> = {
    json: "application/json",
    txt: "text/plain",
    md: "text/markdown",
    html: "text/html",
    xml: "application/xml",
    csv: "text/csv",
    png: "image/png",
    jpg: "image/jpeg",
    pdf: "application/pdf",
  };

  return mimeTypes[ext || ""] || "application/octet-stream";
}
```

### 3. Security

```python
def is_safe_path(base_dir: str, path: str) -> bool:
    """Ensure path doesn't escape base directory"""
    base = os.path.abspath(base_dir)
    target = os.path.abspath(os.path.join(base_dir, path))
    return target.startswith(base)

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri.startswith("file:///"):
        path = uri[8:]
        if not is_safe_path(ALLOWED_DIR, path):
            raise ValueError("Access denied")

        full_path = os.path.join(ALLOWED_DIR, path)
        with open(full_path) as f:
            return f.read()
```

### 4. Caching

```typescript
const resourceCache = new Map<string, { content: string; timestamp: number }>();
const CACHE_TTL = 60000; // 1 minute

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const now = Date.now();

  // Check cache
  const cached = resourceCache.get(uri);
  if (cached && now - cached.timestamp < CACHE_TTL) {
    return {
      contents: [{ uri, mimeType: "application/json", text: cached.content }],
    };
  }

  // Fetch and cache
  const content = await fetchResource(uri);
  resourceCache.set(uri, { content, timestamp: now });

  return {
    contents: [{ uri, mimeType: "application/json", text: content }],
  };
});
```

### 5. Large Resources

```python
@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "db://logs/recent":
        # For large datasets, limit size
        logs = await db.query(
            "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 1000"
        )
        return json.dumps(logs, indent=2)

    if uri == "file:///large.txt":
        # Read first 100KB only
        with open("/path/to/large.txt") as f:
            content = f.read(100 * 1024)
            if f.read(1):  # Check if there's more
                content += "\n\n[Content truncated...]"
            return content
```

### 6. Error Handling

```typescript
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  try {
    const content = await fetchResource(request.params.uri);
    return {
      contents: [
        {
          uri: request.params.uri,
          mimeType: "application/json",
          text: content,
        },
      ],
    };
  } catch (error) {
    if (error instanceof NotFoundError) {
      throw new McpError(ErrorCode.InvalidParams, `Resource not found: ${request.params.uri}`);
    }
    throw new McpError(ErrorCode.InternalError, `Failed to read resource: ${error.message}`);
  }
});
```

---

## Reference: Tools

# MCP Tools Reference

## Tool Definition

Tools are functions that AI assistants can invoke to perform actions or retrieve data.

```typescript
{
  "name": "tool_name",
  "description": "Clear description of what the tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "What this parameter is for"
      }
    },
    "required": ["param1"]
  }
}
```

## Input Schema Patterns

### Simple String Parameter

```typescript
{
  "name": "search_docs",
  "description": "Search documentation for a query",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query",
        "minLength": 1
      }
    },
    "required": ["query"]
  }
}
```

### Enum Values

```typescript
{
  "name": "get_weather",
  "description": "Get weather information",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": { "type": "string" },
      "units": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "default": "celsius",
        "description": "Temperature units"
      }
    },
    "required": ["location"]
  }
}
```

### Nested Objects

```typescript
{
  "name": "create_task",
  "description": "Create a new task",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "minLength": 1 },
      "metadata": {
        "type": "object",
        "properties": {
          "priority": { "type": "string", "enum": ["low", "medium", "high"] },
          "tags": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "required": ["title"]
  }
}
```

### Array Parameters

```typescript
{
  "name": "batch_process",
  "description": "Process multiple items",
  "inputSchema": {
    "type": "object",
    "properties": {
      "items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": { "type": "string" },
            "action": { "type": "string", "enum": ["update", "delete"] }
          },
          "required": ["id", "action"]
        },
        "minItems": 1,
        "maxItems": 100
      }
    },
    "required": ["items"]
  }
}
```

### Union Types (anyOf)

```typescript
{
  "name": "search",
  "description": "Search by ID or query",
  "inputSchema": {
    "type": "object",
    "properties": {
      "search": {
        "anyOf": [
          { "type": "string", "description": "Search query" },
          { "type": "number", "description": "Item ID" }
        ]
      }
    },
    "required": ["search"]
  }
}
```

## Tool Response Formats

### Text Response

```typescript
{
  "content": [
    {
      "type": "text",
      "text": "Operation completed successfully"
    }
  ]
}
```

### Multiple Content Blocks

```typescript
{
  "content": [
    {
      "type": "text",
      "text": "Found 3 results:"
    },
    {
      "type": "text",
      "text": "1. First result\n2. Second result\n3. Third result"
    }
  ]
}
```

### Image Content

```typescript
{
  "content": [
    {
      "type": "image",
      "data": "base64-encoded-image-data",
      "mimeType": "image/png"
    }
  ]
}
```

### Resource Reference

```typescript
{
  "content": [
    {
      "type": "resource",
      "resource": {
        "uri": "file:///data/results.json",
        "mimeType": "application/json",
        "text": "{\"results\": [...]}"
      }
    }
  ]
}
```

## Tool Implementation Patterns

### Database Query Tool

```typescript
// TypeScript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "query_database") {
    const { table, filter, limit } = request.params.arguments as {
      table: string;
      filter?: Record<string, any>;
      limit?: number;
    };

    // Validate table name (prevent SQL injection)
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(table)) {
      throw new McpError(ErrorCode.InvalidParams, "Invalid table name");
    }

    const results = await db.query(table, filter, limit || 10);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(results, null, 2),
        },
      ],
    };
  }
});
```

```python
# Python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "query_database":
        args = QueryArgs(**arguments)  # Pydantic validation

        # Validate table name
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', args.table):
            raise ValueError("Invalid table name")

        results = await db.query(args.table, args.filter, args.limit)

        return [
            TextContent(type="text", text=json.dumps(results, indent=2))
        ]
```

### File System Tool

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "read_file") {
    const { path } = request.params.arguments as { path: string };

    // Security: validate path is within allowed directory
    const safePath = resolvePath(ALLOWED_DIR, path);
    if (!safePath.startsWith(ALLOWED_DIR)) {
      throw new McpError(ErrorCode.InvalidParams, "Access denied");
    }

    const content = await fs.readFile(safePath, "utf-8");

    return {
      content: [{ type: "text", text: content }],
    };
  }
});
```

### HTTP API Tool

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "fetch_api":
        args = FetchArgs(**arguments)

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    args.url,
                    timeout=30.0,
                    headers={"User-Agent": "MCP Server"}
                )
                response.raise_for_status()

                return [
                    TextContent(
                        type="text",
                        text=response.text
                    )
                ]
            except httpx.HTTPError as e:
                raise McpError(INTERNAL_ERROR, f"HTTP request failed: {e}")
```

### Async Background Task

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "start_job") {
    const { jobType, params } = request.params.arguments as {
      jobType: string;
      params: Record<string, any>;
    };

    // Start job asynchronously
    const jobId = await jobQueue.enqueue(jobType, params);

    return {
      content: [
        {
          type: "text",
          text: `Job started with ID: ${jobId}`,
        },
      ],
    };
  }

  if (request.params.name === "check_job") {
    const { jobId } = request.params.arguments as { jobId: string };

    const status = await jobQueue.getStatus(jobId);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(status, null, 2),
        },
      ],
    };
  }
});
```

## Best Practices

### 1. Descriptive Names and Descriptions

```typescript
// Good
{
  "name": "search_knowledge_base",
  "description": "Search the knowledge base using semantic search. Returns top 5 relevant documents with excerpts.",
  "inputSchema": { ... }
}

// Bad
{
  "name": "search",
  "description": "Search",
  "inputSchema": { ... }
}
```

### 2. Input Validation

```python
class SearchArgs(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    max_results: int = Field(default=5, ge=1, le=50)
    filters: dict[str, str] = Field(default_factory=dict)

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        # Sanitize query
        return v.strip()
```

### 3. Error Handling

```typescript
try {
  const result = await executeOperation(params);
  return { content: [{ type: "text", text: result }] };
} catch (error) {
  if (error instanceof ValidationError) {
    throw new McpError(ErrorCode.InvalidParams, error.message);
  }
  if (error instanceof NotFoundError) {
    return {
      content: [{ type: "text", text: "Resource not found" }],
      isError: true,
    };
  }
  throw new McpError(ErrorCode.InternalError, `Operation failed: ${error.message}`);
}
```

### 4. Rate Limiting

```python
from asyncio import Lock
from datetime import datetime, timedelta

rate_limiter = {}
rate_limit_lock = Lock()

async def check_rate_limit(tool_name: str, limit: int = 10) -> None:
    async with rate_limit_lock:
        now = datetime.now()
        if tool_name not in rate_limiter:
            rate_limiter[tool_name] = []

        # Remove old entries
        rate_limiter[tool_name] = [
            t for t in rate_limiter[tool_name]
            if now - t < timedelta(minutes=1)
        ]

        if len(rate_limiter[tool_name]) >= limit:
            raise McpError(-32004, "Rate limit exceeded")

        rate_limiter[tool_name].append(now)
```

### 5. Idempotency

```typescript
// For operations that should be idempotent, use unique IDs
{
  "name": "create_record",
  "inputSchema": {
    "type": "object",
    "properties": {
      "idempotency_key": {
        "type": "string",
        "description": "Unique key to prevent duplicate operations"
      },
      "data": { "type": "object" }
    },
    "required": ["idempotency_key", "data"]
  }
}
```

### 6. Timeouts

```python
import asyncio

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "long_operation":
        try:
            result = await asyncio.wait_for(
                execute_operation(arguments),
                timeout=30.0  # 30 second timeout
            )
            return [TextContent(type="text", text=str(result))]
        except asyncio.TimeoutError:
            raise McpError(INTERNAL_ERROR, "Operation timed out")
```

### 7. Logging

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const startTime = Date.now();
  console.error(`[${new Date().toISOString()}] Tool call: ${request.params.name}`);

  try {
    const result = await executeTool(request.params.name, request.params.arguments);
    const duration = Date.now() - startTime;
    console.error(`[${new Date().toISOString()}] Tool completed in ${duration}ms`);
    return result;
  } catch (error) {
    console.error(`[${new Date().toISOString()}] Tool failed:`, error);
    throw error;
  }
});
```

---

## Reference: Typescript Sdk

# TypeScript SDK Implementation

## Installation

```bash
npm install @modelcontextprotocol/sdk zod
```

## Basic Server Setup

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// Create server instance
const server = new Server(
  {
    name: "example-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
      prompts: {},
    },
  }
);

// Handle tools/list request
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_weather",
        description: "Get current weather for a location",
        inputSchema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "City name or zip code",
            },
            units: {
              type: "string",
              enum: ["celsius", "fahrenheit"],
              default: "celsius",
            },
          },
          required: ["location"],
        },
      },
    ],
  };
});

// Handle tools/call request
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_weather") {
    const location = String(request.params.arguments?.location);
    const units = String(request.params.arguments?.units ?? "celsius");

    // Your tool logic here
    const weatherData = await fetchWeather(location, units);

    return {
      content: [
        {
          type: "text",
          text: `Weather in ${location}: ${weatherData.temp}°${units === "celsius" ? "C" : "F"}`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server with stdio transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP Server running on stdio");
}

main().catch(console.error);
```

## Resource Provider

```typescript
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// List resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "file:///config/settings.json",
        name: "Application Settings",
        description: "Current application configuration",
        mimeType: "application/json",
      },
      {
        uri: "db://users/schema",
        name: "User Schema",
        description: "Database schema for users table",
        mimeType: "text/plain",
      },
    ],
  };
});

// Read resource content
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri === "file:///config/settings.json") {
    const settings = await loadSettings();
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(settings, null, 2),
        },
      ],
    };
  }

  if (uri.startsWith("db://users/")) {
    const schema = await getDatabaseSchema("users");
    return {
      contents: [
        {
          uri,
          mimeType: "text/plain",
          text: schema,
        },
      ],
    };
  }

  throw new Error(`Resource not found: ${uri}`);
});
```

## Prompt Templates

```typescript
import {
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "code_review",
        description: "Generate code review comments",
        arguments: [
          {
            name: "language",
            description: "Programming language",
            required: true,
          },
          {
            name: "code",
            description: "Code to review",
            required: true,
          },
        ],
      },
    ],
  };
});

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  if (request.params.name === "code_review") {
    const language = String(request.params.arguments?.language);
    const code = String(request.params.arguments?.code);

    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Review this ${language} code and provide feedback:\n\n${code}`,
          },
        },
      ],
    };
  }

  throw new Error(`Unknown prompt: ${request.params.name}`);
});
```

## Input Validation with Zod

```typescript
import { z } from "zod";

// Define schemas for validation
const WeatherArgsSchema = z.object({
  location: z.string().min(1),
  units: z.enum(["celsius", "fahrenheit"]).default("celsius"),
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_weather") {
    // Validate and parse arguments
    const args = WeatherArgsSchema.parse(request.params.arguments);

    const weatherData = await fetchWeather(args.location, args.units);

    return {
      content: [
        {
          type: "text",
          text: `Temperature: ${weatherData.temp}°${args.units === "celsius" ? "C" : "F"}`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});
```

## Error Handling

```typescript
import { McpError, ErrorCode } from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Validate input
    if (!request.params.arguments?.location) {
      throw new McpError(
        ErrorCode.InvalidParams,
        "location parameter is required"
      );
    }

    const result = await executeTool(request.params.name, request.params.arguments);
    return { content: [{ type: "text", text: result }] };

  } catch (error) {
    if (error instanceof McpError) {
      throw error; // Re-throw MCP errors
    }

    // Wrap other errors
    throw new McpError(
      ErrorCode.InternalError,
      `Tool execution failed: ${error.message}`
    );
  }
});
```

## Basic Client Setup

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const client = new Client(
  {
    name: "example-client",
    version: "1.0.0",
  },
  {
    capabilities: {},
  }
);

// Connect to server
const transport = new StdioClientTransport({
  command: "node",
  args: ["./server.js"],
});

await client.connect(transport);

// List available tools
const toolsResponse = await client.request(
  { method: "tools/list" },
  ListToolsResultSchema
);

console.log("Available tools:", toolsResponse.tools);

// Call a tool
const result = await client.request(
  {
    method: "tools/call",
    params: {
      name: "get_weather",
      arguments: { location: "San Francisco" },
    },
  },
  CallToolResultSchema
);

console.log("Result:", result.content);
```

## Notifications

```typescript
// Server sends notification
server.notification({
  method: "notifications/resources/updated",
  params: {
    uri: "file:///config/settings.json",
  },
});

// Client handles notifications
client.setNotificationHandler((notification) => {
  if (notification.method === "notifications/resources/updated") {
    console.log("Resource updated:", notification.params.uri);
  }
});
```

## Best Practices

1. **Type Safety**: Use Zod for runtime validation
2. **Error Handling**: Always wrap errors in McpError
3. **Async/Await**: Use async/await throughout
4. **Logging**: Log to stderr, not stdout (stdio transport)
5. **Cleanup**: Handle graceful shutdown
6. **Testing**: Use unit tests with mock transports
7. **Performance**: Cache expensive operations
8. **Security**: Validate all inputs, sanitize outputs
