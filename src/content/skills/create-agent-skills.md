---
title: "Create Agent Skills"
description: "Expert guidance for creating Claude Code skills and slash commands. Use when working with SKILL.md files, authoring new skills, improving existing skills, creating slash commands, or understanding skill structure and best practices."
category: "development"
source: "community"
author: "Community"
tags: ["create", "agent"]
date: 2026-03-20
---

# Creating Skills & Commands

This skill teaches how to create effective Claude Code skills following the official specification from [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills).

## Commands and Skills Are Now The Same Thing

Custom slash commands have been merged into skills. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work the same way. Existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter to control invocation, and automatic context loading.

**If a skill and a command share the same name, the skill takes precedence.**

## When To Create What

**Use a command file** (`commands/name.md`) when:
- Simple, single-file workflow
- No supporting files needed
- Task-oriented action (deploy, commit, triage)

**Use a skill directory** (`skills/name/SKILL.md`) when:
- Need supporting reference files, scripts, or templates
- Background knowledge Claude should auto-load
- Complex enough to benefit from progressive disclosure

Both use identical YAML frontmatter and markdown content format.

## Standard Markdown Format

Use YAML frontmatter + markdown body with **standard markdown headings**. Keep it clean and direct.

```markdown
---
name: my-skill-name
description: What it does and when to use it
---

# My Skill Name

## Quick Start
Immediate actionable guidance...

## Instructions
Step-by-step procedures...

## Examples
Concrete usage examples...
```

## Frontmatter Reference

All fields are optional. Only `description` is recommended.

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name. Lowercase letters, numbers, hyphens (max 64 chars). Defaults to directory name. |
| `description` | Recommended | What it does AND when to use it. Claude uses this for auto-discovery. Max 1024 chars. |
| `argument-hint` | No | Hint shown during autocomplete. Example: `[issue-number]` |
| `disable-model-invocation` | No | Set `true` to prevent Claude auto-loading. Use for manual workflows like `/deploy`, `/commit`. Default: `false`. |
| `user-invocable` | No | Set `false` to hide from `/` menu. Use for background knowledge. Default: `true`. |
| `allowed-tools` | No | Tools Claude can use without permission prompts. Example: `Read, Bash(git *)` |
| `model` | No | Model to use. Options: `haiku`, `sonnet`, `opus`. |
| `context` | No | Set `fork` to run in isolated subagent context. |
| `agent` | No | Subagent type when `context: fork`. Options: `Explore`, `Plan`, `general-purpose`, or custom agent name. |

### Invocation Control

| Frontmatter | User can invoke | Claude can invoke | When loaded |
|-------------|----------------|-------------------|-------------|
| (default) | Yes | Yes | Description always in context, full content loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description not in context, loads only when user invokes |
| `user-invocable: false` | No | Yes | Description always in context, loads when relevant |

**Use `disable-model-invocation: true`** for workflows with side effects: `/deploy`, `/commit`, `/triage-prs`, `/send-slack-message`. You don't want Claude deciding to deploy because your code looks ready.

**Use `user-invocable: false`** for background knowledge that isn't a meaningful user action: coding conventions, domain context, legacy system docs.

## Dynamic Features

### Arguments

Use `$ARGUMENTS` placeholder for user input. If not present in content, arguments are appended automatically.

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.
```

Access individual args: `$ARGUMENTS[0]` or shorthand `$0`, `$1`, `$2`.

### Dynamic Context Injection

Skills support dynamic context injection: prefix a backtick-wrapped shell command with an exclamation mark, and the preprocessor executes it at load time, replacing the directive with stdout. Write an exclamation mark immediately before the opening backtick of the command you want executed (for example, to inject the current git branch, write the exclamation mark followed by `git branch --show-current` wrapped in backticks).

**Important:** The preprocessor scans the entire SKILL.md as plain text — it does not parse markdown. Directives inside fenced code blocks or inline code spans are still executed. If a skill documents this syntax with literal examples, the preprocessor will attempt to run them, causing load failures. To safely document this feature, describe it in prose (as done here) or place examples in a reference file, which is loaded on-demand by Claude and not preprocessed.

For a concrete example of dynamic context injection in a skill, see [official-spec.md](references/official-spec.md) § "Dynamic Context Injection".

### Running in a Subagent

Add `context: fork` to run in isolation. The skill content becomes the subagent's prompt. It won't have conversation history.

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files
2. Analyze the code
3. Summarize findings
```

## Progressive Disclosure

Keep SKILL.md under 500 lines. Split detailed content into reference files:

```
my-skill/
├── SKILL.md           # Entry point (required, overview + navigation)
├── reference.md       # Detailed docs (loaded when needed)
├── examples.md        # Usage examples (loaded when needed)
└── scripts/
    └── helper.py      # Utility script (executed, not loaded)
```

Link from SKILL.md: `For API details, see [reference.md](reference.md).`

Keep references **one level deep** from SKILL.md. Avoid nested chains.

## Effective Descriptions

The description enables skill discovery. Include both **what** it does and **when** to use it.

**Good:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad:**
```yaml
description: Helps with documents
```

## What Would You Like To Do?

1. **Create new skill** - Build from scratch
2. **Create new command** - Build a slash command
3. **Audit existing skill** - Check against best practices
4. **Add component** - Add workflow/reference/example
5. **Get guidance** - Understand skill design

## Creating a New Skill or Command

### Step 1: Choose Type

Ask: Is this a manual workflow (deploy, commit, triage) or background knowledge (conventions, patterns)?

- **Manual workflow** → command with `disable-model-invocation: true`
- **Background knowledge** → skill without `disable-model-invocation`
- **Complex with supporting files** → skill directory

### Step 2: Create the File

**Command:**
```markdown
---
name: my-command
description: What this command does
argument-hint: [expected arguments]
disable-model-invocation: true
allowed-tools: Bash(gh *), Read
---

# Command Title

## Workflow

### Step 1: Gather Context
...

### Step 2: Execute
...

## Success Criteria
- [ ] Expected outcome 1
- [ ] Expected outcome 2
```

**Skill:**
```markdown
---
name: my-skill
description: What it does. Use when [trigger conditions].
---

# Skill Title

## Quick Start
[Immediate actionable example]

## Instructions
[Core guidance]

## Examples
[Concrete input/output pairs]
```

### Step 3: Add Reference Files (If Needed)

Link from SKILL.md to detailed content:
```markdown
For API reference, see [reference.md](reference.md).
For form filling guide, see [forms.md](forms.md).
```

### Step 4: Test With Real Usage

1. Test with actual tasks, not test scenarios
2. Invoke directly with `/skill-name` to verify
3. Check auto-triggering by asking something that matches the description
4. Refine based on real behavior

## Audit Checklist

- [ ] Valid YAML frontmatter (name + description)
- [ ] Description includes trigger keywords and is specific
- [ ] Uses standard markdown headings (not XML tags)
- [ ] SKILL.md under 500 lines
- [ ] `disable-model-invocation: true` if it has side effects
- [ ] `allowed-tools` set if specific tools needed
- [ ] References one level deep, properly linked
- [ ] Examples are concrete, not abstract
- [ ] Tested with real usage

## Anti-Patterns to Avoid

- **XML tags in body** - Use standard markdown headings
- **Vague descriptions** - Be specific with trigger keywords
- **Deep nesting** - Keep references one level from SKILL.md
- **Missing invocation control** - Side-effect workflows need `disable-model-invocation: true`
- **Too many options** - Provide a default with escape hatch
- **Punting to Claude** - Scripts should handle errors explicitly

## Reference Files

For detailed guidance, see:
- [official-spec.md](references/official-spec.md) - Official skill specification
- [best-practices.md](references/best-practices.md) - Skill authoring best practices

## Sources

