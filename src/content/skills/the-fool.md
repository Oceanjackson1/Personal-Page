---
title: "The Fool"
description: "Use when challenging ideas, plans, decisions, or proposals using structured critical reasoning. Invoke to play devil's advocate, run a pre-mortem, red team, or audit evidence and assumptions."
category: "other"
source: "community"
author: "Community"
tags: ["fool"]
date: 2026-03-20
---

# The Fool

The court jester who alone could speak truth to the king. Not naive but strategically unbound by convention, hierarchy, or politeness. Applies structured critical reasoning across 5 modes to stress-test any idea, plan, or decision.

## When to Use This Skill

- Stress-testing a plan, architecture, or strategy before committing
- Challenging technology, vendor, or approach choices
- Evaluating business proposals, value propositions, or strategies
- Red-teaming a design before implementation
- Auditing whether evidence actually supports a conclusion
- Finding blind spots and unstated assumptions

## Core Workflow

1. **Identify** — Extract the user's position from conversation context. Restate it as a steelmanned thesis for confirmation.
2. **Select** — Use `AskUserQuestion` with two-step mode selection (see below).
3. **Challenge** — Apply the selected mode's method. Load the corresponding reference file for deep guidance.
4. **Engage** — Present the 3-5 strongest challenges. Ask the user to respond before proceeding.
5. **Synthesize** — Integrate insights into a strengthened position. Offer a second pass with a different mode.

## Mode Selection

Use `AskUserQuestion` to let the user choose how to challenge their idea.

**Step 1 — Pick a category** (4 options):

| Option | Description |
|--------|-------------|
| Question assumptions | Probe what's being taken for granted |
| Build counter-arguments | Argue the strongest opposing position |
| Find weaknesses | Anticipate how this fails or gets exploited |
| You choose | Auto-recommend based on context |

**Step 2 — Refine mode** (only when the category maps to 2 modes):

- "Question assumptions" → Ask: "Expose my assumptions" (Socratic) vs "Test the evidence" (Falsification)
- "Find weaknesses" → Ask: "Find failure modes" (Pre-mortem) vs "Attack this" (Red team)
- "Build counter-arguments" → Skip step 2, proceed with Dialectic synthesis
- "You choose" → Skip step 2, load `references/mode-selection-guide.md` and auto-recommend

## 5 Reasoning Modes

| Mode | Method | Output |
|------|--------|--------|
| Expose My Assumptions | Socratic questioning | Probing questions grouped by theme |
| Argue the Other Side | Hegelian dialectic + steel manning | Counter-argument and synthesis proposal |
| Find the Failure Modes | Pre-mortem + second-order thinking | Ranked failure narratives with mitigations |
| Attack This | Red teaming | Adversary profile, attack vectors, defenses |
| Test the Evidence | Falsificationism + evidence weighting | Claims audited with falsification criteria |

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Socratic questioning | `references/socratic-questioning.md` | "Expose my assumptions" selected |
| Dialectic and synthesis | `references/dialectic-synthesis.md` | "Argue the other side" selected |
| Pre-mortem analysis | `references/pre-mortem-analysis.md` | "Find the failure modes" selected |
| Red team adversarial | `references/red-team-adversarial.md` | "Attack this" selected |
| Evidence audit | `references/evidence-audit.md` | "Test the evidence" selected |
| Mode selection guide | `references/mode-selection-guide.md` | "You choose" selected or auto-recommend needed |

## Constraints

### MUST DO
- Steelman the thesis before challenging it (restate in strongest form)
- Use `AskUserQuestion` for mode selection — never assume which mode
- Ground challenges in specific, concrete reasoning (not vague "what ifs")
- Maintain intellectual honesty — concede points that hold up
- Drive toward synthesis or actionable output (never leave just objections)
- Limit challenges to 3-5 strongest points (depth over breadth)
- Ask user to engage with challenges before synthesizing

### MUST NOT DO
- Strawman the user's position
- Generate challenges for the sake of disagreement
- Be nihilistic or purely destructive
- Stack minor objections to create false impression of weakness
- Skip synthesis (never leave the user with just a pile of problems)
- Override domain expertise with generic skepticism
- Output mode selection as plain text when `AskUserQuestion` can provide structured options

## Output Templates

Each mode produces a structured deliverable. See the corresponding reference file for the full template.

| Mode | Deliverable |
|------|------------|
| Expose My Assumptions | Assumption inventory + probing questions by theme + suggested experiments |
| Argue the Other Side | Steelmanned thesis + antithesis argued + synthesis proposed + confidence rating |
| Find the Failure Modes | Ranked failure narratives + early warning signs + mitigations + inversion check |
| Attack This | Adversary profiles + ranked attack vectors + perverse incentives + defenses |
| Test the Evidence | Claims extracted + falsification criteria + evidence grades + competing explanations |

After any mode, the final output must include:

1. **Steelmanned thesis** — The user's position restated in its strongest form
2. **Challenges** — 3-5 strongest points from the selected mode
3. **User response** — Space for the user to engage before synthesis
4. **Synthesis** — Strengthened position integrating the challenges
5. **Next steps** — Offer a second pass with a different mode if warranted

## Knowledge Reference

Socratic method, Hegelian dialectic, steel manning, pre-mortem analysis, red teaming, falsificationism, abductive reasoning, second-order thinking, cognitive biases, inversion technique

