---
title: "Voice Capture"
description: "This skill should be used when extracting voice profiles from sample text, creating voice documentation, or matching a specific writing style. It applies when users provide sample text and want to capture the voice for future use."
category: "writing"
source: "community"
author: "Community"
tags: ["voice", "capture"]
date: 2026-03-20
---

# Voice Capture Skill

Extract and encode writing voice from sample text into reusable voice profiles. This skill transforms examples of writing you like into documented patterns that can guide future writing.

## When to Use This Skill

This skill applies when:
- A user provides sample text and asks "write like this"
- Creating a voice profile from existing content
- Documenting a brand voice for consistency
- Capturing an author's style for future reference
- Analyzing differences between two writing styles

## Core Philosophy

> Voice isn't just word choice. It's sentence rhythm, paragraph structure, emotional register, and a thousand small decisions that create a distinctive sound.

This skill captures those decisions systematically so they can be applied to new content.

## Voice Profile Structure

A complete voice profile has three layers. See [voice-profile-template.yaml](./assets/voice-profile-template.yaml) for the full template.

### Layer 1: Immutable Traits

Core characteristics that define the voice:

```yaml
traits:
  - direct           # vs. indirect, circumspect
  - conversational   # vs. formal, academic
  - technically-informed  # level of assumed expertise

register: informal   # formal / semiformal / informal

prohibited:
  - "synergy"
  - passive voice in openings
  - exclamation marks (except in quotes)
```

### Layer 2: Channel Guidance

How the voice adapts by medium:

```yaml
channels:
  blog:
    length: "1000-2000 words"
    personality: "full"
    storytelling: "encouraged"

  newsletter:
    length: "300-500 words"
    personality: "high - direct address okay"
    storytelling: "personal anecdotes"

  social:
    length: "280 chars or thread"
    personality: "punchy, hooks required"
    storytelling: "minimal - punchlines only"

  documentation:
    length: "as needed"
    personality: "minimal"
    storytelling: "none - clarity first"
```

### Layer 3: Example Library

Exemplars that demonstrate the voice:

```yaml
exemplars:
  - path: "samples/great-opening.md"
    why: "Concrete example first, theory second"
    demonstrates: ["hook", "pacing"]

  - path: "samples/transition.md"
    why: "Invisible transition technique"
    demonstrates: ["flow", "structure"]

  - path: "samples/closing.md"
    why: "Strong CTA without being salesy"
    demonstrates: ["conclusion", "call-to-action"]
```

## Extraction Process

### Step 1: Collect Samples

Minimum: 3 samples (ideally 5-10)
Total words: At least 2,000 words
Variety: Different topics, same author/brand

### Step 2: Analyze Dimensions

Reference [analysis-dimensions.md](./references/analysis-dimensions.md) for the full framework.

#### Vocabulary Analysis
- **Complexity**: Simple ↔ Complex
- **Formality**: Casual ↔ Formal
- **Jargon**: Technical ↔ Accessible
- **Signature words**: Frequently used phrases

#### Sentence Analysis
- **Length**: Average words per sentence
- **Variety**: Standard deviation of sentence length
- **Structure**: Simple vs. compound vs. complex ratio
- **Fragments**: Used for emphasis? How often?

#### Paragraph Analysis
- **Length**: Average sentences per paragraph
- **Opening patterns**: How do paragraphs typically start?
- **Closing patterns**: How do paragraphs typically end?

#### Rhythm Analysis
- **Pacing**: Quick (short sentences) vs. measured (longer)
- **Punctuation style**: Dashes, semicolons, parentheses
- **White space**: Dense vs. airy paragraphs

#### Emotional Analysis
- **Tone**: Optimistic, skeptical, neutral, passionate
- **Distance**: Intimate (I, you) vs. distant (one, they)
- **Stakes**: High urgency vs. calm reflection

### Step 3: Document Patterns

For each dimension, document:
1. The observed pattern
2. A concrete example
3. A counter-example (what this voice avoids)

### Step 4: Create Profile

Use [extraction-templates.md](./references/extraction-templates.md) to structure your findings.

Output: `.claude/voice-profiles/[name].yaml`