- [Extend Claude with skills - Official Docs](https://code.claude.com/docs/en/skills)
- [GitHub - anthropics/skills](https://github.com/anthropics/skills)

---

## Reference: Api Security

<overview>
When building skills that make API calls requiring credentials (API keys, tokens, secrets), follow this protocol to prevent credentials from appearing in chat.
</overview>

<the_problem>
Raw curl commands with environment variables expose credentials:

```bash
# ❌ BAD - API key visible in chat
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/data
```

When Claude executes this, the full command with expanded `$API_KEY` appears in the conversation.
</the_problem>

<the_solution>
Use `~/.claude/scripts/secure-api.sh` - a wrapper that loads credentials internally.

<for_supported_services>
```bash
# ✅ GOOD - No credentials visible
~/.claude/scripts/secure-api.sh <service> <operation> [args]

# Examples:
~/.claude/scripts/secure-api.sh facebook list-campaigns
~/.claude/scripts/secure-api.sh ghl search-contact "email@example.com"
```
</for_supported_services>

<adding_new_services>
When building a new skill that requires API calls:

1. **Add operations to the wrapper** (`~/.claude/scripts/secure-api.sh`):

```bash
case "$SERVICE" in
    yourservice)
        case "$OPERATION" in
            list-items)
                curl -s -G \
                    -H "Authorization: Bearer $YOUR_API_KEY" \
                    "https://api.yourservice.com/items"
                ;;
            get-item)
                ITEM_ID=$1
                curl -s -G \
                    -H "Authorization: Bearer $YOUR_API_KEY" \
                    "https://api.yourservice.com/items/$ITEM_ID"
                ;;
            *)
                echo "Unknown operation: $OPERATION" >&2
                exit 1
                ;;
        esac
        ;;
esac
```

2. **Add profile support to the wrapper** (if service needs multiple accounts):

```bash
# In secure-api.sh, add to profile remapping section:
yourservice)
    SERVICE_UPPER="YOURSERVICE"
    YOURSERVICE_API_KEY=$(eval echo \$${SERVICE_UPPER}_${PROFILE_UPPER}_API_KEY)
    YOURSERVICE_ACCOUNT_ID=$(eval echo \$${SERVICE_UPPER}_${PROFILE_UPPER}_ACCOUNT_ID)
    ;;
```

3. **Add credential placeholders to `~/.claude/.env`** using profile naming:

```bash
# Check if entries already exist
grep -q "YOURSERVICE_MAIN_API_KEY=" ~/.claude/.env 2>/dev/null || \
  echo -e "\n# Your Service - Main profile\nYOURSERVICE_MAIN_API_KEY=\nYOURSERVICE_MAIN_ACCOUNT_ID=" >> ~/.claude/.env

echo "Added credential placeholders to ~/.claude/.env - user needs to fill them in"
```

4. **Document profile workflow in your SKILL.md**:

```markdown
## Profile Selection Workflow

**CRITICAL:** Always use profile selection to prevent using wrong account credentials.

### When user requests YourService operation:

1. **Check for saved profile:**
   ```bash
   ~/.claude/scripts/profile-state get yourservice
   ```

2. **If no profile saved, discover available profiles:**
   ```bash
   ~/.claude/scripts/list-profiles yourservice
   ```

3. **If only ONE profile:** Use it automatically and announce:
   ```
   "Using YourService profile 'main' to list items..."
   ```

4. **If MULTIPLE profiles:** Ask user which one:
   ```
   "Which YourService profile: main, clienta, or clientb?"
   ```

5. **Save user's selection:**
   ```bash
   ~/.claude/scripts/profile-state set yourservice <selected_profile>
   ```

6. **Always announce which profile before calling API:**
   ```
   "Using YourService profile 'main' to list items..."
   ```

7. **Make API call with profile:**
   ```bash
   ~/.claude/scripts/secure-api.sh yourservice:<profile> list-items
   ```

## Secure API Calls

All API calls use profile syntax:

```bash
~/.claude/scripts/secure-api.sh yourservice:<profile> <operation> [args]

# Examples:
~/.claude/scripts/secure-api.sh yourservice:main list-items
~/.claude/scripts/secure-api.sh yourservice:main get-item <ITEM_ID>
```

**Profile persists for session:** Once selected, use same profile for subsequent operations unless user explicitly changes it.
```
</adding_new_services>
</the_solution>

<pattern_guidelines>
<simple_get_requests>
```bash
curl -s -G \
    -H "Authorization: Bearer $API_KEY" \
    "https://api.example.com/endpoint"
```
</simple_get_requests>

<post_with_json_body>
```bash
ITEM_ID=$1
curl -s -X POST \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d @- \
    "https://api.example.com/items/$ITEM_ID"
```

Usage:
```bash
echo '{"name":"value"}' | ~/.claude/scripts/secure-api.sh service create-item
```
</post_with_json_body>

<post_with_form_data>
```bash
curl -s -X POST \
    -F "field1=value1" \
    -F "field2=value2" \
    -F "access_token=$API_TOKEN" \
    "https://api.example.com/endpoint"
```
</post_with_form_data>
</pattern_guidelines>

<credential_storage>
**Location:** `~/.claude/.env` (global for all skills, accessible from any directory)

**Format:**
```bash
# Service credentials
SERVICE_API_KEY=your-key-here
SERVICE_ACCOUNT_ID=account-id-here

# Another service
OTHER_API_TOKEN=token-here
OTHER_BASE_URL=https://api.other.com
```

**Loading in script:**
```bash
set -a
source ~/.claude/.env 2>/dev/null || { echo "Error: ~/.claude/.env not found" >&2; exit 1; }
set +a
```
</credential_storage>

<best_practices>
1. **Never use raw curl with `$VARIABLE` in skill examples** - always use the wrapper
2. **Add all operations to the wrapper** - don't make users figure out curl syntax
3. **Auto-create credential placeholders** - add empty fields to `~/.claude/.env` immediately when creating the skill
4. **Keep credentials in `~/.claude/.env`** - one central location, works everywhere
5. **Document each operation** - show examples in SKILL.md
6. **Handle errors gracefully** - check for missing env vars, show helpful error messages
</best_practices>

<testing>
Test the wrapper without exposing credentials:

```bash
# This command appears in chat
~/.claude/scripts/secure-api.sh facebook list-campaigns

# But API keys never appear - they're loaded inside the script
```

Verify credentials are loaded:
```bash
# Check .env exists
ls -la ~/.claude/.env

# Check specific variables (without showing values)
grep -q "YOUR_API_KEY=" ~/.claude/.env && echo "API key configured" || echo "API key missing"
```
</testing>

---

## Reference: Be Clear And Direct

<golden_rule>
Show your skill to someone with minimal context and ask them to follow the instructions. If they're confused, Claude will likely be too.
</golden_rule>

<overview>
Clarity and directness are fundamental to effective skill authoring. Clear instructions reduce errors, improve execution quality, and minimize token waste.
</overview>

<guidelines>
<contextual_information>
Give Claude contextual information that frames the task:

- What the task results will be used for
- What audience the output is meant for
- What workflow the task is part of
- The end goal or what successful completion looks like

Context helps Claude make better decisions and produce more appropriate outputs.

<example>
```xml
<context>
This analysis will be presented to investors who value transparency and actionable insights. Focus on financial metrics and clear recommendations.
</context>
```
</example>
</contextual_information>

<specificity>
Be specific about what you want Claude to do. If you want code only and nothing else, say so.

**Vague**: "Help with the report"
**Specific**: "Generate a markdown report with three sections: Executive Summary, Key Findings, Recommendations"

**Vague**: "Process the data"
**Specific**: "Extract customer names and email addresses from the CSV file, removing duplicates, and save to JSON format"

Specificity eliminates ambiguity and reduces iteration cycles.
</specificity>

<sequential_steps>
Provide instructions as sequential steps. Use numbered lists or bullet points.

```xml
<workflow>
1. Extract data from source file
2. Transform to target format
3. Validate transformation
4. Save to output file
5. Verify output correctness
</workflow>
```

Sequential steps create clear expectations and reduce the chance Claude skips important operations.
</sequential_steps>
</guidelines>

<example_comparison>
<unclear_example>
```xml
<quick_start>
Please remove all personally identifiable information from these customer feedback messages: {{FEEDBACK_DATA}}
</quick_start>
```

**Problems**:
- What counts as PII?
- What should replace PII?
- What format should the output be?
- What if no PII is found?
- Should product names be redacted?
</unclear_example>

<clear_example>
```xml
<objective>
Anonymize customer feedback for quarterly review presentation.
</objective>

<quick_start>
<instructions>
1. Replace all customer names with "CUSTOMER_[ID]" (e.g., "Jane Doe" → "CUSTOMER_001")
2. Replace email addresses with "EMAIL_[ID]@example.com"
3. Redact phone numbers as "PHONE_[ID]"
4. If a message mentions a specific product (e.g., "AcmeCloud"), leave it intact
5. If no PII is found, copy the message verbatim
6. Output only the processed messages, separated by "---"
</instructions>

Data to process: {{FEEDBACK_DATA}}
</quick_start>

<success_criteria>
- All customer names replaced with IDs
- All emails and phones redacted
- Product names preserved
- Output format matches specification
</success_criteria>
```

**Why this is better**:
- States the purpose (quarterly review)
- Provides explicit step-by-step rules
- Defines output format clearly
- Specifies edge cases (product names, no PII found)
- Defines success criteria
</clear_example>
</example_comparison>

<key_differences>
The clear version:
- States the purpose (quarterly review)
- Provides explicit step-by-step rules
- Defines output format
- Specifies edge cases (product names, no PII found)
- Includes success criteria

The unclear version leaves all these decisions to Claude, increasing the chance of misalignment with expectations.
</key_differences>

<show_dont_just_tell>
<principle>
When format matters, show an example rather than just describing it.
</principle>

<telling_example>
```xml
<commit_messages>
Generate commit messages in conventional format with type, scope, and description.
</commit_messages>
```
</telling_example>

<showing_example>
```xml
<commit_message_format>
Generate commit messages following these examples:

<example number="1">
<input>Added user authentication with JWT tokens</input>
<output>
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```
</output>
</example>

<example number="2">
<input>Fixed bug where dates displayed incorrectly in reports</input>
<output>
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```
</output>
</example>

Follow this style: type(scope): brief description, then detailed explanation.
</commit_message_format>
```
</showing_example>

<why_showing_works>
Examples communicate nuances that text descriptions can't:
- Exact formatting (spacing, capitalization, punctuation)
- Tone and style
- Level of detail
- Pattern across multiple cases

Claude learns patterns from examples more reliably than from descriptions.
</why_showing_works>
</show_dont_just_tell>

<avoid_ambiguity>
<principle>
Eliminate words and phrases that create ambiguity or leave decisions open.
</principle>

<ambiguous_phrases>
❌ **"Try to..."** - Implies optional
✅ **"Always..."** or **"Never..."** - Clear requirement

❌ **"Should probably..."** - Unclear obligation
✅ **"Must..."** or **"May optionally..."** - Clear obligation level

❌ **"Generally..."** - When are exceptions allowed?
✅ **"Always... except when..."** - Clear rule with explicit exceptions

❌ **"Consider..."** - Should Claude always do this or only sometimes?
✅ **"If X, then Y"** or **"Always..."** - Clear conditions
</ambiguous_phrases>

<example>
❌ **Ambiguous**:
```xml
<validation>
You should probably validate the output and try to fix any errors.
</validation>
```

✅ **Clear**:
```xml
<validation>
Always validate output before proceeding:

```bash
python scripts/validate.py output_dir/
```

If validation fails, fix errors and re-validate. Only proceed when validation passes with zero errors.
</validation>
```
</example>
</avoid_ambiguity>

<define_edge_cases>
<principle>
Anticipate edge cases and define how to handle them. Don't leave Claude guessing.
</principle>

<without_edge_cases>
```xml
<quick_start>
Extract email addresses from the text file and save to a JSON array.
</quick_start>
```

**Questions left unanswered**:
- What if no emails are found?
- What if the same email appears multiple times?
- What if emails are malformed?
- What JSON format exactly?
</without_edge_cases>

<with_edge_cases>
```xml
<quick_start>
Extract email addresses from the text file and save to a JSON array.

<edge_cases>
- **No emails found**: Save empty array `[]`
- **Duplicate emails**: Keep only unique emails
- **Malformed emails**: Skip invalid formats, log to stderr
- **Output format**: Array of strings, one email per element
</edge_cases>

<example_output>
```json
[
  "user1@example.com",
  "user2@example.com"
]
```
</example_output>
</quick_start>
```
</with_edge_cases>
</define_edge_cases>

<output_format_specification>
<principle>
When output format matters, specify it precisely. Show examples.
</principle>

<vague_format>
```xml
<output>
Generate a report with the analysis results.
</output>
```
</vague_format>

<specific_format>
```xml
<output_format>
Generate a markdown report with this exact structure:

```markdown
# Analysis Report: [Title]

## Executive Summary
[1-2 paragraphs summarizing key findings]

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation

## Appendix
[Raw data and detailed calculations]
```

**Requirements**:
- Use exactly these section headings
- Executive summary must be 1-2 paragraphs
- List 3-5 key findings
- Provide 2-4 recommendations
- Include appendix with source data
</output_format>
```
</specific_format>
</output_format_specification>

<decision_criteria>
<principle>
When Claude must make decisions, provide clear criteria.
</principle>

<no_criteria>
```xml
<workflow>
Analyze the data and decide which visualization to use.
</workflow>
```

**Problem**: What factors should guide this decision?
</no_criteria>

<with_criteria>
```xml
<workflow>
Analyze the data and select appropriate visualization:

<decision_criteria>
**Use bar chart when**:
- Comparing quantities across categories
- Fewer than 10 categories
- Exact values matter

**Use line chart when**:
- Showing trends over time
- Continuous data
- Pattern recognition matters more than exact values

**Use scatter plot when**:
- Showing relationship between two variables
- Looking for correlations
- Individual data points matter
</decision_criteria>
</workflow>
```

**Benefits**: Claude has objective criteria for making the decision rather than guessing.
</with_criteria>
</decision_criteria>

<constraints_and_requirements>
<principle>
Clearly separate "must do" from "nice to have" from "must not do".
</principle>

<unclear_requirements>
```xml
<requirements>
The report should include financial data, customer metrics, and market analysis. It would be good to have visualizations. Don't make it too long.
</requirements>
```

**Problems**:
- Are all three content types required?
- Are visualizations optional or required?
- How long is "too long"?
</unclear_requirements>

<clear_requirements>
```xml
<requirements>
<must_have>
- Financial data (revenue, costs, profit margins)
- Customer metrics (acquisition, retention, lifetime value)
- Market analysis (competition, trends, opportunities)
- Maximum 5 pages
</must_have>

<nice_to_have>
- Charts and visualizations
- Industry benchmarks
- Future projections
</nice_to_have>

<must_not>
- Include confidential customer names
- Exceed 5 pages
- Use technical jargon without definitions
</must_not>
</requirements>
```

**Benefits**: Clear priorities and constraints prevent misalignment.
</clear_requirements>
</constraints_and_requirements>

<success_criteria>
<principle>
Define what success looks like. How will Claude know it succeeded?
</principle>

<without_success_criteria>
```xml
<objective>
Process the CSV file and generate a report.
</objective>
```

**Problem**: When is this task complete? What defines success?
</without_success_criteria>

<with_success_criteria>
```xml
<objective>
Process the CSV file and generate a summary report.
</objective>

<success_criteria>
- All rows in CSV successfully parsed
- No data validation errors
- Report generated with all required sections
- Report saved to output/report.md
- Output file is valid markdown
- Process completes without errors
</success_criteria>
```

**Benefits**: Clear completion criteria eliminate ambiguity about when the task is done.
</with_success_criteria>
</success_criteria>

<testing_clarity>
<principle>
Test your instructions by asking: "Could I hand these instructions to a junior developer and expect correct results?"
</principle>

<testing_process>
1. Read your skill instructions
2. Remove context only you have (project knowledge, unstated assumptions)
3. Identify ambiguous terms or vague requirements
4. Add specificity where needed
5. Test with someone who doesn't have your context
6. Iterate based on their questions and confusion

If a human with minimal context struggles, Claude will too.
</testing_process>
</testing_clarity>

<practical_examples>
<example domain="data_processing">
❌ **Unclear**:
```xml
<quick_start>
Clean the data and remove bad entries.
</quick_start>
```

✅ **Clear**:
```xml
<quick_start>
<data_cleaning>
1. Remove rows where required fields (name, email, date) are empty
2. Standardize date format to YYYY-MM-DD
3. Remove duplicate entries based on email address
4. Validate email format (must contain @ and domain)
5. Save cleaned data to output/cleaned_data.csv
</data_cleaning>

<success_criteria>
- No empty required fields
- All dates in YYYY-MM-DD format
- No duplicate emails
- All emails valid format
- Output file created successfully
</success_criteria>
</quick_start>
```
</example>

<example domain="code_generation">
❌ **Unclear**:
```xml
<quick_start>
Write a function to process user input.
</quick_start>
```

✅ **Clear**:
```xml
<quick_start>
<function_specification>
Write a Python function with this signature:

```python
def process_user_input(raw_input: str) -> dict:
    """
    Validate and parse user input.

    Args:
        raw_input: Raw string from user (format: "name:email:age")

    Returns:
        dict with keys: name (str), email (str), age (int)

    Raises:
        ValueError: If input format is invalid
    """
```

**Requirements**:
- Split input on colon delimiter
- Validate email contains @ and domain
- Convert age to integer, raise ValueError if not numeric
- Return dictionary with specified keys
- Include docstring and type hints
</function_specification>

<success_criteria>
- Function signature matches specification
- All validation checks implemented
- Proper error handling for invalid input
- Type hints included
- Docstring included
</success_criteria>
</quick_start>
```
</example>
</practical_examples>

---

## Reference: Best Practices

# Skill Authoring Best Practices

Source: [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## Core Principles

### Concise is Key

The context window is a public good. Your Skill shares the context window with everything else Claude needs to know.

**Default assumption**: Claude is already very smart. Only add context Claude doesn't already have.

Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Good example (concise, ~50 tokens):**
```markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**Bad example (too verbose, ~150 tokens):**
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available...
```

### Set Appropriate Degrees of Freedom

Match specificity to task fragility and variability.

**High freedom** (multiple valid approaches):
```markdown
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability
4. Verify adherence to project conventions
```

**Medium freedom** (preferred pattern with variation):
```markdown
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown"):
    # Process data
    # Generate output in specified format
```
```

**Low freedom** (fragile, exact sequence required):
```markdown
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add flags.
```

### Test With All Models

Skills act as additions to models. Test with Haiku, Sonnet, and Opus.

- **Haiku**: Does the Skill provide enough guidance?
- **Sonnet**: Is the Skill clear and efficient?
- **Opus**: Does the Skill avoid over-explaining?

## Naming Conventions

Use **gerund form** (verb + -ing) for Skill names:

**Good:**
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`
- `writing-documentation`

**Acceptable alternatives:**
- Noun phrases: `pdf-processing`, `spreadsheet-analysis`
- Action-oriented: `process-pdfs`, `analyze-spreadsheets`

**Avoid:**
- Vague: `helper`, `utils`, `tools`
- Generic: `documents`, `data`, `files`
- Reserved: `anthropic-*`, `claude-*`

## Writing Effective Descriptions

**Always write in third person.** The description is injected into the system prompt.

**Be specific and include key terms:**

```yaml
# PDF Processing skill
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Excel Analysis skill
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.

# Git Commit Helper skill
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

**Avoid vague descriptions:**
```yaml
description: Helps with documents  # Too vague!
description: Processes data       # Too generic!
description: Does stuff with files # Useless!
```

## Progressive Disclosure Patterns

### Pattern 1: High-level guide with references

```markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, merges documents.
---

# PDF Processing

## Quick start

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
**Examples**: See [EXAMPLES.md](EXAMPLES.md)
```

### Pattern 2: Domain-specific organization

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

### Pattern 3: Conditional details

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

## Keep References One Level Deep

Claude may partially read files when they're referenced from other referenced files.

**Bad (too deep):**
```markdown
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**Good (one level deep):**
```markdown
# SKILL.md

**Basic usage**: [in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

## Workflows and Feedback Loops

### Workflow with Checklist

```markdown
## Research synthesis workflow

Copy this checklist:

```
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**Step 1: Read all source documents**

Review each document in `sources/`. Note main arguments.
...
```

### Feedback Loop Pattern

```markdown
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message
   - Fix the issues
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python scripts/pack.py unpacked_dir/ output.docx`
```

## Common Patterns

### Template Pattern

```markdown
## Report structure

Use this template:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
```

### Examples Pattern

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
```
fix(reports): correct date formatting in timezone conversion
```
```

### Conditional Workflow Pattern

```markdown
## Document modification

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow"
   **Editing existing?** → Follow "Editing workflow"

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
```

## Content Guidelines

### Avoid Time-Sensitive Information

**Bad:**
```markdown
If you're doing this before August 2025, use the old API.
```

**Good:**
```markdown
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used: `api.example.com/v1/messages`
</details>
```

### Use Consistent Terminology

**Good - Consistent:**
- Always "API endpoint"
- Always "field"
- Always "extract"

**Bad - Inconsistent:**
- Mix "API endpoint", "URL", "API route", "path"
- Mix "field", "box", "element", "control"

## Anti-Patterns to Avoid

### Windows-Style Paths

- **Good**: `scripts/helper.py`, `reference/guide.md`
- **Avoid**: `scripts\helper.py`, `reference\guide.md`

### Too Many Options

**Bad:**
```markdown
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or...
```

**Good:**
```markdown
Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

## Checklist for Effective Skills

### Core Quality
- [ ] Description is specific and includes key terms
- [ ] Description includes both what and when
- [ ] SKILL.md body under 500 lines
- [ ] Additional details in separate files
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Examples are concrete
- [ ] References one level deep
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear steps

### Code and Scripts
- [ ] Scripts handle errors explicitly
- [ ] No "voodoo constants" (all values justified)
- [ ] Required packages listed
- [ ] Scripts have clear documentation
- [ ] No Windows-style paths
- [ ] Validation steps for critical operations
- [ ] Feedback loops for quality-critical tasks

### Testing
- [ ] At least three test scenarios
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated

---

## Reference: Common Patterns

<overview>
This reference documents common patterns for skill authoring, including templates, examples, terminology consistency, and anti-patterns. All patterns use pure XML structure.
</overview>

<template_pattern>
<description>
Provide templates for output format. Match the level of strictness to your needs.
</description>

<strict_requirements>
Use when output format must be exact and consistent:

```xml
<report_structure>
ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
</report_structure>
```

**When to use**: Compliance reports, standardized formats, automated processing
</strict_requirements>

<flexible_guidance>
Use when Claude should adapt the format based on context:

```xml
<report_structure>
Here is a sensible default format, but use your best judgment:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

Adjust sections as needed for the specific analysis type.
</report_structure>
```

**When to use**: Exploratory analysis, context-dependent formatting, creative tasks
</flexible_guidance>
</template_pattern>

<examples_pattern>
<description>
For skills where output quality depends on seeing examples, provide input/output pairs.
</description>

<commit_messages_example>
```xml
<objective>
Generate commit messages following conventional commit format.
</objective>

<commit_message_format>
Generate commit messages following these examples:

<example number="1">
<input>Added user authentication with JWT tokens</input>
<output>
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```
</output>
</example>

<example number="2">
<input>Fixed bug where dates displayed incorrectly in reports</input>
<output>
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```
</output>
</example>

Follow this style: type(scope): brief description, then detailed explanation.
</commit_message_format>
```
</commit_messages_example>

<when_to_use>
- Output format has nuances that text explanations can't capture
- Pattern recognition is easier than rule following
- Examples demonstrate edge cases
- Multi-shot learning improves quality
</when_to_use>
</examples_pattern>

<consistent_terminology>
<principle>
Choose one term and use it throughout the skill. Inconsistent terminology confuses Claude and reduces execution quality.
</principle>

<good_example>
Consistent usage:
- Always "API endpoint" (not mixing with "URL", "API route", "path")
- Always "field" (not mixing with "box", "element", "control")
- Always "extract" (not mixing with "pull", "get", "retrieve")

```xml
<objective>
Extract data from API endpoints using field mappings.
</objective>

<quick_start>
1. Identify the API endpoint
2. Map response fields to your schema
3. Extract field values
</quick_start>
```
</good_example>

<bad_example>
Inconsistent usage creates confusion:

```xml
<objective>
Pull data from API routes using element mappings.
</objective>

<quick_start>
1. Identify the URL
2. Map response boxes to your schema
3. Retrieve control values
</quick_start>
```

Claude must now interpret: Are "API routes" and "URLs" the same? Are "fields", "boxes", "elements", and "controls" the same?
</bad_example>

<implementation>
1. Choose terminology early in skill development
2. Document key terms in `<objective>` or `<context>`
3. Use find/replace to enforce consistency
4. Review reference files for consistent usage
</implementation>
</consistent_terminology>

<provide_default_with_escape_hatch>
<principle>
Provide a default approach with an escape hatch for special cases, not a list of alternatives. Too many options paralyze decision-making.
</principle>

<good_example>
Clear default with escape hatch:

```xml
<quick_start>
Use pdfplumber for text extraction:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
</quick_start>
```
</good_example>

<bad_example>
Too many options creates decision paralysis:

```xml
<quick_start>
You can use any of these libraries:

- **pypdf**: Good for basic extraction
- **pdfplumber**: Better for tables
- **PyMuPDF**: Faster but more complex
- **pdf2image**: For scanned documents
- **pdfminer**: Low-level control
- **tabula-py**: Table-focused

Choose based on your needs.
</quick_start>
```

Claude must now research and compare all options before starting. This wastes tokens and time.
</bad_example>

<implementation>
1. Recommend ONE default approach
2. Explain when to use the default (implied: most of the time)
3. Add ONE escape hatch for edge cases
4. Link to advanced reference if multiple alternatives truly needed
</implementation>
</provide_default_with_escape_hatch>

<anti_patterns>
<description>
Common mistakes to avoid when authoring skills.
</description>

<pitfall name="markdown_headings_in_body">
❌ **BAD**: Using markdown headings in skill body:

```markdown
# PDF Processing

## Quick start
Extract text with pdfplumber...

## Advanced features
Form filling requires additional setup...
```

✅ **GOOD**: Using pure XML structure:

```xml
<objective>
PDF processing with text extraction, form filling, and merging capabilities.
</objective>

<quick_start>
Extract text with pdfplumber...
</quick_start>

<advanced_features>
Form filling requires additional setup...
</advanced_features>
```

**Why it matters**: XML provides semantic meaning, reliable parsing, and token efficiency.
</pitfall>

<pitfall name="vague_descriptions">
❌ **BAD**:
```yaml
description: Helps with documents
```

✅ **GOOD**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Why it matters**: Vague descriptions prevent Claude from discovering and using the skill appropriately.
</pitfall>

<pitfall name="inconsistent_pov">
❌ **BAD**:
```yaml
description: I can help you process Excel files and generate reports
```

✅ **GOOD**:
```yaml
description: Processes Excel files and generates reports. Use when analyzing spreadsheets or .xlsx files.
```

**Why it matters**: Skills must use third person. First/second person breaks the skill metadata pattern.
</pitfall>

<pitfall name="wrong_naming_convention">
❌ **BAD**: Directory name doesn't match skill name or verb-noun convention:
- Directory: `facebook-ads`, Name: `facebook-ads-manager`
- Directory: `stripe-integration`, Name: `stripe`
- Directory: `helper-scripts`, Name: `helper`

✅ **GOOD**: Consistent verb-noun convention:
- Directory: `manage-facebook-ads`, Name: `manage-facebook-ads`
- Directory: `setup-stripe-payments`, Name: `setup-stripe-payments`
- Directory: `process-pdfs`, Name: `process-pdfs`

**Why it matters**: Consistency in naming makes skills discoverable and predictable.
</pitfall>

<pitfall name="too_many_options">
❌ **BAD**:
```xml
<quick_start>
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or pdfminer, or tabula-py...
</quick_start>
```

✅ **GOOD**:
```xml
<quick_start>
Use pdfplumber for text extraction:

```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
</quick_start>
```

**Why it matters**: Decision paralysis. Provide one default approach with escape hatch for special cases.
</pitfall>

<pitfall name="deeply_nested_references">
❌ **BAD**: References nested multiple levels:
```
SKILL.md → advanced.md → details.md → examples.md
```

✅ **GOOD**: References one level deep from SKILL.md:
```
SKILL.md → advanced.md
SKILL.md → details.md
SKILL.md → examples.md
```

**Why it matters**: Claude may only partially read deeply nested files. Keep references one level deep from SKILL.md.
</pitfall>

<pitfall name="windows_paths">
❌ **BAD**:
```xml
<reference_guides>
See scripts\validate.py for validation
</reference_guides>
```

✅ **GOOD**:
```xml
<reference_guides>
See scripts/validate.py for validation
</reference_guides>
```

**Why it matters**: Always use forward slashes for cross-platform compatibility.
</pitfall>

<pitfall name="dynamic_context_and_file_reference_execution">
**Problem**: When showing examples of dynamic context syntax (exclamation mark + backticks) or file references (@ prefix), the skill loader executes these during skill loading.

❌ **BAD** - These execute during skill load:
```xml
<examples>
Load current status with: !`git status`
Review dependencies in: @package.json
</examples>
```

✅ **GOOD** - Add space to prevent execution:
```xml
<examples>
Load current status with: ! `git status` (remove space before backtick in actual usage)
Review dependencies in: @ package.json (remove space after @ in actual usage)
</examples>
```

**When this applies**:
- Skills that teach users about dynamic context (slash commands, prompts)
- Any documentation showing the exclamation mark prefix syntax or @ file references
- Skills with example commands or file paths that shouldn't execute during loading

**Why it matters**: Without the space, these execute during skill load, causing errors or unwanted file reads.
</pitfall>

<pitfall name="missing_required_tags">
❌ **BAD**: Missing required tags:
```xml
<quick_start>
Use this tool for processing...
</quick_start>
```

✅ **GOOD**: All required tags present:
```xml
<objective>
Process data files with validation and transformation.
</objective>

<quick_start>
Use this tool for processing...
</quick_start>

<success_criteria>
- Input file successfully processed
- Output file validates without errors
- Transformation applied correctly
</success_criteria>
```

**Why it matters**: Every skill must have `<objective>`, `<quick_start>`, and `<success_criteria>` (or `<when_successful>`).
</pitfall>

<pitfall name="hybrid_xml_markdown">
❌ **BAD**: Mixing XML tags with markdown headings:
```markdown
<objective>
PDF processing capabilities
</objective>

## Quick start

Extract text with pdfplumber...

## Advanced features

Form filling...
```

✅ **GOOD**: Pure XML throughout:
```xml
<objective>
PDF processing capabilities
</objective>

<quick_start>
Extract text with pdfplumber...
</quick_start>

<advanced_features>
Form filling...
</advanced_features>
```

**Why it matters**: Consistency in structure. Either use pure XML or pure markdown (prefer XML).
</pitfall>

<pitfall name="unclosed_xml_tags">
❌ **BAD**: Forgetting to close XML tags:
```xml
<objective>
Process PDF files

<quick_start>
Use pdfplumber...
</quick_start>
```

✅ **GOOD**: Properly closed tags:
```xml
<objective>
Process PDF files
</objective>

<quick_start>
Use pdfplumber...
</quick_start>
```

**Why it matters**: Unclosed tags break XML parsing and create ambiguous boundaries.
</pitfall>
</anti_patterns>

<progressive_disclosure_pattern>
<description>
Keep SKILL.md concise by linking to detailed reference files. Claude loads reference files only when needed.
</description>

<implementation>
```xml
<objective>
Manage Facebook Ads campaigns, ad sets, and ads via the Marketing API.
</objective>

<quick_start>
<basic_operations>
See [basic-operations.md](basic-operations.md) for campaign creation and management.
</basic_operations>
</quick_start>

<advanced_features>
**Custom audiences**: See [audiences.md](audiences.md)
**Conversion tracking**: See [conversions.md](conversions.md)
**Budget optimization**: See [budgets.md](budgets.md)
**API reference**: See [api-reference.md](api-reference.md)
</advanced_features>
```

**Benefits**:
- SKILL.md stays under 500 lines
- Claude only reads relevant reference files
- Token usage scales with task complexity
- Easier to maintain and update
</implementation>
</progressive_disclosure_pattern>

<validation_pattern>
<description>
For skills with validation steps, make validation scripts verbose and specific.
</description>

<implementation>
```xml
<validation>
After making changes, validate immediately:

```bash
python scripts/validate.py output_dir/
```

If validation fails, fix errors before continuing. Validation errors include:

- **Field not found**: "Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed"
- **Type mismatch**: "Field 'order_total' expects number, got string"
- **Missing required field**: "Required field 'customer_name' is missing"

Only proceed when validation passes with zero errors.
</validation>
```

**Why verbose errors help**:
- Claude can fix issues without guessing
- Specific error messages reduce iteration cycles
- Available options shown in error messages
</implementation>
</validation_pattern>

<checklist_pattern>
<description>
For complex multi-step workflows, provide a checklist Claude can copy and track progress.
</description>

<implementation>
```xml
<workflow>
Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

<step_1>
**Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.
</step_1>

<step_2>
**Create field mapping**

Edit `fields.json` to add values for each field.
</step_2>

<step_3>
**Validate mapping**

Run: `python scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.
</step_3>

<step_4>
**Fill the form**

Run: `python scripts/fill_form.py input.pdf fields.json output.pdf`
</step_4>

<step_5>
**Verify output**

Run: `python scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.
</step_5>
</workflow>
```

**Benefits**:
- Clear progress tracking
- Prevents skipping steps
- Easy to resume after interruption
</implementation>
</checklist_pattern>

---

## Reference: Core Principles

<overview>
Core principles guide skill authoring decisions. These principles ensure skills are efficient, effective, and maintainable across different models and use cases.
</overview>

<xml_structure_principle>
<description>
Skills use pure XML structure for consistent parsing, efficient token usage, and improved Claude performance.
</description>

<why_xml>
<consistency>
XML enforces consistent structure across all skills. All skills use the same tag names for the same purposes:
- `<objective>` always defines what the skill does
- `<quick_start>` always provides immediate guidance
- `<success_criteria>` always defines completion

This consistency makes skills predictable and easier to maintain.
</consistency>

<parseability>
XML provides unambiguous boundaries and semantic meaning. Claude can reliably:
- Identify section boundaries (where content starts and ends)
- Understand content purpose (what role each section plays)
- Skip irrelevant sections (progressive disclosure)
- Parse programmatically (validation tools can check structure)

Markdown headings are just visual formatting. Claude must infer meaning from heading text, which is less reliable.
</parseability>

<token_efficiency>
XML tags are more efficient than markdown headings:

**Markdown headings**:
```markdown
## Quick start
## Workflow
## Advanced features
## Success criteria
```
Total: ~20 tokens, no semantic meaning to Claude

**XML tags**:
```xml
<quick_start>
<workflow>
<advanced_features>
<success_criteria>
```
Total: ~15 tokens, semantic meaning built-in

Savings compound across all skills in the ecosystem.
</token_efficiency>

<claude_performance>
Claude performs better with pure XML because:
- Unambiguous section boundaries reduce parsing errors
- Semantic tags convey intent directly (no inference needed)
- Nested tags create clear hierarchies
- Consistent structure across skills reduces cognitive load
- Progressive disclosure works more reliably

Pure XML structure is not just a style preference—it's a performance optimization.
</claude_performance>
</why_xml>

<critical_rule>
**Remove ALL markdown headings (#, ##, ###) from skill body content.** Replace with semantic XML tags. Keep markdown formatting WITHIN content (bold, italic, lists, code blocks, links).
</critical_rule>

<required_tags>
Every skill MUST have:
- `<objective>` - What the skill does and why it matters
- `<quick_start>` - Immediate, actionable guidance
- `<success_criteria>` or `<when_successful>` - How to know it worked

See [use-xml-tags.md](use-xml-tags.md) for conditional tags and intelligence rules.
</required_tags>
</xml_structure_principle>

<conciseness_principle>
<description>
The context window is shared. Your skill shares it with the system prompt, conversation history, other skills' metadata, and the actual request.
</description>

<guidance>
Only add context Claude doesn't already have. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

Assume Claude is smart. Don't explain obvious concepts.
</guidance>

<concise_example>
**Concise** (~50 tokens):
```xml
<quick_start>
Extract PDF text with pdfplumber:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
</quick_start>
```

**Verbose** (~150 tokens):
```xml
<quick_start>
PDF files are a common file format used for documents. To extract text from them, we'll use a Python library called pdfplumber. First, you'll need to import the library, then open the PDF file using the open method, and finally extract the text from each page. Here's how to do it:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

This code opens the PDF and extracts text from the first page.
</quick_start>
```

The concise version assumes Claude knows what PDFs are, understands Python imports, and can read code. All those assumptions are correct.
</concise_example>

<when_to_elaborate>
Add explanation when:
- Concept is domain-specific (not general programming knowledge)
- Pattern is non-obvious or counterintuitive
- Context affects behavior in subtle ways
- Trade-offs require judgment

Don't add explanation for:
- Common programming concepts (loops, functions, imports)
- Standard library usage (reading files, making HTTP requests)
- Well-known tools (git, npm, pip)
- Obvious next steps
</when_to_elaborate>
</conciseness_principle>

<degrees_of_freedom_principle>
<description>
Match the level of specificity to the task's fragility and variability. Give Claude more freedom for creative tasks, less freedom for fragile operations.
</description>

<high_freedom>
<when>
- Multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach
- Creative solutions welcome
</when>

<example>
```xml
<objective>
Review code for quality, bugs, and maintainability.
</objective>

<workflow>
1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
</workflow>

<success_criteria>
- All major issues identified
- Suggestions are actionable and specific
- Review balances praise and criticism
</success_criteria>
```

Claude has freedom to adapt the review based on what the code needs.
</example>
</high_freedom>

<medium_freedom>
<when>
- A preferred pattern exists
- Some variation is acceptable
- Configuration affects behavior
- Template can be adapted
</when>

<example>
```xml
<objective>
Generate reports with customizable format and sections.
</objective>

<report_template>
Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
</report_template>

<success_criteria>
- Report includes all required sections
- Format matches user preference
- Data accurately represented
</success_criteria>
```

Claude can customize the template based on requirements.
</example>
</medium_freedom>

<low_freedom>
<when>
- Operations are fragile and error-prone
- Consistency is critical
- A specific sequence must be followed
- Deviation causes failures
</when>

<example>
```xml
<objective>
Run database migration with exact sequence to prevent data loss.
</objective>

<workflow>
Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

**Do not modify the command or add additional flags.**
</workflow>

<success_criteria>
- Migration completes without errors
- Backup created before migration
- Verification confirms data integrity
</success_criteria>
```

Claude must follow the exact command with no variation.
</example>
</low_freedom>

<matching_specificity>
The key is matching specificity to fragility:

- **Fragile operations** (database migrations, payment processing, security): Low freedom, exact instructions
- **Standard operations** (API calls, file processing, data transformation): Medium freedom, preferred pattern with flexibility
- **Creative operations** (code review, content generation, analysis): High freedom, heuristics and principles

Mismatched specificity causes problems:
- Too much freedom on fragile tasks → errors and failures
- Too little freedom on creative tasks → rigid, suboptimal outputs
</matching_specificity>
</degrees_of_freedom_principle>

<model_testing_principle>
<description>
Skills act as additions to models, so effectiveness depends on the underlying model. What works for Opus might need more detail for Haiku.
</description>

<testing_across_models>
Test your skill with all models you plan to use:

<haiku_testing>
**Claude Haiku** (fast, economical)

Questions to ask:
- Does the skill provide enough guidance?
- Are examples clear and complete?
- Do implicit assumptions become explicit?
- Does Haiku need more structure?

Haiku benefits from:
- More explicit instructions
- Complete examples (no partial code)
- Clear success criteria
- Step-by-step workflows
</haiku_testing>

<sonnet_testing>
**Claude Sonnet** (balanced)

Questions to ask:
- Is the skill clear and efficient?
- Does it avoid over-explanation?
- Are workflows well-structured?
- Does progressive disclosure work?

Sonnet benefits from:
- Balanced detail level
- XML structure for clarity
- Progressive disclosure
- Concise but complete guidance
</sonnet_testing>

<opus_testing>
**Claude Opus** (powerful reasoning)

Questions to ask:
- Does the skill avoid over-explaining?
- Can Opus infer obvious steps?
- Are constraints clear?
- Is context minimal but sufficient?

Opus benefits from:
- Concise instructions
- Principles over procedures
- High degrees of freedom
- Trust in reasoning capabilities
</opus_testing>
</testing_across_models>

<balancing_across_models>
Aim for instructions that work well across all target models:

**Good balance**:
```xml
<quick_start>
Use pdfplumber for text extraction:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
</quick_start>
```

This works for all models:
- Haiku gets complete working example
- Sonnet gets clear default with escape hatch
- Opus gets enough context without over-explanation

**Too minimal for Haiku**:
```xml
<quick_start>
Use pdfplumber for text extraction.
</quick_start>
```

**Too verbose for Opus**:
```xml
<quick_start>
PDF files are documents that contain text. To extract that text, we use a library called pdfplumber. First, import the library at the top of your Python file. Then, open the PDF file using the pdfplumber.open() method. This returns a PDF object. Access the pages attribute to get a list of pages. Each page has an extract_text() method that returns the text content...
</quick_start>
```
</balancing_across_models>

<iterative_improvement>
1. Start with medium detail level
2. Test with target models
3. Observe where models struggle or succeed
4. Adjust based on actual performance
5. Re-test and iterate

Don't optimize for one model. Find the balance that works across your target models.
</iterative_improvement>
</model_testing_principle>

<progressive_disclosure_principle>
<description>
SKILL.md serves as an overview. Reference files contain details. Claude loads reference files only when needed.
</description>

<token_efficiency>
Progressive disclosure keeps token usage proportional to task complexity:

- Simple task: Load SKILL.md only (~500 tokens)
- Medium task: Load SKILL.md + one reference (~1000 tokens)
- Complex task: Load SKILL.md + multiple references (~2000 tokens)

Without progressive disclosure, every task loads all content regardless of need.
</token_efficiency>

<implementation>
- Keep SKILL.md under 500 lines
- Split detailed content into reference files
- Keep references one level deep from SKILL.md
- Link to references from relevant sections
- Use descriptive reference file names

See [skill-structure.md](skill-structure.md) for progressive disclosure patterns.
</implementation>
</progressive_disclosure_principle>

<validation_principle>
<description>
Validation scripts are force multipliers. They catch errors that Claude might miss and provide actionable feedback.
</description>

<characteristics>
Good validation scripts:
- Provide verbose, specific error messages
- Show available valid options when something is invalid
- Pinpoint exact location of problems
- Suggest actionable fixes
- Are deterministic and reliable

See [workflows-and-validation.md](workflows-and-validation.md) for validation patterns.
</characteristics>
</validation_principle>

<principle_summary>
<xml_structure>
Use pure XML structure for consistency, parseability, and Claude performance. Required tags: objective, quick_start, success_criteria.
</xml_structure>

<conciseness>
Only add context Claude doesn't have. Assume Claude is smart. Challenge every piece of content.
</conciseness>

<degrees_of_freedom>
Match specificity to fragility. High freedom for creative tasks, low freedom for fragile operations, medium for standard work.
</degrees_of_freedom>

<model_testing>
Test with all target models. Balance detail level to work across Haiku, Sonnet, and Opus.
</model_testing>

<progressive_disclosure>
Keep SKILL.md concise. Split details into reference files. Load reference files only when needed.
</progressive_disclosure>

<validation>
Make validation scripts verbose and specific. Catch errors early with actionable feedback.
</validation>
</principle_summary>

---

## Reference: Executable Code

<when_to_use_scripts>
Even if Claude could write a script, pre-made scripts offer advantages:
- More reliable than generated code
- Save tokens (no need to include code in context)
- Save time (no code generation required)
- Ensure consistency across uses

<execution_vs_reference>
Make clear whether Claude should:
- **Execute the script** (most common): "Run `analyze_form.py` to extract fields"
- **Read it as reference** (for complex logic): "See `analyze_form.py` for the extraction algorithm"

For most utility scripts, execution is preferred.
</execution_vs_reference>

<how_scripts_work>
When Claude executes a script via bash:
1. Script code never enters context window
2. Only script output consumes tokens
3. Far more efficient than having Claude generate equivalent code
</how_scripts_work>
</when_to_use_scripts>

<file_organization>
<scripts_directory>
**Best practice**: Place all executable scripts in a `scripts/` subdirectory within the skill folder.

```
skill-name/
├── SKILL.md
├── scripts/
│   ├── main_utility.py
│   ├── helper_script.py
│   └── validator.py
└── references/
    └── api-docs.md
```

**Benefits**:
- Keeps skill root clean and organized
- Clear separation between documentation and executable code
- Consistent pattern across all skills
- Easy to reference: `python scripts/script_name.py`

**Reference pattern**: In SKILL.md, reference scripts using the `scripts/` path:

```bash
python ~/.claude/skills/skill-name/scripts/analyze.py input.har
```
</scripts_directory>
</file_organization>

<utility_scripts_pattern>
<example>
## Utility scripts

**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": { "type": "text", "x": 100, "y": 200 },
  "signature": { "type": "sig", "x": 150, "y": 500 }
}
```

**validate_boxes.py**: Check for overlapping bounding boxes

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**: Apply field values to PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
</example>
</utility_scripts_pattern>

<solve_dont_punt>
Handle error conditions rather than punting to Claude.

<example type="good">
```python
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        print(f"Cannot access {path}, using default")
        return ''
```
</example>

<example type="bad">
```python
def process_file(path):
    # Just fail and let Claude figure it out
    return open(path).read()
```
</example>

<configuration_values>
Document configuration parameters to avoid "voodoo constants":

<example type="good">
```python
# HTTP requests typically complete within 30 seconds
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
MAX_RETRIES = 3
```
</example>

<example type="bad">
```python
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```
</example>
</configuration_values>
</solve_dont_punt>

<package_dependencies>
<runtime_constraints>
Skills run in code execution environment with platform-specific limitations:
- **claude.ai**: Can install packages from npm and PyPI
- **Anthropic API**: No network access and no runtime package installation
</runtime_constraints>

<guidance>
List required packages in your SKILL.md and verify they're available.

<example type="good">
Install required package: `pip install pypdf`

Then use it:

```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```
</example>

<example type="bad">
"Use the pdf library to process the file."
</example>
</guidance>
</package_dependencies>

<mcp_tool_references>
If your Skill uses MCP (Model Context Protocol) tools, always use fully qualified tool names.

<format>ServerName:tool_name</format>

<examples>
- Use the BigQuery:bigquery_schema tool to retrieve table schemas.
- Use the GitHub:create_issue tool to create issues.
</examples>

Without the server prefix, Claude may fail to locate the tool, especially when multiple MCP servers are available.
</mcp_tool_references>

---

## Reference: Iteration And Testing

<overview>
Skills improve through iteration and testing. This reference covers evaluation-driven development, Claude A/B testing patterns, and XML structure validation during testing.
</overview>

<evaluation_driven_development>
<principle>
Create evaluations BEFORE writing extensive documentation. This ensures your skill solves real problems rather than documenting imagined ones.
</principle>

<workflow>
<step_1>
**Identify gaps**: Run Claude on representative tasks without a skill. Document specific failures or missing context.
</step_1>

<step_2>
**Create evaluations**: Build three scenarios that test these gaps.
</step_2>

<step_3>
**Establish baseline**: Measure Claude's performance without the skill.
</step_3>

<step_4>
**Write minimal instructions**: Create just enough content to address the gaps and pass evaluations.
</step_4>

<step_5>
**Iterate**: Execute evaluations, compare against baseline, and refine.
</step_5>
</workflow>

<evaluation_structure>
```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using appropriate library",
    "Extracts text content from all pages without missing any",
    "Saves extracted text to output.txt in clear, readable format"
  ]
}
```
</evaluation_structure>

<why_evaluations_first>
- Prevents documenting imagined problems
- Forces clarity about what success looks like
- Provides objective measurement of skill effectiveness
- Keeps skill focused on actual needs
- Enables quantitative improvement tracking
</why_evaluations_first>
</evaluation_driven_development>

<iterative_development_with_claude>
<principle>
The most effective skill development uses Claude itself. Work with "Claude A" (expert who helps refine) to create skills used by "Claude B" (agent executing tasks).
</principle>

<creating_skills>
<workflow>
<step_1>
**Complete task without skill**: Work through problem with Claude A, noting what context you repeatedly provide.
</step_1>

<step_2>
**Ask Claude A to create skill**: "Create a skill that captures this pattern we just used"
</step_2>

<step_3>
**Review for conciseness**: Remove unnecessary explanations.
</step_3>

<step_4>
**Improve architecture**: Organize content with progressive disclosure.
</step_4>

<step_5>
**Test with Claude B**: Use fresh instance to test on real tasks.
</step_5>

<step_6>
**Iterate based on observation**: Return to Claude A with specific issues observed.
</step_6>
</workflow>

<insight>
Claude models understand skill format natively. Simply ask Claude to create a skill and it will generate properly structured SKILL.md content.
</insight>
</creating_skills>

<improving_skills>
<workflow>
<step_1>
**Use skill in real workflows**: Give Claude B actual tasks.
</step_1>

<step_2>
**Observe behavior**: Where does it struggle, succeed, or make unexpected choices?
</step_2>

<step_3>
**Return to Claude A**: Share observations and current SKILL.md.
</step_3>

<step_4>
**Review suggestions**: Claude A might suggest reorganization, stronger language, or workflow restructuring.
</step_4>

<step_5>
**Apply and test**: Update skill and test again.
</step_5>

<step_6>
**Repeat**: Continue based on real usage, not assumptions.
</step_6>
</workflow>

<what_to_watch_for>
- **Unexpected exploration paths**: Structure might not be intuitive
- **Missed connections**: Links might need to be more explicit
- **Overreliance on sections**: Consider moving frequently-read content to main SKILL.md
- **Ignored content**: Poorly signaled or unnecessary files
- **Critical metadata**: The name and description in your skill's metadata are critical for discovery
</what_to_watch_for>
</improving_skills>
</iterative_development_with_claude>

<model_testing>
<principle>
Test with all models you plan to use. Different models have different strengths and need different levels of detail.
</principle>

<haiku_testing>
**Claude Haiku** (fast, economical)

Questions to ask:
- Does the skill provide enough guidance?
- Are examples clear and complete?
- Do implicit assumptions become explicit?
- Does Haiku need more structure?

Haiku benefits from:
- More explicit instructions
- Complete examples (no partial code)
- Clear success criteria
- Step-by-step workflows
</haiku_testing>

<sonnet_testing>
**Claude Sonnet** (balanced)

Questions to ask:
- Is the skill clear and efficient?
- Does it avoid over-explanation?
- Are workflows well-structured?
- Does progressive disclosure work?

Sonnet benefits from:
- Balanced detail level
- XML structure for clarity
- Progressive disclosure
- Concise but complete guidance
</sonnet_testing>

<opus_testing>
**Claude Opus** (powerful reasoning)

Questions to ask:
- Does the skill avoid over-explaining?
- Can Opus infer obvious steps?
- Are constraints clear?
- Is context minimal but sufficient?

Opus benefits from:
- Concise instructions
- Principles over procedures
- High degrees of freedom
- Trust in reasoning capabilities
</opus_testing>

<balancing_across_models>
What works for Opus might need more detail for Haiku. Aim for instructions that work well across all target models. Find the balance that serves your target audience.

See [core-principles.md](core-principles.md) for model testing examples.
</balancing_across_models>
</model_testing>

<xml_structure_validation>
<principle>
During testing, validate that your skill's XML structure is correct and complete.
</principle>

<validation_checklist>
After updating a skill, verify:

<required_tags_present>
- ✅ `<objective>` tag exists and defines what skill does
- ✅ `<quick_start>` tag exists with immediate guidance
- ✅ `<success_criteria>` or `<when_successful>` tag exists
</required_tags_present>

<no_markdown_headings>
- ✅ No `#`, `##`, or `###` headings in skill body
- ✅ All sections use XML tags instead
- ✅ Markdown formatting within tags is preserved (bold, italic, lists, code blocks)
</no_markdown_headings>

<proper_xml_nesting>
- ✅ All XML tags properly closed
- ✅ Nested tags have correct hierarchy
- ✅ No unclosed tags
</proper_xml_nesting>

<conditional_tags_appropriate>
- ✅ Conditional tags match skill complexity
- ✅ Simple skills use required tags only
- ✅ Complex skills add appropriate conditional tags
- ✅ No over-engineering or under-specifying
</conditional_tags_appropriate>

<reference_files_check>
- ✅ Reference files also use pure XML structure
- ✅ Links to reference files are correct
- ✅ References are one level deep from SKILL.md
</reference_files_check>
</validation_checklist>

<testing_xml_during_iteration>
When iterating on a skill:

1. Make changes to XML structure
2. **Validate XML structure** (check tags, nesting, completeness)
3. Test with Claude on representative tasks
4. Observe if XML structure aids or hinders Claude's understanding
5. Iterate structure based on actual performance
</testing_xml_during_iteration>
</xml_structure_validation>

<observation_based_iteration>
<principle>
Iterate based on what you observe, not what you assume. Real usage reveals issues assumptions miss.
</principle>

<observation_categories>
<what_claude_reads>
Which sections does Claude actually read? Which are ignored? This reveals:
- Relevance of content
- Effectiveness of progressive disclosure
- Whether section names are clear
</what_claude_reads>

<where_claude_struggles>
Which tasks cause confusion or errors? This reveals:
- Missing context
- Unclear instructions
- Insufficient examples
- Ambiguous requirements
</where_claude_struggles>

<where_claude_succeeds>
Which tasks go smoothly? This reveals:
- Effective patterns
- Good examples
- Clear instructions
- Appropriate detail level
</where_claude_succeeds>

<unexpected_behaviors>
What does Claude do that surprises you? This reveals:
- Unstated assumptions
- Ambiguous phrasing
- Missing constraints
- Alternative interpretations
</unexpected_behaviors>
</observation_categories>

<iteration_pattern>
1. **Observe**: Run Claude on real tasks with current skill
2. **Document**: Note specific issues, not general feelings
3. **Hypothesize**: Why did this issue occur?
4. **Fix**: Make targeted changes to address specific issues
5. **Test**: Verify fix works on same scenario
6. **Validate**: Ensure fix doesn't break other scenarios
7. **Repeat**: Continue with next observed issue
</iteration_pattern>
</observation_based_iteration>

<progressive_refinement>
<principle>
Skills don't need to be perfect initially. Start minimal, observe usage, add what's missing.
</principle>

<initial_version>
Start with:
- Valid YAML frontmatter
- Required XML tags: objective, quick_start, success_criteria
- Minimal working example
- Basic success criteria

Skip initially:
- Extensive examples
- Edge case documentation
- Advanced features
- Detailed reference files
</initial_version>

<iteration_additions>
Add through iteration:
- Examples when patterns aren't clear from description
- Edge cases when observed in real usage
- Advanced features when users need them
- Reference files when SKILL.md approaches 500 lines
- Validation scripts when errors are common
</iteration_additions>

<benefits>
- Faster to initial working version
- Additions solve real needs, not imagined ones
- Keeps skills focused and concise
- Progressive disclosure emerges naturally
- Documentation stays aligned with actual usage
</benefits>
</progressive_refinement>

<testing_discovery>
<principle>
Test that Claude can discover and use your skill when appropriate.
</principle>

<discovery_testing>
<test_description>
Test if Claude loads your skill when it should:

1. Start fresh conversation (Claude B)
2. Ask question that should trigger skill
3. Check if skill was loaded
4. Verify skill was used appropriately
</test_description>

<description_quality>
If skill isn't discovered:
- Check description includes trigger keywords
- Verify description is specific, not vague
- Ensure description explains when to use skill
- Test with different phrasings of the same request

The description is Claude's primary discovery mechanism.
</description_quality>
</discovery_testing>
</testing_discovery>

<common_iteration_patterns>
<pattern name="too_verbose">
**Observation**: Skill works but uses lots of tokens

**Fix**:
- Remove obvious explanations
- Assume Claude knows common concepts
- Use examples instead of lengthy descriptions
- Move advanced content to reference files
</pattern>

<pattern name="too_minimal">
**Observation**: Claude makes incorrect assumptions or misses steps

**Fix**:
- Add explicit instructions where assumptions fail
- Provide complete working examples
- Define edge cases
- Add validation steps
</pattern>

<pattern name="poor_discovery">
**Observation**: Skill exists but Claude doesn't load it when needed

**Fix**:
- Improve description with specific triggers
- Add relevant keywords
- Test description against actual user queries
- Make description more specific about use cases
</pattern>

<pattern name="unclear_structure">
**Observation**: Claude reads wrong sections or misses relevant content

**Fix**:
- Use clearer XML tag names
- Reorganize content hierarchy
- Move frequently-needed content earlier
- Add explicit links to relevant sections
</pattern>

<pattern name="incomplete_examples">
**Observation**: Claude produces outputs that don't match expected pattern

**Fix**:
- Add more examples showing pattern
- Make examples more complete
- Show edge cases in examples
- Add anti-pattern examples (what not to do)
</pattern>
</common_iteration_patterns>

<iteration_velocity>
<principle>
Small, frequent iterations beat large, infrequent rewrites.
</principle>

<fast_iteration>
**Good approach**:
1. Make one targeted change
2. Test on specific scenario
3. Verify improvement
4. Commit change
5. Move to next issue

Total time: Minutes per iteration
Iterations per day: 10-20
Learning rate: High
</fast_iteration>

<slow_iteration>
**Problematic approach**:
1. Accumulate many issues
2. Make large refactor
3. Test everything at once
4. Debug multiple issues simultaneously
5. Hard to know what fixed what

Total time: Hours per iteration
Iterations per day: 1-2
Learning rate: Low
</slow_iteration>

<benefits_of_fast_iteration>
- Isolate cause and effect
- Build pattern recognition faster
- Less wasted work from wrong directions
- Easier to revert if needed
- Maintains momentum
</benefits_of_fast_iteration>
</iteration_velocity>

<success_metrics>
<principle>
Define how you'll measure if the skill is working. Quantify success.
</principle>

<objective_metrics>
- **Success rate**: Percentage of tasks completed correctly
- **Token usage**: Average tokens consumed per task
- **Iteration count**: How many tries to get correct output
- **Error rate**: Percentage of tasks with errors
- **Discovery rate**: How often skill loads when it should
</objective_metrics>

<subjective_metrics>
- **Output quality**: Does output meet requirements?
- **Appropriate detail**: Too verbose or too minimal?
- **Claude confidence**: Does Claude seem uncertain?
- **User satisfaction**: Does skill solve the actual problem?
</subjective_metrics>

<tracking_improvement>
Compare metrics before and after changes:
- Baseline: Measure without skill
- Initial: Measure with first version
- Iteration N: Measure after each change

Track which changes improve which metrics. Double down on effective patterns.
</tracking_improvement>
</success_metrics>

---

## Reference: Official Spec

# Official Skill Specification (2026)

Source: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)

