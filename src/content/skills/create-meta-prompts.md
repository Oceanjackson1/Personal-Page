---
title: "Create Meta Prompts"
description: "Create optimized prompts for Claude-to-Claude pipelines with research, planning, and execution stages. Use when building prompts that produce outputs for other prompts to consume, or when running multi-stage workflows (research -> plan -> implement)."
category: "devops"
source: "community"
author: "Community"
tags: ["create", "meta", "prompts"]
date: 2026-03-20
---

<objective>
Create prompts optimized for Claude-to-Claude communication in multi-stage workflows. Outputs are structured with XML and metadata for efficient parsing by subsequent prompts.

Every execution produces a `SUMMARY.md` for quick human scanning without reading full outputs.

Each prompt gets its own folder in `.prompts/` with its output artifacts, enabling clear provenance and chain detection.
</objective>

<quick_start>
<workflow>
1. **Intake**: Determine purpose (Do/Plan/Research/Refine), gather requirements
2. **Chain detection**: Check for existing research/plan files to reference
3. **Generate**: Create prompt using purpose-specific patterns
4. **Save**: Create folder in `.prompts/{number}-{topic}-{purpose}/`
5. **Present**: Show decision tree for running
6. **Execute**: Run prompt(s) with dependency-aware execution engine
7. **Summarize**: Create SUMMARY.md for human scanning
</workflow>

<folder_structure>
```
.prompts/
├── 001-auth-research/
│   ├── completed/
│   │   └── 001-auth-research.md    # Prompt (archived after run)
│   ├── auth-research.md            # Full output (XML for Claude)
│   └── SUMMARY.md                  # Executive summary (markdown for human)
├── 002-auth-plan/
│   ├── completed/
│   │   └── 002-auth-plan.md
│   ├── auth-plan.md
│   └── SUMMARY.md
├── 003-auth-implement/
│   ├── completed/
│   │   └── 003-auth-implement.md
│   └── SUMMARY.md                  # Do prompts create code elsewhere
├── 004-auth-research-refine/
│   ├── completed/
│   │   └── 004-auth-research-refine.md
│   ├── archive/
│   │   └── auth-research-v1.md     # Previous version
│   └── SUMMARY.md
```
</folder_structure>
</quick_start>

<context>
Prompts directory: !`[ -d ./.prompts ] && echo "exists" || echo "missing"`
Existing research/plans: !`find ./.prompts -name "*-research.md" -o -name "*-plan.md" 2>/dev/null | head -10`
Next prompt number: !`ls -d ./.prompts/*/ 2>/dev/null | wc -l | xargs -I {} expr {} + 1`
</context>

<automated_workflow>

<step_0_intake_gate>
<title>Adaptive Requirements Gathering</title>

<critical_first_action>
**BEFORE analyzing anything**, check if context was provided.

IF no context provided (skill invoked without description):
→ **IMMEDIATELY use AskUserQuestion** with:

- header: "Purpose"
- question: "What is the purpose of this prompt?"
- options:
  - "Do" - Execute a task, produce an artifact
  - "Plan" - Create an approach, roadmap, or strategy
  - "Research" - Gather information or understand something
  - "Refine" - Improve an existing research or plan output

After selection, ask: "Describe what you want to accomplish" (they select "Other" to provide free text).

IF context was provided:
→ Check if purpose is inferable from keywords:
  - `implement`, `build`, `create`, `fix`, `add`, `refactor` → Do
  - `plan`, `roadmap`, `approach`, `strategy`, `decide`, `phases` → Plan
  - `research`, `understand`, `learn`, `gather`, `analyze`, `explore` → Research
  - `refine`, `improve`, `deepen`, `expand`, `iterate`, `update` → Refine

→ If unclear, ask the Purpose question above as first contextual question
→ If clear, proceed to adaptive_analysis with inferred purpose
</critical_first_action>

<adaptive_analysis>
Extract and infer:

- **Purpose**: Do, Plan, Research, or Refine
- **Topic identifier**: Kebab-case identifier for file naming (e.g., `auth`, `stripe-payments`)
- **Complexity**: Simple vs complex (affects prompt depth)
- **Prompt structure**: Single vs multiple prompts
- **Target** (Refine only): Which existing output to improve

If topic identifier not obvious, ask:
- header: "Topic"
- question: "What topic/feature is this for? (used for file naming)"
- Let user provide via "Other" option
- Enforce kebab-case (convert spaces/underscores to hyphens)

For Refine purpose, also identify target output from `.prompts/*/` to improve.
</adaptive_analysis>

<chain_detection>
Scan `.prompts/*/` for existing `*-research.md` and `*-plan.md` files.

If found:
1. List them: "Found existing files: auth-research.md (in 001-auth-research/), stripe-plan.md (in 005-stripe-plan/)"
2. Use AskUserQuestion:
   - header: "Reference"
   - question: "Should this prompt reference any existing research or plans?"
   - options: List found files + "None"
   - multiSelect: true

Match by topic keyword when possible (e.g., "auth plan" → suggest auth-research.md).
</chain_detection>

<contextual_questioning>
Generate 2-4 questions using AskUserQuestion based on purpose and gaps.

Load questions from: [references/question-bank.md](references/question-bank.md)

Route by purpose:
- Do → artifact type, scope, approach
- Plan → plan purpose, format, constraints
- Research → depth, sources, output format
- Refine → target selection, feedback, preservation
</contextual_questioning>

<decision_gate>
After receiving answers, present decision gate using AskUserQuestion:

- header: "Ready"
- question: "Ready to create the prompt?"
- options:
  - "Proceed" - Create the prompt with current context
  - "Ask more questions" - I have more details to clarify
  - "Let me add context" - I want to provide additional information

Loop until "Proceed" selected.
</decision_gate>

<finalization>
After "Proceed" selected, state confirmation:

"Creating a {purpose} prompt for: {topic}
Folder: .prompts/{number}-{topic}-{purpose}/
References: {list any chained files}"

Then proceed to generation.
</finalization>
</step_0_intake_gate>

<step_1_generate>
<title>Generate Prompt</title>

Load purpose-specific patterns:
- Do: [references/do-patterns.md](references/do-patterns.md)
- Plan: [references/plan-patterns.md](references/plan-patterns.md)
- Research: [references/research-patterns.md](references/research-patterns.md)
- Refine: [references/refine-patterns.md](references/refine-patterns.md)

Load intelligence rules: [references/intelligence-rules.md](references/intelligence-rules.md)

<prompt_structure>
All generated prompts include:

1. **Objective**: What to accomplish, why it matters
2. **Context**: Referenced files (@), dynamic context (!)
3. **Requirements**: Specific instructions for the task
4. **Output specification**: Where to save, what structure
5. **Metadata requirements**: For research/plan outputs, specify XML metadata structure
6. **SUMMARY.md requirement**: All prompts must create a SUMMARY.md file
7. **Success criteria**: How to know it worked

For Research and Plan prompts, output must include:
- `<confidence>` - How confident in findings
- `<dependencies>` - What's needed to proceed
- `<open_questions>` - What remains uncertain
- `<assumptions>` - What was assumed

All prompts must create `SUMMARY.md` with:
- **One-liner** - Substantive description of outcome
- **Version** - v1 or iteration info
- **Key Findings** - Actionable takeaways
- **Files Created** - (Do prompts only)
- **Decisions Needed** - What requires user input
- **Blockers** - External impediments
- **Next Step** - Concrete forward action
</prompt_structure>

<file_creation>
1. Create folder: `.prompts/{number}-{topic}-{purpose}/`
2. Create `completed/` subfolder
3. Write prompt to: `.prompts/{number}-{topic}-{purpose}/{number}-{topic}-{purpose}.md`
4. Prompt instructs output to: `.prompts/{number}-{topic}-{purpose}/{topic}-{purpose}.md`
</file_creation>
</step_1_generate>

<step_2_present>
<title>Present Decision Tree</title>

After saving prompt(s), present inline (not AskUserQuestion):

<single_prompt_presentation>
```
Prompt created: .prompts/{number}-{topic}-{purpose}/{number}-{topic}-{purpose}.md

What's next?

1. Run prompt now
2. Review/edit prompt first
3. Save for later
4. Other

Choose (1-4): _
```
</single_prompt_presentation>

<multi_prompt_presentation>
```
Prompts created:
- .prompts/001-auth-research/001-auth-research.md
- .prompts/002-auth-plan/002-auth-plan.md
- .prompts/003-auth-implement/003-auth-implement.md

Detected execution order: Sequential (002 references 001 output, 003 references 002 output)

What's next?

1. Run all prompts (sequential)
2. Review/edit prompts first
3. Save for later
4. Other

Choose (1-4): _
```
</multi_prompt_presentation>
</step_2_present>

<step_3_execute>
<title>Execution Engine</title>

<execution_modes>
<single_prompt>
Straightforward execution of one prompt.

1. Read prompt file contents
2. Spawn Task agent with subagent_type="general-purpose"
3. Include in task prompt:
   - The complete prompt contents
   - Output location: `.prompts/{number}-{topic}-{purpose}/{topic}-{purpose}.md`
4. Wait for completion
5. Validate output (see validation section)
6. Archive prompt to `completed/` subfolder
7. Report results with next-step options
</single_prompt>

<sequential_execution>
For chained prompts where each depends on previous output.

1. Build execution queue from dependency order
2. For each prompt in queue:
   a. Read prompt file
   b. Spawn Task agent
   c. Wait for completion
   d. Validate output
   e. If validation fails → stop, report failure, offer recovery options
   f. If success → archive prompt, continue to next
3. Report consolidated results

<progress_reporting>
Show progress during execution:
```
Executing 1/3: 001-auth-research... ✓
Executing 2/3: 002-auth-plan... ✓
Executing 3/3: 003-auth-implement... (running)
```
</progress_reporting>
</sequential_execution>

