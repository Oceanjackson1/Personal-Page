---
title: "创建 Hooks"
description: "创建、配置和使用 Claude Code Hooks 的专家指导"
category: "workflow"
source: "community"
author: "Community"
tags: ["create", "hooks"]
date: 2026-03-20
---

<objective>
Hooks are event-driven automation for Claude Code that execute shell commands or LLM prompts in response to tool usage, session events, and user interactions. This skill teaches you how to create, configure, and debug hooks for validating commands, automating workflows, injecting context, and implementing custom completion criteria.

Hooks provide programmatic control over Claude's behavior without modifying core code, enabling project-specific automation, safety checks, and workflow customization.
</objective>

<context>
Hooks are shell commands or LLM-evaluated prompts that execute in response to Claude Code events. They operate within an event hierarchy: events (PreToolUse, PostToolUse, Stop, etc.) trigger matchers (tool patterns) which fire hooks (commands or prompts). Hooks can block actions, modify tool inputs, inject context, or simply observe and log Claude's operations.
</context>

<quick_start>
<workflow>
1. Create hooks config file:
   - Project: `.claude/hooks.json`
   - User: `~/.claude/hooks.json`
2. Choose hook event (when it fires)
3. Choose hook type (command or prompt)
4. Configure matcher (which tools trigger it)
5. Test with `claude --debug`
</workflow>

<example>
**Log all bash commands**:

`.claude/hooks.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \\\"No description\\\")\"' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```

This hook:
- Fires before (`PreToolUse`) every `Bash` tool use
- Executes a `command` (not an LLM prompt)
- Logs command + description to a file
</example>
</quick_start>

<hook_types>
| Event | When it fires | Can block? |
|-------|---------------|------------|
| **PreToolUse** | Before tool execution | Yes |
| **PostToolUse** | After tool execution | No |
| **UserPromptSubmit** | User submits a prompt | Yes |
| **Stop** | Claude attempts to stop | Yes |
| **SubagentStop** | Subagent attempts to stop | Yes |
| **SessionStart** | Session begins | No |
| **SessionEnd** | Session ends | No |
| **PreCompact** | Before context compaction | Yes |
| **Notification** | Claude needs input | No |

Blocking hooks can return `"decision": "block"` to prevent the action. See [references/hook-types.md](references/hook-types.md) for detailed use cases.
</hook_types>

<hook_anatomy>
<hook_type name="command">
**Type**: Executes a shell command

**Use when**:
- Simple validation (check file exists)
- Logging (append to file)
- External tools (formatters, linters)
- Desktop notifications

**Input**: JSON via stdin
**Output**: JSON via stdout (optional)

```json
{
  "type": "command",
  "command": "/path/to/script.sh",
  "timeout": 30000
}
```
</hook_type>

<hook_type name="prompt">
**Type**: LLM evaluates a prompt

**Use when**:
- Complex decision logic
- Natural language validation
- Context-aware checks
- Reasoning required

**Input**: Prompt with `$ARGUMENTS` placeholder
**Output**: JSON with `decision` and `reason`

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this command is safe: $ARGUMENTS\n\nReturn JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
}
```
</hook_type>
</hook_anatomy>

<matchers>
Matchers filter which tools trigger the hook:

```json
{
  "matcher": "Bash",           // Exact match
  "matcher": "Write|Edit",     // Multiple tools (regex OR)
  "matcher": "mcp__.*",        // All MCP tools
  "matcher": "mcp__memory__.*" // Specific MCP server
}
```

**No matcher**: Hook fires for all tools
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [...]  // No matcher - fires on every user prompt
      }
    ]
  }
}
```
</matchers>

<input_output>
Hooks receive JSON via stdin with session info, current directory, and event-specific data. Blocking hooks can return JSON to approve/block actions or modify inputs.

**Example output** (blocking hooks):
```json
{
  "decision": "approve" | "block",
  "reason": "Why this decision was made"
}
```

See [references/input-output-schemas.md](references/input-output-schemas.md) for complete schemas for each hook type.
</input_output>

<environment_variables>
Available in hook commands:

| Variable | Value |
|----------|-------|
| `$CLAUDE_PROJECT_DIR` | Project root directory |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin directory (plugin hooks only) |
| `$ARGUMENTS` | Hook input JSON (prompt hooks only) |

**Example**:
```json
{
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.sh"
}
```
</environment_variables>

<common_patterns>
**Desktop notification when input needed**:
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs input\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**Block destructive git commands**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this command is destructive: $ARGUMENTS\n\nBlock if it contains: 'git push --force', 'rm -rf', 'git reset --hard'\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
          }
        ]
      }
    ]
  }
}
```

**Auto-format code after edits**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_PROJECT_DIR",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

**Add context at session start**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": \"Current sprint: Sprint 23. Focus: User authentication\"}}'"
          }
        ]
      }
    ]
  }
}
```
</common_patterns>

<debugging>
Always test hooks with the debug flag:
```bash
claude --debug
```

This shows which hooks matched, command execution, and output. See [references/troubleshooting.md](references/troubleshooting.md) for common issues and solutions.
</debugging>

<reference_guides>
**Hook types and events**: [references/hook-types.md](references/hook-types.md)
- Complete list of hook events
- When each event fires
- Input/output schemas for each
- Blocking vs non-blocking hooks

**Command vs Prompt hooks**: [references/command-vs-prompt.md](references/command-vs-prompt.md)
- Decision tree: which type to use
- Command hook patterns and examples
- Prompt hook patterns and examples
- Performance considerations

**Matchers and patterns**: [references/matchers.md](references/matchers.md)
- Regex patterns for tool matching
- MCP tool matching patterns
- Multiple tool matching
- Debugging matcher issues

**Input/Output schemas**: [references/input-output-schemas.md](references/input-output-schemas.md)
- Complete schema for each hook type
- Field descriptions and types
- Hook-specific output fields
- Example JSON for each event

**Working examples**: [references/examples.md](references/examples.md)
- Desktop notifications
- Command validation
- Auto-formatting workflows
- Logging and audit trails
- Stop logic patterns
- Session context injection

**Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md)
- Hooks not triggering
- Command execution failures
- Prompt hook issues
- Permission problems
- Timeout handling
- Debug workflow
</reference_guides>

<security_checklist>
**Critical safety requirements**:

- **Infinite loop prevention**: Check `stop_hook_active` flag in Stop hooks to prevent recursive triggering
- **Timeout configuration**: Set reasonable timeouts (default: 60s) to prevent hanging
- **Permission validation**: Ensure hook scripts have executable permissions (`chmod +x`)
- **Path safety**: Use absolute paths with `$CLAUDE_PROJECT_DIR` to avoid path injection
- **JSON validation**: Validate hook config with `jq` before use to catch syntax errors
- **Selective blocking**: Be conservative with blocking hooks to avoid workflow disruption

