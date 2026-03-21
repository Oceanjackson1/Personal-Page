---
title: "Market Sizing Analysis"
description: "This skill should be used when the user asks to 'calculate TAM', 'determine SAM', 'estimate SOM', 'size the market', 'calculate market opportunity', 'what's the total addressable market', or..."
category: "development"
source: "community"
author: "Community"
tags: ["market", "sizing", "analysis"]
date: 2026-03-20
---

# Market Sizing Analysis

Comprehensive market sizing methodologies for calculating Total Addressable Market (TAM), Serviceable Available Market (SAM), and Serviceable Obtainable Market (SOM) for startup opportunities.

## Use this skill when

- Working on market sizing analysis tasks or workflows
- Needing guidance, best practices, or checklists for market sizing analysis

## Do not use this skill when

- The task is unrelated to market sizing analysis
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Overview

Market sizing provides the foundation for startup strategy, fundraising, and business planning. Calculate market opportunity using three complementary methodologies: top-down (industry reports), bottom-up (customer segment calculations), and value theory (willingness to pay).

## Core Concepts

### The Three-Tier Market Framework

**TAM (Total Addressable Market)**
- Total revenue opportunity if achieving 100% market share
- Defines the universe of potential customers
- Used for long-term vision and market validation
- Example: All email marketing software revenue globally

**SAM (Serviceable Available Market)**
- Portion of TAM targetable with current product/service
- Accounts for geographic, segment, or capability constraints
- Represents realistic addressable opportunity
- Example: AI-powered email marketing for e-commerce in North America

**SOM (Serviceable Obtainable Market)**
- Realistic market share achievable in 3-5 years
- Accounts for competition, resources, and market dynamics
- Used for financial projections and fundraising
- Example: 2-5% of SAM based on competitive landscape

### When to Use Each Methodology

**Top-Down Analysis**
- Use when established market research exists
- Best for mature, well-defined markets
- Validates market existence and growth
- Starts with industry reports and narrows down

**Bottom-Up Analysis**
- Use when targeting specific customer segments
- Best for new or niche markets
- Most credible for investors
- Builds from customer data and pricing

**Value Theory**
- Use when creating new market categories
- Best for disruptive innovations
- Estimates based on value creation
- Calculates willingness to pay for problem solution

## Three-Methodology Framework

### Methodology 1: Top-Down Analysis

Start with total market size and narrow to addressable segments.

**Process:**
1. Identify total market category from research reports
2. Apply geographic filters (target regions)
3. Apply segment filters (target industries/customers)
4. Calculate competitive positioning adjustments

**Formula:**
```
TAM = Total Market Category Size
SAM = TAM × Geographic % × Segment %
SOM = SAM × Realistic Capture Rate (2-5%)
```

**When to use:** Established markets with available research (e.g., SaaS, fintech, e-commerce)

**Strengths:** Quick, uses credible data, validates market existence

**Limitations:** May overestimate for new categories, less granular

### Methodology 2: Bottom-Up Analysis

Build market size from customer segment calculations.

**Process:**
1. Define target customer segments
2. Estimate number of potential customers per segment
3. Determine average revenue per customer
4. Calculate realistic penetration rates

**Formula:**
```
TAM = Σ (Segment Size × Annual Revenue per Customer)
SAM = TAM × (Segments You Can Serve / Total Segments)
SOM = SAM × Realistic Penetration Rate (Year 3-5)
```

**When to use:** B2B, niche markets, specific customer segments

**Strengths:** Most credible for investors, granular, defensible

**Limitations:** Requires detailed customer research, time-intensive

### Methodology 3: Value Theory

Calculate based on value created and willingness to pay.

**Process:**
1. Identify problem being solved
2. Quantify current cost of problem (time, money, inefficiency)
3. Calculate value of solution (savings, gains, efficiency)
4. Estimate willingness to pay (typically 10-30% of value)
5. Multiply by addressable customer base

**Formula:**
```
Value per Customer = Problem Cost × % Solved by Solution
Price per Customer = Value × Willingness to Pay % (10-30%)
TAM = Total Potential Customers × Price per Customer
SAM = TAM × % Meeting Buy Criteria
SOM = SAM × Realistic Adoption Rate
```

