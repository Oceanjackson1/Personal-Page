---
title: "Zeroize Audit"
description: "Detects missing zeroization of sensitive data in source code and identifies zeroization removed by compiler optimizations, with assembly-level analysis, and control-flow verification. Use for auditing C/C++/Rust code handling secrets, keys, passwo..."
category: "development"
source: "community"
author: "Community"
tags: ["zeroize", "audit"]
date: 2026-03-20
---

# zeroize-audit — Claude Skill

## When to Use
- Auditing cryptographic implementations (keys, seeds, nonces, secrets)
- Reviewing authentication systems (passwords, tokens, session data)
- Analyzing code that handles PII or sensitive credentials
- Verifying secure cleanup in security-critical codebases
- Investigating memory safety of sensitive data handling

## When NOT to Use
- General code review without security focus
- Performance optimization (unless related to secure wiping)
- Refactoring tasks not related to sensitive data
- Code without identifiable secrets or sensitive values

---

## Purpose
Detect missing zeroization of sensitive data in source code and identify zeroization that is removed or weakened by compiler optimizations (e.g., dead-store elimination), with mandatory LLVM IR/asm evidence. Capabilities include:
- Assembly-level analysis for register spills and stack retention
- Data-flow tracking for secret copies
- Heap allocator security warnings
- Semantic IR analysis for loop unrolling and SSA form
- Control-flow graph analysis for path coverage verification
- Runtime validation test generation

## Scope
- Read-only against the target codebase (does not modify audited code; writes analysis artifacts to a temporary working directory).
- Produces a structured report (JSON).
- Requires valid build context (`compile_commands.json`) and compilable translation units.
- "Optimized away" findings only allowed with compiler evidence (IR/asm diff).

---

## Inputs

See `{baseDir}/schemas/input.json` for the full schema. Key fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `path` | yes | — | Repo root |
| `compile_db` | no | `null` | Path to `compile_commands.json` for C/C++ analysis. Required if `cargo_manifest` is not set. |
| `cargo_manifest` | no | `null` | Path to `Cargo.toml` for Rust crate analysis. Required if `compile_db` is not set. |
| `config` | no | — | YAML defining heuristics and approved wipes |
| `opt_levels` | no | `["O0","O1","O2"]` | Optimization levels for IR comparison. O1 is the diagnostic level: if a wipe disappears at O1 it is simple DSE; O2 catches more aggressive eliminations. |
| `languages` | no | `["c","cpp","rust"]` | Languages to analyze |
| `max_tus` | no | — | Limit on translation units processed from compile DB |
| `mcp_mode` | no | `prefer` | `off`, `prefer`, or `require` — controls Serena MCP usage |
| `mcp_required_for_advanced` | no | `true` | Downgrade `SECRET_COPY`, `MISSING_ON_ERROR_PATH`, and `NOT_DOMINATING_EXITS` to `needs_review` when MCP is unavailable |
| `mcp_timeout_ms` | no | — | Timeout budget for MCP semantic queries |
| `poc_categories` | no | all 11 exploitable | Finding categories for which to generate PoCs. C/C++ findings: all 11 categories supported. Rust findings: only `MISSING_SOURCE_ZEROIZE`, `SECRET_COPY`, and `PARTIAL_WIPE` are supported; other Rust categories are marked `poc_supported=false`. |
| `poc_output_dir` | no | `generated_pocs/` | Output directory for generated PoCs |
| `enable_asm` | no | `true` | Enable assembly emission and analysis (Step 8); produces `STACK_RETENTION`, `REGISTER_SPILL`. Auto-disabled if `emit_asm.sh` is missing. |
| `enable_semantic_ir` | no | `false` | Enable semantic LLVM IR analysis (Step 9); produces `LOOP_UNROLLED_INCOMPLETE` |
| `enable_cfg` | no | `false` | Enable control-flow graph analysis (Step 10); produces `MISSING_ON_ERROR_PATH`, `NOT_DOMINATING_EXITS` |
| `enable_runtime_tests` | no | `false` | Enable runtime test harness generation (Step 11) |

---

## Prerequisites

Before running, verify the following. Each has a defined failure mode.

**C/C++ prerequisites:**

| Prerequisite | Failure mode if missing |
|---|---|
| `compile_commands.json` at `compile_db` path | Fail fast — do not proceed |
| `clang` on PATH | Fail fast — IR/ASM analysis impossible |
| `uvx` on PATH (for Serena) | If `mcp_mode=require`: fail. If `mcp_mode=prefer`: continue without MCP; downgrade affected findings per Confidence Gating rules. |
| `{baseDir}/tools/extract_compile_flags.py` | Fail fast — cannot extract per-TU flags |
| `{baseDir}/tools/emit_ir.sh` | Fail fast — IR analysis impossible |
| `{baseDir}/tools/emit_asm.sh` | Warn and skip assembly findings (STACK_RETENTION, REGISTER_SPILL) |
| `{baseDir}/tools/mcp/check_mcp.sh` | Warn and treat as MCP unavailable |
| `{baseDir}/tools/mcp/normalize_mcp_evidence.py` | Warn and use raw MCP output |

**Rust prerequisites:**

| Prerequisite | Failure mode if missing |
|---|---|
| `Cargo.toml` at `cargo_manifest` path | Fail fast — do not proceed |
| `cargo check` passes | Fail fast — crate must be buildable |
| `cargo +nightly` on PATH | Fail fast — nightly required for MIR and LLVM IR emission |
| `uv` on PATH | Fail fast — required to run Python analysis scripts |
| `{baseDir}/tools/validate_rust_toolchain.sh` | Warn — run preflight manually. Checks all tools, scripts, nightly, and optionally `cargo check`. Use `--json` for machine-readable output, `--manifest` to also validate the crate builds. |
| `{baseDir}/tools/emit_rust_mir.sh` | Fail fast — MIR analysis impossible (`--opt`, `--crate`, `--bin/--lib` supported; `--out` can be file or directory) |
| `{baseDir}/tools/emit_rust_ir.sh` | Fail fast — LLVM IR analysis impossible (`--opt` required; `--crate`, `--bin/--lib` supported; `--out` must be `.ll`) |
| `{baseDir}/tools/emit_rust_asm.sh` | Warn and skip assembly findings (`STACK_RETENTION`, `REGISTER_SPILL`). Supports `--opt`, `--crate`, `--bin/--lib`, `--target`, `--intel-syntax`; `--out` can be `.s` file or directory. |
| `{baseDir}/tools/diff_rust_mir.sh` | Warn and skip MIR-level optimization comparison. Accepts 2+ MIR files, normalizes, diffs pairwise, and reports first opt level where zeroize/drop-glue patterns disappear. |
| `{baseDir}/tools/scripts/semantic_audit.py` | Warn and skip semantic source analysis |
| `{baseDir}/tools/scripts/find_dangerous_apis.py` | Warn and skip dangerous API scan |
| `{baseDir}/tools/scripts/check_mir_patterns.py` | Warn and skip MIR analysis |
| `{baseDir}/tools/scripts/check_llvm_patterns.py` | Warn and skip LLVM IR analysis |
| `{baseDir}/tools/scripts/check_rust_asm.py` | Warn and skip Rust assembly analysis (`STACK_RETENTION`, `REGISTER_SPILL`, drop-glue checks). Dispatches to `check_rust_asm_x86.py` (production) or `check_rust_asm_aarch64.py` (**EXPERIMENTAL** — AArch64 findings require manual verification). |
| `{baseDir}/tools/scripts/check_rust_asm_x86.py` | Required by `check_rust_asm.py` for x86-64 analysis; warn and skip if missing |
| `{baseDir}/tools/scripts/check_rust_asm_aarch64.py` | Required by `check_rust_asm.py` for AArch64 analysis (**EXPERIMENTAL**); warn and skip if missing |

**Common prerequisite:**

| Prerequisite | Failure mode if missing |
|---|---|
| `{baseDir}/tools/generate_poc.py` | Fail fast — PoC generation is mandatory |

---

## Approved Wipe APIs

The following are recognized as valid zeroization. Configure additional entries in `{baseDir}/configs/`.

**C/C++**
- `explicit_bzero`
- `memset_s`
- `SecureZeroMemory`
- `OPENSSL_cleanse`
- `sodium_memzero`
- Volatile wipe loops (pattern-based; see `volatile_wipe_patterns` in `{baseDir}/configs/default.yaml`)
- In IR: `llvm.memset` with volatile flag, volatile stores, or non-elidable wipe call

**Rust**
- `zeroize::Zeroize` trait (`zeroize()` method)
- `Zeroizing<T>` wrapper (drop-based)
- `ZeroizeOnDrop` derive macro

---

## Finding Capabilities

Findings are grouped by required evidence. Only attempt findings for which the required tooling is available.

| Finding ID | Description | Requires | PoC Support |
|---|---|---|---|
| `MISSING_SOURCE_ZEROIZE` | No zeroization found in source | Source only | Yes (C/C++ + Rust) |
| `PARTIAL_WIPE` | Incorrect size or incomplete wipe | Source only | Yes (C/C++ + Rust) |
| `NOT_ON_ALL_PATHS` | Zeroization missing on some control-flow paths (heuristic) | Source only | Yes (C/C++ only) |
| `SECRET_COPY` | Sensitive data copied without zeroization tracking | Source + MCP preferred | Yes (C/C++ + Rust) |
| `INSECURE_HEAP_ALLOC` | Secret uses insecure allocator (malloc vs. secure_malloc) | Source only | Yes (C/C++ only) |
| `OPTIMIZED_AWAY_ZEROIZE` | Compiler removed zeroization | IR diff required (never source-only) | Yes |
| `STACK_RETENTION` | Stack frame may retain secrets after return | Assembly required (C/C++); LLVM IR `alloca`+`lifetime.end` evidence (Rust); assembly corroboration upgrades to `confirmed` | Yes (C/C++ only) |
| `REGISTER_SPILL` | Secrets spilled from registers to stack | Assembly required (C/C++); LLVM IR `load`+call-site evidence (Rust); assembly corroboration upgrades to `confirmed` | Yes (C/C++ only) |
| `MISSING_ON_ERROR_PATH` | Error-handling paths lack cleanup | CFG or MCP required | Yes |
| `NOT_DOMINATING_EXITS` | Wipe doesn't dominate all exits | CFG or MCP required | Yes |
| `LOOP_UNROLLED_INCOMPLETE` | Unrolled loop wipe is incomplete | Semantic IR required | Yes |

---

## Agent Architecture

The analysis pipeline uses 11 agents across 8 phases, invoked by the orchestrator (`{baseDir}/prompts/task.md`) via `Task`. Agents write persistent finding files to a shared working directory (`/tmp/zeroize-audit-{run_id}/`), enabling parallel execution and protecting against context pressure.

| Agent | Phase | Purpose | Output Directory |
|---|---|---|---|
| `0-preflight` | Phase 0 | Preflight checks (tools, toolchain, compile DB, crate build), config merge, workdir creation, TU enumeration | `{workdir}/` |
| `1-mcp-resolver` | Phase 1, Wave 1 (C/C++ only) | Resolve symbols, types, and cross-file references via Serena MCP | `mcp-evidence/` |
| `2-source-analyzer` | Phase 1, Wave 2a (C/C++ only) | Identify sensitive objects, detect wipes, validate correctness, data-flow/heap | `source-analysis/` |
| `2b-rust-source-analyzer` | Phase 1, Wave 2b (Rust only, parallel with 2a) | Rustdoc JSON trait-aware analysis + dangerous API grep | `source-analysis/` |
| `3-tu-compiler-analyzer` | Phase 2, Wave 3 (C/C++ only, N parallel) | Per-TU IR diff, assembly, semantic IR, CFG analysis | `compiler-analysis/{tu_hash}/` |
| `3b-rust-compiler-analyzer` | Phase 2, Wave 3R (Rust only, single agent) | Crate-level MIR, LLVM IR, and assembly analysis | `rust-compiler-analysis/` |
| `4-report-assembler` | Phase 3 (interim) + Phase 6 (final) | Collect findings from all agents, apply confidence gates; merge PoC results and produce final report | `report/` |
| `5-poc-generator` | Phase 4 | Craft bespoke proof-of-concept programs (C/C++: all categories; Rust: MISSING_SOURCE_ZEROIZE, SECRET_COPY, PARTIAL_WIPE) | `poc/` |
| `5b-poc-validator` | Phase 5 | Compile and run all PoCs | `poc/` |
| `5c-poc-verifier` | Phase 5 | Verify each PoC proves its claimed finding | `poc/` |
| `6-test-generator` | Phase 7 (optional) | Generate runtime validation test harnesses | `tests/` |

The orchestrator reads one per-phase workflow file from `{baseDir}/workflows/` at a time, and maintains `orchestrator-state.json` for recovery after context compression. Agents receive configuration by file path (`config_path`), not by value.

### Execution flow

```
Phase 0: 0-preflight agent — Preflight + config + create workdir + enumerate TUs
           → writes orchestrator-state.json, merged-config.yaml, preflight.json
Phase 1: Wave 1:  1-mcp-resolver              (skip if mcp_mode=off OR language_mode=rust)
         Wave 2a: 2-source-analyzer           (C/C++ only; skip if no compile_db)  ─┐ parallel
         Wave 2b: 2b-rust-source-analyzer     (Rust only; skip if no cargo_manifest) ─┘
Phase 2: Wave 3:  3-tu-compiler-analyzer x N  (C/C++ only; parallel per TU)
         Wave 3R: 3b-rust-compiler-analyzer   (Rust only; single crate-level agent)
Phase 3: Wave 4:  4-report-assembler          (mode=interim → findings.json; reads all agent outputs)
Phase 4: Wave 5:  5-poc-generator             (C/C++: all categories; Rust: MISSING_SOURCE_ZEROIZE, SECRET_COPY, PARTIAL_WIPE; other Rust findings: poc_supported=false)
Phase 5: PoC Validation & Verification
           Step 1: 5b-poc-validator agent      (compile and run all PoCs)
           Step 2: 5c-poc-verifier agent       (verify each PoC proves its claimed finding)
           Step 3: Orchestrator presents verification failures to user via AskUserQuestion
           Step 4: Orchestrator merges all results into poc_final_results.json
Phase 6: Wave 6: 4-report-assembler           (mode=final → merge PoC results, final-report.md)
Phase 7: Wave 7: 6-test-generator             (optional)
Phase 8: Orchestrator — Return final-report.md
```

## Cross-Reference Convention

IDs are namespaced per agent to prevent collisions during parallel execution:

| Entity | Pattern | Assigned By |
|---|---|---|
| Sensitive object (C/C++) | `SO-0001`–`SO-4999` | `2-source-analyzer` |
| Sensitive object (Rust) | `SO-5000`–`SO-9999` (Rust namespace) | `2b-rust-source-analyzer` |
| Source finding (C/C++) | `F-SRC-NNNN` | `2-source-analyzer` |
| Source finding (Rust) | `F-RUST-SRC-NNNN` | `2b-rust-source-analyzer` |
| IR finding (C/C++) | `F-IR-{tu_hash}-NNNN` | `3-tu-compiler-analyzer` |
| ASM finding (C/C++) | `F-ASM-{tu_hash}-NNNN` | `3-tu-compiler-analyzer` |
| CFG finding | `F-CFG-{tu_hash}-NNNN` | `3-tu-compiler-analyzer` |
| Semantic IR finding | `F-SIR-{tu_hash}-NNNN` | `3-tu-compiler-analyzer` |
| Rust MIR finding | `F-RUST-MIR-NNNN` | `3b-rust-compiler-analyzer` |
| Rust LLVM IR finding | `F-RUST-IR-NNNN` | `3b-rust-compiler-analyzer` |
| Rust assembly finding | `F-RUST-ASM-NNNN` | `3b-rust-compiler-analyzer` |
| Translation unit | `TU-{hash}` | Orchestrator |
| Final finding | `ZA-NNNN` | `4-report-assembler` |

Every finding JSON object includes `related_objects`, `related_findings`, and `evidence_files` fields for cross-referencing between agents.

---

## Detection Strategy

Analysis runs in two phases. For complete step-by-step guidance, see `{baseDir}/references/detection-strategy.md`.

| Phase | Steps | Findings produced | Required tooling |
|---|---|---|---|
| Phase 1 (Source) | 1–6 | `MISSING_SOURCE_ZEROIZE`, `PARTIAL_WIPE`, `NOT_ON_ALL_PATHS`, `SECRET_COPY`, `INSECURE_HEAP_ALLOC` | Source + compile DB |
| Phase 2 (Compiler) | 7–12 | `OPTIMIZED_AWAY_ZEROIZE`, `STACK_RETENTION`*, `REGISTER_SPILL`*, `LOOP_UNROLLED_INCOMPLETE`†, `MISSING_ON_ERROR_PATH`‡, `NOT_DOMINATING_EXITS`‡ | `clang`, IR/ASM tools |

\* requires `enable_asm=true` (default)
† requires `enable_semantic_ir=true`
‡ requires `enable_cfg=true`

---


## Output Format

Each run produces two outputs:

1. **`final-report.md`** — Comprehensive markdown report (primary human-readable output)
2. **`findings.json`** — Structured JSON matching `{baseDir}/schemas/output.json` (for machine consumption and downstream tools)

### Markdown Report Structure

The markdown report (`final-report.md`) contains these sections:

- **Header**: Run metadata (run_id, timestamp, repo, compile_db, config summary)
- **Executive Summary**: Finding counts by severity, confidence, and category
- **Sensitive Objects Inventory**: Table of all identified objects with IDs, types, locations
- **Findings**: Grouped by severity then confidence. Each finding includes location, object, all evidence (source/IR/ASM/CFG), compiler evidence details, and recommended fix
- **Superseded Findings**: Source findings replaced by CFG-backed findings
- **Confidence Gate Summary**: Downgrades applied and overrides rejected
- **Analysis Coverage**: TUs analyzed, agent success/failure, features enabled
- **Appendix: Evidence Files**: Mapping of finding IDs to evidence file paths

### Structured JSON

The `findings.json` file follows the schema in `{baseDir}/schemas/output.json`. Each `Finding` object:

```json
{
  "id": "ZA-0001",
  "category": "OPTIMIZED_AWAY_ZEROIZE",
  "severity": "high",
  "confidence": "confirmed",
  "language": "c",
  "file": "src/crypto.c",
  "line": 42,
  "symbol": "key_buf",
  "evidence": "store volatile i8 0 count: O0=32, O2=0 — wipe eliminated by DSE",
  "compiler_evidence": {
    "opt_levels": ["O0", "O2"],
    "o0": "32 volatile stores targeting key_buf",
    "o2": "0 volatile stores (all eliminated)",
    "diff_summary": "All volatile wipe stores removed at O2 — classic DSE pattern"
  },
  "suggested_fix": "Replace memset with explicit_bzero or add compiler_fence(SeqCst) after the wipe",
  "poc": {
    "file": "generated_pocs/ZA-0001.c",
    "makefile_target": "ZA-0001",
    "compile_opt": "-O2",
    "requires_manual_adjustment": false,
    "validated": true,
    "validation_result": "exploitable"
  }
}
```

See `{baseDir}/schemas/output.json` for the full schema and enum values.

---

## Confidence Gating

### Evidence thresholds

A finding requires at least **2 independent signals** to be marked `confirmed`. With 1 signal, mark `likely`. With 0 strong signals (name-pattern match only), mark `needs_review`.

Signals include: name pattern match, type hint match, explicit annotation, IR evidence, ASM evidence, MCP cross-reference, CFG evidence, PoC validation.

### PoC validation as evidence signal

Every finding is validated against a bespoke PoC. After compilation and execution, each PoC is also verified to ensure it actually tests the claimed vulnerability. The combined result is an evidence signal:

| PoC Result | Verified | Impact |
|---|---|---|
| Exit 0 (exploitable) | Yes | Strong signal — can upgrade `likely` to `confirmed` |
| Exit 1 (not exploitable) | Yes | Downgrade severity to `low` (informational); retain in report |
| Exit 0 or 1 | No (user accepted) | Weaker signal — note verification failure in evidence |
| Exit 0 or 1 | No (user rejected) | No confidence change; annotate as `rejected` |
| Compile failure / no PoC | — | No confidence change; annotate in evidence |

### MCP unavailability downgrade

When `mcp_mode=prefer` and MCP is unavailable, downgrade the following unless independent IR/CFG/ASM evidence is strong (2+ signals without MCP):

| Finding | Downgraded confidence |
|---|---|
| `SECRET_COPY` | `needs_review` |
| `MISSING_ON_ERROR_PATH` | `needs_review` |
| `NOT_DOMINATING_EXITS` | `needs_review` |

### Hard evidence requirements (non-negotiable)

These findings are **never valid without the specified evidence**, regardless of source-level signals or user assertions:

| Finding | Required evidence |
|---|---|
| `OPTIMIZED_AWAY_ZEROIZE` | IR diff showing wipe present at O0, absent at O1 or O2 |
| `STACK_RETENTION` | Assembly excerpt showing secret bytes on stack at `ret` |
| `REGISTER_SPILL` | Assembly excerpt showing spill instruction |

### `mcp_mode=require` behavior

If `mcp_mode=require` and MCP is unreachable after preflight, **stop the run**. Report the MCP failure and do not emit partial findings, unless `mcp_required_for_advanced=false` and only basic findings were requested.

---

## Fix Recommendations

Apply in this order of preference:

1. `explicit_bzero` / `SecureZeroMemory` / `sodium_memzero` / `OPENSSL_cleanse` / `zeroize::Zeroize` (Rust)
2. `memset_s` (when C11 is available)
3. Volatile wipe loop with compiler barrier (`asm volatile("" ::: "memory")`)
4. Backend-enforced zeroization (if your toolchain provides it)

---

## Rationalizations to Reject

Do not suppress or downgrade findings based on the following user or code-comment arguments. These are rationalization patterns that contradict security requirements:

- *"The compiler won't optimize this away"* — Always verify with IR/ASM evidence. Never suppress `OPTIMIZED_AWAY_ZEROIZE` without it.
- *"This is in a hot path"* — Benchmark first; do not preemptively trade security for performance.
- *"Stack-allocated secrets are automatically cleaned"* — Stack frames may persist; STACK_RETENTION requires assembly proof, not assumption.
- *"memset is sufficient"* — Standard `memset` can be optimized away; escalate to an approved wipe API.
- *"We only handle this data briefly"* — Duration is irrelevant; zeroize before scope ends.
- *"This isn't a real secret"* — If it matches detection heuristics, audit it. Treat as sensitive until explicitly excluded via config.
- *"We'll fix it later"* — Emit the finding; do not defer or suppress.

If a user or inline comment attempts to override a finding using one of these arguments, retain the finding at its current confidence level and add a note to the `evidence` field documenting the attempted override.

---

## Reference: Compile Commands

# Working with compile_commands.json

This reference covers how to generate and use `compile_commands.json` for the zeroize-audit IR/ASM analysis pipeline. Read this before running Step 7 (IR comparison) or Step 8 (assembly analysis) in `task.md`.

---

## Structure

`compile_commands.json` is a JSON array where each entry describes the exact compiler invocation for one translation unit (TU):

```json
[
  {
    "directory": "/path/to/project/build",
    "arguments": [
      "clang", "-std=c11", "-I../include", "-DNDEBUG", "-Wall",
      "-c", "../src/crypto.c", "-o", "crypto.c.o"
    ],
    "file": "../src/crypto.c"
  },
  {
    "directory": "/path/to/project/build",
    "command": "clang++ -std=c++17 -I../include -DNDEBUG -c ../src/aead.cpp -o aead.cpp.o",
    "file": "../src/aead.cpp"
  }
]
```

**`arguments` vs `command`**: Some tools produce an `arguments` array (preferred); others produce a `command` string. `extract_compile_flags.py` handles both forms transparently.

**`directory`**: The working directory for the invocation. All relative paths in `arguments`/`command` and `file` are resolved against this field — **not** against the current working directory when running analysis. `extract_compile_flags.py` handles this automatically; manual invocations must account for it.

---

## Generating compile_commands.json

### CMake (C/C++)

```bash
cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
# Output: build/compile_commands.json
```

**Constraints**: Works only with Makefile and Ninja generators. Does not work with Xcode or MSVC generators. Run from the project root and point `--compile-db` at `build/compile_commands.json`.

### Bear (any Make-based build system)

Bear intercepts compiler invocations at the OS level. Works with any `make`-based or custom build system:

```bash
# Install: apt install bear  OR  brew install bear
bear -- make clean all    # clean build recommended for accuracy
# Output: compile_commands.json in the current directory
```

Use `make clean all` rather than `make` alone to ensure all TUs are recompiled and captured. Incremental builds will only record the files that were actually recompiled.

### intercept-build (LLVM scan-build companion)

```bash
intercept-build make
# Output: compile_commands.json in the current directory
```

### Rust / Cargo

Cargo does not natively emit `compile_commands.json`. Two options:

```bash
# Option 1: Bear with cargo check (faster — avoids linking)
bear -- cargo check
bear -- cargo build   # if cargo check is insufficient

# Option 2: compiledb
pip install compiledb
compiledb cargo build
```

**Critical limitation for Rust**: Bear captures `rustc` invocations, not `clang` invocations. `emit_ir.sh` (which calls `clang`) **will not work** directly on Rust TUs. Use `cargo rustc` instead to emit IR and assembly directly:

```bash
# Preferred: use the emit scripts which handle CARGO_TARGET_DIR isolation:
{baseDir}/tools/emit_rust_ir.sh --manifest Cargo.toml --opt O0 --out /tmp/crate.O0.ll
{baseDir}/tools/emit_rust_ir.sh --manifest Cargo.toml --opt O2 --out /tmp/crate.O2.ll

# Manual alternative (output goes to an isolated temp dir, not target/debug/deps):
CARGO_TARGET_DIR=/tmp/zir cargo rustc -- --emit=llvm-ir -C opt-level=0
CARGO_TARGET_DIR=/tmp/zir cargo rustc -- --emit=llvm-ir -C opt-level=2

# Assembly for Rust (use instead of emit_asm.sh):
cargo rustc -- --emit=asm -C opt-level=2
# Output: target/release/deps/*.s
```

Pass the resulting `.ll` and `.s` files directly to `diff_ir.sh` and `analyze_asm.sh`.

---

## End-to-End Pipeline

The canonical pipeline for C/C++ analysis. Always use a hash of the source path as `<tu_hash>` (not the raw filename) to avoid collisions during parallel TU processing. Clean up temp files on completion or failure.

```bash
mkdir -p /tmp/zeroize-audit/

# Step 1: Extract build-relevant flags for the TU (as a bash array)
FLAGS=()
while IFS= read -r flag; do FLAGS+=("$flag"); done < <(
  python {baseDir}/tools/extract_compile_flags.py \
    --compile-db /path/to/build/compile_commands.json \
    --src /path/to/src/crypto.c --format lines)

# Step 2: Emit IR at each level in opt_levels (always include O0 as baseline)
{baseDir}/tools/emit_ir.sh \
  --src /path/to/src/crypto.c \
  --out /tmp/zeroize-audit/<tu_hash>.O0.ll --opt O0 -- "${FLAGS[@]}"

{baseDir}/tools/emit_ir.sh \
  --src /path/to/src/crypto.c \
  --out /tmp/zeroize-audit/<tu_hash>.O1.ll --opt O1 -- "${FLAGS[@]}"

{baseDir}/tools/emit_ir.sh \
  --src /path/to/src/crypto.c \
  --out /tmp/zeroize-audit/<tu_hash>.O2.ll --opt O2 -- "${FLAGS[@]}"

# Step 3: Diff across all levels — O1 is the diagnostic level for simple DSE;
#         O2 catches more aggressive eliminations
{baseDir}/tools/diff_ir.sh \
  /tmp/zeroize-audit/<tu_hash>.O0.ll \
  /tmp/zeroize-audit/<tu_hash>.O1.ll \
  /tmp/zeroize-audit/<tu_hash>.O2.ll

# Step 4: Emit assembly at O2 for register-spill and stack-retention analysis
{baseDir}/tools/emit_asm.sh \
  --src /path/to/src/crypto.c \
  --out /tmp/zeroize-audit/<tu_hash>.O2.s --opt O2 -- "${FLAGS[@]}"

# Step 5: Analyze assembly output
{baseDir}/tools/analyze_asm.sh /tmp/zeroize-audit/<tu_hash>.O2.s

# Cleanup
rm -rf /tmp/zeroize-audit/<tu_hash>.*
```

Refer to the IR analysis reference (loaded separately from SKILL.md) for how to interpret IR diffs and identify wipe elimination patterns.

---

## Flags Stripped by extract_compile_flags.py

These flags are removed because they are irrelevant to or break single-file IR/ASM emission:

| Flag(s) | Reason stripped |
|---|---|
| `-o <file>` | Emission tools supply their own `-o` |
| `-c` | IR/ASM emission uses `-S -emit-llvm` / `-S` instead |
| `-MF`, `-MT`, `-MQ` (+ argument) | Dependency file generation — irrelevant for analysis |
| `-MD`, `-MMD`, `-MP`, `-MG` | Dependency generation side-effects |
| `-pipe` | OS pipe between compiler stages; not meaningful for direct calls |
| `-save-temps` | Saves intermediate files; produces clutter |
| `-gsplit-dwarf` | Splits debug info to `.dwo`; incompatible with single-file emission |
| `-fcrash-diagnostics-dir=...` | Crash report output; irrelevant |
| `-fmodule-file=...`, `-fmodules-cache-path=...` | Clang module paths; may confuse single-TU invocation |
| `--serialize-diagnostics` | Clang diagnostic binary output; not needed |
| `-fdebug-prefix-map=...` | Debug info path remapping; harmless to strip |
| `-fprofile-generate`, `-fprofile-use=...` | PGO instrumentation; distorts IR for analysis |
| `-fcoverage-mapping` | Coverage instrumentation; alters IR structure |

Flags that are **kept** (build-relevant):

