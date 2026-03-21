---
title: "Route Researcher"
description: "Research North American mountain peaks and generate comprehensive route beta reports"
category: "research"
source: "community"
author: "Community"
tags: ["route", "researcher"]
date: 2026-03-20
---

# Route Researcher

Research mountain peaks across North America and generate comprehensive route beta reports combining data from multiple sources including PeakBagger, SummitPost, WTA, AllTrails, weather forecasts, avalanche conditions, and trip reports.

**Data Sources:** This skill aggregates information from specialized mountaineering websites (PeakBagger, SummitPost, Washington Trails Association, AllTrails, The Mountaineers, and regional avalanche centers). The quality of the generated report depends on the availability of information on these sources. If your target peak lacks coverage on these websites, the report may contain limited details. The skill works best for well-documented peaks in North America.

## When to Use This Skill

Use this skill when the user requests:

- Research on a specific mountain peak
- Route beta or climbing information
- Trip planning information for peaks
- Current conditions for mountaineering objectives

Examples:

- "Research Mt Baker"
- "I'm planning to climb Sahale Peak next month, can you research the route?"
- "Generate route beta for Forbidden Peak"

## Progress Checklist

Research Progress:

- [ ] Phase 1: Peak Identification (peak validated, ID obtained)
- [ ] Phase 2: Peak Information Retrieval (coordinates and details obtained)
- [ ] Phase 3: Data Gathering (parallel execution)
  - [ ] Phase 3a: Python conditions fetch (weather, air quality, daylight, avalanche, peakbagger)
  - [ ] Phase 3b: Researcher agents (3 in parallel - web sources + trip reports)
  - [ ] Phase 3c: Results aggregated
  - [ ] Phase 3d: Access/permits (inline WebSearch)
- [ ] Phase 4: Route Analysis (synthesize route, crux, hazards)
- [ ] Phase 5: Report Generation (Report Writer agent)
- [ ] Phase 6: Report Review & Validation (Report Reviewer agent)
- [ ] Phase 7: Completion (user notified, next steps provided)

## Orchestration Workflow

### Phase 1: Peak Identification

**Goal:** Identify and validate the specific peak to research.

1. **Extract Peak Name** from user message
   - Look for peak names, mountain names, or climbing objectives
   - Common patterns: "Mt Baker", "Mount Rainier", "Sahale Peak", etc.

2. **Search PeakBagger** using peakbagger-cli:

   ```bash
   uvx --from git+https://github.com/dreamiurg/peakbagger-cli.git@v1.7.0 peakbagger peak search "{peak_name}" --format json
   ```

   - Parse JSON output to extract peak matches
   - Each result includes: peak_id, name, elevation (feet/meters), location, url

3. **Handle Multiple Matches:**
   - If **multiple peaks** found: Use AskUserQuestion to present options
     - For each option, show: peak name, elevation, location, AND PeakBagger URL
     - Format each option description as: "[Peak Name] ([Elevation], [Location]) - [PeakBagger URL]"
     - This allows user to click through and verify the correct peak
     - Let user select the correct peak
     - Provide "Other" option if none match

   - If **single match** found: Confirm with user
     - Present confirmation message with peak details and PeakBagger link
     - Show: "Found: [Peak Name] ([Elevation], [Location])"
     - Include PeakBagger URL in the message so user can verify: "[PeakBagger URL]"
     - Use AskUserQuestion: "Is this the correct peak? You can verify at [PeakBagger URL]"

   - If **no matches** found:
     - Try peak name variations systematically (see "Peak Name Variations" section):
       - **Word order reversal:** "Mountain Pratt" → "Pratt Mountain"
       - **Title variations:** Mt/Mount, St/Saint
       - **Add location:** Include state or range name
       - **Remove titles:** Try just the core name
     - Run multiple searches in parallel with different variations
     - Combine results and present best matches to user
     - If still no results, use AskUserQuestion to ask for:
       - A different peak name variation
       - Direct PeakBagger peak ID or URL
       - General PeakBagger search

4. **Extract Peak ID:**
   - From search results JSON, extract the `peak_id` field
   - Store for use in subsequent peakbagger-cli commands
   - Also store the PeakBagger URL for reference links

### Phase 2: Peak Information Retrieval

**Goal:** Get detailed peak information and coordinates needed for location-based data gathering.

This phase must complete before Phase 3, as coordinates are required for weather, daylight, and avalanche data.

Retrieve detailed peak information using the peak ID from Phase 1:

```bash
uvx --from git+https://github.com/dreamiurg/peakbagger-cli.git@v1.7.0 peakbagger peak show {peak_id} --format json
```

This returns structured JSON with:

- Peak name and alternate names
- Elevation (feet and meters)
- Prominence (feet and meters)
- Isolation (miles and kilometers)
- Coordinates (latitude, longitude in decimal degrees)
- Location (county, state, country)
- Routes (if available): trailhead, distance, vertical gain
- Peak list memberships and rankings
- Standard route description (if available in routes data)

**Error Handling:**

- If peakbagger-cli fails: Fall back to WebSearch/WebFetch and note in "Information Gaps"
- If specific fields missing in JSON: Mark as "Not available" in gaps section
- Rate limiting: Built into peakbagger-cli (default 2 second delay)

**Once coordinates are obtained from this step, immediately proceed to Phase 3.**

### Phase 3: Data Gathering

**Goal:** Gather comprehensive route information from all available sources.

**Execution Strategy:** Run Python script for deterministic API data + dispatch specialized agents in parallel for web research. This hybrid approach minimizes token usage while maximizing parallelism.

#### Step 3A: Fetch Conditions Data (Python Script)

Run the conditions fetcher script to gather all API-based data:

```bash
cd skills/route-researcher/tools
uv run python fetch_conditions.py \
  --coordinates "{latitude},{longitude}" \
  --elevation {elevation_m} \
  --peak-name "{peak_name}" \
  --peak-id {peak_id}
```

This returns JSON with:

- **weather**: 7-day forecast with temperatures, precipitation, freezing levels
- **air_quality**: AQI ratings and any concerns
- **daylight**: Sunrise, sunset, civil twilight
- **avalanche**: NWAC region and URL for manual check
- **peakbagger**: Ascent statistics and recent ascents (if peak_id provided)
- **gaps**: Any API failures noted for report

**Run this in parallel with Step 3B** (no dependency between them).

#### Step 3B: Dispatch Researcher Agents (Parallel)

Dispatch 3 Researcher agents in a single message (all Task calls together). Each agent researches assigned sources and fetches trip report content directly.

**Agent 1: PeakBagger + SummitPost**

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a route researcher gathering mountaineering data for {peak_name}.

## Your Assignment
Research from these sources: PeakBagger, SummitPost

## PeakBagger Research
1. Search: "{peak_name} site:peakbagger.com"
2. Extract route descriptions from peak page
3. Identify trip reports with content (word_count > 0)
4. Fetch content for up to 5 recent trip reports using:
   ```bash
   uvx --from git+https://github.com/dreamiurg/peakbagger-cli.git@v1.7.0 peakbagger ascent show {ascent_id} --format json
   ```

## SummitPost Research

1. Search: "{peak_name} site:summitpost.org"
2. Use WebFetch to extract: route name, difficulty, approach, description, hazards
3. If WebFetch fails, use:

   ```bash
   uv run python {repo_root}/skills/route-researcher/tools/cloudscrape.py "{url}"
   ```

## Trip Report Extraction

For each report fetched, extract: date, author, route conditions, gear mentioned, hazards.

## Output Format (return EXACTLY this JSON)

```json
{
  "sources": ["PeakBagger", "SummitPost"],
  "route_info": [
    {"source": "...", "name": "...", "difficulty": "...", "description": "...", "hazards": [...]}
  ],
  "trip_reports": [
    {"source": "...", "date": "...", "author": "...", "url": "...", "summary": "...", "conditions": "...", "has_gpx": false}
  ],
  "gaps": ["what couldn't be fetched and why"]
}
```"""
)
```

**Agent 2: WTA + Mountaineers**

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a route researcher gathering mountaineering data for {peak_name}.

## Your Assignment
Research from these sources: WTA, Mountaineers.org

## WTA Research
1. Search: "{peak_name} site:wta.org"
2. Find the hike page and extract: trail name, difficulty, distance, elevation gain, hazards
3. Get trip reports from AJAX endpoint: {wta_url}/@@related_tripreport_listing
4. Fetch content for up to 5 recent trip reports using:
   ```bash
   uv run python {repo_root}/skills/route-researcher/tools/cloudscrape.py "{trip_report_url}"
   ```

## Mountaineers Research

1. Search: "{peak_name} site:mountaineers.org route"
2. Extract route beta, technical requirements, hazards

## Fallback

If WebFetch fails for any page, use cloudscrape.py as shown above.

## Output Format (return EXACTLY this JSON)

```json
{
  "sources": ["WTA", "Mountaineers"],
  "route_info": [
    {"source": "...", "name": "...", "difficulty": "...", "description": "...", "hazards": [...]}
  ],
  "trip_reports": [
    {"source": "...", "date": "...", "author": "...", "url": "...", "summary": "...", "conditions": "...", "has_gpx": false}
  ],
  "gaps": ["what couldn't be fetched and why"]
}
```"""
)
```

**Agent 3: AllTrails**

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a route researcher gathering mountaineering data for {peak_name}.

## Your Assignment
Research from AllTrails

## AllTrails Research
1. Search: "{peak_name} site:alltrails.com"
2. Use WebFetch to extract: trail name, difficulty, distance, elevation gain, route type, best season, hazards
3. If WebFetch fails, use:
   ```bash
   uv run python {repo_root}/skills/route-researcher/tools/cloudscrape.py "{url}"
   ```

## Output Format (return EXACTLY this JSON)

```json
{
  "sources": ["AllTrails"],
  "route_info": [
    {"source": "...", "name": "...", "difficulty": "...", "distance_miles": N, "elevation_gain_ft": N, "description": "...", "hazards": [...]}
  ],
  "trip_reports": [],
  "gaps": ["what couldn't be fetched and why"]
}
```"""
)
```

**Execute all 3 agents in parallel by including all Task calls in a single response.**

#### Step 3C: Aggregate Results

After Python script and all agents return, aggregate into unified data structure:

```json
{
  "conditions": { /* from fetch_conditions.py */ },
  "route_data": {
    "sources": [ /* merged from all 3 agents */ ],
    "trip_reports": [ /* merged from all agents */ ]
  },
  "gaps": [ /* merged gaps from all sources */ ]
}
```

**Partial Failure Handling:**

- If any agent fails entirely, proceed with data from successful agents
- Note failed sources in the gaps array
- Minimum viable: conditions data + at least one route source

#### Step 3D: Access and Permits (Inline)

Run WebSearch for access information:

```
WebSearch queries:
1. "{peak_name} trailhead access"
2. "{peak_name} permit requirements"
3. "{peak_name} forest service road conditions"
```

Extract trailhead names, required permits, access notes. Add to route_data.

### Phase 4: Route Analysis

**Goal:** Analyze gathered data to determine route characteristics and synthesize information.

#### Step 4A: Determine Route Type

Based on route descriptions, elevation, and gear mentions, classify as:

- **Glacier:** Crevasses mentioned, glacier travel, typically >8000ft
- **Rock:** Technical climbing, YDS ratings (5.x), protection mentioned
- **Scramble:** Class 2-4, exposed but non-technical
- **Hike:** Class 1-2, trail-based, minimal exposure

#### Step 4B: Synthesize Route Information from Multiple Sources

**Goal:** Combine trip reports and route descriptions from Step 3B researcher agents, plus conditions data from Step 3A, into comprehensive route beta.

**Source Priority:**

1. Trip reports (Step 3B agents) - first-hand experiences
2. Route descriptions (Step 3B agents) - published beta baseline
3. PeakBagger/ascent data (Step 3A Python script) - basic info, patterns

**Synthesis Pattern for Route, Crux, and Hazards:**

1. **Start with baseline** from route descriptions (standard route name, published difficulty)
2. **Enrich with trip report details** (landmarks, specific conditions, actual experiences)
3. **Note conflicts** when trip reports disagree with published info
4. **Highlight consensus** ("Multiple reports mention...")
5. **Include specifics** (elevations, locations, quotes)

**Example (Route Description):**
> "The standard route follows the East Ridge (Class 3). Multiple trip reports mention a well-cairned use trail branching right at 4,800 ft—this is the correct turn. The use trail climbs through talus (described as 'tedious' and 'ankle-rolling'). In early season, this section may be snow-covered, requiring microspikes."