**When to use:** New categories, disruptive innovations, unclear existing markets

**Strengths:** Shows value creation, works for new markets

**Limitations:** Requires assumptions, harder to validate

## Step-by-Step Process

### Step 1: Define the Market

Clearly specify what market is being measured.

**Questions to answer:**
- What problem is being solved?
- Who are the target customers?
- What's the product/service category?
- What's the geographic scope?
- What's the time horizon?

**Example:**
- Problem: E-commerce companies struggle with email marketing automation
- Customers: E-commerce stores with >$1M annual revenue
- Category: AI-powered email marketing software
- Geography: North America initially, global expansion
- Horizon: 3-5 year opportunity

### Step 2: Gather Data Sources

Identify credible data for calculations.

**Top-Down Sources:**
- Industry research reports (Gartner, Forrester, IDC)
- Government statistics (Census, BLS, trade associations)
- Public company filings and earnings
- Market research firms (Statista, CB Insights, PitchBook)

**Bottom-Up Sources:**
- Customer interviews and surveys
- Sales data and CRM records
- Industry databases (LinkedIn, ZoomInfo, Crunchbase)
- Competitive intelligence
- Academic research

**Value Theory Sources:**
- Customer problem quantification
- Time/cost studies
- ROI case studies
- Pricing research and willingness-to-pay surveys

### Step 3: Calculate TAM

Apply chosen methodology to determine total market.

**For Top-Down:**
1. Find total category size from research
2. Document data source and year
3. Apply growth rate if needed
4. Validate with multiple sources

**For Bottom-Up:**
1. Count total potential customers
2. Calculate average annual revenue per customer
3. Multiply to get TAM
4. Break down by segment

**For Value Theory:**
1. Quantify total addressable customer base
2. Calculate value per customer
3. Estimate pricing based on value
4. Multiply for TAM

### Step 4: Calculate SAM

Narrow TAM to serviceable addressable market.

**Apply Filters:**
- Geographic constraints (regions you can serve)
- Product limitations (features you currently have)
- Customer requirements (size, industry, use case)
- Distribution channel access
- Regulatory or compliance restrictions

**Formula:**
```
SAM = TAM × (% matching all filters)
```

**Example:**
- TAM: $10B global email marketing
- Geographic filter: 40% (North America)
- Product filter: 30% (e-commerce focus)
- Feature filter: 60% (need AI capabilities)
- SAM = $10B × 0.40 × 0.30 × 0.60 = $720M

### Step 5: Calculate SOM

Determine realistic obtainable market share.

**Consider:**
- Current market share of competitors
- Typical market share for new entrants (2-5%)
- Resources available (funding, team, time)
- Go-to-market effectiveness
- Competitive advantages
- Time to achieve (3-5 years typically)

**Conservative Approach:**
```
SOM (Year 3) = SAM × 2%
SOM (Year 5) = SAM × 5%
```

**Example:**
- SAM: $720M
- Year 3 SOM: $720M × 2% = $14.4M
- Year 5 SOM: $720M × 5% = $36M

### Step 6: Validate and Triangulate

Cross-check using multiple methods.

**Validation Techniques:**
1. Compare top-down and bottom-up results (should be within 30%)
2. Check against public company revenues in space
3. Validate customer count assumptions
4. Sense-check pricing assumptions
5. Review with industry experts
6. Compare to similar market categories

**Red Flags:**
- TAM that's too small (< $1B for VC-backed startups)
- TAM that's too large (unsupported by data)
- SOM that's too aggressive (> 10% in 5 years for new entrant)
- Inconsistency between methodologies (> 50% difference)

## Industry-Specific Considerations

### SaaS Markets

**Key Metrics:**
- Number of potential businesses in target segment
- Average contract value (ACV)
- Typical market penetration rates
- Expansion revenue potential

**TAM Calculation:**
```
TAM = Total Target Companies × Average ACV × (1 + Expansion Rate)
```

