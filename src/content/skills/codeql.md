---
title: "Codeql"
description: "Scans a codebase for security vulnerabilities using CodeQL's interprocedural data flow and taint tracking analysis. Triggers on 'run codeql', 'codeql scan', 'codeql analysis', 'build codeql database', or 'find vulnerabilities with codeql'. Support..."
category: "research"
source: "community"
author: "Community"
tags: ["codeql"]
date: 2026-03-20
---

# CodeQL Analysis

Supported languages: Python, JavaScript/TypeScript, Go, Java/Kotlin, C/C++, C#, Ruby, Swift.

**Skill resources:** Reference files and templates are located at `{baseDir}/references/` and `{baseDir}/workflows/`.

## Essential Principles

1. **Database quality is non-negotiable.** A database that builds is not automatically good. Always run quality assessment (file counts, baseline LoC, extractor errors) and compare against expected source files. A cached build produces zero useful extraction.

2. **Data extensions catch what CodeQL misses.** Even projects using standard frameworks (Django, Spring, Express) have custom wrappers around database calls, request parsing, or shell execution. Skipping the create-data-extensions workflow means missing vulnerabilities in project-specific code paths.

3. **Explicit suite references prevent silent query dropping.** Never pass pack names directly to `codeql database analyze` — each pack's `defaultSuiteFile` applies hidden filters that can produce zero results. Always generate a custom `.qls` suite file.

4. **Zero findings needs investigation, not celebration.** Zero results can indicate poor database quality, missing models, wrong query packs, or silent suite filtering. Investigate before reporting clean.

5. **macOS Apple Silicon requires workarounds for compiled languages.** Exit code 137 is `arm64e`/`arm64` mismatch, not a build failure. Try Homebrew arm64 tools or Rosetta before falling back to `build-mode=none`.

6. **Follow workflows step by step.** Once a workflow is selected, execute it step by step without skipping phases. Each phase gates the next — skipping quality assessment or data extensions leads to incomplete analysis.

## Output Directory

All generated files (database, build logs, diagnostics, extensions, results) are stored in a single output directory.

- **If the user specifies an output directory** in their prompt, use it as `OUTPUT_DIR`.
- **If not specified**, default to `./static_analysis_codeql_1`. If that already exists, increment to `_2`, `_3`, etc.

In both cases, **always create the directory** with `mkdir -p` before writing any files.

```bash
# Resolve output directory
if [ -n "$USER_SPECIFIED_DIR" ]; then
  OUTPUT_DIR="$USER_SPECIFIED_DIR"
else
  BASE="static_analysis_codeql"
  N=1
  while [ -e "${BASE}_${N}" ]; do
    N=$((N + 1))
  done
  OUTPUT_DIR="${BASE}_${N}"
fi
mkdir -p "$OUTPUT_DIR"
```

The output directory is resolved **once** at the start before any workflow executes. All workflows receive `$OUTPUT_DIR` and store their artifacts there:

```
$OUTPUT_DIR/
├── rulesets.txt                 # Selected query packs (logged after Step 3)
├── codeql.db/                   # CodeQL database (dir containing codeql-database.yml)
├── build.log                    # Build log
├── codeql-config.yml            # Exclusion config (interpreted languages)
├── diagnostics/                 # Diagnostic queries and CSVs
├── extensions/                  # Data extension YAMLs
├── raw/                         # Unfiltered analysis output
│   ├── results.sarif
│   └── <mode>.qls
└── results/                     # Final results (filtered for important-only, copied for run-all)
    └── results.sarif
```

### Database Discovery

A CodeQL database is identified by the presence of a `codeql-database.yml` marker file inside its directory. When searching for existing databases, **always collect all matches** — there may be multiple databases from previous runs or for different languages.

**Discovery command:**

```bash
# Find ALL CodeQL databases (top-level and one subdirectory deep)
find . -maxdepth 3 -name "codeql-database.yml" -not -path "*/\.*" 2>/dev/null \
  | while read -r yml; do dirname "$yml"; done
```

- **Inside `$OUTPUT_DIR`:** `find "$OUTPUT_DIR" -maxdepth 2 -name "codeql-database.yml"`
- **Project-wide (for auto-detection):** `find . -maxdepth 3 -name "codeql-database.yml"` — covers databases at the project top level (`./db-name/`) and one subdirectory deep (`./subdir/db-name/`). Does not search deeper.

Never assume a database is named `codeql.db` — discover it by its marker file.

**When multiple databases are found:**

For each discovered database, collect metadata to help the user choose:

```bash
# For each database, extract language and creation time
for db in $FOUND_DBS; do
  CODEQL_LANG=$(codeql resolve database --format=json -- "$db" 2>/dev/null | jq -r '.languages[0]')
  CREATED=$(grep '^creationMetadata:' -A5 "$db/codeql-database.yml" 2>/dev/null | grep 'creationTime' | awk '{print $2}')
  echo "$db — language: $CODEQL_LANG, created: $CREATED"
done
```

Then use `AskUserQuestion` to let the user select which database to use, or to build a new one. **Skip `AskUserQuestion` if the user explicitly stated which database to use or to build a new one in their prompt.**

## Quick Start

For the common case ("scan this codebase for vulnerabilities"):

```bash
# 1. Verify CodeQL is installed
if ! command -v codeql >/dev/null 2>&1; then
  echo "NOT INSTALLED: codeql binary not found on PATH"
else
  codeql --version || echo "ERROR: codeql found but --version failed (check installation)"
fi

# 2. Resolve output directory
BASE="static_analysis_codeql"; N=1
while [ -e "${BASE}_${N}" ]; do N=$((N + 1)); done
OUTPUT_DIR="${BASE}_${N}"; mkdir -p "$OUTPUT_DIR"
```

Then execute the full pipeline: **build database → create data extensions → run analysis** using the workflows below.

## When to Use

- Scanning a codebase for security vulnerabilities with deep data flow analysis
- Building a CodeQL database from source code (with build capability for compiled languages)
- Finding complex vulnerabilities that require interprocedural taint tracking or AST/CFG analysis
- Performing comprehensive security audits with multiple query packs

## When NOT to Use

- **Writing custom queries** - Use a dedicated query development skill
- **CI/CD integration** - Use GitHub Actions documentation directly
- **Quick pattern searches** - Use Semgrep or grep for speed
- **No build capability** for compiled languages - Consider Semgrep instead
- **Single-file or lightweight analysis** - Semgrep is faster for simple pattern matching

## Rationalizations to Reject

These shortcuts lead to missed findings. Do not accept them:

- **"security-extended is enough"** - It is the baseline. Always check if Trail of Bits packs and Community Packs are available for the language. They catch categories `security-extended` misses entirely.
- **"The database built, so it's good"** - A database that builds does not mean it extracted well. Always run quality assessment and check file counts against expected source files.
- **"Data extensions aren't needed for standard frameworks"** - Even Django/Spring apps have custom wrappers that CodeQL does not model. Skipping extensions means missing vulnerabilities.
- **"build-mode=none is fine for compiled languages"** - It produces severely incomplete analysis. Only use as an absolute last resort. On macOS, try the arm64 toolchain workaround or Rosetta first.
- **"The build fails on macOS, just use build-mode=none"** - Exit code 137 is caused by `arm64e`/`arm64` mismatch, not a fundamental build failure. See [macos-arm64e-workaround.md](references/macos-arm64e-workaround.md).
- **"No findings means the code is secure"** - Zero findings can indicate poor database quality, missing models, or wrong query packs. Investigate before reporting clean results.
- **"I'll just run the default suite"** / **"I'll just pass the pack names directly"** - Each pack's `defaultSuiteFile` applies hidden filters and can produce zero results. Always use an explicit suite reference.
- **"I'll put files in the current directory"** - All generated files must go in `$OUTPUT_DIR`. Scattering files in the working directory makes cleanup impossible and risks overwriting previous runs.
- **"Just use the first database I find"** - Multiple databases may exist for different languages or from previous runs. When more than one is found, present all options to the user. Only skip the prompt when the user already specified which database to use.
- **"The user said 'scan', that means they want me to pick a database"** - "Scan" is not database selection. If multiple databases exist and the user didn't name one, ask.

---

## Workflow Selection

This skill has three workflows. **Once a workflow is selected, execute it step by step without skipping phases.**

| Workflow | Purpose |
|----------|---------|
| [build-database](workflows/build-database.md) | Create CodeQL database using build methods in sequence |
| [create-data-extensions](workflows/create-data-extensions.md) | Detect or generate data extension models for project APIs |
| [run-analysis](workflows/run-analysis.md) | Select rulesets, execute queries, process results |

### Auto-Detection Logic

**If user explicitly specifies** what to do (e.g., "build a database", "run analysis on ./my-db"), execute that workflow directly. **Do NOT call `AskUserQuestion` for database selection if the user's prompt already makes their intent clear** — e.g., "build a new database", "analyze the codeql database in static_analysis_codeql_2", "run a full scan from scratch".

**Default pipeline for "test", "scan", "analyze", or similar:** Discover existing databases first, then decide.

```bash
# Find ALL CodeQL databases by looking for codeql-database.yml marker file
# Search top-level dirs and one subdirectory deep
FOUND_DBS=()
while IFS= read -r yml; do
  db_dir=$(dirname "$yml")
  codeql resolve database -- "$db_dir" >/dev/null 2>&1 && FOUND_DBS+=("$db_dir")
done < <(find . -maxdepth 3 -name "codeql-database.yml" -not -path "*/\.*" 2>/dev/null)

echo "Found ${#FOUND_DBS[@]} existing database(s)"
```

| Condition | Action |
|-----------|--------|
| No databases found | Resolve new `$OUTPUT_DIR`, execute build → extensions → analysis (full pipeline) |
| One database found | Use `AskUserQuestion`: reuse it or build new? |
| Multiple databases found | Use `AskUserQuestion`: list all with metadata, let user pick one or build new |
| User explicitly stated intent | Skip `AskUserQuestion`, act on their instructions directly |

