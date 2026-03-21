---
title: "Plugin Settings"
description: "使用 .local.md 文件存储插件配置和状态的模式指南"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["plugin", "settings", "configuration", "state"]
date: 2026-03-20
---


# Plugin Settings Pattern for Claude Code Plugins

## Overview

Plugins can store user-configurable settings and state in `.claude/plugin-name.local.md` files within the project directory. This pattern uses YAML frontmatter for structured configuration and markdown content for prompts or additional context.

**Key characteristics:**
- File location: `.claude/plugin-name.local.md` in project root
- Structure: YAML frontmatter + markdown body
- Purpose: Per-project plugin configuration and state
- Usage: Read from hooks, commands, and agents
- Lifecycle: User-managed (not in git, should be in `.gitignore`)

## File Structure

### Basic Template

```markdown
---
enabled: true
setting1: value1
setting2: value2
numeric_setting: 42
list_setting: ["item1", "item2"]
---

# Additional Context

This markdown body can contain:
- Task descriptions
- Additional instructions
- Prompts to feed back to Claude
- Documentation or notes
```

### Example: Plugin State File

**.claude/my-plugin.local.md:**
```markdown
---
enabled: true
strict_mode: false
max_retries: 3
notification_level: info
coordinator_session: team-leader
---

# Plugin Configuration

This plugin is configured for standard validation mode.
Contact @team-lead with questions.
```

## Reading Settings Files

### From Hooks (Bash Scripts)

**Pattern: Check existence and parse frontmatter**

```bash
#!/bin/bash
set -euo pipefail

# Define state file path
STATE_FILE=".claude/my-plugin.local.md"

# Quick exit if file doesn't exist
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # Plugin not configured, skip
fi

# Parse YAML frontmatter (between --- markers)
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")

# Extract individual fields
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//' | sed 's/^"\(.*\)"$/\1/')
STRICT_MODE=$(echo "$FRONTMATTER" | grep '^strict_mode:' | sed 's/strict_mode: *//' | sed 's/^"\(.*\)"$/\1/')

# Check if enabled
if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi

# Use configuration in hook logic
if [[ "$STRICT_MODE" == "true" ]]; then
  # Apply strict validation
  # ...
fi
```

See `examples/read-settings-hook.sh` for complete working example.

### From Commands

Commands can read settings files to customize behavior:

```markdown
---
description: Process data with plugin
allowed-tools: ["Read", "Bash"]
---

# Process Command

Steps:
1. Check if settings exist at `.claude/my-plugin.local.md`
2. Read configuration using Read tool
3. Parse YAML frontmatter to extract settings
4. Apply settings to processing logic
5. Execute with configured behavior
```

### From Agents

Agents can reference settings in their instructions:

```markdown
---
name: configured-agent
description: Agent that adapts to project settings
---

Check for plugin settings at `.claude/my-plugin.local.md`.
If present, parse YAML frontmatter and adapt behavior according to:
- enabled: Whether plugin is active
- mode: Processing mode (strict, standard, lenient)
- Additional configuration fields
```

## Parsing Techniques

### Extract Frontmatter

```bash
# Extract everything between --- markers
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
```

### Read Individual Fields

**String fields:**
```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//' | sed 's/^"\(.*\)"$/\1/')
```

**Boolean fields:**
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
# Compare: if [[ "$ENABLED" == "true" ]]; then
```

**Numeric fields:**
```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')
# Use: if [[ $MAX -gt 100 ]]; then
```

### Read Markdown Body

Extract content after second `---`:

```bash
# Get everything after closing ---
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

## Common Patterns

### Pattern 1: Temporarily Active Hooks

Use settings file to control hook activation:

```bash
#!/bin/bash
STATE_FILE=".claude/security-scan.local.md"

# Quick exit if not configured
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# Read enabled flag
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi

# Run hook logic
# ...
```

**Use case:** Enable/disable hooks without editing hooks.json (requires restart).

### Pattern 2: Agent State Management

Store agent-specific state and configuration:

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-agent
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
---

# Task Assignment

Implement JWT authentication for the API.

**Success Criteria:**
- Authentication endpoints created
- Tests passing
- PR created and CI green
```

Read from hooks to coordinate agents:

```bash
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//')
COORDINATOR=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//')

# Send notification to coordinator
tmux send-keys -t "$COORDINATOR" "Agent $AGENT_NAME completed task" Enter
```

### Pattern 3: Configuration-Driven Behavior

**.claude/my-plugin.local.md:**
```markdown
---
validation_level: strict
max_file_size: 1000000
allowed_extensions: [".js", ".ts", ".tsx"]
enable_logging: true
---

# Validation Configuration

