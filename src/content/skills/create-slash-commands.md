---
title: "Create Slash Commands"
description: "Expert guidance for creating Claude Code slash commands. Use when working with slash commands, creating custom commands, understanding command structure, or learning YAML configuration."
category: "development"
source: "community"
author: "Community"
tags: ["create", "slash", "commands"]
date: 2026-03-20
---

<objective>
Create effective slash commands for Claude Code that enable users to trigger reusable prompts with `/command-name` syntax. Slash commands expand as prompts in the current conversation, allowing teams to standardize workflows and operations. This skill teaches you to structure commands with XML tags, YAML frontmatter, dynamic context loading, and intelligent argument handling.
</objective>

<quick_start>

<workflow>
1. Create `.claude/commands/` directory (project) or use `~/.claude/commands/` (personal)
2. Create `command-name.md` file
3. Add YAML frontmatter (at minimum: `description`)
4. Write command prompt
5. Test with `/command-name [args]`
</workflow>

<example>
**File**: `.claude/commands/optimize.md`

```markdown
---
description: Analyze this code for performance issues and suggest optimizations
---

Analyze the performance of this code and suggest three specific optimizations:
```

**Usage**: `/optimize`

Claude receives the expanded prompt and analyzes the code in context.
</example>
</quick_start>

<xml_structure>
All generated slash commands should use XML tags in the body (after YAML frontmatter) for clarity and consistency.

<required_tags>

**`<objective>`** - What the command does and why it matters
```markdown
<objective>
What needs to happen and why this matters.
Context about who uses this and what it accomplishes.
</objective>
```

**`<process>` or `<steps>`** - How to execute the command
```markdown
<process>
Sequential steps to accomplish the objective:
1. First step
2. Second step
3. Final step
</process>
```

**`<success_criteria>`** - How to know the command succeeded
```markdown
<success_criteria>
Clear, measurable criteria for successful completion.
</success_criteria>
```
</required_tags>

<conditional_tags>

**`<context>`** - When loading dynamic state or files
```markdown
<context>
Current state: ! `git status`
Relevant files: @ package.json
</context>
```
(Note: Remove the space after @ in actual usage)

**`<verification>`** - When producing artifacts that need checking
```markdown
<verification>
Before completing, verify:
- Specific test or check to perform
- How to confirm it works
</verification>
```

**`<testing>`** - When running tests is part of the workflow
```markdown
<testing>
Run tests: ! `npm test`
Check linting: ! `npm run lint`
</testing>
```

**`<output>`** - When creating/modifying specific files
```markdown
<output>
Files created/modified:
- `./path/to/file.ext` - Description
</output>
```
</conditional_tags>

<structure_example>

```markdown
---
name: example-command
description: Does something useful
argument-hint: [input]
---

<objective>
Process $ARGUMENTS to accomplish [goal].

This helps [who] achieve [outcome].
</objective>

<context>
Current state: ! `relevant command`
Files: @ relevant/files
</context>

<process>
1. Parse $ARGUMENTS
2. Execute operation
3. Verify results
</process>

<success_criteria>
- Operation completed without errors
- Output matches expected format
</success_criteria>
```
</structure_example>

<intelligence_rules>

**Simple commands** (single operation, no artifacts):
- Required: `<objective>`, `<process>`, `<success_criteria>`
- Example: `/check-todos`, `/first-principles`

**Complex commands** (multi-step, produces artifacts):
- Required: `<objective>`, `<process>`, `<success_criteria>`
- Add: `<context>` (if loading state), `<verification>` (if creating files), `<output>` (what gets created)
- Example: `/commit`, `/create-prompt`, `/run-prompt`

**Commands with dynamic arguments**:
- Use `$ARGUMENTS` in `<objective>` or `<process>` tags
- Include `argument-hint` in frontmatter
- Make it clear what the arguments are for

**Commands that produce files**:
- Always include `<output>` tag specifying what gets created
- Always include `<verification>` tag with checks to perform

**Commands that run tests/builds**:
- Include `<testing>` tag with specific commands
- Include pass/fail criteria in `<success_criteria>`
</intelligence_rules>
</xml_structure>

<arguments_intelligence>
The skill should intelligently determine whether a slash command needs arguments.

<commands_that_need_arguments>

**User provides specific input:**
- `/fix-issue [issue-number]` - Needs issue number
- `/review-pr [pr-number]` - Needs PR number
- `/optimize [file-path]` - Needs file to optimize
- `/commit [type]` - Needs commit type (optional)

**Pattern:** Task operates on user-specified data

Include `argument-hint: [description]` in frontmatter and reference `$ARGUMENTS` in the body.
</commands_that_need_arguments>

<commands_without_arguments>

**Self-contained procedures:**
- `/check-todos` - Operates on known file (TO-DOS.md)
- `/first-principles` - Operates on current conversation
- `/whats-next` - Analyzes current context

**Pattern:** Task operates on implicit context (current conversation, known files, project state)

Omit `argument-hint` and don't reference `$ARGUMENTS`.
</commands_without_arguments>

<incorporating_arguments>

**In `<objective>` tag:**
```markdown
<objective>
Fix issue #$ARGUMENTS following project conventions.

This ensures bugs are resolved systematically with proper testing.
</objective>
```