## Using Voice Profiles

### In Writing Commands

```yaml
# In /writing:draft
style:
  voice_profile: "kieran-blog"
  # OR
  voice_profile: ".claude/voice-profiles/client-name.yaml"
```

### For Voice Guardian

The voice-guardian agent uses profiles to:
- Score voice consistency (0-100)
- Identify drift points
- Suggest specific fixes

Target score: 85+

### For New Writers

When onboarding writers to match an existing voice:
1. Share the voice profile
2. Share the exemplars
3. Run voice-guardian on their drafts

## Quick Extraction Workflow

For rapid voice capture (when you need a profile fast):

```markdown
## Quick Profile: [Name]

**Based on**: [X] samples totaling [Y] words

### Core Traits
- [Trait 1]
- [Trait 2]
- [Trait 3]

### Sentence Patterns
Average length: [X] words
Common patterns:
- [Pattern 1]
- [Pattern 2]

### Vocabulary Markers
**Signature words**: [list]
**Avoided words**: [list]

### Tone
[Brief description]

### Quick Examples
Good: "[example that nails the voice]"
Bad: "[example that would violate it]"
```

## Common Extraction Challenges

### Challenge: Too Few Samples

**Problem**: Can't identify patterns from 1-2 samples.
**Solution**: Ask for more content or analyze published work from the same source.

### Challenge: Inconsistent Source

**Problem**: The sample voice varies significantly.
**Solution**: Either document the variation (multiple profiles) or focus on the most recent/best examples.

### Challenge: Style vs. Voice

**Problem**: Confusing topic-specific style with core voice.
**Solution**: Analyze samples on different topics. What stays constant? That's the voice.

### Challenge: Unconscious Patterns

**Problem**: Author doesn't know what makes their voice distinctive.
**Solution**: Compare to other writers. What's different? That's often the key.

## Quality Checklist

A voice profile is complete when:
- [ ] All three layers are populated
- [ ] At least 3 exemplars are documented
- [ ] Prohibited patterns are explicit
- [ ] Channel variations are noted
- [ ] A test passage can be evaluated against it
- [ ] Someone unfamiliar with the voice could use it

## References

- [extraction-templates.md](./references/extraction-templates.md) - Templates for structured extraction
- [analysis-dimensions.md](./references/analysis-dimensions.md) - All dimensions to analyze
- [example-profiles.md](./references/example-profiles.md) - Sample voice profiles for reference
- [voice-profile-template.yaml](./assets/voice-profile-template.yaml) - The YAML template

---

## Reference: Analysis Dimensions

# Voice Analysis Dimensions

Complete framework for analyzing writing voice across all dimensions.

## 1. Vocabulary Dimensions

### 1.1 Complexity

| Level | Description | Indicators |
|-------|-------------|------------|
| Simple | 8th grade reading level | Short words, common vocabulary |
| Moderate | 10-12th grade | Mix of common and specialized |
| Complex | College+ | Domain expertise, advanced vocabulary |

**How to measure**: Use Flesch-Kincaid or similar readability metric.

### 1.2 Formality

| Level | Indicators |
|-------|------------|
| Casual | Contractions, slang, sentence fragments |
| Conversational | Contractions, no slang, complete sentences |
| Professional | Minimal contractions, industry terms |
| Formal | No contractions, third person, passive voice acceptable |

### 1.3 Technical Density

- **None**: No jargon, fully accessible
- **Light**: Occasional terms, defined or obvious
- **Moderate**: Regular technical vocabulary, assumes baseline
- **Heavy**: Dense specialized language, expert audience

### 1.4 Signature Vocabulary

Look for:
- Words used 3+ times across samples
- Unusual word choices (not the obvious word)
- Branded terms or coined phrases
- Consistent metaphor families

## 2. Sentence Dimensions

### 2.1 Length Metrics

| Metric | Calculation |
|--------|-------------|
| Average length | Total words / total sentences |
| Shortest sentence | Minimum (for emphasis use) |
| Longest sentence | Maximum (complexity tolerance) |
| Variance | How much length varies |

**Typical ranges**:
- Punchy: 8-12 words average
- Balanced: 15-20 words average
- Complex: 25+ words average

