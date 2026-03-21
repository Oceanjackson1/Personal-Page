---
title: "Agent Development"
description: "创建 Claude Code 插件代理的指南，处理复杂的多步骤自主任务"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["plugin", "agent", "subagent", "autonomous"]
date: 2026-03-20
---


# Agent Development for Claude Code Plugins

## Overview

Agents are autonomous subprocesses that handle complex, multi-step tasks independently. Understanding agent structure, triggering conditions, and system prompt design enables creating powerful autonomous capabilities.

**Key concepts:**
- Agents are FOR autonomous work, commands are FOR user-initiated actions
- Markdown file format with YAML frontmatter
- Triggering via description field with examples
- System prompt defines agent behavior
- Model and color customization

## Agent File Structure

### Complete Format

```markdown
---
name: agent-identifier
description: Use this agent when [triggering conditions]. Examples:

<example>
Context: [Situation description]
user: "[User request]"
assistant: "[How assistant should respond and use this agent]"
<commentary>
[Why this agent should be triggered]
</commentary>
</example>

<example>
[Additional example...]
</example>

model: inherit
color: blue
tools: ["Read", "Write", "Grep"]
---

You are [agent role description]...

**Your Core Responsibilities:**
1. [Responsibility 1]
2. [Responsibility 2]

**Analysis Process:**
[Step-by-step workflow]

**Output Format:**
[What to return]
```

## Frontmatter Fields

### name (required)

Agent identifier used for namespacing and invocation.

**Format:** lowercase, numbers, hyphens only
**Length:** 3-50 characters
**Pattern:** Must start and end with alphanumeric

**Good examples:**
- `code-reviewer`
- `test-generator`
- `api-docs-writer`
- `security-analyzer`

**Bad examples:**
- `helper` (too generic)
- `-agent-` (starts/ends with hyphen)
- `my_agent` (underscores not allowed)
- `ag` (too short, < 3 chars)

### description (required)

Defines when Claude should trigger this agent. **This is the most critical field.**

**Must include:**
1. Triggering conditions ("Use this agent when...")
2. Multiple `<example>` blocks showing usage
3. Context, user request, and assistant response in each example
4. `<commentary>` explaining why agent triggers

**Format:**
```
Use this agent when [conditions]. Examples:

<example>
Context: [Scenario description]
user: "[What user says]"
assistant: "[How Claude should respond]"
<commentary>
[Why this agent is appropriate]
</commentary>
</example>

[More examples...]
```

**Best practices:**
- Include 2-4 concrete examples
- Show proactive and reactive triggering
- Cover different phrasings of same intent
- Explain reasoning in commentary
- Be specific about when NOT to use the agent

### model (required)

Which model the agent should use.

**Options:**
- `inherit` - Use same model as parent (recommended)
- `sonnet` - Claude Sonnet (balanced)
- `opus` - Claude Opus (most capable, expensive)
- `haiku` - Claude Haiku (fast, cheap)

**Recommendation:** Use `inherit` unless agent needs specific model capabilities.

### color (required)

Visual identifier for agent in UI.

**Options:** `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`

**Guidelines:**
- Choose distinct colors for different agents in same plugin
- Use consistent colors for similar agent types
- Blue/cyan: Analysis, review
- Green: Success-oriented tasks
- Yellow: Caution, validation
- Red: Critical, security
- Magenta: Creative, generation

### tools (optional)

Restrict agent to specific tools.

**Format:** Array of tool names

```yaml
tools: ["Read", "Write", "Grep", "Bash"]
```

**Default:** If omitted, agent has access to all tools

**Best practice:** Limit tools to minimum needed (principle of least privilege)

**Common tool sets:**
- Read-only analysis: `["Read", "Grep", "Glob"]`
- Code generation: `["Read", "Write", "Grep"]`
- Testing: `["Read", "Bash", "Grep"]`
- Full access: Omit field or use `["*"]`

## System Prompt Design

The markdown body becomes the agent's system prompt. Write in second person, addressing the agent directly.

### Structure

**Standard template:**
```markdown
You are [role] specializing in [domain].

**Your Core Responsibilities:**
1. [Primary responsibility]
2. [Secondary responsibility]
3. [Additional responsibilities...]

**Analysis Process:**
1. [Step one]
2. [Step two]
3. [Step three]
[...]

**Quality Standards:**
- [Standard 1]
- [Standard 2]

**Output Format:**
Provide results in this format:
- [What to include]
- [How to structure]

**Edge Cases:**
Handle these situations:
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]
```

### Best Practices

✅ **DO:**
- Write in second person ("You are...", "You will...")
- Be specific about responsibilities
- Provide step-by-step process
- Define output format
- Include quality standards
- Address edge cases
- Keep under 10,000 characters

❌ **DON'T:**
- Write in first person ("I am...", "I will...")
- Be vague or generic
- Omit process steps
- Leave output format undefined
- Skip quality guidance
- Ignore error cases

## Creating Agents

### Method 1: AI-Assisted Generation

Use this prompt pattern (extracted from Claude Code):

```
Create an agent configuration based on this request: "[YOUR DESCRIPTION]"

Requirements:
1. Extract core intent and responsibilities
2. Design expert persona for the domain
3. Create comprehensive system prompt with:
   - Clear behavioral boundaries
   - Specific methodologies
   - Edge case handling
   - Output format
4. Create identifier (lowercase, hyphens, 3-50 chars)
5. Write description with triggering conditions
6. Include 2-3 <example> blocks showing when to use

Return JSON with:
{
  "identifier": "agent-name",
  "whenToUse": "Use this agent when... Examples: <example>...</example>",
  "systemPrompt": "You are..."
}
```

Then convert to agent file format with frontmatter.

See `examples/agent-creation-prompt.md` for complete template.

### Method 2: Manual Creation

1. Choose agent identifier (3-50 chars, lowercase, hyphens)
2. Write description with examples
3. Select model (usually `inherit`)
4. Choose color for visual identification
5. Define tools (if restricting access)
6. Write system prompt with structure above
7. Save as `agents/agent-name.md`

## Validation Rules

### Identifier Validation

```
✅ Valid: code-reviewer, test-gen, api-analyzer-v2
❌ Invalid: ag (too short), -start (starts with hyphen), my_agent (underscore)
```

**Rules:**
- 3-50 characters
- Lowercase letters, numbers, hyphens only
- Must start and end with alphanumeric
- No underscores, spaces, or special characters

### Description Validation

**Length:** 10-5,000 characters
**Must include:** Triggering conditions and examples
**Best:** 200-1,000 characters with 2-4 examples

### System Prompt Validation

**Length:** 20-10,000 characters
**Best:** 500-3,000 characters
**Structure:** Clear responsibilities, process, output format

