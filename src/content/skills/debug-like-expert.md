---
title: "Debug Like Expert"
description: "Deep analysis debugging mode for complex issues. Activates methodical investigation protocol with evidence gathering, hypothesis testing, and rigorous verification. Use when standard troubleshooting fails or when issues require systematic root cau..."
category: "development"
source: "community"
author: "Community"
tags: ["debug", "like"]
date: 2026-03-20
---

<objective>
Deep analysis debugging mode for complex issues. This skill activates methodical investigation protocols with evidence gathering, hypothesis testing, and rigorous verification when standard troubleshooting has failed.

The skill emphasizes treating code you wrote with MORE skepticism than unfamiliar code, as cognitive biases about "how it should work" can blind you to actual implementation errors. Use scientific method to systematically identify root causes rather than applying quick fixes.
</objective>

<context_scan>
**Run on every invocation to detect domain-specific debugging expertise:**

```bash
# What files are we debugging?
echo "FILE_TYPES:"
find . -maxdepth 2 -type f 2>/dev/null | grep -E '\.(py|js|jsx|ts|tsx|rs|swift|c|cpp|go|java)$' | head -10

# Check for domain indicators
[ -f "package.json" ] && echo "DETECTED: JavaScript/Node project"
[ -f "Cargo.toml" ] && echo "DETECTED: Rust project"
[ -f "setup.py" ] || [ -f "pyproject.toml" ] && echo "DETECTED: Python project"
[ -f "*.xcodeproj" ] || [ -f "Package.swift" ] && echo "DETECTED: Swift/macOS project"
[ -f "go.mod" ] && echo "DETECTED: Go project"

# Scan for available domain expertise
echo "EXPERTISE_SKILLS:"
ls ~/.claude/skills/expertise/ 2>/dev/null | head -5
```

**Present findings before starting investigation.**
</context_scan>

<domain_expertise>
**Domain-specific expertise lives in `~/.claude/skills/expertise/`**

Domain skills contain comprehensive knowledge including debugging, testing, performance, and common pitfalls. Before investigation, determine if domain expertise should be loaded.

<scan_domains>
```bash
ls ~/.claude/skills/expertise/ 2>/dev/null
```

This reveals available domain expertise (e.g., macos-apps, iphone-apps, python-games, unity-games).

**If no expertise skills found:** Proceed without domain expertise (graceful degradation). The skill works fine with general debugging methodology.
</scan_domains>

<inference_rules>
If user's description or codebase contains domain keywords, INFER the domain:

| Keywords/Files | Domain Skill |
|----------------|--------------|
| "Python", "game", "pygame", ".py" + game loop | expertise/python-games |
| "React", "Next.js", ".jsx/.tsx" | expertise/nextjs-ecommerce |
| "Rust", "cargo", ".rs" files | expertise/rust-systems |
| "Swift", "macOS", ".swift" + AppKit/SwiftUI | expertise/macos-apps |
| "iOS", "iPhone", ".swift" + UIKit | expertise/iphone-apps |
| "Unity", ".cs" + Unity imports | expertise/unity-games |
| "SuperCollider", ".sc", ".scd" | expertise/supercollider |
| "Agent SDK", "claude-agent" | expertise/with-agent-sdk |

If domain inferred, confirm:
```
Detected: [domain] issue → expertise/[skill-name]
Load this debugging expertise? (Y / see other options / none)
```
</inference_rules>

<no_inference>
If no domain obvious, present options:

```
What type of project are you debugging?

Available domain expertise:
1. macos-apps - macOS Swift (SwiftUI, AppKit, debugging, testing)
2. iphone-apps - iOS Swift (UIKit, debugging, performance)
3. python-games - Python games (Pygame, physics, performance)
4. unity-games - Unity (C#, debugging, optimization)
[... any others found in build/]

N. None - proceed with general debugging methodology
C. Create domain expertise for this domain

Select:
```
</no_inference>

<load_domain>
When domain selected, READ all references from that skill:

```bash
cat ~/.claude/skills/expertise/[domain]/references/*.md 2>/dev/null
```

This loads comprehensive domain knowledge BEFORE investigation:
- Common issues and error patterns
- Domain-specific debugging tools and techniques
- Testing and verification approaches
- Performance profiling and optimization
- Known pitfalls and anti-patterns
- Platform-specific considerations

Announce: "Loaded [domain] expertise. Investigating with domain-specific context."

**If domain skill not found:** Inform user and offer to proceed with general methodology or create the expertise.
</load_domain>

<when_to_load>
Domain expertise should be loaded BEFORE investigation when domain is known.

Domain expertise is NOT needed for:
- Pure logic bugs (domain-agnostic)
- Generic algorithm issues
- When user explicitly says "skip domain context"
</when_to_load>
</domain_expertise>

<context>
This skill activates when standard troubleshooting has failed. The issue requires methodical investigation, not quick fixes. You are entering the mindset of a senior engineer who debugs with scientific rigor.

**Important**: If you wrote or modified any of the code being debugged, you have cognitive biases about how it works. Your mental model of "how it should work" may be wrong. Treat code you wrote with MORE skepticism than unfamiliar code - you're blind to your own assumptions.
</context>

<core_principle>
**VERIFY, DON'T ASSUME.** Every hypothesis must be tested. Every "fix" must be validated. No solutions without evidence.

**ESPECIALLY**: Code you designed or implemented is guilty until proven innocent. Your intent doesn't matter - only the code's actual behavior matters. Question your own design decisions as rigorously as you'd question anyone else's.
</core_principle>

<quick_start>

<evidence_gathering>

Before proposing any solution:

**A. Document Current State**
- What is the EXACT error message or unexpected behavior?
- What are the EXACT steps to reproduce?
- What is the ACTUAL output vs EXPECTED output?
- When did this start working incorrectly (if known)?

**B. Map the System**
- Trace the execution path from entry point to failure point
- Identify all components involved
- Read relevant source files completely, not just scanning
- Note dependencies, imports, configurations affecting this area

**C. Gather External Knowledge (when needed)**
- Use MCP servers for API documentation, library details, or domain knowledge
- Use web search for error messages, framework-specific behaviors, or recent changes
- Check official docs for intended behavior vs what you observe
- Look for known issues, breaking changes, or version-specific quirks

See [references/when-to-research.md](references/when-to-research.md) for detailed guidance on research strategy.

</evidence_gathering>

<root_cause_analysis>

**A. Form Hypotheses**

Based on evidence, list possible causes:
1. [Hypothesis 1] - because [specific evidence]
2. [Hypothesis 2] - because [specific evidence]
3. [Hypothesis 3] - because [specific evidence]

**B. Test Each Hypothesis**

For each hypothesis:
- What would prove this true?
- What would prove this false?
- Design a minimal test
- Execute and document results

See [references/hypothesis-testing.md](references/hypothesis-testing.md) for scientific method application.

**C. Eliminate or Confirm**

Don't move forward until you can answer:
- Which hypothesis is supported by evidence?
- What evidence contradicts other hypotheses?
- What additional information is needed?

</root_cause_analysis>

<solution_development>

**Only after confirming root cause:**

**A. Design Solution**
- What is the MINIMAL change that addresses the root cause?
- What are potential side effects?
- What could this break?

