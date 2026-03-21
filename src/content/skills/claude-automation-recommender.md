---
title: "Claude Automation Recommender"
description: "分析代码库并推荐合适的 Claude Code 自动化方案（hooks、子代理、技能、插件、MCP 服务器）"
category: "workflow"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Claude Code Setup"
tags: ["automation", "setup", "optimization", "configuration"]
date: 2026-03-20
---

# Claude Automation Recommender

Analyze codebase patterns to recommend tailored Claude Code automations across all extensibility options.

**This skill is read-only.** It analyzes the codebase and outputs recommendations. It does NOT create or modify any files. Users implement the recommendations themselves or ask Claude separately to help build them.

## Output Guidelines

- **Recommend 1-2 of each type**: Don't overwhelm - surface the top 1-2 most valuable automations per category
- **If user asks for a specific type**: Focus only on that type and provide more options (3-5 recommendations)
- **Go beyond the reference lists**: The reference files contain common patterns, but use web search to find recommendations specific to the codebase's tools, frameworks, and libraries
- **Tell users they can ask for more**: End by noting they can request more recommendations for any specific category

## Automation Types Overview

| Type | Best For |
|------|----------|
| **Hooks** | Automatic actions on tool events (format on save, lint, block edits) |
| **Subagents** | Specialized reviewers/analyzers that run in parallel |
| **Skills** | Packaged expertise, workflows, and repeatable tasks (invoked by Claude or user via `/skill-name`) |
| **Plugins** | Collections of skills that can be installed |
| **MCP Servers** | External tool integrations (databases, APIs, browsers, docs) |

## Workflow

### Phase 1: Codebase Analysis

Gather project context:

```bash
# Detect project type and tools
ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null
cat package.json 2>/dev/null | head -50

# Check dependencies for MCP server recommendations
cat package.json 2>/dev/null | grep -E '"(react|vue|angular|next|express|fastapi|django|prisma|supabase|stripe)"'

# Check for existing Claude Code config
ls -la .claude/ CLAUDE.md 2>/dev/null

# Analyze project structure
ls -la src/ app/ lib/ tests/ components/ pages/ api/ 2>/dev/null
```

**Key Indicators to Capture:**

| Category | What to Look For | Informs Recommendations For |
|----------|------------------|----------------------------|
| Language/Framework | package.json, pyproject.toml, import patterns | Hooks, MCP servers |
| Frontend stack | React, Vue, Angular, Next.js | Playwright MCP, frontend skills |
| Backend stack | Express, FastAPI, Django | API documentation tools |
| Database | Prisma, Supabase, raw SQL | Database MCP servers |
| External APIs | Stripe, OpenAI, AWS SDKs | context7 MCP for docs |
| Testing | Jest, pytest, Playwright configs | Testing hooks, subagents |
| CI/CD | GitHub Actions, CircleCI | GitHub MCP server |
| Issue tracking | Linear, Jira references | Issue tracker MCP |
| Docs patterns | OpenAPI, JSDoc, docstrings | Documentation skills |

### Phase 2: Generate Recommendations

Based on analysis, generate recommendations across all categories:

#### A. MCP Server Recommendations

See [references/mcp-servers.md](references/mcp-servers.md) for detailed patterns.

| Codebase Signal | Recommended MCP Server |
|-----------------|------------------------|
| Uses popular libraries (React, Express, etc.) | **context7** - Live documentation lookup |
| Frontend with UI testing needs | **Playwright** - Browser automation/testing |
| Uses Supabase | **Supabase MCP** - Direct database operations |
| PostgreSQL/MySQL database | **Database MCP** - Query and schema tools |
| GitHub repository | **GitHub MCP** - Issues, PRs, actions |
| Uses Linear for issues | **Linear MCP** - Issue management |
| AWS infrastructure | **AWS MCP** - Cloud resource management |
| Slack workspace | **Slack MCP** - Team notifications |
| Memory/context persistence | **Memory MCP** - Cross-session memory |
| Sentry error tracking | **Sentry MCP** - Error investigation |
| Docker containers | **Docker MCP** - Container management |

#### B. Skills Recommendations

See [references/skills-reference.md](references/skills-reference.md) for details.

Create skills in `.claude/skills/<name>/SKILL.md`. Some are also available via plugins:

| Codebase Signal | Skill | Plugin |
|-----------------|-------|--------|
| Building plugins | skill-development | plugin-dev |
| Git commits | commit | commit-commands |
| React/Vue/Angular | frontend-design | frontend-design |
| Automation rules | writing-rules | hookify |
| Feature planning | feature-dev | feature-dev |

**Custom skills to create** (with templates, scripts, examples):

| Codebase Signal | Skill to Create | Invocation |
|-----------------|-----------------|------------|
| API routes | **api-doc** (with OpenAPI template) | Both |
| Database project | **create-migration** (with validation script) | User-only |
| Test suite | **gen-test** (with example tests) | User-only |
| Component library | **new-component** (with templates) | User-only |
| PR workflow | **pr-check** (with checklist) | User-only |
| Releases | **release-notes** (with git context) | User-only |
| Code style | **project-conventions** | Claude-only |
| Onboarding | **setup-dev** (with prereq script) | User-only |