**Testing protocol**:
```bash
# Always test with debug flag first
claude --debug

# Validate JSON config
jq . .claude/hooks.json
```
</security_checklist>

<success_criteria>
A working hook configuration has:

- Valid JSON in `.claude/hooks.json` (validated with `jq`)
- Appropriate hook event selected for the use case
- Correct matcher pattern that matches target tools
- Command or prompt that executes without errors
- Proper output schema (decision/reason for blocking hooks)
- Tested with `--debug` flag showing expected behavior
- No infinite loops in Stop hooks (checks `stop_hook_active` flag)
- Reasonable timeout set (especially for external commands)
- Executable permissions on script files if using file paths
</success_criteria>

---

## Reference: Command Vs Prompt

# Command vs Prompt Hooks

Decision guide for choosing between command-based and prompt-based hooks.

## Decision Tree

```
Need to execute a hook?
│
├─ Simple yes/no validation?
│  └─ Use COMMAND (faster, cheaper)
│
├─ Need natural language understanding?
│  └─ Use PROMPT (LLM evaluation)
│
├─ External tool interaction?
│  └─ Use COMMAND (formatters, linters, git)
│
├─ Complex decision logic?
│  └─ Use PROMPT (reasoning required)
│
└─ Logging/notification only?
   └─ Use COMMAND (no decision needed)
```

---

## Command Hooks

### Characteristics

- **Execution**: Shell command
- **Input**: JSON via stdin
- **Output**: JSON via stdout (optional)
- **Speed**: Fast (no LLM call)
- **Cost**: Free (no API usage)
- **Complexity**: Limited to shell scripting logic

### When to use

✅ **Use command hooks for**:
- File operations (read, write, check existence)
- Running tools (prettier, eslint, git)
- Simple pattern matching (grep, regex)
- Logging to files
- Desktop notifications
- Fast validation (file size, permissions)

❌ **Don't use command hooks for**:
- Natural language analysis
- Complex decision logic
- Context-aware validation
- Semantic understanding

### Examples

**1. Log bash commands**
```json
{
  "type": "command",
  "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \\\"No description\\\")\"' >> ~/.claude/bash-log.txt"
}
```

**2. Block if file doesn't exist**
```bash
#!/bin/bash
# check-file-exists.sh

input=$(cat)
file=$(echo "$input" | jq -r '.tool_input.file_path')

if [ ! -f "$file" ]; then
  echo '{"decision": "block", "reason": "File does not exist"}'
  exit 0
fi

echo '{"decision": "approve", "reason": "File exists"}'
```

**3. Run prettier after edits**
```json
{
  "type": "command",
  "command": "prettier --write \"$(echo {} | jq -r '.tool_input.file_path')\"",
  "timeout": 10000
}
```

**4. Desktop notification**
```json
{
  "type": "command",
  "command": "osascript -e 'display notification \"Claude needs input\" with title \"Claude Code\"'"
}
```

### Parsing input in commands

Command hooks receive JSON via stdin. Use `jq` to parse:

```bash
#!/bin/bash
input=$(cat)  # Read stdin

# Extract fields
tool_name=$(echo "$input" | jq -r '.tool_name')
command=$(echo "$input" | jq -r '.tool_input.command')
session_id=$(echo "$input" | jq -r '.session_id')

# Your logic here
if [[ "$command" == *"rm -rf"* ]]; then
  echo '{"decision": "block", "reason": "Dangerous command"}'
else
  echo '{"decision": "approve", "reason": "Safe"}'
fi
```

---

## Prompt Hooks

### Characteristics

- **Execution**: LLM evaluates prompt
- **Input**: Prompt string with `$ARGUMENTS` placeholder
- **Output**: LLM generates JSON response
- **Speed**: Slower (~1-3s per evaluation)
- **Cost**: Uses API credits
- **Complexity**: Can reason, understand context, analyze semantics

### When to use

✅ **Use prompt hooks for**:
- Natural language validation
- Semantic analysis (intent, safety, appropriateness)
- Complex decision trees
- Context-aware checks
- Reasoning about code quality
- Understanding user intent

❌ **Don't use prompt hooks for**:
- Simple pattern matching (use regex/grep)
- File operations (use command hooks)
- High-frequency events (too slow/expensive)
- Non-decision tasks (logging, notifications)

### Examples

**1. Validate commit messages**
```json
{
  "type": "prompt",
  "prompt": "Evaluate this git commit message: $ARGUMENTS\n\nCheck if it:\n1. Starts with conventional commit type (feat|fix|docs|refactor|test|chore)\n2. Is descriptive and clear\n3. Under 72 characters\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"specific feedback\"}"
}
```

**2. Check if Stop is appropriate**
```json
{
  "type": "prompt",
  "prompt": "Review the conversation transcript: $ARGUMENTS\n\nDetermine if Claude should stop:\n1. All user tasks completed?\n2. Any errors that need fixing?\n3. Tests passing?\n4. Documentation updated?\n\nIf incomplete: {\"decision\": \"block\", \"reason\": \"what's missing\"}\nIf complete: {\"decision\": \"approve\", \"reason\": \"all done\"}"
}
```

**3. Validate code changes for security**
```json
{
  "type": "prompt",
  "prompt": "Analyze this code change for security issues: $ARGUMENTS\n\nCheck for:\n- SQL injection vulnerabilities\n- XSS attack vectors\n- Authentication bypasses\n- Sensitive data exposure\n\nIf issues found: {\"decision\": \"block\", \"reason\": \"specific vulnerabilities\"}\nIf safe: {\"decision\": \"approve\", \"reason\": \"no issues found\"}"
}
```

**4. Semantic prompt validation**
```json
{
  "type": "prompt",
  "prompt": "Evaluate user prompt: $ARGUMENTS\n\nIs this:\n1. Related to coding/development?\n2. Appropriate and professional?\n3. Clear and actionable?\n\nIf inappropriate: {\"decision\": \"block\", \"reason\": \"why\"}\nIf good: {\"decision\": \"approve\", \"reason\": \"ok\"}"
}
```

### Writing effective prompts

**Be specific about output format**:
```
Return JSON: {"decision": "approve" or "block", "reason": "explanation"}
```

**Provide clear criteria**:
```
Block if:
1. Command contains 'rm -rf /'
2. Force push to main branch
3. Credentials in plain text

Otherwise approve.
```

**Use $ARGUMENTS placeholder**:
```
Analyze this input: $ARGUMENTS

Check for...
```

The `$ARGUMENTS` placeholder is replaced with the actual hook input JSON.

---

## Performance Comparison

