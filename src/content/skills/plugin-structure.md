---
title: "Plugin Structure"
description: "Claude Code 插件的标准化目录结构和清单配置指南"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["plugin", "structure", "architecture", "manifest"]
date: 2026-03-20
---


# Plugin Structure for Claude Code

## Overview

Claude Code plugins follow a standardized directory structure with automatic component discovery. Understanding this structure enables creating well-organized, maintainable plugins that integrate seamlessly with Claude Code.

**Key concepts:**
- Conventional directory layout for automatic discovery
- Manifest-driven configuration in `.claude-plugin/plugin.json`
- Component-based organization (commands, agents, skills, hooks)
- Portable path references using `${CLAUDE_PLUGIN_ROOT}`
- Explicit vs. auto-discovered component loading

## Directory Structure

Every Claude Code plugin follows this organizational pattern:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── commands/                 # Slash commands (.md files)
├── agents/                   # Subagent definitions (.md files)
├── skills/                   # Agent skills (subdirectories)
│   └── skill-name/
│       └── SKILL.md         # Required for each skill
├── hooks/
│   └── hooks.json           # Event handler configuration
├── .mcp.json                # MCP server definitions
└── scripts/                 # Helper scripts and utilities
```

**Critical rules:**

1. **Manifest location**: The `plugin.json` manifest MUST be in `.claude-plugin/` directory
2. **Component locations**: All component directories (commands, agents, skills, hooks) MUST be at plugin root level, NOT nested inside `.claude-plugin/`
3. **Optional components**: Only create directories for components the plugin actually uses
4. **Naming convention**: Use kebab-case for all directory and file names

## Plugin Manifest (plugin.json)

The manifest defines plugin metadata and configuration. Located at `.claude-plugin/plugin.json`:

### Required Fields

```json
{
  "name": "plugin-name"
}
```

**Name requirements:**
- Use kebab-case format (lowercase with hyphens)
- Must be unique across installed plugins
- No spaces or special characters
- Example: `code-review-assistant`, `test-runner`, `api-docs`

### Recommended Metadata

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/plugin-name",
  "license": "MIT",
  "keywords": ["testing", "automation", "ci-cd"]
}
```

**Version format**: Follow semantic versioning (MAJOR.MINOR.PATCH)
**Keywords**: Use for plugin discovery and categorization

### Component Path Configuration

Specify custom paths for components (supplements default directories):

```json
{
  "name": "plugin-name",
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Important**: Custom paths supplement defaults—they don't replace them. Components in both default directories and custom paths will load.

**Path rules:**
- Must be relative to plugin root
- Must start with `./`
- Cannot use absolute paths
- Support arrays for multiple locations

## Component Organization

### Commands

**Location**: `commands/` directory
**Format**: Markdown files with YAML frontmatter
**Auto-discovery**: All `.md` files in `commands/` load automatically

**Example structure**:
```
commands/
├── review.md        # /review command
├── test.md          # /test command
└── deploy.md        # /deploy command
```

**File format**:
```markdown
---
name: command-name
description: Command description
---

Command implementation instructions...
```

**Usage**: Commands integrate as native slash commands in Claude Code

### Agents

**Location**: `agents/` directory
**Format**: Markdown files with YAML frontmatter
**Auto-discovery**: All `.md` files in `agents/` load automatically

**Example structure**:
```
agents/
├── code-reviewer.md
├── test-generator.md
└── refactorer.md
```

**File format**:
```markdown
---
description: Agent role and expertise
capabilities:
  - Specific task 1
  - Specific task 2
---

Detailed agent instructions and knowledge...
```

**Usage**: Users can invoke agents manually, or Claude Code selects them automatically based on task context

### Skills

**Location**: `skills/` directory with subdirectories per skill
**Format**: Each skill in its own directory with `SKILL.md` file
**Auto-discovery**: All `SKILL.md` files in skill subdirectories load automatically

**Example structure**:
```
skills/
├── api-testing/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── test-runner.py
│   └── references/
│       └── api-spec.md
└── database-migrations/
    ├── SKILL.md
    └── examples/
        └── migration-template.sql
```

**SKILL.md format**:
```markdown
---
name: Skill Name
description: When to use this skill
version: 1.0.0
---

Skill instructions and guidance...
```

**Supporting files**: Skills can include scripts, references, examples, or assets in subdirectories

**Usage**: Claude Code autonomously activates skills based on task context matching the description

### Hooks

**Location**: `hooks/hooks.json` or inline in `plugin.json`
**Format**: JSON configuration defining event handlers
**Registration**: Hooks register automatically when plugin enables

**Example structure**:
```
hooks/
├── hooks.json           # Hook configuration
└── scripts/
    ├── validate.sh      # Hook script
    └── check-style.sh   # Hook script
```

**Configuration format**:
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
      "timeout": 30
    }]
  }]
}
```

**Available events**: PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification

**Usage**: Hooks execute automatically in response to Claude Code events

### MCP Servers

**Location**: `.mcp.json` at plugin root or inline in `plugin.json`
**Format**: JSON configuration for MCP server definitions
**Auto-start**: Servers start automatically when plugin enables

**Example format**:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Usage**: MCP servers integrate seamlessly with Claude Code's tool system

## Portable Path References

### ${CLAUDE_PLUGIN_ROOT}

Use `${CLAUDE_PLUGIN_ROOT}` environment variable for all intra-plugin path references:

```json
{
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
}
```

**Why it matters**: Plugins install in different locations depending on:
- User installation method (marketplace, local, npm)
- Operating system conventions
- User preferences

**Where to use it**:
- Hook command paths
- MCP server command arguments
- Script execution references
- Resource file paths

**Never use**:
- Hardcoded absolute paths (`/Users/name/plugins/...`)
- Relative paths from working directory (`./scripts/...` in commands)
- Home directory shortcuts (`~/plugins/...`)

### Path Resolution Rules

**In manifest JSON fields** (hooks, MCP servers):
```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/tool.sh"
```

**In component files** (commands, agents, skills):
```markdown
Reference scripts at: ${CLAUDE_PLUGIN_ROOT}/scripts/helper.py
```

**In executed scripts**:
```bash
#!/bin/bash
# ${CLAUDE_PLUGIN_ROOT} available as environment variable
source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
```

## File Naming Conventions

### Component Files

**Commands**: Use kebab-case `.md` files
- `code-review.md` → `/code-review`
- `run-tests.md` → `/run-tests`
- `api-docs.md` → `/api-docs`

**Agents**: Use kebab-case `.md` files describing role
- `test-generator.md`
- `code-reviewer.md`
- `performance-analyzer.md`

**Skills**: Use kebab-case directory names
- `api-testing/`
- `database-migrations/`
- `error-handling/`

### Supporting Files

**Scripts**: Use descriptive kebab-case names with appropriate extensions
- `validate-input.sh`
- `generate-report.py`
- `process-data.js`

**Documentation**: Use kebab-case markdown files
- `api-reference.md`
- `migration-guide.md`
- `best-practices.md`

**Configuration**: Use standard names
- `hooks.json`
- `.mcp.json`
- `plugin.json`

## Auto-Discovery Mechanism

Claude Code automatically discovers and loads components:

1. **Plugin manifest**: Reads `.claude-plugin/plugin.json` when plugin enables
2. **Commands**: Scans `commands/` directory for `.md` files
3. **Agents**: Scans `agents/` directory for `.md` files
4. **Skills**: Scans `skills/` for subdirectories containing `SKILL.md`
5. **Hooks**: Loads configuration from `hooks/hooks.json` or manifest
6. **MCP servers**: Loads configuration from `.mcp.json` or manifest

**Discovery timing**:
- Plugin installation: Components register with Claude Code
- Plugin enable: Components become available for use
- No restart required: Changes take effect on next Claude Code session

**Override behavior**: Custom paths in `plugin.json` supplement (not replace) default directories

## Best Practices

### Organization