**In `<process>` tag:**
```markdown
<process>
1. Understand issue #$ARGUMENTS from issue tracker
2. Locate relevant code
3. Implement fix
4. Add tests
</process>
```

**In `<context>` tag:**
```markdown
<context>
Issue details: @ issues/$ARGUMENTS.md
Related files: ! `grep -r "TODO.*$ARGUMENTS" src/`
</context>
```
(Note: Remove the space after the exclamation mark in actual usage)
</incorporating_arguments>

<positional_arguments>

For structured input, use `$1`, `$2`, `$3`:

```markdown
---
argument-hint: <pr-number> <priority> <assignee>
---

<objective>
Review PR #$1 with priority $2 and assign to $3.
</objective>
```

**Usage:** `/review-pr 456 high alice`
</positional_arguments>
</arguments_intelligence>

<file_structure>

**Project commands**: `.claude/commands/`
- Shared with team via version control
- Shows `(project)` in `/help` list

**Personal commands**: `~/.claude/commands/`
- Available across all your projects
- Shows `(user)` in `/help` list

**File naming**: `command-name.md` → invoked as `/command-name`
</file_structure>

<yaml_frontmatter>

<field name="description">
**Required** - Describes what the command does

```yaml
description: Analyze this code for performance issues and suggest optimizations
```

Shown in the `/help` command list.
</field>

<field name="allowed-tools">
**Optional** - Restricts which tools Claude can use

```yaml
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```

**Formats**:
- Array: `allowed-tools: [Read, Edit, Write]`
- Single tool: `allowed-tools: SequentialThinking`
- Bash restrictions: `allowed-tools: Bash(git add:*)`

If omitted: All tools available
</field>
</yaml_frontmatter>

<arguments>
<all_arguments_string>

**Command file**: `.claude/commands/fix-issue.md`
```markdown
---
description: Fix issue following coding standards
---

Fix issue #$ARGUMENTS following our coding standards
```

**Usage**: `/fix-issue 123 high-priority`

**Claude receives**: "Fix issue #123 high-priority following our coding standards"
</all_arguments_string>

<positional_arguments_syntax>

**Command file**: `.claude/commands/review-pr.md`
```markdown
---
description: Review PR with priority and assignee
---

Review PR #$1 with priority $2 and assign to $3
```

**Usage**: `/review-pr 456 high alice`

**Claude receives**: "Review PR #456 with priority high and assign to alice"

See [references/arguments.md](references/arguments.md) for advanced patterns.
</positional_arguments_syntax>
</arguments>

<dynamic_context>

Execute bash commands before the prompt using the exclamation mark prefix directly before backticks (no space between).

**Note:** Examples below show a space after the exclamation mark to prevent execution during skill loading. In actual slash commands, remove the space.

Example:

```markdown
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Context

- Current git status: ! `git status`
- Current git diff: ! `git diff HEAD`
- Current branch: ! `git branch --show-current`
- Recent commits: ! `git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

The bash commands execute and their output is included in the expanded prompt.
</dynamic_context>

<file_references>

Use `@` prefix to reference specific files:

```markdown
---
description: Review implementation
---

Review the implementation in @ src/utils/helpers.js
```
(Note: Remove the space after @ in actual usage)

Claude can access the referenced file's contents.
</file_references>

<best_practices>

**1. Always use XML structure**
```yaml
# All slash commands should have XML-structured bodies
```

After frontmatter, use XML tags:
- `<objective>` - What and why (always)
- `<process>` - How to do it (always)
- `<success_criteria>` - Definition of done (always)
- Additional tags as needed (see xml_structure section)

**2. Clear descriptions**
```yaml
# Good
description: Analyze this code for performance issues and suggest optimizations

# Bad
description: Optimize stuff
```

**3. Use dynamic context for state-dependent tasks**
```markdown
Current git status: ! `git status`
Files changed: ! `git diff --name-only`
```

**4. Restrict tools when appropriate**
```yaml
# For git commands - prevent running arbitrary bash
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)

# For analysis - thinking only
allowed-tools: SequentialThinking
```

**5. Use $ARGUMENTS for flexibility**
```markdown
Find and fix issue #$ARGUMENTS
```

**6. Reference relevant files**
```markdown
Review @ package.json for dependencies
Analyze @ src/database/* for schema
```
(Note: Remove the space after @ in actual usage)
</best_practices>

<common_patterns>

**Simple analysis command**:
```markdown
---
description: Review this code for security vulnerabilities
---

<objective>
Review code for security vulnerabilities and suggest fixes.
</objective>

<process>
1. Scan code for common vulnerabilities (XSS, SQL injection, etc.)
2. Identify specific issues with line numbers
3. Suggest remediation for each issue
</process>

<success_criteria>
- All major vulnerability types checked
- Specific issues identified with locations
- Actionable fixes provided
</success_criteria>
```

**Git workflow with context**:
```markdown
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

<objective>
Create a git commit for current changes following repository conventions.
</objective>

<context>
- Current status: ! `git status`
- Changes: ! `git diff HEAD`
- Recent commits: ! `git log --oneline -5`
</context>

<process>
1. Review staged and unstaged changes
2. Stage relevant files
3. Write commit message following recent commit style
4. Create commit
</process>

<success_criteria>
- All relevant changes staged
- Commit message follows repository conventions
- Commit created successfully
</success_criteria>
```