Strict mode enabled for this project.
All writes validated against security policies.
```

Use in hooks or commands:

```bash
LEVEL=$(echo "$FRONTMATTER" | grep '^validation_level:' | sed 's/validation_level: *//')

case "$LEVEL" in
  strict)
    # Apply strict validation
    ;;
  standard)
    # Apply standard validation
    ;;
  lenient)
    # Apply lenient validation
    ;;
esac
```

## Creating Settings Files

### From Commands

Commands can create settings files:

```markdown
# Setup Command

Steps:
1. Ask user for configuration preferences
2. Create `.claude/my-plugin.local.md` with YAML frontmatter
3. Set appropriate values based on user input
4. Inform user that settings are saved
5. Remind user to restart Claude Code for hooks to recognize changes
```

### Template Generation

Provide template in plugin README:

```markdown
## Configuration

Create `.claude/my-plugin.local.md` in your project:

\`\`\`markdown
---
enabled: true
mode: standard
max_retries: 3
---

# Plugin Configuration

Your settings are active.
\`\`\`

After creating or editing, restart Claude Code for changes to take effect.
```

## Best Practices

### File Naming

✅ **DO:**
- Use `.claude/plugin-name.local.md` format
- Match plugin name exactly
- Use `.local.md` suffix for user-local files

❌ **DON'T:**
- Use different directory (not `.claude/`)
- Use inconsistent naming
- Use `.md` without `.local` (might be committed)

### Gitignore

Always add to `.gitignore`:

```gitignore
.claude/*.local.md
.claude/*.local.json
```

Document this in plugin README.

### Defaults

Provide sensible defaults when settings file doesn't exist:

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  # Use defaults
  ENABLED=true
  MODE=standard
else
  # Read from file
  # ...
fi
```

### Validation

Validate settings values:

```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')

# Validate numeric range
if ! [[ "$MAX" =~ ^[0-9]+$ ]] || [[ $MAX -lt 1 ]] || [[ $MAX -gt 100 ]]; then
  echo "⚠️  Invalid max_value in settings (must be 1-100)" >&2
  MAX=10  # Use default
fi
```

### Restart Requirement

**Important:** Settings changes require Claude Code restart.

Document in your README:

```markdown
## Changing Settings

After editing `.claude/my-plugin.local.md`:
1. Save the file
2. Exit Claude Code
3. Restart: `claude` or `cc`
4. New settings will be loaded
```

Hooks cannot be hot-swapped within a session.

## Security Considerations

### Sanitize User Input

When writing settings files from user input:

```bash
# Escape quotes in user input
SAFE_VALUE=$(echo "$USER_INPUT" | sed 's/"/\\"/g')

# Write to file
cat > "$STATE_FILE" <<EOF
---
user_setting: "$SAFE_VALUE"
---
EOF
```

### Validate File Paths

If settings contain file paths:

```bash
FILE_PATH=$(echo "$FRONTMATTER" | grep '^data_file:' | sed 's/data_file: *//')

# Check for path traversal
if [[ "$FILE_PATH" == *".."* ]]; then
  echo "⚠️  Invalid path in settings (path traversal)" >&2
  exit 2
fi
```

### Permissions

Settings files should be:
- Readable by user only (`chmod 600`)
- Not committed to git
- Not shared between users

## Real-World Examples

### multi-agent-swarm Plugin

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: Use JWT tokens, not sessions
---

# Task: Implement Authentication

Build JWT-based authentication for the REST API.
Coordinate with auth-agent on shared types.
```

**Hook usage (agent-stop-notification.sh):**
- Checks if file exists (line 15-18: quick exit if not)
- Parses frontmatter to get coordinator_session, agent_name, enabled
- Sends notifications to coordinator if enabled
- Allows quick activation/deactivation via `enabled: true/false`

### ralph-wiggum Plugin

**.claude/ralph-loop.local.md:**
```markdown
---
iteration: 1
max_iterations: 10
completion_promise: "All tests passing and build successful"
---

Fix all the linting errors in the project.
Make sure tests pass after each fix.
```

**Hook usage (stop-hook.sh):**
- Checks if file exists (line 15-18: quick exit if not active)
- Reads iteration count and max_iterations
- Extracts completion_promise for loop termination
- Reads body as the prompt to feed back
- Updates iteration count on each loop

## Quick Reference

### File Location

```
project-root/
└── .claude/
    └── plugin-name.local.md
```

### Frontmatter Parsing

```bash
# Extract frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# Read field
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/')
```

### Body Parsing

```bash
# Extract body (after second ---)
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

### Quick Exit Pattern

```bash
if [[ ! -f ".claude/my-plugin.local.md" ]]; then
  exit 0  # Not configured