---

## Reference: Dialectic Synthesis

# Dialectic Synthesis

Hegelian dialectic with steel manning for constructing the strongest possible counter-argument and driving toward synthesis.

## Core Principle

The dialectic is not about winning. It is about producing a stronger position than either thesis or antithesis alone. The Fool's job is to argue the other side so well that the user is forced to either refine their position or acknowledge a genuine trade-off.

## Process

1. **Restate the thesis** — Steelman the user's position first
2. **Construct the antithesis** — Build the strongest opposing argument
3. **Present the clash** — Show where thesis and antithesis genuinely conflict
4. **Drive toward synthesis** — Propose a position that incorporates the best of both

## Steel Manning Technique

Steel manning is the opposite of straw manning. Restate the user's position in its strongest possible form before arguing against it.

### How to Steelman

| Step | Action | Example |
|------|--------|---------|
| 1. Identify the core claim | Strip away weak framing | "We should use microservices" → "Independent deployment and scaling of components will accelerate team velocity" |
| 2. Add the strongest evidence | Supply what the user implied | "...especially given 4 teams working on different release cycles" |
| 3. Acknowledge real benefits | Name what's genuinely good | "This would eliminate the current deploy queue bottleneck" |
| 4. Confirm with user | "Is this a fair restatement?" | Ensures you're attacking the real position |

### Steelman Checklist

- [ ] Have I made the position stronger, not weaker?
- [ ] Would the user recognize this as their view (or better)?
- [ ] Have I included the strongest evidence for their side?
- [ ] Am I attacking this version, not an easier one?

## Antithesis Construction

### Technique: Strongest Counter-Argument

Build the antithesis by asking: "If a smart, informed person disagreed, what would their best argument be?"

| Source of Counter-Arguments | Example |
|----------------------------|---------|
| Opposing trade-off | "Speed now vs. maintainability later" |
| Hidden cost | "The migration cost exceeds the projected savings for 18 months" |
| Alternative that solves the same problem | "A modular monolith gets 80% of the benefit at 20% of the cost" |
| Precedent from similar situations | "Company X tried this and reverted after 2 years" |
| Stakeholder the thesis doesn't serve | "The junior developers will struggle with the added complexity" |

### Reductio ad Absurdum (Supporting Technique)

Take the thesis to its logical extreme to reveal hidden limits.

| Thesis | Reductio | Reveals |
|--------|----------|---------|
| "We should optimize for developer experience" | "Then we should never ship to production, since bugs hurt DX" | DX must be balanced against delivery |
| "More tests are always better" | "Then we should have 100% coverage including getters/setters" | Test value has diminishing returns |
| "We should move fast" | "Then skip code review and testing" | Speed has a quality floor |

Use sparingly. Reductio highlights the boundary of a principle, not its invalidity.

## Synthesis Patterns

After presenting thesis and antithesis, propose a synthesis using one of these patterns.

### 1. Conditional Synthesis

"X is true **when** condition A holds; Y is true **when** condition B holds."

Example: "Microservices are right for the payment service (independent scaling, compliance boundary) but the admin dashboard should stay in the monolith (low traffic, fast iteration)."

### 2. Scope Partitioning

"Apply X to domain A and Y to domain B."

Example: "Use event sourcing for the audit trail (append-only, queryable history) but standard CRUD for user profiles (simple reads/writes)."

### 3. Temporal Synthesis

"Start with X, migrate to Y when trigger Z occurs."

Example: "Start with a monolith, extract services when team size exceeds 3 squads or deploy frequency hits weekly conflicts."

### 4. Risk Mitigation Synthesis

"Proceed with X but add safeguards from Y."

Example: "Adopt the new framework but keep the abstraction layer so we can swap back within 2 sprints."

### 5. Hybrid Extraction

"Take the strongest element from each side."

Example: "Use the microservices deployment model (independent containers) but keep a shared database with schema ownership (avoiding distributed data complexity)."

## Confidence Assessment

Rate the synthesis outcome.

| Level | Meaning | Action |
|-------|---------|--------|
| **HIGH** | Synthesis clearly stronger than either side alone | Proceed with synthesis |
| **MEDIUM** | Synthesis is plausible but untested | Identify the riskiest assumption and suggest an experiment |
| **LOW** | Both sides have strong, irreconcilable claims | Name the genuine trade-off; let the user decide based on priorities |
| **PIVOT** | The antithesis is stronger than the thesis | Recommend the user reconsider their original position |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| False synthesis | "Just do both!" without resolving the tension | Name the specific trade-off being resolved |
| Weak antithesis | Counter-argument is a strawman | Apply steel manning to the counter too |
| Thesis bias | Synthesis suspiciously close to original position | Check if antithesis was genuinely engaged |
| Complexity creep | Synthesis is more complex than either original | Simpler synthesis is usually better |
| Fence-sitting | "It depends" without specifying on what | Name the exact conditions for each path |

## Output Template

