---
title: "Notion Research & Documentation"
description: "跨 Notion 工作区搜索信息，综合发现并生成结构化研究文档"
category: "research"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Notion"
tags: ["notion", "research", "documentation", "synthesis"]
date: 2026-03-20
---


# Research & Documentation

Pull relevant Notion pages, synthesize findings, and publish clear briefs or reports (with citations and links to sources).

## Quick start
1) Find sources with `Notion:notion-search` using targeted queries; confirm scope with the user.
2) Fetch pages via `Notion:notion-fetch`; note key sections and capture citations (`reference/citations.md`).
3) Choose output format (brief, summary, comparison, comprehensive report) using `reference/format-selection-guide.md`.
4) Draft in Notion with `Notion:notion-create-pages` using the matching template (quick, summary, comparison, comprehensive).
5) Link sources and add a references/citations section; update as new info arrives with `Notion:notion-update-page`.

## Workflow
### 0) If any MCP call fails because Notion MCP is not connected, pause and set it up:
1. Add the Notion MCP:
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Enable remote MCP client:
   - Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
3. Log in with OAuth:
   - `codex mcp login notion`

After successful login, the user will have to restart codex. You should finish your answer and tell them so when they try again they can continue with Step 1.

### 1) Gather sources
- Search first (`Notion:notion-search`); refine queries, and ask the user to confirm if multiple results appear.
- Fetch relevant pages (`Notion:notion-fetch`), skim for facts, metrics, claims, constraints, and dates.
- Track each source URL/ID for later citation; prefer direct quotes for critical facts.

### 2) Select the format
- Quick readout → quick brief.
- Single-topic dive → research summary.
- Option tradeoffs → comparison.
- Deep dive / exec-ready → comprehensive report.
- See `reference/format-selection-guide.md` for when to pick each.

### 3) Synthesize
- Outline before writing; group findings by themes/questions.
- Note evidence with source IDs; flag gaps or contradictions.
- Keep user goal in view (decision, summary, plan, recommendation).

### 4) Create the doc
- Pick the matching template in `reference/` (brief, summary, comparison, comprehensive) and adapt it.
- Create the page with `Notion:notion-create-pages`; include title, summary, key findings, supporting evidence, and recommendations/next steps when relevant.
- Add citations inline and a references section; link back to source pages.

### 5) Finalize & handoff
- Add highlights, risks, and open questions.
- If the user needs follow-ups, create tasks or a checklist in the page; link any task database entries if applicable.
- Share a short changelog or status using `Notion:notion-update-page` when updating.

## References and examples
- `reference/` — search tactics, format selection, templates, and citation rules (e.g., `advanced-search.md`, `format-selection-guide.md`, `research-summary-template.md`, `comparison-template.md`, `citations.md`).
- `examples/` — end-to-end walkthroughs (e.g., `competitor-analysis.md`, `technical-investigation.md`, `market-research.md`, `trip-planning.md`).


---

## Example: competitor analysis

# Example: Competitor Analysis

## User Request

> "Research competitor pricing models and create a comparison document"

## Workflow Execution

### Step 1: Search for Competitor Information

```
Notion:notion-search
query: "competitor pricing"
query_type: "internal"
filters: {
  created_date_range: {
    start_date: "2024-01-01"
  }
}
```

**Results Found:**
- "Competitor Analysis - Stripe" (Product)
- "Market Research Q3 2024" (Strategy)
- "Pricing Strategy Discussion" (Product)
- "Competitor Feature Matrix" (Product)

### Step 2: Fetch and Analyze

```
Notion:notion-fetch for each page
```

**Extracted Information:**

**Stripe**:
- Pay-as-you-go: 2.9% + $0.30 per transaction
- No monthly fees
- Volume discounts available

**Square**:
- Pay-as-you-go: 2.6% + $0.10 per transaction
- Monthly plan: $29/month with lower rates
- Hardware costs separate

**PayPal**:
- Standard: 3.49% + $0.49 per transaction
- Advanced: $30/month + 2.59% + $0.49
- Multi-currency fees