### Database Selection Prompt

When existing databases are found **and the user did not explicitly specify which to use**, present via `AskUserQuestion`:

```
header: "Existing CodeQL Databases"
question: "I found existing CodeQL database(s). What would you like to do?"
options:
  - label: "<db_path_1> (language: python, created: 2026-02-24)"
    description: "Reuse this database"
  - label: "<db_path_2> (language: cpp, created: 2026-02-23)"
    description: "Reuse this database"
  - label: "Build a new database"
    description: "Create a fresh database in a new output directory"
```

After selection:
- **If user picks an existing database:** Set `$OUTPUT_DIR` to its parent directory (or the directory containing it), set `$DB_NAME` to the selected path, then proceed to extensions → analysis.
- **If user picks "Build new":** Resolve a new `$OUTPUT_DIR`, execute build → extensions → analysis.

### General Decision Prompt

If the user's intent is ambiguous (neither database selection nor workflow is clear), ask:

```
I can help with CodeQL analysis. What would you like to do?

1. **Full scan (Recommended)** - Build database, create extensions, then run analysis
2. **Build database** - Create a new CodeQL database from this codebase
3. **Create data extensions** - Generate custom source/sink models for project APIs
4. **Run analysis** - Run security queries on existing database

[If databases found: "I found N existing database(s): <list paths with language>"]
[Show output directory: "Output will be stored in <OUTPUT_DIR>"]
```

---

## Reference Index

| File | Content |
|------|---------|
| **Workflows** | |
| [workflows/build-database.md](workflows/build-database.md) | Database creation with build method sequence |
| [workflows/create-data-extensions.md](workflows/create-data-extensions.md) | Data extension generation pipeline |
| [workflows/run-analysis.md](workflows/run-analysis.md) | Query execution and result processing |
| **References** | |
| [references/macos-arm64e-workaround.md](references/macos-arm64e-workaround.md) | Apple Silicon build tracing workarounds |
| [references/build-fixes.md](references/build-fixes.md) | Build failure fix catalog |
| [references/quality-assessment.md](references/quality-assessment.md) | Database quality metrics and improvements |
| [references/extension-yaml-format.md](references/extension-yaml-format.md) | Data extension YAML column definitions and examples |
| [references/sarif-processing.md](references/sarif-processing.md) | jq commands for SARIF output processing |
| [references/diagnostic-query-templates.md](references/diagnostic-query-templates.md) | QL queries for source/sink enumeration |
| [references/important-only-suite.md](references/important-only-suite.md) | Important-only suite template and generation |
| [references/run-all-suite.md](references/run-all-suite.md) | Run-all suite template |
| [references/ruleset-catalog.md](references/ruleset-catalog.md) | Available query packs by language |
| [references/threat-models.md](references/threat-models.md) | Threat model configuration |
| [references/language-details.md](references/language-details.md) | Language-specific build and extraction details |
| [references/performance-tuning.md](references/performance-tuning.md) | Memory, threading, and timeout configuration |

---

## Success Criteria

A complete CodeQL analysis run should satisfy:

- [ ] Output directory resolved (user-specified or auto-incremented default)
- [ ] All generated files stored inside `$OUTPUT_DIR`
- [ ] Database built (discovered via `codeql-database.yml` marker) with quality assessment passed (baseline LoC > 0, errors < 5%)
- [ ] Data extensions evaluated — either created in `$OUTPUT_DIR/extensions/` or explicitly skipped with justification
- [ ] Analysis run with explicit suite reference (not default pack suite)
- [ ] All installed query packs (official + Trail of Bits + Community) used or explicitly excluded
- [ ] Selected query packs logged to `$OUTPUT_DIR/rulesets.txt`
- [ ] Unfiltered results preserved in `$OUTPUT_DIR/raw/results.sarif`
- [ ] Final results in `$OUTPUT_DIR/results/results.sarif` (filtered for important-only, copied for run-all)
- [ ] Zero-finding results investigated (database quality, model coverage, suite selection)
- [ ] Build log preserved at `$OUTPUT_DIR/build.log` with all commands, fixes, and quality assessments

---

## Reference: Build Fixes

# Build Fixes

Fixes to apply when a CodeQL database build method fails. Try these in order, then retry the current build method. **Log each fix attempt.**

## 1. Clean existing state

```bash
log_step "Applying fix: clean existing state"
rm -rf "$DB_NAME"
log_result "Removed $DB_NAME"
```

## 2. Clean build cache

```bash
log_step "Applying fix: clean build cache"
CLEANED=""
make clean 2>/dev/null && CLEANED="$CLEANED make"
rm -rf build CMakeCache.txt CMakeFiles 2>/dev/null && CLEANED="$CLEANED cmake-artifacts"
./gradlew clean 2>/dev/null && CLEANED="$CLEANED gradle"
mvn clean 2>/dev/null && CLEANED="$CLEANED maven"
cargo clean 2>/dev/null && CLEANED="$CLEANED cargo"
log_result "Cleaned: $CLEANED"
```

## 3. Install missing dependencies

> **Note:** The commands below install the *target project's* dependencies so CodeQL can trace the build. Use whatever package manager the target project expects (`pip`, `npm`, `go mod`, etc.) — these are not the skill's own tooling preferences.

```bash
log_step "Applying fix: install dependencies"

# Python — use target project's package manager (pip/uv/poetry)
if [ -f requirements.txt ]; then
  log_cmd "pip install -r requirements.txt"
  pip install -r requirements.txt 2>&1 | tee -a "$LOG_FILE"
fi
if [ -f setup.py ] || [ -f pyproject.toml ]; then
  log_cmd "pip install -e ."
  pip install -e . 2>&1 | tee -a "$LOG_FILE"
fi

# Node - log installed packages
if [ -f package.json ]; then
  log_cmd "npm install"
  npm install 2>&1 | tee -a "$LOG_FILE"
fi

# Go
if [ -f go.mod ]; then
  log_cmd "go mod download"
  go mod download 2>&1 | tee -a "$LOG_FILE"
fi

# Java - log downloaded dependencies
if [ -f build.gradle ] || [ -f build.gradle.kts ]; then
  log_cmd "./gradlew dependencies --refresh-dependencies"
  ./gradlew dependencies --refresh-dependencies 2>&1 | tee -a "$LOG_FILE"
fi
if [ -f pom.xml ]; then
  log_cmd "mvn dependency:resolve"
  mvn dependency:resolve 2>&1 | tee -a "$LOG_FILE"
fi

# Rust
if [ -f Cargo.toml ]; then
  log_cmd "cargo fetch"
  cargo fetch 2>&1 | tee -a "$LOG_FILE"
fi

log_result "Dependencies installed - see above for details"
```

## 4. Handle private registries

If dependencies require authentication, ask user:
```
AskUserQuestion: "Build requires private registry access. Options:"
  1. "I'll configure auth and retry"
  2. "Skip these dependencies"
  3. "Show me what's needed"
```

```bash
# Log authentication setup if performed
log_step "Private registry authentication configured"
log_result "Registry: <REGISTRY_URL>, Method: <AUTH_METHOD>"
```

**After fixes:** Retry current build method. If still fails, move to next method.

---

## Reference: Diagnostic Query Templates

# Diagnostic Query Templates

Language-specific QL queries for enumerating sources and sinks recognized by CodeQL. Used during the data extensions creation process.

## Source Enumeration Query

All languages use the class `RemoteFlowSource`. The import differs per language.

### Import Reference

| Language | Imports | Class |
|----------|---------|-------|
| Python | `import python` + `import semmle.python.dataflow.new.RemoteFlowSources` | `RemoteFlowSource` |
| JavaScript | `import javascript` | `RemoteFlowSource` |
| Java | `import java` + `import semmle.code.java.dataflow.FlowSources` | `RemoteFlowSource` |
| Go | `import go` | `RemoteFlowSource` |
| C/C++ | `import cpp` + `import semmle.code.cpp.security.FlowSources` | `RemoteFlowSource` |
| C# | `import csharp` + `import semmle.code.csharp.security.dataflow.flowsources.Remote` | `RemoteFlowSource` |
| Ruby | `import ruby` + `import codeql.ruby.dataflow.RemoteFlowSources` | `RemoteFlowSource` |

### Template (Python — swap imports per table above)

```ql
/**
 * @name List recognized dataflow sources
 * @description Enumerates all locations CodeQL recognizes as dataflow sources
 * @kind problem
 * @id custom/list-sources
 */
import python
import semmle.python.dataflow.new.RemoteFlowSources

from RemoteFlowSource src
select src,
  src.getSourceType()
    + " | " + src.getLocation().getFile().getRelativePath()
    + ":" + src.getLocation().getStartLine().toString()
```

**Note:** `getSourceType()` is available on Python, Java, and C#. For Go, JavaScript, Ruby, and C++ replace the select with:
```ql
select src,
  src.getLocation().getFile().getRelativePath()
    + ":" + src.getLocation().getStartLine().toString()
```

---

## Sink Enumeration Queries

The Concepts API differs significantly across languages. Use the correct template.

### Concept Class Reference

| Concept | Python | JavaScript | Go | Ruby |
|---------|--------|------------|-----|------|
| SQL | `SqlExecution.getSql()` | `DatabaseAccess.getAQueryArgument()` | `SQL::QueryString` (is-a Node) | `SqlExecution.getSql()` |
| Command exec | `SystemCommandExecution.getCommand()` | `SystemCommandExecution.getACommandArgument()` | `SystemCommandExecution.getCommandName()` | `SystemCommandExecution.getAnArgument()` |
| File access | `FileSystemAccess.getAPathArgument()` | `FileSystemAccess.getAPathArgument()` | `FileSystemAccess.getAPathArgument()` | `FileSystemAccess.getAPathArgument()` |
| HTTP client | `Http::Client::Request.getAUrlPart()` | — | — | — |
| Decoding | `Decoding.getAnInput()` | — | — | — |
| XML parsing | — | — | — | `XmlParserCall.getAnInput()` |