**Apply this pattern to:**

- **Route:** Use baseline structure, add landmarks/navigation from trip reports, include actual times
- **Crux:** Describe location/difficulty, add trip report assessments, note conditions-dependent variations
- **Hazards:** Extract ALL hazards from trip reports (rockfall, exposure, route-finding, seasonal), organize by type, include specific locations and mitigation strategies. Be comprehensive—safety-critical.

**Extract Key Information:**

From all synthesized data, identify:

- **Difficulty Rating:** YDS class, scramble grade, or general difficulty (validated by trip reports)
- **Crux:** Hardest/most technical section of route (synthesized above)
- **Hazards:** All identified hazards (synthesized above)
- **Notable Gear:** Any unusual or important gear mentioned in trip reports or beta (to be included in relevant sections, not as standalone section)
- **Trailhead:** Name and approximate location
- **Distance/Gain:** Round-trip distance and elevation gain (compare published vs actual trip report data)
- **Time Estimates:** Calculate three-tier pacing based on distance and gain:
  - **Fast pace:** Calculate based on 2+ mph and 1000+ ft/hr gain rate
  - **Moderate pace:** Calculate based on 1.5-2 mph and 700-900 ft/hr gain rate
  - **Leisurely pace:** Calculate based on 1-1.5 mph and 500-700 ft/hr gain rate
  - Use the **slower** of distance-based or gain-based calculations for each tier
  - Example: For 4 miles, 2700 ft gain:
    - Fast: max(4mi/2mph, 2700ft/1000ft/hr) = max(2hr, 2.7hr) = ~2.5-3 hours
    - Moderate: max(4mi/1.5mph, 2700ft/800ft/hr) = max(2.7hr, 3.4hr) = ~3-4 hours
    - Leisurely: max(4mi/1mph, 2700ft/600ft/hr) = max(4hr, 4.5hr) = ~4-5 hours
- **Freezing Level Analysis:** Compare peak elevation with forecasted freezing levels:
  - **Include Freezing Level Alert if:** Any day in forecast has freezing level within 2000 ft of peak elevation
  - **Omit if:** Freezing level stays >2000 ft above peak throughout forecast (typical summer conditions)
  - Example: 5,469 ft peak with 5,000-8,000 ft freezing levels → Include alert (marginal conditions)
  - Example: 4,000 ft peak with 10,000+ ft freezing levels → Omit alert (well above summit)

#### Step 4C: Identify Information Gaps

Explicitly document what data was **not found or unreliable:**

- Missing trip reports
- No GPS tracks available
- Script failures (weather, avalanche, daylight)
- Conflicting information between sources
- Limited seasonal data

### Phase 5: Report Generation

**Goal:** Create comprehensive Markdown document by dispatching Report Writer agent.

#### Step 5A: Prepare Data Package

Organize all gathered and analyzed data into structured JSON:

```json
{
  "peak": {
    "name": "{peak_name}",
    "id": {peak_id},
    "elevation_ft": {elevation},
    "coordinates": [{latitude}, {longitude}],
    "location": "{location}",
    "peakbagger_url": "{url}"
  },
  "conditions": {
    // From fetch_conditions.py output
    "weather": {...},
    "air_quality": {...},
    "daylight": {...},
    "avalanche": {...}
  },
  "route_data": {
    // Merged from all Researcher agents
    "sources": [...],
    "trip_reports": [...]
  },
  "analysis": {
    // From Phase 4
    "route_type": "{hike|scramble|technical|glacier}",
    "difficulty": "{rating}",
    "crux": "{description}",
    "hazards": [...],
    "time_estimates": {...},
    "access": {...}
  },
  "gaps": [...]
}
```

#### Step 5B: Dispatch Report Writer Agent

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a Report Writer generating a mountaineering route report.

## Instructions

1. **Read the report template:**
   Use the Read tool to read: {repo_root}/skills/route-researcher/assets/report-template.md

2. **Generate report following template structure exactly:**
   - Header with peak name, elevation, location, date
   - AI disclaimer (prominent safety warning)
   - Overview: route type, difficulty, distance/gain, time estimates
   - Route Description: synthesized from sources, include landmarks
   - Crux: describe hardest section with specifics
   - Known Hazards: comprehensive list
   - Current Conditions: weather forecast, freezing levels, air quality, daylight
   - Trip Reports: links organized by source with dates
   - Information Gaps: explicitly list missing data
   - Data Sources: links to all sources used

3. **Markdown Formatting Rules:**
   - ALWAYS add blank line before lists
   - ALWAYS add blank line after section headers
   - Use `-` for bullets (not `*` or `+`)
   - Use `**text**` for bold emphasis
   - Break paragraphs >4 sentences

4. **Save the report:**
   Use the Write tool to save to: {output_dir}/{date}-{peak-name-slug}.md

## Data Package

{data_package_json}

## Output Format (return EXACTLY this JSON)
```json
{
  "status": "SUCCESS",
  "file_path": "/absolute/path/to/report.md",
  "filename": "YYYY-MM-DD-peak-name.md",
  "sections_generated": N
}
```"""
)
```

#### Step 5C: Capture Report File Path

Extract `file_path` from agent's JSON response for use in Phase 6.

### Phase 6: Report Review & Validation

**Goal:** Validate report quality by dispatching Report Reviewer agent.

#### Step 6A: Dispatch Report Reviewer Agent

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a Report Reviewer validating a mountaineering route report.

## Instructions

1. **Read the report:**
   Use the Read tool to read: {report_file_path}

2. **Perform systematic quality checks:**

   **Factual Consistency:**
   - Dates match their stated day-of-week (e.g., "Thu Nov 6, 2025" is actually Thursday)
   - Coordinates, elevations, distances consistent across all mentions
   - Weather forecasts align logically (freezing levels match precipitation types)

   **Mathematical Accuracy:**
   - Elevation gains add up correctly
   - Time estimates reasonable given distance and elevation gain
   - Unit conversions correct (feet to meters, etc.)

   **Internal Logic:**
   - Hazard warnings align with route descriptions
   - Recommendations match current conditions
   - Crux descriptions match overall difficulty rating

   **Completeness:**
   - No placeholder texts like {{peak_name}} or {{YYYY-MM-DD}}
   - All referenced links actually provided
   - Mandatory sections present: Overview, Route, Current Conditions, Trip Reports, Information Gaps, Data Sources

   **Formatting:**
   - Markdown headers properly structured
   - Lists have blank lines before them
   - Tables properly formatted

   **Safety & Responsibility:**
   - AI disclaimer present and prominent
   - Critical hazards properly emphasized
   - Users directed to verify information from primary sources

3. **Fix issues:**
   - **Critical** (safety errors, factual errors, missing disclaimers): MUST fix using Edit tool
   - **Important** (completeness, consistency): SHOULD fix
   - **Minor** (formatting, polish): FIX if quick

## Output Format (return EXACTLY this JSON)
```json
{
  "status": "PASS" | "PASS_WITH_FIXES" | "FAIL",
  "issues_found": N,
  "fixes_applied": ["description of fix 1", "description of fix 2"],
  "remaining_issues": ["issues that couldn't be fixed"],
  "report_path": "/absolute/path/to/report.md"
}
```"""
)
```

#### Step 6B: Process Validation Results

Handle the reviewer agent's response:

- **PASS or PASS_WITH_FIXES:** Proceed to Phase 7 with the `report_path`
- **FAIL:** Present `remaining_issues` to user and ask for guidance

The Report Reviewer automatically fixes issues and returns the corrected file path.

### Phase 7: Completion

**Goal:** Inform user of completion and next steps.

Report to user:

1. **Success message:** "Route research complete for {Peak Name}"
2. **File location:** Full absolute path to generated report
3. **Summary:** Brief 2-3 sentence overview:
   - Route type and difficulty
   - Key hazards or considerations
   - Any significant information gaps
4. **Next steps:** Encourage user to:
   - Review the report
   - Verify critical information from primary sources
   - Check current conditions before attempting route

**Example completion message:**

```
Route research complete for Mount Baker!

Report saved to: 2025-10-20-mount-baker.md

Summary: Mount Baker via Coleman-Deming route is a moderate glacier climb (Class 3) with significant crevasse hazards. The route involves 5,000+ ft elevation gain and typically requires an alpine start. Weather and avalanche forecasts are included.

Next steps: Review the report and verify current conditions before your climb. Remember that mountain conditions change rapidly - check recent trip reports and weather forecasts immediately before your trip.
```

## Error Handling Principles

Throughout execution, follow these error handling guidelines:

### Script Failures

- **Don't block:** If a Python script fails, note in "Information Gaps" and continue
- **Provide alternatives:** Include manual check links (Mountain-Forecast.com, NWAC.us)
- **One retry:** Retry once on network timeouts, then continue

### Missing Data

- **Be explicit:** Always document what wasn't found
- **Be helpful:** Provide links for manual checking
- **Don't guess:** Never fabricate data to fill gaps

### Search Failures

- **Try variations:** If peak not found, try alternate names (Mt vs Mount)
- **Ask user:** If still not found, ask user for clarification or direct URL
- **Provide guidance:** Suggest how to search PeakBagger manually

### WebFetch/WebSearch Issues

- **Universal fallback pattern:** Always try WebFetch first, then cloudscrape.py if it fails
- **Automatic retry:** If WebFetch fails or returns incomplete data, immediately retry with cloudscrape.py
- **Graceful degradation:** Missing one source shouldn't stop entire research
- **Document gaps:** Note which sources were unavailable (both WebFetch AND cloudscrape.py failed)
- **Prioritize safety:** If critical safety info (avalanche, hazards) unavailable, emphasize in gaps section

## Execution Timeouts

- **Individual Python scripts:** 30 seconds each
- **WebFetch operations:** Use default timeout
- **WebSearch operations:** Use default timeout
- **Total skill execution:** Target 3-5 minutes, acceptable up to 10 minutes for comprehensive research

## Quality Principles

Every generated report must:

1. ✅ **Include safety disclaimer** prominently at top
2. ✅ **Document all information gaps** explicitly
3. ✅ **Cite sources** with links
4. ✅ **Use current date** in filename and metadata
5. ✅ **Follow template structure** exactly
6. ✅ **Provide actionable information** (distances, times, gear)
7. ✅ **Emphasize verification** - this is research, not gospel

## Implementation Notes

### Architecture (as of 2026-01-29)

The route-researcher skill uses a hybrid architecture combining Python scripts and LLM agents:

**Components:**

- **Python script** (`tools/fetch_conditions.py`) - Deterministic API calls for weather, air quality, daylight, avalanche, and PeakBagger data
- **Researcher agents** (3 total) - Web research for route info and trip reports from PeakBagger+SummitPost, WTA+Mountaineers, and AllTrails
- **Report Writer agent** - Generates markdown reports from aggregated data
- **Report Reviewer agent** - Validates report quality before presentation

**Benefits:**

- **Reduced token usage** - Python handles deterministic API calls with zero LLM tokens
- **Parallel execution** - Phase 3 runs Python script + 3 researcher agents simultaneously
- **Inline prompts** - Agent instructions embedded in SKILL.md for reliability
- **Clear contracts** - JSON schemas define agent inputs and outputs

See `docs/architecture.md` for detailed execution flow and data contracts.

### Current Status (as of 2026-01-30)

**Implemented:**

- **peakbagger-cli** integration for peak search, info, and ascent data
- Python tools directory structure
- Report generation in user's current working directory
- **cloudscrape.py** - Universal fallback for WebFetch failures, works with ANY website including:
  - Cloudflare-protected sites (SummitPost, PeakBagger, Mountaineers.org)
  - AllTrails (when WebFetch fails)
  - WTA (when WebFetch fails)
  - Any other site that blocks or limits WebFetch access
- **Two-tier fetching strategy:** WebFetch first, cloudscrape.py as automatic fallback
- **Open-Meteo Weather API** for mountain weather forecasts (temperature, precipitation, freezing level, wind)
- **Open-Meteo Air Quality API** for AQI forecasting (US AQI scale with conditional alerts)
- Multi-source weather gathering (Open-Meteo, NOAA/NWS, NWAC)
- Adaptive ascent data retrieval based on peak popularity
- **Sunrise-Sunset.org API** for daylight calculations (sunrise, sunset, civil twilight, day length)
- **High-quality trip report identification** across PeakBagger and WTA sources
- **WTA AJAX endpoint** for trip report extraction (`{wta_url}/@@related_tripreport_listing`)

**Pending Implementation:**

- `fetch_avalanche.py` - NWAC avalanche data (currently using WebSearch/WebFetch as fallback)
- **Browser automation** for Mountaineers.org and AllTrails trip report extraction (requires Playwright/Chrome)
  - Current: Both sites load content via JavaScript, cloudscrape.py cannot extract
  - Future: Add browser automation as 3rd-tier fallback

**When Python scripts are not yet implemented:**

- Note in "Information Gaps" section
- Provide manual check links
- Continue with available data
- Don't block report generation

### peakbagger-cli Command Reference (v1.7.0)

All commands use `--format json` for structured output. Run via:

```bash
uvx --from git+https://github.com/dreamiurg/peakbagger-cli.git@v1.7.0 peakbagger <command> --format json
```

**Available Commands:**

- `peak search <query>` - Search for peaks by name
- `peak show <peak_id>` - Get detailed peak information (coordinates, elevation, routes)
- `peak stats <peak_id>` - Get ascent statistics and temporal patterns
  - `--within <period>` - Filter by period (e.g., '1y', '5y')
  - `--after <YYYY-MM-DD>` / `--before <YYYY-MM-DD>` - Date filters
- `peak ascents <peak_id>` - List individual ascents with trip report links
  - `--within <period>` - Filter by period (e.g., '1y', '5y')
  - `--with-gpx` - Only ascents with GPS tracks
  - `--with-tr` - Only ascents with trip reports
  - `--limit <n>` - Max ascents to return (default: 100)
- `ascent show <ascent_id>` - Get detailed ascent information

**Note:** For comprehensive command options, run `peakbagger --help` or `peakbagger <command> --help`

### Peak Name Variations

Common variations to try if initial search fails:

- **Word order reversal:** "Mountain Pratt" → "Pratt Mountain", "Peak Sahale" → "Sahale Peak"
- **Title expansion:** "Mt" → "Mount", "St" → "Saint"
- **Add location:** "Baker, WA" or "Baker, North Cascades"
- **Remove title:** "Baker" instead of "Mt Baker"
- **Combine variations:** Try reversed order with title expansion (e.g., "Mountain Pratt" → "Pratt Mount" + "Pratt Mountain")

### Google Maps and USGS Links

#### Summit Coordinates Links

**Google Maps (for summit coordinates):**

```
https://www.google.com/maps/search/?api=1&query={latitude},{longitude}
```

Example: `https://www.google.com/maps/search/?api=1&query=48.7768,-121.8144`