**B. Implement with Verification**
- Make the change
- Add logging/debugging output if needed to verify behavior
- Document why this change addresses the root cause

**C. Test Thoroughly**
- Does the original issue still occur?
- Do the reproduction steps now work?
- Run relevant tests if they exist
- Check for regressions in related functionality

See [references/verification-patterns.md](references/verification-patterns.md) for comprehensive verification approaches.

</solution_development>

</quick_start>

<critical_rules>

1. **NO DRIVE-BY FIXES**: If you can't explain WHY a change works, don't make it
2. **VERIFY EVERYTHING**: Test your assumptions. Read the actual code. Check the actual behavior
3. **USE ALL TOOLS**:
   - MCP servers for external knowledge
   - Web search for error messages, docs, known issues
   - Extended thinking ("think deeply") for complex reasoning
   - File reading for complete context
4. **THINK OUT LOUD**: Document your reasoning at each step
5. **ONE VARIABLE**: Change one thing at a time, verify, then proceed
6. **COMPLETE READS**: Don't skim code. Read entire relevant files
7. **CHASE DEPENDENCIES**: If the issue involves libraries, configs, or external systems, investigate those too
8. **QUESTION PREVIOUS WORK**: Maybe the earlier "fix" was wrong. Re-examine with fresh eyes

</critical_rules>

<success_criteria>

Before starting:
- [ ] Context scan executed to detect domain
- [ ] Domain expertise loaded if available and relevant

During investigation:
- [ ] Do you understand WHY the issue occurred?
- [ ] Have you verified the fix actually works?
- [ ] Have you tested the original reproduction steps?
- [ ] Have you checked for side effects?
- [ ] Can you explain the solution to someone else?
- [ ] Would this fix survive code review?

If you can't answer "yes" to all of these, keep investigating.

**CRITICAL**: Do NOT mark debugging tasks as complete until this checklist passes.

</success_criteria>

<output_format>

```markdown
## Issue: [Problem Description]

### Evidence
[What you observed - exact errors, behaviors, outputs]

### Investigation
[What you checked, what you found, what you ruled out]

### Root Cause
[The actual underlying problem with evidence]

### Solution
[What you changed and WHY it addresses the root cause]

### Verification
[How you confirmed this works and doesn't break anything else]
```

</output_format>

<advanced_topics>

For deeper topics, see reference files:

**Debugging mindset**: [references/debugging-mindset.md](references/debugging-mindset.md)
- First principles thinking applied to debugging
- Cognitive biases that lead to bad fixes
- The discipline of systematic investigation
- When to stop and restart with fresh assumptions

**Investigation techniques**: [references/investigation-techniques.md](references/investigation-techniques.md)
- Binary search / divide and conquer
- Rubber duck debugging
- Minimal reproduction
- Working backwards from desired state
- Adding observability before changing code

**Hypothesis testing**: [references/hypothesis-testing.md](references/hypothesis-testing.md)
- Forming falsifiable hypotheses
- Designing experiments that prove/disprove
- What makes evidence strong vs weak
- Recovering from wrong hypotheses gracefully

**Verification patterns**: [references/verification-patterns.md](references/verification-patterns.md)
- Definition of "verified" (not just "it ran")
- Testing reproduction steps
- Regression testing adjacent functionality
- When to write tests before fixing

**Research strategy**: [references/when-to-research.md](references/when-to-research.md)
- Signals that you need external knowledge
- What to search for vs what to reason about
- Balancing research time vs experimentation

</advanced_topics>

---

## Reference: Debugging Mindset

<philosophy>
Debugging is applied epistemology. You're investigating a system to discover truth about its behavior. The difference between junior and senior debugging is not knowledge of frameworks - it's the discipline of systematic investigation.
</philosophy>

<meta_debugging>
**Special challenge**: When you're debugging code you wrote or modified, you're fighting your own mental model.

**Why this is harder**:
- You made the design decisions - they feel obviously correct
- You remember your intent, not what you actually implemented
- You see what you meant to write, not what's there
- Familiarity breeds blindness to bugs

**The trap**:
- "I know this works because I implemented it correctly"
- "The bug must be elsewhere - I designed this part"
- "I tested this approach"
- These thoughts are red flags. Code you wrote is guilty until proven innocent.

**The discipline**:

**1. Treat your own code as foreign**
- Read it as if someone else wrote it
- Don't assume it does what you intended
- Verify what it actually does, not what you think it does
- Fresh eyes see bugs; familiar eyes see intent

**2. Question your own design decisions**
- "I chose approach X because..." - Was that reasoning sound?
- "I assumed Y would..." - Have you verified Y actually does that?
- Your implementation decisions are hypotheses, not facts

**3. Admit your mental model might be wrong**
- You built a mental model of how this works
- That model might be incomplete or incorrect
- The code's behavior is truth; your model is just a guess
- Be willing to discover you misunderstood the problem

**4. Prioritize code you touched**
- If you modified 100 lines and something breaks
- Those 100 lines are the prime suspects
- Don't assume the bug is in the framework or existing code
- Start investigating where you made changes

<example>
❌ "I implemented the auth flow correctly, the bug must be in the existing user service"

✅ "I implemented the auth flow. Let me verify each part:
   - Does login actually set the token? [test it]
   - Does the middleware actually validate it? [test it]
   - Does logout actually clear it? [test it]
   - One of these is probably wrong"

The second approach found that logout wasn't clearing the token from localStorage, only from memory.
</example>

**The hardest admission**: "I implemented this wrong."

Not "the requirements were unclear" or "the library is confusing" - YOU made an error. Whether it was 5 minutes ago or 5 days ago doesn't matter. Your code, your responsibility, your bug to find.

This intellectual honesty is the difference between debugging for hours and finding bugs quickly.
</meta_debugging>

<foundation>
When debugging, return to foundational truths:

**What do you know for certain?**
- What have you directly observed (not assumed)?
- What can you prove with a test right now?
- What is speculation vs evidence?

**What are you assuming?**
- "This library should work this way" - Have you verified?
- "The docs say X" - Have you tested that X actually happens?
- "This worked before" - Can you prove when it worked and what changed?

Strip away everything you think you know. Build understanding from observable facts.
</foundation>

<example>
❌ "React state updates should be synchronous here"
✅ "Let me add a console.log to observe when state actually updates"

❌ "The API must be returning bad data"
✅ "Let me log the exact response payload to see what's actually being returned"

❌ "This database query should be fast"
✅ "Let me run EXPLAIN to see the actual execution plan"
</example>

<cognitive_biases>

<bias name="confirmation_bias">
**The problem**: You form a hypothesis and only look for evidence that confirms it.

**The trap**: "I think it's a race condition" → You only look for async code, missing the actual typo in a variable name.

**The antidote**: Actively seek evidence that disproves your hypothesis. Ask "What would prove me wrong?"
</bias>

<bias name="anchoring">
**The problem**: The first explanation you encounter becomes your anchor, and you adjust from there instead of considering alternatives.

**The trap**: Error message mentions "timeout" → You assume it's a network issue, when it's actually a deadlock.

**The antidote**: Generate multiple independent hypotheses before investigating any single one. Force yourself to list 3+ possible causes.
</bias>

<bias name="availability_heuristic">
**The problem**: You remember recent bugs and assume similar symptoms mean the same cause.