### Marketplace Markets

**Key Metrics:**
- Gross Merchandise Value (GMV) of category
- Take rate (% of GMV you capture)
- Total transactions or users

**TAM Calculation:**
```
TAM = Total Category GMV × Expected Take Rate
```

### Consumer Markets

**Key Metrics:**
- Total addressable users/households
- Average revenue per user (ARPU)
- Engagement frequency

**TAM Calculation:**
```
TAM = Total Users × ARPU × Purchase Frequency per Year
```

### B2B Services

**Key Metrics:**
- Number of target companies by size/industry
- Average project value or retainer
- Typical buying frequency

**TAM Calculation:**
```
TAM = Total Target Companies × Average Deal Size × Deals per Year
```

## Presenting Market Sizing

### For Investors

**Structure:**
1. Market definition and problem scope
2. TAM/SAM/SOM with methodology
3. Data sources and assumptions
4. Growth projections and drivers
5. Competitive landscape context

**Key Points:**
- Lead with bottom-up calculation (most credible)
- Show triangulation with top-down
- Explain conservative assumptions
- Link to revenue projections
- Highlight market growth rate

### For Strategy

**Structure:**
1. Addressable customer segments
2. Prioritization by opportunity size
3. Entry strategy by segment
4. Expected penetration timeline
5. Resource requirements

**Key Points:**
- Focus on SAM and SOM
- Show segment-level detail
- Connect to go-to-market plan
- Identify expansion opportunities
- Discuss competitive positioning

## Common Mistakes to Avoid

**Mistake 1: Confusing TAM with SAM**
- Don't claim entire market as addressable
- Apply realistic product/geographic constraints
- Be honest about serviceable market

**Mistake 2: Overly Aggressive SOM**
- New entrants rarely capture > 5% in 5 years
- Account for competition and resources
- Show realistic ramp timeline

**Mistake 3: Using Only Top-Down**
- Investors prefer bottom-up validation
- Top-down alone lacks credibility
- Always triangulate with multiple methods

**Mistake 4: Cherry-Picking Data**
- Use consistent, recent data sources
- Don't mix methodologies inappropriately
- Document all assumptions clearly

**Mistake 5: Ignoring Market Dynamics**
- Account for market growth/decline
- Consider competitive intensity
- Factor in switching costs and barriers

## Additional Resources

### Reference Files

For detailed methodologies and frameworks:
- **`references/methodology-deep-dive.md`** - Comprehensive guide to each methodology with step-by-step worksheets
- **`references/data-sources.md`** - Curated list of market research sources, databases, and tools
- **`references/industry-templates.md`** - Specific templates for SaaS, marketplace, consumer, B2B, and fintech markets

### Example Files

Working examples with complete calculations:
- **`examples/saas-market-sizing.md`** - Complete TAM/SAM/SOM for a B2B SaaS product
- **`examples/marketplace-sizing.md`** - Marketplace platform market opportunity calculation
- **`examples/value-theory-example.md`** - Value-based market sizing for disruptive innovation

Use these examples as templates for your own market sizing analysis. Each includes real numbers, data sources, and assumptions documented clearly.

## Quick Start

To perform market sizing analysis:

1. **Define the market** - Problem, customers, category, geography
2. **Choose methodology** - Bottom-up (preferred) or top-down + triangulation
3. **Gather data** - Industry reports, customer data, competitive intelligence
4. **Calculate TAM** - Apply methodology formula
5. **Narrow to SAM** - Apply product, geographic, segment filters
6. **Estimate SOM** - 2-5% realistic capture rate
7. **Validate** - Cross-check with alternative methods
8. **Document** - Show methodology, sources, assumptions
9. **Present** - Structure for audience (investors, strategy, operations)

For detailed step-by-step guidance on each methodology, reference the files in `references/` directory. For complete worked examples, see `examples/` directory.

---

## Reference: Data Sources

# Market Sizing Data Sources

Curated list of credible sources for market research and sizing analysis.

## Industry Research Reports

### Premium Research Firms