**Parameterized command**:
```markdown
---
description: Fix issue following coding standards
argument-hint: [issue-number]
---

<objective>
Fix issue #$ARGUMENTS following project coding standards.

This ensures bugs are resolved systematically with proper testing.
</objective>

<process>
1. Understand the issue described in ticket #$ARGUMENTS
2. Locate the relevant code in codebase
3. Implement a solution that addresses root cause
4. Add appropriate tests
5. Verify fix resolves the issue
</process>

<success_criteria>
- Issue fully understood and addressed
- Solution follows coding standards
- Tests added and passing
- No regressions introduced
</success_criteria>
```

**File-specific command**:
```markdown
---
description: Optimize code performance
argument-hint: [file-path]
---

<objective>
Analyze performance of @ $ARGUMENTS and suggest specific optimizations.

This helps improve application performance through targeted improvements.
</objective>

<process>
1. Review code in @ $ARGUMENTS for performance issues
2. Identify bottlenecks and inefficiencies
3. Suggest three specific optimizations with rationale
4. Estimate performance impact of each
</process>

<success_criteria>
- Performance issues clearly identified
- Three concrete optimizations suggested
- Implementation guidance provided
- Performance impact estimated
</success_criteria>
```

**Usage**: `/optimize src/utils/helpers.js`

See [references/patterns.md](references/patterns.md) for more examples.
</common_patterns>

<reference_guides>

**Arguments reference**: [references/arguments.md](references/arguments.md)
- $ARGUMENTS variable
- Positional arguments ($1, $2, $3)
- Parsing strategies
- Examples from official docs

**Patterns reference**: [references/patterns.md](references/patterns.md)
- Git workflows
- Code analysis
- File operations
- Security reviews
- Examples from official docs

**Tool restrictions**: [references/tool-restrictions.md](references/tool-restrictions.md)
- Bash command patterns
- Security best practices
- When to restrict tools
- Examples from official docs
</reference_guides>

<generation_protocol>

1. **Analyze the user's request**:
   - What is the command's purpose?
   - Does it need user input ($ARGUMENTS)?
   - Does it produce files or artifacts?
   - Does it require verification or testing?
   - Is it simple (single-step) or complex (multi-step)?

2. **Create frontmatter**:
   ```yaml
   ---
   name: command-name
   description: Clear description of what it does
   argument-hint: [input] # Only if arguments needed
   allowed-tools: [...] # Only if tool restrictions needed
   ---
   ```

3. **Create XML-structured body**:

   **Always include:**
   - `<objective>` - What and why
   - `<process>` - How to do it (numbered steps)
   - `<success_criteria>` - Definition of done

   **Include when relevant:**
   - `<context>` - Dynamic state (! `commands`) or file references (@ files)
   - `<verification>` - Checks to perform if creating artifacts
   - `<testing>` - Test commands if tests are part of workflow
   - `<output>` - Files created/modified

4. **Integrate $ARGUMENTS properly**:
   - If user input needed: Add `argument-hint` and use `$ARGUMENTS` in tags
   - If self-contained: Omit `argument-hint` and `$ARGUMENTS`

5. **Apply intelligence**:
   - Simple commands: Keep it concise (objective + process + success criteria)
   - Complex commands: Add context, verification, testing as needed
   - Don't over-engineer simple commands
   - Don't under-specify complex commands

6. **Save the file**:
   - Project: `.claude/commands/command-name.md`
   - Personal: `~/.claude/commands/command-name.md`
</generation_protocol>

<success_criteria>
A well-structured slash command meets these criteria:

**YAML Frontmatter**:
- `description` field is clear and concise
- `argument-hint` present if command accepts arguments
- `allowed-tools` specified if tool restrictions needed

**XML Structure**:
- All three required tags present: `<objective>`, `<process>`, `<success_criteria>`
- Conditional tags used appropriately based on complexity
- No raw markdown headings in body
- All XML tags properly closed

**Arguments Handling**:
- `$ARGUMENTS` used when command operates on user-specified data
- Positional arguments (`$1`, `$2`, etc.) used when structured input needed
- No `$ARGUMENTS` reference for self-contained commands

**Functionality**:
- Command expands correctly when invoked
- Dynamic context loads properly (bash commands, file references)
- Tool restrictions prevent unauthorized operations
- Command accomplishes intended purpose reliably

**Quality**:
- Clear, actionable instructions in `<process>` tag
- Measurable completion criteria in `<success_criteria>`
- Appropriate level of detail (not over-engineered for simple tasks)
- Examples provided when beneficial
</success_criteria>

---

## Reference: Arguments

# Arguments Reference

Official documentation examples for using arguments in slash commands.

## $ARGUMENTS - All Arguments

**Source**: Official Claude Code documentation

Captures all arguments as a single concatenated string.

### Basic Example

**Command file**: `.claude/commands/fix-issue.md`
```markdown
---
description: Fix issue following coding standards
---

Fix issue #$ARGUMENTS following our coding standards
```

**Usage**:
```
/fix-issue 123 high-priority
```

