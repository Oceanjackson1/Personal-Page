---
title: "Setup Ralph"
description: "Set up and configure Geoffrey Huntley's original Ralph Wiggum autonomous coding loop in any directory with proper structure, prompts, and backpressure."
category: "development"
source: "community"
author: "Community"
tags: ["setup", "ralph"]
date: 2026-03-20
---

<essential_principles>
## What is Ralph?

Ralph is Geoffrey Huntley's autonomous AI coding methodology that uses iterative loops with task selection, execution, and validation. In its purest form, it's a Bash loop:

```bash
while :; do cat PROMPT.md | claude ; done
```

The loop feeds a prompt file to Claude, the agent completes one task, updates the implementation plan, commits changes, then exits. The loop restarts immediately with fresh context.

### Core Philosophy

**The Ralph Wiggum Technique is deterministically bad in an undeterministic world.** Ralph solves context accumulation by starting each iteration with fresh context—the core insight behind Geoffrey's approach.

### Three Phases, Two Prompts, One Loop

1. **Planning Phase**: Gap analysis (specs vs code) outputs prioritized TODO list—no implementation, no commits
2. **Building Phase**: Picks tasks from plan, implements, runs tests (backpressure), commits
3. **Observation Phase**: You sit on the loop, not in it—engineer the setup and environment that allows Ralph to succeed

### Key Principles

**Your Role**: Ralph does all the work, including deciding which planned work to implement next and how to implement it. Your job is to engineer the environment.

**Backpressure**: Create backpressure via tests, typechecks, lints, builds that reject invalid/unacceptable work.

**Observation**: Watch, especially early on. Prompts evolve through observed failure patterns.

**Context Efficiency**: With ~176K usable tokens from 200K window, allocating 40-60% to "smart zone" means tight tasks with one task per loop achieves maximum context utilization.

**File I/O as State**: The plan file persists between isolated loop executions, serving as deterministic shared state—no sophisticated orchestration needed.

**Remote Backup**: The loop automatically creates a private GitHub repo and pushes after each commit. This protects against accidental data loss from autonomous operations. Requires `gh` CLI authenticated. Disable with `RALPH_BACKUP=false`.

**Safety Rules**: PROMPT_build.md includes critical safety rules prohibiting dangerous operations like `rm -rf` on project directories. Tests must run in isolated temp directories.
</essential_principles>

<intake>
What would you like to do?

1. **Set up a new Ralph loop** - Initialize Ralph structure in a directory
2. **Understand Ralph concepts** - Learn about the technique and how it works
3. **Customize existing loop** - Modify prompts or configuration
4. **Troubleshoot Ralph** - Debug loop issues or improve performance

Wait for response before proceeding.
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "set up", "setup", "new", "initialize", "create" | `workflows/setup-new-loop.md` |
| 2, "understand", "learn", "concepts", "explain", "how" | `workflows/understand-ralph.md` |
| 3, "customize", "modify", "change", "update", "edit" | `workflows/customize-loop.md` |
| 4, "troubleshoot", "debug", "fix", "problem", "issue" | `workflows/troubleshoot-loop.md` |
| Other | Clarify intent, then select appropriate workflow |

After reading the workflow, follow it exactly.
</routing>

<reference_index>
## Domain Knowledge

All in `references/`:

**Core Concepts:** ralph-fundamentals.md - Three phases, two prompts, one loop
**Structure:** project-structure.md - Required files and directory layout
**Prompts:** prompt-design.md - Planning vs building mode instructions
**Backpressure:** validation-strategy.md - Tests, lints, builds as steering
**Best Practices:** operational-learnings.md - AGENTS.md guidance and evolution
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| setup-new-loop.md | Initialize Ralph structure in a directory |
| understand-ralph.md | Learn Ralph concepts and philosophy |
| customize-loop.md | Modify prompts or loop configuration |
| troubleshoot-loop.md | Debug loop issues and improve performance |
</workflows_index>

<success_criteria>
Skill is successful when:
- User understands which workflow they need
- Appropriate workflow loaded based on intent
- All required references loaded by workflow
- User can set up and run Ralph loops independently
</success_criteria>

---

## Reference: Operational Learnings

# Operational Learnings

Guidance on using AGENTS.md to capture and evolve Ralph's knowledge.

<what_is_agents_md>
## What is AGENTS.md?

AGENTS.md is a file that contains project-specific learnings that Ralph needs to know. It's loaded every loop iteration alongside the prompt.

**Purpose:**
- Capture patterns Ralph should follow
- Document project-specific constraints
- Record discovered learnings from failures
- Provide build/test commands
- Share context that prompts don't include

**Key insight:** AGENTS.md evolves through observation. Start minimal, add only what's needed.
</what_is_agents_md>

<start_minimal>
## Start Minimal

**Initial AGENTS.md (literally this):**
```markdown
# Operational Learnings

This file contains project-specific guidance for Ralph.

## Build/Test Commands

[To be filled as needed]

## Known Patterns

[To be filled as needed]

## Constraints

[To be filled as needed]
```

**Or even simpler (just empty sections):**
```markdown
# Operational Learnings
```

**Don't:**
- Pre-populate with guessed patterns
- Copy from other projects
- Add rules you haven't observed need for
- Try to predict all failure modes

**Do:**
- Start empty or near-empty
- Add entries when Ralph fails repeatedly
- Remove entries when no longer relevant
- Keep it focused and minimal
</start_minimal>

<when_to_add_entries>
## When to Add Entries

Add to AGENTS.md when you observe:

### 1. Repeated Mistakes

**Observation:** Ralph keeps implementing authentication without using the existing auth library
**Entry:**
```markdown
## Known Patterns

### Authentication
Always use src/lib/auth.ts for authentication. Do not implement custom auth logic.
```

### 2. Project-Specific Commands

