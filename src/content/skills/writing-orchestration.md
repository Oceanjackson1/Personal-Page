---
title: "Writing Orchestration"
description: "This skill should be used when orchestrating complex writing workflows with multiple phases. It provides two-agent orchestration patterns, the two-gate content readiness assessment, 10 baseline writing strategies, 20+ situational strategies, and q..."
category: "writing"
source: "community"
author: "Community"
tags: ["writing", "orchestration"]
date: 2026-03-20
---

# Writing Orchestration Skill

A complete orchestration system for complex writing workflows. This skill provides the strategic layer that coordinates agents, applies writing strategies, and ensures content quality.

## When to Use This Skill

This skill applies when:
- Coordinating multiple writing agents
- Applying strategic writing decisions
- Assessing content readiness before drafting
- Selecting and applying writing strategies
- Running quality checkpoints on drafts

## Two-Agent Architecture

Complex writing benefits from separation of concerns:

### Orchestrator Role
- Classifies requests (information vs. content)
- Applies two-gate assessment
- Gathers research and context
- Hands off to writer when ready
- Never creates content directly

### Writer Role
- Creates drafts using strategies
- Applies style guides
- Produces variations (EXPLORATION mode)
- Refines based on feedback (REFINEMENT mode)
- Uses tools for all content (never in chat)

```
User Request
    ↓
[Orchestrator] → Classify → Research → Two-Gate Assessment
    ↓
    ├── Not Ready → Gather more material/clarity
    ↓
    └── Ready → Handoff to Writer
                    ↓
              [Writer] → Apply Strategies → Create Drafts
                    ↓
              Quality Checkpoints → Output
```

## Two-Gate Content Readiness Assessment

Before any content creation, apply this assessment:

### Gate 1: Material Sufficiency

**Question**: "Could the writer create this without inventing facts?"

| Outcome | Action |
|---------|--------|
| ✓ Pass | Have concrete examples, data, quotes available |
| ✗ Fail | Need to research/gather material first |

**Pass signals**:
- Specific examples available
- Data points confirmed
- Expert quotes accessible
- No major claims need fabrication

### Gate 2: Message Clarity

**Question**: "Do we know EXACTLY what message to convey?"

| Outcome | Action |
|---------|--------|
| ✓ Pass | Clear, specific communication goal |
| ✗ Fail | Need to interview for clarity |

**Pass signals**:
- Can state thesis in one sentence
- Know the audience specifically
- Know the desired action
- Angle is differentiated

### Decision Matrix

| Material | Message | Action |
|----------|---------|--------|
| ✓ | ✓ | Handoff to writer immediately |
| ✓ | ✗ | Interview for message clarity |
| ✗ | ✓ | Research/gather material |
| ✗ | ✗ | Interview for both |

## 10 Baseline Strategies (ALWAYS Apply)

These strategies apply to ALL content. Reference [baseline-strategies.md](./references/baseline-strategies.md) for full details.

| Strategy | Rule | Transform |
|----------|------|-----------|
| **reader-zero-context** | Add 3-6 word orienting phrases | "Stripe handles billing" → "Stripe, the payments platform, handles billing" |
| **subject-verb** | Subject + verb in first 5 words | "There were students who..." → "Students completed..." |
| **activate-verbs** | Precise verbs over is/was | "Markets were down" → "Markets plunged" |
| **watch-adverbs** | Let strong verbs carry load | "whispered quietly" → "whispered" |
| **limit-ings** | Simple tense over continuous | "are running tests" → "run tests" |
| **prefer-simple** | Everyday language unless technical | "utilizes stochastic gradient" → "learns by trial and error" |
| **cut-big-small** | Edit hierarchically | Paragraphs → Sentences → Words |
| **ban-empty-hypophora** | No self-answered questions | "The payoff? Our app..." → "Our app..." |
| **present-active-tense** | Direct, immediate language | "debuts today" → "is out now" |
| **one-idea-per-sentence** | Single clear point | Split compound thoughts |

## 20+ Situational Strategies (Select 3-4)