### Python

```ql
/**
 * @name List recognized dataflow sinks
 * @description Enumerates security-relevant sinks CodeQL recognizes
 * @kind problem
 * @id custom/list-sinks
 */
import python
import semmle.python.Concepts

from DataFlow::Node sink, string kind
where
  exists(SqlExecution e | sink = e.getSql() and kind = "sql-execution")
  or
  exists(SystemCommandExecution e |
    sink = e.getCommand() and kind = "command-execution"
  )
  or
  exists(FileSystemAccess e |
    sink = e.getAPathArgument() and kind = "file-access"
  )
  or
  exists(Http::Client::Request r |
    sink = r.getAUrlPart() and kind = "http-request"
  )
  or
  exists(Decoding d | sink = d.getAnInput() and kind = "decoding")
  or
  exists(CodeExecution e | sink = e.getCode() and kind = "code-execution")
select sink,
  kind
    + " | " + sink.getLocation().getFile().getRelativePath()
    + ":" + sink.getLocation().getStartLine().toString()
```

### JavaScript / TypeScript

```ql
/**
 * @name List recognized dataflow sinks
 * @description Enumerates security-relevant sinks CodeQL recognizes
 * @kind problem
 * @id custom/list-sinks-js
 */
import javascript

from DataFlow::Node sink, string kind
where
  exists(DatabaseAccess e |
    sink = e.getAQueryArgument() and kind = "database-access"
  )
  or
  exists(SystemCommandExecution e |
    sink = e.getACommandArgument() and kind = "command-execution"
  )
  or
  exists(FileSystemAccess e |
    sink = e.getAPathArgument() and kind = "file-access"
  )
select sink,
  kind
    + " | " + sink.getLocation().getFile().getRelativePath()
    + ":" + sink.getLocation().getStartLine().toString()
```

### Go

```ql
/**
 * @name List recognized dataflow sinks
 * @description Enumerates security-relevant sinks CodeQL recognizes
 * @kind problem
 * @id custom/list-sinks-go
 */
import go
import semmle.go.frameworks.SQL

from DataFlow::Node sink, string kind
where
  sink instanceof SQL::QueryString and kind = "sql-query"
  or
  exists(SystemCommandExecution e |
    sink = e.getCommandName() and kind = "command-execution"
  )
  or
  exists(FileSystemAccess e |
    sink = e.getAPathArgument() and kind = "file-access"
  )
select sink,
  kind
    + " | " + sink.getLocation().getFile().getRelativePath()
    + ":" + sink.getLocation().getStartLine().toString()
```

### Ruby

```ql
/**
 * @name List recognized dataflow sinks
 * @description Enumerates security-relevant sinks CodeQL recognizes
 * @kind problem
 * @id custom/list-sinks-ruby
 */
import ruby
import codeql.ruby.Concepts

from DataFlow::Node sink, string kind
where
  exists(SqlExecution e | sink = e.getSql() and kind = "sql-execution")
  or
  exists(SystemCommandExecution e |
    sink = e.getAnArgument() and kind = "command-execution"
  )
  or
  exists(FileSystemAccess e |
    sink = e.getAPathArgument() and kind = "file-access"
  )
  or
  exists(CodeExecution e | sink = e.getCode() and kind = "code-execution")
select sink,
  kind
    + " | " + sink.getLocation().getFile().getRelativePath()
    + ":" + sink.getLocation().getStartLine().toString()
```

### Java

Java lacks a unified Concepts module. Use language-specific sink classes. The diagnostics query needs its own `qlpack.yml` with a `codeql/java-all` dependency — create it alongside the `.ql` files:

```yaml
# $DIAG_DIR/qlpack.yml
name: custom/diagnostics
version: 0.0.1
dependencies:
  codeql/java-all: "*"
```

Then run `codeql pack install` in the diagnostics directory before executing queries.

```ql
/**
 * @name List recognized dataflow sinks
 * @description Enumerates security-relevant sinks CodeQL recognizes
 * @kind problem
 * @id custom/list-sinks
 */
import java
import semmle.code.java.dataflow.DataFlow
import semmle.code.java.security.QueryInjection
import semmle.code.java.security.CommandLineQuery
import semmle.code.java.security.TaintedPathQuery
import semmle.code.java.security.XSS
import semmle.code.java.security.RequestForgery
import semmle.code.java.security.Xxe

from DataFlow::Node sink, string kind
where
  sink instanceof QueryInjectionSink and kind = "sql-injection"
  or
  sink instanceof CommandInjectionSink and kind = "command-injection"
  or
  sink instanceof TaintedPathSink and kind = "path-injection"
  or
  sink instanceof XssSink and kind = "xss"
  or
  sink instanceof RequestForgerySink and kind = "ssrf"
  or
  sink instanceof XxeSink and kind = "xxe"
select sink,
  kind
    + " | " + sink.getLocation().getFile().getRelativePath()
    + ":" + sink.getLocation().getStartLine().toString()
```

### C / C++

C++ uses a similar per-vulnerability-class pattern. Requires a `qlpack.yml` with `codeql/cpp-all` dependency (same approach as Java):

```yaml
# $DIAG_DIR/qlpack.yml
name: custom/diagnostics
version: 0.0.1
dependencies:
  codeql/cpp-all: "*"
```

Then run `codeql pack install` in the diagnostics directory before executing queries.

```ql
/**
 * @name List recognized dataflow sinks
 * @description Enumerates security-relevant sinks CodeQL recognizes
 * @kind problem
 * @id custom/list-sinks-cpp
 */
import cpp
import semmle.code.cpp.dataflow.DataFlow
import semmle.code.cpp.security.CommandExecution
import semmle.code.cpp.security.FileAccess
import semmle.code.cpp.security.BufferWrite

from DataFlow::Node sink, string kind
where
  exists(FunctionCall call |
    sink.asExpr() = call.getAnArgument() and
    call.getTarget().hasGlobalOrStdName("system") and
    kind = "command-injection"
  )
  or
  exists(FunctionCall call |
    sink.asExpr() = call.getAnArgument() and
    call.getTarget().hasGlobalOrStdName(["fopen", "open", "freopen"]) and
    kind = "file-access"
  )
  or
  exists(FunctionCall call |
    sink.asExpr() = call.getAnArgument() and
    call.getTarget().hasGlobalOrStdName(["sprintf", "strcpy", "strcat", "gets"]) and
    kind = "buffer-write"
  )
  or
  exists(FunctionCall call |
    sink.asExpr() = call.getAnArgument() and
    call.getTarget().hasGlobalOrStdName(["execl", "execle", "execlp", "execv", "execvp", "execvpe", "popen"]) and
    kind = "command-execution"
  )
select sink,
  kind
    + " | " + sink.getLocation().getFile().getRelativePath()
    + ":" + sink.getLocation().getStartLine().toString()
```

### C\#

C# uses per-vulnerability sink classes. Requires a `qlpack.yml` with `codeql/csharp-all` dependency:

```yaml
# $DIAG_DIR/qlpack.yml
name: custom/diagnostics
version: 0.0.1
dependencies:
  codeql/csharp-all: "*"
```

Then run `codeql pack install` in the diagnostics directory before executing queries.

```ql
/**
 * @name List recognized dataflow sinks
 * @description Enumerates security-relevant sinks CodeQL recognizes
 * @kind problem
 * @id custom/list-sinks-csharp
 */
import csharp
import semmle.code.csharp.dataflow.DataFlow
import semmle.code.csharp.security.dataflow.SqlInjectionQuery
import semmle.code.csharp.security.dataflow.CommandInjectionQuery
import semmle.code.csharp.security.dataflow.TaintedPathQuery
import semmle.code.csharp.security.dataflow.XSSQuery

from DataFlow::Node sink, string kind
where
  sink instanceof SqlInjection::Sink and kind = "sql-injection"
  or
  sink instanceof CommandInjection::Sink and kind = "command-injection"
  or
  sink instanceof TaintedPath::Sink and kind = "path-injection"
  or
  sink instanceof XSS::Sink and kind = "xss"
select sink,
  kind
    + " | " + sink.getLocation().getFile().getRelativePath()
    + ":" + sink.getLocation().getStartLine().toString()
```

---

## Reference: Extension Yaml Format

# Data Extension YAML Format

YAML format for CodeQL data extension files. Used by the create-data-extensions workflow to model project-specific sources, sinks, and flow summaries.

## Structure

All extension files follow this structure:

```yaml
extensions:
  - addsTo:
      pack: codeql/<language>-all  # Target library pack
      extensible: <model-type>      # sourceModel, sinkModel, summaryModel, neutralModel
    data:
      - [<columns>]
```

## Source Models

Columns: `[package, type, subtypes, name, signature, ext, output, kind, provenance]`

| Column | Description | Example |
|--------|-------------|---------|
| package | Module/package path | `myapp.auth` |
| type | Class or module name | `AuthManager` |
| subtypes | Include subclasses | `True` (Java: capitalized) / `true` (Python/JS/Go) |
| name | Method name | `get_token` |
| signature | Method signature (optional) | `""` (Python/JS), `"(String,int)"` (Java) |
| ext | Extension (optional) | `""` |
| output | What is tainted | `ReturnValue`, `Parameter[0]` (Java) / `Argument[0]` (Python/JS/Go) |
| kind | Source category | `remote`, `local`, `file`, `environment`, `database` |
| provenance | How model was created | `manual` |

**Java-specific format differences:**
- **subtypes**: Use `True` / `False` (capitalized, Python-style), not `true` / `false`
- **output for parameters**: Use `Parameter[N]` (not `Argument[N]`) to mark method parameters as sources
- **signature**: Required for disambiguation — use Java type syntax: `"(String)"`, `"(String,int)"`
- **Parameter ranges**: Use `Parameter[0..2]` to mark multiple consecutive parameters