**Adyen**:
- Interchange++ pricing model
- Custom enterprise pricing
- Setup and monthly fees apply

### Step 3: Create Comparison Document

```
Notion:notion-create-pages

pages: [{
  properties: {
    "title": "Competitor Pricing Analysis - Payment Processors"
  },
  content: "[Comparison document using template]"
}]
```

## Output Document

```markdown
# Competitor Pricing Analysis - Payment Processors

**Date**: October 14, 2025  
**Research Team**: Product Strategy

## Executive Summary

We analyzed four major payment processor competitors: Stripe, Square, PayPal, and Adyen. Pricing models vary from simple pay-as-you-go (Stripe) to complex interchange-plus (Adyen). Key insight: All competitors offer volume discounts for high-transaction merchants, with breakpoints typically at $100K/month processing volume.

## Comparison Matrix

| Feature | Stripe | Square | PayPal | Adyen |
|---------|--------|--------|--------|-------|
| **Base Rate** | 2.9% + $0.30 | 2.6% + $0.10 | 3.49% + $0.49 | Interchange++ |
| **Monthly Fee** | $0 | $0-29 | $0-30 | Custom |
| **Volume Discounts** | Yes, >$80K | Yes, >$250K | Yes, >$100K | Yes, custom |
| **Setup Fee** | $0 | $0 | $0 | $1,000-5,000 |
| **Multi-currency** | 1% extra | 3% extra | 3-4% extra | Included |
| **Chargeback Fee** | $15 | $15-25 | $20 | Custom |
| **Target Market** | Startups-Enterprise | Small-Medium | Small-Medium | Enterprise |

## Detailed Analysis

### Stripe

**Pricing Structure**:
- **Standard**: 2.9% + $0.30 per successful card charge
- **Volume discounts**: Available for businesses processing >$80,000/month
- **International cards**: +1% fee
- **Currency conversion**: 1% above market rate

**Strengths**:
- Simple, transparent pricing
- No setup fees or monthly minimums
- Excellent developer experience
- Quick onboarding

**Weaknesses**:
- Higher per-transaction fee for high volume
- Volume discounts less aggressive than Adyen

**Best for**: Startups and growth-stage companies needing quick integration

**Source**: <mention-page url="...">Competitor Analysis - Stripe</mention-page>

### Square

**Pricing Structure**:
- **Pay-as-you-go**: 2.6% + $0.10 per tap, dip, or swipe
- **Keyed-in**: 3.5% + $0.15
- **Plus plan**: $29/month for lower rates (2.5% + $0.10)
- **Premium plan**: Custom pricing

**Strengths**:
- Lowest per-transaction fee for in-person
- All-in-one hardware + software
- No long-term contracts

**Weaknesses**:
- Higher rates for online/keyed transactions
- Hardware costs ($49-$299)
- Less suitable for online-only businesses

**Best for**: Brick-and-mortar retail and restaurants

**Source**: <mention-page url="...">Market Research Q3 2024</mention-page>

### PayPal

**Pricing Structure**:
- **Standard**: 3.49% + $0.49 per transaction
- **Advanced**: $30/month + 2.59% + $0.49
- **Payments Pro**: Additional $30/month for direct credit card processing

**Strengths**:
- Huge customer base (PayPal checkout)
- Buyer protection increases trust
- International reach (200+ countries)

**Weaknesses**:
- Highest per-transaction fees
- Complex fee structure
- Account holds and reserves common

**Best for**: Businesses where PayPal brand trust matters (e-commerce, marketplaces)

**Source**: <mention-page url="...">Pricing Strategy Discussion</mention-page>

### Adyen

**Pricing Structure**:
- **Interchange++**: Actual interchange + scheme fees + fixed markup
- **Setup fee**: $1,000-5,000 (negotiable)
- **Monthly minimum**: Typically $10,000+ processing volume
- **Per-transaction**: Interchange + 0.6% + $0.12 (example)

**Strengths**:
- Most transparent cost structure at scale
- Lowest effective rate for high volume
- True multi-currency (100+ currencies)
- Direct connections to schemes

**Weaknesses**:
- Complex pricing requires analysis
- High minimums ($10K+/month)
- Longer integration time
- Not suitable for small businesses

**Best for**: Enterprise with $1M+/month processing volume

**Source**: <mention-page url="...">Competitor Feature Matrix</mention-page>

## Pricing Trends & Insights

### Volume-Based Discounting
All competitors offer discounts at scale:
- **Entry point**: $80K-$250K/month processing
- **Typical discount**: 10-30 basis points reduction
- **Negotiation leverage**: Begins at $500K/month+

### Hidden Costs to Consider

| Cost Type | Stripe | Square | PayPal | Adyen |
|-----------|--------|--------|--------|-------|
| Chargeback | $15 | $15-25 | $20 | $15-25 |
| Account verification | $0 | $0 | $0 | Varies |
| PCI compliance | $0 | $0 | $0 | $0 |
| Currency conversion | 1% | 3% | 3-4% | 0% |
| Refund fees | Returned | Returned | Not returned | Varies |

### Market Positioning

```
High Volume / Enterprise
    ↑
    |                    Adyen
    |                      
    |         Stripe             
    |    
    |  Square    PayPal
    |
    └──────────────────→
      Small / Simple        Complex / International