**Claude receives**:
```
Fix issue #123 high-priority following our coding standards
```

### Multi-Step Workflow Example

**Command file**: `.claude/commands/fix-issue.md`
```markdown
---
description: Fix issue following coding standards
---

Fix issue #$ARGUMENTS. Follow these steps:

1. Understand the issue described in the ticket
2. Locate the relevant code in our codebase
3. Implement a solution that addresses the root cause
4. Add appropriate tests
5. Prepare a concise PR description
```

**Usage**:
```
/fix-issue 456
```

**Claude receives the full prompt** with "456" replacing $ARGUMENTS.

## Positional Arguments - $1, $2, $3

**Source**: Official Claude Code documentation

Access specific arguments individually.

### Example

**Command file**: `.claude/commands/review-pr.md`
```markdown
---
description: Review PR with priority and assignee
---

Review PR #$1 with priority $2 and assign to $3
```

**Usage**:
```
/review-pr 456 high alice
```

**Claude receives**:
```
Review PR #456 with priority high and assign to alice
```

- `$1` becomes `456`
- `$2` becomes `high`
- `$3` becomes `alice`

## Argument Patterns from Official Docs

### Pattern 1: File Reference with Argument

**Command**:
```markdown
---
description: Optimize code performance
---

Analyze the performance of this code and suggest three specific optimizations:

@ $ARGUMENTS
```

**Usage**:
```
/optimize src/utils/helpers.js
```

References the file specified in the argument.

### Pattern 2: Issue Tracking

**Command**:
```markdown
---
description: Find and fix issue
---

Find and fix issue #$ARGUMENTS.

Follow these steps:
1. Understand the issue described in the ticket
2. Locate the relevant code in our codebase
3. Implement a solution that addresses the root cause
4. Add appropriate tests
5. Prepare a concise PR description
```

**Usage**:
```
/fix-issue 789
```

### Pattern 3: Code Review with Context

**Command**:
```markdown
---
description: Review PR with context
---

Review PR #$1 with priority $2 and assign to $3

Context from git:
- Changes: ! `gh pr diff $1`
- Status: ! `gh pr view $1 --json state`
```

**Usage**:
```
/review-pr 123 critical bob
```

Combines positional arguments with dynamic bash execution.

## Best Practices

### Use $ARGUMENTS for Simple Commands

When you just need to pass a value through:
```markdown
Fix issue #$ARGUMENTS
Optimize @ $ARGUMENTS
Summarize $ARGUMENTS
```

### Use Positional Arguments for Structure

When different arguments have different meanings:
```markdown
Review PR #$1 with priority $2 and assign to $3
Deploy $1 to $2 environment with tag $3
```

### Provide Clear Descriptions

Help users understand what arguments are expected:
```yaml
# Good
description: Fix issue following coding standards (usage: /fix-issue <issue-number>)

# Better - if using argument-hint field
description: Fix issue following coding standards
argument-hint: <issue-number> [priority]
```

## Empty Arguments

Commands work with or without arguments:

**Command**:
```markdown
---
description: Analyze code for issues
---

Analyze this code for issues: $ARGUMENTS

If no specific file provided, analyze the current context.
```

**Usage 1**: `/analyze src/app.js`
**Usage 2**: `/analyze` (analyzes current conversation context)

## Combining with Other Features

### Arguments + Dynamic Context

```markdown
---
description: Review changes for issue
---

Issue #$ARGUMENTS

Recent changes:
- Status: ! `git status`
- Diff: ! `git diff`

Review the changes related to this issue.
```

### Arguments + File References

```markdown
---
description: Compare files
---

Compare @ $1 with @ $2 and highlight key differences.
```

**Usage**: `/compare src/old.js src/new.js`

### Arguments + Tool Restrictions

```markdown
---
description: Commit changes for issue
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

Create commit for issue #$ARGUMENTS

Status: ! `git status`
Changes: ! `git diff HEAD`
```

## Notes

- Arguments are whitespace-separated by default
- Quote arguments containing spaces: `/command "argument with spaces"`
- Arguments are passed as-is (no special parsing)
- Empty arguments are replaced with empty string

---

## Reference: Patterns

# Command Patterns Reference

Verified patterns from official Claude Code documentation.

## Git Workflow Patterns

### Pattern: Commit with Full Context

**Source**: Official Claude Code documentation

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

<objective>
Create a git commit for current changes following repository conventions.
</objective>

<context>
- Current git status: ! `git status`
- Current git diff (staged and unstaged changes): ! `git diff HEAD`
- Current branch: ! `git branch --show-current`
- Recent commits: ! `git log --oneline -10`
</context>

<process>
1. Review staged and unstaged changes
2. Stage relevant files with git add
3. Write commit message following recent commit style
4. Create commit
</process>

<success_criteria>
- All relevant changes staged
- Commit message follows repository conventions
- Commit created successfully
</success_criteria>
```

**Key features**:
- Tool restrictions prevent running arbitrary bash commands
- Dynamic context loaded via the exclamation mark prefix before backticks
- Git state injected before prompt execution

### Pattern: Simple Git Commit

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

<objective>
Create a commit for current changes.
</objective>

<context>
Current changes: ! `git status`
</context>

<process>
1. Review changes
2. Stage files
3. Create commit
</process>

<success_criteria>
- Changes committed successfully
</success_criteria>
```

