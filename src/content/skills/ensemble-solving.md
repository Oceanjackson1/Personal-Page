---
title: "Ensemble Solving"
description: "Generate multiple diverse solutions in parallel and select the best. Use for architecture decisions, code generation with multiple valid approaches, or creative tasks where exploring alternatives improves quality."
category: "development"
source: "community"
author: "Community"
tags: ["ensemble", "solving"]
date: 2026-03-20
---

# Ensemble Problem Solving

Generate multiple solutions in parallel by spawning 3 subagents with different approaches, then evaluate and select the best result.

## When to Use

**Activation phrases:**
- "Give me options for..."
- "What's the best way to..."
- "Explore different approaches..."
- "I want to see alternatives..."
- "Compare approaches for..."
- "Which approach should I use..."

**Good candidates:**
- Architecture decisions with trade-offs
- Code generation with multiple valid implementations
- API design with different philosophies
- Naming, branding, documentation style
- Refactoring strategies
- Algorithm selection

**Skip ensemble for:**
- Simple lookups or syntax questions
- Single-cause bug fixes
- File operations, git commands
- Deterministic configuration changes
- Tasks with one obvious solution

## What It Does

1. **Analyzes the task** to determine if ensemble approach is valuable
2. **Generates 3 distinct prompts** using appropriate diversification strategy
3. **Spawns 3 parallel subagents** to develop solutions independently
4. **Evaluates all solutions** using weighted criteria
5. **Returns the best solution** with explanation and alternatives summary

## Approach

### Step 1: Classify Task Type

Determine which category fits:
- **Code Generation**: Functions, classes, APIs, algorithms
- **Architecture/Design**: System design, data models, patterns
- **Creative**: Writing, naming, documentation

### Step 2: Invoke Ensemble Orchestrator

```
Task tool with:
- subagent_type: 'ensemble-orchestrator'
- description: 'Generate and evaluate 3 parallel solutions'
- prompt: [User's original task with full context]
```

The orchestrator handles:
- Prompt diversification
- Parallel execution
- Solution evaluation
- Winner selection

### Step 3: Present Result

The orchestrator returns:
- The winning solution (in full)
- Evaluation scores for all 3 approaches
- Why the winner was selected
- When alternatives might be preferred

## Diversification Strategies

**For Code (Constraint Variation):**
| Approach | Focus |
|----------|-------|
| Simplicity | Minimal code, maximum readability |
| Performance | Efficient, optimized |
| Extensibility | Clean abstractions, easy to extend |

**For Architecture (Approach Variation):**
| Approach | Focus |
|----------|-------|
| Top-down | Requirements → Interfaces → Implementation |
| Bottom-up | Primitives → Composition → Structure |
| Lateral | Analogies from other domains |

**For Creative (Persona Variation):**
| Approach | Focus |
|----------|-------|
| Expert | Technical precision, authoritative |
| Pragmatic | Ship-focused, practical |
| Innovative | Creative, unconventional |

## Evaluation Rubric

| Criterion | Base Weight | Description |
|-----------|-------------|-------------|
| Correctness | 30% | Solves the problem correctly |
| Completeness | 20% | Addresses all requirements |
| Quality | 20% | How well-crafted |
| Clarity | 15% | How understandable |
| Elegance | 15% | How simple/beautiful |

Weights adjust based on task type.

## Example

**User:** "What's the best way to implement a rate limiter?"

**Skill:**
1. Classifies as Code Generation
2. Invokes ensemble-orchestrator
3. Three approaches generated:
   - Simple: Token bucket with in-memory counter
   - Performance: Sliding window with atomic operations
   - Extensible: Strategy pattern with pluggable backends
4. Evaluation selects extensible approach (score 8.4)
5. Returns full implementation with explanation

**Output:**
```
## Selected Solution

[Full rate limiter implementation with strategy pattern]

## Why This Solution Won

The extensible approach scored highest (8.4) because it provides
a clean abstraction that works for both simple use cases and
complex distributed scenarios. The strategy pattern allows
swapping Redis/Memcached backends without code changes.

## Alternatives

- **Simple approach**: Best if you just need basic in-memory
  limiting and will never scale beyond one process.

- **Performance approach**: Best for high-throughput scenarios
  where every microsecond matters.
```