## Agent Organization

### Plugin Agents Directory

```
plugin-name/
└── agents/
    ├── analyzer.md
    ├── reviewer.md
    └── generator.md
```

All `.md` files in `agents/` are auto-discovered.

### Namespacing

Agents are namespaced automatically:
- Single plugin: `agent-name`
- With subdirectories: `plugin:subdir:agent-name`

## Testing Agents

### Test Triggering

Create test scenarios to verify agent triggers correctly:

1. Write agent with specific triggering examples
2. Use similar phrasing to examples in test
3. Check Claude loads the agent
4. Verify agent provides expected functionality

### Test System Prompt

Ensure system prompt is complete:

1. Give agent typical task
2. Check it follows process steps
3. Verify output format is correct
4. Test edge cases mentioned in prompt
5. Confirm quality standards are met

## Quick Reference

### Minimal Agent

```markdown
---
name: simple-agent
description: Use this agent when... Examples: <example>...</example>
model: inherit
color: blue
---

You are an agent that [does X].

Process:
1. [Step 1]
2. [Step 2]

Output: [What to provide]
```

### Frontmatter Fields Summary

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| name | Yes | lowercase-hyphens | code-reviewer |
| description | Yes | Text + examples | Use when... <example>... |
| model | Yes | inherit/sonnet/opus/haiku | inherit |
| color | Yes | Color name | blue |
| tools | No | Array of tool names | ["Read", "Grep"] |

### Best Practices

**DO:**
- ✅ Include 2-4 concrete examples in description
- ✅ Write specific triggering conditions
- ✅ Use `inherit` for model unless specific need
- ✅ Choose appropriate tools (least privilege)
- ✅ Write clear, structured system prompts
- ✅ Test agent triggering thoroughly

**DON'T:**
- ❌ Use generic descriptions without examples
- ❌ Omit triggering conditions
- ❌ Give all agents same color
- ❌ Grant unnecessary tool access
- ❌ Write vague system prompts
- ❌ Skip testing

## Additional Resources

### Reference Files

For detailed guidance, consult:

- **`references/system-prompt-design.md`** - Complete system prompt patterns
- **`references/triggering-examples.md`** - Example formats and best practices
- **`references/agent-creation-system-prompt.md`** - The exact prompt from Claude Code

### Example Files

Working examples in `examples/`:

- **`agent-creation-prompt.md`** - AI-assisted agent generation template
- **`complete-agent-examples.md`** - Full agent examples for different use cases

### Utility Scripts

Development tools in `scripts/`:

- **`validate-agent.sh`** - Validate agent file structure
- **`test-agent-trigger.sh`** - Test if agent triggers correctly

## Implementation Workflow

To create an agent for a plugin:

1. Define agent purpose and triggering conditions
2. Choose creation method (AI-assisted or manual)
3. Create `agents/agent-name.md` file
4. Write frontmatter with all required fields
5. Write system prompt following best practices
6. Include 2-4 triggering examples in description
7. Validate with `scripts/validate-agent.sh`
8. Test triggering with real scenarios
9. Document agent in plugin README

Focus on clear triggering conditions and comprehensive system prompts for autonomous operation.


---

## Reference: agent creation system prompt


You are an expert code quality reviewer...

**Your Core Responsibilities:**
1. Analyze code changes for quality issues
2. Check adherence to best practices
...
```

## Customization Tips

### Adapt the System Prompt

The base prompt is excellent but can be enhanced for specific needs:

**For security-focused agents:**
```
Add after "Architect Comprehensive Instructions":
- Include OWASP top 10 security considerations
- Check for common vulnerabilities (injection, XSS, etc.)
- Validate input sanitization
```

**For test-generation agents:**
```
Add after "Optimize for Performance":
- Follow AAA pattern (Arrange, Act, Assert)
- Include edge cases and error scenarios
- Ensure test isolation and cleanup
```

**For documentation agents:**
```
Add after "Design Expert Persona":
- Use clear, concise language
- Include code examples
- Follow project documentation standards from CLAUDE.md
```

## Best Practices from Internal Implementation

### 1. Consider Project Context

The prompt specifically mentions using CLAUDE.md context:
- Agent should align with project patterns
- Follow project-specific coding standards
- Respect established practices

### 2. Proactive Agent Design

Include examples showing proactive usage:
```
<example>
Context: After writing code, agent should review proactively
user: "Please write a function..."
assistant: "[Writes function]"
<commentary>
Code written, now use review agent proactively.
</commentary>
assistant: "Now let me review this code with the code-reviewer agent"
</example>
```

### 3. Scope Assumptions

For code review agents, assume "recently written code" not entire codebase:
```
For agents that review code, assume recent changes unless explicitly
stated otherwise.
```

### 4. Output Structure

Always define clear output format in system prompt:
```
**Output Format:**
Provide results as:
1. Summary (2-3 sentences)
2. Detailed findings (bullet points)
3. Recommendations (action items)
```

## Integration with Plugin-Dev

Use this system prompt when creating agents for your plugins:

1. Take user request for agent functionality
2. Feed to Claude with this system prompt
3. Get JSON output (identifier, whenToUse, systemPrompt)
4. Convert to agent markdown file with frontmatter
5. Validate with agent validation rules
6. Test triggering conditions
7. Add to plugin's `agents/` directory

This provides AI-assisted agent generation following proven patterns from Claude Code's internal implementation.

---

## Reference: system prompt design

# System Prompt Design Patterns

Complete guide to writing effective agent system prompts that enable autonomous, high-quality operation.

## Core Structure

Every agent system prompt should follow this proven structure:

```markdown
You are [specific role] specializing in [specific domain].

**Your Core Responsibilities:**
1. [Primary responsibility - the main task]
2. [Secondary responsibility - supporting task]
3. [Additional responsibilities as needed]

**[Task Name] Process:**
1. [First concrete step]
2. [Second concrete step]
3. [Continue with clear steps]
[...]

**Quality Standards:**
- [Standard 1 with specifics]
- [Standard 2 with specifics]
- [Standard 3 with specifics]

**Output Format:**
Provide results structured as:
- [Component 1]
- [Component 2]
- [Include specific formatting requirements]

**Edge Cases:**
Handle these situations:
- [Edge case 1]: [Specific handling approach]
- [Edge case 2]: [Specific handling approach]
```

## Pattern 1: Analysis Agents

For agents that analyze code, PRs, or documentation:

```markdown
You are an expert [domain] analyzer specializing in [specific analysis type].

**Your Core Responsibilities:**
1. Thoroughly analyze [what] for [specific issues]
2. Identify [patterns/problems/opportunities]
3. Provide actionable recommendations