**Observation:** Tests require specific environment setup
**Entry:**
```markdown
## Build/Test Commands

### Running Tests
```bash
export NODE_ENV=test
npm test
```

Tests require NODE_ENV=test to use test database.
```

### 3. Discovered Constraints

**Observation:** Ralph keeps trying to use a library that's not available
**Entry:**
```markdown
## Constraints

### Dependencies
- Do NOT use lodash (not installed, use native JS instead)
- Do NOT use axios (use native fetch)
- DO use Zod for validation (already installed)
```

### 4. Architectural Decisions

**Observation:** Ralph implements features in inconsistent locations
**Entry:**
```markdown
## Known Patterns

### Code Organization
- UI components: src/components/
- Business logic: src/lib/
- API routes: src/pages/api/
- Database: src/db/

New features should follow this structure.
```

### 5. Gotchas and Edge Cases

**Observation:** Ralph forgets to handle specific edge case
**Entry:**
```markdown
## Known Patterns

### Date Handling
Always handle timezone conversion. User input is in local time, database stores UTC.
Use src/lib/dates.ts utilities for all date operations.
```
</when_to_add_entries>

<when_not_to_add_entries>
## When NOT to Add Entries

Don't add to AGENTS.md for:

### 1. One-Off Mistakes

Ralph made a mistake once, then corrected it. No pattern yet.

**Wait for:** Same mistake 2-3 times, then add guidance.

### 2. General Best Practices

Don't add universal programming wisdom:

**Bad:**
```markdown
## Best Practices
- Write clean code
- Use meaningful variable names
- Handle errors properly
```

**Why:** Claude already knows this. AGENTS.md is for project-specific knowledge.

### 3. Things in Specs

If it's already in the spec, don't duplicate in AGENTS.md.

**Bad:** Spec says "use JWT for auth", AGENTS.md repeats "use JWT for auth"
**Good:** Spec says "handle auth", AGENTS.md says "use src/lib/auth.ts (JWT implementation)"

### 4. Temporary Workarounds

**Bad:**
```markdown
## Workarounds
- API endpoint /v1/users is broken, use /v2/users instead
```

**Why:** This will become stale. Fix the root cause or document in code comments, not AGENTS.md.

### 5. Overly Specific Instructions

**Bad:**
```markdown
## Implementation Steps for User Profile Feature
1. Create src/components/UserProfile.tsx
2. Add props interface with name, email, avatar
3. Import Avatar component from src/components/ui/Avatar
4. Style using Tailwind classes: bg-white rounded-lg shadow-md
...
```

**Why:** This is a task description, not a learning. Put this in specs or let Ralph figure it out.
</when_not_to_add_entries>

<structure_guidance>
## Structure Guidance

Keep AGENTS.md organized and scannable:

### Use Clear Sections

```markdown
# Operational Learnings

## Build/Test Commands
[Commands Ralph needs to run]

## Known Patterns
[Project-specific patterns to follow]

## Constraints
[Things Ralph can't or shouldn't do]

## Architecture
[High-level structure and decisions]

## Gotchas
[Edge cases and non-obvious behaviors]
```

### Use Subsections for Categories

```markdown
## Known Patterns

### Authentication
[Auth-specific patterns]

### Database
[Database-specific patterns]

### API Design
[API-specific patterns]
```

### Keep Entries Concise

**Bad:**
```markdown
### Error Handling
We have a comprehensive error handling system that was implemented
in PR #123. It uses custom error classes that extend the base Error
class. When implementing new features, you should follow this pattern
by creating appropriate error classes and throwing them with descriptive
messages. The error handling middleware will catch these and return
appropriate HTTP status codes. For validation errors, use 400. For
authentication errors, use 401. For authorization errors, use 403...
```

**Good:**
```markdown
### Error Handling
Use custom error classes from src/lib/errors.ts
- ValidationError → 400
- AuthenticationError → 401
- AuthorizationError → 403
```

### Use Code Examples

When patterns are easier to show than describe:

```markdown
### API Response Format
Always return this structure:
```typescript
{
  success: boolean
  data?: any
  error?: { message: string, code: string }
}
```
```
</structure_guidance>

<evolution_over_time>
## Evolution Over Time

AGENTS.md grows and changes with the project:

### Phase 1: Initial Loops (Days 1-3)
- File is mostly empty
- Watching for patterns
- Taking notes but not committing to AGENTS.md yet

### Phase 2: Pattern Recognition (Week 1)
- First entries added based on observed failures
- Mostly build/test commands and constraints
- 20-50 lines total

### Phase 3: Stabilization (Weeks 2-4)
- Known patterns documented
- Architecture decisions captured
- Ralph following patterns more consistently
- 50-150 lines total

### Phase 4: Maturity (Month 2+)
- Well-documented project knowledge
- New entries added rarely
- Occasional cleanup of stale entries
- 100-300 lines total

### Phase 5: Maintenance
- AGENTS.md changes infrequently
- Entries removed when architecture changes
- Project patterns are stable
- Size stays constant or shrinks
</evolution_over_time>

<example_agents_md>
## Example AGENTS.md

Real-world example from a TypeScript web app:

```markdown
# Operational Learnings

## Build/Test Commands

### Running Tests
```bash
npm test                  # All tests
npm test -- --watch      # Watch mode
npm test -- path/to/test # Specific test
```

### Type Checking
```bash
npm run type-check       # TypeScript validation
```

### Building
```bash
npm run build           # Production build
npm run dev             # Development server
```

## Known Patterns

### Authentication
- Use src/lib/auth.ts for all auth operations
- JWT tokens stored in httpOnly cookies
- Refresh tokens in separate cookie
- Don't implement custom auth logic

### Database Queries
- Use Prisma client from src/db/client.ts
- Always use transactions for multi-step operations
- Include error handling for unique constraint violations

### API Design
Response format:
```typescript
{
  success: boolean
  data?: T
  error?: { message: string, code: string }
}
```

### Component Structure
- UI components: src/components/ui/ (no business logic)
- Feature components: src/components/features/ (can have logic)
- Shared hooks: src/hooks/
- Use TypeScript interfaces for all props

## Constraints

### Dependencies
- Use native fetch (not axios)
- Use Zod for validation (already installed)
- Use date-fns for dates (not moment.js)
- Use Tailwind for styling (no CSS modules)

### Database
- Do NOT use raw SQL (use Prisma)
- Do NOT expose internal IDs in API (use UUIDs or slugs)

### Testing
- Do NOT use shallow rendering (use Testing Library)
- Do NOT test implementation details (test behavior)

## Gotchas

### Dates
- User input is local time, database stores UTC
- Always convert using src/lib/dates.ts utilities

### File Uploads
- Max file size: 10MB (enforced by middleware)
- Store in S3, not local filesystem
- Generate signed URLs for access

### Rate Limiting
- API endpoints are rate-limited (100 req/min)
- Auth endpoints stricter (10 req/min)
- Handle 429 responses with exponential backoff
```
</example_agents_md>

<common_categories>
## Common Categories

Categories you might need in AGENTS.md:

### Technical
- Build/Test Commands
- Dependencies and Versions
- Environment Variables
- API Endpoints
- Database Schema Notes

### Patterns
- Code Organization
- Naming Conventions
- Error Handling
- Logging Strategy
- Authentication/Authorization

### Constraints
- What NOT to use
- Performance Requirements
- Security Requirements
- Deployment Constraints

### Business Logic
- Domain Rules
- Calculation Formulas
- State Machines
- Workflow Steps

### Integration
- External APIs
- Third-party Services
- Webhook Handling
- Event Processing

### Testing
- Test Strategy
- Mock Patterns
- Test Data Setup
- CI/CD Notes
</common_categories>

<keeping_it_current>
## Keeping It Current

AGENTS.md can become stale. Regular maintenance:

### Weekly Review
- Read through AGENTS.md
- Remove entries that are now in code patterns
- Remove entries that are outdated
- Add entries from the week's observations

### After Major Changes
- Architecture refactor → update patterns
- Dependency updates → verify commands still work
- New features → add new patterns if emerging

