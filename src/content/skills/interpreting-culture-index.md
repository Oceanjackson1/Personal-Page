---
title: "Interpreting Culture Index"
description: "Interprets Culture Index (CI) surveys, behavioral profiles, and personality assessment data. Supports individual profile interpretation, team composition analysis (gas/brake/glue), burnout detection, profile comparison, hiring profiles, manager co..."
category: "other"
source: "community"
author: "Community"
tags: ["interpreting", "culture", "index"]
date: 2026-03-20
---

<essential_principles>

**Culture Index measures behavioral traits, not intelligence or skills. There is no "good" or "bad" profile.**

<principle name="never-compare-absolutes">
**Never compare absolute trait values between people.**

The 0-10 scale is just a ruler. What matters is **distance from the red arrow** (population mean at 50th percentile). The arrow position varies between surveys based on EU.

**Why the arrow moves:** Higher EU scores cause the arrow to plot further right; lower EU causes it to plot further left. This does not affect validity—we always measure distance from wherever the arrow lands.

**Wrong**: "Dan has higher autonomy than Jim because his A is 8 vs 5"
**Right**: "Dan is +3 centiles from his arrow; Jim is +1 from his arrow"

Always ask: Where is the arrow, and how far is the dot from it?
</principle>

<principle name="survey-vs-job">
**Survey = who you ARE. Job = who you're TRYING TO BE.**

> **"You can't send a duck to Eagle school."** Traits are hardwired—you can only modify behaviors temporarily, at the cost of energy.

- **Top graph (Survey Traits)**: Hardwired by age 12-16. Does not change. Writing with your dominant hand.
- **Bottom graph (Job Behaviors)**: Adaptive behavior at work. Can change. Writing with your non-dominant hand.

Large differences between graphs indicate behavior modification, which drains energy and causes burnout if sustained 3-6+ months.
</principle>

<principle name="distance-interpretation">
**Distance from arrow determines trait strength.**

| Distance | Label | Percentile | Interpretation |
|----------|-------|------------|----------------|
| On arrow | Normative | 50th | Flexible, situational |
| ±1 centile | Tendency | ~67th | Easier to modify |
| ±2 centiles | Pronounced | ~84th | Noticeable difference |
| ±4+ centiles | Extreme | ~98th | Hardwired, compulsive, predictable |

**Key insight:** Every 2 centiles of distance = 1 standard deviation.

Extreme traits drive extreme results but are harder to modify and less relatable to average people.
</principle>

<principle name="l-and-i-exception">
**L (Logic) and I (Ingenuity) use absolute values.**

Unlike A, B, C, D, you CAN compare L and I scores directly between people:
- Logic 8 means "High Logic" regardless of arrow position
- Ingenuity 2 means "Low Ingenuity" for anyone

Only these two traits break the "no absolute comparison" rule.
</principle>

</essential_principles>

## When to Use

- Interpreting Culture Index survey results (individual or team)
- Analyzing CI profiles from PDF or JSON data
- Assessing team composition using Gas/Brake/Glue framework
- Detecting burnout risk by comparing Survey vs Job graphs
- Defining hiring profiles based on CI trait patterns
- Coaching managers on how to work with specific CI profiles
- Predicting CI traits from interview transcripts
- Mediating team conflict using CI profile data

## When NOT to Use

- For non-CI behavioral assessments (DISC, Myers-Briggs, StrengthsFinder, Predictive Index, Enneagram)
- For clinical psychological assessments or diagnoses
- As the sole basis for hiring/firing decisions — CI is one data point among many

<input_formats>

**JSON (Use if available)**

If JSON data is already extracted, use it directly:
```python
import json
with open("person_name.json") as f:
    profile = json.load(f)
```

JSON format:
```json
{
  "name": "Person Name",
  "archetype": "Architect",
  "survey": {
    "eu": 21,
    "arrow": 2.3,
    "a": [5, 2.7],
    "b": [0, -2.3],
    "c": [1, -1.3],
    "d": [3, 0.7],
    "logic": [5, null],
    "ingenuity": [2, null]
  },
  "job": { "..." : "same structure as survey" },
  "analysis": {
    "energy_utilization": 148,
    "status": "stress"
  }
}
```

Note: Trait values are `[absolute, relative_to_arrow]` tuples. Use the relative value for interpretation.

Check same directory as PDF for matching `.json` file, or ask user if they have extracted JSON.

**PDF Input (MUST EXTRACT FIRST)**

⚠️ **NEVER use visual estimation for trait values.** Visual estimation has 20-30% error rate.

When given a PDF:
1. Check if JSON already exists (same directory as PDF, or ask user)
2. If not, run extraction with verification:
   ```bash
   uv run {baseDir}/scripts/extract_pdf.py --verify /path/to/file.pdf [output.json]
   ```
3. Visually confirm the verification summary matches the PDF
4. Use the extracted JSON for interpretation

**If uv is not installed:** Stop and instruct user to install it (`brew install uv` or `pip install uv`). Do NOT fall back to vision.

**PDF Vision (Reference Only)**

Vision may be used ONLY to verify extracted values look reasonable, NOT to extract trait scores.

</input_formats>

<intake>

**Step 0: Do you have JSON or PDF?**

1. **If JSON provided or found:** Use it directly (skip extraction)
   - Check same directory as PDF for `.json` file with matching name
   - Check if user provided JSON path
2. **If only PDF:** Run extraction script with `--verify` flag
   ```bash
   uv run {baseDir}/scripts/extract_pdf.py --verify /path/to/file.pdf [output.json]
   ```
3. **If extraction fails:** Report error, do NOT fall back to vision

**Step 1: What data do you have?**

- **CI Survey JSON** → Proceed to Step 2
- **CI Survey PDF** → Extract first (Step 0), then proceed to Step 2
- **Interview transcript only** → Go to option 8 (predict traits from interview)
- **No data yet** → "Please provide Culture Index profile (PDF or JSON) or interview transcript"

**Step 2: What would you like to do?**

**Profile Analysis:**
1. **Interpret an individual profile** - Understand one person's traits, strengths, and challenges
2. **Analyze team composition** - Assess gas/brake/glue balance, identify gaps
3. **Detect burnout signals** - Compare Survey vs Job, flag stress/frustration
4. **Compare multiple profiles** - Understand compatibility, collaboration dynamics
5. **Get motivator recommendations** - Learn how to engage and retain someone

**Hiring & Candidates:**
6. **Define hiring profile** - Determine ideal CI traits for a role
7. **Coach manager on direct report** - Adjust management style based on both profiles
8. **Predict traits from interview** - Analyze interview transcript to estimate CI traits
9. **Interview debrief** - Assess candidate fit based on predicted traits

**Team Development:**
10. **Plan onboarding** - Design first 90 days based on new hire and team profiles
11. **Mediate conflict** - Understand friction between two people using their profiles

**Provide the profile data (JSON or PDF) and select an option, or describe what you need.**

</intake>

<routing>

| Response | Workflow |
|----------|----------|
| "extract", "parse pdf", "convert pdf", "get json from pdf" | `workflows/extract-from-pdf.md` |
| 1, "individual", "interpret", "understand", "analyze one", "single profile" | `workflows/interpret-individual.md` |
| 2, "team", "composition", "gaps", "balance", "gas brake glue" | `workflows/analyze-team.md` |
| 3, "burnout", "stress", "frustration", "survey vs job", "energy", "flight risk" | `workflows/detect-burnout.md` |
| 4, "compare", "compatibility", "collaboration", "multiple", "two profiles" | `workflows/compare-profiles.md` |
| 5, "motivate", "engage", "retain", "communicate" | Read `references/motivators.md` directly |
| 6, "hire", "hiring profile", "role profile", "recruit", "what profile for" | `workflows/define-hiring-profile.md` |
| 7, "manage", "coach", "1:1", "direct report", "manager" | `workflows/coach-manager.md` |
| 8, "transcript", "interview", "predict traits", "guess", "estimate", "recording" | `workflows/predict-from-interview.md` |
| 9, "debrief", "should we hire", "candidate fit", "proceed", "offer" | `workflows/interview-debrief.md` |
| 10, "onboard", "new hire", "integrate", "starting", "first 90 days" | `workflows/plan-onboarding.md` |
| 11, "conflict", "friction", "mediate", "not working together", "clash" | `workflows/mediate-conflict.md` |
| "conversation starters", "how to talk to", "engage with" | Read `references/conversation-starters.md` directly |

**After reading the workflow, follow it exactly.**

</routing>

<verification_loop>

After every interpretation, verify:

1. **Did you use relative positions?** Never stated "A is 8" without context
2. **Did you reference the arrow?** All trait interpretations relative to arrow
3. **Did you compare Survey vs Job?** Identified any behavior modification
4. **Did you avoid value judgments?** No traits called "good" or "bad"
5. **Did you check EU?** Energy utilization calculated if both graphs present

Report to user:
- "Interpretation complete"
- Key findings (2-3 bullet points)
- Recommended actions

</verification_loop>

<reference_index>

**Domain Knowledge** (in `references/`):

**Primary Traits:**
- `primary-traits.md` - A (Autonomy), B (Social), C (Pace), D (Conformity)

**Secondary Traits:**
- `secondary-traits.md` - EU (Energy Units), L (Logic), I (Ingenuity)

**Patterns:**
- `patterns-archetypes.md` - Behavioral patterns, trait combinations, archetypes