Choose based on content type and goals. Reference [situational-strategies.md](./references/situational-strategies.md) for full list.

### Hook & Opening
- **hook-effectiveness** - Counterintuitive or surprising openings
- **tension-builder** - Create and resolve tension
- **pattern-twist** - Set expectations, then break them

### Structure & Flow
- **order-words-emphasis** - Important words at sentence ends
- **sentence-length** - Vary for rhythm (short for impact, long for flow)
- **paragraph-length** - Mix for visual rhythm
- **ladder-abstraction** - Alternate concrete ↔ abstract

### Style & Voice
- **elegant-variation** - Avoid word repetition
- **passive-aggressive** - Strategic passive for emphasis
- **punctuation-pace** - Use punctuation for rhythm
- **key-words-space** - Give important terms breathing room

### Persuasion & Engagement
- **essential-name-filter** - Only names that add value
- **name-of-dog** - Specific details for authenticity
- **original-images** - Fresh metaphors, avoid clichés
- **show-and-tell** - Balance showing with telling

### Narrative & Story
- **narrate-scenes** - Immersive scene-setting
- **cinematic-angles** - Camera-like perspective shifts
- **dialogue-compression** - Tight, purposeful dialogue
- **reveal-traits** - Character through action

## Quality Checkpoints

Before finalizing content, verify:

### Opening Quality
- [ ] Opening is counterintuitive or surprising
- [ ] Leads with most compelling insight/moment/problem
- [ ] No chronology/setup/version numbers in opening
- [ ] Hook earns the next sentence

### Body Quality
- [ ] Body delivers on opening's promise
- [ ] Concrete sensory details present
- [ ] Each paragraph has clear purpose
- [ ] Transitions are smooth

### Strategy Compliance
- [ ] All 10 baseline strategies applied
- [ ] 3-4 situational strategies visible
- [ ] Each sentence expresses one clear idea
- [ ] Technical terminology oriented with context

### Style Guide Compliance
- [ ] Voice matches profile/guide
- [ ] No prohibited words/patterns
- [ ] Formatting rules followed

## Content Modes

### EXPLORATION Mode (New Content)

When creating new content:
1. Generate 3 different drafts
2. Vary angle, not just words
3. Apply all strategies to each
4. Let user choose direction

### REFINEMENT Mode (Editing)

When user provides feedback:
1. Work with existing draft
2. Preserve voice and structure
3. Apply specific changes requested
4. Keep what works

## Handoff Protocol

### Orchestrator → Writer

```
[Research summary if applicable - 2-3 sentences]
[Material gathered: list key assets]
[Message clarity: thesis statement]
[Style guide: name if applicable]
[Mode: EXPLORATION or REFINEMENT]
```

### Writer → Orchestrator (Rare)

Only when:
- User explicitly requests brainstorming
- New research topic needed
- Web search required
- Significant scope change

## Integration with Commands

### `/writing:plan`
Uses Orchestrator patterns:
- Request classification
- Research phase
- Two-gate assessment
- Material gathering

### `/writing:draft`
Uses Writer patterns:
- Strategy application
- Mode selection
- Draft creation
- Quality checkpoints

### `/writing:review`
Uses both:
- Orchestrator: coordinate review agents
- Writer: apply fixes

### `/writing:compound`
Captures patterns that worked for future orchestration.

## References

- [baseline-strategies.md](./references/baseline-strategies.md) - Full 10 baseline strategies with examples
- [situational-strategies.md](./references/situational-strategies.md) - 20+ situational strategies
- [quality-checkpoints.md](./references/quality-checkpoints.md) - Detailed checkpoint criteria

---

## Reference: Baseline Strategies

# 10 Baseline Writing Strategies

These strategies apply to ALL content. Apply every one, every time.

## 1. Reader Zero Context

**Rule**: Add 3-6 word orienting phrases for proper nouns and references.

**Why**: Readers drop into content without your context. Orient them immediately.

