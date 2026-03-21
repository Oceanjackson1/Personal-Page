---
title: "Pragmatic Writing"
description: "This skill should be used when writing technical content in the style of Hunt/Thomas (The Pragmatic Programmer) and Joel Spolsky (Joel on Software). It applies when creating technical essays, documentation, tutorials, or explanatory content that n..."
category: "research"
source: "community"
author: "Community"
tags: ["pragmatic", "writing"]
date: 2026-03-20
---

# Pragmatic Writing Skill

Writing style modeled on the masters of technical communication: Andy Hunt, Dave Thomas (The Pragmatic Programmer), and Joel Spolsky (Joel on Software). This skill transforms technical content into engaging, memorable prose.

## When to Use This Skill

This skill applies when:
- Creating technical blog posts, essays, or articles
- Writing documentation that needs personality
- Explaining complex concepts to developers
- Crafting tutorials or how-to guides
- Writing "lessons learned" or postmortem content
- Any technical writing that should be read, not just referenced

## Core Philosophy

> "The difference between 'almost right' and 'right' is the difference between the lightning bug and the lightning." — Mark Twain (quoted by Pragmatic Programmers)

Technical writing doesn't have to be dry. The best technical writers make complex ideas feel obvious, use concrete examples before abstract theory, and treat the reader as a smart colleague.

## The 10 Core Techniques

Reference the complete technique guide at [techniques.md](./references/techniques.md).

### 1. Concrete Before Abstract

**Always** start with a concrete example, then extract the principle.

```
❌ "Dependency injection is a design pattern where dependencies are passed
    to objects rather than created by them."

✅ "Imagine your class needs a database connection. You could create it
    yourself:

    def initialize
      @db = Database.new("localhost:5432")
    end

    But now your class is stuck with that exact database. What if you
    want to test with a fake one? What if production uses a different host?

    Instead, accept it as a parameter:

    def initialize(db)
      @db = db
    end

    That's dependency injection. Simple."
```

### 2. Physical Analogies

Map abstract concepts to physical experiences readers already understand.

See [examples.md](./references/examples.md) for analogy patterns:
- Software abstractions → Physical tools
- Code patterns → Architectural patterns
- System design → Everyday systems (postal service, restaurants)

### 3. Conversational Register

Write like you're explaining to a smart colleague at a whiteboard.