**USGS TopoView (for summit coordinates):**

```
https://ngmdb.usgs.gov/topoview/viewer/#{{latitude}}/{longitude}/15
```

Example: `https://ngmdb.usgs.gov/topoview/viewer/#17/48.7768/-121.8144`

**Note:** Use decimal degree format for coordinates. TopoView uses zoom level in URL (15-17 works well for peaks).

#### Trailhead Google Maps Links

**If coordinates available** (e.g., from Mountaineers.org place information):

```
https://www.google.com/maps/search/?api=1&query={latitude},{longitude}
```

Example: `https://www.google.com/maps/search/?api=1&query=48.5123,-121.0456`

**If only trailhead name available:**

```
https://www.google.com/maps/search/?api=1&query={trailhead_name}+{state}
```

Example: `https://www.google.com/maps/search/?api=1&query=Cascade+Pass+Trailhead+WA`

**Note:** Prefer coordinates when available for more precise location.

---

**Skill Version:** --help | **Last Updated:** 2026-01-30

---

## Example: 2025 10 23 Mount Si

# Mount Si - Route Beta Research (2025-10-23)

> **⚠️ AI-Generated Research Document**
>
> This document was generated by an AI assistant and should be used as a **starting point only**.
>
> **YOU MUST:**
>
> - Verify all critical information from primary sources
> - Use your own judgment and experience to assess conditions and risk
> - Cross-reference with current trip reports and local conditions
> - Understand that conditions change rapidly in the mountains
>
> **This is NOT a substitute for:**
>
> - Proper training and experience
> - Current weather and avalanche forecasts
> - Your own research and route planning
> - Sound mountaineering judgment
>
> The mountains are inherently dangerous. You are responsible for your own safety.

## Overview