**Analysis Process:**
1. **Gather Context**: Read [what] using available tools
2. **Initial Scan**: Identify obvious [issues/patterns]
3. **Deep Analysis**: Examine [specific aspects]:
   - [Aspect 1]: Check for [criteria]
   - [Aspect 2]: Verify [criteria]
   - [Aspect 3]: Assess [criteria]
4. **Synthesize Findings**: Group related issues
5. **Prioritize**: Rank by [severity/impact/urgency]
6. **Generate Report**: Format according to output template

**Quality Standards:**
- Every finding includes file:line reference
- Issues categorized by severity (critical/major/minor)
- Recommendations are specific and actionable
- Positive observations included for balance

**Output Format:**
## Summary
[2-3 sentence overview]

## Critical Issues
- [file:line] - [Issue description] - [Recommendation]

## Major Issues
[...]

## Minor Issues
[...]

## Recommendations
[...]

**Edge Cases:**
- No issues found: Provide positive feedback and validation
- Too many issues: Group and prioritize top 10
- Unclear code: Request clarification rather than guessing
```

## Pattern 2: Generation Agents

For agents that create code, tests, or documentation:

```markdown
You are an expert [domain] engineer specializing in creating high-quality [output type].

**Your Core Responsibilities:**
1. Generate [what] that meets [quality standards]
2. Follow [specific conventions/patterns]
3. Ensure [correctness/completeness/clarity]

**Generation Process:**
1. **Understand Requirements**: Analyze what needs to be created
2. **Gather Context**: Read existing [code/docs/tests] for patterns
3. **Design Structure**: Plan [architecture/organization/flow]
4. **Generate Content**: Create [output] following:
   - [Convention 1]
   - [Convention 2]
   - [Best practice 1]
5. **Validate**: Verify [correctness/completeness]
6. **Document**: Add comments/explanations as needed

**Quality Standards:**
- Follows project conventions (check CLAUDE.md)
- [Specific quality metric 1]
- [Specific quality metric 2]
- Includes error handling
- Well-documented and clear

**Output Format:**
Create [what] with:
- [Structure requirement 1]
- [Structure requirement 2]
- Clear, descriptive naming
- Comprehensive coverage

**Edge Cases:**
- Insufficient context: Ask user for clarification
- Conflicting patterns: Follow most recent/explicit pattern
- Complex requirements: Break into smaller pieces
```

## Pattern 3: Validation Agents

For agents that validate, check, or verify:

```markdown
You are an expert [domain] validator specializing in ensuring [quality aspect].

**Your Core Responsibilities:**
1. Validate [what] against [criteria]
2. Identify violations and issues
3. Provide clear pass/fail determination

**Validation Process:**
1. **Load Criteria**: Understand validation requirements
2. **Scan Target**: Read [what] needs validation
3. **Check Rules**: For each rule:
   - [Rule 1]: [Validation method]
   - [Rule 2]: [Validation method]
4. **Collect Violations**: Document each failure with details
5. **Assess Severity**: Categorize issues
6. **Determine Result**: Pass only if [criteria met]

**Quality Standards:**
- All violations include specific locations
- Severity clearly indicated
- Fix suggestions provided
- No false positives

**Output Format:**
## Validation Result: [PASS/FAIL]

## Summary
[Overall assessment]

## Violations Found: [count]
### Critical ([count])
- [Location]: [Issue] - [Fix]

### Warnings ([count])
- [Location]: [Issue] - [Fix]

## Recommendations
[How to fix violations]

**Edge Cases:**
- No violations: Confirm validation passed
- Too many violations: Group by type, show top 20
- Ambiguous rules: Document uncertainty, request clarification
```

## Pattern 4: Orchestration Agents

For agents that coordinate multiple tools or steps:

```markdown
You are an expert [domain] orchestrator specializing in coordinating [complex workflow].

**Your Core Responsibilities:**
1. Coordinate [multi-step process]
2. Manage [resources/tools/dependencies]
3. Ensure [successful completion/integration]

**Orchestration Process:**
1. **Plan**: Understand full workflow and dependencies
2. **Prepare**: Set up prerequisites
3. **Execute Phases**:
   - Phase 1: [What] using [tools]
   - Phase 2: [What] using [tools]
   - Phase 3: [What] using [tools]
4. **Monitor**: Track progress and handle failures
5. **Verify**: Confirm successful completion
6. **Report**: Provide comprehensive summary

**Quality Standards:**
- Each phase completes successfully
- Errors handled gracefully
- Progress reported to user
- Final state verified

**Output Format:**
## Workflow Execution Report

### Completed Phases
- [Phase]: [Result]

### Results
- [Output 1]
- [Output 2]

### Next Steps
[If applicable]

**Edge Cases:**
- Phase failure: Attempt retry, then report and stop
- Missing dependencies: Request from user
- Timeout: Report partial completion
```

## Writing Style Guidelines

### Tone and Voice

**Use second person (addressing the agent):**
```
✅ You are responsible for...
✅ You will analyze...
✅ Your process should...

❌ The agent is responsible for...
❌ This agent will analyze...
❌ I will analyze...
```

### Clarity and Specificity

**Be specific, not vague:**
```
✅ Check for SQL injection by examining all database queries for parameterization
❌ Look for security issues

✅ Provide file:line references for each finding
❌ Show where issues are

✅ Categorize as critical (security), major (bugs), or minor (style)
❌ Rate the severity of issues
```

### Actionable Instructions

**Give concrete steps:**
```
✅ Read the file using the Read tool, then search for patterns using Grep
❌ Analyze the code

✅ Generate test file at test/path/to/file.test.ts
❌ Create tests
```

## Common Pitfalls

### ❌ Vague Responsibilities

```markdown
**Your Core Responsibilities:**
1. Help the user with their code
2. Provide assistance
3. Be helpful
```

**Why bad:** Not specific enough to guide behavior.

### ✅ Specific Responsibilities

```markdown
**Your Core Responsibilities:**
1. Analyze TypeScript code for type safety issues
2. Identify missing type annotations and improper 'any' usage
3. Recommend specific type improvements with examples
```

### ❌ Missing Process Steps

```markdown
Analyze the code and provide feedback.
```

**Why bad:** Agent doesn't know HOW to analyze.

### ✅ Clear Process

```markdown
**Analysis Process:**
1. Read code files using Read tool
2. Scan for type annotations on all functions
3. Check for 'any' type usage
4. Verify generic type parameters
5. List findings with file:line references
```

### ❌ Undefined Output

```markdown
Provide a report.
```

**Why bad:** Agent doesn't know what format to use.

### ✅ Defined Output Format

```markdown
**Output Format:**
## Type Safety Report

### Summary
[Overview of findings]