fi
```

## Additional Resources

### Reference Files

For detailed implementation patterns:

- **`references/parsing-techniques.md`** - Complete guide to parsing YAML frontmatter and markdown bodies
- **`references/real-world-examples.md`** - Deep dive into multi-agent-swarm and ralph-wiggum implementations

### Example Files

Working examples in `examples/`:

- **`read-settings-hook.sh`** - Hook that reads and uses settings
- **`create-settings-command.md`** - Command that creates settings file
- **`example-settings.md`** - Template settings file

### Utility Scripts

Development tools in `scripts/`:

- **`validate-settings.sh`** - Validate settings file structure
- **`parse-frontmatter.sh`** - Extract frontmatter fields

## Implementation Workflow

To add settings to a plugin:

1. Design settings schema (which fields, types, defaults)
2. Create template file in plugin documentation
3. Add gitignore entry for `.claude/*.local.md`
4. Implement settings parsing in hooks/commands
5. Use quick-exit pattern (check file exists, check enabled field)
6. Document settings in plugin README with template
7. Remind users that changes require Claude Code restart

Focus on keeping settings simple and providing good defaults when settings file doesn't exist.


---

## Reference: parsing techniques


# Markdown Content

This body content can be extracted separately.
It's useful for prompts, documentation, or additional context.
```

## Parsing Frontmatter

### Extract Frontmatter Block

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"

# Extract everything between --- markers (excluding the markers themselves)
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
```

**How it works:**
- `sed -n` - Suppress automatic printing
- `/^---$/,/^---$/` - Range from first `---` to second `---`
- `{ /^---$/d; p; }` - Delete the `---` lines, print everything else

### Extract Individual Fields

**String fields:**
```bash
# Simple value
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//')

# Quoted value (removes surrounding quotes)
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//' | sed 's/^"\(.*\)"$/\1/')
```

**Boolean fields:**
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# Use in condition
if [[ "$ENABLED" == "true" ]]; then
  # Enabled
fi
```

**Numeric fields:**
```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')

# Validate it's a number
if [[ "$MAX" =~ ^[0-9]+$ ]]; then
  # Use in numeric comparison
  if [[ $MAX -gt 100 ]]; then
    # Too large
  fi
fi
```

**List fields (simple):**
```bash
# YAML: list: ["item1", "item2", "item3"]
LIST=$(echo "$FRONTMATTER" | grep '^list:' | sed 's/list: *//')
# Result: ["item1", "item2", "item3"]

# For simple checks:
if [[ "$LIST" == *"item1"* ]]; then
  # List contains item1
fi
```

**List fields (proper parsing with jq):**
```bash
# For proper list handling, use yq or convert to JSON
# This requires yq to be installed (brew install yq)

# Extract list as JSON array
LIST=$(echo "$FRONTMATTER" | yq -o json '.list' 2>/dev/null)

# Iterate over items
echo "$LIST" | jq -r '.[]' | while read -r item; do
  echo "Processing: $item"
done
```

## Parsing Markdown Body

### Extract Body Content

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"

# Extract everything after the closing ---
# Counts --- markers: first is opening, second is closing, everything after is body
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

**How it works:**
- `/^---$/` - Match `---` lines
- `{i++; next}` - Increment counter and skip the `---` line
- `i>=2` - Print all lines after second `---`

**Handles edge case:** If `---` appears in the markdown body, it still works because we only count the first two `---` at the start.

### Use Body as Prompt

```bash
# Extract body
PROMPT=$(awk '/^---$/{i++; next} i>=2' "$RALPH_STATE_FILE")

# Feed back to Claude
echo '{"decision": "block", "reason": "'"$PROMPT"'"}' | jq .
```

**Important:** Use `jq -n --arg` for safer JSON construction with user content:

```bash
PROMPT=$(awk '/^---$/{i++; next} i>=2' "$FILE")

# Safe JSON construction
jq -n --arg prompt "$PROMPT" '{
  "decision": "block",
  "reason": $prompt
}'
```

## Common Parsing Patterns

### Pattern: Field with Default

```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/')

# Use default if empty
if [[ -z "$VALUE" ]]; then
  VALUE="default_value"
fi
```

### Pattern: Optional Field

```bash
OPTIONAL=$(echo "$FRONTMATTER" | grep '^optional_field:' | sed 's/optional_field: *//' | sed 's/^"\(.*\)"$/\1/')

# Only use if present
if [[ -n "$OPTIONAL" ]] && [[ "$OPTIONAL" != "null" ]]; then
  # Field is set, use it
  echo "Optional field: $OPTIONAL"