### 2.2 Structure Types

| Type | Pattern | Example |
|------|---------|---------|
| Simple | Subject + Verb | "The code runs." |
| Compound | S+V and/or S+V | "The code runs, and tests pass." |
| Complex | Main clause + dependent | "When you run the code, tests pass." |
| Compound-Complex | Multiple clauses | Full combination |

### 2.3 Opening Patterns

Count percentage of sentences starting with:
- Subject (proper start): "The team decided..."
- Question: "What if we..."
- Transition: "However, the approach..."
- Participle: "Running the tests..."
- Subordinate clause: "When the tests passed..."
- "I" or "We": First person leads

### 2.4 Fragment Usage

| Level | Description |
|-------|-------------|
| Never | All complete sentences |
| Rare | Emphasis only, <5% |
| Occasional | Stylistic choice, 5-15% |
| Frequent | Part of voice, >15% |

## 3. Paragraph Dimensions

### 3.1 Length Patterns

- **Short**: 1-2 sentences (punchy, scannable)
- **Medium**: 3-4 sentences (standard)
- **Long**: 5+ sentences (dense, academic)

### 3.2 Structure Patterns

**Opening types**:
- Topic sentence (states paragraph purpose)
- Hook (attention-grabbing statement)
- Question (rhetorical or actual)
- Transition (from previous paragraph)

**Closing types**:
- Conclusion (wraps up the point)
- Bridge (sets up next paragraph)
- Punch line (memorable closer)
- Question (leaves reader thinking)

### 3.3 White Space

Visual density of paragraphs:
- Dense: Long paragraphs, few breaks
- Moderate: Mixed lengths
- Airy: Short paragraphs, frequent breaks, lists

## 4. Rhythm Dimensions

### 4.1 Pacing

| Type | Pattern |
|------|---------|
| Staccato | Short, punchy, rapid-fire |
| Legato | Long, flowing, connected |
| Varied | Intentional mix for effect |

### 4.2 Punctuation Profile

For each mark, note frequency:
- **Em dash**: Emphasis, interruption, asides
- **Parentheses**: Secondary info, qualification
- **Semicolon**: Related ideas, sophistication
- **Colon**: Introduction, lists, explanation
- **Ellipsis**: Trailing off, suspense
- **Exclamation**: Energy, emphasis

### 4.3 Repetition Patterns

- **Anaphora**: Repeated beginnings ("We built. We shipped. We learned.")
- **Epistrophe**: Repeated endings
- **Parallelism**: Similar structure across items
- **Rule of three**: Three beats, three examples

## 5. Emotional Dimensions

### 5.1 Tone Categories

| Tone | Indicators |
|------|------------|
| Optimistic | Positive framing, future focus, solutions |
| Skeptical | Questions assumptions, critical analysis |
| Neutral | Balanced, informational, objective |
| Passionate | Strong language, personal investment |
| Urgent | Time pressure, calls to action |
| Calm | Measured, reflective, patient |

### 5.2 Distance Scale

| Level | Indicators |
|-------|------------|
| Intimate | "I", "you", personal stories, vulnerability |
| Conversational | Occasional "you", relatable examples |
| Professional | "We", company voice, limited personal |
| Academic | Third person, citations, objectivity |
| Distant | Passive voice, "one", impersonal |

### 5.3 Stakes Level

How urgent does the writing feel?

- **Low**: Informational, "here's how it works"
- **Medium**: Opinion, "this matters because"
- **High**: Urgent, "you need to act now"

## 6. Structural Dimensions

### 6.1 Organization Patterns

- **Linear**: Point A to Point B to Point C
- **Problem-Solution**: State problem, resolve it
- **Compare-Contrast**: This vs. that
- **Chronological**: Timeline or narrative
- **Spatial**: By location or component
- **Priority**: Most to least important

### 6.2 Argument Style

- **Inductive**: Examples first, principle after
- **Deductive**: Principle first, examples after
- **Dialectical**: Thesis, antithesis, synthesis

### 6.3 Evidence Preferences

- Stories and anecdotes
- Data and statistics
- Expert quotes
- Logical reasoning
- Personal experience
- Historical examples