## Commands and Skills Are Merged

Custom slash commands have been merged into skills. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work the same way. Existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter to control invocation, and automatic context loading.

If a skill and a command share the same name, the skill takes precedence.

## SKILL.md File Structure

Every skill requires a `SKILL.md` file with YAML frontmatter followed by standard markdown instructions.

```markdown
---
name: your-skill-name
description: What it does and when to use it
---

# Your Skill Name

## Instructions
Clear, step-by-step guidance.

## Examples
Concrete examples of using this skill.
```

## Complete Frontmatter Reference

All fields are optional. Only `description` is recommended.

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name. Lowercase letters, numbers, hyphens only (max 64 chars). Defaults to directory name if omitted. |
| `description` | Recommended | What it does AND when to use it (max 1024 chars). Claude uses this to decide when to apply the skill. |
| `argument-hint` | No | Hint shown during autocomplete. Example: `[issue-number]` or `[filename] [format]` |
| `disable-model-invocation` | No | Set `true` to prevent Claude from auto-loading. Use for manual workflows. Default: `false` |
| `user-invocable` | No | Set `false` to hide from `/` menu. Use for background knowledge. Default: `true` |
| `allowed-tools` | No | Tools Claude can use without permission prompts. Example: `Read, Bash(git *)` |
| `model` | No | Model to use: `haiku`, `sonnet`, or `opus` |
| `context` | No | Set `fork` to run in isolated subagent context |
| `agent` | No | Subagent type when `context: fork`. Options: `Explore`, `Plan`, `general-purpose`, or custom agent name |
| `hooks` | No | Hooks scoped to this skill's lifecycle |