| Aspect | Command Hook | Prompt Hook |
|--------|--------------|-------------|
| **Speed** | <100ms | 1-3s |
| **Cost** | Free | ~$0.001-0.01 per call |
| **Complexity** | Shell scripting | Natural language |
| **Context awareness** | Limited | High |
| **Reasoning** | No | Yes |
| **Best for** | Operations, logging | Validation, analysis |

---

## Combining Both

You can use multiple hooks for the same event:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$input\" >> ~/bash-log.txt",
            "comment": "Log every command (fast)"
          },
          {
            "type": "prompt",
            "prompt": "Analyze this bash command for safety: $ARGUMENTS",
            "comment": "Validate with LLM (slower, smarter)"
          }
        ]
      }
    ]
  }
}
```

Hooks execute in order. If any hook blocks, execution stops.

---

## Recommendations

**High-frequency events** (PreToolUse, PostToolUse):
- Prefer command hooks
- Use prompt hooks sparingly
- Cache LLM decisions when possible

**Low-frequency events** (Stop, UserPromptSubmit):
- Prompt hooks are fine
- Cost/latency less critical

**Balance**:
- Command hooks for simple checks
- Prompt hooks for complex validation
- Combine when appropriate

---

## Reference: Examples

# Working Examples

Real-world hook configurations ready to use.

## Desktop Notifications

### macOS notification when input needed
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs your input\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
```

### Linux notification (notify-send)
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input' --urgency=normal"
          }
        ]
      }
    ]
  }
}
```

### Play sound on notification
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Glass.aiff"
          }
        ]
      }
    ]
  }
}
```

---

## Logging

### Log all bash commands
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"[\" + (.timestamp // now | todate) + \"] \" + .tool_input.command + \" - \" + (.tool_input.description // \"No description\")' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Log file operations
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"[\" + (now | todate) + \"] \" + .tool_name + \": \" + .tool_input.file_path' >> ~/.claude/file-operations.log"
          }
        ]
      }
    ]
  }
}
```

### Audit trail for MCP operations
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "jq '. + {timestamp: now}' >> ~/.claude/mcp-audit.jsonl"
          }
        ]
      }
    ]
  }
}
```

---

## Code Quality

### Auto-format after edits
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$(echo {} | jq -r '.tool_input.file_path')\" 2>/dev/null || true",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

### Run linter after code changes
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "eslint \"$(echo {} | jq -r '.tool_input.file_path')\" --fix 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Run tests before stopping
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-tests.sh"
          }
        ]
      }
    ]
  }
}
```

`check-tests.sh`:
```bash
#!/bin/bash
cd "$cwd" || exit 1

# Run tests
npm test > /dev/null 2>&1

if [ $? -eq 0 ]; then
  echo '{"decision": "approve", "reason": "All tests passing"}'
else
  echo '{"decision": "block", "reason": "Tests are failing. Please fix before stopping.", "systemMessage": "Run npm test to see failures"}'
fi
```

---

## Safety and Validation

### Block destructive commands
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-command-safety.sh"
          }
        ]
      }
    ]
  }
}
```

`check-command-safety.sh`:
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# Check for dangerous patterns
if [[ "$command" == *"rm -rf /"* ]] || \
   [[ "$command" == *"mkfs"* ]] || \
   [[ "$command" == *"> /dev/sda"* ]]; then
  echo '{"decision": "block", "reason": "Destructive command detected", "systemMessage": "This command could cause data loss"}'
  exit 0
fi

# Check for force push to main
if [[ "$command" == *"git push"*"--force"* ]] && \
   [[ "$command" == *"main"* || "$command" == *"master"* ]]; then
  echo '{"decision": "block", "reason": "Force push to main branch blocked", "systemMessage": "Use a feature branch instead"}'
  exit 0
fi

echo '{"decision": "approve", "reason": "Command is safe"}'
```

### Validate commit messages
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this is a git commit command: $ARGUMENTS\n\nIf it's a git commit, validate the message follows conventional commits format (feat|fix|docs|refactor|test|chore): description\n\nIf invalid format: {\"decision\": \"block\", \"reason\": \"Commit message must follow conventional commits\"}\nIf valid or not a commit: {\"decision\": \"approve\", \"reason\": \"ok\"}"
          }
        ]
      }
    ]
  }
}
```

### Block writes to critical files
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-protected-files.sh"
          }
        ]
      }
    ]
  }
}
```

`check-protected-files.sh`:
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# Protected files
protected_files=(
  "package-lock.json"
  ".env.production"
  "credentials.json"
)

for protected in "${protected_files[@]}"; do
  if [[ "$file_path" == *"$protected"* ]]; then
    echo "{\"decision\": \"block\", \"reason\": \"Cannot modify $protected\", \"systemMessage\": \"This file is protected from automated changes\"}"
    exit 0
  fi
done

echo '{"decision": "approve", "reason": "File is not protected"}'
```

---

## Context Injection

### Load sprint context at session start
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/load-sprint-context.sh"
          }
        ]
      }
    ]
  }
}
```

`load-sprint-context.sh`:
```bash
#!/bin/bash

# Read sprint info from file
sprint_info=$(cat "$CLAUDE_PROJECT_DIR/.sprint-context.txt" 2>/dev/null || echo "No sprint context available")

# Return as SessionStart context
jq -n \
  --arg context "$sprint_info" \
  '{
    "hookSpecificOutput": {
      "hookEventName": "SessionStart",
      "additionalContext": $context
    }
  }'
```

### Load git branch context
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$cwd\" && git branch --show-current | jq -Rs '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": (\"Current branch: \" + .)}}'"
          }
        ]
      }
    ]
  }
}
```

### Load environment info
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": \"Environment: '$(hostname)'\\nNode version: '$(node --version 2>/dev/null || echo 'not installed')'\\nPython version: '$(python3 --version 2>/dev/null || echo 'not installed)'\"}}'"
          }
        ]
      }
    ]
  }
}
```

---

## Workflow Automation

### Auto-commit after major changes
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/auto-commit.sh"
          }
        ]
      }
    ]
  }
}
```

`auto-commit.sh`:
```bash
#!/bin/bash
cd "$cwd" || exit 1

# Check if there are changes
if ! git diff --quiet; then
  git add -A
  git commit -m "chore: auto-commit from claude session" --no-verify
  echo '{"systemMessage": "Changes auto-committed"}'
fi
```

### Update documentation after code changes
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/update-docs.sh",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