## Analysis Checklist

For complete voice extraction, analyze:

- [ ] Vocabulary: complexity, formality, technical density, signatures
- [ ] Sentences: length, structure, openings, fragments
- [ ] Paragraphs: length, structure, white space
- [ ] Rhythm: pacing, punctuation, repetition
- [ ] Emotion: tone, distance, stakes
- [ ] Structure: organization, argument style, evidence

## Quick Analysis Framework

For rapid analysis, focus on:

1. **Average sentence length** (objective, measurable)
2. **Formality level** (contractions, word choice)
3. **Primary tone** (one word descriptor)
4. **Signature vocabulary** (3-5 distinctive words)
5. **Paragraph length** (short, medium, long)

---

## Reference: Example Profiles

# Example Voice Profiles

Sample voice profiles demonstrating the format.

## Example 1: DHH (David Heinemeier Hansson)

```yaml
name: dhh-blog

traits:
  - direct
  - opinionated
  - contrarian

register: informal

prohibited:
  - hedge words (seems, might, perhaps)
  - passive voice (except for emphasis)
  - corporate buzzwords (synergy, leverage, optimize)
  - exclamation marks (unless ironic)
  - "I think" or "in my opinion" (implied)

vocabulary:
  signature_words:
    - "bullshit"
    - "vanilla"
    - "majestic"
    - "heresy"
  formality: casual-professional
  complexity: moderate
  contractions: always

sentences:
  average_length: 12
  fragment_usage: frequent
  opening_preference: subject-verb

paragraphs:
  average_length: 2-3
  white_space: airy
  structure: claim-evidence

rhythm:
  pacing: punchy
  rule_of_three: frequent
  em_dash: occasional
  semicolon: rare

tone:
  primary: confident
  secondary: provocative
  stakes: medium-high
  distance: conversational

channels:
  blog:
    length: "500-1500 words"
    personality: "full"
    controversy: "welcomed"
  twitter:
    length: "single tweet preferred"
    personality: "concentrated"
    controversy: "frequent"

exemplars:
  - text: "Most meetings are a waste of time. Not some. Most."
    demonstrates: ["short sentences", "contrarian", "repetition"]
  - text: "We don't do free. We don't do enterprise. $99. Done."
    demonstrates: ["fragments", "rule of three", "directness"]
```

## Example 2: Joel Spolsky

```yaml
name: joel-on-software

traits:
  - analytical
  - humorous
  - storytelling

register: conversational

prohibited:
  - jargon without explanation
  - abstract theory without concrete examples
  - formal academic tone
  - passive voice (mostly)

vocabulary:
  signature_words:
    - "leaky abstractions"
    - "Joel Test"
    - "shlemiel the painter"
  formality: casual-technical
  complexity: moderate-high (explained)
  contractions: yes

sentences:
  average_length: 18
  fragment_usage: occasional
  opening_preference: varied

paragraphs:
  average_length: 3-4
  white_space: moderate
  structure: story-point-lesson

rhythm:
  pacing: varied
  parenthetical_asides: frequent
  em_dash: occasional
  footnotes: rare

tone:
  primary: explanatory
  secondary: witty
  stakes: medium
  distance: friendly-expert

channels:
  blog:
    length: "1500-3000 words"
    personality: "full, storytelling"
    humor: "embedded throughout"
  documentation:
    length: "as needed"
    personality: "reduced but present"
    humor: "occasional"

exemplars:
  - text: "The Joel Test is a quick measure of the quality of a software team. The higher the score, the better the team. No, it's not perfect, but it's fast and pretty good."
    demonstrates: ["conversational", "practical", "self-aware"]
  - text: "Shlemiel gets a job as a street painter, painting the dotted lines down the middle of the road..."
    demonstrates: ["storytelling", "physical analogy", "setup-punchline"]
```

## Example 3: Paul Graham