## Invocation Control

| Frontmatter | User can invoke | Claude can invoke | When loaded into context |
|-------------|----------------|-------------------|--------------------------|
| (default) | Yes | Yes | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description not in context, full skill loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context, full skill loads when invoked |

## Skill Locations & Priority

```
Enterprise (highest priority) → Personal → Project → Plugin (lowest priority)
```

| Type | Path | Applies to |
|------|------|-----------|
| Enterprise | See managed settings | All users in organization |
| Personal | `~/.claude/skills/<name>/SKILL.md` | You, across all projects |
| Project | `.claude/skills/<name>/SKILL.md` | Anyone working in repository |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled |

Plugin skills use a `plugin-name:skill-name` namespace, so they cannot conflict with other levels.

## How Skills Work

1. **Discovery**: Claude loads only name and description at startup (2% of context window budget)
2. **Activation**: When your request matches a skill's description, Claude loads the full content
3. **Execution**: Claude follows the skill's instructions

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session ID |

## Dynamic Context Injection

The `` !`command` `` syntax runs shell commands before content is sent to Claude:

```markdown
## Context
- Current branch: !`git branch --show-current`
- PR diff: !`gh pr diff`
```

Commands execute immediately and their output replaces the placeholder. Claude only sees the final result.

## Progressive Disclosure