**Application:**
- `motivators.md` - How to motivate each trait type
- `team-composition.md` - Gas, brake, glue framework
- `anti-patterns.md` - Common interpretation mistakes
- `conversation-starters.md` - How to engage each pattern and trait type
- `interview-trait-signals.md` - Signals for predicting traits from interviews

</reference_index>

<workflows_index>

**Workflows** (in `workflows/`):

| File | Purpose |
|------|---------|
| `extract-from-pdf.md` | Extract profile data from Culture Index PDF to JSON format |
| `interpret-individual.md` | Analyze single profile, identify archetype, summarize strengths/challenges |
| `analyze-team.md` | Assess team balance (gas/brake/glue), identify gaps, recommend hires |
| `detect-burnout.md` | Compare Survey vs Job, calculate EU utilization, flag risk signals |
| `compare-profiles.md` | Compare multiple profiles, assess compatibility, collaboration dynamics |
| `define-hiring-profile.md` | Define ideal CI traits for a role, identify acceptable patterns and red flags |
| `coach-manager.md` | Help managers adjust their style for specific direct reports |
| `predict-from-interview.md` | Analyze interview transcripts to predict CI traits before survey |
| `interview-debrief.md` | Assess candidate fit using predicted traits from transcript analysis |
| `plan-onboarding.md` | Design first 90 days based on new hire profile and team composition |
| `mediate-conflict.md` | Understand and address friction between team members using their profiles |

</workflows_index>

<quick_reference>

**Trait Colors:**
| Trait | Color | Measures |
|-------|-------|----------|
| A | Maroon | Autonomy, initiative, self-confidence |
| B | Yellow | Social ability, need for interaction |
| C | Blue | Pace/Patience, urgency level |
| D | Green | Conformity, attention to detail |
| L | Purple | Logic, emotional processing |
| I | Cyan | Ingenuity, inventiveness |

**Energy Utilization Formula:**
```
Utilization = (Job EU / Survey EU) × 100

70-130% = Healthy
>130% = STRESS (burnout risk)
<70% = FRUSTRATION (flight risk)
```

**Gas/Brake/Glue:**
| Role | Trait | Function |
|------|-------|----------|
| Gas | High A | Growth, risk-taking, driving results |
| Brake | High D | Quality control, risk aversion, finishing |
| Glue | High B | Relationships, morale, culture |

**Score Precision:**
| Value | Precision | Example |
|-------|-----------|---------|
| Traits (A,B,C,D,L,I) | Integer 0-10 | 0, 1, 2, ... 10 |
| Arrow position | Tenths | 0.4, 2.2, 3.8 |
| Energy Units (EU) | Integer | 11, 31, 45 |

</quick_reference>

<success_criteria>

A well-interpreted Culture Index profile:
- Uses relative positions (distance from arrow), never absolute values alone
- Identifies the archetype/pattern correctly
- Highlights 2-3 key strengths based on leading traits
- Notes 2-3 challenges or development areas
- Compares Survey vs Job if both are available
- Provides actionable recommendations
- Avoids value judgments ("good"/"bad")
- Acknowledges Culture Index is one data point, not a complete picture

</success_criteria>

---

## Reference: Anti Patterns

<overview>

Common mistakes when interpreting Culture Index profiles. Avoiding these errors is as important as understanding the methodology itself.

</overview>

<interpretation_mistakes>

<mistake name="comparing-absolutes">

**Comparing absolute trait values between people**

**Wrong:** "Dan has higher autonomy than Jim because his A is 8 vs 5"

**Right:** "Dan is +3 centiles from his arrow; Jim is +1 from his arrow"

**Why it's wrong:** The arrow position varies between surveys based on EU. An 8 with an arrow at 6 is only +2 from norm. A 5 with an arrow at 2 is +3 from norm.

**Only exception:** L and I use absolute values and CAN be compared directly.

</mistake>

<mistake name="ignoring-arrow">

**Ignoring the red arrow position**

The arrow is the population mean (50th percentile). All interpretation must be relative to it.

**Wrong:** "This person has low B (score of 3)"

**Right:** "This person's B is 2 centiles left of their arrow, indicating pronounced introversion"

</mistake>

<mistake name="value-judgments">

**Treating traits as "good" or "bad"**

Culture Index measures behavioral traits, not value or capability.

**Wrong:**
- "High D is good because they're detail-oriented"
- "Low B is bad because they're not social"

**Right:**
- "High D indicates strong attention to detail - fits roles requiring precision"
- "Low B indicates preference for focused work - fits analytical roles"

There is no universally "good" profile. Fit depends on role, team, and context.

</mistake>

<mistake name="stale-data">

**Using outdated data (18+ months old)**

Job behaviors update as environment, leadership, or projects change. Stale data leads to wrong conclusions.

**Best practice:** Resurvey job behaviors every 6 months, especially after major role or leadership changes.

</mistake>

<mistake name="single-trait-focus">

**Over-indexing on a single trait**

The pattern (relationship between traits) matters more than any individual dot.

**Wrong:** "They have High A, so they're a leader"

**Right:** "High A combined with High D suggests they can build new systems. High A with Low D suggests they'll drive fast but may miss details."

</mistake>

<mistake name="ignoring-survey-vs-job">

**Not comparing Survey vs Job graphs**

Missing burnout signals by only looking at one graph.

**Always check:**
- Did the arrow move? (Stress/Frustration signal)
- Did any dots flip sides? (Polarizing shift - flight risk)
- What's the EU utilization? (>130% stress, <70% frustration)

</mistake>

<mistake name="confusing-traits-behaviors">

**Confusing traits with behaviors**