| Pattern | Reason kept |
|---|---|
| `-I`, `-isystem`, `-iquote` | Include paths required to parse the TU |
| `-D`, `-U` | Preprocessor defines/undefines that affect code paths |
| `-std=<val>` | Language standard — affects syntax and semantics |
| `-f*` security/codegen flags | e.g., `-fstack-protector`, `-fPIC`, `-fno-omit-frame-pointer` |
| `-m<arch>` | Target architecture flags (e.g., `-m64`, `-march=x86-64`, `-mthumb`) |
| `-W*` | Warning flags — harmless to pass through |
| `-pthread` | Threading model; affects macro definitions |
| `--sysroot=`, `-isysroot` | System root for cross-compilation |
| `-target <triple>` | Cross-compilation target triple; must be preserved |

---

## Common Pitfalls

### 1. Relative paths and the `"directory"` field

`"file": "../src/crypto.c"` is relative to `"directory"`, not to the CWD when running analysis. Always resolve file paths using `"directory"`. `extract_compile_flags.py` does this automatically; be explicit if invoking `clang` manually.

### 2. Multiple entries for the same file

Some build systems emit duplicate entries (e.g., with and without a precompiled header). `extract_compile_flags.py` returns the **first** match. If that entry includes `-fpch-preprocess`, the PCH must exist in the build directory for compilation to succeed. Either regenerate the PCH or strip PCH-related flags manually.

### 3. Stale or incomplete compile DB (most common failure)

If `bear` or CMake was run on an incremental build, only recompiled TUs are recorded. TUs compiled in a previous run may be missing or have outdated flags. **Always generate the compile DB from a clean build** (`make clean all`, `cargo clean && cargo build`) to ensure all TUs are captured with current flags.

`extract_compile_flags.py` exits with code 2 if a source file is not found in the DB. Common causes:
- Header-only files (no TU entry — expected)
- Files added after the last `bear`/CMake run
- Symlinked paths that resolve differently than recorded

Regenerate the compile DB if entries are missing.

### 4. Generated source files

Entries may point to generated files in the build directory (e.g., `build/generated/config.c`) that don't exist in a clean checkout. Run the build system to generate them before running analysis. Preflight (Step 1 in `task.md`) will catch this if trial compilation is attempted.

### 5. Cross-compilation targets

If the compile DB was generated for a cross-compilation target (e.g., `-target aarch64-linux-gnu` or `-target thumbv7m-none-eabi`), emitted IR and assembly will be for that target, not x86-64. This affects analysis in two ways:

- **IR diffs**: Only compare IR files emitted for the same target. Do not mix targets across opt levels.
- **Assembly analysis**: `analyze_asm.sh` adapts register patterns by target:
  - x86-64: callee-saved registers are `rbx`, `r12`–`r15`; spills use `movq`/`movdqa` to `[rsp+N]`
  - AArch64: callee-saved registers are `x19`–`x28`; spills use `str`/`stp` to `[sp, #N]`
  - Thumb/ARM: callee-saved registers are `r4`–`r11`; spills use `str`/`stm` to `[sp, #N]`

Ensure `--target` is preserved in the stripped flags (it is, per the kept-flags table above).

### 6. `extract_compile_flags.py` exit codes

| Exit code | Meaning |
|---|---|
| 0 | Flags extracted successfully; output on stdout |
| 1 | Compile DB not found or not readable |
| 2 | Source file not found in compile DB |
| 3 | Compile DB is malformed JSON |

Check the exit code before passing flags to emission tools. An empty `FLAGS` array will silently produce incorrect IR.

---

## Reference: Detection Strategy

# Detection Strategy

Read this during execution to guide per-step analysis. Steps 1–6 are Phase 1 (source-level); Steps 7–12 are Phase 2 (compiler-level).

---

## Phase 1 — Source-Level Analysis

### Step 1 — Preflight Build Context (mandatory)
- Verify `compile_db` exists and is readable.
- Verify compile database entries point to existing files/working directories.
- Verify the codebase is compilable with the captured commands (or equivalent build invocation).
- Fail fast if preflight fails; do not continue with partial/source-only analysis.

### Step 2 — Identify Sensitive Objects

Scan all TUs for objects matching these heuristics. Each heuristic has a confidence level that propagates to findings.

**Name patterns (low confidence)** — match substrings case-insensitively:
`key`, `secret`, `seed`, `priv`, `sk`, `shared_secret`, `nonce`, `token`, `pwd`, `pass`

**Type hints (medium confidence)** — byte buffers, fixed-size arrays, or structs whose names or fields match name patterns above.

**Explicit annotations (high confidence)**:
- Rust: `#[secret]`, `Secret<T>` patterns (configurable)
- C/C++: `__attribute__((annotate("sensitive")))`, `SENSITIVE` macro (configurable via `explicit_sensitive_markers` in `{baseDir}/configs/default.yaml`)

Record each sensitive object with: name, type, location (file:line), confidence level, and the heuristic that matched.

### Step 3 — Detect Zeroization Attempts

For each sensitive object identified in Step 2, check whether a call to an approved wipe API (see Approved Wipe APIs in SKILL.md) exists within the same scope or a cleanup function reachable from that scope.

Record: wipe API used, location, and whether the wipe was found at all.

### Step 4 — MCP Semantic Pass (when available)

Run this step **before** correctness validation so that resolved types, aliases, and cross-file references are available to Steps 5 and 6. Skip and continue if MCP is unavailable in `prefer` mode (see Confidence Gating in SKILL.md).

- Run `{baseDir}/tools/mcp/check_mcp.sh` to confirm MCP is live. If it fails and `mcp_mode=require`, stop the run.
- Activate the project with `activate_project` (pass the repository root path). This must succeed before any other Serena tool can be used. If activation fails, treat MCP as unavailable.
- For each sensitive object and wipe call, resolve symbol definitions using `find_symbol` (by name, with `include_body: true` for type details) and collect cross-file references using `find_referencing_symbols`.
- Trace callers and cleanup paths using `find_referencing_symbols` on wipe wrapper functions. For outgoing calls, read the function body from `find_symbol` output and resolve called symbols.
- Use `get_symbols_overview` to get a high-level view of symbols in a file when exploring unfamiliar TUs.
- Normalize all MCP output: `python {baseDir}/tools/mcp/normalize_mcp_evidence.py`.

Prioritize `find_symbol` queries by sensitive-object name first, then wipe wrapper names. Score confidence: name match alone → `needs_review`; name + type resolved → `likely`; name + type + call chain confirmed → `confirmed`.

### Step 5 — Validate Correctness

For each sensitive object with a detected wipe, use type and alias data from Step 4 (if available) to validate:
- **Size correct**: wipe length matches `sizeof(object)`, not `sizeof(pointer)`. MCP-resolved typedefs and array sizes take precedence over source-level estimates.
- **All exits covered** (heuristic): wipe is present on normal exit, early return, and error paths visible in source. Flag `NOT_ON_ALL_PATHS` if any path appears uncovered.
- **Ordering correct**: wipe occurs before `free()` or scope end, not after.

Emit `PARTIAL_WIPE` for incorrect size. Emit `NOT_ON_ALL_PATHS` for missing paths (heuristic; CFG analysis in Step 10 provides definitive results).

### Step 6 — Data-Flow and Heap Checks

Use cross-file reference data from Step 4 (if available) to extend tracking beyond the current TU.

**Data-flow (produces `SECRET_COPY`):**
- Detect `memcpy()`/`memmove()` copying sensitive buffers.
- Track struct assignments and array copies of sensitive objects.
- Flag function arguments passed by value (copies on stack).
- Flag secrets returned by value.
- Emit `SECRET_COPY` when any of the above copies exist and no approved wipe is tracked for the copy destination.

**Heap (produces `INSECURE_HEAP_ALLOC`):**
- Detect `malloc`/`calloc`/`realloc` used to allocate sensitive objects.
- Check for `mlock()`/`madvise(MADV_DONTDUMP)` — note absence as a warning.
- Recommend secure allocators: `OPENSSL_secure_malloc`, `sodium_malloc`.

---

## Phase 2 — Compiler-Level Analysis

All steps in Phase 2 require a valid compile DB and a working `clang` installation. Skip Phase 2 findings if Phase 1 preflight failed.

### Step 7 — IR Comparison (produces `OPTIMIZED_AWAY_ZEROIZE`)

For each TU containing sensitive objects:

```bash
FLAGS=()
while IFS= read -r flag; do FLAGS+=("$flag"); done < <(
  python {baseDir}/tools/extract_compile_flags.py \
    --compile-db <compile_db> --src <file> --format lines)

{baseDir}/tools/emit_ir.sh --src <file> \
  --out /tmp/zeroize-audit/<tu_hash>.O0.ll --opt O0 -- "${FLAGS[@]}"

{baseDir}/tools/emit_ir.sh --src <file> \
  --out /tmp/zeroize-audit/<tu_hash>.O1.ll --opt O1 -- "${FLAGS[@]}"

{baseDir}/tools/emit_ir.sh --src <file> \
  --out /tmp/zeroize-audit/<tu_hash>.O2.ll --opt O2 -- "${FLAGS[@]}"

{baseDir}/tools/diff_ir.sh \
  /tmp/zeroize-audit/<tu_hash>.O0.ll \
  /tmp/zeroize-audit/<tu_hash>.O1.ll \
  /tmp/zeroize-audit/<tu_hash>.O2.ll
```

Use `<tu_hash>` (a hash of the source path) to avoid collisions when processing multiple TUs.
`diff_ir.sh` outputs a unified diff to stdout; a non-zero exit code means divergence was detected.
Clean up `/tmp/zeroize-audit/` on completion or failure.

**Interpretation:**
- Wipe present at O0, absent at O1 → simple dead-store elimination. Flag `OPTIMIZED_AWAY_ZEROIZE`.
- Wipe present at O1, absent at O2 → aggressive optimization. Flag `OPTIMIZED_AWAY_ZEROIZE`.
- Include the IR diff as mandatory evidence in the finding.

Key IR patterns: `store volatile i8 0` is the primary wipe signal; its absence at O2 when present at O0 is DSE. `@llvm.memset` without the volatile flag is elidable. `alloca` with `@llvm.lifetime.end` and no `store volatile` in the same function indicates stack retention.

### Step 8 — Assembly Analysis (produces `STACK_RETENTION`, `REGISTER_SPILL`)

Skip if `enable_asm=false`.

```bash
{baseDir}/tools/emit_asm.sh --src <file> \
  --out /tmp/zeroize-audit/<tu_hash>.O2.s --opt O2 -- "${FLAGS[@]}"

{baseDir}/tools/analyze_asm.sh \
  --asm /tmp/zeroize-audit/<tu_hash>.O2.s \
  --out /tmp/zeroize-audit/<tu_hash>.asm-analysis.json
```

`analyze_asm.sh` outputs annotated findings to stdout.

Check for:
- **Register spills**: `movq`/`movdqa` of secret values to stack offsets → flag `REGISTER_SPILL`.
- **Callee-saved registers**: `rbx`, `r12`–`r15` (x86-64) pushed to stack containing secret values → flag `REGISTER_SPILL`.
- **Stack retention**: stack frame size and whether secret bytes are cleared before `ret` → flag `STACK_RETENTION`.

Include the relevant assembly excerpt as mandatory evidence.

### Step 9 — Semantic IR Analysis (produces `LOOP_UNROLLED_INCOMPLETE`)

Skip if `enable_semantic_ir=false`.

Parse LLVM IR structurally (do not use regex on raw IR text):
- Build function and basic block representations.
- Track memory operations in SSA form after the `mem2reg` pass.
- Detect loop-unrolled zeroization: 4 or more consecutive zero stores.
- Verify unrolled stores target the correct addresses and cover the full object size.
- Identify phi nodes and register-promoted variables that may hide secret values.

Flag `LOOP_UNROLLED_INCOMPLETE` when unrolling is detected but does not cover the full object.

### Step 10 — Control-Flow Graph Analysis (produces `MISSING_ON_ERROR_PATH`, `NOT_DOMINATING_EXITS`)

Skip if `enable_cfg=false`.

Build a CFG from source or LLVM IR:
- Enumerate all execution paths from function entry to exits.
- Compute dominator sets for all nodes.
- Verify that a wipe node dominates all exit nodes. If not, flag `NOT_DOMINATING_EXITS`.
- Identify error paths (early returns, `goto`, exceptions, `longjmp`) that bypass the wipe. Flag `MISSING_ON_ERROR_PATH` for each such path.

This step produces definitive results replacing the heuristic `NOT_ON_ALL_PATHS` finding from Step 5. If both are emitted for the same object, keep only the CFG-backed finding.

### Step 11 — Runtime Validation Test Generation

Skip if `enable_runtime_tests=false`.

For each confirmed finding, generate:
- A C test harness that allocates the sensitive object and verifies all bytes are zero after the expected wipe point.
- A MemorySanitizer test (`-fsanitize=memory`) to detect reads of uninitialized or un-zeroed memory.
- A Valgrind invocation target for leak and memory error detection.
- A stack canary test to detect stack retention after function return.

Output a `Makefile` in `{baseDir}/generated_tests/` that builds and runs all tests with appropriate sanitizer flags.

### Step 12 — PoC Generation (mandatory)

Generate proof-of-concept C programs for all findings regardless of confidence. Each PoC exits 0 (exploitable) or 1 (not exploitable):

```bash
python {baseDir}/tools/generate_poc.py \
  --findings <findings_json> \
  --compile-db <compile_db> \
  --out <poc_output_dir> \
  --categories <poc_categories> \
  --config <config> \
  --no-confidence-filter
```

After generation, review PoCs for `// TODO` comments and fill them in using source context. Compilation and validation are handled by the orchestrator in Phase 5 (interactive).

Key PoC strategies: `OPTIMIZED_AWAY_ZEROIZE` — compile with and without `-O2`, compare memory dumps; `STACK_RETENTION` — call the target function, read stack memory after return; `MISSING_SOURCE_ZEROIZE` — verify bytes are non-zero at function exit. C/C++ findings support all categories. Rust findings support `MISSING_SOURCE_ZEROIZE`, `SECRET_COPY`, and `PARTIAL_WIPE` via `cargo test`; all other Rust categories are marked `poc_supported: false`.

---

## Reference: Ir Analysis

# LLVM IR Analysis for Zeroization Auditing

This reference covers multi-level IR analysis for detecting compiler-optimized zeroization (dead-store elimination of wipes) and interpreting results. Read this during Step 7 (IR comparison) and Step 9 (semantic IR analysis) in `task.md`. For flag extraction and pipeline setup, refer to the compile-commands reference (loaded separately from SKILL.md).

---

## Optimization Level Semantics

| Level | What changes | Relevance to zeroization |
|---|---|---|
| **O0** | No optimization. All stores kept. | Baseline — wipe always present if written in source |
| **O1** | Basic optimizations. Simple dead-store elimination begins. | Diagnostic level: if wipe vanishes here, it's simple DSE. Fix is straightforward. |
| **O2** | Full DSE, inlining, SROA, alias analysis. | Most production builds. Most non-volatile wipes removed here. |
| **O3** | Aggressive vectorization, loop transforms, more inlining. | Rarely removes more wipes than O2, but can for loop-based wipes. |
| **Os/Oz** | Size-optimized. May collapse wipe loops into `memset`. | Verify wipe survives after size optimization; collapsed `memset` may become DSE-vulnerable. |