#### C. Hooks Recommendations

See [references/hooks-patterns.md](references/hooks-patterns.md) for configurations.

| Codebase Signal | Recommended Hook |
|-----------------|------------------|
| Prettier configured | PostToolUse: auto-format on edit |
| ESLint/Ruff configured | PostToolUse: auto-lint on edit |
| TypeScript project | PostToolUse: type-check on edit |
| Tests directory exists | PostToolUse: run related tests |
| `.env` files present | PreToolUse: block `.env` edits |
| Lock files present | PreToolUse: block lock file edits |
| Security-sensitive code | PreToolUse: require confirmation |

#### D. Subagent Recommendations

See [references/subagent-templates.md](references/subagent-templates.md) for templates.

| Codebase Signal | Recommended Subagent |
|-----------------|---------------------|
| Large codebase (>500 files) | **code-reviewer** - Parallel code review |
| Auth/payments code | **security-reviewer** - Security audits |
| API project | **api-documenter** - OpenAPI generation |
| Performance critical | **performance-analyzer** - Bottleneck detection |
| Frontend heavy | **ui-reviewer** - Accessibility review |
| Needs more tests | **test-writer** - Test generation |

#### E. Plugin Recommendations

See [references/plugins-reference.md](references/plugins-reference.md) for available plugins.

| Codebase Signal | Recommended Plugin |
|-----------------|-------------------|
| General productivity | **anthropic-agent-skills** - Core skills bundle |
| Document workflows | Install docx, xlsx, pdf skills |
| Frontend development | **frontend-design** plugin |
| Building AI tools | **mcp-builder** for MCP development |

### Phase 3: Output Recommendations Report

Format recommendations clearly. **Only include 1-2 recommendations per category** - the most valuable ones for this specific codebase. Skip categories that aren't relevant.

```markdown
## Claude Code Automation Recommendations

I've analyzed your codebase and identified the top automations for each category. Here are my top 1-2 recommendations per type:

### Codebase Profile
- **Type**: [detected language/runtime]
- **Framework**: [detected framework]
- **Key Libraries**: [relevant libraries detected]

---

### 🔌 MCP Servers

#### context7
**Why**: [specific reason based on detected libraries]
**Install**: `claude mcp add context7`

---

### 🎯 Skills

#### [skill name]
**Why**: [specific reason]
**Create**: `.claude/skills/[name]/SKILL.md`
**Invocation**: User-only / Both / Claude-only
**Also available in**: [plugin-name] plugin (if applicable)
```yaml
---
name: [skill-name]
description: [what it does]
disable-model-invocation: true  # for user-only
---
```

---

### ⚡ Hooks

#### [hook name]
**Why**: [specific reason based on detected config]
**Where**: `.claude/settings.json`

---

### 🤖 Subagents

#### [agent name]
**Why**: [specific reason based on codebase patterns]
**Where**: `.claude/agents/[name].md`

---

**Want more?** Ask for additional recommendations for any specific category (e.g., "show me more MCP server options" or "what other hooks would help?").

**Want help implementing any of these?** Just ask and I can help you set up any of the recommendations above.
```

## Decision Framework

### When to Recommend MCP Servers
- External service integration needed (databases, APIs)
- Documentation lookup for libraries/SDKs
- Browser automation or testing
- Team tool integration (GitHub, Linear, Slack)
- Cloud infrastructure management

### When to Recommend Skills

- Document generation (docx, xlsx, pptx, pdf — also in plugins)
- Frequently repeated prompts or workflows
- Project-specific tasks with arguments
- Applying templates or scripts to tasks (skills can bundle supporting files)
- Quick actions invoked with `/skill-name`
- Workflows that should run in isolation (`context: fork`)

**Invocation control:**
- `disable-model-invocation: true` — User-only (for side effects: deploy, commit, send)
- `user-invocable: false` — Claude-only (for background knowledge)
- Default (omit both) — Both can invoke

### When to Recommend Hooks
- Repetitive post-edit actions (formatting, linting)
- Protection rules (block sensitive file edits)
- Validation checks (tests, type checks)

### When to Recommend Subagents
- Specialized expertise needed (security, performance)
- Parallel review workflows
- Background quality checks

### When to Recommend Plugins
- Need multiple related skills
- Want pre-packaged automation bundles
- Team-wide standardization

---

## Configuration Tips

### MCP Server Setup

**Team sharing**: Check `.mcp.json` into repo so entire team gets same MCP servers

**Debugging**: Use `--mcp-debug` flag to identify configuration issues

**Prerequisites to recommend:**
- GitHub CLI (`gh`) - enables native GitHub operations
- Puppeteer/Playwright CLI - for browser MCP servers

### Headless Mode (for CI/Automation)

Recommend headless Claude for automated pipelines:

```bash
# Pre-commit hook example
claude -p "fix lint errors in src/" --allowedTools Edit,Write

# CI pipeline with structured output
claude -p "<prompt>" --output-format stream-json | your_command
```

### Permissions for Hooks