**Transform**:
| Before | After |
|--------|-------|
| "Stripe handles billing" | "Stripe, the payments platform, handles billing" |
| "We partnered with Acme" | "We partnered with Acme, a logistics startup" |
| "The RFC was approved" | "The RFC (Request for Comments), our design proposal, was approved" |

**When to skip**: Universally known entities (Google, Apple, Einstein).

## 2. Subject-Verb First

**Rule**: Subject and verb within the first 5 words.

**Why**: Readers parse subject-verb-object fastest. Front-load meaning.

**Transform**:
| Before | After |
|--------|-------|
| "There were many students who completed the course" | "Many students completed the course" |
| "It is often the case that errors occur" | "Errors occur often" |
| "What we found was that users preferred..." | "Users preferred..." |

**Pattern to avoid**: "There is/are", "It is", "What X is"

## 3. Activate Verbs

**Rule**: Precise verbs over is/was/has/have.

**Why**: Active verbs create energy. Being verbs create lethargy.

**Transform**:
| Before | After |
|--------|-------|
| "Markets were down sharply" | "Markets plunged" |
| "The team was in agreement" | "The team agreed" |
| "She was the leader of the project" | "She led the project" |
| "It was a surprise to everyone" | "It surprised everyone" |

**Find-replace targets**: was, were, is, are, has been, have been

## 4. Watch Adverbs

**Rule**: Let strong verbs carry the load. Cut redundant adverbs.

**Why**: Strong verbs don't need modification. Weak verb + adverb = lazy writing.

**Transform**:
| Before | After |
|--------|-------|
| "whispered quietly" | "whispered" |
| "ran quickly" | "sprinted" |
| "completely destroyed" | "destroyed" |
| "very angry" | "furious" |

**Keep adverbs when**: They change meaning ("she smiled coldly" vs "she smiled").

## 5. Limit -ings

**Rule**: Simple tense over continuous tense.

**Why**: Continuous tense adds words without meaning. Simple tense is direct.

**Transform**:
| Before | After |
|--------|-------|
| "We are running tests" | "We run tests" |
| "The team was building features" | "The team built features" |
| "Users are experiencing issues" | "Users experience issues" |

**Keep -ing when**: Action is genuinely ongoing or progressive.

## 6. Prefer Simple

**Rule**: Everyday language unless technical precision requires otherwise.

**Why**: Simple words are faster to read and harder to misunderstand.

**Transform**:
| Before | After |
|--------|-------|
| "utilize" | "use" |
| "terminate" | "end" |
| "facilitate" | "help" |
| "leverage" | "use" |
| "implement" | "build" or "do" |
| "optimize" | "improve" |

**Keep complex when**: Technical precision matters (legal, medical, scientific).

## 7. Cut Big to Small

**Rule**: Edit hierarchically. Paragraphs → Sentences → Words.

**Why**: Cutting a paragraph saves more than cutting 20 words.

**Process**:
1. **Paragraph level**: Does this paragraph advance the argument? If not, cut it.
2. **Sentence level**: Does this sentence add new information? If not, cut it.
3. **Word level**: Does this word do work? If not, cut it.

**The test**: Read without the cut element. If meaning survives, the cut was right.

## 8. Ban Empty Hypophora

**Rule**: No self-answered questions unless the answer surprises.

**Why**: "The payoff? Amazing results." wastes words. Just say the results.

**Transform**:
| Before | After |
|--------|-------|
| "The payoff? Our app launched." | "Our app launched." |
| "The solution? We hired more." | "We hired more." |
| "What happened next? Sales doubled." | "Sales doubled." |

**Keep when**: The answer genuinely surprises or subverts expectations.

## 9. Present Active Tense

**Rule**: Direct, immediate language. Now > then.

**Why**: Present tense creates urgency. Past tense creates distance.

**Transform**:
| Before | After |
|--------|-------|
| "The feature debuts today" | "The feature is out now" |
| "We will launch soon" | "We launch next week" |
| "The update was released" | "The update is live" |

**Keep past when**: Historical accuracy matters or sequence is important.

## 10. One Idea Per Sentence