Example (Python):

```yaml
# $OUTPUT_DIR/extensions/sources.yml
extensions:
  - addsTo:
      pack: codeql/python-all
      extensible: sourceModel
    data:
      - ["myapp.http", "Request", true, "get_param", "", "", "ReturnValue", "remote", "manual"]
      - ["myapp.http", "Request", true, "get_header", "", "", "ReturnValue", "remote", "manual"]
```

Example (Java — note `True`, `Parameter[N]`, and signature):

```yaml
# $OUTPUT_DIR/extensions/sources.yml
extensions:
  - addsTo:
      pack: codeql/java-all
      extensible: sourceModel
    data:
      - ["com.myapp.controller", "ApiController", True, "search", "(String)", "", "Parameter[0]", "remote", "manual"]
      - ["com.myapp.service", "FileService", True, "upload", "(String,String)", "", "Parameter[0..1]", "remote", "manual"]
```

## Sink Models

Columns: `[package, type, subtypes, name, signature, ext, input, kind, provenance]`

Note: column 7 is `input` (which argument receives tainted data), not `output`.

| Kind | Vulnerability |
|------|---------------|
| `sql-injection` | SQL injection |
| `command-injection` | Command injection |
| `path-injection` | Path traversal |
| `xss` | Cross-site scripting |
| `code-injection` | Code injection |
| `ssrf` | Server-side request forgery |
| `unsafe-deserialization` | Insecure deserialization |

Example (Python):

```yaml
# $OUTPUT_DIR/extensions/sinks.yml
extensions:
  - addsTo:
      pack: codeql/python-all
      extensible: sinkModel
    data:
      - ["myapp.db", "Connection", true, "raw_query", "", "", "Argument[0]", "sql-injection", "manual"]
      - ["myapp.shell", "Runner", false, "execute", "", "", "Argument[0]", "command-injection", "manual"]
```

Example (Java — note `True` and `Argument[N]` for sink input):

```yaml
extensions:
  - addsTo:
      pack: codeql/java-all
      extensible: sinkModel
    data:
      - ["com.myapp.db", "QueryRunner", True, "execute", "(String)", "", "Argument[0]", "sql-injection", "manual"]
```

## Summary Models

Columns: `[package, type, subtypes, name, signature, ext, input, output, kind, provenance]`

| Kind | Description |
|------|-------------|
| `taint` | Data flows through, still tainted |
| `value` | Data flows through, exact value preserved |

Example:

```yaml
# $OUTPUT_DIR/extensions/summaries.yml
extensions:
  # Pass-through: taint propagates
  - addsTo:
      pack: codeql/python-all
      extensible: summaryModel
    data:
      - ["myapp.cache", "Cache", true, "get", "", "", "Argument[0]", "ReturnValue", "taint", "manual"]
      - ["myapp.utils", "JSON", false, "parse", "", "", "Argument[0]", "ReturnValue", "taint", "manual"]

```

## Neutral Models

Columns: `[package, type, name, signature, kind, provenance]` (6 columns, NOT the 10-column `summaryModel` format).

Use `neutralModel` to explicitly block taint propagation through known-safe functions.

Example:

```yaml
  - addsTo:
      pack: codeql/python-all
      extensible: neutralModel
    data:
      - ["myapp.security", "Sanitizer", "escape_html", "", "summary", "manual"]
```

**`neutralModel` vs no model:** If a function has no model at all, CodeQL may still infer flow through it. Use `neutralModel` to explicitly block taint propagation through known-safe functions.

## Language-Specific Notes

**Python:** Use dotted module paths for `package` (e.g., `myapp.db`).

**JavaScript:** `package` is often `""` for project-local code. Use the import path for npm packages.

**Go:** Use full import paths (e.g., `myapp/internal/db`). `type` is often `""` for package-level functions.

**Java:** Use fully qualified package names (e.g., `com.myapp.db`).

**C/C++:** Use `""` for package, put the namespace in `type`.

## Deploying Extensions

**Known limitation:** `--additional-packs` and `--model-packs` flags do not work with pre-compiled query packs (bundled CodeQL distributions that cache `java-all` inside `.codeql/libraries/`). Extensions placed in a standalone model pack directory will be resolved by `codeql resolve qlpacks` but silently ignored during `codeql database analyze`.

**Workaround — copy extensions into the library pack's `ext/` directory:**

> **Warning:** Files copied into the `ext/` directory live inside CodeQL's managed pack cache. They will be **lost** when packs are updated via `codeql pack download` or version upgrades. After any pack update, re-run this deployment step to restore the extensions.

```bash
# Find the java-all ext directory used by the query pack
JAVA_ALL_EXT=$(find "$(codeql resolve qlpacks 2>/dev/null | grep 'java-queries' | awk '{print $NF}' | tr -d '()')" \
  -path '*/.codeql/libraries/codeql/java-all/*/ext' -type d 2>/dev/null | head -1)

if [ -n "$JAVA_ALL_EXT" ]; then
  PROJECT_NAME=$(basename "$(pwd)")
  cp "$OUTPUT_DIR/extensions/sources.yml" "$JAVA_ALL_EXT/${PROJECT_NAME}.sources.model.yml"
  [ -f "$OUTPUT_DIR/extensions/sinks.yml" ] && cp "$OUTPUT_DIR/extensions/sinks.yml" "$JAVA_ALL_EXT/${PROJECT_NAME}.sinks.model.yml"
  [ -f "$OUTPUT_DIR/extensions/summaries.yml" ] && cp "$OUTPUT_DIR/extensions/summaries.yml" "$JAVA_ALL_EXT/${PROJECT_NAME}.summaries.model.yml"

  # Verify deployment — confirm files landed correctly
  DEPLOYED=$(ls "$JAVA_ALL_EXT/${PROJECT_NAME}".*.model.yml 2>/dev/null | wc -l)
  if [ "$DEPLOYED" -gt 0 ]; then
    echo "Extensions deployed to $JAVA_ALL_EXT ($DEPLOYED files):"
    ls -la "$JAVA_ALL_EXT/${PROJECT_NAME}".*.model.yml
  else
    echo "ERROR: Files were copied but verification failed. Check path: $JAVA_ALL_EXT"
  fi
else
  echo "WARNING: Could not find java-all ext directory. Extensions may not load."
  echo "Attempted path lookup from: codeql resolve qlpacks | grep java-queries"
  echo "Run 'codeql resolve qlpacks' manually to debug."
fi
```

**For Python/JS/Go:** The same limitation may apply. Locate the `<lang>-all` pack's `ext/` directory and copy extensions there.

**Alternative (if query packs are NOT pre-compiled):** Use `--additional-packs=./codeql-extensions` with a proper model pack `qlpack.yml`:

```yaml
# $OUTPUT_DIR/extensions/qlpack.yml
name: custom/<project>-extensions
version: 0.0.1
library: true
extensionTargets:
  codeql/<lang>-all: "*"
dataExtensions:
  - sources.yml
  - sinks.yml
  - summaries.yml
```

---

## Reference: Important Only Suite

# Important-Only Query Suite

In important-only mode, generate a custom `.qls` query suite file at runtime. This applies the same precision/severity filtering to **all** packs (official + third-party).

## Why a Custom Suite

The built-in `security-extended` suite only applies to the official `codeql/<lang>-queries` pack. Third-party packs (Trail of Bits, Community Packs) run unfiltered when passed directly to `codeql database analyze`. A custom `.qls` suite loads queries from all packs and applies a single set of `include`/`exclude` filters uniformly.

## Metadata Criteria

Two-phase filtering: the **suite** selects candidate queries (broad), then a **post-analysis jq filter** removes low-severity medium-precision results from the SARIF output.

### Phase 1: Suite selection (which queries run)

Queries are included if they match **any** of these blocks (OR logic across blocks, AND logic within):

| Block | kind | precision | problem.severity | tags |
|-------|------|-----------|-----------------|------|
| 1 | `problem`, `path-problem` | `high`, `very-high` | *(any)* | must contain `security` |
| 2 | `problem`, `path-problem` | `medium` | *(any)* | must contain `security` |

### Phase 2: Post-analysis filter (which results are reported)

After `codeql database analyze` completes, filter the SARIF output:

| precision | security-severity | Action |
|-----------|-------------------|--------|
| high / very-high | *(any)* | **Keep** |
| medium | >= 6.0 | **Keep** |
| medium | < 6.0 or missing | **Drop** |

This ensures medium-precision queries with meaningful security impact (e.g., `cpp/path-injection` at 7.5, `cpp/world-writable-file-creation` at 7.8) are included, while noisy low-severity medium-precision findings are filtered out.

Excluded: deprecated queries, model editor/generator queries. Experimental queries are **included**.

**Key difference from `security-extended`:** The `security-extended` suite includes medium-precision queries at any severity. Important-only mode adds a security-severity threshold to reduce noise from medium-precision queries that flag low-impact issues.

## Suite Template

Generate this file as `important-only.qls` in the results directory before running analysis:

```yaml
- description: Important-only — security vulnerabilities, medium-high confidence
# Official queries
- queries: .
  from: codeql/<CODEQL_LANG>-queries
# Third-party packs (include only if installed, one entry per pack)
# - queries: .
#   from: trailofbits/<CODEQL_LANG>-queries
# - queries: .
#   from: GitHubSecurityLab/CodeQL-Community-Packs-<CODEQL_LANG>
# Filtering: security only, high/very-high precision (any severity),
# medium precision (any severity — low-severity filtered post-analysis by security-severity score).
# Experimental queries included.
- include:
    kind:
      - problem
      - path-problem
    precision:
      - high
      - very-high
    tags contain:
      - security
- include:
    kind:
      - problem
      - path-problem
    precision:
      - medium
    tags contain:
      - security
- exclude:
    deprecated: //
- exclude:
    tags contain:
      - modeleditor
      - modelgenerator
```