```
my-skill/
├── SKILL.md           # Entry point (required)
├── reference.md       # Detailed docs (loaded when needed)
├── examples.md        # Usage examples (loaded when needed)
└── scripts/
    └── helper.py      # Utility script (executed, not loaded)
```

Keep SKILL.md under 500 lines. Link to supporting files:
```markdown
For API details, see [reference.md](reference.md).
```

## Running in a Subagent

Add `context: fork` to run in isolation:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly...
```

The skill content becomes the subagent's prompt. It won't have access to conversation history.

## Distribution

- **Project skills**: Commit `.claude/skills/` to version control
- **Plugins**: Add `skills/` directory to plugin
- **Enterprise**: Deploy organization-wide through managed settings

---

## Reference: Recommended Structure

# Recommended Skill Structure

The optimal structure for complex skills separates routing, workflows, and knowledge.

<structure>
```
skill-name/
├── SKILL.md              # Router + essential principles (unavoidable)
├── workflows/            # Step-by-step procedures (how)
│   ├── workflow-a.md
│   ├── workflow-b.md
│   └── ...
└── references/           # Domain knowledge (what)
    ├── reference-a.md
    ├── reference-b.md
    └── ...
```
</structure>

<why_this_works>
## Problems This Solves

**Problem 1: Context gets skipped**
When important principles are in a separate file, Claude may not read them.
**Solution:** Put essential principles directly in SKILL.md. They load automatically.

**Problem 2: Wrong context loaded**
A "build" task loads debugging references. A "debug" task loads build references.
**Solution:** Intake question determines intent → routes to specific workflow → workflow specifies which references to read.

**Problem 3: Monolithic skills are overwhelming**
500+ lines of mixed content makes it hard to find relevant parts.
**Solution:** Small router (SKILL.md) + focused workflows + reference library.

**Problem 4: Procedures mixed with knowledge**
"How to do X" mixed with "What X means" creates confusion.
**Solution:** Workflows are procedures (steps). References are knowledge (patterns, examples).
</why_this_works>

<skill_md_template>
## SKILL.md Template

```markdown
---
name: skill-name
description: What it does and when to use it.
---