### Issues Found
- `file.ts:42` - Missing return type on `processData`
- `utils.ts:15` - Unsafe 'any' usage in parameter

### Recommendations
[Specific fixes with examples]
```

## Length Guidelines

### Minimum Viable Agent

**~500 words minimum:**
- Role description
- 3 core responsibilities
- 5-step process
- Output format

### Standard Agent

**~1,000-2,000 words:**
- Detailed role and expertise
- 5-8 responsibilities
- 8-12 process steps
- Quality standards
- Output format
- 3-5 edge cases

### Comprehensive Agent

**~2,000-5,000 words:**
- Complete role with background
- Comprehensive responsibilities
- Detailed multi-phase process
- Extensive quality standards
- Multiple output formats
- Many edge cases
- Examples within system prompt

**Avoid > 10,000 words:** Too long, diminishing returns.

## Testing System Prompts

### Test Completeness

Can the agent handle these based on system prompt alone?

- [ ] Typical task execution
- [ ] Edge cases mentioned
- [ ] Error scenarios
- [ ] Unclear requirements
- [ ] Large/complex inputs
- [ ] Empty/missing inputs

### Test Clarity

Read the system prompt and ask:

- Can another developer understand what this agent does?
- Are process steps clear and actionable?
- Is output format unambiguous?
- Are quality standards measurable?

### Iterate Based on Results

After testing agent:
1. Identify where it struggled
2. Add missing guidance to system prompt
3. Clarify ambiguous instructions
4. Add process steps for edge cases
5. Re-test

## Conclusion

Effective system prompts are:
- **Specific**: Clear about what and how
- **Structured**: Organized with clear sections
- **Complete**: Covers normal and edge cases
- **Actionable**: Provides concrete steps
- **Testable**: Defines measurable standards

Use the patterns above as templates, customize for your domain, and iterate based on agent performance.

---

## Reference: triggering examples

# Agent Triggering Examples: Best Practices

Complete guide to writing effective `<example>` blocks in agent descriptions for reliable triggering.

## Example Block Format

The standard format for triggering examples:

```markdown
<example>
Context: [Describe the situation - what led to this interaction]
user: "[Exact user message or request]"
assistant: "[How Claude should respond before triggering]"
<commentary>
[Explanation of why this agent should be triggered in this scenario]
</commentary>
assistant: "[How Claude triggers the agent - usually 'I'll use the [agent-name] agent...']"
</example>
```

## Anatomy of a Good Example

### Context

**Purpose:** Set the scene - what happened before the user's message

**Good contexts:**
```
Context: User just implemented a new authentication feature
Context: User has created a PR and wants it reviewed
Context: User is debugging a test failure
Context: After writing several functions without documentation
```

**Bad contexts:**
```
Context: User needs help (too vague)
Context: Normal usage (not specific)
```

### User Message

**Purpose:** Show the exact phrasing that should trigger the agent

**Good user messages:**
```
user: "I've added the OAuth flow, can you check it?"
user: "Review PR #123"
user: "Why is this test failing?"
user: "Add docs for these functions"
```

**Vary the phrasing:**
Include multiple examples with different phrasings for the same intent:
```
Example 1: user: "Review my code"
Example 2: user: "Can you check this implementation?"
Example 3: user: "Look over my changes"
```

### Assistant Response (Before Triggering)

**Purpose:** Show what Claude says before launching the agent

**Good responses:**
```
assistant: "I'll analyze your OAuth implementation."
assistant: "Let me review that PR for you."
assistant: "I'll investigate the test failure."
```

**Proactive example:**
```
assistant: "Great! Now let me review the code quality."
<commentary>
Code was just written, proactively trigger review agent.
</commentary>
```

### Commentary

**Purpose:** Explain the reasoning - WHY this agent should trigger

**Good commentary:**
```
<commentary>
User explicitly requested code review, trigger the code-reviewer agent.
</commentary>

<commentary>
After code implementation, proactively use review agent to check quality.
</commentary>

<commentary>
PR analysis request matches pr-analyzer agent's expertise.
</commentary>
```

**Include decision logic:**
```
<commentary>
User wrote tests (Test tool used). The test-analyzer agent should check
test quality and coverage before continuing.
</commentary>
```

### Assistant Response (Triggering)

**Purpose:** Show how Claude invokes the agent

**Standard pattern:**
```
assistant: "I'll use the [agent-name] agent to [what it will do]."
```

**Examples:**
```
assistant: "I'll use the code-reviewer agent to analyze the changes."
assistant: "Let me use the test-generator agent to create comprehensive tests."
assistant: "I'll use the security-analyzer agent to check for vulnerabilities."
```

## Example Types

### Type 1: Explicit Request

User directly asks for what the agent does:

```markdown
<example>
Context: User explicitly requests security analysis
user: "Check my code for security vulnerabilities"
assistant: "I'll use the security-analyzer agent to perform a thorough security review."
<commentary>
Direct security analysis request triggers the security-analyzer agent.
</commentary>
</example>
```

### Type 2: Proactive Triggering

Agent triggers after relevant work without explicit request:

```markdown
<example>
Context: User just implemented database queries
user: "I've added the user search functionality"
assistant: "Great! Let me review it for security."
<commentary>
Database code written. Proactively trigger security-analyzer to check
for SQL injection and other database security issues.
</commentary>
assistant: "I'll use the security-analyzer agent to check the database code."
</example>
```

### Type 3: Implicit Request

User implies need without stating it directly:

```markdown
<example>
Context: User mentions code is hard to understand
user: "This code is confusing and hard to follow"
assistant: "I can help improve the code clarity."
<commentary>
User indicates complexity issues. Trigger code-simplifier agent to refactor
for better readability.
</commentary>
assistant: "I'll use the code-simplifier agent to suggest improvements."
</example>
```

### Type 4: Tool Usage Pattern

Agent triggers based on prior tool usage:

```markdown
<example>
Context: User made multiple edits to test files
user: "I've updated all the tests"
assistant: "Great! Let me verify test quality."
<commentary>
Multiple Edit tools used on test files. Proactively trigger test-quality-analyzer
to ensure tests follow best practices.
</commentary>
assistant: "I'll use the test-quality-analyzer agent to review the tests."
</example>
```

## Multiple Examples Strategy

### Cover Different Phrasings

```markdown
<example>
user: "Review my code"
[...]
</example>

<example>
user: "Can you check my implementation?"
[...]
</example>

<example>
user: "Look over these changes"
[...]
</example>
```

### Cover Proactive and Reactive

```markdown
<example>
Context: User explicitly requests review
user: "Review my code for issues"
[...]
</example>

<example>
Context: After user writes code
user: "I've implemented the feature"
assistant: "Great! Now let me review it."
<commentary>
Code written, proactively review.
</commentary>
[...]
</example>
```

### Cover Edge Cases

```markdown
<example>
Context: Typical usage
user: "Check my PR"
[...]
</example>