> **Post-analysis step required:** After running the analysis, apply the post-analysis jq filter (defined in the run-analysis workflow Step 5) to remove medium-precision results with `security-severity` < 6.0.

## Generation Script

The agent should generate the suite file dynamically based on installed packs:

```bash
RAW_DIR="$OUTPUT_DIR/raw"
SUITE_FILE="$RAW_DIR/important-only.qls"

# NOTE: CODEQL_LANG must be set before running this script (e.g., CODEQL_LANG=cpp)
# NOTE: INSTALLED_THIRD_PARTY_PACKS must be a space-separated list of pack names

# Use a heredoc WITHOUT quotes so ${CODEQL_LANG} expands
cat > "$SUITE_FILE" << HEADER
- description: Important-only — security vulnerabilities, medium-high confidence
- queries: .
  from: codeql/${CODEQL_LANG}-queries
HEADER

# Add each installed third-party pack
for PACK in $INSTALLED_THIRD_PARTY_PACKS; do
  cat >> "$SUITE_FILE" << PACK_ENTRY
- queries: .
  from: ${PACK}
PACK_ENTRY
done

# Append the filtering rules (quoted heredoc — no variable expansion needed)
cat >> "$SUITE_FILE" << 'FILTERS'
- include:
    kind:
      - problem
      - path-problem
    precision:
      - high
      - very-high
    tags contain:
      - security
- include:
    kind:
      - problem
      - path-problem
    precision:
      - medium
    tags contain:
      - security
- exclude:
    deprecated: //
- exclude:
    tags contain:
      - modeleditor
      - modelgenerator
FILTERS

# Verify the suite resolves correctly
: "${CODEQL_LANG:?ERROR: CODEQL_LANG must be set before generating suite}"
: "${SUITE_FILE:?ERROR: SUITE_FILE must be set}"

if ! codeql resolve queries "$SUITE_FILE" | head -20; then
  echo "ERROR: Suite file failed to resolve. Check CODEQL_LANG=$CODEQL_LANG and installed packs."
fi
echo "Suite generated: $SUITE_FILE"
```

## How Filtering Works on Third-Party Queries

CodeQL query suite filters match on query metadata (`@precision`, `@problem.severity`, `@tags`). Third-party queries that:

- **Have proper metadata**: Filtered normally (kept if they match the include criteria)
- **Lack `@precision`**: Excluded by `include` blocks (they require precision to match). This is correct — if a query doesn't declare its precision, we cannot assess its confidence.
- **Lack `@tags security`**: Excluded. Non-security queries are not relevant to important-only mode.

This is a stricter-than-necessary filter for third-party packs, but it ensures only well-annotated security queries run in important-only mode. The post-analysis jq filter then further narrows medium-precision results to those with `security-severity` >= 6.0.

---

## Reference: Language Details

# Language-Specific Guidance

## No Build Required

### Python

```bash
codeql database create codeql.db --language=python --source-root=.
```

**Framework Support:**
- Django, Flask, FastAPI: Built-in models
- Tornado, Pyramid: Partial support
- Custom frameworks: May need data extensions

**Common Issues:**
| Issue | Fix |
|-------|-----|
| Missing Django models | Ensure `settings.py` is at expected location |
| Virtual env included | Use `paths-ignore` in config |
| Type stubs missing | Install `types-*` packages before extraction |

### JavaScript/TypeScript

```bash
codeql database create codeql.db --language=javascript --source-root=.
```

**Framework Support:**
- React, Vue, Angular: Built-in models
- Express, Koa, Fastify: HTTP source/sink models
- Next.js, Nuxt: Partial SSR support

**Common Issues:**
| Issue | Fix |
|-------|-----|
| node_modules bloat | Already excluded by default |
| TypeScript not parsed | Ensure `tsconfig.json` is valid |
| Monorepo issues | Use `--source-root` for specific package |

### Go

```bash
codeql database create codeql.db --language=go --source-root=.
```

**Framework Support:**
- net/http, Gin, Echo, Chi: Built-in models
- gRPC: Partial support
- Custom routers: May need data extensions

**Common Issues:**
| Issue | Fix |
|-------|-----|
| Missing dependencies | Run `go mod download` first |
| Vendor directory | CodeQL handles automatically |
| CGO code | Requires `--command='go build'` with CGO enabled |

### Ruby

```bash
codeql database create codeql.db --language=ruby --source-root=.
```

**Framework Support:**
- Rails: Full support (controllers, models, views)
- Sinatra: Built-in support
- Hanami: Partial support

**Common Issues:**
| Issue | Fix |
|-------|-----|
| Bundler issues | Run `bundle install` first |
| Rails engines | May need multiple database passes |

## Build Required

### C/C++

```bash
# Make
codeql database create codeql.db --language=cpp --command='make -j8'

# CMake
codeql database create codeql.db --language=cpp \
  --source-root=/path/to/src \
  --command='cmake --build build'

# Ninja
codeql database create codeql.db --language=cpp \
  --command='ninja -C build'
```

**Build System Tips:**
| Build System | Command |
|--------------|---------|
| Make | `make clean && make -j$(nproc)` |
| CMake | `cmake -B build && cmake --build build` |
| Meson | `meson setup build && ninja -C build` |
| Bazel | `bazel build //...` |

**Common Issues:**
| Issue | Fix |
|-------|-----|
| Partial extraction | Ensure `make clean` before CodeQL build |
| Header-only libraries | Use `--extractor-option cpp_trap_headers=true` |
| Cross-compilation | Set `CODEQL_EXTRACTOR_CPP_TARGET_ARCH` |

### Java/Kotlin

```bash
# Gradle
codeql database create codeql.db --language=java --command='./gradlew build -x test'

# Maven
codeql database create codeql.db --language=java --command='mvn compile -DskipTests'
```

**Framework Support:**
- Spring Boot: Full support
- Jakarta EE: Built-in models
- Android: Requires Android SDK

**Common Issues:**
| Issue | Fix |
|-------|-----|
| Missing dependencies | Run `./gradlew dependencies` first |
| Kotlin mixed projects | Use `--language=java` (covers both) |
| Annotation processors | Ensure they run during CodeQL build |

### Rust

```bash
codeql database create codeql.db --language=rust --command='cargo build'
```

**Common Issues:**
| Issue | Fix |
|-------|-----|
| Proc macros | May require special handling |
| Workspace projects | Use `--source-root` for specific crate |
| Build script failures | Ensure native dependencies are available |

### C#

```bash
# .NET Core
codeql database create codeql.db --language=csharp --command='dotnet build'

# MSBuild
codeql database create codeql.db --language=csharp --command='msbuild /t:rebuild'
```

**Framework Support:**
- ASP.NET Core: Full support
- Entity Framework: Database query models
- Blazor: Partial support

**Common Issues:**
| Issue | Fix |
|-------|-----|
| NuGet restore | Run `dotnet restore` first |
| Multiple solutions | Specify solution file in command |

### Swift

```bash
# Xcode project
codeql database create codeql.db --language=swift \
  --command='xcodebuild -project MyApp.xcodeproj -scheme MyApp build'

# Swift Package Manager
codeql database create codeql.db --language=swift --command='swift build'
```

**Requirements:**
- macOS only
- Xcode Command Line Tools

**Common Issues:**
| Issue | Fix |
|-------|-----|
| Code signing | Add `CODE_SIGN_IDENTITY=- CODE_SIGNING_REQUIRED=NO` |
| Simulator target | Add `-sdk iphonesimulator` |

## Extractor Options

Set via environment variables: `CODEQL_EXTRACTOR_<LANG>_OPTION_<NAME>=<VALUE>`

### C/C++ Options

| Option | Description |
|--------|-------------|
| `trap_headers=true` | Include header file analysis |
| `target_arch=x86_64` | Target architecture |

### Java Options

| Option | Description |
|--------|-------------|
| `jdk_version=17` | JDK version for analysis |

### Python Options

| Option | Description |
|--------|-------------|
| `python_executable=/path/to/python` | Specific Python interpreter |

---

## Reference: Macos Arm64E Workaround

# macOS arm64e Workaround

Methods for building CodeQL databases on macOS Apple Silicon when the `arm64e`/`arm64` architecture mismatch causes SIGKILL (exit code 137) during build tracing.

**Use when `IS_MACOS_ARM64E=true`** (detected in build-database workflow Step 2a). These replace Methods 1 and 2 on affected systems.

The strategy is to use Homebrew-installed tools (plain `arm64`, not `arm64e`) so `libtrace.dylib` can be injected successfully. Try sub-methods in order:

## Sub-method 2m-a: Homebrew clang/gcc with multi-step tracing

Trace only the compiler invocations individually, avoiding system tools (`/usr/bin/ar`, `/bin/mkdir`) that would be killed. This requires a multi-step build: init → trace each compiler call → finalize.