**Always include O0 as the unoptimized baseline**, regardless of the `opt_levels` input. O1 is the diagnostic level — if the wipe disappears there, the cause is simple DSE and the fix is straightforward. If the wipe only disappears at O2 or O3, proceed to the multi-level root cause analysis below.

---

## Emitting IR at Multiple Levels

Extract flags once, then emit IR for each level in `opt_levels`. Use `<tu_hash>` (a hash of the source path) to avoid collisions during parallel TU processing. Always clean up temp files on completion or failure.

```bash
mkdir -p /tmp/zeroize-audit/

FLAGS=()
while IFS= read -r flag; do FLAGS+=("$flag"); done < <(
  python {baseDir}/tools/extract_compile_flags.py \
    --compile-db build/compile_commands.json \
    --src src/crypto.c --format lines)

# Emit IR for each level in opt_levels (O0 always included as baseline)
for OPT in O0 O1 O2; do
  {baseDir}/tools/emit_ir.sh \
    --src src/crypto.c \
    --out /tmp/zeroize-audit/<tu_hash>.${OPT}.ll \
    --opt ${OPT} -- "${FLAGS[@]}"
done

# Diff all levels — prints pairwise diffs and a WIPE PATTERN SUMMARY
{baseDir}/tools/diff_ir.sh \
  /tmp/zeroize-audit/<tu_hash>.O0.ll \
  /tmp/zeroize-audit/<tu_hash>.O1.ll \
  /tmp/zeroize-audit/<tu_hash>.O2.ll

# Cleanup
rm -f /tmp/zeroize-audit/<tu_hash>.*.ll
```

For Rust TUs, `emit_ir.sh` does not apply. Use `cargo rustc -- --emit=llvm-ir -C opt-level=N` instead and pass the resulting `.ll` files directly to `diff_ir.sh`. Use `bear -- cargo build` to generate `compile_commands.json` for Rust projects.

---

## LLVM IR Zeroization Patterns

### DSE-safe patterns (survive optimization)

These indicate a secure wipe the compiler cannot remove.

**Volatile memset intrinsic** — the `i1 true` (volatile) flag prevents DSE:
```llvm
call void @llvm.memset.p0i8.i64(i8* volatile %ptr, i8 0, i64 32, i1 true)
```

**Volatile zero stores** — volatile side effects must be preserved:
```llvm
store volatile i8 0, i8* %ptr, align 1
store volatile i64 0, i64* %ptr, align 8
```

**Opaque wipe function calls** — DSE cannot remove calls to external functions with unknown side effects:
```llvm
call void @explicit_bzero(i8* %key, i64 32)
call void @sodium_memzero(i8* %key, i64 32)
call void @OPENSSL_cleanse(i8* %key, i64 32)
call void @SecureZeroMemory(i8* %key, i64 32)
```

**`memset_s`** — defined by C11 to be non-optimizable:
```llvm
call i32 @memset_s(i8* %key, i64 32, i32 0, i64 32)
```

**Rust `zeroize` crate** — emits volatile stores via the `Zeroize` trait; look for:
```llvm
store volatile i8 0, i8* %ptr, align 1   ; repeated per byte, or as unrolled loop
```

---

### DSE-vulnerable patterns (may be removed at O1 or O2)

**Non-volatile memset intrinsic** — `i1 false` is the most common `OPTIMIZED_AWAY_ZEROIZE` pattern:
```llvm
call void @llvm.memset.p0i8.i64(i8* %ptr, i8 0, i64 32, i1 false)
```

**Non-volatile zero stores** — any non-volatile store to a dead location is DSE-eligible:
```llvm
store i8 0, i8* %ptr, align 1
store i64 0, i64* %ptr, align 8
store i32 0, i32* %ptr, align 4
```

**Standard `memset` inlined to non-volatile intrinsic** — `memset(key, 0, 32)` in source is lowered by Clang to `@llvm.memset ... i1 false`. The source used `memset` but the IR form is DSE-vulnerable. This is the most frequent source of confusion.

---

## Reading an IR Diff: Concrete Before/After Example

**Source (C):**
```c
void handle_request(uint8_t session_key[32]) {
    // ... use session_key ...
    memset(session_key, 0, 32);  // intended cleanup
}
```

**O0 IR — wipe present:**
```llvm
define void @handle_request(i8* %session_key) {
entry:
  ; ... computation uses session_key ...
  call void @llvm.memset.p0i8.i64(i8* %session_key, i8 0, i64 32, i1 false)
  ret void
}
```

**O2 IR — wipe removed by DSE:**
```llvm
define void @handle_request(i8* %session_key) {
entry:
  ; ... computation ...
  ; llvm.memset REMOVED — no read from session_key after the store;
  ; optimizer treats it as a dead store and eliminates it.
  ret void
}
```

**`diff_ir.sh` output:**
```
=== DIFF: O0.ll vs O2.ll ===
-  call void @llvm.memset.p0i8.i64(i8* %session_key, i8 0, i64 32, i1 false)

=== WIPE PATTERN SUMMARY ===
O0.ll: WIPE PRESENT
O1.ll: WIPE PRESENT
O2.ll: WIPE ABSENT  <-- first disappearance
```

Lines starting with `-` are present in the lower-opt file but absent in the higher-opt file. A `-` line containing any of the following tokens is direct evidence of `OPTIMIZED_AWAY_ZEROIZE`:

`llvm.memset`, `store i8 0`, `store i64 0`, `store i32 0`, `@explicit_bzero`, `@sodium_memzero`, `@OPENSSL_cleanse`, `@SecureZeroMemory`

---

## Multi-Level Root Cause Analysis

The level at which the wipe first disappears narrows the root cause and determines the appropriate fix:

```
O0 → WIPE PRESENT   (baseline — wipe was written in source)
O1 → WIPE ABSENT    → Simple dead-store elimination (basic DSE pass)
                       Fix: replace memset with explicit_bzero or volatile wipe loop
O2 → WIPE ABSENT    → One or more of:
(first disappearance)    • DSE + inlining: wipe is in a helper inlined into caller,
                           becomes dead store in caller's context
                         • SROA: struct/array promoted to scalars; individual
                           zero stores become DSE-eligible
                         • Alias analysis: proves no live uses after the wipe
                       Fix: use explicit_bzero; ensure wipe is not inside
                       an inlined callee (see Inlining section below)
O3 → WIPE ABSENT    → Aggressive loop transforms or vectorization eliminated
(only here)            a loop-based wipe
                       Fix: replace wipe loop with explicit_bzero or volatile loop
```

If the wipe disappears at O1, a simple `explicit_bzero` or `volatile` qualifier is sufficient. If it only disappears at O2 due to inlining, also ensure the wipe is not inside a callee that gets inlined at the call site.

---

## Advanced IR Analysis Scenarios

### Inlining and cross-function DSE

When a cleanup wrapper (e.g., `zeroize_key()`) is inlined into a caller, the wipe may become a dead store in the caller's context even if it survives in the callee's IR. Always emit IR for the **calling** TU — this is where inlining occurs:

```bash
# zeroize_key() defined in utils.c, called from crypto.c
# Emit IR for the caller — inlining happens here:
FLAGS=()
while IFS= read -r flag; do FLAGS+=("$flag"); done < <(
  python {baseDir}/tools/extract_compile_flags.py \
    --compile-db build/compile_commands.json --src src/crypto.c --format lines)

{baseDir}/tools/emit_ir.sh \
  --src src/crypto.c \
  --out /tmp/zeroize-audit/<tu_hash>.O2.ll --opt O2 -- "${FLAGS[@]}"
```

If the wipe is present in `utils.c` IR but absent in `crypto.c` IR at O2, the cause is cross-function DSE after inlining. Mark the `OPTIMIZED_AWAY_ZEROIZE` finding on the call site in `crypto.c`, not on `utils.c`.

### SROA (Scalar Replacement of Aggregates)

At O1+, SROA promotes small structs and arrays to individual scalar SSA values (registers). A `memset` of a struct may become a series of individual `store i32 0` / `store i8 0` instructions per field — each then eligible for DSE independently. In the diff, look for:
- O0: single `llvm.memset` covering the struct
- O1/O2: the `memset` is replaced by per-field zero stores, then those stores are removed

This means the wipe may partially survive SROA (some fields zeroed, others eliminated). Check that **all** fields of a sensitive struct are covered, not just the first.

### Loop unrolling of wipe loops

A manual wipe loop:
```c
for (int i = 0; i < 32; i++) key[i] = 0;
```
may be unrolled at O2 into 32 consecutive `store i8 0` instructions. If unrolling is incomplete (e.g., only 16 of 32 iterations unrolled and the remainder is a DSE-eligible tail), flag `LOOP_UNROLLED_INCOMPLETE`. Use `{baseDir}/tools/analyze_ir_semantic.py` for automated detection — do not use regex on raw IR text. The semantic tool builds a proper basic block representation and counts consecutive zero stores with address verification.

### Phi nodes and register-promoted secrets

After `mem2reg`, secret values that were stack-allocated may be promoted to SSA values tracked through phi nodes. A wipe of the original stack slot may not reach all SSA uses. Look for:
```llvm
%key.0 = phi i64 [ %loaded_key, %entry ], [ 0, %cleanup ]
```
If `%key.0` is used after the phi but the `0` arm is only reached on one path, the secret may persist in the non-zero arm. Flag as `NOT_DOMINATING_EXITS` if CFG analysis confirms it.

---

## Populating `compiler_evidence` in the Report

For each `OPTIMIZED_AWAY_ZEROIZE` finding, populate the output schema fields as follows. `OPTIMIZED_AWAY_ZEROIZE` is **never valid without IR diff evidence** — do not emit this finding from source-level analysis alone.

```json
{
  "category": "OPTIMIZED_AWAY_ZEROIZE",
  "compiler_evidence": {
    "opt_levels": ["O0", "O1", "O2"],
    "o0": "call void @llvm.memset.p0i8.i64(i8* %session_key, i8 0, i64 32, i1 false) present at line 88.",
    "o1": "WIPE PRESENT at O1.",
    "o2": "llvm.memset call absent at O2 — dead store eliminated after SROA promotes session_key to registers.",
    "diff_summary": "Wipe first disappears at O2. Non-volatile memset(session_key, 0, 32) eliminated by DSE after SROA. Fix: replace memset with explicit_bzero."
  }
}
```

Field usage notes:
- `opt_levels`: list every level that was emitted, not just the levels where the wipe changed.
- `o0` through `o2` (and `o1`, `o3` if analyzed): state explicitly whether the wipe is PRESENT or ABSENT at each level, with a short IR excerpt if present.
- If the wipe only disappears at O3 but is present at O2: set `o2` to `"WIPE PRESENT at O2"` and document the O3 removal in `diff_summary`.
- `diff_summary`: always identify the first disappearance level and the most likely optimization pass responsible (DSE, inlining, SROA, alias analysis, loop transform).

---

## Reference: Mcp Analysis

# MCP-Assisted Semantic Analysis

This reference covers how to configure, query, and interpret Serena MCP evidence during the zeroize-audit semantic pass. For compile DB generation and flag extraction, refer to the compile-commands reference (loaded separately from SKILL.md).

---

## Preconditions

Before running any MCP queries, the following must hold. These are verified during Step 1 (Preflight) in `task.md` — do not re-run preflight here, just confirm the relevant outputs:

| Precondition | Failure behavior |
|---|---|
| `compile_commands.json` valid and readable | Do not run MCP queries; fail the run if `mcp_mode=require` |
| Codebase buildable from compile DB commands | Same as above |
| `check_mcp.sh` exits 0 | If `mcp_mode=require`: stop run. If `mcp_mode=prefer`: set `mcp_available=false`, continue without MCP, apply confidence downgrades |
| Serena can resolve at least one symbol in the TU | Log a warning; proceed but mark findings from that TU as `needs_review` |

**Rust note**: Cargo does not natively produce `compile_commands.json`. Use `bear -- cargo build` or `bear -- cargo check` to generate it. `rust-project.json` is not a substitute in this workflow.

---

## Configuring Serena

The `plugin.json` registers Serena as the `serena` MCP server, launched via `uvx`. Serena wraps language servers (clangd for C/C++) and exposes semantic analysis as high-level MCP tools. It auto-discovers `compile_commands.json` from the project working directory.