Survey (top) = hardwired traits (who you ARE)
Job (bottom) = adaptive behaviors (who you're TRYING TO BE)

Traits don't change. Behaviors can be modified temporarily - but at an energy cost.

**"You can't send a duck to Eagle school."** - You can train behaviors, not traits.

</mistake>

</interpretation_mistakes>

<application_mistakes>

<mistake name="seeking-homogeneity">

**Hiring for homogeneous teams**

Hiring people who match the manager's profile creates blind spots.

**Better approach:** Build diverse teams with complementary traits. Every team needs Gas (High A), Brake (High D), and Glue (High B) in appropriate proportions.

</mistake>

<mistake name="overloading-high-a">

**Overloading on High A's**

High A's are "the single hardest trait to employ." They work for "me, Inc." first.

Too many High A's = power struggles, lack of follow-through, no one to execute.

**You are only RENTING High A's** - they need a mutually beneficial partnership.

</mistake>

<mistake name="neglecting-brake">

**Neglecting the Brake (High D)**

Every team needs quality control, risk management, and follow-through.

Without Brake: Erosion, mistakes, lawsuits, quality issues, things start but never finish.

</mistake>

<mistake name="assuming-fit-permanent">

**Assuming job fit is permanent**

People's roles evolve. Business needs change. What fit yesterday may not fit tomorrow.

Regular check-ins (resurvey every 6 months) catch misalignment before it becomes burnout or turnover.

</mistake>

<mistake name="using-ci-alone">

**Using Culture Index as the only data point**

Culture Index is ONE tool among many. It measures behavioral traits, not:
- Skills or competencies
- Intelligence
- Experience
- Values
- Motivation

**Best practice:** Use CI alongside interviews, references, skills assessments, and performance data.

</mistake>

</application_mistakes>

<communication_mistakes>

<mistake name="sharing-raw-scores">

**Sharing raw scores without context**

Telling someone "Your A is 8" without explaining relative position is meaningless and potentially harmful.

**Always communicate:**
- Position relative to arrow
- What that means behaviorally
- Why it's neither good nor bad
- How it fits (or doesn't) with their role

</mistake>

<mistake name="labeling-people">

**Using CI to label or box people**

CI shows tendencies, not destiny.

**Wrong:** "You're a Persuader, so you should only do sales"

**Right:** "Your pattern shows strengths in influence and relationship building. How do you use those in your current role?"

</mistake>

<mistake name="public-comparison">

**Comparing profiles publicly**

Never compare individuals' profiles in group settings without their consent.

Discussing "Person A is more detail-oriented than Person B" creates hierarchy and judgment.

</mistake>

</communication_mistakes>

<red_flags>

**Signals that suggest deeper investigation:**

| Signal | What to Check |
|--------|---------------|
| EU 0-10 (avoidant response) | Was survey completed properly? Trust issues? |
| All dots on or near arrow | Chameleon pattern - less than 0.57% of population. Verify validity. |
| Job behaviors completely opposite of Survey | Imminent flight risk. What's causing this extreme modification? |
| EU utilization > 150% | Severe stress. Immediate conversation needed. |
| EU utilization < 50% | Severe disengagement. May have already mentally quit. |
| D raised significantly in Job behaviors | Most common unsustainable stress pattern. Why do they feel they need to be so much more perfectionist? |

</red_flags>

<checklist>

**Before finalizing any interpretation:**

- [ ] Did I use relative positions (distance from arrow)?
- [ ] Did I avoid calling any trait "good" or "bad"?
- [ ] Did I compare Survey vs Job if both available?
- [ ] Did I calculate EU utilization?
- [ ] Did I consider the full pattern, not just leading traits?
- [ ] Is my data current (less than 18 months old)?
- [ ] Did I note that CI is one data point among many?

</checklist>

<rationalization_table>

**Common excuses that indicate you're about to make a CI interpretation mistake:**

| Excuse | Reality |
|--------|---------|
| "Their A is higher so they're more autonomous" | Compare distance from arrow, not absolute values |
| "This is a bad profile for leadership" | No bad profiles - fit depends on role and context |
| "They need to change their C trait" | Survey traits are hardwired - change the environment instead |
| "Low B means they're not a team player" | Low B means they prefer focused work - they can still collaborate |
| "High D is always good for quality" | High D without other traits can mean paralysis and rigidity |
| "They should be more like their manager" | Different profiles bring complementary strengths |
| "This pattern can't do that job" | Patterns indicate tendencies, not hard limits |
| "Their EU is fine, the job is the problem" | EU tells you about energy, not about job design |
| "I remember their profile from last year" | Resurvey Job behaviors every 6 months - they change |
| "The arrow doesn't matter, just look at the dots" | The arrow IS the reference point - dots mean nothing without it |
| "L and I work the same as A, B, C, D" | L and I use absolute values, primary traits are relative |
| "Survey and Job will be the same" | Survey = hardwired, Job = adaptive. They often differ. |
| "High A means they're selfish" | High A means they're self-directed - not the same thing |
| "We need all High A's on this high-growth team" | You're renting High A's, and they'll clash with each other |
| "This hire looks good, skip the CI" | CI is one data point - use it WITH other assessments, not instead of |

</rationalization_table>

---

## Reference: Conversation Starters

<overview>

Conversation starters and engagement strategies based on Culture Index traits. Use these to build rapport, deliver feedback effectively, and engage team members based on their profile.

</overview>

<by_pattern>

<architect label="Architect/Visionary (High A, Low C, Low D)">

**What engages them:**
- Strategic discussions, big picture thinking
- Future vision and possibilities
- ROI and business impact
- Being asked for their opinion

**Good conversation starters:**
- "What do you think is the biggest opportunity we're missing?"
- "If you could redesign this from scratch, what would you change?"
- "What's your take on [strategic topic]?"
- "Where do you see this going in 2-3 years?"

**How to deliver feedback:**
- Focus on outcomes and impact, not process
- Be direct and confident - don't hedge
- Frame as investment in their success
- Bullet points, not paragraphs

**Topics to avoid:**
- Excessive detail about implementation
- Step-by-step instructions
- Past failures (they've moved on)
- Lengthy consensus-building

</architect>

<rainmaker label="Rainmaker/Persuader (High A, High B, Low C)">

**What engages them:**
- Relationship building
- Competitive challenges
- Public recognition opportunities
- Stories and narratives

**Good conversation starters:**
- "How did you land that account?"
- "What's your read on [person/client]?"
- "Tell me about your biggest win this quarter"
- "Who should I talk to about [topic]?"

**How to deliver feedback:**
- Balance directness with relationship
- Public praise, private criticism
- Frame around their reputation and influence
- Keep it brief - they'll want to talk

**Topics to avoid:**
- Detailed process requirements
- Solitary work expectations
- Administrative tasks
- Slow-moving, bureaucratic topics

</rainmaker>

<scholar label="Scholar/Specialist (Low B, High C, High D)">

**What engages them:**
- Deep expertise discussions
- Complex technical problems
- Quality and precision topics
- Learning opportunities

**Good conversation starters:**
- "I'd like your expert opinion on [technical topic]"
- "Can you walk me through how this works?"
- "What do you think is the right way to approach this?"
- "I'm trying to understand [complex topic] - can you help?"

**How to deliver feedback:**
- Be specific and fact-based
- Reference documentation or standards
- Give them time to process
- Private, not public
- Written follow-up appreciated

**Topics to avoid:**
- Forced small talk
- Vague, unstructured discussions
- Expecting quick verbal responses
- Public attention or praise

</scholar>

<technical_expert label="Technical Expert (Low A, Low B, Low C, High D)">

**What engages them:**
- Efficient, focused discussions
- Clear problems with clear solutions
- Quality and accuracy
- Getting things done

**Good conversation starters:**
- "I need your help solving [specific problem]"
- "What's the correct way to do this?"
- "Can you review this for accuracy?"
- "Here's the situation - what's your take?"

**How to deliver feedback:**
- Very direct and specific
- Focus on the work, not the person
- Provide clear standards to meet
- Brief and efficient

**Topics to avoid:**
- Extended social conversation
- Vague or open-ended questions
- Consensus-building meetings
- Public recognition (uncomfortable)

</technical_expert>

<craftsman label="Craftsman (Low A, Low B, High C, High D)">

**What engages them:**
- Mastery and expertise
- Consistent, reliable processes
- Quality discussions
- Predictable environments

**Good conversation starters:**
- "You're the expert on this - what should I know?"
- "What's the best practice for [specific task]?"
- "I want to make sure we do this right"
- "Can you help me understand the proper process?"

**How to deliver feedback:**
- Frame as process improvement
- Reference standards and best practices
- One topic at a time
- Allow time to process and respond

**Topics to avoid:**
- Rapid-fire questions
- Unstructured brainstorming
- Public speaking or presentations
- Frequent change of plans

</craftsman>

<accommodator label="Accommodator (Low A, High B, High C)">

**What engages them:**
- Team and relationship discussions
- Helping others succeed
- Collaborative problem-solving
- Stable, supportive environments

**Good conversation starters:**
- "How's the team doing?"
- "Who needs support right now?"
- "What would make this easier for everyone?"
- "How can I help you help the team?"

**How to deliver feedback:**
- Gentle but clear
- Acknowledge their contributions
- Frame around team impact
- Give time to adjust

**Topics to avoid:**
- Aggressive confrontation
- Demanding immediate decisions
- Forcing them to take sides
- Public criticism

</accommodator>

<philosopher label="Philosopher (High A, Low B, High C)">

**What engages them:**
- Deep analytical discussions
- Strategic thinking
- Independent problem-solving
- Time to think and process

**Good conversation starters:**
- "What's your analysis of [complex situation]?"
- "I'd value your perspective on this"
- "If you had to choose a direction, what would it be?"
- "What patterns are you seeing?"

**How to deliver feedback:**
- Logical, fact-based
- Allow processing time
- Written communication works well
- Respect their independence

**Topics to avoid:**
- Forced team activities
- Rapid decision demands
- Excessive small talk
- Public group discussions

</philosopher>

</by_pattern>

<by_trait>

<high_a label="Engaging High A (Autonomous/Assertive)">

**Do:**
- Ask for their opinion before sharing yours
- Give outcomes, not instructions
- Respect their time (be efficient)
- Challenge them intellectually
- Acknowledge their expertise

**Don't:**
- Micromanage or over-explain
- Expect consensus-building
- Take too long to get to the point
- Show hesitation or uncertainty
- Dismiss their ideas without discussion

**Feedback style:**
- Direct, confident, brief
- Focus on ROI and impact
- Their investment in success

</high_a>

<low_a label="Engaging Low A (Supportive/Collaborative)">

**Do:**
- Include them in discussions
- Acknowledge their contributions
- Provide clear direction
- Give specific praise
- Allow time for input

**Don't:**
- Put them on the spot for decisions
- Expect aggressive initiative
- Skip collaboration for speed
- Interpret silence as agreement
- Assume they'll speak up with concerns

**Feedback style:**
- Specific, supportive
- Private, not public
- Clear expectations

</low_a>

<high_b label="Engaging High B (Social/Relational)">

**Do:**
- Start with personal connection
- Allow time for rapport
- Include in group activities
- Praise publicly
- Ask about relationships and team

**Don't:**
- Skip small talk
- Isolate with solo work
- Give criticism publicly
- Expect brief, task-only interaction
- Forget they process verbally

**Feedback style:**
- Start with relationship
- Verbal praise matters
- Private for criticism

</high_b>

<low_b label="Engaging Low B (Reserved/Task-Focused)">

**Do:**
- Get to the point
- Respect their focus time
- Use written communication
- Give private recognition
- Allow solo work time

**Don't:**
- Force extended social interaction
- Expect verbal processing
- Praise publicly (uncomfortable)
- Require constant meetings
- Mistake quiet for disengagement

**Feedback style:**
- Efficient, task-focused
- Written is appreciated
- Private, not public

</low_b>

<high_c label="Engaging High C (Patient/Steady)">

**Do:**
- Send agendas in advance
- One topic at a time
- Give advance notice of changes
- Respect their routines
- Allow processing time

**Don't:**
- Surprise them with changes
- Rush decisions
- Interrupt their focus time
- Multi-topic meetings
- Create unnecessary urgency

**Feedback style:**
- Scheduled, predictable
- Advance notice helpful
- One issue at a time

</high_c>

<low_c label="Engaging Low C (Urgent/Fast-Paced)">

**Do:**
- Put deadlines in subject lines
- Keep them busy with variety
- Accept their urgency
- Use their energy productively
- Be ready for interruptions

**Don't:**
- Expect patient waiting
- Give slow, drawn-out responses
- Bore them with routine
- Slow-walk decisions
- Be surprised by multitasking

**Feedback style:**
- Quick and direct
- Deadlines motivate
- Don't delay

</low_c>

<high_d label="Engaging High D (Detail/Precise)">

**Do:**
- Be accurate and specific
- Reference standards and process
- Provide documentation
- Acknowledge their precision
- Build trust carefully

**Don't:**
- Make it personal
- Skip details that matter
- Break commitments
- Expect flexibility on quality
- Give vague instructions

**Feedback style:**
- Process improvement framing
- Specific, documented
- Don't break trust

</high_d>

<low_d label="Engaging Low D (Flexible/Big-Picture)">

**Do:**
- Give creative problems
- Provide options
- Focus on outcomes
- Accept 80% solutions
- Allow flexibility

**Don't:**
- Over-structure
- Expect precise documentation
- Hold grudges for missed details
- Box them in with rules
- Require perfection

**Feedback style:**
- Focus on what matters
- Pick your battles
- Options over mandates

</low_d>

</by_trait>

<quick_reference>

| Pattern | Open With | Avoid | Feedback Style |
|---------|-----------|-------|----------------|
| Architect | "What's your vision..." | Detail-heavy | Direct, ROI-focused |
| Rainmaker | "How did you..." | Solitary topics | Public praise, private critique |
| Scholar | "Walk me through..." | Small talk | Written, specific |
| Technical Expert | "I need help with..." | Open-ended | Direct, efficient |
| Craftsman | "What's the right way..." | Rapid-fire | Process improvement |
| Accommodator | "How's the team..." | Confrontation | Gentle, supportive |
| Philosopher | "What's your analysis..." | Forced social | Logical, written |

</quick_reference>

---

## Reference: Interview Trait Signals

<overview>

This reference helps predict Culture Index traits from interview transcripts. Candidates don't take CI during interviews - these signals help estimate traits before the actual survey is administered after an offer is signed.

**Important caveats:**
- Predictions are estimates, not definitive assessments
- Interview context affects behavior (stress, performance mode)
- Always note confidence level for each trait
- Actual CI survey will confirm or correct predictions

</overview>

<trait_signals>

<autonomy_a label="Autonomy (A) Signals">

**High A indicators (right of arrow):**
- Uses "I" frequently: "I decided...", "I built...", "I led..."
- Takes personal credit for outcomes
- Describes situations where they acted independently
- Pushes back on interviewer questions or reframes them
- Strategic framing - connects work to business outcomes
- Confident tone, assertive statements
- Mentions enjoying autonomy, disliking micromanagement
- Describes taking initiative without being asked

**Low A indicators (left of arrow):**
- Uses "we" predominantly: "We decided...", "Our team..."
- Deflects credit to the team
- Asks clarifying questions before answering
- Seeks validation: "Does that make sense?"
- Describes collaborative decision-making
- Mentions appreciating clear direction
- More tentative language: "I think...", "Maybe..."
- Waits for prompts rather than driving conversation

**Confidence modifiers:**
- HIGH confidence: Multiple consistent signals across different questions
- MEDIUM confidence: Mixed signals or few data points
- LOW confidence: Signals only in specific contexts (may be performance mode)

</autonomy_a>

<social_b label="Social Ability (B) Signals">

**High B indicators (right of arrow):**
- Builds rapport quickly, asks about interviewer
- Animated, expressive communication style
- Tells stories with people as central characters
- Discusses team dynamics, relationships
- Uses humor, creates connection
- Mentions enjoying collaboration, team activities
- Verbose responses, talks through thinking
- Mirrors interviewer's energy and style

**Low B indicators (left of arrow):**
- Brief, direct answers without elaboration
- Skips small talk, gets to the point
- Task-focused: describes what was done, not who was involved
- Reserved or flat affect
- Minimal questions about the team/culture
- Doesn't engage with personal questions
- Processes internally before responding
- Technical precision over narrative style

**Confidence modifiers:**
- HIGH confidence: Behavior consistent throughout entire interview
- MEDIUM confidence: Opens up later (may be warming up)
- LOW confidence: Interviewer-driven variation (some interviewers draw out B)

</social_b>

<pace_c label="Pace/Patience (C) Signals">

**High C indicators (right of arrow):**
- Thoughtful pauses before answering
- Asks for clarification, wants to understand fully
- Structured, methodical responses
- Mentions preferring stable environments
- Describes careful, deliberate decision-making
- Discomfort with hypotheticals or rapid-fire questions
- References to planning, preparation
- Prefers one topic at a time

**Low C indicators (left of arrow):**
- Rapid responses, quick wit
- Interrupts or finishes interviewer's sentences
- Topic-jumps, tangential connections
- Mentions thriving under pressure, deadlines
- Comfortable with ambiguity and pivots
- Describes multitasking positively
- Energy increases with urgency
- Short attention span for detailed questions

**Confidence modifiers:**
- HIGH confidence: Consistent pace throughout interview
- MEDIUM confidence: Interview pressure may affect natural pace
- LOW confidence: Phone vs in-person may show different C

</pace_c>

<conformity_d label="Conformity/Detail (D) Signals">

**High D indicators (right of arrow):**
- Precise language, specific numbers and dates
- References rules, processes, best practices
- Structured answers following question format
- Mentions quality, accuracy, standards
- Asks about company processes, documentation
- Describes checking work, seeking feedback
- Uses technical terms correctly and consistently
- Follows interview structure carefully

**Low D indicators (left of arrow):**
- Big-picture answers, approximations
- Comfortable with "it depends" responses
- Creative interpretations of questions
- Mentions flexibility, adaptability
- Skeptical of rigid processes
- Focuses on outcomes over methods
- May challenge question premises
- Unstructured, flowing responses

**Confidence modifiers:**
- HIGH confidence: Consistent precision (or lack of) across topics
- MEDIUM confidence: Higher precision in domain expertise areas
- LOW confidence: May mask natural D to appear more flexible

</conformity_d>

<logic_l label="Logic (L) Signals">

Note: L uses absolute values (not relative to arrow).

**High L indicators (7-10):**
- Data-driven reasoning: "The numbers showed..."
- Logical frameworks: "First... then... therefore..."
- Emotion-neutral language
- Focuses on facts over feelings
- Analytical approach to problems
- May seem detached when discussing difficult situations
- Questions based on data or evidence

**Low L indicators (0-3):**
- Values-driven language: "It felt right..."
- Emotional context in stories
- Empathy-focused responses
- Describes gut feelings, intuition
- People-impact framing
- May get emotional discussing meaningful work
- Questions based on culture, values, impact

**Moderate L (4-6):**
- Blends logic and emotion contextually
- Adapts framing to situation
- Can argue both sides

</logic_l>

<ingenuity_i label="Ingenuity (I) Signals">

Note: I uses absolute values (not relative to arrow).

**High I indicators (7-10):**
- Novel approaches to problems
- Questions assumptions, challenges status quo
- Connects unrelated concepts
- Describes inventing solutions
- Mentions boredom with routine
- Creative reframing of questions
- Original examples, not textbook answers

**Low I indicators (0-3):**
- Conventional approaches, proven methods
- References industry standards, best practices
- Prefers established processes
- Practical, grounded solutions
- Describes following playbooks successfully
- May seem less creative but highly reliable

**Moderate I (4-6):**
- Creative within constraints
- Innovates when necessary, follows when appropriate

</ingenuity_i>

</trait_signals>

<pattern_combinations>

Look for trait combinations that suggest patterns:

| Signal Cluster | Likely Pattern |
|----------------|----------------|
| High A + Low B + rapid pace + big-picture | Architect/Visionary |
| High A + High B + rapid pace | Rainmaker/Persuader |
| Low B + deliberate pace + precise | Scholar/Specialist |
| Low A + High B + deliberate | Accommodator |
| Low A + Low B + precise | Technical Expert |

</pattern_combinations>

<transcript_analysis_tips>

**When analyzing transcripts:**

1. **Count language patterns** - "I" vs "we", precise vs approximate
2. **Note energy shifts** - What topics animate them? What topics flatten them?
3. **Watch for consistency** - Same signals across different questions?
4. **Consider context** - Technical questions vs behavioral questions
5. **Flag uncertainties** - Note where evidence is weak

**Red flags for confidence:**
- Candidate clearly in "interview mode" (performing)
- Very short interview (insufficient data)
- Interviewer dominated conversation
- Technical-only questions (limited behavioral data)

</transcript_analysis_tips>

<output_format>

When predicting traits from transcripts, output:

```
## Predicted Culture Index Profile: [Candidate Name]

### Trait Predictions
| Trait | Predicted Position | Confidence | Key Evidence |
|-------|-------------------|------------|--------------|
| A | High/Low/Norm | H/M/L | "Quote..." |
| B | High/Low/Norm | H/M/L | "Quote..." |
| C | High/Low/Norm | H/M/L | "Quote..." |
| D | High/Low/Norm | H/M/L | "Quote..." |
| L | Score (0-10) | H/M/L | "Quote..." |
| I | Score (0-10) | H/M/L | "Quote..." |

### Predicted Pattern
[Pattern name] - [Confidence]

### Evidence Summary
[2-3 sentences on strongest signals]

### Uncertainty Areas
[Where more data would help]

### Caveats
- Interview behavior may differ from natural behavior
- Actual CI survey will be administered after offer
- This prediction is a hypothesis, not a diagnosis
```

</output_format>

---

## Reference: Motivators

<overview>

The simplest way to drive engagement and productivity is to find the leading dot among A, B, D (the three confidence traits) and install motivators for that trait consistently.

</overview>

<motivator_framework>

**Step 1: Find the leading dot** between A, B, and D (the three confidence traits)
**Step 2: Go to that trait's motivator box** (see below)
**Step 3: Install 3-4 of those motivators consistently**

**When dots are stacked** (three confidence traits close together): D always wins - start with D trait motivators first, then B, then A.

**Master level:** Hit motivators for all four primary dots. Takes 2-3 years of practice.

**Retention tip:** Expect to retain ~30% of workshop content initially. Quarterly team discussions with real-life examples help mobilize learning.

</motivator_framework>

<motivators_by_trait>

<high_a label="High Autonomy Motivators">

- **Variable compensation** - Bonus, equity, commission over fixed salary
- **Autonomy** - Freedom to decide how to achieve goals
- **ROI-focused communication** - Bullet points, not walls of text
- **Outcomes over process** - "Bake me a cake" not "here's the recipe"
- **Challenge** - Opportunities to compete and win
- **Buy-in through questions** - Let them "own" the idea
- **Respect their time** - Don't waste it with unnecessary meetings

**What doesn't work:** Micromanagement, detailed instructions, fixed salary only, consensus-driven decisions

</high_a>

<low_a label="Low Autonomy Motivators">

- **Specific praise** - "Great job on the Johnson proposal" not "Great job"
- **Consistent compensation** - Predictable over variable bonuses
- **Clear frameworks** - For novel decisions
- **Direction before action** - Don't expect self-initiation
- **Team recognition** - Acknowledge collaborative contributions
- **Safety to disagree** - Probe for true concerns (they won't volunteer)

**What doesn't work:** Variable compensation, ambiguous direction, expecting initiative on new challenges

</low_a>

<high_b label="High Social Motivators">

- **Words of affirmation** - Primary currency - verbal praise, public recognition
- **Small talk time** - Not wasted time, it's relationship investment
- **Group activities** - Include them in social events
- **People interaction** - Don't isolate with solo work
- **Public recognition** - Acknowledge in team settings
- **Relationship building time** - Before getting to tasks

**What doesn't work:** Solo work for extended periods, skipping small talk, private-only recognition, purely transactional relationships

</high_b>

<low_b label="Low Social Motivators">

- **Leave them alone** - Minimize unnecessary check-ins
- **Written communication** - Email/async over meetings
- **Private recognition** - Public praise is uncomfortable
- **Thoughtful gifts** - A useful book means more than "great job"
- **Quality 1:1 time** - Meaningful conversations over group settings
- **Focus time protection** - No unnecessary interruptions

**What doesn't work:** Frequent check-ins, group meetings, public praise, forced social events

</low_b>

<high_c label="High Patience Motivators">

- **Advance notice** - Of changes, meetings, new projects
- **Meeting agendas** - Sent in advance, no surprises
- **One topic per meeting** - Multi-topic meetings are stressful
- **Protected focus time** - Shield from interruptions
- **Predictable schedules** - Same routine, same environment
- **Written checklists** - Structured approaches to follow
- **28-minute rule** - Respect their recovery time after interruptions

**What doesn't work:** Last-minute changes, frequent pivots, multi-topic meetings, constant interruptions

</high_c>

<low_c label="Low Patience Motivators">

- **Variety** - Keep them busy, load them up
- **Changing environments** - Thrive in consistent pivots
- **Movement** - Mental or physical in their day
- **Fires to fight** - Creative problems to solve
- **DEADLINES** - Critical motivator - put in email subject lines
- **Multiple projects** - Allow switching between tasks
- **Quick wins** - Short-term goals they can complete fast

**What doesn't work:** Monotony, long-term projects without milestones, no deadlines, forced focus on single tasks

</low_c>

<high_d label="High Conformity Motivators">

- **Don't make it personal** - Frame as process improvement, not personal failure (they're already wearing it)
- **Training opportunities** - The currency is knowledge (conferences, CEUs, certifications)
- **Structured environment** - Accountable, with enforced standards
- **Recognition when deserved** - But ONLY if deserved. Don't compliment if it's not great; they know.
- **Fair, justified pay** - Based on education, experience, market rates - give them the details
- **Trust** - Huge word for high Ds. Don't break it.
- **SOPs and documentation** - Railroad tracks to stay on

**What doesn't work:** Personal criticism, unearned praise, arbitrary decisions, broken commitments, chaotic environments

</high_d>

<low_d label="Low Conformity Motivators">

- **Creative problems** - Give them something to figure out
- **Room to run** - Freedom from too much structure and rules
- **Options** - Don't box them in, offer choices
- **Pick your battles** - Focus on the 3 things that financially move the needle
- **Big picture focus** - Don't drown in details
- **Innovation opportunities** - Space to experiment

**What doesn't work:** Too many rules, excessive structure, detail-heavy work, micromanagement, rigid processes

</low_d>

</motivators_by_trait>

<communication_styles>

| Trait | Communication Approach |
|-------|------------------------|
| High A | Bullet points, ROI focus, outcomes not process, let them "own" ideas |
| Low A | Clear direction, specific feedback, collaborative framing |
| High B | Build relationship first, verbal processing time, public recognition |
| Low B | Written communication, private recognition, respect their processing time |
| High C | Advance notice, agendas, one topic at a time, protect focus |
| Low C | Deadlines in subject line, variety, quick transitions |
| High D | Data and details, justify decisions, earn trust, don't make personal |
| Low D | Big picture first, options, creative framing |

</communication_styles>

<confidence_recovery>

When someone's confidence is shaken, recovery method depends on their leading confidence trait:

| Confidence Source | Recovery Strategy |
|-------------------|-------------------|
| High A (Inner self-confidence) | Stack easy wins - get back in the winner's circle |
| High B (Social confidence) | Relationship reconnection - rebuild social bonds |
| High D (Knowledge confidence) | Acquire more knowledge - training, certifications |

</confidence_recovery>

---

## Reference: Patterns Archetypes

<overview>

Culture Index identifies 19 distinct behavioral patterns based on the configuration of A, B, C, D traits. The interaction between traits reveals more than individual positions.

</overview>

<common_archetypes>

| Archetype | Pattern | Description | Typical Roles |
|-----------|---------|-------------|---------------|
| Visionary/Architect | High A, Low C, Low D | Big-picture, fast-paced, dislikes details. Best system builders when also high D. | CEO, Entrepreneur, Founder |
| Rainmaker/Persuader | High A, High B, Low C | Aggressive, charming, fast. Closes deals, builds relationships. | Sales Hunter, BD, Account Executive |
| Scholar/Specialist | Low B, High C, High D | Introverted, patient, detail-oriented. Deep expertise. | Engineer, CFO, Analyst |
| Accommodator | Low A, High B, High C | Team player, patient, people-focused. Service orientation. | HR, Customer Success |
| Debater | High B, Low A, Low D | Charming, non-conforming, unfiltered. Good storyteller. | Sales (relationship), Creative |
| Technical Expert | Low A, Low B, Low C, High D | Efficient specialists. Fast-moving detail people. | Security, QC, Ops |
| Craftsman | Low A, Low B, High C, High D | Patient, precise executors. Expert taskmasters. | Finance, Compliance |
| Socializer | Low A, High B, High C, Low D | Go along, get along. Team-focused, people-focused, slowing down. | Support, HR |
| Philosopher | High A, Low B, High C | Patient, analytical thinkers. Independent contemplation. | Strategy, Research |
| Administrator | Moderate across traits | Versatile generalists. Can adapt to many situations. | Operations, General Management |

</common_archetypes>

<trait_combinations>

Notable combinations and their implications:

| Combination | Name | Behavior |
|-------------|------|----------|
| High A + Low D | **Greatest Risk Takers** | Aggressive risk-taker without brakes. Gas pedal only. Most independent people (two types of independence combined). |
| Low A + High D | **Most Risk Averse** | Conservative, careful, will never cut corners. Bottom-line protectors. |
| Low A + High B | Collaborative Leader | Servant leadership, great team builder, may avoid necessary conflict |
| Low B + High C | "Leave Me Alone x2" | Strongly prefers solitary, focused work. Double introversion signal. |
| High B + Low C | Verbal Sprayer | Talks fast, often, many topics. Processing out loud rapidly. |
| High A + Low B | Results Driver | Drives results without regard for feelings. May seem low EQ. |
| High D + Low A | Perfectionist Follower | Executes exactly as instructed, never cuts corners. Good at optimizing existing processes. |
| High A + High D | Process Builder | Forward-thinking AND detail-oriented. Can build NEW systems and processes. (Architects, Scholars, Technical Experts) |
| Low C + Low D | Double Error Risk | Moving fast (Low C) + not checking work (Low D) = high error rate. Needs systems to catch mistakes. |
| Low C + High D | Wound Tight | Impatient AND perfectionist. High strung, worrisome, feels everything is urgent and must be perfect. |

</trait_combinations>

<task_vs_people>

A vs B determines task vs people orientation:

| Pattern | Meaning |
|---------|---------|
| A > B | Values tasks over people; will push through to get results |
| B > A | Values people over tasks; prioritizes harmony and relationships |

</task_vs_people>

<strategic_cross>

**Low C + Low D = "Maverick" or "Change Agent"**

- Fast-moving (Low C) and unconcerned with rules (Low D)
- Natural agents of change and innovation
- May cause disruption
- Good for turnarounds, startups, transformations

</strategic_cross>

<technical_stack>

**High C + High D = "Specialist" or "Operator"**

- Patient (High C) and precise (High D)
- Will ensure work is done correctly, won't rush
- May resist change
- Good for compliance, quality, operations

</technical_stack>

<chameleon_pattern>

**All four primary dots near the arrow = "Chameleon"**

- Statistically average across all traits
- Unpublished pattern making up less than 0.57% of population
- Maximum flexibility but may lack strong, predictable drivers
- Hard to pin down - adapts to situations

</chameleon_pattern>

<pattern_width>

The spread between traits matters as much as individual positions.

**Wide pattern** (traits spread far apart):
- More extreme, predictable behaviors
- Stronger drivers
- Easier to predict day-to-day behavior

**Narrow pattern** (traits clustered):
- More moderate, flexible behaviors
- Less predictable
- Can adapt to situations

Two people can have identical A positions but vastly different overall patterns due to B/C/D spread.

</pattern_width>

<pattern_fit_warning>

**Flight risk signal**: When someone's Job behaviors show the opposite of their Survey traits.

Example: Architect pattern (High A, Low C, Low D) → Socializer in job (Low A, High B, High C, Low D)
- All dots flipped to opposite side
- This is imminent flight risk
- Something must change or they will leave

</pattern_fit_warning>

<role_fit_questions>

When determining what pattern fits a role, ask:

| Question | Left Answer | Right Answer | Relevant Trait |
|----------|-------------|--------------|----------------|
| Is this role more **macro** or **micro**? | Micro (details, execution) | Macro (big picture, strategy) | A trait |
| Is this position more about **people skills** or **problem solving**? | Problem solving | People skills | B trait |
| How much **repetition** is in this role? | Low repetition, chaos, variety | High repetition, stability, predictable | C trait |

**Use these to match patterns:**
- Macro + people + variety = High A, High B, Low C (Rainmaker/Persuader)
- Micro + problem solving + stability = Low A, Low B, High C, High D (Craftsman/Specialist)
- Macro + problem solving + stability = High A, Low B, High C, High D (Scholar/Architect)

</role_fit_questions>

<identifying_pattern>

**Quick interpretation method:**

1. Find the farthest dot from the normative line (highest deviation)
2. Identify which range it falls into:
   - ±2 centiles = "somewhat" or "very" (one standard deviation)
   - ±4 centiles = "extremely" (entering six-sigma territory)
3. Use word descriptors from the appropriate column

**Example**: D trait is 4.5 centiles right of the norm = "extremely conforming perfectionist, precise, cautious, accurate."

**For dots on or near the line** (±0.5): "Situationally, depending on your level of comfort and experience, you might be [right-side words] or [left-side words]."

</identifying_pattern>

---

## Reference: Primary Traits

<overview>

The four primary traits (A, B, C, D) are the main drivers of behavior. The relationship BETWEEN dots is often more important than individual positions. All interpretations are relative to the red arrow (population mean).

</overview>

<trait name="A" color="maroon" label="Autonomy">

Measures **mental initiative** (think and start on their own) and **inner self-confidence** (belief in self that they will win regardless of circumstance).

<high_a side="right">

**Characteristics:**
- Self-confident, self-starter, self-motivated, self-driven, self-reliant
- Assertive, aggressive, ruthlessly competitive
- Future-focused and strategic - sees the full 360-degree lay of the land
- Prioritizes time based on ROI - trades in time and money
- Willing to confront - conflict is just a means to an end
- "Enough equals more" - always raises the bar, never satisfied
- Opinionated - typically thinks they're the smartest person in the room

**Challenges:**
- Single hardest trait to employ - they work for "me, Inc." first
- "You are only RENTING high A's" - need mutually beneficial partnership
- Kryptonite is people - people will consistently disappoint them
- May take matters into their own hands when others "move too slow"
- Can LEAD (vision, strategy) but struggle to MANAGE (routine operations)

**Best Fit Roles:** Leadership, sales, entrepreneurship, strategy

**Communicating with High A's:**
- Use bullet points focused on ROI - they won't read walls of text
- "Bake me a cake" approach: Give outcomes, not step-by-step instructions
- Get buy-in through questions, not statements - let them "own" the idea
- Prefer variable compensation (bonus, equity, commission) over fixed salary

**Who High A's Respect:**
- People ahead of them (mentors, more successful peers)
- People with inner confidence who aren't threatened by them
- NOT people who capitulate or seem "weak"

</high_a>

<low_a side="left">

**Characteristics:**
- Helpful, supportive, service-oriented, accommodating, peaceful
- Servant leadership orientation - "what do WE need to win"
- Tactical and present-focused (vs high A's strategic future-focus)
- Excel at execution once direction is clear
- Team-oriented - finds genuine satisfaction in supporting others' success
- Prefers direction before acting - doesn't initiate on their own

**Challenges:**
- Indecisive with NEW challenges - need frameworks, precedents, or direction
- Conflict averse - may agree to things they don't support to keep peace
- May be put in leadership roles they didn't seek (and will burn out)
- Can appear passive when waiting for direction

**Best Fit Roles:** Support roles, customer service, collaborative teams, execution

**Managing Low A's:**
- Provide specific praise, not general ("Great job on the Johnson proposal")
- Offer consistent, predictable compensation over variable bonuses
- Give clear frameworks for novel decisions
- Don't interpret conflict avoidance as agreement - probe for true concerns

</low_a>

<leadership_styles>

| Style | Trait | Mindset | Characteristics |
|-------|-------|---------|-----------------|
| ABL (Action Based Leadership) | High A | "What do I need to win?" | Self-directed, competitive, drives from front |
| WPL (Wolf Pack Leadership) | Low A | "What do WE need to win?" | Collaborative, consensus-building, servant leadership |

Neither is better - depends on context. High-growth/turnaround may need ABL. Stable/complex operations may benefit from WPL.

</leadership_styles>

</trait>

<trait name="B" color="yellow" label="Social Ability">

Measures need for social interaction and persuasion.

<high_b side="right">

**Characteristics:**
- Dual nature: Social competence (skill to connect) + need for acceptance (drive to connect)
- Verbal processors - "think out loud." First statement isn't final position.
- Relational equity required - must build relationship BEFORE discussing tasks
- Culture builders - create positive atmosphere, the "fun part of the zoo"
- Energized by people, drained by isolation
- Fear: rejection, exclusion, being disliked

**Managing High B's:**
- Words of affirmation are primary currency - verbal praise, public recognition
- Allow small talk - it's not wasted time, it's relationship investment
- Include them in group activities and social events
- Don't isolate them with solo work for extended periods
- Note: With Low C, they become "sprayers" - lots of fast talking

**Best Fit Roles:** Sales, PR, public speaking, management, team building

</high_b>

<low_b side="left">

**Characteristics:**
- "There for the work" - not for relationships. Socializing feels like a tax.
- Prefer solitary or small-group work environments
- Process internally before speaking - silence does not equal disengagement
- Analytical, reserved, focused - ideal for deep work
- Fear: being forced into social situations, public attention

**Managing Low B's:**
- Leave them alone - minimize unnecessary check-ins
- Email/async preferred over meetings - let them process in writing
- Private recognition - public praise is uncomfortable
- Thoughtful gifts > verbal praise (a useful book means more than "great job")
- Quality time: meaningful 1:1 > group settings
- Don't mistake quiet for disengagement or unhappiness

**Best Fit Roles:** Engineering, accounting, research, coding, analysis

</low_b>

</trait>

<trait name="C" color="blue" label="Pace/Patience">

Measures patience, urgency, and rate of motion. **Force multiplier** - intensifies or calms how other traits manifest.

**Analogy:** High C = scheduled surgeons (focused, present, deliberate). Low C = emergency room operators (spinning plates, time-sensitive, variety).

<high_c side="right">

**Characteristics:**
- Patient, steady, calm, consistent, resists sudden change
- Extended focus capability - can concentrate for long periods
- **28-minute recovery** from interruptions - protect their focus time
- Sequential, systematic processing - one thing at a time
- Checklist oriented - give structured approaches, they'll follow exactly
- Consistency preferred - same desk, schedule, tools
- Patient with complexity - will work through problems methodically

**Managing High C's:**
- Send meeting agendas in advance - no surprises
- One meeting, one topic - multi-topic meetings are stressful
- Protect them from frequent interruptions
- Provide predictable schedules and environments
- Give advance notice of changes

**Best Fit Roles:** Administrative work, long-term projects, routine tasks, operations

</high_c>

<low_c side="left">

**Characteristics:**
- Impatient, quick, fast, restless, multifocused, intense, urgent
- Zero to 60 immediately - instant attention ramp-up
- Short attention span - a bit of ADD tendency
- Change agents - open to change primarily because they get bored easily
- Struggle staying in the moment - constantly thinking "what's next?"
- If D is not high: procrastination ("if I wait to the last minute, it only takes a minute")
- Overextension/over-scheduling - overestimate how much they can accomplish

**Pluses:**
- Create urgency and drive results (GSD - get stuff done)
- Good with variety and pivots - pivot faster than high C
- Good under pressure/stress (even if they look animated/hair on fire)
- Firefighters - when attention turns to something, they're fully engaged

**Minuses:**
- Can spin up others unnecessarily - disruptive when situation doesn't warrant urgency
- Interrupt others ("Did you get that email? Did you get back to me?")
- Moving fast leads to errors (especially without high D to catch mistakes)
- Get bored easily - often over-promoted because "can I help?" is misread as ambition

**Low C Motivators:**
- Variety - keep them busy, load them up
- Evolving, changing environments - thrive in consistent pivots
- Movement (mental or physical) in their day
- Fires to fight - creative problems to solve
- **DEADLINES** - critical motivator. Put deadlines in email subject lines.

**Best Fit Roles:** Startups, emergency response, rapid-fire environments

</low_c>

<c_as_modifier>

C acts as a **force multiplier** for other traits:

**Low C (Intensifier):** Adds urgency and "violence" to other traits
- High B + Low C = Proactively social, "buzzing around," many shorter conversations
- High D + Low C = Mistakes get called out QUICKLY
- High A + Low C = Aggressive, impatient driver who demands results NOW

**High C (Sedative):** Calms and steadies other traits
- High B + High C = Better listener, deeper conversations
- High D + High C = Notices issues but approaches steadily, might fix it themselves quietly
- High A + High C = Strategic and determined, but willing to wait for the right moment

</c_as_modifier>

</trait>

<trait name="D" color="green" label="Conformity">

Measures attention to detail, rules, and structure. **Third confidence trait** - confidence rooted in knowledge and competency.

<high_d side="right">

**Characteristics:**
- Accurate, careful, detail-oriented, historical, specific, micro-organized
- **Need SOPs** - must lay "railroad tracks" for them to stay on track
- Won't feel comfortable doing anything until they've mastered it - "no" until "know"
- Look back to see what the measurement is before acting (historical mindset)
- High levels of self-discipline and self-management
- Their own worst critic - take themselves "behind the woodshed" when they make mistakes
- Long memories - remember nitpicky particulars, including who failed them in 2018
- Currency they trade in is knowledge - all the certifications

**Pluses:**
- Reliable, dependable, consistent quality
- Executors and finishers - sustain and maintain things, circle back around
- Highly accountable - will do what they say
- Risk mitigation experts - defenders of what's right, defenders of the truth
- Good delegation targets - when you delegate to them, certainty they'll do it well (if properly defined)
- Quality control, compliance, operational excellence backbone

**Minuses:**
- Lost without SOPs - struggle outside the box, inflexible, rigid
- Uncomfortable when asked to do something beyond normal role
- Don't naturally delegate - hard to trust others, becomes bottleneck
- Long memories can lead to grudge-holding
- Critical - find the flaw, focus on what's wrong (even when 9 of 10 things are right)
- Judgmental - "I give 110%, you should too"
- Thin-skinned and blame-avoidant when confronted personally

**High D Motivators:**
- Don't make it personal - frame as process improvement, not personal failure
- Training and learning opportunities - the currency is knowledge
- Structured, accountable environment
- Recognition for hard work - but ONLY if deserved
- Fair pay based on education, experience, market rates
- Trust - huge word for high Ds. Don't break it.

**Best Fit Roles:** Finance, compliance, quality control, legal, security, ops

</high_d>

<low_d side="left">

**Characteristics:**
- Non-conforming, out of the box, free-spirited, conceptual, casual, flexible
- Don't need historical context or proof of concept to experiment
- Every day is a new day - shorter recall, don't hold on to yesterday
- Really good at getting things 80% done, then need others for maintenance/finishing
- Unfiltered - don't always mind their p's and q's
- Rules are meant to be interpreted, bent, broken

**Pluses:**
- Willingness to delegate (opposite of high D)
- Flexible and resilient - don't see limitations
- Creative brainstorming partners - look at things in non-traditional ways
- Good with innovation and experimentation
- Shorter recall = resiliency (get kicked in the mouth today, blank slate tomorrow)

**Minuses:**
- Inconsistent follow-through - out of sight, out of mind
- Forgetful - need systems/automation to catch things
- Sloppy execution when disinterested
- Don't always stay in their lane - don't see lanes as much
- Won't circle back on finer details without systems

**Low D Motivators:**
- Creative problems to solve - give them something to figure out
- Room to run - freedom from too much structure and too many rules
- Options - don't box them in, offer choices
- Pick your battles - focus on the 3 things that financially move the needle

**Best Fit Roles:** Strategy, creative roles, R&D, visionary leadership

</low_d>

<key_relationship>

"The A starts, the D finishes."

- A initiates and drives; D executes and completes
- Building NEW processes: High A + High D = architects, scholars, technical experts
- Optimizing EXISTING processes: Low A + High D = specialists

**Independence Types:**
- High A independence: "I have a goal, I have a plan, I don't care if anyone follows me"
- Low D independence: "Don't control me. Don't tell me not to do something."
- Most independent people: High A + Low D
- Greatest risk takers: High A + Low D
- Most risk averse: Low A + High D

</key_relationship>

</trait>

---

## Reference: Secondary Traits

<overview>

Secondary traits (EU, L, I) supplement the primary traits. L and I are unique: they use **absolute values** and CAN be compared directly between people.

</overview>

<trait name="EU" label="Energy Units">

Measures **mental stamina** - how long a person can work before needing a short 5-10 minute mental break to recharge. If they don't take that break, they operate in a mentally fatigued state (frustrated, lacking clarity, missing things).

<important_note>
EU is NOT:
- Physical energy
- Work ethic
- Intelligence or capability
</important_note>

<interpretation>

| Range | Label | Management Approach |
|-------|-------|---------------------|
| 0-10 | **Potentially avoidant** | Flag for review - may need hand-scoring |
| 11-19 | Lower EU | Prioritize important work first thing in morning, earlier in week |
| 20-40 | Most common for executives | Regular short breaks throughout day (4-5 per 10-hour day) |
| 41-60 | Above average | Longer sustained focus possible |
| 61-80 | High ("energizer bunnies") | As mentally fresh at 9pm as 9am; watch for late-night emails |

</interpretation>

<avoidant_responses>

If EU is 0-10, flag for review. Common causes:
1. Didn't read instructions - selected one word per column
2. Interrupted before completing
3. Took survey in non-native language
4. Overly guarded/skeptical - trust issue ("How will this be used against me?")
5. Below 8th grade reading level

**If multiple direct reports return avoidant:** Look at the manager - "Why do you have a culture of fear or mistrust?"

</avoidant_responses>

<energy_drain>

**Critical insight**: Living in your TOP graph (natural traits) does NOT drain EU - it's effortless.

What DRAINS EU is behavior modification - when your bottom graph differs from your top graph, you're expending mental energy to "act" differently than you're wired.

</energy_drain>

<utilization_formula>

**Compare EU between Survey and Job using:**

```
Energy Utilization = (Job EU / Survey EU) × 100
```

| Utilization | Signal | Meaning |
|-------------|--------|---------|
| 70-130% | Healthy | Sustainable workload alignment |
| >130% | **STRESS** | Good stress (self-induced caring) OR bad stress (overutilization). Burnout risk. |
| <70% | **FRUSTRATION** | Disengaged, apathetic, going through motions, underutilized, bored. **Flight risk.** |

**Example**: Survey EU = 41, Job EU = 31. Utilization = 31/41 = 75%. Approaching check-engine-light zone for frustration/disengagement.

</utilization_formula>

<stress_types>

**>130% Stress Types:**
- **Good stress (self-induced)**: "I really care about this company, I love what I do" - but still potential for burnout and health issues if sustained 3-6 months
- **Bad stress (overutilization)**: Loaded with too much work, or work requires too much behavior modification

**<70% Frustration:** Work doesn't quite fit them. Might have a lot to do, but the work doesn't match their traits. Not punching eject yet, but getting close.

</stress_types>

<resurvey_cadence>

Job behaviors should be resurveyed biannually. Don't make decisions on stale data (18+ months old).

</resurvey_cadence>

</trait>

<trait name="L" color="purple" label="Logic">

Measures how a person receives and processes new information - the first filter when receiving new information, especially sensitive information. **Also measures self-esteem** - the lower the logic, the lower the self-esteem.

<important_note>
L uses **absolute values**. You CAN compare L scores directly between people.
Logic 8 means "High Logic" regardless of arrow position.
</important_note>

<interpretation>

| Score | Label | Behavior |
|-------|-------|----------|
| 0-2 | Low Logic | Emotional, sensitive, heartfelt, passionate; emotions filter information first |
| 3-7 | Normative | Emotionally available competency - balanced head and heart working in tandem |
| 8-10 | High Logic | Rational, logical, black/white; high emotional compartmentalization; detach in the moment |

</interpretation>

<low_logic range="0-2">

**Characteristics:**
- Lack emotional control in the moment - first response may be chemically induced, not fact-based
- Introduces unpredictability - irrational in-the-moment decision making
- Can have high self-confidence (A) but low self-esteem simultaneously

**Benefit:** Emotional attachment can drive extraordinary results (Olympians, entrepreneurs)

**Managing Low Logic:**
- Don't say "calm down"
- Create distance - "Let's talk at 4pm today"
- They'll meet you as an adult once emotions settle

</low_logic>

<normative_logic range="3-7">

- Natural EQ - emotionally available but not governed by emotions
- 3-4: Lead more heart than head, but not disconnected from rational thought
- 5: Dead smack in the middle
- 6-7: Lead more head than heart

</normative_logic>

<high_logic range="8-10">

**Characteristics:**
- Clear thinking when things are hitting the fan
- Complete separation from emotions; tough situations don't phase them

**Watch:** Can come across cold, detached, insensitive. "Toughens the dots up."

**Combination note:** High B + Logic 10 = outgoing but can say insensitive things (a bit of an "ahole factor")

**Combination note:** Low B + Logic 10 = "sensitivity is not going to be your strong suit"

</high_logic>

<job_behavior_signal>

When a high logic person (9-10) drops their logic in job behaviors (to 4-5), it's almost always an indication of **people-related challenges**. They're trying to be more emotionally open because they've been told they're too cold/detached.

</job_behavior_signal>

</trait>

<trait name="I" color="cyan" label="Ingenuity">

Measures raw inventiveness and spatial reasoning - how detached from reality someone thinks. "Clever or original thinking."

<important_note>
I uses **absolute values**. You CAN compare I scores directly between people.
Ingenuity 8 means "High Ingenuity" regardless of arrow position.
</important_note>

<interpretation>

| Score | Label | Behavior |
|-------|-------|----------|
| 0-2 | Low Ingenuity | **Most common score**. Linear, practical, grounded. If it doesn't exist, need to touch/see/feel/experience it. |
| 3-6 | Occasional | Occasional moments of inspiration - looking at things in a more layered, original way. |
| 7-10 | High Ingenuity | Ingenious, inventive, eccentric, multidimensional thinkers. Detached from reality. |

</interpretation>

<the_pen_test>

Ask what a pen is:
- Low ingenuity (0-2): "It's a pen."
- High ingenuity (9): "It's how we pump oil in Texas. A window into another world. Executive decision-making. A weapon."
- Low ingenuity response to high ingenuity: "No, moron. It's a freaking pen."

</the_pen_test>

<high_ingenuity range="7-10">

**Where it helps:**
- New business lines and revenue opportunities
- Creative proposals
- R&D
- Creative marketing
- Don't see limitations - experimental, try unconventional approaches

**Watch for:**
- Can be distracting with constant weird ideas
- Not all ideas monetizable - need A trait to commercialize
- Especially disruptive if in position to initiate ideas

</high_ingenuity>

<low_ingenuity range="0-2">

**Most common score.** Not a negative - indicates practical, grounded thinking.

**Note:** Single-tail IQ correlation. High I → likely high IQ. However, low I does NOT mean low IQ - plenty of certified geniuses have low ingenuity scores.

</low_ingenuity>

<job_behavior_signal>

When a low ingenuity person raises their ingenuity in job behaviors, the traditional approach is not working. They're trying to figure out a more inventive way to handle something they're stuck on.

</job_behavior_signal>

</trait>

<confidence_sources>

Culture Index identifies three sources of confidence, each tied to a trait:

| Trait | Confidence Source | Description |
|-------|-------------------|-------------|
| High A | Inner self-confidence | Belief in self regardless of circumstances. "I believe I'll win." Can be in a hitting slump and picks themselves up by bootstraps. |
| High B | Social confidence | Confidence from ability to influence and connect. If people don't respond, starts questioning self. High A + High B can fall back on A's self-confidence. |
| High D | Knowledge/Expertise confidence | "If I know it, I know it." Confidence rooted in mastery and competency. Great vetters. |

**Confidence recovery:**
- High A's recover by getting back in the winner's circle (stack easy wins)
- High B's recover through relationship reconnection
- High D's recover through acquiring more knowledge/training

</confidence_sources>

---

## Reference: Team Composition

<overview>

Every team needs the right mix of Gas, Brake, and Glue for its current needs. The ratio depends on the season of business, the function, and current gaps.

</overview>

<gas_brake_glue>

| Role | Trait | Function | Too Little | Too Much |
|------|-------|----------|------------|----------|
| **Gas Pedal** | High A | Growth, risk-taking, innovation, driving results | Stagnation, waiting around, no decisive action | Chaos, recklessness, burnout |
| **Brake Pedal** | High D | Risk aversion, quality control, compliance, finishing | Erosion, mistakes, lawsuits, quality issues | Paralysis, perfectionism, can't ship |
| **Glue** | High B | Relationships, morale, optimism, "fun part of the zoo" | Root canal culture, morale problems, no fun | All talk, no action, groupthink |

</gas_brake_glue>

<diagnostic_questions>

| Symptom | Likely Gap |
|---------|------------|
| Lacking growth, decisive action, or strategic problem-solving | Not enough high A (Gas) |
| Morale sucks, culture feels like a root canal, no fun | Not enough high B (Glue) |
| Quality erosion, mistakes, compliance issues | Not enough high D (Brake) |
| Chaos, recklessness, burnout, no follow-through | Too much Gas, not enough Brake |
| Paralysis, perfectionism, can't ship anything | Too much Brake, not enough Gas |
| All talk, no action, groupthink, avoiding hard decisions | Too much Glue, not enough Gas |

</diagnostic_questions>

<business_season>

The ideal balance depends on what the team/company needs now:

| Season | Priority | What You Need |
|--------|----------|---------------|
| **High-growth / Turnaround** | Gas | Drivers and risk-takers. High A's who will push through. |
| **Consolidation / Stability** | Brake | Quality and consistency. High D's who ensure nothing breaks. |
| **Culture Building** | Glue | Relationship builders. High B's who create positive environment. |
| **Complex Operations** | Brake + Glue | Precision and collaboration. Need both quality control and team cohesion. |
| **Innovation / R&D** | Gas + Low D | Risk-takers who experiment. High A + Low D = willingness to fail fast. |
| **Compliance-Heavy** | Brake | High D's who follow rules precisely. Risk aversion is a feature. |

</business_season>

<function_needs>

Different functions naturally need different balances:

| Function | Primary Need | Why |
|----------|-------------|-----|
| Sales | Gas (High A) | Drive results, close deals, push through objections |
| Engineering | Brake (High D) | Quality code, attention to detail, systematic approach |
| Customer Success | Glue (High B) | Relationships, retention, advocacy |
| Operations | Brake (High D) | Consistency, reliability, process adherence |
| Marketing (Creative) | Gas + Low D | Innovation, experimentation, bold ideas |
| Finance | Brake (High D) | Accuracy, compliance, risk management |
| HR | Glue (High B) | Culture, relationships, employee advocacy |
| Executive Team | Balanced | Need all three: drive (Gas), quality (Brake), culture (Glue) |

</function_needs>

<c_trait_team_impact>

C (Pace/Patience) affects team dynamics beyond Gas/Brake/Glue:

| Team Pattern | Implication |
|--------------|-------------|
| Mostly Low C | Fast-moving, urgent, may create unnecessary chaos. Need someone to slow things down occasionally. |
| Mostly High C | Steady, patient, but may resist change. Need someone to push urgency when required. |
| Mixed C | Natural tension between fast and slow movers. Can be healthy friction if managed. |

**Considerations:**
- If major projects require urgent pivots → need some Low C
- If major projects require sustained focus → need some High C
- Pairing Low C with High C can create complementary partnerships (one pushes, one steadies)

</c_trait_team_impact>

<a_vs_b_team_balance>

Team-wide task vs people orientation:

| Pattern | Implication |
|---------|-------------|
| A > B (most people) | Task-focused, results-driven. May neglect relationships and culture. Risk of burnout and turnover. |
| B > A (most people) | People-focused, harmonious. May avoid tough decisions and underperform on results. |
| Mixed A/B | Healthy tension. Task drivers balanced by relationship builders. |

</a_vs_b_team_balance>

<hiring_to_fill_gaps>

When hiring to fill a gap, specify the ideal profile:

**Gap: Not enough Gas**
```
Ideal Hire Pattern:
- A: High (right of arrow) - drives results, takes initiative
- B: Any (based on role) - depends on whether role is people-facing
- C: Low preferred - urgency and pace
- D: Any (consider existing Brake capacity)
```

**Gap: Not enough Brake**
```
Ideal Hire Pattern:
- A: Any - Low A + High D = specialist optimizer
- B: Any (based on role)
- C: High preferred - patience for detailed work
- D: High (right of arrow) - quality focus, follow-through
```

**Gap: Not enough Glue**
```
Ideal Hire Pattern:
- A: Any - Low A + High B = collaborative culture builder
- B: High (right of arrow) - relationship builder
- C: Any (based on role pace)
- D: Any
```

</hiring_to_fill_gaps>

<conflict_pairs>

Trait combinations that create friction on teams:

| Combination | Friction Point | Mitigation |
|-------------|----------------|------------|
| High A vs High A | Power struggles, both want to lead | Clear role delineation, separate domains |
| High A vs Low A | Independence vs collaboration | High A provides direction, respects Low A's process |
| High B vs Low B | Social needs mismatch | High B allows Low B alone time; Low B participates minimally |
| High C vs Low C | Pace/urgency mismatch | Low C respects focus time; High C accepts some urgency |
| High D vs Low D | Detail orientation clash | High D accepts "good enough"; Low D follows through |
| High D vs High D | Both perfectionist, both critical | Can be excellent partnership if aligned on standards |

</conflict_pairs>

<remote_team_considerations>

For remote/distributed teams:

- **Glue is even more critical** - Without casual office interactions, High B's are essential for maintaining culture
- **Low B's thrive** - Remote work is natural for those who prefer isolation
- **Low C's may struggle** - Harder to get immediate responses, may feel urgency isn't matched
- **High D's need clear processes** - More documentation, explicit SOPs for remote work

</remote_team_considerations>