```

## Strategic Implications

### For Startups (<$100K/month)
**Recommended**: Stripe
- Lowest friction to start
- No upfront costs
- Great documentation
- Acceptable rates at this scale

### For Growing Companies ($100K-$1M/month)
**Recommended**: Stripe or Square
- Negotiate volume discounts
- Evaluate interchange++ if international
- Consider Square if in-person dominant

### For Enterprises (>$1M/month)
**Recommended**: Adyen or Negotiated Stripe
- Interchange++ models save significantly
- Direct scheme connections
- Multi-region capabilities matter
- ROI on integration complexity

## Recommendations

1. **Immediate**: Benchmark our current 2.8% + $0.25 against Stripe's standard
2. **Short-term**: Request volume discount quote from Stripe at our current $150K/month
3. **Long-term**: Evaluate Adyen when we cross $1M/month threshold

## Next Steps

- [ ] Request detailed pricing proposal from Stripe for volume discounts
- [ ] Create pricing calculator comparing all 4 at different volume levels
- [ ] Interview customers about payment method preferences
- [ ] Analyze our transaction mix (domestic vs international, card types)

## Sources

### Primary Research
- <mention-page url="...">Competitor Analysis - Stripe</mention-page>
- <mention-page url="...">Market Research Q3 2024</mention-page>
- <mention-page url="...">Pricing Strategy Discussion</mention-page>
- <mention-page url="...">Competitor Feature Matrix</mention-page>

### External References
- Stripe.com pricing page (Oct 2025)
- Square pricing documentation
- PayPal merchant fees
- Adyen pricing transparency report
```

## Key Success Factors

1. **Structured comparison**: Matrix format for quick scanning
2. **Multiple dimensions**: Price, features, target market
3. **Strategic recommendations**: Not just data, but implications
4. **Visual elements**: Table and positioning diagram
5. **Actionable next steps**: Clear recommendations
6. **Comprehensive sources**: Internal research + external validation

## Workflow Pattern Demonstrated

- **Date-filtered search** (recent information only)
- **Multiple competitor synthesis** (4 different companies)
- **Comparison template** (matrix + detailed analysis)
- **Strategic layer** (implications and recommendations)
- **Action-oriented** (next steps included)

---

## Example: market research

# Example: Market Research

**User Request**: "Research the current state of AI coding assistants market and create a summary document in Notion"

## Workflow

### 1. Search
```
Notion:notion-search
query: "AI coding assistants market"
```
Found 3 relevant pages across Engineering, Strategy, and Product teamspaces.

### 2. Fetch & Analyze
```
Notion:notion-fetch (3x)
```
Extracted market size, competitive landscape, technology trends from source pages.

### 3. Create Documentation
```
Notion:notion-create-pages
```

## Output (Condensed)