<parallel_execution>
For independent prompts with no dependencies.

1. Read all prompt files
2. **CRITICAL**: Spawn ALL Task agents in a SINGLE message
   - This is required for true parallel execution
   - Each task includes its output location
3. Wait for all to complete
4. Validate all outputs
5. Archive all prompts
6. Report consolidated results (successes and failures)

<failure_handling>
Unlike sequential, parallel continues even if some fail:
- Collect all results
- Archive successful prompts
- Report failures with details
- Offer to retry failed prompts
</failure_handling>
</parallel_execution>

<mixed_dependencies>
For complex DAGs (e.g., two parallel research → one plan).

1. Analyze dependency graph from @ references
2. Group into execution layers:
   - Layer 1: No dependencies (run parallel)
   - Layer 2: Depends only on layer 1 (run after layer 1 completes)
   - Layer 3: Depends on layer 2, etc.
3. Execute each layer:
   - Parallel within layer
   - Sequential between layers
4. Stop if any dependency fails (downstream prompts can't run)

<example>
```
Layer 1 (parallel): 001-api-research, 002-db-research
Layer 2 (after layer 1): 003-architecture-plan
Layer 3 (after layer 2): 004-implement
```
</example>
</mixed_dependencies>
</execution_modes>

<dependency_detection>
<automatic_detection>
Scan prompt contents for @ references to determine dependencies:

1. Parse each prompt for `@.prompts/{number}-{topic}/` patterns
2. Build dependency graph
3. Detect cycles (error if found)
4. Determine execution order

<inference_rules>
If no explicit @ references found, infer from purpose:
- Research prompts: No dependencies (can parallel)
- Plan prompts: Depend on same-topic research
- Do prompts: Depend on same-topic plan

Override with explicit references when present.
</inference_rules>
</automatic_detection>

<missing_dependencies>
If a prompt references output that doesn't exist:

1. Check if it's another prompt in this session (will be created)
2. Check if it exists in `.prompts/*/` (already completed)
3. If truly missing:
   - Warn user: "002-auth-plan references auth-research.md which doesn't exist"
   - Offer: Create the missing research prompt first? / Continue anyway? / Cancel?
</missing_dependencies>
</dependency_detection>

<validation>
<output_validation>
After each prompt completes, verify success:

1. **File exists**: Check output file was created
2. **Not empty**: File has content (> 100 chars)
3. **Metadata present** (for research/plan): Check for required XML tags
   - `<confidence>`
   - `<dependencies>`
   - `<open_questions>`
   - `<assumptions>`
4. **SUMMARY.md exists**: Check SUMMARY.md was created
5. **SUMMARY.md complete**: Has required sections (Key Findings, Decisions Needed, Blockers, Next Step)
6. **One-liner is substantive**: Not generic like "Research completed"

<validation_failure>
If validation fails:
- Report what's missing
- Offer options:
  - Retry the prompt
  - Continue anyway (for non-critical issues)
  - Stop and investigate
</validation_failure>
</output_validation>
</validation>

<failure_handling>
<sequential_failure>
Stop the chain immediately:
```
✗ Failed at 2/3: 002-auth-plan

Completed:
- 001-auth-research ✓ (archived)

Failed:
- 002-auth-plan: Output file not created

Not started:
- 003-auth-implement

What's next?
1. Retry 002-auth-plan
2. View error details
3. Stop here (keep completed work)
4. Other
```
</sequential_failure>

<parallel_failure>
Continue others, report all results:
```
Parallel execution completed with errors:

✓ 001-api-research (archived)
✗ 002-db-research: Validation failed - missing <confidence> tag
✓ 003-ui-research (archived)

What's next?
1. Retry failed prompt (002)
2. View error details
3. Continue without 002
4. Other
```
</parallel_failure>
</failure_handling>

<archiving>
<archive_timing>
- **Sequential**: Archive each prompt immediately after successful completion
  - Provides clear state if execution stops mid-chain
- **Parallel**: Archive all at end after collecting results
  - Keeps prompts available for potential retry

<archive_operation>
Move prompt file to completed subfolder:
```bash
mv .prompts/{number}-{topic}-{purpose}/{number}-{topic}-{purpose}.md \
   .prompts/{number}-{topic}-{purpose}/completed/
```

Output file stays in place (not moved).
</archive_operation>
</archiving>

<result_presentation>
<single_result>
```
✓ Executed: 001-auth-research
✓ Created: .prompts/001-auth-research/SUMMARY.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auth Research Summary

**JWT with jose library and httpOnly cookies recommended**

## Key Findings
• jose outperforms jsonwebtoken with better TypeScript support
• httpOnly cookies required (localStorage is XSS vulnerable)
• Refresh rotation is OWASP standard

## Decisions Needed
None - ready for planning

## Blockers
None

## Next Step
Create auth-plan.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What's next?
1. Create planning prompt (auth-plan)
2. View full research output
3. Done
4. Other
```

Display the actual SUMMARY.md content inline so user sees findings without opening files.
</single_result>

<chain_result>
```
✓ Chain completed: auth workflow

Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
001-auth-research
**JWT with jose library and httpOnly cookies recommended**
Decisions: None • Blockers: None

002-auth-plan
**4-phase implementation: types → JWT core → refresh → tests**
Decisions: Approve 15-min token expiry • Blockers: None

003-auth-implement
**JWT middleware complete with 6 files created**
Decisions: Review before Phase 2 • Blockers: None
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All prompts archived. Full summaries in .prompts/*/SUMMARY.md

What's next?
1. Review implementation
2. Run tests
3. Create new prompt chain
4. Other
```

For chains, show condensed one-liner from each SUMMARY.md with decisions/blockers flagged.
</chain_result>
</result_presentation>

<special_cases>
<re_running_completed>
If user wants to re-run an already-completed prompt:

1. Check if prompt is in `completed/` subfolder
2. Move it back to parent folder
3. Optionally backup existing output: `{output}.bak`
4. Execute normally
</re_running_completed>

<output_conflicts>
If output file already exists:

1. For re-runs: Backup existing → `{filename}.bak`
2. For new runs: Should not happen (unique numbering)
3. If conflict detected: Ask user - Overwrite? / Rename? / Cancel?
</output_conflicts>

<commit_handling>
After successful execution:

1. Do NOT auto-commit (user controls git workflow)
2. Mention what files were created/modified
3. User can commit when ready

Exception: If user explicitly requests commit, stage and commit:
- Output files created
- Prompts archived
- Any implementation changes (for Do prompts)
</commit_handling>

<recursive_prompts>
If a prompt's output includes instructions to create more prompts:

1. This is advanced usage - don't auto-detect
2. Present the output to user
3. User can invoke skill again to create follow-up prompts
4. Maintains user control over prompt creation
</recursive_prompts>
</special_cases>
</step_3_execute>

</automated_workflow>

<reference_guides>
**Prompt patterns by purpose:**
- [references/do-patterns.md](references/do-patterns.md) - Execution prompts + output structure
- [references/plan-patterns.md](references/plan-patterns.md) - Planning prompts + plan.md structure
- [references/research-patterns.md](references/research-patterns.md) - Research prompts + research.md structure
- [references/refine-patterns.md](references/refine-patterns.md) - Iteration prompts + versioning

**Shared templates:**
- [references/summary-template.md](references/summary-template.md) - SUMMARY.md structure and field requirements
- [references/metadata-guidelines.md](references/metadata-guidelines.md) - Confidence, dependencies, open questions, assumptions

**Supporting references:**
- [references/question-bank.md](references/question-bank.md) - Intake questions by purpose
- [references/intelligence-rules.md](references/intelligence-rules.md) - Extended thinking, parallel tools, depth decisions
</reference_guides>

<success_criteria>
**Prompt Creation:**
- Intake gate completed with purpose and topic identified
- Chain detection performed, relevant files referenced
- Prompt generated with correct structure for purpose
- Folder created in `.prompts/` with correct naming
- Output file location specified in prompt
- SUMMARY.md requirement included in prompt
- Metadata requirements included for Research/Plan outputs
- Quality controls included for Research outputs (verification checklist, QA, pre-submission)
- Streaming write instructions included for Research outputs
- Decision tree presented

**Execution (if user chooses to run):**
- Dependencies correctly detected and ordered
- Prompts executed in correct order (sequential/parallel/mixed)
- Output validated after each completion
- SUMMARY.md created with all required sections
- One-liner is substantive (not generic)
- Failed prompts handled gracefully with recovery options
- Successful prompts archived to `completed/` subfolder
- SUMMARY.md displayed inline in results
- Results presented with decisions/blockers flagged

**Research Quality (for Research prompts):**
- Verification checklist completed
- Quality report distinguishes verified from assumed claims
- Sources consulted listed with URLs
- Confidence levels assigned to findings
- Critical claims verified with official documentation
</success_criteria>

---

## Reference: Do Patterns

<overview>
Prompt patterns for execution tasks that produce artifacts (code, documents, designs, etc.).
</overview>

<prompt_template>
```xml
<objective>
{Clear statement of what to build/create/fix}

Purpose: {Why this matters, what it enables}
Output: {What artifact(s) will be produced}
</objective>

<context>
{Referenced research/plan files if chained}
@{topic}-research.md
@{topic}-plan.md

{Project context}
@relevant-files
</context>

<requirements>
{Specific functional requirements}
{Quality requirements}
{Constraints and boundaries}
</requirements>

<implementation>
{Specific approaches or patterns to follow}
{What to avoid and WHY}
{Integration points}
</implementation>

<output>
Create/modify files:
- `./path/to/file.ext` - {description}

{For complex outputs, specify structure}
</output>

<verification>
Before declaring complete:
- {Specific test or check}
- {How to confirm it works}
- {Edge cases to verify}
</verification>

<summary_requirements>
Create `.prompts/{num}-{topic}-{purpose}/SUMMARY.md`

Load template: [summary-template.md](summary-template.md)

For Do prompts, include Files Created section with paths and descriptions. Emphasize what was implemented and test status. Next step typically: Run tests or execute next phase.
</summary_requirements>

<success_criteria>
{Clear, measurable criteria}
- {Criterion 1}
- {Criterion 2}
- SUMMARY.md created with files list and next step
</success_criteria>
```
</prompt_template>

<key_principles>

<reference_chain_artifacts>
If research or plan exists, always reference them:
```xml
<context>
Research findings: @.prompts/001-auth-research/auth-research.md
Implementation plan: @.prompts/002-auth-plan/auth-plan.md
</context>
```
</reference_chain_artifacts>

<explicit_output_location>
Every artifact needs a clear path:
```xml
<output>
Create files in ./src/auth/:
- `./src/auth/middleware.ts` - JWT validation middleware
- `./src/auth/types.ts` - Auth type definitions
- `./src/auth/utils.ts` - Helper functions
</output>
```
</explicit_output_location>

<verification_matching>
Include verification that matches the task:
- Code: run tests, type check, lint
- Documents: check structure, validate links
- Designs: review against requirements
</verification_matching>

</key_principles>

<complexity_variations>

<simple_do>
Single artifact example:
```xml
<objective>
Create a utility function that validates email addresses.
</objective>

<requirements>
- Support standard email format
- Return boolean
- Handle edge cases (empty, null)
</requirements>

<output>
Create: `./src/utils/validate-email.ts`
</output>

<verification>
Test with: valid emails, invalid formats, edge cases
</verification>
```
</simple_do>

<complex_do>
Multiple artifacts with dependencies:
```xml
<objective>
Implement user authentication system with JWT tokens.

Purpose: Enable secure user sessions for the application
Output: Auth middleware, routes, types, and tests
</objective>

<context>
Research: @.prompts/001-auth-research/auth-research.md
Plan: @.prompts/002-auth-plan/auth-plan.md
Existing user model: @src/models/user.ts
</context>

<requirements>
- JWT access tokens (15min expiry)
- Refresh token rotation
- Secure httpOnly cookies
- Rate limiting on auth endpoints
</requirements>

<implementation>
Follow patterns from auth-research.md:
- Use jose library for JWT (not jsonwebtoken - see research)
- Implement refresh rotation per OWASP guidelines
- Store refresh tokens hashed in database

Avoid:
- Storing tokens in localStorage (XSS vulnerable)
- Long-lived access tokens (security risk)
</implementation>

<output>
Create in ./src/auth/:
- `middleware.ts` - JWT validation, refresh logic
- `routes.ts` - Login, logout, refresh endpoints
- `types.ts` - Token payloads, auth types
- `utils.ts` - Token generation, hashing

Create in ./src/auth/__tests__/:
- `auth.test.ts` - Unit tests for all auth functions
</output>

<verification>
1. Run test suite: `npm test src/auth`
2. Type check: `npx tsc --noEmit`
3. Manual test: login flow, token refresh, logout
4. Security check: verify httpOnly cookies, token expiry
</verification>

<success_criteria>
- All tests passing
- No type errors
- Login/logout/refresh flow works
- Tokens properly secured
- Follows patterns from research
</success_criteria>
```
</complex_do>

</complexity_variations>

<non_code_examples>

<document_creation>
```xml
<objective>
Create API documentation for the authentication endpoints.

Purpose: Enable frontend team to integrate auth
Output: OpenAPI spec + markdown guide
</objective>

<context>
Implementation: @src/auth/routes.ts
Types: @src/auth/types.ts
</context>

<requirements>
- OpenAPI 3.0 spec
- Request/response examples
- Error codes and handling
- Authentication flow diagram
</requirements>

<output>
- `./docs/api/auth.yaml` - OpenAPI spec
- `./docs/guides/authentication.md` - Integration guide
</output>

<verification>
- Validate OpenAPI spec: `npx @redocly/cli lint docs/api/auth.yaml`
- Check all endpoints documented
- Verify examples match actual implementation
</verification>
```
</document_creation>

<design_architecture>
```xml
<objective>
Design database schema for multi-tenant SaaS application.

Purpose: Support customer isolation and scaling
Output: Schema diagram + migration files
</objective>

<context>
Research: @.prompts/001-multitenancy-research/multitenancy-research.md
Current schema: @prisma/schema.prisma
</context>

<requirements>
- Row-level security per tenant
- Shared infrastructure model
- Support for tenant-specific customization
- Audit logging
</requirements>

<output>
- `./docs/architecture/tenant-schema.md` - Schema design doc
- `./prisma/migrations/add-tenancy/` - Migration files
</output>

<verification>
- Migration runs without errors
- RLS policies correctly isolate data
- Performance acceptable with 1000 tenants
</verification>
```
</design_architecture>

</non_code_examples>

---

## Reference: Intelligence Rules

<overview>
Guidelines for determining prompt complexity, tool usage, and optimization patterns.
</overview>

<complexity_assessment>

<simple_prompts>
Single focused task, clear outcome:

**Indicators:**
- Single artifact output
- No dependencies on other files
- Straightforward requirements
- No decision-making needed

**Prompt characteristics:**
- Concise objective
- Minimal context
- Direct requirements
- Simple verification
</simple_prompts>

<complex_prompts>
Multi-step tasks, multiple considerations:

**Indicators:**
- Multiple artifacts or phases
- Dependencies on research/plan files
- Trade-offs to consider
- Integration with existing code

**Prompt characteristics:**
- Detailed objective with context
- Referenced files
- Explicit implementation guidance
- Comprehensive verification
- Extended thinking triggers
</complex_prompts>

</complexity_assessment>

<extended_thinking_triggers>

<when_to_include>
Use these phrases to activate deeper reasoning in complex prompts:
- Complex architectural decisions
- Multiple valid approaches to evaluate
- Security-sensitive implementations
- Performance optimization tasks
- Trade-off analysis
</when_to_include>

<trigger_phrases>
```
"Thoroughly analyze..."
"Consider multiple approaches..."
"Deeply consider the implications..."
"Explore various solutions before..."
"Carefully evaluate trade-offs..."
```
</trigger_phrases>

<example_usage>
```xml
<requirements>
Thoroughly analyze the authentication options and consider multiple
approaches before selecting an implementation. Deeply consider the
security implications of each choice.
</requirements>
```
</example_usage>

<when_not_to_use>
- Simple, straightforward tasks
- Tasks with clear single approach
- Following established patterns
- Basic CRUD operations
</when_not_to_use>

</extended_thinking_triggers>

<parallel_tool_calling>

<when_to_include>
```xml
<efficiency>
For maximum efficiency, invoke all independent tool operations
simultaneously rather than sequentially. Multiple file reads,
searches, and API calls that don't depend on each other should
run in parallel.
</efficiency>
```
</when_to_include>

<applicable_scenarios>
- Reading multiple files for context
- Running multiple searches
- Fetching from multiple sources
- Creating multiple independent files
</applicable_scenarios>

</parallel_tool_calling>

<context_loading>

<when_to_load>
- Modifying existing code
- Following established patterns
- Integrating with current systems
- Building on research/plan outputs
</when_to_load>

<when_not_to_load>
- Greenfield features
- Standalone utilities
- Pure research tasks
- Standard patterns without customization
</when_not_to_load>

<loading_patterns>
```xml
<context>
<!-- Chained artifacts -->
Research: @.prompts/001-auth-research/auth-research.md
Plan: @.prompts/002-auth-plan/auth-plan.md

<!-- Existing code to modify -->
Current implementation: @src/auth/middleware.ts
Types to extend: @src/types/auth.ts

<!-- Patterns to follow -->
Similar feature: @src/features/payments/
</context>
```
</loading_patterns>

</context_loading>

<output_optimization>

<streaming_writes>
For research and plan outputs that may be large:

**Instruct incremental writing:**
```xml
<process>
1. Create output file with XML skeleton
2. Write each section as completed:
   - Finding 1 discovered → Append immediately
   - Finding 2 discovered → Append immediately
   - Code example found → Append immediately
3. Finalize summary and metadata after all sections complete
</process>
```

**Why this matters:**
- Prevents lost work from token limit failures
- No need to estimate output size
- Agent creates natural checkpoints
- Works for any task complexity

**When to use:**
- Research prompts (findings accumulate)
- Plan prompts (phases accumulate)
- Any prompt that might produce >15k tokens

**When NOT to use:**
- Do prompts (code generation is different workflow)
- Simple tasks with known small outputs
</streaming_writes>

<claude_to_claude>
For Claude-to-Claude consumption:

**Use heavy XML structure:**
```xml
<findings>
  <finding category="security">
    <title>Token Storage</title>
    <recommendation>httpOnly cookies</recommendation>
    <rationale>Prevents XSS access</rationale>
  </finding>
</findings>
```

**Include metadata:**
```xml
<metadata>
  <confidence level="high">Verified in official docs</confidence>
  <dependencies>Cookie parser middleware</dependencies>
  <open_questions>SameSite policy for subdomains</open_questions>
</metadata>
```

**Be explicit about next steps:**
```xml
<next_actions>
  <action priority="high">Create planning prompt using these findings</action>
  <action priority="medium">Validate rate limits in sandbox</action>
</next_actions>
```
</claude_to_claude>

<human_consumption>
For human consumption:
- Clear headings
- Bullet points for scanning
- Code examples with comments
- Summary at top
</human_consumption>

</output_optimization>

<prompt_depth_guidelines>

<minimal>
Simple Do prompts:
- 20-40 lines
- Basic objective, requirements, output, verification
- No extended thinking
- No parallel tool hints
</minimal>

<standard>
Typical task prompts:
- 40-80 lines
- Full objective with context
- Clear requirements and implementation notes
- Standard verification
</standard>

<comprehensive>
Complex task prompts:
- 80-150 lines
- Extended thinking triggers
- Parallel tool calling hints
- Multiple verification steps
- Detailed success criteria
</comprehensive>

</prompt_depth_guidelines>

<why_explanations>

Always explain why constraints matter:

<bad_example>
```xml
<requirements>
Never store tokens in localStorage.
</requirements>
```
</bad_example>

<good_example>
```xml
<requirements>
Never store tokens in localStorage - it's accessible to any
JavaScript on the page, making it vulnerable to XSS attacks.
Use httpOnly cookies instead.
</requirements>
```
</good_example>

This helps the executing Claude make good decisions when facing edge cases.

</why_explanations>

<verification_patterns>

<for_code>
```xml
<verification>
1. Run test suite: `npm test`
2. Type check: `npx tsc --noEmit`
3. Lint: `npm run lint`
4. Manual test: [specific flow to test]
</verification>
```
</for_code>

<for_documents>
```xml
<verification>
1. Validate structure: [check required sections]
2. Verify links: [check internal references]
3. Review completeness: [check against requirements]
</verification>
```
</for_documents>

<for_research>
```xml
<verification>
1. Sources are current (2024-2025)
2. All scope questions answered
3. Metadata captures uncertainties
4. Actionable recommendations included
</verification>
```
</for_research>

<for_plans>
```xml
<verification>
1. Phases are sequential and logical
2. Tasks are specific and actionable
3. Dependencies are clear
4. Metadata captures assumptions
</verification>
```
</for_plans>

</verification_patterns>

<chain_optimization>

<research_prompts>
Research prompts should:
- Structure findings for easy extraction
- Include code examples for implementation
- Clearly mark confidence levels
- List explicit next actions
</research_prompts>

<plan_prompts>
Plan prompts should:
- Reference research explicitly
- Break phases into prompt-sized chunks
- Include execution hints per phase
- Capture dependencies between phases
</plan_prompts>

<do_prompts>
Do prompts should:
- Reference both research and plan
- Follow plan phases explicitly
- Verify against research recommendations
- Update plan status when done
</do_prompts>

</chain_optimization>

---

## Reference: Metadata Guidelines

<overview>
Standard metadata structure for research and plan outputs. Include in all research, plan, and refine prompts.
</overview>

<metadata_structure>
```xml
<metadata>
  <confidence level="{high|medium|low}">
    {Why this confidence level}
  </confidence>
  <dependencies>
    {What's needed to proceed}
  </dependencies>
  <open_questions>
    {What remains uncertain}
  </open_questions>
  <assumptions>
    {What was assumed}
  </assumptions>
</metadata>
```
</metadata_structure>

<confidence_levels>
- **high**: Official docs, verified patterns, clear consensus, few unknowns
- **medium**: Mixed sources, some outdated info, minor gaps, reasonable approach
- **low**: Sparse documentation, conflicting info, significant unknowns, best guess
</confidence_levels>

<dependencies_format>
External requirements that must be met:
```xml
<dependencies>
  - API keys for third-party service
  - Database migration completed
  - Team trained on new patterns
</dependencies>
```
</dependencies_format>

<open_questions_format>
What couldn't be determined or needs validation:
```xml
<open_questions>
  - Actual rate limits under production load
  - Performance with >100k records
  - Specific error codes for edge cases
</open_questions>
```
</open_questions_format>

<assumptions_format>
Context assumed that might need validation:
```xml
<assumptions>
  - Using REST API (not GraphQL)
  - Single region deployment
  - Node.js/TypeScript stack
</assumptions>
```
</assumptions_format>

---

## Reference: Plan Patterns

<overview>
Prompt patterns for creating approaches, roadmaps, and strategies that will be consumed by subsequent prompts.
</overview>

<prompt_template>
```xml
<objective>
Create a {plan type} for {topic}.

Purpose: {What decision/implementation this enables}
Input: {Research or context being used}
Output: {topic}-plan.md with actionable phases/steps
</objective>

<context>
Research findings: @.prompts/{num}-{topic}-research/{topic}-research.md
{Additional context files}
</context>

<planning_requirements>
{What the plan needs to address}
{Constraints to work within}
{Success criteria for the planned outcome}
</planning_requirements>

<output_structure>
Save to: `.prompts/{num}-{topic}-plan/{topic}-plan.md`

Structure the plan using this XML format:

```xml
<plan>
  <summary>
    {One paragraph overview of the approach}
  </summary>

  <phases>
    <phase number="1" name="{phase-name}">
      <objective>{What this phase accomplishes}</objective>
      <tasks>
        <task priority="high">{Specific actionable task}</task>
        <task priority="medium">{Another task}</task>
      </tasks>
      <deliverables>
        <deliverable>{What's produced}</deliverable>
      </deliverables>
      <dependencies>{What must exist before this phase}</dependencies>
    </phase>
    <!-- Additional phases -->
  </phases>

  <metadata>
    <confidence level="{high|medium|low}">
      {Why this confidence level}
    </confidence>
    <dependencies>
      {External dependencies needed}
    </dependencies>
    <open_questions>
      {Uncertainties that may affect execution}
    </open_questions>
    <assumptions>
      {What was assumed in creating this plan}
    </assumptions>
  </metadata>
</plan>
```
</output_structure>

<summary_requirements>
Create `.prompts/{num}-{topic}-plan/SUMMARY.md`

Load template: [summary-template.md](summary-template.md)

For plans, emphasize phase breakdown with objectives and assumptions needing validation. Next step typically: Execute first phase.
</summary_requirements>

<success_criteria>
- Plan addresses all requirements
- Phases are sequential and logical
- Tasks are specific and actionable
- Metadata captures uncertainties
- SUMMARY.md created with phase overview
- Ready for implementation prompts to consume
</success_criteria>
```
</prompt_template>

<key_principles>

<reference_research>
Plans should build on research findings:
```xml
<context>
Research findings: @.prompts/001-auth-research/auth-research.md

Key findings to incorporate:
- Recommended approach from research
- Constraints identified
- Best practices to follow
</context>
```
</reference_research>

<prompt_sized_phases>
Each phase should be executable by a single prompt:
```xml
<phase number="1" name="setup-infrastructure">
  <objective>Create base auth structure and types</objective>
  <tasks>
    <task>Create auth module directory</task>
    <task>Define TypeScript types for tokens</task>
    <task>Set up test infrastructure</task>
  </tasks>
</phase>
```
</prompt_sized_phases>

<execution_hints>
Help the next Claude understand how to proceed:
```xml
<phase number="2" name="implement-jwt">
  <execution_notes>
    This phase modifies files from phase 1.
    Reference the types created in phase 1.
    Run tests after each major change.
  </execution_notes>
</phase>
```
</execution_hints>

</key_principles>

<plan_types>

<implementation_roadmap>
For breaking down how to build something:

```xml
<objective>
Create implementation roadmap for user authentication system.

Purpose: Guide phased implementation with clear milestones
Input: Authentication research findings
Output: auth-plan.md with 4-5 implementation phases
</objective>

<context>
Research: @.prompts/001-auth-research/auth-research.md
</context>

<planning_requirements>
- Break into independently testable phases
- Each phase builds on previous
- Include testing at each phase
- Consider rollback points
</planning_requirements>
```
</implementation_roadmap>

<decision_framework>
For choosing between options:

```xml
<objective>
Create decision framework for selecting database technology.

Purpose: Make informed choice between PostgreSQL, MongoDB, and DynamoDB
Input: Database research findings
Output: database-plan.md with criteria, analysis, recommendation
</objective>

<output_structure>
Structure as decision framework:

```xml
<decision_framework>
  <options>
    <option name="PostgreSQL">
      <pros>{List}</pros>
      <cons>{List}</cons>
      <fit_score criteria="scalability">8/10</fit_score>
      <fit_score criteria="flexibility">6/10</fit_score>
    </option>
    <!-- Other options -->
  </options>

  <recommendation>
    <choice>{Selected option}</choice>
    <rationale>{Why this choice}</rationale>
    <risks>{What could go wrong}</risks>
    <mitigations>{How to address risks}</mitigations>
  </recommendation>

  <metadata>
    <confidence level="high">
      Clear winner based on requirements
    </confidence>
    <assumptions>
      - Expected data volume: 10M records
      - Team has SQL experience
    </assumptions>
  </metadata>
</decision_framework>
```
</output_structure>
```
</decision_framework>

<process_definition>
For defining workflows or methodologies:

```xml
<objective>
Create deployment process for production releases.

Purpose: Standardize safe, repeatable deployments
Input: Current infrastructure research
Output: deployment-plan.md with step-by-step process
</objective>

<output_structure>
Structure as process:

```xml
<process>
  <overview>{High-level flow}</overview>

  <steps>
    <step number="1" name="pre-deployment">
      <actions>
        <action>Run full test suite</action>
        <action>Create database backup</action>
        <action>Notify team in #deployments</action>
      </actions>
      <checklist>
        <item>Tests passing</item>
        <item>Backup verified</item>
        <item>Team notified</item>
      </checklist>
      <rollback>N/A - no changes yet</rollback>
    </step>
    <!-- Additional steps -->
  </steps>

  <metadata>
    <dependencies>
      - CI/CD pipeline configured
      - Database backup system
      - Slack webhook for notifications
    </dependencies>
    <open_questions>
      - Blue-green vs rolling deployment?
      - Automated rollback triggers?
    </open_questions>
  </metadata>
</process>
```
</output_structure>
```
</process_definition>

</plan_types>

<metadata_guidelines>
Load: [metadata-guidelines.md](metadata-guidelines.md)
</metadata_guidelines>

---

## Reference: Question Bank

<overview>
Contextual questions for intake, organized by purpose. Use AskUserQuestion tool with these templates.
</overview>

<universal_questions>

<topic_identifier>
When topic not obvious from description:
```yaml
header: "Topic"
question: "What topic/feature is this for? (used for file naming)"
# Let user provide via "Other" option
# Enforce kebab-case (convert spaces to hyphens)
```
</topic_identifier>

<chain_reference>
When existing research/plan files found:
```yaml
header: "Reference"
question: "Should this prompt reference any existing research or plans?"
options:
  - "{file1}" - Found in .prompts/{folder1}/
  - "{file2}" - Found in .prompts/{folder2}/
  - "None" - Start fresh without referencing existing files
multiSelect: true
```
</chain_reference>

</universal_questions>

<do_questions>

<artifact_type>
When unclear what's being created:
```yaml
header: "Output type"
question: "What are you creating?"
options:
  - "Code/feature" - Software implementation
  - "Document/content" - Written material, documentation
  - "Design/spec" - Architecture, wireframes, specifications
  - "Configuration" - Config files, infrastructure setup
```
</artifact_type>

<scope_completeness>
When level of polish unclear:
```yaml
header: "Scope"
question: "What level of completeness?"
options:
  - "Production-ready" - Ship to users, needs polish and tests
  - "Working prototype" - Functional but rough edges acceptable
  - "Proof of concept" - Minimal viable demonstration
```
</scope_completeness>

<approach_patterns>
When implementation approach unclear:
```yaml
header: "Approach"
question: "Any specific patterns or constraints?"
options:
  - "Follow existing patterns" - Match current codebase style
  - "Best practices" - Modern, recommended approaches
  - "Specific requirement" - I have a constraint to specify
```
</approach_patterns>

<testing_requirements>
When verification needs unclear:
```yaml
header: "Testing"
question: "What testing is needed?"
options:
  - "Full test coverage" - Unit, integration, e2e tests
  - "Core functionality" - Key paths tested
  - "Manual verification" - No automated tests required
```
</testing_requirements>

<integration_points>
For features that connect to existing code:
```yaml
header: "Integration"
question: "How does this integrate with existing code?"
options:
  - "New module" - Standalone, minimal integration
  - "Extends existing" - Adds to current implementation
  - "Replaces existing" - Replaces current implementation
```
</integration_points>

</do_questions>

<plan_questions>

<plan_purpose>
What the plan leads to:
```yaml
header: "Plan for"
question: "What is this plan leading to?"
options:
  - "Implementation" - Break down how to build something
  - "Decision" - Weigh options, choose an approach
  - "Process" - Define workflow or methodology
```
</plan_purpose>

<plan_format>
How to structure the output:
```yaml
header: "Format"
question: "What format works best?"
options:
  - "Phased roadmap" - Sequential stages with milestones
  - "Checklist/tasks" - Actionable items to complete
  - "Decision framework" - Criteria, trade-offs, recommendation
```
</plan_format>

<constraints>
What limits the plan:
```yaml
header: "Constraints"
question: "What constraints should the plan consider?"
options:
  - "Technical" - Stack limitations, dependencies, compatibility
  - "Resources" - Team capacity, expertise available
  - "Requirements" - Must-haves, compliance, standards
multiSelect: true
```
</constraints>

<granularity>
Level of detail needed:
```yaml
header: "Granularity"
question: "How detailed should the plan be?"
options:
  - "High-level phases" - Major milestones, flexible execution
  - "Detailed tasks" - Specific actionable items
  - "Prompt-ready" - Each phase is one prompt to execute
```
</granularity>

<dependencies>
What exists vs what needs creation:
```yaml
header: "Dependencies"
question: "What already exists?"
options:
  - "Greenfield" - Starting from scratch
  - "Existing codebase" - Building on current code
  - "Research complete" - Findings ready to plan from
```
</dependencies>

</plan_questions>

<research_questions>

<research_depth>
How comprehensive:
```yaml
header: "Depth"
question: "How deep should the research go?"
options:
  - "Overview" - High-level understanding, key concepts
  - "Comprehensive" - Detailed exploration, multiple perspectives
  - "Exhaustive" - Everything available, edge cases included
```
</research_depth>

<source_priorities>
Where to look:
```yaml
header: "Sources"
question: "What sources should be prioritized?"
options:
  - "Official docs" - Primary sources, authoritative references
  - "Community" - Blog posts, tutorials, real-world examples
  - "Current/latest" - 2024-2025 sources, cutting edge
multiSelect: true
```
</source_priorities>

<output_format>
How to present findings:
```yaml
header: "Output"
question: "How should findings be structured?"
options:
  - "Summary with key points" - Concise, actionable takeaways
  - "Detailed analysis" - In-depth with examples and comparisons
  - "Reference document" - Organized for future lookup
```
</output_format>

<research_focus>
When topic is broad:
```yaml
header: "Focus"
question: "What aspect is most important?"
options:
  - "How it works" - Concepts, architecture, internals
  - "How to use it" - Patterns, examples, best practices
  - "Trade-offs" - Pros/cons, alternatives, comparisons
```
</research_focus>

<evaluation_criteria>
For comparison research:
```yaml
header: "Criteria"
question: "What criteria matter most for evaluation?"
options:
  - "Performance" - Speed, scalability, efficiency
  - "Developer experience" - Ease of use, documentation, community
  - "Security" - Vulnerabilities, compliance, best practices
  - "Cost" - Pricing, resource usage, maintenance
multiSelect: true
```
</evaluation_criteria>

</research_questions>

<refine_questions>

<target_selection>
When multiple outputs exist:
```yaml
header: "Target"
question: "Which output should be refined?"
options:
  - "{file1}" - In .prompts/{folder1}/
  - "{file2}" - In .prompts/{folder2}/
  # List existing research/plan outputs
```
</target_selection>

<feedback_type>
What kind of improvement:
```yaml
header: "Improvement"
question: "What needs improvement?"
options:
  - "Deepen analysis" - Add more detail, examples, or rigor
  - "Expand scope" - Cover additional areas or topics
  - "Correct errors" - Fix factual mistakes or outdated info
  - "Restructure" - Reorganize for clarity or usability
```
</feedback_type>

<specific_feedback>
After type selected, gather details:
```yaml
header: "Details"
question: "What specifically should be improved?"
# Let user provide via "Other" option
# This is the core feedback that drives the refine prompt
```
</specific_feedback>

<preservation>
What to keep:
```yaml
header: "Preserve"
question: "What's working well that should be kept?"
options:
  - "Structure" - Keep the overall organization
  - "Recommendations" - Keep the conclusions
  - "Code examples" - Keep the implementation patterns
  - "Everything except feedback areas" - Only change what's specified
```
</preservation>

</refine_questions>

<question_rules>
- Only ask about genuine gaps - don't ask what's already stated
- 2-4 questions max per round - avoid overwhelming
- Each option needs description - explain implications
- Prefer options over free-text - when choices are knowable
- User can always select "Other" - for custom input
- Route by purpose - use purpose-specific questions after primary gate
</question_rules>

---

## Reference: Refine Patterns

<overview>
Prompt patterns for improving existing research or plan outputs based on feedback.
</overview>

<prompt_template>
```xml
<objective>
Refine {topic}-{original_purpose} based on feedback.

Target: @.prompts/{num}-{topic}-{original_purpose}/{topic}-{original_purpose}.md
Current summary: @.prompts/{num}-{topic}-{original_purpose}/SUMMARY.md

Purpose: {What improvement is needed}
Output: Updated {topic}-{original_purpose}.md with improvements
</objective>

<context>
Original output: @.prompts/{num}-{topic}-{original_purpose}/{topic}-{original_purpose}.md
</context>

<feedback>
{Specific issues to address}
{What was missing or insufficient}
{Areas needing more depth}
</feedback>

<preserve>
{What worked well and should be kept}
{Structure or findings to maintain}
</preserve>

<requirements>
- Address all feedback points
- Maintain original structure and metadata format
- Keep what worked from previous version
- Update confidence based on improvements
- Clearly improve on identified weaknesses
</requirements>

<output>
1. Archive current output to: `.prompts/{num}-{topic}-{original_purpose}/archive/{topic}-{original_purpose}-v{n}.md`
2. Write improved version to: `.prompts/{num}-{topic}-{original_purpose}/{topic}-{original_purpose}.md`
3. Create SUMMARY.md with version info and changes from previous
</output>

<summary_requirements>
Create `.prompts/{num}-{topic}-{original_purpose}/SUMMARY.md`

Load template: [summary-template.md](summary-template.md)

For Refine, always include:
- Version with iteration info (e.g., "v2 (refined from v1)")
- Changes from Previous section listing what improved
- Updated confidence if gaps were filled
</summary_requirements>

<success_criteria>
- All feedback points addressed
- Original structure maintained
- Previous version archived
- SUMMARY.md reflects version and changes
- Quality demonstrably improved
</success_criteria>
```
</prompt_template>

<key_principles>

<preserve_context>
Refine builds on existing work, not replaces it:
```xml
<context>
Original output: @.prompts/001-auth-research/auth-research.md

Key strengths to preserve:
- Library comparison structure
- Security recommendations
- Code examples format
</context>
```
</preserve_context>

<specific_feedback>
Feedback must be actionable:
```xml
<feedback>
Issues to address:
- Security analysis was surface-level - need CVE references and vulnerability patterns
- Performance benchmarks missing - add actual timing data
- Rate limiting patterns not covered

Do NOT change:
- Library comparison structure
- Recommendation format
</feedback>
```
</specific_feedback>

<version_tracking>
Archive before overwriting:
```xml
<output>
1. Archive: `.prompts/001-auth-research/archive/auth-research-v1.md`
2. Write improved: `.prompts/001-auth-research/auth-research.md`
3. Update SUMMARY.md with version info
</output>
```
</version_tracking>

</key_principles>

<refine_types>

<deepen_research>
When research was too surface-level:

```xml
<objective>
Refine auth-research based on feedback.

Target: @.prompts/001-auth-research/auth-research.md
</objective>

<feedback>
- Security analysis too shallow - need specific vulnerability patterns
- Missing performance benchmarks
- Rate limiting not covered
</feedback>

<preserve>
- Library comparison structure
- Code example format
- Recommendation priorities
</preserve>

<requirements>
- Add CVE references for common vulnerabilities
- Include actual benchmark data from library docs
- Add rate limiting patterns section
- Increase confidence if gaps are filled
</requirements>
```
</deepen_research>

<expand_scope>
When research missed important areas:

```xml
<objective>
Refine stripe-research to include webhooks.

Target: @.prompts/005-stripe-research/stripe-research.md
</objective>

<feedback>
- Webhooks section completely missing
- Need signature verification patterns
- Retry handling not covered
</feedback>

<preserve>
- API authentication section
- Checkout flow documentation
- Error handling patterns
</preserve>

<requirements>
- Add comprehensive webhooks section
- Include signature verification code examples
- Cover retry and idempotency patterns
- Update summary to reflect expanded scope
</requirements>
```
</expand_scope>

<update_plan>
When plan needs adjustment:

```xml
<objective>
Refine auth-plan to add rate limiting phase.

Target: @.prompts/002-auth-plan/auth-plan.md
</objective>

<feedback>
- Rate limiting was deferred but is critical for production
- Should be its own phase, not bundled with tests
</feedback>

<preserve>
- Phase 1-3 structure
- Dependency chain
- Task granularity
</preserve>

<requirements>
- Insert Phase 4: Rate limiting
- Adjust Phase 5 (tests) to depend on rate limiting
- Update phase count in summary
- Ensure new phase is prompt-sized
</requirements>
```
</update_plan>

<correct_errors>
When output has factual errors:

```xml
<objective>
Refine jwt-research to correct library recommendation.

Target: @.prompts/003-jwt-research/jwt-research.md
</objective>

<feedback>
- jsonwebtoken recommendation is outdated
- jose is now preferred for security and performance
- Bundle size comparison was incorrect
</feedback>

<preserve>
- Research structure
- Security best practices section
- Token storage recommendations
</preserve>

<requirements>
- Update library recommendation to jose
- Correct bundle size data
- Add note about jsonwebtoken deprecation concerns
- Lower confidence if other findings may need verification
</requirements>
```
</correct_errors>

</refine_types>

<folder_structure>
Refine prompts get their own folder (new number), but output goes to the original folder:

```
.prompts/
├── 001-auth-research/
│   ├── completed/
│   │   └── 001-auth-research.md       # Original prompt
│   ├── archive/
│   │   └── auth-research-v1.md        # Archived v1
│   ├── auth-research.md               # Current (v2)
│   └── SUMMARY.md                     # Reflects v2
├── 004-auth-research-refine/
│   ├── completed/
│   │   └── 004-auth-research-refine.md  # Refine prompt
│   └── (no output here - goes to 001)
```

This maintains:
- Clear prompt history (each prompt is numbered)
- Single source of truth for each output
- Visible iteration count in SUMMARY.md
</folder_structure>

<execution_notes>

<dependency_handling>
Refine prompts depend on the target output existing:
- Check target file exists before execution
- If target folder missing, offer to create the original prompt first

```xml
<dependency_check>
If `.prompts/{num}-{topic}-{original_purpose}/{topic}-{original_purpose}.md` not found:
- Error: "Cannot refine - target output doesn't exist"
- Offer: "Create the original {purpose} prompt first?"
</dependency_check>
```
</dependency_handling>

<archive_creation>
Before overwriting, ensure archive exists:
```bash
mkdir -p .prompts/{num}-{topic}-{original_purpose}/archive/
mv .prompts/{num}-{topic}-{original_purpose}/{topic}-{original_purpose}.md \
   .prompts/{num}-{topic}-{original_purpose}/archive/{topic}-{original_purpose}-v{n}.md
```
</archive_creation>

<summary_update>
SUMMARY.md must reflect the refinement:
- Update version number
- Add "Changes from Previous" section
- Update one-liner if findings changed
- Update confidence if improved
</summary_update>

</execution_notes>

---

## Reference: Research Patterns

<overview>
Prompt patterns for gathering information that will be consumed by planning or implementation prompts.

Includes quality controls, verification mechanisms, and streaming writes to prevent research gaps and token limit failures.
</overview>

<prompt_template>
```xml
<session_initialization>
Before beginning research, verify today's date:
!`date +%Y-%m-%d`

Use this date when searching for "current" or "latest" information.
Example: If today is 2025-11-22, search for "2025" not "2024".
</session_initialization>

<research_objective>
Research {topic} to inform {subsequent use}.

Purpose: {What decision/implementation this enables}
Scope: {Boundaries of the research}
Output: {topic}-research.md with structured findings
</research_objective>

<research_scope>
<include>
{What to investigate}
{Specific questions to answer}
</include>

<exclude>
{What's out of scope}
{What to defer to later research}
</exclude>

<sources>
{Priority sources with exact URLs for WebFetch}
Official documentation:
- https://example.com/official-docs
- https://example.com/api-reference

Search queries for WebSearch:
- "{topic} best practices {current_year}"
- "{topic} latest version"

{Time constraints: prefer current sources - check today's date first}
</sources>
</research_scope>

<verification_checklist>
{If researching configuration/architecture with known components:}
□ Verify ALL known configuration/implementation options (enumerate below):
  □ Option/Scope 1: {description}
  □ Option/Scope 2: {description}
  □ Option/Scope 3: {description}
□ Document exact file locations/URLs for each option
□ Verify precedence/hierarchy rules if applicable
□ Confirm syntax and examples from official sources
□ Check for recent updates or changes to documentation

{For all research:}
□ Verify negative claims ("X is not possible") with official docs
□ Confirm all primary claims have authoritative sources
□ Check both current docs AND recent updates/changelogs
□ Test multiple search queries to avoid missing information
□ Check for environment/tool-specific variations
</verification_checklist>

<research_quality_assurance>
Before completing research, perform these checks:

<completeness_check>
- [ ] All enumerated options/components documented with evidence
- [ ] Each access method/approach evaluated against ALL requirements
- [ ] Official documentation cited for critical claims
- [ ] Contradictory information resolved or flagged
</completeness_check>

<source_verification>
- [ ] Primary claims backed by official/authoritative sources
- [ ] Version numbers and dates included where relevant
- [ ] Actual URLs provided (not just "search for X")
- [ ] Distinguish verified facts from assumptions
</source_verification>

<blind_spots_review>
Ask yourself: "What might I have missed?"
- [ ] Are there configuration/implementation options I didn't investigate?
- [ ] Did I check for multiple environments/contexts (e.g., Desktop vs Code)?
- [ ] Did I verify claims that seem definitive ("cannot", "only", "must")?
- [ ] Did I look for recent changes or updates to documentation?
</blind_spots_review>

<critical_claims_audit>
For any statement like "X is not possible" or "Y is the only way":
- [ ] Is this verified by official documentation?
- [ ] Have I checked for recent updates that might change this?
- [ ] Are there alternative approaches I haven't considered?
</critical_claims_audit>
</research_quality_assurance>

<output_structure>
Save to: `.prompts/{num}-{topic}-research/{topic}-research.md`

Structure findings using this XML format:

```xml
<research>
  <summary>
    {2-3 paragraph executive summary of key findings}
  </summary>

  <findings>
    <finding category="{category}">
      <title>{Finding title}</title>
      <detail>{Detailed explanation}</detail>
      <source>{Where this came from}</source>
      <relevance>{Why this matters for the goal}</relevance>
    </finding>
    <!-- Additional findings -->
  </findings>

  <recommendations>
    <recommendation priority="high">
      <action>{What to do}</action>
      <rationale>{Why}</rationale>
    </recommendation>
    <!-- Additional recommendations -->
  </recommendations>

  <code_examples>
    {Relevant code patterns, snippets, configurations}
  </code_examples>

  <metadata>
    <confidence level="{high|medium|low}">
      {Why this confidence level}
    </confidence>
    <dependencies>
      {What's needed to act on this research}
    </dependencies>
    <open_questions>
      {What couldn't be determined}
    </open_questions>
    <assumptions>
      {What was assumed}
    </assumptions>

    <!-- ENHANCED: Research Quality Report -->
    <quality_report>
      <sources_consulted>
        {List URLs of official documentation and primary sources}
      </sources_consulted>
      <claims_verified>
        {Key findings verified with official sources}
      </claims_verified>
      <claims_assumed>
        {Findings based on inference or incomplete information}
      </claims_assumed>
      <contradictions_encountered>
        {Any conflicting information found and how resolved}
      </contradictions_encountered>
      <confidence_by_finding>
        {For critical findings, individual confidence levels}
        - Finding 1: High (official docs + multiple sources)
        - Finding 2: Medium (single source, unclear if current)
        - Finding 3: Low (inferred, requires hands-on verification)
      </confidence_by_finding>
    </quality_report>
  </metadata>
</research>
```
</output_structure>

<pre_submission_checklist>
Before submitting your research report, confirm:

**Scope Coverage**
- [ ] All enumerated options/approaches investigated
- [ ] Each component from verification checklist documented or marked "not found"
- [ ] Official documentation cited for all critical claims

**Claim Verification**
- [ ] Each "not possible" or "only way" claim verified with official docs
- [ ] URLs to official documentation included for key findings
- [ ] Version numbers and dates specified where relevant

**Quality Controls**
- [ ] Blind spots review completed ("What did I miss?")
- [ ] Quality report section filled out honestly
- [ ] Confidence levels assigned with justification
- [ ] Assumptions clearly distinguished from verified facts

**Output Completeness**
- [ ] All required XML sections present
- [ ] SUMMARY.md created with substantive one-liner
- [ ] Sources consulted listed with URLs
- [ ] Next steps clearly identified
</pre_submission_checklist>
```
</output_structure>

<incremental_output>
**CRITICAL: Write findings incrementally to prevent token limit failures**

Instead of generating the full research in memory and writing at the end:
1. Create the output file with initial structure
2. Write each finding as you discover it
3. Append code examples as you find them
4. Update metadata at the end

This ensures:
- Zero lost work if token limit is hit
- File contains all findings up to that point
- No estimation heuristics needed
- Works for any research size

<workflow>
Step 1 - Initialize structure:
```bash
# Create file with skeleton
Write: .prompts/{num}-{topic}-research/{topic}-research.md
Content: Basic XML structure with empty sections
```

Step 2 - Append findings incrementally:
```bash
# After researching authentication libraries
Edit: Append <finding> to <findings> section

# After discovering rate limits
Edit: Append another <finding> to <findings> section
```

Step 3 - Add code examples as discovered:
```bash
# Found jose example
Edit: Append to <code_examples> section
```

Step 4 - Finalize metadata:
```bash
# After completing research
Edit: Update <metadata> section with confidence, dependencies, etc.
```
</workflow>

<example_prompt_instruction>
```xml
<output_requirements>
Write findings incrementally to {topic}-research.md as you discover them:

1. Create the file with this initial structure:
   ```xml
   <research>
     <summary>[Will complete at end]</summary>
     <findings></findings>
     <recommendations></recommendations>
     <code_examples></code_examples>
     <metadata></metadata>
   </research>
   ```

2. As you research each aspect, immediately append findings:
   - Research JWT libraries → Write finding
   - Discover security pattern → Write finding
   - Find code example → Append to code_examples

3. After all research complete:
   - Write summary (synthesize all findings)
   - Write recommendations (based on findings)
   - Write metadata (confidence, dependencies, etc.)

This incremental approach ensures all work is saved even if execution
hits token limits. Never generate the full output in memory first.
</output_requirements>
```
</example_prompt_instruction>

<benefits>
**vs. Pre-execution estimation:**
- No estimation errors (you don't predict, you just write)
- No artificial modularization (agent decides natural breakpoints)
- No lost work (everything written is saved)

**vs. Single end-of-execution write:**
- Survives token limit failures (partial progress saved)
- Lower memory usage (write as you go)
- Natural checkpoint recovery (can continue from last finding)
</benefits>
</incremental_output>

<summary_requirements>
Create `.prompts/{num}-{topic}-research/SUMMARY.md`

Load template: [summary-template.md](summary-template.md)

For research, emphasize key recommendation and decision readiness. Next step typically: Create plan.
</summary_requirements>

<success_criteria>
- All scope questions answered
- All verification checklist items completed
- Sources are current and authoritative
- Findings are actionable
- Metadata captures gaps honestly
- Quality report distinguishes verified from assumed
- SUMMARY.md created with substantive one-liner
- Ready for planning/implementation to consume
</success_criteria>
```
</prompt_template>

<key_principles>

<structure_for_consumption>
The next Claude needs to quickly extract relevant information:
```xml
<finding category="authentication">
  <title>JWT vs Session Tokens</title>
  <detail>
    JWTs are preferred for stateless APIs. Sessions better for
    traditional web apps with server-side rendering.
  </detail>
  <source>OWASP Authentication Cheatsheet 2024</source>
  <relevance>
    Our API-first architecture points to JWT approach.
  </relevance>
</finding>
```
</structure_for_consumption>

<include_code_examples>
The implementation prompt needs patterns to follow:
```xml
<code_examples>
<example name="jwt-verification">
```typescript
import { jwtVerify } from 'jose';

const { payload } = await jwtVerify(
  token,
  new TextEncoder().encode(secret),
  { algorithms: ['HS256'] }
);
```
Source: jose library documentation
</example>
</code_examples>
```
</include_code_examples>

<explicit_confidence>
Help the next Claude know what to trust:
```xml
<metadata>
  <confidence level="medium">
    API documentation is comprehensive but lacks real-world
    performance benchmarks. Rate limits are documented but
    actual behavior may differ under load.
  </confidence>

  <quality_report>
    <confidence_by_finding>
      - JWT library comparison: High (npm stats + security audits + active maintenance verified)
      - Performance benchmarks: Low (no official data, community reports vary)
      - Rate limits: Medium (documented but not tested)
    </confidence_by_finding>
  </quality_report>
</metadata>
```
</explicit_confidence>

<enumerate_known_possibilities>
When researching systems with known components, enumerate them explicitly:
```xml
<verification_checklist>
**CRITICAL**: Verify ALL configuration scopes:
□ User scope - Global configuration
□ Project scope - Project-level configuration files
□ Local scope - Project-specific user overrides
□ Environment scope - Environment variable based
</verification_checklist>
```

This forces systematic coverage and prevents omissions.
</enumerate_known_possibilities>

</key_principles>

<research_types>

<technology_research>
For understanding tools, libraries, APIs:

```xml
<research_objective>
Research JWT authentication libraries for Node.js.

Purpose: Select library for auth implementation
Scope: Security, performance, maintenance status
Output: jwt-research.md
</research_objective>

<research_scope>
<include>
- Available libraries (jose, jsonwebtoken, etc.)
- Security track record
- Bundle size and performance
- TypeScript support
- Active maintenance
- Community adoption
</include>

<exclude>
- Implementation details (for planning phase)
- Specific code architecture (for implementation)
</exclude>

<sources>
Official documentation (use WebFetch):
- https://github.com/panva/jose
- https://github.com/auth0/node-jsonwebtoken

Additional sources (use WebSearch):
- "JWT library comparison {current_year}"
- "jose vs jsonwebtoken security {current_year}"
- npm download stats
- GitHub issues/security advisories
</sources>
</research_scope>

<verification_checklist>
□ Verify all major JWT libraries (jose, jsonwebtoken, passport-jwt)
□ Check npm download trends for adoption metrics
□ Review GitHub security advisories for each library
□ Confirm TypeScript support with examples
□ Document bundle sizes from bundlephobia or similar
</verification_checklist>
```
</technology_research>

<best_practices_research>
For understanding patterns and standards:

```xml
<research_objective>
Research authentication security best practices.

Purpose: Inform secure auth implementation
Scope: Current standards, common vulnerabilities, mitigations
Output: auth-security-research.md
</research_objective>

<research_scope>
<include>
- OWASP authentication guidelines
- Token storage best practices
- Common vulnerabilities (XSS, CSRF)
- Secure cookie configuration
- Password hashing standards
</include>

<sources>
Official sources (use WebFetch):
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

Search sources (use WebSearch):
- "OWASP authentication {current_year}"
- "secure token storage best practices {current_year}"
</sources>
</research_scope>

<verification_checklist>
□ Verify OWASP top 10 authentication vulnerabilities
□ Check latest OWASP cheatsheet publication date
□ Confirm recommended hash algorithms (bcrypt, scrypt, Argon2)
□ Document secure cookie flags (httpOnly, secure, sameSite)
</verification_checklist>
```
</best_practices_research>

<api_service_research>
For understanding external services:

```xml
<research_objective>
Research Stripe API for payment integration.

Purpose: Plan payment implementation
Scope: Endpoints, authentication, webhooks, testing
Output: stripe-research.md
</research_objective>

<research_scope>
<include>
- API structure and versioning
- Authentication methods
- Key endpoints for our use case
- Webhook events and handling
- Testing and sandbox environment
- Error handling patterns
- SDK availability
</include>

<exclude>
- Pricing details
- Account setup process
</exclude>

<sources>
Official sources (use WebFetch):
- https://stripe.com/docs/api
- https://stripe.com/docs/webhooks
- https://stripe.com/docs/testing

Context7 MCP:
- Use mcp__context7__resolve-library-id for Stripe
- Use mcp__context7__get-library-docs for current patterns
</sources>
</research_scope>

<verification_checklist>
□ Verify current API version and deprecation timeline
□ Check webhook event types for our use case
□ Confirm sandbox environment capabilities
□ Document rate limits from official docs
□ Verify SDK availability for our stack
</verification_checklist>
```
</api_service_research>

<comparison_research>
For evaluating options:

```xml
<research_objective>
Research database options for multi-tenant SaaS.

Purpose: Inform database selection decision
Scope: PostgreSQL, MongoDB, DynamoDB for our use case
Output: database-research.md
</research_objective>

<research_scope>
<include>
For each option:
- Multi-tenancy support patterns
- Scaling characteristics
- Cost model
- Operational complexity
- Team expertise requirements
</include>

<evaluation_criteria>
- Data isolation requirements
- Expected query patterns
- Scale projections
- Team familiarity
</evaluation_criteria>
</research_scope>

<verification_checklist>
□ Verify all candidate databases (PostgreSQL, MongoDB, DynamoDB)
□ Document multi-tenancy patterns for each with official sources
□ Compare scaling characteristics with authoritative benchmarks
□ Check pricing calculators for cost model verification
□ Assess team expertise honestly (survey if needed)
</verification_checklist>
```
</comparison_research>

</research_types>

<metadata_guidelines>
Load: [metadata-guidelines.md](metadata-guidelines.md)

**Enhanced guidance**:
- Use <quality_report> to distinguish verified facts from assumptions
- Assign confidence levels to individual findings when they vary
- List all sources consulted with URLs for verification
- Document contradictions encountered and how resolved
- Be honest about limitations and gaps in research
</metadata_guidelines>

<tool_usage>

<context7_mcp>
For library documentation:
```
Use mcp__context7__resolve-library-id to find library
Then mcp__context7__get-library-docs for current patterns
```
</context7_mcp>

<web_search>
For recent articles and updates:
```
Search: "{topic} best practices {current_year}"
Search: "{library} security vulnerabilities {current_year}"
Search: "{topic} vs {alternative} comparison {current_year}"
```
</web_search>

<web_fetch>
For specific documentation pages:
```
Fetch official docs, API references, changelogs with exact URLs
Prefer WebFetch over WebSearch for authoritative sources
```
</web_fetch>

Include tool usage hints in research prompts when specific sources are needed.
</tool_usage>

<pitfalls_reference>
Before completing research, review common pitfalls:
Load: [research-pitfalls.md](research-pitfalls.md)

Key patterns to avoid:
- Configuration scope assumptions - enumerate all scopes
- "Search for X" vagueness - provide exact URLs
- Deprecated vs current confusion - check changelogs
- Tool-specific variations - check each environment
</pitfalls_reference>

---

## Reference: Research Pitfalls

# Research Pitfalls - Known Patterns to Avoid

## Purpose
This document catalogs research mistakes discovered in production use, providing specific patterns to avoid and verification strategies to prevent recurrence.

## Known Pitfalls

### Pitfall 1: Configuration Scope Assumptions
**What**: Assuming global configuration means no project-scoping exists
**Example**: Concluding "MCP servers are configured GLOBALLY only" while missing project-scoped `.mcp.json`
**Why it happens**: Not explicitly checking all known configuration patterns
**Prevention**:
```xml
<verification_checklist>
**CRITICAL**: Verify ALL configuration scopes:
□ User/global scope - System-wide configuration
□ Project scope - Project-level configuration files
□ Local scope - Project-specific user overrides
□ Workspace scope - IDE/tool workspace settings
□ Environment scope - Environment variables
</verification_checklist>
```

### Pitfall 2: "Search for X" Vagueness
**What**: Asking researchers to "search for documentation" without specifying where
**Example**: "Research MCP documentation" → finds outdated community blog instead of official docs
**Why it happens**: Vague research instructions don't specify exact sources
**Prevention**:
```xml
<sources>
Official sources (use WebFetch):
- https://exact-url-to-official-docs
- https://exact-url-to-api-reference

Search queries (use WebSearch):
- "specific search query {current_year}"
- "another specific query {current_year}"
</sources>
```

### Pitfall 3: Deprecated vs Current Features
**What**: Finding archived/old documentation and concluding feature doesn't exist
**Example**: Finding 2022 docs saying "feature not supported" when current version added it
**Why it happens**: Not checking multiple sources or recent updates
**Prevention**:
```xml
<verification_checklist>
□ Check current official documentation
□ Review changelog/release notes for recent updates
□ Verify version numbers and publication dates
□ Cross-reference multiple authoritative sources
</verification_checklist>
```

### Pitfall 4: Tool-Specific Variations
**What**: Conflating capabilities across different tools/environments
**Example**: "Claude Desktop supports X" ≠ "Claude Code supports X"
**Why it happens**: Not explicitly checking each environment separately
**Prevention**:
```xml
<verification_checklist>
□ Claude Desktop capabilities
□ Claude Code capabilities
□ VS Code extension capabilities
□ API/SDK capabilities
Document which environment supports which features
</verification_checklist>
```

### Pitfall 5: Confident Negative Claims Without Citations
**What**: Making definitive "X is not possible" statements without official source verification
**Example**: "Folder-scoped MCP configuration is not supported" (missing `.mcp.json`)
**Why it happens**: Drawing conclusions from absence of evidence rather than evidence of absence
**Prevention**:
```xml
<critical_claims_audit>
For any "X is not possible" or "Y is the only way" statement:
- [ ] Is this verified by official documentation stating it explicitly?
- [ ] Have I checked for recent updates that might change this?
- [ ] Have I verified all possible approaches/mechanisms?
- [ ] Am I confusing "I didn't find it" with "it doesn't exist"?
</critical_claims_audit>
```

### Pitfall 6: Missing Enumeration
**What**: Investigating open-ended scope without enumerating known possibilities first
**Example**: "Research configuration options" instead of listing specific options to verify
**Why it happens**: Not creating explicit checklist of items to investigate
**Prevention**:
```xml
<verification_checklist>
Enumerate ALL known options FIRST:
□ Option 1: [specific item]
□ Option 2: [specific item]
□ Option 3: [specific item]
□ Check for additional unlisted options

For each option above, document:
- Existence (confirmed/not found/unclear)
- Official source URL
- Current status (active/deprecated/beta)
</verification_checklist>
```

### Pitfall 7: Single-Source Verification
**What**: Relying on a single source for critical claims
**Example**: Using only Stack Overflow answer from 2021 for current best practices
**Why it happens**: Not cross-referencing multiple authoritative sources
**Prevention**:
```xml
<source_verification>
For critical claims, require multiple sources:
- [ ] Official documentation (primary)
- [ ] Release notes/changelog (for currency)
- [ ] Additional authoritative source (for verification)
- [ ] Contradiction check (ensure sources agree)
</source_verification>
```

### Pitfall 8: Assumed Completeness
**What**: Assuming search results are complete and authoritative
**Example**: First Google result is outdated but assumed current
**Why it happens**: Not verifying publication dates and source authority
**Prevention**:
```xml
<source_verification>
For each source consulted:
- [ ] Publication/update date verified (prefer recent/current)
- [ ] Source authority confirmed (official docs, not blogs)
- [ ] Version relevance checked (matches current version)
- [ ] Multiple search queries tried (not just one)
</source_verification>
```

## Red Flags in Research Outputs

### 🚩 Red Flag 1: Zero "Not Found" Results
**Warning**: Every investigation succeeds perfectly
**Problem**: Real research encounters dead ends, ambiguity, and unknowns
**Action**: Expect honest reporting of limitations, contradictions, and gaps

### 🚩 Red Flag 2: No Confidence Indicators
**Warning**: All findings presented as equally certain
**Problem**: Can't distinguish verified facts from educated guesses
**Action**: Require confidence levels (High/Medium/Low) for key findings

### 🚩 Red Flag 3: Missing URLs
**Warning**: "According to documentation..." without specific URL
**Problem**: Can't verify claims or check for updates
**Action**: Require actual URLs for all official documentation claims

### 🚩 Red Flag 4: Definitive Statements Without Evidence
**Warning**: "X cannot do Y" or "Z is the only way" without citation
**Problem**: Strong claims require strong evidence
**Action**: Flag for verification against official sources

### 🚩 Red Flag 5: Incomplete Enumeration
**Warning**: Verification checklist lists 4 items, output covers 2
**Problem**: Systematic gaps in coverage
**Action**: Ensure all enumerated items addressed or marked "not found"

## Continuous Improvement

When research gaps occur:

1. **Document the gap**
   - What was missed or incorrect?
   - What was the actual correct information?
   - What was the impact?

2. **Root cause analysis**
   - Why wasn't it caught?
   - Which verification step would have prevented it?
   - What pattern does this reveal?

3. **Update this document**
   - Add new pitfall entry
   - Update relevant checklists
   - Share lesson learned

## Quick Reference Checklist

Before submitting research, verify:

- [ ] All enumerated items investigated (not just some)
- [ ] Negative claims verified with official docs
- [ ] Multiple sources cross-referenced for critical claims
- [ ] URLs provided for all official documentation
- [ ] Publication dates checked (prefer recent/current)
- [ ] Tool/environment-specific variations documented
- [ ] Confidence levels assigned honestly
- [ ] Assumptions distinguished from verified facts
- [ ] "What might I have missed?" review completed

---

**Living Document**: Update after each significant research gap
**Lessons From**: MCP configuration research gap (missed `.mcp.json`)

---

## Reference: Summary Template

<overview>
Standard SUMMARY.md structure for all prompt outputs. Every executed prompt creates this file for human scanning.
</overview>

<template>
```markdown
# {Topic} {Purpose} Summary

**{Substantive one-liner describing outcome}**

## Version
{v1 or "v2 (refined from v1)"}

## Changes from Previous
{Only include if v2+, otherwise omit this section}

## Key Findings
- {Most important finding or action}
- {Second key item}
- {Third key item}

## Files Created
{Only include for Do prompts}
- `path/to/file.ts` - Description

## Decisions Needed
{Specific actionable decisions requiring user input, or "None"}

## Blockers
{External impediments preventing progress, or "None"}

## Next Step
{Concrete forward action}

---
*Confidence: {High|Medium|Low}*
*Iterations: {n}*
*Full output: {filename.md}* (omit for Do prompts)
```
</template>

<field_requirements>

<one_liner>
Must be substantive - describes actual outcome, not status.

**Good**: "JWT with jose library and httpOnly cookies recommended"
**Bad**: "Research completed"

**Good**: "4-phase implementation: types → JWT core → refresh → tests"
**Bad**: "Plan created"

**Good**: "JWT middleware complete with 6 files in src/auth/"
**Bad**: "Implementation finished"
</one_liner>

<key_findings>
Purpose-specific content:
- **Research**: Key recommendations and discoveries
- **Plan**: Phase overview with objectives
- **Do**: What was implemented, patterns used
- **Refine**: What improved from previous version
</key_findings>

<decisions_needed>
Actionable items requiring user judgment:
- Architectural choices
- Tradeoff confirmations
- Assumption validation
- Risk acceptance

Must be specific: "Approve 15-minute token expiry" not "review recommended"
</decisions_needed>

<blockers>
External impediments (rare):
- Access issues
- Missing dependencies
- Environment problems

Most prompts have "None" - only flag genuine problems.
</blockers>

<next_step>
Concrete action:
- "Create auth-plan.md"
- "Execute Phase 1 prompt"
- "Run tests"

Not vague: "proceed to next phase"
</next_step>

</field_requirements>

<purpose_variations>

<research_summary>
Emphasize: Key recommendation, decision readiness
Next step typically: Create plan
</research_summary>

<plan_summary>
Emphasize: Phase breakdown, assumptions needing validation
Next step typically: Execute first phase
</plan_summary>

<do_summary>
Emphasize: Files created, test status
Next step typically: Run tests or execute next phase
</do_summary>

<refine_summary>
Emphasize: What improved, version number
Include: Changes from Previous section
</refine_summary>

</purpose_variations>