### Run pre-commit hooks
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-pre-commit.sh"
          }
        ]
      }
    ]
  }
}
```

`check-pre-commit.sh`:
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# If git commit, run pre-commit hooks first
if [[ "$command" == *"git commit"* ]]; then
  pre-commit run --all-files > /dev/null 2>&1

  if [ $? -ne 0 ]; then
    echo '{"decision": "block", "reason": "Pre-commit hooks failed", "systemMessage": "Fix formatting/linting issues first"}'
    exit 0
  fi
fi

echo '{"decision": "approve", "reason": "ok"}'
```

---

## Session Management

### Archive transcript on session end
```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/archive-session.sh"
          }
        ]
      }
    ]
  }
}
```

`archive-session.sh`:
```bash
#!/bin/bash
input=$(cat)
transcript_path=$(echo "$input" | jq -r '.transcript_path')
session_id=$(echo "$input" | jq -r '.session_id')

# Create archive directory
archive_dir="$HOME/.claude/archives"
mkdir -p "$archive_dir"

# Copy transcript with timestamp
timestamp=$(date +%Y%m%d-%H%M%S)
cp "$transcript_path" "$archive_dir/${timestamp}-${session_id}.jsonl"

echo "Session archived to $archive_dir"
```

### Save session stats
```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "jq '. + {ended_at: now}' >> ~/.claude/session-stats.jsonl"
          }
        ]
      }
    ]
  }
}
```

---

## Advanced Patterns

### Intelligent stop logic
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the conversation: $ARGUMENTS\n\nCheck if:\n1. All user-requested tasks are complete\n2. Tests are passing (if code changes made)\n3. No errors that need fixing\n4. Documentation updated (if applicable)\n\nIf incomplete: {\"decision\": \"block\", \"reason\": \"specific issue\", \"systemMessage\": \"what needs to be done\"}\n\nIf complete: {\"decision\": \"approve\", \"reason\": \"all tasks done\"}\n\nIMPORTANT: If stop_hook_active is true, return {\"decision\": undefined} to avoid infinite loop",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

### Chain multiple hooks
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'First hook' >> /tmp/hook-chain.log"
          },
          {
            "type": "command",
            "command": "echo 'Second hook' >> /tmp/hook-chain.log"
          },
          {
            "type": "prompt",
            "prompt": "Final validation: $ARGUMENTS"
          }
        ]
      }
    ]
  }
}
```

Hooks execute in order. First block stops the chain.

### Conditional execution based on file type
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/format-by-type.sh"
          }
        ]
      }
    ]
  }
}
```

`format-by-type.sh`:
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

case "$file_path" in
  *.js|*.jsx|*.ts|*.tsx)
    prettier --write "$file_path"
    ;;
  *.py)
    black "$file_path"
    ;;
  *.go)
    gofmt -w "$file_path"
    ;;
esac
```

---

## Project-Specific Hooks

Use `$CLAUDE_PROJECT_DIR` for project-specific hooks:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/init-session.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-changes.sh"
          }
        ]
      }
    ]
  }
}
```

This keeps hook scripts versioned with the project.

---

## Reference: Hook Types

# Hook Types and Events

Complete reference for all Claude Code hook events.

## PreToolUse

**When it fires**: Before any tool is executed

**Can block**: Yes

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm install",
    "description": "Install dependencies"
  }
}
```

**Output schema** (to control execution):
```json
{
  "decision": "approve" | "block",
  "reason": "Explanation",
  "permissionDecision": "allow" | "deny" | "ask",
  "permissionDecisionReason": "Why",
  "updatedInput": {
    "command": "npm install --save-exact"
  }
}
```

**Use cases**:
- Validate commands before execution
- Block dangerous operations
- Modify tool inputs
- Log command attempts
- Ask user for confirmation

**Example**: Block force pushes to main
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this git command is safe: $ARGUMENTS\n\nBlock if: force push to main/master\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
          }
        ]
      }
    ]
  }
}
```

---

## PostToolUse

**When it fires**: After a tool completes execution

**Can block**: No (tool already executed)

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.js",
    "content": "..."
  },
  "tool_output": "File created successfully"
}
```

**Output schema**:
```json
{
  "systemMessage": "Optional message to display",
  "suppressOutput": false
}
```

**Use cases**:
- Auto-format code after Write/Edit
- Run tests after code changes
- Update documentation
- Trigger CI builds
- Send notifications

**Example**: Auto-format after edits
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_PROJECT_DIR",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

---

## UserPromptSubmit

**When it fires**: User submits a prompt to Claude

**Can block**: Yes

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate factorial"
}
```

**Output schema**:
```json
{
  "decision": "approve" | "block",
  "reason": "Explanation",
  "systemMessage": "Message to user"
}
```

**Use cases**:
- Validate prompt format
- Block inappropriate requests
- Preprocess user input
- Add context to prompts
- Enforce prompt templates

**Example**: Require issue numbers in prompts
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if prompt mentions an issue number (e.g., #123 or PROJ-456): $ARGUMENTS\n\nIf no issue number: {\"decision\": \"block\", \"reason\": \"Please include issue number\"}\nOtherwise: {\"decision\": \"approve\", \"reason\": \"ok\"}"
          }
        ]
      }
    ]
  }
}
```

---

## Stop

**When it fires**: Claude attempts to stop working

**Can block**: Yes

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

**Output schema**:
```json
{
  "decision": "block" | undefined,
  "reason": "Why Claude should continue",
  "continue": true,
  "systemMessage": "Additional instructions"
}
```

**Use cases**:
- Verify all tasks completed
- Check for errors that need fixing
- Ensure tests pass before stopping
- Validate deliverables
- Custom completion criteria

**Example**: Verify tests pass before stopping
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npm test && echo '{\"decision\": \"approve\"}' || echo '{\"decision\": \"block\", \"reason\": \"Tests failing\"}'"
          }
        ]
      }
    ]
  }
}
```

**Important**: Check `stop_hook_active` to avoid infinite loops. If true, don't block again.

---

## SubagentStop

**When it fires**: A subagent attempts to stop

**Can block**: Yes

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false
}
```

**Output schema**: Same as Stop

**Use cases**:
- Verify subagent completed its task
- Check for errors in subagent output
- Validate subagent deliverables
- Ensure quality before accepting results

**Example**: Check if code-reviewer provided feedback
```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the subagent transcript: $ARGUMENTS\n\nDid the code-reviewer provide:\n1. Specific issues found\n2. Severity ratings\n3. Remediation steps\n\nIf missing: {\"decision\": \"block\", \"reason\": \"Incomplete review\"}\nOtherwise: {\"decision\": \"approve\", \"reason\": \"Complete\"}"
          }
        ]
      }
    ]
  }
}
```

---

## SessionStart

**When it fires**: At the beginning of a Claude session

**Can block**: No

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

**Output schema**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context to inject into session"
  }
}
```

**Use cases**:
- Load project context
- Inject sprint information
- Set environment variables
- Initialize state
- Display welcome messages