```markdown
# AI Coding Assistants Market Research - Oct 2025

## Executive Summary
The AI coding assistant market is experiencing 150%+ YoY growth. GitHub Copilot dominates with 60% share, but specialized tools are gaining traction in specific niches.

## Key Findings

### Market Size and Growth
$800M in 2024 → $2.5B projected by 2026. Developer adoption: 23% (2023) → 47% (2024).
Source: <mention-page url="...">Market Trends Q3 2025</mention-page>

### Competitive Landscape
- GitHub Copilot: 60% (strong IDE integration)
- Cursor: 15% (rapid growth, full IDE)
- Tabnine: 10% (enterprise, on-premise)
- Cody: 5% (codebase-aware)
- CodeWhisperer: 8% (AWS integration)
Source: <mention-page url="...">AI Tools Competitive Analysis</mention-page>

### Technology Trends
Key differentiators: context awareness, customization, multi-modal interfaces, code verification.
Source: <mention-page url="...">Developer Tools Landscape</mention-page>

## Next Steps
1. Monitor Cursor growth and feature releases
2. Evaluate Cody's codebase-aware capabilities
3. Document enterprise security/compliance requirements
4. Track pricing trends
```

## Key Takeaways
- Found relevant pages across multiple teamspaces
- Synthesized competitive, market, and technical perspectives
- Used proper citations linking to source pages
- Created actionable recommendations

---

## Example: technical investigation

# Example: Technical Investigation

## User Request

> "Research our current caching strategy and create a technical summary"

## Workflow Execution

### Step 1: Search for Caching Information

```
Notion:notion-search
query: "caching strategy architecture"
query_type: "internal"
teamspace_id: "engineering-teamspace-id"
```

**Results Found:**
- "System Architecture Overview" (Engineering)
- "Redis Implementation Guide" (Backend Docs)
- "Performance Optimization - Q3 2024" (Engineering)
- "API Caching Decision Record" (Architecture)

### Step 2: Fetch Relevant Pages

```
Notion:notion-fetch
id: "system-architecture-page-url"
```

Extracted: Current caching architecture uses Redis for API responses, Memcached for session storage.

```
Notion:notion-fetch
id: "redis-implementation-guide-url"
```

Extracted: Implementation details, TTL settings, invalidation strategies.

```
Notion:notion-fetch
id: "api-caching-decision-record-url"
```

Extracted: Why Redis was chosen over alternatives, trade-offs considered.

### Step 3: Synthesize Findings

**Key findings identified:**
- Two-tier caching: Redis (API responses) + Memcached (sessions)
- TTL strategy: 5 minutes for dynamic data, 1 hour for static
- Invalidation: Event-driven for critical updates
- Performance impact: 75% reduction in database load
- Known issues: Cache stampede on popular endpoints

### Step 4: Create Technical Summary

```
Notion:notion-create-pages

parent: { page_id: "engineering-docs-parent-id" }

pages: [{
  properties: {
    "title": "Technical Summary: Caching Strategy - Oct 2025"
  },
  content: "[Structured technical summary using template]"
}]
```

## Output Document