## Code Analysis Patterns

### Pattern: Performance Optimization

**Source**: Official Claude Code documentation

**File**: `.claude/commands/optimize.md`
```markdown
---
description: Analyze the performance of this code and suggest three specific optimizations
---

<objective>
Analyze code performance and suggest three specific optimizations.

This helps improve application performance through targeted improvements.
</objective>

<process>
1. Review code in current conversation context
2. Identify bottlenecks and inefficiencies
3. Suggest three specific optimizations with rationale
4. Estimate performance impact of each
</process>

<success_criteria>
- Performance issues clearly identified
- Three concrete optimizations suggested
- Implementation guidance provided
- Performance impact estimated
</success_criteria>
```

**Usage**: `/optimize`

Claude analyzes code in the current conversation context.

### Pattern: Security Review

**File**: `.claude/commands/security-review.md`
```markdown
---
description: Review this code for security vulnerabilities
---

<objective>
Review code for security vulnerabilities and suggest fixes.
</objective>

<process>
1. Scan code for common vulnerabilities (XSS, SQL injection, CSRF, etc.)
2. Identify specific issues with line numbers
3. Assess severity of each vulnerability
4. Suggest remediation for each issue
</process>

<success_criteria>
- All major vulnerability types checked
- Specific issues identified with locations
- Severity levels assigned
- Actionable fixes provided
</success_criteria>
```

**Usage**: `/security-review`

### Pattern: File-Specific Analysis

```markdown
---
description: Optimize specific file
argument-hint: [file-path]
---

<objective>
Analyze performance of @ $ARGUMENTS and suggest three specific optimizations.

This helps improve application performance through targeted file improvements.
</objective>

<process>
1. Review code in @ $ARGUMENTS for performance issues
2. Identify bottlenecks and inefficiencies
3. Suggest three specific optimizations with rationale
4. Estimate performance impact of each
</process>

<success_criteria>
- File analyzed thoroughly
- Performance issues identified
- Three concrete optimizations suggested
- Implementation guidance provided
</success_criteria>
```

**Usage**: `/optimize src/utils/helpers.js`

References the specified file.

## Issue Tracking Patterns

### Pattern: Fix Issue with Workflow

**Source**: Official Claude Code documentation

```markdown
---
description: Find and fix issue following workflow
argument-hint: [issue-number]
---

<objective>
Find and fix issue #$ARGUMENTS following project workflow.

This ensures bugs are resolved systematically with proper testing and documentation.
</objective>

<process>
1. Understand the issue described in ticket #$ARGUMENTS
2. Locate the relevant code in codebase
3. Implement a solution that addresses the root cause
4. Add appropriate tests
5. Prepare a concise PR description
</process>

<success_criteria>
- Issue fully understood and addressed
- Solution addresses root cause
- Tests added and passing
- PR description clearly explains fix
</success_criteria>
```

**Usage**: `/fix-issue 123`

### Pattern: PR Review with Context

```markdown
---
description: Review PR with priority and assignment
argument-hint: <pr-number> <priority> <assignee>
---

<objective>
Review PR #$1 with priority $2 and assign to $3.

This ensures PRs are reviewed systematically with proper prioritization and assignment.
</objective>

<process>
1. Fetch PR #$1 details
2. Review code changes
3. Assess based on priority $2
4. Provide feedback
5. Assign to $3
</process>

<success_criteria>
- PR reviewed thoroughly
- Priority considered in review depth
- Constructive feedback provided
- Assigned to correct person
</success_criteria>
```

**Usage**: `/review-pr 456 high alice`

Uses positional arguments for structured input.

## File Operation Patterns

### Pattern: File Reference

**Source**: Official Claude Code documentation

```markdown
---
description: Review implementation
---

<objective>
Review the implementation in @ src/utils/helpers.js.

This ensures code quality and identifies potential improvements.
</objective>

<process>
1. Read @ src/utils/helpers.js
2. Analyze code structure and patterns
3. Check for best practices
4. Identify potential improvements
5. Suggest specific changes
</process>

<success_criteria>
- File reviewed thoroughly
- Code quality assessed
- Specific improvements identified
- Actionable suggestions provided
</success_criteria>
```

Uses `@` prefix to reference specific files.

### Pattern: Dynamic File Reference

```markdown
---
description: Review specific file
argument-hint: [file-path]
---

<objective>
Review the implementation in @ $ARGUMENTS.

This allows flexible file review based on user specification.
</objective>

<process>
1. Read @ $ARGUMENTS
2. Analyze code structure and patterns
3. Check for best practices
4. Identify potential improvements
5. Suggest specific changes
</process>

<success_criteria>
- File reviewed thoroughly
- Code quality assessed
- Specific improvements identified
- Actionable suggestions provided
</success_criteria>
```

**Usage**: `/review src/app.js`

File path comes from argument.

### Pattern: Multi-File Analysis