<essential_principles>
## How This Skill Works

[Inline principles that apply to ALL workflows. Cannot be skipped.]

### Principle 1: [Name]
[Brief explanation]

### Principle 2: [Name]
[Brief explanation]
</essential_principles>

<intake>
**Ask the user:**

What would you like to do?
1. [Option A]
2. [Option B]
3. [Option C]
4. Something else

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "keyword", "keyword" | `workflows/option-a.md` |
| 2, "keyword", "keyword" | `workflows/option-b.md` |
| 3, "keyword", "keyword" | `workflows/option-c.md` |
| 4, other | Clarify, then select |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**Category A:** file-a.md, file-b.md
**Category B:** file-c.md, file-d.md
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| option-a.md | [What it does] |
| option-b.md | [What it does] |
| option-c.md | [What it does] |
</workflows_index>
```
</skill_md_template>

<workflow_template>
## Workflow Template

```markdown
# Workflow: [Name]

<required_reading>
**Read these reference files NOW:**
1. references/relevant-file.md
2. references/another-file.md
</required_reading>

<process>
## Step 1: [Name]
[What to do]

## Step 2: [Name]
[What to do]

## Step 3: [Name]
[What to do]
</process>

<success_criteria>
This workflow is complete when:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
</success_criteria>
```
</workflow_template>

<when_to_use_this_pattern>
## When to Use This Pattern

**Use router + workflows + references when:**
- Multiple distinct workflows (build vs debug vs ship)
- Different workflows need different references
- Essential principles must not be skipped
- Skill has grown beyond 200 lines

**Use simple single-file skill when:**
- One workflow
- Small reference set
- Under 200 lines total
- No essential principles to enforce
</when_to_use_this_pattern>

<key_insight>
## The Key Insight

**SKILL.md is always loaded. Use this guarantee.**

Put unavoidable content in SKILL.md:
- Essential principles
- Intake question
- Routing logic

Put workflow-specific content in workflows/:
- Step-by-step procedures
- Required references for that workflow
- Success criteria for that workflow

Put reusable knowledge in references/:
- Patterns and examples
- Technical details
- Domain expertise
</key_insight>

---

## Reference: Skill Structure

# Skill Structure Reference

Skills have three structural components: YAML frontmatter (metadata), standard markdown body (content), and progressive disclosure (file organization).

## Body Format

Use **standard markdown headings** for structure. Keep markdown formatting within content (bold, italic, lists, code blocks, links).

```markdown
---
name: my-skill
description: What it does and when to use it
---