**Example**: Load current sprint context
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat $CLAUDE_PROJECT_DIR/.sprint-context.txt | jq -Rs '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": .}}'"
          }
        ]
      }
    ]
  }
}
```

---

## SessionEnd

**When it fires**: When a Claude session ends

**Can block**: No (cannot prevent session end)

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",
  "reason": "exit" | "error" | "timeout"
}
```

**Output schema**: None (hook output ignored)

**Use cases**:
- Save session state
- Cleanup temporary files
- Update logs
- Send analytics
- Archive transcripts

**Example**: Archive session transcript
```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cp $transcript_path $CLAUDE_PROJECT_DIR/.claude/archives/$(date +%Y%m%d-%H%M%S).jsonl"
          }
        ]
      }
    ]
  }
}
```

---

## PreCompact

**When it fires**: Before context window compaction

**Can block**: Yes

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",
  "trigger": "manual" | "auto",
  "custom_instructions": "User's compaction instructions"
}
```

**Output schema**:
```json
{
  "decision": "approve" | "block",
  "reason": "Explanation"
}
```

**Use cases**:
- Validate state before compaction
- Save important context
- Custom compaction logic
- Prevent compaction at critical moments

---

## Notification

**When it fires**: Claude needs user input (awaiting response)

**Can block**: No

**Input schema**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "Notification"
}
```

**Output schema**: None

**Use cases**:
- Desktop notifications
- Sound alerts
- Status bar updates
- External notifications (Slack, etc.)

**Example**: macOS notification
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs input\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

---

## Reference: Input Output Schemas

# Input/Output Schemas

Complete JSON schemas for all hook types.

## Common Input Fields

All hooks receive these fields:

```typescript
{
  session_id: string           // Unique session identifier
  transcript_path: string      // Path to session transcript (.jsonl file)
  cwd: string                  // Current working directory
  permission_mode: string      // "default" | "plan" | "acceptEdits" | "bypassPermissions"
  hook_event_name: string      // Name of the hook event
}
```

---

## PreToolUse

**Input**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/Users/username/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm install",
    "description": "Install dependencies"
  }
}
```

**Output** (optional, for control):
```json
{
  "decision": "approve" | "block",
  "reason": "Explanation for the decision",
  "permissionDecision": "allow" | "deny" | "ask",
  "permissionDecisionReason": "Why this permission decision",
  "updatedInput": {
    "command": "npm install --save-exact"
  },
  "systemMessage": "Message displayed to user",
  "suppressOutput": false,
  "continue": true
}
```

**Fields**:
- `decision`: Whether to allow the tool call
- `reason`: Explanation (required if blocking)
- `permissionDecision`: Override permission system
- `updatedInput`: Modified tool input (partial update)
- `systemMessage`: Message shown to user
- `suppressOutput`: Hide hook output from user
- `continue`: If false, stop execution

---

## PostToolUse

**Input**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/Users/username/project",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.js",
    "content": "const x = 1;"
  },
  "tool_output": "File created successfully at: /path/to/file.js"
}
```

**Output** (optional):
```json
{
  "systemMessage": "Code formatted successfully",
  "suppressOutput": false
}
```

**Fields**:
- `systemMessage`: Additional message to display
- `suppressOutput`: Hide tool output from user

---

## UserPromptSubmit

**Input**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/Users/username/project",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate factorial"
}
```

**Output**:
```json
{
  "decision": "approve" | "block",
  "reason": "Prompt is clear and actionable",
  "systemMessage": "Optional message to user"
}
```

**Fields**:
- `decision`: Whether to allow the prompt
- `reason`: Explanation (required if blocking)
- `systemMessage`: Message shown to user

---

## Stop

**Input**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/Users/username/project",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

**Output**:
```json
{
  "decision": "block" | undefined,
  "reason": "Tests are still failing - please fix before stopping",
  "continue": true,
  "stopReason": "Cannot stop yet",
  "systemMessage": "Additional context"
}
```

**Fields**:
- `decision`: `"block"` to prevent stopping, `undefined` to allow
- `reason`: Why Claude should continue (required if blocking)
- `continue`: If true and blocking, Claude continues working
- `stopReason`: Message shown when stopping is blocked
- `systemMessage`: Additional context for Claude
- `stop_hook_active`: If true, don't block again (prevents infinite loops)

**Important**: Always check `stop_hook_active` to avoid infinite loops:

```javascript
if (input.stop_hook_active) {
  return { decision: undefined }; // Don't block again
}
```

---

## SubagentStop

**Input**: Same as Stop

**Output**: Same as Stop

**Usage**: Same as Stop, but for subagent completion

---

## SessionStart

**Input**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/Users/username/project",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup" | "continue" | "checkpoint"
}
```

**Output**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current sprint: Sprint 23\nFocus: User authentication\nDeadline: Friday"
  }
}
```

**Fields**:
- `additionalContext`: Text injected into session context
- Multiple SessionStart hooks' contexts are concatenated

---

## SessionEnd

**Input**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/Users/username/project",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",
  "reason": "exit" | "error" | "timeout" | "compact"
}
```

**Output**: None (ignored)

**Usage**: Cleanup tasks only. Cannot prevent session end.

---

## PreCompact

**Input**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/Users/username/project",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",
  "trigger": "manual" | "auto",
  "custom_instructions": "Preserve all git commit messages"
}
```

**Output**:
```json
{
  "decision": "approve" | "block",
  "reason": "Safe to compact" | "Wait until task completes"
}
```

**Fields**:
- `trigger`: How compaction was initiated
- `custom_instructions`: User's compaction preferences (if manual)
- `decision`: Whether to proceed with compaction
- `reason`: Explanation

---

## Notification

**Input**:
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/Users/username/project",
  "permission_mode": "default",
  "hook_event_name": "Notification"
}
```

**Output**: None (hook just performs notification action)

**Usage**: Trigger external notifications (desktop, sound, status bar)

---

## Common Output Fields

These fields can be returned by any hook:

```json
{
  "continue": true | false,
  "stopReason": "Reason shown when stopping",
  "suppressOutput": true | false,
  "systemMessage": "Additional context or message"
}
```

**Fields**:
- `continue`: If false, stop Claude's execution immediately
- `stopReason`: Message displayed when execution stops
- `suppressOutput`: If true, hide hook's stdout/stderr from user
- `systemMessage`: Context added to Claude's next message

---

## LLM Prompt Hook Response

When using `type: "prompt"`, the LLM must return JSON:

```json
{
  "decision": "approve" | "block",
  "reason": "Detailed explanation",
  "systemMessage": "Optional message",
  "continue": true | false,
  "stopReason": "Optional stop message"
}
```