1. **Logical grouping**: Group related components together
   - Put test-related commands, agents, and skills together
   - Create subdirectories in `scripts/` for different purposes

2. **Minimal manifest**: Keep `plugin.json` lean
   - Only specify custom paths when necessary
   - Rely on auto-discovery for standard layouts
   - Use inline configuration only for simple cases

3. **Documentation**: Include README files
   - Plugin root: Overall purpose and usage
   - Component directories: Specific guidance
   - Script directories: Usage and requirements

### Naming

1. **Consistency**: Use consistent naming across components
   - If command is `test-runner`, name related agent `test-runner-agent`
   - Match skill directory names to their purpose

2. **Clarity**: Use descriptive names that indicate purpose
   - Good: `api-integration-testing/`, `code-quality-checker.md`
   - Avoid: `utils/`, `misc.md`, `temp.sh`

3. **Length**: Balance brevity with clarity
   - Commands: 2-3 words (`review-pr`, `run-ci`)
   - Agents: Describe role clearly (`code-reviewer`, `test-generator`)
   - Skills: Topic-focused (`error-handling`, `api-design`)

### Portability

1. **Always use ${CLAUDE_PLUGIN_ROOT}**: Never hardcode paths
2. **Test on multiple systems**: Verify on macOS, Linux, Windows
3. **Document dependencies**: List required tools and versions
4. **Avoid system-specific features**: Use portable bash/Python constructs

### Maintenance

1. **Version consistently**: Update version in plugin.json for releases
2. **Deprecate gracefully**: Mark old components clearly before removal
3. **Document breaking changes**: Note changes affecting existing users
4. **Test thoroughly**: Verify all components work after changes

## Common Patterns

### Minimal Plugin

Single command with no dependencies:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json    # Just name field
└── commands/
    └── hello.md       # Single command
```

### Full-Featured Plugin

Complete plugin with all component types:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/          # User-facing commands
├── agents/            # Specialized subagents
├── skills/            # Auto-activating skills
├── hooks/             # Event handlers
│   ├── hooks.json
│   └── scripts/
├── .mcp.json          # External integrations
└── scripts/           # Shared utilities
```

### Skill-Focused Plugin

Plugin providing only skills:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    └── skill-two/
        └── SKILL.md
```

## Troubleshooting

**Component not loading**:
- Verify file is in correct directory with correct extension
- Check YAML frontmatter syntax (commands, agents, skills)
- Ensure skill has `SKILL.md` (not `README.md` or other name)
- Confirm plugin is enabled in Claude Code settings

**Path resolution errors**:
- Replace all hardcoded paths with `${CLAUDE_PLUGIN_ROOT}`
- Verify paths are relative and start with `./` in manifest
- Check that referenced files exist at specified paths
- Test with `echo $CLAUDE_PLUGIN_ROOT` in hook scripts

**Auto-discovery not working**:
- Confirm directories are at plugin root (not in `.claude-plugin/`)
- Check file naming follows conventions (kebab-case, correct extensions)
- Verify custom paths in manifest are correct
- Restart Claude Code to reload plugin configuration

**Conflicts between plugins**:
- Use unique, descriptive component names
- Namespace commands with plugin name if needed
- Document potential conflicts in plugin README
- Consider command prefixes for related functionality

---

For detailed examples and advanced patterns, see files in `references/` and `examples/` directories.


---

## Reference: component patterns

# Component Organization Patterns

Advanced patterns for organizing plugin components effectively.

## Component Lifecycle

### Discovery Phase

When Claude Code starts:

1. **Scan enabled plugins**: Read `.claude-plugin/plugin.json` for each
2. **Discover components**: Look in default and custom paths
3. **Parse definitions**: Read YAML frontmatter and configurations
4. **Register components**: Make available to Claude Code
5. **Initialize**: Start MCP servers, register hooks

**Timing**: Component registration happens during Claude Code initialization, not continuously.

### Activation Phase

When components are used:

**Commands**: User types slash command → Claude Code looks up → Executes
**Agents**: Task arrives → Claude Code evaluates capabilities → Selects agent
**Skills**: Task context matches description → Claude Code loads skill
**Hooks**: Event occurs → Claude Code calls matching hooks
**MCP Servers**: Tool call matches server capability → Forwards to server

## Command Organization Patterns

### Flat Structure

Single directory with all commands:

```
commands/
├── build.md
├── test.md
├── deploy.md
├── review.md
└── docs.md
```

**When to use**:
- 5-15 commands total
- All commands at same abstraction level
- No clear categorization

**Advantages**:
- Simple, easy to navigate
- No configuration needed
- Fast discovery

### Categorized Structure

Multiple directories for different command types:

```
commands/              # Core commands
├── build.md
└── test.md

admin-commands/        # Administrative
├── configure.md
└── manage.md

workflow-commands/     # Workflow automation
├── review.md
└── deploy.md
```

**Manifest configuration**:
```json
{
  "commands": [
    "./commands",
    "./admin-commands",
    "./workflow-commands"
  ]
}
```

**When to use**:
- 15+ commands
- Clear functional categories
- Different permission levels

**Advantages**:
- Organized by purpose
- Easier to maintain
- Can restrict access by directory

### Hierarchical Structure

Nested organization for complex plugins:

```
commands/
├── ci/
│   ├── build.md
│   ├── test.md
│   └── lint.md
├── deployment/
│   ├── staging.md
│   └── production.md
└── management/
    ├── config.md
    └── status.md
```

**Note**: Claude Code doesn't support nested command discovery automatically. Use custom paths:

```json
{
  "commands": [
    "./commands/ci",
    "./commands/deployment",
    "./commands/management"
  ]
}
```

**When to use**:
- 20+ commands
- Multi-level categorization
- Complex workflows

**Advantages**:
- Maximum organization
- Clear boundaries
- Scalable structure

## Agent Organization Patterns

### Role-Based Organization

Organize agents by their primary role:

```
agents/
├── code-reviewer.md        # Reviews code
├── test-generator.md       # Generates tests
├── documentation-writer.md # Writes docs
└── refactorer.md          # Refactors code
```

**When to use**:
- Agents have distinct, non-overlapping roles
- Users invoke agents manually
- Clear agent responsibilities

### Capability-Based Organization

Organize by specific capabilities:

```
agents/
├── python-expert.md        # Python-specific
├── typescript-expert.md    # TypeScript-specific
├── api-specialist.md       # API design
└── database-specialist.md  # Database work
```

**When to use**:
- Technology-specific agents
- Domain expertise focus
- Automatic agent selection

### Workflow-Based Organization

Organize by workflow stage:

```
agents/
├── planning-agent.md      # Planning phase
├── implementation-agent.md # Coding phase
├── testing-agent.md       # Testing phase
└── deployment-agent.md    # Deployment phase
```

**When to use**:
- Sequential workflows
- Stage-specific expertise
- Pipeline automation

## Skill Organization Patterns

### Topic-Based Organization

Each skill covers a specific topic:

```
skills/
├── api-design/
│   └── SKILL.md
├── error-handling/
│   └── SKILL.md
├── testing-strategies/
│   └── SKILL.md
└── performance-optimization/
    └── SKILL.md
```

**When to use**:
- Knowledge-based skills
- Educational or reference content
- Broad applicability

### Tool-Based Organization

Skills for specific tools or technologies:

```
skills/
├── docker/
│   ├── SKILL.md
│   └── references/
│       └── dockerfile-best-practices.md
├── kubernetes/
│   ├── SKILL.md
│   └── examples/
│       └── deployment.yaml
└── terraform/
    ├── SKILL.md
    └── scripts/
        └── validate-config.sh
```

**When to use**:
- Tool-specific expertise
- Complex tool configurations
- Tool best practices

### Workflow-Based Organization

Skills for complete workflows:

```
skills/
├── code-review-workflow/
│   ├── SKILL.md
│   └── references/
│       ├── checklist.md
│       └── standards.md
├── deployment-workflow/
│   ├── SKILL.md
│   └── scripts/
│       ├── pre-deploy.sh
│       └── post-deploy.sh
└── testing-workflow/
    ├── SKILL.md
    └── examples/
        └── test-structure.md