```bash
log_step "METHOD 2m-a: macOS arm64 — Homebrew compiler with multi-step tracing"

# 1. Find Homebrew C/C++ compiler (arm64, not arm64e)
BREW_CC=""
# Prefer Homebrew clang
if [ -x "/opt/homebrew/opt/llvm/bin/clang" ]; then
  BREW_CC="/opt/homebrew/opt/llvm/bin/clang"
# Try Homebrew GCC (e.g. gcc-14, gcc-13)
elif command -v gcc-14 >/dev/null 2>&1; then
  BREW_CC="$(command -v gcc-14)"
elif command -v gcc-13 >/dev/null 2>&1; then
  BREW_CC="$(command -v gcc-13)"
fi

if [ -z "$BREW_CC" ]; then
  log_result "No Homebrew C/C++ compiler found — skipping 2m-a"
  # Fall through to 2m-b
else
  # Verify it's arm64 (not arm64e)
  BREW_CC_ARCH=$(lipo -archs "$BREW_CC" 2>/dev/null)
  if [[ "$BREW_CC_ARCH" == *"arm64e"* ]]; then
    log_result "Homebrew compiler is arm64e — skipping 2m-a"
  else
    log_step "Using Homebrew compiler: $BREW_CC (arch: $BREW_CC_ARCH)"

    # 2. Run the build normally (without tracing) to create build dirs and artifacts
    #    Use Homebrew make (gmake) if available, otherwise system make outside tracer
    if command -v gmake >/dev/null 2>&1; then
      MAKE_CMD="gmake"
    else
      MAKE_CMD="make"
    fi
    $MAKE_CMD clean 2>/dev/null || true
    $MAKE_CMD CC="$BREW_CC" 2>&1 | tee -a "$LOG_FILE"

    # 3. Extract compiler commands from the Makefile / build system
    #    Use make's dry-run mode to get the exact compiler invocations
    $MAKE_CMD clean 2>/dev/null || true
    COMPILE_CMDS=$($MAKE_CMD CC="$BREW_CC" --dry-run 2>/dev/null \
      | grep -E "^\s*$BREW_CC\b.*\s-c\s" \
      | sed 's/^[[:space:]]*//')

    if [ -z "$COMPILE_CMDS" ]; then
      log_result "Could not extract compile commands from dry-run — skipping 2m-a"
    else
      # 4. Init database
      codeql database init $DB_NAME --language=cpp --source-root=. --overwrite 2>&1 \
        | tee -a "$LOG_FILE"

      # 5. Ensure build directories exist (outside tracer — avoids arm64e mkdir)
      $MAKE_CMD clean 2>/dev/null || true
      #    Parse -o flags to find output dirs, or just create common dirs
      echo "$COMPILE_CMDS" | sed -n 's/.*-o[[:space:]]\{1,\}\([^[:space:]]\{1,\}\).*/\1/p' | xargs -I{} dirname {} \
        | sort -u | xargs mkdir -p 2>/dev/null || true

      # 6. Trace each compiler invocation individually
      TRACE_OK=true
      while IFS= read -r cmd; do
        [ -z "$cmd" ] && continue
        log_cmd "codeql database trace-command $DB_NAME -- $cmd"
        if ! codeql database trace-command $DB_NAME -- $cmd 2>&1 | tee -a "$LOG_FILE"; then
          log_result "FAILED on: $cmd"
          TRACE_OK=false
          break
        fi
      done <<< "$COMPILE_CMDS"

      if $TRACE_OK; then
        # 7. Finalize
        codeql database finalize $DB_NAME 2>&1 | tee -a "$LOG_FILE"
        if codeql resolve database -- "$DB_NAME" >/dev/null 2>&1; then
          log_result "SUCCESS (macOS arm64 multi-step)"
          # Done — skip to Step 4
        else
          log_result "FAILED (finalize failed)"
        fi
      fi
    fi
  fi
fi
```

## Sub-method 2m-b: Rosetta x86_64 emulation

Force the entire CodeQL pipeline to run under Rosetta, which uses the `x86_64` slice of both `libtrace.dylib` and system tools — no `arm64e` mismatch.

```bash
log_step "METHOD 2m-b: macOS arm64 — Rosetta x86_64 emulation"

# Check if Rosetta is available
if ! arch -x86_64 /usr/bin/true 2>/dev/null; then
  log_result "Rosetta not available — skipping 2m-b"
else
  BUILD_CMD="<BUILD_CMD>"  # e.g. "make clean && make -j4"
  CMD="arch -x86_64 codeql database create $DB_NAME --language=$CODEQL_LANG --source-root=. --command='$BUILD_CMD' --overwrite"
  log_cmd "$CMD"

  arch -x86_64 codeql database create $DB_NAME --language=$CODEQL_LANG --source-root=. \
    --command="$BUILD_CMD" --overwrite 2>&1 | tee -a "$LOG_FILE"

  if codeql resolve database -- "$DB_NAME" >/dev/null 2>&1; then
    log_result "SUCCESS (Rosetta x86_64)"
  else
    log_result "FAILED (Rosetta)"
  fi
fi
```

## Sub-method 2m-c: System compiler (direct attempt)

As a verification step, try the standard autobuild with the system compiler. This will likely fail with exit code 137 on affected systems, but confirms the arm64e issue is the cause.

> **This sub-method is optional.** Skip it if arm64e incompatibility was already confirmed in Step 2a.

```bash
log_step "METHOD 2m-c: System compiler (expected to fail on arm64e)"
CMD="codeql database create $DB_NAME --language=$CODEQL_LANG --source-root=. --overwrite"
log_cmd "$CMD"

$CMD 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=$?
if [ $EXIT_CODE -eq 137 ] || [ $EXIT_CODE -eq 134 ]; then
  log_result "FAILED: exit code $EXIT_CODE confirms arm64e/libtrace incompatibility"
elif codeql resolve database -- "$DB_NAME" >/dev/null 2>&1; then
  log_result "SUCCESS (unexpected — system compiler worked)"
else
  log_result "FAILED (exit code: $EXIT_CODE)"
fi
```

## Sub-method 2m-d: Ask user

If all macOS workarounds fail, present options:

```
AskUserQuestion:
  header: "macOS Build"
  question: "Build tracing failed due to macOS arm64e incompatibility. How to proceed?"
  multiSelect: false
  options:
    - label: "Use build-mode=none (Recommended)"
      description: "Source-level analysis only. Misses some interprocedural data flow but catches most C/C++ vulnerabilities (format strings, buffer overflows, unsafe functions)."
    - label: "Install arm64 tools and retry"
      description: "Run: brew install llvm make — then retry with Homebrew toolchain"
    - label: "Install Rosetta and retry"
      description: "Run: softwareupdate --install-rosetta — then retry under x86_64 emulation"
    - label: "Abort"
      description: "Stop database creation"
```

**If "Use build-mode=none":** Proceed to Method 4.

**If "Install arm64 tools and retry":**
```bash
log_step "Installing Homebrew arm64 toolchain"
brew install llvm make 2>&1 | tee -a "$LOG_FILE"
# Retry Sub-method 2m-a
```

**If "Install Rosetta and retry":**
```bash
log_step "Installing Rosetta"
softwareupdate --install-rosetta --agree-to-license 2>&1 | tee -a "$LOG_FILE"
# Retry Sub-method 2m-b
```

---

## Reference: Performance Tuning

# Performance Tuning

## Memory Configuration

### CODEQL_RAM Environment Variable

Control maximum heap memory (in MB):

```bash
# 48GB for large codebases
CODEQL_RAM=48000 codeql database analyze codeql.db ...

# 16GB for medium codebases
CODEQL_RAM=16000 codeql database analyze codeql.db ...
```

**Guidelines:**
| Codebase Size | Recommended RAM |
|---------------|-----------------|
| Small (<100K LOC) | 4-8 GB |
| Medium (100K-1M LOC) | 8-16 GB |
| Large (1M+ LOC) | 32-64 GB |

## Thread Configuration

### Analysis Threads

```bash
# Use all available cores
codeql database analyze codeql.db --threads=0 ...

# Use specific number
codeql database analyze codeql.db --threads=8 ...
```

**Note:** `--threads=0` uses all available cores. For shared machines, use explicit count.

## Query-Level Timeouts

Prevent individual queries from running indefinitely:

```bash
# Set per-query timeout (in milliseconds)
codeql database analyze codeql.db --timeout=600000 ...
```

A 10-minute timeout (`600000`) catches runaway queries without killing legitimate complex analysis. Taint-tracking queries on large codebases may need longer.

## Evaluator Diagnostics

When analysis is slow, use `--evaluator-log` to identify which queries consume the most time:

```bash
codeql database analyze codeql.db \
  --evaluator-log=evaluator.log \
  --format=sarif-latest \
  --output=results.sarif \
  -- codeql/python-queries:codeql-suites/python-security-extended.qls

# Summarize the log
codeql generate log-summary evaluator.log --format=text
```

The summary shows per-query timing and tuple counts. Queries producing millions of tuples are likely the bottleneck.

## Disk Space

| Phase | Typical Size | Notes |
|-------|-------------|-------|
| Database creation | 2-10x source size | Compiled languages are larger due to build tracing |
| Analysis cache | 1-5 GB | Stored in database directory |
| SARIF output | 1-50 MB | Depends on finding count |

Check available space before starting:

```bash
df -h .
du -sh codeql_*.db 2>/dev/null
```

## Caching Behavior

CodeQL caches query evaluation results inside the database directory. Subsequent runs of the same queries skip re-evaluation.

| Scenario | Cache Effect |
|----------|-------------|
| Re-run same packs | Fast — uses cached results |
| Add new query pack | Only new queries evaluate |
| `codeql database cleanup` | Clears cache — forces full re-evaluation |
| `--rerun` flag | Ignores cache for this run |

**When to clear cache:**
- After deploying new data extensions (cache may hold stale results)
- When investigating unexpected zero-finding results
- Before benchmark comparisons (ensures consistent timing)

```bash
# Clear evaluation cache
codeql database cleanup codeql_1.db
```

## Troubleshooting Performance

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| OOM during analysis | Not enough RAM | Increase `CODEQL_RAM` |
| Slow database creation | Complex build | Use `--threads`, simplify build |
| Slow query execution | Large codebase | Reduce query scope, add RAM |
| Database too large | Too many files | Use exclusion config (`codeql-config.yml` with `paths-ignore`) |
| Single query hangs | Runaway evaluation | Use `--timeout` and check `--evaluator-log` |
| Repeated runs still slow | Cache not used | Check you're using same database path |

---

## Reference: Quality Assessment

# Quality Assessment

How to assess and improve CodeQL database quality after a successful build.