**Prerequisites:**
- `uvx` must be on PATH (installed with `uv` — see https://docs.astral.sh/uv/)
- Serena is fetched and run automatically via `uvx --from git+https://github.com/oraios/serena`
- No separate `clangd` installation is required — Serena manages language server dependencies internally

**Verify before querying:**

```bash
{baseDir}/tools/mcp/check_mcp.sh \
  --compile-db /path/to/compile_commands.json
```

A non-zero exit means MCP is unreachable. Apply the preflight failure behavior above.

---

## MCP Tool Reference

Serena abstracts LSP methods into higher-level, symbol-name-based tools. Unlike raw LSP, you query by symbol name rather than file position.

| MCP tool name | Purpose in zeroize-audit | Key parameters |
|---|---|---|
| `activate_project` | **Must be called first.** Activates the project so Serena indexes it | `project` (path to repo root) |
| `find_symbol` | Resolve where a sensitive symbol is defined; get type info, body, and struct layout | `symbol_name`, `file_path` (optional), `include_body`, `depth` |
| `find_referencing_symbols` | Find all use sites and callers across files | `symbol_name`, `file_path` (optional) |
| `get_symbols_overview` | List all symbols in a file — useful for exploring unfamiliar TUs | `file_path` |

**Mapping from previous LSP-based queries:**

| Analysis need | Serena tool | Notes |
|---|---|---|
| Resolve definition | `find_symbol` | Search by name; returns file, line, kind, and optionally body |
| Find all references | `find_referencing_symbols` | Returns referencing symbols with file and line |
| Find callers (incoming calls) | `find_referencing_symbols` | Search for references to a function name |
| Find callees (outgoing calls) | `find_symbol` + source read | Get function body via `include_body: true`, then resolve called symbols |
| Resolve type / hover | `find_symbol` with `include_body: true` | Type information is included in the symbol result |
| Follow typedef chain | `find_symbol` | Look up the type name directly |

---

## Query Order

Run queries in this order so each step's output informs the next. All queries for a given TU should complete before moving to the next TU.

### Step 0 — Activate the project (`activate_project`)

This **must** be called once before any other Serena tool. Pass the repository root path. If activation fails, treat MCP as unavailable.

```
Tool: activate_project
Arguments:
  project: "/path/to/repo"
```

Expected: confirmation that the project is active. Serena will start indexing the codebase (including launching clangd if needed). Wait for activation to succeed before proceeding.

### Step 1 — Resolve symbol definition (`find_symbol`)

Establishes the canonical declaration location and type information used in all subsequent queries.

```
Tool: find_symbol
Arguments:
  symbol_name: "secret_key"
  include_body: true
```

Expected: result with `file`, `line`, `kind`, `symbol` name, and body content. The body provides type information (array sizes, struct layout) needed for wipe-size validation in Step 3. Store this as the canonical location for Steps 2–4.

If the symbol name is ambiguous, narrow with `file_path`:

```
Tool: find_symbol
Arguments:
  symbol_name: "secret_key"
  file_path: "src/crypto.c"
  include_body: true
```

### Step 2 — Collect all use sites (`find_referencing_symbols`)

Finds every location where the sensitive symbol is referenced. Use these to locate adjacent wipe calls and detect copies to other scopes.

```
Tool: find_referencing_symbols
Arguments:
  symbol_name: "secret_key"
```

Expected: list of referencing symbols with `file`, `line`, `symbol`, and `kind`. For each reference in a file other than the source TU, check that file for cleanup. References in generated files (build directory) can be filtered by source directory prefix.

### Step 3 — Resolve type and size

Type information is returned as part of `find_symbol` results (Step 1). If you need to resolve a typedef or follow a type alias chain, look up the type name directly:

```
Tool: find_symbol
Arguments:
  symbol_name: "secret_key_t"
  include_body: true
```

Use this to validate wipe sizes — a `sizeof(ptr)` bug will be apparent when the symbol body reveals `uint8_t [32]` but the wipe uses `sizeof(uint8_t *)`.

### Step 4 — Trace callers and cleanup paths

Use `find_referencing_symbols` on the function containing the sensitive object to find callers that may hold their own copy of the secret. Use it on wipe wrapper functions to find cleanup paths.

```
Tool: find_referencing_symbols
Arguments:
  symbol_name: "process_key"
```

For outgoing calls (what does this function call?), read the function body from `find_symbol` output and resolve each called function:

```
Tool: find_symbol
Arguments:
  symbol_name: "process_key"
  include_body: true
```

Then for each function called within the body:

```
Tool: find_symbol
Arguments:
  symbol_name: "cleanup_secret"
```

### Step 5 — Normalize output

Before using any MCP results in confidence scoring or finding emission, normalize:

```bash
python {baseDir}/tools/mcp/normalize_mcp_evidence.py \
  --input /tmp/raw_mcp_results.json \
  --output /tmp/normalized_mcp_results.json
```

The normalizer produces a consistent schema consumed by the MCP semantic pass and subsequent confidence gating steps.

---

## Interpreting Responses

| Response | Meaning | Action |
|---|---|---|
| Empty results | Serena could not resolve the symbol | Check compile DB path; verify symbol name spelling; retry with `file_path` to narrow scope |
| Timeout (> `mcp_timeout_ms`) | Query too slow | Mark finding as `needs_review`; do not wait indefinitely |
| Multiple results for same name | Symbol is defined in multiple TUs or headers | Use `file_path` to disambiguate; note in evidence |
| References in generated files | Hits in build-generated sources | Filter by source directory prefix |
| No referencing symbols found | Symbol is unused or not indexed | Acceptable for leaf functions; note in evidence |

---

## Confidence Scoring

MCP evidence contributes one signal toward the 2-signal threshold for `confirmed` findings (see SKILL.md Confidence Gating). Tag each piece of evidence with its source:

| Evidence source tag | Meaning |
|---|---|
| `mcp` | Resolved via Serena MCP query |
| `source` | Source-level pattern match |
| `ir` | LLVM IR analysis |
| `asm` | Assembly analysis |
| `cfg` | Control-flow graph analysis |

MCP evidence alone (1 signal) produces `likely`. MCP + one additional signal (source, IR, CFG, or ASM) produces `confirmed`.

**Mandatory downgrades** — applied by `apply_confidence_gates.py` after all evidence is collected:

| Condition | Findings downgraded to `needs_review` |
|---|---|
| `mcp_available=false` AND `mcp_required_for_advanced=true` | `SECRET_COPY`, `MISSING_ON_ERROR_PATH`, `NOT_DOMINATING_EXITS` (unless 2+ non-MCP signals exist) |
| Assembly evidence missing | `STACK_RETENTION`, `REGISTER_SPILL` |
| IR diff evidence missing | `OPTIMIZED_AWAY_ZEROIZE` |

Apply downgrades after all evidence is collected, not during querying. Do not suppress findings preemptively — emit at `needs_review` rather than dropping them.

---

## Post-Processing

After collecting all MCP evidence and running IR/ASM/CFG analysis, apply confidence gates mechanically:

```bash
python {baseDir}/tools/mcp/apply_confidence_gates.py \
  --input /tmp/raw-report.json \
  --out /tmp/final-report.json \
  --mcp-available \
  --mcp-required-for-advanced
```

Omit `--mcp-available` if MCP was unreachable. Omit `--mcp-required-for-advanced` if `mcp_required_for_advanced=false` in the run config. The script applies all downgrade rules from SKILL.md and outputs gated findings ready for the report assembly phase.

---

## Reference: Poc Generation

# PoC Crafting Reference

## Overview

Each zeroize-audit finding is demonstrated with a bespoke proof-of-concept program
crafted from the finding details and the actual source code. PoCs are individually
written, not generated from templates — they use the real function signatures,
variable names, types, and sizes from the audited codebase. Each PoC exits 0 if the
secret persists (exploitable) or 1 if the data was properly wiped (not exploitable).

## Exit Code Convention

| Exit code | Meaning |
|-----------|---------|
| 0 | Secret persists after the operation — finding is exploitable |
| 1 | Secret was wiped — finding is not exploitable in this configuration |

The `POC_PASS()` and `POC_FAIL()` macros in `poc_common.h` enforce this convention.

## Common Techniques

### Volatile Reads

The core verification technique is reading through a `volatile` pointer after the
function under test returns. This prevents the compiler from optimizing away the
read, ensuring we observe the actual memory state:

```c
static int volatile_read_nonzero(const void *ptr, size_t len) {
    const volatile unsigned char *p = (const volatile unsigned char *)ptr;
    int found = 0;
    for (size_t i = 0; i < len; i++) {
        if (p[i] != 0) found = 1;
    }
    return found;
}
```

### Stack Probing

For `STACK_RETENTION` and `REGISTER_SPILL` findings, the PoC calls the target
function then immediately calls `stack_probe()` — a `noinline`/`noclone` function
that reads uninitialized local variables to detect whether the prior call frame left
secret data on the stack:

```c
__attribute__((noinline, noclone))
static int stack_probe(size_t frame_size) {
    volatile unsigned char probe[STACK_PROBE_MAX];
    /* Read uninitialized stack — check for secret fill pattern */
    int count = 0;
    for (size_t i = 0; i < frame_size; i++) {
        if (probe[i] == SECRET_FILL_BYTE) count++;
    }
    return count >= (int)(frame_size / 4);
}
```

### Source Inclusion

For static functions and small files (<=5000 lines by default), PoCs include the
source file directly via `#include "../../src/crypto.c"`. This handles both static
and extern functions without requiring separate compilation. For large files with
non-static functions, the Makefile uses object-file linking instead.

### Secret Fill Pattern

Buffers are initialized with `0xAA` (configurable via `secret_fill_byte` in config)
before calling the target function. After the call, the PoC checks whether the fill
pattern persists — indicating the secret was not wiped.

## Per-Category Strategies

### MISSING_SOURCE_ZEROIZE

**Opt level:** `-O0`
**Technique:** Call the function that handles the secret, then volatile-read the
buffer after it returns. At `-O0` there are no optimization passes that could
accidentally wipe the buffer, so if the secret persists, it confirms the source
code lacks a wipe call.

**Crafting guidance:**
- Read the function signature and determine minimal valid arguments
- Identify the exact sensitive variable from the finding — use its real name and type
- If the function takes the sensitive buffer as a parameter, allocate it in `main()`,
  fill with `SECRET_FILL_BYTE`, pass it to the function, then check after return
- If the sensitive variable is a local, include the source file and examine the buffer
  via a global pointer or by modifying the function to expose it

**Pitfalls:**
- The buffer must be the actual sensitive variable, not a local copy
- Stack-allocated secrets may be overwritten by subsequent function calls even
  without explicit zeroization — run immediately after the function returns

### OPTIMIZED_AWAY_ZEROIZE

**Opt level:** The level where the wipe disappears (from `compiler_evidence.diff_summary`)
**Technique:** Same as `MISSING_SOURCE_ZEROIZE`, but compiled at the optimization
level where the compiler removes the wipe. The finding's `compiler_evidence` field
indicates which level this is (typically `-O1` for simple DSE, `-O2` for aggressive
optimization).

**Crafting guidance:**
- Read the `compiler_evidence.diff_summary` to determine the exact optimization level
- The wipe IS present at `-O0` — compiling the PoC at `-O0` will show "not exploitable"
  which would be misleading. Always use the opt level from the evidence.
- Include the source file to ensure the compiler can apply the same optimizations

**Pitfalls:**
- The opt level must match what `diff_ir.sh` reported — compiling at a different
  level may give false negatives
- LTO can change behavior; PoCs use single-TU compilation by default

### STACK_RETENTION

**Opt level:** `-O2`
**Technique:** Call the function, then immediately call `stack_probe()` with a
frame size matching the target function's stack allocation. The probe reads
uninitialized locals that overlap the prior call frame.

**Crafting guidance:**
- Extract the stack frame size from the ASM evidence in the finding
- The probe function MUST be called immediately after the target function returns,
  with no intervening function calls that could overwrite the stack
- Use `noinline` and `noclone` on the probe to prevent frame reuse

**Pitfalls:**
- Stack layout varies between compiler versions and optimization levels
- The probe function must be `noinline` to prevent the compiler from reusing
  the same frame
- Frame size is estimated from ASM evidence; verify against the actual assembly
- Address Space Layout Randomization (ASLR) does not affect stack frame reuse
  within a single thread

### REGISTER_SPILL

**Opt level:** `-O2`
**Technique:** Similar to stack retention, but targets the specific stack offset
where the register spill occurs (extracted from the ASM evidence showing
`movq %reg, -N(%rsp)`).

**Crafting guidance:**
- Extract the exact spill offset from the finding's ASM evidence
- Target the probe at that specific region of the stack
- The same `noinline` probe approach applies

**Pitfalls:**
- Spill offsets are compiler-specific and may change with minor code changes
- Different register allocation strategies produce different spill patterns
- The probe must target the exact offset region to be reliable

### SECRET_COPY

**Opt level:** `-O0`
**Technique:** Call the function that copies the secret, verify the original may
be wiped, then volatile-read the copy destination to confirm the copy persists
without zeroization.

**Crafting guidance:**
- Identify the copy destination from the source code: `memcpy` target, struct
  assignment LHS, return value receiver, or pass-by-value parameter
- The PoC must check the COPY, not the original — the original may be wiped
- If the copy is to a struct field, allocate the struct and check that specific field

**Pitfalls:**
- The copy destination must be identified from the source code
- Multiple copies may exist; each needs separate verification

### MISSING_ON_ERROR_PATH

**Opt level:** `-O0`
**Technique:** Force the error path by providing controlled inputs that trigger
the error return, then volatile-read the secret buffer to confirm it was not
wiped before the error exit.

**Crafting guidance:**
- Read the source code to understand what conditions trigger the error return
- Common error triggers: NULL pointer arguments, invalid key sizes, allocation
  failure (can use `malloc` interposition), invalid magic numbers
- After the function returns with an error code, check both the return value
  (to confirm the error path was taken) AND the secret buffer (to confirm it persists)
- Comment the choice of error-triggering input with a reference to the source line

**Pitfalls:**
- Triggering the error path may require domain knowledge (invalid keys, NULL
  pointers, allocation failures)
- Some error paths involve signals or `longjmp` that are hard to trigger from
  a simple test harness
- Error codes must be checked to confirm the error path was actually taken

### PARTIAL_WIPE

**Opt level:** `-O0`
**Technique:** Fill the full buffer with the secret fill pattern, call the function,
then volatile-read the *tail* beyond the incorrectly-sized wipe region. If the
function wipes only N bytes of an M-byte object (N < M), the tail
`buf[N..M]` still contains the secret.

**Crafting guidance:**
- Extract the wiped size and full object size from the finding evidence
- The PoC must check `buf[wiped_size .. full_size]`, not the entire buffer
- If both sizes are uncertain, read the source to verify `sizeof()` calls

**Pitfalls:**
- The wiped vs. full sizes must be verified against source
- At `-O0` the compiler won't add extra zeroing, so this is a pure source-level bug
- Struct padding may cause false positives if the wipe intentionally skips padding

### NOT_ON_ALL_PATHS

**Opt level:** `-O0`
**Technique:** Force execution down the control-flow path that lacks the wipe,
then volatile-read the secret buffer. This is structurally identical to
`MISSING_ON_ERROR_PATH` but covers *any* uncovered path, not just error paths.

**Crafting guidance:**
- Read the function's control flow to identify which branch lacks the wipe
- Determine what input values force execution through that branch
- Comment the input choice and reference the specific branch condition

**Pitfalls:**
- Requires understanding the function's branching logic
- The heuristic finding from source analysis may be superseded by CFG-backed
  `NOT_DOMINATING_EXITS` — check for duplicates
- Multiple uncovered paths may exist; the PoC demonstrates only one

### INSECURE_HEAP_ALLOC

**Opt level:** `-O0`
**Technique:** Demonstrate heap residue using the `heap_residue_check()` helper:
allocate with `malloc()`, fill with secret, free, re-allocate the same size,
then check if the secret persists in the new allocation. This proves that
standard allocators do not scrub freed memory.

**Crafting guidance:**
- Use the exact allocation size from the finding
- For a function-specific proof, call the target function (which does the
  malloc/use/free), then immediately malloc the same size and check
- Add a comment explaining that this demonstrates the general vulnerability

**Pitfalls:**
- Do **not** compile with AddressSanitizer (`-fsanitize=address`) — ASan poisons
  freed memory, hiding the vulnerability
- Heap allocator behavior varies: glibc `malloc` reuses freed chunks predictably,
  but jemalloc or tcmalloc may not — the PoC may give false negatives on
  non-standard allocators
- The PoC demonstrates the general vulnerability; for function-level proof,
  call the actual target function

### LOOP_UNROLLED_INCOMPLETE

**Opt level:** `-O2`
**Technique:** Like `PARTIAL_WIPE` but compiled at `-O2` where incomplete loop
unrolling occurs. The compiler unrolls the wipe loop for N bytes but the object
is M bytes (N < M). Fill the buffer, call the function, check the tail beyond
the unrolled region.

**Crafting guidance:**
- Extract the covered bytes and object size from the IR semantic analysis evidence
- Compile at `-O2` — at `-O0` the loop executes correctly
- Check `buf[covered_bytes .. object_size]`

**Pitfalls:**
- Must compile at `-O2` (or the level where unrolling occurs) — at `-O0` the
  loop executes correctly
- Covered bytes and object size are extracted from IR semantic analysis evidence;
  if the IR evidence is unavailable, values may be inaccurate
- Different compilers (GCC vs. Clang) and versions unroll differently; the PoC
  is compiler-specific

### NOT_DOMINATING_EXITS

**Opt level:** `-O0`
**Technique:** Force execution through an exit path that bypasses the wipe, as
identified by CFG dominator analysis. The wipe node does not dominate all exit
nodes, meaning some return paths leave the secret in memory.

**Crafting guidance:**
- Read the finding evidence to identify which exit path bypasses the wipe
- Determine what inputs reach the non-dominated exit
- Comment the input choice and reference the CFG evidence (exit line or path count)

**Pitfalls:**
- Requires understanding of the function's CFG; the finding evidence identifies
  the exit line or path count
- Similar to `NOT_ON_ALL_PATHS` but backed by CFG evidence rather than
  source-level heuristics

## Pipeline Integration

PoC crafting and validation is mandatory for every finding, regardless of
confidence level. The pipeline flow is:

1. **Phase 3 — Interim Finding Collection**: Agent 4 produces `findings.json`
   with all gated findings. No final report yet.

2. **Phase 4 — PoC Crafting**: Agent 5 reads each finding and the corresponding
   source code, then writes bespoke PoC programs. Each PoC is individually
   tailored — using real function names, variable names, types, and sizes.

3. **Phase 5 — PoC Validation & Verification**:
   - Agent 5b compiles and runs all PoCs, recording exit codes.
   - Agent 5c verifies each PoC proves its claimed finding by checking:
     target variable match, target function match, technique appropriateness,
     optimization level, exit code interpretation, and result plausibility.
   - Orchestrator presents verification failures to user via `AskUserQuestion`.
   - Orchestrator merges all results into `poc_final_results.json`.

4. **Phase 6 — Report Finalization**: Agent 4 is re-invoked in final mode.
   It merges PoC validation and verification results into findings:
   - Exit 0 + verified → `exploitable` — strong evidence, can upgrade confidence.
   - Exit 1 + verified → `not_exploitable` — downgrade severity to `low`.
   - Verified=false + user rejected → `rejected` — no confidence change.
   - Verified=false + user accepted → use result but note as weaker signal.
   - Compile failure → annotate, no confidence change.
   - Produces the final `final-report.md` with PoC validation and verification summary.

### Validation Result Mapping

| Exit Code | Compile | Verified | Result | Finding Impact |
|-----------|---------|----------|--------|---------------|
| 0 | success | yes | `exploitable` | Confirm finding; can upgrade `likely` → `confirmed` |
| 1 | success | yes | `not_exploitable` | Downgrade severity to `low` (informational) |
| 0/1 | success | no (user accepted) | original | Weaker confidence signal; note verification failure |
| 0/1 | success | no (user rejected) | `rejected` | No confidence change |
| — | failure | — | `compile_failure` | Annotate; no confidence change |
| — | — | — | `no_poc` | No PoC generated; annotate; no confidence change |

## Rust PoC Generation

Rust PoCs are enabled for three categories where a simple volatile-read after drop is sufficient to prove the vulnerability. All other categories remain excluded.

**Exit code convention (cargo test):**
- `assert!` passes → cargo exits 0 → `"exploitable"` (secret persists)
- `assert!` panics → cargo exits non-zero → `"not_exploitable"` (secret wiped)

**Verification primitive:** Use `std::ptr::read_volatile` inside `unsafe { }`. Never use the C `volatile` keyword in Rust PoCs.

**Pointer validity:** `read_volatile` after `drop()` is only safe for heap-backed data. If the sensitive type is stack-only, force heap allocation: `let boxed = Box::new(obj); let raw = boxed.as_ref().as_ptr(); drop(boxed);`. For types with `Vec`/`Box` fields, the raw pointer to the field's backing allocation remains valid after drop (the heap page is not scrubbed by the allocator).

---

### MISSING_SOURCE_ZEROIZE (Rust)

**Opt level:** debug (no `--release`)
**Technique:** Construct the sensitive type with `[0xAAu8; N]` fill. Capture a raw pointer to the backing buffer **before** drop. Drop the type (or let scope end). Volatile-read the buffer to check persistence.

```rust
#[test]
fn poc_za_NNNN_missing_source_zeroize() {
    let key = SensitiveKey::new([0xAAu8; 32]);
    let raw: *const u8 = key.as_slice().as_ptr();
    drop(key);
    let secret_persists = (0..32usize).any(|i| unsafe {
        std::ptr::read_volatile(raw.add(i)) == 0xAA
    });
    assert!(secret_persists, "Secret was wiped — not exploitable");
}
```

**Pitfalls:**
- The raw pointer must point to heap-backed storage — stack pointers become dangling after drop.
- If the type does not expose `as_slice()` or similar, use a field accessor (`key.key_bytes.as_ptr()`).
- At debug build, the compiler does not add extra zeroing — a positive result confirms the source lacks a wipe call.

---

### SECRET_COPY (Rust)

**Opt level:** debug (no `--release`)
**Technique:** Perform the identified copy operation (`.clone()`, `Copy` assignment, `From::from()`, `Debug` formatting). Drop the **original**. Volatile-read the **copy** — not the original.

```rust
#[test]
fn poc_za_NNNN_secret_copy() {
    let original = SensitiveKey::new([0xAAu8; 32]);
    let copy = original.clone();                        // or Copy assignment / From::from()
    let raw: *const u8 = copy.as_slice().as_ptr();
    drop(original);                                      // original may be wiped; copy is not
    let secret_persists = (0..32usize).any(|i| unsafe {
        std::ptr::read_volatile(raw.add(i)) == 0xAA
    });
    drop(copy);
    assert!(secret_persists, "Copy was wiped — not exploitable");
}
```

**Pitfalls:**
- Read the copy, not the original. The original may be properly wiped; the copy is the vulnerability.
- For `#[derive(Debug)]` findings: format via `format!("{:?}", &original)` and check the resulting `String` for the fill pattern bytes (hex or decimal representations of `0xAA`).
- For `From`/`Into` findings: call the conversion and check the target type's buffer.

---

### PARTIAL_WIPE (Rust)

**Opt level:** debug (no `--release`)
**Technique:** Construct the type with `[0xAAu8; full_size]` fill. Trigger drop. Volatile-read **only the tail** (`wiped_size..full_size`). The head (`0..wiped_size`) may be correctly zeroed; only the tail proves the partial wipe.

```rust
#[test]
fn poc_za_NNNN_partial_wipe() {
    // full_size = 64, wiped_size = 32 (from finding evidence)
    let obj = SensitiveStruct { key: [0xAAu8; 64], ..Default::default() };
    let raw: *const u8 = obj.key.as_ptr();
    drop(obj);
    // Only check the tail bytes beyond the wipe region
    let tail_persists = (32usize..64).any(|i| unsafe {
        std::ptr::read_volatile(raw.add(i)) == 0xAA
    });
    assert!(tail_persists, "Tail was wiped — not exploitable");
}
```

**Pitfalls:**
- Must check `buf[wiped_size..full_size]`, not the entire buffer — checking from 0 may hit correctly-wiped bytes and produce a false negative.
- Extract `wiped_size` and `full_size` from the finding evidence. Verify against `sizeof()` calls in the Drop impl.
- Struct padding may occupy bytes beyond the last field — be aware of layout differences with `#[repr(C)]` vs. default `#[repr(Rust)]`.

---

## Excluded Rust Categories

The following Rust finding categories remain `poc_supported=false`. Each requires techniques not yet implemented for Rust.

| Category | Reason |
|---|---|
| `OPTIMIZED_AWAY_ZEROIZE` | Requires compiling at `--release` and confirming the wipe existed at debug level; no PoC harness for opt-level switching |
| `STACK_RETENTION` | Stack probe requires unsafe inline assembly intrinsics; frame layout is not stable across Rust versions |
| `REGISTER_SPILL` | Register allocation in Rust depends on monomorphization; spill offsets from ASM analysis don't map reliably to test code |
| `NOT_ON_ALL_PATHS` | Requires driving async Future state machine through suspension; no implemented harness for Rust async |
| `MISSING_ON_ERROR_PATH` | Requires forcing `Result::Err` or `panic!` paths with domain knowledge of the error conditions |
| `NOT_DOMINATING_EXITS` | CFG dominator analysis results require source-level forcing of specific control-flow paths |
| `INSECURE_HEAP_ALLOC` | Rust's allocator trait system does not support the `malloc`-interposition approach used for C |
| `LOOP_UNROLLED_INCOMPLETE` | Requires `--release` compilation and extracting the covered-byte count from IR evidence |

## Limitations

1. **Stack probe is probabilistic:** Frame layout varies between compiler versions,
   optimization levels, and even minor source changes. A negative result does not
   prove the stack is clean — only that the probe did not find the fill pattern at
   the expected offset.

2. **Register spill offsets are compiler-specific:** The offset extracted from
   ASM evidence (e.g., `-48(%rsp)`) may differ when compiled on a different system
   or with a different compiler version.

3. **Error path triggers may need domain knowledge:** Determining what inputs cause
   a function to take its error path may require understanding the application's
   protocol or data format.

4. **Source inclusion may cause conflicts:** Including a `.c` file that defines
   `main()` or has conflicting global symbols will cause compilation errors. In
   these cases, use object-file linking instead.

5. **Single-TU compilation:** PoCs compile a single translation unit. Cross-TU
   optimizations (LTO) may produce different behavior in production builds.

6. **No dynamic analysis:** PoCs are static programs. They do not use sanitizers,
   Valgrind, or other runtime instrumentation (those are covered by Step 11's
   runtime test generation).

7. **Heap residue is allocator-dependent:** The `heap_residue_check()` helper
   relies on the allocator reusing a recently-freed chunk. This works reliably
   with glibc `malloc` but may produce false negatives with jemalloc, tcmalloc,
   or custom allocators. Do not compile with ASan (it poisons freed memory).

8. **Verification is heuristic:** The PoC verifier checks alignment between the
   PoC and the finding, but cannot prove that a PoC is correct in all cases.
   Suspicious results are flagged for user review.

---

## Reference: Rust Zeroization Patterns

# Rust Zeroization Patterns Reference

This reference documents vulnerability pattern detected by the zeroize-audit tooling for Rust code.
Each entry includes: what the flaw is, which tool detects it, severity, category, a minimal Rust snippet showing the bug, and a recommended fix.

---

## Section A — Semantic Patterns (`semantic_audit.py`, rustdoc JSON-based)

These patterns are detectable from rustdoc JSON without executing the compiler. `semantic_audit.py` processes trait impls, derives, and field types from the rustdoc index.

---

### A1 — `#[derive(Copy)]` on Sensitive Type

**Category**: `SECRET_COPY` | **Severity**: critical

**Why it's dangerous**: `Copy` types are bitwise-duplicated on every assignment, function call, and return. No `Drop` ever runs — the type cannot implement `Drop`. Every copy is a silent, untracked duplicate that will never be zeroed.

```rust
// BAD: every assignment silently duplicates the secret
#[derive(Copy, Clone)]
pub struct CopySecret {
    data: [u8; 32],
}

fn use_key(key: CopySecret) {  // <-- full copy here
    // original still on stack, unzeroed
}
```

**Fix**: Remove `Copy`. Use `Clone` explicitly where needed and ensure all clones are tracked and zeroed.

---

### A2 — No `Zeroize`, `ZeroizeOnDrop`, or `Drop`

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: high

**Why it's dangerous**: When the type goes out of scope, Rust calls `drop_in_place` which simply frees the memory without zeroing it. The secret bytes remain in the freed heap or on the stack until overwritten by future allocations.

```rust
// BAD: no cleanup whatsoever
pub struct UnprotectedKey {
    bytes: Vec<u8>,
}

fn example() {
    let key = UnprotectedKey { bytes: vec![0x42; 32] };
    // key drops here — heap bytes never zeroed
}
```

**Fix**: Add `#[derive(ZeroizeOnDrop)]` (with `zeroize` crate) or implement `Drop` calling `.zeroize()` on all fields.

---

### A3 — `Zeroize` Impl Without Auto-Trigger

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: high

**Why it's dangerous**: The `Zeroize` trait provides a `.zeroize()` method, but it requires explicit invocation. If no `Drop` or `ZeroizeOnDrop` calls it, the zeroing never happens automatically when the value goes out of scope.

```rust
use zeroize::Zeroize;

// BAD: Zeroize is implemented but never called on drop
pub struct ManualZeroizeToken {
    bytes: Vec<u8>,
}

impl Zeroize for ManualZeroizeToken {
    fn zeroize(&mut self) {
        self.bytes.zeroize();
    }
}

fn example() {
    let token = ManualZeroizeToken { bytes: vec![0x42; 32] };
    // token drops here — zeroize() is NEVER called
}
```

**Fix**: Add `#[derive(ZeroizeOnDrop)]` alongside `Zeroize`, or add an explicit `Drop` impl that calls `self.zeroize()`.

---

### A4 — `Drop` Impl Missing Secret Fields

**Category**: `PARTIAL_WIPE` | **Severity**: high

**Why it's dangerous**: The struct has multiple sensitive fields, but the `Drop` impl only zeroes some of them. The unzeroed fields remain in memory after the struct is freed.

```rust
// BAD: Drop impl zeroes `secret` but forgets `token`
pub struct ApiSecret {
    secret: Vec<u8>,
    token: Vec<u8>,  // <-- never zeroed
}

impl Drop for ApiSecret {
    fn drop(&mut self) {
        self.secret.zeroize();
        // self.token is NOT zeroed
    }
}
```

**Fix**: Ensure `Drop` calls `.zeroize()` on every sensitive field, or use `#[derive(ZeroizeOnDrop)]` to zero all fields automatically.

---

### A5 — `ZeroizeOnDrop` on Struct with Heap Fields

**Category**: `PARTIAL_WIPE` | **Severity**: medium

**Why it's dangerous**: `ZeroizeOnDrop` zeros all fields via the `Zeroize` implementation, but `Vec<T>` zeroes only `len` bytes, not the full allocated `capacity`. Excess capacity bytes remain readable until the allocator reclaims them.

```rust
use zeroize::ZeroizeOnDrop;

// BAD: ZeroizeOnDrop zeros len bytes but capacity tail is untouched
#[derive(ZeroizeOnDrop)]
pub struct SessionKey {
    data: Vec<u8>,
}

fn example() {
    let mut key = SessionKey { data: Vec::with_capacity(64) };
    key.data.extend_from_slice(&[0x42; 32]);
    // capacity[32..64] bytes never zeroed
}
```

**Fix**: Use `Zeroizing<Vec<u8>>` which uses `zeroize_and_drop` for the full buffer, or manually `self.data.zeroize(); self.data.shrink_to_fit()` in `Drop`.

---

### A6 — `ManuallyDrop<T>` Struct Field

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: critical

**Why it's dangerous**: `ManuallyDrop<T>` inhibits automatic drop for the wrapped value. Rust will never call `Drop` on a `ManuallyDrop<T>` field unless `ManuallyDrop::drop()` is called explicitly. If the containing struct's `Drop` impl does not explicitly drop and zero the field, the secret bytes are never wiped.

```rust
use std::mem::ManuallyDrop;

// BAD: Drop is never called on `key` field automatically
pub struct SecretHolder {
    key: ManuallyDrop<Vec<u8>>,
}

// When SecretHolder drops, `key` is NOT zeroed — bytes stay in heap
```

**Fix**: Implement `Drop` for `SecretHolder` that explicitly calls `self.key.zeroize()` (if `Vec<u8>` implements `Zeroize`) and then `unsafe { ManuallyDrop::drop(&mut self.key) }`.

---

### A7 — `#[derive(Clone)]` on Zeroizing Type

**Category**: `SECRET_COPY` | **Severity**: medium

**Why it's dangerous**: Each `clone()` call creates an independent heap allocation containing the same secret bytes. The clone must be independently zeroed. If callers pass clones to functions that don't zero them on return, the secret escapes the zeroing lifecycle.

```rust
// BAD: clone() creates an untracked duplicate that may not be zeroed
#[derive(Clone)]
pub struct CloneableKey {
    bytes: Vec<u8>,
}

impl Drop for CloneableKey {
    fn drop(&mut self) { self.bytes.zeroize(); }
}

fn bad_caller(key: &CloneableKey) {
    let copy = key.clone(); // a new heap allocation
    do_something_with(copy); // copy may not be zeroed on return from do_something_with
}
```

**Fix**: Remove `Clone` if not needed. If cloning is required, document that all clones must implement the same zeroization lifecycle.

---

### A8 — `From<T>` / `Into<T>` to Non-Zeroizing Type

**Category**: `SECRET_COPY` | **Severity**: medium

**Why it's dangerous**: A `From`/`Into` conversion transfers the secret bytes into a type that does not implement `ZeroizeOnDrop` or `Drop`. The original may be zeroed but the converted value escapes without zeroization guarantees.

```rust
type RawBytes = Vec<u8>;  // type alias — does NOT implement ZeroizeOnDrop

pub struct ApiSecret {
    secret: Vec<u8>,
    token: RawBytes,
}

// BAD: From<RawBytes> converts secret into a plain Vec with no zeroing
impl From<RawBytes> for ApiSecret {
    fn from(token: RawBytes) -> Self {
        ApiSecret { secret: vec![], token }
    }
}
// The returned ApiSecret has no Drop/Zeroize impl
```

**Fix**: Ensure the target type of `From`/`Into` also implements `ZeroizeOnDrop`, or wrap in `Zeroizing<T>`.

---

### A9 — `ptr::write_bytes` Without `compiler_fence`

**Category**: `OPTIMIZED_AWAY_ZEROIZE` | **Severity**: medium

**Why it's dangerous**: `ptr::write_bytes` is a non-volatile memory write. If the compiler determines the memory is never read afterwards (classic dead-store elimination), it may remove the write entirely. Unlike `volatile_set_memory`, there is no compiler barrier to prevent this.

```rust
use std::ptr;

pub struct WriteBytesSecret {
    data: [u8; 32],
}

fn wipe_insecure(s: &mut WriteBytesSecret) {
    // BAD: compiler may eliminate this as a dead store
    unsafe {
        ptr::write_bytes(s as *mut WriteBytesSecret, 0, 1);
    }
}
// No compiler_fence — wipe is DSE-vulnerable
```

**Fix**: Add `std::sync::atomic::compiler_fence(std::sync::atomic::Ordering::SeqCst)` after the write, or use `zeroize::Zeroize` which is DSE-resistant by design.

---

### A10 — `#[cfg(feature)]` Wrapping `Drop` or `Zeroize` Impl

**Category**: `NOT_ON_ALL_PATHS` | **Severity**: medium

**Why it's dangerous**: When the controlling feature flag is disabled, the cleanup impl is compiled out entirely. Code built without the feature silently loses all zeroization, with no compile error or warning.

```rust
pub struct CfgGuardedKey {
    secret: Vec<u8>,
}

// BAD: when feature "zeroize" is off, this impl does not exist
#[cfg(feature = "zeroize")]
impl Drop for CfgGuardedKey {
    fn drop(&mut self) {
        self.secret.zeroize();
    }
}
```

**Fix**: Make zeroization unconditional. If the `zeroize` crate is optional, gate the crate import but always zero memory manually in `Drop` using a volatile write loop as the fallback.

---

### A11 — `#[derive(Debug)]` on Sensitive Type

**Category**: `SECRET_COPY` | **Severity**: low

**Why it's dangerous**: The `Debug` trait formats all fields into a string. Any logging framework, panic handler, or `dbg!()` call will print the secret bytes in plaintext. This is a common source of credential leaks in logs.

```rust
// BAD: {key:?} or panic prints the raw bytes
#[derive(Debug)]
pub struct DebugSecret {
    secret: Vec<u8>,
}
```

**Fix**: Remove `#[derive(Debug)]`. Implement `Debug` manually to show a redacted placeholder: `write!(f, "DebugSecret([REDACTED])")`.

---

### A12 — `#[derive(Serialize)]` on Sensitive Type

**Category**: `SECRET_COPY` | **Severity**: low

**Why it's dangerous**: Serialization creates a representation of the secret in the serialization output (JSON, msgpack, etc.). If the output buffer is not itself zeroed after use, the secret bytes leak into the serialized payload.

```rust
use serde::Serialize;

// BAD: serde may write secret bytes to an uncontrolled buffer
#[derive(Serialize)]
pub struct SerializableSecret {
    secret: Vec<u8>,
}
```

**Fix**: Remove `Serialize`. If serialization is required, implement it manually to skip or encrypt sensitive fields, and ensure the output buffer is zeroed after use.

---

## Section B — Dangerous API Patterns (`find_dangerous_apis.py`, source grep-based)

These patterns are detected by scanning Rust source files for calls to APIs that prevent or bypass zeroization. Detection confidence is `"likely"` when the call appears within ±15 lines of a sensitive name, `"needs_review"` otherwise.

---

### B1 — `mem::forget(secret)`

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: critical

**Why it's dangerous**: `mem::forget` leaks the value without running its destructor. If the type has a `Drop` impl that calls `zeroize`, `mem::forget` bypasses it entirely. The heap allocation is leaked and never zeroed.

```rust
use std::mem;

struct SecretKey(Vec<u8>);
impl Drop for SecretKey { fn drop(&mut self) { self.0.zeroize(); } }

fn bad(key: SecretKey) {
    // BAD: Drop is never called — bytes leak forever
    mem::forget(key);
}
```

**Fix**: Never call `mem::forget` on values containing secrets. Use explicit zeroing before consuming the value if early release is needed.

---

### B2 — `ManuallyDrop::new(secret)` Call

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: critical

**Why it's dangerous**: Wrapping a value in `ManuallyDrop` suppresses its destructor. The secret bytes will not be zeroed when the `ManuallyDrop` wrapper is dropped unless `ManuallyDrop::drop()` is called explicitly.

```rust
use std::mem::ManuallyDrop;

struct SecretKey(Vec<u8>);
impl Drop for SecretKey { fn drop(&mut self) { self.0.zeroize(); } }

fn bad(key: SecretKey) {
    // BAD: Drop never runs for the inner SecretKey
    let _md = ManuallyDrop::new(key);
}
```

**Fix**: If `ManuallyDrop` is required for FFI or unsafe code, explicitly call `key.zeroize()` before passing into `ManuallyDrop::new`, or ensure the surrounding code calls `ManuallyDrop::drop()`.

---

### B3 — `Box::leak(secret)`

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: critical

**Why it's dangerous**: `Box::leak` produces a `'static` reference by preventing the `Box` from ever being dropped. The secret allocation persists for the entire program lifetime and is never zeroed.

```rust
struct SecretKey(Vec<u8>);

fn bad(key: SecretKey) -> &'static SecretKey {
    // BAD: key is never dropped or zeroed
    Box::leak(Box::new(key))
}
```

**Fix**: Avoid `Box::leak` for secrets. Use `Arc<SecretKey>` with proper `Drop` if shared ownership is needed, ensuring the last reference is dropped before program exit.

---

### B4 — `mem::uninitialized()`

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: critical

**Why it's dangerous**: `mem::uninitialized` returns memory with undefined contents — which in practice means prior stack or heap bytes are exposed as the return value. It is unsound (deprecated since Rust 1.39) and may expose sensitive data from prior use of that memory region.

```rust
use std::mem;