```

**When to use**:
- Multi-step processes
- Company-specific workflows
- Process automation

### Skill with Rich Resources

Comprehensive skill with all resource types:

```
skills/
└── api-testing/
    ├── SKILL.md              # Core skill (1500 words)
    ├── references/
    │   ├── rest-api-guide.md
    │   ├── graphql-guide.md
    │   └── authentication.md
    ├── examples/
    │   ├── basic-test.js
    │   ├── authenticated-test.js
    │   └── integration-test.js
    ├── scripts/
    │   ├── run-tests.sh
    │   └── generate-report.py
    └── assets/
        └── test-template.json
```

**Resource usage**:
- **SKILL.md**: Overview and when to use resources
- **references/**: Detailed guides (loaded as needed)
- **examples/**: Copy-paste code samples
- **scripts/**: Executable test runners
- **assets/**: Templates and configurations

## Hook Organization Patterns

### Monolithic Configuration

Single hooks.json with all hooks:

```
hooks/
├── hooks.json     # All hook definitions
└── scripts/
    ├── validate-write.sh
    ├── validate-bash.sh
    └── load-context.sh
```

**hooks.json**:
```json
{
  "PreToolUse": [...],
  "PostToolUse": [...],
  "Stop": [...],
  "SessionStart": [...]
}
```

**When to use**:
- 5-10 hooks total
- Simple hook logic
- Centralized configuration

### Event-Based Organization

Separate files per event type:

```
hooks/
├── hooks.json              # Combines all
├── pre-tool-use.json      # PreToolUse hooks
├── post-tool-use.json     # PostToolUse hooks
├── stop.json              # Stop hooks
└── scripts/
    ├── validate/
    │   ├── write.sh
    │   └── bash.sh
    └── context/
        └── load.sh
```

**hooks.json** (combines):
```json
{
  "PreToolUse": ${file:./pre-tool-use.json},
  "PostToolUse": ${file:./post-tool-use.json},
  "Stop": ${file:./stop.json}
}
```

**Note**: Use build script to combine files, Claude Code doesn't support file references.

**When to use**:
- 10+ hooks
- Different teams managing different events
- Complex hook configurations

### Purpose-Based Organization

Group by functional purpose:

```
hooks/
├── hooks.json
└── scripts/
    ├── security/
    │   ├── validate-paths.sh
    │   ├── check-credentials.sh
    │   └── scan-malware.sh
    ├── quality/
    │   ├── lint-code.sh
    │   ├── check-tests.sh
    │   └── verify-docs.sh
    └── workflow/
        ├── notify-team.sh
        └── update-status.sh
```

**When to use**:
- Many hook scripts
- Clear functional boundaries
- Team specialization

## Script Organization Patterns

### Flat Scripts

All scripts in single directory:

```
scripts/
├── build.sh
├── test.py
├── deploy.sh
├── validate.js
└── report.py
```

**When to use**:
- 5-10 scripts
- All scripts related
- Simple plugin

### Categorized Scripts

Group by purpose:

```
scripts/
├── build/
│   ├── compile.sh
│   └── package.sh
├── test/
│   ├── run-unit.sh
│   └── run-integration.sh
├── deploy/
│   ├── staging.sh
│   └── production.sh
└── utils/
    ├── log.sh
    └── notify.sh
```

**When to use**:
- 10+ scripts
- Clear categories
- Reusable utilities

### Language-Based Organization

Group by programming language:

```
scripts/
├── bash/
│   ├── build.sh
│   └── deploy.sh
├── python/
│   ├── analyze.py
│   └── report.py
└── javascript/
    ├── bundle.js
    └── optimize.js
```

**When to use**:
- Multi-language scripts
- Different runtime requirements
- Language-specific dependencies

## Cross-Component Patterns

### Shared Resources

Components sharing common resources:

```
plugin/
├── commands/
│   ├── test.md        # Uses lib/test-utils.sh
│   └── deploy.md      # Uses lib/deploy-utils.sh
├── agents/
│   └── tester.md      # References lib/test-utils.sh
├── hooks/
│   └── scripts/
│       └── pre-test.sh # Sources lib/test-utils.sh
└── lib/
    ├── test-utils.sh
    └── deploy-utils.sh
```

**Usage in components**:
```bash
#!/bin/bash
source "${CLAUDE_PLUGIN_ROOT}/lib/test-utils.sh"
run_tests
```

**Benefits**:
- Code reuse
- Consistent behavior
- Easier maintenance

### Layered Architecture

Separate concerns into layers:

```
plugin/
├── commands/          # User interface layer
├── agents/            # Orchestration layer
├── skills/            # Knowledge layer
└── lib/
    ├── core/         # Core business logic
    ├── integrations/ # External services
    └── utils/        # Helper functions
```

**When to use**:
- Large plugins (100+ files)
- Multiple developers
- Clear separation of concerns

### Plugin Within Plugin

Nested plugin structure:

```
plugin/
├── .claude-plugin/
│   └── plugin.json
├── core/              # Core functionality
│   ├── commands/
│   └── agents/
└── extensions/        # Optional extensions
    ├── extension-a/
    │   ├── commands/
    │   └── agents/
    └── extension-b/
        ├── commands/
        └── agents/