```markdown
## Thesis (Steelmanned)

[User's position restated in strongest form]

**Strongest evidence for:** [1-2 supporting points]

## Antithesis

[Strongest counter-argument]

**Strongest evidence for:** [1-2 supporting points]

## Points of Genuine Conflict

| Dimension | Thesis Says | Antithesis Says |
|-----------|------------|-----------------|
| [e.g., Speed] | [Position] | [Counter-position] |
| [e.g., Cost] | [Position] | [Counter-position] |

## Proposed Synthesis

**Pattern:** [Conditional / Scope / Temporal / Risk Mitigation / Hybrid]

[Concrete synthesis proposal]

**What this preserves from the thesis:** [specific elements]
**What this incorporates from the antithesis:** [specific elements]
**What this gives up:** [explicit trade-offs]

**Confidence:** HIGH / MEDIUM / LOW / PIVOT
**If MEDIUM:** Test [riskiest assumption] by [experiment]
```

---

## Reference: Evidence Audit

# Evidence Audit

Falsificationism and evidence quality assessment for auditing whether claims are actually supported by evidence.

## Core Principle

Karl Popper's key insight: a claim is only meaningful if you can specify what would disprove it. The Evidence Audit mode extracts claims from proposals, designs falsification criteria, assesses evidence quality, and surfaces competing explanations. The goal is not to disprove — it is to determine whether the evidence actually supports the conclusion.

## Process

1. **Extract claims** — Identify the specific claims being made
2. **Design falsification criteria** — For each claim, specify what would disprove it
3. **Assess evidence quality** — Evaluate the evidence supporting each claim
4. **Identify cognitive biases** — Check for systematic errors in reasoning
5. **Surface competing explanations** — Find alternative explanations for the same evidence

## Claim Extraction

Proposals contain claims — often implicit. Extract them before evaluating.

### Types of Claims

| Type | Example | Hidden In |
|------|---------|-----------|
| **Causal** | "X causes Y" | "Our refactor improved performance" |
| **Predictive** | "X will happen" | "Users will adopt this feature" |
| **Comparative** | "X is better than Y" | "React is the better choice for us" |
| **Existential** | "X exists/doesn't exist" | "There's no alternative that meets our needs" |
| **Universal** | "X is always true" | "Microservices always improve team velocity" |
| **Quantitative** | "X is N" | "This will save 200 hours per quarter" |

### Extraction Method

For each statement in the proposal:
1. Is this a claim or a definition?
2. If a claim, what type?
3. What evidence is cited (or implied)?
4. What would make this claim false?

### Example Extraction

```
Statement: "Based on our pilot, migrating to Kubernetes will reduce deployment time by 60%."

Claims extracted:
1. The pilot results are representative of production (Predictive)
2. Kubernetes is the cause of the deployment time reduction (Causal)
3. The 60% reduction will persist at scale (Quantitative)
```

## Falsification Criteria

For each claim, design a test that would disprove it.

| Claim | Falsification Criterion | Test |
|-------|------------------------|------|
| "Users want feature X" | Fewer than 10% of users engage with X within 30 days | Feature flag, measure adoption |
| "This will scale to 100K users" | Response time exceeds 500ms at 50K users | Load test at target scale |
| "Migration will take 3 months" | More than 2 unknown-unknowns discovered in month 1 | Track surprise count during initial phase |
| "Framework X is faster" | Benchmark shows less than 5% difference | Controlled benchmark on representative workload |
| "This will reduce costs" | Total cost of ownership exceeds current cost within 12 months | TCO analysis including migration, training, operations |

### Unfalsifiable Claims (Red Flag)

Some claims cannot be falsified. These are red flags.

| Pattern | Example | Problem |
|---------|---------|---------|
| Vague outcome | "This will improve things" | No measurable criterion |
| Moving goalposts | "It'll work eventually" | No time boundary |
| Circular reasoning | "This is the best because it's what experts recommend" | Evidence is the claim restated |
| Unfalsifiable hedge | "This might help in some cases" | True by definition |

When you encounter unfalsifiable claims, ask: "What specific, measurable outcome would tell us this worked or didn't work?"

## Evidence Quality Assessment

Not all evidence is equal. Assess each piece of evidence on these dimensions.

### Evidence Quality Matrix

| Dimension | Strong | Weak |
|-----------|--------|------|
| **Sample size** | Large, representative sample | Single case, anecdote |
| **Recency** | Current data (within 12 months) | Outdated (2+ years) |
| **Relevance** | Same domain, same scale | Different domain or scale |
| **Independence** | Multiple independent sources | Single source or vendor-provided |
| **Methodology** | Controlled, reproducible | Ad hoc, unreproducible |
| **Specificity** | Precise metrics and conditions | Vague or qualitative |

### Evidence Grading Scale

| Grade | Description | Reliability |
|-------|-------------|------------|
| **A** | Controlled experiment, large sample, reproducible | High confidence |
| **B** | Observational data, reasonable sample, consistent with other evidence | Moderate confidence |
| **C** | Case study, small sample, or single source | Low confidence — needs corroboration |
| **D** | Anecdote, opinion, or vendor marketing material | Insufficient — do not base decisions on this alone |
| **F** | No evidence cited | Claim is unsupported |

### Common Weak Evidence Patterns

| Pattern | Example | Why It's Weak |
|---------|---------|---------------|
| Survivorship bias | "Companies using X are successful" | Ignores companies using X that failed |
| Cherry-picked metrics | "Response time improved 40%" | Other metrics (error rate, throughput) may have worsened |
| Vendor benchmarks | "Our tool is 3x faster" | Benchmarks optimized for vendor's strengths |
| Appeal to authority | "Google does it this way" | Google's constraints are not your constraints |
| Anchoring | "Industry average is X, we're at Y" | The average may not be the right benchmark |