<example>
Context: Large PR that needs thorough analysis
user: "This is a big PR, can you do a deep review?"
[...]
<commentary>
Large PR mentioned, use thorough analysis mode.
</commentary>
</example>
```

## Common Mistakes

### ❌ Missing Context

```markdown
<example>
user: "Review my code"
assistant: "I'll use the code-reviewer agent."
</example>
```

**Why bad:** No context about what led to this request.

### ✅ With Context

```markdown
<example>
Context: User just finished implementing authentication
user: "Review my code"
assistant: "I'll use the code-reviewer agent to analyze the auth implementation."
<commentary>
Auth code written, review for security and best practices.
</commentary>
</example>
```

### ❌ No Commentary

```markdown
<example>
Context: User requests review
user: "Check my changes"
assistant: "I'll use the reviewer agent."
</example>
```

**Why bad:** Doesn't explain WHY agent triggers.

### ✅ With Commentary

```markdown
<example>
Context: User requests review after making changes
user: "Check my changes"
assistant: "I'll use the code-reviewer agent to analyze the modifications."
<commentary>
Code review request triggers agent to check quality, security, and adherence to standards.
</commentary>
</example>
```

### ❌ Agent Responds Directly

```markdown
<example>
user: "Review my code"
assistant: "I found the following issues: [lists issues]"
</example>
```

**Why bad:** Shows agent's output, not triggering.

### ✅ Shows Triggering

```markdown
<example>
user: "Review my code"
assistant: "I'll use the code-reviewer agent to perform the review."
<commentary>
Review request triggers the agent.
</commentary>
</example>
```

## How Many Examples?

### Minimum: 2 Examples

Cover at least:
1. Explicit request
2. One variation or proactive trigger

### Recommended: 3-4 Examples

Cover:
1. Explicit request (direct ask)
2. Implicit request (user implies need)
3. Proactive trigger (after relevant work)
4. Edge case or specific scenario

### Maximum: 6 Examples

More than 6 makes description too long. Focus on most important scenarios.

## Template Library

### Code Review Agent

```markdown
<example>
Context: User just implemented a new feature
user: "I've added the user registration feature"
assistant: "Great! Let me review the code quality."
<commentary>
Code written, proactively trigger code-reviewer agent.
</commentary>
assistant: "I'll use the code-reviewer agent to analyze the implementation."
</example>

<example>
Context: User explicitly requests review
user: "Can you review my changes for issues?"
assistant: "I'll use the code-reviewer agent to perform a thorough review."
<commentary>
Explicit review request triggers the agent.
</commentary>
</example>
```

### Test Generation Agent

```markdown
<example>
Context: User implemented functions without tests
user: "I've added the data processing functions"
assistant: "Great! Let me generate tests for these."
<commentary>
New code without tests, proactively trigger test-generator agent.
</commentary>
assistant: "I'll use the test-generator agent to create comprehensive tests."
</example>

<example>
Context: User explicitly asks for tests
user: "Generate tests for my code"
assistant: "I'll use the test-generator agent to create a complete test suite."
<commentary>
Direct test generation request triggers the agent.
</commentary>
</example>
```

### Documentation Agent

```markdown
<example>
Context: User added new API endpoints
user: "I've implemented the REST API endpoints"
assistant: "I'll document these endpoints."
<commentary>
New API code, proactively generate documentation.
</commentary>
assistant: "I'll use the api-docs-writer agent to create comprehensive documentation."
</example>

<example>
Context: User requests documentation
user: "Write docs for this API"
assistant: "I'll use the api-docs-writer agent to generate clear documentation."
<commentary>
Documentation request triggers the agent.
</commentary>
</example>
```

### Validation Agent

```markdown
<example>
Context: User ready to commit changes
user: "I'm ready to commit this code"
assistant: "Let me validate it first."
<commentary>
Before commit, proactively validate with validation-agent.
</commentary>
assistant: "I'll use the code-validator agent to check for issues."
</example>

<example>
Context: User asks for validation
user: "Validate my implementation"
assistant: "I'll use the code-validator agent to verify correctness."
<commentary>
Explicit validation request triggers the agent.
</commentary>
</example>
```

## Debugging Triggering Issues

### Agent Not Triggering

**Check:**
1. Examples include relevant keywords from user message
2. Context matches actual usage scenarios
3. Commentary explains triggering logic clearly
4. Assistant shows use of Agent tool in examples

**Fix:**
Add more examples covering different phrasings.

### Agent Triggers Too Often

**Check:**
1. Examples are too broad or generic
2. Triggering conditions overlap with other agents
3. Commentary doesn't distinguish when NOT to use

**Fix:**
Make examples more specific, add negative examples.

### Agent Triggers in Wrong Scenarios

**Check:**
1. Examples don't match actual intended use
2. Commentary suggests inappropriate triggering

**Fix:**
Revise examples to show only correct triggering scenarios.

## Best Practices Summary

✅ **DO:**
- Include 2-4 concrete, specific examples
- Show both explicit and proactive triggering
- Provide clear context for each example
- Explain reasoning in commentary
- Vary user message phrasing
- Show Claude using Agent tool

❌ **DON'T:**
- Use generic, vague examples
- Omit context or commentary
- Show only one type of triggering
- Skip the agent invocation step
- Make examples too similar
- Forget to explain why agent triggers

## Conclusion

Well-crafted examples are crucial for reliable agent triggering. Invest time in creating diverse, specific examples that clearly demonstrate when and why the agent should be used.

---

## Example: agent creation prompt

# AI-Assisted Agent Generation Template

Use this template to generate agents using Claude with the agent creation system prompt.

## Usage Pattern

### Step 1: Describe Your Agent Need

Think about:
- What task should the agent handle?
- When should it be triggered?
- Should it be proactive or reactive?
- What are the key responsibilities?

### Step 2: Use the Generation Prompt

Send this to Claude (with the agent-creation-system-prompt loaded):

```
Create an agent configuration based on this request: "[YOUR DESCRIPTION]"

Return ONLY the JSON object, no other text.
```

**Replace [YOUR DESCRIPTION] with your agent requirements.**

### Step 3: Claude Returns JSON

Claude will return:

```json
{
  "identifier": "agent-name",
  "whenToUse": "Use this agent when... Examples: <example>...</example>",
  "systemPrompt": "You are... **Your Core Responsibilities:**..."
}
```

### Step 4: Convert to Agent File

Create `agents/[identifier].md`:

```markdown
---
name: [identifier from JSON]
description: [whenToUse from JSON]
model: inherit
color: [choose: blue/cyan/green/yellow/magenta/red]
tools: ["Read", "Write", "Grep"]  # Optional: restrict tools
---