## Success Criteria

- 3 genuinely different solutions generated
- Clear evaluation rationale provided
- Winner selected with confidence
- Alternatives summarized with use cases
- User understands trade-offs

## Token Cost

~4x overhead vs single attempt. Worth it for:
- High-stakes architecture decisions
- Creative work where first attempt rarely optimal
- Learning scenarios where seeing alternatives is valuable
- Code that will be maintained long-term

## Integration

- **feature-planning**: Can ensemble architecture decisions
- **code-auditor**: Can ensemble analysis perspectives
- **plan-implementer**: Executes the winning approach

---

## Reference: Diversification Strategies

# Prompt Diversification Strategies

This reference provides detailed guidance on generating diverse prompts that lead to genuinely different solutions.

## Strategy Selection Matrix

| Task Type | Primary Strategy | Secondary Option |
|-----------|-----------------|------------------|
| Function/Class implementation | Constraint Variation | Persona |
| API design | Approach Variation | Constraint |
| System architecture | Approach Variation | Persona |
| Algorithm selection | Constraint Variation | Approach |
| Documentation writing | Persona Variation | Constraint |
| Naming/Branding | Persona Variation | Approach |
| Refactoring | Constraint Variation | Approach |
| Test strategy | Approach Variation | Constraint |

## Constraint Variation (Technical Tasks)

Use when: Optimizing for different quality attributes.

### Template

```markdown
## Task
[Original user request]

## Optimization Focus: [SIMPLICITY / PERFORMANCE / EXTENSIBILITY]

## Guidelines
[Specific guidelines for this focus]

## Constraints
[What to prioritize and de-prioritize]

## Output
[Expected deliverable format]
```

### Simplicity Focus

**Guidelines:**
- Minimize lines of code
- Use standard library over external dependencies
- Prefer obvious implementations over clever ones
- Readable by any developer in 30 seconds

**Constraints:**
- No premature optimization
- No unnecessary abstractions
- Inline where it aids readability
- Comments only where truly needed

### Performance Focus

**Guidelines:**
- Minimize time complexity
- Reduce memory allocations
- Use efficient data structures
- Consider cache locality

**Constraints:**
- Pre-compute where possible
- Use early exits
- Avoid unnecessary copies
- Profile-guided decisions

### Extensibility Focus

**Guidelines:**
- Clean separation of concerns
- Dependency injection where appropriate
- Interface-driven design
- Easy to add new variants

**Constraints:**
- SOLID principles
- Don't repeat yourself
- Open for extension, closed for modification
- Document extension points

## Approach Variation (Architecture Tasks)

Use when: Multiple valid design philosophies exist.

### Template

```markdown
## Task
[Original user request]

## Design Approach: [TOP-DOWN / BOTTOM-UP / LATERAL]

## Methodology
[How to approach the problem]

## Starting Point
[Where to begin the design]

## Output
[Expected deliverable format]
```

### Top-Down Approach

**Methodology:**
- Start from user requirements and business goals
- Define high-level interfaces first
- Decompose into components
- Implementation details emerge from contracts

**Starting Point:**
- What does the user need to accomplish?
- What are the main use cases?
- What data flows through the system?

### Bottom-Up Approach

**Methodology:**
- Start from primitives and building blocks
- Compose small, well-tested pieces
- Let structure emerge from usage patterns
- Refactor as patterns become clear

**Starting Point:**
- What are the fundamental operations?
- What data types are involved?
- What existing utilities can we build on?

### Lateral Approach

**Methodology:**
- Draw analogies from other domains
- Challenge conventional patterns
- Look for proven solutions in adjacent fields
- Question "obvious" approaches

**Starting Point:**
- What similar problems exist elsewhere?
- What unconventional patterns might apply?
- What would a completely different industry do?

## Persona Variation (Creative Tasks)