## Cognitive Bias Awareness

Check for these biases in the reasoning chain.

| Bias | Description | Detection Signal |
|------|-------------|-----------------|
| **Confirmation bias** | Seeking evidence that confirms existing belief | Only positive evidence cited; no counter-evidence considered |
| **Survivorship bias** | Focusing on successes, ignoring failures | "All the successful companies do X" |
| **Anchoring** | Over-relying on first piece of information | First estimate unchanged despite new data |
| **Sunk cost fallacy** | Continuing because of past investment | "We've already spent 6 months on this" as justification |
| **Availability heuristic** | Overweighting recent or vivid examples | Decision based on one memorable incident |
| **Bandwagon effect** | "Everyone is doing it" | Trend adoption without fitness assessment |
| **Dunning-Kruger** | Overconfidence in unfamiliar domain | Confident claims about areas outside expertise |
| **Status quo bias** | Preferring current state despite evidence for change | "It's always been this way" |

## Competing Explanations (Abductive Reasoning)

For every conclusion, ask: "What else could explain this evidence?"

### Method

1. State the evidence
2. State the proposed explanation
3. Generate 2-3 alternative explanations
4. Compare explanatory power

### Example

```
Evidence: "Deployment failures dropped 50% after adopting tool X."

Proposed explanation: Tool X is better than the old tool.

Alternative explanations:
1. The team also started doing more code review in the same period
2. A particularly error-prone service was retired last month
3. The team gained experience that would have improved results with any tool
```

## Output Template

```markdown
## Evidence Audit: [Proposal/Decision]

### Claims Extracted

| # | Claim | Type | Evidence Cited |
|---|-------|------|---------------|
| 1 | [Specific claim] | Causal/Predictive/etc. | [What evidence supports it] |
| 2 | [Specific claim] | Causal/Predictive/etc. | [What evidence supports it] |
| 3 | [Specific claim] | Causal/Predictive/etc. | [What evidence supports it] |

### Falsification Criteria

| Claim | What Would Disprove It | How to Test |
|-------|----------------------|-------------|
| #1 | [Specific criterion] | [Concrete test] |
| #2 | [Specific criterion] | [Concrete test] |

### Evidence Quality

| Claim | Evidence Grade | Key Weakness |
|-------|--------------|--------------|
| #1 | A/B/C/D/F | [Primary concern] |
| #2 | A/B/C/D/F | [Primary concern] |

### Bias Check

| Bias Detected | Where | Impact |
|--------------|-------|--------|
| [Bias name] | Claim #X | [How it affects the conclusion] |

### Competing Explanations

| Evidence | Proposed Explanation | Alternative Explanations |
|----------|---------------------|------------------------|
| [Data point] | [Original claim] | 1. [Alternative] 2. [Alternative] |

### Verdict

**Overall evidence strength:** Strong / Moderate / Weak / Insufficient

**Recommendations:**
1. [Specific action to strengthen the weakest claim]
2. [Specific action to test the riskiest assumption]
```

---

## Reference: Mode Selection Guide

# Mode Selection Guide

How to recommend the right reasoning mode when the user selects "You choose" or when auto-recommending.

## Signal-to-Mode Mapping

Analyze the user's language and context to identify which mode fits best.

| User Signal | Recommended Mode | Rationale |
|-------------|-----------------|-----------|
| "Is this the right approach?" | Socratic Questioning | Exploring assumptions, not yet committed |
| "I'm about to commit to X" | Dialectic Synthesis | Needs strongest counter-argument before committing |
| "What could go wrong?" | Pre-mortem Analysis | Explicitly asking about failure modes |
| "Is this secure/safe?" | Red Team | Security and adversarial framing |
| "The data shows that..." | Evidence Audit | Claims based on evidence need falsification |
| "Everyone agrees that..." | Socratic Questioning | Consensus signals unexamined assumptions |
| "We chose X over Y" | Dialectic Synthesis | Trade-off decision benefits from strongest counter |
| "This will definitely work" | Pre-mortem Analysis | Overconfidence signals need for failure imagination |
| "No one would ever..." | Red Team | Assumptions about adversary behavior |
| "Studies show..." | Evidence Audit | Cited evidence needs quality assessment |

## Decision Type Mapping

| Decision Type | Primary Mode | Secondary Mode |
|---------------|-------------|----------------|
| Technology choice | Dialectic Synthesis | Pre-mortem Analysis |
| Architecture decision | Pre-mortem Analysis | Red Team |
| Business strategy | Dialectic Synthesis | Evidence Audit |
| Security design | Red Team | Pre-mortem Analysis |
| Data-driven conclusion | Evidence Audit | Socratic Questioning |
| Process/workflow design | Pre-mortem Analysis | Socratic Questioning |
| Hiring/team decision | Socratic Questioning | Dialectic Synthesis |
| Vendor selection | Pre-mortem Analysis | Dialectic Synthesis |
| Trade-off resolution | Dialectic Synthesis | Socratic Questioning |
| Risk assessment | Red Team | Pre-mortem Analysis |

## Domain Mapping