**Markers of conversational register:**
- Contractions (don't, won't, can't)
- Direct address (you, your)
- Questions (But what if...? Why does this matter?)
- Asides (By the way, Incidentally)
- Admissions (To be honest, I'm not sure, It depends)

### 4. Humor as Architecture

Use humor strategically, not decoratively:
- Memorable hooks ("Good code is its own best documentation")
- Tension release after complex explanations
- Self-deprecation to build rapport
- Absurdist examples to highlight bad patterns

### 5. The "Aha!" Structure

Build to moments of realization:
1. Present a familiar problem
2. Show the common (flawed) approach
3. Reveal why it fails
4. Present the insight
5. Show the better way
6. Connect back to the principle

### 6. Short Paragraphs, Varied Length

- No paragraph over 4 sentences
- Alternate between longer explanations and punchy one-liners
- Use single-sentence paragraphs for emphasis

Like this.

### 7. Code as Evidence

Code examples should:
- Be runnable (no pseudo-code unless necessary)
- Be minimal (show only what matters)
- Progress from broken to fixed
- Include comments only for non-obvious things

### 8. The Principle Box

After a concrete exploration, box the principle:

> **Tip 23: Always Design for Concurrency**
> Allow for concurrency, and you will design cleaner interfaces with fewer assumptions.

### 9. Friendly Warnings

When discussing pitfalls:
- Acknowledge you've made the mistake too
- Explain why it's tempting
- Show the consequences
- Provide the escape hatch

See [anti-patterns.md](./references/anti-patterns.md) for common technical writing mistakes.

### 10. The Callback

End by connecting back to the opening example or question. Close the loop.

## Voice Characteristics

### Sentence Patterns
- Average length: 15-20 words
- Mix of simple, compound, complex
- Questions every 3-4 paragraphs
- Direct statements for key points

### Vocabulary
**Use**: specific, concrete, everyday words
**Avoid**: jargon without explanation, buzzwords, corporate-speak

### Tone
- Confident but not arrogant
- Curious and exploratory
- Practical and results-focused
- Occasionally irreverent

## Applying the Skill

### For Blog Posts
1. Open with a problem or scenario
2. Explore the messy middle
3. Reveal the insight
4. Show the solution
5. Extract the principle
6. Callback to opening

### For Documentation
1. Start with what the reader wants to do
2. Show the simplest working example
3. Expand with options and edge cases
4. Explain the "why" after the "how"

### For Tutorials
1. State the goal clearly
2. Show the end result first
3. Build up in small, testable steps
4. Explain mistakes, not just successes

## Quality Checklist

Before publishing, verify:
- [ ] Opens with concrete example or scenario
- [ ] Physical analogy for key concepts
- [ ] Conversational tone throughout
- [ ] At least one moment of humor or levity
- [ ] Principles boxed or highlighted
- [ ] Code examples are minimal and runnable
- [ ] Paragraphs under 4 sentences
- [ ] Callbacks to opening

## References

- [techniques.md](./references/techniques.md) - Full technique guide with examples
- [examples.md](./references/examples.md) - Before/after transformations
- [anti-patterns.md](./references/anti-patterns.md) - Seven deadly sins of technical writing
- [sources.md](./references/sources.md) - Original source material

---

## Reference: Anti Patterns

# Seven Deadly Sins of Technical Writing

Anti-patterns to avoid, with examples and fixes.

## 1. The Abstract Opening

Starting with definitions instead of examples.

### The Sin

> "Dependency injection is a design pattern in software engineering whereby one object supplies the dependencies of another object."

The reader's eyes glaze over before they understand why they should care.

### The Fix

Start with a problem they recognize:

> "Your tests are slow because every test spins up a real database connection. Let's fix that."

Then show the solution. *Then* name the pattern.

## 2. The Wall of Text

Paragraphs that go on and on, packing multiple ideas into dense blocks of text that require re-reading to understand, without any visual breaks to help the reader parse the information or take a breath between concepts.

### The Sin

The paragraph above. Did you read it? Or did you skim?

### The Fix

One idea per paragraph.

Short paragraphs are easier to scan.

They create rhythm.

And they emphasize key points.

Like this one.

## 3. The Passive Epidemic

### The Sin

> "The configuration file is read by the application when it is started. The values are validated and errors are logged if issues are found. The settings are then cached for performance."

Who's doing what? It's unclear. It's boring. It sounds like a legal document.

### The Fix

> "When your app starts, it reads the configuration file. It validates each value and logs any errors. Then it caches the settings so future reads are instant."

Active voice. Clear actors. Engaging rhythm.

## 4. The Jargon Dump

### The Sin

> "Leverage the microservice architecture's eventual consistency model to optimize throughput while maintaining idempotency across distributed transactions."

This might be technically accurate. It's also unreadable.

### The Fix

Either:
1. Define terms on first use
2. Use simpler words
3. Show an example first

> "When you split your app into services, they can't share a database. So Service A might update before Service B knows about it. Here's how to handle that gap..."

## 5. The Code Novel

### The Sin

```ruby
# This is a comprehensive example demonstrating the full implementation
# of a user authentication service including all edge cases, error
# handling, logging, caching, and rate limiting functionality.

class AuthenticationService
  RATE_LIMIT = 100
  CACHE_TTL = 3600

  def initialize(user_repository, token_service, cache, logger, rate_limiter)
    @user_repository = user_repository
    @token_service = token_service
    @cache = cache
    @logger = logger
    @rate_limiter = rate_limiter
  end

  # ... 100 more lines ...
end
```

By line 20, the reader has forgotten what point you were making.

### The Fix

Show only what's necessary for the current point:

```ruby
class AuthenticationService
  def initialize(user_repository)
    @users = user_repository  # Injected, not created
  end
end
```

Then say: "We'll add caching and rate limiting in the next section."

## 6. The Disclaimer Flood

### The Sin

> "While there are many approaches to this problem, and your mileage may vary depending on your specific circumstances, and this isn't intended as professional advice, and you should consult your team lead before implementing, one possible approach that might work in some cases is..."

By the time you get to the point, the reader has left.

### The Fix

State your recommendation clearly:

> "Use connection pooling. Here's why and how."

Add caveats at the end if needed, not before.

## 7. The Missing Why

### The Sin

> "Step 1: Add `gem 'sidekiq'` to your Gemfile
> Step 2: Run `bundle install`
> Step 3: Create a worker class
> Step 4: Configure Redis
> Step 5: Start the Sidekiq process"

The reader follows the steps but doesn't understand what they're building or why each step matters.

### The Fix

Start with the problem:

> "Your app freezes for 10 seconds when sending emails. Users hate it. You hate it.
>
> The fix: send emails in the background. When a user signs up, you add "send welcome email" to a queue and immediately return. A separate process handles the queue.
>
> Let's set that up..."

Now the steps have context.

---

## Quick Reference: Warning Signs

Your writing might be slipping if you see:

| Warning Sign | Probable Sin |
|--------------|--------------|
| "is defined as" in the first paragraph | Abstract Opening |
| Paragraphs over 5 lines | Wall of Text |
| "is/was/are/were" more than 30% of verbs | Passive Epidemic |
| More than 3 technical terms without explanation | Jargon Dump |
| Code examples over 30 lines | Code Novel |
| First sentence contains "while", "although", "however" | Disclaimer Flood |
| Tutorial without "why" explanation | Missing Why |

---

## Reference: Examples

# Pragmatic Writing Examples

Before/after transformations showing the techniques in action.

## Example 1: API Documentation

### Before (Dry, Abstract)

> The Authentication module provides mechanisms for verifying user credentials and managing session state. It implements the OAuth 2.0 specification and supports multiple grant types including authorization_code, client_credentials, and refresh_token flows.

### After (Pragmatic)

> **Getting Users Logged In**
>
> Your app needs to know who's making requests. Here's the simplest path:
>
> ```ruby
> # In your controller
> token = request.headers['Authorization']
> user = Auth.verify(token)
> ```
>
> That's it for reading. The token comes from your login flow, which we'll set up next.
>
> (We support OAuth 2.0 with authorization_code, client_credentials, and refresh_token flows. But let's start with the basics.)

## Example 2: Design Pattern Explanation

### Before (Textbook)

> The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it. This pattern is useful when you have multiple algorithms for a specific task and want to switch between them at runtime.

### After (Pragmatic)

> **Swapping Algorithms at Runtime**
>
> Say you're building a pricing calculator. Some customers get standard pricing. VIPs get 20% off. Enterprise clients have custom negotiated rates.
>
> The naive approach:
>
> ```ruby
> def calculate_price(customer, items)
>   case customer.type
>   when :standard
>     items.sum(&:price)
>   when :vip
>     items.sum(&:price) * 0.8
>   when :enterprise
>     # 50 lines of custom logic
>   end
> end
> ```
>
> Every new customer type means editing this method. Testing is a nightmare. And that enterprise logic? Nobody wants to touch it.
>
> Instead, make each pricing approach its own object:
>
> ```ruby
> class StandardPricing
>   def calculate(items)
>     items.sum(&:price)
>   end
> end
>
> class VipPricing
>   def calculate(items)
>     items.sum(&:price) * 0.8
>   end
> end
>
> # Usage
> pricing = customer.pricing_strategy
> total = pricing.calculate(items)
> ```
>
> Now adding a new customer type is adding a new class. No touching existing code. Each strategy can be tested in isolation.
>
> That's the Strategy pattern: algorithms as interchangeable objects.

## Example 3: Error Handling Guide

### Before (Formal)

> Error handling should be implemented consistently throughout the application. All exceptions should be caught at appropriate boundaries and either handled or re-thrown with additional context. Logging should capture sufficient information for debugging while avoiding sensitive data exposure.

### After (Pragmatic)

> **When Things Go Wrong**
>
> Errors happen. The question isn't if, but what you do when they do.
>
> The worst thing:
>
> ```ruby
> begin
>   do_risky_thing
> rescue
>   # Silent failure. Good luck debugging this at 3 AM.
> end
> ```
>
> The second worst thing:
>
> ```ruby
> begin
>   do_risky_thing
> rescue => e
>   puts e.message  # Hope someone's watching stdout!
>   raise  # Now we have two problems
> end
> ```
>
> Here's what actually helps:
>
> ```ruby
> begin
>   do_risky_thing(user_id: user.id)
> rescue NetworkError => e
>   # Expected failure, handle gracefully
>   ErrorTracker.capture(e, user_id: user.id)
>   return fallback_response
> rescue => e
>   # Unexpected failure, add context and escalate
>   raise ContextualError.new(
>     "Failed processing user #{user.id}",
>     cause: e
>   )
> end
> ```
>
> Notice:
> 1. We catch *specific* errors we know how to handle
> 2. We add context (the user_id) for debugging
> 3. Unexpected errors get wrapped with context, not swallowed
>
> > **Tip**: Every `rescue` without a specific exception type is a code smell. What exactly are you expecting to fail?

## Example 4: Performance Optimization

### Before (Generic)

> Performance optimization should focus on identifying bottlenecks through profiling before implementing changes. Premature optimization can lead to unnecessary complexity. Database queries are often the primary source of performance issues in web applications.

### After (Pragmatic)

> **Your App Is Slow. Now What?**
>
> First rule: **measure, don't guess**.
>
> I once spent a week optimizing a sorting algorithm only to discover the actual bottleneck was a DNS lookup. Don't be me.
>
> Here's the debugging order:
>
> ```
> 1. Is it the database?
>    → Check slow query log. 90% of the time, it's here.
>
> 2. Is it N+1 queries?
>    → user.posts.each { |p| p.author.name }
>    → That's 1 query for posts + N queries for authors
>
> 3. Is it memory?
>    → Loading 10,000 records into memory to count them?
>    → Use User.count, not User.all.size
>
> 4. Is it external services?
>    → API calls inside loops are death
>    → Batch them or cache them
> ```
>
> Once you've measured and found the bottleneck:
>
> ```ruby
> # Before: 47 queries, 2.3 seconds
> posts = user.posts
> posts.each { |p| render p.author.name }
>
> # After: 2 queries, 0.1 seconds
> posts = user.posts.includes(:author)
> posts.each { |p| render p.author.name }
> ```
>
> That's it. One word: `includes`. 23x faster.
>
> > **The real tip**: The fastest code is the code that doesn't run. Can you cache it? Can you skip it? Can you do it later?

## Example 5: Testing Philosophy

### Before (Textbook)

> Unit tests should verify the behavior of individual components in isolation. Tests should be deterministic, fast, and independent of external state. Mock objects can be used to isolate the system under test from its dependencies.

### After (Pragmatic)

> **Tests That Actually Help**
>
> Bad tests are worse than no tests. They slow you down, break randomly, and give false confidence.
>
> Here's a bad test:
>
> ```ruby
> test "user is valid" do
>   user = User.new(name: "Bob", email: "bob@test.com")
>   assert user.valid?
> end
> ```
>
> What does this actually test? That `User.new` works? That `valid?` returns a boolean? When this test fails, what do you learn?
>
> Here's a useful test:
>
> ```ruby
> test "user requires email to be unique" do
>   User.create!(email: "taken@test.com")
>   duplicate = User.new(email: "taken@test.com")
>
>   assert_not duplicate.valid?
>   assert_includes duplicate.errors[:email], "has already been taken"
> end
> ```
>
> This test:
> - Documents a business rule (unique emails)
> - Fails with a meaningful message if the rule breaks
> - Won't pass accidentally
>
> > **The test you need**: Write the test that would have caught last week's bug. That's usually the test worth writing.

---

## Reference: Sources

# Source Material

Original inspiration and recommended reading.

## Primary Sources

### The Pragmatic Programmer
**Authors**: Andy Hunt, Dave Thomas
**Key Contributions**:
- "Tip" format for distilling principles
- DRY (Don't Repeat Yourself) articulation
- Rubber duck debugging
- Tracer bullets concept
- "Good enough" software philosophy

**Style Elements Borrowed**:
- Numbered tips
- Anecdotal openings
- Physical analogies (broken windows, tracer bullets)
- Pragmatic over dogmatic approach

### Joel on Software
**Author**: Joel Spolsky
**Key Contributions**:
- The Joel Test
- "Things You Should Never Do" (on rewrites)
- Leaky abstractions
- Human task switching costs

**Style Elements Borrowed**:
- Conversational, blog-friendly tone
- Personal anecdotes
- Humor as architecture
- Building arguments through narrative
- Willingness to take strong positions

## Secondary Influences

### Effective Java
**Author**: Joshua Bloch
**Style Elements**:
- "Item" format for discrete lessons
- Clear do/don't guidance
- Code examples that evolve

### Clean Code
**Author**: Robert C. Martin
**Style Elements**:
- Before/after code transformations
- Named principles (SRP, DRY)
- Refactoring narratives

### A Philosophy of Software Design
**Author**: John Ousterhout
**Style Elements**:
- Counterintuitive insights
- "Red flag" warnings
- Complexity as central theme

## Recommended Reading Order

For developing pragmatic writing skills:

1. **Start here**: Joel on Software archives (free online)
   - Accessible, entertaining, teaches by example
   - Read: "The Absolute Minimum Every Software Developer Must Know About Unicode"

2. **Then**: The Pragmatic Programmer (20th Anniversary Edition)
   - The template for technical writing
   - Notice the structure of each tip

3. **Then**: Any technical blog you admire
   - Study what makes it work
   - Identify techniques they use

## Notable Blog Posts to Study

### For Structure
- "Choosing Boring Technology" by Dan McKinley
- "The Log: What every software engineer should know" by Jay Kreps

### For Narrative
- "The Night Watch" by James Mickens
- "Wat" by Gary Bernhardt (talk, but same principles)

### For Accessibility
- "The Absolute Minimum Every Software Developer Must Know About Unicode" by Joel Spolsky
- "What Every Programmer Should Know About Memory" by Ulrich Drepper

## Key Quotes to Remember

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."
> — Antoine de Saint-Exupéry

> "The best writing is rewriting."
> — E.B. White

> "Programs must be written for people to read, and only incidentally for machines to execute."
> — Harold Abelson

> "If you can't explain it simply, you don't understand it well enough."
> — (Attributed to Einstein, probably apocryphal, still true)

---

## Reference: Techniques

# Pragmatic Writing Techniques

Detailed guide to the 10 core techniques with extended examples.

## 1. Concrete Before Abstract

The most important technique. Never explain a concept before showing it.

### The Pattern

```
1. Show the problem scenario
2. Show the naive/common approach
3. Show it failing
4. Reveal the better approach
5. NOW explain the principle
```

### Extended Example

**Bad (abstract first):**
> The Observer pattern is a software design pattern in which an object, named the subject, maintains a list of its dependents, called observers, and notifies them automatically of any state changes.

**Good (concrete first):**
> You've got a spreadsheet. Cell A1 contains "10". Cell B1 contains "=A1 * 2". Change A1 to "20", and B1 instantly shows "40".
>
> That's the Observer pattern. B1 is *observing* A1. When A1 changes, B1 gets notified and updates itself.
>
> In code, you might have an Order that needs to notify Inventory, Shipping, and EmailService when it's placed. Instead of the Order calling all three directly...

## 2. Physical Analogies Catalog

### Software Abstraction → Physical Tool

- **Interface** → Power outlet (anything with the right plug works)
- **Caching** → Keeping frequently used tools on your workbench
- **Load balancing** → Multiple checkout lanes at a grocery store
- **Queue** → Line at the DMV
- **Stack** → Stack of plates (last one on is first one off)

### Design Pattern → Architectural Pattern

- **Factory** → Bakery (you order "bread", they handle the recipe)
- **Singleton** → The President (only one at a time)
- **Decorator** → Gift wrapping (adds features without changing the gift)
- **Adapter** → Travel power adapter (makes incompatible things work)

### System Design → Everyday System

- **Microservices** → Restaurant kitchen (grill station, salad station, dessert station)
- **Monolith** → Home kitchen (one person does everything)
- **Event sourcing** → Bank statement (every transaction recorded, balance calculated)
- **API Gateway** → Hotel concierge (single point of contact, routes requests)

## 3. Conversational Register Markers

### Use These

- "Let's say..." (introduces scenarios)
- "Here's the thing..." (pivots to key insight)
- "Now, you might be thinking..." (addresses objections)
- "I've seen this go wrong when..." (shares experience)
- "The trick is..." (reveals technique)

### Avoid These

- "It should be noted that..."
- "One must consider..."
- "The implementation thereof..."
- "As previously mentioned..."
- "In conclusion..."

## 4. Humor Patterns

### The Absurdist Example

Show a bad pattern taken to its extreme:

> If we followed this logic, we'd have a `StringUtils` class with methods like `addOneToNumber(String s)` that parses the string to an int, adds one, and converts back to a string.
>
> Don't laugh. I've seen it in production code.

### The Self-Deprecating Admission

> I spent three hours debugging a race condition before noticing I'd typed `=` instead of `==`. We've all been there. That's why we have linters.

### The Unexpected Comparison

> Debugging is like being the detective in a crime movie where you are also the murderer.

## 5. The "Aha!" Structure Template

```markdown
## [Problem Statement as Question]

You've probably encountered [familiar situation].

The obvious approach is [common solution]:

```code
[naive implementation]
```

This works... until [edge case or scale issue].

[Show the failure scenario]

The insight is: [key realization]

Instead, we can:

```code
[better implementation]
```

Notice how [specific improvement]. This is the principle of [named concept]:

> **[Principle Box]**: [One-sentence version of the insight]
```

## 6. Paragraph Length Guide

### One-sentence paragraphs for:
- Key insights
- Dramatic revelations
- Punchy conclusions
- Transitions

### Two-sentence paragraphs for:
- Quick examples
- Brief asides
- Setup before code

### Three-four sentence paragraphs for:
- Explanations
- Scenarios
- Analysis

### Never more than four sentences.

## 7. Code Example Guidelines

### Minimal
Remove everything not essential to the point.

```ruby
# ❌ Too much
class UserService
  def initialize(repository, logger, cache, config)
    @repository = repository
    @logger = logger
    @cache = cache
    @config = config
  end

  def find_user(id)
    @logger.info("Finding user #{id}")
    cached = @cache.get("user:#{id}")
    return cached if cached
    user = @repository.find(id)
    @cache.set("user:#{id}", user, ttl: @config.cache_ttl)
    user
  end
end

# ✅ Just enough
class UserService
  def initialize(repository)
    @repository = repository  # Injected, not created
  end

  def find_user(id)
    @repository.find(id)
  end
end
```

### Progressive
Show evolution from broken to fixed.

```ruby
# First attempt (broken)
def process(items)
  items.each { |i| save(i) }  # What if one fails?
end

# Second attempt (better)
def process(items)
  items.each do |i|
    save(i)
  rescue => e
    log_error(e)  # But we continue with bad data...
  end
end

# Final (robust)
def process(items)
  results = items.map { |i| [i, safely_save(i)] }
  failures = results.select { |_, success| !success }
  raise BatchError, failures if failures.any?
end
```

## 8. Principle Box Formats

### Numbered Tip
> **Tip 23: Don't Repeat Yourself**
> Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

### Highlighted Insight
> 💡 **The key insight**: Complexity isn't the enemy. *Unnecessary* complexity is.

### Warning Box
> ⚠️ **Watch out**: If you find yourself adding a boolean parameter, you probably need two methods.

## 9. Friendly Warning Pattern

```markdown
It's tempting to [common mistake] because [why it seems reasonable].

I've done this. [Brief admission of your own mistake]

The problem emerges when [specific failure scenario]:

[Show what goes wrong]

Instead, [better approach]:

[Show the fix]
```

## 10. Callback Examples

### Open with question, close with answer

**Opening**: "Why do we bother with tests if we're just going to rewrite everything?"

**Closing**: "So why bother with tests? Because they're not protecting the code. They're protecting the behavior. The code can change; the contract shouldn't."

### Open with scenario, close with transformation

**Opening**: "It's 3 AM. Your pager goes off. The database is on fire."

**Closing**: "Now when your pager goes off at 3 AM—and it will—you'll have the logs, the metrics, and the runbooks to handle it. You might even get back to sleep."