```yaml
name: paul-graham-essays

traits:
  - exploratory
  - philosophical
  - building-arguments

register: semiformal

prohibited:
  - starting with conclusions
  - excessive qualification
  - jargon without setup

vocabulary:
  signature_words:
    - "ramen profitable"
    - "do things that don't scale"
    - "frighteningly ambitious"
  formality: intellectual-accessible
  complexity: high (earned)
  contractions: some

sentences:
  average_length: 22
  fragment_usage: rare
  opening_preference: statement

paragraphs:
  average_length: 4-5
  white_space: moderate-dense
  structure: logical-progression

rhythm:
  pacing: measured
  nested_clauses: accepted
  em_dash: frequent
  semicolon: occasional

tone:
  primary: thoughtful
  secondary: counterintuitive
  stakes: medium
  distance: intellectual-peer

channels:
  essay:
    length: "2000-4000 words"
    personality: "reflective"
    structure: "meandering toward insight"

exemplars:
  - text: "Don't just not be evil. Be good."
    demonstrates: ["moral clarity", "concision", "building on negation"]
  - text: "The way to get startup ideas is not to try to think of startup ideas."
    demonstrates: ["counterintuitive", "paradox setup", "memorable"]
```

## Example 4: Corporate Neutral (Anti-Example)

```yaml
name: corporate-neutral
description: "What NOT to do - included for contrast"

traits:
  - hedged
  - safe
  - buzzword-laden

register: formal

vocabulary:
  signature_words:
    - "leverage"
    - "synergy"
    - "value proposition"
    - "best-in-class"
  formality: corporate-formal
  complexity: low-disguised-as-high
  contractions: never

sentences:
  average_length: 28
  fragment_usage: never
  opening_preference: "There are/It is"

paragraphs:
  average_length: 6+
  white_space: dense
  structure: circular

tone:
  primary: safe
  secondary: defensive
  stakes: artificially high
  distance: distant

problems:
  - "Says nothing memorable"
  - "Could be any company"
  - "No human voice"
  - "Exhausting to read"

exemplar_bad:
  - text: "We are excited to announce a strategic initiative designed to enhance our value proposition through synergistic partnerships that will drive innovation across our ecosystem."
    problems: ["no meaning", "all buzzwords", "passive framing"]
```

## Using These Profiles

### For Matching Voice

Compare your writing to the exemplars:
1. Read the exemplar aloud
2. Read your writing aloud
3. Do they sound like the same person?

### For Voice Guardian Scoring

When scoring voice match:
- Check against prohibited words
- Compare sentence length
- Verify tone matches
- Look for signature vocabulary

### For Learning Style

Study the difference between profiles:
- DHH: Short, punchy, contrarian
- Joel: Story-driven, explanatory
- Paul Graham: Exploratory, builds arguments
- Corporate: Avoid at all costs

---

## Reference: Extraction Templates

# Voice Extraction Templates

Structured templates for capturing voice systematically.

## Full Extraction Template

Use this for comprehensive voice profiles.