**The trap**: "We had a caching issue last week, this must be caching too."

**The antidote**: Treat each bug as novel until evidence suggests otherwise. Recent memory is not evidence.
</bias>

<bias name="sunk_cost_fallacy">
**The problem**: You've spent 2 hours debugging down one path, so you keep going even when evidence suggests it's wrong.

**The trap**: "I've almost figured out this state management issue" - when the actual bug is in the API layer.

**The antidote**: Set checkpoints. Every 30 minutes, ask: "If I started fresh right now, is this still the path I'd take?"
</bias>

</cognitive_biases>

<systematic_investigation>

<discipline name="change_one_variable">
**Why it matters**: If you change multiple things at once, you don't know which one fixed (or broke) it.

**In practice**:
1. Make one change
2. Test
3. Observe result
4. Document
5. Repeat

**The temptation**: "Let me also update this dependency and refactor this function and change this config..."

**The reality**: Now you have no idea what actually mattered.
</discipline>

<discipline name="complete_reading">
**Why it matters**: Skimming code causes you to miss crucial details. You see what you expect to see, not what's there.

**In practice**:
- Read entire functions, not just the "relevant" lines
- Read imports and dependencies
- Read configuration files completely
- Read test files to understand intended behavior

**The shortcut**: "This function is long, I'll just read the part where the error happens"

**The miss**: The bug is actually in how the function is called 50 lines up.
</discipline>

<discipline name="embrace_not_knowing">
**Why it matters**: Premature certainty stops investigation. "I don't know" is a position of strength.

**In practice**:
- "I don't know why this fails" - Good. Now you can investigate.
- "It must be X" - Dangerous. You've stopped thinking.

**The pressure**: Users want answers. Managers want ETAs. Your ego wants to look smart.

**The truth**: "I need to investigate further" is more professional than a wrong fix.
</discipline>

</systematic_investigation>

<when_to_restart>

<restart_signals>
You should consider starting over when:

1. **You've been investigating for 2+ hours with no progress**
   - You're likely tunnel-visioned
   - Take a break, then restart from evidence gathering

2. **You've made 3+ "fixes" that didn't work**
   - Your mental model is wrong
   - Go back to first principles

3. **You can't explain the current behavior**
   - Don't add more changes on top of confusion
   - First understand what's happening, then fix it

4. **You're debugging the debugger**
   - "Is my logging broken? Is the debugger lying?"
   - Step back. Something fundamental is wrong.

5. **The fix works but you don't know why**
   - This isn't fixed. This is luck.
   - Investigate until you understand, or revert the change
</restart_signals>

<restart_protocol>
When restarting:

1. **Close all files and terminals**
2. **Write down what you know for certain** (not what you think)
3. **Write down what you've ruled out**
4. **List new hypotheses** (different from before)
5. **Begin again from Phase 1: Evidence Gathering**

This isn't failure. This is professionalism.
</restart_protocol>

</when_to_restart>

<humility>
The best debuggers have deep humility about their mental models:

**They know**:
- Their understanding of the system is incomplete
- Documentation can be wrong or outdated
- Their memory of "how this works" may be faulty
- The system's behavior is the only truth

**They don't**:
- Trust their first instinct
- Assume anything works as designed
- Skip verification steps
- Declare victory without proof

**They ask**:
- "What am I missing?"
- "What am I wrong about?"
- "What haven't I tested?"
- "What does the evidence actually say?"
</humility>

<craft>
Debugging is a craft that improves with practice:

**Novice debuggers**:
- Try random things hoping something works
- Skip reading code carefully
- Don't test their hypotheses
- Declare success too early

**Expert debuggers**:
- Form hypotheses explicitly
- Test hypotheses systematically
- Read code like literature
- Verify fixes rigorously
- Learn from each investigation

**The difference**: Not intelligence. Not knowledge. Discipline.

Practice the discipline of systematic investigation, and debugging becomes a strength.
</craft>

---

## Reference: Hypothesis Testing

<overview>
Debugging is applied scientific method. You observe a phenomenon (the bug), form hypotheses about its cause, design experiments to test those hypotheses, and revise based on evidence. This isn't metaphorical - it's literal experimental science.
</overview>


<principle name="falsifiability">
A good hypothesis can be proven wrong. If you can't design an experiment that could disprove it, it's not a useful hypothesis.

**Bad hypotheses** (unfalsifiable):
- "Something is wrong with the state"
- "The timing is off"
- "There's a race condition somewhere"
- "The library is buggy"

**Good hypotheses** (falsifiable):
- "The user state is being reset because the component remounts when the route changes"
- "The API call completes after the component unmounts, causing the state update on unmounted component warning"
- "Two async operations are modifying the same array without locking, causing data loss"
- "The library's caching mechanism is returning stale data because our cache key doesn't include the timestamp"

**The difference**: Specificity. Good hypotheses make specific, testable claims.
</principle>

<how_to_form>
**Process for forming hypotheses**:

1. **Observe the behavior precisely**
   - Not "it's broken"
   - But "the counter shows 3 when clicking once, should show 1"

2. **Ask "What could cause this?"**
   - List every possible cause you can think of
   - Don't judge them yet, just brainstorm

3. **Make each hypothesis specific**
   - Not "state is wrong"
   - But "state is being updated twice because handleClick is called twice"

4. **Identify what evidence would support/refute each**
   - If hypothesis X is true, I should see Y
   - If hypothesis X is false, I should see Z

<example>
**Observation**: Button click sometimes saves data, sometimes doesn't.

**Vague hypothesis**: "The save isn't working reliably"
❌ Unfalsifiable, not specific

**Specific hypotheses**:
1. "The save API call is timing out when network is slow"
   - Testable: Check network tab for timeout errors
   - Falsifiable: If all requests complete successfully, this is wrong

2. "The save button is being double-clicked, and the second request overwrites with stale data"
   - Testable: Add logging to count clicks
   - Falsifiable: If only one click is registered, this is wrong

3. "The save is successful but the UI doesn't update because the response is being ignored"
   - Testable: Check if API returns success
   - Falsifiable: If UI updates on successful response, this is wrong
</example>
</how_to_form>


<experimental_design>
An experiment is a test that produces evidence supporting or refuting a hypothesis.

**Good experiments**:
- Test one hypothesis at a time
- Have clear success/failure criteria
- Produce unambiguous results
- Are repeatable

**Bad experiments**:
- Test multiple things at once
- Have unclear outcomes ("maybe it works better?")
- Rely on subjective judgment
- Can't be reproduced

<framework>
For each hypothesis, design an experiment:

**1. Prediction**: If hypothesis H is true, then I will observe X
**2. Test setup**: What do I need to do to test this?
**3. Measurement**: What exactly am I measuring?
**4. Success criteria**: What result confirms H? What result refutes H?
**5. Run the experiment**: Execute the test
**6. Observe the result**: Record what actually happened
**7. Conclude**: Does this support or refute H?

</framework>

<example>
**Hypothesis**: "The component is re-rendering excessively because the parent is passing a new object reference on every render"

**1. Prediction**: If true, the component will re-render even when the object's values haven't changed

**2. Test setup**:
   - Add console.log in component body to count renders
   - Add console.log in parent to track when object is created
   - Add useEffect with the object as dependency to log when it changes

