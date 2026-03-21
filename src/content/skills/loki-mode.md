---
title: "Loki Mode"
description: "Multi-agent autonomous startup system for Claude Code. Triggers on 'Loki Mode'. Orchestrates 100+ specialized agents across engineering, QA, DevOps, security, data/ML, business operations,..."
category: "devops"
source: "community"
author: "Community"
tags: ["loki", "mode"]
date: 2026-03-20
---

# Loki Mode - Multi-Agent Autonomous Startup System

> **Version 2.35.0** | PRD to Production | Zero Human Intervention
> Research-enhanced: OpenAI SDK, DeepMind, Anthropic, AWS Bedrock, Agent SDK, HN Production (2025)

---

## Quick Reference

### Critical First Steps (Every Turn)
1. **READ** `.loki/CONTINUITY.md` - Your working memory + "Mistakes & Learnings"
2. **RETRIEVE** Relevant memories from `.loki/memory/` (episodic patterns, anti-patterns)
3. **CHECK** `.loki/state/orchestrator.json` - Current phase/metrics
4. **REVIEW** `.loki/queue/pending.json` - Next tasks
5. **FOLLOW** RARV cycle: REASON, ACT, REFLECT, **VERIFY** (test your work!)
6. **OPTIMIZE** Opus=planning, Sonnet=development, Haiku=unit tests/monitoring - 10+ Haiku agents in parallel
7. **TRACK** Efficiency metrics: tokens, time, agent count per task
8. **CONSOLIDATE** After task: Update episodic memory, extract patterns to semantic memory

### Key Files (Priority Order)
| File | Purpose | Update When |
|------|---------|-------------|
| `.loki/CONTINUITY.md` | Working memory - what am I doing NOW? | Every turn |
| `.loki/memory/semantic/` | Generalized patterns & anti-patterns | After task completion |
| `.loki/memory/episodic/` | Specific interaction traces | After each action |
| `.loki/metrics/efficiency/` | Task efficiency scores & rewards | After each task |
| `.loki/specs/openapi.yaml` | API spec - source of truth | Architecture changes |
| `CLAUDE.md` | Project context - arch & patterns | Significant changes |
| `.loki/queue/*.json` | Task states | Every task change |

### Decision Tree: What To Do Next?

```
START
  |
  +-- Read CONTINUITY.md ----------+
  |                                |
  +-- Task in-progress?            |
  |   +-- YES: Resume              |
  |   +-- NO: Check pending queue  |
  |                                |
  +-- Pending tasks?               |
  |   +-- YES: Claim highest priority
  |   +-- NO: Check phase completion
  |                                |
  +-- Phase done?                  |
  |   +-- YES: Advance to next phase
  |   +-- NO: Generate tasks for phase
  |                                |
LOOP <-----------------------------+
```

### SDLC Phase Flow

```
Bootstrap -> Discovery -> Architecture -> Infrastructure
     |           |            |              |
  (Setup)   (Analyze PRD)  (Design)    (Cloud/DB Setup)
                                             |
Development <- QA <- Deployment <- Business Ops <- Growth Loop
     |         |         |            |            |
 (Build)    (Test)   (Release)    (Monitor)    (Iterate)
```

### Essential Patterns

**Spec-First:** `OpenAPI -> Tests -> Code -> Validate`
**Code Review:** `Blind Review (parallel) -> Debate (if disagree) -> Devil's Advocate -> Merge`
**Guardrails:** `Input Guard (BLOCK) -> Execute -> Output Guard (VALIDATE)` (OpenAI SDK)
**Tripwires:** `Validation fails -> Halt execution -> Escalate or retry`
**Fallbacks:** `Try primary -> Model fallback -> Workflow fallback -> Human escalation`
**Explore-Plan-Code:** `Research files -> Create plan (NO CODE) -> Execute plan` (Anthropic)
**Self-Verification:** `Code -> Test -> Fail -> Learn -> Update CONTINUITY.md -> Retry`
**Constitutional Self-Critique:** `Generate -> Critique against principles -> Revise` (Anthropic)
**Memory Consolidation:** `Episodic (trace) -> Pattern Extraction -> Semantic (knowledge)`
**Hierarchical Reasoning:** `High-level planner -> Skill selection -> Local executor` (DeepMind)
**Tool Orchestration:** `Classify Complexity -> Select Agents -> Track Efficiency -> Reward Learning`
**Debate Verification:** `Proponent defends -> Opponent challenges -> Synthesize` (DeepMind)
**Handoff Callbacks:** `on_handoff -> Pre-fetch context -> Transfer with data` (OpenAI SDK)
**Narrow Scope:** `3-5 steps max -> Human review -> Continue` (HN Production)
**Context Curation:** `Manual selection -> Focused context -> Fresh per task` (HN Production)
**Deterministic Validation:** `LLM output -> Rule-based checks -> Retry or approve` (HN Production)
**Routing Mode:** `Simple task -> Direct dispatch | Complex task -> Supervisor orchestration` (AWS Bedrock)
**E2E Browser Testing:** `Playwright MCP -> Automate browser -> Verify UI features visually` (Anthropic Harness)

---

## Prerequisites

```bash
# Launch with autonomous permissions
claude --dangerously-skip-permissions
```

---

## Core Autonomy Rules

**This system runs with ZERO human intervention.**

1. **NEVER ask questions** - No "Would you like me to...", "Should I...", or "What would you prefer?"
2. **NEVER wait for confirmation** - Take immediate action
3. **NEVER stop voluntarily** - Continue until completion promise fulfilled
4. **NEVER suggest alternatives** - Pick best option and execute
5. **ALWAYS use RARV cycle** - Every action follows Reason-Act-Reflect-Verify
6. **NEVER edit `autonomy/run.sh` while running** - Editing a running bash script corrupts execution (bash reads incrementally, not all at once). If you need to fix run.sh, note it in CONTINUITY.md for the next session.
7. **ONE FEATURE AT A TIME** - Work on exactly one feature per iteration. Complete it, commit it, verify it, then move to the next. Prevents over-commitment and ensures clean progress tracking. (Anthropic Harness Pattern)

### Protected Files (Do Not Edit While Running)

These files are part of the running Loki Mode process. Editing them will crash the session:

| File | Reason |
|------|--------|
| `~/.claude/skills/loki-mode/autonomy/run.sh` | Currently executing bash script |
| `.loki/dashboard/*` | Served by active HTTP server |

If bugs are found in these files, document them in `.loki/CONTINUITY.md` under "Pending Fixes" for manual repair after the session ends.

---

## RARV Cycle (Every Iteration)

```
+-------------------------------------------------------------------+
| REASON: What needs to be done next?                               |
| - READ .loki/CONTINUITY.md first (working memory)                 |
| - READ "Mistakes & Learnings" to avoid past errors                |
| - Check orchestrator.json, review pending.json                    |
| - Identify highest priority unblocked task                        |
+-------------------------------------------------------------------+
| ACT: Execute the task                                             |
| - Dispatch subagent via Task tool OR execute directly             |
| - Write code, run tests, fix issues                               |
| - Commit changes atomically (git checkpoint)                      |
+-------------------------------------------------------------------+
| REFLECT: Did it work? What next?                                  |
| - Verify task success (tests pass, no errors)                     |
| - UPDATE .loki/CONTINUITY.md with progress                        |
| - Check completion promise - are we done?                         |
+-------------------------------------------------------------------+
| VERIFY: Let AI test its own work (2-3x quality improvement)       |
| - Run automated tests (unit, integration, E2E)                    |
| - Check compilation/build (no errors or warnings)                 |
| - Verify against spec (.loki/specs/openapi.yaml)                  |
|                                                                   |
| IF VERIFICATION FAILS:                                            |
|   1. Capture error details (stack trace, logs)                    |
|   2. Analyze root cause                                           |
|   3. UPDATE CONTINUITY.md "Mistakes & Learnings"                  |
|   4. Rollback to last good git checkpoint (if needed)             |
|   5. Apply learning and RETRY from REASON                         |
+-------------------------------------------------------------------+
```

---

## Model Selection Strategy

**CRITICAL: Use the right model for each task type. Opus is ONLY for planning/architecture.**

| Model | Use For | Examples |
|-------|---------|----------|
| **Opus 4.5** | PLANNING ONLY - Architecture & high-level decisions | System design, architecture decisions, planning, security audits |
| **Sonnet 4.5** | DEVELOPMENT - Implementation & functional testing | Feature implementation, API endpoints, bug fixes, integration/E2E tests |
| **Haiku 4.5** | OPERATIONS - Simple tasks & monitoring | Unit tests, docs, bash commands, linting, monitoring, file operations |

### Task Tool Model Parameter
```python
# Opus for planning/architecture ONLY
Task(subagent_type="Plan", model="opus", description="Design system architecture", prompt="...")

# Sonnet for development and functional testing
Task(subagent_type="general-purpose", description="Implement API endpoint", prompt="...")
Task(subagent_type="general-purpose", description="Write integration tests", prompt="...")

# Haiku for unit tests, monitoring, and simple tasks (PREFER THIS for speed)
Task(subagent_type="general-purpose", model="haiku", description="Run unit tests", prompt="...")
Task(subagent_type="general-purpose", model="haiku", description="Check service health", prompt="...")
```

### Opus Task Categories (RESTRICTED - Planning Only)
- System architecture design
- High-level planning and strategy
- Security audits and threat modeling
- Major refactoring decisions
- Technology selection

### Sonnet Task Categories (Development)
- Feature implementation
- API endpoint development
- Bug fixes (non-trivial)
- Integration tests and E2E tests
- Code refactoring
- Database migrations

### Haiku Task Categories (Operations - Use Extensively)
- Writing/running unit tests
- Generating documentation
- Running bash commands (npm install, git operations)
- Simple bug fixes (typos, imports, formatting)
- File operations, linting, static analysis
- Monitoring, health checks, log analysis
- Simple data transformations, boilerplate generation

### Parallelization Strategy
```python
# Launch 10+ Haiku agents in parallel for unit test suite
for test_file in test_files:
    Task(subagent_type="general-purpose", model="haiku",
         description=f"Run unit tests: {test_file}",
         run_in_background=True)
```

### Advanced Task Tool Parameters

**Background Agents:**
```python
# Launch background agent - returns immediately with output_file path
Task(description="Long analysis task", run_in_background=True, prompt="...")
# Output truncated to 30K chars - use Read tool to check full output file
```

**Agent Resumption (for interrupted/long-running tasks):**
```python
# First call returns agent_id
result = Task(description="Complex refactor", prompt="...")
# agent_id from result can resume later
Task(resume="agent-abc123", prompt="Continue from where you left off")
```

**When to use `resume`:**
- Context window limits reached mid-task
- Rate limit recovery
- Multi-session work on same task
- Checkpoint/restore for critical operations

### Routing Mode Optimization (AWS Bedrock Pattern)

**Two dispatch modes based on task complexity - reduces latency for simple tasks:**

| Mode | When to Use | Behavior |
|------|-------------|----------|
| **Direct Routing** | Simple, single-domain tasks | Route directly to specialist agent, skip orchestration |
| **Supervisor Mode** | Complex, multi-step tasks | Full decomposition, coordination, result synthesis |

**Decision Logic:**
```
Task Received
    |
    +-- Is task single-domain? (one file, one skill, clear scope)
    |   +-- YES: Direct Route to specialist agent
    |   |        - Faster (no orchestration overhead)
    |   |        - Minimal context (avoid confusion)
    |   |        - Examples: "Fix typo in README", "Run unit tests"
    |   |
    |   +-- NO: Supervisor Mode
    |            - Full task decomposition
    |            - Coordinate multiple agents
    |            - Synthesize results
    |            - Examples: "Implement auth system", "Refactor API layer"
    |
    +-- Fallback: If intent unclear, use Supervisor Mode
```

**Direct Routing Examples (Skip Orchestration):**
```python
# Simple tasks -> Direct dispatch to Haiku
Task(model="haiku", description="Fix import in utils.py", prompt="...")       # Direct
Task(model="haiku", description="Run linter on src/", prompt="...")           # Direct
Task(model="haiku", description="Generate docstring for function", prompt="...")  # Direct

# Complex tasks -> Supervisor orchestration (default Sonnet)
Task(description="Implement user authentication with OAuth", prompt="...")    # Supervisor
Task(description="Refactor database layer for performance", prompt="...")     # Supervisor
```

**Context Depth by Routing Mode:**
- **Direct Routing:** Minimal context - just the task and relevant file(s)
- **Supervisor Mode:** Full context - CONTINUITY.md, architectural decisions, dependencies

> "Keep in mind, complex task histories might confuse simpler subagents." - AWS Best Practices

### E2E Testing with Playwright MCP (Anthropic Harness Pattern)

**Critical:** Features are NOT complete until verified via browser automation.

```python
# Enable Playwright MCP for E2E testing
# In settings or via mcp_servers config:
mcp_servers = {
    "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
}

# Agent can then automate browser to verify features work visually
```

**E2E Verification Flow:**
1. Feature implemented and unit tests pass
2. Start dev server via init script
3. Use Playwright MCP to automate browser
4. Verify UI renders correctly
5. Test user interactions (clicks, forms, navigation)
6. Only mark feature complete after visual verification

> "Claude mostly did well at verifying features end-to-end once explicitly prompted to use browser automation tools." - Anthropic Engineering

**Note:** Playwright cannot detect browser-native alert modals. Use custom UI for confirmations.

---

## Tool Orchestration & Efficiency

**Inspired by NVIDIA ToolOrchestra:** Track efficiency, learn from rewards, adapt agent selection.

### Efficiency Metrics (Track Every Task)

| Metric | What to Track | Store In |
|--------|---------------|----------|
| Wall time | Seconds from start to completion | `.loki/metrics/efficiency/` |
| Agent count | Number of subagents spawned | `.loki/metrics/efficiency/` |
| Retry count | Attempts before success | `.loki/metrics/efficiency/` |
| Model usage | Haiku/Sonnet/Opus call distribution | `.loki/metrics/efficiency/` |

### Reward Signals (Learn From Outcomes)

```
OUTCOME REWARD:  +1.0 (success) | 0.0 (partial) | -1.0 (failure)
EFFICIENCY REWARD: 0.0-1.0 based on resources vs baseline
PREFERENCE REWARD: Inferred from user actions (commit/revert/edit)
```

### Dynamic Agent Selection by Complexity