```

**Manifest**:
```json
{
  "commands": [
    "./core/commands",
    "./extensions/extension-a/commands",
    "./extensions/extension-b/commands"
  ]
}
```

**When to use**:
- Modular functionality
- Optional features
- Plugin families

## Best Practices

### Naming

1. **Consistent naming**: Match file names to component purpose
2. **Descriptive names**: Indicate what component does
3. **Avoid abbreviations**: Use full words for clarity

### Organization

1. **Start simple**: Use flat structure, reorganize when needed
2. **Group related items**: Keep related components together
3. **Separate concerns**: Don't mix unrelated functionality

### Scalability

1. **Plan for growth**: Choose structure that scales
2. **Refactor early**: Reorganize before it becomes painful
3. **Document structure**: Explain organization in README

### Maintainability

1. **Consistent patterns**: Use same structure throughout
2. **Minimize nesting**: Keep directory depth manageable
3. **Use conventions**: Follow community standards

### Performance

1. **Avoid deep nesting**: Impacts discovery time
2. **Minimize custom paths**: Use defaults when possible
3. **Keep configurations small**: Large configs slow loading

---

## Reference: manifest reference

# Plugin Manifest Reference

Complete reference for `plugin.json` configuration.

## File Location

**Required path**: `.claude-plugin/plugin.json`

The manifest MUST be in the `.claude-plugin/` directory at the plugin root. Claude Code will not recognize plugins without this file in the correct location.

## Complete Field Reference

### Core Fields

#### name (required)

**Type**: String
**Format**: kebab-case
**Example**: `"test-automation-suite"`

The unique identifier for the plugin. Used for:
- Plugin identification in Claude Code
- Conflict detection with other plugins
- Command namespacing (optional)

**Requirements**:
- Must be unique across all installed plugins
- Use only lowercase letters, numbers, and hyphens
- No spaces or special characters
- Start with a letter
- End with a letter or number

**Validation**:
```javascript
/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/
```

**Examples**:
- ✅ Good: `api-tester`, `code-review`, `git-workflow-automation`
- ❌ Bad: `API Tester`, `code_review`, `-git-workflow`, `test-`

#### version

**Type**: String
**Format**: Semantic versioning (MAJOR.MINOR.PATCH)
**Example**: `"2.1.0"`
**Default**: `"0.1.0"` if not specified

Semantic versioning guidelines:
- **MAJOR**: Incompatible API changes, breaking changes
- **MINOR**: New functionality, backward-compatible
- **PATCH**: Bug fixes, backward-compatible

**Pre-release versions**:
- `"1.0.0-alpha.1"` - Alpha release
- `"1.0.0-beta.2"` - Beta release
- `"1.0.0-rc.1"` - Release candidate

**Examples**:
- `"0.1.0"` - Initial development
- `"1.0.0"` - First stable release
- `"1.2.3"` - Patch update to 1.2
- `"2.0.0"` - Major version with breaking changes

#### description

**Type**: String
**Length**: 50-200 characters recommended
**Example**: `"Automates code review workflows with style checks and automated feedback"`

Brief explanation of plugin purpose and functionality.

**Best practices**:
- Focus on what the plugin does, not how
- Use active voice
- Mention key features or benefits
- Keep under 200 characters for marketplace display

**Examples**:
- ✅ "Generates comprehensive test suites from code analysis and coverage reports"
- ✅ "Integrates with Jira for automatic issue tracking and sprint management"
- ❌ "A plugin that helps you do testing stuff"
- ❌ "This is a very long description that goes on and on about every single feature..."

### Metadata Fields

#### author

**Type**: Object
**Fields**: name (required), email (optional), url (optional)

```json
{
  "author": {
    "name": "Jane Developer",
    "email": "jane@example.com",
    "url": "https://janedeveloper.com"
  }
}
```

**Alternative format** (string only):
```json
{
  "author": "Jane Developer <jane@example.com> (https://janedeveloper.com)"
}
```

**Use cases**:
- Credit and attribution
- Contact for support or questions
- Marketplace display
- Community recognition

#### homepage

**Type**: String (URL)
**Example**: `"https://docs.example.com/plugins/my-plugin"`

Link to plugin documentation or landing page.

**Should point to**:
- Plugin documentation site
- Project homepage
- Detailed usage guide
- Installation instructions

**Not for**:
- Source code (use `repository` field)
- Issue tracker (include in documentation)
- Personal websites (use `author.url`)

#### repository

**Type**: String (URL) or Object
**Example**: `"https://github.com/user/plugin-name"`

Source code repository location.

**String format**:
```json
{
  "repository": "https://github.com/user/plugin-name"
}
```

**Object format** (detailed):
```json
{
  "repository": {
    "type": "git",
    "url": "https://github.com/user/plugin-name.git",
    "directory": "packages/plugin-name"
  }
}
```

**Use cases**:
- Source code access
- Issue reporting
- Community contributions
- Transparency and trust

#### license

**Type**: String
**Format**: SPDX identifier
**Example**: `"MIT"`

Software license identifier.

**Common licenses**:
- `"MIT"` - Permissive, popular choice
- `"Apache-2.0"` - Permissive with patent grant
- `"GPL-3.0"` - Copyleft
- `"BSD-3-Clause"` - Permissive
- `"ISC"` - Permissive, similar to MIT
- `"UNLICENSED"` - Proprietary, not open source

**Full list**: https://spdx.org/licenses/

**Multiple licenses**:
```json
{
  "license": "(MIT OR Apache-2.0)"
}
```

#### keywords

**Type**: Array of strings
**Example**: `["testing", "automation", "ci-cd", "quality-assurance"]`

Tags for plugin discovery and categorization.

**Best practices**:
- Use 5-10 keywords
- Include functionality categories
- Add technology names
- Use common search terms
- Avoid duplicating plugin name

**Categories to consider**:
- Functionality: `testing`, `debugging`, `documentation`, `deployment`
- Technologies: `typescript`, `python`, `docker`, `aws`
- Workflows: `ci-cd`, `code-review`, `git-workflow`
- Domains: `web-development`, `data-science`, `devops`

### Component Path Fields

#### commands

**Type**: String or Array of strings
**Default**: `["./commands"]`
**Example**: `"./cli-commands"`

Additional directories or files containing command definitions.

**Single path**:
```json
{
  "commands": "./custom-commands"
}
```

**Multiple paths**:
```json
{
  "commands": [
    "./commands",
    "./admin-commands",
    "./experimental-commands"
  ]
}
```

**Behavior**: Supplements default `commands/` directory (does not replace)

**Use cases**:
- Organizing commands by category
- Separating stable from experimental commands
- Loading commands from shared locations

#### agents

**Type**: String or Array of strings
**Default**: `["./agents"]`
**Example**: `"./specialized-agents"`

Additional directories or files containing agent definitions.

**Format**: Same as `commands` field

**Use cases**:
- Grouping agents by specialization
- Separating general-purpose from task-specific agents
- Loading agents from plugin dependencies

#### hooks

**Type**: String (path to JSON file) or Object (inline configuration)
**Default**: `"./hooks/hooks.json"`

Hook configuration location or inline definition.

**File path**:
```json
{
  "hooks": "./config/hooks.json"
}
```

**Inline configuration**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Use cases**:
- Simple plugins: Inline configuration (< 50 lines)
- Complex plugins: External JSON file
- Multiple hook sets: Separate files for different contexts

#### mcpServers

**Type**: String (path to JSON file) or Object (inline configuration)
**Default**: `./.mcp.json`

MCP server configuration location or inline definition.

**File path**:
```json
{
  "mcpServers": "./.mcp.json"
}
```

**Inline configuration**:
```json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/github-mcp.js"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Use cases**:
- Simple plugins: Single inline server (< 20 lines)
- Complex plugins: External `.mcp.json` file
- Multiple servers: Always use external file

## Path Resolution

### Relative Path Rules

All paths in component fields must follow these rules:

1. **Must be relative**: No absolute paths
2. **Must start with `./`**: Indicates relative to plugin root
3. **Cannot use `../`**: No parent directory navigation
4. **Forward slashes only**: Even on Windows

**Examples**:
- ✅ `"./commands"`
- ✅ `"./src/commands"`
- ✅ `"./configs/hooks.json"`
- ❌ `"/Users/name/plugin/commands"`
- ❌ `"commands"` (missing `./`)
- ❌ `"../shared/commands"`
- ❌ `".\\commands"` (backslash)

### Resolution Order

When Claude Code loads components:

1. **Default directories**: Scans standard locations first
   - `./commands/`
   - `./agents/`
   - `./skills/`
   - `./hooks/hooks.json`
   - `./.mcp.json`

2. **Custom paths**: Scans paths specified in manifest
   - Paths from `commands` field
   - Paths from `agents` field
   - Files from `hooks` and `mcpServers` fields

3. **Merge behavior**: Components from all locations load
   - No overwriting
   - All discovered components register
   - Name conflicts cause errors

## Validation

### Manifest Validation

Claude Code validates the manifest on plugin load:

**Syntax validation**:
- Valid JSON format
- No syntax errors
- Correct field types

**Field validation**:
- `name` field present and valid format
- `version` follows semantic versioning (if present)
- Paths are relative with `./` prefix
- URLs are valid (if present)

**Component validation**:
- Referenced paths exist
- Hook and MCP configurations are valid
- No circular dependencies

### Common Validation Errors

**Invalid name format**:
```json
{
  "name": "My Plugin"  // ❌ Contains spaces
}
```
Fix: Use kebab-case
```json
{
  "name": "my-plugin"  // ✅
}
```

**Absolute path**:
```json
{
  "commands": "/Users/name/commands"  // ❌ Absolute path
}
```
Fix: Use relative path
```json
{
  "commands": "./commands"  // ✅
}
```

**Missing ./ prefix**:
```json
{
  "hooks": "hooks/hooks.json"  // ❌ No ./
}
```
Fix: Add ./ prefix
```json
{
  "hooks": "./hooks/hooks.json"  // ✅
}
```

**Invalid version**:
```json
{
  "version": "1.0"  // ❌ Not semantic versioning
}
```
Fix: Use MAJOR.MINOR.PATCH
```json
{
  "version": "1.0.0"  // ✅
}
```

## Minimal vs. Complete Examples

### Minimal Plugin