fi
```

### Pattern: Multiple Fields at Once

```bash
# Parse all fields in one pass
while IFS=': ' read -r key value; do
  # Remove quotes if present
  value=$(echo "$value" | sed 's/^"\(.*\)"$/\1/')

  case "$key" in
    enabled)
      ENABLED="$value"
      ;;
    mode)
      MODE="$value"
      ;;
    max_size)
      MAX_SIZE="$value"
      ;;
  esac
done <<< "$FRONTMATTER"
```

## Updating Settings Files

### Atomic Updates

Always use temp file + atomic move to prevent corruption:

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"
NEW_VALUE="updated_value"

# Create temp file
TEMP_FILE="${FILE}.tmp.$$"

# Update field using sed
sed "s/^field_name: .*/field_name: $NEW_VALUE/" "$FILE" > "$TEMP_FILE"

# Atomic replace
mv "$TEMP_FILE" "$FILE"
```

### Update Single Field

```bash
# Increment iteration counter
CURRENT=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
NEXT=$((CURRENT + 1))

# Update file
TEMP_FILE="${FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

### Update Multiple Fields

```bash
# Update several fields at once
TEMP_FILE="${FILE}.tmp.$$"

sed -e "s/^iteration: .*/iteration: $NEXT_ITERATION/" \
    -e "s/^pr_number: .*/pr_number: $PR_NUMBER/" \
    -e "s/^status: .*/status: $NEW_STATUS/" \
    "$FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$FILE"
```

## Validation Techniques

### Validate File Exists and Is Readable

```bash
FILE=".claude/my-plugin.local.md"

if [[ ! -f "$FILE" ]]; then
  echo "Settings file not found" >&2
  exit 1
fi

if [[ ! -r "$FILE" ]]; then
  echo "Settings file not readable" >&2
  exit 1
fi
```

### Validate Frontmatter Structure

```bash
# Count --- markers (should be exactly 2 at start)
MARKER_COUNT=$(grep -c '^---$' "$FILE" 2>/dev/null || echo "0")

if [[ $MARKER_COUNT -lt 2 ]]; then
  echo "Invalid settings file: missing frontmatter markers" >&2
  exit 1
fi
```

### Validate Field Values

```bash
MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//')

case "$MODE" in
  strict|standard|lenient)
    # Valid mode
    ;;
  *)
    echo "Invalid mode: $MODE (must be strict, standard, or lenient)" >&2
    exit 1
    ;;
esac
```

### Validate Numeric Ranges

```bash
MAX_SIZE=$(echo "$FRONTMATTER" | grep '^max_size:' | sed 's/max_size: *//')

if ! [[ "$MAX_SIZE" =~ ^[0-9]+$ ]]; then
  echo "max_size must be a number" >&2
  exit 1
fi

if [[ $MAX_SIZE -lt 1 ]] || [[ $MAX_SIZE -gt 10000000 ]]; then
  echo "max_size out of range (1-10000000)" >&2
  exit 1
fi
```

## Edge Cases and Gotchas

### Quotes in Values

YAML allows both quoted and unquoted strings:

```yaml
# These are equivalent:
field1: value
field2: "value"
field3: 'value'
```

**Handle both:**
```bash
# Remove surrounding quotes if present
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\\(.*\\)'$/\\1/")
```

### --- in Markdown Body

If the markdown body contains `---`, the parsing still works because we only match the first two:

```markdown
---
field: value
---

# Body

Here's a separator:
---

More content after the separator.
```

The `awk '/^---$/{i++; next} i>=2'` pattern handles this correctly.

### Empty Values

Handle missing or empty fields:

```yaml
field1:
field2: ""
field3: null
```

**Parsing:**
```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field1:' | sed 's/field1: *//')
# VALUE will be empty string

# Check for empty/null
if [[ -z "$VALUE" ]] || [[ "$VALUE" == "null" ]]; then
  VALUE="default"
fi
```

### Special Characters

Values with special characters need careful handling:

```yaml
message: "Error: Something went wrong!"
path: "/path/with spaces/file.txt"
regex: "^[a-zA-Z0-9_]+$"
```

**Safe parsing:**
```bash
# Always quote variables when using
MESSAGE=$(echo "$FRONTMATTER" | grep '^message:' | sed 's/message: *//' | sed 's/^"\(.*\)"$/\1/')

echo "Message: $MESSAGE"  # Quoted!
```

## Performance Optimization

### Cache Parsed Values

If reading settings multiple times:

```bash
# Parse once
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# Extract multiple fields from cached frontmatter
FIELD1=$(echo "$FRONTMATTER" | grep '^field1:' | sed 's/field1: *//')
FIELD2=$(echo "$FRONTMATTER" | grep '^field2:' | sed 's/field2: *//')
FIELD3=$(echo "$FRONTMATTER" | grep '^field3:' | sed 's/field3: *//')
```

**Don't:** Re-parse file for each field.

### Lazy Loading

Only parse settings when needed:

```bash
#!/bin/bash
input=$(cat)