Use when: Tone, style, or perspective matters.

### Template

```markdown
## Task
[Original user request]

## Persona: [EXPERT / PRAGMATIC / INNOVATIVE]

## Voice
[How to communicate]

## Priorities
[What this persona values]

## Output
[Expected deliverable format]
```

### Expert Persona

**Voice:**
- Technical and precise
- Authoritative but accessible
- Reference best practices and standards
- Use proper terminology

**Priorities:**
- Correctness over brevity
- Industry standards
- Comprehensive coverage
- Professional polish

### Pragmatic Persona

**Voice:**
- Direct and practical
- Focus on shipping
- Acknowledge trade-offs explicitly
- "Good enough" is valid

**Priorities:**
- Getting things done
- Clear ROI
- Maintainability
- Team velocity

### Innovative Persona

**Voice:**
- Creative and exploratory
- Challenge assumptions
- Embrace unconventional ideas
- Think differently

**Priorities:**
- Novel approaches
- User delight
- Breaking from convention when valuable
- Future possibilities

## Combining Strategies

For complex tasks, combine strategies:

**Example: "Design a caching system"**

| Solution | Primary | Secondary |
|----------|---------|-----------|
| 1 | Top-down | Simplicity |
| 2 | Bottom-up | Performance |
| 3 | Lateral | Extensibility |

This ensures diversity across both design approach AND optimization focus.

## Anti-Patterns

**Don't generate prompts that are:**
- Trivially different (just reworded)
- Focused on same trade-off space
- Likely to produce identical solutions
- Too vague to guide differentiation

**Do generate prompts that:**
- Target different quality attributes
- Use different reasoning approaches
- Would appeal to different stakeholders
- Explore different parts of solution space

---

## Reference: Evaluation Rubrics

# Evaluation Rubrics

Detailed scoring criteria for evaluating ensemble solutions.

## Base Rubric

| Criterion | Weight | Score 9-10 | Score 7-8 | Score 5-6 | Score 3-4 | Score 1-2 |
|-----------|--------|------------|-----------|-----------|-----------|-----------|
| **Correctness** | 30% | Flawless, handles all cases | Works correctly, minor edge cases | Mostly correct, some issues | Significant bugs | Fundamentally broken |
| **Completeness** | 20% | All requirements, extras | All requirements met | Most requirements | Missing key features | Incomplete |
| **Quality** | 20% | Production-ready, polished | High quality, minor polish | Acceptable, needs work | Rough, needs rework | Unusable |
| **Clarity** | 15% | Crystal clear, self-documenting | Clear, easy to follow | Understandable with effort | Confusing | Incomprehensible |
| **Elegance** | 15% | Beautiful, minimal | Clean and simple | Adequate | Over-complicated | Mess |

## Task-Specific Adjustments

### Code Generation Rubric

| Criterion | Adjusted Weight |
|-----------|-----------------|
| Correctness | 35% |
| Completeness | 20% |
| Quality | 15% |
| Clarity | 10% |
| Elegance | 10% |
| **Testability** | 10% |

**Testability scoring:**
- 9-10: Easy to test, clear inputs/outputs, no side effects
- 7-8: Testable with minor setup
- 5-6: Testable but requires mocking/stubs
- 3-4: Difficult to test in isolation
- 1-2: Untestable without major refactoring

### Architecture/Design Rubric

| Criterion | Adjusted Weight |
|-----------|-----------------|
| Correctness | 25% |
| Completeness | 25% |
| Quality | 15% |
| Clarity | 10% |
| Elegance | 15% |
| **Flexibility** | 10% |

**Flexibility scoring:**
- 9-10: Easily adapts to changing requirements
- 7-8: Can accommodate most changes
- 5-6: Some flexibility, some rigidity
- 3-4: Requires significant rework for changes
- 1-2: Locked-in, impossible to modify

### Creative Tasks Rubric

| Criterion | Adjusted Weight |
|-----------|-----------------|
| Correctness | 20% |
| Completeness | 20% |
| Quality | 15% |
| Clarity | 10% |
| Elegance | 25% |
| **Originality** | 10% |