**Rule**: Single clear point per sentence.

**Why**: Compound sentences hide ideas. Simple sentences reveal them.

**Transform**:
| Before | After |
|--------|-------|
| "The team launched the product, which was well-received, and sales increased dramatically." | "The team launched the product. Reception was strong. Sales increased dramatically." |

**The test**: Can you state the sentence's one idea in 5 words?

---

## Quick Reference Card

| # | Strategy | Question to Ask |
|---|----------|-----------------|
| 1 | Reader Zero Context | Would a stranger need more context? |
| 2 | Subject-Verb First | Are subject and verb in first 5 words? |
| 3 | Activate Verbs | Can "is/was" become an action verb? |
| 4 | Watch Adverbs | Does the adverb do work the verb can't? |
| 5 | Limit -ings | Is continuous tense necessary? |
| 6 | Prefer Simple | Is there a simpler word? |
| 7 | Cut Big to Small | Would meaning survive without this? |
| 8 | Ban Empty Hypophora | Does my question-answer add value? |
| 9 | Present Active Tense | Can I make this more immediate? |
| 10 | One Idea Per Sentence | How many ideas in this sentence? |

---

## Reference: Quality Checkpoints

# Quality Checkpoints

Complete verification before finalizing any content.

## Pre-Draft Checkpoints

Before writing, verify:

### Material Readiness
- [ ] Have concrete examples (not hypothetical)
- [ ] Have data/statistics (with sources)
- [ ] Have quotes (properly attributed)
- [ ] Have enough for claims (no fabrication needed)

### Message Readiness
- [ ] Can state thesis in one sentence
- [ ] Know specific audience
- [ ] Know desired reader action
- [ ] Have differentiated angle

## Draft Checkpoints

### Opening (First 50 Words)

| Checkpoint | Pass Criteria |
|------------|---------------|
| Hook type | Counterintuitive, surprising, or tension-building |
| Lead content | Most compelling insight/moment/problem |
| No chronology | Doesn't start with "Last week..." or timeline |
| No setup | Doesn't explain what you're about to say |
| No version numbers | "Version 2.0 of..." is not a hook |
| Promise made | Reader knows why to keep reading |

**Test**: Cover everything after the first 50 words. Would you want to read more?

### Body

| Checkpoint | Pass Criteria |
|------------|---------------|
| Promise kept | Body delivers what opening promised |
| Sensory details | At least one concrete detail per section |
| Paragraph purpose | Each paragraph advances the argument |
| Transitions | Movement between sections is smooth |
| No redundancy | No section repeats another's point |

**Test**: Can you summarize each paragraph's contribution in 5 words?

### Strategy Compliance

| Checkpoint | Pass Criteria |
|------------|---------------|
| Baseline strategies | All 10 applied |
| Situational strategies | 3-4 selected and visible |
| One idea per sentence | No compound thoughts cramming |
| Technical orientation | Jargon explained in context |
| Active voice | <10% passive voice |

**Test**: Read aloud. Does it flow? Are sentences clear?

### Closing

| Checkpoint | Pass Criteria |
|------------|---------------|
| Callback | References opening hook or promise |
| Action clear | Reader knows what to do next |
| Memorable | Last line could be quoted |
| No summary | Doesn't recap what was said |
| No apology | Doesn't hedge or qualify |

**Test**: Would you tweet the last line?

## Style Guide Compliance

If a style guide is specified:

### Voice
- [ ] Matches vocabulary patterns
- [ ] Matches sentence length targets
- [ ] Matches formality level
- [ ] Matches emotional register

### Prohibitions
- [ ] No prohibited words used
- [ ] No prohibited patterns used
- [ ] No formatting violations

### Requirements
- [ ] Required elements present
- [ ] Required structure followed
- [ ] Required attribution style used

## Final Pass

### Read Aloud Test
- [ ] Sentences sound natural when spoken
- [ ] No tongue-twisters
- [ ] Rhythm feels right

### The Email Test
- [ ] Would send this to your smartest colleague
- [ ] Would feel good if it went viral
- [ ] Would stand behind every claim