```markdown
---
description: Compare two files
argument-hint: <file1> <file2>
---

<objective>
Compare @ $1 with @ $2 and highlight key differences.

This helps understand changes and identify important variations between files.
</objective>

<process>
1. Read @ $1 and @ $2
2. Identify structural differences
3. Compare functionality and logic
4. Highlight key changes
5. Assess impact of differences
</process>

<success_criteria>
- Both files analyzed
- Key differences identified
- Impact of changes assessed
- Clear comparison provided
</success_criteria>
```

**Usage**: `/compare src/old.js src/new.js`

## Thinking-Only Patterns

### Pattern: Deep Analysis

```markdown
---
description: Analyze problem from first principles
allowed-tools: SequentialThinking
---

<objective>
Analyze the current problem from first principles.

This helps discover optimal solutions by stripping away assumptions and rebuilding from fundamental truths.
</objective>

<process>
1. Identify the core problem
2. Strip away all assumptions
3. Identify fundamental truths and constraints
4. Rebuild solution from first principles
5. Compare with current approach
</process>

<success_criteria>
- Problem analyzed from ground up
- Assumptions identified and questioned
- Solution rebuilt from fundamentals
- Novel insights discovered
</success_criteria>
```

Tool restriction ensures Claude only uses SequentialThinking.

### Pattern: Strategic Planning

```markdown
---
description: Plan implementation strategy
allowed-tools: SequentialThinking
argument-hint: [task description]
---

<objective>
Create a detailed implementation strategy for: $ARGUMENTS

This ensures complex tasks are approached systematically with proper planning.
</objective>

<process>
1. Break down task into phases
2. Identify dependencies between phases
3. Estimate complexity for each phase
4. Suggest optimal approach
5. Identify potential risks
</process>

<success_criteria>
- Task broken into clear phases
- Dependencies mapped
- Complexity estimated
- Optimal approach identified
- Risks and mitigations outlined
</success_criteria>
```

## Bash Execution Patterns

### Pattern: Dynamic Environment Loading

```markdown
---
description: Check project status
---

<objective>
Provide a comprehensive project health summary.

This helps understand current project state across git, dependencies, and tests.
</objective>

<context>
- Git: ! `git status --short`
- Node: ! `npm list --depth=0 2>/dev/null | head -20`
- Tests: ! `npm test -- --listTests 2>/dev/null | wc -l`
</context>

<process>
1. Analyze git status for uncommitted changes
2. Review npm dependencies for issues
3. Check test coverage
4. Identify potential problems
5. Provide actionable recommendations
</process>

<success_criteria>
- All metrics checked
- Current state clearly described
- Issues identified
- Recommendations provided
</success_criteria>
```

Multiple bash commands load environment state.

### Pattern: Conditional Execution

```markdown
---
description: Deploy if tests pass
allowed-tools: Bash(npm test:*), Bash(npm run deploy:*)
---

<objective>
Deploy to production only if all tests pass.

This ensures deployment safety through automated testing gates.
</objective>

<context>
Test results: ! `npm test`
</context>

<process>
1. Review test results
2. If all tests passed, proceed to deployment
3. If any tests failed, report failures and abort
4. Monitor deployment process
5. Confirm successful deployment
</process>

<success_criteria>
- All tests verified passing
- Deployment executed only on test success
- Deployment confirmed successful
- Or deployment aborted with clear failure reasons
</success_criteria>
```

## Multi-Step Workflow Patterns

### Pattern: Structured Workflow

```markdown
---
description: Complete feature development workflow
argument-hint: [feature description]
---

<objective>
Complete full feature development workflow for: $ARGUMENTS

This ensures features are developed systematically with proper planning, implementation, testing, and documentation.
</objective>

<process>
1. **Planning**
   - Review requirements
   - Design approach
   - Identify files to modify

2. **Implementation**
   - Write code
   - Add tests
   - Update documentation

3. **Review**
   - Run tests: ! `npm test`
   - Check lint: ! `npm run lint`
   - Verify changes: ! `git diff`

4. **Completion**
   - Create commit
   - Write PR description
</process>

<testing>
- Run tests: ! `npm test`
- Check lint: ! `npm run lint`
</testing>

<verification>
Before completing:
- All tests passing
- No lint errors
- Documentation updated
- Changes verified with git diff
</verification>

<success_criteria>
- Feature fully implemented
- Tests added and passing
- Code passes linting
- Documentation updated
- Commit created
- PR description written
</success_criteria>
```

## Command Chaining Patterns

### Pattern: Analysis → Action

```markdown
---
description: Analyze and fix performance issues
argument-hint: [file-path]
---

<objective>
Analyze and fix performance issues in @ $ARGUMENTS.

This provides end-to-end performance improvement from analysis through verification.
</objective>

<process>
1. Analyze @ $ARGUMENTS for performance issues
2. Identify top 3 most impactful optimizations
3. Implement the optimizations
4. Verify improvements with benchmarks
</process>

<verification>
Before completing:
- Benchmarks run showing performance improvement
- No functionality regressions
- Code quality maintained
</verification>

<success_criteria>
- Performance issues identified and fixed
- Measurable performance improvement
- Benchmarks confirm gains
- No regressions introduced
</success_criteria>
```

Sequential steps in single command.

## Tool Restriction Patterns

### Pattern: Git-Only Command

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*)
description: Git workflow command
---

<objective>
Perform git operations safely with tool restrictions.