```markdown
# Technical Summary: Caching Strategy - Oct 2025

## Executive Summary

Our caching infrastructure uses a two-tier approach with Redis for API response caching and Memcached for session management. This strategy has reduced database load by 75% and improved API response times from 200ms to 50ms average.

## Architecture Overview

### Layer 1: API Response Caching (Redis)
**Technology**: Redis 7.0 cluster (3 nodes)
**Purpose**: Cache GET endpoint responses
**TTL Strategy**:
- Dynamic content: 5 minutes
- Static content: 1 hour
- User-specific: 15 minutes

**Source**: <mention-page url="...">System Architecture Overview</mention-page>

### Layer 2: Session Storage (Memcached)
**Technology**: Memcached 1.6
**Purpose**: User session data, temporary state
**TTL**: 24 hours (session lifetime)

## Implementation Details

### Cache Key Format
```
api:v1:{endpoint}:{params_hash}
session:{user_id}:{session_id}
```

### Invalidation Strategy
- **Event-driven**: Critical data changes trigger immediate invalidation
- **Time-based**: TTL expiration for non-critical data
- **Manual**: Admin tools for emergency cache clear

**Source**: <mention-page url="...">Redis Implementation Guide</mention-page>

## Decision Rationale

### Why Redis for API Caching?

**Pros**:
- Advanced data structures (sorted sets, hashes)
- Built-in TTL with automatic eviction
- Pub/sub for cache invalidation events
- Persistence options for durability

**Cons**:
- Higher memory usage than Memcached
- More complex cluster management

**Decision**: Chosen for flexibility and rich feature set needed for API caching.

**Source**: <mention-page url="...">API Caching Decision Record</mention-page>

### Why Memcached for Sessions?

**Pros**:
- Simpler, lighter weight
- Excellent for key-value storage
- Lower memory footprint

**Cons**:
- No persistence
- Limited data structures

**Decision**: Perfect fit for ephemeral session data where simplicity is valued.

## Performance Impact

| Metric | Before Caching | After Caching | Improvement |
|--------|----------------|---------------|-------------|
| Avg Response Time | 200ms | 50ms | 75% faster |
| Database Load | 100% | 25% | 75% reduction |
| Cache Hit Rate | - | 85% | - |
| Peak RPS Handled | 1,000 | 4,000 | 4x increase |

**Source**: <mention-page url="...">Performance Optimization - Q3 2024</mention-page>

## Known Issues & Limitations

### Cache Stampede
**Issue**: When popular cache entries expire, multiple requests hit database simultaneously

**Mitigation**: Implemented probabilistic early expiration and request coalescing

**Status**: Reduced by 90% but not eliminated

### Stale Data Risk
**Issue**: Cached data can be up to TTL duration stale

**Mitigation**: Event-driven invalidation for critical data paths

**Status**: Acceptable trade-off for performance gains

## Monitoring & Observability

**Metrics tracked**:
- Cache hit/miss rates per endpoint
- Memory usage and eviction rates
- Response time distributions
- Invalidation event frequency

**Tools**: DataDog dashboards, CloudWatch alarms

## Future Considerations

1. **Edge Caching**: Evaluate CDN integration for static assets
2. **Cache Warming**: Pre-populate cache for predictable traffic spikes
3. **Adaptive TTLs**: Adjust TTLs based on data change frequency
4. **Regional Caching**: Multi-region cache replication for global performance

## Related Documentation

- <mention-page url="...">System Architecture Overview</mention-page>
- <mention-page url="...">Redis Implementation Guide</mention-page>
- <mention-page url="...">API Caching Decision Record</mention-page>
- <mention-page url="...">Performance Optimization - Q3 2024</mention-page>

## Appendix: Configuration Examples

### Redis Configuration
```yaml
maxmemory: 8gb
maxmemory-policy: allkeys-lru
tcp-keepalive: 60
```

### Common Cache Operations
```python
# Set with TTL
cache.set(key, value, ttl=300)

# Get with fallback
value = cache.get(key) or fetch_from_db(key)

# Invalidate pattern
cache.delete_pattern("api:v1:users:*")
```
```

## Key Success Factors

1. **Multiple source integration**: Combined architecture docs, implementation guides, and decision records
2. **Technical depth**: Included configuration, code examples, metrics
3. **Decision context**: Explained why choices were made, not just what
4. **Practical focus**: Real performance numbers and known issues
5. **Future-looking**: Noted areas for improvement
6. **Well-cited**: Every major point links back to source material

## Workflow Pattern Demonstrated

This example shows the complete research workflow:
- **Scoped search** (teamspace filter for engineering)
- **Multi-page synthesis** (4 different sources)
- **Technical template** (architecture-focused format)
- **Proper placement** (under engineering docs)
- **Comprehensive citations** (links to all sources)

---

## Example: trip planning

# Example: Group Trip Research & Planning

**User Request**: "Research and plan our friends' trip to Japan in March - we're 6 people looking for 10 days"

## Workflow

### 1. Search Existing Notes
```
Notion:notion-search
query: "Japan travel"
```
Found: Japan Travel Guide (from friend), Tokyo Restaurants, Kyoto Temple Guide