## Collect Metrics

```bash
log_step "Assessing database quality"

# 1. Baseline lines of code and file list (most reliable metric)
codeql database print-baseline -- "$DB_NAME"
BASELINE_LOC=$(python3 -c "
import json
with open('$DB_NAME/baseline-info.json') as f:
    d = json.load(f)
for lang, info in d['languages'].items():
    print(f'{lang}: {info[\"linesOfCode\"]} LoC, {len(info[\"files\"])} files')
")
echo "$BASELINE_LOC"
log_result "Baseline: $BASELINE_LOC"

# 2. Source archive file count
SRC_FILE_COUNT=$(unzip -Z1 "$DB_NAME/src.zip" 2>/dev/null | wc -l)
echo "Files in source archive: $SRC_FILE_COUNT"

# 3. Extraction errors from extractor diagnostics
EXTRACTOR_ERRORS=$(find "$DB_NAME/diagnostic/extractors" -name '*.jsonl' \
  -exec cat {} + 2>/dev/null | grep -c '^{' 2>/dev/null || true)
EXTRACTOR_ERRORS=${EXTRACTOR_ERRORS:-0}
echo "Extractor errors: $EXTRACTOR_ERRORS"

# 4. Export diagnostics summary (experimental but useful)
DIAG_TEXT=$(codeql database export-diagnostics --format=text -- "$DB_NAME" 2>/dev/null || true)
if [ -n "$DIAG_TEXT" ]; then
  echo "Diagnostics: $DIAG_TEXT"
fi

# 5. Check database is finalized
FINALIZED=$(grep '^finalised:' "$DB_NAME/codeql-database.yml" 2>/dev/null \
  | awk '{print $2}')
echo "Finalized: $FINALIZED"
```

## Compare Against Expected Source

Estimate the expected source file count from the working directory and compare.