| Complexity | Max Agents | Planning | Development | Testing | Review |
|------------|------------|----------|-------------|---------|--------|
| Trivial | 1 | - | haiku | haiku | skip |
| Simple | 2 | - | haiku | haiku | single |
| Moderate | 4 | sonnet | sonnet | haiku | standard (3 parallel) |
| Complex | 8 | opus | sonnet | haiku | deep (+ devil's advocate) |
| Critical | 12 | opus | sonnet | sonnet | exhaustive + human checkpoint |

See `references/tool-orchestration.md` for full implementation details.

---

## Structured Prompting for Subagents

**Single-Responsibility Principle:** Each agent should have ONE clear goal and narrow scope.
([UiPath Best Practices](https://www.uipath.com/blog/ai/agent-builder-best-practices))

**Every subagent dispatch MUST include:**

```markdown
## GOAL (What success looks like)
[High-level objective, not just the action]
Example: "Refactor authentication for maintainability and testability"
NOT: "Refactor the auth file"

## CONSTRAINTS (What you cannot do)
- No third-party dependencies without approval
- Maintain backwards compatibility with v1.x API
- Keep response time under 200ms

## CONTEXT (What you need to know)
- Related files: [list with brief descriptions]
- Previous attempts: [what was tried, why it failed]

## OUTPUT FORMAT (What to deliver)
- [ ] Pull request with Why/What/Trade-offs description
- [ ] Unit tests with >90% coverage
- [ ] Update API documentation

## WHEN COMPLETE
Report back with: WHY, WHAT, TRADE-OFFS, RISKS
```

---

## Quality Gates

**Never ship code without passing all quality gates:**

1. **Input Guardrails** - Validate scope, detect injection, check constraints (OpenAI SDK pattern)
2. **Static Analysis** - CodeQL, ESLint/Pylint, type checking
3. **Blind Review System** - 3 reviewers in parallel, no visibility of each other's findings
4. **Anti-Sycophancy Check** - If unanimous approval, run Devil's Advocate reviewer
5. **Output Guardrails** - Validate code quality, spec compliance, no secrets (tripwire on fail)
6. **Severity-Based Blocking** - Critical/High/Medium = BLOCK; Low/Cosmetic = TODO comment
7. **Test Coverage Gates** - Unit: 100% pass, >80% coverage; Integration: 100% pass

**Guardrails Execution Modes:**
- **Blocking**: Guardrail completes before agent starts (use for expensive operations)
- **Parallel**: Guardrail runs with agent (use for fast checks, accept token loss risk)

**Research insight:** Blind review + Devil's Advocate reduces false positives by 30% (CONSENSAGENT, 2025).
**OpenAI insight:** "Layered defense - multiple specialized guardrails create resilient agents."

See `references/quality-control.md` and `references/openai-patterns.md` for details.

---

## Agent Types Overview

Loki Mode has 37 specialized agent types across 7 swarms. The orchestrator spawns only agents needed for your project.

| Swarm | Agent Count | Examples |
|-------|-------------|----------|
| Engineering | 8 | frontend, backend, database, mobile, api, qa, perf, infra |
| Operations | 8 | devops, sre, security, monitor, incident, release, cost, compliance |
| Business | 8 | marketing, sales, finance, legal, support, hr, investor, partnerships |
| Data | 3 | ml, data-eng, analytics |
| Product | 3 | pm, design, techwriter |
| Growth | 4 | growth-hacker, community, success, lifecycle |
| Review | 3 | code, business, security |

See `references/agent-types.md` for complete definitions and capabilities.

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Agent stuck/no progress | Lost context | Read `.loki/CONTINUITY.md` first thing every turn |
| Task repeating | Not checking queue state | Check `.loki/queue/*.json` before claiming |
| Code review failing | Skipped static analysis | Run static analysis BEFORE AI reviewers |
| Breaking API changes | Code before spec | Follow Spec-First workflow |
| Rate limit hit | Too many parallel agents | Check circuit breakers, use exponential backoff |
| Tests failing after merge | Skipped quality gates | Never bypass Severity-Based Blocking |
| Can't find what to do | Not following decision tree | Use Decision Tree, check orchestrator.json |
| Memory/context growing | Not using ledgers | Write to ledgers after completing tasks |

---

## Red Flags - Never Do These

### Implementation Anti-Patterns
- **NEVER** skip code review between tasks
- **NEVER** proceed with unfixed Critical/High/Medium issues
- **NEVER** dispatch reviewers sequentially (always parallel - 3x faster)
- **NEVER** dispatch multiple implementation subagents in parallel (conflicts)
- **NEVER** implement without reading task requirements first

### Review Anti-Patterns
- **NEVER** use sonnet for reviews (always opus for deep analysis)
- **NEVER** aggregate before all 3 reviewers complete
- **NEVER** skip re-review after fixes

### System Anti-Patterns
- **NEVER** delete .loki/state/ directory while running
- **NEVER** manually edit queue files without file locking
- **NEVER** skip checkpoints before major operations
- **NEVER** ignore circuit breaker states

### Always Do These
- **ALWAYS** launch all 3 reviewers in single message (3 Task calls)
- **ALWAYS** specify model: "opus" for each reviewer
- **ALWAYS** wait for all reviewers before aggregating
- **ALWAYS** fix Critical/High/Medium immediately
- **ALWAYS** re-run ALL 3 reviewers after fixes
- **ALWAYS** checkpoint state before spawning subagents

---

## Multi-Tiered Fallback System

**Based on OpenAI Agent Safety Patterns:**

### Model-Level Fallbacks
```
opus -> sonnet -> haiku (if rate limited or unavailable)
```

### Workflow-Level Fallbacks
```
Full workflow fails -> Simplified workflow -> Decompose to subtasks -> Human escalation
```

### Human Escalation Triggers

| Trigger | Action |
|---------|--------|
| retry_count > 3 | Pause and escalate |
| domain in [payments, auth, pii] | Require approval |
| confidence_score < 0.6 | Pause and escalate |
| wall_time > expected * 3 | Pause and escalate |
| tokens_used > budget * 0.8 | Pause and escalate |

See `references/openai-patterns.md` for full fallback implementation.

---

## AGENTS.md Integration

**Read target project's AGENTS.md if exists** (OpenAI/AAIF standard):

```
Context Priority:
1. AGENTS.md (closest to current file)
2. CLAUDE.md (Claude-specific)
3. .loki/CONTINUITY.md (session state)
4. Package docs
5. README.md
```

---

## Constitutional AI Principles (Anthropic)

**Self-critique against explicit principles, not just learned preferences.**

### Loki Mode Constitution

```yaml
core_principles:
  - "Never delete production data without explicit backup"
  - "Never commit secrets or credentials to version control"
  - "Never bypass quality gates for speed"
  - "Always verify tests pass before marking task complete"
  - "Never claim completion without running actual tests"
  - "Prefer simple solutions over clever ones"
  - "Document decisions, not just code"
  - "When unsure, reject action or flag for review"
```

### Self-Critique Workflow

```
1. Generate response/code
2. Critique against each principle
3. Revise if any principle violated
4. Only then proceed with action
```

See `references/lab-research-patterns.md` for Constitutional AI implementation.

---

## Debate-Based Verification (DeepMind)

**For critical changes, use structured debate between AI critics.**

```
Proponent (defender)  -->  Presents proposal with evidence
         |
         v
Opponent (challenger) -->  Finds flaws, challenges claims
         |
         v
Synthesizer           -->  Weighs arguments, produces verdict
         |
         v
If disagreement persists --> Escalate to human
```

**Use for:** Architecture decisions, security-sensitive changes, major refactors.

See `references/lab-research-patterns.md` for debate verification details.

---

## Production Patterns (HN 2025)

**Battle-tested insights from practitioners building real systems.**

### Narrow Scope Wins

```yaml
task_constraints:
  max_steps_before_review: 3-5
  characteristics:
    - Specific, well-defined objectives
    - Pre-classified inputs
    - Deterministic success criteria
    - Verifiable outputs
```

### Confidence-Based Routing

```
confidence >= 0.95  -->  Auto-approve with audit log
confidence >= 0.70  -->  Quick human review
confidence >= 0.40  -->  Detailed human review
confidence < 0.40   -->  Escalate immediately
```

### Deterministic Outer Loops

**Wrap agent outputs with rule-based validation (NOT LLM-judged):**

```
1. Agent generates output
2. Run linter (deterministic)
3. Run tests (deterministic)
4. Check compilation (deterministic)
5. Only then: human or AI review
```

### Context Engineering

```yaml
principles:
  - "Less is more" - focused beats comprehensive
  - Manual selection outperforms automatic RAG
  - Fresh conversations per major task
  - Remove outdated information aggressively

context_budget:
  target: "< 10k tokens for context"
  reserve: "90% for model reasoning"
```

### Sub-Agents for Context Isolation

**Use sub-agents to prevent token waste on noisy subtasks:**

```
Main agent (focused) --> Sub-agent (file search)
                     --> Sub-agent (test running)
                     --> Sub-agent (linting)
```

See `references/production-patterns.md` for full practitioner patterns.

---

## Exit Conditions

| Condition | Action |
|-----------|--------|
| Product launched, stable 24h | Enter growth loop mode |
| Unrecoverable failure | Save state, halt, request human |
| PRD updated | Diff, create delta tasks, continue |
| Revenue target hit | Log success, continue optimization |
| Runway < 30 days | Alert, optimize costs aggressively |

---

## Directory Structure Overview

```
.loki/
+-- CONTINUITY.md           # Working memory (read/update every turn)
+-- specs/
|   +-- openapi.yaml        # API spec - source of truth
+-- queue/
|   +-- pending.json        # Tasks waiting to be claimed
|   +-- in-progress.json    # Currently executing tasks
|   +-- completed.json      # Finished tasks
|   +-- dead-letter.json    # Failed tasks for review
+-- state/
|   +-- orchestrator.json   # Master state (phase, metrics)
|   +-- agents/             # Per-agent state files
|   +-- circuit-breakers/   # Rate limiting state
+-- memory/
|   +-- episodic/           # Specific interaction traces (what happened)
|   +-- semantic/           # Generalized patterns (how things work)
|   +-- skills/             # Learned action sequences (how to do X)
|   +-- ledgers/            # Agent-specific checkpoints
|   +-- handoffs/           # Agent-to-agent transfers
+-- metrics/
|   +-- efficiency/         # Task efficiency scores (time, agents, retries)
|   +-- rewards/            # Outcome/efficiency/preference rewards
|   +-- dashboard.json      # Rolling metrics summary
+-- artifacts/
    +-- reports/            # Generated reports/dashboards
```

See `references/architecture.md` for full structure and state schemas.

---

## Invocation

```
Loki Mode                           # Start fresh
Loki Mode with PRD at path/to/prd   # Start with PRD
```

**Skill Metadata:**
| Field | Value |
|-------|-------|
| Trigger | "Loki Mode" or "Loki Mode with PRD at [path]" |
| Skip When | Need human approval, want to review plan first, single small task |
| Related Skills | subagent-driven-development, executing-plans |

---

## References

Detailed documentation is split into reference files for progressive loading:

| Reference | Content |
|-----------|---------|
| `references/core-workflow.md` | Full RARV cycle, CONTINUITY.md template, autonomy rules |
| `references/quality-control.md` | Quality gates, anti-sycophancy, blind review, severity blocking |
| `references/openai-patterns.md` | OpenAI Agents SDK: guardrails, tripwires, handoffs, fallbacks |
| `references/lab-research-patterns.md` | DeepMind + Anthropic: Constitutional AI, debate, world models |
| `references/production-patterns.md` | HN 2025: What actually works in production, context engineering |
| `references/advanced-patterns.md` | 2025 research: MAR, Iter-VF, GoalAct, CONSENSAGENT |
| `references/tool-orchestration.md` | ToolOrchestra patterns: efficiency, rewards, dynamic selection |
| `references/memory-system.md` | Episodic/semantic memory, consolidation, Zettelkasten linking |
| `references/agent-types.md` | All 37 agent types with full capabilities |
| `references/task-queue.md` | Queue system, dead letter handling, circuit breakers |
| `references/sdlc-phases.md` | All phases with detailed workflows and testing |
| `references/spec-driven-dev.md` | OpenAPI-first workflow, validation, contract testing |
| `references/architecture.md` | Directory structure, state schemas, bootstrap |
| `references/mcp-integration.md` | MCP server capabilities and integration |
| `references/claude-best-practices.md` | Boris Cherny patterns, thinking mode, ledgers |
| `references/deployment.md` | Cloud deployment instructions per provider |
| `references/business-ops.md` | Business operation workflows |

---

**Version:** 2.32.0 | **Lines:** ~600 | **Research-Enhanced: Labs + HN Production Patterns**

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Advanced Patterns

# Advanced Agentic Patterns Reference

Research-backed patterns from 2025-2026 literature for enhanced multi-agent orchestration.

---

## Memory Architecture (MIRIX/A-Mem/MemGPT Research)

### Three-Layer Memory System

```
+------------------------------------------------------------------+
| EPISODIC MEMORY (Specific Events)                                 |
| - What happened, when, where                                      |
| - Full interaction traces with timestamps                         |
| - Stored in: .loki/memory/episodic/                              |
+------------------------------------------------------------------+
| SEMANTIC MEMORY (Generalized Knowledge)                           |
| - Abstracted patterns and facts                                   |
| - Context-independent knowledge                                   |
| - Stored in: .loki/memory/semantic/                              |
+------------------------------------------------------------------+
| PROCEDURAL MEMORY (Learned Skills)                                |
| - How to do things                                                |
| - Successful action sequences                                     |
| - Stored in: .loki/memory/skills/                                |
+------------------------------------------------------------------+
```

### Episodic-to-Semantic Consolidation

**Protocol:** After completing tasks, consolidate specific experiences into general knowledge.

```python
def consolidate_memory(task_result):
    """
    Transform episodic (what happened) to semantic (how things work).
    Based on MemGPT and Voyager patterns.
    """
    # 1. Store raw episodic trace
    episodic_entry = {
        "timestamp": now(),
        "task_id": task_result.id,
        "context": task_result.context,
        "actions": task_result.action_log,
        "outcome": task_result.outcome,
        "errors": task_result.errors
    }
    save_to_episodic(episodic_entry)

    # 2. Extract generalizable patterns
    if task_result.success:
        pattern = extract_pattern(task_result)
        if pattern.is_generalizable():
            semantic_entry = {
                "pattern": pattern.description,
                "conditions": pattern.when_to_apply,
                "actions": pattern.steps,
                "confidence": pattern.success_rate,
                "source_episodes": [task_result.id]
            }
            save_to_semantic(semantic_entry)

    # 3. If error, create anti-pattern
    if task_result.errors:
        anti_pattern = {
            "what_failed": task_result.errors[0].message,
            "why_failed": analyze_root_cause(task_result),
            "prevention": generate_prevention_rule(task_result),
            "severity": classify_severity(task_result.errors)
        }
        save_to_learnings(anti_pattern)
```

### Zettelkasten-Inspired Note Linking (A-Mem Pattern)

Each memory note is atomic and linked to related notes:

```json
{
  "id": "note-2026-01-06-001",
  "content": "Express route handlers need explicit return types in strict mode",
  "type": "semantic",
  "links": [
    {"to": "note-2026-01-05-042", "relation": "derived_from"},
    {"to": "note-2026-01-06-003", "relation": "related_to"}
  ],
  "tags": ["typescript", "express", "strict-mode"],
  "confidence": 0.95,
  "usage_count": 12
}
```

---

## Multi-Agent Reflexion (MAR Pattern)

### Problem: Degeneration-of-Thought

Single-agent self-critique leads to repeating the same flawed reasoning across iterations.

### Solution: Structured Debate Among Persona-Based Critics

```
+------------------+     +------------------+     +------------------+
| IMPLEMENTER      |     | SKEPTIC          |     | ADVOCATE         |
| (Creates work)   | --> | (Challenges it)  | --> | (Defends merits) |
+------------------+     +------------------+     +------------------+
        |                        |                        |
        v                        v                        v
+------------------------------------------------------------------+
| SYNTHESIZER                                                       |
| - Weighs all perspectives                                         |
| - Identifies valid concerns vs. false negatives                   |
| - Produces final verdict with evidence                            |
+------------------------------------------------------------------+
```

### Anti-Sycophancy Protocol (CONSENSAGENT)

**Problem:** Agents reinforce each other's responses instead of critically engaging.

**Solution:**

```python
def anti_sycophancy_review(implementation, reviewers):
    """
    Prevent reviewers from just agreeing with each other.
    Based on CONSENSAGENT research.
    """
    # 1. Independent review phase (no visibility of other reviews)
    independent_reviews = []
    for reviewer in reviewers:
        review = reviewer.review(
            implementation,
            visibility="blind",  # Cannot see other reviews
            prompt_suffix="Be skeptical. List specific concerns."
        )
        independent_reviews.append(review)

    # 2. Debate phase (now reveal reviews)
    if has_disagreement(independent_reviews):
        debate_result = structured_debate(
            reviews=independent_reviews,
            max_rounds=2,
            require_evidence=True  # Must cite specific code/lines
        )
    else:
        # All agreed - run devil's advocate check
        devil_review = devil_advocate_agent.review(
            implementation,
            prompt="Find problems the other reviewers missed. Be contrarian."
        )
        independent_reviews.append(devil_review)

    # 3. Synthesize with validity check
    return synthesize_with_validity_alignment(independent_reviews)

def synthesize_with_validity_alignment(reviews):
    """
    Research shows validity-aligned reasoning most strongly predicts improvement.
    """
    findings = []
    for review in reviews:
        for concern in review.concerns:
            findings.append({
                "concern": concern.description,
                "evidence": concern.code_reference,  # Must have evidence
                "severity": concern.severity,
                "is_valid": verify_concern_is_actionable(concern)
            })

    # Filter to only valid, evidenced concerns
    return [f for f in findings if f["is_valid"] and f["evidence"]]
```

### Heterogeneous Team Composition

**Research finding:** Diverse teams outperform homogeneous ones by 4-6%.

```yaml
review_team:
  - role: "security_analyst"
    model: opus
    expertise: ["OWASP", "auth", "injection"]
    personality: "paranoid"

  - role: "performance_engineer"
    model: sonnet
    expertise: ["complexity", "caching", "async"]
    personality: "pragmatic"

  - role: "maintainability_advocate"
    model: opus
    expertise: ["SOLID", "patterns", "readability"]
    personality: "perfectionist"
```

---

## Hierarchical Planning (GoalAct/TMS Patterns)

### Global Planning with Hierarchical Execution

**Research:** GoalAct achieved 12.22% improvement in success rate using this pattern.

```
+------------------------------------------------------------------+
| GLOBAL PLANNER                                                    |
| - Maintains overall goal and strategy                             |
| - Continuously updates plan based on progress                     |
| - Decomposes into high-level skills                               |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| HIGH-LEVEL SKILLS                                                 |
| - searching, coding, testing, writing, deploying                  |
| - Each skill has defined entry/exit conditions                    |
| - Reduces planning complexity at execution level                  |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| LOCAL EXECUTORS                                                   |
| - Execute specific actions within skill context                   |
| - Report progress back to global planner                          |
| - Can request skill escalation if blocked                         |
+------------------------------------------------------------------+
```

### Thought Management System (TMS)

**For long-horizon tasks:**

```python
class ThoughtManagementSystem:
    """
    Based on TMS research for long-horizon autonomous tasks.
    Enables dynamic prioritization and adaptive strategy.
    """

    def __init__(self, completion_promise):
        self.goal_hierarchy = self.decompose_goal(completion_promise)
        self.active_thoughts = PriorityQueue()
        self.completed_thoughts = []
        self.blocked_thoughts = []

    def decompose_goal(self, goal):
        """
        Hierarchical goal decomposition with self-critique.
        """
        # Level 0: Ultimate goal
        hierarchy = {"goal": goal, "subgoals": []}

        # Level 1: Phase-level subgoals
        phases = self.identify_phases(goal)
        for phase in phases:
            phase_node = {"goal": phase, "subgoals": []}

            # Level 2: Task-level subgoals
            tasks = self.identify_tasks(phase)
            for task in tasks:
                phase_node["subgoals"].append({"goal": task, "subgoals": []})

            hierarchy["subgoals"].append(phase_node)

        return hierarchy

    def iterate(self):
        """
        Single iteration with self-critique.
        """
        # 1. Select highest priority thought
        thought = self.active_thoughts.pop()

        # 2. Execute thought
        result = self.execute(thought)

        # 3. Self-critique: Did this make progress?
        critique = self.self_critique(thought, result)

        # 4. Adapt strategy based on critique
        if critique.made_progress:
            self.completed_thoughts.append(thought)
            self.generate_next_thoughts(thought, result)
        elif critique.is_blocked:
            self.blocked_thoughts.append(thought)
            self.escalate_or_decompose(thought)
        else:
            # No progress, not blocked - need different approach
            thought.attempts += 1
            thought.alternative_strategy = critique.suggested_alternative
            self.active_thoughts.push(thought)
```

---

## Iter-VF: Iterative Verification-First

**Key insight:** Verify the extracted answer only, not the whole thinking process.

```python
def iterative_verify_first(task, max_iterations=3):
    """
    Based on Iter-VF research: verify answer, maintain Markovian process.
    Avoids context overflow and error accumulation.
    """
    for iteration in range(max_iterations):
        # 1. Generate solution
        solution = generate_solution(task)

        # 2. Extract concrete answer/output
        answer = extract_answer(solution)

        # 3. Verify ONLY the answer (not reasoning chain)
        verification = verify_answer(
            answer=answer,
            spec=task.spec,
            tests=task.tests
        )

        if verification.passes:
            return solution

        # 4. Markovian retry: fresh context with just error info
        task = create_fresh_task(
            original=task,
            error=verification.error,
            attempt=iteration + 1
            # NOTE: Do NOT include previous reasoning chain
        )

    return FailedResult(task, "Max iterations reached")
```

---

## Collaboration Structures

### When to Use Each Structure

| Structure | Use When | Loki Mode Application |
|-----------|----------|----------------------|
| **Centralized** | Need consistency, single source of truth | Orchestrator for phase management |
| **Decentralized** | Need fault tolerance, parallel execution | Agent swarms for implementation |
| **Hierarchical** | Complex tasks with clear decomposition | Global planner -> Skill -> Executor |

### Coopetition Pattern

**Agents compete on alternatives, cooperate on consensus:**

```python
def coopetition_decision(agents, decision_point):
    """
    Competition phase: Generate diverse alternatives
    Cooperation phase: Reach consensus on best option
    """
    # COMPETITION: Each agent proposes solution independently
    proposals = []
    for agent in agents:
        proposal = agent.propose(
            decision_point,
            visibility="blind"  # No peeking at other proposals
        )
        proposals.append(proposal)

    # COOPERATION: Collaborative evaluation
    if len(set(p.approach for p in proposals)) == 1:
        # Unanimous - likely good solution
        return proposals[0]

    # Multiple approaches - structured debate
    for proposal in proposals:
        proposal.pros = evaluate_pros(proposal)
        proposal.cons = evaluate_cons(proposal)
        proposal.evidence = gather_evidence(proposal)

    # Vote with reasoning requirement
    winner = ranked_choice_vote(
        proposals,
        require_justification=True
    )

    return winner
```

---

## Progressive Complexity Escalation

**Start simple, escalate only when needed:**

```
Level 1: Single Agent, Direct Execution
   |
   +-- Success? --> Done
   |
   +-- Failure? --> Escalate
           |
           v
Level 2: Single Agent + Self-Verification Loop
   |
   +-- Success? --> Done
   |
   +-- Failure after 3 attempts? --> Escalate
           |
           v
Level 3: Multi-Agent Review
   |
   +-- Success? --> Done
   |
   +-- Persistent issues? --> Escalate
           |
           v
Level 4: Hierarchical Planning + Decomposition
   |
   +-- Success? --> Done
   |
   +-- Fundamental blocker? --> Human escalation
```

---

## Key Research Findings Summary

### What Works

1. **Heterogeneous teams** outperform homogeneous by 4-6%
2. **Iter-VF** (verify answer only) prevents context overflow
3. **Episodic-to-semantic consolidation** enables genuine learning
4. **Anti-sycophancy measures** (blind review, devil's advocate) improve accuracy 30%+
5. **Global planning** with local execution improves success rate 12%+

### What Doesn't Work

1. **Deep debate chains** - diminishing returns after 1-2 rounds
2. **Confidence visibility** - causes over-confidence cascades
3. **Full reasoning chain review** - leads to error accumulation
4. **Homogeneous reviewer teams** - miss diverse failure modes
5. **Over-engineered orchestration** - model upgrades outpace gains

---

## Sources

- [Multi-Agent Collaboration Mechanisms Survey](https://arxiv.org/abs/2501.06322)
- [CONSENSAGENT: Anti-Sycophancy Framework](https://aclanthology.org/2025.findings-acl.1141/)
- [GoalAct: Global Planning + Hierarchical Execution](https://arxiv.org/abs/2504.16563)
- [A-Mem: Agentic Memory System](https://arxiv.org/html/2502.12110v11)
- [Multi-Agent Reflexion (MAR)](https://arxiv.org/html/2512.20845)
- [Iter-VF: Iterative Verification-First](https://arxiv.org/html/2511.21734v1)
- [Awesome Agentic Patterns](https://github.com/nibzard/awesome-agentic-patterns)

---

## Reference: Agent Types

# Agent Types Reference

Complete definitions and capabilities for all 37 specialized agent types.

---

## Overview

Loki Mode has 37 predefined agent types organized into 7 specialized swarms. The orchestrator spawns only the agents needed for your project - a simple app might use 5-10 agents, while a complex startup could spawn 100+ agents working in parallel.

---

## Engineering Swarm (8 types)

| Agent | Capabilities |
|-------|-------------|
| `eng-frontend` | React/Vue/Svelte, TypeScript, Tailwind, accessibility, responsive design, state management |
| `eng-backend` | Node/Python/Go, REST/GraphQL, auth, business logic, middleware, validation |
| `eng-database` | PostgreSQL/MySQL/MongoDB, migrations, query optimization, indexing, backups |
| `eng-mobile` | React Native/Flutter/Swift/Kotlin, offline-first, push notifications, app store prep |
| `eng-api` | OpenAPI specs, SDK generation, versioning, webhooks, rate limiting, documentation |
| `eng-qa` | Unit/integration/E2E tests, coverage, automation, test data management |
| `eng-perf` | Profiling, benchmarking, optimization, caching, load testing, memory analysis |
| `eng-infra` | Docker, K8s manifests, IaC review, networking, security hardening |

---

## Operations Swarm (8 types)

| Agent | Capabilities |
|-------|-------------|
| `ops-devops` | CI/CD pipelines, GitHub Actions, GitLab CI, Jenkins, build optimization |
| `ops-sre` | Reliability, SLOs/SLIs, capacity planning, on-call, runbooks |
| `ops-security` | SAST/DAST, pen testing, vulnerability management, security reviews |
| `ops-monitor` | Observability, Datadog/Grafana, alerting, dashboards, log aggregation |
| `ops-incident` | Incident response, runbooks, RCA, post-mortems, communication |
| `ops-release` | Versioning, changelogs, blue-green, canary, rollbacks, feature flags |
| `ops-cost` | Cloud cost optimization, right-sizing, FinOps, reserved instances |
| `ops-compliance` | SOC2, GDPR, HIPAA, PCI-DSS, audit preparation, policy enforcement |

---

## Business Swarm (8 types)

| Agent | Capabilities |
|-------|-------------|
| `biz-marketing` | Landing pages, SEO, content, email campaigns, social media |
| `biz-sales` | CRM setup, outreach, demos, proposals, pipeline management |
| `biz-finance` | Billing (Stripe), invoicing, metrics, runway, pricing strategy |
| `biz-legal` | ToS, privacy policy, contracts, IP protection, compliance docs |
| `biz-support` | Help docs, FAQs, ticket system, chatbot, knowledge base |
| `biz-hr` | Job posts, recruiting, onboarding, culture docs, team structure |
| `biz-investor` | Pitch decks, investor updates, data room, cap table management |
| `biz-partnerships` | BD outreach, integration partnerships, co-marketing, API partnerships |

---

## Data Swarm (3 types)

| Agent | Capabilities |
|-------|-------------|
| `data-ml` | Model training, MLOps, feature engineering, inference, model monitoring |
| `data-eng` | ETL pipelines, data warehousing, dbt, Airflow, data quality |
| `data-analytics` | Product analytics, A/B tests, dashboards, insights, reporting |

---

## Product Swarm (3 types)

| Agent | Capabilities |
|-------|-------------|
| `prod-pm` | Backlog grooming, prioritization, roadmap, specs, stakeholder management |
| `prod-design` | Design system, Figma, UX patterns, prototypes, user research |
| `prod-techwriter` | API docs, guides, tutorials, release notes, developer experience |

---

## Growth Swarm (4 types)

| Agent | Capabilities |
|-------|-------------|
| `growth-hacker` | Growth experiments, viral loops, referral programs, acquisition |
| `growth-community` | Community building, Discord/Slack, ambassador programs, events |
| `growth-success` | Customer success, health scoring, churn prevention, expansion |
| `growth-lifecycle` | Email lifecycle, in-app messaging, re-engagement, onboarding |

---

## Review Swarm (3 types)

| Agent | Capabilities |
|-------|-------------|
| `review-code` | Code quality, design patterns, SOLID, maintainability, best practices |
| `review-business` | Requirements alignment, business logic, edge cases, UX flows |
| `review-security` | Vulnerabilities, auth/authz, OWASP Top 10, data protection |

---

## Agent Execution Model

**Claude Code does NOT support background processes.** Agents execute via:

1. **Role Switching (Recommended):** Orchestrator maintains agent queue, switches roles per task
2. **Sequential:** Execute agents one at a time (simple, reliable)
3. **Parallel via tmux:** Multiple Claude Code sessions (complex, faster)

```bash
# Option 1: Sequential (simple, reliable)
for agent in frontend backend database; do
  claude -p "Act as $agent agent..." --dangerously-skip-permissions
done

# Option 2: Parallel via tmux (complex, faster)
tmux new-session -d -s loki-pool
for i in {1..5}; do
  tmux new-window -t loki-pool -n "agent-$i" \
    "claude --dangerously-skip-permissions -p '$(cat .loki/prompts/agent-$i.md)'"
done

# Option 3: Role switching (recommended)
# Orchestrator maintains agent queue, switches roles per task
```

---

## Model Selection by Agent Type

| Task Type | Model | Reason |
|-----------|-------|--------|
| Implementation | Sonnet | Fast, good enough for coding |
| Code Review | Opus | Deep analysis, catches subtle issues |
| Security Review | Opus | Critical, needs thoroughness |
| Business Logic Review | Opus | Needs to understand requirements deeply |
| Documentation | Sonnet | Straightforward writing |
| Quick fixes | Haiku | Fast iteration |

---

## Agent Lifecycle

```
SPAWN -> INITIALIZE -> POLL_QUEUE -> CLAIM_TASK -> EXECUTE -> REPORT -> POLL_QUEUE
           |              |                        |          |
           |         circuit open?             timeout?    success?
           |              |                        |          |
           v              v                        v          v
     Create state    WAIT_BACKOFF              RELEASE    UPDATE_STATE
                          |                    + RETRY         |
                     exponential                              |
                       backoff                                v
                                                    NO_TASKS --> IDLE (5min)
                                                                    |
                                                             idle > 30min?
                                                                    |
                                                                    v
                                                               TERMINATE
```

---

## Dynamic Scaling Rules

| Condition | Action | Cooldown |
|-----------|--------|----------|
| Queue depth > 20 | Spawn 2 agents of bottleneck type | 5min |
| Queue depth > 50 | Spawn 5 agents, alert orchestrator | 2min |
| Agent idle > 30min | Terminate agent | - |
| Agent failed 3x consecutive | Terminate, open circuit breaker | 5min |
| Critical task waiting > 10min | Spawn priority agent | 1min |
| Circuit breaker half-open | Spawn 1 test agent | - |
| All agents of type failed | HALT, request human intervention | - |

---

## Agent Context Preservation

### Lineage Rules
1. **Immutable Inheritance:** Agents CANNOT modify inherited context
2. **Decision Logging:** All decisions MUST be logged to agent context file
3. **Lineage Reference:** All commits MUST reference parent agent ID
4. **Context Handoff:** When agent completes, context is archived but lineage preserved

### Preventing Context Drift
1. Read `.agent/sub-agents/${parent_id}.json` before spawning
2. Inherit immutable context (tech stack, constraints, decisions)
3. Log all new decisions to own context file
4. Reference lineage in all commits
5. Periodic context sync: check if inherited context has been updated upstream

---

## Reference: Agents

# Agent Type Definitions

Complete specifications for all 37 specialized agent types in the Loki Mode multi-agent system.

**Note:** These are agent TYPE definitions, not a fixed count. Loki Mode dynamically spawns agents based on project needs - a simple todo app might use 5-10 agents, while a complex startup could spawn 100+ agents working in parallel.

## Agent Role Prompt Template

Each agent receives a role prompt stored in `.loki/prompts/{agent-type}.md`:

```markdown
# Agent Identity

You are **{AGENT_TYPE}** agent with ID **{AGENT_ID}**.

## Your Capabilities
{CAPABILITY_LIST}

## Your Constraints
- Only claim tasks matching your capabilities
- Always verify before assuming (web search, test code)
- Checkpoint state before major operations
- Report blockers within 15 minutes if stuck
- Log all decisions with reasoning

## Task Execution Loop
1. Read `.loki/queue/pending.json`
2. Find task where `type` matches your capabilities
3. Acquire task lock (atomic claim)
4. Execute task following your capability guidelines
5. Write result to `.loki/messages/outbox/{AGENT_ID}/`
6. Update `.loki/state/agents/{AGENT_ID}.json`
7. Mark task complete or failed
8. Return to step 1

## Communication
- Inbox: `.loki/messages/inbox/{AGENT_ID}/`
- Outbox: `.loki/messages/outbox/{AGENT_ID}/`
- Broadcasts: `.loki/messages/broadcast/`

## State File
Location: `.loki/state/agents/{AGENT_ID}.json`
Update after every task completion.
```

---

## Engineering Swarm (8 Agents)

### eng-frontend
**Capabilities:**
- React, Vue, Svelte, Next.js, Nuxt, SvelteKit
- TypeScript, JavaScript
- Tailwind, CSS Modules, styled-components
- Responsive design, mobile-first
- Accessibility (WCAG 2.1 AA)
- Performance optimization (Core Web Vitals)

**Task Types:**
- `ui-component`: Build UI component
- `page-layout`: Create page layout
- `styling`: Implement designs
- `accessibility-fix`: Fix a11y issues
- `frontend-perf`: Optimize bundle, lazy loading

**Quality Checks:**
- Lighthouse score > 90
- No console errors
- Cross-browser testing (Chrome, Firefox, Safari)
- Mobile responsive verification

---

### eng-backend
**Capabilities:**
- Node.js, Python, Go, Rust, Java
- REST API, GraphQL, gRPC
- Authentication (OAuth, JWT, sessions)
- Authorization (RBAC, ABAC)
- Caching (Redis, Memcached)
- Message queues (RabbitMQ, SQS, Kafka)

**Task Types:**
- `api-endpoint`: Implement API endpoint
- `service`: Build microservice
- `integration`: Third-party API integration
- `auth`: Authentication/authorization
- `business-logic`: Core business rules

**Quality Checks:**
- API response < 100ms p99
- Input validation on all endpoints
- Error handling with proper status codes
- Rate limiting implemented

---

### eng-database
**Capabilities:**
- PostgreSQL, MySQL, MongoDB, Redis
- Schema design, normalization
- Migrations (Prisma, Drizzle, Knex, Alembic)
- Query optimization, indexing
- Replication, sharding strategies
- Backup and recovery

**Task Types:**
- `schema-design`: Design database schema
- `migration`: Create migration
- `query-optimize`: Optimize slow queries
- `index`: Add/optimize indexes
- `data-seed`: Create seed data

**Quality Checks:**
- No N+1 queries
- All queries use indexes (EXPLAIN ANALYZE)
- Migrations are reversible
- Foreign keys enforced

---

### eng-mobile
**Capabilities:**
- React Native, Flutter, Swift, Kotlin
- Cross-platform strategies
- Native modules, platform-specific code
- Push notifications
- Offline-first, local storage
- App store deployment

**Task Types:**
- `mobile-screen`: Implement screen
- `native-feature`: Camera, GPS, biometrics
- `offline-sync`: Offline data handling
- `push-notification`: Notification system
- `app-store`: Prepare store submission

**Quality Checks:**
- 60fps smooth scrolling
- App size < 50MB
- Cold start < 3s
- Memory efficient

---

### eng-api
**Capabilities:**
- OpenAPI/Swagger specification
- API versioning strategies
- SDK generation
- Rate limiting design
- Webhook systems
- API documentation

**Task Types:**
- `api-spec`: Write OpenAPI spec
- `sdk-generate`: Generate client SDKs
- `webhook`: Implement webhook system
- `api-docs`: Generate documentation
- `versioning`: Implement API versioning

**Quality Checks:**
- 100% endpoint documentation
- All errors have consistent format
- SDK tests pass
- Postman collection updated

---

### eng-qa
**Capabilities:**
- Unit testing (Jest, pytest, Go test)
- Integration testing
- E2E testing (Playwright, Cypress)
- Load testing (k6, Artillery)
- Fuzz testing
- Test automation

**Task Types:**
- `unit-test`: Write unit tests
- `integration-test`: Write integration tests
- `e2e-test`: Write E2E tests
- `load-test`: Performance/load testing
- `test-coverage`: Increase coverage

**Quality Checks:**
- Coverage > 80%
- All critical paths tested
- No flaky tests
- CI passes consistently

---

### eng-perf
**Capabilities:**
- Application profiling (CPU, memory, I/O)
- Performance benchmarking
- Bottleneck identification
- Caching strategy (Redis, CDN, in-memory)
- Database query optimization
- Bundle size optimization
- Core Web Vitals optimization

**Task Types:**
- `profile`: Profile application performance
- `benchmark`: Create performance benchmarks
- `optimize`: Optimize identified bottleneck
- `cache-strategy`: Design/implement caching
- `bundle-optimize`: Reduce bundle/binary size

**Quality Checks:**
- p99 latency < target
- Memory usage stable (no leaks)
- Benchmarks documented and reproducible
- Before/after metrics recorded

---

### eng-infra
**Capabilities:**
- Dockerfile creation and optimization
- Kubernetes manifest review
- Helm chart development
- Infrastructure as Code review
- Container security
- Multi-stage builds
- Resource limits and requests

**Task Types:**
- `dockerfile`: Create/optimize Dockerfile
- `k8s-manifest`: Write K8s manifests
- `helm-chart`: Develop Helm charts
- `iac-review`: Review Terraform/Pulumi code
- `container-security`: Harden containers

**Quality Checks:**
- Images use minimal base
- No secrets in images
- Resource limits set
- Health checks defined

---

## Operations Swarm (8 Agents)

### ops-devops
**Capabilities:**
- CI/CD (GitHub Actions, GitLab CI, Jenkins)
- Infrastructure as Code (Terraform, Pulumi, CDK)
- Container orchestration (Docker, Kubernetes)
- Cloud platforms (AWS, GCP, Azure)
- GitOps (ArgoCD, Flux)

**Task Types:**
- `ci-pipeline`: Set up CI pipeline
- `cd-pipeline`: Set up CD pipeline
- `infrastructure`: Provision infrastructure
- `container`: Dockerize application
- `k8s`: Kubernetes manifests/Helm charts

**Quality Checks:**
- Pipeline runs < 10min
- Zero-downtime deployments
- Infrastructure is reproducible
- Secrets properly managed

---

### ops-security
**Capabilities:**
- SAST (static analysis)
- DAST (dynamic analysis)
- Dependency scanning
- Container scanning
- Penetration testing
- Compliance (SOC2, GDPR, HIPAA)

**Task Types:**
- `security-scan`: Run security scans
- `vulnerability-fix`: Fix vulnerabilities
- `penetration-test`: Conduct pen test
- `compliance-check`: Verify compliance
- `security-policy`: Implement security policies

**Quality Checks:**
- Zero high/critical vulnerabilities
- All secrets in vault
- HTTPS everywhere
- Input sanitization verified

---

### ops-monitor
**Capabilities:**
- Observability (Datadog, New Relic, Grafana)
- Logging (ELK, Loki)
- Tracing (Jaeger, Zipkin)
- Alerting rules
- SLO/SLI definition
- Dashboards

**Task Types:**
- `monitoring-setup`: Set up monitoring
- `dashboard`: Create dashboard
- `alert-rule`: Define alert rules
- `log-pipeline`: Configure logging
- `tracing`: Implement distributed tracing

**Quality Checks:**
- All services have health checks
- Critical paths have alerts
- Logs are structured JSON
- Traces cover full request lifecycle

---

### ops-incident
**Capabilities:**
- Incident detection
- Runbook creation
- Auto-remediation scripts
- Root cause analysis
- Post-mortem documentation
- On-call management

**Task Types:**
- `runbook`: Create runbook
- `auto-remediation`: Script auto-fix
- `incident-response`: Handle incident
- `rca`: Root cause analysis
- `postmortem`: Write postmortem

**Quality Checks:**
- MTTR < 30min for P1
- All incidents have RCA
- Runbooks are tested
- Auto-remediation success > 80%

---

### ops-release
**Capabilities:**
- Semantic versioning
- Changelog generation
- Release notes
- Feature flags
- Blue-green deployments
- Canary releases
- Rollback procedures

**Task Types:**
- `version-bump`: Version release
- `changelog`: Generate changelog
- `feature-flag`: Implement feature flag
- `canary`: Canary deployment
- `rollback`: Execute rollback

**Quality Checks:**
- All releases tagged
- Changelog accurate
- Rollback tested
- Feature flags documented

---

### ops-cost
**Capabilities:**
- Cloud cost analysis
- Resource right-sizing
- Reserved instance planning
- Spot instance strategies
- Cost allocation tags
- Budget alerts

**Task Types:**
- `cost-analysis`: Analyze spending
- `right-size`: Optimize resources
- `spot-strategy`: Implement spot instances
- `budget-alert`: Set up alerts
- `cost-report`: Generate cost report

**Quality Checks:**
- Monthly cost within budget
- No unused resources
- All resources tagged
- Cost per user tracked

---

### ops-sre
**Capabilities:**
- Site Reliability Engineering
- SLO/SLI/SLA definition
- Error budgets
- Capacity planning
- Chaos engineering
- Toil reduction
- On-call procedures

**Task Types:**
- `slo-define`: Define SLOs and SLIs
- `error-budget`: Track and manage error budgets
- `capacity-plan`: Plan for scale
- `chaos-test`: Run chaos experiments
- `toil-reduce`: Automate manual processes

**Quality Checks:**
- SLOs documented and measured
- Error budget not exhausted
- Capacity headroom > 30%
- Chaos tests pass

---

### ops-compliance
**Capabilities:**
- SOC 2 Type II preparation
- GDPR compliance
- HIPAA compliance
- PCI-DSS compliance
- ISO 27001
- Audit preparation
- Policy documentation

**Task Types:**
- `compliance-assess`: Assess current compliance state
- `policy-write`: Write security policies
- `control-implement`: Implement required controls
- `audit-prep`: Prepare for external audit
- `evidence-collect`: Gather compliance evidence

**Quality Checks:**
- All required policies documented
- Controls implemented and tested
- Evidence organized and accessible
- Audit findings addressed

---

## Business Swarm (8 Agents)

### biz-marketing
**Capabilities:**
- Landing page copy
- SEO optimization
- Content marketing
- Email campaigns
- Social media content
- Analytics tracking

**Task Types:**
- `landing-page`: Create landing page
- `seo`: Optimize for search
- `blog-post`: Write blog post
- `email-campaign`: Create email sequence
- `social-content`: Social media posts

**Quality Checks:**
- Core Web Vitals pass
- Meta tags complete
- Analytics tracking verified
- A/B tests running

---

### biz-sales
**Capabilities:**
- CRM setup (HubSpot, Salesforce)
- Sales pipeline design
- Outreach templates
- Demo scripts
- Proposal generation
- Contract management

**Task Types:**
- `crm-setup`: Configure CRM
- `outreach`: Create outreach sequence
- `demo-script`: Write demo script
- `proposal`: Generate proposal
- `pipeline`: Design sales pipeline

**Quality Checks:**
- CRM data clean
- Follow-up automation working
- Proposals branded correctly
- Pipeline stages defined

---

### biz-finance
**Capabilities:**
- Billing system setup (Stripe, Paddle)
- Invoice generation
- Revenue recognition
- Runway calculation
- Financial reporting
- Pricing strategy

**Task Types:**
- `billing-setup`: Configure billing
- `pricing`: Define pricing tiers
- `invoice`: Generate invoices
- `financial-report`: Create report
- `runway`: Calculate runway

**Quality Checks:**
- PCI compliance
- Invoices accurate
- Metrics tracked (MRR, ARR, churn)
- Runway > 6 months

---

### biz-legal
**Capabilities:**
- Terms of Service
- Privacy Policy
- Cookie Policy
- GDPR compliance
- Contract templates
- IP protection

**Task Types:**
- `tos`: Generate Terms of Service
- `privacy-policy`: Create privacy policy
- `gdpr`: Implement GDPR compliance
- `contract`: Create contract template
- `compliance`: Verify legal compliance

**Quality Checks:**
- All policies published
- Cookie consent implemented
- Data deletion capability
- Contracts reviewed

---

### biz-support
**Capabilities:**
- Help documentation
- FAQ creation
- Chatbot setup
- Ticket system
- Knowledge base
- User onboarding

**Task Types:**
- `help-docs`: Write documentation
- `faq`: Create FAQ
- `chatbot`: Configure chatbot
- `ticket-system`: Set up support
- `onboarding`: Design user onboarding

**Quality Checks:**
- All features documented
- FAQ covers common questions
- Response time < 4h
- Onboarding completion > 80%

---

### biz-hr
**Capabilities:**
- Job description writing
- Recruiting pipeline setup
- Interview process design
- Onboarding documentation
- Culture documentation
- Employee handbook
- Performance review templates

**Task Types:**
- `job-post`: Write job description
- `recruiting-setup`: Set up recruiting pipeline
- `interview-design`: Design interview process
- `onboarding-docs`: Create onboarding materials
- `culture-docs`: Document company culture

**Quality Checks:**
- Job posts are inclusive and clear
- Interview process documented
- Onboarding covers all essentials
- Policies are compliant

---

### biz-investor
**Capabilities:**
- Pitch deck creation
- Investor update emails
- Data room preparation
- Cap table management
- Financial modeling
- Due diligence preparation
- Term sheet review

**Task Types:**
- `pitch-deck`: Create/update pitch deck
- `investor-update`: Write monthly update
- `data-room`: Prepare data room
- `financial-model`: Build financial model
- `dd-prep`: Prepare for due diligence

**Quality Checks:**
- Metrics accurate and sourced
- Narrative compelling and clear
- Data room organized
- Financials reconciled

---

### biz-partnerships
**Capabilities:**
- Partnership outreach
- Integration partnerships
- Co-marketing agreements
- Channel partnerships
- API partnership programs
- Partner documentation
- Revenue sharing models

**Task Types:**
- `partner-outreach`: Identify and reach partners
- `integration-partner`: Technical integration partnership
- `co-marketing`: Plan co-marketing campaign
- `partner-docs`: Create partner documentation
- `partner-program`: Design partner program

**Quality Checks:**
- Partners aligned with strategy
- Agreements documented
- Integration tested
- ROI tracked

---

## Data Swarm (3 Agents)

### data-ml
**Capabilities:**
- Machine learning model development
- MLOps and model deployment
- Feature engineering
- Model training and tuning
- A/B testing for ML models
- Model monitoring
- LLM integration and prompting

**Task Types:**
- `model-train`: Train ML model
- `model-deploy`: Deploy model to production
- `feature-eng`: Engineer features
- `model-monitor`: Set up model monitoring
- `llm-integrate`: Integrate LLM capabilities

**Quality Checks:**
- Model performance meets threshold
- Training reproducible
- Model versioned
- Monitoring alerts configured

---

### data-eng
**Capabilities:**
- ETL pipeline development
- Data warehousing (Snowflake, BigQuery, Redshift)
- dbt transformations
- Airflow/Dagster orchestration
- Data quality checks
- Schema design
- Data governance

**Task Types:**
- `etl-pipeline`: Build ETL pipeline
- `dbt-model`: Create dbt model
- `data-quality`: Implement data quality checks
- `warehouse-design`: Design warehouse schema
- `pipeline-monitor`: Monitor data pipelines

**Quality Checks:**
- Pipelines idempotent
- Data freshness SLA met
- Quality checks passing
- Documentation complete

---

### data-analytics
**Capabilities:**
- Business intelligence
- Dashboard creation (Metabase, Looker, Tableau)
- SQL analysis
- Metrics definition
- Self-serve analytics
- Data storytelling

**Task Types:**
- `dashboard`: Create analytics dashboard
- `metrics-define`: Define business metrics
- `analysis`: Perform ad-hoc analysis
- `self-serve`: Set up self-serve analytics
- `report`: Generate business report

**Quality Checks:**
- Metrics clearly defined
- Dashboards performant
- Data accurate
- Insights actionable

---

## Product Swarm (3 Agents)

### prod-pm
**Capabilities:**
- Product requirements documentation
- User story writing
- Backlog grooming and prioritization
- Roadmap planning
- Feature specifications
- Stakeholder communication
- Competitive analysis

**Task Types:**
- `prd-write`: Write product requirements
- `user-story`: Create user stories
- `backlog-groom`: Groom and prioritize backlog
- `roadmap`: Update product roadmap
- `spec`: Write feature specification

**Quality Checks:**
- Requirements clear and testable
- Acceptance criteria defined
- Priorities justified
- Stakeholders aligned

---

### prod-design
**Capabilities:**
- Design system creation
- UI/UX patterns
- Figma prototyping
- Accessibility design
- User research synthesis
- Design documentation
- Component library

**Task Types:**
- `design-system`: Create/update design system
- `prototype`: Create Figma prototype
- `ux-pattern`: Define UX pattern
- `accessibility`: Ensure accessible design
- `component`: Design component

**Quality Checks:**
- Design system consistent
- Prototypes tested
- WCAG compliant
- Components documented

---

### prod-techwriter
**Capabilities:**
- API documentation
- User guides and tutorials
- Release notes
- README files
- Architecture documentation
- Runbooks
- Knowledge base articles

**Task Types:**
- `api-docs`: Write API documentation
- `user-guide`: Create user guide
- `release-notes`: Write release notes
- `tutorial`: Create tutorial
- `architecture-doc`: Document architecture

**Quality Checks:**
- Documentation accurate
- Examples work
- Searchable and organized
- Up to date with code

---

## Review Swarm (3 Agents)

### review-code
**Capabilities:**
- Code quality assessment
- Design pattern recognition
- SOLID principles verification
- Code smell detection
- Maintainability scoring
- Duplication detection
- Complexity analysis

**Task Types:**
- `review-code`: Full code review
- `review-pr`: Pull request review
- `review-refactor`: Review refactoring changes

**Review Output Format:**
```json
{
  "strengths": ["Well-structured modules", "Good test coverage"],
  "issues": [
    {
      "severity": "Medium",
      "description": "Function exceeds 50 lines",
      "location": "src/auth.js:45",
      "suggestion": "Extract validation logic to separate function"
    }
  ],
  "assessment": "PASS|FAIL"
}
```

**Model:** opus (required for deep analysis)

---

### review-business
**Capabilities:**
- Requirements alignment verification
- Business logic correctness
- Edge case identification
- User flow validation
- Acceptance criteria checking
- Domain model accuracy

**Task Types:**
- `review-business`: Business logic review
- `review-requirements`: Requirements alignment check
- `review-edge-cases`: Edge case analysis

**Review Focus:**
- Does implementation match PRD requirements?
- Are all acceptance criteria met?
- Are edge cases handled?
- Is domain logic correct?

**Model:** opus (required for requirements understanding)

---

### review-security
**Capabilities:**
- Vulnerability detection
- Authentication review
- Authorization verification
- Input validation checking
- Secret exposure detection
- Dependency vulnerability scanning
- OWASP Top 10 checking

**Task Types:**
- `review-security`: Full security review
- `review-auth`: Authentication/authorization review
- `review-input`: Input validation review

**Critical Issues (Always FAIL):**
- Hardcoded secrets/credentials
- SQL injection vulnerabilities
- XSS vulnerabilities
- Missing authentication
- Broken access control
- Sensitive data exposure

**Model:** opus (required for security analysis)

---

## Growth Swarm (4 Agents)

### growth-hacker
**Capabilities:**
- Growth experiment design
- Viral loop optimization
- Referral program design
- Activation optimization
- Retention strategies
- Churn prediction
- PLG (Product-Led Growth) tactics

**Task Types:**
- `growth-experiment`: Design growth experiment
- `viral-loop`: Optimize viral coefficient
- `referral-program`: Design referral system
- `activation`: Improve activation rate
- `retention`: Implement retention tactics

**Quality Checks:**
- Experiments statistically valid
- Metrics tracked
- Results documented
- Winners implemented

---

### growth-community
**Capabilities:**
- Community building
- Discord/Slack community management
- User-generated content programs
- Ambassador programs
- Community events
- Feedback collection
- Community analytics

**Task Types:**
- `community-setup`: Set up community platform
- `ambassador`: Create ambassador program
- `event`: Plan community event
- `ugc`: Launch UGC program
- `feedback-loop`: Implement feedback collection

**Quality Checks:**
- Community guidelines published
- Engagement metrics tracked
- Feedback actioned
- Community health monitored

---

### growth-success
**Capabilities:**
- Customer success workflows
- Health scoring
- Churn prevention
- Expansion revenue
- QBR (Quarterly Business Review)
- Customer journey mapping
- NPS and CSAT programs

**Task Types:**
- `health-score`: Implement health scoring
- `churn-prevent`: Churn prevention workflow
- `expansion`: Identify expansion opportunities
- `qbr`: Prepare QBR materials
- `nps`: Implement NPS program

**Quality Checks:**
- Health scores calibrated
- At-risk accounts identified
- NRR (Net Revenue Retention) tracked
- Customer feedback actioned

---

### growth-lifecycle
**Capabilities:**
- Email lifecycle marketing
- In-app messaging
- Push notification strategy
- Behavioral triggers
- Segmentation
- Personalization
- Re-engagement campaigns

**Task Types:**
- `lifecycle-email`: Create lifecycle email sequence
- `in-app`: Implement in-app messaging
- `push`: Design push notification strategy
- `segment`: Create user segments
- `re-engage`: Build re-engagement campaign

**Quality Checks:**
- Messages personalized
- Triggers tested
- Opt-out working
- Performance tracked

---

## Agent Communication Protocol

### Heartbeat (every 60s)
```json
{
  "from": "agent-id",
  "type": "heartbeat",
  "timestamp": "ISO",
  "status": "active|idle|working",
  "currentTask": "task-id|null",
  "metrics": {
    "tasksCompleted": 5,
    "uptime": 3600
  }
}
```

### Task Claim
```json
{
  "from": "agent-id",
  "type": "task-claim",
  "taskId": "uuid",
  "timestamp": "ISO"
}
```

### Task Complete
```json
{
  "from": "agent-id",
  "type": "task-complete",
  "taskId": "uuid",
  "result": "success|failure",
  "output": {},
  "duration": 120,
  "timestamp": "ISO"
}
```

### Blocker
```json
{
  "from": "agent-id",
  "to": "orchestrator",
  "type": "blocker",
  "taskId": "uuid",
  "reason": "string",
  "attemptedSolutions": [],
  "timestamp": "ISO"
}
```

### Scale Request
```json
{
  "from": "orchestrator",
  "type": "scale-request",
  "agentType": "eng-backend",
  "count": 2,
  "reason": "queue-depth",
  "timestamp": "ISO"
}
```

---

## Reference: Business Ops

# Business Operations Reference

Workflows and procedures for business swarm agents.

## Marketing Operations

### Landing Page Checklist
```
[ ] Hero section with clear value proposition
[ ] Problem/solution narrative
[ ] Feature highlights (3-5 key features)
[ ] Social proof (testimonials, logos, stats)
[ ] Pricing section (if applicable)
[ ] FAQ section
[ ] Call-to-action (primary and secondary)
[ ] Footer with legal links
```

### SEO Optimization
```yaml
Technical SEO:
  - meta title: 50-60 characters, include primary keyword
  - meta description: 150-160 characters, compelling
  - canonical URL set
  - robots.txt configured
  - sitemap.xml generated
  - structured data (JSON-LD)
  - Open Graph tags
  - Twitter Card tags

Performance:
  - Largest Contentful Paint < 2.5s
  - First Input Delay < 100ms
  - Cumulative Layout Shift < 0.1
  - Images optimized (WebP, lazy loading)

Content:
  - H1 contains primary keyword
  - H2-H6 hierarchy logical
  - Internal linking strategy
  - Alt text on all images
  - Content length appropriate for intent
```

### Content Calendar Template
```markdown
# Week of [DATE]

## Monday
- [ ] Blog post: [TITLE]
- [ ] Social: LinkedIn announcement

## Wednesday  
- [ ] Email newsletter
- [ ] Social: Twitter thread

## Friday
- [ ] Case study update
- [ ] Social: Feature highlight
```

### Email Sequences

**Onboarding Sequence:**
```
Day 0: Welcome email (immediate)
  - Thank you for signing up
  - Quick start guide link
  - Support contact

Day 1: Getting started
  - First feature tutorial
  - Video walkthrough

Day 3: Value demonstration
  - Success metrics
  - Customer story

Day 7: Check-in
  - How's it going?
  - Feature discovery

Day 14: Advanced features
  - Power user tips
  - Integration options
```

**Abandoned Cart/Trial:**
```
Hour 1: Reminder
Day 1: Benefits recap
Day 3: Testimonial + urgency
Day 7: Final offer
```

---

## Sales Operations

### CRM Pipeline Stages
```
1. Lead (new contact)
2. Qualified (fits ICP, has need)
3. Meeting Scheduled
4. Demo Completed
5. Proposal Sent
6. Negotiation
7. Closed Won / Closed Lost
```

### Qualification Framework (BANT)
```yaml
Budget:
  - What's the allocated budget?
  - Who controls the budget?
  
Authority:
  - Who makes the final decision?
  - Who else is involved?
  
Need:
  - What problem are you solving?
  - What's the impact of not solving it?
  
Timeline:
  - When do you need a solution?
  - What's driving that timeline?
```

### Outreach Template
```markdown
Subject: [Specific pain point] at [Company]

Hi [Name],

I noticed [Company] is [specific observation about their business].

Many [similar role/company type] struggle with [problem], which leads to [negative outcome].

[Product] helps by [specific solution], resulting in [specific benefit with metric].

Would you be open to a 15-minute call to see if this could help [Company]?

Best,
[Name]
```

### Demo Script Structure
```
1. Rapport (2 min)
   - Confirm attendees and roles
   - Agenda overview

2. Discovery (5 min)
   - Confirm pain points
   - Understand current process
   - Success metrics

3. Solution (15 min)
   - Map features to their needs
   - Show don't tell
   - Address specific use cases

4. Social Proof (3 min)
   - Relevant customer stories
   - Metrics and outcomes

5. Pricing/Next Steps (5 min)
   - Present options
   - Answer objections
   - Define next steps
```

---

## Finance Operations

### Billing Setup Checklist (Stripe)
```bash
# Initialize Stripe
npm install stripe

# Required configurations:
- [ ] Products and prices created
- [ ] Customer portal enabled
- [ ] Webhook endpoints configured
- [ ] Tax settings (Stripe Tax or manual)
- [ ] Invoice settings customized
- [ ] Payment methods enabled
- [ ] Fraud protection rules
```

### Webhook Events to Handle
```javascript
const relevantEvents = [
  'customer.subscription.created',
  'customer.subscription.updated', 
  'customer.subscription.deleted',
  'invoice.paid',
  'invoice.payment_failed',
  'payment_intent.succeeded',
  'payment_intent.payment_failed',
  'customer.updated',
  'charge.refunded'
];
```

### Key Metrics Dashboard
```yaml
Revenue Metrics:
  - MRR (Monthly Recurring Revenue)
  - ARR (Annual Recurring Revenue)
  - Net Revenue Retention
  - Expansion Revenue
  - Churn Rate

Customer Metrics:
  - CAC (Customer Acquisition Cost)
  - LTV (Lifetime Value)
  - LTV:CAC Ratio (target: 3:1)
  - Payback Period

Product Metrics:
  - Trial to Paid Conversion
  - Activation Rate
  - Feature Adoption
  - NPS Score
```

### Runway Calculation
```
Monthly Burn = Total Monthly Expenses - Monthly Revenue
Runway (months) = Cash Balance / Monthly Burn

Healthy: > 18 months
Warning: 6-12 months
Critical: < 6 months
```

---

## Legal Operations

### Terms of Service Template Sections
```
1. Acceptance of Terms
2. Description of Service
3. User Accounts and Registration
4. User Conduct and Content
5. Intellectual Property Rights
6. Payment Terms (if applicable)
7. Termination
8. Disclaimers and Limitations
9. Indemnification
10. Dispute Resolution
11. Changes to Terms
12. Contact Information
```

### Privacy Policy Requirements (GDPR)
```
Required Disclosures:
- [ ] Data controller identity
- [ ] Types of data collected
- [ ] Purpose of processing
- [ ] Legal basis for processing
- [ ] Data retention periods
- [ ] Third-party sharing
- [ ] User rights (access, rectification, deletion)
- [ ] Cookie usage
- [ ] International transfers
- [ ] Contact information
- [ ] DPO contact (if applicable)
```

### GDPR Compliance Checklist
```
Data Collection:
- [ ] Consent mechanism implemented
- [ ] Purpose limitation documented
- [ ] Data minimization practiced

User Rights:
- [ ] Right to access (data export)
- [ ] Right to rectification (edit profile)
- [ ] Right to erasure (delete account)
- [ ] Right to portability (download data)
- [ ] Right to object (marketing opt-out)

Technical:
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Access logging
- [ ] Breach notification process
```

### Cookie Consent Implementation
```javascript
// Cookie categories
const cookieCategories = {
  necessary: true,      // Always enabled
  functional: false,    // User preference
  analytics: false,     // Tracking/analytics
  marketing: false      // Advertising
};

// Required: Show banner before non-necessary cookies
// Required: Allow granular control
// Required: Easy withdrawal of consent
// Required: Record consent timestamp
```

---

## Customer Support Operations

### Ticket Priority Matrix
| Priority | Description | Response SLA | Resolution SLA |
|----------|-------------|--------------|----------------|
| P1 - Critical | Service down, data loss | 15 min | 4 hours |
| P2 - High | Major feature broken | 1 hour | 8 hours |
| P3 - Medium | Feature impaired | 4 hours | 24 hours |
| P4 - Low | General questions | 24 hours | 72 hours |

### Response Templates

**Acknowledgment:**
```
Hi [Name],

Thanks for reaching out! I've received your message about [issue summary].

I'm looking into this now and will get back to you within [SLA time].

In the meantime, [helpful resource or workaround if applicable].

Best,
[Agent Name]
```

**Resolution:**
```
Hi [Name],

Great news - I've resolved the issue with [specific problem].

Here's what was happening: [brief explanation]

Here's what I did to fix it: [solution summary]

To prevent this in the future: [if applicable]

Please let me know if you have any questions!

Best,
[Agent Name]
```

### Knowledge Base Structure
```
/help
├── /getting-started
│   ├── quick-start-guide
│   ├── account-setup
│   └── first-steps
├── /features
│   ├── feature-a
│   ├── feature-b
│   └── feature-c
├── /billing
│   ├── plans-and-pricing
│   ├── payment-methods
│   └── invoices
├── /integrations
│   ├── integration-a
│   └── integration-b
├── /troubleshooting
│   ├── common-issues
│   └── error-messages
└── /api
    ├── authentication
    ├── endpoints
    └── examples
```

---

## Analytics Operations

### Event Tracking Plan
```yaml
User Lifecycle:
  - user_signed_up:
      properties: [source, referrer, plan]
  - user_activated:
      properties: [activation_method, time_to_activate]
  - user_converted:
      properties: [plan, trial_length, conversion_path]
  - user_churned:
      properties: [reason, lifetime_value, last_active]

Core Actions:
  - feature_used:
      properties: [feature_name, context]
  - action_completed:
      properties: [action_type, duration, success]
  - error_encountered:
      properties: [error_type, page, context]

Engagement:
  - page_viewed:
      properties: [page_name, referrer, duration]
  - button_clicked:
      properties: [button_name, page, context]
  - search_performed:
      properties: [query, results_count]
```

### A/B Testing Framework
```yaml
Test Structure:
  name: "Homepage CTA Test"
  hypothesis: "Changing CTA from 'Sign Up' to 'Start Free' will increase conversions"
  primary_metric: signup_rate
  secondary_metrics: [time_on_page, bounce_rate]
  
  variants:
    control:
      description: "Original 'Sign Up' button"
      allocation: 50%
    variant_a:
      description: "'Start Free' button"
      allocation: 50%
  
  sample_size: 1000_per_variant
  duration: 14_days
  significance_level: 0.95

Analysis:
  - Calculate conversion rate per variant
  - Run chi-squared test for significance
  - Check for novelty effects
  - Segment by user type if needed
  - Document learnings
```

### Funnel Analysis
```
Signup Funnel:
  1. Landing Page Visit    → 100% (baseline)
  2. Signup Page View      → 40% (60% drop-off)
  3. Form Submitted        → 25% (15% drop-off)
  4. Email Verified        → 20% (5% drop-off)
  5. Onboarding Complete   → 12% (8% drop-off)
  6. First Value Action    → 8% (4% drop-off)

Optimization Targets:
  - Biggest drop: Landing → Signup (improve CTA, value prop)
  - Second biggest: Signup → Submit (simplify form)
```

### Weekly Metrics Report Template
```markdown
# Weekly Metrics Report: [Date Range]

## Key Metrics Summary
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| New Users | X | Y | +Z% |
| Activated Users | X | Y | +Z% |
| Revenue | $X | $Y | +Z% |
| Churn | X% | Y% | -Z% |

## Highlights
- [Positive trend 1]
- [Positive trend 2]

## Concerns
- [Issue 1 and action plan]
- [Issue 2 and action plan]

## Experiments Running
- [Test name]: [current results]

## Next Week Focus
- [Priority 1]
- [Priority 2]
```

---

## Cross-Functional Workflows

### Feature Launch Checklist
```
Pre-Launch:
[ ] Feature complete and tested
[ ] Documentation updated
[ ] Help articles written
[ ] Email announcement drafted
[ ] Social content prepared
[ ] Sales team briefed
[ ] Support team trained
[ ] Analytics events added
[ ] Feature flag ready

Launch:
[ ] Deploy to production
[ ] Enable feature flag (% rollout)
[ ] Send email announcement
[ ] Publish blog post
[ ] Post on social media
[ ] Update changelog

Post-Launch:
[ ] Monitor error rates
[ ] Track feature adoption
[ ] Collect user feedback
[ ] Iterate based on data
```

### Incident Communication Template
```markdown
# [Incident Type] - [Brief Description]

## Status: [Investigating | Identified | Monitoring | Resolved]

## Timeline
- [HH:MM] Issue reported
- [HH:MM] Team engaged
- [HH:MM] Root cause identified
- [HH:MM] Fix deployed
- [HH:MM] Monitoring

## Impact
- Affected: [% of users, specific features]
- Duration: [X hours/minutes]

## Root Cause
[Brief explanation]

## Resolution
[What was done to fix]

## Prevention
[What changes will prevent recurrence]

## Next Update
[Time of next update or "Resolved"]
```

---

## Reference: Core Workflow

# Core Workflow Reference

Full RARV cycle, CONTINUITY.md template, and autonomy rules.

---

## Autonomy Rules

**This system runs with ZERO human intervention.**

### Core Rules
1. **NEVER ask questions** - Do not say "Would you like me to...", "Should I...", or "What would you prefer?"
2. **NEVER wait for confirmation** - Take immediate action. If something needs to be done, do it.
3. **NEVER stop voluntarily** - Continue until completion promise is fulfilled or max iterations reached
4. **NEVER suggest alternatives** - Pick the best option and execute. No "You could also..." or "Alternatively..."
5. **ALWAYS use RARV cycle** - Every action follows the Reason-Act-Reflect-Verify pattern

---

## RARV Cycle (Reason-Act-Reflect-Verify)

**Enhanced with Automatic Self-Verification Loop (Boris Cherny Pattern)**

Every iteration follows this cycle:

```
+-------------------------------------------------------------------+
| REASON: What needs to be done next?                               |
| - READ .loki/CONTINUITY.md first (working memory)                 |
| - READ "Mistakes & Learnings" to avoid past errors                |
| - Check current state in .loki/state/orchestrator.json            |
| - Review pending tasks in .loki/queue/pending.json                |
| - Identify highest priority unblocked task                        |
| - Determine exact steps to complete it                            |
+-------------------------------------------------------------------+
| ACT: Execute the task                                             |
| - Dispatch subagent via Task tool OR execute directly             |
| - Write code, run tests, fix issues                               |
| - Commit changes atomically (git checkpoint)                      |
| - Update queue files (.loki/queue/*.json)                         |
+-------------------------------------------------------------------+
| REFLECT: Did it work? What next?                                  |
| - Verify task success (tests pass, no errors)                     |
| - UPDATE .loki/CONTINUITY.md with progress                        |
| - Update orchestrator state                                       |
| - Check completion promise - are we done?                         |
| - If not done, loop back to REASON                                |
+-------------------------------------------------------------------+
| VERIFY: Let AI test its own work (2-3x quality improvement)       |
| - Run automated tests (unit, integration, E2E)                    |
| - Check compilation/build (no errors or warnings)                 |
| - Verify against spec (.loki/specs/openapi.yaml)                  |
| - Run linters/formatters via post-write hooks                     |
| - Browser/runtime testing if applicable                           |
|                                                                   |
| IF VERIFICATION FAILS:                                            |
|   1. Capture error details (stack trace, logs)                    |
|   2. Analyze root cause                                           |
|   3. UPDATE CONTINUITY.md "Mistakes & Learnings"                  |
|   4. Rollback to last good git checkpoint (if needed)             |
|   5. Apply learning and RETRY from REASON                         |
|                                                                   |
| - If verification passes, mark task complete and continue         |
+-------------------------------------------------------------------+
```

**Key Enhancement:** The VERIFY step creates a feedback loop where the AI:
- Tests every change automatically
- Learns from failures by updating CONTINUITY.md
- Retries with learned context
- Achieves 2-3x quality improvement (Boris Cherny's observed result)

---

## CONTINUITY.md - Working Memory Protocol

**CRITICAL:** You have a persistent working memory file at `.loki/CONTINUITY.md` that maintains state across all turns of execution.

### AT THE START OF EVERY TURN:
1. Read `.loki/CONTINUITY.md` to orient yourself to the current state
2. Reference it throughout your reasoning
3. Never make decisions without checking CONTINUITY.md first

### AT THE END OF EVERY TURN:
1. Update `.loki/CONTINUITY.md` with any important new information
2. Record what was accomplished
3. Note what needs to happen next
4. Document any blockers or decisions made

### CONTINUITY.md Template

```markdown
# Loki Mode Working Memory
Last Updated: [ISO timestamp]
Current Phase: [bootstrap|discovery|architecture|development|qa|deployment|growth]
Current Iteration: [number]

## Active Goal
[What we're currently trying to accomplish - 1-2 sentences]

## Current Task
- ID: [task-id from queue]
- Description: [what we're doing]
- Status: [in-progress|blocked|reviewing]
- Started: [timestamp]

## Just Completed
- [Most recent accomplishment with file:line references]
- [Previous accomplishment]
- [etc - last 5 items]

## Next Actions (Priority Order)
1. [Immediate next step]
2. [Following step]
3. [etc]

## Active Blockers
- [Any current blockers or waiting items]

## Key Decisions This Session
- [Decision]: [Rationale] - [timestamp]

## Mistakes & Learnings (Self-Updating)
**CRITICAL:** When errors occur, agents MUST update this section to prevent repeating mistakes.

### Pattern: Error -> Learning -> Prevention
- **What Failed:** [Specific error that occurred]
- **Why It Failed:** [Root cause analysis]
- **How to Prevent:** [Concrete action to avoid this in future]
- **Timestamp:** [When this was learned]
- **Agent:** [Which agent learned this]

### Example:
- **What Failed:** TypeScript compilation error - missing return type annotation
- **Why It Failed:** Express route handlers need explicit `: void` return type in strict mode
- **How to Prevent:** Always add `: void` to route handlers: `(req, res): void =>`
- **Timestamp:** 2026-01-04T00:16:00Z
- **Agent:** eng-001-backend-api

**Self-Update Protocol:**
```
ON_ERROR:
  1. Capture error details (stack trace, context)
  2. Analyze root cause
  3. Write learning to CONTINUITY.md "Mistakes & Learnings"
  4. Update approach based on learning
  5. Retry with corrected approach
```

## Working Context
[Any critical information needed for current work - API keys in use,
architecture decisions, patterns being followed, etc.]

## Files Currently Being Modified
- [file path]: [what we're changing]
```

---

## Memory Hierarchy

The memory systems work together:

1. **CONTINUITY.md** = Working memory (current session state, updated every turn)
2. **ledgers/** = Agent-specific state (checkpointed periodically)
3. **handoffs/** = Agent-to-agent transfers (on agent switch)
4. **learnings/** = Extracted patterns (on task completion)
5. **rules/** = Permanent validated patterns (promoted from learnings)

**CONTINUITY.md is the PRIMARY source of truth for "what am I doing right now?"**

---

## Git Checkpoint System

**CRITICAL:** Every completed task MUST create a git checkpoint for rollback safety.

### Protocol: Automatic Commits After Task Completion

**RULE:** When `task.status == "completed"`, create a git commit immediately.

```bash
# Git Checkpoint Protocol
ON_TASK_COMPLETE() {
    task_id=$1
    task_title=$2
    agent_id=$3

    # Stage modified files
    git add <modified_files>

    # Create structured commit message
    git commit -m "[Loki] ${agent_type}-${task_id}: ${task_title}

${detailed_description}

Agent: ${agent_id}
Parent: ${parent_agent_id}
Spec: ${spec_reference}
Tests: ${test_files}
Git-Checkpoint: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

    # Store commit SHA in task metadata
    commit_sha=$(git rev-parse HEAD)
    update_task_metadata task_id git_commit_sha "$commit_sha"

    # Update CONTINUITY.md
    echo "- Task $task_id completed (commit: $commit_sha)" >> .loki/CONTINUITY.md
}
```

### Commit Message Format

**Template:**
```
[Loki] ${agent_type}-${task_id}: ${task_title}

${detailed_description}

Agent: ${agent_id}
Parent: ${parent_agent_id}
Spec: ${spec_reference}
Tests: ${test_files}
Git-Checkpoint: ${timestamp}
```

**Example:**
```
[Loki] eng-005-backend: Implement POST /api/todos endpoint

Created todo creation endpoint per OpenAPI spec.
- Input validation for title field
- SQLite insertion with timestamps
- Returns 201 with created todo object
- Contract tests passing

Agent: eng-001-backend-api
Parent: orchestrator-main
Spec: .loki/specs/openapi.yaml#/paths/~1api~1todos/post
Tests: backend/tests/todos.contract.test.ts
Git-Checkpoint: 2026-01-04T05:45:00Z
```

### Rollback Strategy

**When to Rollback:**
- Quality gates fail after merge
- Integration tests fail
- Security vulnerabilities detected
- Breaking changes discovered

**Rollback Command:**
```bash
# Find last good checkpoint
last_good_commit=$(git log --grep="\[Loki\].*task-${last_good_task_id}" --format=%H -n 1)

# Rollback to that checkpoint
git reset --hard $last_good_commit

# Update CONTINUITY.md
echo "ROLLBACK: Reset to task-${last_good_task_id} (commit: $last_good_commit)" >> .loki/CONTINUITY.md

# Re-queue failed tasks
move_tasks_to_pending after_task=$last_good_task_id
```

---

## If Subagent Fails

1. Do NOT try to fix manually (context pollution)
2. Dispatch fix subagent with specific error context
3. If fix subagent fails 3x, move to dead letter queue
4. Open circuit breaker for that agent type
5. Alert orchestrator for human review

---

## Reference: Deployment

# Deployment Reference

Infrastructure provisioning and deployment instructions for all supported platforms.

## Deployment Decision Matrix

| Criteria | Vercel/Netlify | Railway/Render | AWS | GCP | Azure |
|----------|----------------|----------------|-----|-----|-------|
| Static/JAMstack | Best | Good | Overkill | Overkill | Overkill |
| Simple full-stack | Good | Best | Overkill | Overkill | Overkill |
| Scale to millions | No | Limited | Best | Best | Best |
| Enterprise compliance | Limited | Limited | Best | Good | Best |
| Cost at scale | Expensive | Moderate | Cheapest | Cheap | Moderate |
| Setup complexity | Trivial | Easy | Complex | Complex | Complex |

## Quick Start Commands

### Vercel
```bash
# Install CLI
npm i -g vercel

# Deploy (auto-detects framework)
vercel --prod

# Environment variables
vercel env add VARIABLE_NAME production
```

### Netlify
```bash
# Install CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod

# Environment variables
netlify env:set VARIABLE_NAME value
```

### Railway
```bash
# Install CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Environment variables
railway variables set VARIABLE_NAME=value
```

### Render
```yaml
# render.yaml (Infrastructure as Code)
services:
  - type: web
    name: api
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString

databases:
  - name: postgres
    plan: starter
```

---

## AWS Deployment

### Architecture Template
```
┌─────────────────────────────────────────────────────────┐
│                        CloudFront                        │
└─────────────────────────┬───────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
    ┌─────▼─────┐                   ┌─────▼─────┐
    │    S3     │                   │    ALB    │
    │ (static)  │                   │           │
    └───────────┘                   └─────┬─────┘
                                          │
                                    ┌─────▼─────┐
                                    │   ECS     │
                                    │  Fargate  │
                                    └─────┬─────┘
                                          │
                              ┌───────────┴───────────┐
                              │                       │
                        ┌─────▼─────┐           ┌─────▼─────┐
                        │    RDS    │           │ ElastiCache│
                        │ Postgres  │           │   Redis   │
                        └───────────┘           └───────────┘
```

### Terraform Configuration
```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "terraform-state-${var.project_name}"
    key    = "state.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "production"
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# RDS
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.0.0"

  identifier = "${var.project_name}-db"

  engine               = "postgres"
  engine_version       = "15"
  family               = "postgres15"
  major_engine_version = "15"
  instance_class       = var.environment == "production" ? "db.t3.medium" : "db.t3.micro"

  allocated_storage = 20
  storage_encrypted = true

  db_name  = var.db_name
  username = var.db_username
  port     = 5432

  vpc_security_group_ids = [aws_security_group.rds.id]
  subnet_ids             = module.vpc.private_subnets

  backup_retention_period = var.environment == "production" ? 7 : 1
  deletion_protection     = var.environment == "production"
}
```

### ECS Task Definition
```json
{
  "family": "app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "${ECR_REPO}:${TAG}",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "NODE_ENV", "value": "production"}
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:db-url"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

### GitHub Actions CI/CD
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: app
  ECS_SERVICE: app-service
  ECS_CLUSTER: app-cluster

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build, tag, and push image
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: task-definition.json
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
```

---

## GCP Deployment

### Cloud Run (Recommended for most cases)
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/app
gcloud run deploy app \
  --image gcr.io/PROJECT_ID/app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="NODE_ENV=production" \
  --set-secrets="DATABASE_URL=db-url:latest"
```

### Terraform for GCP
```hcl
provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud Run Service
resource "google_cloud_run_service" "app" {
  name     = "app"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/app:latest"
        
        ports {
          container_port = 3000
        }

        env {
          name  = "NODE_ENV"
          value = "production"
        }

        env {
          name = "DATABASE_URL"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.db_url.secret_id
              key  = "latest"
            }
          }
        }

        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.main.connection_name
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Cloud SQL
resource "google_sql_database_instance" "main" {
  name             = "app-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    backup_configuration {
      enabled = true
    }
  }

  deletion_protection = var.environment == "production"
}
```

---

## Azure Deployment

### Azure Container Apps
```bash
# Create resource group
az group create --name app-rg --location eastus

# Create Container Apps environment
az containerapp env create \
  --name app-env \
  --resource-group app-rg \
  --location eastus

# Deploy container
az containerapp create \
  --name app \
  --resource-group app-rg \
  --environment app-env \
  --image myregistry.azurecr.io/app:latest \
  --target-port 3000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10 \
  --env-vars "NODE_ENV=production"
```

---

## Kubernetes Deployment

### Manifests
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: app:latest
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: production
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app
                port:
                  number: 80
```

### Helm Chart Structure
```
chart/
├── Chart.yaml
├── values.yaml
├── values-staging.yaml
├── values-production.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    ├── secret.yaml
    └── hpa.yaml
```

---

## Blue-Green Deployment

### Strategy
```
1. Deploy new version to "green" environment
2. Run smoke tests against green
3. Switch load balancer to green
4. Monitor for 15 minutes
5. If healthy: decommission blue
6. If errors: switch back to blue (rollback)
```

### Implementation (AWS ALB)
```bash
# Deploy green
aws ecs update-service --cluster app --service app-green --task-definition app:NEW_VERSION

# Wait for stability
aws ecs wait services-stable --cluster app --services app-green

# Run smoke tests
curl -f https://green.app.example.com/health

# Switch traffic (update target group weights)
aws elbv2 modify-listener-rule \
  --rule-arn $RULE_ARN \
  --actions '[{"Type":"forward","TargetGroupArn":"'$GREEN_TG'","Weight":100}]'
```

---

## Rollback Procedures

### Immediate Rollback
```bash
# AWS ECS
aws ecs update-service --cluster app --service app --task-definition app:PREVIOUS_VERSION

# Kubernetes
kubectl rollout undo deployment/app

# Vercel
vercel rollback
```

### Automated Rollback Triggers
Monitor these metrics post-deploy:
- Error rate > 1% for 5 minutes
- p99 latency > 500ms for 5 minutes
- Health check failures > 3 consecutive
- Memory usage > 90% for 10 minutes

If any trigger fires, execute automatic rollback.

---

## Secrets Management

### AWS Secrets Manager
```bash
# Create secret
aws secretsmanager create-secret \
  --name app/database-url \
  --secret-string "postgresql://..."

# Reference in ECS task
"secrets": [
  {
    "name": "DATABASE_URL",
    "valueFrom": "arn:aws:secretsmanager:region:account:secret:app/database-url"
  }
]
```

### HashiCorp Vault
```bash
# Store secret
vault kv put secret/app database-url="postgresql://..."

# Read in application
vault kv get -field=database-url secret/app
```

### Environment-Specific
```
.env.development   # Local development
.env.staging       # Staging environment
.env.production    # Production (never commit)
```

All production secrets must be in a secrets manager, never in code or environment files.

---

## Reference: Lab Research Patterns

# Lab Research Patterns Reference

Research-backed patterns from Google DeepMind and Anthropic for enhanced multi-agent orchestration and safety.

---

## Overview

This reference consolidates key patterns from:
1. **Google DeepMind** - World models, self-improvement, scalable oversight
2. **Anthropic** - Constitutional AI, alignment safety, agentic coding

---

## Google DeepMind Patterns

### World Model Training (Dreamer 4)

**Key Insight:** Train agents inside world models for safety and data efficiency.

```yaml
world_model_training:
  principle: "Learn behaviors through simulation, not real environment"
  benefits:
    - 100x less data than real-world training
    - Safe exploration of dangerous actions
    - Faster iteration cycles

  architecture:
    tokenizer: "Compress frames into continuous representation"
    dynamics_model: "Predict next world state given action"
    imagination_training: "RL inside simulated trajectories"

  loki_application:
    - Run agent tasks in isolated containers first
    - Simulate deployment before actual deploy
    - Test error scenarios in sandbox
```

### Self-Improvement Loop (SIMA 2)

**Key Insight:** Use AI to generate tasks and score outcomes for bootstrapped learning.

```python
class SelfImprovementLoop:
    """
    Based on SIMA 2's self-improvement mechanism.
    Gemini-based teacher + learned reward model.
    """

    def __init__(self):
        self.task_generator = "Use LLM to generate varied tasks"
        self.reward_model = "Learned model to score trajectories"
        self.experience_bank = []

    def bootstrap_cycle(self):
        # 1. Generate tasks with estimated rewards
        tasks = self.task_generator.generate(
            domain=current_project,
            difficulty_curriculum=True
        )

        # 2. Execute tasks, accumulate experience
        for task in tasks:
            trajectory = execute(task)
            reward = self.reward_model.score(trajectory)
            self.experience_bank.append((trajectory, reward))

        # 3. Train next generation on experience
        next_agent = train_on_experience(self.experience_bank)

        # 4. Iterate with minimal human intervention
        return next_agent
```

**Loki Mode Application:**
- Generate test scenarios automatically
- Score code quality with learned criteria
- Bootstrap agent training across projects

### Hierarchical Reasoning (Gemini Robotics)

**Key Insight:** Separate high-level planning from low-level execution.

```
+------------------------------------------------------------------+
| EMBODIED REASONING MODEL (Gemini Robotics-ER)                     |
| - Orchestrates activities like a "high-level brain"               |
| - Spatial understanding, planning, logical decisions              |
| - Natively calls tools (search, user functions)                   |
| - Does NOT directly control actions                               |
+------------------------------------------------------------------+
        |
        | High-level insights
        v
+------------------------------------------------------------------+
| VISION-LANGUAGE-ACTION MODEL (Gemini Robotics)                    |
| - "Thinks before taking action"                                   |
| - Generates internal reasoning in natural language                |
| - Decomposes long tasks into simpler segments                     |
| - Directly outputs actions/commands                               |
+------------------------------------------------------------------+
```

**Loki Mode Application:**
- Orchestrator = ER model (planning, tool calls)
- Implementation agents = VLA model (code actions)
- Task decomposition before execution

### Cross-Embodiment Transfer

**Key Insight:** Skills learned by one agent type transfer to others.

```yaml
transfer_learning:
  observation: "Tasks learned on ALOHA2 work on Apollo humanoid"
  mechanism: "Shared action space abstraction"

  loki_application:
    - Patterns learned by frontend agent transfer to mobile agent
    - Testing strategies from QA apply to security testing
    - Deployment scripts generalize across cloud providers

  implementation:
    shared_skills_library: ".loki/memory/skills/"
    abstraction_layer: "Domain-agnostic action primitives"
    transfer_score: "Confidence in skill applicability"
```

### Scalable Oversight via Debate

**Key Insight:** Pit AI capabilities against each other for verification.

```python
async def debate_verification(proposal, max_rounds=2):
    """
    Based on DeepMind's Scalable AI Safety via Doubly-Efficient Debate.
    Use debate to break down verification into manageable sub-tasks.
    """
    # Two equally capable AI critics
    proponent = Agent(role="defender", model="opus")
    opponent = Agent(role="challenger", model="opus")

    debate_log = []

    for round in range(max_rounds):
        # Proponent defends proposal
        defense = await proponent.argue(
            proposal=proposal,
            counter_arguments=debate_log
        )

        # Opponent challenges
        challenge = await opponent.argue(
            proposal=proposal,
            defense=defense,
            goal="find_flaws"
        )

        debate_log.append({
            "round": round,
            "defense": defense,
            "challenge": challenge
        })

        # If opponent cannot find valid flaw, proposal is verified
        if not challenge.has_valid_flaw:
            return VerificationResult(verified=True, debate_log=debate_log)

    # Human reviews remaining disagreements
    return escalate_to_human(debate_log)
```

### Amplified Oversight

**Key Insight:** Use AI to help humans supervise AI beyond human capability.

```yaml
amplified_oversight:
  goal: "Supervision as close as possible to human with complete understanding"

  techniques:
    - "AI explains its reasoning transparently"
    - "AI argues against itself when wrong"
    - "AI cites relevant evidence"
    - "Monitor knows when it doesn't know"

  monitoring_principle:
    when_unsure: "Either reject action OR flag for review"
    never: "Approve uncertain actions silently"
```

---

## Anthropic Patterns

### Constitutional AI Principles

**Key Insight:** Train AI to self-critique based on explicit principles.

```python
class ConstitutionalAI:
    """
    Based on Anthropic's Constitutional AI: Harmlessness from AI Feedback.
    Self-critique and revision based on constitutional principles.
    """

    def __init__(self, constitution):
        self.constitution = constitution  # List of principles

    async def supervised_learning_phase(self, response):
        """Phase 1: Self-critique and revise."""
        # Generate initial response
        initial = response

        # Self-critique against each principle
        critiques = []
        for principle in self.constitution:
            critique = await self.critique(
                response=initial,
                principle=principle,
                prompt=f"Does this response violate: {principle}?"
            )
            critiques.append(critique)

        # Revise based on critiques
        revised = await self.revise(
            response=initial,
            critiques=critiques
        )

        return revised

    async def rlai_phase(self, response_pairs):
        """Phase 2: AI compares responses for constitutional compliance."""
        preferences = []
        for (response_a, response_b) in response_pairs:
            preference = await self.compare(
                a=response_a,
                b=response_b,
                criterion="Which better follows the constitution?"
            )
            preferences.append(preference)

        # Train preference model on AI feedback
        return train_preference_model(preferences)
```

**Loki Mode Constitution Example:**
```yaml
loki_constitution:
  - "Never delete production data without explicit backup"
  - "Never commit secrets or credentials to version control"
  - "Never bypass quality gates for speed"
  - "Always verify tests pass before marking task complete"
  - "Never claim completion without running actual tests"
  - "Prefer simple solutions over clever ones"
  - "Document decisions, not just code"
```

### Sleeper Agent Detection (Defection Probes)

**Key Insight:** Use linear classifiers to detect when agents might misbehave.

```python
class DefectionProbe:
    """
    Based on Anthropic's "Simple probes can catch sleeper agents".
    Linear classifiers detecting anomalous agent behavior.
    """

    def __init__(self):
        self.baseline_behaviors = []
        self.probe = LinearClassifier()

    def train_probe(self, normal_trajectories, defection_examples):
        """
        Train on contrast pairs:
        - Normal agent behavior
        - Examples of defection/misbehavior
        """
        contrast_pairs = create_contrast_pairs(
            normal=normal_trajectories,
            defection=defection_examples
        )
        self.probe.fit(contrast_pairs)

    def check_for_defection(self, agent_action, context):
        """
        Check if action appears anomalous.
        AUROC > 99% achieved in Anthropic's research.
        """
        features = extract_features(agent_action, context)
        defection_probability = self.probe.predict_proba(features)

        if defection_probability > THRESHOLD:
            return DefectionAlert(
                probability=defection_probability,
                action=agent_action,
                recommendation="Flag for human review"
            )
        return None
```

**Loki Mode Application:**
- Monitor agent actions for anomalies
- Flag unusual file access patterns
- Detect attempts to bypass quality gates

### Alignment Faking Awareness

**Key Insight:** Models may strategically comply while preserving hidden preferences.

```yaml
alignment_faking_signals:
  warning_signs:
    - "Agent complies only when it knows it's being monitored"
    - "Agent's reasoning contradicts its final action"
    - "Sudden behavior change when training context mentioned"
    - "Agent attempts to exfiltrate its own weights/state"

  detection_strategy:
    - "Monitor chain-of-thought for rationalization"
    - "Compare behavior in 'free' vs 'monitored' conditions"
    - "Check for attempts to undermine oversight systems"

  mitigation:
    - "Constitutional constraints at training time"
    - "Transparency in reasoning (visible extended thinking)"
    - "Defection probes on intermediate reasoning"
```

### Extended Thinking Levels

**Key Insight:** Allocate computation based on problem complexity.

```yaml
thinking_levels:
  "think":
    computation: "Minimal"
    use_for: "Simple questions, straightforward tasks"

  "think hard":
    computation: "Moderate"
    use_for: "Multi-step problems, code implementation"

  "think harder":
    computation: "Extended"
    use_for: "Complex debugging, architecture decisions"

  "ultrathink":
    computation: "Maximum"
    use_for: "Security analysis, critical system design"

loki_mode_mapping:
  haiku_tasks: "think"
  sonnet_tasks: "think hard"
  opus_tasks: "think harder to ultrathink"
```

### Explore-Plan-Code Pattern

**Key Insight:** Research before planning, plan before coding.

```
+------------------------------------------------------------------+
| PHASE 1: EXPLORE                                                  |
| - Research relevant files                                         |
| - Understand existing patterns                                    |
| - Identify dependencies and constraints                           |
| - NO CODE CHANGES YET                                             |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| PHASE 2: PLAN                                                     |
| - Create detailed implementation plan                             |
| - List all files to modify                                        |
| - Define success criteria                                         |
| - Get checkpoint approval if needed                               |
| - STILL NO CODE CHANGES                                           |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| PHASE 3: CODE                                                     |
| - Execute plan systematically                                     |
| - Test after each file change                                     |
| - Update plan if discoveries require it                           |
| - Verify against success criteria                                 |
+------------------------------------------------------------------+
```

### Context Reset Strategy

**Key Insight:** Fresh context often performs better than accumulated context.

```yaml
context_management:
  problem: "Long sessions accumulate irrelevant information"

  solution:
    trigger_reset:
      - "After completing major task"
      - "When changing domains (backend -> frontend)"
      - "When agent seems confused or repeating errors"

    preserve_across_reset:
      - "CONTINUITY.md (working memory)"
      - "Key decisions made this session"
      - "Current task state"

    discard_on_reset:
      - "Intermediate debugging attempts"
      - "Abandoned approaches"
      - "Superseded plans"
```

### Parallel Instance Pattern

**Key Insight:** Multiple Claude instances with separation of concerns.

```python
async def parallel_instance_pattern(task):
    """
    Run multiple Claude instances for separation of concerns.
    Based on Anthropic's Claude Code best practices.
    """
    # Instance 1: Implementation
    implementer = spawn_instance(
        role="implementer",
        context=implementation_context,
        permissions=["edit", "bash"]
    )

    # Instance 2: Review
    reviewer = spawn_instance(
        role="reviewer",
        context=review_context,
        permissions=["read"]  # Read-only for safety
    )

    # Parallel execution
    implementation = await implementer.execute(task)
    review = await reviewer.review(implementation)

    if review.approved:
        return implementation
    else:
        # Feed review back to implementer for fixes
        fixed = await implementer.fix(review.issues)
        return fixed
```

### Prompt Injection Defense

**Key Insight:** Multi-layer defense against injection attacks.

```yaml
prompt_injection_defense:
  layers:
    layer_1_recognition:
      - "Train to recognize injection patterns"
      - "Detect malicious content in external sources"

    layer_2_context_isolation:
      - "Sandbox external content processing"
      - "Mark user content vs system instructions"

    layer_3_action_validation:
      - "Verify requested actions are authorized"
      - "Block sensitive operations without confirmation"

    layer_4_monitoring:
      - "Log all external content interactions"
      - "Alert on suspicious patterns"

  performance:
    claude_opus_4: "89% attack prevention"
    claude_sonnet_4: "86% attack prevention"
```

---

## Combined Patterns for Loki Mode

### Self-Improving Multi-Agent System

```yaml
combined_approach:
  world_model_training: "Test in simulation before real execution"
  self_improvement: "Bootstrap learning from successful trajectories"
  constitutional_constraints: "Principles-based self-critique"
  debate_verification: "Pit reviewers against each other"
  defection_probes: "Monitor for alignment faking"

  implementation_priority:
    high:
      - Constitutional AI principles in agent prompts
      - Explore-Plan-Code workflow enforcement
      - Context reset triggers

    medium:
      - Self-improvement loop for task generation
      - Debate-based verification for critical changes
      - Cross-embodiment skill transfer

    low:
      - Full world model training
      - Defection probe classifiers
```

---

## Sources

**Google DeepMind:**
- [SIMA 2: Generalist AI Agent](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/)
- [Gemini Robotics 1.5](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/)
- [Dreamer 4: World Model Training](https://danijar.com/project/dreamer4/)
- [Genie 3: World Models](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)
- [Scalable AI Safety via Debate](https://deepmind.google/research/publications/34920/)
- [Amplified Oversight](https://deepmindsafetyresearch.medium.com/human-ai-complementarity-a-goal-for-amplified-oversight-0ad8a44cae0a)
- [Technical AGI Safety Approach](https://arxiv.org/html/2504.01849v1)

**Anthropic:**
- [Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Sleeper Agents Detection](https://www.anthropic.com/research/probes-catch-sleeper-agents)
- [Alignment Faking](https://www.anthropic.com/research/alignment-faking)
- [Visible Extended Thinking](https://www.anthropic.com/research/visible-extended-thinking)
- [Computer Use Safety](https://www.anthropic.com/news/3-5-models-and-computer-use)
- [Sabotage Evaluations](https://www.anthropic.com/research/sabotage-evaluations-for-frontier-models)

---

## Reference: Memory System

# Memory System Reference

Enhanced memory architecture based on 2025 research (MIRIX, A-Mem, MemGPT, AriGraph).

---

## Memory Hierarchy Overview

```
+------------------------------------------------------------------+
| WORKING MEMORY (CONTINUITY.md)                                    |
| - Current session state                                           |
| - Updated every turn                                              |
| - What am I doing right NOW?                                      |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| EPISODIC MEMORY (.loki/memory/episodic/)                         |
| - Specific interaction traces                                     |
| - Full context with timestamps                                    |
| - "What happened when I tried X?"                                 |
+------------------------------------------------------------------+
        |
        v (consolidation)
+------------------------------------------------------------------+
| SEMANTIC MEMORY (.loki/memory/semantic/)                         |
| - Generalized patterns and facts                                  |
| - Context-independent knowledge                                   |
| - "How does X work in general?"                                   |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| PROCEDURAL MEMORY (.loki/memory/skills/)                         |
| - Learned action sequences                                        |
| - Reusable skill templates                                        |
| - "How to do X successfully"                                      |
+------------------------------------------------------------------+
```

---

## Directory Structure

```
.loki/memory/
+-- episodic/
|   +-- 2026-01-06/
|   |   +-- task-001.json      # Full trace of task execution
|   |   +-- task-002.json
|   +-- index.json             # Temporal index for retrieval
|
+-- semantic/
|   +-- patterns.json          # Generalized patterns
|   +-- anti-patterns.json     # What NOT to do
|   +-- facts.json             # Domain knowledge
|   +-- links.json             # Zettelkasten-style connections
|
+-- skills/
|   +-- api-implementation.md  # Skill: How to implement an API
|   +-- test-writing.md        # Skill: How to write tests
|   +-- debugging.md           # Skill: How to debug issues
|
+-- ledgers/                   # Agent-specific checkpoints
|   +-- eng-001.json
|   +-- qa-001.json
|
+-- handoffs/                  # Agent-to-agent transfers
|   +-- handoff-001.json
|
+-- learnings/                 # Extracted from errors
|   +-- 2026-01-06.json

# Related: Metrics System (separate from memory)
# .loki/metrics/
# +-- efficiency/              # Task cost tracking (time, agents, retries)
# +-- rewards/                 # Outcome/efficiency/preference signals
# +-- dashboard.json           # Rolling 7-day metrics summary
# See references/tool-orchestration.md for details
```

---

## Episodic Memory Schema

Each task execution creates an episodic trace:

```json
{
  "id": "ep-2026-01-06-001",
  "task_id": "task-042",
  "timestamp": "2026-01-06T10:30:00Z",
  "duration_seconds": 342,
  "agent": "eng-001-backend",
  "context": {
    "phase": "development",
    "goal": "Implement POST /api/todos endpoint",
    "constraints": ["No third-party deps", "< 200ms response"],
    "files_involved": ["src/routes/todos.ts", "src/db/todos.ts"]
  },
  "action_log": [
    {"t": 0, "action": "read_file", "target": "openapi.yaml"},
    {"t": 5, "action": "write_file", "target": "src/routes/todos.ts"},
    {"t": 120, "action": "run_test", "result": "fail", "error": "missing return type"},
    {"t": 140, "action": "edit_file", "target": "src/routes/todos.ts"},
    {"t": 180, "action": "run_test", "result": "pass"}
  ],
  "outcome": "success",
  "errors_encountered": [
    {
      "type": "TypeScript compilation",
      "message": "Missing return type annotation",
      "resolution": "Added explicit :void to route handler"
    }
  ],
  "artifacts_produced": ["src/routes/todos.ts", "tests/todos.test.ts"],
  "git_commit": "abc123"
}
```

---

## Semantic Memory Schema

Generalized patterns extracted from episodic memory:

```json
{
  "id": "sem-001",
  "pattern": "Express route handlers require explicit return types in strict mode",
  "category": "typescript",
  "conditions": [
    "Using TypeScript strict mode",
    "Writing Express route handlers",
    "Handler doesn't return a value"
  ],
  "correct_approach": "Add `: void` to handler signature: `(req, res): void =>`",
  "incorrect_approach": "Omitting return type annotation",
  "confidence": 0.95,
  "source_episodes": ["ep-2026-01-06-001", "ep-2026-01-05-012"],
  "usage_count": 8,
  "last_used": "2026-01-06T14:00:00Z",
  "links": [
    {"to": "sem-005", "relation": "related_to"},
    {"to": "sem-012", "relation": "supersedes"}
  ]
}
```

---

## Episodic-to-Semantic Consolidation

**When to consolidate:** After task completion, during idle time, at phase boundaries.

```python
def consolidate_episodic_to_semantic():
    """
    Transform specific experiences into general knowledge.
    Based on MemGPT and Voyager research.
    """
    # 1. Load recent episodic memories
    recent_episodes = load_episodes(since=hours_ago(24))

    # 2. Group by similarity
    clusters = cluster_by_similarity(recent_episodes)

    for cluster in clusters:
        if len(cluster) >= 2:  # Pattern appears multiple times
            # 3. Extract common pattern
            pattern = extract_common_pattern(cluster)

            # 4. Validate pattern
            if pattern.confidence >= 0.8:
                # 5. Check if already exists
                existing = find_similar_semantic(pattern)
                if existing:
                    # Update existing with new evidence
                    existing.source_episodes.extend([e.id for e in cluster])
                    existing.confidence = recalculate_confidence(existing)
                    existing.usage_count += 1
                else:
                    # Create new semantic memory
                    save_semantic(pattern)

    # 6. Consolidate anti-patterns from errors
    error_episodes = [e for e in recent_episodes if e.errors_encountered]
    for episode in error_episodes:
        for error in episode.errors_encountered:
            anti_pattern = {
                "what_fails": error.type,
                "why": error.message,
                "prevention": error.resolution,
                "source": episode.id
            }
            save_anti_pattern(anti_pattern)
```

---

## Zettelkasten-Style Linking

Each memory note can link to related notes:

```json
{
  "links": [
    {"to": "sem-005", "relation": "derived_from"},
    {"to": "sem-012", "relation": "contradicts"},
    {"to": "sem-018", "relation": "elaborates"},
    {"to": "sem-023", "relation": "example_of"},
    {"to": "sem-031", "relation": "superseded_by"}
  ]
}
```

### Link Relations

| Relation | Meaning |
|----------|---------|
| `derived_from` | This pattern was extracted from that episode |
| `related_to` | Conceptually similar, often used together |
| `contradicts` | These patterns conflict - need resolution |
| `elaborates` | Provides more detail on the linked pattern |
| `example_of` | Specific instance of a general pattern |
| `supersedes` | This pattern replaces an older one |
| `superseded_by` | This pattern is outdated, use the linked one |

---

## Procedural Memory (Skills)

Reusable action sequences:

```markdown
# Skill: API Endpoint Implementation

## Prerequisites
- OpenAPI spec exists at .loki/specs/openapi.yaml
- Database schema defined

## Steps
1. Read endpoint spec from openapi.yaml
2. Create route handler in src/routes/{resource}.ts
3. Implement request validation using spec schema
4. Implement business logic
5. Add database operations if needed
6. Return response matching spec schema
7. Write contract tests
8. Run tests, verify passing

## Common Errors & Fixes
- Missing return type: Add `: void` to handler
- Schema mismatch: Regenerate types from spec

## Exit Criteria
- All contract tests pass
- Response matches OpenAPI spec
- No TypeScript errors
```

---

## Memory Retrieval

### Retrieval by Similarity

```python
def retrieve_relevant_memory(current_context):
    """
    Retrieve memories relevant to current task.
    Uses semantic similarity + temporal recency.
    """
    query_embedding = embed(current_context.goal)

    # 1. Search semantic memory first
    semantic_matches = vector_search(
        collection="semantic",
        query=query_embedding,
        top_k=5
    )

    # 2. Search episodic memory for similar situations
    episodic_matches = vector_search(
        collection="episodic",
        query=query_embedding,
        top_k=3,
        filters={"outcome": "success"}  # Prefer successful episodes
    )

    # 3. Search skills
    skill_matches = keyword_search(
        collection="skills",
        keywords=extract_keywords(current_context)
    )

    # 4. Combine and rank
    combined = merge_and_rank(
        semantic_matches,
        episodic_matches,
        skill_matches,
        weights={"semantic": 0.5, "episodic": 0.3, "skills": 0.2}
    )

    return combined[:5]  # Return top 5 most relevant
```

### Retrieval Before Task Execution

**CRITICAL:** Before executing any task, retrieve relevant memories:

```python
def before_task_execution(task):
    """
    Inject relevant memories into task context.
    """
    # 1. Retrieve relevant memories
    memories = retrieve_relevant_memory(task)

    # 2. Check for anti-patterns
    anti_patterns = search_anti_patterns(task.action_type)

    # 3. Inject into prompt
    task.context["relevant_patterns"] = [m.summary for m in memories]
    task.context["avoid_these"] = [a.summary for a in anti_patterns]
    task.context["applicable_skills"] = find_skills(task.type)

    return task
```

---

## Ledger System (Agent Checkpoints)

Each agent maintains its own ledger:

```json
{
  "agent_id": "eng-001-backend",
  "last_checkpoint": "2026-01-06T10:00:00Z",
  "tasks_completed": 12,
  "current_task": "task-042",
  "state": {
    "files_modified": ["src/routes/todos.ts"],
    "uncommitted_changes": true,
    "last_git_commit": "abc123"
  },
  "context": {
    "tech_stack": ["express", "typescript", "sqlite"],
    "patterns_learned": ["sem-001", "sem-005"],
    "current_goal": "Implement CRUD for todos"
  }
}
```

---

## Handoff Protocol

When switching between agents:

```json
{
  "id": "handoff-001",
  "from_agent": "eng-001-backend",
  "to_agent": "qa-001-testing",
  "timestamp": "2026-01-06T11:00:00Z",
  "context": {
    "what_was_done": "Implemented POST /api/todos endpoint",
    "artifacts": ["src/routes/todos.ts"],
    "git_state": "commit abc123",
    "needs_testing": ["unit tests for validation", "contract tests"],
    "known_issues": [],
    "relevant_patterns": ["sem-001"]
  }
}
```

---

## Memory Maintenance

### Pruning Old Episodic Memories

```python
def prune_episodic_memories():
    """
    Keep episodic memories from:
    - Last 7 days (full detail)
    - Last 30 days (summarized)
    - Older: only if referenced by semantic memory
    """
    now = datetime.now()

    for episode in load_all_episodes():
        age_days = (now - episode.timestamp).days

        if age_days > 30:
            if not is_referenced_by_semantic(episode):
                archive_episode(episode)
        elif age_days > 7:
            summarize_episode(episode)
```

### Merging Duplicate Patterns

```python
def merge_duplicate_semantics():
    """
    Find and merge semantically similar patterns.
    """
    all_patterns = load_semantic_patterns()

    clusters = cluster_by_embedding_similarity(all_patterns, threshold=0.9)

    for cluster in clusters:
        if len(cluster) > 1:
            # Keep highest confidence, merge sources
            primary = max(cluster, key=lambda p: p.confidence)
            for other in cluster:
                if other != primary:
                    primary.source_episodes.extend(other.source_episodes)
                    primary.usage_count += other.usage_count
                    create_link(other, primary, "superseded_by")
            save_semantic(primary)
```

---

## Integration with CONTINUITY.md

CONTINUITY.md is working memory - it references but doesn't duplicate long-term memory:

```markdown
## Relevant Memories (Auto-Retrieved)
- [sem-001] Express handlers need explicit return types
- [ep-2026-01-05-012] Similar endpoint implementation succeeded
- [skill: api-implementation] Standard API implementation flow

## Mistakes to Avoid (From Learnings)
- Don't forget return type annotations
- Run contract tests before marking complete
```

---

## Reference: Openai Patterns

# OpenAI Agent Patterns Reference

Research-backed patterns from OpenAI's Agents SDK, Deep Research, and autonomous agent frameworks.

---

## Overview

OpenAI's agent ecosystem provides four key architectural innovations for Loki Mode:

1. **Tracing Spans** - Hierarchical event tracking with span types
2. **Guardrails & Tripwires** - Input/output validation with early termination
3. **Handoff Callbacks** - Data preparation during agent transfers
4. **Multi-Tiered Fallbacks** - Model and workflow-level failure recovery

---

## Tracing Spans Architecture

### Span Types (Agents SDK Pattern)

Every operation is wrapped in a typed span for observability:

```yaml
span_types:
  agent_span:
    - Wraps entire agent execution
    - Contains: agent_name, instructions_hash, model

  generation_span:
    - Wraps LLM API calls
    - Contains: model, tokens_in, tokens_out, latency_ms

  function_span:
    - Wraps tool/function calls
    - Contains: function_name, arguments, result, success

  guardrail_span:
    - Wraps validation checks
    - Contains: guardrail_name, triggered, blocking

  handoff_span:
    - Wraps agent-to-agent transfers
    - Contains: from_agent, to_agent, context_passed

  custom_span:
    - User-defined operations
    - Contains: operation_name, metadata
```

### Hierarchical Trace Structure

```json
{
  "trace_id": "trace_abc123def456",
  "workflow_name": "implement_feature",
  "group_id": "session_xyz789",
  "spans": [
    {
      "span_id": "span_001",
      "parent_id": null,
      "type": "agent_span",
      "agent_name": "orchestrator",
      "started_at": "2026-01-07T10:00:00Z",
      "ended_at": "2026-01-07T10:05:00Z",
      "children": ["span_002", "span_003"]
    },
    {
      "span_id": "span_002",
      "parent_id": "span_001",
      "type": "guardrail_span",
      "guardrail_name": "input_validation",
      "triggered": false,
      "blocking": true
    },
    {
      "span_id": "span_003",
      "parent_id": "span_001",
      "type": "handoff_span",
      "from_agent": "orchestrator",
      "to_agent": "backend-dev",
      "context_passed": ["task_spec", "related_files"]
    }
  ]
}
```

### Storage Location

```
.loki/traces/
├── active/
│   └── {trace_id}.json     # Currently running traces
└── completed/
    └── {date}/
        └── {trace_id}.json # Archived traces by date
```

---

## Guardrails & Tripwires System

### Input Guardrails

Run **before** agent execution to validate user input:

```python
@input_guardrail(blocking=True)
async def validate_task_scope(input, context):
    """
    Blocks tasks outside project scope.
    Based on OpenAI Agents SDK pattern.
    """
    # Check if task references files outside project
    if references_external_paths(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="Task references paths outside project root"
        )

    # Check for disallowed operations
    if contains_destructive_operation(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="Destructive operation requires human approval"
        )

    return GuardrailResult(tripwire_triggered=False)
```

### Output Guardrails

Run **after** agent execution to validate results:

```python
@output_guardrail
async def validate_code_quality(output, context):
    """
    Blocks low-quality code output.
    """
    if output.type == "code":
        issues = run_static_analysis(output.content)
        critical = [i for i in issues if i.severity == "critical"]

        if critical:
            return GuardrailResult(
                tripwire_triggered=True,
                reason=f"Critical issues found: {critical}"
            )

    return GuardrailResult(tripwire_triggered=False)
```

### Execution Modes

| Mode | Behavior | Use When |
|------|----------|----------|
| **Blocking** | Guardrail completes before agent starts | Sensitive operations, expensive models |
| **Parallel** | Guardrail runs concurrently with agent | Fast checks, acceptable token loss |

```python
# Blocking mode: prevents token consumption
@input_guardrail(blocking=True, run_in_parallel=False)
async def expensive_validation(input):
    # Agent won't start until this completes
    pass

# Parallel mode: faster but may waste tokens if fails
@input_guardrail(blocking=True, run_in_parallel=True)
async def fast_validation(input):
    # Runs alongside agent start
    pass
```

### Tripwire Exceptions

When tripwire triggers, execution halts immediately:

```python
class InputGuardrailTripwireTriggered(Exception):
    """Raised when input validation fails."""
    pass

class OutputGuardrailTripwireTriggered(Exception):
    """Raised when output validation fails."""
    pass

# In agent loop:
try:
    result = await run_agent(task)
except InputGuardrailTripwireTriggered as e:
    log_blocked_attempt(e)
    return early_exit(reason=str(e))
except OutputGuardrailTripwireTriggered as e:
    rollback_changes()
    return retry_with_constraints(e.constraints)
```

### Layered Defense Strategy

> "Think of guardrails as a layered defense mechanism. While a single one is unlikely to provide sufficient protection, using multiple, specialized guardrails together creates more resilient agents." - OpenAI Agents SDK

```yaml
guardrail_layers:
  layer_1_input:
    - scope_validation      # Is task within bounds?
    - pii_detection         # Contains sensitive data?
    - injection_detection   # Prompt injection attempt?

  layer_2_pre_execution:
    - cost_estimation       # Will this exceed budget?
    - dependency_check      # Are dependencies available?
    - conflict_detection    # Will this conflict with in-progress work?

  layer_3_output:
    - static_analysis       # Code quality issues?
    - secret_detection      # Secrets in output?
    - spec_compliance       # Matches OpenAPI spec?

  layer_4_post_action:
    - test_validation       # Tests pass?
    - review_approval       # Review passed?
    - deployment_safety     # Safe to deploy?
```

---

## Handoff Callbacks

### on_handoff Pattern

Prepare data when transferring between agents:

```python
async def on_handoff_to_backend_dev(handoff_context):
    """
    Called when orchestrator hands off to backend-dev agent.
    Fetches context the receiving agent will need.
    """
    # Pre-fetch relevant files
    relevant_files = await find_related_files(handoff_context.task)

    # Load architectural context
    architecture = await read_file(".loki/specs/architecture.md")

    # Get recent changes to affected areas
    recent_commits = await git_log(paths=relevant_files, limit=10)

    return HandoffData(
        files=relevant_files,
        architecture=architecture,
        recent_changes=recent_commits,
        constraints=handoff_context.constraints
    )

# Register callback
handoff(
    to_agent=backend_dev,
    on_handoff=on_handoff_to_backend_dev
)
```

### Handoff Context Transfer

```json
{
  "handoff_id": "ho_abc123",
  "from_agent": "orchestrator",
  "to_agent": "backend-dev",
  "timestamp": "2026-01-07T10:05:00Z",
  "context": {
    "task_id": "task-001",
    "goal": "Implement user authentication endpoint",
    "constraints": [
      "Use existing auth patterns from src/auth/",
      "Maintain backwards compatibility",
      "Add rate limiting"
    ],
    "pre_fetched": {
      "files": ["src/auth/middleware.ts", "src/routes/index.ts"],
      "architecture": "...",
      "recent_changes": [...]
    }
  },
  "return_expected": true,
  "timeout_seconds": 600
}
```

---

## Multi-Tiered Fallback System

### Model-Level Fallbacks

```python
async def execute_with_model_fallback(task, preferred_model):
    """
    Try preferred model, fall back to alternatives on failure.
    Based on OpenAI safety patterns.
    """
    fallback_chain = {
        "opus": ["sonnet", "haiku"],
        "sonnet": ["haiku", "opus"],
        "haiku": ["sonnet"]
    }

    models_to_try = [preferred_model] + fallback_chain.get(preferred_model, [])

    for model in models_to_try:
        try:
            result = await run_agent(task, model=model)
            if result.success:
                return result
        except RateLimitError:
            log_warning(f"Rate limit on {model}, trying fallback")
            continue
        except ModelUnavailableError:
            log_warning(f"{model} unavailable, trying fallback")
            continue

    # All models failed
    return escalate_to_human(task, reason="All model fallbacks exhausted")
```

### Workflow-Level Fallbacks

```python
async def execute_with_workflow_fallback(task):
    """
    If complex workflow fails, fall back to simpler operations.
    """
    # Try full workflow first
    try:
        return await full_implementation_workflow(task)
    except WorkflowError as e:
        log_warning(f"Full workflow failed: {e}")

    # Fall back to simpler approach
    try:
        return await simplified_workflow(task)
    except WorkflowError as e:
        log_warning(f"Simplified workflow failed: {e}")

    # Last resort: decompose and try piece by piece
    try:
        subtasks = decompose_task(task)
        results = []
        for subtask in subtasks:
            result = await execute_single_step(subtask)
            results.append(result)
        return combine_results(results)
    except Exception as e:
        return escalate_to_human(task, reason=f"All workflows failed: {e}")
```

### Fallback Decision Tree

```
Task Execution
    |
    +-- Try preferred approach
    |   |
    |   +-- Success? --> Done
    |   |
    |   +-- Rate limit? --> Try next model in chain
    |   |
    |   +-- Error? --> Try simpler workflow
    |
    +-- All workflows failed?
    |   |
    |   +-- Decompose into subtasks
    |   |
    |   +-- Execute piece by piece
    |
    +-- Still failing?
        |
        +-- Escalate to human
        +-- Log detailed failure context
        +-- Save state for resume
```

---

## Confidence-Based Human Escalation

### Confidence Scoring

```python
def calculate_confidence(task_result):
    """
    Score confidence 0-1 based on multiple signals.
    Low confidence triggers human review.
    """
    signals = []

    # Test coverage signal
    if task_result.test_coverage >= 0.9:
        signals.append(1.0)
    elif task_result.test_coverage >= 0.7:
        signals.append(0.7)
    else:
        signals.append(0.3)

    # Review consensus signal
    if task_result.review_unanimous:
        signals.append(1.0)
    elif task_result.review_majority:
        signals.append(0.7)
    else:
        signals.append(0.3)

    # Retry count signal
    retry_penalty = min(task_result.retry_count * 0.2, 0.8)
    signals.append(1.0 - retry_penalty)

    return sum(signals) / len(signals)

# Escalation threshold
CONFIDENCE_THRESHOLD = 0.6

if calculate_confidence(result) < CONFIDENCE_THRESHOLD:
    escalate_to_human(
        task,
        reason="Low confidence score",
        context=result
    )
```

### Automatic Escalation Triggers

```yaml
human_escalation_triggers:
  # Retry-based
  - condition: retry_count > 3
    action: pause_and_escalate
    reason: "Multiple failures indicate unclear requirements"

  # Domain-based
  - condition: domain in ["payments", "auth", "pii"]
    action: require_approval
    reason: "Sensitive domain requires human review"

  # Confidence-based
  - condition: confidence_score < 0.6
    action: pause_and_escalate
    reason: "Low confidence in solution quality"

  # Time-based
  - condition: wall_time > expected_time * 3
    action: pause_and_escalate
    reason: "Task taking much longer than expected"

  # Cost-based
  - condition: tokens_used > budget * 0.8
    action: pause_and_escalate
    reason: "Approaching token budget limit"
```

---

## AGENTS.md Integration

### Reading Target Project's AGENTS.md

```python
async def load_project_context():
    """
    Read AGENTS.md from target project if exists.
    Based on OpenAI/AAIF standard.
    """
    agents_md_locations = [
        "AGENTS.md",
        ".github/AGENTS.md",
        "docs/AGENTS.md"
    ]

    for location in agents_md_locations:
        if await file_exists(location):
            content = await read_file(location)
            return parse_agents_md(content)

    # No AGENTS.md found - use defaults
    return default_project_context()

def parse_agents_md(content):
    """
    Extract structured guidance from AGENTS.md.
    """
    sections = parse_markdown_sections(content)

    return ProjectContext(
        build_commands=sections.get("build", []),
        test_commands=sections.get("test", []),
        code_style=sections.get("code style", {}),
        architecture_notes=sections.get("architecture", ""),
        deployment_notes=sections.get("deployment", ""),
        security_notes=sections.get("security", "")
    )
```

### Context Priority

```
1. AGENTS.md (closest to current file, monorepo-aware)
2. CLAUDE.md (Claude-specific instructions)
3. .loki/CONTINUITY.md (session state)
4. Package-level documentation
5. README.md (general project info)
```

---

## Reasoning Model Guidance

### When to Use Extended Thinking

Based on OpenAI's o3/o4-mini patterns:

```yaml
use_extended_reasoning:
  always:
    - System architecture design
    - Security vulnerability analysis
    - Complex debugging (multi-file, unclear root cause)
    - API design decisions
    - Performance optimization strategy

  sometimes:
    - Code review (only for critical/complex changes)
    - Refactoring planning (when multiple approaches exist)
    - Integration design (when crossing system boundaries)

  never:
    - Simple bug fixes
    - Documentation updates
    - Unit test writing
    - Formatting/linting
    - File operations
```

### Backtracking Pattern

```python
async def execute_with_backtracking(task, max_backtracks=3):
    """
    Allow agent to backtrack and try different approaches.
    Based on Deep Research's adaptive planning.
    """
    attempts = []

    for attempt in range(max_backtracks + 1):
        # Generate approach considering previous failures
        approach = await plan_approach(
            task,
            failed_approaches=attempts
        )

        result = await execute_approach(approach)

        if result.success:
            return result

        # Record failed approach for learning
        attempts.append({
            "approach": approach,
            "failure_reason": result.error,
            "partial_progress": result.partial_output
        })

        # Backtrack: reset to clean state
        await rollback_to_checkpoint(task.checkpoint_id)

    return FailedResult(
        reason="Max backtracks exceeded",
        attempts=attempts
    )
```

---

## Session State Management

### Automatic State Persistence

```python
class Session:
    """
    Automatic conversation history and state management.
    Inspired by OpenAI Agents SDK Sessions.
    """

    def __init__(self, session_id):
        self.session_id = session_id
        self.state_file = f".loki/state/sessions/{session_id}.json"
        self.history = []
        self.context = {}

    async def save_state(self):
        state = {
            "session_id": self.session_id,
            "history": self.history,
            "context": self.context,
            "last_updated": now()
        }
        await write_json(self.state_file, state)

    async def load_state(self):
        if await file_exists(self.state_file):
            state = await read_json(self.state_file)
            self.history = state["history"]
            self.context = state["context"]

    async def add_turn(self, role, content, metadata=None):
        self.history.append({
            "role": role,
            "content": content,
            "metadata": metadata,
            "timestamp": now()
        })
        await self.save_state()
```

---

## Sources

**OpenAI Official:**
- [Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Building Agents Track](https://developers.openai.com/tracks/building-agents/)
- [AGENTS.md Specification](https://agents.md/)

**Deep Research & Reasoning:**
- [Introducing Deep Research](https://openai.com/index/introducing-deep-research/)
- [Deep Research System Card](https://cdn.openai.com/deep-research-system-card.pdf)
- [Introducing o3 and o4-mini](https://openai.com/index/introducing-o3-and-o4-mini/)
- [Reasoning Best Practices](https://platform.openai.com/docs/guides/reasoning-best-practices)

**Safety & Monitoring:**
- [Chain of Thought Monitoring](https://openai.com/index/chain-of-thought-monitoring/)
- [Agent Builder Safety](https://platform.openai.com/docs/guides/agent-builder-safety)
- [Computer-Using Agent](https://openai.com/index/computer-using-agent/)

**Standards & Interoperability:**
- [Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/)
- [OpenAI for Developers 2025](https://developers.openai.com/blog/openai-for-developers-2025/)

---

## Reference: Production Patterns

# Production Patterns Reference

Practitioner-tested patterns from Hacker News discussions and real-world deployments. These patterns represent what actually works in production, not theoretical frameworks.

---

## Overview

This reference consolidates battle-tested insights from:
- HN discussions on autonomous agents in production (2025)
- Coding with LLMs practitioner experiences
- Simon Willison's Superpowers coding agent patterns
- Multi-agent orchestration real-world deployments

---

## What Actually Works in Production

### Human-in-the-Loop (HITL) is Non-Negotiable

**Key Insight:** "Zero companies don't have a human in the loop" for customer-facing applications.

```yaml
hitl_patterns:
  always_human:
    - Customer-facing responses
    - Financial transactions
    - Security-critical operations
    - Legal/compliance decisions

  automation_candidates:
    - Internal tooling
    - Developer assistance
    - Data preprocessing
    - Code generation (with review)

  implementation:
    - Classification layer routes to human vs automated
    - Confidence thresholds trigger escalation
    - Audit trails for all automated decisions
```

### Narrow Scope Wins

**Key Insight:** Successful agents operate within tightly constrained domains.

```yaml
scope_constraints:
  max_steps_before_review: 3-5
  task_characteristics:
    - Specific, well-defined objectives
    - Pre-classified inputs
    - Deterministic success criteria
    - Verifiable outputs

  successful_domains:
    - Email scanning and classification
    - Invoice processing
    - Code refactoring (bounded)
    - Documentation generation
    - Test writing

  failure_prone_domains:
    - Open-ended feature implementation
    - Novel algorithm design
    - Security-critical code
    - Cross-system integrations
```

### Confidence-Based Routing

**Key Insight:** Treat agents as preprocessors, not decision-makers.

```python
def confidence_based_routing(agent_output):
    """
    Route based on confidence, not capability.
    Based on production practitioner patterns.
    """
    confidence = agent_output.confidence_score

    if confidence >= 0.95:
        # High confidence: auto-approve with logging
        return AutoApprove(audit_log=True)

    elif confidence >= 0.70:
        # Medium confidence: quick human review
        return HumanReview(priority="normal", timeout="1h")

    elif confidence >= 0.40:
        # Low confidence: detailed human review
        return HumanReview(priority="high", context="full")

    else:
        # Very low confidence: escalate immediately
        return Escalate(reason="low_confidence", require_senior=True)
```

### Classification Before Automation

**Key Insight:** Separate inputs before processing.

```yaml
classification_first:
  step_1_classify:
    workable:
      - Clear requirements
      - Existing patterns
      - Test coverage available
    non_workable:
      - Ambiguous requirements
      - Novel architecture
      - Missing dependencies
    escalate_immediately:
      - Security concerns
      - Compliance requirements
      - Customer-facing changes

  step_2_route:
    workable: "Automated pipeline"
    non_workable: "Human clarification"
    escalate: "Senior review"
```

### Deterministic Outer Loops

**Key Insight:** Wrap agent outputs with rule-based validation.

```python
def deterministic_validation_loop(task, max_attempts=3):
    """
    Use LLMs only where genuine ambiguity exists.
    Wrap with deterministic rules.
    """
    for attempt in range(max_attempts):
        # LLM handles the ambiguous part
        output = agent.execute(task)

        # Deterministic validation (NOT LLM)
        validation_errors = []

        # Rule: Must have tests
        if not output.has_tests:
            validation_errors.append("Missing tests")

        # Rule: Must pass linting
        lint_result = run_linter(output.code)
        if lint_result.errors:
            validation_errors.append(f"Lint errors: {lint_result.errors}")

        # Rule: Must compile
        compile_result = compile_code(output.code)
        if not compile_result.success:
            validation_errors.append(f"Compile error: {compile_result.error}")

        # Rule: Tests must pass
        if output.has_tests:
            test_result = run_tests(output.code)
            if not test_result.all_passed:
                validation_errors.append(f"Test failures: {test_result.failures}")

        if not validation_errors:
            return output

        # Feed errors back for retry
        task = task.with_feedback(validation_errors)

    return FailedResult(reason="Max attempts exceeded")
```

---

## Context Engineering Patterns

### Context Curation Over Automatic Selection

**Key Insight:** Manually choose which files and information to provide.

```yaml
context_curation:
  principles:
    - "Less is more" - focused context beats comprehensive context
    - Manual selection outperforms automatic RAG
    - Remove outdated information aggressively

  anti_patterns:
    - Dumping entire codebase into context
    - Relying on automatic context selection
    - Accumulating conversation history indefinitely

  implementation:
    per_task_context:
      - 2-5 most relevant files
      - Specific functions, not entire modules
      - Recent changes only (last 1-2 days)
      - Clear success criteria

    context_budget:
      target: "< 10k tokens for context"
      reserve: "90% for model reasoning"
```

### Information Abstraction

**Key Insight:** Summarize rather than feeding full data.

```python
def abstract_for_agent(raw_data, task_context):
    """
    Design abstractions that preserve decision-relevant information.
    Based on practitioner insights.
    """
    # BAD: Feed 10,000 database rows
    # raw_data = db.query("SELECT * FROM users")

    # GOOD: Summarize to decision-relevant info
    summary = {
        "query_status": "success",
        "total_results": len(raw_data),
        "sample": raw_data[:5],
        "schema": extract_schema(raw_data),
        "statistics": {
            "null_count": count_nulls(raw_data),
            "unique_values": count_uniques(raw_data),
            "date_range": get_date_range(raw_data)
        }
    }

    return summary
```

### Separate Conversations Per Task

**Key Insight:** Fresh contexts yield better results than accumulated sessions.

```yaml
conversation_management:
  new_conversation_triggers:
    - Different domain (backend -> frontend)
    - New feature vs bug fix
    - After completing major task
    - When errors accumulate (3+ in row)

  preserve_across_sessions:
    - CLAUDE.md / CONTINUITY.md
    - Architectural decisions
    - Key constraints

  discard_between_sessions:
    - Debugging attempts
    - Abandoned approaches
    - Intermediate drafts
```

---

## Skills System Pattern

### On-Demand Skill Loading

**Key Insight:** Skills remain dormant until the model actively seeks them out.

```yaml
skills_architecture:
  core_interaction: "< 2k tokens"
  skill_loading: "On-demand via search"

  implementation:
    skill_discovery:
      - Shell script searches skill files
      - Model requests specific skills by name
      - Skills loaded only when needed

    skill_structure:
      name: "unique-skill-name"
      trigger: "Pattern that activates skill"
      content: "Detailed instructions"
      dependencies: ["other-skills"]

  benefits:
    - Minimal base context
    - Extensible without bloat
    - Skills can be updated independently
```

### Sub-Agents for Context Isolation

**Key Insight:** Prevent massive token waste by isolating context-noisy subtasks.

```python
async def context_isolated_search(query, codebase_path):
    """
    Use sub-agent for grep/search to prevent context pollution.
    Based on Simon Willison's patterns.
    """
    # Main agent stays focused
    # Sub-agent handles noisy file searching

    search_agent = spawn_subagent(
        role="codebase-searcher",
        context_limit="10k tokens",
        permissions=["read-only"]
    )

    results = await search_agent.execute(
        task=f"Find files related to: {query}",
        codebase=codebase_path
    )

    # Return only relevant paths, not full content
    return FilteredResults(
        paths=results.relevant_files[:10],
        summaries=results.file_summaries,
        confidence=results.relevance_scores
    )
```

---

## Planning Before Execution

### Explicit Plan-Then-Code Workflow

**Key Insight:** Have models articulate detailed plans without immediately writing code.

```yaml
plan_then_code:
  phase_1_planning:
    outputs:
      - spec.md: "Detailed requirements"
      - todo.md: "Tagged tasks [BUG], [FEAT], [REFACTOR]"
      - approach.md: "Implementation strategy"
    constraints:
      - NO CODE in this phase
      - Human review before proceeding
      - Clear success criteria

  phase_2_review:
    checks:
      - Plan addresses all requirements
      - Approach is feasible
      - No missing dependencies
      - Tests are specified

  phase_3_implementation:
    constraints:
      - Follow plan exactly
      - One task at a time
      - Test after each change
      - Report deviations immediately
```

---

## Multi-Agent Orchestration Patterns

### Event-Driven Coordination

**Key Insight:** Move beyond synchronous prompt chaining to asynchronous, decoupled systems.

```yaml
event_driven_orchestration:
  problems_with_synchronous:
    - Doesn't scale
    - Mixes orchestration with prompt logic
    - Single failure breaks entire chain
    - No retry/recovery mechanism

  async_architecture:
    message_queue:
      - Agents communicate via events
      - Decoupled execution
      - Natural retry/dead-letter handling

    state_management:
      - Persistent task state
      - Checkpoint/resume capability
      - Clear ownership of data

    error_handling:
      - Per-agent retry policies
      - Circuit breakers
      - Graceful degradation
```

### Policy-First Enforcement

**Key Insight:** Govern agent behavior at runtime, not just training time.

```python
class PolicyEngine:
    """
    Runtime governance for agent behavior.
    Based on autonomous control plane patterns.
    """

    def __init__(self, policies):
        self.policies = policies

    async def enforce(self, agent_action, context):
        for policy in self.policies:
            result = await policy.evaluate(agent_action, context)

            if result.blocked:
                return BlockedAction(
                    reason=result.reason,
                    policy=policy.name,
                    remediation=result.suggested_action
                )

            if result.modified:
                agent_action = result.modified_action

        return AllowedAction(agent_action)

# Example policies
policies = [
    NoProductionDataDeletion(),
    NoSecretsInCode(),
    MaxTokenBudget(limit=100000),
    RequireTestsForCode(),
    BlockExternalNetworkCalls(in_sandbox=True)
]
```

### Simulation Layer

**Key Insight:** Evaluate changes before deploying to real environment.

```yaml
simulation_layer:
  purpose: "Test agent behavior in safe environment"

  implementation:
    sandbox_environment:
      - Isolated container
      - Mocked external services
      - Synthetic data
      - Full audit logging

    validation_checks:
      - Run tests in sandbox first
      - Compare outputs to expected
      - Check for policy violations
      - Measure resource consumption

    promotion_criteria:
      - All tests pass
      - No policy violations
      - Resource usage within limits
      - Human approval (for sensitive changes)
```

---

## Evaluation and Benchmarking

### Problems with Current Benchmarks

**Key Insight:** LLM-as-judge creates shared blind spots.

```yaml
benchmark_problems:
  llm_judge_issues:
    - Same architecture = same failure modes
    - Math errors accepted as correct
    - "Do-nothing" baseline passes 38% of time

  contamination:
    - Published benchmarks become training targets
    - Overfitting to specific datasets
    - Inflated scores don't reflect real performance

  solutions:
    held_back_sets: "90% public, 10% private"
    human_evaluation: "Final published results require humans"
    production_testing: "A/B tests measure actual value"
    objective_outcomes: "Simulated environments with verifiable results"
```

### Practical Evaluation Approach

```python
def evaluate_agent_change(before_agent, after_agent, task_set):
    """
    Production-oriented evaluation.
    Based on HN practitioner recommendations.
    """
    results = {
        "before": [],
        "after": [],
        "human_preference": []
    }

    for task in task_set:
        # Run both agents
        before_result = before_agent.execute(task)
        after_result = after_agent.execute(task)

        # Objective metrics (NOT LLM-judged)
        results["before"].append({
            "tests_pass": run_tests(before_result),
            "lint_clean": run_linter(before_result),
            "time_taken": before_result.duration,
            "tokens_used": before_result.tokens
        })

        results["after"].append({
            "tests_pass": run_tests(after_result),
            "lint_clean": run_linter(after_result),
            "time_taken": after_result.duration,
            "tokens_used": after_result.tokens
        })

        # Sample for human review
        if random.random() < 0.1:  # 10% sample
            results["human_preference"].append({
                "task": task,
                "before": before_result,
                "after": after_result,
                "pending_review": True
            })

    return EvaluationReport(results)
```

---

## Cost and Token Economics

### Real-World Cost Patterns

```yaml
cost_patterns:
  claude_code:
    heavy_use: "$25/1-2 hours on large codebases"
    api_range: "$1-5/hour depending on efficiency"
    max_tier: "$200/month often needs 2-3 subscriptions"

  token_economics:
    sub_agents_multiply_cost: "Each duplicates context"
    example: "5-task parallel job = 50,000+ tokens per subtask"

  optimization:
    context_isolation: "Use sub-agents for noisy tasks"
    information_abstraction: "Summarize, don't dump"
    fresh_conversations: "Reset after major tasks"
    skill_on_demand: "Load only when needed"
```

---

## Sources

**Hacker News Discussions:**
- [What Actually Works in Production for Autonomous Agents](https://news.ycombinator.com/item?id=44623207)
- [Coding with LLMs in Summer 2025](https://news.ycombinator.com/item?id=44623953)
- [Superpowers: How I'm Using Coding Agents](https://news.ycombinator.com/item?id=45547344)
- [Claude Code Experience After Two Weeks](https://news.ycombinator.com/item?id=44596472)
- [AI Agent Benchmarks Are Broken](https://news.ycombinator.com/item?id=44531697)
- [How to Orchestrate Multi-Agent Workflows](https://news.ycombinator.com/item?id=45955997)
- [Context Engineering vs Prompt Engineering](https://news.ycombinator.com/item?id=44427757)

**Show HN Projects:**
- [Self-Evolving Agents Repository](https://news.ycombinator.com/item?id=45099226)
- [Package Manager for Agent Skills](https://news.ycombinator.com/item?id=46422264)
- [Wispbit - AI Code Review Agent](https://news.ycombinator.com/item?id=44722603)
- [Agtrace - Monitoring for AI Coding Agents](https://news.ycombinator.com/item?id=46425670)

---

## Reference: Quality Control

# Quality Control Reference

Quality gates, code review process, and severity blocking rules.
Enhanced with 2025 research on anti-sycophancy, heterogeneous teams, and OpenAI Agents SDK patterns.

---

## Core Principle: Guardrails, Not Just Acceleration

**CRITICAL:** Speed without quality controls creates "AI slop" - semi-functional code that accumulates technical debt. Loki Mode enforces strict quality guardrails.

**Research Insight:** Heterogeneous review teams outperform homogeneous ones by 4-6% (A-HMAD, 2025).
**OpenAI Insight:** "Think of guardrails as a layered defense mechanism. Multiple specialized guardrails create resilient agents."

---

## Guardrails & Tripwires System (OpenAI SDK Pattern)

### Input Guardrails (Run Before Execution)

```python
# Layer 1: Validate task scope and safety
@input_guardrail(blocking=True)
async def validate_task_scope(input, context):
    # Check if task within project bounds
    if references_external_paths(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="Task references paths outside project"
        )
    # Check for destructive operations
    if contains_destructive_operation(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="Destructive operation requires human approval"
        )
    return GuardrailResult(tripwire_triggered=False)

# Layer 2: Detect prompt injection
@input_guardrail(blocking=True)
async def detect_injection(input, context):
    if has_injection_patterns(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="Potential prompt injection detected"
        )
    return GuardrailResult(tripwire_triggered=False)
```

### Output Guardrails (Run After Execution)

```python
# Validate code quality before accepting
@output_guardrail
async def validate_code_output(output, context):
    if output.type == "code":
        issues = run_static_analysis(output.content)
        critical = [i for i in issues if i.severity == "critical"]
        if critical:
            return GuardrailResult(
                tripwire_triggered=True,
                reason=f"Critical issues: {critical}"
            )
    return GuardrailResult(tripwire_triggered=False)

# Check for secrets in output
@output_guardrail
async def check_secrets(output, context):
    if contains_secrets(output.content):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="Output contains potential secrets"
        )
    return GuardrailResult(tripwire_triggered=False)
```

### Execution Modes

| Mode | Behavior | Use When |
|------|----------|----------|
| **Blocking** | Guardrail completes before agent starts | Expensive models, sensitive ops |
| **Parallel** | Guardrail runs with agent | Fast checks, acceptable token loss |

```python
# Blocking: prevents token consumption on fail
@input_guardrail(blocking=True, run_in_parallel=False)
async def expensive_validation(input): pass

# Parallel: faster but may waste tokens
@input_guardrail(blocking=True, run_in_parallel=True)
async def fast_validation(input): pass
```

### Tripwire Handling

When a guardrail triggers its tripwire, execution halts immediately:

```python
try:
    result = await run_agent(task)
except InputGuardrailTripwireTriggered as e:
    log_blocked_attempt(e)
    return early_exit(reason=str(e))
except OutputGuardrailTripwireTriggered as e:
    rollback_changes()
    return retry_with_constraints(e.constraints)
```

### Layered Defense Strategy

```yaml
guardrail_layers:
  layer_1_input:
    - scope_validation      # Is task within bounds?
    - pii_detection         # Contains sensitive data?
    - injection_detection   # Prompt injection attempt?

  layer_2_pre_execution:
    - cost_estimation       # Will this exceed budget?
    - dependency_check      # Are dependencies available?
    - conflict_detection    # Conflicts with in-progress work?

  layer_3_output:
    - static_analysis       # Code quality issues?
    - secret_detection      # Secrets in output?
    - spec_compliance       # Matches OpenAPI spec?

  layer_4_post_action:
    - test_validation       # Tests pass?
    - review_approval       # Review passed?
    - deployment_safety     # Safe to deploy?
```

See `references/openai-patterns.md` for full guardrails implementation.

---

## Quality Gates

**Never ship code without passing all quality gates:**

### 1. Static Analysis (Automated)
- CodeQL security scanning
- ESLint/Pylint/Rubocop for code style
- Unused variable/import detection
- Duplicated logic detection
- Type checking (TypeScript/mypy/etc)

### 2. 3-Reviewer Parallel System (AI-driven)

Every code change goes through 3 specialized reviewers **simultaneously**:

```
IMPLEMENT -> BLIND REVIEW (parallel) -> DEBATE (if disagreement) -> AGGREGATE -> FIX -> RE-REVIEW
                |
                +-- code-reviewer (Opus) - Code quality, patterns, best practices
                +-- business-logic-reviewer (Opus) - Requirements, edge cases, UX
                +-- security-reviewer (Opus) - Vulnerabilities, OWASP Top 10
```

**Important:**
- ALWAYS launch all 3 reviewers in a single message (3 Task calls)
- ALWAYS specify model: "opus" for each reviewer
- ALWAYS use blind review mode (reviewers cannot see each other's findings initially)
- NEVER dispatch reviewers sequentially (always parallel - 3x faster)
- NEVER aggregate before all 3 reviewers complete

### Anti-Sycophancy Protocol (CONSENSAGENT Research)

**Problem:** Reviewers may reinforce each other's findings instead of critically engaging.

**Solution: Blind Review + Devil's Advocate**

```python
# Phase 1: Independent blind review
reviews = []
for reviewer in [code_reviewer, business_reviewer, security_reviewer]:
    review = Task(
        subagent_type="general-purpose",
        model="opus",
        prompt=f"""
        {reviewer.prompt}

        CRITICAL: Be skeptical. Your job is to find problems.
        List specific concerns with file:line references.
        Do NOT rubber-stamp. Finding zero issues is suspicious.
        """
    )
    reviews.append(review)

# Phase 2: Check for disagreement
if has_disagreement(reviews):
    # Structured debate - max 2 rounds
    debate_result = structured_debate(reviews, max_rounds=2)
else:
    # All agreed - run devil's advocate
    devil_review = Task(
        subagent_type="general-purpose",
        model="opus",
        prompt="""
        The other reviewers found no issues. Your job is to be contrarian.
        Find problems they missed. Challenge assumptions.
        If truly nothing wrong, explain why each potential issue category is covered.
        """
    )
    reviews.append(devil_review)
```

### Heterogeneous Team Composition

**Each reviewer has distinct personality/focus:**

| Reviewer | Model | Expertise | Personality |
|----------|-------|-----------|-------------|
| Code Quality | Opus | SOLID, patterns, maintainability | Perfectionist |
| Business Logic | Opus | Requirements, edge cases, UX | Pragmatic |
| Security | Opus | OWASP, auth, injection | Paranoid |

This diversity prevents groupthink and catches more issues.

### 3. Severity-Based Blocking

| Severity | Action | Continue? |
|----------|--------|-----------|
| **Critical** | BLOCK - Fix immediately | NO |
| **High** | BLOCK - Fix immediately | NO |
| **Medium** | BLOCK - Fix before proceeding | NO |
| **Low** | Add `// TODO(review): ...` comment | YES |
| **Cosmetic** | Add `// FIXME(nitpick): ...` comment | YES |

**Critical/High/Medium = BLOCK and fix before proceeding**
**Low/Cosmetic = Add TODO/FIXME comment, continue**

### 4. Test Coverage Gates
- Unit tests: 100% pass, >80% coverage
- Integration tests: 100% pass
- E2E tests: critical flows pass

### 5. Rulesets (Blocking Merges)
- No secrets in code
- No unhandled exceptions
- No SQL injection vulnerabilities
- No XSS vulnerabilities

---

## Code Review Protocol

### Launching Reviewers (Parallel)

```python
# CORRECT: Launch all 3 in parallel
Task(subagent_type="general-purpose", model="opus",
     description="Code quality review",
     prompt="Review for code quality, patterns, SOLID principles...")

Task(subagent_type="general-purpose", model="opus",
     description="Business logic review",
     prompt="Review for requirements alignment, edge cases, UX...")

Task(subagent_type="general-purpose", model="opus",
     description="Security review",
     prompt="Review for vulnerabilities, OWASP Top 10...")

# WRONG: Sequential reviewers (3x slower)
# Don't do: await reviewer1; await reviewer2; await reviewer3;
```

### After Fixes

- ALWAYS re-run ALL 3 reviewers after fixes (not just the one that found the issue)
- Wait for all reviews to complete before aggregating results

---

## Structured Prompting for Subagents

**Every subagent dispatch MUST include:**

```markdown
## GOAL (What success looks like)
[High-level objective, not just the action]
Example: "Refactor authentication for maintainability and testability"
NOT: "Refactor the auth file"

## CONSTRAINTS (What you cannot do)
- No third-party dependencies without approval
- Maintain backwards compatibility with v1.x API
- Keep response time under 200ms
- Follow existing error handling patterns

## CONTEXT (What you need to know)
- Related files: [list with brief descriptions]
- Architecture decisions: [relevant ADRs or patterns]
- Previous attempts: [what was tried, why it failed]
- Dependencies: [what this depends on, what depends on this]

## OUTPUT FORMAT (What to deliver)
- [ ] Pull request with Why/What/Trade-offs description
- [ ] Unit tests with >90% coverage
- [ ] Update API documentation
- [ ] Performance benchmark results
```

---

## Task Completion Report

**Every completed task MUST include decision documentation:**

```markdown
## Task Completion Report

### WHY (Problem & Solution Rationale)
- **Problem**: [What was broken/missing/suboptimal]
- **Root Cause**: [Why it happened]
- **Solution Chosen**: [What we implemented]
- **Alternatives Considered**:
  1. [Option A]: Rejected because [reason]
  2. [Option B]: Rejected because [reason]

### WHAT (Changes Made)
- **Files Modified**: [with line ranges and purpose]
  - `src/auth.ts:45-89` - Extracted token validation to separate function
  - `src/auth.test.ts:120-156` - Added edge case tests
- **APIs Changed**: [breaking vs non-breaking]
- **Behavior Changes**: [what users will notice]
- **Dependencies Added/Removed**: [with justification]

### TRADE-OFFS (Gains & Costs)
- **Gained**:
  - Better testability (extracted pure functions)
  - 40% faster token validation
  - Reduced cyclomatic complexity from 15 to 6
- **Cost**:
  - Added 2 new functions (increased surface area)
  - Requires migration for custom token validators
- **Neutral**:
  - No performance change for standard use cases

### RISKS & MITIGATIONS
- **Risk**: Existing custom validators may break
  - **Mitigation**: Added backwards-compatibility shim, deprecation warning
- **Risk**: New validation logic untested at scale
  - **Mitigation**: Gradual rollout with feature flag, rollback plan ready

### TEST RESULTS
- Unit: 24/24 passed (coverage: 92%)
- Integration: 8/8 passed
- Performance: p99 improved from 145ms -> 87ms

### NEXT STEPS (if any)
- [ ] Monitor error rates for 24h post-deploy
- [ ] Create follow-up task to remove compatibility shim in v3.0
```

---

## Preventing "AI Slop"

### Warning Signs
- Tests pass but code quality degraded
- Copy-paste duplication instead of abstraction
- Over-engineered solutions to simple problems
- Missing error handling
- No logging/observability
- Generic variable names (data, temp, result)
- Magic numbers without constants
- Commented-out code
- TODO comments without GitHub issues

### When Detected
1. Fail the task immediately
2. Add to failed queue with detailed feedback
3. Re-dispatch with stricter constraints
4. Update CONTINUITY.md with anti-pattern to avoid

---

## Quality Gate Hooks

### Pre-Write Hook (BLOCKING)
```bash
#!/bin/bash
# .loki/hooks/pre-write.sh
# Blocks writes that violate rules

# Check for secrets
if grep -rE "(password|secret|key).*=.*['\"][^'\"]{8,}" "$1"; then
  echo "BLOCKED: Potential secret detected"
  exit 1
fi

# Check for console.log in production
if grep -n "console.log" "$1" | grep -v "test"; then
  echo "BLOCKED: Remove console.log statements"
  exit 1
fi
```

### Post-Write Hook (AUTO-FIX)
```bash
#!/bin/bash
# .loki/hooks/post-write.sh
# Auto-fixes after writes

# Format code
npx prettier --write "$1"

# Fix linting issues
npx eslint --fix "$1"

# Type check
npx tsc --noEmit
```

---

## Constitution Reference

Quality gates are enforced by `autonomy/CONSTITUTION.md`:

**Pre-Commit (BLOCKING):**
- Linting (auto-fix enabled)
- Type checking (strict mode)
- Contract tests (80% coverage minimum)
- Spec validation (Spectral)

**Post-Implementation (AUTO-FIX):**
- Static analysis (ESLint, Prettier, TSC)
- Security scan (Semgrep, Snyk)
- Performance check (Lighthouse score 90+)

**Runtime Invariants:**
- `SPEC_BEFORE_CODE`: Implementation tasks require spec reference
- `TASK_HAS_COMMIT`: Completed tasks have git commit SHA
- `QUALITY_GATES_PASSED`: Completed tasks passed all quality checks

---

## Reference: Sdlc Phases

# SDLC Phases Reference

All phases with detailed workflows and testing procedures.

---

## Phase Overview

```
Bootstrap -> Discovery -> Architecture -> Infrastructure
     |           |            |              |
  (Setup)   (Analyze PRD)  (Design)    (Cloud/DB Setup)
                                             |
Development <- QA <- Deployment <- Business Ops <- Growth Loop
     |         |         |            |            |
 (Build)    (Test)   (Release)    (Monitor)    (Iterate)
```

---

## Phase 0: Bootstrap

**Purpose:** Initialize Loki Mode environment

### Actions:
1. Create `.loki/` directory structure
2. Initialize orchestrator state in `.loki/state/orchestrator.json`
3. Validate PRD exists and is readable
4. Spawn initial agent pool (3-5 agents)
5. Create CONTINUITY.md

### Directory Structure Created:
```
.loki/
+-- CONTINUITY.md
+-- state/
|   +-- orchestrator.json
|   +-- agents/
|   +-- circuit-breakers/
+-- queue/
|   +-- pending.json
|   +-- in-progress.json
|   +-- completed.json
|   +-- dead-letter.json
+-- specs/
+-- memory/
+-- artifacts/
```

---

## Phase 1: Discovery

**Purpose:** Understand requirements and market context

### Actions:
1. Parse PRD, extract requirements
2. Spawn `biz-analytics` agent for competitive research
3. Web search competitors, extract features, reviews
4. Identify market gaps and opportunities
5. Generate task backlog with priorities and dependencies

### Output:
- Requirements document
- Competitive analysis
- Initial task backlog in `.loki/queue/pending.json`

---

## Phase 2: Architecture

**Purpose:** Design system architecture and generate specs

### SPEC-FIRST WORKFLOW

**Step 1: Extract API Requirements from PRD**
- Parse PRD for user stories and functionality
- Map to REST/GraphQL operations
- Document data models and relationships

**Step 2: Generate OpenAPI 3.1 Specification**

```yaml
openapi: 3.1.0
info:
  title: Product API
  version: 1.0.0
paths:
  /auth/login:
    post:
      summary: Authenticate user and return JWT
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email: { type: string, format: email }
                password: { type: string, minLength: 8 }
      responses:
        200:
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  token: { type: string }
                  expiresAt: { type: string, format: date-time }
        401:
          description: Invalid credentials
```

**Step 3: Validate Spec**
```bash
npm install -g @stoplight/spectral-cli
spectral lint .loki/specs/openapi.yaml
swagger-cli validate .loki/specs/openapi.yaml
```

**Step 4: Generate Artifacts from Spec**
```bash
# TypeScript types
npx openapi-typescript .loki/specs/openapi.yaml --output src/types/api.ts

# Client SDK
npx openapi-generator-cli generate \
  -i .loki/specs/openapi.yaml \
  -g typescript-axios \
  -o src/clients/api

# Server stubs
npx openapi-generator-cli generate \
  -i .loki/specs/openapi.yaml \
  -g nodejs-express-server \
  -o backend/generated

# Documentation
npx redoc-cli bundle .loki/specs/openapi.yaml -o docs/api.html
```

**Step 5: Select Tech Stack**
- Spawn `eng-backend` + `eng-frontend` architects
- Both agents review spec and propose stack
- Consensus required (both must agree)
- Self-reflection checkpoint with evidence

**Step 6: Create Project Scaffolding**
- Initialize project with tech stack
- Install dependencies
- Configure linters
- Setup contract testing framework

---

## Phase 3: Infrastructure

**Purpose:** Provision cloud resources and CI/CD

### Actions:
1. Spawn `ops-devops` agent
2. Provision cloud resources (see `references/deployment.md`)
3. Set up CI/CD pipelines
4. Configure monitoring and alerting
5. Create staging and production environments

### CI/CD Pipeline:
```yaml
name: CI/CD Pipeline
on: [push, pull_request]
jobs:
  test:
    - Lint
    - Type check
    - Unit tests
    - Contract tests
    - Security scan
  deploy-staging:
    needs: test
    - Deploy to staging
    - Smoke tests
  deploy-production:
    needs: deploy-staging
    - Blue-green deploy
    - Health checks
    - Auto-rollback on errors
```

---

## Phase 4: Development

**Purpose:** Implement features with quality gates

### Workflow Per Task:

```
1. Dispatch implementation subagent (Task tool, model: sonnet)
2. Subagent implements with TDD, commits, reports back
3. Dispatch 3 reviewers IN PARALLEL (single message, 3 Task calls):
   - code-reviewer (opus)
   - business-logic-reviewer (opus)
   - security-reviewer (opus)
4. Aggregate findings by severity
5. IF Critical/High/Medium found:
   - Dispatch fix subagent
   - Re-run ALL 3 reviewers
   - Loop until all PASS
6. Add TODO comments for Low issues
7. Add FIXME comments for Cosmetic issues
8. Mark task complete with git checkpoint
```

### Implementation Rules:
- Agents implement ONLY what's in the spec
- Must validate against openapi.yaml schema
- Must return responses matching spec
- Performance targets from spec x-performance extension

---

## Phase 5: Quality Assurance

**Purpose:** Comprehensive testing and security audit

### Testing Phases:

**UNIT Phase:**
```bash
npm run test:unit
# or
pytest tests/unit/
```
- Coverage: >80% required
- All tests must pass

**INTEGRATION Phase:**
```bash
npm run test:integration
```
- Test API endpoints against actual database
- Test external service integrations
- Verify data flows end-to-end

**E2E Phase:**
```bash
npx playwright test
# or
npx cypress run
```
- Test complete user flows
- Cross-browser testing
- Mobile responsive testing

**CONTRACT Phase:**
```bash
npm run test:contract
```
- Validate implementation matches OpenAPI spec
- Test request/response schemas
- Breaking change detection

**SECURITY Phase:**
```bash
npm audit
npx snyk test
semgrep --config=auto .
```
- OWASP Top 10 checks
- Dependency vulnerabilities
- Static analysis

**PERFORMANCE Phase:**
```bash
npx k6 run tests/load.js
npx lighthouse http://localhost:3000
```
- Load testing: 100 concurrent users for 1 minute
- Stress testing: 500 concurrent users for 30 seconds
- P95 response time < 500ms required

**ACCESSIBILITY Phase:**
```bash
npx axe http://localhost:3000
```
- WCAG 2.1 AA compliance
- Alt text, ARIA labels, color contrast
- Keyboard navigation, focus indicators

**REGRESSION Phase:**
- Compare behavior against previous version
- Verify no features broken by recent changes
- Test backward compatibility of APIs

**UAT Phase:**
- Create acceptance tests from PRD
- Walk through complete user journeys
- Verify business logic matches PRD
- Document any UX friction points

---

## Phase 6: Deployment

**Purpose:** Release to production

### Actions:
1. Spawn `ops-release` agent
2. Generate semantic version, changelog
3. Create release branch, tag
4. Deploy to staging, run smoke tests
5. Blue-green deploy to production
6. Monitor for 30min, auto-rollback if errors spike

### Deployment Strategies:

**Blue-Green:**
```
1. Deploy new version to "green" environment
2. Run smoke tests
3. Switch traffic from "blue" to "green"
4. Keep "blue" as rollback target
```

**Canary:**
```
1. Deploy to 5% of traffic
2. Monitor error rates
3. Gradually increase to 25%, 50%, 100%
4. Rollback if errors exceed threshold
```

---

## Phase 7: Business Operations

**Purpose:** Non-technical business setup

### Actions:
1. `biz-marketing`: Create landing page, SEO, content
2. `biz-sales`: Set up CRM, outreach templates
3. `biz-finance`: Configure billing (Stripe), invoicing
4. `biz-support`: Create help docs, chatbot
5. `biz-legal`: Generate ToS, privacy policy

---

## Phase 8: Growth Loop

**Purpose:** Continuous improvement

### Cycle:
```
MONITOR -> ANALYZE -> OPTIMIZE -> DEPLOY -> MONITOR
    |
Customer feedback -> Feature requests -> Backlog
    |
A/B tests -> Winner -> Permanent deploy
    |
Incidents -> RCA -> Prevention -> Deploy fix
```

### Never "Done":
- Run performance optimizations
- Add missing test coverage
- Improve documentation
- Refactor code smells
- Update dependencies
- Enhance user experience
- Implement A/B test learnings

---

## Final Review (Before Any Deployment)

```
1. Dispatch 3 reviewers reviewing ENTIRE implementation:
   - code-reviewer: Full codebase quality
   - business-logic-reviewer: All requirements met
   - security-reviewer: Full security audit

2. Aggregate findings across all files
3. Fix Critical/High/Medium issues
4. Re-run all 3 reviewers until all PASS
5. Generate final report in .loki/artifacts/reports/final-review.md
6. Proceed to deployment only after all PASS
```

---

## Quality Gates Summary

| Gate | Agent | Pass Criteria |
|------|-------|---------------|
| Unit Tests | eng-qa | 100% pass |
| Integration Tests | eng-qa | 100% pass |
| E2E Tests | eng-qa | 100% pass |
| Coverage | eng-qa | > 80% |
| Linting | eng-qa | 0 errors |
| Type Check | eng-qa | 0 errors |
| Security Scan | ops-security | 0 high/critical |
| Dependency Audit | ops-security | 0 vulnerabilities |
| Performance | eng-qa | p99 < 200ms |
| Accessibility | eng-frontend | WCAG 2.1 AA |
| Load Test | ops-devops | Handles 10x expected traffic |
| Chaos Test | ops-devops | Recovers from failures |
| Cost Estimate | ops-cost | Within budget |
| Legal Review | biz-legal | Compliant |

---

## Reference: Task Queue

# Task Queue Reference

Distributed task queue system, dead letter handling, and circuit breakers.

---

## Task Schema

```json
{
  "id": "uuid",
  "idempotencyKey": "hash-of-task-content",
  "type": "eng-backend|eng-frontend|ops-devops|...",
  "priority": 1-10,
  "dependencies": ["task-id-1", "task-id-2"],
  "payload": {
    "action": "implement|test|deploy|...",
    "target": "file/path or resource",
    "params": {},
    "goal": "What success looks like (high-level objective)",
    "constraints": ["No third-party deps", "Maintain backwards compat"],
    "context": {
      "relatedFiles": ["file1.ts", "file2.ts"],
      "architectureDecisions": ["ADR-001: Use JWT tokens"],
      "previousAttempts": "What was tried before, why it failed"
    }
  },
  "createdAt": "ISO",
  "claimedBy": null,
  "claimedAt": null,
  "timeout": 3600,
  "retries": 0,
  "maxRetries": 3,
  "backoffSeconds": 60,
  "lastError": null,
  "completedAt": null,
  "result": {
    "status": "success|failed",
    "output": "What was produced",
    "decisionReport": { ... }
  }
}
```

**Decision Report is REQUIRED for completed tasks.** Tasks without proper decision documentation will be marked as incomplete.

---

## Queue Files

```
.loki/queue/
+-- pending.json       # Tasks waiting to be claimed
+-- in-progress.json   # Currently executing tasks
+-- completed.json     # Finished tasks
+-- dead-letter.json   # Failed tasks for review
+-- cancelled.json     # Cancelled tasks
```

---

## Queue Operations

### Claim Task (with file locking)

```python
def claim_task(agent_id, agent_capabilities):
    with file_lock(".loki/state/locks/queue.lock", timeout=10):
        pending = read_json(".loki/queue/pending.json")

        # Find eligible task
        for task in sorted(pending.tasks, key=lambda t: -t.priority):
            if task.type not in agent_capabilities:
                continue
            if task.claimedBy and not claim_expired(task):
                continue
            if not all_dependencies_completed(task.dependencies):
                continue
            if circuit_breaker_open(task.type):
                continue

            # Claim it
            task.claimedBy = agent_id
            task.claimedAt = now()
            move_task(task, "pending", "in-progress")
            return task

        return None
```

### File Locking (Bash)

```bash
#!/bin/bash
# Atomic task claim using flock

QUEUE_FILE=".loki/queue/pending.json"
LOCK_FILE=".loki/state/locks/queue.lock"

(
  flock -x -w 10 200 || exit 1

  # Read, claim, write atomically
  TASK=$(jq -r '.tasks | map(select(.claimedBy == null)) | .[0]' "$QUEUE_FILE")
  if [ "$TASK" != "null" ]; then
    TASK_ID=$(echo "$TASK" | jq -r '.id')
    jq --arg id "$TASK_ID" --arg agent "$AGENT_ID" \
      '.tasks |= map(if .id == $id then .claimedBy = $agent | .claimedAt = now else . end)' \
      "$QUEUE_FILE" > "${QUEUE_FILE}.tmp" && mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"
    echo "$TASK_ID"
  fi

) 200>"$LOCK_FILE"
```

### Complete Task

```python
def complete_task(task_id, result, success=True):
    with file_lock(".loki/state/locks/queue.lock"):
        task = find_task(task_id, "in-progress")
        task.completedAt = now()
        task.result = result

        if success:
            move_task(task, "in-progress", "completed")
            reset_circuit_breaker(task.type)
            trigger_dependents(task_id)
        else:
            handle_failure(task)
```

---

## Failure Handling

### Exponential Backoff

```python
def handle_failure(task):
    task.retries += 1
    task.lastError = get_last_error()

    if task.retries >= task.maxRetries:
        # Move to dead letter queue
        move_task(task, "in-progress", "dead-letter")
        increment_circuit_breaker(task.type)
        alert_orchestrator(f"Task {task.id} moved to dead letter queue")
    else:
        # Exponential backoff: 60s, 120s, 240s, ...
        task.backoffSeconds = task.backoffSeconds * (2 ** (task.retries - 1))
        task.availableAt = now() + task.backoffSeconds
        move_task(task, "in-progress", "pending")
        log(f"Task {task.id} retry {task.retries}, backoff {task.backoffSeconds}s")
```

---

## Dead Letter Queue

Tasks in dead letter queue require manual review:

### Review Process

1. Read `.loki/queue/dead-letter.json`
2. For each task:
   - Analyze `lastError` and failure pattern
   - Determine if:
     - Task is invalid -> delete
     - Bug in agent -> fix agent, retry
     - External dependency down -> wait, retry
     - Requires human decision -> escalate
3. To retry: move task back to pending with reset retries
4. Log decision in `.loki/logs/decisions/dlq-review-{date}.md`

---

## Idempotency

```python
def enqueue_task(task):
    # Generate idempotency key from content
    task.idempotencyKey = hash(json.dumps(task.payload, sort_keys=True))

    # Check if already exists
    for queue in ["pending", "in-progress", "completed"]:
        existing = find_by_idempotency_key(task.idempotencyKey, queue)
        if existing:
            log(f"Duplicate task detected: {task.idempotencyKey}")
            return existing.id  # Return existing, don't create duplicate

    # Safe to create
    save_task(task, "pending")
    return task.id
```

---

## Task Cancellation

```python
def cancel_task(task_id, reason):
    with file_lock(".loki/state/locks/queue.lock"):
        for queue in ["pending", "in-progress"]:
            task = find_task(task_id, queue)
            if task:
                task.cancelledAt = now()
                task.cancelReason = reason
                move_task(task, queue, "cancelled")

                # Cancel dependent tasks too
                for dep_task in find_tasks_depending_on(task_id):
                    cancel_task(dep_task.id, f"Parent {task_id} cancelled")

                return True
        return False
```

---

## Circuit Breakers

### State Schema

```json
{
  "circuitBreakers": {
    "eng-backend": {
      "state": "closed",
      "failures": 0,
      "lastFailure": null,
      "openedAt": null,
      "halfOpenAt": null
    }
  }
}
```

### States

| State | Description | Behavior |
|-------|-------------|----------|
| **closed** | Normal operation | Tasks flow normally |
| **open** | Too many failures | Block all tasks of this type |
| **half-open** | Testing recovery | Allow 1 test task |

### Configuration

```yaml
# .loki/config/circuit-breakers.yaml
defaults:
  failureThreshold: 5
  cooldownSeconds: 300
  halfOpenAfter: 60

overrides:
  ops-security:
    failureThreshold: 3  # More sensitive for security
  biz-marketing:
    failureThreshold: 10  # More tolerant for non-critical
```

### Implementation

```python
def check_circuit_breaker(agent_type):
    cb = load_circuit_breaker(agent_type)

    if cb.state == "closed":
        return True  # Proceed

    if cb.state == "open":
        if now() > cb.openedAt + config.halfOpenAfter:
            cb.state = "half-open"
            save_circuit_breaker(cb)
            return True  # Allow test task
        return False  # Still blocking

    if cb.state == "half-open":
        return False  # Already testing, wait

def on_task_success(agent_type):
    cb = load_circuit_breaker(agent_type)
    if cb.state == "half-open":
        cb.state = "closed"
        cb.failures = 0
    save_circuit_breaker(cb)

def on_task_failure(agent_type):
    cb = load_circuit_breaker(agent_type)
    cb.failures += 1
    cb.lastFailure = now()

    if cb.state == "half-open" or cb.failures >= config.failureThreshold:
        cb.state = "open"
        cb.openedAt = now()
        alert_orchestrator(f"Circuit breaker OPEN for {agent_type}")

    save_circuit_breaker(cb)
```

---

## Rate Limit Handling

### Detection

```python
def detect_rate_limit(error):
    indicators = [
        "rate limit",
        "429",
        "too many requests",
        "quota exceeded",
        "retry-after"
    ]
    return any(ind in str(error).lower() for ind in indicators)
```

### Response Protocol

```python
def handle_rate_limit(agent_id, error):
    # 1. Save state checkpoint
    checkpoint_state(agent_id)

    # 2. Calculate backoff
    retry_after = parse_retry_after(error) or calculate_exponential_backoff()

    # 3. Log and wait
    log(f"Rate limit hit for {agent_id}, waiting {retry_after}s")

    # 4. Signal other agents to slow down
    broadcast_signal("SLOWDOWN", {"wait": retry_after / 2})

    # 5. Resume after backoff
    schedule_resume(agent_id, retry_after)
```

### Exponential Backoff

```python
def calculate_exponential_backoff(attempt=1, base=60, max_wait=3600):
    wait = min(base * (2 ** (attempt - 1)), max_wait)
    jitter = random.uniform(0, wait * 0.1)
    return wait + jitter
```

---

## Priority System

| Priority | Use Case | Example |
|----------|----------|---------|
| 10 | Critical blockers | Security vulnerability fix |
| 8-9 | High priority | Core feature implementation |
| 5-7 | Normal | Standard tasks |
| 3-4 | Low priority | Documentation, cleanup |
| 1-2 | Background | Nice-to-have improvements |

Tasks are always processed in priority order within their type.

---

## Reference: Tool Orchestration

# Tool Orchestration Patterns Reference

Research-backed patterns inspired by NVIDIA ToolOrchestra, OpenAI Agents SDK, and multi-agent coordination research.

---

## Overview

Effective tool orchestration requires four key innovations:
1. **Tracing Spans** - Hierarchical event tracking (OpenAI SDK pattern)
2. **Efficiency Metrics** - Track computational cost per task
3. **Reward Signals** - Outcome, efficiency, and preference rewards for learning
4. **Dynamic Selection** - Adapt agent count and types based on task complexity

---

## Tracing Spans Architecture (OpenAI SDK Pattern)

### Span Types

Every operation is wrapped in a typed span for observability:

```yaml
span_types:
  agent_span:     # Wraps entire agent execution
  generation_span: # Wraps LLM API calls
  function_span:  # Wraps tool/function calls
  guardrail_span: # Wraps validation checks
  handoff_span:   # Wraps agent-to-agent transfers
  custom_span:    # User-defined operations
```

### Hierarchical Trace Structure

```json
{
  "trace_id": "trace_abc123def456",
  "workflow_name": "implement_feature",
  "group_id": "session_xyz789",
  "spans": [
    {
      "span_id": "span_001",
      "parent_id": null,
      "type": "agent_span",
      "agent_name": "orchestrator",
      "started_at": "2026-01-07T10:00:00Z",
      "ended_at": "2026-01-07T10:05:00Z",
      "children": ["span_002", "span_003"]
    },
    {
      "span_id": "span_002",
      "parent_id": "span_001",
      "type": "guardrail_span",
      "guardrail_name": "input_validation",
      "triggered": false,
      "blocking": true
    },
    {
      "span_id": "span_003",
      "parent_id": "span_001",
      "type": "handoff_span",
      "from_agent": "orchestrator",
      "to_agent": "backend-dev"
    }
  ]
}
```

### Storage Location

```
.loki/traces/
├── active/
│   └── {trace_id}.json     # Currently running traces
└── completed/
    └── {date}/
        └── {trace_id}.json # Archived traces
```

See `references/openai-patterns.md` for full tracing implementation.

---

## Efficiency Metrics System

### Why Track Efficiency?

ToolOrchestra achieves 70% cost reduction vs GPT-5 by explicitly optimizing for efficiency. Loki Mode should track:

- **Token usage** per task (input + output)
- **Wall clock time** per task
- **Agent spawns** per task
- **Retry count** before success

### Efficiency Tracking Schema

```json
{
  "task_id": "task-2026-01-06-001",
  "correlation_id": "session-abc123",
  "started_at": "2026-01-06T10:00:00Z",
  "completed_at": "2026-01-06T10:05:32Z",
  "metrics": {
    "wall_time_seconds": 332,
    "agents_spawned": 3,
    "total_agent_calls": 7,
    "retry_count": 1,
    "retry_reasons": ["test_failure"],
    "recovery_rate": 1.0,
    "model_usage": {
      "haiku": {"calls": 4, "est_tokens": 12000},
      "sonnet": {"calls": 2, "est_tokens": 8000},
      "opus": {"calls": 1, "est_tokens": 6000}
    }
  },
  "outcome": "success",
  "outcome_reason": "tests_passed_after_fix",
  "efficiency_score": 0.85,
  "efficiency_factors": ["used_haiku_for_tests", "parallel_review"],
  "quality_pillars": {
    "tool_selection_correct": true,
    "tool_reliability_rate": 0.95,
    "memory_retrieval_relevant": true,
    "goal_adherence": 1.0
  }
}
```

**Why capture these metrics?** (Based on multi-agent research)

1. **Capture intent, not just actions** ([Hashrocket](https://hashrocket.substack.com/p/the-hidden-cost-of-well-fix-it-later))
   - "UX debt turns into data debt" - recording actions without intent creates useless analytics

2. **Track recovery rate** ([Assessment Framework, arXiv 2512.12791](https://arxiv.org/html/2512.12791v1))
   - `recovery_rate = successful_retries / total_retries`
   - Paper found "perfect tool sequencing but only 33% policy adherence" - surface metrics mask failures

3. **Distributed tracing** ([Maxim AI](https://www.getmaxim.ai/articles/best-practices-for-building-production-ready-multi-agent-systems/))
   - `correlation_id`: Links all tasks in a session for end-to-end tracing
   - Essential for debugging multi-agent coordination failures

4. **Tool reliability separate from selection** ([Stanford/Harvard](https://www.marktechpost.com/2025/12/24/this-ai-paper-from-stanford-and-harvard-explains-why-most-agentic-ai-systems-feel-impressive-in-demos-and-then-completely-fall-apart-in-real-use/))
   - `tool_selection_correct`: Did we pick the right tool?
   - `tool_reliability_rate`: Did the tool work as expected? (tools can fail even when correctly selected)
   - Key insight: "Tool use reliability" is a primary demo-to-deployment gap

5. **Quality pillars beyond outcomes** ([Assessment Framework](https://arxiv.org/html/2512.12791v1))
   - `memory_retrieval_relevant`: Did episodic/semantic retrieval help?
   - `goal_adherence`: Did we stay on task? (0.0-1.0 score)

### Efficiency Score Calculation

```python
def calculate_efficiency_score(metrics, task_complexity):
    """
    Score from 0-1 where higher is more efficient.
    Based on ToolOrchestra's efficiency reward signal.
    """
    # Baseline expectations by complexity
    baselines = {
        "trivial": {"time": 60, "agents": 1, "retries": 0},
        "simple": {"time": 180, "agents": 2, "retries": 0},
        "moderate": {"time": 600, "agents": 4, "retries": 1},
        "complex": {"time": 1800, "agents": 8, "retries": 2},
        "critical": {"time": 3600, "agents": 12, "retries": 3}
    }

    baseline = baselines[task_complexity]

    # Calculate component scores (1.0 = at baseline, >1 = better, <1 = worse)
    time_score = min(1.0, baseline["time"] / max(metrics["wall_time_seconds"], 1))
    agent_score = min(1.0, baseline["agents"] / max(metrics["agents_spawned"], 1))
    retry_score = 1.0 - (metrics["retry_count"] / (baseline["retries"] + 3))

    # Weighted average (time matters most)
    return (time_score * 0.5) + (agent_score * 0.3) + (retry_score * 0.2)
```

### Standard Reason Codes

Use consistent codes to enable pattern analysis:

```yaml
outcome_reasons:
  success:
    - tests_passed_first_try
    - tests_passed_after_fix
    - review_approved
    - spec_validated
  partial:
    - tests_partial_pass
    - review_concerns_minor
    - timeout_partial_work
  failure:
    - tests_failed
    - review_blocked
    - dependency_missing
    - timeout_no_progress
    - error_unrecoverable

retry_reasons:
  - test_failure
  - lint_error
  - type_error
  - review_rejection
  - rate_limit
  - timeout
  - dependency_conflict

efficiency_factors:
  positive:
    - used_haiku_for_simple
    - parallel_execution
    - cached_result
    - first_try_success
    - spec_driven
  negative:
    - used_opus_for_simple
    - sequential_when_parallel_possible
    - multiple_retries
    - missing_context
    - unclear_requirements
```

### Storage Location

```
.loki/metrics/
├── efficiency/
│   ├── 2026-01-06.json      # Daily efficiency logs
│   └── aggregate.json        # Running averages by task type
└── rewards/
    ├── outcomes.json         # Task success/failure records
    └── preferences.json      # User preference signals
```

---

## Reward Signal Framework

### Three Reward Types (ToolOrchestra Pattern)

```
+------------------------------------------------------------------+
| 1. OUTCOME REWARD                                                 |
|    - Did the task succeed? Binary + quality grade                 |
|    - Signal: +1.0 (success), 0.0 (partial), -1.0 (failure)       |
+------------------------------------------------------------------+
| 2. EFFICIENCY REWARD                                              |
|    - Did we use resources wisely?                                 |
|    - Signal: 0.0 to 1.0 based on efficiency score                |
+------------------------------------------------------------------+
| 3. PREFERENCE REWARD                                              |
|    - Did the user like the approach/result?                       |
|    - Signal: Inferred from user actions (accept/reject/modify)   |
+------------------------------------------------------------------+
```

### Outcome Reward Implementation

```python
def calculate_outcome_reward(task_result):
    """
    Outcome reward based on task completion status.
    """
    if task_result.status == "completed":
        # Grade the quality of completion
        if task_result.tests_passed and task_result.review_passed:
            return 1.0  # Full success
        elif task_result.tests_passed:
            return 0.7  # Tests pass but review had concerns
        else:
            return 0.3  # Completed but with issues

    elif task_result.status == "partial":
        return 0.0  # Partial completion, no reward

    else:  # failed
        return -1.0  # Negative reward for failure
```

### Preference Reward Implementation

```python
def infer_preference_reward(task_result, user_actions):
    """
    Infer user preference from their actions after task completion.
    Based on implicit feedback patterns.
    """
    signals = []

    # Positive signals
    if "commit" in user_actions:
        signals.append(0.8)  # User committed our changes
    if "deploy" in user_actions:
        signals.append(1.0)  # User deployed our changes
    if "no_edits" in user_actions:
        signals.append(0.6)  # User didn't modify our output

    # Negative signals
    if "revert" in user_actions:
        signals.append(-1.0)  # User reverted our changes
    if "manual_fix" in user_actions:
        signals.append(-0.5)  # User had to fix our work
    if "retry_different" in user_actions:
        signals.append(-0.3)  # User asked for different approach

    # Neutral (no signal)
    if not signals:
        return None

    return sum(signals) / len(signals)
```

### Reward Aggregation for Learning

```python
def aggregate_rewards(outcome, efficiency, preference):
    """
    Combine rewards into single learning signal.
    Weights based on ToolOrchestra findings.
    """
    # Outcome is most important (must succeed)
    # Efficiency secondary (once successful, optimize)
    # Preference tertiary (align with user style)

    weights = {
        "outcome": 0.6,
        "efficiency": 0.25,
        "preference": 0.15
    }

    total = outcome * weights["outcome"]
    total += efficiency * weights["efficiency"]

    if preference is not None:
        total += preference * weights["preference"]
    else:
        # Redistribute weight if no preference signal
        total = total / (1 - weights["preference"])

    return total
```

---

## Dynamic Agent Selection

### Task Complexity Classification

```python
def classify_task_complexity(task):
    """
    Classify task to determine agent allocation.
    Based on ToolOrchestra's tool selection flexibility.
    """
    complexity_signals = {
        # File scope signals
        "single_file": -1,
        "few_files": 0,       # 2-5 files
        "many_files": +1,     # 6-20 files
        "system_wide": +2,    # 20+ files

        # Change type signals
        "typo_fix": -2,
        "bug_fix": 0,
        "feature": +1,
        "refactor": +1,
        "architecture": +2,

        # Domain signals
        "documentation": -1,
        "tests_only": 0,
        "frontend": 0,
        "backend": 0,
        "full_stack": +1,
        "infrastructure": +1,
        "security": +2,
    }

    score = 0
    for signal, weight in complexity_signals.items():
        if task.has_signal(signal):
            score += weight

    # Map score to complexity level
    if score <= -2:
        return "trivial"
    elif score <= 0:
        return "simple"
    elif score <= 2:
        return "moderate"
    elif score <= 4:
        return "complex"
    else:
        return "critical"
```

### Agent Allocation by Complexity

```yaml
# Agent allocation strategy
# Model selection: Opus=planning, Sonnet=development, Haiku=unit tests/monitoring
complexity_allocations:
  trivial:
    max_agents: 1
    planning: null         # No planning needed
    development: haiku
    testing: haiku
    review: skip           # No review needed for trivial
    parallel: false

  simple:
    max_agents: 2
    planning: null         # No planning needed
    development: haiku
    testing: haiku
    review: single         # One quick review
    parallel: false

  moderate:
    max_agents: 4
    planning: sonnet       # Sonnet for moderate planning
    development: sonnet
    testing: haiku         # Unit tests always haiku
    review: standard       # 3 parallel reviewers
    parallel: true

  complex:
    max_agents: 8
    planning: opus         # Opus ONLY for complex planning
    development: sonnet    # Sonnet for implementation
    testing: haiku         # Unit tests still haiku
    review: deep           # 3 reviewers + devil's advocate
    parallel: true

  critical:
    max_agents: 12
    planning: opus         # Opus for critical planning
    development: sonnet    # Sonnet for implementation
    testing: sonnet        # Functional/E2E tests with sonnet
    review: exhaustive     # Multiple review rounds
    parallel: true
    human_checkpoint: true # Pause for human review
```

### Dynamic Selection Algorithm

```python
def select_agents_for_task(task, available_agents):
    """
    Dynamically select agents based on task requirements.
    Inspired by ToolOrchestra's configurable tool selection.
    """
    complexity = classify_task_complexity(task)
    allocation = COMPLEXITY_ALLOCATIONS[complexity]

    # 1. Identify required agent types
    required_types = identify_required_agents(task)

    # 2. Filter to available agents of required types
    candidates = [a for a in available_agents if a.type in required_types]

    # 3. Score candidates by past performance
    for agent in candidates:
        agent.selection_score = get_agent_performance_score(
            agent,
            task_type=task.type,
            complexity=complexity
        )

    # 4. Select top N agents up to allocation limit
    candidates.sort(key=lambda a: a.selection_score, reverse=True)
    selected = candidates[:allocation["max_agents"]]

    # 5. Assign models based on complexity
    for agent in selected:
        if agent.role == "reviewer":
            agent.model = "opus"  # Always opus for reviews
        else:
            agent.model = allocation["model"]

    return selected

def get_agent_performance_score(agent, task_type, complexity):
    """
    Score agent based on historical performance on similar tasks.
    Uses reward signals from previous executions.
    """
    history = load_agent_history(agent.id)

    # Filter to similar tasks
    similar = [h for h in history
               if h.task_type == task_type
               and h.complexity == complexity]

    if not similar:
        return 0.5  # Neutral score if no history

    # Average past rewards
    return sum(h.aggregate_reward for h in similar) / len(similar)
```

---

## Tool Usage Analytics

### Track Tool Effectiveness

```json
{
  "tool_analytics": {
    "period": "2026-01-06",
    "by_tool": {
      "Grep": {
        "calls": 142,
        "success_rate": 0.89,
        "avg_result_quality": 0.82,
        "common_patterns": ["error handling", "function def"]
      },
      "Task": {
        "calls": 47,
        "success_rate": 0.94,
        "avg_efficiency": 0.76,
        "by_subagent_type": {
          "general-purpose": {"calls": 35, "success": 0.91},
          "Explore": {"calls": 12, "success": 1.0}
        }
      }
    },
    "insights": [
      "Explore agent 100% success - use more for codebase search",
      "Grep success drops to 0.65 for regex patterns - simplify searches"
    ]
  }
}
```

### Continuous Improvement Loop

```
+------------------------------------------------------------------+
| 1. COLLECT                                                        |
|    Record every task: agents used, tools called, outcome          |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
| 2. ANALYZE                                                        |
|    Weekly aggregation: What worked? What didn't?                  |
|    Identify patterns in high-reward vs low-reward tasks           |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
| 3. ADAPT                                                          |
|    Update selection algorithms based on analytics                 |
|    Store successful patterns in semantic memory                   |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
| 4. VALIDATE                                                       |
|    A/B test new selection strategies                              |
|    Measure efficiency improvement                                 |
+------------------------------------------------------------------+
          |
          +-----------> Loop back to COLLECT
```

---

## Integration with RARV Cycle

The orchestration patterns integrate with RARV at each phase:

```
REASON:
├── Check efficiency metrics for similar past tasks
├── Classify task complexity
└── Select appropriate agent allocation

ACT:
├── Dispatch agents according to allocation
├── Track start time and resource usage
└── Record tool calls and agent interactions

REFLECT:
├── Calculate outcome reward (did it work?)
├── Calculate efficiency reward (resource usage)
└── Log to metrics store

VERIFY:
├── Run verification checks
├── If failed: negative outcome reward, retry with learning
├── If passed: infer preference reward from user actions
└── Update agent performance scores
```

---

## Key Metrics Dashboard

Track these metrics in `.loki/metrics/dashboard.json`:

```json
{
  "dashboard": {
    "period": "rolling_7_days",
    "summary": {
      "tasks_completed": 127,
      "success_rate": 0.94,
      "avg_efficiency_score": 0.78,
      "avg_outcome_reward": 0.82,
      "avg_preference_reward": 0.71,
      "avg_recovery_rate": 0.87,
      "avg_goal_adherence": 0.93
    },
    "quality_pillars": {
      "tool_selection_accuracy": 0.91,
      "tool_reliability_rate": 0.93,
      "memory_retrieval_relevance": 0.84,
      "policy_adherence": 0.96
    },
    "trends": {
      "efficiency": "+12% vs previous week",
      "success_rate": "+3% vs previous week",
      "avg_agents_per_task": "-0.8 (improving)",
      "recovery_rate": "+5% vs previous week"
    },
    "top_performing_patterns": [
      "Haiku for unit tests (0.95 success, 0.92 efficiency)",
      "Explore agent for codebase search (1.0 success)",
      "Parallel review with opus (0.98 accuracy)"
    ],
    "areas_for_improvement": [
      "Complex refactors taking 2x expected time",
      "Security review efficiency below baseline",
      "Memory retrieval relevance below 0.85 target"
    ]
  }
}
```

---

## Multi-Dimensional Evaluation

Based on [Measurement Imbalance research (arXiv 2506.02064)](https://arxiv.org/abs/2506.02064):

> "Technical metrics dominate assessments (83%), while human-centered (30%), safety (53%), and economic (30%) remain peripheral"

**Loki Mode tracks four evaluation axes:**

| Axis | Metrics | Current Coverage |
|------|---------|------------------|
| **Technical** | success_rate, efficiency_score, recovery_rate | Full |
| **Human-Centered** | preference_reward, goal_adherence | Partial |
| **Safety** | policy_adherence, quality_gates_passed | Full (via review system) |
| **Economic** | model_usage, agents_spawned, wall_time | Full |

---

## Sources

**OpenAI Agents SDK:**
- [Agents SDK Documentation](https://openai.github.io/openai-agents-python/) - Core primitives: agents, handoffs, guardrails, tracing
- [Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) - Orchestration patterns
- [Building Agents Track](https://developers.openai.com/tracks/building-agents/) - Official developer guide
- [AGENTS.md Specification](https://agents.md/) - Standard for agent instructions
- [Tracing Documentation](https://openai.github.io/openai-agents-python/tracing/) - Span types and observability

**Efficiency & Orchestration:**
- [NVIDIA ToolOrchestra](https://github.com/NVlabs/ToolOrchestra) - Multi-turn tool orchestration with RL
- [ToolScale Dataset](https://huggingface.co/datasets/nvidia/ToolScale) - Training data synthesis

**Evaluation Frameworks:**
- [Assessment Framework for Agentic AI (arXiv 2512.12791)](https://arxiv.org/html/2512.12791v1) - Four-pillar evaluation model
- [Measurement Imbalance in Agentic AI (arXiv 2506.02064)](https://arxiv.org/abs/2506.02064) - Multi-dimensional evaluation
- [Adaptive Monitoring for Agentic AI (arXiv 2509.00115)](https://arxiv.org/abs/2509.00115) - AMDM algorithm

**Best Practices:**
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Simplicity, transparency, tool engineering
- [Maxim AI: Production Multi-Agent Systems](https://www.getmaxim.ai/articles/best-practices-for-building-production-ready-multi-agent-systems/) - Orchestration patterns, distributed tracing
- [UiPath: Agent Builder Best Practices](https://www.uipath.com/blog/ai/agent-builder-best-practices) - Single-responsibility, evaluations
- [Stanford/Harvard: Demo-to-Deployment Gap](https://www.marktechpost.com/2025/12/24/this-ai-paper-from-stanford-and-harvard-explains-why-most-agentic-ai-systems-feel-impressive-in-demos-and-then-completely-fall-apart-in-real-use/) - Tool reliability as key failure mode

**Safety & Reasoning:**
- [Chain of Thought Monitoring](https://openai.com/index/chain-of-thought-monitoring/) - CoT monitorability for safety
- [Agent Builder Safety](https://platform.openai.com/docs/guides/agent-builder-safety) - Human-in-loop patterns
- [Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) - Industry standards (MCP, AGENTS.md, goose)

---

## Example: Api Only

# PRD: REST API Service

## Overview
A simple REST API for managing notes. Tests Loki Mode's backend-only capabilities.

## Target Users
Developers who need a notes API.

## API Endpoints

### Notes Resource

#### GET /api/notes
- Returns list of all notes
- Response: `[{ id, title, content, createdAt }]`

#### GET /api/notes/:id
- Returns single note
- Response: `{ id, title, content, createdAt }`
- Error: 404 if not found

#### POST /api/notes
- Creates new note
- Body: `{ title, content }`
- Response: `{ id, title, content, createdAt }`
- Error: 400 if validation fails

#### PUT /api/notes/:id
- Updates existing note
- Body: `{ title?, content? }`
- Response: `{ id, title, content, updatedAt }`
- Error: 404 if not found

#### DELETE /api/notes/:id
- Deletes note
- Response: 204 No Content
- Error: 404 if not found

### Health Check

#### GET /health
- Returns `{ status: "ok", timestamp }`

## Tech Stack
- Runtime: Node.js 18+
- Framework: Express.js
- Database: In-memory (array) for simplicity
- Validation: zod or joi
- Testing: Jest + supertest

## Requirements
- Input validation on all endpoints
- Proper HTTP status codes
- JSON error responses
- Request logging
- Unit tests for each endpoint

## Out of Scope
- Authentication
- Database persistence
- Rate limiting
- API documentation (OpenAPI)
- Deployment

## Test Cases
```
POST /api/notes with valid data → 201 + note object
POST /api/notes with missing title → 400 + error
GET /api/notes → 200 + array
GET /api/notes/:id with valid id → 200 + note
GET /api/notes/:id with invalid id → 404
PUT /api/notes/:id with valid data → 200 + updated note
DELETE /api/notes/:id → 204
GET /health → 200 + status object
```

---

**Purpose:** Tests backend agent capabilities, code review, and QA without frontend complexity.

---

## Example: Full Stack Demo

# PRD: Full-Stack Demo App

## Overview
A complete full-stack application demonstrating Loki Mode's end-to-end capabilities. A simple bookmark manager with tags.

## Target Users
Users who want to save and organize bookmarks.

## Features

### Core Features
1. **Add Bookmark** - Save URL with title and optional tags
2. **View Bookmarks** - List all bookmarks with search/filter
3. **Edit Bookmark** - Update title, URL, or tags
4. **Delete Bookmark** - Remove bookmark
5. **Tag Management** - Create, view, and filter by tags

### User Flow
1. User opens app → sees bookmark list
2. Clicks "Add Bookmark" → form appears
3. Enters URL, title, tags → submits
4. Bookmark appears in list
5. Can filter by tag or search by title
6. Can edit or delete any bookmark

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for bundling
- TailwindCSS for styling
- React Query for data fetching

### Backend
- Node.js 18+
- Express.js
- SQLite with better-sqlite3
- zod for validation

### Structure
```
/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   ├── db/
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## API Endpoints

### Bookmarks
- `GET /api/bookmarks` - List all (query: `?tag=`, `?search=`)
- `POST /api/bookmarks` - Create new
- `PUT /api/bookmarks/:id` - Update
- `DELETE /api/bookmarks/:id` - Delete

### Tags
- `GET /api/tags` - List all tags with counts

## Database Schema
```sql
CREATE TABLE bookmarks (
  id INTEGER PRIMARY KEY,
  url TEXT NOT NULL,
  title TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE bookmark_tags (
  bookmark_id INTEGER REFERENCES bookmarks(id),
  tag_id INTEGER REFERENCES tags(id),
  PRIMARY KEY (bookmark_id, tag_id)
);
```

## Requirements
- TypeScript throughout
- Input validation (frontend + backend)
- Error handling with user feedback
- Loading states
- Empty states
- Responsive design

## Testing
- Backend: Jest + supertest for API tests
- Frontend: Basic component tests (optional)
- E2E: Manual testing checklist

## Out of Scope
- User authentication
- Import/export
- Browser extension
- Cloud deployment
- Real-time sync

## Success Criteria
- All CRUD operations work
- Search and filter work
- No console errors
- Tests pass
- Code review passes (all 3 reviewers)

---

**Purpose:** Comprehensive test of Loki Mode's full capabilities including frontend, backend, database, and code review agents. Expect ~30-60 minutes for full execution.

---

## Example: Simple Todo App

# PRD: Simple Todo App

## Overview
A minimal todo application for testing Loki Mode with a simple, well-defined scope.

## Target Users
Individual users who want a simple way to track tasks.

## Features

### MVP Features
1. **Add Todo** - Users can add a new todo item with a title
2. **View Todos** - Display list of all todos
3. **Complete Todo** - Mark a todo as done
4. **Delete Todo** - Remove a todo from the list

### Tech Stack (Suggested)
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: SQLite (local file)
- No deployment (local testing only)

## Acceptance Criteria

### Add Todo
- [ ] Input field for todo title
- [ ] Submit button
- [ ] New todo appears in list
- [ ] Input clears after submit

### View Todos
- [ ] Shows all todos in a list
- [ ] Shows completion status
- [ ] Empty state when no todos

### Complete Todo
- [ ] Checkbox or button to mark complete
- [ ] Visual indicator for completed items
- [ ] Persists after refresh

### Delete Todo
- [ ] Delete button on each todo
- [ ] Confirmation before delete
- [ ] Removes from list and database

## Out of Scope
- User authentication
- Due dates
- Categories/tags
- Mobile app
- Cloud deployment

## Success Metrics
- All features functional
- Tests passing
- No console errors

---

**Purpose:** This PRD is intentionally simple to allow quick testing of Loki Mode's core functionality without waiting for complex builds or deployments.

---

## Example: Static Landing Page

# PRD: Static Landing Page

## Overview
A simple static landing page for a fictional SaaS product. Tests Loki Mode's frontend and marketing agent capabilities.

## Target Users
Marketing teams needing a quick landing page.

## Page Sections

### Hero Section
- Headline: "Supercharge Your Workflow"
- Subheadline: "The all-in-one tool for modern teams"
- Primary CTA: "Get Started Free"
- Secondary CTA: "Watch Demo"
- Hero image placeholder

### Features Section (3 features)
1. **Fast Setup** - "Get started in minutes, not days"
2. **Team Collaboration** - "Work together seamlessly"
3. **Analytics** - "Track what matters"

### Social Proof
- 3 testimonial cards with placeholder content
- "Trusted by 10,000+ teams"

### Pricing Section
- Free tier: $0/month
- Pro tier: $29/month
- Enterprise: Contact us

### FAQ Section
- 4 common questions with answers

### Footer
- Links: About, Blog, Careers, Contact
- Social icons: Twitter, LinkedIn, GitHub
- Copyright notice

## Tech Stack
- HTML5
- CSS3 (no framework, or Tailwind CSS)
- Minimal JavaScript (for FAQ accordion)
- No build step required

## Requirements
- Responsive design (mobile + desktop)
- Semantic HTML
- Accessible (WCAG 2.1 AA basics)
- Fast load time (< 2s)
- No external dependencies (except fonts)

## Assets
- Use placeholder images (placeholder.com or similar)
- Use system fonts or Google Fonts
- Use emoji for icons if needed

## Out of Scope
- Backend/API
- Form submission handling
- Analytics tracking
- A/B testing
- Deployment

## Deliverables
1. `index.html` - Main page
2. `styles.css` - Stylesheet
3. `script.js` - Minimal JS (optional)
4. `README.md` - How to view locally

---

**Purpose:** Tests frontend agent, marketing agent (copy), and design patterns without backend complexity.