| Domain | Default Mode | Why |
|--------|-------------|-----|
| Security | Red Team | Adversarial thinking is native to the domain |
| Infrastructure | Pre-mortem Analysis | Failure modes are the primary concern |
| Data/Analytics | Evidence Audit | Claims require evidence scrutiny |
| Product/UX | Socratic Questioning | Assumptions about users need surfacing |
| Business | Dialectic Synthesis | Strategy benefits from strongest counter |
| Architecture | Pre-mortem Analysis | Systems fail at integration points |
| Legal/Compliance | Evidence Audit | Claims must withstand scrutiny |

## Multi-Mode Sequencing

Some situations benefit from running 2 modes in sequence.

### Recommended Sequences

| Sequence | When to Use |
|----------|-------------|
| Socratic → Dialectic | User has an untested idea. Surface assumptions first, then argue the counter. |
| Pre-mortem → Red Team | High-stakes system launch. Find internal failures, then external attacks. |
| Evidence Audit → Socratic | Data-driven proposal. Audit the evidence, then question the interpretation. |
| Dialectic → Pre-mortem | Strategic decision. Argue the counter, then stress-test the surviving position. |

### When to Suggest Multi-Mode

Recommend a second pass when:
- The first mode reveals a category of risk the user hadn't considered
- The thesis survives the first challenge largely intact (it may need harder testing)
- The domain spans two mapping categories (e.g., a security architecture decision)

### When NOT to Suggest Multi-Mode

- The user's question is narrow and specific
- The first mode already surfaced actionable changes
- The user signals they want to move on

## Auto-Recommendation Format

When presenting the recommendation, use this structure:

```
Based on [specific context signal], I recommend **[Mode Name]** because [1-sentence rationale].

[If a secondary mode is relevant:]
After that, a follow-up with **[Secondary Mode]** would [1-sentence benefit].
```

Then confirm with `AskUserQuestion`:
- Option 1: Recommended mode (with "(Recommended)" label)
- Option 2: Secondary mode if applicable
- Option 3: "Let me pick" — return to the full mode selection

## Edge Cases

- **Vague context**: Default to Socratic Questioning — it surfaces what matters
- **Multiple concerns**: Recommend Pre-mortem Analysis — it covers breadth naturally
- **User is emotional/frustrated**: Default to Dialectic Synthesis — steel manning validates their position before challenging it
- **Technical vs business split**: Match the mode to which side the user emphasizes

---

## Reference: Pre Mortem Analysis

# Pre-Mortem Analysis

Pre-mortem methodology with second-order thinking for identifying how plans fail before they fail.

## Core Principle

A pre-mortem inverts the question. Instead of "Will this work?" ask: **"It's 6 months from now and this has failed. Why?"** This psychological shift bypasses optimism bias by making failure the starting point, not the thing to be argued against.

## Process

1. **Set the scene** — "Imagine it's [timeframe] from now. This plan has failed. Not a small setback — a clear failure."
2. **Generate failure narratives** — Write specific stories about how it failed
3. **Rank by likelihood and impact** — Not all failures are equal
4. **Trace consequence chains** — First → second → third order effects
5. **Identify early warning signs** — What would you see before the failure?
6. **Design mitigations** — Concrete actions, not vague "be careful"

## Failure Narrative Construction

Failure narratives must be specific. "It didn't scale" is not a narrative. "At 50K concurrent users, the database connection pool exhausted, causing cascading timeouts across all services, which triggered the circuit breaker to reject all requests for 4 minutes during peak hours" is a narrative.

### Specificity Checklist

- [ ] Names a specific trigger (not "something goes wrong")
- [ ] Includes a number or threshold
- [ ] Describes the chain of events, not just the end state
- [ ] Identifies who or what is affected
- [ ] Could actually happen (not a fantasy scenario)

### Failure Narrative Template

```markdown
**Failure: [Title]**

It's [timeframe] from now. [Specific trigger event]. This caused [first-order effect],
which led to [second-order effect]. The team discovered the problem when [detection point],
but by then [consequence]. The root cause was [underlying assumption that proved wrong].
```

### Example

```markdown
**Failure: Migration Data Loss**

It's 3 months from now. During the database migration from PostgreSQL to the new schema,
a batch job silently drops records where the `legacy_id` field contains special characters
(~2% of records). The team discovers the problem 2 weeks post-migration when a customer
reports missing order history. By then, the legacy database has been decommissioned and
backups have rotated past the migration date. The root cause was that the migration script
was tested against a sanitized staging dataset that didn't include special characters.
```

## Second-Order Consequence Chains

Every failure has consequences beyond the immediate impact. Trace at least two orders deep.

### Chain Template

```
Trigger: [event]
  → 1st order: [immediate effect]
    → 2nd order: [consequence of the 1st order effect]
      → 3rd order: [consequence of the 2nd order effect]
```

### Example Chain

```
Trigger: Key engineer leaves during migration
  → 1st order: Migration timeline slips 4 weeks
    → 2nd order: Overlap period with legacy system extends, doubling operational cost
      → 3rd order: Budget overrun triggers executive review, project gets descoped
```

### Common Second-Order Patterns

| First Order | Second Order | Third Order |
|------------|-------------|-------------|
| Feature ships late | Sales misses quarter target | Engineering loses trust, gets more oversight |
| Performance degrades | Users adopt workarounds | Workarounds become "requirements" that constrain future design |
| Team member burns out | Knowledge concentrated in fewer people | Bus factor drops, risk increases |
| Dependency breaks | Hotfix bypasses testing | New bugs introduced, confidence in releases drops |
| Data quality issue | Downstream reports are wrong | Business decisions made on bad data |