### 2. Fetch & Extract Tips
```
Notion:notion-fetch (3x)
```
**Key info from previous travelers:**
- Best time: March-April (cherry blossoms)
- Must-see: Tokyo, Kyoto, Osaka
- Budget: $200-300/day (mid-range)
- Book accommodations 3 months ahead
- Get JR Pass before arrival
- Top restaurants: Sushi Dai, Ichiran Ramen, Tsunahachi Tempura

### 3. Research & Synthesize
Combined previous traveler insights with:
- Flight options and prices
- Accommodation types (hotels/ryokans/Airbnb)
- Transportation (JR Pass essential)
- 10-day itinerary structure
- Budget breakdown

### 4. Create Comprehensive Plan
```
Notion:notion-create-pages
parent: { page_id: "travel-plans-parent-id" }
pages: [{
  properties: {
    title: "Japan Trip 2026 - March 15-25 (10 Days)"
  },
  content: "[Full trip plan with itinerary, budget, tips...]"
}]
```

## Output Sample

```markdown
# Japan Trip 2026 - March 15-25 (10 Days)

## Trip Overview
**Dates**: March 15-25, 2026 (Cherry Blossom Season 🌸)
**Group**: 6 people | **Budget**: $3,000-4,000/person

## Itinerary Summary

**Days 1-3: Tokyo**
- Arrive, explore Shibuya, Harajuku, Shinjuku
- Visit Tsukiji Market, Imperial Palace, Sensoji Temple
- Experience Tokyo nightlife, teamLab Borderless

**Days 4-5: Hakone**  
- Day trip from Tokyo
- Hot springs, Mt. Fuji views, Lake Ashi cruise

**Days 6-8: Kyoto**
- Bullet train from Tokyo
- Fushimi Inari, Kinkaku-ji, Arashiyama Bamboo Grove
- Geisha district (Gion), traditional tea ceremony

**Days 9-10: Osaka + Depart**
- Osaka Castle, Dotonbori food district
- Nara day trip (deer park, Todai-ji Temple)
- Return flight from Osaka (KIX)

## Budget Breakdown (per person)
- **Flights**: $900-1,200 (round-trip)
- **Accommodations**: $700-1,000 (9 nights)
- **JR Pass**: $280 (7-day pass)
- **Food**: $500-700 ($50-70/day)
- **Activities**: $300-400
- **Local transport**: $100
**Total**: $2,780-3,680

## Key Bookings
- **Flights**: Book 3-4 months ahead
- **Hotels**: Book now (cherry blossom season)
  - Tokyo: Shinjuku area (2 nights) + Asakusa (1 night)
  - Kyoto: Gion area (3 nights)
  - Osaka: Namba area (2 nights)
- **JR Pass**: Order 2-3 weeks before travel
- **Restaurants**: Reserve 1 week ahead (Sushi Dai, high-end spots)

## Essential Tips
Source: <mention-page url="...">Japan Travel Guide</mention-page>
- Get pocket WiFi or eSIM on arrival
- Download: Google Translate, Hyperdia (train routes), Tabelog (restaurants)
- Cash-heavy country - withdraw at 7-Eleven ATMs
- Shoes off in temples, ryokans, some restaurants
- Trains extremely punctual - don't be late
- Learn basic phrases: arigatou, sumimasen, itadakimasu

## Packing List
- Comfortable walking shoes (10k+ steps/day)
- Light jacket (March 55-65°F)
- Backpack for day trips
- Cash pouch
- Portable charger

## Next Steps
- [ ] Book flights (target: <$1,100/person)
- [ ] Order JR Passes
- [ ] Book hotels (Tokyo → Kyoto → Osaka)
- [ ] Create shared expense tracker
- [ ] Schedule group planning call

## Sources
- <mention-page url="...">Japan Travel Guide</mention-page> (Sarah's 2024 trip)
- <mention-page url="...">Tokyo Restaurant Recommendations</mention-page>
- <mention-page url="...">Kyoto Temple Guide</mention-page>
```

## Key Takeaways
- Leveraged previous traveler notes from Notion
- Combined personal insights with research
- Created actionable itinerary with budget breakdown
- Included practical tips from experienced travelers
- Set clear next steps for group coordination