This prevents running arbitrary bash commands while allowing necessary git operations.
</objective>

<context>
Current git state: ! `git status`
</context>

<process>
1. Review git status
2. Perform git operations
3. Verify changes
</process>

<success_criteria>
- Git operations completed successfully
- No arbitrary commands executed
- Repository state as expected
</success_criteria>
```

Prevents running non-git bash commands.

### Pattern: Read-Only Analysis

```markdown
---
allowed-tools: [Read, Grep, Glob]
description: Analyze codebase
argument-hint: [search pattern]
---

<objective>
Search codebase for pattern: $ARGUMENTS

This provides safe codebase analysis without modification or execution permissions.
</objective>

<process>
1. Use Grep to search for pattern across codebase
2. Analyze findings
3. Identify relevant files and code sections
4. Provide summary of results
</process>

<success_criteria>
- Pattern search completed
- All matches identified
- Relevant context provided
- No files modified
</success_criteria>
```

No write or execution permissions.

### Pattern: Specific Bash Commands

```markdown
---
allowed-tools: Bash(npm test:*), Bash(npm run lint:*)
description: Run project checks
---

<objective>
Run project quality checks (tests and linting).

This ensures code quality while restricting to specific npm scripts.
</objective>

<testing>
Tests: ! `npm test`
Lint: ! `npm run lint`
</testing>

<process>
1. Run tests and capture results
2. Run linting and capture results
3. Analyze both outputs
4. Report on pass/fail status
5. Provide specific failure details if any
</process>

<success_criteria>
- All tests passing
- No lint errors
- Clear report of results
- Or specific failures identified with details
</success_criteria>
```

Only allows specific npm scripts.

## Best Practices

### 1. Use Tool Restrictions for Safety

```yaml
# Git commands
allowed-tools: Bash(git add:*), Bash(git status:*)

# Analysis only
allowed-tools: [Read, Grep, Glob]