**Originality scoring:**
- 9-10: Fresh perspective, memorable
- 7-8: Interesting take, stands out
- 5-6: Competent but conventional
- 3-4: Generic, forgettable
- 1-2: Cliched, uninspired

## Evaluation Process

### Step 1: Score Each Solution

For each criterion, assess the solution on a 1-10 scale:

```
Solution 1: [Approach Name]
- Correctness: X/10
- Completeness: X/10
- Quality: X/10
- Clarity: X/10
- Elegance: X/10
- [Task-specific]: X/10
```

### Step 2: Calculate Weighted Scores

```
Total = Sum(score × weight) for each criterion
```

Example calculation (Code Generation):
```
Correctness: 8 × 0.35 = 2.80
Completeness: 7 × 0.20 = 1.40
Quality: 8 × 0.15 = 1.20
Clarity: 9 × 0.10 = 0.90
Elegance: 7 × 0.10 = 0.70
Testability: 8 × 0.10 = 0.80
Total: 7.80
```

### Step 3: Compare and Select

1. Identify highest scoring solution
2. Check margin of victory:
   - > 0.5 points: Clear winner
   - 0.2-0.5 points: Winner with caveats
   - < 0.2 points: Tie, consider synthesis

### Step 4: Consider Synthesis

If solutions are close, check if combining elements improves result:
- Can we take the core from Solution A and the error handling from Solution B?
- Does Solution C have a unique insight we can incorporate?

Only synthesize if the combination is clearly better than any individual solution.

## Scoring Calibration

### What "Correctness" Means By Task Type

**Code:**
- Compiles/runs without errors
- Produces expected output
- Handles edge cases
- No security vulnerabilities

**Architecture:**
- Meets functional requirements
- Satisfies non-functional requirements
- Components interact correctly
- Data flows as expected

**Creative:**
- Addresses the brief
- Appropriate for audience
- Achieves intended effect
- Factually accurate (if applicable)

### What "Elegance" Means By Task Type

**Code:**
- Minimal lines for the job
- Clear flow, no convoluted logic
- Good abstractions (not too many, not too few)
- Idiomatic for the language

**Architecture:**
- Simple components, clear responsibilities
- Minimal coupling between parts
- Obvious how pieces fit together
- No unnecessary complexity

**Creative:**
- Concise yet complete
- Well-structured
- Flows naturally
- Aesthetically pleasing

## Edge Cases

### When to Override Scores

**Dealbreakers** (score 0 for entire solution):
- Security vulnerability
- Data corruption risk
- Violates explicit requirements
- Fundamentally misunderstands problem

**Bonuses** (add up to +0.5):
- Exceptional insight
- Solves adjacent problems
- Educational value
- Particularly maintainable

### Handling Ties

If two solutions are within 0.2 points:

1. **Prefer simpler** if equivalent quality
2. **Prefer more testable** if code
3. **Prefer more flexible** if architecture
4. **Prefer more original** if creative
5. **Ask user** if still tied

## Output Template

```markdown
## Evaluation Results

### Scores

| Criterion | Weight | Sol 1 | Sol 2 | Sol 3 |
|-----------|--------|-------|-------|-------|
| Correctness | 35% | 8 | 7 | 9 |
| Completeness | 20% | 7 | 8 | 8 |
| Quality | 15% | 8 | 7 | 8 |
| Clarity | 10% | 9 | 6 | 7 |
| Elegance | 10% | 7 | 5 | 8 |
| Testability | 10% | 8 | 6 | 9 |
| **Weighted Total** | | **7.80** | **6.85** | **8.35** |

### Winner: Solution 3

**Margin**: +0.55 over Solution 1 (clear winner)

**Key differentiators**:
- Higher correctness (handles all edge cases)
- Better testability (pure functions, no side effects)
- More elegant abstraction

**When alternatives might be preferred**:
- Solution 1: If simplicity is paramount
- Solution 2: If you need maximum performance (benchmark first)
```