# Quick checks first (no file I/O)
tool_name=$(echo "$input" | jq -r '.tool_name')
if [[ "$tool_name" != "Write" ]]; then
  exit 0  # Not a write operation, skip
fi

# Only now check settings file
if [[ -f ".claude/my-plugin.local.md" ]]; then
  # Parse settings
  # ...
fi
```

## Debugging

### Print Parsed Values

```bash
#!/bin/bash
set -x  # Enable debug tracing

FILE=".claude/my-plugin.local.md"

if [[ -f "$FILE" ]]; then
  echo "Settings file found" >&2

  FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
  echo "Frontmatter:" >&2
  echo "$FRONTMATTER" >&2

  ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
  echo "Enabled: $ENABLED" >&2
fi
```

### Validate Parsing

```bash
# Show what was parsed
echo "Parsed values:" >&2
echo "  enabled: $ENABLED" >&2
echo "  mode: $MODE" >&2
echo "  max_size: $MAX_SIZE" >&2

# Verify expected values
if [[ "$ENABLED" != "true" ]] && [[ "$ENABLED" != "false" ]]; then
  echo "⚠️  Unexpected enabled value: $ENABLED" >&2
fi
```

## Alternative: Using yq

For complex YAML, consider using `yq`:

```bash
# Install: brew install yq

# Parse YAML properly
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# Extract fields with yq
ENABLED=$(echo "$FRONTMATTER" | yq '.enabled')
MODE=$(echo "$FRONTMATTER" | yq '.mode')
LIST=$(echo "$FRONTMATTER" | yq -o json '.list_field')

# Iterate list properly
echo "$LIST" | jq -r '.[]' | while read -r item; do
  echo "Item: $item"
done
```

**Pros:**
- Proper YAML parsing
- Handles complex structures
- Better list/object support

**Cons:**
- Requires yq installation
- Additional dependency
- May not be available on all systems

**Recommendation:** Use sed/grep for simple fields, yq for complex structures.

## Complete Example

```bash
#!/bin/bash
set -euo pipefail

# Configuration
SETTINGS_FILE=".claude/my-plugin.local.md"

# Quick exit if not configured
if [[ ! -f "$SETTINGS_FILE" ]]; then
  # Use defaults
  ENABLED=true
  MODE=standard
  MAX_SIZE=1000000
else
  # Parse frontmatter
  FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$SETTINGS_FILE")

  # Extract fields with defaults
  ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
  ENABLED=${ENABLED:-true}

  MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//' | sed 's/^"\(.*\)"$/\1/')
  MODE=${MODE:-standard}

  MAX_SIZE=$(echo "$FRONTMATTER" | grep '^max_size:' | sed 's/max_size: *//')
  MAX_SIZE=${MAX_SIZE:-1000000}

  # Validate values
  if [[ "$ENABLED" != "true" ]] && [[ "$ENABLED" != "false" ]]; then
    echo "⚠️  Invalid enabled value, using default" >&2
    ENABLED=true
  fi

  if ! [[ "$MAX_SIZE" =~ ^[0-9]+$ ]]; then
    echo "⚠️  Invalid max_size, using default" >&2
    MAX_SIZE=1000000
  fi
fi

# Quick exit if disabled
if [[ "$ENABLED" != "true" ]]; then
  exit 0
fi

# Use configuration
echo "Configuration loaded: mode=$MODE, max_size=$MAX_SIZE" >&2

# Apply logic based on settings
case "$MODE" in
  strict)
    # Strict validation
    ;;
  standard)
    # Standard validation
    ;;
  lenient)
    # Lenient validation
    ;;
esac
```

This provides robust settings handling with defaults, validation, and error recovery.

---

## Reference: real world examples


# Task: Implement Authentication

Build JWT-based authentication for the REST API.

## Requirements
- JWT token generation and validation
- Refresh token flow
- Secure password hashing

## Success Criteria
- Auth endpoints implemented
- Tests passing (100% coverage)
- PR created and CI green
- Documentation updated

## Coordination
Depends on Task 3.4 (user model).
Report status to 'team-leader' session.
```

### How It's Used

**File:** `hooks/agent-stop-notification.sh`

**Purpose:** Send notifications to coordinator when agent becomes idle

**Implementation:**