**Gartner** (https://www.gartner.com)
- Technology market forecasts and sizing
- Magic Quadrants for competitive positioning
- Typical cost: $5K-$50K per report
- Best for: Enterprise software, IT services, emerging tech

**Forrester** (https://www.forrester.com)
- Business technology and digital transformation
- Wave evaluations for vendor comparison
- Typical cost: $3K-$30K per report
- Best for: Marketing tech, customer experience, B2B

**IDC** (https://www.idc.com)
- IT market intelligence and sizing
- Detailed segment breakdowns
- Typical cost: $4K-$40K per report
- Best for: Hardware, software, IT services

**McKinsey** (https://www.mckinsey.com/featured-insights)
- Free insights and reports
- Strategic industry analysis
- Best for: Industry trends, macroeconomic context

### Accessible Research

**Statista** (https://www.statista.com)
- Cost: $39/month individual, $199/month business
- Coverage: 80,000+ topics across industries
- Best for: Quick market size estimates, charts, trends

**CB Insights** (https://www.cbinsights.com)
- Cost: Custom pricing (typically $10K+/year)
- Coverage: Venture capital, startup markets
- Best for: Emerging markets, competitive intelligence

**PitchBook** (https://pitchbook.com)
- Cost: Institutional pricing
- Coverage: Private company valuations, M&A, VC
- Best for: Startup valuations, funding trends

**Grand View Research** (https://www.grandviewresearch.com)
- Cost: $2K-$5K per report
- Coverage: B2C and emerging markets
- Best for: Consumer markets, healthcare, cleantech

## Government and Public Data

### U.S. Government Sources

**U.S. Census Bureau** (https://www.census.gov)
- Free, authoritative demographic data
- Economic census every 5 years
- Best for: Business counts, demographics, spending

**Bureau of Labor Statistics** (https://www.bls.gov)
- Free employment and economic data
- Industry-specific statistics
- Best for: Employment trends, wages, productivity

**SEC EDGAR** (https://www.sec.gov/edgar)
- Free public company filings
- 10-K, 10-Q reports with segment revenue
- Best for: Validating market size with public company data

**Data.gov** (https://www.data.gov)
- Free government datasets
- Aggregates across agencies
- Best for: Specialized industry data

### International Sources

**OECD** (https://data.oecd.org)
- Free international economic data
- Best for: Cross-country comparisons

**World Bank** (https://data.worldbank.org)
- Free global development data
- Best for: Emerging markets, macro trends

**Eurostat** (https://ec.europa.eu/eurostat)
- Free European Union statistics
- Best for: European market sizing

## Trade Associations

Industry associations often publish market research:

**Software & SaaS**
- Software & Information Industry Association (SIIA)
- Cloud Security Alliance (CSA)

**E-commerce & Retail**
- National Retail Federation (NRF)
- Digital Commerce 360

**Financial Services**
- American Bankers Association (ABA)
- Financial Technology Association (FTA)

**Healthcare**
- Healthcare Information and Management Systems Society (HIMSS)
- American Hospital Association (AHA)

**Manufacturing**
- National Association of Manufacturers (NAM)
- Industrial Internet Consortium (IIC)

## Company and Customer Data

### B2B Databases

**LinkedIn Sales Navigator** ($99/month)
- Company and employee counts
- Industry filters
- Best for: B2B customer counting

**ZoomInfo** (Custom pricing)
- Company databases with firmographics
- Contact data
- Best for: B2B TAM calculations

**Crunchbase** ($29-$99/month)
- Startup company data
- Funding and employee information
- Best for: Tech startup markets

**BuiltWith** ($295-$995/month)
- Technology usage data
- Website analytics
- Best for: Technology adoption sizing

### Consumer Data

**Euromonitor** (Custom pricing)
- Consumer market research
- Best for: B2C product markets

**Nielsen** (Custom pricing)
- Consumer behavior and media
- Best for: CPG, retail, media markets

**Mintel** (Custom pricing)
- Consumer trends and insights
- Best for: B2C products and services

## Search and Discovery Tools

### Market Research Aggregators

**Research and Markets** (https://www.researchandmarkets.com)
- Aggregates reports from 100+ publishers
- $500-$10K per report
- Search across all major research firms

**MarketsandMarkets** (https://www.marketsandmarkets.com)
- Custom and syndicated research
- $4K-$10K per report
- Good for niche B2B markets

### Free Search Tools

**Google Scholar** (https://scholar.google.com)
- Free academic research
- Best for: Emerging technologies, academic validation

**SSRN** (https://www.ssrn.com)
- Free working papers
- Best for: Financial services, economics

**arXiv** (https://arxiv.org)
- Free preprints in CS, physics, etc.
- Best for: AI/ML, scientific markets

## Competitive Intelligence

### Public Company Analysis

**Yahoo Finance** (Free)
- Public company financials
- Segment revenue from earnings

**Seeking Alpha** (Free + Premium)
- Earnings transcripts
- Analyst estimates

**Public company investor relations**
- Annual reports (10-K)
- Investor presentations

### Private Company Intelligence

**PrivCo** (Custom pricing)
- Private company financials
- M&A transaction data

**Owler** (Free + Premium)
- Company profiles and news
- Revenue estimates

**SimilarWeb** (Free + Premium)
- Website traffic analytics
- Best for: Online business sizing

## Survey and Primary Research

### Survey Tools

**SurveyMonkey** ($25-$75/month)
- DIY surveys
- Best for: Customer willingness to pay

**Typeform** ($25-$83/month)
- Conversational surveys
- Best for: User research

**Qualtrics** (Enterprise pricing)
- Professional research platform
- Best for: Large-scale studies

### Panel Providers

**Respondent.io** ($100-$200 per response)
- Recruit professionals for interviews
- Best for: B2B customer research

**UserTesting** ($49 per participant)
- User research and testing
- Best for: Product validation

**Google Surveys** ($0.10-$3.50 per response)
- Quick consumer surveys
- Best for: Basic consumer insights

## Data Quality Checklist

When evaluating sources:

**Authority**
- [ ] Who published the research?
- [ ] What's their reputation?
- [ ] Do they have industry expertise?

**Methodology**
- [ ] How was data collected?
- [ ] What's the sample size?
- [ ] When was research conducted?

**Recency**
- [ ] Is data current (< 2 years old)?
- [ ] Has market changed significantly?
- [ ] Are growth rates still applicable?

**Consistency**
- [ ] Do multiple sources agree?
- [ ] Are definitions consistent?
- [ ] Do numbers triangulate?

**Relevance**
- [ ] Does it match your market definition?
- [ ] Is geography appropriate?
- [ ] Are segments aligned?

## Free vs. Paid Strategy

**Start with free sources:**
1. Government data for customer counts
2. Public company filings for segment revenue
3. Trade associations for industry trends
4. Google Scholar for academic research

**Upgrade to paid when:**
- Raising institutional funding (investors expect premium sources)
- Need detailed segment breakdowns
- Market is niche or emerging
- Free sources are outdated or insufficient

**Cost-effective approach:**
- Buy 1-2 key reports that cover your core market
- Use free sources for triangulation
- Supplement with primary research (customer interviews)
- Cite mix of free and paid sources

## Citation Best Practices

Always cite sources in market sizing:

**Format:**
```
Market Size: $X.XB
Source: [Publisher], [Report Name], [Date]
URL: [link if available]
```

**Example:**
```
Email Marketing Software TAM: $7.5B (2024)
Source: Gartner, "Market Share: Email Marketing Software, Worldwide, 2024"
Note: Includes all email marketing software revenue globally
```

**Include:**
- Publisher and report name
- Publication date
- Geography and scope
- Any adjustments made
- Link to source (if public)

## Keeping Research Current

**Set Google Alerts**
- Industry keywords
- Company names
- Market terms

**Follow Research Firms**
- Twitter accounts
- LinkedIn updates
- Free newsletter summaries

**Track Public Companies**
- Earnings calendars
- Investor relations pages
- Annual reports

**Join Industry Groups**
- LinkedIn groups
- Slack communities
- Trade associations

**Review Annually**
- Update market size with new data
- Adjust growth assumptions
- Revisit methodology if market changed

## Emergency Research Guide

**Need market size in < 2 hours?**

1. **Check Statista** (15 min) - Quick industry overview
2. **Find public companies** (30 min) - Get segment revenue from 10-Ks
3. **LinkedIn search** (20 min) - Count potential B2B customers
4. **Google Scholar** (20 min) - Find academic papers
5. **Calculate bottom-up** (30 min) - Customers × Price
6. **Triangulate** (15 min) - Compare sources

**Document everything:**
- Write down all sources
- Note all assumptions
- Show your methodology
- Caveat data quality

Better to have a defensible estimate with clear limitations than no data at all.

---

## Example: Saas Market Sizing

# SaaS Market Sizing Example: AI-Powered Email Marketing for E-Commerce

Complete TAM/SAM/SOM calculation for a B2B SaaS startup using bottom-up and top-down methodologies.

## Company Overview

**Product:** AI-powered email marketing automation platform
**Target:** E-commerce companies with $1M+ annual revenue
**Geography:** North America (initial), global expansion planned
**Pricing:** $500/month average (scales by email volume)
**Timeline:** 3-5 year market opportunity

## Methodology 1: Bottom-Up Analysis (Primary)

### Step 1: Define Target Customer Segments

**Segment Criteria:**
- E-commerce companies (D2C and marketplace sellers)
- $1M+ in annual revenue
- North America based
- Currently using email marketing

**Segment Breakdown:**

| Segment | Annual Revenue | Count | ACV | Priority |
|---------|---------------|-------|-----|----------|
| Small E-commerce | $1M-$5M | 85,000 | $3,600 | High |
| Mid-Market E-commerce | $5M-$50M | 18,000 | $9,600 | High |
| Enterprise E-commerce | $50M+ | 2,500 | $24,000 | Medium |

**Data Sources:**
- U.S. Census Bureau: E-commerce business counts
- Shopify, BigCommerce, WooCommerce: Published merchant counts
- Statista: E-commerce market statistics
- LinkedIn Sales Navigator: Company search validation

### Step 2: Calculate TAM (Total Addressable Market)

**Formula:**
```
TAM = Σ (Segment Count × Annual Contract Value)
```

**Calculation:**
```
Small E-commerce:   85,000 × $3,600  = $306M
Mid-Market:         18,000 × $9,600  = $173M
Enterprise:          2,500 × $24,000 = $60M
                                      --------
TAM (North America):                  $539M
```

**Global Expansion Multiplier:**
- North America = 35% of global e-commerce market
- Global TAM = $539M / 0.35 = $1.54B

**TAM = $1.54B globally, $539M North America**

### Step 3: Calculate SAM (Serviceable Available Market)

**Filters Applied:**

1. **Geographic Filter: North America Only (Year 1-2)**
   - Base TAM: $539M
   - Filter: 100% (starting in North America)
   - Result: $539M

2. **Product Capability Filter: AI-Ready Customers**
   - Customers ready to adopt AI email marketing
   - Excludes: Companies with basic email needs only
   - Filter: 45% (based on survey data)
   - Result: $539M × 0.45 = $242M

3. **Current Tool Filter: Addressable Switching Market**
   - Customers using incumbent tools who would switch
   - Excludes: Recently switched, custom built solutions
   - Filter: 70% (typical B2B SaaS switching market)
   - Result: $242M × 0.70 = $169M

**SAM = $169M**

**SAM Breakdown by Segment:**
```
Small E-commerce:   $306M × 0.45 × 0.70 = $96M (57%)
Mid-Market:         $173M × 0.45 × 0.70 = $54M (32%)
Enterprise:         $60M × 0.45 × 0.70  = $19M (11%)
```

### Step 4: Calculate SOM (Serviceable Obtainable Market)

**Market Share Assumptions:**

**Year 3 Target: 2.5% of SAM**
- Typical new entrant market share
- Requires strong product-market fit
- Assumes $10M in funding for GTM

**Year 5 Target: 5% of SAM**
- Achievable with scale and brand
- Requires effective sales and marketing
- Assumes additional funding for growth

**Calculation:**
```
SOM (Year 3) = $169M × 2.5% = $4.2M ARR
SOM (Year 5) = $169M × 5.0% = $8.5M ARR
```

**SOM by Segment (Year 5):**
```
Small E-commerce:   $96M × 5% = $4.8M ARR (565 customers)
Mid-Market:         $54M × 5% = $2.7M ARR (281 customers)
Enterprise:         $19M × 5% = $1.0M ARR (42 customers)
                                --------
Total:                          $8.5M ARR (888 customers)
```

### Bottom-Up Summary

| Metric | North America | Notes |
|--------|---------------|-------|
| **TAM** | $539M | All e-commerce $1M+ revenue |
| **SAM** | $169M | AI-ready, addressable switching market |
| **SOM (Year 3)** | $4.2M | 2.5% market share, 495 customers |
| **SOM (Year 5)** | $8.5M | 5% market share, 888 customers |

## Methodology 2: Top-Down Analysis (Validation)

### Step 1: Identify Total Market Category

**Market Category:** Email Marketing Software
**Source:** Gartner Market Share Report (2024)

**Global Email Marketing Software Market:**
- Market Size: $7.5B (2024)
- Growth Rate: 12% CAGR
- Geography: Worldwide

**Data Source:** Gartner, "Market Share: Email Marketing Software, Worldwide, 2024"

### Step 2: Apply Geographic Filter

**North America Market Share:**
- North America = 40% of global software spending
- Email Marketing NA = $7.5B × 0.40 = $3.0B

### Step 3: Apply Segment Filters

**E-Commerce Focus:**
- E-commerce email marketing = 25% of total email marketing
- E-commerce segment = $3.0B × 0.25 = $750M

**$1M+ Revenue Filter:**
- Companies with $1M+ revenue = 65% of e-commerce market
- TAM = $750M × 0.65 = $488M

**AI-Powered Subset:**
- AI-powered email marketing = 35% of market (growing rapidly)
- SAM = $488M × 0.35 = $171M

### Top-Down Summary

| Metric | Amount | Calculation |
|--------|--------|-------------|
| **TAM** | $488M | NA e-commerce email marketing $1M+ |
| **SAM** | $171M | AI-powered subset |

## Triangulation and Validation

### Comparing Methodologies

| Metric | Bottom-Up | Top-Down | Variance |
|--------|-----------|----------|----------|
| **TAM** | $539M | $488M | +10% |
| **SAM** | $169M | $171M | -1% |

**Validation Result:** ✅ Excellent alignment (< 2% variance on SAM)

**Why alignment matters:**
- Bottom-up and top-down within 10% gives high confidence
- SAM alignment of 1% is exceptional
- Use bottom-up as primary (more granular)
- Reference top-down for validation

### Public Company Validation

**Klaviyo (Public, KVYO):**
- 2024 Revenue: ~$700M
- Focus: E-commerce email/SMS marketing
- Market Share: ~46% of our SAM
- Validates large e-commerce email market exists

**Mailchimp (Intuit-owned):**
- 2024 Revenue: ~$800M (estimated)
- Broader focus, includes SMBs
- Significant e-commerce customer base

**Validation:** Market leaders have $700M-$800M revenue, supporting $1.5B+ global TAM

### Sanity Checks

**Customer Count Check:**
✅ 888 customers at Year 5 (5% market share) = reasonable
✅ Implies ~14,000 total addressable customers
✅ Aligns with estimated 105,000 e-commerce cos $1M+ in NA

**Average Revenue Check:**
✅ $8.5M ARR / 888 customers = $9,571 ACV
✅ Within expected range of $3.6K-$24K by segment
✅ Weighted average makes sense given segment mix

**Market Share Check:**
✅ 5% market share in Year 5 is achievable for well-funded startup
✅ Lower than Klaviyo (46%), appropriate for new entrant
✅ Room for growth beyond Year 5

## Growth Projections

### Market Growth Assumptions

**Email Marketing Market CAGR: 12%**
- Source: Gartner market forecast
- Drivers: E-commerce growth, marketing automation adoption

**AI Subset Growth: 25% CAGR**
- Higher than overall market
- AI adoption accelerating in marketing
- More companies seeking AI-powered tools

### SAM Evolution (5-Year Forecast)

| Year | SAM | Growth | Notes |
|------|-----|--------|-------|
| 2026 | $169M | - | Starting point |
| 2027 | $211M | +25% | AI adoption accelerating |
| 2028 | $264M | +25% | Mainstream adoption begins |
| 2029 | $330M | +25% | AI becomes table stakes |
| 2030 | $413M | +25% | Market maturity |

**Growing SAM Impact:**
- Year 5 SOM of 5% applied to $413M SAM = $20.6M potential
- Provides headroom for growth
- Supports expansion beyond initial 5% share

## Competitive Context

### Market Share Distribution

**Current Leaders:**
- Klaviyo: ~46% share
- Mailchimp: ~35% share
- Others: ~19% share (fragmented)

**Market Dynamics:**
- Two dominant players
- Long tail of smaller competitors
- Opportunity in AI-differentiated positioning
- Typical SaaS market consolidation pattern

**Implications for SOM:**
- 5% share requires strong differentiation
- AI capabilities could drive 10-15% share long-term
- Acquisition potential if unable to reach scale

## Investment Thesis Validation

### Market Opportunity Score: ✅ Strong

**Positives:**
✅ Large market: $1.5B+ global TAM
✅ Growing market: 12% CAGR, 25% for AI subset
✅ Addressable: $169M SAM with clear path to customers
✅ Achievable: $8.5M Year 5 ARR reasonable
✅ Validation: Public companies prove market exists

**Risks:**
⚠️ Competition: Klaviyo and Mailchimp are strong
⚠️ Switching costs: Customers invested in current tools
⚠️ Market share: 5% requires excellent execution

**Verdict:** Market opportunity supports venture-scale outcome ($100M+ exit possible)

## Presentation to Investors

### Slide 1: Market Opportunity Summary

```
AI-Powered Email Marketing for E-Commerce

TAM: $1.5B Global, $539M North America
SAM: $169M (AI-ready e-commerce companies)
SOM: $8.5M ARR by Year 5 (5% market share)

Market Growing 25% CAGR (AI subset)
Validated by Klaviyo ($700M revenue)
```

### Slide 2: Bottom-Up Validation

```
Target: 105,000 E-Commerce Companies ($1M+ revenue)

Segment Breakdown:
• Small ($1M-$5M): 85,000 companies × $3,600 ACV
• Mid-Market ($5M-$50M): 18,000 × $9,600
• Enterprise ($50M+): 2,500 × $24,000

Year 5: 888 customers, $8.5M ARR (5% market share)
```

### Slide 3: Market Validation

```
Top-Down: $171M SAM (Gartner + market filters)
Bottom-Up: $169M SAM (<2% variance)

Public Company Validation:
• Klaviyo: $700M revenue (46% market share)
• Mailchimp: $800M revenue (Intuit-owned)

Demonstrates large, proven market
```

## Key Takeaways

**Market Sizing Results:**
- TAM: $1.5B globally, $539M North America
- SAM: $169M (North America, AI-ready customers)
- SOM: $4.2M (Year 3), $8.5M (Year 5)

**Methodology:**
- Bottom-up primary (most granular and credible)
- Top-down validation (<2% variance on SAM)
- Public company validation (Klaviyo, Mailchimp)

**Investment Implications:**
- Market supports venture-scale outcome
- 5% market share achievable with strong execution
- Growing market (25% CAGR) provides tailwinds
- Competitive but differentiated positioning possible

**Next Steps:**
1. Validate pricing assumptions with customer research
2. Refine segment prioritization based on GTM capacity
3. Update SAM annually as market evolves
4. Track Klaviyo/Mailchimp as competitive benchmarks
5. Monitor AI adoption rates in e-commerce segment

This bottom-up market sizing provides a defensible, data-driven foundation for business planning and fundraising.