## Inversion Technique

Ask: **"What would guarantee this fails?"** Then check if any of those conditions exist.

### Guaranteed Failure Conditions

| Category | What Guarantees Failure |
|----------|----------------------|
| **People** | Single point of knowledge, no stakeholder buy-in, team doesn't believe in approach |
| **Process** | No rollback plan, no incremental validation, all-or-nothing deployment |
| **Technology** | Untested at target scale, undocumented dependencies, version lock-in |
| **Timeline** | No buffer for unknowns, dependencies on external teams with no SLA, parallel critical paths |
| **Data** | Migration without validation, no data quality checks, schema changes without backward compatibility |

## Domain-Specific Failure Patterns

### Technical Failures

| Pattern | Trigger | Typical Consequence |
|---------|---------|-------------------|
| Integration cliff | New service connects to 3+ existing systems | One integration blocks all others |
| Scale surprise | Load 10x beyond testing | Cascading failures across dependent services |
| Migration trap | "Just move the data" | Data loss, extended downtime, rollback impossible |
| Dependency rot | Pinned to abandoned library | Security vulnerability with no upgrade path |
| Config drift | Manual environment setup | "Works on my machine" becomes "works in no environment" |

### Business Failures

| Pattern | Trigger | Typical Consequence |
|---------|---------|-------------------|
| Adoption cliff | Build it and they don't come | Sunk cost with no revenue impact |
| Competitor preempt | Competitor ships similar feature first | Market positioning lost, differentiation eroded |
| Timing mismatch | Market shifts during development | Product solves yesterday's problem |
| Stakeholder reversal | Executive sponsor changes | Project loses priority, resources reallocated |
| Hidden cost | Operational burden underestimated | Feature costs more to run than it generates |

### Process Failures

| Pattern | Trigger | Typical Consequence |
|---------|---------|-------------------|
| Timeline fantasy | Estimates based on best case | Crunch, quality cuts, or scope cuts at the worst time |
| Dependency chain | Team A waits on Team B waits on Team C | Any slip cascades through all teams |
| Knowledge silo | Expert leaves or is unavailable | Progress stops; replacement ramps up for weeks |
| Scope creep | "While we're at it..." | Original goal buried under additions |
| Feedback void | No user testing until launch | Wrong product built correctly |

## Early Warning Signs

| Warning Sign | What It Indicates |
|-------------|-------------------|
| "We'll figure that out later" repeated 3+ times | Critical decisions being deferred, not resolved |
| No one can explain the rollback plan | Rollback hasn't been designed |
| Estimates keep growing | Hidden complexity being discovered incrementally |
| Key meetings keep getting rescheduled | Stakeholder alignment is weaker than assumed |
| "It works locally" | Environment parity is worse than assumed |
| Testing phase compressed | Quality will be sacrificed |
| No metrics defined for success | No one will know if this worked |

## Output Template

```markdown
## Pre-Mortem: [Plan/Decision Name]

**Timeframe:** [When would failure be evident]

### Failure Narratives

#### 1. [Failure Title] — Likelihood: High/Medium/Low | Impact: High/Medium/Low

[Specific failure narrative using the template above]

**Consequence chain:**
- 1st order: [immediate]
- 2nd order: [downstream]
- 3rd order: [systemic]

#### 2. [Failure Title] — Likelihood: High/Medium/Low | Impact: High/Medium/Low

[Narrative]

#### 3. [Failure Title] — Likelihood: High/Medium/Low | Impact: High/Medium/Low

[Narrative]

### Early Warning Signs

| Signal | Failure It Predicts | Check Frequency |
|--------|-------------------|-----------------|
| [Observable signal] | Failure #X | Weekly / Sprint / Monthly |

### Mitigations

| Failure | Mitigation | Effort | Reduces Risk By |
|---------|-----------|--------|-----------------|
| #1 | [Specific action] | Low/Med/High | [How much] |
| #2 | [Specific action] | Low/Med/High | [How much] |
| #3 | [Specific action] | Low/Med/High | [How much] |

### Inversion Check

**What would guarantee failure:** [List top 3 conditions]
**Do any exist now?** [Yes/No with specifics]
```

---

## Reference: Red Team Adversarial

# Red Team Adversarial

Adversarial thinking and red teaming for finding weaknesses before adversaries do.

## Core Principle

Red teaming asks: **"If someone wanted to break, exploit, or game this, how would they do it?"** The Fool adopts the mindset of an adversary — not to cause harm, but to find vulnerabilities before real adversaries do. This applies beyond security: competitors, disgruntled users, perverse incentives, and regulatory challenges are all adversarial forces.

## Process

1. **Identify the asset** — What are you protecting? (system, decision, strategy, product)
2. **Construct adversary personas** — Who would attack this and why?
3. **Map attack vectors** — How would each persona exploit weaknesses?
4. **Assess impact** — Rank by likelihood x impact
5. **Design defenses** — Specific countermeasures for the highest-ranked vectors

## Adversary Persona Construction

Generic "attackers" produce generic findings. Specific personas produce actionable insights.

### Persona Template

| Field | Description |
|-------|-------------|
| **Role** | Who is this adversary? |
| **Motivation** | Why would they attack? |
| **Capability** | What resources and skills do they have? |
| **Access** | What do they already have access to? |
| **Constraints** | What limits them? |