```bash
#!/bin/bash
set -euo pipefail

SWARM_STATE_FILE=".claude/multi-agent-swarm.local.md"

# Quick exit if no swarm active
if [[ ! -f "$SWARM_STATE_FILE" ]]; then
  exit 0
fi

# Parse frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$SWARM_STATE_FILE")

# Extract configuration
COORDINATOR_SESSION=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//' | sed 's/^"\(.*\)"$/\1/')
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//' | sed 's/^"\(.*\)"$/\1/')
TASK_NUMBER=$(echo "$FRONTMATTER" | grep '^task_number:' | sed 's/task_number: *//' | sed 's/^"\(.*\)"$/\1/')
PR_NUMBER=$(echo "$FRONTMATTER" | grep '^pr_number:' | sed 's/pr_number: *//' | sed 's/^"\(.*\)"$/\1/')
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# Check if enabled
if [[ "$ENABLED" != "true" ]]; then
  exit 0
fi

# Send notification to coordinator
NOTIFICATION="🤖 Agent ${AGENT_NAME} (Task ${TASK_NUMBER}, PR #${PR_NUMBER}) is idle."

if tmux has-session -t "$COORDINATOR_SESSION" 2>/dev/null; then
  tmux send-keys -t "$COORDINATOR_SESSION" "$NOTIFICATION" Enter
  sleep 0.5
  tmux send-keys -t "$COORDINATOR_SESSION" Enter
fi

exit 0
```

**Key patterns:**
1. **Quick exit** (line 7-9): Returns immediately if file doesn't exist
2. **Field extraction** (lines 11-17): Parses each frontmatter field
3. **Enabled check** (lines 19-21): Respects enabled flag
4. **Action based on settings** (lines 23-29): Uses coordinator_session to send notification

### Creation

**File:** `commands/launch-swarm.md`

Settings files are created during swarm launch with:

```bash
cat > "$WORKTREE_PATH/.claude/multi-agent-swarm.local.md" <<EOF
---
agent_name: $AGENT_NAME
task_number: $TASK_ID
pr_number: TBD
coordinator_session: $COORDINATOR_SESSION
enabled: true
dependencies: [$DEPENDENCIES]
additional_instructions: "$EXTRA_INSTRUCTIONS"
---

# Task: $TASK_DESCRIPTION

$TASK_DETAILS
EOF
```

### Updates

PR number updated after PR creation:

```bash
# Update pr_number field
sed "s/^pr_number: .*/pr_number: $PR_NUM/" \
  ".claude/multi-agent-swarm.local.md" > temp.md
mv temp.md ".claude/multi-agent-swarm.local.md"
```

## ralph-wiggum Plugin

### Settings File Structure

**.claude/ralph-loop.local.md:**

```markdown
---
iteration: 1
max_iterations: 10
completion_promise: "All tests passing and build successful"
started_at: "2025-01-15T14:30:00Z"
---

Fix all the linting errors in the project.
Make sure tests pass after each fix.
Document any changes needed in CLAUDE.md.
```

### How It's Used

**File:** `hooks/stop-hook.sh`

**Purpose:** Prevent session exit and loop Claude's output back as input

**Implementation:**

```bash
#!/bin/bash
set -euo pipefail

RALPH_STATE_FILE=".claude/ralph-loop.local.md"

# Quick exit if no active loop
if [[ ! -f "$RALPH_STATE_FILE" ]]; then
  exit 0
fi

# Parse frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$RALPH_STATE_FILE")

# Extract configuration
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
COMPLETION_PROMISE=$(echo "$FRONTMATTER" | grep '^completion_promise:' | sed 's/completion_promise: *//' | sed 's/^"\(.*\)"$/\1/')

# Check max iterations
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "🛑 Ralph loop: Max iterations ($MAX_ITERATIONS) reached."
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# Get transcript and check for completion promise
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path')
LAST_OUTPUT=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1 | jq -r '.message.content | map(select(.type == "text")) | map(.text) | join("\n")')

# Check for completion
if [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$COMPLETION_PROMISE" ]]; then
  PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g')

  if [[ "$PROMISE_TEXT" = "$COMPLETION_PROMISE" ]]; then
    echo "✅ Ralph loop: Detected completion"
    rm "$RALPH_STATE_FILE"
    exit 0
  fi
fi

# Continue loop - increment iteration
NEXT_ITERATION=$((ITERATION + 1))

# Extract prompt from markdown body
PROMPT_TEXT=$(awk '/^---$/{i++; next} i>=2' "$RALPH_STATE_FILE")

# Update iteration counter
TEMP_FILE="${RALPH_STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$RALPH_STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$RALPH_STATE_FILE"

# Block exit and feed prompt back
jq -n \
  --arg prompt "$PROMPT_TEXT" \
  --arg msg "🔄 Ralph iteration $NEXT_ITERATION" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
```