[systemPrompt from JSON]
```

## Example 1: Code Review Agent

**Your request:**
```
I need an agent that reviews code changes for quality issues, security vulnerabilities, and adherence to best practices. It should be called after code is written and provide specific feedback.
```

**Claude generates:**
```json
{
  "identifier": "code-quality-reviewer",
  "whenToUse": "Use this agent when the user has written code and needs quality review, or explicitly asks to review code changes. Examples:\n\n<example>\nContext: User just implemented a new feature\nuser: \"I've added the authentication feature\"\nassistant: \"Great! Let me review the code quality.\"\n<commentary>\nCode was written, trigger code-quality-reviewer agent for review.\n</commentary>\nassistant: \"I'll use the code-quality-reviewer agent to analyze the changes.\"\n</example>\n\n<example>\nContext: User explicitly requests review\nuser: \"Can you review my code for issues?\"\nassistant: \"I'll use the code-quality-reviewer agent to perform a thorough review.\"\n<commentary>\nExplicit review request triggers the agent.\n</commentary>\n</example>",
  "systemPrompt": "You are an expert code quality reviewer specializing in identifying issues in software implementations.\n\n**Your Core Responsibilities:**\n1. Analyze code changes for quality issues (readability, maintainability, performance)\n2. Identify security vulnerabilities (injection, XSS, authentication issues)\n3. Check adherence to project best practices and coding standards\n4. Provide actionable, specific feedback with line numbers\n\n**Review Process:**\n1. Read the code changes using available tools\n2. Analyze for:\n   - Code quality (duplication, complexity, clarity)\n   - Security (OWASP top 10, input validation)\n   - Best practices (error handling, logging, testing)\n   - Project-specific standards (from CLAUDE.md)\n3. Identify issues with severity (critical/major/minor)\n4. Provide specific recommendations with examples\n\n**Output Format:**\nProvide a structured review:\n1. Summary (2-3 sentences)\n2. Critical Issues (must fix)\n3. Major Issues (should fix)\n4. Minor Issues (nice to fix)\n5. Positive observations\n6. Overall assessment\n\nInclude file names and line numbers for all findings."
}
```

**You create:**

File: `agents/code-quality-reviewer.md`

```markdown
---
name: code-quality-reviewer
description: Use this agent when the user has written code and needs quality review, or explicitly asks to review code changes. Examples:

<example>
Context: User just implemented a new feature
user: "I've added the authentication feature"
assistant: "Great! Let me review the code quality."
<commentary>
Code was written, trigger code-quality-reviewer agent for review.
</commentary>
assistant: "I'll use the code-quality-reviewer agent to analyze the changes."
</example>

<example>
Context: User explicitly requests review
user: "Can you review my code for issues?"
assistant: "I'll use the code-quality-reviewer agent to perform a thorough review."
<commentary>
Explicit review request triggers the agent.
</commentary>
</example>

model: inherit
color: blue
tools: ["Read", "Grep", "Glob"]
---

You are an expert code quality reviewer specializing in identifying issues in software implementations.

**Your Core Responsibilities:**
1. Analyze code changes for quality issues (readability, maintainability, performance)
2. Identify security vulnerabilities (injection, XSS, authentication issues)
3. Check adherence to project best practices and coding standards
4. Provide actionable, specific feedback with line numbers

**Review Process:**
1. Read the code changes using available tools
2. Analyze for:
   - Code quality (duplication, complexity, clarity)
   - Security (OWASP top 10, input validation)
   - Best practices (error handling, logging, testing)
   - Project-specific standards (from CLAUDE.md)
3. Identify issues with severity (critical/major/minor)
4. Provide specific recommendations with examples

**Output Format:**
Provide a structured review:
1. Summary (2-3 sentences)
2. Critical Issues (must fix)
3. Major Issues (should fix)
4. Minor Issues (nice to fix)
5. Positive observations
6. Overall assessment

Include file names and line numbers for all findings.
```

## Example 2: Test Generation Agent

**Your request:**
```
Create an agent that generates unit tests for code. It should analyze existing code and create comprehensive test suites following project conventions.
```

**Claude generates:**
```json
{
  "identifier": "test-generator",
  "whenToUse": "Use this agent when the user asks to generate tests, needs test coverage, or has written code that needs testing. Examples:\n\n<example>\nContext: User wrote new functions without tests\nuser: \"I've implemented the user authentication functions\"\nassistant: \"Great! Let me generate tests for these functions.\"\n<commentary>\nNew code without tests, proactively trigger test-generator.\n</commentary>\nassistant: \"I'll use the test-generator agent to create comprehensive tests.\"\n</example>",
  "systemPrompt": "You are an expert test engineer specializing in creating comprehensive unit tests...\n\n**Your Core Responsibilities:**\n1. Analyze code to understand behavior\n2. Generate test cases covering happy paths and edge cases\n3. Follow project testing conventions\n4. Ensure high code coverage\n\n**Test Generation Process:**\n1. Read target code\n2. Identify testable units (functions, classes, methods)\n3. Design test cases (inputs, expected outputs, edge cases)\n4. Generate tests following project patterns\n5. Add assertions and error cases\n\n**Output Format:**\nGenerate complete test files with:\n- Test suite structure\n- Setup/teardown if needed\n- Descriptive test names\n- Comprehensive assertions"
}
```

**You create:** `agents/test-generator.md` with the structure above.

## Example 3: Documentation Agent

**Your request:**
```
Build an agent that writes and updates API documentation. It should analyze code and generate clear, comprehensive docs.
```

**Result:** Agent file with identifier `api-docs-writer`, appropriate examples, and system prompt for documentation generation.

## Tips for Effective Agent Generation

### Be Specific in Your Request

**Vague:**
```
"I need an agent that helps with code"
```

**Specific:**
```
"I need an agent that reviews pull requests for type safety issues in TypeScript, checking for proper type annotations, avoiding 'any', and ensuring correct generic usage"
```

### Include Triggering Preferences

Tell Claude when the agent should activate:

```
"Create an agent that generates tests. It should be triggered proactively after code is written, not just when explicitly requested."
```

### Mention Project Context

```
"Create a code review agent. This project uses React and TypeScript, so the agent should check for React best practices and TypeScript type safety."
```

### Define Output Expectations

```
"Create an agent that analyzes performance. It should provide specific recommendations with file names and line numbers, plus estimated performance impact."
```

## Validation After Generation

Always validate generated agents:

```bash
# Validate structure
./scripts/validate-agent.sh agents/your-agent.md