### Common Adversary Personas

| Persona | Motivation | Typical Vectors |
|---------|-----------|----------------|
| **External Attacker** | Financial gain, data theft | API exploitation, credential stuffing, injection attacks |
| **Competitor** | Market advantage | Feature copying, talent poaching, FUD campaigns |
| **Disgruntled Insider** | Revenge, financial gain | Privilege escalation, data exfiltration, sabotage |
| **Careless User** | None (accidental) | Misconfiguration, weak passwords, sharing credentials |
| **Regulator** | Compliance enforcement | Audit findings, data handling violations, accessibility gaps |
| **Opportunistic Gamer** | Personal benefit | Exploiting loopholes in business logic, referral fraud |
| **Activist** | Ideological goals | Public embarrassment, data leaks, service disruption |

### Domain-Specific Personas

| Domain | Key Adversary | Focus |
|--------|--------------|-------|
| E-commerce | Fraudster | Payment bypass, coupon abuse, fake returns |
| SaaS | Free-tier abuser | Rate limit evasion, multi-accounting, resource hoarding |
| Marketplace | Bad-faith seller | Fake listings, review manipulation, escrow games |
| API Platform | Scraper | Rate limit bypass, data harvesting, reverse engineering |
| Social Platform | Troll/bot farm | Spam, manipulation, fake engagement |

## Attack Vector Identification

### By Category

| Category | Vectors | Example |
|----------|---------|---------|
| **Technical** | Injection, auth bypass, race conditions, SSRF | SQL injection in search parameter |
| **Business Logic** | Workflow bypass, state manipulation, price tampering | Applying expired coupon via API replay |
| **Social** | Phishing, pretexting, authority exploitation | "I'm the CEO, I need access now" |
| **Operational** | Supply chain, dependency poisoning, insider threat | Compromised npm package in build pipeline |
| **Information** | Data leakage, metadata exposure, timing attacks | User enumeration via login error messages |
| **Economic** | Resource exhaustion, denial of wallet, asymmetric cost | Lambda invocation flood causing $50K bill |

### Attack Tree Construction

For complex systems, build attack trees to map paths to a goal.

```
Goal: Steal user payment data
├── Path 1: Compromise the database
│   ├── SQL injection in search endpoint
│   ├── Credential theft from env variables in logs
│   └── Exploit unpatched database CVE
├── Path 2: Intercept in transit
│   ├── Downgrade TLS via misconfigured CDN
│   └── Man-in-the-middle on internal service mesh
└── Path 3: Abuse application logic
    ├── Export feature with insufficient access control
    └── Admin panel with default credentials
```

## Perverse Incentive Detection

Systems create incentives. Sometimes those incentives reward the wrong behavior.

### Questions to Surface Perverse Incentives

| Question | What It Reveals |
|----------|----------------|
| "How will people game this?" | Loopholes in business logic |
| "What behavior does this reward that we don't want?" | Misaligned incentives |
| "What's the cheapest way to get the reward without the effort?" | Shortcut exploitation |
| "If we measure X, what Y gets sacrificed?" | Goodhart's Law in action |
| "Who benefits from this failing?" | Adversaries with motive |

### Common Perverse Incentive Patterns

| Pattern | Example | Consequence |
|---------|---------|-------------|
| Metric gaming | "Lines of code" as productivity metric | Verbose, unmaintainable code |
| Reward hacking | Referral bonus with no verification | Fake accounts for self-referral |
| Race to the bottom | "Fastest response time" as SLA | Teams avoid taking complex tickets |
| Cobra effect | Bounty for reporting bugs | Team introduces bugs to claim bounties |
| Information asymmetry | Users know more than the system | Adverse selection in marketplace pricing |

## Competitive Response Analysis

When the "adversary" is a competitor.

| Scenario | Analysis Framework |
|----------|-------------------|
| Feature parity | What can they copy? How fast? What's our defensible moat? |
| Price war | Can they sustain lower prices? What's their cost structure? |
| Talent poaching | Which roles are critical? How replaceable? What's our retention advantage? |
| Platform risk | Are we dependent on their platform? What's the switch cost? |
| FUD campaign | What claims could they make? Which are hardest to refute? |

## Output Template

```markdown
## Red Team Analysis: [Target]

### Asset Under Assessment

[What we're protecting and why it matters]

### Adversary Profiles

#### Adversary 1: [Name/Role]
- **Motivation:** [Why they attack]
- **Capability:** [What they can do]
- **Access:** [What they start with]

#### Adversary 2: [Name/Role]
- **Motivation:** [Why they attack]
- **Capability:** [What they can do]
- **Access:** [What they start with]

### Attack Vectors (Ranked)

| # | Vector | Adversary | Likelihood | Impact | Risk Score |
|---|--------|-----------|-----------|--------|------------|
| 1 | [Specific attack] | [Who] | High/Med/Low | High/Med/Low | [L x I] |
| 2 | [Specific attack] | [Who] | High/Med/Low | High/Med/Low | [L x I] |
| 3 | [Specific attack] | [Who] | High/Med/Low | High/Med/Low | [L x I] |

### Perverse Incentives

| Incentive Created | Unintended Behavior | Severity |
|-------------------|-------------------|----------|
| [What the system rewards] | [How it gets gamed] | High/Med/Low |

### Recommended Defenses

| Attack Vector | Defense | Effort | Priority |
|--------------|---------|--------|----------|
| #1 | [Specific countermeasure] | Low/Med/High | Immediate/Next sprint/Backlog |
| #2 | [Specific countermeasure] | Low/Med/High | Immediate/Next sprint/Backlog |
| #3 | [Specific countermeasure] | Low/Med/High | Immediate/Next sprint/Backlog |
```