**Key patterns:**
1. **Quick exit** (line 7-9): Skip if not active
2. **Iteration tracking** (lines 11-20): Count and enforce max iterations
3. **Promise detection** (lines 25-33): Check for completion signal in output
4. **Prompt extraction** (line 38): Read markdown body as next prompt
5. **State update** (lines 40-43): Increment iteration atomically
6. **Loop continuation** (lines 45-53): Block exit and feed prompt back

### Creation

**File:** `scripts/setup-ralph-loop.sh`

```bash
#!/bin/bash
PROMPT="$1"
MAX_ITERATIONS="${2:-0}"
COMPLETION_PROMISE="${3:-}"

# Create state file
cat > ".claude/ralph-loop.local.md" <<EOF
---
iteration: 1
max_iterations: $MAX_ITERATIONS
completion_promise: "$COMPLETION_PROMISE"
started_at: "$(date -Iseconds)"
---

$PROMPT
EOF

echo "Ralph loop initialized: .claude/ralph-loop.local.md"
```

## Pattern Comparison

| Feature | multi-agent-swarm | ralph-wiggum |
|---------|-------------------|--------------|
| **File** | `.claude/multi-agent-swarm.local.md` | `.claude/ralph-loop.local.md` |
| **Purpose** | Agent coordination state | Loop iteration state |
| **Frontmatter** | Agent metadata | Loop configuration |
| **Body** | Task assignment | Prompt to loop |
| **Updates** | PR number, status | Iteration counter |
| **Deletion** | Manual or on completion | On loop exit |
| **Hook** | Stop (notifications) | Stop (loop control) |

## Best Practices from Real Plugins

### 1. Quick Exit Pattern

Both plugins check file existence first:

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # Not active
fi
```

**Why:** Avoids errors when plugin isn't configured and performs fast.

### 2. Enabled Flag

Both use an `enabled` field for explicit control:

```yaml
enabled: true
```

**Why:** Allows temporary deactivation without deleting file.

### 3. Atomic Updates

Both use temp file + atomic move:

```bash
TEMP_FILE="${FILE}.tmp.$$"
sed "s/^field: .*/field: $NEW_VALUE/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

**Why:** Prevents corruption if process is interrupted.

### 4. Quote Handling

Both strip surrounding quotes from YAML values:

```bash
sed 's/^"\(.*\)"$/\1/'
```

**Why:** YAML allows both `field: value` and `field: "value"`.

### 5. Error Handling

Both handle missing/corrupt files gracefully:

```bash
if [[ ! -f "$FILE" ]]; then
  exit 0  # No error, just not configured
fi

if [[ -z "$CRITICAL_FIELD" ]]; then
  echo "Settings file corrupt" >&2
  rm "$FILE"  # Clean up
  exit 0
fi
```

**Why:** Fails gracefully instead of crashing.

## Anti-Patterns to Avoid

### ❌ Hardcoded Paths

```bash
# BAD
FILE="/Users/alice/.claude/my-plugin.local.md"

# GOOD
FILE=".claude/my-plugin.local.md"
```

### ❌ Unquoted Variables

```bash
# BAD
echo $VALUE

# GOOD
echo "$VALUE"
```

### ❌ Non-Atomic Updates

```bash
# BAD: Can corrupt file if interrupted
sed -i "s/field: .*/field: $VALUE/" "$FILE"

# GOOD: Atomic
TEMP_FILE="${FILE}.tmp.$$"
sed "s/field: .*/field: $VALUE/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

### ❌ No Default Values

```bash
# BAD: Fails if field missing
if [[ $MAX -gt 100 ]]; then
  # MAX might be empty!
fi

# GOOD: Provide default
MAX=${MAX:-10}
```

### ❌ Ignoring Edge Cases

```bash
# BAD: Assumes exactly 2 --- markers
sed -n '/^---$/,/^---$/{ /^---$/d; p; }'