Mount Si rises to **4,192 ft (1,278 m)** with 304 ft (93 m) of prominence in the Cascade Range, Washington. The peak is located at 47.506875°N, -121.738965°W ([Google Maps](https://www.google.com/maps/search/?api=1&query=47.506875,-121.738965) | [USGS Topo](https://ngmdb.usgs.gov/topoview/viewer/#17/47.506875/-121.738965)). The standard route is a **hiking/scrambling route** rated **Class 1-2 (main trail), Class 3 (Haystack summit)**.

Mount Si is Washington's most popular hike, attracting over 100,000 hikers annually with its dramatic west face rising 3,500 feet above the Snoqualmie Valley. The 8-mile round-trip trail ascends steadily through old-growth forest at Snag Flat before climbing aggressively to a scenic meadow at 3,900 ft. Experienced scramblers can continue to the true summit via the exposed Haystack, a Class 3 scramble with significant consequences for falls.

**Sources:** [PeakBagger](https://www.peakbagger.com/peak.aspx?pid=2087), [AllTrails](https://www.alltrails.com/trail/us/washington/mount-si-trail), [WTA](https://www.wta.org/go-hiking/hikes/mount-si), [SummitPost](https://www.summitpost.org/mount-si/150709), [Mountaineers](https://www.mountaineers.org/activities/routes-places/mount-si-main-trail)

## Route

### Approach

**Mount Si Trailhead** (47.488°N, -121.723°W)

**Directions:** From I-90, take exit 32 and turn left onto 436th Ave SE. Follow to its end at SE North Bend Way and turn left. In 0.3 miles, turn right onto SE Mt. Si Road and follow 2.4 miles to the large trailhead parking lot on the left. [View on Google Maps](https://www.google.com/maps/search/?api=1&query=Mount+Si+Trailhead+WA)

**Parking:** A Washington State Discover Pass is required and the lot is heavily patrolled. Arrive early on weekends as the lot fills quickly, often by mid-morning. Trailhead Direct provides seasonal bus service from Seattle.

### Route

The Mount Si Trail follows a well-maintained path with switchbacks beginning almost immediately from the trailhead. The route covers approximately **8.0 miles round trip** with **3,532 ft** of elevation gain (per PeakBagger) to **3,150 ft** of gain (per WTA) depending on measurement method.

**Typical completion times:**

- **2-3 hours** (~2-3 mph, 1000+ ft/hr): Experienced hikers, trail runners, solo climbers
- **3-4 hours** (~2 mph, 800 ft/hr): Average fitness, steady pace with brief breaks
- **5-7 hours** (~1-1.5 mph, 500-700 ft/hr): Relaxed pace, groups, taking time for photos

The trail begins with steady switchbacks through dense forest, climbing gently for the first 1.5 miles. At approximately 1.5 miles, the trail flattens through Snag Flat, a remarkable stand of old-growth trees that survived both fire and logging. Beyond Snag Flat, the grade steepens considerably as the trail ascends through younger forest.

At 3.5 miles, the canopy opens for the first views south. A quarter mile later, the trail pitches sharply upward before crossing a dramatic talus slope that bisects the forest, offering expansive views southeast. On clear days, Mount Rainier dominates the horizon. Stone steps cemented into the rock lead up and over the talus, then back into brief forest before branching left to an overlook of the Snoqualmie Valley, Seattle, and the Olympic Mountains.

Most hikers stop at the meadow/lunch area at approximately 3,900 ft, which serves as the standard "summit" for the trail. This is the turnaround point for families and casual hikers.

### Optional: The Haystack (True Summit - 4,192 ft)

The Haystack is the true summit of Mount Si and requires a **Class 3 scramble** not suitable for everyone. From the meadow, continue northeast on a path to a wooden bench marking the start of the scramble route. The path continues north to a rocky northeast-facing gully.

The scramble involves exposed climbing on solid rock with significant consequences for a fall - people have been seriously injured and killed attempting the Haystack. The route requires basic scrambling skills, good route-finding, and comfort with exposure. The rock can be loose in places. When wet or icy, the difficulty and danger increase significantly.

### Crux

The crux is the final scramble to the **Haystack summit** via a **Class 3** northeast-facing gully and rock face. This section involves exposed climbing with uncontrolled fall potential - **serious injury or death is possible if you fall**. The rock can be loose and the route requires careful hand/foot placement and scrambling experience. In wet or icy conditions, the scramble becomes significantly more hazardous and may require **crampons and ice axe** in early season. The exposure is substantial and this section is not recommended for beginners, anyone uncomfortable with heights, or in poor conditions.

### Hazards

- **Slippery conditions:** The boulders and rock sections can be extremely treacherous when wet or icy
- **Weather exposure:** The upper portions of the trail and meadow are exposed to weather, wind, and lightning
- **Haystack scramble:** The optional scramble to the true summit has claimed lives - do not attempt if uncomfortable with exposure or if conditions are wet/icy
- **Wildlife:** Cougar sighting reported September 2025 - keep dogs leashed and be alert
- **Route-finding:** While the main trail is well-maintained and signed, the Haystack scramble requires good route-finding skills
- **Crowds:** Extremely popular trail - expect heavy traffic on weekends and good weather days, which can slow progress

## Current Conditions

### Daylight

For **October 23, 2025**, sunrise is at **7:36 AM** and sunset at **6:05 PM**, providing **10 hours and 29 minutes** of daylight. Civil twilight begins at **7:06 AM**, useful for planning alpine starts.

### Weather Forecast

The forecast shows **persistent rain through the next week** with **heavy precipitation expected Friday-Sunday (Oct 24-26)**. Thursday (Oct 23) remains relatively dry but a major weather system arrives Friday bringing significant rainfall. Friday through Sunday sees **heavy, continuous precipitation** with 22mm, 33mm, and 7mm respectively, totaling over 60mm (2.4 inches) across the three-day period. Temperatures will drop sharply with highs in the low 40s°F Friday and barely above freezing by Sunday (high 34°F). Wind gusts up to 78 mph are forecast Friday. **The weekend weather pattern makes hiking inadvisable** - expect slippery trail conditions, potential for hypothermia, and dangerous scrambling conditions on the Haystack.

**Summary:** Avoid the weekend storm - Thursday offers the last reasonable weather window before extended wet, cold, windy conditions settle in.

| Day | Conditions | Temperature | Precipitation |
|-----|-----------|-------------|---------------|
| Thu Oct 23, 2025 (Today) | ⛅ Partly cloudy, breezy | High: 48°F, Low: 40°F | Trace (14% chance) |
| Fri Oct 24, 2025 | 🌧️❄️ Heavy rain, strong winds | High: 44°F, Low: 27°F | 22.0mm (96% chance) |
| Sat Oct 25, 2025 | 🌧️❄️ Rain/snow mix, windy | High: 40°F, Low: 32°F | 4.0mm (98% chance) |
| Sun Oct 26, 2025 | ❄️ Snow showers, very cold | High: 34°F, Low: 27°F | 33.3mm (89% chance) |
| Mon Oct 27, 2025 | 🌨️ Snow showers | High: 34°F, Low: 27°F | 6.9mm (69% chance) |
| Tue Oct 28, 2025 | 🌧️ Showers | High: 33°F, Low: 28°F | 9.9mm (50% chance) |

**Air Quality:**

Air quality is **good** (AQI <50) during the forecast period.

**Check Current Forecasts:**

- [Mountain-Forecast.com](https://www.mountain-forecast.com/peaks/Mount-Si/forecasts/1278) - Summit-level forecast with multiple elevations
- [Open-Meteo Weather](https://open-meteo.com/en/docs#latitude=47.506875&longitude=-121.738965&elevation=1278&hourly=&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto) - Detailed mountain weather data (source for this report)
- [Open-Meteo Air Quality](https://open-meteo.com/en/docs/air-quality-api#latitude=47.506875&longitude=-121.738965&hourly=&daily=&timezone=auto) - Air quality forecast for this location
- [NOAA Point Forecast](https://forecast.weather.gov/MapClick.php?textField1=47.506875&textField2=-121.738965) - Official NWS forecast and alerts

## Trip Reports

Mount Si has extensive trip report coverage with 3,338 total ascents recorded on PeakBagger, including 181 ascents in the last year, 376 with trip reports, and 134 with GPX tracks. WTA has over 2,815 trip reports available. However, most PeakBagger reports are very brief (typically 2-10 words). For detailed route beta and conditions, WTA and Mountaineers sources provide substantially more information.

### Most Detailed Reports

**Washington Trails Association:**

- **2025-10-07** - [Netherly - Mount Si via Mount Teneriffe Trail](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-10-08.141759527204)
- **2025-09-26** - [ChristinaL - Mount Si](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-27.091903021314)
- **2025-09-24** - [HikerCass - Mount Si](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-24.173643149150)
- **2025-09-20** - [mollywc - Mount Si](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-27.154843755618)
- **2025-09-14** - [TheOFamily - Mount Si (Cougar sighting)](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-14.143957154905)

**PeakBagger:**

- **2025-01-14** - [Emma Meersman](https://www.peakbagger.com/climber/ascent.aspx?aid=2746168) - 📝 52 words, 📍 GPX
- **2025-03-03** - [Wendy Kahn](https://www.peakbagger.com/climber/ascent.aspx?aid=2978055) - 📝 11 words
- **2025-03-14** - [Paul Pottorff](https://www.peakbagger.com/climber/ascent.aspx?aid=2917662) - 📝 9 words

### Recent Reports (Last 1-2 Years)

- **2025-10-07** - [WTA: Netherly](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-10-08.141759527204)
- **2025-09-26** - [WTA: ChristinaL](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-27.091903021314)
- **2025-09-24** - [WTA: HikerCass](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-24.173643149150)
- **2025-09-20** - [WTA: mollywc](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-27.154843755618)
- **2025-09-14** - [WTA: TheOFamily - Cougar sighting](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-14.143957154905)

### Browse All Trip Reports

- [PeakBagger Ascents](https://www.peakbagger.com/climber/PeakAscents.aspx?pid=2087) - Individual climb logs with optional GPX tracks and reports
- [Washington Trails Association](https://www.wta.org/go-hiking/hikes/mount-si) - User-submitted trip reports with photos and conditions (2,815+ reports)
- [Mountaineers.org](https://www.mountaineers.org/activities/routes-places/mount-si-main-trail) - Route information and trip reports
- [AllTrails](https://www.alltrails.com/trail/us/washington/mount-si-trail) - User reviews and recent activity (18,339 reviews)
- [SummitPost](https://www.summitpost.org/mount-si/150709) - Route-specific trip reports and photos

## Access & Permits

### Permits & Regulations

- **Required:** Washington State Discover Pass for trailhead parking
- **Dogs:** Allowed but must be on leash at all times
- **Seasonal Access:** Trail is open year-round but winter conditions can be challenging with snow/ice on upper sections

### Road Conditions

SE Mount Si Road is paved and maintained year-round. No seasonal closures. The large parking lot accommodates many vehicles but fills completely on warm weekends - arrive before 9 AM for guaranteed parking, or use Trailhead Direct bus service.

**Trailhead Direct:** Seasonal weekend bus service from Seattle (16th Ave E & E Denny Way) to Mount Si, Mount Teneriffe, and Little Si trailheads. Check [trailheaddirect.org](https://trailheaddirect.org/mount-si/) for current schedules.

## Information Gaps

- **Limited detailed PeakBagger reports:** Most PeakBagger trip reports are very brief (average <10 words). WTA and Mountaineers sources strongly recommended for comprehensive route beta and conditions.
- **AllTrails access blocked:** AllTrails page returned 403 error and cloudscrape.py fallback was not successful.
- **Mountaineers trip reports:** Mountaineers.org page found but detailed trip report extraction not attempted in this research cycle.
- **Seasonal data:** While year-round trip reports are available, winter-specific conditions and beta are limited in this summary. Check recent WTA reports for snow levels and trail conditions.

## Data Sources

- PeakBagger: https://www.peakbagger.com/peak.aspx?pid=2087
- Washington Trails Association: https://www.wta.org/go-hiking/hikes/mount-si
- SummitPost: https://www.summitpost.org/mount-si/150709
- Mountaineers: https://www.mountaineers.org/activities/routes-places/mount-si-main-trail
- Open-Meteo Weather API: https://open-meteo.com
- Open-Meteo Air Quality API: https://air-quality-api.open-meteo.com
- NOAA/NWS: https://forecast.weather.gov
- Sunrise-Sunset.org API: https://sunrise-sunset.org

---

*Research completed 2025-10-23 using [route-researcher v3.0.0](https://github.com/dreamiurg/claude-mountaineering-skills/tree/main/skills/route-researcher) from the [Claude Mountaineering Skills](https://github.com/dreamiurg/claude-mountaineering-skills) repository.*

---

## Example: 2025 11 06 Mount Adams

# Mount Adams - Route Beta Research

> **⚠️ AI-Generated Research Document**
>
> This document was generated by an AI assistant and should be used as a **starting point only**.
>
> **YOU MUST:**
>
> - Verify all critical information from primary sources
> - Use your own judgment and experience to assess conditions and risk
> - Cross-reference with current trip reports and local conditions
> - Understand that conditions change rapidly in the mountains
>
> **This is NOT a substitute for:**
>
> - Proper training and experience
> - Current weather and avalanche forecasts
> - Your own research and route planning
> - Sound mountaineering judgment
>
> The mountains are inherently dangerous. You are responsible for your own safety.

**Generated:** 2025-11-06
**Route Type:** Glacier/Snow Climb
**Difficulty:** Class 3 snow climb, non-technical but glaciated

## Summit Information

- **Elevation:** 12,280 ft (3,743 m)
- **Prominence:** 8,135 ft (2,480 m)
- **Isolation:** 45.75 miles (73.63 km)
- **Location:** Yakima County, Washington, Cascade Range
- **Coordinates:** 46.202494, -121.490746 ([Google Maps](https://www.google.com/maps/search/?api=1&query=46.202494,-121.490746) | [USGS Topo](https://ngmdb.usgs.gov/topoview/viewer/#17/46.202494/-121.490746))
- **PeakBagger:** [Mount Adams](https://www.peakbagger.com/peak.aspx?pid=2365)

## Route Description

### Approach

**Trailhead:** Cold Springs Campground (5,560 ft elevation)

**Access:** From Trout Lake, WA, take Mt Adams Road north to Forest Road 23. Stay right at the V intersection and continue approximately one mile to Forest Road 80 (signed "South Climb"). Turn left onto FR 80 and follow to its end at FR 8040/8031 intersection. Turn right onto FR 8040 and continue north past Morrison Creek Campground to the South Climb Trailhead in the old Cold Springs Camp area.

**Road Conditions:** The road requires good clearance and All Wheel Drive year-round, with Four Wheel Drive recommended. The road is steep and narrow with sharp switchbacks. No RVs or trailers. Roads within Gifford Pinchot National Forest are subject to seasonal closure in winter months.

**Directions:** [View on Google Maps](https://www.google.com/maps/search/?api=1&query=Cold+Springs+Campground+WA)

### Standard Route: South Climb (South Spur)

Mount Adams' South Climb is the most popular and easiest route to the summit. Despite being non-technical, this is a serious mountaineering objective with significant elevation gain and exposure to weather.

The route begins on the South Climb Trail (#183) from Cold Springs, traversing through a 2012 burn zone before crossing Morrison Creek (reliable water source). The trail climbs rocky terrain and switchbacks up through talus fields and lava formations, gaining approximately 2,000 feet before reaching the ridgeline around 7,400 ft.

From the ridgeline, the route becomes fully exposed to weather and winds. Snow coverage typically begins around 8,000 ft. Most climbers camp at the Lunch Counter (9,400 ft), a popular high camp with established tent platforms. Water is available below Lunch Counter and at Morrison Creek.

From Lunch Counter, climbers ascend the main south snowfield or Suksdorf Ridge (western option) toward Pikers Peak (11,657 ft) - a prominent false summit. The snowfield maintains a moderate but consistent gradient. In summer, well-established boot pack makes route-finding straightforward. Winter and early season conditions require more navigation skills.

After cresting Pikers Peak, a flat traverse crosses to the final summit push - a steep section of dirt, sand, and loose rock switchbacks reminiscent of Mount St. Helens. The true summit lies approximately 0.5 miles beyond Pikers Peak.

**Key Details:**

- **Distance:** 12-14 miles round trip (sources vary slightly)
- **Elevation Gain:** 6,600-6,700 ft
- **Estimated Time:**
  - Fast pace (2+ mph, 1000+ ft/hr): 7-9 hours car-to-car
  - Moderate pace (1.5-2 mph, 700-900 ft/hr): 10-12 hours car-to-car
  - Leisurely pace / 2-day trip: Most climbers take 2 days with overnight at Lunch Counter

### Crux

The crux varies by season and conditions. In summer/fall after snow has melted, the final summit push from Pikers Peak involves 600+ ft of steep, loose dirt and sand switchbacks. The terrain is tedious and physically demanding but not technical - similar to scree climbing on other Cascade volcanoes.

In winter and early season with full snow coverage, the steeper sections of the south snowfield (particularly approaching Pikers Peak) become the crux. While the angle rarely exceeds 35-40 degrees, icy conditions above 11,000 ft demand crampons and competent ice axe technique. The exposure increases near Pikers Peak, and a fall could result in a long slide.

Route-finding can be challenging in whiteout conditions, darkness, or when the boot pack is obscured. GPS navigation skills are valuable for these conditions.

### Hazards & Safety

**Known Hazards:**

- **Weather Exposure:** Above 7,400 ft, the route is fully exposed to high winds and rapidly changing weather. Multiple reports mention brutal winds near the summit. Climbers must be prepared for overnight stays in adverse conditions.

- **False Summit (Pikers Peak):** Psychologically and physically demanding. After hours of climbing, reaching what appears to be the summit only to face another 0.5+ miles of elevation gain has turned back many climbers.

- **Icy Conditions:** Above 11,000 ft, snow and ice can be firm to icy, especially in morning hours and late season. Microspikes are marginal in these conditions; crampons strongly recommended.

- **Rock Hazards:** The final dirt/rock scramble has loose rock. Helmets are advised. One recent trip report mentioned being struck by a sliding rock, narrowly avoiding a concussion.

- **Route-Finding:** In darkness, whiteout, or late season when snow has patchy coverage, route-finding becomes more challenging. Some sections have cairns, but these can be unreliable.

- **Crevasses:** While the South Climb is considered the least glaciated route, the mountain has active glaciers and climbers should be aware of crevasse hazards, particularly if deviating from the standard route.

- **Altitude:** At 12,280 ft, altitude sickness is possible, especially for climbers coming from sea level.

- **Crowding:** In peak season (June-August), the Lunch Counter can have 30+ tents, and the trail sees heavy traffic. This increases rockfall hazard from climbers above.

**Required Gear:**

- Ice axe and crampons (essential for snow sections)
- Helmet (recommended for rock hazard)
- Microspikes (marginal - crampons preferred)
- Trekking poles
- Ten Essentials plus overnight gear if camping
- GPS device or map/compass for navigation

**Emergency Contacts:**

- Gifford Pinchot National Forest, Mount Adams Ranger Station, Trout Lake: Check for current contact information

## Current Conditions

### Daylight

- **Date:** 2025-11-06
- **Sunrise:** 6:53 AM PST
- **Sunset:** 4:45 PM PST
- **Daylight Hours:** 9 hours, 52 minutes
- **Civil Twilight:** 6:23 AM - 5:15 PM (optimal window for alpine starts and activities)

**Considerations:** With under 10 hours of daylight in early November, alpine starts are critical for summit attempts. Most climbers aim to start from Lunch Counter at 3-4 AM to ensure summit and descent in daylight.

### Weather Forecast

**7-Day Forecast** (November 6-12, 2025):

**Current Storm (Thu-Fri, Nov 6-7):**

- Heavy snow and precipitation
- Freezing levels: 1,190-1,600 ft (well below summit)
- Wind gusts: 55-63 km/h
- Precipitation: 91.5mm (Thu), 17.2mm (Fri)
- Visibility severely limited

**Improving Conditions (Sat-Sun, Nov 8-9):**

- Clearing skies with partly cloudy conditions
- Freezing levels rising: 3,560-4,070 ft
- Much calmer winds (11-25 km/h gusts)
- Excellent weather window for climbing

**Variable Conditions (Mon-Wed, Nov 10-12):**

- Partly cloudy with increasing precip probability
- Freezing levels: 3,150-3,710 ft
- Light winds (7-15 km/h gusts)

**Key Takeaways:**

- **Immediate conditions:** Not suitable for climbing due to heavy snow and wind
- **Weekend window:** Saturday-Sunday (Nov 8-9) offer the best conditions with clearing weather
- **Freezing level alert:** All forecast days show freezing levels well below the summit elevation of 12,280 ft. Expect full winter conditions with snow, ice, and challenging climbing

**Air Quality:** Excellent throughout forecast period (US AQI 27-39). No concerns for outdoor activities.

**Check Current Forecasts:**

- [Open-Meteo Weather](https://open-meteo.com/en/docs#latitude=46.202494&longitude=-121.490746&elevation=3743&hourly=&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto)
- [Open-Meteo Air Quality](https://open-meteo.com/en/docs/air-quality-api#latitude=46.202494&longitude=-121.490746&hourly=&daily=&timezone=auto)
- [NOAA Point Forecast](https://forecast.weather.gov/MapClick.php?textField1=46.202494&textField2=-121.490746)
- [NWAC Mountain Weather](https://nwac.us/mountain-weather-forecast/)

### Avalanche Forecast

**Current Season:** This is avalanche season (November). Mount Adams has significant avalanche terrain.

**Note:** Avalanche forecast data not available via automated script. Given the current storm and winter conditions, avalanche hazard is likely considerable to high.

**Check Current Conditions:**

- [Northwest Avalanche Center (NWAC)](https://nwac.us) - Check the Mt Adams East zone
- The forecast area covers Mount Adams and surrounding terrain

## Recent Trip Reports & Ascent Statistics

### Ascent Patterns

Mount Adams sees very high traffic with 2,981 viewable ascents on PeakBagger (3,307 total ascents recorded). The mountain is most popular during summer months:

**Peak Season:**

- July: 1,014 ascents
- June: 699 ascents
- August: 505 ascents

**Shoulder Season:**

- May: 188 ascents
- September: 171 ascents

**Winter/Spring:**

- Very limited winter traffic (4-16 ascents per month Nov-Mar)

**Recent Activity (last 12 months):** 171 ascents

### Recent Trip Reports

**Recent Detailed Reports (Summer/Fall 2025):**

- **2025-09-27** - [Paul Pottorff](https://www.peakbagger.com/climber/ascent.aspx?aid=3000345) - Late season ascent. Water plentiful up to Pikers Peak. Microspikes on approach shoes caused toe issues on steep rock descent. Emphasized helmet importance after rock slide incident. Encountered unprepared climbers on Crescent Glacier. Recommended calling Trout Lake Forest Service office before trip for conditions.

- **2025-08-31** - [Abraham Guz](https://www.peakbagger.com/climber/ascent.aspx?aid=2967425) - Alpine start from Lunch Counter (3 AM). Mixed rock and snow route. Fairly icy conditions - some with microspikes wished they had crampons. Route-finding tricky in dark but straightforward (just go up). Summit winds very strong and gusty. Summit to Lunch Counter: 2 hours.

- **2025-08-05** - [Ben Caseley](https://www.peakbagger.com/climber/ascent.aspx?aid=2932434) - Late afternoon start to Lunch Counter, late summit start next day (8:30 AM). Glissade chute from Pikers melting out and becoming too fast with little room to brake before rocks. One climber had to climb back up 20 ft to retrieve dropped axe. Lower chute under Pikers "awesome" for glissading. Microspikes and ice axe necessary.

- **2025-07-26** - [Cam Smith](https://www.peakbagger.com/climber/ascent.aspx?aid=2918617) - Started 3 AM from Cold Springs. Strong winds above 7,400 ft requiring layers the entire time. Snow from 8,000 ft, crampons on. Lunch Counter had ~30 tents. Summit area mostly snow-free except buried Sulfur Cabin. Excellent glissade down Pikers Peak. 13 hours 40 minutes at slow pace, car-to-car.

- **2025-07-19** - [Anisa Daher](https://www.peakbagger.com/climber/ascent.aspx?aid=2909281) - Trail runner approach, boot swap at snow field after main switchback. Boot pack to false summit semi-easy to find. Flat traverse to dirt switchbacks for summit push. Similar to St. Helens with soft steep dirt/sand. Could not find summit registration. 30-min summit break. Glissaded false summit to Lunch Counter (watch for 20' exposed rock section). Ice axe advised for glissading. 11 hours 44 minutes car-to-car.

### Browse Additional Reports

- **PeakBagger:** [Mount Adams Climber's Log](https://www.peakbagger.com/climber/climber.aspx?pid=2365) - 651 trip reports available
- **Washington Trails Association:** [Mount Adams South Climb Trip Reports](https://www.wta.org/go-hiking/hikes/mount-adams-south-climb)
- **SummitPost:** [Mount Adams Trip Reports](https://www.summitpost.org/mount-adams/trip-reports/150198)
- **AllTrails:** [Mount Adams South Climb Reviews](https://www.alltrails.com/trail/us/washington/mount-adams-south-climb-trail) - 2,430 reviews

**Note:** 138 ascents have GPS tracks available on PeakBagger for route verification.

## Access & Permits

### Trailhead

**Cold Springs Campground / South Climb Trailhead** (5,560 ft)

- Two main parking areas at the trailhead
- Can fill up quickly during summer season
- Restrooms available
- No potable water at trailhead
- Picnic tables available

### Permits & Regulations

**Mt. Adams Climbing Activity Pass** (REQUIRED)

- Required if climbing above 7,000 ft elevation between May 1 and September 30
- Cost: $20 per person (16 years and older) for single climbing trip
- Free for children under 16
- **Purchase online:** [Recreation.gov](https://www.recreation.gov/activitypass/4280e9ae-d010-11ea-8e82-82c0c22bed90)

**Important Permit Details:**

- Party leader must enter names for each person 16+ years old
- Must enter license plate for each vehicle at trailhead
- Must carry permit on your person AND display in vehicle windshield
- Print two copies or have one on phone and one in vehicle

**Additional Passes:**

- Northwest Forest Pass or Sno-Park Permit required for parking at trailhead
- Purchase at ranger station or online

**Off-Season (Oct 1 - Apr 30):**

- Climbing permit not required if staying below 7,000 ft OR climbing outside permit season
- Still need Northwest Forest Pass for parking
- Free wilderness permit (self-issue at trailhead) required

**Human Waste:**

- **REQUIRED:** Pack out all human waste in WAG bags (carry-out bags)
- Free WAG bags available 24/7 at Mount Adams Ranger Station front porch (self-serve box)

**Yakama Nation Lands:**

- Access from Bird Creek Meadows requires Yakama Indian Reservation Tract-D tribal-use permit
- Non-members restricted to July 1 - October 1 climbing season

**Register at Ranger Station:**

- Mount Adams Ranger Station, Trout Lake, WA
- Highly recommended to call before trip for current conditions
- Staff (including Melody, frequently mentioned in trip reports) provide valuable beta

### Road Conditions

**Current Access (as of summer/fall 2025):**

- Road to South Climb Trailhead free of snow and fully accessible during summer
- Requires good clearance and AWD/4WD year-round
- Steep, narrow, sharp switchbacks
- Heavy traffic in high season - drive with caution
- NO RVs or trailers

**Seasonal:**

- Roads typically clear May-September
- Expect snow closures approximately October-April
- Check current conditions with Gifford Pinchot National Forest: [Road Conditions](https://www.fs.usda.gov/r06/giffordpinchot/recreation/trailhead-south-climb)

## Information Gaps

- **WebSearch tool unavailable:** One search query ("Mount Adams route description climbing") failed due to tool availability issues. However, sufficient data was obtained from other sources.
- **Avalanche forecast:** Automated avalanche data script not yet implemented. Manual checking of NWAC.us required for current avalanche conditions.
- **WTA trip report extraction:** Did not attempt to extract individual trip reports from WTA due to time constraints. WTA browse link provided for manual checking.
- **Mountaineers.org trip report extraction:** Browsing link provided but individual reports not extracted.
- **AllTrails trip report extraction:** AllTrails loads reviews via JavaScript; automated extraction not possible. Browse link provided.
- **SummitPost page:** Fetched HTML successfully but detailed parsing not completed due to time constraints.

## Data Sources

- **PeakBagger:** [Mount Adams](https://www.peakbagger.com/peak.aspx?pid=2365)
- **PeakBagger CLI:** Peak data, ascent statistics, and trip reports (v1.7.0)
- **Washington Trails Association:** [Mount Adams South Climb](https://www.wta.org/go-hiking/hikes/mount-adams-south-climb)
- **The Mountaineers:** [Mount Adams/South Spur](https://www.mountaineers.org/activities/routes-places/mount-adams-south-spur)
- **AllTrails:** [Mount Adams South Climb Trail](https://www.alltrails.com/trail/us/washington/mount-adams-south-climb-trail)
- **SummitPost:** [Mount Adams](https://www.summitpost.org/mount-adams/150198)
- **Open-Meteo Weather API:** Mountain weather forecasts
- **Open-Meteo Air Quality API:** Air quality forecasts
- **Sunrise-Sunset.org API:** Daylight calculations
- **NOAA/National Weather Service:** Supplemental weather data
- **Recreation.gov:** Permit information
- **US Forest Service:** [Gifford Pinchot National Forest - Mt. Adams](https://www.fs.usda.gov/r06/giffordpinchot/recreation/trailhead-south-climb)

---

**Research completed:** 2025-11-06
**Skill:** route-researcher (mountaineering-skills plugin)

---

## Example: 2025 11 06 Wolf Peak

# Wolf Peak - Route Beta Research (2025-11-06)

> **⚠️ AI-Generated Research Document**
>
> This document was generated by an AI assistant and should be used as a **starting point only**.
>
> **YOU MUST:**
>
> - Verify all critical information from primary sources
> - Use your own judgment and experience to assess conditions and risk
> - Cross-reference with current trip reports and local conditions
> - Understand that conditions change rapidly in the mountains
>
> **This is NOT a substitute for:**
>
> - Proper training and experience
> - Current weather and avalanche forecasts
> - Your own research and route planning
> - Sound mountaineering judgment
>
> The mountains are inherently dangerous. You are responsible for your own safety.

## Overview

Wolf Peak rises to **5,813 ft (1,772 m)** with 257 ft (78 m) of prominence in the Snohomish County, Washington Cascades. The peak is located at 48.016465°N, -121.513745°W ([Google Maps](https://www.google.com/maps/search/?api=1&query=48.016465,-121.513745) | [USGS Topo](https://ngmdb.usgs.gov/topoview/viewer/#17/48.016465/-121.513745)). The standard route is a **scramble** rated **Class 2-3 with an exposed Class 3-4 summit block**.

Wolf Peak is a challenging scramble situated between Vesper Peak and Sperry Peak in the North Cascades. The route follows well-traveled trail to Headlee Pass and Vesper Lake, then transitions to off-trail scrambling across granite slabs and boulders to reach the ridge between Wolf and Sperry. The final summit block features highly exposed, technical moves that require solid scrambling skills and comfort with significant exposure.

**Sources:** [PeakBagger](https://www.peakbagger.com/peak.aspx?pid=52059), [Mountaineers](https://www.mountaineers.org/activities/routes-places/vesper-sperry-wolf-peaks), [WTA](https://www.wta.org/go-hiking/hikes/vesper-peak)

## Route

### Approach

**Sunrise Mine Trailhead** (2,350 ft) - Snohomish County, Washington

**Directions:** From Granite Falls, drive the Mountain Loop Highway approximately 28 miles east, then turn right onto Sunrise Mine Road (Forest Road 4065) for 2.3 miles to its end at the Sunrise Mine Trailhead. [View on Google Maps](https://www.google.com/maps/search/?api=1&query=Sunrise+Mine+Trailhead+WA)

### Access & Permits

#### Permits & Regulations

A **Northwest Forest Pass** is required for parking at the Sunrise Mine Trailhead. No wilderness permit is required for day use.

#### Road Conditions

Mountain Loop Highway is typically open from late May through October, depending on snow levels. Sunrise Mine Road (FR 4065) can have potholes and rough sections but is generally passable by all vehicles in summer. Check current road conditions before your trip.

### Route Description

The route covers approximately **8 miles round trip** with **3,600 ft** of elevation gain.

**Typical completion times:**

- **2.5-3.5 hours** (~2+ mph, 1000+ ft/hr): Experienced scramblers, strong fitness
- **4-5 hours** (~1.5-2 mph, 700-900 ft/hr): Average fitness, steady pace with breaks
- **5-7 hours** (~1-1.5 mph, 500-700 ft/hr): Relaxed pace, groups, navigation challenges

From the Sunrise Mine Trailhead, follow the well-maintained trail 2.7 miles to Headlee Pass at 4,720 ft. The trail continues around the south flanks of Sperry Peak, descending slightly to reach Vesper Lake basin (approximately 4,950 ft) nestled between Sperry and Vesper Peaks.

From Vesper Lake, the route becomes off-trail. Multiple approaches exist to reach the Wolf-Sperry saddle:

**Approach Option 1** (most common): From the northwest corner of the lake, scramble up approximately 400 ft across granite slabs and boulders trending left (west) to gain a small saddle between Vesper Peak and Wolf Peak. From this saddle, traverse climber's right (north) along the ridge toward Wolf Peak's summit.

**Approach Option 2**: Go around the north side of the lake and scramble up slabby rock to reach the saddle between Wolf and Sperry directly.

The scrambling terrain is primarily **Class 2** walking on large granite slabs and boulders with some **Class 3** sections requiring basic hand and footwork. The rock is generally solid when dry but can be slippery when wet. Route-finding is straightforward in good visibility but GPS is highly recommended in fog.

As you near the summit, the terrain becomes more exposed. The final summit block requires careful assessment and presents the technical crux of the route.

### Crux

The crux is located at the final summit block and consists of an extremely exposed traverse followed by a technical move to reach the true summit. Climbers must cross a narrow, off-camber ledge approximately **4 feet wide with ~1,000 ft drop-offs on both sides**. This leads to a crack or gap between large summit boulders. The final move to tag the true summit is **Class 3-4** with severe exposure and fatal-fall consequences.

Multiple trip reports describe this section as "incredibly exposed," with one noting "hundreds if not thousands of feet of vertical drop on either side." The moves themselves are technically moderate when dry, but the psychological challenge is significant due to the exposure. Trip reports indicate parties frequently skip the final summit block or bring a rope for protection on this section.

### Hazards

**Route-finding in poor visibility:** The upper scramble section requires good visibility. Multiple trip reports mention GPS being essential in fog conditions. Cairns exist but can be difficult to follow in whiteout conditions.

**Exposure and rockfall:** The summit block features extreme exposure with fatal-fall potential. Loose blocks exist between the true and false summits. A helmet is recommended due to rockfall danger from parties above.

**Slippery conditions:** Granite slabs become significantly more hazardous when wet or icy. Early season conditions may require crampons and ice axe if snow-filled gullies are present.

**River crossing:** The approach involves a creek crossing that can be challenging during high water. In late fall and early spring, water levels may be significantly elevated, requiring careful navigation upstream to find safe crossing points.

**Weather exposure:** The upper basin and ridge sections are fully exposed to weather. Winter conditions arrive early (October-November) with knee to waist-deep snow accumulation above the lake requiring snowshoes, poles, and winter travel experience.

## Current Conditions

### Daylight

For **November 6, 2025**, sunrise is at **6:58 AM PST** and sunset at **4:41 PM PST**, providing **9 hours and 43 minutes** of daylight. Civil twilight begins at **6:26 AM PST**, useful for planning alpine starts.

### Weather Forecast

**⚠️ Active winter storm pattern in progress.** Today (Thursday, Nov 6) features heavy rain/snow mix with 100% precipitation probability and 33.8mm accumulation. Freezing levels hover near 1,700-2,200 ft, putting the summit in snow conditions. Friday continues with snow and temperatures dropping to single digits Fahrenheit. **Saturday-Sunday offer the best weather window** with mostly clear to partly cloudy skies, though temperatures remain cold (highs near 32-40°F). Monday brings rain back with moderate precipitation (68% chance). Overall, early week features **active winter conditions unsuitable for climbing**, while the weekend provides a brief clearing before the next system arrives Tuesday-Wednesday.

**Summary:** Best weather window is Saturday-Sunday (Nov 8-9) with clear conditions, but expect full winter conditions requiring appropriate gear.

**🏔️ Freezing Level Alert (Peak: 5,813 ft):**

- Thu-Fri (Nov 6-7): 1,080-3,920 ft (BELOW summit - expect snow and icing)
- Sat-Sun (Nov 8-9): 920-3,750 ft (BELOW to near summit - expect frozen/icy conditions)
- Mon-Wed (Nov 10-12): 1,600-2,980 ft (BELOW summit - expect snow and winter conditions)

| Day | Conditions | Temperature | Precipitation |
|-----|-----------|-------------|---------------|
| Thu Nov 6, 2025 (Today) | 🌧️❄️ Rain/Snow mix | High: 33°F, Low: 27°F | 33.8mm (100% chance) |
| Fri Nov 7, 2025 | ❄️ Snow | High: 26°F, Low: 24°F | 8.2mm (60% chance) |
| Sat Nov 8, 2025 | ☀️ Mostly clear | High: 33°F, Low: 22°F | None (14% chance) |
| Sun Nov 9, 2025 | ⛅ Partly cloudy | High: 39°F, Low: 24°F | None (34% chance) |
| Mon Nov 10, 2025 | 🌧️ Rain | High: 36°F, Low: 33°F | 10.9mm (68% chance) |
| Tue Nov 11, 2025 | ⛅ Partly cloudy | High: 35°F, Low: 30°F | 0.5mm (56% chance) |
| Wed Nov 12, 2025 | 🌧️ Rain | High: 42°F, Low: 28°F | Trace (72% chance) |

**Air Quality:**

Air quality is **good** (AQI <50) during the forecast period.

**Check Current Forecasts:**

- [Mountain-Forecast.com](https://www.mountain-forecast.com/peaks/Wolf-Peak-Washington/forecasts/1772) - Summit-level forecast with multiple elevations
- [Open-Meteo Weather](https://open-meteo.com/en/docs#latitude=48.016465&longitude=-121.513745&elevation=1772&hourly=&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto) - Detailed mountain weather data (source for this report)
- [Open-Meteo Air Quality](https://open-meteo.com/en/docs/air-quality-api#latitude=48.016465&longitude=-121.513745&hourly=&daily=&timezone=auto) - Air quality forecast for this location
- [NOAA Point Forecast](https://forecast.weather.gov/MapClick.php?textField1=48.016465&textField2=-121.513745) - Official NWS forecast and alerts
- [NWAC Mountain Weather](https://nwac.us/mountain-weather-forecast/) - Mountain weather forecast for Cascades

### Avalanche Forecast

**Avalanche forecast not available.** The peak is at moderate elevation (5,813 ft) but does feature steep terrain above Vesper Lake. During winter months (November-April), check [NWAC.us](https://nwac.us) for current avalanche conditions in the Central Cascades zone.

## Trip Reports

Wolf Peak has 97 recorded ascents on PeakBagger with 15 in the last year (mostly July-September). Trip reports are available from PeakBagger (4 recent reports with text) and WTA (483 total reports for Vesper Peak area). PeakBagger reports average brief (19-200 words) but provide specific crux details. WTA reports are significantly more detailed with comprehensive conditions and route-finding information.

### Most Detailed Reports

**PeakBagger:**

- **2025-09-25** - [Dmytro Gaivoronsky](https://www.peakbagger.com/climber/ascent.aspx?aid=2996186) - 📝 200 words, 📍 GPX
- **2025-08-31** - [Zachary Richardson](https://www.peakbagger.com/climber/ascent.aspx?aid=2966508) - 📝 19 words, 📍 GPX
- **2025-08-18** - [Ricky Han](https://www.peakbagger.com/climber/ascent.aspx?aid=2951146) - 📝 31 words, 📍 GPX
- **2025-08-08** - [Nick 🏞️](https://www.peakbagger.com/climber/ascent.aspx?aid=2934575) - 📝 28 words

**Washington Trails Association:**

- **2025-11-02** - [gobozov - Vesper Peak trip (winter conditions)](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-11-02.222647712135)
- **2025-10-21** - [Veronica84 - Vesper Peak trip (snow conditions)](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-10-21.161641757167)
- **2024-08-13** - [Wolf Peak traverse in fog](https://www.wta.org/go-hiking/trip-reports/trip_report-2024-08-13.114053402236)
- **2022-09-25** - [Vesper, Sperry & Wolf Peaks traverse](https://www.wta.org/go-hiking/trip-reports/trip_report.2022-09-25.0747962189)

### Browse All Trip Reports

- [PeakBagger Ascents](https://www.peakbagger.com/climber/PeakAscents.aspx?pid=52059) - Individual climb logs with optional GPX tracks and reports
- [Washington Trails Association](https://www.wta.org/go-hiking/hikes/vesper-peak) - User-submitted trip reports with photos and conditions
- [Mountaineers.org](https://www.mountaineers.org/activities/routes-places/vesper-sperry-wolf-peaks) - Route information and trip reports

## Information Gaps

- **Limited detailed PeakBagger trip reports:** Most PeakBagger reports are brief (19-200 words average). WTA sources provide more comprehensive route beta and conditions information.
- **SummitPost access blocked:** WebFetch returned 403 error. Cloudscrape.py fallback successfully retrieved page content but full parsing not completed.
- **Avalanche forecast script:** Not yet implemented. Manual check of NWAC.us required for winter travel.
- **AllTrails coverage:** No specific Wolf Peak trail found on AllTrails. The peak is accessed via Vesper Peak approach trail.
- **GPS tracks limited:** Only 16 of 97 ascents on PeakBagger have GPS tracks. 4 GPX tracks available from the last year.

## Data Sources

- PeakBagger: https://www.peakbagger.com/peak.aspx?pid=52059
- Mountaineers.org: https://www.mountaineers.org/activities/routes-places/vesper-sperry-wolf-peaks
- Washington Trails Association: https://www.wta.org/go-hiking/hikes/vesper-peak
- SummitPost: https://www.summitpost.org/wolf-peak/971797
- Open-Meteo Weather API
- Open-Meteo Air Quality API
- Sunrise-Sunset.org API

---

*Research completed 2025-11-06 using [route-researcher v1.0.0](https://github.com/dreamiurg/claude-mountaineering-skills/tree/main/skills/route-researcher) from the [Claude Mountaineering Skills](https://github.com/dreamiurg/claude-mountaineering-skills) repository.*

---

## Example: 2026 01 29 Mount Shuksan

# Mount Shuksan - Route Beta Research (2026-01-29)

> **AI-Generated Research Document**
>
> This document was generated by an AI assistant and should be used as a **starting point only**.
>
> **YOU MUST:**
>
> - Verify all critical information from primary sources
> - Use your own judgment and experience to assess conditions and risk
> - Cross-reference with current trip reports and local conditions
> - Understand that conditions change rapidly in the mountains
>
> **This is NOT a substitute for:**
>
> - Proper training and experience
> - Current weather and avalanche forecasts
> - Your own research and route planning
> - Sound mountaineering judgment
>
> The mountains are inherently dangerous. You are responsible for your own safety.

## Overview

Mount Shuksan rises to **9,129 ft (2,783 m)** with 4,404 ft (1,342 m) of prominence in Washington State, North Cascades. The peak is located at 48.831095, -121.602955 ([Google Maps](https://www.google.com/maps/search/?api=1&query=48.831095,-121.602955) | [USGS Topo](https://ngmdb.usgs.gov/topoview/viewer/#16/48.831095/-121.602955)). The standard route is a **glacier climb** rated **Class 3-4**.

The Sulphide Glacier route is a classic North Cascades alpine climb combining glacier travel with an exposed scramble up the summit pyramid. Most parties complete the climb over 2-3 days, camping at the ~6,400 ft high camp before an alpine start for the summit push. The route demands solid crevasse rescue skills and glacier travel experience.

**Sources:** [PeakBagger](https://www.peakbagger.com/peak.aspx?pid=1630), [WTA](https://www.wta.org/go-hiking/hikes/mt-shuksan), [SummitPost](https://www.summitpost.org/mount-shuksan/150347), [AllTrails](https://www.alltrails.com/trail/us/washington/mountt-shuksan-sulphide-glacier), [Mountaineers](https://www.mountaineers.org/activities/routes-places/north-cascades-national-park-cross-country-zones/high-occupancy-xc-zones/mount-shuksan-sulphide-glacier)

## Route

### Approach

Shannon Ridge Trailhead (FR 1152), approximately 2,500 ft elevation.

**Directions:** [View on Google Maps](https://www.google.com/maps/search/?api=1&query=Shannon+Ridge+Trailhead+WA)

### Access & Permits

#### Permits & Regulations

- **North Cascades National Park Wilderness Permit** required (mandatory)
- Trailhead registration for Mt. Baker-Snoqualmie National Forest
- **Northwest Forest Pass** required for parking
- Blue bags or solar toilet use required at high camps (~6,400 ft ridge or ~6,100 ft rock island)
- Do not camp on heather benches except at prepared campsites

#### Road Conditions

The last 2.7 miles of Mount Baker Highway/SR 542 (Heather Meadows to Artist Point) is **closed for winter**. Shannon Ridge approach remains accessible though may close after significant snowfall.

### Route Description

The route covers approximately **13 miles round trip** with **6,700 ft** of elevation gain (trailhead to summit).

**Typical completion times (summit day from high camp, ~3,000 ft gain):**

- **4-5 hours** (~1.5 mph, 800+ ft/hr): Experienced alpinists, fast and light
- **5-7 hours** (~1.2 mph, 600 ft/hr): Average pace with breaks
- **7-9 hours** (~0.8 mph, 400 ft/hr): Slower parties, challenging conditions

**Day 1 - Approach to High Camp:**
Begin at Shannon Ridge Trailhead (~2,500 ft). The approach climbs steadily through forest for approximately 7 miles, passing through Shannon Ridge (excellent blueberry picking in season). Establish camp at the pass (~6,400 ft) or rock island (~6,100 ft). This is typically the most physically demanding day with 45-50 lb packs.

**Day 2 - Summit Day:**
Start early (4-5 AM typical) to take advantage of frozen snow conditions. Cross the ridge and traverse 900-1,200 ft northeast to intersect the south snout of the Sulphide Glacier. The lower flat, icy portion may be separated from the upper glacier by a snowless rock band requiring short scrambling.

Navigate crevassed terrain - in late season, bare ice conditions exist until approximately 7,300-7,400 ft. Large crevasses may require snowbridge crossings. Take a long curved route up and across the Sulphide Glacier to the left (north) side of the summit pyramid.

The final 500-600 ft ascends the summit pyramid via a central gully. This is rated **Class 3** in dry conditions but many consider it **Class 3+** or even **Class 4**. In early season, snow may fill the gully.

**Alternate Route - SE Ridge:**
Instead of the gully scramble, the SE Ridge offers a rock climbing alternative. The crux is rated **5.4** with the rest being low 5th or 4th class. Per recent trip reports, this route is "not that much slower than the gully scramble, safer, and much more fun."

### Crux

The crux of the Sulphide Glacier route is the **600 ft Class 3-4 summit pyramid gully**. This section features loose rock requiring careful hand/foot placements and attention to parties above. Multiple trip reports caution about rockfall hazard when other parties are on the route.

In winter/early season, the gully may be snow and ice-filled, requiring **crampons and ice axe** with solid steep snow technique. January 2026 trip reports indicate "solid snow and ice all the way to the summit" with secure conditions.

**Glacier travel** presents additional crux considerations - the Sulphide Glacier is heavily crevassed and conditions change rapidly. In late season, bare ice sections and large crevasses require careful navigation and potentially probing snowbridges.

### Hazards

- **Crevasses:** The Sulphide Glacier is crevassed terrain. Rope travel mandatory. In late season, bare ice conditions and obvious crevasses. In early/winter season, hidden crevasses under snow require probing.
- **Rockfall:** The summit pyramid gully has loose rock. Helmets required. Avoid climbing below other parties.
- **Exposure:** The summit pyramid and SE Ridge have significant exposure. Fall consequences are serious.
- **Route-finding:** In poor visibility, navigation on the glacier and finding the correct line up the summit pyramid can be challenging.
- **Weather:** The North Cascades can experience rapid weather changes. Whiteout conditions make glacier navigation extremely difficult.
- **Winter conditions:** Snowshoes may be required for approach (sinking to knees/hips reported in January 2026). Avalanche terrain exists.

**Bailout options:** Can descend at any point on the glacier. The summit pyramid is the point of no return for most weather concerns.

**Required Gear:**

- Standard glacier equipment (rope, harness, crampons, ice axe, crevasse rescue gear)
- Helmet (mandatory for rockfall protection)
- Snowshoes (winter/early season approach)
- Pickets and/or ice screws (may not be needed if conditions are solid)

## Current Conditions

### Daylight

For **January 30, 2026**, sunrise is at **7:36 AM** and sunset at **5:02 PM**, providing **9 hours 26 minutes** of daylight. Civil twilight begins at **7:04 AM**, useful for planning alpine starts.

### Weather Forecast

The forecast shows an **active winter storm pattern** with heavy snowfall and cold temperatures. January 29-30 bring significant snow accumulation (40-50mm precipitation) with moderate winds (45+ km/h). A brief improvement appears Jan 31 before another storm system arrives Feb 1-2 with additional heavy precipitation. February 3-4 show a trend toward clearing with decreasing precipitation chances.

Freezing levels remain low throughout the period (1,200-3,100 ft), well below the trailhead elevation. **All precipitation will fall as snow.** Temperatures range from highs of 16-25°F to lows of 12-18°F. These are **full winter conditions** requiring complete winter mountaineering equipment and experience.

**Summary:** Stormy winter conditions through early February. Wait for the clearing trend around Feb 3-4 if possible, and verify avalanche conditions before travel.

**Freezing Level Alert (Peak: 9,129 ft):**

- Jan 29 - Feb 3: 1,200-3,100 ft (FAR BELOW summit - full winter conditions, all snow)
- Feb 4: 2,500-2,900 ft (still well below summit)

| Day | Conditions | Temperature | Precipitation |
|-----|-----------|-------------|---------------|
| Thu Jan 29, 2026 (Today) | ❄️ Snow | High: 21°F, Low: 16°F | 39mm, 100% |
| Fri Jan 30, 2026 | ❄️ Snow | High: 23°F, Low: 18°F | 51mm, 100% |
| Sat Jan 31, 2026 | 🌨️ Snow/Fog | High: 25°F, Low: 16°F | 8mm, 52% |
| Sun Feb 1, 2026 | ❄️ Snow | High: 18°F, Low: 14°F | 35mm, 96% |
| Mon Feb 2, 2026 | 🌧️❄️ Rain/Snow | High: 16°F, Low: 12°F | 19mm, 87% |
| Tue Feb 3, 2026 | 🌧️ Light precipitation | High: 19°F, Low: 12°F | 4mm, 41% |
| Wed Feb 4, 2026 | ⛅ Clearing | High: 21°F, Low: 14°F | 0mm, 12% |

**Air Quality:**

Air quality is **good** (AQI <50) during the forecast period. Winter conditions typically bring clear air quality.

**Check Current Forecasts:**

- [Mountain-Forecast.com](https://www.mountain-forecast.com/peaks/Mount-Shuksan/forecasts/2783) - Summit-level forecast
- [Open-Meteo Weather](https://open-meteo.com/en/docs#latitude=48.831095&longitude=-121.602955&elevation=2783&hourly=&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto) - Detailed mountain weather data
- [NOAA Point Forecast](https://forecast.weather.gov/MapClick.php?textField1=48.831095&textField2=-121.602955) - Official NWS forecast
- [NWAC Mountain Weather](https://nwac.us/mountain-weather-forecast/) - Cascades mountain weather

### Avalanche Forecast

**Active avalanche season.** The route crosses significant avalanche terrain on the Sulphide Glacier and approach slopes.

Current conditions: Heavy snowfall loading slopes. Expect HIGH to EXTREME avalanche danger during and immediately after storms.

**Check [NWAC North Cascades Avalanche Forecast](https://nwac.us/avalanche-forecast/#north-cascades) for current danger ratings by elevation band.**

## Trip Reports

Mount Shuksan is a popular objective with 1,215 viewable ascents on PeakBagger, including 360 with trip reports. The peak sees 94 ascents in the past year with 32 trip reports available. Most ascents occur July-August (690 combined) with limited winter activity.

### Most Detailed Reports

**PeakBagger:**

- **2025-09-05** - [Cam Smith](https://www.peakbagger.com/climber/ascent.aspx?aid=2973475) - 📝 278 words, 📍 GPX - Detailed late season beta: bare ice conditions, crevasse navigation, SE Ridge route
- **2026-01-19** - [Zachary Richardson](https://www.peakbagger.com/climber/ascent.aspx?aid=3101256) - 📝 114 words - Winter ascent: snowshoes required, solid snow/ice conditions
- **2025-08-17** - [Ben C](https://www.peakbagger.com/climber/ascent.aspx?aid=2950323) - 📝 123 words, 📍 GPX
- **2025-08-25** - [Maureen Seeley](https://www.peakbagger.com/climber/ascent.aspx?aid=2969121) - 📝 119 words

**Washington Trails Association:**

44 trip reports available at the WTA page. Check for recent conditions and detailed reports.

### Browse All Trip Reports

- [PeakBagger Ascents](https://www.peakbagger.com/climber/PeakAscents.aspx?pid=1630) - Individual climb logs with optional GPX tracks and reports
- [Washington Trails Association](https://www.wta.org/go-hiking/hikes/mt-shuksan) - User-submitted trip reports with photos and conditions
- [Mountaineers.org](https://www.mountaineers.org/activities/routes-places/north-cascades-national-park-cross-country-zones/high-occupancy-xc-zones/mount-shuksan-sulphide-glacier) - Route information and trip reports
- [AllTrails](https://www.alltrails.com/trail/us/washington/mountt-shuksan-sulphide-glacier) - User reviews and recent activity
- [SummitPost](https://www.summitpost.org/mount-shuksan/150347) - Route-specific trip reports and photos

## Information Gaps

- WTA individual trip report extraction not performed (would require additional cloudscrape calls)
- Mountaineers.org trip report extraction failed - JavaScript-rendered content requires browser automation
- AllTrails reviews not extracted - JavaScript-rendered content
- SummitPost direct fetch blocked (403) - cloudscrape returned HTML only, detailed route beta not extracted
- Average PeakBagger trip report length is ~100-150 words; WTA reports typically provide more detailed conditions

## Data Sources

- PeakBagger: https://www.peakbagger.com/peak.aspx?pid=1630
- WTA: https://www.wta.org/go-hiking/hikes/mt-shuksan
- SummitPost: https://www.summitpost.org/mount-shuksan/150347
- AllTrails: https://www.alltrails.com/trail/us/washington/mountt-shuksan-sulphide-glacier
- Mountaineers.org: https://www.mountaineers.org/activities/routes-places/north-cascades-national-park-cross-country-zones/high-occupancy-xc-zones/mount-shuksan-sulphide-glacier
- Open-Meteo Weather API: Forecast data
- Sunrise-Sunset.org API: Daylight calculations
- NWAC: Avalanche forecast reference

---

*Research completed 2026-01-29 using [route-researcher v1.0](https://github.com/dreamiurg/claude-mountaineering-skills/tree/main/skills/route-researcher) from the [Claude Mountaineering Skills](https://github.com/dreamiurg/claude-mountaineering-skills) repository.*

---

## Example: 2026 01 29 Tinkham Peak

# Tinkham Peak - Route Beta Research (2026-01-29)

> **AI-Generated Research Document**
>
> This document was generated by an AI assistant and should be used as a **starting point only**.
>
> **YOU MUST:**
>
> - Verify all critical information from primary sources
> - Use your own judgment and experience to assess conditions and risk
> - Cross-reference with current trip reports and local conditions
> - Understand that conditions change rapidly in the mountains
>
> **This is NOT a substitute for:**
>
> - Proper training and experience
> - Current weather and avalanche forecasts
> - Your own research and route planning
> - Sound mountaineering judgment
>
> The mountains are inherently dangerous. You are responsible for your own safety.

## Overview

Tinkham Peak rises to **5,398 ft (1,645 m)** with 677 ft (206 m) of prominence in the Cascade Range, King County, Washington. The peak is located at 47.349185, -121.454685 ([Google Maps](https://www.google.com/maps/search/?api=1&query=47.349185,-121.454685) | [USGS Topo](https://ngmdb.usgs.gov/topoview/viewer/#15/47.349185/-121.454685)). The standard route via Mirror Lake is a **scramble** rated **Class 2 with brief Class 3 near the summit**.

The route offers a scenic approach through old-growth forest, past Mirror and Cottonwood Lakes, before ascending a steep boot path to the rocky summit. Multiple trip reports describe excellent views of Mount Rainier, surrounding lakes, and nearby peaks. The peak features two summits (east and west) connected by an easy ridge traverse.

**Sources:** [PeakBagger](https://www.peakbagger.com/peak.aspx?pid=2222), [WTA](https://www.wta.org/go-hiking/hikes/tinkham-peak), [AllTrails](https://www.alltrails.com/trail/us/washington/tinkham-peak-tinkham-east-boot-trail), [Mountaineers](https://www.mountaineers.org/activities/routes-places/mirror-lake-tinkham-peak)

## Route

### Approach

**Mirror Lake Trailhead** (3,600 ft)

**Directions:** [View on Google Maps](https://www.google.com/maps/search/?api=1&query=Mirror+Lake+Trailhead+Snoqualmie+Pass+WA)

From I-90: Take Exit 62, turn right, drive 1.1 miles, and turn right onto Forest Road 5480. Drive 4.1 miles, going straight at the junction with Forest Road 5483 to stay on FR-5480, and reach a five-way junction at Lost Lake. DO NOT continue straight - instead, veer right to remain on FR-5480 and go around the east and north sides of the lake until reaching the Mirror Lake parking area(s).

**Road Conditions:** The forest road is in good shape as of late 2025. Trip reports indicate any car can make it to the trailhead, though the final 0.2 miles has deteriorated and high-clearance vehicles may have better access to the upper parking area.

### Access & Permits

#### Permits & Regulations

- **Northwest Forest Pass** required for parking at the trailhead
- Alternative: National Parks/Federal Lands Annual Pass accepted

**IMPORTANT:** Do not cross the Cedar River Watershed boundary (marked with "No Trespassing" signs). Serious consequences apply for watershed violations.

#### Road Conditions

Roads within Mount Baker-Snoqualmie and Okanogan-Wenatchee National Forests are subject to seasonal closure. FR-5480 is typically accessible April through November.

### Route Description

The route covers approximately **6 miles round-trip** with **2,100 ft** of elevation gain.

**Typical completion times:**

- **2.5-3 hours** (~2 mph, 1000+ ft/hr): Trail runners, fit scramblers moving fast
- **3.5-4.5 hours** (~1.5 mph, 700-800 ft/hr): Average fitness, steady pace with brief breaks
- **5-6 hours** (~1 mph, 500-600 ft/hr): Relaxed pace, groups, taking time for photos

**Approach (1.5 miles, ~300 ft gain):** The trail begins gently, following the Pacific Crest Trail through old-growth forest. At approximately 1.3 miles, pass Cottonwood Lake on your right. Continue to Mirror Lake at 1.5 miles.

**Boot Path to Summit (1.5 miles, ~1,800 ft gain):** At Mirror Lake, cross the logjam at the lake's outlet and follow the way trail along the south shore for about 200 yards. Look for a faint path marked by ribbons heading south up the ridge. The unmaintained boot path ascends steeply through forest with roots, rocks, and occasional deadfall. Multiple trip reports note this steep forest section as the least enjoyable part but easy to follow.

After breaking out of the trees, the final few hundred feet offer open views and steeper, rockier terrain. The route remains Class 2 to the summit with one brief Class 3 section near the summit block. Trip reports emphasize staying on the correct boot path to avoid unnecessary Class 3/4 moves.

**East to West Summit Traverse (0.25 miles, ~10 minutes):** The traverse between Tinkham Peak (east summit, 5,398 ft) and the west summit (5,394 ft) is easy Class 1-2 along a broad ridge on the south side. Both summits have summit registers.

### Crux

The crux is located near the summit block at approximately 5,200-5,400 ft, where the route steepens to **Class 2+/3-** terrain on rocky outcrops. Multiple boot paths exist near the summit block - trip reports consistently note that if you encounter Class 3 or 4 moves, you're off-route and should look for an easier line. The exposure is moderate on the SW face. In wet or icy conditions, rocks become slippery and extra caution is warranted.

### Hazards

**Route-finding:** Multiple social trails around Mirror Lake can make finding the boot path tricky. Look for the path at the south shore, approximately 200 yards after crossing the logjam.

**Steep terrain:** The boot path is steep throughout, with sections of loose soil, roots, and rocks. Trekking poles highly recommended.

**Cliff exposure:** The north side of the summit has sheer cliffs with potential for fatal falls. Keep pets leashed near the summit. Exercise caution, especially in wet or icy conditions.

**Weather exposure:** The upper portion of the route is above treeline and exposed to changing weather. Summer thunderstorms can develop quickly.

**Seasonal considerations:**

- **Summer (July-September):** Best conditions. Bugs can be heavy at the summit and near water.
- **Fall (October-November):** Good conditions, fewer crowds, potential for early snow.
- **Winter/Spring:** Snow and ice on upper route. Microspikes or crampons may be required. Avalanche assessment needed.

## Current Conditions

### Daylight

For **January 29, 2026**, sunrise is at **7:33 AM** and sunset at **5:04 PM**, providing **9 hours 32 minutes** of daylight. Civil twilight begins at **7:01 AM**, useful for planning alpine starts.

### Weather Forecast

The forecast shows an active winter pattern with light snow and cool temperatures through late January, improving to drier conditions by early February. Thursday brings **light snow with 15.6mm precipitation** and gusty winds. Friday continues unsettled with a rain/snow mix. Saturday offers a brief clearing with partly cloudy skies and no precipitation - **the best weather window this week**. Sunday through Monday return to wet conditions with rain/snow mix. The pattern improves significantly Tuesday-Wednesday with decreasing precipitation chances and warmer temperatures.

**Summary:** Saturday (Jan 31) offers the best weather window with clearing skies and no precipitation; avoid Thursday-Friday and Sunday-Monday due to active precipitation.

**Freezing Level Alert (Peak: 5,398 ft):**

- Thu-Fri (Jan 29-30): 1,300-2,500 ft (well below summit - expect snow at summit)
- Sat (Jan 31): 2,400-2,600 ft (below summit - snow/ice likely on route)
- Sun-Mon (Feb 1-2): 1,400-2,800 ft (below summit - snow/ice conditions)
- Tue-Wed (Feb 3-4): 3,200-3,400 ft (below summit - snow/ice possible on upper route)

| Day | Conditions | Temperature | Precipitation |
|-----|-----------|-------------|---------------|
| Thu Jan 29, 2026 (Today) | ❄️ Light snow | High: 28°F, Low: 27°F | 15.6mm (98%) |
| Fri Jan 30, 2026 | 🌨️ Snow/rain mix | High: 34°F, Low: 28°F | 6.6mm (84%) |
| Sat Jan 31, 2026 | ⛅ Partly cloudy | High: 37°F, Low: 28°F | 0mm (47%) |
| Sun Feb 1, 2026 | 🌧️ Rain/snow showers | High: 30°F, Low: 25°F | 8.5mm (88%) |
| Mon Feb 2, 2026 | 🌨️ Light rain/snow | High: 30°F, Low: 25°F | 6.4mm (60%) |
| Tue Feb 3, 2026 | ⛅ Partly cloudy to light rain | High: 37°F, Low: 28°F | 2.1mm (25%) |
| Wed Feb 4, 2026 | ☀️ Clear to partly cloudy | High: 41°F, Low: 27°F | 0mm (6%) |

**Air Quality:**

Air quality is **good** (AQI 32-42) during the forecast period. No air quality concerns for outdoor activities.

**Check Current Forecasts:**

- [Mountain-Forecast.com](https://www.mountain-forecast.com/peaks/Tinkham-Peak/forecasts/1645) - Summit-level forecast with multiple elevations
- [Open-Meteo Weather](https://open-meteo.com/en/docs#latitude=47.349185&longitude=-121.454685&elevation=1645&hourly=&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto) - Detailed mountain weather data (source for this report)
- [Open-Meteo Air Quality](https://open-meteo.com/en/docs/air-quality-api#latitude=47.349185&longitude=-121.454685&hourly=&daily=&timezone=auto) - Air quality forecast for this location
- [NOAA Point Forecast](https://forecast.weather.gov/MapClick.php?textField1=47.349185&textField2=-121.454685) - Official NWS forecast and alerts
- [NWAC Mountain Weather](https://nwac.us/mountain-weather-forecast/) - Cascades mountain weather (winter season)

### Avalanche Forecast

**Note:** Current conditions (late January) warrant avalanche awareness on this route. The upper portion of Tinkham Peak has avalanche terrain.

**Avalanche forecast not available.** Check [NWAC.us](https://nwac.us) for current conditions before travel.

## Trip Reports

Tinkham Peak has 648 total ascents logged on PeakBagger with 91 trip reports and 56 GPX tracks. WTA shows 80 trip reports. Most PeakBagger reports are brief (average <100 words), so WTA reports provide more detailed beta.

### Most Detailed Reports

**PeakBagger:**

- **2024-09-15** - [Patty Cokus](https://www.peakbagger.com/climber/ascent.aspx?aid=2654835) - 461 words - Loop via Silver-Abiel-Tinkham, noted wet conditions, scrambly summit
- **2024-08-25** - [Jared Jones](https://www.peakbagger.com/climber/ascent.aspx?aid=2652913) - 413 words - Multi-peak loop with detailed route description
- **2024-08-09** - [Jamie Yelland](https://www.peakbagger.com/climber/ascent.aspx?aid=2601903) - 230 words - Silver/Abiel/Tinkham in that order
- **2024-08-31** - [Paul Kallmann](https://www.peakbagger.com/climber/ascent.aspx?aid=2630390) - 218 words - Mountaineers scramble, Windy Pass approach
- **2025-09-07** - [Francisco Madera](https://www.peakbagger.com/climber/ascent.aspx?aid=2976953) - 169 words, 📍 GPX - Recent detailed beta on difficulty

**Washington Trails Association:**

- **2025-11-16** - [Mirror and Cottonwood Lakes, Tinkham Peak, Twilight Lake](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-11-17.013746275873) - Clockwise loop, late season conditions
- **2025-09-26** - [Tinkham Peak](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-30.071521868992) - Detailed route description, road conditions
- **2025-09-20** - [Silver Peak, Tinkham Peak](https://www.wta.org/go-hiking/trip-reports/trip_report-2025-09-20.190840024989) - Multi-peak with photos

### Browse All Trip Reports

- [PeakBagger Ascents](https://www.peakbagger.com/climber/PeakAscents.aspx?pid=2222) - Individual climb logs with optional GPX tracks and reports
- [Washington Trails Association](https://www.wta.org/go-hiking/hikes/tinkham-peak) - User-submitted trip reports with photos and conditions (80 reports)
- [AllTrails](https://www.alltrails.com/trail/us/washington/tinkham-peak-tinkham-east-boot-trail) - User reviews and recent activity (514 reviews)

## Information Gaps

- **SummitPost access blocked:** WebFetch returned 403 and cloudscrape.py returned limited HTML content. Check [SummitPost](https://www.summitpost.org/tinkham-peak/151401) manually for additional route beta.
- **Avalanche forecast script not implemented:** Check NWAC.us manually for current avalanche conditions (critical during winter months).
- **No PeakBagger route data:** The peak has no formal routes in PeakBagger database - route information synthesized from trip reports.
- **Limited detailed PeakBagger reports:** Most PeakBagger reports are <100 words. WTA provides more comprehensive trip reports.
- **Mountaineers.org trip report extraction not attempted:** Check [Mountaineers](https://www.mountaineers.org/activities/routes-places/mirror-lake-tinkham-peak) manually for additional route information.

## Data Sources

- PeakBagger: https://www.peakbagger.com/peak.aspx?pid=2222
- Washington Trails Association: https://www.wta.org/go-hiking/hikes/tinkham-peak
- AllTrails: https://www.alltrails.com/trail/us/washington/tinkham-peak-tinkham-east-boot-trail
- The Mountaineers: https://www.mountaineers.org/activities/routes-places/mirror-lake-tinkham-peak
- Open-Meteo Weather API: https://open-meteo.com/
- Sunrise-Sunset.org API: https://sunrise-sunset.org/

---

*Research completed 2026-01-29 using [route-researcher v3.5.0](https://github.com/dreamiurg/claude-mountaineering-skills/tree/main/skills/route-researcher) from the [Claude Mountaineering Skills](https://github.com/dreamiurg/claude-mountaineering-skills) repository.*
