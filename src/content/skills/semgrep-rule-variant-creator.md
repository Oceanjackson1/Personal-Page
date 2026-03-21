---
title: "Semgrep Rule Variant Creator"
description: "Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to specified target languages. Takes an existing rule and target languages as input, produces independent rule+test directories for each language."
category: "development"
source: "community"
author: "Community"
tags: ["semgrep", "rule", "variant", "creator"]
date: 2026-03-20
---

# Semgrep Rule Variant Creator

Port existing Semgrep rules to new target languages with proper applicability analysis and test-driven validation.

## When to Use

**Ideal scenarios:**
- Porting an existing Semgrep rule to one or more target languages
- Creating language-specific variants of a universal vulnerability pattern
- Expanding rule coverage across a polyglot codebase
- Translating rules between languages with equivalent constructs

## When NOT to Use

Do NOT use this skill for:
- Creating a new Semgrep rule from scratch (use `semgrep-rule-creator` instead)
- Running existing rules against code
- Languages where the vulnerability pattern fundamentally doesn't apply
- Minor syntax variations within the same language

## Input Specification

This skill requires:
1. **Existing Semgrep rule** - YAML file path or YAML rule content
2. **Target languages** - One or more languages to port to (e.g., "Golang and Java")

## Output Specification

For each applicable target language, produces:
```
<original-rule-id>-<language>/
├── <original-rule-id>-<language>.yaml     # Ported Semgrep rule
└── <original-rule-id>-<language>.<ext>    # Test file with annotations
```

Example output for porting `sql-injection` to Go and Java:
```
sql-injection-golang/
├── sql-injection-golang.yaml
└── sql-injection-golang.go

sql-injection-java/
├── sql-injection-java.yaml
└── sql-injection-java.java
```

## Rationalizations to Reject

When porting Semgrep rules, reject these common shortcuts:

| Rationalization | Why It Fails | Correct Approach |
|-----------------|--------------|------------------|
| "Pattern structure is identical" | Different ASTs across languages | Always dump AST for target language |
| "Same vulnerability, same detection" | Data flow differs between languages | Analyze target language idioms |
| "Rule doesn't need tests since original worked" | Language edge cases differ | Write NEW test cases for target |
| "Skip applicability - it obviously applies" | Some patterns are language-specific | Complete applicability analysis first |
| "I'll create all variants then test" | Errors compound, hard to debug | Complete full cycle per language |
| "Library equivalent is close enough" | Surface similarity hides differences | Verify API semantics match |
| "Just translate the syntax 1:1" | Languages have different idioms | Research target language patterns |

## Strictness Level

This workflow is **strict** - do not skip steps:
- **Applicability analysis is mandatory**: Don't assume patterns translate
- **Each language is independent**: Complete full cycle before moving to next
- **Test-first for each variant**: Never write a rule without test cases
- **100% test pass required**: "Most tests pass" is not acceptable

## Overview

This skill guides the creation of language-specific variants of existing Semgrep rules. Each target language goes through an independent 4-phase cycle:

```
FOR EACH target language:
  Phase 1: Applicability Analysis → Verdict
  Phase 2: Test Creation (Test-First)
  Phase 3: Rule Creation
  Phase 4: Validation
  (Complete full cycle before moving to next language)
```

## Foundational Knowledge

**The `semgrep-rule-creator` skill is the authoritative reference for Semgrep rule creation fundamentals.** While this skill focuses on porting existing rules to new languages, the core principles of writing quality rules remain the same.

Consult `semgrep-rule-creator` for guidance on:
- **When to use taint mode vs pattern matching** - Choosing the right approach for the vulnerability type
- **Test-first methodology** - Why tests come before rules and how to write effective test cases
- **Anti-patterns to avoid** - Common mistakes like overly broad or overly specific patterns
- **Iterating until tests pass** - The validation loop and debugging techniques
- **Rule optimization** - Removing redundant patterns after tests pass

When porting a rule, you're applying these same principles in a new language context. If uncertain about rule structure or approach, refer to `semgrep-rule-creator` first.

## Four-Phase Workflow

### Phase 1: Applicability Analysis

Before porting, determine if the pattern applies to the target language.

**Analysis criteria:**
1. Does the vulnerability class exist in the target language?
2. Does an equivalent construct exist (function, pattern, library)?
3. Are the semantics similar enough for meaningful detection?

**Verdict options:**
- `APPLICABLE` → Proceed with variant creation
- `APPLICABLE_WITH_ADAPTATION` → Proceed but significant changes needed
- `NOT_APPLICABLE` → Skip this language, document why