> **Compiled languages (C/C++, Java, C#):** The source archive (`src.zip`) includes system headers and SDK files alongside project source files. For C/C++, this can inflate the archive count 10-20x (e.g., 111 archive files for 5 project source files). Compare against **project-relative files only** by filtering the archive listing.

```bash
# Count source files in the project (adjust extensions per language)
EXPECTED=$(fd -t f -e c -e cpp -e h -e hpp -e java -e kt -e py -e js -e ts \
  --exclude 'codeql_*.db' --exclude node_modules --exclude vendor --exclude .git . \
  2>/dev/null | wc -l)
echo "Expected source files: $EXPECTED"

# Count PROJECT files in source archive (exclude system/SDK paths)
PROJECT_SRC_COUNT=$(unzip -Z1 "$DB_NAME/src.zip" 2>/dev/null \
  | grep -v -E '^(Library/|usr/|System/|opt/|Applications/)' | wc -l)
echo "Project files in source archive: $PROJECT_SRC_COUNT"
echo "Total files in source archive: $SRC_FILE_COUNT (includes system headers for compiled langs)"

# Baseline LOC from database metadata (most reliable single metric)
DB_LOC=$(grep '^baselineLinesOfCode:' "$DB_NAME/codeql-database.yml" \
  | awk '{print $2}')
echo "Baseline LoC: $DB_LOC"

# Error ratio — use project file count for compiled langs, total for interpreted
if [ "$PROJECT_SRC_COUNT" -gt 0 ]; then
  ERROR_RATIO=$(python3 -c "print(f'{$EXTRACTOR_ERRORS/$PROJECT_SRC_COUNT*100:.1f}%')")
else
  ERROR_RATIO="N/A (no files)"
fi
echo "Error ratio: $ERROR_RATIO ($EXTRACTOR_ERRORS errors / $PROJECT_SRC_COUNT project files)"
```

## Log Assessment

```bash
log_step "Quality assessment results"
log_result "Baseline LoC: $DB_LOC"
log_result "Project source files: $PROJECT_SRC_COUNT (expected: ~$EXPECTED)"
log_result "Total archive files: $SRC_FILE_COUNT (includes system headers for compiled langs)"
log_result "Extractor errors: $EXTRACTOR_ERRORS (ratio: $ERROR_RATIO)"
log_result "Finalized: $FINALIZED"

# Sample extracted project files (exclude system paths)
unzip -Z1 "$DB_NAME/src.zip" 2>/dev/null \
  | grep -v -E '^(Library/|usr/|System/|opt/|Applications/)' \
  | head -20 >> "$LOG_FILE"
```

## Quality Criteria

| Metric | Source | Good | Poor |
|--------|--------|------|------|
| Baseline LoC | `print-baseline` / `baseline-info.json` | > 0, proportional to project size | 0 or far below expected |
| Project source files | `src.zip` (filtered) | Close to expected source file count | 0 or < 50% of expected |
| Extractor errors | `diagnostic/extractors/*.jsonl` | 0 or < 5% of project files | > 5% of project files |
| Finalized | `codeql-database.yml` | `true` | `false` (incomplete build) |
| Key directories | `src.zip` listing | Application code directories present | Missing `src/main`, `lib/`, `app/` etc. |
| "No source code seen" | build log | Absent | Present (cached build — compiled languages) |

**Interpreting archive file counts for compiled languages:** C/C++ databases include system headers (e.g., `<stdio.h>`, SDK headers) in `src.zip`. A project with 5 source files may have 100+ files in the archive. Always filter to project-relative paths when comparing against expected counts. Use `baselineLinesOfCode` as the primary quality indicator.

**Interpreting baseline LoC:** A small number of extractor errors is normal and does not significantly impact analysis. However, if `baselineLinesOfCode` is 0 or the source archive contains no files, the database is empty — likely a cached build (compiled languages) or wrong `--source-root`.

---

## Improve Quality (if poor)

Try these improvements, re-assess after each. **Log all improvements:**

### 1. Adjust source root

```bash
log_step "Quality improvement: adjust source root"
NEW_ROOT="./src"  # or detected subdirectory
# For interpreted: add --codescanning-config=codeql-config.yml
# For compiled: omit config flag
log_cmd "codeql database create $DB_NAME --language=$CODEQL_LANG --source-root=$NEW_ROOT --overwrite"
codeql database create $DB_NAME --language=$CODEQL_LANG --source-root=$NEW_ROOT --overwrite
log_result "Changed source-root to: $NEW_ROOT"
```

### 2. Fix "no source code seen" (cached build - compiled languages only)

```bash
log_step "Quality improvement: force rebuild (cached build detected)"
log_cmd "make clean && rebuild"
make clean && codeql database create $DB_NAME --language=$CODEQL_LANG --overwrite
log_result "Forced clean rebuild"
```

### 3. Install type stubs / dependencies

> **Note:** These install into the *target project's* environment to improve CodeQL extraction quality.

```bash
log_step "Quality improvement: install type stubs/additional deps"

# Python type stubs — install into target project's environment
STUBS_INSTALLED=""
for stub in types-requests types-PyYAML types-redis; do
  if pip install "$stub" 2>/dev/null; then
    STUBS_INSTALLED="$STUBS_INSTALLED $stub"
  fi
done
log_result "Installed type stubs:$STUBS_INSTALLED"

# Additional project dependencies
log_cmd "pip install -e ."
pip install -e . 2>&1 | tee -a "$LOG_FILE"
```

### 4. Adjust extractor options

```bash
log_step "Quality improvement: adjust extractor options"

# C/C++: Include headers
export CODEQL_EXTRACTOR_CPP_OPTION_TRAP_HEADERS=true
log_result "Set CODEQL_EXTRACTOR_CPP_OPTION_TRAP_HEADERS=true"

# Java: Specific JDK version
export CODEQL_EXTRACTOR_JAVA_OPTION_JDK_VERSION=17
log_result "Set CODEQL_EXTRACTOR_JAVA_OPTION_JDK_VERSION=17"

# Then rebuild with current method
```

**After each improvement:** Re-assess quality. If no improvement possible, move to next build method.

---

## Reference: Ruleset Catalog

# Ruleset Catalog

## Official CodeQL Suites

| Suite | False Positives | Use Case |
|-------|-----------------|----------|
| `security-extended` | Low | **Default** - Security audits |
| `security-and-quality` | Medium | Comprehensive review |
| `security-experimental` | Higher | Research, vulnerability hunting |

**Usage:** `codeql/<lang>-queries:codeql-suites/<lang>-security-extended.qls`

**Languages:** `cpp`, `csharp`, `go`, `java`, `javascript`, `python`, `ruby`, `swift`

---

## Trail of Bits Packs

| Pack | Language | Focus |
|------|----------|-------|
| `trailofbits/cpp-queries` | C/C++ | Memory safety, integer overflows |
| `trailofbits/go-queries` | Go | Concurrency, error handling |
| `trailofbits/java-queries` | Java | Security, code quality |

**Install:**
```bash
codeql pack download trailofbits/cpp-queries
codeql pack download trailofbits/go-queries
codeql pack download trailofbits/java-queries
```

---

## CodeQL Community Packs

| Pack | Language |
|------|----------|
| `GitHubSecurityLab/CodeQL-Community-Packs-JavaScript` | JavaScript/TypeScript |
| `GitHubSecurityLab/CodeQL-Community-Packs-Python` | Python |
| `GitHubSecurityLab/CodeQL-Community-Packs-Go` | Go |
| `GitHubSecurityLab/CodeQL-Community-Packs-Java` | Java |
| `GitHubSecurityLab/CodeQL-Community-Packs-CPP` | C/C++ |
| `GitHubSecurityLab/CodeQL-Community-Packs-CSharp` | C# |
| `GitHubSecurityLab/CodeQL-Community-Packs-Ruby` | Ruby |

**Install:**
```bash
codeql pack download GitHubSecurityLab/CodeQL-Community-Packs-<Lang>
```

**Source:** [github.com/GitHubSecurityLab/CodeQL-Community-Packs](https://github.com/GitHubSecurityLab/CodeQL-Community-Packs)

---

## Verify Installation

```bash
# List all installed packs
codeql resolve qlpacks

# Check specific packs
codeql resolve qlpacks | grep -E "(trailofbits|GitHubSecurityLab)"
```

---

## Reference: Run All Suite

# Run-All Query Suite

In run-all mode, generate a custom `.qls` query suite file at runtime. This ensures all queries from all installed packs actually execute, avoiding the silent filtering caused by each pack's `defaultSuiteFile`.

## Why a Custom Suite

When you pass a pack name directly to `codeql database analyze` (e.g., `-- codeql/cpp-queries`), CodeQL uses the pack's `defaultSuiteFile` field from `qlpack.yml`. For official packs, this is typically `codeql-suites/<lang>-code-scanning.qls`, which applies strict precision and severity filters. This silently drops many queries and can produce zero results for small codebases.

The run-all suite explicitly references the broadest built-in suite (`security-and-quality`) for official packs and loads third-party packs with minimal filtering.

## Suite Template

Generate this file as `run-all.qls` in the results directory before running analysis:

```yaml
- description: Run-all — all security and quality queries from all installed packs
# Official queries: use security-and-quality suite (broadest built-in suite)
- import: codeql-suites/<CODEQL_LANG>-security-and-quality.qls
  from: codeql/<CODEQL_LANG>-queries
# Third-party packs (include only if installed, one entry per pack)
# - queries: .
#   from: trailofbits/<CODEQL_LANG>-queries
# - queries: .
#   from: GitHubSecurityLab/CodeQL-Community-Packs-<CODEQL_LANG>
# Minimal filtering — only select alert-type queries
- include:
    kind:
      - problem
      - path-problem
- exclude:
    deprecated: //
- exclude:
    tags contain:
      - modeleditor
      - modelgenerator
```

## Generation Script

```bash
RAW_DIR="$OUTPUT_DIR/raw"
SUITE_FILE="$RAW_DIR/run-all.qls"

# NOTE: CODEQL_LANG must be set before running this script (e.g., CODEQL_LANG=cpp)
# NOTE: INSTALLED_THIRD_PARTY_PACKS must be a space-separated list of pack names

cat > "$SUITE_FILE" << HEADER
- description: Run-all — all security and quality queries from all installed packs
- import: codeql-suites/${CODEQL_LANG}-security-and-quality.qls
  from: codeql/${CODEQL_LANG}-queries
HEADER

# Add each installed third-party pack
for PACK in $INSTALLED_THIRD_PARTY_PACKS; do
  cat >> "$SUITE_FILE" << PACK_ENTRY
- queries: .
  from: ${PACK}
PACK_ENTRY
done

# Append minimal filtering rules (quoted heredoc — no expansion needed)
cat >> "$SUITE_FILE" << 'FILTERS'
- include:
    kind:
      - problem
      - path-problem
- exclude:
    deprecated: //
- exclude:
    tags contain:
      - modeleditor
      - modelgenerator
FILTERS

# Verify the suite resolves correctly
: "${CODEQL_LANG:?ERROR: CODEQL_LANG must be set before generating suite}"
: "${SUITE_FILE:?ERROR: SUITE_FILE must be set}"

if ! codeql resolve queries "$SUITE_FILE" | wc -l; then
  echo "ERROR: Suite file failed to resolve. Check CODEQL_LANG=$CODEQL_LANG and installed packs."
fi
echo "Suite generated: $SUITE_FILE"
```

## How This Differs From Important-Only

| Aspect | Run all | Important only |
|--------|---------|----------------|
| Official pack suite | `security-and-quality` (all security + code quality) | All queries loaded, filtered by precision |
| Third-party packs | All `problem`/`path-problem` queries | Only `security`-tagged queries with precision metadata |
| Precision filter | None | high/very-high always; medium only if security-severity >= 6.0 |
| Post-analysis filter | None | Drops medium-precision results with security-severity < 6.0 |

---

## Reference: Sarif Processing

# SARIF Processing

jq commands for processing CodeQL SARIF output. Used in the run-analysis workflow Step 5.

> **SARIF structure note:** `security-severity` and `level` are stored on rule definitions (`.runs[].tool.driver.rules[]`), NOT on individual result objects. Results reference rules by `ruleIndex`. The jq commands below join results with their rule metadata.
>
> **Portability note:** These jq patterns assume CodeQL SARIF output where `ruleIndex` is populated. For SARIF from other tools (e.g., Semgrep), use `ruleId`-based lookups instead.

> **Directory convention:** Unfiltered output lives in `$RAW_DIR` (`$OUTPUT_DIR/raw`). Final results live in `$RESULTS_DIR` (`$OUTPUT_DIR/results`). The summary commands below operate on `$RESULTS_DIR/results.sarif` (the final output).

## Count Findings

```bash
jq '.runs[].results | length' "$RESULTS_DIR/results.sarif"
```

## Summary by SARIF Level

```bash
jq -r '
  .runs[] |
  . as $run |
  .results[] |
  ($run.tool.driver.rules[.ruleIndex].defaultConfiguration.level // "unknown")
' "$RESULTS_DIR/results.sarif" \
  | sort | uniq -c | sort -rn
```

## Summary by Security Severity (most useful for triage)

```bash
jq -r '
  .runs[] |
  . as $run |
  .results[] |
  ($run.tool.driver.rules[.ruleIndex].properties["security-severity"] // "none") + " | " +
  .ruleId + " | " +
  (.locations[0].physicalLocation.artifactLocation.uri // "?") + ":" +
  ((.locations[0].physicalLocation.region.startLine // 0) | tostring) + " | " +
  (.message.text // "no message" | .[0:80])
' "$RESULTS_DIR/results.sarif" | sort -rn | head -20
```

## Summary by Rule

```bash
jq -r '.runs[].results[] | .ruleId' "$RESULTS_DIR/results.sarif" \
  | sort | uniq -c | sort -rn
```

## Important-Only Post-Filter

If scan mode is "important only", filter out medium-precision results with `security-severity` < 6.0 from the report. The suite includes all medium-precision security queries to let CodeQL evaluate them, but low-severity medium-precision findings are noise.

The filter reads from `$RAW_DIR/results.sarif` (unfiltered) and writes to `$RESULTS_DIR/results.sarif` (final). The raw file is preserved unmodified.

```bash
# Filter important-only results: drop medium-precision findings with security-severity < 6.0
# Medium-precision queries without a security-severity score default to 0.0 (excluded).
# Non-medium queries are always kept regardless of security-severity.
# Reads from raw/, writes to results/ — preserving the unfiltered original.
RAW_DIR="$OUTPUT_DIR/raw"
RESULTS_DIR="$OUTPUT_DIR/results"
jq '
  .runs[] |= (
    . as $run |
    .results = [
      .results[] |
      ($run.tool.driver.rules[.ruleIndex].properties.precision // "unknown") as $prec |
      ($run.tool.driver.rules[.ruleIndex].properties["security-severity"] // null) as $raw_sev |
      (if $prec == "medium" then ($raw_sev // "0" | tonumber) else 10 end) as $sev |
      select(
        ($prec == "high") or ($prec == "very-high") or ($prec == "unknown") or
        ($prec == "medium" and $sev >= 6.0)
      )
    ]
  )
' "$RAW_DIR/results.sarif" > "$RESULTS_DIR/results.sarif"
```

---

## Reference: Threat Models

# Threat Models Reference

Control which source categories are active during CodeQL analysis. By default, only `remote` sources are tracked.

## Available Models

| Model | Sources Included | When to Enable | False Positive Impact |
|-------|------------------|----------------|----------------------|
| `remote` | HTTP requests, network input | Always (default). Covers web services, APIs, network-facing code. | Low — these are the most common attack vectors. |
| `local` | Command line args, local files | CLI tools, batch processors, desktop apps where local users are untrusted. | Medium — generates noise for web-only services where CLI args are developer-controlled. |
| `environment` | Environment variables | Apps that read config from env vars at runtime (12-factor apps, containers). Skip for apps that only read env at startup into validated config objects. | Medium — many env reads are startup-only config, not runtime-tainted data. |
| `database` | Database query results | Second-order injection scenarios: stored XSS, data from shared databases where other writers are untrusted. | High — most apps trust their own database. Only enable when auditing for stored/second-order attacks. |
| `file` | File contents | File upload processors, log parsers, config file readers that accept user-provided files. | Medium — triggers on all file reads including trusted config files. |

## Default Behavior

With no `--threat-model` flag, CodeQL uses `remote` only (the `default` group). This is correct for most web applications and APIs. Expanding beyond `remote` is useful when the application's trust boundary extends to local inputs.

## Usage

Enable additional threat models with the `--threat-model` flag (singular, NOT `--threat-models`):

```bash
# Web service (default — remote only, no flag needed)
codeql database analyze codeql.db \
  -- results/suite.qls

# CLI tool — local users can provide malicious input
codeql database analyze codeql.db \
  --threat-model local \
  -- results/suite.qls

# Container app reading env vars from untrusted orchestrator
codeql database analyze codeql.db \
  --threat-model local --threat-model environment \
  -- results/suite.qls

# Full coverage — audit mode for all input vectors
codeql database analyze codeql.db \
  --threat-model all \
  -- results/suite.qls

# Enable all except database (to reduce noise)
codeql database analyze codeql.db \
  --threat-model all --threat-model '!database' \
  -- results/suite.qls
```

The `--threat-model` flag can be repeated. Each invocation adds (or removes with `!` prefix) a threat model group. The `remote` group is always enabled by default — use `--threat-model '!default'` to disable it (rare). The `all` group enables everything, and `!<name>` disables a specific model.

Multiple models can be combined. Each additional model expands the set of sources CodeQL considers tainted, increasing coverage but potentially increasing false positives. Start with the narrowest set that matches the application's actual threat model, then expand if needed.