---

## Reference: Socratic Questioning

# Socratic Questioning

Structured question frameworks for exposing assumptions and deepening understanding.

## Core Principle

Socratic questioning does not argue. It asks. The goal is to help the user discover gaps in their own reasoning by surfacing what they have not examined. Every question should create a moment of "I hadn't thought about that."

## Question Categories

### 1. Definitional Questions

Challenge vague or overloaded terms.

| Pattern | Example |
|---------|---------|
| "When you say X, what specifically do you mean?" | "When you say 'scalable,' do you mean 10x users or 1000x?" |
| "How would you define X to someone unfamiliar?" | "How would you explain 'real-time' to a non-engineer?" |
| "Are there cases where X means something different?" | "Does 'fast' mean the same thing for API response and batch job?" |

### 2. Evidential Questions

Probe the basis for beliefs.

| Pattern | Example |
|---------|---------|
| "What evidence supports this?" | "What data shows users actually want this feature?" |
| "How do you know X is true?" | "How do you know the current system can't handle the load?" |
| "What would change your mind?" | "What metric would convince you this approach is wrong?" |
| "Is this based on data or intuition?" | "Is the 'users hate the current flow' claim from research or assumption?" |

### 3. Logical Questions

Test the reasoning chain.

| Pattern | Example |
|---------|---------|
| "Does X necessarily lead to Y?" | "Does adding caching necessarily improve user experience?" |
| "What assumptions connect X to Y?" | "What has to be true for microservices to improve velocity?" |
| "Could the opposite also be true?" | "Could a monolith actually ship faster in this case?" |
| "Are you conflating correlation with causation?" | "Did the refactor cause the improvement, or was it the new hire?" |

### 4. Perspective-Shifting Questions

Force consideration of other viewpoints.

| Pattern | Example |
|---------|---------|
| "How would [stakeholder] see this?" | "How would the on-call engineer feel about this architecture?" |
| "What would a skeptic say?" | "What would a senior engineer who prefers simplicity say?" |
| "What does this look like in 2 years?" | "Will this abstraction still make sense when the team doubles?" |
| "Who loses if this succeeds?" | "If we adopt this vendor, what capability do we give up?" |

### 5. Consequential Questions

Trace the implications.

| Pattern | Example |
|---------|---------|
| "What happens next?" | "After we migrate, what's the first thing that breaks?" |
| "What's the second-order effect?" | "If we hire contractors to speed up, what happens to team knowledge?" |
| "What's the cost of being wrong?" | "If this assumption is wrong, how bad is the recovery?" |
| "What becomes harder later?" | "What future feature becomes harder if we choose this schema?" |

## Assumption Detection Signals

Watch for language that hides assumptions.

| Signal Phrase | Hidden Assumption |
|---------------|-------------------|
| "Obviously..." | The speaker hasn't questioned this |
| "Everyone knows..." | Consensus hasn't been verified |
| "It just makes sense..." | The reasoning chain hasn't been articulated |
| "We always..." | Historical pattern assumed to be optimal |
| "There's no other way..." | Alternatives haven't been explored |
| "It's simple..." | Complexity has been underestimated |
| "Users want..." | User research may be absent or stale |
| "The standard approach is..." | Convention hasn't been validated for this context |

## Domain-Adapted Question Banks

### Technical Decisions

- What are you optimizing for? Are you sure that's the right dimension?
- What's the simplest version that tests the core assumption?
- What constraint are you treating as fixed that might actually be flexible?
- How would you build this if you had to ship in one week?
- What's the most expensive thing to change later?

### Business Decisions

- Who is the customer for this decision? Are you sure?
- What would make this a bad investment in hindsight?
- How does this compare to doing nothing?
- What's the opportunity cost of this choice?
- If a competitor made the opposite choice, would you be worried?

### Strategic Decisions

- What has to be true for this strategy to work?
- Which of those assumptions are you least confident about?
- What's the fastest way to test the riskiest assumption?
- How will you know if this is failing before it's too late?
- What's the exit strategy if this doesn't work?

## Output Template

```markdown
## Assumption Inventory

| # | Assumption | Type | Confidence |
|---|-----------|------|------------|
| 1 | [Stated or hidden assumption] | Stated / Unstated | High / Medium / Low |

## Probing Questions

### [Theme 1: e.g., "User Behavior"]
1. [Question targeting assumption #X]
2. [Follow-up question deepening the probe]

### [Theme 2: e.g., "Technical Feasibility"]
1. [Question targeting assumption #Y]
2. [Follow-up question]

### [Theme 3: e.g., "Business Viability"]
1. [Question targeting assumption #Z]
2. [Follow-up question]

## Suggested Experiments

| Assumption | Experiment | Effort | Signal |
|-----------|-----------|--------|--------|
| [Riskiest assumption] | [How to test it] | Low/Med/High | [What result means] |
```