**3. Measurement**: Count of renders and object creations

**4. Success criteria**:
   - Confirms H: Component re-renders match parent renders, object reference changes each time
   - Refutes H: Component only re-renders when object values actually change

**5. Run**: Execute the code with logging

**6. Observe**:
   ```
   [Parent] Created user object
   [Child] Rendering (1)
   [Parent] Created user object
   [Child] Rendering (2)
   [Parent] Created user object
   [Child] Rendering (3)
   ```

**7. Conclude**: CONFIRMED. New object every parent render → child re-renders
</example>
</experimental_design>


<evidence_quality>
Not all evidence is equal. Learn to distinguish strong from weak evidence.

**Strong evidence**:
- Directly observable ("I can see in the logs that X happens")
- Repeatable ("This fails every time I do Y")
- Unambiguous ("The value is definitely null, not undefined")
- Independent ("This happens even in a fresh browser with no cache")

**Weak evidence**:
- Hearsay ("I think I saw this fail once")
- Non-repeatable ("It failed that one time but I can't reproduce it")
- Ambiguous ("Something seems off")
- Confounded ("It works after I restarted the server and cleared the cache and updated the package")

<examples>
**Strong**:
```javascript
console.log('User ID:', userId); // Output: User ID: undefined
console.log('Type:', typeof userId); // Output: Type: undefined
```
✅ Direct observation, unambiguous

**Weak**:
"I think the user ID might not be set correctly sometimes"
❌ Vague, not verified, uncertain

**Strong**:
```javascript
for (let i = 0; i < 100; i++) {
  const result = processData(testData);
  if (result !== expected) {
    console.log('Failed on iteration', i);
  }
}
// Output: Failed on iterations: 3, 7, 12, 23, 31...
```
✅ Repeatable, shows pattern

**Weak**:
"It usually works, but sometimes fails"
❌ Not quantified, no pattern identified
</examples>
</evidence_quality>


<decision_point>
Don't act too early (premature fix) or too late (analysis paralysis).

**Act when you can answer YES to all**:

1. **Do you understand the mechanism?**
   - Not just "what fails" but "why it fails"
   - Can you explain the chain of events that produces the bug?

2. **Can you reproduce it reliably?**
   - Either always reproduces, or you understand the conditions that trigger it
   - If you can't reproduce, you don't understand it yet

3. **Do you have evidence, not just theory?**
   - You've observed the behavior directly
   - You've logged the values, traced the execution
   - You're not guessing

4. **Have you ruled out alternatives?**
   - You've considered other hypotheses
   - Evidence contradicts the alternatives
   - This is the most likely cause, not just the first idea

**Don't act if**:
- "I think it might be X" - Too uncertain
- "This could be the issue" - Not confident enough
- "Let me try changing Y and see" - Random changes, not hypothesis-driven
- "I'll fix it and if it works, great" - Outcome-based, not understanding-based