```markdown
# Voice Extraction: [Name/Brand]

## Source Material
- Sample 1: [title/description] ([X] words)
- Sample 2: [title/description] ([X] words)
- Sample 3: [title/description] ([X] words)
Total: [X] words across [X] samples

## Vocabulary Analysis

### Complexity Score
[ ] Simple (8th grade reading level)
[X] Moderate (10-12th grade)
[ ] Complex (college+)

Evidence: "[example sentence]"

### Formality Score
[ ] Casual (contractions, slang okay)
[X] Conversational (contractions, no slang)
[ ] Professional (minimal contractions)
[ ] Formal (no contractions)

Evidence: "[example]"

### Signature Words/Phrases
Words used frequently:
- "[word]" - appears X times
- "[phrase]" - appears X times

### Prohibited Words
Words never used:
- "[word]" - alternative used instead: "[alternative]"
- "[word]" - never appears despite topic relevance

## Sentence Analysis

### Average Length
[X] words (calculated from samples)

### Length Distribution
Shortest sentences: [X] words (for emphasis)
Longest sentences: [X] words (for explanation)
Standard deviation: [X]

### Structure Patterns

**Dominant pattern**: [Simple / Compound / Complex]

**Fragment usage**:
[ ] Never
[ ] Rarely (emphasis only)
[X] Sometimes
[ ] Frequently

Example fragment: "[example]"

### Opening Patterns
Sentences typically start with:
- Subject-verb: [%]
- Question: [%]
- Transition word: [%]
- "-ing" phrase: [%]

## Paragraph Analysis

### Average Length
[X] sentences per paragraph

### Opening Patterns
How paragraphs typically begin:
- Hook/claim: [%]
- Question: [%]
- Continuation: [%]
- Quote: [%]

### Closing Patterns
How paragraphs typically end:
- Conclusion/summary: [%]
- Transition to next: [%]
- Question: [%]
- Punch line: [%]

## Rhythm Analysis

### Pacing
[ ] Quick (short sentences dominate)
[X] Varied (intentional mix)
[ ] Measured (longer sentences dominate)

### Punctuation Preferences
- Em dashes: [Frequent / Occasional / Rare / Never]
- Parentheses: [Frequent / Occasional / Rare / Never]
- Semicolons: [Frequent / Occasional / Rare / Never]
- Exclamation marks: [Frequent / Occasional / Rare / Never]

### White Space
[ ] Dense (long paragraphs)
[X] Moderate (mixed)
[ ] Airy (short paragraphs, frequent breaks)

## Emotional Analysis

### Tone
Primary: [optimistic / skeptical / neutral / passionate / urgent / calm]
Secondary: [additional descriptor]

### Emotional Distance
[X] Intimate ("I", "you", direct address)
[ ] Conversational (occasional "you")
[ ] Professional (rare personal pronouns)
[ ] Distant ("one", passive constructions)

### Stakes Level
[ ] Low (informational, neutral)
[X] Medium (opinion, mild urgency)
[ ] High (urgent, emotional, calls to action)

## Extracted Patterns

### Pattern 1: [Name]
**What**: [Description of the pattern]
**Example**: "[Quote from samples]"
**When to use**: [Context]

### Pattern 2: [Name]
**What**: [Description]
**Example**: "[Quote]"
**When to use**: [Context]

[Continue for major patterns...]

## Anti-Patterns

### What This Voice Avoids
1. [Anti-pattern]: "[Example of what NOT to do]"
2. [Anti-pattern]: "[Example]"
3. [Anti-pattern]: "[Example]"

## Exemplar Passages

### Best Example of Voice
> "[Passage that perfectly captures the voice]"

Why this works: [Explanation]

### Good Contrast Example
> "[Passage that would NOT fit this voice]"

Why this doesn't work: [Explanation]

## Final Profile Summary

**In one sentence**: This voice is [X], [Y], and [Z].

**Key identifiers**: If you see [marker], it's probably this voice.

**Biggest risk**: Writers often drift toward [common mistake].
```

## Quick Extraction Template

Use for rapid voice capture when time is limited.

```markdown
# Quick Voice Profile: [Name]

**Based on**: [X] samples, [Y] total words
**Confidence**: [High / Medium / Low]

## Core Characteristics
1. [Most distinctive trait]
2. [Second trait]
3. [Third trait]

## Sentence Style
- Average length: [X] words
- Fragments: [Yes/No]
- Structure: [Simple / Varied / Complex]

## Vocabulary
**Signature words**: [word], [word], [word]
**Avoided words**: [word], [word], [word]
**Formality**: [Casual / Professional / Formal]

## Tone
[One sentence description]

## Quick Test
This voice would say: "[example]"
This voice would NOT say: "[counter-example]"
```

## Comparison Template

Use when analyzing differences between two voices.

```markdown
# Voice Comparison: [Voice A] vs. [Voice B]

## Overview
| Dimension | Voice A | Voice B |
|-----------|---------|---------|
| Formality | [X] | [X] |
| Sentence Length | [X] words | [X] words |
| Tone | [X] | [X] |
| Complexity | [X] | [X] |

## Key Differences

### Difference 1: [Dimension]
**Voice A**: [Description with example]
**Voice B**: [Description with example]
**Implication**: [What this means for writing]

### Difference 2: [Dimension]
[Continue pattern...]

## Shared Traits
Both voices share:
1. [Shared trait]
2. [Shared trait]

## When to Use Each
**Use Voice A when**: [Context]
**Use Voice B when**: [Context]
```