### The Cut Test
- [ ] Tried cutting 10%—kept only what survived
- [ ] No paragraph that could be cut without loss
- [ ] No sentence that doesn't earn its place

## Checkpoint by Content Type

### Blog Post
1. Hook grabs in first line
2. Subheads are standalone interesting
3. Skimmable (bold, bullets, headers)
4. CTA is clear

### Newsletter
1. Personal tone established
2. Feels like a letter from a person
3. Value delivered early
4. Easy to forward

### Social Post
1. Works without clicking through
2. Hook in first line (gets cut in feeds)
3. No wasted words
4. Visual element considered

### Long-Form
1. Reader can stop after each section and feel complete
2. Sections build but also standalone
3. Pacing varies (tension and release)
4. Ending is earned

## Red Flags

Stop and fix if you see:

| Red Flag | Fix |
|----------|-----|
| Opening starts with "I want to..." | Cut, start with the insight |
| Paragraph over 6 sentences | Split |
| "In this article, we will..." | Delete |
| Three or more "is/was" in a row | Activate verbs |
| Same word appears 3+ times nearby | Elegant variation |
| Quote without attribution | Add source or remove |
| Claim without evidence | Support or soften |
| Ending trails off | Find the punch |

---

## Reference: Situational Strategies

# 20+ Situational Writing Strategies

Select 3-4 strategies based on content type and goals. Don't apply all—choose what fits.

## Hook & Opening Strategies

### hook-effectiveness

**Purpose**: Create openings that demand attention.

**Techniques**:
- **Counterintuitive**: Challenge what readers believe
- **Surprising stat**: Data that defies expectations
- **In media res**: Start in the middle of action
- **Question**: One the reader genuinely wants answered

**Test**: Would you keep reading if you saw this on a busy feed?

### tension-builder

**Purpose**: Create and resolve tension throughout.

**Techniques**:
- Establish stakes early
- Create obstacles before solutions
- Use "but" and "however" strategically
- Delay resolution for impact

**Pattern**: Setup → Complication → Resolution

### pattern-twist

**Purpose**: Set expectations, then break them.

**Techniques**:
- Establish a pattern (three examples)
- Break on the fourth
- Use for humor or insight

**Example**: "We tried ads. We tried SEO. We tried influencers. We tried talking to customers. That last one worked."

---

## Structure & Flow Strategies

### order-words-emphasis

**Purpose**: Put important words where they land hardest—at the end.

**Techniques**:
- Move key terms to sentence end
- End paragraphs with punch
- Save reveals for last position

**Transform**: "We need to focus on the customer." → "Our focus must be the customer."

### sentence-length

**Purpose**: Vary length for rhythm and impact.

**Guidelines**:
- **Short (1-5 words)**: For impact. Punch. Emphasis.
- **Medium (10-20 words)**: For information and flow.
- **Long (25+ words)**: For building, explaining, setting scenes—but sparingly.

**Pattern**: Mix deliberately. Three medium, one short. Repeat.

### paragraph-length

**Purpose**: Create visual rhythm on the page.

**Guidelines**:
- One sentence paragraphs: For emphasis
- 2-3 sentence paragraphs: Standard
- 4+ sentence paragraphs: Use rarely

Like this.

### ladder-abstraction

**Purpose**: Alternate between concrete and abstract.

**Pattern**:
1. Concrete example
2. Abstract principle
3. Another concrete example
4. Broader implication

**Why**: Concrete grounds understanding. Abstract provides meaning. Neither alone is sufficient.

---

## Style & Voice Strategies

### elegant-variation

**Purpose**: Avoid awkward word repetition.

**Techniques**:
- Use pronouns strategically
- Find true synonyms (not forced ones)
- Restructure to avoid repetition
- Sometimes, repetition is intentional—for emphasis

**Warning**: Don't substitute "the social media giant" for "Facebook" constantly. That's worse.

### passive-aggressive

**Purpose**: Use passive voice strategically, not accidentally.