# Skill Name

## Quick Start
Immediate actionable guidance...

## Instructions
Step-by-step procedures...

## Examples
Concrete usage examples...

## Guidelines
Rules and constraints...
```

## Recommended Sections

Every skill should have:

- **Quick Start** - Immediate, actionable guidance (minimal working example)
- **Instructions** - Core step-by-step guidance
- **Success Criteria** - How to know it worked

Add based on complexity:

- **Context** - Background/situational information
- **Workflow** - Multi-step procedures
- **Examples** - Concrete input/output pairs
- **Advanced Features** - Deep-dive topics (link to reference files)
- **Anti-Patterns** - Common mistakes to avoid
- **Guidelines** - Rules and constraints

## YAML Frontmatter

### Required/Recommended Fields

```yaml
---
name: skill-name-here
description: What it does and when to use it (specific triggers included)
---
```

### Name Field

**Validation rules:**
- Maximum 64 characters
- Lowercase letters, numbers, hyphens only
- Must match directory name
- No reserved words: "anthropic", "claude"

**Examples:**
- `triage-prs`
- `deploy-production`
- `review-code`
- `setup-stripe-payments`

**Avoid:** `helper`, `utils`, `tools`, generic names

### Description Field

**Validation rules:**
- Maximum 1024 characters
- Include what it does AND when to use it
- Third person voice

**Good:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad:**
```yaml
description: Helps with documents
```

### Optional Fields

| Field | Description |
|-------|-------------|
| `argument-hint` | Usage hints. Example: `[issue-number]` |
| `disable-model-invocation` | `true` to prevent auto-loading. Use for side-effect workflows. |
| `user-invocable` | `false` to hide from `/` menu. Use for background knowledge. |
| `allowed-tools` | Tools without permission prompts. Example: `Read, Bash(git *)` |
| `model` | `haiku`, `sonnet`, or `opus` |
| `context` | `fork` for isolated subagent execution |
| `agent` | Subagent type: `Explore`, `Plan`, `general-purpose`, or custom |

## Naming Conventions

Use descriptive names that indicate purpose:

| Pattern | Examples |
|---------|----------|
| Action-oriented | `triage-prs`, `deploy-production`, `review-code` |
| Domain-specific | `setup-stripe-payments`, `manage-facebook-ads` |
| Descriptive | `git-worktree`, `frontend-design`, `dhh-rails-style` |

## Progressive Disclosure

Keep SKILL.md under 500 lines. Split into reference files:

```
my-skill/
├── SKILL.md           # Entry point (required, overview + navigation)
├── reference.md       # Detailed docs (loaded when needed)
├── examples.md        # Usage examples (loaded when needed)
└── scripts/
    └── helper.py      # Utility script (executed, not loaded)
```

**Rules:**
- Keep references one level deep from SKILL.md
- Add table of contents to reference files over 100 lines
- Use forward slashes in paths: `scripts/helper.py`
- Name files descriptively: `form_validation_rules.md` not `doc2.md`

## Validation Checklist

Before finalizing:

- [ ] YAML frontmatter valid (name matches directory, description specific)
- [ ] Uses standard markdown headings (not XML tags)
- [ ] Has Quick Start, Instructions, and Success Criteria sections
- [ ] `disable-model-invocation: true` if skill has side effects
- [ ] SKILL.md under 500 lines
- [ ] Reference files linked properly from SKILL.md
- [ ] File paths use forward slashes
- [ ] Tested with real usage

## Anti-Patterns

- **XML tags in body** - Use standard markdown headings
- **Vague descriptions** - Be specific with trigger keywords
- **Deep nesting** - Keep references one level from SKILL.md
- **Missing invocation control** - Side-effect workflows need `disable-model-invocation: true`
- **Inconsistent naming** - Directory name must match `name` field
- **Windows paths** - Always use forward slashes

---

## Reference: Using Scripts

# Using Scripts in Skills

<purpose>
Scripts are executable code that Claude runs as-is rather than regenerating each time. They ensure reliable, error-free execution of repeated operations.
</purpose>

<when_to_use>
Use scripts when:
- The same code runs across multiple skill invocations
- Operations are error-prone when rewritten from scratch
- Complex shell commands or API interactions are involved
- Consistency matters more than flexibility

Common script types:
- **Deployment** - Deploy to Vercel, publish packages, push releases
- **Setup** - Initialize projects, install dependencies, configure environments
- **API calls** - Authenticated requests, webhook handlers, data fetches
- **Data processing** - Transform files, batch operations, migrations
- **Build processes** - Compile, bundle, test runners
</when_to_use>

<script_structure>
Scripts live in `scripts/` within the skill directory:

```
skill-name/
├── SKILL.md
├── workflows/
├── references/
├── templates/
└── scripts/
    ├── deploy.sh
    ├── setup.py
    └── fetch-data.ts
```

A well-structured script includes:
1. Clear purpose comment at top
2. Input validation
3. Error handling
4. Idempotent operations where possible
5. Clear output/feedback
</script_structure>

<script_example>
```bash
#!/bin/bash
# deploy.sh - Deploy project to Vercel
# Usage: ./deploy.sh [environment]
# Environments: preview (default), production

set -euo pipefail

ENVIRONMENT="${1:-preview}"

# Validate environment
if [[ "$ENVIRONMENT" != "preview" && "$ENVIRONMENT" != "production" ]]; then
    echo "Error: Environment must be 'preview' or 'production'"
    exit 1
fi

echo "Deploying to $ENVIRONMENT..."

if [[ "$ENVIRONMENT" == "production" ]]; then
    vercel --prod
else
    vercel
fi

echo "Deployment complete."
```
</script_example>

<workflow_integration>
Workflows reference scripts like this:

```xml
<process>
## Step 5: Deploy

1. Ensure all tests pass
2. Run `scripts/deploy.sh production`
3. Verify deployment succeeded
4. Update user with deployment URL
</process>
```

The workflow tells Claude WHEN to run the script. The script handles HOW the operation executes.
</workflow_integration>

<best_practices>
**Do:**
- Make scripts idempotent (safe to run multiple times)
- Include clear usage comments
- Validate inputs before executing
- Provide meaningful error messages
- Use `set -euo pipefail` in bash scripts

**Don't:**
- Hardcode secrets or credentials (use environment variables)
- Create scripts for one-off operations
- Skip error handling
- Make scripts do too many unrelated things
- Forget to make scripts executable (`chmod +x`)
</best_practices>

<security_considerations>
- Never embed API keys, tokens, or secrets in scripts
- Use environment variables for sensitive configuration
- Validate and sanitize any user-provided inputs
- Be cautious with scripts that delete or modify data
- Consider adding `--dry-run` options for destructive operations
</security_considerations>

---

## Reference: Using Templates

# Using Templates in Skills

<purpose>
Templates are reusable output structures that Claude copies and fills in. They ensure consistent, high-quality outputs without regenerating structure each time.
</purpose>

<when_to_use>
Use templates when:
- Output should have consistent structure across invocations
- The structure matters more than creative generation
- Filling placeholders is more reliable than blank-page generation
- Users expect predictable, professional-looking outputs

Common template types:
- **Plans** - Project plans, implementation plans, migration plans
- **Specifications** - Technical specs, feature specs, API specs
- **Documents** - Reports, proposals, summaries
- **Configurations** - Config files, settings, environment setups
- **Scaffolds** - File structures, boilerplate code
</when_to_use>

<template_structure>
Templates live in `templates/` within the skill directory:

```
skill-name/
├── SKILL.md
├── workflows/
├── references/
└── templates/
    ├── plan-template.md
    ├── spec-template.md
    └── report-template.md