**Example prompt**:
```
Evaluate this command: $ARGUMENTS

Check if it's safe to execute.

Return JSON:
{
  "decision": "approve" or "block",
  "reason": "your explanation"
}
```

The `$ARGUMENTS` placeholder is replaced with the hook's input JSON.

---

## Tool-Specific Input Fields

Different tools provide different `tool_input` fields:

### Bash
```json
{
  "tool_input": {
    "command": "npm install",
    "description": "Install dependencies",
    "timeout": 120000,
    "run_in_background": false
  }
}
```

### Write
```json
{
  "tool_input": {
    "file_path": "/path/to/file.js",
    "content": "const x = 1;"
  }
}
```

### Edit
```json
{
  "tool_input": {
    "file_path": "/path/to/file.js",
    "old_string": "const x = 1;",
    "new_string": "const x = 2;",
    "replace_all": false
  }
}
```

### Read
```json
{
  "tool_input": {
    "file_path": "/path/to/file.js",
    "offset": 0,
    "limit": 100
  }
}
```

### Grep
```json
{
  "tool_input": {
    "pattern": "function.*",
    "path": "/path/to/search",
    "output_mode": "content"
  }
}
```

### MCP tools
```json
{
  "tool_input": {
    // MCP tool-specific parameters
  }
}
```

Access these in hooks:
```bash
command=$(echo "$input" | jq -r '.tool_input.command')
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
```

---

## Modifying Tool Input

PreToolUse hooks can modify `tool_input` before execution:

**Original input**:
```json
{
  "tool_input": {
    "command": "npm install lodash"
  }
}
```

**Hook output**:
```json
{
  "decision": "approve",
  "reason": "Adding --save-exact flag",
  "updatedInput": {
    "command": "npm install --save-exact lodash"
  }
}
```

**Result**: Tool executes with modified input.

**Partial updates**: Only specify fields you want to change:
```json
{
  "updatedInput": {
    "timeout": 300000  // Only update timeout, keep other fields
  }
}
```

---

## Error Handling

**Command hooks**: Return non-zero exit code to indicate error
```bash
if [ error ]; then
  echo '{"decision": "block", "reason": "Error occurred"}' >&2
  exit 1
fi
```

**Prompt hooks**: LLM should return valid JSON. If malformed, hook fails gracefully.

**Timeout**: Set `timeout` (ms) to prevent hanging:
```json
{
  "type": "command",
  "command": "/path/to/slow-script.sh",
  "timeout": 30000
}
```

Default: 60000ms (60s)

---

## Reference: Matchers

# Matchers and Pattern Matching

Complete guide to matching tools with hook matchers.

## What are matchers?

Matchers are regex patterns that filter which tools trigger a hook. They allow you to:
- Target specific tools (e.g., only `Bash`)
- Match multiple tools (e.g., `Write|Edit`)
- Match tool categories (e.g., all MCP tools)
- Match everything (omit matcher)

---

## Syntax

Matchers use JavaScript regex syntax:

```json
{
  "matcher": "pattern"
}
```

The pattern is tested against the tool name using `new RegExp(pattern).test(toolName)`.

---

## Common Patterns

### Exact match
```json
{
  "matcher": "Bash"
}
```
Matches: `Bash`
Doesn't match: `bash`, `BashOutput`

### Multiple tools (OR)
```json
{
  "matcher": "Write|Edit"
}
```
Matches: `Write`, `Edit`
Doesn't match: `Read`, `Bash`

### Starts with
```json
{
  "matcher": "^Bash"
}
```
Matches: `Bash`, `BashOutput`
Doesn't match: `Read`

### Ends with
```json
{
  "matcher": "Output$"
}
```
Matches: `BashOutput`
Doesn't match: `Bash`, `Read`

### Contains
```json
{
  "matcher": ".*write.*"
}
```
Matches: `Write`, `NotebookWrite`, `TodoWrite`
Doesn't match: `Read`, `Edit`

Case-sensitive! `write` won't match `Write`.

### Any tool (no matcher)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [...]  // No matcher = matches all tools
      }
    ]
  }
}
```

---

## Tool Categories

### All file operations
```json
{
  "matcher": "Read|Write|Edit|Glob|Grep"
}
```

### All bash tools
```json
{
  "matcher": "Bash.*"
}
```
Matches: `Bash`, `BashOutput`, `BashKill`

### All MCP tools
```json
{
  "matcher": "mcp__.*"
}
```
Matches: `mcp__memory__store`, `mcp__filesystem__read`, etc.

### Specific MCP server
```json
{
  "matcher": "mcp__memory__.*"
}
```
Matches: `mcp__memory__store`, `mcp__memory__retrieve`
Doesn't match: `mcp__filesystem__read`

### Specific MCP tool
```json
{
  "matcher": "mcp__.*__write.*"
}
```
Matches: `mcp__filesystem__write`, `mcp__memory__write`
Doesn't match: `mcp__filesystem__read`

---

## MCP Tool Naming

MCP tools follow the pattern: `mcp__{server}__{tool}`

Examples:
- `mcp__memory__store`
- `mcp__filesystem__read`
- `mcp__github__create_issue`

**Match all tools from a server**:
```json
{
  "matcher": "mcp__github__.*"
}
```

**Match specific tool across all servers**:
```json
{
  "matcher": "mcp__.*__read.*"
}
```

---

## Real-World Examples

### Log all bash commands
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Format code after any file write
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_PROJECT_DIR"
          }
        ]
      }
    ]
  }
}
```

### Validate all MCP memory writes
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate this memory operation: $ARGUMENTS\n\nCheck if data is appropriate to store.\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"why\"}"
          }
        ]
      }
    ]
  }
}
```

### Block destructive git commands
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-git-safety.sh"
          }
        ]
      }
    ]
  }
}
```

`check-git-safety.sh`:
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

if [[ "$command" == *"git push --force"* ]] || \
   [[ "$command" == *"rm -rf /"* ]] || \
   [[ "$command" == *"git reset --hard"* ]]; then
  echo '{"decision": "block", "reason": "Destructive command detected"}'
else
  echo '{"decision": "approve", "reason": "Safe"}'
fi
```

---

## Multiple Matchers

You can have multiple matcher blocks for the same event:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/bash-validator.sh"
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/file-validator.sh"
          }
        ]
      },
      {
        "matcher": "mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/mcp-logger.sh"
          }
        ]
      }
    ]
  }
}
```

Each matcher is evaluated independently. A tool can match multiple matchers.

---

## Debugging Matchers

### Enable debug mode
```bash
claude --debug
```

Debug output shows:
```
[DEBUG] Getting matching hook commands for PreToolUse with query: Bash
[DEBUG] Found 3 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Bash"
```