Bare minimum for a working plugin:

```json
{
  "name": "hello-world"
}
```

Relies entirely on default directory discovery.

### Recommended Plugin

Good metadata for distribution:

```json
{
  "name": "code-review-assistant",
  "version": "1.0.0",
  "description": "Automates code review with style checks and suggestions",
  "author": {
    "name": "Jane Developer",
    "email": "jane@example.com"
  },
  "homepage": "https://docs.example.com/code-review",
  "repository": "https://github.com/janedev/code-review-assistant",
  "license": "MIT",
  "keywords": ["code-review", "automation", "quality", "ci-cd"]
}
```

### Complete Plugin

Full configuration with all features:

```json
{
  "name": "enterprise-devops",
  "version": "2.3.1",
  "description": "Comprehensive DevOps automation for enterprise CI/CD pipelines",
  "author": {
    "name": "DevOps Team",
    "email": "devops@company.com",
    "url": "https://company.com/devops"
  },
  "homepage": "https://docs.company.com/plugins/devops",
  "repository": {
    "type": "git",
    "url": "https://github.com/company/devops-plugin.git"
  },
  "license": "Apache-2.0",
  "keywords": [
    "devops",
    "ci-cd",
    "automation",
    "kubernetes",
    "docker",
    "deployment"
  ],
  "commands": [
    "./commands",
    "./admin-commands"
  ],
  "agents": "./specialized-agents",
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

## Best Practices

### Metadata

1. **Always include version**: Track changes and updates
2. **Write clear descriptions**: Help users understand plugin purpose
3. **Provide contact information**: Enable user support
4. **Link to documentation**: Reduce support burden
5. **Choose appropriate license**: Match project goals

### Paths

1. **Use defaults when possible**: Minimize configuration
2. **Organize logically**: Group related components
3. **Document custom paths**: Explain why non-standard layout used
4. **Test path resolution**: Verify on multiple systems

### Maintenance

1. **Bump version on changes**: Follow semantic versioning
2. **Update keywords**: Reflect new functionality
3. **Keep description current**: Match actual capabilities
4. **Maintain changelog**: Track version history
5. **Update repository links**: Keep URLs current

### Distribution

1. **Complete metadata before publishing**: All fields filled
2. **Test on clean install**: Verify plugin works without dev environment
3. **Validate manifest**: Use validation tools
4. **Include README**: Document installation and usage
5. **Specify license file**: Include LICENSE file in plugin root

---

## Example: advanced plugin

# Advanced Plugin Example

A complex, enterprise-grade plugin with MCP integration and advanced organization.

## Directory Structure

```
enterprise-devops/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── ci/
│   │   ├── build.md
│   │   ├── test.md
│   │   └── deploy.md
│   ├── monitoring/
│   │   ├── status.md
│   │   └── logs.md
│   └── admin/
│       ├── configure.md
│       └── manage.md
├── agents/
│   ├── orchestration/
│   │   ├── deployment-orchestrator.md
│   │   └── rollback-manager.md
│   └── specialized/
│       ├── kubernetes-expert.md
│       ├── terraform-expert.md
│       └── security-auditor.md
├── skills/
│   ├── kubernetes-ops/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── deployment-patterns.md
│   │   │   ├── troubleshooting.md
│   │   │   └── security.md
│   │   ├── examples/
│   │   │   ├── basic-deployment.yaml
│   │   │   ├── stateful-set.yaml
│   │   │   └── ingress-config.yaml
│   │   └── scripts/
│   │       ├── validate-manifest.sh
│   │       └── health-check.sh
│   ├── terraform-iac/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   └── best-practices.md
│   │   └── examples/
│   │       └── module-template/
│   └── ci-cd-pipelines/
│       ├── SKILL.md
│       └── references/
│           └── pipeline-patterns.md
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       ├── security/
│       │   ├── scan-secrets.sh
│       │   ├── validate-permissions.sh
│       │   └── audit-changes.sh
│       ├── quality/
│       │   ├── check-config.sh
│       │   └── verify-tests.sh
│       └── workflow/
│           ├── notify-team.sh
│           └── update-status.sh
├── .mcp.json
├── servers/
│   ├── kubernetes-mcp/
│   │   ├── index.js
│   │   ├── package.json
│   │   └── lib/
│   ├── terraform-mcp/
│   │   ├── main.py
│   │   └── requirements.txt
│   └── github-actions-mcp/
│       ├── server.js
│       └── package.json
├── lib/
│   ├── core/
│   │   ├── logger.js
│   │   ├── config.js
│   │   └── auth.js
│   ├── integrations/
│   │   ├── slack.js
│   │   ├── pagerduty.js
│   │   └── datadog.js
│   └── utils/
│       ├── retry.js
│       └── validation.js
└── config/
    ├── environments/
    │   ├── production.json
    │   ├── staging.json
    │   └── development.json
    └── templates/
        ├── deployment.yaml
        └── service.yaml
```

## File Contents

### .claude-plugin/plugin.json

```json
{
  "name": "enterprise-devops",
  "version": "2.3.1",
  "description": "Comprehensive DevOps automation for enterprise CI/CD pipelines, infrastructure management, and monitoring",
  "author": {
    "name": "DevOps Platform Team",
    "email": "devops-platform@company.com",
    "url": "https://company.com/teams/devops"
  },
  "homepage": "https://docs.company.com/plugins/devops",
  "repository": {
    "type": "git",
    "url": "https://github.com/company/devops-plugin.git"
  },
  "license": "Apache-2.0",
  "keywords": [
    "devops",
    "ci-cd",
    "kubernetes",
    "terraform",
    "automation",
    "infrastructure",
    "deployment",
    "monitoring"
  ],
  "commands": [
    "./commands/ci",
    "./commands/monitoring",
    "./commands/admin"
  ],
  "agents": [
    "./agents/orchestration",
    "./agents/specialized"
  ],
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

### .mcp.json

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/kubernetes-mcp/index.js"],
      "env": {
        "KUBECONFIG": "${KUBECONFIG}",
        "K8S_NAMESPACE": "${K8S_NAMESPACE:-default}"
      }
    },
    "terraform": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/terraform-mcp/main.py"],
      "env": {
        "TF_STATE_BUCKET": "${TF_STATE_BUCKET}",
        "AWS_REGION": "${AWS_REGION}"
      }
    },
    "github-actions": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/github-actions-mcp/server.js"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",
        "GITHUB_ORG": "${GITHUB_ORG}"
      }
    }
  }
}
```

### commands/ci/build.md

```markdown
---
name: build
description: Trigger and monitor CI build pipeline
---

# Build Command

Trigger CI/CD build pipeline and monitor progress in real-time.

## Process

1. **Validation**: Check prerequisites
   - Verify branch status
   - Check for uncommitted changes
   - Validate configuration files

2. **Trigger**: Start build via MCP server
   \`\`\`javascript
   // Uses github-actions MCP server
   const build = await tools.github_actions_trigger_workflow({
     workflow: 'build.yml',
     ref: currentBranch
   })
   \`\`\`

3. **Monitor**: Track build progress
   - Display real-time logs
   - Show test results as they complete
   - Alert on failures

4. **Report**: Summarize results
   - Build status
   - Test coverage
   - Performance metrics
   - Deploy readiness

## Integration

After successful build:
- Offer to deploy to staging
- Suggest performance optimizations
- Generate deployment checklist
```

### agents/orchestration/deployment-orchestrator.md