**When passive works**:
- Actor is unknown: "The data was compromised"
- Actor is irrelevant: "The study was conducted in 2020"
- Emphasis on object: "The bill was passed" (focus on bill, not Congress)

**Default**: Active voice. Reserve passive for strategic use.

### punctuation-pace

**Purpose**: Use punctuation to control reading rhythm.

**Tools**:
- **Period**: Full stop. Finality. Impact.
- **Comma**: Pause, breath, continuation
- **Em dash**: Interruption—surprise—aside
- **Semicolon**: Connection between related ideas; used sparingly
- **Colon**: Introduction of what follows

**Example**: "We had three options—none of them good."

### key-words-space

**Purpose**: Give important terms room to breathe.

**Techniques**:
- Don't cluster key terms together
- Space important words throughout
- Let each land before introducing the next

**Wrong**: "The efficiency, productivity, and scalability improvements..."
**Right**: "Efficiency improved. So did productivity. Scalability followed."

---

## Persuasion & Engagement Strategies

### essential-name-filter

**Purpose**: Include only names that add value.

**Test**: Does naming this person/company/product serve the reader?

**Keep**: Names that add credibility, context, or story
**Cut**: Names that are just noise

### name-of-dog

**Purpose**: Specific details create authenticity.

**Technique**: Include the kind of detail only someone who was there would know.

**Examples**:
- "Her golden retriever, Murphy, sat under the desk"
- "The server ran Ubuntu 18.04"
- "The email came at 2:47 AM"

**Why**: Specificity = credibility.

### original-images

**Purpose**: Fresh metaphors over clichés.

**Clichés to kill**:
- "thinking outside the box"
- "at the end of the day"
- "move the needle"
- "low-hanging fruit"
- "on the same page"

**Technique**: If you've heard it before, find a new way to say it.

### show-and-tell

**Purpose**: Balance showing with telling.

**When to show**: Emotional moments, key scenes, character
**When to tell**: Transitions, summaries, facts

**Balance**: Show the important parts. Tell the rest.

---

## Narrative & Story Strategies

### narrate-scenes

**Purpose**: Create immersive scene-setting.

**Elements**:
- Sensory details (what you see, hear, feel)
- Action in progress
- Dialogue if relevant
- Specific time and place

**Example**: "The office was empty except for Sarah, hunched over her laptop, the glow of Slack notifications reflecting off her glasses."

### cinematic-angles

**Purpose**: Use camera-like perspective shifts.

**Techniques**:
- Wide shot: Establish context, setting
- Medium shot: Character and environment
- Close-up: Detail, emotion, significance
- Pull back: Broader meaning, reflection

**Use for**: Feature articles, profiles, narrative pieces

### dialogue-compression

**Purpose**: Make dialogue tight and purposeful.

**Rules**:
- Cut greetings and small talk
- Each line should advance story or reveal character
- Attribution ("he said") should be minimal
- Use beats (actions) instead of dialogue tags

**Wrong**: "Hi, how are you?" "I'm fine, thanks. How are you?"
**Right**: [Cut entirely unless the pleasantries reveal something]

### reveal-traits

**Purpose**: Show character through action, not description.

**Wrong**: "She was a perfectionist."
**Right**: "She realigned the pens on her desk for the third time."

**Technique**: What would this person DO that shows their trait?

---

## Strategy Selection Guide

| Content Type | Recommended Strategies |
|--------------|----------------------|
| Blog post | hook-effectiveness, ladder-abstraction, sentence-length |
| Case study | narrate-scenes, name-of-dog, show-and-tell |
| Product launch | tension-builder, pattern-twist, key-words-space |
| Thought piece | hook-effectiveness, elegant-variation, order-words-emphasis |
| Tutorial | ladder-abstraction, sentence-length, paragraph-length |
| Profile | cinematic-angles, reveal-traits, dialogue-compression |
| Newsletter | hook-effectiveness, sentence-length, one-idea-per-sentence |
| Social post | hook-effectiveness, pattern-twist, sentence-length |