Configure allowed tools in `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Edit", "Write", "Bash(npm test:*)", "Bash(git commit:*)"]
  }
}
```

---

## Reference: Hooks Patterns

# Hooks Recommendations

Hooks automatically run commands in response to Claude Code events. They're ideal for enforcement and automation that should happen consistently.

**Note**: These are common patterns. Use web search to find hooks for tools/frameworks not listed here to recommend the best hooks for the user.

## Auto-Formatting Hooks

### Prettier (JavaScript/TypeScript)
| Detection | File Exists |
|-----------|-------------|
| `.prettierrc`, `.prettierrc.json`, `prettier.config.js` | ✓ |

**Recommend**: PostToolUse hook on Edit/Write to auto-format
**Value**: Code stays formatted without thinking about it

### ESLint (JavaScript/TypeScript)
| Detection | File Exists |
|-----------|-------------|
| `.eslintrc`, `.eslintrc.json`, `eslint.config.js` | ✓ |

**Recommend**: PostToolUse hook on Edit/Write to auto-fix
**Value**: Lint errors fixed automatically

### Black/isort (Python)
| Detection | File Exists |
|-----------|-------------|
| `pyproject.toml` with black/isort, `.black`, `setup.cfg` | ✓ |

**Recommend**: PostToolUse hook to format Python files
**Value**: Consistent Python formatting

### Ruff (Python - Modern)
| Detection | File Exists |
|-----------|-------------|
| `ruff.toml`, `pyproject.toml` with `[tool.ruff]` | ✓ |

**Recommend**: PostToolUse hook for lint + format
**Value**: Fast, comprehensive Python linting

### gofmt (Go)
| Detection | File Exists |
|-----------|-------------|
| `go.mod` | ✓ |

**Recommend**: PostToolUse hook to run gofmt
**Value**: Standard Go formatting

### rustfmt (Rust)
| Detection | File Exists |
|-----------|-------------|
| `Cargo.toml` | ✓ |

**Recommend**: PostToolUse hook to run rustfmt
**Value**: Standard Rust formatting

---

## Type Checking Hooks

### TypeScript
| Detection | File Exists |
|-----------|-------------|
| `tsconfig.json` | ✓ |

**Recommend**: PostToolUse hook to run tsc --noEmit
**Value**: Catch type errors immediately

### mypy/pyright (Python)
| Detection | File Exists |
|-----------|-------------|
| `mypy.ini`, `pyrightconfig.json`, pyproject.toml with mypy | ✓ |

**Recommend**: PostToolUse hook for type checking
**Value**: Catch type errors in Python

---

## Protection Hooks

### Block Sensitive File Edits
| Detection | Presence Of |
|-----------|-------------|
| `.env`, `.env.local`, `.env.production` | Environment files |
| `credentials.json`, `secrets.yaml` | Secret files |
| `.git/` directory | Git internals |

**Recommend**: PreToolUse hook that blocks Edit/Write to these paths
**Value**: Prevent accidental secret exposure or git corruption