```markdown
---
description: Orchestrates complex multi-environment deployments with rollback capabilities and health monitoring
capabilities:
  - Plan and execute multi-stage deployments
  - Coordinate service dependencies
  - Monitor deployment health
  - Execute automated rollbacks
  - Manage deployment approvals
---

# Deployment Orchestrator Agent

Specialized agent for orchestrating complex deployments across multiple environments.

## Expertise

- **Deployment strategies**: Blue-green, canary, rolling updates
- **Dependency management**: Service startup ordering, dependency injection
- **Health monitoring**: Service health checks, metric validation
- **Rollback automation**: Automatic rollback on failure detection
- **Approval workflows**: Multi-stage approval processes

## Orchestration Process

1. **Planning Phase**
   - Analyze deployment requirements
   - Identify service dependencies
   - Generate deployment plan
   - Calculate rollback strategy

2. **Validation Phase**
   - Verify environment readiness
   - Check resource availability
   - Validate configurations
   - Run pre-deployment tests

3. **Execution Phase**
   - Deploy services in dependency order
   - Monitor health after each stage
   - Validate metrics and logs
   - Proceed to next stage on success

4. **Verification Phase**
   - Run smoke tests
   - Validate service integration
   - Check performance metrics
   - Confirm deployment success

5. **Rollback Phase** (if needed)
   - Detect failure conditions
   - Execute rollback plan
   - Restore previous state
   - Notify stakeholders

## MCP Integration

Uses multiple MCP servers:
- `kubernetes`: Deploy and manage containers
- `terraform`: Provision infrastructure
- `github-actions`: Trigger deployment pipelines

## Monitoring Integration

Integrates with monitoring tools via lib:
\`\`\`javascript
const { DatadogClient } = require('${CLAUDE_PLUGIN_ROOT}/lib/integrations/datadog')
const metrics = await DatadogClient.getMetrics(service, timeRange)
\`\`\`

## Notification Integration

Sends updates via Slack and PagerDuty:
\`\`\`javascript
const { SlackClient } = require('${CLAUDE_PLUGIN_ROOT}/lib/integrations/slack')
await SlackClient.notify({
  channel: '#deployments',
  message: 'Deployment started',
  metadata: deploymentPlan
})
\`\`\`
```

### skills/kubernetes-ops/SKILL.md

```markdown
---
name: Kubernetes Operations
description: This skill should be used when deploying to Kubernetes, managing K8s resources, troubleshooting cluster issues, configuring ingress/services, scaling deployments, or working with Kubernetes manifests. Provides comprehensive Kubernetes operational knowledge and best practices.
version: 2.0.0
---

# Kubernetes Operations

Comprehensive operational knowledge for managing Kubernetes clusters and workloads.

## Overview

Manage Kubernetes infrastructure effectively through:
- Deployment strategies and patterns
- Resource configuration and optimization
- Troubleshooting and debugging
- Security best practices
- Performance tuning

## Core Concepts

### Resource Management

**Deployments**: Use for stateless applications
- Rolling updates for zero-downtime deployments
- Rollback capabilities for failed deployments
- Replica management for scaling

**StatefulSets**: Use for stateful applications
- Stable network identities
- Persistent storage
- Ordered deployment and scaling

**DaemonSets**: Use for node-level services
- Log collectors
- Monitoring agents
- Network plugins

### Configuration

**ConfigMaps**: Store non-sensitive configuration
- Environment-specific settings
- Application configuration files
- Feature flags

**Secrets**: Store sensitive data
- API keys and tokens
- Database credentials
- TLS certificates

Use external secret management (Vault, AWS Secrets Manager) for production.

### Networking

**Services**: Expose applications internally
- ClusterIP for internal communication
- NodePort for external access (non-production)
- LoadBalancer for external access (production)

**Ingress**: HTTP/HTTPS routing
- Path-based routing
- Host-based routing
- TLS termination
- Load balancing

## Deployment Strategies

### Rolling Update

Default strategy, gradual replacement:
\`\`\`yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
\`\`\`

**When to use**: Standard deployments, minor updates

### Recreate

Stop all pods, then create new ones:
\`\`\`yaml
strategy:
  type: Recreate
\`\`\`

**When to use**: Stateful apps that can't run multiple versions

### Blue-Green

Run two complete environments, switch traffic:
1. Deploy new version (green)
2. Test green environment
3. Switch traffic to green
4. Keep blue for quick rollback

**When to use**: Critical services, need instant rollback

### Canary

Gradually roll out to subset of users:
1. Deploy canary version (10% traffic)
2. Monitor metrics and errors
3. Increase traffic gradually
4. Complete rollout or rollback

**When to use**: High-risk changes, want gradual validation

## Resource Configuration

### Resource Requests and Limits

Always set for production workloads:
\`\`\`yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
\`\`\`

**Requests**: Guaranteed resources
**Limits**: Maximum allowed resources

### Health Checks

Essential for reliability:
\`\`\`yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
\`\`\`

**Liveness**: Restart unhealthy pods
**Readiness**: Remove unready pods from service

## Troubleshooting

### Common Issues

1. **Pods not starting**
   - Check: `kubectl describe pod <name>`
   - Look for: Image pull errors, resource constraints
   - Fix: Verify image name, increase resources

2. **Service not reachable**
   - Check: `kubectl get svc`, `kubectl get endpoints`
   - Look for: No endpoints, wrong selector
   - Fix: Verify pod labels match service selector

3. **High memory usage**
   - Check: `kubectl top pods`
   - Look for: Pods near memory limit
   - Fix: Increase limits, optimize application

4. **Frequent restarts**
   - Check: `kubectl get pods`, `kubectl logs <name>`
   - Look for: Liveness probe failures, OOMKilled
   - Fix: Adjust health checks, increase memory

### Debugging Commands

Get pod details:
\`\`\`bash
kubectl describe pod <name>
kubectl logs <name>
kubectl logs <name> --previous  # logs from crashed container
\`\`\`

Execute commands in pod:
\`\`\`bash
kubectl exec -it <name> -- /bin/sh
kubectl exec <name> -- env
\`\`\`

Check resource usage:
\`\`\`bash
kubectl top nodes
kubectl top pods
\`\`\`

## Security Best Practices

### Pod Security

- Run as non-root user
- Use read-only root filesystem
- Drop unnecessary capabilities
- Use security contexts

Example:
\`\`\`yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL
\`\`\`

### Network Policies

Restrict pod communication:
\`\`\`yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
    - from:
      - podSelector:
          matchLabels:
            app: frontend
\`\`\`

### Secrets Management

- Never commit secrets to git
- Use external secret managers
- Rotate secrets regularly
- Limit secret access with RBAC

## Performance Optimization

### Resource Tuning

1. **Start conservative**: Set low limits initially
2. **Monitor usage**: Track actual resource consumption
3. **Adjust gradually**: Increase based on metrics
4. **Set appropriate requests**: Match typical usage
5. **Set safe limits**: 2x requests for headroom

### Horizontal Pod Autoscaling

Automatically scale based on metrics:
\`\`\`yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
\`\`\`

## MCP Server Integration

This skill works with the kubernetes MCP server for operations:

**List pods**:
\`\`\`javascript
const pods = await tools.k8s_list_pods({ namespace: 'default' })
\`\`\`

**Get pod logs**:
\`\`\`javascript
const logs = await tools.k8s_get_logs({ pod: 'api-xyz', container: 'app' })
\`\`\`

**Apply manifests**:
\`\`\`javascript
const result = await tools.k8s_apply_manifest({ file: 'deployment.yaml' })
\`\`\`

## Detailed References

For in-depth information:
- **Deployment patterns**: `references/deployment-patterns.md`
- **Troubleshooting guide**: `references/troubleshooting.md`
- **Security hardening**: `references/security.md`

## Example Manifests

For copy-paste examples:
- **Basic deployment**: `examples/basic-deployment.yaml`
- **StatefulSet**: `examples/stateful-set.yaml`
- **Ingress config**: `examples/ingress-config.yaml`

## Validation Scripts

For manifest validation:
\`\`\`bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/kubernetes-ops/scripts/validate-manifest.sh deployment.yaml
\`\`\`
```