### Test your matcher

Use JavaScript regex to test patterns:

```javascript
const toolName = "mcp__memory__store";
const pattern = "mcp__memory__.*";
const regex = new RegExp(pattern);
console.log(regex.test(toolName)); // true
```

Or in Node.js:
```bash
node -e "console.log(/mcp__memory__.*/.test('mcp__memory__store'))"
```

### Common mistakes

❌ **Case sensitivity**
```json
{
  "matcher": "bash"  // Won't match "Bash"
}
```

✅ **Correct**
```json
{
  "matcher": "Bash"
}
```

---

❌ **Missing escape**
```json
{
  "matcher": "mcp__memory__*"  // * is literal, not wildcard
}
```

✅ **Correct**
```json
{
  "matcher": "mcp__memory__.*"  // .* is regex for "any characters"
}
```

---

❌ **Unintended partial match**
```json
{
  "matcher": "Write"  // Matches "Write", "TodoWrite", "NotebookWrite"
}
```

✅ **Exact match only**
```json
{
  "matcher": "^Write$"
}
```

---

## Advanced Patterns

### Negative lookahead (exclude tools)
```json
{
  "matcher": "^(?!Read).*"
}
```
Matches: Everything except `Read`

### Match any file operation except Grep
```json
{
  "matcher": "^(Read|Write|Edit|Glob)$"
}
```

### Case-insensitive match
```json
{
  "matcher": "(?i)bash"
}
```
Matches: `Bash`, `bash`, `BASH`

(Note: Claude Code tools are PascalCase by convention, so this is rarely needed)

---

## Performance Considerations

**Broad matchers** (e.g., `.*`) run on every tool use:
- Simple command hooks: negligible impact
- Prompt hooks: can slow down significantly

**Recommendation**: Be as specific as possible with matchers to minimize unnecessary hook executions.

**Example**: Instead of matching all tools and checking inside the hook:
```json
{
  "matcher": ".*",  // Runs on EVERY tool
  "hooks": [
    {
      "type": "command",
      "command": "if [[ $(jq -r '.tool_name') == 'Bash' ]]; then ...; fi"
    }
  ]
}
```

Do this:
```json
{
  "matcher": "Bash",  // Only runs on Bash
  "hooks": [
    {
      "type": "command",
      "command": "..."
    }
  ]
}
```

---

## Tool Name Reference

Common Claude Code tool names:
- `Bash`
- `BashOutput`
- `KillShell`
- `Read`
- `Write`
- `Edit`
- `Glob`
- `Grep`
- `TodoWrite`
- `NotebookEdit`
- `WebFetch`
- `WebSearch`
- `Task`
- `Skill`
- `SlashCommand`
- `AskUserQuestion`
- `ExitPlanMode`

MCP tools: `mcp__{server}__{tool}` (varies by installed servers)

Run `claude --debug` and watch tool calls to discover available tool names.

---

## Reference: Troubleshooting

# Troubleshooting

Common issues and solutions when working with hooks.

## Hook Not Triggering

### Symptom
Hook never executes, even when expected event occurs.

### Diagnostic steps

**1. Enable debug mode**
```bash
claude --debug
```

Look for:
```
[DEBUG] Getting matching hook commands for PreToolUse with query: Bash
[DEBUG] Found 0 hooks
```

**2. Check hook file location**

Hooks must be in:
- Project: `.claude/hooks.json`
- User: `~/.claude/hooks.json`
- Plugin: `{plugin}/hooks.json`

Verify:
```bash
cat .claude/hooks.json
# or
cat ~/.claude/hooks.json
```

**3. Validate JSON syntax**

Invalid JSON is silently ignored:
```bash
jq . .claude/hooks.json
```

If error: fix JSON syntax.

**4. Check matcher pattern**

Common mistakes:

❌ Case sensitivity
```json
{
  "matcher": "bash"  // Won't match "Bash"
}
```

✅ Fix
```json
{
  "matcher": "Bash"
}
```

---

❌ Missing escape for regex
```json
{
  "matcher": "mcp__memory__*"  // Literal *, not wildcard
}
```

✅ Fix
```json
{
  "matcher": "mcp__memory__.*"  // Regex wildcard
}
```

**5. Test matcher in isolation**

```bash
node -e "console.log(/Bash/.test('Bash'))"  # true
node -e "console.log(/bash/.test('Bash'))"  # false
```

### Solutions

**Missing hook file**: Create `.claude/hooks.json` or `~/.claude/hooks.json`

**Invalid JSON**: Use `jq` to validate and format:
```bash
jq . .claude/hooks.json > temp.json && mv temp.json .claude/hooks.json
```

**Wrong matcher**: Check tool names with `--debug` and update matcher

**No matcher specified**: If you want to match all tools, omit the matcher field entirely:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [...]  // No matcher = all tools
      }
    ]
  }
}
```

---

## Command Hook Failing

### Symptom
Hook executes but fails with error.

### Diagnostic steps

**1. Check debug output**
```
[DEBUG] Hook command completed with status 1: <error message>
```

Status 1 = command failed.

**2. Test command directly**

Copy the command and run in terminal:
```bash
echo '{"session_id":"test","tool_name":"Bash"}' | /path/to/your/hook.sh
```

**3. Check permissions**
```bash
ls -l /path/to/hook.sh
chmod +x /path/to/hook.sh  # If not executable
```

**4. Verify dependencies**

Does the command require tools?
```bash
which jq  # Check if jq is installed
which osascript  # macOS only
```

### Common issues

**Missing executable permission**
```bash
chmod +x /path/to/hook.sh
```

**Missing dependencies**

Install required tools:
```bash
# macOS
brew install jq