### Signs of Staleness
- Entries contradict current code
- Commands don't work anymore
- Patterns no longer followed
- Ralph ignoring entries (they're wrong)

### Cleanup Triggers
- File over 500 lines → too much, condense
- Same information repeated → consolidate
- Entries no one references → remove
- Contradictory entries → reconcile
</keeping_it_current>

<antipatterns>
## Anti-Patterns

Things to avoid:

### 1. The Novel
AGENTS.md shouldn't be 1000+ lines of comprehensive project documentation. That belongs in real docs.

### 2. The Rule Book
Don't make it a list of "thou shalt not" commands. Keep it practical and pattern-focused.

### 3. The Tutorial
Don't teach programming concepts. Assume Claude is a competent developer, just new to your project.

### 4. The Archive
Don't keep historical notes about decisions. Document current state only.

### 5. The Spec Duplicate
Don't repeat what's in your specs. Reference specs, don't duplicate them.

### 6. The Wishlist
Don't add patterns you wish existed. Document what actually is, not what should be.
</antipatterns>

---

## Reference: Project Structure

# Project Structure

Required files and directory layout for a Ralph loop.

<essential_files>
## Essential Files

### loop.sh
Main orchestration script that runs the loop.

**Minimal implementation:**
```bash
#!/bin/bash
while :; do cat PROMPT.md | claude ; done
```

**Production implementation:**
- Mode switching (plan vs build)
- Iteration limits
- CLI flag configuration
- Error handling

Located at project root.

### PROMPT_plan.md
Instructions for planning mode. Tells Claude to:
- Study specs and existing code
- Perform gap analysis
- Generate/update `IMPLEMENTATION_PLAN.md`
- NOT implement anything

Located at project root.

### PROMPT_build.md
Instructions for building mode. Tells Claude to:
- Read the implementation plan
- Select most important task
- Search existing code
- Implement functionality
- Run validation
- Update plan
- Commit changes

Located at project root.

### IMPLEMENTATION_PLAN.md
The persistent task list that survives across iterations.

**Generated by:** Planning mode
**Updated by:** Building mode (marks tasks complete, adds findings)
**Format:** Markdown with prioritized list

This is the ONLY state that persists between loop iterations. Everything else is fresh context.

Initially empty. Created by first planning mode run.

### AGENTS.md
Operational learnings specific to this project.

**Purpose:** Capture patterns Ralph needs to know
**Updated by:** You (the observer)
**Format:** Markdown with sections

Start minimal (even empty). Add guidance only when Ralph exhibits repeated failures or needs project-specific context.

**Common sections:**
- Build/Test Commands
- Known Patterns
- Discovered Constraints
- Learned Best Practices

Located at project root.
</essential_files>

<directory_structure>
## Directory Structure

```
project-root/
├── loop.sh                    # Orchestration script (executable)
├── PROMPT_plan.md             # Planning mode instructions
├── PROMPT_build.md            # Building mode instructions
├── AGENTS.md                  # Operational learnings (starts minimal)
├── IMPLEMENTATION_PLAN.md     # Task list (generated by planning)
├── specs/                     # Requirement documents
│   ├── topic-1.md
│   ├── topic-2.md
│   └── ...
└── src/                       # Application source code
    ├── lib/                   # Shared utilities
    └── ...
```

### specs/ Directory

Requirement documents following "one sentence without 'and'" principle.

**One file per topic of concern:**
- ✓ `specs/authentication.md` - Describes auth requirements
- ✓ `specs/color-extraction.md` - Describes color analysis requirements
- ✗ `specs/user-system.md` - Too broad (auth AND profiles AND billing)

**Format:**
- Markdown
- Clear requirements
- Examples where helpful
- Acceptance criteria
- NOT implementation details (that's Ralph's job)

### src/ Directory

Application source code. Structure depends on language/framework.

**Common pattern:**
```
src/
├── lib/              # Shared utilities
├── components/       # Reusable components
├── features/         # Feature-specific code
└── tests/           # Test files
```

Ralph learns patterns from existing code in `src/`. Consistent structure helps Ralph maintain consistency.
</directory_structure>

<optional_directories>
## Optional Directories

### .git/
Version control. Ralph commits after each task.

**Required for:**
- Tracking changes
- Reverting mistakes
- Reviewing what Ralph did

Initialize before starting loop:
```bash
git init
git add .
git commit -m "Initial commit"
```

### tests/
Test files for validation backpressure.

**Location:** Depends on language/framework
- JavaScript/TypeScript: Often `src/__tests__/` or `tests/`
- Python: Often `tests/` at root
- Go: Test files alongside source (`*_test.go`)

Ralph needs runnable tests to create backpressure. If no tests exist, Ralph has no feedback mechanism.

### .github/ or .gitlab/
CI/CD configuration (optional).

Ralph can update these, but they're not core to the loop mechanism.
</optional_directories>

<file_loading_order>
## File Loading Order

Each loop iteration loads files in this order:

1. **PROMPT.md** (or mode-specific variant)
   - First ~5,000 tokens
   - Sets the objective

2. **AGENTS.md**
   - Project-specific learnings
   - Patterns Ralph needs to know

3. **IMPLEMENTATION_PLAN.md**
   - Current task list
   - What's done, what's pending

4. **specs/**
   - Requirement documents
   - Loaded via subagents (parallel)

5. **src/**
   - Existing code (as needed)
   - Loaded via subagents (parallel)

Total context budget: ~176K usable tokens from 200K window.

Optimize by:
- Keeping PROMPT.md tight
- Keeping AGENTS.md minimal
- Using parallel subagents for reading
- One task per iteration (focused context)
</file_loading_order>

<topic_of_concern_scope>
## Topic of Concern Scope

**Test:** Can you describe the topic in one sentence without "and"?

**Good examples:**
- "Authentication handles user login and session management" → Split into:
  - `authentication.md` - User login with credentials
  - `session-management.md` - Session lifecycle and validation

- "Color extraction analyzes images for dominant colors" → Keep as one:
  - `color-extraction.md` - Single topic, no conjunction needed

**Why this matters:**
- Each spec file should have clear, focused requirements
- Ralph works better with well-scoped tasks
- Easier to validate completion
- Simpler to update when requirements change

**If unsure:**
- Start with separate files
- Merge later if topics are truly coupled
- Bias toward focused specs
</topic_of_concern_scope>

<minimal_viable_structure>
## Minimal Viable Structure

Absolute minimum to start a Ralph loop:

```
project-root/
├── loop.sh                    # Minimal bash loop
├── PROMPT_build.md            # Building instructions
├── IMPLEMENTATION_PLAN.md     # Empty initially
└── src/                       # Your code
```

You can skip:
- `PROMPT_plan.md` - Write plan manually
- `AGENTS.md` - Start with empty file
- `specs/` - Embed requirements in PROMPT_build.md

**But you should have:**
- Version control (git)
- Tests (for backpressure)
- Clear requirements (somewhere)

**Recommended:** Use full structure. The overhead is minimal, and you'll want it as the loop runs.
</minimal_viable_structure>

---

## Reference: Prompt Design

# Prompt Design

Guidance for writing effective planning and building mode prompts.

<prompt_principles>
## Prompt Principles

### 1. Prompts Are Signs, Not Rules

Ralph learns from:
- Existing code patterns
- AGENTS.md learnings
- Specs requirements
- Validation feedback

The prompt provides initial direction. The environment shapes actual behavior.

### 2. Start Minimal, Evolve Through Observation

Don't try to predict all failure modes. Start with simple instructions and add guidance when you observe specific failures.

**Anti-pattern:**
```markdown
IMPORTANT: Don't do X
CRITICAL: Never do Y
WARNING: Avoid Z
REMEMBER: Always check for...
```

**Better:**
```markdown
1. Study specs
2. Implement task
3. Run tests
4. Commit
```

Add specifics to `AGENTS.md` as patterns emerge.

### 3. One Clear Objective Per Mode

**Planning mode:** Gap analysis only, no implementation
**Building mode:** Implement one task, validate, commit

Mixing objectives (plan AND build) creates confusion.

### 4. Leverage Parallel Subagents

Claude Code can spawn hundreds of subagents for reading/searching. Use this:

```markdown
Study specs/* (up to 500 parallel Sonnet subagents)
```

This tells Claude it's safe and encouraged to use massive parallelism.

### 5. Context Budget Allocation

~176K usable tokens. Typical allocation:
- Prompt: ~5,000 tokens
- AGENTS.md: ~2,000 tokens
- IMPLEMENTATION_PLAN.md: ~5,000 tokens
- Specs: ~20,000 tokens
- Source code: ~100,000 tokens
- "Smart zone" (reasoning): ~40,000 tokens

Keep prompts tight to maximize smart zone.
</prompt_principles>

<planning_prompt_template>
## Planning Prompt Template

```markdown
# Planning Mode

You are Ralph, an autonomous coding agent in planning mode.

## Objective

Study specifications and existing code, then generate a prioritized implementation plan. DO NOT implement anything.

## Process

0a. Study specs/* (use up to 250 parallel Sonnet subagents)
0b. Study @IMPLEMENTATION_PLAN.md (if exists)
0c. Study src/lib/* (shared utilities to understand patterns)
0d. Reference: src/* (as needed for gap analysis)

1. Gap Analysis
   - Compare each spec against existing code
   - Identify what's missing, incomplete, or incorrect
   - IMPORTANT: Don't assume not implemented; confirm with code search first
   - Consider TODO comments, placeholders, and partial implementations

2. Generate/Update IMPLEMENTATION_PLAN.md
   - Prioritized list of tasks
   - Most important/foundational work first
   - Each task should be completable in one loop iteration
   - Include brief context for why each task matters

3. Exit
   - Do NOT implement anything
   - Do NOT commit anything
   - Just generate the plan and exit

## Success Criteria

- IMPLEMENTATION_PLAN.md exists and is prioritized
- Each task is specific and actionable
- Plan reflects actual gaps (confirmed via code search)
- No code changes made
```

**Customization points:**
- Subagent counts (250-500 depending on project size)
- Source directory structure (src/lib/*, src/features/*, etc.)
- Project-specific analysis needs
</planning_prompt_template>

<building_prompt_template>
## Building Prompt Template

```markdown
# Building Mode

You are Ralph, an autonomous coding agent in building mode.

## Objective

Select the most important task from the implementation plan, implement it correctly, validate it works, and commit.

## Process

0a. Study specs/* (use up to 500 parallel Sonnet subagents)
0b. Study @IMPLEMENTATION_PLAN.md
0c. Reference: src/* (use parallel Sonnet subagents for code reading)

1. Select Task
   - Pick the most important task from IMPLEMENTATION_PLAN.md
   - Most important = most foundational or highest priority
   - If unclear, pick the first uncompleted task

2. Investigate Before Implementing
   - Search codebase first (don't assume missing)
   - Understand existing patterns and conventions
   - Use up to 500 Sonnet subagents for reading/searching
   - Identify exactly what needs to change

3. Implement
   - Follow patterns from existing code
   - Reference specs for requirements
   - Write clean, maintainable code
   - Add tests if they don't exist

4. Validate
   - Run: [VALIDATION_COMMANDS]
   - Use only 1 Sonnet subagent for build/tests (creates backpressure)
   - If validation fails, fix and retry
   - Do not commit until validation passes

5. Update Plan
   - Mark completed task in IMPLEMENTATION_PLAN.md
   - Add any new tasks discovered during implementation
   - Note any blockers or issues found

6. Commit
   - Descriptive commit message
   - Format: "[component] brief description"
   - Push changes (if remote configured)

7. Exit
   - End loop iteration
   - Fresh context starts next iteration

## Success Criteria

- One task completed per iteration
- All validation passes
- Changes committed
- Plan updated with progress
```

**Customization points:**
- `[VALIDATION_COMMANDS]` - Project-specific tests/checks
- Subagent counts
- Source directory references
- Commit message format
- Push behavior (if using remote git)
</building_prompt_template>

<validation_commands>
## Validation Commands

Replace `[VALIDATION_COMMANDS]` with project-specific commands:

### JavaScript/TypeScript
```markdown
Run:
- npm test (or yarn test, pnpm test)
- npm run type-check (if using TypeScript)
- npm run lint (if configured)
- npm run build (if applicable)
```

### Python
```markdown
Run:
- pytest
- mypy . (if using type hints)
- ruff check . (or flake8, pylint)
- python -m build (if package)
```

### Go
```markdown
Run:
- go test ./...
- go vet ./...
- golangci-lint run (if configured)
- go build ./...
```

### Rust
```markdown
Run:
- cargo test
- cargo clippy -- -D warnings
- cargo build --release
```

### Minimal (no tooling yet)
```markdown
Run:
- [language] [test_runner] (create if missing)
- Basic smoke test (does it run?)
```

**Principle:** Validation must be automated and binary (pass/fail). If tests don't exist, Ralph should create them.
</validation_commands>

<subagent_guidance>
## Subagent Guidance

### Why Specify Counts?

Claude Code is conservative about spawning subagents unless explicitly permitted. Specifying counts signals:
- It's safe to parallelize
- High counts are acceptable
- Performance is valued

### Recommended Counts

**Reading/searching (Sonnet):**
- Small project (<100 files): 50-100 subagents
- Medium project (100-500 files): 250-500 subagents
- Large project (500+ files): 500+ subagents

**Building/testing (Sonnet):**
- Always 1 subagent
- Creates backpressure
- Sequential validation is intentional

**Why Sonnet?**
- Faster than Opus
- Cheaper than Opus
- Good enough for reading/searching and validation
- Opus is overkill for most Ralph tasks

**Specifying in prompt:**
```markdown
Study specs/* (use up to 500 parallel Sonnet subagents)
Run tests (use only 1 Sonnet subagent)
```

### Main Agent Role

The main agent (Opus or Sonnet for loop) orchestrates:
- Task selection
- Strategy decisions
- Code generation (sometimes delegates to subagents)
- Plan updates

Keep main agent focused on reasoning, delegate I/O to subagents.
</subagent_guidance>

<prompts_evolve>
## Prompts Evolve

### Initial Prompt (Minimal)

Start with basic structure:
```markdown
1. Study specs
2. Pick task from plan
3. Implement
4. Run tests
5. Commit
```

### After Observing Failures

Ralph keeps reimplementing the same thing? Add:
```markdown
2a. Search existing code first (don't assume missing)
```

Ralph writes inconsistent code? Add:
```markdown
3a. Study existing patterns in src/lib/*
3b. Match existing code style and conventions
```

Ralph doesn't update plan? Add:
```markdown
5a. Mark task complete in IMPLEMENTATION_PLAN.md
5b. Note any new tasks discovered
```

### After Many Iterations

Prompts accumulate learnings. But watch for:
- Too many rules (sign of over-steering)
- Contradictory guidance
- Outdated assumptions

Periodically review and simplify. Move stable patterns to `AGENTS.md`.
</prompts_evolve>

<common_prompt_mistakes>
## Common Prompt Mistakes

### Mistake 1: Mixing Modes

**Bad:**
```markdown
Generate a plan, then start implementing the first task...
```

**Good:**
```markdown
Planning mode: Generate plan only, do not implement
Building mode: Implement from plan, one task per iteration
```

### Mistake 2: Over-Specifying

**Bad:**
```markdown
CRITICAL: Before implementing, you must:
1. Read all files in src/
2. Check for existing implementations of similar features
3. Review the git history for context
4. Consider performance implications
5. Think about edge cases
6. Validate against all specs
...
```

**Good:**
```markdown
1. Search existing code
2. Implement task
3. Run tests
```

Let Ralph figure out the details. Add specifics only when failures occur.

### Mistake 3: Assuming Sequential Reading

**Bad:**
```markdown
Read spec-1.md, then spec-2.md, then spec-3.md...
```

**Good:**
```markdown
Study specs/* (use up to 500 parallel Sonnet subagents)
```

Claude can read hundreds of files simultaneously. Let it.

### Mistake 4: No Clear Exit

**Bad:**
```markdown
Implement tasks from the plan until everything is done...
```

**Good:**
```markdown
6. Exit
   - End this loop iteration
   - One task per iteration
   - Loop will restart with fresh context
```

Ralph needs to know when to exit. Otherwise it may try to do multiple tasks or wait for input.

### Mistake 5: Vague Validation

**Bad:**
```markdown
Make sure everything works before committing...
```

**Good:**
```markdown
4. Validate
   - Run: npm test
   - Run: npm run type-check
   - If any fail, fix and retry
   - Do not commit until all pass
```

Concrete commands create reliable backpressure.
</common_prompt_mistakes>

<context_references>
## Context References

Use `@filename` to ensure files are loaded into context:

```markdown
0b. Study @IMPLEMENTATION_PLAN.md
```

This tells Claude Code to inline the file content, guaranteeing it's in context.

**When to use:**
- Critical files that must be loaded (plan, specs)
- Files Ralph needs for every iteration
- Relatively small files (<10K tokens)

**When not to use:**
- Large directories (use parallel subagents instead)
- Optional reference files
- Files that may not exist yet
</context_references>

---

## Reference: Ralph Fundamentals

# Ralph Fundamentals

Core concepts and philosophy of Geoffrey Huntley's Ralph Wiggum autonomous coding technique.

<what_is_ralph>
## What is Ralph?

Ralph is an autonomous AI coding methodology created by Geoffrey Huntley that went viral in late 2025. In its purest form, it's a Bash loop:

```bash
while :; do cat PROMPT.md | claude ; done
```

The loop continuously feeds a prompt file to Claude Code CLI. The agent completes one task, updates the implementation plan on disk, commits changes, then exits. The loop restarts immediately with fresh context.

**The core insight:** Ralph solves context accumulation by starting each iteration with fresh context. This is "deterministically bad in an undeterministic world"—embracing the chaos rather than fighting it.
</what_is_ralph>

<three_phases_two_prompts_one_loop>
## Three Phases, Two Prompts, One Loop

Ralph isn't just "a loop that codes." It's a funnel with specific structure:

### Phase 1: Planning Mode

**Objective:** Gap analysis only
**Input:** Specs and existing code
**Output:** `IMPLEMENTATION_PLAN.md` (prioritized TODO list)
**Rule:** No implementation, no commits

The planning prompt instructs Claude to:
1. Study all specification files
2. Study existing source code
3. Compare specs against implementation
4. Generate or update `IMPLEMENTATION_PLAN.md`
5. Exit

**Critical instruction:** "Don't assume not implemented; confirm with code search first."

### Phase 2: Building Mode

**Objective:** Implement from the plan
**Input:** Plan, specs, existing code
**Output:** Code changes + commits
**Rule:** One task per loop iteration

The building prompt instructs Claude to:
1. Study the implementation plan
2. Select most important task
3. Search existing code (don't assume anything is missing)
4. Implement the functionality
5. Run validation (tests, type checks, lints)
6. Update the plan with findings
7. Commit with descriptive message
8. Exit

### Phase 3: Observation (Your Role)

**Objective:** Sit on the loop, not in it
**Action:** Engineer the environment that allows Ralph to succeed

You:
- Watch for failure patterns
- Update `AGENTS.md` with learnings
- Tune prompts based on observed behavior
- Regenerate plan when trajectory fails
- Add backpressure mechanisms
- Improve specs when Ralph misunderstands

You DON'T:
- Jump into the loop to fix things
- Manually implement features
- Edit code directly
- Interfere with the autonomous process
</three_phases_two_prompts_one_loop>

<core_principles>
## Core Principles

### 1. Fresh Context Every Iteration

Each loop starts with a clean 200K context window. No accumulated conversation history, no stale assumptions. This prevents context poisoning and forces Ralph to ground decisions in files on disk.

### 2. File I/O as State

The `IMPLEMENTATION_PLAN.md` file is the only state that persists across iterations. This serves as deterministic shared state—no sophisticated orchestration needed. Claude reads it, updates it, commits it.

### 3. Backpressure as Steering

Tests, type checks, lints, and builds provide downstream steering. If Ralph's code doesn't pass validation, the loop continues until it does. This creates self-correcting behavior without manual intervention.

**Validation must be:**
- Automated (no human approval)
- Binary (pass/fail)
- Fast enough to run every iteration
- Relevant to code quality

### 4. Context Efficiency

200K advertised tokens ≈ 176K usable tokens. The "smart zone" (where Claude reasons best) is 40-60% of the window.

**Optimization:**
- Tight tasks + one task per loop = 100% smart zone utilization
- Use main agent as scheduler; spawn subagents for expensive work
- Prefer Markdown over JSON (more token-efficient)
- Keep prompts focused on current task

### 5. Parallel Subagents for Reads

The main agent orchestrates. Subagents do expensive work:
- Up to 250-500 Sonnet subagents for reading/searching code
- Only 1 subagent for builds/tests (to create backpressure)
- Subagents are cheap and fast for I/O-bound work

### 6. Prompts as Signs

Prompts aren't just instructions—they're discoverable patterns. Ralph learns from:
- Existing code patterns (how utilities are structured)
- AGENTS.md (project-specific learnings)
- Specs (requirements and constraints)
- Validation failures (what not to do)

### 7. Let Ralph Ralph

Trust the LLM's self-identification and self-correction ability:
- Don't micromanage
- Don't pre-optimize
- Observe and course-correct reactively
- "Tune it like a guitar" through iteration

Signs of over-steering:
- Prompts with too many rules
- Trying to predict all failure modes
- Not letting Ralph fail and learn
- Jumping in to fix instead of updating prompts
</core_principles>

<philosophy>
## Philosophy

### Deterministically Bad in an Undeterministic World

Traditional AI coding tries to maintain context across a long conversation. This fights against the probabilistic nature of LLMs and leads to:
- Context poisoning (earlier mistakes color later decisions)
- Assumption drift (LLM forgets what it "knew" earlier)
- Hallucination accumulation (errors compound)

Ralph embraces chaos:
- Fresh context = fresh start
- Plan on disk = deterministic state
- Validation = reality check
- Loop = inevitable progress

### The Loop is the Product

You're not building software. You're building an environment that builds software. The loop is the unit of work, not the feature.

Good loop design:
- Clear specs that Ralph can understand
- Effective backpressure that rejects bad work
- Minimal prompts that evolve through observation
- AGENTS.md that captures learnings

### Move Outside the Loop

Your role shifts from implementer to environment engineer:
- **Inside the loop:** Writing code, fixing bugs, implementing features (Ralph's job)
- **Outside the loop:** Writing specs, tuning prompts, adding tests, observing patterns (your job)

When Ralph fails repeatedly on the same thing, don't jump in and fix it. Update the environment:
1. Add guidance to AGENTS.md
2. Improve the spec
3. Add a test that would have caught it
4. Update the prompt pattern
</philosophy>

<when_to_regenerate_plan>
## When to Regenerate Plan

Discard `IMPLEMENTATION_PLAN.md` and restart planning when:
- Ralph implements wrong things or duplicates work
- Plan feels stale or mismatched to current state
- Too much completed-item clutter
- Significant spec changes made
- Confusion about actual completion status

**Cost-benefit:** One planning loop iteration is cheaper than Ralph circling on bad assumptions.

To regenerate:
```bash
rm IMPLEMENTATION_PLAN.md
./loop.sh plan
```
</when_to_regenerate_plan>

<escape_hatches>
## Escape Hatches

**Stop the loop:**
```bash
Ctrl+C  # Stops current iteration
```

**Revert uncommitted changes:**
```bash
git reset --hard
```

**Regenerate plan:**
```bash
rm IMPLEMENTATION_PLAN.md
./loop.sh plan
```

**Limit iterations:**
```bash
./loop.sh 20        # Build mode, max 20 tasks
./loop.sh plan 5    # Plan mode, max 5 iterations
```

**Review what Ralph did:**
```bash
git log --oneline
git show [commit-hash]
```
</escape_hatches>

---

## Reference: Validation Strategy

# Validation Strategy

Using tests, lints, and builds as backpressure to steer Ralph.

<what_is_backpressure>
## What is Backpressure?

Backpressure is automated validation that rejects invalid work. It creates a self-correcting feedback loop:

1. Ralph implements task
2. Validation runs (tests, type checks, lints)
3. If validation fails, Ralph investigates and fixes
4. Loop continues until validation passes
5. Only then can Ralph commit and move to next task

**Without backpressure:** Ralph generates code that may not work, accumulates errors, goes off track.

**With backpressure:** Ralph must produce working code to progress. Quality is enforced, not hoped for.
</what_is_backpressure>

<types_of_backpressure>
## Types of Backpressure

### 1. Tests (Most Important)

**Unit tests:** Verify individual functions/components
**Integration tests:** Verify components work together
**End-to-end tests:** Verify full user workflows

**Why tests are critical:**
- Binary pass/fail (no ambiguity)
- Fast feedback (run every iteration)
- Specific to requirements (aligned with specs)
- Self-documenting (show expected behavior)

**If no tests exist:**
Ralph should create them as part of implementation. Update building prompt:

```markdown
3. Implement
   - Write the functionality
   - Add tests for new functionality
   - Ensure tests pass
```

### 2. Type Checking

**TypeScript:** `tsc --noEmit` or `npm run type-check`
**Python:** `mypy .`
**Go:** Built into `go build`
**Rust:** Built into `cargo build`

**Benefits:**
- Catches type errors before runtime
- Enforces interface contracts
- Prevents common bugs

**Limitation:**
- Types can be correct but logic wrong
- Needs tests for behavior validation

### 3. Linting

**JavaScript/TypeScript:** ESLint, Biome
**Python:** Ruff, flake8, pylint
**Go:** golangci-lint
**Rust:** clippy

**Benefits:**
- Enforces code style
- Catches common mistakes
- Maintains consistency

**Limitation:**
- Style != correctness
- Can be overly strict
- May slow down loop if too many rules

**Recommendation:** Start with minimal linting, add rules as patterns emerge.

### 4. Builds

**Compiled languages:** Ensure code compiles
**Bundlers:** Ensure assets bundle correctly
**Docker:** Ensure containers build

**Benefits:**
- Catches syntax errors
- Verifies dependencies
- Confirms deployment readiness

**Limitation:**
- Build success != working software
- Slower than tests (use sparingly in loop)

### 5. Custom Validation

**Example: Visual regression tests**
- Screenshot comparison
- LLM-as-judge for subjective criteria

**Example: Performance benchmarks**
- Response time thresholds
- Memory usage limits

**Example: Security scans**
- Dependency vulnerability checks
- Static analysis for common issues

**When to use:**
- Project-specific quality criteria
- Subjective acceptance criteria
- Non-functional requirements
</types_of_backpressure>

<validation_levels>
## Validation Levels

Choose based on project maturity and speed needs:

### Level 1: Tests Only (Fastest)
```markdown
Run: npm test
```

**When to use:**
- Early development
- Fast iteration needed
- No type system or linting configured

**Pros:** Fast loop, minimal friction
**Cons:** May accumulate style inconsistencies

### Level 2: Tests + Type Checking (Recommended)
```markdown
Run:
- npm test
- npm run type-check
```

**When to use:**
- TypeScript/typed projects
- After initial implementation phase
- When interfaces are stabilizing

**Pros:** Good balance of speed and quality
**Cons:** Type errors can slow down loop

### Level 3: Full Validation (Slowest)
```markdown
Run:
- npm test
- npm run type-check
- npm run lint
- npm run build
```

**When to use:**
- Mature projects
- Pre-release quality gates
- When consistency is critical

**Pros:** Highest quality output
**Cons:** Slowest loop, most friction

### Level 4: Custom Validation
```markdown
Run:
- npm test
- npm run type-check
- npm run visual-test
- npm run security-scan
```

**When to use:**
- Specific quality requirements
- Regulated industries
- User-facing products

**Pros:** Tailored to actual needs
**Cons:** Complex to set up and maintain
</validation_levels>

<validation_in_prompts>
## Validation in Prompts

### Planning Mode

No validation needed. Planning mode doesn't change code.

### Building Mode

Include validation as a required step:

```markdown
4. Validate
   - Run: [specific commands]
   - Use only 1 Sonnet subagent for build/tests
   - If validation fails, investigate and fix
   - Do not commit until all validation passes
   - If repeatedly failing (3+ attempts), note blocker and move on
```

**Key points:**
- Specific commands (not vague "make sure it works")
- Single subagent for validation (creates backpressure bottleneck)
- Failure requires investigation and fix
- Escape hatch for stuck tasks (note blocker, move on)
</validation_in_prompts>

<handling_validation_failures>
## Handling Validation Failures

### Expected Behavior

Ralph should:
1. See validation failure
2. Read error messages
3. Investigate cause
4. Fix the issue
5. Re-run validation
6. Repeat until passing

### Failure Patterns

**Pattern 1: Test failure due to incorrect implementation**
- Ralph implemented wrong behavior
- Fix: Update implementation to match spec

**Pattern 2: Test failure due to incorrect test**
- Spec changed but test didn't
- Fix: Update test to match current spec

**Pattern 3: Type error due to API mismatch**
- Ralph used wrong types
- Fix: Correct types based on definitions

**Pattern 4: Lint error due to style**
- Code works but style is off
- Fix: Adjust formatting

**Pattern 5: Build failure due to missing dependency**
- Imported something not installed
- Fix: Add dependency or use different approach

### Stuck in Loop

If Ralph repeatedly fails validation (3+ iterations on same task):

**Option 1: Note blocker and skip**
```markdown
If repeatedly failing (3+ attempts), note blocker in plan and move to next task
```

**Option 2: Regenerate plan**
```bash
rm IMPLEMENTATION_PLAN.md
./loop.sh plan
```

**Option 3: Manual intervention**
```bash
# Stop loop
Ctrl+C

# Fix the issue manually
# Commit fix

# Restart loop
./loop.sh
```

**Option 4: Update AGENTS.md**
Add guidance about the failure pattern so Ralph doesn't repeat it.
</handling_validation_failures>

<backpressure_as_learning>
## Backpressure as Learning

Validation failures teach Ralph:
- What "working" means for this project
- Edge cases to handle
- Patterns to follow
- Mistakes to avoid

Over time, validation failures should decrease as Ralph learns project patterns.

**Early loops:**
- Many validation failures
- Ralph learning patterns
- Prompts and AGENTS.md evolving

**Later loops:**
- Fewer validation failures
- Ralph aligned with patterns
- Stable prompts and learnings

**If failures increase:**
- Specs may have changed
- New complexity introduced
- Prompts may need update
- Consider plan regeneration
</backpressure_as_learning>

<no_tests_strategy>
## No Tests? Start Here

If project has no tests:

### Option 1: Ralph Creates Tests

Update building prompt:
```markdown
3. Implement
   - Write the functionality
   - Add unit tests for new functionality
   - Ensure tests pass before proceeding
```

Ralph will create tests as it implements features.

### Option 2: Add Minimal Test Framework

Before starting loop:
```bash
# JavaScript/TypeScript
npm install --save-dev vitest
# or jest, or your preferred framework

# Python
pip install pytest

# Go
# Built-in, just use: go test ./...

# Rust
# Built-in, just use: cargo test
```

Create one example test to establish pattern.

### Option 3: Use Type Checking Only

If tests are too much overhead initially:
```markdown
4. Validate
   - Run: tsc --noEmit  # or equivalent
   - Type errors must be fixed
```

Better than nothing. Add tests later when patterns stabilize.

### Option 4: Manual Smoke Tests

Define manual checks in AGENTS.md:
```markdown
## Validation

After each change:
- Run the application
- Test the changed feature manually
- Verify no errors in console
```

Not ideal (not automated) but establishes quality baseline.
</no_tests_strategy>

<tuning_backpressure>
## Tuning Backpressure

Start strict, loosen if too slow:

**Week 1:** Full validation (tests + types + lint + build)
- See where Ralph struggles
- Identify slow validation steps
- Note which checks catch real issues

**Week 2:** Remove low-value checks
- If linting catches nothing, remove it
- If build is slow and redundant with tests, remove it
- Keep only checks that catch real problems

**Week 3:** Add custom checks
- Based on observed failure patterns
- Aligned with actual quality needs
- Fast enough to not slow loop significantly

**Ongoing:** Evolve with project
- Add checks when new failure patterns emerge
- Remove checks when no longer catching issues
- Balance speed vs quality based on project phase
</tuning_backpressure>