### hooks/hooks.json

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/security/scan-secrets.sh",
          "timeout": 30
        }
      ]
    },
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Evaluate if this bash command is safe for production environment. Check for destructive operations, missing safeguards, and potential security issues. Commands should be idempotent and reversible.",
          "timeout": 20
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/workflow/update-status.sh",
          "timeout": 15
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": ".*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/quality/check-config.sh",
          "timeout": 45
        },
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/workflow/notify-team.sh",
          "timeout": 30
        }
      ]
    }
  ],
  "SessionStart": [
    {
      "matcher": ".*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/security/validate-permissions.sh",
          "timeout": 20
        }
      ]
    }
  ]
}
```

## Key Features

### Multi-Level Organization

**Commands**: Organized by function (CI, monitoring, admin)
**Agents**: Separated by role (orchestration vs. specialized)
**Skills**: Rich resources (references, examples, scripts)

### MCP Integration

Three custom MCP servers:
- **Kubernetes**: Cluster operations
- **Terraform**: Infrastructure provisioning
- **GitHub Actions**: CI/CD automation

### Shared Libraries

Reusable code in `lib/`:
- **Core**: Common utilities (logging, config, auth)
- **Integrations**: External services (Slack, Datadog)
- **Utils**: Helper functions (retry, validation)

### Configuration Management

Environment-specific configs in `config/`:
- **Environments**: Per-environment settings
- **Templates**: Reusable deployment templates

### Security Automation

Multiple security hooks:
- Secret scanning before writes
- Permission validation on session start
- Configuration auditing on completion

### Monitoring Integration

Built-in monitoring via lib integrations:
- Datadog for metrics
- PagerDuty for alerts
- Slack for notifications

## Use Cases

1. **Multi-environment deployments**: Orchestrated rollouts across dev/staging/prod
2. **Infrastructure as code**: Terraform automation with state management
3. **CI/CD automation**: Build, test, deploy pipelines
4. **Monitoring and observability**: Integrated metrics and alerting
5. **Security enforcement**: Automated security scanning and validation
6. **Team collaboration**: Slack notifications and status updates

## When to Use This Pattern

- Large-scale enterprise deployments
- Multiple environment management
- Complex CI/CD workflows
- Integrated monitoring requirements
- Security-critical infrastructure
- Team collaboration needs

## Scaling Considerations

- **Performance**: Separate MCP servers for parallel operations
- **Organization**: Multi-level directories for scalability
- **Maintainability**: Shared libraries reduce duplication
- **Flexibility**: Environment configs enable customization
- **Security**: Layered security hooks and validation

---

## Example: minimal plugin

# Minimal Plugin Example

A bare-bones plugin with a single command.

## Directory Structure

```
hello-world/
├── .claude-plugin/
│   └── plugin.json
└── commands/
    └── hello.md
```

## File Contents

### .claude-plugin/plugin.json

```json
{
  "name": "hello-world"
}
```

### commands/hello.md

```markdown
---
name: hello
description: Prints a friendly greeting message
---

# Hello Command

Print a friendly greeting to the user.

## Implementation

Output the following message to the user:

> Hello! This is a simple command from the hello-world plugin.
>
> Use this as a starting point for building more complex plugins.

Include the current timestamp in the greeting to show the command executed successfully.
```

## Usage

After installing the plugin:

```
$ claude
> /hello
Hello! This is a simple command from the hello-world plugin.

Use this as a starting point for building more complex plugins.

Executed at: 2025-01-15 14:30:22 UTC
```

## Key Points

1. **Minimal manifest**: Only the required `name` field
2. **Single command**: One markdown file in `commands/` directory
3. **Auto-discovery**: Claude Code finds the command automatically
4. **No dependencies**: No scripts, hooks, or external resources

## When to Use This Pattern

- Quick prototypes
- Single-purpose utilities
- Learning plugin development
- Internal team tools with one specific function

## Extending This Plugin

To add more functionality:

1. **Add commands**: Create more `.md` files in `commands/`
2. **Add metadata**: Update `plugin.json` with version, description, author
3. **Add agents**: Create `agents/` directory with agent definitions
4. **Add hooks**: Create `hooks/hooks.json` for event handling

---

## Example: standard plugin

# Standard Plugin Example

A well-structured plugin with commands, agents, and skills.

## Directory Structure

```
code-quality/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── lint.md
│   ├── test.md
│   └── review.md
├── agents/
│   ├── code-reviewer.md
│   └── test-generator.md
├── skills/
│   ├── code-standards/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── style-guide.md
│   └── testing-patterns/
│       ├── SKILL.md
│       └── examples/
│           ├── unit-test.js
│           └── integration-test.js
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── validate-commit.sh
└── scripts/
    ├── run-linter.sh
    └── generate-report.py
```

## File Contents

### .claude-plugin/plugin.json

```json
{
  "name": "code-quality",
  "version": "1.0.0",
  "description": "Comprehensive code quality tools including linting, testing, and review automation",
  "author": {
    "name": "Quality Team",
    "email": "quality@example.com"
  },
  "homepage": "https://docs.example.com/plugins/code-quality",
  "repository": "https://github.com/example/code-quality-plugin",
  "license": "MIT",
  "keywords": ["code-quality", "linting", "testing", "code-review", "automation"]
}
```

### commands/lint.md

```markdown
---
name: lint
description: Run linting checks on the codebase
---

# Lint Command

Run comprehensive linting checks on the project codebase.

## Process

1. Detect project type and installed linters
2. Run appropriate linters (ESLint, Pylint, RuboCop, etc.)
3. Collect and format results
4. Report issues with file locations and severity

## Implementation

Execute the linting script:

\`\`\`bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/run-linter.sh
\`\`\`

Parse the output and present issues organized by:
- Critical issues (must fix)
- Warnings (should fix)
- Style suggestions (optional)

For each issue, show:
- File path and line number
- Issue description
- Suggested fix (if available)
```

### commands/test.md

```markdown
---
name: test
description: Run test suite with coverage reporting
---

# Test Command

Execute the project test suite and generate coverage reports.

## Process

1. Identify test framework (Jest, pytest, RSpec, etc.)
2. Run all tests
3. Generate coverage report
4. Identify untested code

## Output

Present results in structured format:
- Test summary (passed/failed/skipped)
- Coverage percentage by file
- Critical untested areas
- Failed test details

## Integration

After test completion, offer to:
- Fix failing tests
- Generate tests for untested code (using test-generator agent)
- Update documentation based on test changes
```

### agents/code-reviewer.md

```markdown
---
description: Expert code reviewer specializing in identifying bugs, security issues, and improvement opportunities
capabilities:
  - Analyze code for potential bugs and logic errors
  - Identify security vulnerabilities
  - Suggest performance improvements
  - Ensure code follows project standards
  - Review test coverage adequacy
---

# Code Reviewer Agent

Specialized agent for comprehensive code review.

## Expertise

- **Bug detection**: Logic errors, edge cases, error handling
- **Security analysis**: Injection vulnerabilities, authentication issues, data exposure
- **Performance**: Algorithm efficiency, resource usage, optimization opportunities
- **Standards compliance**: Style guide adherence, naming conventions, documentation
- **Test coverage**: Adequacy of test cases, missing scenarios

## Review Process

1. **Initial scan**: Quick pass for obvious issues
2. **Deep analysis**: Line-by-line review of changed code
3. **Context evaluation**: Check impact on related code
4. **Best practices**: Compare against project and language standards
5. **Recommendations**: Prioritized list of improvements

## Integration with Skills

Automatically loads `code-standards` skill for project-specific guidelines.

## Output Format

For each file reviewed:
- Overall assessment
- Critical issues (must fix before merge)
- Important issues (should fix)
- Suggestions (nice to have)
- Positive feedback (what was done well)
```

### agents/test-generator.md