# Linux
apt-get install jq
```

**Bad path**

Use absolute paths:
```json
{
  "command": "/Users/username/.claude/hooks/script.sh"
}
```

Or use environment variables:
```json
{
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh"
}
```

**Timeout**

If command takes too long:
```json
{
  "command": "/path/to/slow-script.sh",
  "timeout": 120000  // 2 minutes
}
```

---

## Prompt Hook Not Working

### Symptom
Prompt hook blocks everything or doesn't block when expected.

### Diagnostic steps

**1. Check LLM response format**

Debug output shows:
```
[DEBUG] Hook command completed with status 0: {"decision": "approve", "reason": "ok"}
```

Verify JSON is valid.

**2. Check prompt structure**

Ensure prompt is clear:
```json
{
  "prompt": "Evaluate: $ARGUMENTS\n\nReturn JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"why\"}"
}
```

**3. Test prompt manually**

Submit similar prompt to Claude directly to see response format.

### Common issues

**Ambiguous instructions**

❌ Vague
```json
{
  "prompt": "Is this ok? $ARGUMENTS"
}
```

✅ Clear
```json
{
  "prompt": "Check if this command is safe: $ARGUMENTS\n\nBlock if: contains 'rm -rf', 'mkfs', or force push to main\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
}
```

**Missing $ARGUMENTS**

❌ No placeholder
```json
{
  "prompt": "Validate this command"
}
```

✅ With placeholder
```json
{
  "prompt": "Validate this command: $ARGUMENTS"
}
```

**Invalid JSON response**

The LLM must return valid JSON. If it returns plain text, the hook fails.

Add explicit formatting instructions:
```
IMPORTANT: Return ONLY valid JSON, no other text:
{
  "decision": "approve" or "block",
  "reason": "your explanation"
}
```

---

## Hook Blocks Everything

### Symptom
Hook blocks all operations, even safe ones.

### Diagnostic steps

**1. Check hook logic**

Review the script/prompt logic. Is the condition too broad?

**2. Test with known-safe input**

```bash
echo '{"tool_name":"Read","tool_input":{"file_path":"test.txt"}}' | /path/to/hook.sh
```

Expected: `{"decision": "approve"}`

**3. Check for errors in script**

Add error output:
```bash
#!/bin/bash
set -e  # Exit on error
input=$(cat)
# ... rest of script
```

### Solutions

**Logic error**

Review conditions:
```bash
# Before (blocks everything)
if [[ "$command" != "safe_command" ]]; then
  block
fi

# After (blocks dangerous commands)
if [[ "$command" == *"dangerous"* ]]; then
  block
fi
```

**Default to approve**

If logic is complex, default to approve on unclear cases:
```bash
# Default
decision="approve"
reason="ok"

# Only change if dangerous
if [[ "$command" == *"rm -rf"* ]]; then
  decision="block"
  reason="Dangerous command"
fi

echo "{\"decision\": \"$decision\", \"reason\": \"$reason\"}"
```

---

## Infinite Loop in Stop Hook

### Symptom
Stop hook runs repeatedly, Claude never stops.

### Cause
Hook blocks stop without checking `stop_hook_active` flag.

### Solution

**Always check the flag**:
```bash
#!/bin/bash
input=$(cat)
stop_hook_active=$(echo "$input" | jq -r '.stop_hook_active')

# If hook already active, don't block again
if [[ "$stop_hook_active" == "true" ]]; then
  echo '{"decision": undefined}'
  exit 0
fi

# Your logic here
if [ tests_passing ]; then
  echo '{"decision": "approve", "reason": "Tests pass"}'
else
  echo '{"decision": "block", "reason": "Tests failing"}'
fi
```

Or in prompt hooks:
```json
{
  "prompt": "Evaluate stopping: $ARGUMENTS\n\nIMPORTANT: If stop_hook_active is true, return {\"decision\": undefined}\n\nOtherwise check if tasks complete..."
}
```

---

## Hook Output Not Visible

### Symptom
Hook runs but output not shown to user.

### Cause
`suppressOutput: true` or output goes to stderr.

### Solutions

**Don't suppress output**:
```json
{
  "decision": "approve",
  "reason": "ok",
  "suppressOutput": false
}
```

**Use systemMessage**:
```json
{
  "decision": "approve",
  "reason": "ok",
  "systemMessage": "This message will be shown to user"
}
```

**Write to stdout, not stderr**:
```bash
echo "This is shown" >&1
echo "This is hidden" >&2
```

---

## Permission Errors

### Symptom
Hook script can't read files or execute commands.

### Solutions

**Make script executable**:
```bash
chmod +x /path/to/hook.sh
```

**Check file ownership**:
```bash
ls -l /path/to/hook.sh
chown $USER /path/to/hook.sh
```

**Use absolute paths**:
```bash
# Instead of
command="./script.sh"

# Use
command="$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh"
```

---

## Hook Timeouts

### Symptom
```
[DEBUG] Hook command timed out after 60000ms
```

### Solutions

**Increase timeout**:
```json
{
  "type": "command",
  "command": "/path/to/slow-script.sh",
  "timeout": 300000  // 5 minutes
}
```

**Optimize script**:
- Reduce unnecessary operations
- Cache results when possible
- Run expensive operations in background

**Run in background**:
```bash
#!/bin/bash
# Start long operation in background
/path/to/long-operation.sh &

# Return immediately
echo '{"decision": "approve", "reason": "ok"}'
```

---

## Matcher Conflicts

### Symptom
Multiple hooks triggering when only one expected.

### Cause
Tool name matches multiple matchers.

### Diagnostic
```
[DEBUG] Matched 3 hooks for query "Bash"
```

### Solutions

**Be more specific**:
```json
// Instead of
{"matcher": ".*"}  // Matches everything

// Use
{"matcher": "Bash"}  // Exact match
```

**Check overlapping patterns**:
```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Bash", ...},        // Matches Bash
      {"matcher": "Bash.*", ...},      // Also matches Bash!
      {"matcher": ".*", ...}           // Also matches everything!
    ]
  }
}
```

Remove overlaps or make them mutually exclusive.

---

## Environment Variables Not Working

### Symptom
`$CLAUDE_PROJECT_DIR` or other variables are empty.

### Solutions

**Check variable spelling**:
- `$CLAUDE_PROJECT_DIR` (correct)
- `$CLAUDE_PROJECT_ROOT` (wrong)

**Use double quotes**:
```json
{
  "command": "$CLAUDE_PROJECT_DIR/hooks/script.sh"
}
```

**In shell scripts, use from input**:
```bash
#!/bin/bash
input=$(cat)
cwd=$(echo "$input" | jq -r '.cwd')
cd "$cwd" || exit 1
```

---

## Debugging Workflow

**Step 1**: Enable debug mode
```bash
claude --debug
```

**Step 2**: Look for hook execution logs
```
[DEBUG] Executing hooks for PreToolUse:Bash
[DEBUG] Found 1 hook matchers
[DEBUG] Executing hook command: /path/to/script.sh
[DEBUG] Hook command completed with status 0
```

**Step 3**: Test hook in isolation
```bash
echo '{"test":"data"}' | /path/to/hook.sh
```

**Step 4**: Check script with `set -x`
```bash
#!/bin/bash
set -x  # Print each command before executing
# ... your script
```

**Step 5**: Add logging
```bash
#!/bin/bash
echo "Hook started" >> /tmp/hook-debug.log
input=$(cat)
echo "Input: $input" >> /tmp/hook-debug.log
# ... your logic
echo "Decision: $decision" >> /tmp/hook-debug.log
```

**Step 6**: Verify JSON output
```bash
echo '{"decision":"approve","reason":"test"}' | jq .
```

If `jq` fails, JSON is invalid.