# Thinking only
allowed-tools: SequentialThinking
```

### 2. Load Dynamic Context When Needed

```markdown
Current state: ! `git status`
Recent activity: ! `git log --oneline -5`
```

### 3. Reference Files Explicitly

```markdown
Review @ package.json for dependencies
Check @ src/config/* for settings
```

### 4. Structure Complex Commands

```markdown
## Step 1: Analysis
[analysis prompt]

## Step 2: Implementation
[implementation prompt]

## Step 3: Verification
[verification prompt]
```

### 5. Use Arguments for Flexibility

```markdown
# Simple
Fix issue #$ARGUMENTS

# Positional
Review PR #$1 with priority $2

# File reference
Analyze @ $ARGUMENTS
```

## Anti-Patterns to Avoid

### ❌ No Description

```yaml
---
# Missing description field
---
```

### ❌ Overly Broad Tool Access

```yaml
# Git command with no restrictions
---
description: Create commit
---
```

Better:
```yaml
---
description: Create commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---
```

### ❌ Vague Instructions

```markdown
Do the thing for $ARGUMENTS
```

Better:
```markdown
Fix issue #$ARGUMENTS by:
1. Understanding the issue
2. Locating relevant code
3. Implementing solution
4. Adding tests
```

### ❌ Missing Context for State-Dependent Tasks

```markdown
Create a git commit
```

Better:
```markdown
Current changes: ! `git status`
Diff: ! `git diff`

Create a git commit for these changes
```

---

## Reference: Tool Restrictions

# Tool Restrictions Reference

Official documentation on restricting tool access in slash commands.

## Why Restrict Tools

Tool restrictions provide:
- **Security**: Prevent accidental destructive operations
- **Focus**: Limit scope for specialized commands
- **Safety**: Ensure commands only perform intended operations

## allowed-tools Field

**Location**: YAML frontmatter

**Format**: Array of tool names or patterns

**Default**: If omitted, all tools available

## Basic Patterns

### Array Format

```yaml
---
description: My command
allowed-tools: [Read, Edit, Write]
---
```

### Single Tool

```yaml
---
description: Thinking command
allowed-tools: SequentialThinking
---
```

## Bash Command Restrictions

**Source**: Official Claude Code documentation

Restrict bash commands to specific patterns using wildcards.

### Git-Only Commands

```yaml
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---
```

**Allows**:
- `git add <anything>`
- `git status <anything>`
- `git commit <anything>`

**Prevents**:
- `rm -rf`
- `curl <url>`
- Any non-git bash commands

### NPM Script Restrictions

```yaml
---
description: Run tests and lint
allowed-tools: Bash(npm test:*), Bash(npm run lint:*)
---
```

**Allows**:
- `npm test`
- `npm test -- --watch`
- `npm run lint`
- `npm run lint:fix`

**Prevents**:
- `npm install malicious-package`
- `npm run deploy`
- Other npm commands

### Multiple Bash Patterns

```yaml
---
description: Development workflow
allowed-tools: Bash(git status:*), Bash(npm test:*), Bash(npm run build:*)
---
```

Combines multiple bash command patterns.

## Common Tool Restriction Patterns

### Pattern 1: Git Workflows

**Use case**: Commands that create commits, check status, etc.

```yaml
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*)
---

Current status: ! `git status`
Changes: ! `git diff HEAD`

Create a commit for these changes.
```

**Security benefit**: Cannot accidentally run destructive commands like `rm -rf` or `curl malicious-site.com`

### Pattern 2: Read-Only Analysis

**Use case**: Commands that analyze code without modifying it

```yaml
---
description: Analyze codebase for pattern
allowed-tools: [Read, Grep, Glob]
---

Search codebase for: $ARGUMENTS
```

**Security benefit**: Cannot write files or execute code

### Pattern 3: Thinking-Only Commands

**Use case**: Deep analysis or planning without file operations

```yaml
---
description: Analyze problem from first principles
allowed-tools: SequentialThinking
---

Analyze the current problem from first principles.
```

**Focus benefit**: Claude focuses purely on reasoning, no file operations

### Pattern 4: Controlled File Operations

**Use case**: Commands that should only read/edit specific types

```yaml
---
description: Update documentation
allowed-tools: [Read, Edit(*.md)]
---

Update documentation in @ $ARGUMENTS
```

**Note**: File pattern restrictions may not be supported in all versions.

## Real Examples from Official Docs

### Example 1: Git Commit Command

**Source**: Official Claude Code documentation

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: ! `git status`
- Current git diff (staged and unstaged changes): ! `git diff HEAD`
- Current branch: ! `git branch --show-current`
- Recent commits: ! `git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

**Allowed bash commands**:
- `git add .`
- `git add file.js`
- `git status`
- `git status --short`
- `git commit -m "message"`
- `git commit --amend`

**Blocked commands**:
- `rm file.js`
- `curl https://malicious.com`
- `npm install`
- Any non-git commands

### Example 2: Code Review (No Restrictions)

```markdown
---
description: Review this code for security vulnerabilities
---

Review this code for security vulnerabilities:
```

**No allowed-tools field** = All tools available

Claude can:
- Read files
- Write files
- Execute bash commands
- Use any tool

**Use when**: Command needs full flexibility

## When to Restrict Tools

### ✅ Restrict when:

1. **Security-sensitive operations**
   ```yaml
   # Git operations only
   allowed-tools: Bash(git add:*), Bash(git status:*)
   ```

2. **Focused tasks**
   ```yaml
   # Deep thinking only
   allowed-tools: SequentialThinking
   ```

3. **Read-only analysis**
   ```yaml
   # No modifications
   allowed-tools: [Read, Grep, Glob]
   ```

4. **Specific bash commands**
   ```yaml
   # Only npm scripts
   allowed-tools: Bash(npm run test:*), Bash(npm run build:*)
   ```

### ❌ Don't restrict when:

1. **Command needs flexibility**
   - Complex workflows
   - Exploratory tasks
   - Multi-step operations

2. **Tool needs are unpredictable**
   - General problem-solving
   - Debugging unknown issues

3. **Already in safe environment**
   - Sandboxed execution
   - Non-production systems

## Best Practices

### 1. Use Wildcards for Command Families

```yaml
# Good - allows all git commands
allowed-tools: Bash(git *)

# Better - specific git operations
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)

# Best - minimal necessary permissions
allowed-tools: Bash(git status:*), Bash(git diff:*)
```

### 2. Combine Tool Types Appropriately

```yaml
# Analysis with optional git context
allowed-tools: [Read, Grep, Bash(git status:*)]
```

### 3. Test Restrictions

Create command and verify:
- Allowed operations work
- Blocked operations are prevented
- Error messages are clear

### 4. Document Why

```yaml
---
description: Create git commit (restricted to git commands only for security)
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---
```

## Tool Types

### File Operations
- `Read` - Read files
- `Write` - Write new files
- `Edit` - Modify existing files
- `Grep` - Search file contents
- `Glob` - Find files by pattern

### Execution
- `Bash(pattern:*)` - Execute bash commands matching pattern
- `SequentialThinking` - Reasoning tool

### Other
- `Task` - Invoke subagents
- `WebSearch` - Search the web
- `WebFetch` - Fetch web pages

## Security Patterns

### Pattern: Prevent Data Exfiltration

```yaml
---
description: Analyze code locally
allowed-tools: [Read, Grep, Glob, SequentialThinking]
# No Bash, WebFetch - cannot send data externally
---
```

### Pattern: Prevent Destructive Operations

```yaml
---
description: Review changes
allowed-tools: [Read, Bash(git diff:*), Bash(git log:*)]
# No Write, Edit, git reset, git push --force
---
```

### Pattern: Controlled Deployment

```yaml
---
description: Deploy to staging
allowed-tools: Bash(npm run deploy:staging), Bash(git push origin:staging)
# Cannot deploy to production accidentally
---
```

## Limitations

1. **Wildcard patterns** may vary by version
2. **File-specific restrictions** (like `Edit(*.md)`) may not be supported
3. **Cannot blacklist** - only whitelist
4. **All or nothing** for tool types - can't partially restrict

## Testing Tool Restrictions

### Verify Restrictions Work

1. Create command with restrictions
2. Try to use restricted tool
3. Confirm operation is blocked
4. Check error message

Example test:
```markdown
---
description: Test restrictions
allowed-tools: [Read]
---

Try to write a file - this should fail.
```

Expected: Write operations blocked with error message.