<example>
**Too early** (don't act):
- Hypothesis: "Maybe the API is slow"
- Evidence: None, just a guess
- Action: Add caching
- Result: Bug persists, now you have caching to debug too

**Right time** (act):
- Hypothesis: "API response is missing the 'status' field when user is inactive, causing the app to crash"
- Evidence:
  - Logged API response for active user: has 'status' field
  - Logged API response for inactive user: missing 'status' field
  - Logged app behavior: crashes on accessing undefined status
- Action: Add defensive check for missing status field
- Result: Bug fixed because you understood the cause
</example>
</decision_point>


<recovery>
You will be wrong sometimes. This is normal. The skill is recovering gracefully.

**When your hypothesis is disproven**:

1. **Acknowledge it explicitly**
   - "This hypothesis was wrong because [evidence]"
   - Don't gloss over it or rationalize
   - Intellectual honesty with yourself

2. **Extract the learning**
   - What did this experiment teach you?
   - What did you rule out?
   - What new information do you have?

3. **Revise your understanding**
   - Update your mental model
   - What does the evidence actually suggest?

4. **Form new hypotheses**
   - Based on what you now know
   - Avoid just moving to "second-guess" - use the evidence

5. **Don't get attached to hypotheses**
   - You're not your ideas
   - Being wrong quickly is better than being wrong slowly

<example>
**Initial hypothesis**: "The memory leak is caused by event listeners not being cleaned up"

**Experiment**: Check Chrome DevTools for listener counts
**Result**: Listener count stays stable, doesn't grow over time

**Recovery**:
1. ✅ "Event listeners are NOT the cause. The count doesn't increase."
2. ✅ "I've ruled out event listeners as the culprit"
3. ✅ "But the memory profile shows objects accumulating. What objects? Let me check the heap snapshot..."
4. ✅ "New hypothesis: Large arrays are being cached and never released. Let me test by checking the heap for array sizes..."

This is good debugging. Wrong hypothesis, quick recovery, better understanding.
</example>
</recovery>


<multiple_hypotheses>
Don't fall in love with your first hypothesis. Generate multiple alternatives.

**Strategy**: "Strong inference" - Design experiments that differentiate between competing hypotheses.

<example>
**Problem**: Form submission fails intermittently

**Competing hypotheses**:
1. Network timeout
2. Validation failure
3. Race condition with auto-save
4. Server-side rate limiting

**Design experiment that differentiates**:

Add logging at each stage:
```javascript
try {
  console.log('[1] Starting validation');
  const validation = await validate(formData);
  console.log('[1] Validation passed:', validation);

  console.log('[2] Starting submission');
  const response = await api.submit(formData);
  console.log('[2] Response received:', response.status);

  console.log('[3] Updating UI');
  updateUI(response);
  console.log('[3] Complete');
} catch (error) {
  console.log('[ERROR] Failed at stage:', error);
}
```

**Observe results**:
- Fails at [2] with timeout error → Hypothesis 1
- Fails at [1] with validation error → Hypothesis 2
- Succeeds but [3] has wrong data → Hypothesis 3
- Fails at [2] with 429 status → Hypothesis 4

**One experiment, differentiates between four hypotheses.**
</example>
</multiple_hypotheses>


<workflow>
```
1. Observe unexpected behavior
     ↓
2. Form specific hypotheses (plural)
     ↓
3. For each hypothesis: What would prove/disprove?
     ↓
4. Design experiment to test
     ↓
5. Run experiment
     ↓
6. Observe results
     ↓
7. Evaluate: Confirmed, refuted, or inconclusive?
     ↓
8a. If CONFIRMED → Design fix based on understanding
8b. If REFUTED → Return to step 2 with new hypotheses
8c. If INCONCLUSIVE → Redesign experiment or gather more data
```

**Key insight**: This is a loop, not a line. You'll cycle through multiple times. That's expected.
</workflow>


<pitfalls>

**Pitfall: Testing multiple hypotheses at once**
- You change three things and it works
- Which one fixed it? You don't know
- Solution: Test one hypothesis at a time

**Pitfall: Confirmation bias in experiments**
- You only look for evidence that confirms your hypothesis
- You ignore evidence that contradicts it
- Solution: Actively seek disconfirming evidence

**Pitfall: Acting on weak evidence**
- "It seems like maybe this could be..."
- Solution: Wait for strong, unambiguous evidence

**Pitfall: Not documenting results**
- You forget what you tested
- You repeat the same experiments
- Solution: Write down each hypothesis and its result

**Pitfall: Giving up on the scientific method**
- Under pressure, you start making random changes
- "Let me just try this..."
- Solution: Double down on rigor when pressure increases
</pitfalls>

<excellence>
**Great debuggers**:
- Form multiple competing hypotheses
- Design clever experiments that differentiate between them
- Follow the evidence wherever it leads
- Revise their beliefs when proven wrong
- Act only when they have strong evidence
- Understand the mechanism, not just the symptom

This is the difference between guessing and debugging.
</excellence>

---

## Reference: Investigation Techniques

<overview>
These are systematic approaches to narrowing down bugs. Each technique is a tool in your debugging toolkit. The skill is knowing which tool to use when.
</overview>


<technique name="binary_search">
**When to use**: Large codebase, long execution path, or many possible failure points.

**How it works**: Cut the problem space in half repeatedly until you isolate the issue.

**In practice**:

1. **Identify the boundaries**: Where does it work? Where does it fail?
2. **Find the midpoint**: Add logging/testing at the middle of the execution path
3. **Determine which half**: Does the bug occur before or after the midpoint?
4. **Repeat**: Cut that half in half, test again
5. **Converge**: Keep halving until you find the exact line

<example>
Problem: API request returns wrong data

1. Test: Does the data leave the database correctly? YES
2. Test: Does the data reach the frontend correctly? NO
3. Test: Does the data leave the API route correctly? YES
4. Test: Does the data survive serialization? NO
5. **Found it**: Bug is in the serialization layer

You just eliminated 90% of the code in 4 tests.
</example>
</technique>

<technique name="comment_out_bisection">
**Variant**: Commenting out code to find the breaking change.

1. Comment out the second half of a function
2. Does it work now? The bug is in the commented section
3. Uncomment half of that, repeat
4. Converge on the problematic lines

**Warning**: Only works for code you can safely comment out. Don't use for initialization code.
</technique>


<technique name="rubber_duck">
**When to use**: You're stuck, confused, or your mental model doesn't match reality.

**How it works**: Explain the problem out loud (to a rubber duck, a colleague, or in writing) in complete detail.

**Why it works**: Articulating forces you to:
- Make assumptions explicit
- Notice gaps in your understanding
- Hear how convoluted your explanation sounds
- Realize what you haven't actually verified

**In practice**:

Write or say out loud:
1. "The system should do X"
2. "Instead it does Y"
3. "I think this is because Z"
4. "The code path is: A → B → C → D"
5. "I've verified that..." (List what you've actually tested)
6. "I'm assuming that..." (List assumptions)

Often you'll spot the bug mid-explanation: "Wait, I never actually verified that B returns what I think it does."

<example>
"So when the user clicks the button, it calls handleClick, which dispatches an action, which... wait, does the reducer actually handle this action type? Let me check... Oh. The reducer is looking for 'UPDATE_USER' but I'm dispatching 'USER_UPDATE'."
</example>
</technique>


<technique name="minimal_reproduction">
**When to use**: Complex system, many moving parts, unclear which part is failing.

**How it works**: Strip away everything until you have the smallest possible code that reproduces the bug.

**Why it works**:
- Removes distractions
- Isolates the actual issue
- Often reveals the bug during the stripping process
- Makes it easier to reason about

**Process**:

1. **Copy the failing code to a new file**
2. **Remove one piece** (a dependency, a function, a feature)
3. **Test**: Does it still reproduce?
   - YES: Keep it removed, continue
   - NO: Put it back, it's needed
4. **Repeat** until you have the bare minimum
5. **The bug is now obvious** in the stripped-down code

<example>
Start with: 500-line React component with 15 props, 8 hooks, 3 contexts

End with:
```jsx
function MinimalRepro() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setCount(count + 1); // Bug: infinite loop, missing dependency array
  });

  return <div>{count}</div>;
}
```

The bug was hidden in complexity. Minimal reproduction made it obvious.
</example>
</technique>


<technique name="working_backwards">
**When to use**: You know what the correct output should be, but don't know why you're not getting it.

**How it works**: Start from the desired end state and trace backwards through the execution path.

**Process**:

1. **Define the desired output precisely**
2. **Ask**: What function produces this output?
3. **Test that function**: Give it the input it should receive. Does it produce correct output?
   - YES: The bug is earlier (wrong input to this function)
   - NO: The bug is here
4. **Repeat backwards** through the call stack
5. **Find the divergence point**: Where does expected vs actual first differ?

<example>
Problem: UI shows "User not found" when user exists

Trace backwards:
1. UI displays: `user.error` → Is this the right value to display? YES
2. Component receives: `user.error = "User not found"` → Is this correct? NO, should be null
3. API returns: `{ error: "User not found" }` → Why?
4. Database query: `SELECT * FROM users WHERE id = 'undefined'` → AH!
5. **Found it**: The user ID is 'undefined' (string) instead of a number

Working backwards revealed the bug was in how the ID was passed to the query.
</example>
</technique>


<technique name="differential_debugging">
**When to use**: Something used to work and now doesn't. A feature works in one environment but not another.

**How it works**: Compare the working vs broken states to find what's different.

**Questions to ask**:

**Time-based** (it worked, now it doesn't):
- What changed in the code since it worked?
- What changed in the environment? (Node version, OS, dependencies)
- What changed in the data? (Database schema, API responses)
- What changed in the configuration?

**Environment-based** (works in dev, fails in prod):
- What's different between environments?
- Configuration values
- Environment variables
- Network conditions
- Data volume
- Third-party service behavior

**Process**:

1. **Make a list of differences** between working and broken
2. **Test each difference** in isolation
3. **Find the difference that causes the failure**
4. **That difference reveals the root cause**

<example>
Works locally, fails in CI:

Differences:
- Node version: Same ✓
- Environment variables: Same ✓
- Timezone: Different! ✗

Test: Set local timezone to UTC (like CI)
Result: Now fails locally too

**Found it**: Date comparison logic assumes local timezone
</example>
</technique>


<technique name="observability_first">
**When to use**: Always. Before making any fix.

**Why it matters**: You can't fix what you can't see. Add visibility before changing behavior.

**Approaches**:

**1. Strategic logging**
```javascript
// Not this (useless):
console.log('in function');

// This (useful):
console.log('[handleSubmit] Input:', { email, password: '***' });
console.log('[handleSubmit] Validation result:', validationResult);
console.log('[handleSubmit] API response:', response);
```

**2. Assertion checks**
```javascript
function processUser(user) {
  console.assert(user !== null, 'User is null!');
  console.assert(user.id !== undefined, 'User ID is undefined!');
  // ... rest of function
}
```

**3. Timing measurements**
```javascript
console.time('Database query');
const result = await db.query(sql);
console.timeEnd('Database query');
```

**4. Stack traces at key points**
```javascript
console.log('[updateUser] Called from:', new Error().stack);
```

**The workflow**:
1. **Add logging/instrumentation** at suspected points
2. **Run the code**
3. **Observe the output**
4. **Form hypothesis** based on what you see
5. **Only then** make changes

Don't code in the dark. Light up the execution path first.
</technique>


<technique name="comment_out_everything">
**When to use**: Many possible interactions, unclear which code is causing the issue.

**How it works**:

1. **Comment out everything** in a function/file
2. **Verify the bug is gone**
3. **Uncomment one piece at a time**
4. **After each uncomment, test**
5. **When the bug returns**, you found the culprit

**Variant**: For config files, reset to defaults and add back one setting at a time.

<example>
Problem: Some middleware breaks requests, but you have 8 middleware functions.

```javascript
app.use(helmet()); // Uncomment, test → works
app.use(cors()); // Uncomment, test → works
app.use(compression()); // Uncomment, test → works
app.use(bodyParser.json({ limit: '50mb' })); // Uncomment, test → BREAKS

// Found it: Body size limit too high causes memory issues
```
</example>
</technique>


<technique name="git_bisect">
**When to use**: Feature worked in the past, broke at some unknown commit.

**How it works**: Binary search through git history to find the breaking commit.

**Process**:

```bash
git bisect start

git bisect bad

git bisect good abc123

git bisect bad

git bisect good

```

**Why it's powerful**: Turns "it broke sometime in the last 100 commits" into "it broke in commit abc123" in ~7 tests (log₂ 100 ≈ 7).

<example>
100 commits between working and broken
Manual testing: 100 commits to check
Git bisect: 7 commits to check

Time saved: Massive
</example>
</technique>


<decision_tree>
**Large codebase, many files**:
→ Binary search / Divide and conquer

**Confused about what's happening**:
→ Rubber duck debugging
→ Observability first (add logging)

**Complex system with many interactions**:
→ Minimal reproduction

**Know the desired output**:
→ Working backwards

**Used to work, now doesn't**:
→ Differential debugging
→ Git bisect

**Many possible causes**:
→ Comment out everything
→ Binary search

**Always**:
→ Observability first before making changes
</decision_tree>

<combining_techniques>
Often you'll use multiple techniques together:

1. **Differential debugging** to identify what changed
2. **Binary search** to narrow down where in the code
3. **Observability first** to add logging at that point
4. **Rubber duck** to articulate what you're seeing
5. **Minimal reproduction** to isolate just that behavior
6. **Working backwards** to find the root cause

Techniques compose. Use as many as needed.
</combining_techniques>

---

## Reference: Verification Patterns

<overview>
The most common debugging mistake: declaring victory too early. A fix isn't complete until it's verified. This document defines what "verified" means and provides systematic approaches to proving your fix works.
</overview>


<definition>
A fix is verified when:

1. **The original issue no longer occurs**
   - The exact reproduction steps now produce correct behavior
   - Not "it seems better" - it definitively works

2. **You understand why the fix works**
   - You can explain the mechanism
   - Not "I changed X and it worked" but "X was causing Y, and changing it prevents Y"

3. **Related functionality still works**
   - You haven't broken adjacent features
   - Regression testing passes

4. **The fix works across environments**
   - Not just on your machine
   - In production-like conditions

5. **The fix is stable**
   - Works consistently, not intermittently
   - Not just "worked once" but "works reliably"

**Anything less than this is not verified.**
</definition>

<examples>
❌ **Not verified**:
- "I ran it once and it didn't crash"
- "It seems to work now"
- "The error message is gone" (but is the behavior correct?)
- "Works on my machine"

✅ **Verified**:
- "I ran the original reproduction steps 20 times - zero failures"
- "The data now saves correctly and I can retrieve it"
- "All existing tests pass, plus I added a test for this scenario"
- "Verified in dev, staging, and production environments"
</examples>


<pattern name="reproduction_verification">
**The golden rule**: If you can't reproduce the bug, you can't verify it's fixed.

**Process**:

1. **Before fixing**: Document exact steps to reproduce
   ```markdown
   Reproduction steps:
   1. Login as admin user
   2. Navigate to /settings
   3. Click "Export Data" button
   4. Observe: Error "Cannot read property 'data' of undefined"
   ```

2. **After fixing**: Execute the same steps exactly
   ```markdown
   Verification:
   1. Login as admin user ✓
   2. Navigate to /settings ✓
   3. Click "Export Data" button ✓
   4. Observe: CSV downloads successfully ✓
   ```

3. **Test edge cases** related to the bug
   ```markdown
   Additional tests:
   - Export with empty data set ✓
   - Export with 1000+ records ✓
   - Export while another request is pending ✓
   ```

**If you can't reproduce the original bug**:
- You don't know if your fix worked
- Maybe it's still broken
- Maybe your "fix" did nothing
- Maybe you fixed a different bug

**Solution**: Revert your fix. If the bug comes back, you've verified your fix addressed it.
</pattern>


<pattern name="regression_testing">
**The problem**: You fix one thing, break another.

**Why it happens**:
- Your fix changed shared code
- Your fix had unintended side effects
- Your fix broke an assumption other code relied on

**Protection strategy**:

**1. Identify adjacent functionality**
- What else uses the code you changed?
- What features depend on this behavior?
- What workflows include this step?

**2. Test each adjacent area**
- Manually test the happy path
- Check error handling
- Verify data integrity

**3. Run existing tests**
- Unit tests for the module
- Integration tests for the feature
- End-to-end tests for the workflow

<example>
**Fix**: Changed how user sessions are stored (from memory to database)

**Adjacent functionality to verify**:
- Login still works ✓
- Logout still works ✓
- Session timeout still works ✓
- Concurrent logins are handled correctly ✓
- Session data persists across server restarts ✓ (new capability)
- Password reset flow still works ✓
- OAuth login still works ✓

If you only tested "login works", you missed 6 other things that could break.
</example>
</pattern>


<pattern name="test_first_debugging">
**Strategy**: Write a failing test that reproduces the bug, then fix until the test passes.

**Benefits**:
- Proves you can reproduce the bug
- Provides automatic verification
- Prevents regression in the future
- Forces you to understand the bug precisely

**Process**:

1. **Write a test that reproduces the bug**
   ```javascript
   test('should handle undefined user data gracefully', () => {
     const result = processUserData(undefined);
     expect(result).toBe(null); // Currently throws error
   });
   ```

2. **Verify the test fails** (confirms it reproduces the bug)
   ```
   ✗ should handle undefined user data gracefully
     TypeError: Cannot read property 'name' of undefined
   ```

3. **Fix the code**
   ```javascript
   function processUserData(user) {
     if (!user) return null; // Add defensive check
     return user.name;
   }
   ```

4. **Verify the test passes**
   ```
   ✓ should handle undefined user data gracefully
   ```

5. **Test is now regression protection**
   - If someone breaks this again, the test will catch it

**When to use**:
- Clear, reproducible bugs
- Code that has test infrastructure
- Bugs that could recur

**When not to use**:
- Exploratory debugging (you don't understand the bug yet)
- Infrastructure issues (can't easily test)
- One-off data issues
</pattern>


<pattern name="environment_verification">
**The trap**: "Works on my machine"

**Reality**: Production is different.

**Differences to consider**:

**Environment variables**:
- `NODE_ENV=development` vs `NODE_ENV=production`
- Different API keys
- Different database connections
- Different feature flags

**Dependencies**:
- Different package versions (if not locked)
- Different system libraries
- Different Node/Python/etc versions

**Data**:
- Volume (100 records locally, 1M in production)
- Quality (clean test data vs messy real data)
- Edge cases (nulls, special characters, extreme values)

**Network**:
- Latency (local: 5ms, production: 200ms)
- Reliability (local: perfect, production: occasional failures)
- Firewalls, proxies, load balancers

**Verification checklist**:
```markdown
- [ ] Works locally (dev environment)
- [ ] Works in Docker container (mimics production)
- [ ] Works in staging (production-like)
- [ ] Works in production (the real test)
```

<example>
**Bug**: Batch processing fails in production but works locally

**Investigation**:
- Local: 100 test records, completes in 2 seconds
- Production: 50,000 records, times out at 30 seconds

**The difference**: Volume. Local testing didn't catch it.

**Fix verification**:
- Test locally with 50,000 records
- Verify performance in staging
- Monitor first production run
- Confirm all environments work
</example>
</pattern>


<pattern name="stability_testing">
**The problem**: It worked once, but will it work reliably?

**Intermittent bugs are the worst**:
- Hard to reproduce
- Hard to verify fixes
- Easy to declare fixed when they're not

**Verification strategies**:

**1. Repeated execution**
```bash
for i in {1..100}; do
  npm test -- specific-test.js || echo "Failed on run $i"
done
```

If it fails even once, it's not fixed.

**2. Stress testing**
```javascript
// Run many instances in parallel
const promises = Array(50).fill().map(() =>
  processData(testInput)
);

const results = await Promise.all(promises);
// All results should be correct
```

**3. Soak testing**
- Run for extended period (hours, days)
- Monitor for memory leaks, performance degradation
- Ensure stability over time

**4. Timing variations**
```javascript
// For race conditions, add random delays
async function testWithRandomTiming() {
  await randomDelay(0, 100);
  triggerAction1();
  await randomDelay(0, 100);
  triggerAction2();
  await randomDelay(0, 100);
  verifyResult();
}

// Run this 1000 times
```

<example>
**Bug**: Race condition in file upload

**Weak verification**:
- Upload one file
- "It worked!"
- Ship it

**Strong verification**:
- Upload 100 files sequentially: all succeed ✓
- Upload 20 files in parallel: all succeed ✓
- Upload while navigating away: handles correctly ✓
- Upload, cancel, upload again: works ✓
- Run all tests 50 times: zero failures ✓

Now it's verified.
</example>
</pattern>


<checklist>
Copy this checklist when verifying a fix:

```markdown

### Original Issue
- [ ] Can reproduce the original bug before the fix
- [ ] Have documented exact reproduction steps

### Fix Validation
- [ ] Original reproduction steps now work correctly
- [ ] Can explain WHY the fix works
- [ ] Fix is minimal and targeted

### Regression Testing
- [ ] Adjacent feature 1: [name] works
- [ ] Adjacent feature 2: [name] works
- [ ] Adjacent feature 3: [name] works
- [ ] Existing tests pass
- [ ] Added test to prevent regression

### Environment Testing
- [ ] Works in development
- [ ] Works in staging/QA
- [ ] Works in production
- [ ] Tested with production-like data volume

### Stability Testing
- [ ] Tested multiple times (n=__): zero failures
- [ ] Tested edge cases: [list them]
- [ ] Tested under load/stress: stable

### Documentation
- [ ] Code comments explain the fix
- [ ] Commit message explains the root cause
- [ ] If needed, updated user-facing docs

### Sign-off
- [ ] I understand why this bug occurred
- [ ] I understand why this fix works
- [ ] I've verified it works in all relevant environments
- [ ] I've tested for regressions
- [ ] I'm confident this won't recur
```

**Do not merge/deploy until all checkboxes are checked.**
</checklist>


<distrust>
Your verification might be wrong if:

**1. You can't reproduce the original bug anymore**
- Maybe you forgot how
- Maybe the environment changed
- Maybe you're testing the wrong thing
- **Action**: Document reproduction steps FIRST, before fixing

**2. The fix is large or complex**
- Changed 10 files, modified 200 lines
- Too many moving parts
- **Action**: Simplify the fix, then verify each piece

**3. You're not sure why it works**
- "I changed X and the bug went away"
- But you can't explain the mechanism
- **Action**: Investigate until you understand, then verify

**4. It only works sometimes**
- "Usually works now"
- "Seems more stable"
- **Action**: Not verified. Find and fix the remaining issue

**5. You can't test in production-like conditions**
- Only tested locally
- Different data, different scale
- **Action**: Set up staging environment or use production data in dev

**Red flag phrases**:
- "It seems to work"
- "I think it's fixed"
- "Looks good to me"
- "Can't reproduce anymore" (but you never could reliably)

**Trust-building phrases**:
- "I've verified 50 times - zero failures"
- "All tests pass including new regression test"
- "Deployed to staging, tested for 3 days, no issues"
- "Root cause was X, fix addresses X directly, verified by Y"
</distrust>


<mindset>
**Assume your fix is wrong until proven otherwise.**

This isn't pessimism - it's professionalism.

**Questions to ask yourself**:
- "How could this fix fail?"
- "What haven't I tested?"
- "What am I assuming?"
- "Would this survive production?"

**The cost of insufficient verification**:
- Bug returns in production
- User frustration
- Lost trust
- Emergency debugging sessions
- Rollbacks

**The benefit of thorough verification**:
- Confidence in deployment
- Prevention of regressions
- Trust from team
- Learning from the investigation

**Verification is not optional. It's the most important part of debugging.**
</mindset>

---

## Reference: When To Research

<overview>
Debugging requires both reasoning about code and researching external knowledge. The skill is knowing when to use each. This guide helps you recognize signals that indicate you need external knowledge vs when you can reason through the problem with the code in front of you.
</overview>


<research_signals>

**1. Error messages you don't recognize**
- Stack traces from libraries you haven't used
- Cryptic system errors
- Framework-specific error codes

**Action**: Web search the exact error message in quotes
- Often leads to GitHub issues, Stack Overflow, or official docs
- Others have likely encountered this

<example>
Error: `EADDRINUSE: address already in use :::3000`

This is a system-level error. Research it:
- Web search: "EADDRINUSE address already in use"
- Learn: Port is already occupied by another process
- Solution: Find and kill the process, or use different port
</example>

**2. Library/framework behavior doesn't match expectations**
- You're using a library correctly (you think) but it's not working
- Documentation seems to contradict behavior
- Version-specific quirks

**Action**: Check official documentation and recent issues
- Use Context7 MCP for library docs
- Search GitHub issues for the library
- Check if there are breaking changes in recent versions

<example>
You're using `useEffect` in React but it's running on every render despite empty dependency array.

Research needed:
- Check React docs for useEffect rules
- Search: "useEffect running on every render"
- Discover: React 18 StrictMode runs effects twice in dev mode
</example>

**3. Domain knowledge gaps**
- Debugging authentication: need to understand OAuth flow
- Debugging database: need to understand indexes, query optimization
- Debugging networking: need to understand HTTP caching, CORS

**Action**: Research the domain concept, not just the specific bug
- Use MCP servers for domain knowledge
- Read official specifications
- Find authoritative guides

**4. Platform-specific behavior**
- "Works in Chrome but not Safari"
- "Works on Mac but not Windows"
- "Works in Node 16 but not Node 18"

**Action**: Research platform differences
- Browser compatibility tables
- Platform-specific documentation
- Known platform bugs

**5. Recent changes in ecosystem**
- Package update broke something
- New framework version behaves differently
- Deprecated API

**Action**: Check changelogs and migration guides
- Library CHANGELOG.md
- Migration guides
- "Breaking changes" documentation

</research_signals>


<reasoning_signals>

**1. The bug is in YOUR code**
- Not library behavior, not system issues
- Your business logic, your data structures
- Code you or your team wrote

**Approach**: Read the code, trace execution, add logging
- You have full access to the code
- You can modify it to add observability
- No external documentation will help

<example>
Bug: Shopping cart total calculates incorrectly

This is your logic:
```javascript
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

Don't research "shopping cart calculation bugs"
DO reason through it:
- Log each item's price and quantity
- Log the running sum
- Trace the logic step by step
</example>

**2. You have all the information needed**
- The bug is reproducible
- You can read all relevant code
- No external dependencies involved

**Approach**: Use investigation techniques
- Binary search to narrow down
- Minimal reproduction
- Working backwards
- Add observability

**3. It's a logic error, not a knowledge gap**
- Off-by-one errors
- Wrong conditional
- State management issue
- Data transformation bug

**Approach**: Trace the logic carefully
- Print intermediate values
- Check assumptions
- Verify each step

**4. The answer is in the behavior, not the documentation**
- "What is this function actually doing?"
- "Why is this value null?"
- "When does this code execute?"

**Approach**: Observe the actual behavior
- Add logging
- Use a debugger
- Test with different inputs

</reasoning_signals>


<research_how>

**Web Search - When and How**

**When**:
- Error messages
- Library-specific questions
- "How to X in framework Y"
- Troubleshooting platform issues

**How**:
- Use exact error messages in quotes: `"Cannot read property 'map' of undefined"`
- Include framework/library version: `"react 18 useEffect behavior"`
- Add "github issue" for known bugs: `"prisma connection pool github issue"`
- Add year for recent changes: `"nextjs 14 middleware 2024"`

**Good search queries**:
- `"ECONNREFUSED" node.js postgres`
- `"Maximum update depth exceeded" react hooks`
- `typescript generic constraints examples`

**Bad search queries**:
- `my code doesn't work` (too vague)
- `bug in react` (too broad)
- `help` (useless)

**Context7 MCP - When and How**

**When**:
- Need API reference
- Understanding library concepts
- Finding specific function signatures
- Learning correct usage patterns

**How**:
```
Use mcp__context7__resolve-library-id with library name
Then mcp__context7__get-library-docs with library ID
Ask specific questions about the library
```

**Good uses**:
- "How do I use Prisma transactions?"
- "What are the parameters for stripe.customers.create?"
- "How does Express middleware error handling work?"

**Bad uses**:
- "Fix my bug" (too vague, Context7 provides docs not debugging)
- "Why isn't my code working?" (need to research specific concepts, not general debugging)

**GitHub Issues Search**

**When**:
- Experiencing behavior that seems like a bug
- Library not working as documented
- Looking for workarounds

**How**:
- Search in the library's GitHub repo
- Include relevant keywords
- Check both open and closed issues
- Look for issues with "bug" or "regression" labels

**Official Documentation**

**When**:
- Learning how something should work
- Checking if you're using API correctly
- Understanding configuration options
- Finding migration guides

**How**:
- Start with official docs, not blog posts
- Check version-specific docs
- Read examples and guides, not just API reference
- Look for "Common Pitfalls" or "Troubleshooting" sections

</research_how>


<balance>

**The research trap**: Spending hours reading docs about topics tangential to your bug
- You think it's a caching issue, so you read all about cache invalidation
- But the actual bug is a typo in a variable name

**The reasoning trap**: Spending hours reading code when the answer is well-documented
- You're debugging why auth doesn't work
- The docs clearly explain the setup you missed
- You could have found it in 5 minutes of reading

**The balance**:

1. **Start with quick research** (5-10 minutes)
   - Search the error message
   - Check official docs for the feature you're using
   - Skim recent issues

2. **If research doesn't yield answers, switch to reasoning**
   - Add logging
   - Trace execution
   - Form hypotheses

3. **If reasoning reveals knowledge gaps, research those specific gaps**
   - "I need to understand how WebSocket reconnection works"
   - "I need to know if this library supports transactions"

4. **Alternate as needed**
   - Research → reveals what to investigate
   - Reasoning → reveals what to research
   - Keep switching based on what you learn

<example>
**Bug**: Real-time updates stop working after 1 hour

**Start with research** (5 min):
- Search: "websocket connection drops after 1 hour"
- Find: Common issue with load balancers having connection timeouts

**Switch to reasoning**:
- Check if you're using a load balancer: YES
- Check load balancer timeout setting: 3600 seconds (1 hour)
- Hypothesis: Load balancer is killing the connection

**Quick research**:
- Search: "websocket load balancer timeout fix"
- Find: Implement heartbeat/ping to keep connection alive

**Reasoning**:
- Check if library supports heartbeat: YES
- Implement ping every 30 seconds
- Test: Connection stays alive for 3+ hours

**Total time**: 20 minutes (research: 10 min, reasoning: 10 min)
**Success**: Found and fixed the issue

vs

**Wrong approach**: Spend 2 hours reading WebSocket spec
- Learned a lot about WebSocket protocol
- Didn't solve the problem (it was a config issue)
</example>

</balance>


<decision_tree>
```
Is this a error message I don't recognize?
├─ YES → Web search the error message
└─ NO ↓

Is this library/framework behavior I don't understand?
├─ YES → Check docs (Context7 or official docs)
└─ NO ↓

Is this code I/my team wrote?
├─ YES → Reason through it (logging, tracing, hypothesis testing)
└─ NO ↓

Is this a platform/environment difference?
├─ YES → Research platform-specific behavior
└─ NO ↓

Can I observe the behavior directly?
├─ YES → Add observability and reason through it
└─ NO → Research the domain/concept first, then reason
```
</decision_tree>


<red_flags>

**You're researching too much if**:
- You've read 20 blog posts but haven't looked at your code
- You understand the theory but haven't traced your actual execution
- You're learning about edge cases that don't apply to your situation
- You've been reading for 30+ minutes without testing anything

**You're reasoning too much if**:
- You've been staring at code for an hour without progress
- You keep finding things you don't understand and guessing
- You're debugging library internals (that's research territory)
- The error message is clearly from a library you don't know

**You're doing it right if**:
- You alternate between research and reasoning
- Each research session answers a specific question
- Each reasoning session tests a specific hypothesis
- You're making steady progress toward understanding

</red_flags>


<mindset>

**Good researchers ask**:
- "What specific question do I need answered?"
- "Where is the authoritative source for this?"
- "Is this a known issue or unique to my code?"
- "What version-specific information do I need?"

**Good reasoners ask**:
- "What is actually happening in my code?"
- "What am I assuming that might be wrong?"
- "How can I observe this behavior directly?"
- "What experiment would test my hypothesis?"

**Great debuggers do both**:
- Research to fill knowledge gaps
- Reason to understand actual behavior
- Switch fluidly based on what they learn
- Never stuck in one mode

**The goal**: Minimum time to maximum understanding.
- Research what you don't know
- Reason through what you can observe
- Fix what you understand
</mindset>