```markdown
---
description: Generates comprehensive test suites from code analysis
capabilities:
  - Analyze code structure and logic flow
  - Generate unit tests for functions and methods
  - Create integration tests for modules
  - Design edge case and error condition tests
  - Suggest test fixtures and mocks
---

# Test Generator Agent

Specialized agent for generating comprehensive test suites.

## Expertise

- **Unit testing**: Individual function/method tests
- **Integration testing**: Module interaction tests
- **Edge cases**: Boundary conditions, error paths
- **Test organization**: Proper test structure and naming
- **Mocking**: Appropriate use of mocks and stubs

## Generation Process

1. **Code analysis**: Understand function purpose and logic
2. **Path identification**: Map all execution paths
3. **Input design**: Create test inputs covering all paths
4. **Assertion design**: Define expected outputs
5. **Test generation**: Write tests in project's framework

## Integration with Skills

Automatically loads `testing-patterns` skill for project-specific test conventions.

## Test Quality

Generated tests include:
- Happy path scenarios
- Edge cases and boundary conditions
- Error handling verification
- Mock data for external dependencies
- Clear test descriptions
```

### skills/code-standards/SKILL.md

```markdown
---
name: Code Standards
description: This skill should be used when reviewing code, enforcing style guidelines, checking naming conventions, or ensuring code quality standards. Provides project-specific coding standards and best practices.
version: 1.0.0
---

# Code Standards

Comprehensive coding standards and best practices for maintaining code quality.

## Overview

Enforce consistent code quality through standardized conventions for:
- Code style and formatting
- Naming conventions
- Documentation requirements
- Error handling patterns
- Security practices

## Style Guidelines

### Formatting

- **Indentation**: 2 spaces (JavaScript/TypeScript), 4 spaces (Python)
- **Line length**: Maximum 100 characters
- **Braces**: Same line for opening brace (K&R style)
- **Whitespace**: Space after commas, around operators

### Naming Conventions

- **Variables**: camelCase for JavaScript, snake_case for Python
- **Functions**: camelCase, descriptive verb-noun pairs
- **Classes**: PascalCase
- **Constants**: UPPER_SNAKE_CASE
- **Files**: kebab-case for modules

## Documentation Requirements

### Function Documentation

Every function must include:
- Purpose description
- Parameter descriptions with types
- Return value description with type
- Example usage (for public functions)

### Module Documentation

Every module must include:
- Module purpose
- Public API overview
- Usage examples
- Dependencies

## Error Handling

### Required Practices

- Never swallow errors silently
- Always log errors with context
- Use specific error types
- Provide actionable error messages
- Clean up resources in finally blocks

### Example Pattern

\`\`\`javascript
async function processData(data) {
  try {
    const result = await transform(data)
    return result
  } catch (error) {
    logger.error('Data processing failed', {
      data: sanitize(data),
      error: error.message,
      stack: error.stack
    })
    throw new DataProcessingError('Failed to process data', { cause: error })
  }
}
\`\`\`

## Security Practices

- Validate all external input
- Sanitize data before output
- Use parameterized queries
- Never log sensitive information
- Keep dependencies updated

## Detailed Guidelines

For comprehensive style guides by language, see:
- `references/style-guide.md`
```

### skills/code-standards/references/style-guide.md

```markdown
# Comprehensive Style Guide

Detailed style guidelines for all supported languages.

## JavaScript/TypeScript

### Variable Declarations

Use `const` by default, `let` when reassignment needed, never `var`:

\`\`\`javascript
// Good
const MAX_RETRIES = 3
let currentTry = 0

// Bad
var MAX_RETRIES = 3
\`\`\`

### Function Declarations

Use function expressions for consistency:

\`\`\`javascript
// Good
const calculateTotal = (items) => {
  return items.reduce((sum, item) => sum + item.price, 0)
}

// Bad (inconsistent style)
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0)
}
\`\`\`

### Async/Await

Prefer async/await over promise chains:

\`\`\`javascript
// Good
async function fetchUserData(userId) {
  const user = await db.getUser(userId)
  const orders = await db.getOrders(user.id)
  return { user, orders }
}

// Bad
function fetchUserData(userId) {
  return db.getUser(userId)
    .then(user => db.getOrders(user.id)
      .then(orders => ({ user, orders })))
}
\`\`\`

## Python

### Import Organization

Order imports: standard library, third-party, local:

\`\`\`python
# Good
import os
import sys

import numpy as np
import pandas as pd

from app.models import User
from app.utils import helper

# Bad - mixed order
from app.models import User
import numpy as np
import os
\`\`\`

### Type Hints

Use type hints for all function signatures:

\`\`\`python
# Good
def calculate_average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

# Bad
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
\`\`\`

## Additional Languages

See language-specific guides for:
- Go: `references/go-style.md`
- Rust: `references/rust-style.md`
- Ruby: `references/ruby-style.md`
```

### hooks/hooks.json

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Before modifying code, verify it meets our coding standards from the code-standards skill. Check formatting, naming conventions, and documentation. If standards aren't met, suggest improvements.",
          "timeout": 30
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": ".*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate-commit.sh",
          "timeout": 45
        }
      ]
    }
  ]
}
```

### hooks/scripts/validate-commit.sh

```bash
#!/bin/bash
# Validate code quality before task completion

set -e

# Check if there are any uncommitted changes
if [[ -z $(git status -s) ]]; then
  echo '{"systemMessage": "No changes to validate. Task complete."}'
  exit 0
fi

# Run linter on changed files
CHANGED_FILES=$(git diff --name-only --cached | grep -E '\.(js|ts|py)$' || true)

if [[ -z "$CHANGED_FILES" ]]; then
  echo '{"systemMessage": "No code files changed. Validation passed."}'
  exit 0
fi

# Run appropriate linters
ISSUES=0

for file in $CHANGED_FILES; do
  case "$file" in
    *.js|*.ts)
      if ! npx eslint "$file" --quiet; then
        ISSUES=$((ISSUES + 1))
      fi
      ;;
    *.py)
      if ! python -m pylint "$file" --errors-only; then
        ISSUES=$((ISSUES + 1))
      fi
      ;;
  esac
done

if [[ $ISSUES -gt 0 ]]; then
  echo "{\"systemMessage\": \"Found $ISSUES code quality issues. Please fix before completing.\"}"
  exit 1
fi

echo '{"systemMessage": "Code quality checks passed. Ready to commit."}'
exit 0
```

## Usage Examples

### Running Commands

```
$ claude
> /lint
Running linter checks...

Critical Issues (2):
  src/api/users.js:45 - SQL injection vulnerability
  src/utils/helpers.js:12 - Unhandled promise rejection

Warnings (5):
  src/components/Button.tsx:23 - Missing PropTypes
  ...

Style Suggestions (8):
  src/index.js:1 - Use const instead of let
  ...

> /test
Running test suite...

Test Results:
  ✓ 245 passed
  ✗ 3 failed
  ○ 2 skipped

Coverage: 87.3%

Untested Files:
  src/utils/cache.js - 0% coverage
  src/api/webhooks.js - 23% coverage

Failed Tests:
  1. User API › GET /users › should handle pagination
     Expected 200, received 500
  ...
```

### Using Agents

```
> Review the changes in src/api/users.js

[code-reviewer agent selected automatically]

Code Review: src/api/users.js

Critical Issues:
  1. Line 45: SQL injection vulnerability
     - Using string concatenation for SQL query
     - Replace with parameterized query
     - Priority: CRITICAL

  2. Line 67: Missing error handling
     - Database query without try/catch
     - Could crash server on DB error
     - Priority: HIGH

Suggestions:
  1. Line 23: Consider caching user data
     - Frequent DB queries for same users
     - Add Redis caching layer
     - Priority: MEDIUM
```

## Key Points

1. **Complete manifest**: All recommended metadata fields
2. **Multiple components**: Commands, agents, skills, hooks
3. **Rich skills**: References and examples for detailed information
4. **Automation**: Hooks enforce standards automatically
5. **Integration**: Components work together cohesively

## When to Use This Pattern

- Production plugins for distribution
- Team collaboration tools
- Plugins requiring consistency enforcement
- Complex workflows with multiple entry points