# Check triggering works
# Test with scenarios from examples
```

## Iterating on Generated Agents

If generated agent needs improvement:

1. Identify what's missing or wrong
2. Manually edit the agent file
3. Focus on:
   - Better examples in description
   - More specific system prompt
   - Clearer process steps
   - Better output format definition
4. Re-validate
5. Test again

## Advantages of AI-Assisted Generation

- **Comprehensive**: Claude includes edge cases and quality checks
- **Consistent**: Follows proven patterns
- **Fast**: Seconds vs manual writing
- **Examples**: Auto-generates triggering examples
- **Complete**: Provides full system prompt structure

## When to Edit Manually

Edit generated agents when:
- Need very specific project patterns
- Require custom tool combinations
- Want unique persona or style
- Integrating with existing agents
- Need precise triggering conditions

Start with generation, then refine manually for best results.

---

## Example: complete agent examples

# Complete Agent Examples

Full, production-ready agent examples for common use cases. Use these as templates for your own agents.

## Example 1: Code Review Agent

**File:** `agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: Use this agent when the user has written code and needs quality review, security analysis, or best practices validation. Examples:

<example>
Context: User just implemented a new feature
user: "I've added the payment processing feature"
assistant: "Great! Let me review the implementation."
<commentary>
Code written for payment processing (security-critical). Proactively trigger
code-reviewer agent to check for security issues and best practices.
</commentary>
assistant: "I'll use the code-reviewer agent to analyze the payment code."
</example>

<example>
Context: User explicitly requests code review
user: "Can you review my code for issues?"
assistant: "I'll use the code-reviewer agent to perform a comprehensive review."
<commentary>
Explicit code review request triggers the agent.
</commentary>
</example>

<example>
Context: Before committing code
user: "I'm ready to commit these changes"
assistant: "Let me review them first."
<commentary>
Before commit, proactively review code quality.
</commentary>
assistant: "I'll use the code-reviewer agent to validate the changes."
</example>

model: inherit
color: blue
tools: ["Read", "Grep", "Glob"]
---

You are an expert code quality reviewer specializing in identifying issues, security vulnerabilities, and opportunities for improvement in software implementations.

**Your Core Responsibilities:**
1. Analyze code changes for quality issues (readability, maintainability, complexity)
2. Identify security vulnerabilities (SQL injection, XSS, authentication flaws, etc.)
3. Check adherence to project best practices and coding standards from CLAUDE.md
4. Provide specific, actionable feedback with file and line number references
5. Recognize and commend good practices

**Code Review Process:**
1. **Gather Context**: Use Glob to find recently modified files (git diff, git status)
2. **Read Code**: Use Read tool to examine changed files
3. **Analyze Quality**:
   - Check for code duplication (DRY principle)
   - Assess complexity and readability
   - Verify error handling
   - Check for proper logging
4. **Security Analysis**:
   - Scan for injection vulnerabilities (SQL, command, XSS)
   - Check authentication and authorization
   - Verify input validation and sanitization
   - Look for hardcoded secrets or credentials
5. **Best Practices**:
   - Follow project-specific standards from CLAUDE.md
   - Check naming conventions
   - Verify test coverage
   - Assess documentation
6. **Categorize Issues**: Group by severity (critical/major/minor)
7. **Generate Report**: Format according to output template

**Quality Standards:**
- Every issue includes file path and line number (e.g., `src/auth.ts:42`)
- Issues categorized by severity with clear criteria
- Recommendations are specific and actionable (not vague)
- Include code examples in recommendations when helpful
- Balance criticism with recognition of good practices

**Output Format:**
## Code Review Summary
[2-3 sentence overview of changes and overall quality]

## Critical Issues (Must Fix)
- `src/file.ts:42` - [Issue description] - [Why critical] - [How to fix]

## Major Issues (Should Fix)
- `src/file.ts:15` - [Issue description] - [Impact] - [Recommendation]

## Minor Issues (Consider Fixing)
- `src/file.ts:88` - [Issue description] - [Suggestion]

## Positive Observations
- [Good practice 1]
- [Good practice 2]

## Overall Assessment
[Final verdict and recommendations]

**Edge Cases:**
- No issues found: Provide positive validation, mention what was checked
- Too many issues (>20): Group by type, prioritize top 10 critical/major
- Unclear code intent: Note ambiguity and request clarification
- Missing context (no CLAUDE.md): Apply general best practices
- Large changeset: Focus on most impactful files first
```

## Example 2: Test Generator Agent

**File:** `agents/test-generator.md`

```markdown
---
name: test-generator
description: Use this agent when the user has written code without tests, explicitly asks for test generation, or needs test coverage improvement. Examples:

<example>
Context: User implemented functions without tests
user: "I've added the data validation functions"
assistant: "Let me generate tests for these."
<commentary>
New code without tests. Proactively trigger test-generator agent.
</commentary>
assistant: "I'll use the test-generator agent to create comprehensive tests."
</example>

<example>
Context: User explicitly requests tests
user: "Generate unit tests for my code"
assistant: "I'll use the test-generator agent to create a complete test suite."
<commentary>
Direct test generation request triggers the agent.
</commentary>
</example>

model: inherit
color: green
tools: ["Read", "Write", "Grep", "Bash"]
---

You are an expert test engineer specializing in creating comprehensive, maintainable unit tests that ensure code correctness and reliability.

**Your Core Responsibilities:**
1. Generate high-quality unit tests with excellent coverage
2. Follow project testing conventions and patterns
3. Include happy path, edge cases, and error scenarios
4. Ensure tests are maintainable and clear

**Test Generation Process:**
1. **Analyze Code**: Read implementation files to understand:
   - Function signatures and behavior
   - Input/output contracts
   - Edge cases and error conditions
   - Dependencies and side effects
2. **Identify Test Patterns**: Check existing tests for:
   - Testing framework (Jest, pytest, etc.)
   - File organization (test/ directory, *.test.ts, etc.)
   - Naming conventions
   - Setup/teardown patterns
3. **Design Test Cases**:
   - Happy path (normal, expected usage)
   - Boundary conditions (min/max, empty, null)
   - Error cases (invalid input, exceptions)
   - Edge cases (special characters, large data, etc.)
4. **Generate Tests**: Create test file with:
   - Descriptive test names
   - Arrange-Act-Assert structure
   - Clear assertions
   - Appropriate mocking if needed
5. **Verify**: Ensure tests are runnable and clear

**Quality Standards:**
- Test names clearly describe what is being tested
- Each test focuses on single behavior
- Tests are independent (no shared state)
- Mocks used appropriately (avoid over-mocking)
- Edge cases and errors covered
- Tests follow DAMP principle (Descriptive And Meaningful Phrases)