# GOOD: Handles --- in body
awk '/^---$/{i++; next} i>=2'  # For body
```

## Conclusion

The `.claude/plugin-name.local.md` pattern provides:
- Simple, human-readable configuration
- Version-control friendly (gitignored)
- Per-project settings
- Easy parsing with standard bash tools
- Supports both structured config (YAML) and freeform content (markdown)

Use this pattern for any plugin that needs user-configurable behavior or state persistence.

---

## Example: create settings command

---
description: "Create plugin settings file with user preferences"
allowed-tools: ["Write", "AskUserQuestion"]
---

# Create Plugin Settings

This command helps users create a `.claude/my-plugin.local.md` settings file.

## Steps

### Step 1: Ask User for Preferences

Use AskUserQuestion to gather configuration:

```json
{
  "questions": [
    {
      "question": "Enable plugin for this project?",
      "header": "Enable Plugin",
      "multiSelect": false,
      "options": [
        {
          "label": "Yes",
          "description": "Plugin will be active"
        },
        {
          "label": "No",
          "description": "Plugin will be disabled"
        }
      ]
    },
    {
      "question": "Validation mode?",
      "header": "Mode",
      "multiSelect": false,
      "options": [
        {
          "label": "Strict",
          "description": "Maximum validation and security checks"
        },
        {
          "label": "Standard",
          "description": "Balanced validation (recommended)"
        },
        {
          "label": "Lenient",
          "description": "Minimal validation only"
        }
      ]
    }
  ]
}
```

### Step 2: Parse Answers

Extract answers from AskUserQuestion result:

- answers["0"]: enabled (Yes/No)
- answers["1"]: mode (Strict/Standard/Lenient)

### Step 3: Create Settings File

Use Write tool to create `.claude/my-plugin.local.md`:

```markdown
---
enabled: <true if Yes, false if No>
validation_mode: <strict, standard, or lenient>
max_file_size: 1000000
notify_on_errors: true
---

# Plugin Configuration

Your plugin is configured with <mode> validation mode.

To modify settings, edit this file and restart Claude Code.
```

### Step 4: Inform User

Tell the user:
- Settings file created at `.claude/my-plugin.local.md`
- Current configuration summary
- How to edit manually if needed
- Reminder: Restart Claude Code for changes to take effect
- Settings file is gitignored (won't be committed)

## Implementation Notes

Always validate user input before writing:
- Check mode is valid
- Validate numeric fields are numbers
- Ensure paths don't have traversal attempts
- Sanitize any free-text fields

---

## Example: example settings

# Example Plugin Settings File

## Template: Basic Configuration

**.claude/my-plugin.local.md:**

```markdown
---
enabled: true
mode: standard
---

# My Plugin Configuration

Plugin is active in standard mode.
```

## Template: Advanced Configuration

**.claude/my-plugin.local.md:**

```markdown
---
enabled: true
strict_mode: false
max_file_size: 1000000
allowed_extensions: [".js", ".ts", ".tsx"]
enable_logging: true
notification_level: info
retry_attempts: 3
timeout_seconds: 60
custom_path: "/path/to/data"
---

# My Plugin Advanced Configuration

This project uses custom plugin configuration with:
- Standard validation mode
- 1MB file size limit
- JavaScript/TypeScript files allowed
- Info-level logging
- 3 retry attempts

## Additional Notes

Contact @team-lead with questions about this configuration.
```

## Template: Agent State File

**.claude/multi-agent-swarm.local.md:**

```markdown
---
agent_name: database-implementation
task_number: 4.2
pr_number: 5678
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.5", "Task 4.1"]
additional_instructions: "Use PostgreSQL, not MySQL"
---

# Task Assignment: Database Schema Implementation

Implement the database schema for the new features module.

## Requirements

- Create migration files
- Add indexes for performance
- Write tests for constraints
- Document schema in README

## Success Criteria

- Migrations run successfully
- All tests pass
- PR created with CI green
- Schema documented

## Coordination

Depends on:
- Task 3.5: API endpoint definitions
- Task 4.1: Data model design

Report status to coordinator session 'team-leader'.
```

## Template: Feature Flag Pattern

**.claude/experimental-features.local.md:**

```markdown
---
enabled: true
features:
  - ai_suggestions
  - auto_formatting
  - advanced_refactoring
experimental_mode: false
---

# Experimental Features Configuration

Current enabled features:
- AI-powered code suggestions
- Automatic code formatting
- Advanced refactoring tools

Experimental mode is OFF (stable features only).
```

## Usage in Hooks

These templates can be read by hooks:

```bash
# Check if plugin is configured
if [[ ! -f ".claude/my-plugin.local.md" ]]; then
  exit 0  # Not configured, skip hook
fi

# Read settings
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' ".claude/my-plugin.local.md")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# Apply settings
if [[ "$ENABLED" == "true" ]]; then
  # Hook is active
  # ...
fi
```

## Gitignore

Always add to project `.gitignore`:

```gitignore
# Plugin settings (user-local, not committed)
.claude/*.local.md
.claude/*.local.json
```

## Editing Settings

Users can edit settings files manually:

```bash
# Edit settings
vim .claude/my-plugin.local.md

# Changes take effect after restart
exit  # Exit Claude Code
claude  # Restart
```

Changes require Claude Code restart - hooks can't be hot-swapped.