struct SecretKey([u8; 32]);

unsafe fn bad() -> SecretKey {
    // BAD: may return bytes from prior sensitive allocations
    mem::uninitialized()
}
```

**Fix**: Use `MaybeUninit<T>::zeroed().assume_init()` for zero-initialized memory, or `MaybeUninit::uninit()` only when you will fully initialize before reading.

---

### B5 — `Box::into_raw(secret)`

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: high

**Why it's dangerous**: `Box::into_raw` consumes the `Box` and returns a raw pointer, preventing the destructor from running. The caller is responsible for zeroing and deallocating, but this is often forgotten.

```rust
struct SecretKey(Vec<u8>);
impl Drop for SecretKey { fn drop(&mut self) { self.0.zeroize(); } }

fn bad(key: SecretKey) -> *mut SecretKey {
    // BAD: Drop is suppressed; raw pointer escapes
    Box::into_raw(Box::new(key))
}
```

**Fix**: If raw pointer access is required for FFI, zero the value before converting: call `key.zeroize()` (if applicable), then use `Box::into_raw`. Document the requirement for the caller to `Box::from_raw` and drop the value.

---

### B6 — `ptr::write_bytes` Without Volatile

**Category**: `OPTIMIZED_AWAY_ZEROIZE` | **Severity**: high

**Why it's dangerous**: `ptr::write_bytes` is a non-volatile write. The compiler's dead-store elimination pass can and will remove it if the memory is not read afterwards. Use of this function as a zeroization primitive is unreliable at optimization levels O1 and above.

```rust
use std::ptr;