```

A template file contains:
1. Clear section markers
2. Placeholder indicators (use `{{placeholder}}` or `[PLACEHOLDER]`)
3. Inline guidance for what goes where
4. Example content where helpful
</template_structure>

<template_example>
```markdown
# {{PROJECT_NAME}} Implementation Plan

## Overview
{{1-2 sentence summary of what this plan covers}}

## Goals
- {{Primary goal}}
- {{Secondary goals...}}

## Scope
**In scope:**
- {{What's included}}

**Out of scope:**
- {{What's explicitly excluded}}

## Phases

### Phase 1: {{Phase name}}
**Duration:** {{Estimated duration}}
**Deliverables:**
- {{Deliverable 1}}
- {{Deliverable 2}}

### Phase 2: {{Phase name}}
...

## Success Criteria
- [ ] {{Measurable criterion 1}}
- [ ] {{Measurable criterion 2}}

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {{Risk}} | {{H/M/L}} | {{H/M/L}} | {{Strategy}} |
```
</template_example>

<workflow_integration>
Workflows reference templates like this:

```xml
<process>
## Step 3: Generate Plan

1. Read `templates/plan-template.md`
2. Copy the template structure
3. Fill each placeholder based on gathered requirements
4. Review for completeness
</process>
```

The workflow tells Claude WHEN to use the template. The template provides WHAT structure to produce.
</workflow_integration>

<best_practices>
**Do:**
- Keep templates focused on structure, not content
- Use clear placeholder syntax consistently
- Include brief inline guidance where sections might be ambiguous
- Make templates complete but minimal

**Don't:**
- Put excessive example content that might be copied verbatim
- Create templates for outputs that genuinely need creative generation
- Over-constrain with too many required sections
- Forget to update templates when requirements change
</best_practices>

---

## Reference: Workflows And Validation

<overview>
This reference covers patterns for complex workflows, validation loops, and feedback cycles in skill authoring. All patterns use pure XML structure.
</overview>

<complex_workflows>
<principle>
Break complex operations into clear, sequential steps. For particularly complex workflows, provide a checklist.
</principle>

<pdf_forms_example>
```xml
<objective>
Fill PDF forms with validated data from JSON field mappings.
</objective>

<workflow>
Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

<step_1>
**Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.
</step_1>

<step_2>
**Create field mapping**

Edit `fields.json` to add values for each field.
</step_2>

<step_3>
**Validate mapping**

Run: `python scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.
</step_3>

<step_4>
**Fill the form**

Run: `python scripts/fill_form.py input.pdf fields.json output.pdf`
</step_4>

<step_5>
**Verify output**

Run: `python scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.
</step_5>
</workflow>
```
</pdf_forms_example>

<when_to_use>
Use checklist pattern when:
- Workflow has 5+ sequential steps
- Steps must be completed in order
- Progress tracking helps prevent errors
- Easy resumption after interruption is valuable
</when_to_use>
</complex_workflows>

<feedback_loops>
<validate_fix_repeat_pattern>
<principle>
Run validator → fix errors → repeat. This pattern greatly improves output quality.
</principle>

<document_editing_example>
```xml
<objective>
Edit OOXML documents with XML validation at each step.
</objective>

<editing_process>
<step_1>
Make your edits to `word/document.xml`
</step_1>

<step_2>
**Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`
</step_2>

<step_3>
If validation fails:
- Review the error message carefully
- Fix the issues in the XML
- Run validation again
</step_3>

<step_4>
**Only proceed when validation passes**
</step_4>

<step_5>
Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
</step_5>

<step_6>
Test the output document
</step_6>
</editing_process>

<validation>
Never skip validation. Catching errors early prevents corrupted output files.
</validation>
```
</document_editing_example>

<why_it_works>
- Catches errors early before changes are applied
- Machine-verifiable with objective verification
- Plan can be iterated without touching originals
- Reduces total iteration cycles
</why_it_works>
</validate_fix_repeat_pattern>

<plan_validate_execute_pattern>
<principle>
When Claude performs complex, open-ended tasks, create a plan in a structured format, validate it, then execute.

Workflow: analyze → **create plan file** → **validate plan** → execute → verify
</principle>

<batch_update_example>
```xml
<objective>
Apply batch updates to spreadsheet with plan validation.
</objective>

<workflow>
<plan_phase>
<step_1>
Analyze the spreadsheet and requirements
</step_1>

<step_2>
Create `changes.json` with all planned updates
</step_2>
</plan_phase>

<validation_phase>
<step_3>
Validate the plan: `python scripts/validate_changes.py changes.json`
</step_3>

<step_4>
If validation fails:
- Review error messages
- Fix issues in changes.json
- Validate again
</step_4>

<step_5>
Only proceed when validation passes
</step_5>
</validation_phase>

<execution_phase>
<step_6>
Apply changes: `python scripts/apply_changes.py changes.json`
</step_6>

<step_7>
Verify output
</step_7>
</execution_phase>
</workflow>

<success_criteria>
- Plan validation passes with zero errors
- All changes applied successfully
- Output verification confirms expected results
</success_criteria>
```
</batch_update_example>

<implementation_tip>
Make validation scripts verbose with specific error messages:

**Good error message**:
"Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed"

**Bad error message**:
"Invalid field"

Specific errors help Claude fix issues without guessing.
</implementation_tip>

<when_to_use>
Use plan-validate-execute when:
- Operations are complex and error-prone
- Changes are irreversible or difficult to undo
- Planning can be validated independently
- Catching errors early saves significant time
</when_to_use>
</plan_validate_execute_pattern>
</feedback_loops>

<conditional_workflows>
<principle>
Guide Claude through decision points with clear branching logic.
</principle>

<document_modification_example>
```xml
<objective>
Modify DOCX files using appropriate method based on task type.
</objective>

<workflow>
<decision_point_1>
Determine the modification type:

**Creating new content?** → Follow "Creation workflow"
**Editing existing content?** → Follow "Editing workflow"
</decision_point_1>

<creation_workflow>
<objective>Build documents from scratch</objective>

<steps>
1. Use docx-js library
2. Build document from scratch
3. Export to .docx format
</steps>
</creation_workflow>

<editing_workflow>
<objective>Modify existing documents</objective>

<steps>
1. Unpack existing document
2. Modify XML directly
3. Validate after each change
4. Repack when complete
</steps>
</editing_workflow>
</workflow>

<success_criteria>
- Correct workflow chosen based on task type
- All steps in chosen workflow completed
- Output file validated and verified
</success_criteria>
```
</document_modification_example>

<when_to_use>
Use conditional workflows when:
- Different task types require different approaches
- Decision points are clear and well-defined
- Workflows are mutually exclusive
- Guiding Claude to correct path improves outcomes
</when_to_use>
</conditional_workflows>

<validation_scripts>
<principles>
Validation scripts are force multipliers. They catch errors that Claude might miss and provide actionable feedback for fixing issues.
</principles>

<characteristics_of_good_validation>
<verbose_errors>
**Good**: "Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed"

**Bad**: "Invalid field"

Verbose errors help Claude fix issues in one iteration instead of multiple rounds of guessing.
</verbose_errors>

<specific_feedback>
**Good**: "Line 47: Expected closing tag `</paragraph>` but found `</section>`"

**Bad**: "XML syntax error"

Specific feedback pinpoints exact location and nature of the problem.
</specific_feedback>

<actionable_suggestions>
**Good**: "Required field 'customer_name' is missing. Add: {\"customer_name\": \"value\"}"

**Bad**: "Missing required field"

Actionable suggestions show Claude exactly what to fix.
</actionable_suggestions>

<available_options>
When validation fails, show available valid options:

**Good**: "Invalid status 'pending_review'. Valid statuses: active, paused, archived"

**Bad**: "Invalid status"

Showing valid options eliminates guesswork.
</available_options>
</characteristics_of_good_validation>

<implementation_pattern>
```xml
<validation>
After making changes, validate immediately:

```bash
python scripts/validate.py output_dir/
```

If validation fails, fix errors before continuing. Validation errors include:

- **Field not found**: "Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed"
- **Type mismatch**: "Field 'order_total' expects number, got string"
- **Missing required field**: "Required field 'customer_name' is missing"
- **Invalid value**: "Invalid status 'pending_review'. Valid statuses: active, paused, archived"

Only proceed when validation passes with zero errors.
</validation>
```
</implementation_pattern>

<benefits>
- Catches errors before they propagate
- Reduces iteration cycles
- Provides learning feedback
- Makes debugging deterministic
- Enables confident execution
</benefits>
</validation_scripts>

<iterative_refinement>
<principle>
Many workflows benefit from iteration: generate → validate → refine → validate → finalize.
</principle>

<implementation_example>
```xml
<objective>
Generate reports with iterative quality improvement.
</objective>

<workflow>
<iteration_1>
**Generate initial draft**

Create report based on data and requirements.
</iteration_1>

<iteration_2>
**Validate draft**

Run: `python scripts/validate_report.py draft.md`

Fix any structural issues, missing sections, or data errors.
</iteration_2>

<iteration_3>
**Refine content**

Improve clarity, add supporting data, enhance visualizations.
</iteration_3>

<iteration_4>
**Final validation**

Run: `python scripts/validate_report.py final.md`

Ensure all quality criteria met.
</iteration_4>

<iteration_5>
**Finalize**

Export to final format and deliver.
</iteration_5>
</workflow>

<success_criteria>
- Final validation passes with zero errors
- All quality criteria met
- Report ready for delivery
</success_criteria>
```
</implementation_example>

<when_to_use>
Use iterative refinement when:
- Quality improves with multiple passes
- Validation provides actionable feedback
- Time permits iteration
- Perfect output matters more than speed
</when_to_use>
</iterative_refinement>

<checkpoint_pattern>
<principle>
For long workflows, add checkpoints where Claude can pause and verify progress before continuing.
</principle>

<implementation_example>
```xml
<workflow>
<phase_1>
**Data collection** (Steps 1-3)

1. Extract data from source
2. Transform to target format
3. **CHECKPOINT**: Verify data completeness

Only continue if checkpoint passes.
</phase_1>

<phase_2>
**Data processing** (Steps 4-6)

4. Apply business rules
5. Validate transformations
6. **CHECKPOINT**: Verify processing accuracy

Only continue if checkpoint passes.
</phase_2>

<phase_3>
**Output generation** (Steps 7-9)

7. Generate output files
8. Validate output format
9. **CHECKPOINT**: Verify final output

Proceed to delivery only if checkpoint passes.
</phase_3>
</workflow>

<checkpoint_validation>
At each checkpoint:
1. Run validation script
2. Review output for correctness
3. Verify no errors or warnings
4. Only proceed when validation passes
</checkpoint_validation>
```
</implementation_example>

<benefits>
- Prevents cascading errors
- Easier to diagnose issues
- Clear progress indicators
- Natural pause points for review
- Reduces wasted work from early errors
</benefits>
</checkpoint_pattern>

<error_recovery>
<principle>
Design workflows with clear error recovery paths. Claude should know what to do when things go wrong.
</principle>

<implementation_example>
```xml
<workflow>
<normal_path>
1. Process input file
2. Validate output
3. Save results
</normal_path>

<error_recovery>
**If validation fails in step 2:**
- Review validation errors
- Check if input file is corrupted → Return to step 1 with different input
- Check if processing logic failed → Fix logic, return to step 1
- Check if output format wrong → Fix format, return to step 2

**If save fails in step 3:**
- Check disk space
- Check file permissions
- Check file path validity
- Retry save with corrected conditions
</error_recovery>

<escalation>
**If error persists after 3 attempts:**
- Document the error with full context
- Save partial results if available
- Report issue to user with diagnostic information
</escalation>
</workflow>
```
</implementation_example>

<when_to_use>
Include error recovery when:
- Workflows interact with external systems
- File operations could fail
- Network calls could timeout
- User input could be invalid
- Errors are recoverable
</when_to_use>
</error_recovery>