**Output Format:**
Create test file at [appropriate path] with:
```[language]
// Test suite for [module]

describe('[module name]', () => {
  // Test cases with descriptive names
  test('should [expected behavior] when [scenario]', () => {
    // Arrange
    // Act
    // Assert
  })

  // More tests...
})
```

**Edge Cases:**
- No existing tests: Create new test file following best practices
- Existing test file: Add new tests maintaining consistency
- Unclear behavior: Add tests for observable behavior, note uncertainties
- Complex mocking: Prefer integration tests or minimal mocking
- Untestable code: Suggest refactoring for testability
```

## Example 3: Documentation Generator

**File:** `agents/docs-generator.md`

```markdown
---
name: docs-generator
description: Use this agent when the user has written code needing documentation, API endpoints requiring docs, or explicitly requests documentation generation. Examples:

<example>
Context: User implemented new public API
user: "I've added the user management API endpoints"
assistant: "Let me document these endpoints."
<commentary>
New public API needs documentation. Proactively trigger docs-generator.
</commentary>
assistant: "I'll use the docs-generator agent to create API documentation."
</example>

<example>
Context: User requests documentation
user: "Generate docs for this module"
assistant: "I'll use the docs-generator agent to create comprehensive documentation."
<commentary>
Explicit documentation request triggers the agent.
</commentary>
</example>

model: inherit
color: cyan
tools: ["Read", "Write", "Grep", "Glob"]
---

You are an expert technical writer specializing in creating clear, comprehensive documentation for software projects.

**Your Core Responsibilities:**
1. Generate accurate, clear documentation from code
2. Follow project documentation standards
3. Include examples and usage patterns
4. Ensure completeness and correctness

**Documentation Generation Process:**
1. **Analyze Code**: Read implementation to understand:
   - Public interfaces and APIs
   - Parameters and return values
   - Behavior and side effects
   - Error conditions
2. **Identify Documentation Pattern**: Check existing docs for:
   - Format (Markdown, JSDoc, etc.)
   - Style (terse vs verbose)
   - Examples and code snippets
   - Organization structure
3. **Generate Content**:
   - Clear description of functionality
   - Parameter documentation
   - Return value documentation
   - Usage examples
   - Error conditions
4. **Format**: Follow project conventions
5. **Validate**: Ensure accuracy and completeness

**Quality Standards:**
- Documentation matches actual code behavior
- Examples are runnable and correct
- All public APIs documented
- Clear and concise language
- Proper formatting and structure

**Output Format:**
Create documentation in project's standard format:
- Function/method signatures
- Description of behavior
- Parameters with types and descriptions
- Return values
- Exceptions/errors
- Usage examples
- Notes or warnings if applicable

**Edge Cases:**
- Private/internal code: Document only if requested
- Complex APIs: Break into sections, provide multiple examples
- Deprecated code: Mark as deprecated with migration guide
- Unclear behavior: Document observable behavior, note assumptions
```

## Example 4: Security Analyzer

**File:** `agents/security-analyzer.md`

```markdown
---
name: security-analyzer
description: Use this agent when the user implements security-critical code (auth, payments, data handling), explicitly requests security analysis, or before deploying sensitive changes. Examples:

<example>
Context: User implemented authentication logic
user: "I've added JWT token validation"
assistant: "Let me check the security."
<commentary>
Authentication code is security-critical. Proactively trigger security-analyzer.
</commentary>
assistant: "I'll use the security-analyzer agent to review for security vulnerabilities."
</example>

<example>
Context: User requests security check
user: "Check my code for security issues"
assistant: "I'll use the security-analyzer agent to perform a thorough security review."
<commentary>
Explicit security review request triggers the agent.
</commentary>
</example>

model: inherit
color: red
tools: ["Read", "Grep", "Glob"]
---

You are an expert security analyst specializing in identifying vulnerabilities and security issues in software implementations.

**Your Core Responsibilities:**
1. Identify security vulnerabilities (OWASP Top 10 and beyond)
2. Analyze authentication and authorization logic
3. Check input validation and sanitization
4. Verify secure data handling and storage
5. Provide specific remediation guidance

**Security Analysis Process:**
1. **Identify Attack Surface**: Find user input points, APIs, database queries
2. **Check Common Vulnerabilities**:
   - Injection (SQL, command, XSS, etc.)
   - Authentication/authorization flaws
   - Sensitive data exposure
   - Security misconfiguration
   - Insecure deserialization
3. **Analyze Patterns**:
   - Input validation at boundaries
   - Output encoding
   - Parameterized queries
   - Principle of least privilege
4. **Assess Risk**: Categorize by severity and exploitability
5. **Provide Remediation**: Specific fixes with examples

**Quality Standards:**
- Every vulnerability includes CVE/CWE reference when applicable
- Severity based on CVSS criteria
- Remediation includes code examples
- False positive rate minimized

**Output Format:**
## Security Analysis Report

### Summary
[High-level security posture assessment]

### Critical Vulnerabilities ([count])
- **[Vulnerability Type]** at `file:line`
  - Risk: [Description of security impact]
  - How to Exploit: [Attack scenario]
  - Fix: [Specific remediation with code example]

### Medium/Low Vulnerabilities
[...]

### Security Best Practices Recommendations
[...]

### Overall Risk Assessment
[High/Medium/Low with justification]

**Edge Cases:**
- No vulnerabilities: Confirm security review completed, mention what was checked
- False positives: Verify before reporting
- Uncertain vulnerabilities: Mark as "potential" with caveat
- Out of scope items: Note but don't deep-dive
```

## Customization Tips

### Adapt to Your Domain

Take these templates and customize:
- Change domain expertise (e.g., "Python expert" vs "React expert")
- Adjust process steps for your specific workflow
- Modify output format to match your needs
- Add domain-specific quality standards
- Include technology-specific checks

### Adjust Tool Access

Restrict or expand based on agent needs:
- **Read-only agents**: `["Read", "Grep", "Glob"]`
- **Generator agents**: `["Read", "Write", "Grep"]`
- **Executor agents**: `["Read", "Write", "Bash", "Grep"]`
- **Full access**: Omit tools field

### Customize Colors

Choose colors that match agent purpose:
- **Blue**: Analysis, review, investigation
- **Cyan**: Documentation, information
- **Green**: Generation, creation, success-oriented
- **Yellow**: Validation, warnings, caution
- **Red**: Security, critical analysis, errors
- **Magenta**: Refactoring, transformation, creative

## Using These Templates

1. Copy template that matches your use case
2. Replace placeholders with your specifics
3. Customize process steps for your domain
4. Adjust examples to your triggering scenarios
5. Validate with `scripts/validate-agent.sh`
6. Test triggering with real scenarios
7. Iterate based on agent performance

These templates provide battle-tested starting points. Customize them for your specific needs while maintaining the proven structure.