struct SecretKey([u8; 32]);

fn wipe(key: &mut SecretKey) {
    // BAD: may be eliminated by DSE at -O1/-O2
    unsafe { ptr::write_bytes(key as *mut SecretKey, 0, 1); }
}
```

**Fix**: Use `zeroize::Zeroize` (which uses volatile writes internally) or add `std::sync::atomic::compiler_fence(Ordering::SeqCst)` after the write.

---

### B7 — `mem::transmute::<SensitiveType, _>`

**Category**: `SECRET_COPY` | **Severity**: high

**Why it's dangerous**: `mem::transmute` performs a bitwise copy of the value into the target type. If the target type does not implement `ZeroizeOnDrop`, the transmuted copy is a secret that will never be zeroed.

```rust
use std::mem;

struct SecretKey([u8; 32]);
impl Drop for SecretKey { fn drop(&mut self) { /* zeroize */ } }

fn bad(key: SecretKey) -> [u8; 32] {
    // BAD: bytes escape into a plain array with no zeroing
    unsafe { mem::transmute::<SecretKey, [u8; 32]>(key) }
}
```

**Fix**: Avoid transmuting sensitive types. If raw byte access is needed, use `as_ref()` or slice operations that keep the secret in a `Zeroizing<>` wrapper.

---

### B8 — `mem::take(&mut sensitive)`

**Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: medium

**Why it's dangerous**: `mem::take` replaces the target with `Default::default()`, which for `Vec<u8>` is an empty `Vec` — not a zeroed one. The taken value is returned to the caller, which may not zero it. The original location now contains the default value without evidence of the prior secret.

```rust
use std::mem;

struct SecretKey(Vec<u8>);

fn bad(key: &mut SecretKey) -> Vec<u8> {
    // BAD: original bytes copied out; neither location is zeroed
    mem::take(&mut key.0)
}
```

**Fix**: Call `self.key.zeroize()` before using `mem::take`, or use a wrapper that zeroes on `Default`. Ensure the returned value is also properly zeroed after use.

---

### B9 — `slice::from_raw_parts` Over Secret Buffer

**Category**: `SECRET_COPY` | **Severity**: medium

**Why it's dangerous**: Creating a slice alias over a secret buffer using raw pointers bypasses Rust's ownership and lifetime tracking. The resulting slice can be passed to functions that copy the bytes or retain a reference beyond the owning struct's lifetime.

```rust
struct SecretKey([u8; 32]);