See [applicability-analysis.md]({baseDir}/references/applicability-analysis.md) for detailed guidance.

### Phase 2: Test Creation (Test-First)

**Always write tests before the rule.**

Create test file with target language idioms:
- Minimum 2 vulnerable cases (`ruleid:`)
- Minimum 2 safe cases (`ok:`)
- Include language-specific edge cases

```go
// ruleid: sql-injection-golang
db.Query("SELECT * FROM users WHERE id = " + userInput)

// ok: sql-injection-golang
db.Query("SELECT * FROM users WHERE id = ?", userInput)
```

### Phase 3: Rule Creation

1. **Analyze AST**: `semgrep --dump-ast -l <lang> test-file`
2. **Translate patterns** to target language syntax
3. **Update metadata**: language key, message, rule ID
4. **Adapt for idioms**: Handle language-specific constructs

See [language-syntax-guide.md]({baseDir}/references/language-syntax-guide.md) for translation guidance.

### Phase 4: Validation

```bash
# Validate YAML
semgrep --validate --config rule.yaml

# Run tests
semgrep --test --config rule.yaml test-file
```

**Checkpoint**: Output MUST show `All tests passed`.

For taint rule debugging:
```bash
semgrep --dataflow-traces -f rule.yaml test-file
```

See [workflow.md]({baseDir}/references/workflow.md) for detailed workflow and troubleshooting.

## Quick Reference

| Task | Command |
|------|---------|
| Run tests | `semgrep --test --config rule.yaml test-file` |
| Validate YAML | `semgrep --validate --config rule.yaml` |
| Dump AST | `semgrep --dump-ast -l <lang> <file>` |
| Debug taint flow | `semgrep --dataflow-traces -f rule.yaml file` |


## Key Differences from Rule Creation

| Aspect | semgrep-rule-creator | This skill |
|--------|---------------------|------------|
| Input | Bug pattern description | Existing rule + target languages |
| Output | Single rule+test | Multiple rule+test directories |
| Workflow | Single creation cycle | Independent cycle per language |
| Phase 1 | Problem analysis | Applicability analysis per language |
| Library research | Always relevant | Optional (when original uses libraries) |

## Documentation

**REQUIRED**: Before porting rules, read relevant Semgrep documentation:

- [Rule Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax) - YAML structure and operators
- [Pattern Syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax) - Pattern matching and metavariables
- [Pattern Examples](https://semgrep.dev/docs/writing-rules/pattern-examples) - Per-language pattern references
- [Testing Rules](https://semgrep.dev/docs/writing-rules/testing-rules) - Testing annotations
- [Trail of Bits Testing Handbook](https://appsec.guide/docs/static-analysis/semgrep/advanced/) - Advanced patterns

## Next Steps

- For applicability analysis guidance, see [applicability-analysis.md]({baseDir}/references/applicability-analysis.md)
- For language translation guidance, see [language-syntax-guide.md]({baseDir}/references/language-syntax-guide.md)
- For detailed workflow and examples, see [workflow.md]({baseDir}/references/workflow.md)

---

## Reference: Applicability Analysis

# Applicability Analysis

Phase 1 of the variant creation workflow. Before porting a rule, analyze whether the vulnerability pattern applies to the target language.

## Analysis Process

For EACH target language, answer these questions:

### 1. Does the Vulnerability Class Exist?

**Determine if the vulnerability type is possible in the target language.**

Examples:
- Buffer overflow: Applies to C/C++, may apply to Rust (in unsafe blocks), does NOT apply to Python/Java
- SQL injection: Applies to any language with database access
- XSS: Applies to any language generating HTML output
- Memory leak: Relevant in C/C++, less relevant in garbage-collected languages
- Type confusion: Relevant in dynamically typed languages, less relevant in strongly typed

### 2. Does an Equivalent Construct Exist?

**Identify what the original rule detects and find equivalents.**

Parse the original rule to identify:
- **Sinks**: What dangerous functions/methods does it detect?
- **Sources**: Where does tainted data originate?
- **Pattern type**: Is it taint-mode or pattern-matching?

Then research the target language:
- What are the equivalent dangerous functions?
- What are the common source patterns?
- Are there language-specific idioms to consider?

### 3. Are the Semantics Similar Enough?

**Verify the pattern translates meaningfully.**

Consider:
- Does the vulnerability manifest the same way?
- Are there language-specific mitigations that change detection needs?
- Would the ported rule provide actual security value?

## Verdict Format

Document your analysis for each target language:

```
TARGET: <language>
VERDICT: APPLICABLE | APPLICABLE_WITH_ADAPTATION | NOT_APPLICABLE
REASONING: <specific analysis>
ADAPTATIONS_NEEDED: <if APPLICABLE_WITH_ADAPTATION>
EQUIVALENT_CONSTRUCTS:
  - Original: <function/pattern>
  - Target: <equivalent function/pattern>
```

## Verdict Definitions

### APPLICABLE

The pattern translates directly with minor syntax adjustments.

**Criteria:**
- Equivalent constructs exist with same semantics
- Vulnerability manifests identically
- Detection logic remains the same

**Example:**
```
Original: Python os.system(user_input)
Target: Go exec.Command(user_input)

VERDICT: APPLICABLE
REASONING: Both execute shell commands with user input. Vulnerability is
identical (command injection). Detection logic (taint from input to exec)
translates directly.
```

### APPLICABLE_WITH_ADAPTATION

The pattern can be ported but requires significant changes.

**Criteria:**
- Vulnerability class exists but manifests differently
- Equivalent constructs exist but with different APIs
- Additional patterns needed for target language idioms

**Example:**
```
Original: Python pickle.loads(untrusted)
Target: Java ObjectInputStream.readObject()

VERDICT: APPLICABLE_WITH_ADAPTATION
REASONING: Both detect deserialization vulnerabilities but the APIs differ
significantly. Java requires detection of ObjectInputStream creation and
readObject() calls, not a single function call.
ADAPTATIONS_NEEDED:
  - Different sink patterns (readObject vs loads)
  - May need pattern-inside for ObjectInputStream context
  - Consider readUnshared() variant
```

### NOT_APPLICABLE

The pattern should not be ported to this language.

**Criteria:**
- Vulnerability class doesn't exist in target language
- No equivalent construct exists
- Pattern would be meaningless or misleading

**Example:**
```
Original: C buffer overflow detection
Target: Python

VERDICT: NOT_APPLICABLE
REASONING: Python handles memory management automatically. Buffer overflows
in the traditional C sense don't exist. The vulnerability class is not
present in the target language.
```

## Common Applicability Patterns

### Always Translate (Language-Agnostic Vulnerabilities)

These vulnerability classes exist across most languages:
- SQL injection (any language with DB access)
- Command injection (any language with shell execution)
- Path traversal (any language with file operations)
- SSRF (any language with HTTP clients)
- XSS (any language generating HTML)

### Sometimes Translate (Context-Dependent)

These require careful analysis:
- Deserialization: Different mechanisms per language
- Cryptographic weaknesses: Language-specific crypto libraries
- Race conditions: Depends on concurrency model
- Integer overflow: Depends on type system

### Rarely Translate (Language-Specific)

These are often NOT_APPLICABLE for other languages:
- Memory corruption (C/C++ specific)
- Type juggling (PHP specific)
- Prototype pollution (JavaScript specific)
- GIL-related issues (Python specific)

## Library-Specific Rules

When the original rule targets a third-party library:

### Step 1: Identify the Library's Purpose

What functionality does the library provide?
- ORM / Database access
- HTTP client/server
- Serialization
- Templating
- etc.

### Step 2: Research Target Language Ecosystem

For the target language, identify:
- Standard library equivalents
- Popular third-party libraries with same functionality
- Language-specific idioms for this functionality

### Step 3: Decide on Scope

Options:
- **Native constructs only**: Port to standard library equivalents
- **Popular library**: Port to the most common library in target ecosystem
- **Multiple variants**: Create separate rules for multiple libraries

**Recommendation**: Start with standard library or most popular option. Additional library variants can be created separately if needed.

## Analysis Checklist

Before proceeding past Phase 1:

- [ ] Parsed original rule and identified pattern type
- [ ] Identified sinks, sources, and sanitizers (if taint mode)
- [ ] Researched equivalent constructs in target language
- [ ] Documented verdict with specific reasoning
- [ ] If APPLICABLE_WITH_ADAPTATION, listed required changes
- [ ] If NOT_APPLICABLE, documented clear explanation

## Example Analysis

**Original Rule**: Python command injection via subprocess

```yaml
rules:
  - id: python-command-injection
    mode: taint
    languages: [python]
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: subprocess.call($CMD, shell=True, ...)
```

**Target**: Go

```
TARGET: Go
VERDICT: APPLICABLE_WITH_ADAPTATION

REASONING:
- Command injection exists in Go (vulnerability class present)
- Go uses exec.Command() and exec.CommandContext() for command execution
- Go doesn't have shell=True equivalent; commands run directly by default
- Shell execution in Go requires explicit bash -c wrapping

EQUIVALENT_CONSTRUCTS:
  - Original sink: subprocess.call(cmd, shell=True)
  - Target sinks:
    - exec.Command("bash", "-c", cmd)
    - exec.Command("sh", "-c", cmd)
    - exec.Command(cmd) when cmd comes from user input

ADAPTATIONS_NEEDED:
1. Different sink patterns for Go's exec package
2. Source patterns need Go HTTP handler equivalents (r.URL.Query(), r.FormValue())
3. Consider both direct exec.Command and shell-wrapped variants
```

**Target**: Java

```
TARGET: Java
VERDICT: APPLICABLE

REASONING:
- Command injection exists in Java (vulnerability class present)
- Java uses Runtime.exec() and ProcessBuilder for command execution
- Direct equivalent functionality available

EQUIVALENT_CONSTRUCTS:
  - Original sink: subprocess.call(cmd, shell=True)
  - Target sinks:
    - Runtime.getRuntime().exec(cmd)
    - new ProcessBuilder(cmd).start()

ADAPTATIONS_NEEDED:
- Source patterns need Java servlet equivalents (request.getParameter())
- Consider both Runtime.exec and ProcessBuilder patterns
```

---

## Reference: Language Syntax Guide

# Language Syntax Translation Guide

Guidance for translating Semgrep patterns between languages. This is NOT a pre-built mapping—use these principles to research and adapt patterns for your specific case.

## General Translation Principles

### 1. Never Assume Syntax Equivalence

What looks similar may parse differently:

```python
# Python: method call on object
obj.method(arg)

# Go: might be method OR field access + function call
obj.Method(arg)      # Method call
obj.Field(arg)       # Field holding function, then called
```

**Always dump the AST** for your target language to see the actual structure.

### 2. Research Before Translating

For each construct in the original rule:
1. Search target language documentation for equivalent
2. Look for multiple ways the same thing can be written
3. Check if language idioms differ significantly

### 3. Preserve Detection Intent, Not Literal Syntax

The goal is detecting the same vulnerability, not matching identical syntax.

```yaml
# Original (Python) - detects eval of user input
pattern: eval($USER_INPUT)

# Go doesn't have eval() - what's the equivalent danger?
# Research shows: template execution, reflect-based eval, etc.
# Adapt to what actually creates the vulnerability in Go
```

## AST Analysis

### Always Dump the AST

```bash
semgrep --dump-ast -l <target-language> test-file
```

Compare how similar constructs are represented:

```python
# Python
cursor.execute(query)
```

```go
// Go
db.Query(query)
```

The AST structure may differ significantly even for conceptually similar operations.

### Key Differences to Watch

| Aspect | May Differ |
|--------|-----------|
| Method calls | Receiver position, syntax |
| Function arguments | Named vs positional, defaults |
| String handling | Interpolation, concatenation |
| Error handling | Exceptions vs return values |
| Imports | How namespaces work |

## Metavariable Adaptation

### Metavariables Work Cross-Language

Semgrep metavariables (`$X`, `$FUNC`, etc.) work in all languages:

```yaml
# Works in Python
pattern: $OBJ.execute($QUERY)

# Works in Java
pattern: $OBJ.executeQuery($QUERY)

# Works in Go
pattern: $DB.Query($QUERY, ...)
```

### Ellipsis Behavior

`...` matches language-appropriate constructs:
- In Python: matches arguments, statements
- In Go: matches arguments, statements (handles multi-return)
- In Java: matches arguments, statements, annotations

## Common Translation Categories

### Database Queries

**Research for your target language:**
- Standard library database package
- Popular ORM frameworks
- Raw query execution methods

Common patterns to look for:
- Query execution methods
- Prepared statement patterns
- String interpolation into queries

### Command Execution

**Research for your target language:**
- Standard library process/exec package
- Shell execution vs direct execution
- Argument passing (array vs string)

### File Operations

**Research for your target language:**
- File open/read/write APIs
- Path construction methods
- Directory traversal patterns

### HTTP Handling

**Research for your target language:**
- Request parameter access
- Header access
- Body parsing

## Researching Equivalents

### Step 1: Identify What the Original Detects

Parse the original rule:
- What function/method is the sink?
- What's the vulnerability being detected?
- What makes it dangerous?

### Step 2: Search Target Language Docs

Search for:
- `"<target language> <functionality>"` (e.g., "golang exec command")
- `"<target language> <vulnerability>"` (e.g., "java sql injection")
- Standard library documentation
- [Semgrep Pattern Examples](https://semgrep.dev/docs/writing-rules/pattern-examples) - Per-language pattern references

### Step 3: Find All Variants

A single Python function may have multiple equivalents:

```python
# Python has one main way
os.system(cmd)
```

```java
// Java has multiple
Runtime.getRuntime().exec(cmd);
new ProcessBuilder(cmd).start();
ProcessBuilder.command(cmd).start();
```

Include all common variants in your rule.

### Step 4: Check for Idioms

Languages have preferred patterns:

```python
# Python: often inline
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

```go
// Go: typically uses placeholders
db.Query("SELECT * FROM users WHERE id = ?", userID)
// Vulnerability is when they DON'T use placeholders
db.Query("SELECT * FROM users WHERE id = " + userID)
```

## Source Pattern Translation

### Web Framework Sources

Original rule sources need framework-specific translation:

```yaml
# Python Flask
pattern: request.args.get(...)

# Java Servlet
pattern: $REQUEST.getParameter(...)

# Go net/http
pattern: $R.URL.Query().Get(...)
pattern: $R.FormValue(...)

# Node.js Express
pattern: $REQ.query.$PARAM
pattern: $REQ.body.$PARAM
```

### User Input Sources

Research common input sources for target language, for example:
- HTTP request parameters
- Command line arguments
- Environment variables
- File reads
- Standard input

## Sanitizer Translation

### Research Sanitization Patterns

Each language has different sanitization approaches:

```python
# Python
shlex.quote(cmd)  # Shell escaping
html.escape(s)    # HTML escaping
```

```go
// Go
template.HTMLEscapeString(s)
// Prepared statements (implicit sanitization)
db.Query("SELECT ... WHERE id = ?", id)
```

```java
// Java
StringEscapeUtils.escapeHtml4(s)
PreparedStatement (implicit sanitization)
```

## Import/Namespace Considerations

### Pattern May Need Context

Some languages require matching imports:

```yaml
# Python - function in global namespace after import
pattern: pickle.loads(...)

# Java - may need full path or import context
pattern: java.io.ObjectInputStream
pattern: ObjectInputStream
```

### When to Use Full Paths

- When function name is common/ambiguous
- When you want to match specific library
- When namespace matters for security

## Testing Your Translation

### Verify with AST Dump

After writing test cases, verify patterns match:

```bash
# Dump AST of test file
semgrep --dump-ast -l <lang> test-file

# Compare with your pattern
# Adjust pattern to match AST structure
```

### Test Edge Cases

Each language has unique edge cases:
- Different string types (Go: string vs []byte)
- Different call syntaxes (method chaining)
- Different argument patterns

## Example: Translating SQL Injection Rule

**Original (Python):**
```yaml
pattern-sinks:
  - pattern: $CURSOR.execute($QUERY, ...)
```

**Research for Go:**
1. Standard database package: `database/sql`
2. Query methods: `Query`, `QueryRow`, `Exec`, `QueryContext`, etc.
3. ORM equivalents: GORM, sqlx, etc.

**Translated (Go - standard library):**
```yaml
pattern-sinks:
  - pattern: $DB.Query($QUERY, ...)
  - pattern: $DB.QueryRow($QUERY, ...)
  - pattern: $DB.Exec($QUERY, ...)
  - pattern: $DB.QueryContext($CTX, $QUERY, ...)
```

**Research for Java:**
1. JDBC: `Statement`, `PreparedStatement`
2. Query methods: `executeQuery`, `executeUpdate`, `execute`

**Translated (Java):**
```yaml
pattern-sinks:
  - pattern: (Statement $S).executeQuery($QUERY)
  - pattern: (Statement $S).executeUpdate($QUERY)
  - pattern: (Statement $S).execute($QUERY)
```

## Checklist Before Writing Rule

- [ ] Dumped AST for target language test file
- [ ] Researched equivalent functions/methods
- [ ] Identified all common variants
- [ ] Checked for language-specific idioms
- [ ] Identified appropriate source patterns
- [ ] Identified appropriate sanitizer patterns
- [ ] Verified patterns match AST structure

---

## Reference: Workflow

# Detailed Variant Creation Workflow

Complete step-by-step workflow for porting Semgrep rules to new languages.

## Core Principle: Independent Cycles

Each target language goes through the complete 4-phase cycle independently:

```
FOR EACH target language:
  ┌─────────────────────────────────────────────────────────┐
  │ Phase 1: Applicability Analysis                         │
  │   └─→ APPLICABLE? Continue                              │
  │   └─→ NOT_APPLICABLE? Skip to next language             │
  │                                                         │
  │ Phase 2: Test Creation (Test-First)                     │
  │   └─→ Create test file with ruleid/ok annotations       │
  │                                                         │
  │ Phase 3: Rule Creation                                  │
  │   └─→ Analyze AST, write rule, update metadata          │
  │                                                         │
  │ Phase 4: Validation                                     │
  │   └─→ Tests pass? Complete, proceed to next language    │
  │   └─→ Tests fail? Iterate phases 2-4                    │
  └─────────────────────────────────────────────────────────┘
```

**Do NOT batch**: Complete all phases for one language before starting the next.

## Phase 1: Applicability Analysis

### Step 1.1: Parse the Original Rule

Extract key components:

```yaml
# Example original rule
rules:
  - id: python-sql-injection
    mode: taint
    languages: [python]
    severity: ERROR
    message: SQL injection vulnerability
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: cursor.execute($QUERY, ...)
    pattern-sanitizers:
      - pattern: sanitize(...)
```

Document:
- **Rule ID**: python-sql-injection
- **Mode**: taint (optional, if taint mode used via `mode: taint`)
- **Sources**: request.args.get(...) (via `pattern-sources` - if taint analysis mode used)
- **Sinks**: cursor.execute($QUERY, ...) (via `pattern-sinks` - if taint analysis mode used)
- **Sanitizers**: sanitize(...) (via `pattern-sanitizers` - optional, if taint analysis used)

### Step 1.2: Analyze for Target Language

For each target language, determine applicability.

See [applicability-analysis.md]({baseDir}/references/applicability-analysis.md) for detailed guidance.

### Step 1.3: Document Verdict

```
TARGET: golang
VERDICT: APPLICABLE
REASONING: SQL injection applies to Go. database/sql package provides
Query/Exec functions that can be vulnerable to injection when string
concatenation is used instead of parameterized queries.
EQUIVALENT_CONSTRUCTS:
  - Source: request.args.get → r.URL.Query().Get(), r.FormValue()
  - Sink: cursor.execute → db.Query(), db.Exec()
```

If `NOT_APPLICABLE`, document why and proceed to next target language.

## Phase 2: Test Creation

### Step 2.1: Create Directory Structure

```bash
mkdir <original-rule-id>-<language>
```

Example:
```bash
mkdir python-sql-injection-golang
```

### Step 2.2: Write Test File

Create test file with target language extension:

```go
// python-sql-injection-golang.go
package main

import (
    "database/sql"
    "net/http"
)

// Vulnerable cases - MUST be flagged
func vulnerable1(db *sql.DB, r *http.Request) {
    userID := r.URL.Query().Get("id")
    // ruleid: python-sql-injection-golang
    db.Query("SELECT * FROM users WHERE id = " + userID)
}

func vulnerable2(db *sql.DB, r *http.Request) {
    name := r.FormValue("name")
    // ruleid: python-sql-injection-golang
    db.Exec("DELETE FROM users WHERE name = '" + name + "'")
}

// Safe cases - must NOT be flagged
func safeParameterized(db *sql.DB, r *http.Request) {
    userID := r.URL.Query().Get("id")
    // ok: python-sql-injection-golang
    db.Query("SELECT * FROM users WHERE id = ?", userID)
}

func safeHardcoded(db *sql.DB) {
    // ok: python-sql-injection-golang
    db.Query("SELECT * FROM users WHERE id = 1")
}
```

### Step 2.3: Test Case Requirements

**Minimum cases:**
- 2+ vulnerable cases (`ruleid:`)
- 2+ safe cases (`ok:`)

**Include variations:**
- Different sink functions (Query, Exec, QueryRow)
- Different source patterns (URL params, form values)
- Different string construction (concatenation, fmt.Sprintf)
- Safe patterns (parameterized queries, hardcoded values)

### Step 2.4: Annotation Placement

**CRITICAL**: The annotation comment must be on the line IMMEDIATELY BEFORE the code:

```go
// ruleid: my-rule
vulnerableCode()  // This line gets flagged

// ok: my-rule
safeCode()  // This line must NOT be flagged
```

## Phase 3: Rule Creation

### Step 3.1: Analyze AST

```bash
semgrep --dump-ast -l go python-sql-injection-golang.go
```

Study the AST structure for:
- How function calls are represented
- How string concatenation appears
- How method calls are structured

### Step 3.2: Write the Rule

Create rule file with adapted patterns:

```yaml
# python-sql-injection-golang.yaml
rules:
  - id: python-sql-injection-golang
    mode: taint
    languages: [go]
    severity: ERROR
    message: >-
      SQL injection vulnerability. User input from $SOURCE flows to
      database query without sanitization.
    metadata:
      original-rule: python-sql-injection
      ported-from: python
    pattern-sources:
      - patterns:
          - pattern: $R.URL.Query().Get(...)
      - patterns:
          - pattern: $R.FormValue(...)
    pattern-sinks:
      - patterns:
          - pattern: $DB.Query($QUERY, ...)
          - focus-metavariable: $QUERY
      - patterns:
          - pattern: $DB.Exec($QUERY, ...)
          - focus-metavariable: $QUERY
      - patterns:
          - pattern: $DB.QueryRow($QUERY, ...)
          - focus-metavariable: $QUERY
```

### Step 3.3: Update Metadata

For each ported rule:
- **id**: Append `-<language>` to original ID
- **languages**: Change to target language
- **message**: Adapt if needed for language context
- **metadata**: Add `original-rule` and `ported-from` fields

### Step 3.4: Adapt Pattern Syntax

See [language-syntax-guide.md]({baseDir}/references/language-syntax-guide.md) for translation guidance.

## Phase 4: Validation

### Step 4.1: Validate YAML

```bash
semgrep --validate --config python-sql-injection-golang.yaml
```

Fix any syntax errors before proceeding.

### Step 4.2: Run Tests

```bash
semgrep --test --config python-sql-injection-golang.yaml python-sql-injection-golang.go
```

### Step 4.3: Check Results

**Success:**
```
1/1: ✓ All tests passed
```

**Failure - missed lines:**
```
✗ python-sql-injection-golang
  missed lines: [15, 22]
```

Rule didn't match when it should. Check:
- Pattern too specific
- Missing pattern variant
- AST structure mismatch

**Failure - incorrect lines:**
```
✗ python-sql-injection-golang
  incorrect lines: [30, 35]
```

Rule matched when it shouldn't. Check:
- Pattern too broad
- Need pattern-not exclusion
- Sanitizer pattern missing

### Step 4.4: Debug Taint Rules

If using taint mode and having issues:

```bash
semgrep --dataflow-traces -f python-sql-injection-golang.yaml python-sql-injection-golang.go
```

Shows:
- Where taint originates
- How taint propagates
- Where taint reaches sinks
- Why taint might not flow (sanitizers, breaks in flow)

### Step 4.5: Iterate Until Pass

Repeat phases 2-4 as needed:
1. Add test cases to cover edge cases
2. Adjust patterns to match/exclude correctly
3. Re-run tests
4. Continue until "All tests passed"

## Phase 5: Proceed to Next Language

Only after all tests pass for one language:
1. Document completion
2. Move to next target language
3. Start fresh at Phase 1

## Output Structure

After completing all target languages:

```
python-sql-injection-golang/
├── python-sql-injection-golang.yaml
└── python-sql-injection-golang.go

python-sql-injection-java/
├── python-sql-injection-java.yaml
└── python-sql-injection-java.java

# If a language was NOT_APPLICABLE, no directory is created
# Document the reason in your response
```

## Troubleshooting

### Pattern Not Matching

1. **Dump AST**: `semgrep --dump-ast -l <lang> file`
2. **Compare structure**: Your pattern vs actual AST
3. **Check metavariables**: Correct binding?
4. **Try broader pattern**: Then narrow down

### Taint Not Propagating

1. **Use --dataflow-traces**: See where taint stops
2. **Check sanitizers**: Too broad?
3. **Verify sources**: Pattern actually matching?
4. **Check focus-metavariable**: On correct part of sink?

### Too Many False Positives

1. **Add pattern-not**: Exclude safe patterns
2. **Add sanitizers**: Validation functions
3. **Use pattern-inside**: Limit scope
4. **Check safe test cases**: Are they actually safe?

### YAML Syntax Errors

1. **Run --validate**: Get specific error
2. **Check indentation**: YAML is whitespace-sensitive
3. **Quote strings**: If they contain special characters
4. **Use multiline**: For complex patterns (`|` or `>-`)

## Example: Complete Workflow

### Original Rule

```yaml
# python-command-injection.yaml
rules:
  - id: python-command-injection
    mode: taint
    languages: [python]
    severity: ERROR
    message: Command injection vulnerability
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: os.system(...)
      - pattern: subprocess.call($CMD, shell=True, ...)
    pattern-sanitizers:
      - pattern: shlex.quote(...)
```

### Target Languages: Go and Java

---

### Go Variant

**Phase 1: Applicability**
```
TARGET: Go
VERDICT: APPLICABLE
REASONING: Command injection applies. Go's os/exec package can execute
commands. When user input is passed to exec.Command or wrapped in shell
execution, it's vulnerable.
```

**Phase 2: Test File** (`python-command-injection-golang.go`)
```go
package main

import (
    "net/http"
    "os/exec"
)

func vulnerable1(r *http.Request) {
    cmd := r.URL.Query().Get("cmd")
    // ruleid: python-command-injection-golang
    exec.Command("bash", "-c", cmd).Run()
}

func vulnerable2(r *http.Request) {
    input := r.FormValue("input")
    // ruleid: python-command-injection-golang
    exec.Command("sh", "-c", input).Run()
}

func safeNoShell(r *http.Request) {
    arg := r.URL.Query().Get("arg")
    // ok: python-command-injection-golang
    exec.Command("echo", arg).Run()
}

func safeHardcoded() {
    // ok: python-command-injection-golang
    exec.Command("ls", "-la").Run()
}
```

**Phase 3: Rule** (`python-command-injection-golang.yaml`)
```yaml
rules:
  - id: python-command-injection-golang
    mode: taint
    languages: [go]
    severity: ERROR
    message: Command injection via shell execution
    metadata:
      original-rule: python-command-injection
      ported-from: python
    pattern-sources:
      - pattern: $R.URL.Query().Get(...)
      - pattern: $R.FormValue(...)
    pattern-sinks:
      - patterns:
          - pattern: exec.Command("bash", "-c", $CMD, ...)
          - focus-metavariable: $CMD
      - patterns:
          - pattern: exec.Command("sh", "-c", $CMD, ...)
          - focus-metavariable: $CMD
```

**Phase 4: Validate**
```bash
semgrep --validate --config python-command-injection-golang.yaml
semgrep --test --config python-command-injection-golang.yaml python-command-injection-golang.go
# Output: ✓ All tests passed
```

---

### Java Variant

**Phase 1: Applicability**
```
TARGET: Java
VERDICT: APPLICABLE
REASONING: Command injection applies. Java's Runtime.exec() and
ProcessBuilder can execute commands. User input passed directly is vulnerable.
```

**Phase 2: Test File** (`python-command-injection-java.java`)
```java
import javax.servlet.http.*;
import java.io.*;

public class CommandTest {
    // ruleid: python-command-injection-java
    public void vulnerable1(HttpServletRequest request) throws Exception {
        String cmd = request.getParameter("cmd");
        Runtime.getRuntime().exec(cmd);
    }

    // ruleid: python-command-injection-java
    public void vulnerable2(HttpServletRequest request) throws Exception {
        String cmd = request.getParameter("cmd");
        new ProcessBuilder(cmd).start();
    }

    // ok: python-command-injection-java
    public void safeHardcoded() throws Exception {
        Runtime.getRuntime().exec("ls -la");
    }

    // ok: python-command-injection-java
    public void safeArray(HttpServletRequest request) throws Exception {
        String arg = request.getParameter("arg");
        Runtime.getRuntime().exec(new String[]{"echo", arg});
    }
}
```

**Phase 3: Rule** (`python-command-injection-java.yaml`)
```yaml
rules:
  - id: python-command-injection-java
    mode: taint
    languages: [java]
    severity: ERROR
    message: Command injection vulnerability
    metadata:
      original-rule: python-command-injection
      ported-from: python
    pattern-sources:
      - pattern: (HttpServletRequest $REQ).getParameter(...)
    pattern-sinks:
      - pattern: Runtime.getRuntime().exec($CMD)
        focus-metavariable: $CMD
      - patterns:
          - pattern: new ProcessBuilder($CMD, ...).start()
          - focus-metavariable: $CMD
```

**Phase 4: Validate**
```bash
semgrep --validate --config python-command-injection-java.yaml
semgrep --test --config python-command-injection-java.yaml python-command-injection-java.java
# Output: ✓ All tests passed
```

---

### Final Output

```
python-command-injection-golang/
├── python-command-injection-golang.yaml
└── python-command-injection-golang.go

python-command-injection-java/
├── python-command-injection-java.yaml
└── python-command-injection-java.java
```