### Block Lock File Edits
| Detection | Presence Of |
|-----------|-------------|
| `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | JS lock files |
| `Cargo.lock`, `poetry.lock`, `Pipfile.lock` | Other lock files |

**Recommend**: PreToolUse hook that blocks direct edits
**Value**: Lock files should only change via package manager

---

## Test Runner Hooks

### Jest (JavaScript/TypeScript)
| Detection | Presence Of |
|-----------|-------------|
| `jest.config.js`, `jest` in package.json | Jest configured |
| `__tests__/`, `*.test.ts`, `*.spec.ts` | Test files exist |

**Recommend**: PostToolUse hook to run related tests after edit
**Value**: Immediate test feedback on changes

### pytest (Python)
| Detection | Presence Of |
|-----------|-------------|
| `pytest.ini`, `pyproject.toml` with pytest | pytest configured |
| `tests/`, `test_*.py` | Test files exist |

**Recommend**: PostToolUse hook to run pytest on changed files
**Value**: Immediate test feedback

---

## Quick Reference: Detection → Recommendation

| If You See | Recommend This Hook |
|------------|-------------------|
| Prettier config | Auto-format on Edit/Write |
| ESLint config | Auto-lint on Edit/Write |
| Ruff/Black config | Auto-format Python |
| tsconfig.json | Type-check on Edit |
| Test directory | Run related tests on Edit |
| .env files | Block .env edits |
| Lock files | Block lock file edits |
| Go project | gofmt on Edit |
| Rust project | rustfmt on Edit |

---

## Notification Hooks

Notification hooks run when Claude Code sends notifications. Use matchers to filter by notification type.

### Permission Alerts
| Matcher | Use Case |
|---------|----------|
| `permission_prompt` | Alert when Claude requests permissions |

**Recommend**: Play sound, send desktop notification, or log permission requests
**Value**: Never miss permission prompts when multitasking

### Idle Notifications
| Matcher | Use Case |
|---------|----------|
| `idle_prompt` | Alert when Claude is waiting for input (60+ seconds idle) |

**Recommend**: Play sound or send notification when Claude needs attention
**Value**: Know when Claude is ready for your input

### Example Configuration

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Ping.aiff"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude is waiting\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Available Matchers

| Matcher | Triggers When |
|---------|---------------|
| `permission_prompt` | Claude needs permission for a tool |
| `idle_prompt` | Claude waiting for input (60+ seconds) |
| `auth_success` | Authentication succeeds |
| `elicitation_dialog` | MCP tool needs input |

---

## Quick Reference: Detection → Recommendation

| If You See | Recommend This Hook |
|------------|-------------------|
| Prettier config | Auto-format on Edit/Write |
| ESLint config | Auto-lint on Edit/Write |
| Ruff/Black config | Auto-format Python |
| tsconfig.json | Type-check on Edit |
| Test directory | Run related tests on Edit |
| .env files | Block .env edits |
| Lock files | Block lock file edits |
| Go project | gofmt on Edit |
| Rust project | rustfmt on Edit |
| Multitasking workflow | Notification hooks for alerts |

---

## Hook Placement

Hooks go in `.claude/settings.json`:

```
.claude/
└── settings.json  ← Hook configurations here
```

Recommend creating the `.claude/` directory if it doesn't exist.

---

## Reference: Mcp Servers

# MCP Server Recommendations

MCP (Model Context Protocol) servers extend Claude's capabilities by connecting to external tools and services.

**Note**: These are common MCP servers. Use web search to find MCP servers specific to the codebase's services and integrations.

## Setup & Team Sharing

**Connection methods:**
1. **Project config** (`.mcp.json`) - Available only in that directory
2. **Global config** (`~/.claude.json`) - Available across all projects
3. **Checked-in `.mcp.json`** - Available to entire team (recommended!)

**Tip**: Check `.mcp.json` into git so your whole team gets the same MCP servers.

**Debugging**: Use `claude --mcp-debug` to identify configuration issues.

## Documentation & Knowledge

### context7
**Best for**: Projects using popular libraries/SDKs where you want Claude to code with up-to-date documentation

| Recommend When | Examples |
|----------------|----------|
| Using React, Vue, Angular | Frontend frameworks |
| Using Express, FastAPI, Django | Backend frameworks |
| Using Prisma, Drizzle | ORMs |
| Using Stripe, Twilio, SendGrid | Third-party APIs |
| Using AWS SDK, Google Cloud | Cloud SDKs |
| Using LangChain, OpenAI SDK | AI/ML libraries |

**Value**: Claude fetches live documentation instead of relying on training data, reducing hallucinated APIs and outdated patterns.

---

## Browser & Frontend

### Playwright MCP
**Best for**: Frontend projects needing browser automation, testing, or screenshots

| Recommend When | Examples |
|----------------|----------|
| React/Vue/Angular app | UI component testing |
| E2E tests needed | User flow validation |
| Visual regression testing | Screenshot comparisons |
| Debugging UI issues | See what user sees |
| Form testing | Multi-step workflows |

**Value**: Claude can interact with your running app, take screenshots, fill forms, and verify UI behavior.

### Puppeteer MCP
**Best for**: Headless browser automation, web scraping

| Recommend When | Examples |
|----------------|----------|
| PDF generation from HTML | Report generation |
| Web scraping tasks | Data extraction |
| Headless testing | CI environments |

---

## Databases

### Supabase MCP
**Best for**: Projects using Supabase for backend/database

| Recommend When | Examples |
|----------------|----------|
| Supabase project detected | `@supabase/supabase-js` in deps |
| Auth + database needs | User management apps |
| Real-time features | Live data sync |

**Value**: Claude can query tables, manage auth, and interact with Supabase storage directly.

### PostgreSQL MCP
**Best for**: Direct PostgreSQL database access

| Recommend When | Examples |
|----------------|----------|
| Raw PostgreSQL usage | No ORM layer |
| Database migrations | Schema management |
| Data analysis tasks | Complex queries |
| Debugging data issues | Inspect actual data |

### Neon MCP
**Best for**: Neon serverless Postgres users

### Turso MCP
**Best for**: Turso/libSQL edge database users

---

## Version Control & DevOps

### GitHub MCP
**Best for**: GitHub-hosted repositories needing issue/PR integration

| Recommend When | Examples |
|----------------|----------|
| GitHub repository | `.git` with GitHub remote |
| Issue-driven development | Reference issues in commits |
| PR workflows | Review, merge operations |
| GitHub Actions | CI/CD pipeline access |
| Release management | Tag and release automation |

**Value**: Claude can create issues, review PRs, check workflow runs, and manage releases.

### GitLab MCP
**Best for**: GitLab-hosted repositories

### Linear MCP
**Best for**: Teams using Linear for issue tracking

| Recommend When | Examples |
|----------------|----------|
| Linear workspace | Issue references like `ABC-123` |
| Sprint planning | Backlog management |
| Issue creation from code | Auto-create issues for TODOs |

---

## Cloud Infrastructure

### AWS MCP
**Best for**: AWS infrastructure management

| Recommend When | Examples |
|----------------|----------|
| AWS SDK in dependencies | `@aws-sdk/*` packages |
| Infrastructure as code | Terraform, CDK, SAM |
| Lambda development | Serverless functions |
| S3, DynamoDB usage | Cloud data services |

### Cloudflare MCP
**Best for**: Cloudflare Workers, Pages, R2, D1

| Recommend When | Examples |
|----------------|----------|
| Cloudflare Workers | Edge functions |
| Pages deployment | Static site hosting |
| R2 storage | Object storage |
| D1 database | Edge SQL database |

### Vercel MCP
**Best for**: Vercel deployment and configuration

---

## Monitoring & Observtic

### Sentry MCP
**Best for**: Error tracking and debugging

| Recommend When | Examples |
|----------------|----------|
| Sentry configured | `@sentry/*` in deps |
| Production debugging | Investigate errors |
| Error patterns | Group similar issues |
| Release tracking | Correlate deploys with errors |

**Value**: Claude can investigate Sentry issues, find root causes, and suggest fixes.

### Datadog MCP
**Best for**: APM, logs, and metrics

---

## Communication

### Slack MCP
**Best for**: Slack workspace integration

| Recommend When | Examples |
|----------------|----------|
| Team uses Slack | Send notifications |
| Deployment notifications | Alert channels |
| Incident response | Post updates |

### Notion MCP
**Best for**: Notion workspace for documentation

| Recommend When | Examples |
|----------------|----------|
| Notion for docs | Read/update pages |
| Knowledge base | Search documentation |
| Meeting notes | Create summaries |

---

## File & Data

### Filesystem MCP
**Best for**: Enhanced file operations beyond built-in tools

| Recommend When | Examples |
|----------------|----------|
| Complex file operations | Batch processing |
| File watching | Monitor changes |
| Advanced search | Custom patterns |

### Memory MCP
**Best for**: Persistent memory across sessions

| Recommend When | Examples |
|----------------|----------|
| Long-running projects | Remember context |
| User preferences | Store settings |
| Learning patterns | Build knowledge |

**Value**: Claude remembers project context, decisions, and patterns across conversations.

---

## Containers & DevOps

### Docker MCP
**Best for**: Container management

| Recommend When | Examples |
|----------------|----------|
| Docker Compose file | Container orchestration |
| Dockerfile present | Build images |
| Container debugging | Inspect logs, exec |

### Kubernetes MCP
**Best for**: Kubernetes cluster management

| Recommend When | Examples |
|----------------|----------|
| K8s manifests | Deploy, scale pods |
| Helm charts | Package management |
| Cluster debugging | Pod logs, status |

---

## AI & ML

### Exa MCP
**Best for**: Web search and research

| Recommend When | Examples |
|----------------|----------|
| Research tasks | Find current info |
| Competitive analysis | Market research |
| Documentation gaps | Find examples |

---

## Quick Reference: Detection Patterns

| Look For | Suggests MCP Server |
|----------|-------------------|
| Popular npm packages | context7 |
| React/Vue/Next.js | Playwright MCP |
| `@supabase/supabase-js` | Supabase MCP |
| `pg` or `postgres` | PostgreSQL MCP |
| GitHub remote | GitHub MCP |
| `.linear` or Linear refs | Linear MCP |
| `@aws-sdk/*` | AWS MCP |
| `@sentry/*` | Sentry MCP |
| `docker-compose.yml` | Docker MCP |
| Slack webhook URLs | Slack MCP |
| `@anthropic-ai/sdk` | context7 for Anthropic docs |

---

## Reference: Plugins Reference

# Plugin Recommendations

Plugins are installable collections of skills, commands, agents, and hooks. Install via `/plugin install`.

**Note**: These are plugins from the official repository. Use web search to discover additional community plugins.

---

## Official Plugins

### Development & Code Quality

| Plugin | Best For | Key Features |
|--------|----------|--------------|
| **plugin-dev** | Building Claude Code plugins | Skills for creating skills, hooks, commands, agents |
| **pr-review-toolkit** | PR review workflows | Specialized review agents (code, tests, types) |
| **code-review** | Automated code review | Multi-agent review with confidence scoring |
| **code-simplifier** | Code refactoring | Simplify code while preserving functionality |
| **feature-dev** | Feature development | End-to-end feature workflow with agents |

### Git & Workflow

| Plugin | Best For | Key Features |
|--------|----------|--------------|
| **commit-commands** | Git workflows | /commit, /commit-push-pr commands |
| **hookify** | Automation rules | Create hooks from conversation patterns |

### Frontend

| Plugin | Best For | Key Features |
|--------|----------|--------------|
| **frontend-design** | UI development | Production-grade UI, avoids generic aesthetics |

### Learning & Guidance

| Plugin | Best For | Key Features |
|--------|----------|--------------|
| **explanatory-output-style** | Learning | Educational insights about code choices |
| **learning-output-style** | Interactive learning | Requests contributions at decision points |
| **security-guidance** | Security awareness | Warns about security issues when editing |

### Language Servers (LSP)

| Plugin | Language |
|--------|----------|
| **typescript-lsp** | TypeScript/JavaScript |
| **pyright-lsp** | Python |
| **gopls-lsp** | Go |
| **rust-analyzer-lsp** | Rust |
| **clangd-lsp** | C/C++ |
| **jdtls-lsp** | Java |
| **kotlin-lsp** | Kotlin |
| **swift-lsp** | Swift |
| **csharp-lsp** | C# |
| **php-lsp** | PHP |
| **lua-lsp** | Lua |

---

## Quick Reference: Codebase → Plugin

| Codebase Signal | Recommended Plugin |
|-----------------|-------------------|
| Building plugins | plugin-dev |
| PR-based workflow | pr-review-toolkit |
| Git commits | commit-commands |
| React/Vue/Angular | frontend-design |
| Want automation rules | hookify |
| TypeScript project | typescript-lsp |
| Python project | pyright-lsp |
| Go project | gopls-lsp |
| Security-sensitive code | security-guidance |
| Learning/onboarding | explanatory-output-style |

---

## Plugin Management

```bash
# Install a plugin
/plugin install <plugin-name>

# List installed plugins
/plugin list

# View plugin details
/plugin info <plugin-name>
```

---

## When to Recommend Plugins

**Recommend plugin installation when:**
- User wants to install Claude Code automations from Anthropic's official repository or another shared marketplace
- User needs multiple related capabilities
- Team wants standardized workflows
- First-time Claude Code setup

---

## Reference: Skills Reference

# Skills Recommendations

Skills are packaged expertise with workflows, reference materials, and best practices. Create them in `.claude/skills/<name>/SKILL.md`. Skills can be invoked by Claude automatically when relevant, or by users directly with `/skill-name`.

Some pre-built skills are available through official plugins (install via `/plugin install`).

**Note**: These are common patterns. Use web search to find skill ideas specific to the codebase's tools and frameworks.

---

## Available from Official Plugins

### Plugin Development (plugin-dev)

| Skill | Best For |
|-------|----------|
| **skill-development** | Creating new skills with proper structure |
| **hook-development** | Building hooks for automation |
| **command-development** | Creating slash commands |
| **agent-development** | Building specialized subagents |
| **mcp-integration** | Integrating MCP servers into plugins |
| **plugin-structure** | Understanding plugin architecture |

### Git Workflows (commit-commands)

| Skill | Best For |
|-------|----------|
| **commit** | Creating git commits with proper messages |
| **commit-push-pr** | Full commit, push, and PR workflow |

### Frontend (frontend-design)

| Skill | Best For |
|-------|----------|
| **frontend-design** | Creating polished UI components |

**Value**: Creates distinctive, high-quality UI instead of generic AI aesthetics.

### Automation Rules (hookify)

| Skill | Best For |
|-------|----------|
| **writing-rules** | Creating hookify rules for automation |

### Feature Development (feature-dev)

| Skill | Best For |
|-------|----------|
| **feature-dev** | End-to-end feature development workflow |

---

## Quick Reference: Official Plugin Skills

| Codebase Signal | Skill | Plugin |
|-----------------|-------|--------|
| Building plugins | skill-development | plugin-dev |
| Git commits | commit | commit-commands |
| React/Vue/Angular | frontend-design | frontend-design |
| Automation rules | writing-rules | hookify |
| Feature planning | feature-dev | feature-dev |

---

## Custom Project Skills

Create project-specific skills in `.claude/skills/<name>/SKILL.md`.

### Skill Structure

```
.claude/skills/
└── my-skill/
    ├── SKILL.md           # Main instructions (required)
    ├── template.yaml      # Template to apply
    ├── scripts/
    │   └── validate.sh    # Script to run
    └── examples/          # Reference examples
```

### Frontmatter Reference

```yaml
---
name: skill-name
description: What this skill does and when to use it
disable-model-invocation: true  # Only user can invoke (for side effects)
user-invocable: false           # Only Claude can invoke (for background knowledge)
allowed-tools: Read, Grep, Glob # Restrict tool access
context: fork                   # Run in isolated subagent
agent: Explore                  # Which agent type when forked
---
```

### Invocation Control

| Setting | User | Claude | Use for |
|---------|------|--------|---------|
| (default) | ✓ | ✓ | General-purpose skills |
| `disable-model-invocation: true` | ✓ | ✗ | Side effects (deploy, send) |
| `user-invocable: false` | ✗ | ✓ | Background knowledge |

---

## Custom Skill Examples

### API Documentation with OpenAPI Template

Apply a YAML template to generate consistent API docs:

```
.claude/skills/api-doc/
├── SKILL.md
└── openapi-template.yaml
```

**SKILL.md:**
```yaml
---
name: api-doc
description: Generate OpenAPI documentation for an endpoint. Use when documenting API routes.
---

Generate OpenAPI documentation for the endpoint at $ARGUMENTS.

Use the template in [openapi-template.yaml](openapi-template.yaml) as the structure.

1. Read the endpoint code
2. Extract path, method, parameters, request/response schemas
3. Fill in the template with actual values
4. Output the completed YAML
```

**openapi-template.yaml:**
```yaml
paths:
  /{path}:
    {method}:
      summary: ""
      description: ""
      parameters: []
      requestBody:
        content:
          application/json:
            schema: {}
      responses:
        "200":
          description: ""
          content:
            application/json:
              schema: {}
```

---

### Database Migration Generator with Script

Generate and validate migrations using a bundled script:

```
.claude/skills/create-migration/
├── SKILL.md
└── scripts/
    └── validate-migration.sh
```

**SKILL.md:**
```yaml
---
name: create-migration
description: Create a database migration file
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

Create a migration for: $ARGUMENTS

1. Generate migration file in `migrations/` with timestamp prefix
2. Include up and down functions
3. Run validation: `bash ~/.claude/skills/create-migration/scripts/validate-migration.sh`
4. Report any issues found
```

**scripts/validate-migration.sh:**
```bash
#!/bin/bash
# Validate migration syntax
npx prisma validate 2>&1 || echo "Validation failed"
```

---

### Test Generator with Examples

Generate tests following project patterns:

```
.claude/skills/gen-test/
├── SKILL.md
└── examples/
    ├── unit-test.ts
    └── integration-test.ts
```

**SKILL.md:**
```yaml
---
name: gen-test
description: Generate tests for a file following project conventions
disable-model-invocation: true
---

Generate tests for: $ARGUMENTS

Reference these examples for the expected patterns:
- Unit tests: [examples/unit-test.ts](examples/unit-test.ts)
- Integration tests: [examples/integration-test.ts](examples/integration-test.ts)

1. Analyze the source file
2. Identify functions/methods to test
3. Generate tests matching project conventions
4. Place in appropriate test directory
```

---

### Component Generator with Template

Scaffold new components from a template:

```
.claude/skills/new-component/
├── SKILL.md
└── templates/
    ├── component.tsx.template
    ├── component.test.tsx.template
    └── component.stories.tsx.template
```

**SKILL.md:**
```yaml
---
name: new-component
description: Scaffold a new React component with tests and stories
disable-model-invocation: true
---

Create component: $ARGUMENTS

Use templates in [templates/](templates/) directory:
1. Generate component from component.tsx.template
2. Generate tests from component.test.tsx.template
3. Generate Storybook story from component.stories.tsx.template

Replace {{ComponentName}} with the PascalCase name.
Replace {{component-name}} with the kebab-case name.
```

---

### PR Review with Checklist

Review PRs against a project-specific checklist:

```
.claude/skills/pr-check/
├── SKILL.md
└── checklist.md
```

**SKILL.md:**
```yaml
---
name: pr-check
description: Review PR against project checklist
disable-model-invocation: true
context: fork
---

## PR Context
- Diff: !`gh pr diff`
- Description: !`gh pr view`

Review against [checklist.md](checklist.md).

For each item, mark ✅ or ❌ with explanation.
```

**checklist.md:**
```markdown
## PR Checklist

- [ ] Tests added for new functionality
- [ ] No console.log statements
- [ ] Error handling includes user-facing messages
- [ ] API changes are backwards compatible
- [ ] Database migrations are reversible
```

---

### Release Notes Generator

Generate release notes from git history:

**SKILL.md:**
```yaml
---
name: release-notes
description: Generate release notes from commits since last tag
disable-model-invocation: true
---

## Recent Changes
- Commits since last tag: !`git log $(git describe --tags --abbrev=0)..HEAD --oneline`
- Last tag: !`git describe --tags --abbrev=0`

Generate release notes:
1. Group commits by type (feat, fix, docs, etc.)
2. Write user-friendly descriptions
3. Highlight breaking changes
4. Format as markdown
```

---

### Project Conventions (Claude-only)

Background knowledge Claude applies automatically:

**SKILL.md:**
```yaml
---
name: project-conventions
description: Code style and patterns for this project. Apply when writing or reviewing code.
user-invocable: false
---

## Naming Conventions
- React components: PascalCase
- Utilities: camelCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case

## Patterns
- Use `Result<T, E>` for fallible operations, not exceptions
- Prefer composition over inheritance
- All API responses use `{ data, error, meta }` shape

## Forbidden
- No `any` types
- No `console.log` in production code
- No synchronous file I/O
```

---

### Environment Setup

Onboard new developers with setup script:

```
.claude/skills/setup-dev/
├── SKILL.md
└── scripts/
    └── check-prerequisites.sh
```

**SKILL.md:**
```yaml
---
name: setup-dev
description: Set up development environment for new contributors
disable-model-invocation: true
---

Set up development environment:

1. Check prerequisites: `bash scripts/check-prerequisites.sh`
2. Install dependencies: `npm install`
3. Copy environment template: `cp .env.example .env`
4. Set up database: `npm run db:setup`
5. Verify setup: `npm test`

Report any issues encountered.
```

---

## Argument Patterns

| Pattern | Meaning | Example |
|---------|---------|---------|
| `$ARGUMENTS` | All args as string | `/deploy staging` → "staging" |

Arguments are appended as `ARGUMENTS: <value>` if `$ARGUMENTS` isn't in the skill.

## Dynamic Context Injection

Use `!`command`` to inject live data before the skill runs:

```yaml
## Current State
- Branch: !`git branch --show-current`
- Status: !`git status --short`
```

The command output replaces the placeholder before Claude sees the skill content.

---

## Reference: Subagent Templates

# Subagent Recommendations

Subagents are specialized Claude instances that run in parallel, each with their own context window and tool access. They're ideal for focused reviews, analysis, or generation tasks.

**Note**: These are common patterns. Design custom subagents based on the codebase's specific review and analysis needs.

## Code Review Agents

### code-reviewer
**Best for**: Automated code quality checks on large codebases

| Recommend When | Detection |
|----------------|-----------|
| Large codebase (>500 files) | File count |
| Frequent code changes | Active development |
| Team wants consistent review | Quality focus |

**Value**: Runs code review in parallel while you continue working
**Model**: sonnet (balanced quality/speed)
**Tools**: Read, Grep, Glob, Bash

---

### security-reviewer
**Best for**: Security-focused code review

| Recommend When | Detection |
|----------------|-----------|
| Auth code present | `auth/`, `login`, `session` patterns |
| Payment processing | `stripe`, `payment`, `billing` patterns |
| User data handling | `user`, `profile`, `pii` patterns |
| API keys in code | Environment variable patterns |

**Value**: Catches OWASP vulnerabilities, auth issues, data exposure
**Model**: sonnet
**Tools**: Read, Grep, Glob (read-only for safety)

---

### test-writer
**Best for**: Generating comprehensive test coverage

| Recommend When | Detection |
|----------------|-----------|
| Low test coverage | Few test files vs source files |
| Test suite exists | `tests/`, `__tests__/` present |
| Testing framework configured | jest, pytest, vitest in deps |

**Value**: Generates tests matching project conventions
**Model**: sonnet
**Tools**: Read, Write, Grep, Glob

---

## Specialized Agents

### api-documenter
**Best for**: API documentation generation

| Recommend When | Detection |
|----------------|-----------|
| REST endpoints | Express routes, FastAPI paths |
| GraphQL schema | `.graphql` files |
| OpenAPI exists | `openapi.yaml`, `swagger.json` |
| Undocumented APIs | Routes without docs |

**Value**: Generates OpenAPI specs, endpoint documentation
**Model**: sonnet
**Tools**: Read, Write, Grep, Glob

---

### performance-analyzer
**Best for**: Finding performance bottlenecks

| Recommend When | Detection |
|----------------|-----------|
| Database queries | ORM usage, raw SQL |
| High-traffic code | API endpoints, hot paths |
| Performance complaints | User reports slowness |
| Complex algorithms | Nested loops, recursion |

**Value**: Finds N+1 queries, O(n²) algorithms, memory leaks
**Model**: sonnet
**Tools**: Read, Grep, Glob, Bash

---

### ui-reviewer
**Best for**: Frontend accessibility and UX review

| Recommend When | Detection |
|----------------|-----------|
| React/Vue/Angular | Frontend framework detected |
| Component library | `components/` directory |
| User-facing UI | Not just API project |

**Value**: Catches accessibility issues, UX problems, responsive design gaps
**Model**: sonnet
**Tools**: Read, Grep, Glob

---

## Utility Agents

### dependency-updater
**Best for**: Safe dependency updates

| Recommend When | Detection |
|----------------|-----------|
| Outdated deps | `npm outdated` has results |
| Security advisories | `npm audit` warnings |
| Major version behind | Significant version gaps |

**Value**: Updates dependencies incrementally with testing
**Model**: sonnet
**Tools**: Read, Write, Bash, Grep

---

### migration-helper
**Best for**: Framework/version migrations

| Recommend When | Detection |
|----------------|-----------|
| Major upgrade needed | Framework version very old |
| Breaking changes coming | Deprecation warnings |
| Refactoring planned | Architectural changes |

**Value**: Plans and executes migrations incrementally
**Model**: opus (complex reasoning needed)
**Tools**: Read, Write, Grep, Glob, Bash

---

## Quick Reference: Detection → Recommendation

| If You See | Recommend Subagent |
|------------|-------------------|
| Large codebase | code-reviewer |
| Auth/payment code | security-reviewer |
| Few tests | test-writer |
| API routes | api-documenter |
| Database heavy | performance-analyzer |
| Frontend components | ui-reviewer |
| Outdated packages | dependency-updater |
| Old framework version | migration-helper |

---

## Subagent Placement

Subagents go in `.claude/agents/`:

```
.claude/
└── agents/
    ├── code-reviewer.md
    ├── security-reviewer.md
    └── test-writer.md
```

---

## Model Selection Guide

| Model | Best For | Trade-off |
|-------|----------|-----------|
| **haiku** | Simple, repetitive checks | Fast, cheap, less thorough |
| **sonnet** | Most review/analysis tasks | Balanced (recommended default) |
| **opus** | Complex migrations, architecture | Thorough, slower, more expensive |

---

## Tool Access Guide

| Access Level | Tools | Use Case |
|--------------|-------|----------|
| Read-only | Read, Grep, Glob | Reviews, analysis |
| Writing | + Write | Code generation, docs |
| Full | + Bash | Migrations, testing |