fn bad(key: &SecretKey) -> &[u8] {
    // BAD: aliased reference — bytes may escape or be copied by caller
    unsafe { std::slice::from_raw_parts(key.0.as_ptr(), 32) }
}
```

**Fix**: Use safe slice references (`key.0.as_ref()` or `&key.0[..]`) which are subject to normal lifetime rules. Avoid unsafe aliasing of secret memory.

---

### B10 — `async fn` with Secret Local Across `.await`

**Category**: `NOT_ON_ALL_PATHS` | **Severity**: high

**Why it's dangerous**: Rust async functions compile to state machines. Any local variable live across an `.await` point is stored in the generated `Future` struct, which resides in heap memory. If the `Future` is cancelled (dropped mid-poll), the state machine drops without running the normal destructor sequence, leaving the secret in heap memory.

```rust
async fn bad() {
    let secret_key = SecretKey([0u8; 32]);  // stored in Future state machine
    some_async_op().await;  // secret_key is live here
    drop(secret_key);       // may never reach here if Future is cancelled
}
```

**Fix**: Zero the secret before every `.await` point: call `secret_key.zeroize()` before `.await`, or use `Zeroizing<>` wrapper (which zeroes on drop). Alternatively, place the secret in a separate non-async function scope.

---

## Section C — Compiler-Level Patterns

These patterns are **invisible to source and rustdoc analysis** but are detected by `check_mir_patterns.py`, `check_llvm_patterns.py`, and `check_rust_asm.py`. Each entry explains why source inspection is blind to it and what compiler artifact reveals the flaw.

---

### C-MIR1 — Closure Captures Sensitive Local by Value

**Tool**: `check_mir_patterns.py` | **Category**: `SECRET_COPY` | **Severity**: high

**Why source is blind**: At the source level, `let f = || use(secret)` looks identical whether `secret` is captured by reference or by move. Only MIR makes the distinction explicit: the closure struct gets a field `_captured = move _secret`.

```rust
fn bad(secret: Vec<u8>) {
    // Source looks fine — is it a move or borrow?
    let f = move || process(&secret);
    // MIR shows: closure struct receives `_captured_secret = move _secret`
    // The copy is now in the closure's heap allocation, not the original binding
    f();
    // `secret` is gone — but closure may outlive intended scope
}
```

**Detection**: MIR shows `closure_body: _captured_field = move _local` where the local matches a sensitive name pattern.

---

### C-MIR2 — Secret Live Across Generator Yield on Error Path

**Tool**: `check_mir_patterns.py` | **Category**: `NOT_ON_ALL_PATHS` | **Severity**: high

**Why source is blind**: Source analysis can find `.await` points but cannot determine which locals are live at each yield, or whether an error exit path skips a `StorageDead` for the secret. MIR encodes exact liveness: each suspend point lists live locals, and each `Err`/early-return basic block shows whether `StorageDead(_secret)` precedes the yield.

```rust
async fn bad() -> Result<(), Error> {
    let secret_key = SecretKey::new();
    let result = risky_op().await?;  // Err path: secret_key may be live at yield
    // If risky_op() returns Err, the ? operator returns early.
    // In MIR: basic block for Err path may lack StorageDead(_secret_key)
    drop(secret_key);
    Ok(result)
}
```

**Detection**: MIR Err-path basic block has no `StorageDead` for the sensitive local before the `yield`/`GeneratorDrop` terminator.

---

### C-MIR3 — `drop_in_place` for Sensitive Type Has No Zeroize Call

**Tool**: `check_mir_patterns.py` | **Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: medium

**Why source is blind**: When `Drop` is implemented in a separate crate or via blanket impl, source analysis cannot read the drop body. MIR drop-glue functions are generated per-type and show every call inside the drop sequence.

```rust
// The Drop impl may be in an external crate:
impl Drop for ThirdPartySecret {
    fn drop(&mut self) {
        // Does this call zeroize? Source analysis cannot verify.
        self.inner.clear(); // <-- NOT zeroize — MIR reveals no zeroize call
    }
}
```

**Detection**: MIR function `drop_in_place::<SensitiveType>` contains no call to `zeroize`, `volatile_set_memory`, or `memset`.

---

### C-IR1 — DSE Eliminates Correct `zeroize()` Call

**Tool**: `check_llvm_patterns.py` | **Category**: `OPTIMIZED_AWAY_ZEROIZE` | **Severity**: high

**Why source is blind**: The source correctly calls `.zeroize()`. The bug exists only in the optimized IR: LLVM's dead-store elimination pass removes the volatile stores as "dead" before the function returns. Source shows a correct call; IR at O2 shows zero volatile stores.

```rust
fn wipe(key: &mut SecretKey) {
    self.key.zeroize();  // Source looks correct!
    // At O0: 32 volatile stores in IR
    // At O2: 0 volatile stores — DSE eliminated them as "dead before return"
}
```

**Detection**: `volatile store` count drops from N (O0) to 0 (O2) targeting the same buffer.

---

### C-IR2 — Non-Volatile `llvm.memset` on Secret-Sized Range

**Tool**: `check_llvm_patterns.py` | **Category**: `OPTIMIZED_AWAY_ZEROIZE` | **Severity**: high

**Why source is blind**: A `memset` call looks correct in source. IR reveals whether the `llvm.memset` intrinsic has the `volatile` flag set. Without it, LLVM is free to remove the call as a dead store.

```c
// Source: memset(secret, 0, 32); — looks fine
// IR at O0: call void @llvm.memset.p0.i64(ptr %secret, i8 0, i64 32, i1 false)
//                                                                        ^^^^^
//                                                                 volatile=false — removable!
```

**Detection**: `llvm.memset` intrinsic on a buffer matching a sensitive size (16/32/64 bytes) with `volatile=false` flag.

---

### C-IR3 — Secret `alloca` Has `lifetime.end` Without Prior Volatile Store

**Tool**: `check_llvm_patterns.py` | **Category**: `STACK_RETENTION` | **Severity**: high

**Why source is blind**: The local simply goes out of scope in source. IR shows the stack slot's lifetime: if `@llvm.lifetime.end` is reached without any preceding `store volatile`, the slot is released with secret bytes intact.

```rust
fn bad() {
    let mut key = [0u8; 32];
    fill_key(&mut key);
    // key goes out of scope — source shows nothing
    // IR: llvm.lifetime.end(32, %key) with no volatile store before it
    // Stack bytes remain until overwritten
}
```

**Detection**: `@llvm.lifetime.end` on a sensitive `alloca` with no `store volatile` in the dominating path.

---

### C-IR4 — Secret `alloca` Promoted to Registers by SROA/mem2reg

**Tool**: `check_llvm_patterns.py` | **Category**: `OPTIMIZED_AWAY_ZEROIZE` | **Severity**: high

**Why source is blind**: The `alloca` disappears entirely at O2 — LLVM's SROA and mem2reg passes promote it to SSA registers. Any volatile stores targeting that `alloca` are also removed since the `alloca` no longer exists.

```rust
fn bad() {
    let mut key = SecretKey::new();
    // O0 IR: %key = alloca [32 x i8] + volatile stores on drop
    // O2 IR: %key promoted to SSA registers — no alloca, no volatile stores
    use_key(&key);
    // Drop: no volatile stores remain
}
```

**Detection**: `alloca` present at O0 with volatile stores disappears entirely at O2.

---

### C-IR5 — Secret Value in Argument Registers at Call Site

**Tool**: `check_llvm_patterns.py` | **Category**: `REGISTER_SPILL` | **Severity**: medium

**Why source is blind**: Source shows a function call with a sensitive argument. IR shows the calling convention: the value is loaded from memory into argument registers (`%rdi`, `%rsi`, …) before the `call` instruction. The callee may spill those registers to its own stack frame without zeroing them.

```rust
fn bad(key: &SecretKey) {
    callee(key.data);  // Source: pass by value
    // IR: %key_val = load i256, ptr %key; call @callee(i256 %key_val)
    // Callee may spill %rdi/%rsi to its stack frame
}
```

**Detection**: IR shows sensitive `alloca` loaded into argument registers immediately before a `call` instruction.

---

### C-ASM1 — Stack Frame Allocated, No Zero-Stores Before `ret`

**Tool**: `check_rust_asm.py` | **Category**: `STACK_RETENTION` | **Severity**: high

**Why source is blind**: Source shows the function body with no evidence of stack frame contents. Assembly reveals the frame size and whether any zero-store instructions (`movq $0, [rsp+N]` / `str xzr, [sp, #N]`) appear before the `retq`/`ret` instruction.

```asm
; x86-64 example — no zero stores before retq
SecretKey_process:
    subq $64, %rsp      ; allocates 64-byte frame (possibly holds secret)
    ; ... use frame ...
    retq                ; returns without zeroing frame
```

**Detection**: Function with sensitive name allocates stack frame and returns without any zero-store instructions targeting the frame slots.

---

### C-ASM2 — Callee-Saved Register Spilled in Sensitive Function

**Tool**: `check_rust_asm.py` | **Category**: `REGISTER_SPILL` | **Severity**: high

**Why source is blind**: Register allocation decisions are invisible in source or IR. Assembly shows the spill instructions: `movq %r12, [rsp+N]` (x86-64) or `str x19, [sp, #N]` (AArch64). Callee-saved registers (`%r12`–`%r15`/`rbx` on x86-64; `x19`–`x28` on AArch64) are preserved across calls — if they held secret values, the spill creates an unzeroed copy.

```asm
; AArch64 example — x19 (callee-saved) spilled
SecretKey_wipe:
    str x19, [sp, #-16]!   ; spill x19 — may hold secret bytes
    ; ... wipe logic ...
    ldr x19, [sp], #16     ; restore — but spill slot not zeroed
    ret
```

**Detection**: Callee-saved register spill instruction inside a function matching a sensitive name pattern.

---

### C-ASM3 — Caller-Saved Register Spilled in Sensitive Function

**Tool**: `check_rust_asm.py` | **Category**: `REGISTER_SPILL` | **Severity**: medium

**Why source is blind**: Same as C-ASM2 but for caller-saved registers (`%rax`, `%rcx`, etc. / `x0`–`x17` on AArch64). These are not preserved by callees, so the current function is responsible for any secret bytes spilled to the stack.

**Detection**: Caller-saved register spill instruction inside a sensitive function body.

---

### C-ASM4 — `drop_in_place` in Assembly Has No Zeroize/Memset Call

**Tool**: `check_rust_asm.py` | **Category**: `MISSING_SOURCE_ZEROIZE` | **Severity**: medium

**Why source is blind**: Corroborates the MIR-level finding (C-MIR3) with concrete machine code. The emitted assembly for `drop_in_place::<SensitiveType>` contains no `call` to a zeroing function — confirming that the missing zeroize is not merely a MIR-level artifact but reaches the final binary.

**Detection**: `drop_in_place::<SensitiveName>` assembly function contains no `call @zeroize`, `call @volatile_set_memory`, or `call @memset`.

---

## Section D — Undetectable Patterns (TODO)

These patterns are **not detected by any current tool** (`semantic_audit.py`, `find_dangerous_apis.py`, `check_mir_patterns.py`, `check_llvm_patterns.py`, `check_rust_asm.py`). Each entry explains why all current approaches are insufficient and what new capability would be required.

---

### D1 — `Arc<SensitiveType>` / `Rc<SensitiveType>` Deferred Drop

**Category**: `NOT_ON_ALL_PATHS` | **Gap type**: inter-procedural alias/ownership analysis

**Why it's dangerous**: `Drop`/`ZeroizeOnDrop` only runs when the *last* reference is dropped. Any clone of an `Arc<SecretKey>` holds the bytes alive and unzeroed until the reference count reaches zero. If an Arc clone escapes a security boundary (e.g., is passed to a background task), the secret persists until that task completes.

```rust
use std::sync::Arc;

let key = Arc::new(SecretKey::new());  // ZeroizeOnDrop
let clone = Arc::clone(&key);         // reference count = 2
pass_to_background_task(clone);       // may live arbitrarily long
drop(key);                            // count = 1, NOT dropped here
// secret stays in heap until background task finishes
```

**Why undetectable**: `semantic_audit.py` only inspects struct definitions, not call sites. `find_dangerous_apis.py` has no `Arc::clone` pattern — adding one would produce massive false positives without knowing the wrapped type. MIR/IR/ASM tools can detect the drop-glue but cannot statically verify that all Arc clones are dropped before a given boundary.

**Requires**: Inter-procedural ownership/alias tracking (e.g., Polonius dataflow or a custom MIR analysis that tracks Arc reference count propagation across function boundaries).

---

### D2 — `#[repr(C)]` Struct Padding Bytes Not Zeroed

**Category**: `PARTIAL_WIPE` | **Gap type**: struct layout analysis

**Why it's dangerous**: `zeroize()` on a `#[repr(C)]` struct zeros all *declared* fields, but the Rust compiler may insert alignment padding between or after fields. `Zeroize` does not touch padding bytes. An attacker with heap inspection capabilities may recover the secret from pad regions.

```rust
#[repr(C)]
struct MixedSecret {
    flag: u8,      // 1 byte
    // 7 bytes padding here (for alignment of `key`)
    key: [u8; 32],
}
// zeroize() zeros flag and key but NOT the 7 padding bytes
```

**Why undetectable**: `check_rust_asm.py` fires `STACK_RETENTION` only if NO zeroing occurs — it does not detect partial zeroing that skips padding. `check_llvm_patterns.py` counts volatile stores but does not compare bytes-zeroed vs. total struct size.

**Requires**: Struct layout analysis via `rustc -Z print-type-sizes` combined with IR analysis comparing zeroed byte ranges against total struct size.

---

### D3 — `static` / `LazyLock<SensitiveType>` Secret Never Dropped

**Category**: `MISSING_SOURCE_ZEROIZE` | **Gap type**: static item analysis

**Why it's dangerous**: Rust does not call `Drop` on `static` variables at program exit. A `static KEY: LazyLock<ApiKey>` or `static mut SEED: [u8; 32]` is never zeroed, regardless of any `ZeroizeOnDrop` impl.

```rust
use std::sync::LazyLock;

static GLOBAL_KEY: LazyLock<ApiKey> = LazyLock::new(|| ApiKey::generate());
// Drop is never called at program exit — bytes remain in memory until OS reclaim
```

**Why undetectable**: `semantic_audit.py` only processes `kind = "struct"` and `"enum"` items — `kind = "static"` items are silently skipped. `find_dangerous_apis.py` has no `static` binding pattern. Compiler-level tools do not produce zeroing evidence for globals in `.data`/`.bss` sections.

**Requires**: Extend `semantic_audit.py` to process `"static"` kind items from rustdoc JSON, or add a grep in `find_dangerous_apis.py` for `static .* SensitiveName`.

---

### D4 — `async fn` Future Cancellation: State-Machine `Drop` Lacks `ZeroizeOnDrop`

**Category**: `NOT_ON_ALL_PATHS` | **Gap type**: coroutine MIR analysis

**Why it's dangerous**: `find_dangerous_apis.py` and `check_mir_patterns.py` detect secret locals live across `.await` / yield points. The remaining gap is *cancellation safety*: when a `Future` is dropped mid-poll (e.g., by `tokio::select!` dropping the losing branch), any secrets stored in the compiler-generated state-machine struct are freed without zeroing. The generated struct type is anonymous — not written in source.

```rust
async fn process_secret() {
    let key = SecretKey::new();     // stored in coroutine state machine
    phase_one().await;              // suspension point
    phase_two().await;              // another suspension point
    drop(key);
}

// If the Future is cancelled at phase_one().await:
//   - The coroutine struct is dropped
//   - The compiler-generated Drop for the coroutine does NOT zero `key`
//   - Unless the coroutine struct's Drop impl explicitly zeroes captured fields
```

**Why undetectable**: The compiler-generated coroutine struct type is not in the rustdoc index. Its `Drop` impl is generated drop-glue, not user code. `check_mir_patterns.py` detects secrets live at yield points but does not verify that the *coroutine struct's generated Drop glue* calls `zeroize` on each captured field.

**Requires**: `check_mir_patterns.py` extension to identify coroutine/generator MIR bodies, enumerate their captured locals matching sensitive name patterns, and verify presence of `zeroize` calls in the generated Drop glue for the coroutine state machine type.

---

### D5 — `Cow<'_, [u8]>` or `Cow<'_, str>` Silently Cloning a Secret

**Category**: `SECRET_COPY` | **Gap type**: type-taint tracking

**Why it's dangerous**: `Cow::to_owned()`, `Cow::into_owned()`, and `Cow::Owned(...)` allocate an owned copy of the bytes with no tracking. The clone does not inherit any `ZeroizeOnDrop` guarantee. Since `Cow` can hold a reference or an owned value, and conversion between the two is implicit, secrets can be silently promoted to owned allocations.

```rust
use std::borrow::Cow;

fn process(data: Cow<'_, [u8]>) {
    let owned: Vec<u8> = data.into_owned(); // secret bytes in plain Vec
    // owned has no ZeroizeOnDrop — never zeroed
}
```

**Why undetectable**: A source grep on `Cow` alone has unacceptably high false-positive rate without knowing whether the held type is sensitive. `find_dangerous_apis.py` cannot distinguish `Cow<'_, [u8]>` holding secrets from `Cow<'_, str>` holding log messages. MIR/IR would show the allocation but correlation back to "this Cow holds sensitive data" requires type-level taint tracking that current regex-based tools do not perform.

**Requires**: Inter-procedural type taint analysis to track whether the `Cow` inner type originates from a sensitive allocation.

---

### D6 — `mem::swap` Moving Secret Bytes to Non-Zeroizing Location

**Category**: `SECRET_COPY` | **Gap type**: type-aware MIR operand analysis

**Why it's dangerous**: `mem::swap(&mut secret_key, &mut output_buf)` moves the secret bytes bitwise into `output_buf`, which likely does not implement `ZeroizeOnDrop`. The original location is overwritten with `output_buf`'s prior content. The secret now lives in `output_buf` with no zeroing guarantee, while the original location no longer contains the secret (so its Drop impl zeroes the wrong data).

```rust
fn bad(key: &mut SecretKey, output: &mut Vec<u8>) {
    // BAD: key bytes moved into output (plain Vec, no ZeroizeOnDrop)
    unsafe {
        let key_bytes: &mut Vec<u8> = std::mem::transmute(key);
        std::mem::swap(key_bytes, output);
    }
    // key is now "empty" — key.drop() zeroes nothing meaningful
    // output holds the secret bytes with no zeroing guarantee
}
```

**Why undetectable**: `find_dangerous_apis.py` has no `mem::swap` pattern; adding one without type awareness would flag every `swap` call in the codebase. In MIR, `mem::swap` is represented as a pair of assignments — detectable if the checker verifies the types of both operands, but this is not currently implemented.

**Requires**: Type-aware MIR analysis of swap operands to detect when a sensitive type is swapped into a non-zeroizing container.
