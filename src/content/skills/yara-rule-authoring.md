---
title: "Yara Rule Authoring"
description: "Guides authoring of high-quality YARA-X detection rules for malware identification. Use when writing, reviewing, or optimizing YARA rules. Covers naming conventions, string selection, performance optimization, migration from legacy YARA, and false..."
category: "writing"
source: "community"
author: "Community"
tags: ["yara", "rule", "authoring"]
date: 2026-03-20
---

# YARA-X Rule Authoring

Write detection rules that catch malware without drowning in false positives.

> **This skill targets YARA-X**, the Rust-based successor to legacy YARA. YARA-X powers VirusTotal's production systems and is the recommended implementation. See [Migrating from Legacy YARA](#migrating-from-legacy-yara) if you have existing rules.

## Core Principles

1. **Strings must generate good atoms** — YARA extracts 4-byte subsequences for fast matching. Strings with repeated bytes, common sequences, or under 4 bytes force slow bytecode verification on too many files.

2. **Target specific families, not categories** — "Detects ransomware" catches everything and nothing. "Detects LockBit 3.0 configuration extraction routine" catches what you want.

3. **Test against goodware before deployment** — A rule that fires on Windows system files is useless. Validate against VirusTotal's goodware corpus or your own clean file set.

4. **Short-circuit with cheap checks first** — Put `filesize < 10MB and uint16(0) == 0x5A4D` before expensive string searches or module calls.

5. **Metadata is documentation** — Future you (and your team) need to know what this catches, why, and where the sample came from.

## When to Use

- Writing new YARA-X rules for malware detection
- Reviewing existing rules for quality or performance issues
- Optimizing slow-running rulesets
- Converting IOCs or threat intel into detection signatures
- Debugging false positive issues
- Preparing rules for production deployment
- Migrating legacy YARA rules to YARA-X
- Analyzing Chrome extensions (crx module)
- Analyzing Android apps (dex module)

## When NOT to Use

- Static analysis requiring disassembly → use Ghidra/IDA skills
- Dynamic malware analysis → use sandbox analysis skills
- Network-based detection → use Suricata/Snort skills
- Memory forensics with Volatility → use memory forensics skills
- Simple hash-based detection → just use hash lists

## YARA-X Overview

YARA-X is the Rust-based successor to legacy YARA: 5-10x faster regex, better errors, built-in formatter, stricter validation, new modules (crx, dex), 99% rule compatibility.

**Install:** `brew install yara-x` (macOS) or `cargo install yara-x`

**Essential commands:** `yr scan`, `yr check`, `yr fmt`, `yr dump`

## Platform Considerations

YARA works on any file type. Adapt patterns to your target:

| Platform | Magic Bytes | Bad Strings | Good Strings |
|----------|-------------|-------------|--------------|
| **Windows PE** | `uint16(0) == 0x5A4D` | API names, Windows paths | Mutex names, PDB paths |
| **macOS Mach-O** | `uint32(0) == 0xFEEDFACE` (32-bit), `0xFEEDFACF` (64-bit), `0xCAFEBABE` (universal) | Common Obj-C methods | Keylogger strings, persistence paths |
| **JavaScript/Node** | (none needed) | `require`, `fetch`, `axios` | Obfuscator signatures, eval+decode chains |
| **npm/pip packages** | (none needed) | `postinstall`, `dependencies` | Suspicious package names, exfil URLs |
| **Office docs** | `uint32(0) == 0x504B0304` | VBA keywords | Macro auto-exec, encoded payloads |
| **VS Code extensions** | (none needed) | `vscode.workspace` | Uncommon activationEvents, hidden file access |
| **Chrome extensions** | Use `crx` module | Common Chrome APIs | Permission abuse, manifest anomalies |
| **Android apps** | Use `dex` module | Standard DEX structure | Obfuscated classes, suspicious permissions |

### macOS Malware Detection

No dedicated Mach-O module exists yet. Use magic byte checks + string patterns:

**Magic bytes:**
```yara
// Mach-O 32-bit
uint32(0) == 0xFEEDFACE
// Mach-O 64-bit
uint32(0) == 0xFEEDFACF
// Universal binary (fat binary)
uint32(0) == 0xCAFEBABE or uint32(0) == 0xBEBAFECA
```

**Good indicators for macOS malware:**
- Keylogger artifacts: `CGEventTapCreate`, `kCGEventKeyDown`
- SSH tunnel strings: `ssh -D`, `tunnel`, `socks`
- Persistence paths: `~/Library/LaunchAgents`, `/Library/LaunchDaemons`
- Credential theft: `security find-generic-password`, `keychain`

**Example pattern from Airbnb BinaryAlert:**
```yara
rule SUSP_Mac_ProtonRAT
{
    strings:
        // Library indicators
        $lib1 = "SRWebSocket" ascii
        $lib2 = "SocketRocket" ascii

        // Behavioral indicators
        $behav1 = "SSH tunnel not launched" ascii
        $behav2 = "Keylogger" ascii

    condition:
        (uint32(0) == 0xFEEDFACF or uint32(0) == 0xCAFEBABE) and
        any of ($lib*) and any of ($behav*)
}
```

### JavaScript Detection Decision Tree

```
Writing a JavaScript rule?
├─ npm package?
│  ├─ Check package.json patterns
│  ├─ Look for postinstall/preinstall hooks
│  └─ Target exfil patterns: fetch + env access + credential paths
├─ Browser extension?
│  ├─ Chrome: Use crx module
│  └─ Others: Target manifest patterns, background script behaviors
├─ Standalone JS file?
│  ├─ Look for obfuscation markers: eval+atob, fromCharCode chains
│  ├─ Target unique function/variable names (often survive minification)
│  └─ Check for packed/encoded payloads
└─ Minified/webpack bundle?
   ├─ Target unique strings that survive bundling (URLs, magic values)
   └─ Avoid function names (will be mangled)
```

**JavaScript-specific good strings:**
- Ethereum function selectors: `{ 70 a0 82 31 }` (transfer)
- Zero-width characters (steganography): `{ E2 80 8B E2 80 8C }`
- Obfuscator signatures: `_0x`, `var _0x`
- Specific C2 patterns: domain names, webhook URLs

**JavaScript-specific bad strings:**
- `require`, `fetch`, `axios` — too common
- `Buffer`, `crypto` — legitimate uses everywhere
- `process.env` alone — need specific env var names

## Essential Toolkit

| Tool | Purpose |
|------|---------|
| **yarGen** | Extract candidate strings: `yarGen.py -m samples/ --excludegood` → validate with `yr check` |
| **FLOSS** | Extract obfuscated/stack strings: `floss sample.exe` (when yarGen fails) |
| **yr CLI** | Validate: `yr check`, scan: `yr scan -s`, inspect: `yr dump -m pe` |
| **signature-base** | Study quality examples |
| **YARA-CI** | Goodware corpus testing before deployment |

Master these five. Don't get distracted by tool catalogs.

## Rationalizations to Reject

When you catch yourself thinking these, stop and reconsider.

| Rationalization | Expert Response |
|-----------------|-----------------|
| "This generic string is unique enough" | Test against goodware first. Your intuition is wrong. |
| "yarGen gave me these strings" | yarGen suggests, you validate. Check each one manually. |
| "It works on my 10 samples" | 10 samples ≠ production. Use VirusTotal goodware corpus. |
| "One rule to catch all variants" | Causes FP floods. Target specific families. |
| "I'll make it more specific if we get FPs" | Write tight rules upfront. FPs burn trust. |
| "This hex pattern is unique" | Unique in one sample ≠ unique across malware ecosystem. |
| "Performance doesn't matter" | One slow rule slows entire ruleset. Optimize atoms. |
| "PEiD rules still work" | Obsolete. 32-bit packers aren't relevant. |
| "I'll add more conditions later" | Weak rules deployed = damage done. |
| "This is just for hunting" | Hunting rules become detection rules. Same quality bar. |
| "The API name makes it malicious" | Legitimate software uses same APIs. Need behavioral context. |
| "any of them is fine for these common strings" | Common strings + any = FP flood. Use `any of` only for individually unique strings. |
| "This regex is specific enough" | `/fetch.*token/` matches all auth code. Add exfil destination requirement. |
| "The JavaScript looks clean" | Attackers poison legitimate code with injects. Check for eval+decode chains. |
| "I'll use .* for flexibility" | Unbounded regex = performance disaster + memory explosion. Use `.{0,30}`. |
| "I'll use --relaxed-re-syntax everywhere" | Masks real bugs. Fix the regex instead of hiding problems. |

## Decision Trees

### Is This String Good Enough?

```
Is this string good enough?
├─ Less than 4 bytes?
│  └─ NO — find longer string
├─ Contains repeated bytes (0000, 9090)?
│  └─ NO — add surrounding context
├─ Is an API name (VirtualAlloc, CreateRemoteThread)?
│  └─ NO — use hex pattern of call site instead
├─ Appears in Windows system files?
│  └─ NO — too generic, find something unique
├─ Is it a common path (C:\Windows\, cmd.exe)?
│  └─ NO — find malware-specific paths
├─ Unique to this malware family?
│  └─ YES — use it
└─ Appears in other malware too?
   └─ MAYBE — combine with family-specific marker
```

### When to Use "all of" vs "any of"

```
Should I require all strings or allow any?
├─ Strings are individually unique to malware?
│  └─ any of them (each alone is suspicious)
├─ Strings are common but combination is suspicious?
│  └─ all of them (require the full pattern)
├─ Strings have different confidence levels?
│  └─ Group: all of ($core_*) and any of ($variant_*)
└─ Seeing many false positives?
   └─ Tighten: switch any → all, add more required strings
```

**Lesson from production:** Rules using `any of ($network_*)` where strings included "fetch", "axios", "http" matched virtually all web applications. Switching to require credential path AND network call AND exfil destination eliminated FPs.

### When to Abandon a Rule Approach

Stop and pivot when:

- **yarGen returns only API names and paths** → See [When Strings Fail, Pivot to Structure](#when-strings-fail-pivot-to-structure)

- **Can't find 3 unique strings** → Probably packed. Target the unpacked version or detect the packer.

- **Rule matches goodware files** → Strings aren't unique enough. 1-2 matches = investigate and tighten; 3-5 matches = find different indicators; 6+ matches = start over.

- **Performance is terrible even after optimization** → Architecture problem. Split into multiple focused rules or add strict pre-filters.

- **Description is hard to write** → The rule is too vague. If you can't explain what it catches, it catches too much.

### Debugging False Positives

```
FP Investigation Flow:
│
├─ 1. Which string matched?
│     Run: yr scan -s rule.yar false_positive.exe
│
├─ 2. Is it in a legitimate library?
│     └─ Add: not $fp_vendor_string exclusion
│
├─ 3. Is it a common development pattern?
│     └─ Find more specific indicator, replace the string
│
├─ 4. Are multiple generic strings matching together?
│     └─ Tighten to require all + add unique marker
│
└─ 5. Is the malware using common techniques?
      └─ Target malware-specific implementation details, not the technique
```

### Hex vs Text vs Regex

```
What string type should I use?
│
├─ Exact ASCII/Unicode text?
│  └─ TEXT: $s = "MutexName" ascii wide
│
├─ Specific byte sequence?
│  └─ HEX: $h = { 4D 5A 90 00 }
│
├─ Byte sequence with variation?
│  └─ HEX with wildcards: { 4D 5A ?? ?? 50 45 }
│
├─ Pattern with structure (URLs, paths)?
│  └─ BOUNDED REGEX: /https:\/\/[a-z]{5,20}\.onion/
│
└─ Unknown encoding (XOR, base64)?
   └─ TEXT with modifier: $s = "config" xor(0x00-0xFF)
```

### Is the Sample Packed? (Check First)

Before writing any string-based rule:

```
Is the sample packed?
├─ Entropy > 7.0?
│  └─ Likely packed — find unpacked layer first
├─ Few/no readable strings?
│  └─ Likely packed — use entropy, PE structure, or packer signatures
├─ UPX/MPRESS/custom packer detected?
│  └─ Target the unpacked payload OR detect the packer itself
└─ Readable strings available?
   └─ Proceed with string-based detection
```

**Expert guidance:** Don't write rules against packed layers. The packing changes; the payload doesn't.

### When Strings Fail, Pivot to Structure

If yarGen returns only API names and generic paths:

```
String extraction failed — what now?
├─ High entropy sections?
│  └─ Use math.entropy() on specific sections
├─ Unusual imports pattern?
│  └─ Use pe.imphash() for import hash clustering
├─ Consistent PE structure anomalies?
│  └─ Target section names, sizes, characteristics
├─ Metadata present?
│  └─ Target version info, timestamps, resources
└─ Nothing unique?
   └─ This sample may not be detectable with YARA alone
```

**Expert guidance:** "One can try to use other file properties, such as metadata, entropy, import hashes or other data which stays constant." — Kaspersky Applied YARA Training

## Expert Heuristics

**String selection:** Mutex names are gold; C2 paths silver; error messages bronze. Stack strings are almost always unique. If you need >6 strings, you're over-fitting.

**Condition design:** Start with `filesize <`, then magic bytes, then strings, then modules. If >5 lines, split into multiple rules.

**Quality signals:** yarGen output needs 80% filtering. Rules matching <50% of variants are too narrow; matching goodware are too broad.

**Modifier discipline:**
- **Never use `nocase` or `wide` speculatively** — only when you have confirmed evidence the case/encoding varies in samples
- `nocase` doubles atom generation; `wide` doubles string matching — both have real costs
- "If you don't have a clear reason for using those modifiers, don't do it" — Kaspersky Applied YARA

**Regex anchoring:**
- Regex without a 4+ byte literal substring **evaluates at every file offset** — catastrophic performance
- Always anchor regex to a distinctive literal: `/mshta\.exe http:\/\/.../` not `/http:\/\/.../`
- If you can't anchor, consider hex pattern with wildcards instead

**Loop discipline:**
- Always bound loops with filesize: `filesize < 100KB and for all i in (1..#a) : ...`
- Unbounded `#a` can be thousands in large files — exponential slowdown

**YARA-X tips:** `$_unused` to suppress warnings; `private $s` to hide from output; `yr check` + `yr fmt` before every commit.

### When to Use Modules vs. Byte Checks

```
Should I use a module or raw bytes?
├─ Need imphash/rich header/authenticode?
│  └─ Use PE module — too complex to replicate
├─ Just checking magic bytes or simple offsets?
│  └─ Use uint16/uint32 — faster, no module overhead
├─ Checking section names/sizes?
│  └─ PE module is cleaner, but add magic bytes filter FIRST
├─ Checking Chrome extension permissions?
│  └─ Use crx module — string parsing is fragile
└─ Checking LNK target paths?
   └─ Use lnk module — LNK format is complex
```

**Expert guidance:** "Avoid the magic module — use explicit hex checks instead" — Neo23x0. Apply this principle: if you can do it with uint32(), don't load a module.

## YARA-X New Features

Key additions from recent releases:

- **Private patterns** (v1.3.0+): `private $helper = "pattern"` — matches but hidden from output
- **Warning suppression** (v1.4.0+): `// suppress: slow_pattern` inline comments
- **Numeric underscores** (v1.5.0+): `filesize < 10_000_000` for readability
- **Built-in formatter**: `yr fmt rules/` to standardize formatting
- **NDJSON output**: `yr scan --output-format ndjson` for tooling

## YARA-X Tooling Workflow

YARA-X provides diagnostic tools legacy YARA lacks:

**Rule development cycle:**
```bash
# 1. Write initial rule
# 2. Check syntax with detailed errors
yr check rule.yar

# 3. Format consistently
yr fmt -w rule.yar

# 4. Dump module output to inspect file structure (no dummy rule needed)
yr dump -m pe sample.exe --output-format yaml

# 5. Scan with timing info
time yr scan -s rule.yar corpus/
```

**When to use `yr dump`:**
- Investigating what PE/ELF/Mach-O fields are available
- Debugging why module conditions aren't matching
- Exploring new modules (crx, lnk, dotnet) before writing rules

**YARA-X diagnostic advantage:** Error messages include precise source locations. If `yr check` points to line 15, the issue is actually on line 15 (unlike legacy YARA).

## Chrome Extension Analysis (crx module)

The `crx` module enables detection of malicious Chrome extensions. Requires YARA-X v1.5.0+ (basic), v1.11.0+ for `permhash()`.

**Key APIs:** `crx.is_crx`, `crx.permissions`, `crx.permhash()`

**Red flags:** `nativeMessaging` + `downloads`, `debugger` permission, content scripts on `<all_urls>`

```yara
import "crx"

rule SUSP_CRX_HighRiskPerms {
    condition:
        crx.is_crx and
        for any perm in crx.permissions : (perm == "debugger")
}
```

See [crx-module.md](references/crx-module.md) for complete API reference, permission risk assessment, and example rules.

## Android DEX Analysis (dex module)

The `dex` module enables detection of Android malware. Requires YARA-X v1.11.0+. **Not compatible with legacy YARA's dex module** — API is completely different.

**Key APIs:** `dex.is_dex`, `dex.contains_class()`, `dex.contains_method()`, `dex.contains_string()`

**Red flags:** Single-letter class names (obfuscation), `DexClassLoader` reflection, encrypted assets

```yara
import "dex"

rule SUSP_DEX_DynamicLoading {
    condition:
        dex.is_dex and
        dex.contains_class("Ldalvik/system/DexClassLoader;")
}
```

See [dex-module.md](references/dex-module.md) for complete API reference, obfuscation detection, and example rules.

## Migrating from Legacy YARA

YARA-X has 99% rule compatibility, but enforces stricter validation.

**Quick migration:**
```bash
yr check --relaxed-re-syntax rules/  # Identify issues
# Fix each issue, then:
yr check rules/  # Verify without relaxed mode
```

**Common fixes:**
| Issue | Legacy | YARA-X Fix |
|-------|--------|------------|
| Literal `{` in regex | `/{/` | `/\{/` |
| Invalid escapes | `\R` silently literal | `\\R` or `R` |
| Base64 strings | Any length | 3+ chars required |
| Negative indexing | `@a[-1]` | `@a[#a - 1]` |
| Duplicate modifiers | Allowed | Remove duplicates |

> **Note:** Use `--relaxed-re-syntax` only as a diagnostic tool. Fix issues rather than relying on relaxed mode.

## Quick Reference

### Naming Convention

```
{CATEGORY}_{PLATFORM}_{FAMILY}_{VARIANT}_{DATE}
```

**Common prefixes:** `MAL_` (malware), `HKTL_` (hacking tool), `WEBSHELL_`, `EXPL_`, `SUSP_` (suspicious), `GEN_` (generic)

**Platforms:** `Win_`, `Lnx_`, `Mac_`, `Android_`, `CRX_`

**Example:** `MAL_Win_Emotet_Loader_Jan25`

See [style-guide.md](references/style-guide.md) for full conventions, metadata requirements, and naming examples.

### Required Metadata

Every rule needs: `description` (starts with "Detects"), `author`, `reference`, `date`.

```yara
meta:
    description = "Detects Example malware via unique mutex and C2 path"
    author = "Your Name <email@example.com>"
    reference = "https://example.com/analysis"
    date = "2025-01-29"
```

### String Selection

**Good:** Mutex names, PDB paths, C2 paths, stack strings, configuration markers
**Bad:** API names, common executables, format specifiers, generic paths

See [strings.md](references/strings.md) for the full decision tree and examples.

### Condition Patterns

**Order conditions for short-circuit:**
1. `filesize < 10MB` (instant)
2. `uint16(0) == 0x5A4D` (nearly instant)
3. String matches (cheap)
4. Module checks (expensive)

See [performance.md](references/performance.md) for detailed optimization patterns.

## Workflow

1. **Gather samples** — Multiple samples; single-sample rules are brittle
2. **Extract candidates** — `yarGen -m samples/ --excludegood`
3. **Validate quality** — Use decision tree; yarGen needs 80% filtering
4. **Write initial rule** — Follow template with proper metadata
5. **Lint and test** — `yr check`, `yr fmt`, linter script
6. **Goodware validation** — VirusTotal corpus or local clean files
7. **Deploy** — Add to repo with full metadata, monitor for FPs

See [testing.md](references/testing.md) for detailed validation workflow and FP investigation.

For a comprehensive step-by-step guide covering all phases from sample collection to deployment, see [rule-development.md](workflows/rule-development.md).

## Common Mistakes

| Mistake | Bad | Good |
|---------|-----|------|
| API names as indicators | `"VirtualAlloc"` | Hex pattern of call site + unique mutex |
| Unbounded regex | `/https?:\/\/.*/` | `/https?:\/\/[a-z0-9]{8,12}\.onion/` |
| Missing file type filter | `pe.imports(...)` first | `uint16(0) == 0x5A4D and filesize < 10MB` first |
| Short strings | `"abc"` (3 bytes) | `"abcdef"` (4+ bytes) |
| Unescaped braces (YARA-X) | `/config{key}/` | `/config\{key\}/` |

## Performance Optimization

**Quick wins:** Put `filesize` first, avoid `nocase`, bounded regex `{1,100}`, prefer hex over regex.

**Red flags:** Strings <4 bytes, unbounded regex (`.*`), modules without file-type filter.

See [performance.md](references/performance.md) for atom theory and optimization details.

## Reference Documents

| Topic | Document |
|-------|----------|
| Naming and metadata conventions | [style-guide.md](references/style-guide.md) |
| Performance and atom optimization | [performance.md](references/performance.md) |
| String types and judgment | [strings.md](references/strings.md) |
| Testing and validation | [testing.md](references/testing.md) |
| Chrome extension module (crx) | [crx-module.md](references/crx-module.md) |
| Android DEX module (dex) | [dex-module.md](references/dex-module.md) |

## Workflows

| Topic | Document |
|-------|----------|
| Complete rule development process | [rule-development.md](workflows/rule-development.md) |

## Example Rules

The `examples/` directory contains real, attributed rules demonstrating best practices:

| Example | Demonstrates | Source |
|---------|--------------|--------|
| [MAL_Win_Remcos_Jan25.yar](examples/MAL_Win_Remcos_Jan25.yar) | PE malware: graduated string counts, multiple rules per family | Elastic Security |
| [MAL_Mac_ProtonRAT_Jan25.yar](examples/MAL_Mac_ProtonRAT_Jan25.yar) | macOS: Mach-O magic bytes, multi-category grouping | Airbnb BinaryAlert |
| [MAL_NPM_SupplyChain_Jan25.yar](examples/MAL_NPM_SupplyChain_Jan25.yar) | npm supply chain: real attack patterns, ERC-20 selectors | Stairwell Research |
| [SUSP_JS_Obfuscation_Jan25.yar](examples/SUSP_JS_Obfuscation_Jan25.yar) | JavaScript: obfuscator detection, density-based matching | imp0rtp3, Nils Kuhnert |
| [SUSP_CRX_SuspiciousPermissions.yar](examples/SUSP_CRX_SuspiciousPermissions.yar) | Chrome extensions: crx module, permissions | Educational |

## Scripts

```bash
uv run {baseDir}/scripts/yara_lint.py rule.yar      # Validate style/metadata
uv run {baseDir}/scripts/atom_analyzer.py rule.yar  # Check string quality
```

See [README.md](../../README.md#scripts) for detailed script documentation.

## Quality Checklist

Before deploying any rule:

- [ ] Name follows `{CATEGORY}_{PLATFORM}_{FAMILY}_{VARIANT}_{DATE}` format
- [ ] Description starts with "Detects" and explains what/how
- [ ] All required metadata present (author, reference, date)
- [ ] Strings are unique (not API names, common paths, or format strings)
- [ ] All strings have 4+ bytes with good atom potential
- [ ] Base64 modifier only on strings with 3+ characters
- [ ] Regex patterns have escaped `{` and valid escape sequences
- [ ] Condition starts with cheap checks (filesize, magic bytes)
- [ ] Rule matches all target samples
- [ ] Rule produces zero matches on goodware corpus
- [ ] `yr check` passes with no errors
- [ ] `yr fmt --check` passes (consistent formatting)
- [ ] Linter passes with no errors
- [ ] Peer review completed

## Resources

### Quality YARA Rule Repositories

Learn from production rules. These repositories contain well-tested, properly attributed rules:

| Repository | Focus | Maintainer |
|------------|-------|------------|
| [Neo23x0/signature-base](https://github.com/Neo23x0/signature-base) | 17,000+ production rules, multi-platform | Florian Roth |
| [Elastic/protections-artifacts](https://github.com/elastic/protections-artifacts) | 1,000+ endpoint-tested rules | Elastic Security |
| [reversinglabs/reversinglabs-yara-rules](https://github.com/reversinglabs/reversinglabs-yara-rules) | Threat research rules | ReversingLabs |
| [imp0rtp3/js-yara-rules](https://github.com/imp0rtp3/js-yara-rules) | JavaScript/browser malware | imp0rtp3 |
| [InQuest/awesome-yara](https://github.com/InQuest/awesome-yara) | Curated index of resources | InQuest |

### Style & Performance Guides

| Guide | Purpose |
|-------|---------|
| [YARA Style Guide](https://github.com/Neo23x0/YARA-Style-Guide) | Naming conventions, metadata, string prefixes |
| [YARA Performance Guidelines](https://github.com/Neo23x0/YARA-Performance-Guidelines) | Atom optimization, regex bounds |
| [Kaspersky Applied YARA Training](https://yara.readthedocs.io/) | Expert techniques from production use |

### Tools

| Tool | Purpose |
|------|---------|
| [yarGen](https://github.com/Neo23x0/yarGen) | Extract candidate strings from samples |
| [FLOSS](https://github.com/mandiant/flare-floss) | Extract obfuscated and stack strings |
| [YARA-CI](https://yara-ci.cloud.virustotal.com/) | Automated goodware testing |
| [YaraDbg](https://yaradbg.dev) | Web-based rule debugger |

### macOS-Specific Resources

| Resource | Purpose |
|----------|---------|
| Apple XProtect | Production macOS rules at `/System/Library/CoreServices/XProtect.bundle/` |
| [objective-see](https://objective-see.org/) | macOS malware research and samples |
| [macOS Security Tools](https://github.com/0xmachos/macos-security-tools) | Reference list |

### Multi-Indicator Clustering Pattern

Production rules often group indicators by type:

```yara
strings:
    // Category A: Library indicators
    $a1 = "SRWebSocket" ascii
    $a2 = "SocketRocket" ascii

    // Category B: Behavioral indicators
    $b1 = "SSH tunnel" ascii
    $b2 = "keylogger" ascii nocase

    // Category C: C2 patterns
    $c1 = /https:\/\/[a-z0-9]{8,16}\.onion/

condition:
    filesize < 10MB and
    any of ($a*) and any of ($b*)  // Require evidence from BOTH categories
```

**Why this works:** Different indicator types have different confidence levels. A single C2 domain might be definitive, while you need multiple library imports to be confident. Grouping by `$a*`, `$b*`, `$c*` lets you express graduated requirements.

---

## Reference: Crx Module

# YARA-X CRX Module Reference

The `crx` module enables analysis of Chrome extension packages (CRX files). Use it to detect malicious extensions based on their declared permissions, manifest structure, and metadata.

**Version requirements:** YARA-X v1.5.0+

## Module Import

```yara
import "crx"
```

## API Reference

### File Type Validation

| Field | Type | Description |
|-------|------|-------------|
| `crx.is_crx` | bool | Returns true if file is a valid CRX package |

**Always check `crx.is_crx` first.** The module's other fields will not work correctly on non-CRX files.

### Extension Metadata

| Field | Type | Description |
|-------|------|-------------|
| `crx.id` | string | Extension identifier |
| `crx.version` | string | Extension version string |
| `crx.name` | string | Extension display name (localized) |
| `crx.description` | string | Extension description (localized) |
| `crx.raw_name` | string | Extension name without localization |
| `crx.raw_description` | string | Extension description without localization |
| `crx.homepage_url` | string | Extension homepage URL |

### CRX Format Information

| Field | Type | Description |
|-------|------|-------------|
| `crx.crx_version` | integer | CRX format version (2 or 3) |
| `crx.header_size` | integer | Size of the CRX header in bytes |

### Permission Analysis

| Field | Description | Example |
|-------|-------------|---------|
| `crx.permissions` | Array of declared permissions | `for any perm in crx.permissions` |
| `crx.optional_permissions` | Array of optional permissions | `for any perm in crx.optional_permissions` |
| `crx.host_permissions` | Array of host patterns (MV3) | `for any host in crx.host_permissions` |
| `crx.optional_host_permissions` | Array of optional host patterns | `for any host in crx.optional_host_permissions` |

### Signature Verification

| Field | Type | Description |
|-------|------|-------------|
| `crx.signatures` | array | Array of signature objects |
| `crx.signatures[i].key` | string | Public key for this signature |
| `crx.signatures[i].verified` | bool | Whether signature verification passed |

```yara
// Check if extension has a verified signature
rule CRX_VerifiedSignature
{
    condition:
        crx.is_crx and
        for any sig in crx.signatures : (sig.verified)
}
```

## Permission Risk Assessment

### High-Risk Permissions

These permissions enable significant access and should trigger careful review:

| Permission | Risk | Legitimate Uses |
|------------|------|-----------------|
| `debugger` | Can intercept all traffic, modify any page | DevTools extensions |
| `nativeMessaging` | Communicate with local executables | Password managers, native integrations |
| `<all_urls>` | Access all websites | Ad blockers, universal tools |
| `proxy` | Route all traffic through specified proxy | VPN extensions |
| `webRequest` + `webRequestBlocking` | Intercept/modify requests | Ad blockers, privacy tools |
| `cookies` (with broad hosts) | Access authentication tokens | Session managers |
| `history` | Read complete browsing history | Productivity trackers |

### Red Flag Combinations

These permission combinations are especially suspicious:

```yara
// Data exfiltration potential
condition:
    crx.is_crx and
    for any perm in crx.permissions : (perm == "nativeMessaging") and
    for any perm in crx.permissions : (perm == "<all_urls>" or perm == "*://*/*")

// Credential theft potential
condition:
    crx.is_crx and
    for any perm in crx.permissions : (perm == "webRequest") and
    for any perm in crx.permissions : (perm == "webRequestBlocking") and
    for any host in crx.host_permissions : (host contains "://*/*")

// Man-in-the-browser potential
condition:
    crx.is_crx and
    for any perm in crx.permissions : (perm == "debugger") and
    for any perm in crx.permissions : (perm == "tabs")
```

## Example Rules

### Detect High-Risk Extension

```yara
import "crx"

rule SUSP_CRX_HighRiskProfile
{
    meta:
        description = "Detects extensions with high-risk permission combinations"
        score = 70

    condition:
        crx.is_crx and

        // Count dangerous permissions
        (
            (for any p in crx.permissions : (p == "debugger")) +
            (for any p in crx.permissions : (p == "nativeMessaging")) +
            (for any p in crx.permissions : (p == "proxy")) +
            (for any p in crx.permissions : (p == "webRequestBlocking"))
        ) >= 2 and

        // Has broad host access
        for any h in crx.host_permissions : (
            h == "<all_urls>" or h contains "://*/*"
        )
}
```

### Detect Unverified Signatures

```yara
import "crx"

rule SUSP_CRX_UnverifiedSignature
{
    meta:
        description = "Detects CRX files with unverified or missing signatures"
        score = 60

    condition:
        crx.is_crx and
        not for any sig in crx.signatures : (sig.verified)
}
```

### Combine with String Patterns

```yara
import "crx"

rule SUSP_CRX_CryptoMiner
{
    meta:
        description = "Detects potential cryptomining extensions"
        score = 80

    strings:
        $miner1 = "CoinHive" ascii wide nocase
        $miner2 = "coinhive.min.js" ascii
        $miner3 = /Miner\.(start|stop)\s*\(/
        $wasm_miner = "cryptonight" ascii
        $pool_stratum = /stratum\+tcp:\/\//

    condition:
        crx.is_crx and

        // Needs background execution
        for any perm in crx.permissions : (
            perm == "background" or perm == "alarms"
        ) and

        // Miner indicators
        (2 of ($miner*) or $wasm_miner or $pool_stratum)
}
```

## Best Practices

1. **Always validate file type first** — Start conditions with `crx.is_crx`

2. **Don't over-match on common permissions** — `storage`, `activeTab`, `tabs` are used by most extensions

3. **Combine permissions with behavioral indicators** — Permission + suspicious string pattern is stronger than permission alone

4. **Use signatures for hunting** — Extensions with unverified signatures are worth investigating

5. **Test against legitimate extensions** — Chrome Web Store top extensions are your goodware corpus

## Troubleshooting

**Rule doesn't match CRX files:**
- Verify the file is a valid CRX (not just a renamed ZIP)
- Check YARA-X version (`yr --version`) meets requirements
- Use `yr dump -m crx extension.crx` to inspect what the module sees

**Permission iteration not working:**
- Ensure proper syntax: `for any perm in crx.permissions : (perm == "...")`
- Permissions are strings, not identifiers

**Signature verification questions:**
- `crx.signatures` may be empty for unsigned extensions
- CRX v2 uses RSA signatures; CRX v3 uses ECDSA

---

## Reference: Dex Module

# YARA-X DEX Module Reference

The `dex` module enables analysis of Android Dalvik Executable (DEX) files. Use it to detect Android malware based on class structure, method signatures, string content, and obfuscation patterns.

**Version requirements:** YARA-X v1.11.0+

**Important:** The YARA-X `dex` module is **not compatible** with legacy YARA's `dex` module. The API is completely different. Rules must be rewritten.

## Module Import

```yara
import "dex"
```

## API Reference

### File Type Validation

| Field | Type | Description |
|-------|------|-------------|
| `dex.is_dex` | bool | Returns true if file is valid DEX |

**Always check `dex.is_dex` first.** Other fields will not work correctly on non-DEX files.

### Header Information

Access via `dex.header.*`:

| Field | Type | Description |
|-------|------|-------------|
| `dex.header.magic` | integer | DEX magic bytes (hex) |
| `dex.header.version` | integer | DEX version (35, 36, 37, ...) |
| `dex.header.checksum` | integer | Adler32 checksum from header (hex) |
| `dex.header.signature` | string | SHA-1 hash from header |
| `dex.header.file_size` | integer | Total file size in bytes |
| `dex.header.header_size` | integer | Header size (hex, usually 0x70) |
| `dex.header.endian_tag` | integer | Endianness indicator (hex) |
| `dex.header.link_size` | integer | Link section size |
| `dex.header.link_off` | integer | Link section offset (hex) |
| `dex.header.data_size` | integer | Data section size |
| `dex.header.data_off` | integer | Data section offset (hex) |

### Collections

| Field | Type | Description |
|-------|------|-------------|
| `dex.strings` | string[] | Array of all strings in DEX |
| `dex.types` | string[] | Array of type descriptors |
| `dex.protos` | array | Array of method prototypes |
| `dex.fields` | array | Array of field definitions |
| `dex.methods` | array | Array of method definitions |
| `dex.class_defs` | array | Array of class definitions |

### Method Item Structure

Each item in `dex.methods`:

| Field | Type | Description |
|-------|------|-------------|
| `class` | string | Owning class name |
| `name` | string | Method name |
| `proto.shorty` | string | Short-form method signature |
| `proto.return_type` | string | Return type descriptor |
| `proto.parameters_count` | integer | Number of parameters |
| `proto.parameters` | string[] | Parameter type descriptors |

### Class Definition Structure

Each item in `dex.class_defs`:

| Field | Type | Description |
|-------|------|-------------|
| `class` | string | Fully qualified class name |
| `access_flags` | integer | Class access modifiers |
| `superclass` | string | Parent class name |
| `source_file` | string | Source file name (if present) |

### Convenience Functions

These functions search across all entries efficiently using binary search:

| Function | Description | Example |
|----------|-------------|---------|
| `dex.contains_string(pattern)` | Check if any string matches | `dex.contains_string("decrypt")` |
| `dex.contains_method(pattern)` | Check if any method name matches | `dex.contains_method("loadClass")` |
| `dex.contains_class(pattern)` | Check if any class matches | `dex.contains_class("Ldalvik/system/DexClassLoader;")` |

### Integrity Functions

| Function | Description |
|----------|-------------|
| `dex.checksum()` | Compute actual Adler32 checksum (compare with `dex.header.checksum`) |
| `dex.signature()` | Compute actual SHA-1 signature (compare with `dex.header.signature`) |

```yara
// Detect tampered DEX files
rule SUSP_DEX_ChecksumMismatch
{
    condition:
        dex.is_dex and
        dex.checksum() != dex.header.checksum
}
```

## Obfuscation Detection

### Single-Letter Class Names

Heavy obfuscation often produces single-letter class/package names:

```yara
import "dex"

rule SUSP_DEX_HeavyObfuscation
{
    meta:
        description = "Detects DEX with likely ProGuard/R8 aggressive obfuscation"

    condition:
        dex.is_dex and

        // Count classes with single-letter names
        for 10 c in dex.class_defs : (
            c.class matches /^L[a-z]\/[a-z]\/[a-z];$/
        )
}
```

### Missing Source File Info

Legitimate apps usually preserve source file names for crash reports:

```yara
rule SUSP_DEX_StrippedDebugInfo
{
    meta:
        description = "DEX has no source file information - unusual for production apps"

    condition:
        dex.is_dex and

        // No class has source file info
        for all c in dex.class_defs : (
            c.source_file == ""
        )
}
```

### String Encryption Detection

Malware often encrypts strings to evade static analysis:

```yara
rule SUSP_DEX_StringDecryption
{
    meta:
        description = "Detects common string decryption patterns in Android malware"

    condition:
        dex.is_dex and

        // Look for decryption method patterns
        (
            dex.contains_method("decrypt") or
            dex.contains_method("deobfuscate")
        ) and

        // Combined with XOR or Base64 indicators
        dex.contains_string("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
}
```

## Common Malware Patterns

### Reflection-Based Loading

Malware uses reflection to load code dynamically:

```yara
import "dex"

rule SUSP_DEX_ReflectionLoading
{
    meta:
        description = "Detects dynamic class loading via reflection"

    condition:
        dex.is_dex and

        // DexClassLoader or PathClassLoader usage
        (
            dex.contains_class("Ldalvik/system/DexClassLoader;") or
            dex.contains_class("Ldalvik/system/PathClassLoader;") or
            dex.contains_class("Ldalvik/system/InMemoryDexClassLoader;")
        ) and

        // Combined with reflection
        (
            dex.contains_method("loadClass") or
            dex.contains_method("forName")
        )
}
```

### SMS/Call Interception

Banking trojans commonly intercept SMS for 2FA bypass:

```yara
import "dex"

rule MAL_DEX_SMSInterception
{
    meta:
        description = "Detects SMS interception capabilities"
        score = 70

    condition:
        dex.is_dex and

        // SMS receiver registration
        dex.contains_string("android.provider.Telephony.SMS_RECEIVED") and

        // SMS content access
        (
            dex.contains_string("content://sms") or
            dex.contains_method("getMessageBody")
        ) and

        // Network exfiltration
        (
            dex.contains_class("Ljava/net/HttpURLConnection;") or
            dex.contains_class("Lokhttp3/OkHttpClient;")
        )
}
```

### Accessibility Service Abuse

Malware abuses accessibility for overlay attacks:

```yara
import "dex"

rule SUSP_DEX_AccessibilityAbuse
{
    meta:
        description = "Detects potential accessibility service abuse for overlay attacks"

    condition:
        dex.is_dex and

        // AccessibilityService implementation
        for any c in dex.class_defs : (
            c.superclass contains "AccessibilityService"
        ) and

        // Window overlay
        (
            dex.contains_string("android.permission.SYSTEM_ALERT_WINDOW") or
            dex.contains_string("TYPE_APPLICATION_OVERLAY")
        ) and

        // Combined with sensitive actions
        (
            dex.contains_string("performGlobalAction") or
            dex.contains_method("dispatchGesture")
        )
}
```

## Example Rules

### Banking Trojan Detection

```yara
import "dex"

rule MAL_DEX_BankingTrojan
{
    meta:
        description = "Detects common banking trojan patterns"
        score = 80

    strings:
        // Overlay injection strings
        $overlay1 = "android.app.action.ADD_DEVICE_ADMIN" ascii
        $overlay2 = "BIND_ACCESSIBILITY_SERVICE" ascii

        // Target banking app packages
        $bank1 = "com.chase.sig.android" ascii
        $bank2 = "com.wellsfargo.mobile" ascii
        $bank3 = "com.bankofamerica" ascii

    condition:
        dex.is_dex and

        // Has accessibility abuse potential
        for any c in dex.class_defs : (
            c.superclass contains "AccessibilityService"
        ) and

        // Overlay indicators
        any of ($overlay*) and

        // Targets specific banks (reduce FPs)
        any of ($bank*) and

        // Network capability
        (
            dex.contains_class("Lokhttp3/") or
            dex.contains_class("Ljava/net/HttpURLConnection;")
        )
}
```

### RAT Detection

```yara
import "dex"

rule MAL_DEX_RemoteAccessTrojan
{
    meta:
        description = "Detects Android RAT capabilities"
        score = 85

    condition:
        dex.is_dex and

        // Camera/mic access
        (
            dex.contains_string("android.permission.CAMERA") and
            dex.contains_string("android.permission.RECORD_AUDIO")
        ) and

        // Location tracking
        dex.contains_string("android.permission.ACCESS_FINE_LOCATION") and

        // Command channel
        (
            dex.contains_string("socket") or
            dex.contains_class("Ljava/net/Socket;")
        ) and

        // File exfiltration
        (
            dex.contains_method("getExternalStorage") or
            dex.contains_string("/sdcard/")
        )
}
```

## Best Practices

1. **Always validate file type first** — Start with `dex.is_dex`

2. **Use `contains_*()` functions** — They use binary search and are optimized

3. **Combine class/method patterns** — Single indicators are weak; combinations are stronger

4. **Account for obfuscation** — Class names may be mangled; look for method behaviors

5. **Test on legitimate apps** — Top Play Store apps are your goodware corpus

6. **Consider multi-dex** — Large apps split into multiple DEX files; scan all

## Troubleshooting

**Rule doesn't match DEX files:**
- Verify the file is valid DEX (`file sample.dex` should show "Dalvik dex file")
- Check YARA-X version is v1.11.0+
- Use `yr dump -m dex sample.dex` to inspect module output

**contains_* functions not working:**
- Requires YARA-X v1.11.0+
- String patterns are case-sensitive by default
- Use exact class names with L prefix and ; suffix: `Lcom/example/Class;`

**Migrating from legacy YARA dex module:**
- APIs are completely different — rewrite is required
- Legacy: `dex.has_class("...")` → YARA-X: `dex.contains_class("...")`
- Legacy field names differ from YARA-X field names

---

## Reference: Performance

# YARA-X Performance Guidelines

Understanding how YARA-X works internally helps you write rules that scan fast.

> **YARA-X Performance:** YARA-X is 5-10x faster than legacy YARA for regex-heavy rules due to its Rust-based regex engine. The atom extraction and matching principles remain the same.

## How YARA Scanning Works

### Three-Phase Process

1. **Atom Extraction** — YARA extracts short byte sequences (atoms) from your strings
2. **Aho-Corasick Matching** — Fast multi-pattern search finds atom occurrences
3. **Bytecode Verification** — For each atom hit, verify the full string/condition

The key insight: **Phase 2 is fast, Phase 3 is slow.** Poor atoms cause excessive Phase 3 verification.

### What Makes a Good Atom

YARA extracts 4-byte atoms from your strings. The best atoms are:

- **Rare in target files** — Unique byte sequences
- **Unambiguous** — No wildcards in the 4-byte window
- **Not in common data** — Avoid patterns found in every PE

```
String: "MalwareConfig"
Atom:   "Malw" (bytes 0-3)

String: { 4D 5A ?? ?? 50 45 }
Atom:   { 50 45 ?? ?? } — wildcards limit options
```

## Slow Pattern Killers

### Short Strings (< 4 bytes)

```yara
// TERRIBLE: No valid 4-byte atom
$bad = "abc"        // Only 3 bytes
$bad = { 4D 5A }    // Only 2 bytes

// GOOD: Full atoms available
$good = "abcdef"
$good = { 4D 5A 90 00 50 45 }
```

Short strings force YARA to check every file, defeating the Aho-Corasick optimization.

### Repeated Byte Patterns

```yara
// SLOW: Atom "0000" matches constantly
$nops = { 90 90 90 90 90 90 }  // NOP sled
$null = { 00 00 00 00 }         // Null bytes

// BETTER: Add context
$nop_context = { E8 ?? ?? ?? ?? 90 90 90 90 }  // Call followed by NOPs
```

### Unbounded Regex

```yara
// CATASTROPHIC: Backtracking explosion
$url = /https?:\/\/.*/

// SLOW: Still too broad
$url = /https?:\/\/[^\s]+/

// ACCEPTABLE: Bounded
$url = /https?:\/\/[a-z0-9\.\-]{5,50}\/[a-z0-9\/]{1,100}/
```

### Leading Wildcards

```yara
// SLOW: No stable atom at start
$bad = { ?? ?? 4D 5A 90 00 }

// FAST: Stable bytes first
$good = { 4D 5A 90 00 ?? ?? }
```

### Common Byte Sequences

```yara
// SLOW: Found in most PE files
$pe_header = { 4D 5A }         // MZ
$dos_stub = "This program"     // DOS stub message

// BETTER: Add unique context
$pe_anomaly = { 4D 5A 00 00 00 00 00 00 }  // Unusual null-padded MZ
```

## Optimization Techniques

### Short-Circuit with Cheap Checks

Order conditions from cheapest to most expensive:

```yara
condition:
    // 1. Instant: filesize check
    filesize < 10MB and

    // 2. Near-instant: magic bytes
    uint16(0) == 0x5A4D and

    // 3. Fast: string matches (if good atoms)
    all of ($strings_*) and

    // 4. Moderate: module imports
    pe.imports("kernel32.dll", "VirtualAlloc") and

    // 5. Slow: expensive computations
    pe.imphash() == "abc123..."
```

If the cheap check fails, expensive checks never run.

**Platform adaptation:**

| Platform | Short-circuit pattern |
|----------|----------------------|
| **PE files** | `filesize < 10MB and uint16(0) == 0x5A4D and ...` |
| **JavaScript** | `filesize < 1MB and ...` (no magic bytes, JS files are text) |
| **npm packages** | Check for `"name":` or `package.json` content first |
| **Office docs (OOXML)** | `filesize < 50MB and uint32(0) == 0x504B0304 and ...` |
| **Chrome extensions** | `crx.is_crx and ...` (use crx module) |
| **Android apps** | `dex.header.magic == "dex\n" and ...` (use dex module) |

### Use `for..of` Efficiently

```yara
// SLOW: Checks all strings even after match
any of them

// FAST: Short-circuits after first match
for any of them : ( $ )

// OPTIMIZED: With early exit
for any i in (0..#s1) : ( @s1[i] < 1000 )
```

### Prefer `in` Over Position Calculations

```yara
// SLOWER: Arithmetic
$header at pe.entry_point + 100

// FASTER: Range check
$header in (pe.entry_point..pe.entry_point + 200)
```

### Avoid Module Overhead When Possible

```yara
// EXPENSIVE: Loads PE module
pe.entry_point

// CHEAP: Direct byte access
uint32(uint32(0x3C) + 0x28)  // Entry point from PE header
```

Use modules when you need complex analysis, but simple byte checks are faster.

### Bounded Regex Patterns

```yara
// BAD
$url = /https?:\/\/[^\s]*/

// GOOD: Explicit length bounds
$url = /https?:\/\/[a-z0-9\.\-]{5,50}\//

// BETTER: Fixed prefix for better atom
$url = /https:\/\/api\.[a-z]{5,20}\.com\//
```

### Regex Performance Rules

**Expert guidance:** Anchor every regex to a string atom. Unanchored regex consumes memory proportional to file size.

```yara
// CATASTROPHIC: Runs against every byte, unbounded backtracking
$bad = /eval\(.*\)/

// SLOW: Still unbounded despite negated class
$bad = /eval\([^\)]+\)/

// GOOD: Bounded, controlled, anchored to "eval"
$good = /eval\s*\(\s*(atob|unescape)\s*\(/ nocase
```

**Rule of thumb:** If your regex doesn't have a literal string of 4+ characters that YARA can extract as an atom, it will be slow. The atom determines which files get checked.

```yara
// NO ATOM: Entirely character classes
$no_atom = /[a-z]+\.[a-z]+\([^)]*\)/

// HAS ATOM: "fetch" is extracted, limits files checked
$has_atom = /fetch\s*\(\s*['"][^'"]{1,100}['"]\s*\)/
```

**Controlled ranges table:**

| Pattern | Performance | Use Case |
|---------|-------------|----------|
| `.*` | Catastrophic | Never use |
| `.+` | Catastrophic | Never use |
| `[^x]*` | Slow | Avoid |
| `.{0,30}` | Good | Short variable content |
| `.{0,100}` | Acceptable | Longer bounded content |
| `[a-z]{5,20}` | Best | Known character set + length |

### Use `fullword` for Word Boundaries

```yara
// May match "MalwareAnalysis" in middle of binary
$s = "Malware"

// Only matches isolated word
$s = "Malware" fullword
```

## Module Usage Guidelines

### Expensive Operations

| Operation | Cost | Alternative |
|-----------|------|-------------|
| `pe.imphash()` | High | Pre-filter with uint16(0) == 0x5A4D |
| `hash.md5()` | Very High | Use for small files only |
| `pe.rich_header` | Moderate | Pre-filter with filesize |
| `math.entropy()` | High | Use for specific sections only |

### Pre-Filter Before Modules

```yara
import "pe"
import "hash"

rule Example
{
    condition:
        // Pre-filters (instant)
        filesize > 1KB and
        filesize < 5MB and
        uint16(0) == 0x5A4D and

        // Now safe to use expensive checks
        pe.number_of_sections > 3 and
        hash.md5(0, filesize) == "abc123..."
}
```

## Measuring Performance

### YARA-X Profiling

```bash
# Time rule execution
time yr scan rules/ /path/to/files/

# Count matches without output
yr scan -c rules/ /path/to/files/
```

### Rule-by-Rule Analysis

Test individual rules against a corpus:

```bash
for rule in rules/*.yar; do
    echo "Testing: $rule"
    time yr scan "$rule" /corpus/ > /dev/null
done
```

### String Quality Check

Use the atom analyzer script:

```bash
uv run {baseDir}/scripts/atom_analyzer.py rule.yar
```

## Real-World Examples

### Before Optimization

```yara
rule Slow_Example
{
    strings:
        $s1 = "exe"                          // 3 bytes
        $s2 = { 00 00 00 00 }                // Common nulls
        $url = /.*/                          // Unbounded

    condition:
        pe.imphash() == "abc123" and         // Expensive first
        any of them
}
```

### After Optimization

```yara
rule Fast_Example
{
    strings:
        $s1 = "malware.exe" fullword         // 11 bytes, unique
        $s2 = { 43 4F 4E 46 00 00 00 00 }    // "CONF" + nulls
        $url = /https:\/\/[a-z]{5,20}\.com/  // Bounded

    condition:
        filesize < 10MB and                  // Instant
        uint16(0) == 0x5A4D and              // Instant
        2 of ($s*) and                       // Fast strings
        pe.imphash() == "abc123"             // Expensive last
}
```

## Checklist

Before deploying rules:

- [ ] No strings under 4 bytes
- [ ] No unbounded regex (`.*`, `.+`, `[^x]*`)
- [ ] No repeated byte patterns without context
- [ ] Conditions ordered: cheap → expensive
- [ ] Module checks pre-filtered with magic bytes/filesize
- [ ] Tested against large corpus for timing
- [ ] Atom analyzer shows no warnings

---

## Reference: Strings

# YARA-X String Selection

Choosing the right strings is the most critical decision in YARA rule writing.

> **YARA-X Note:** YARA-X enforces stricter validation on strings. Base64 modifier requires 3+ character strings, and regex patterns must have properly escaped metacharacters.

## String Quality Judgment

Before using any string, run through this mental checklist:

```
Is this string good enough?
├─ At least 4 bytes? (minimum for useful atoms)
├─ Contains 4 consecutive unique bytes? (not 0000, 9090, FFFF)
├─ NOT an API name? (VirtualAlloc, CreateRemoteThread = reject)
├─ NOT a common path? (C:\Windows\, cmd.exe = reject)
├─ NOT a format string? (%s, %d, Error: %s = reject)
├─ Would match in Windows system files? (if yes = reject)
├─ Specific to this malware family? (if yes = use it)
└─ Found in other malware too? (combine with unique marker)
```

## High-Value String Sources

**Gold tier** — Almost always unique:
- Mutex names: `"Global\\MyMalwareMutex"`
- Stack strings (decoded at runtime)
- PDB paths: `"C:\\Users\\dev\\malware.pdb"`

**Silver tier** — Usually unique:
- C2 paths: `"/api/beacon/check"`
- Configuration markers: `"CONFIG_START"`
- Custom protocol headers: `"BEACON_1.0"`

**Bronze tier** — Unique with context:
- Unique error messages: `"Failed to inject into explorer"`
- Campaign IDs: `"OPERATION_X"`

## String Types

### Text Strings

```yara
$text = "Hello World"              // Basic ASCII
$text_wide = "Hello" wide          // UTF-16LE (Windows Unicode)
$text_both = "Hello" ascii wide    // Match either encoding
$text_nocase = "hello" nocase      // Case-insensitive (performance cost)
$text_full = "hello" fullword      // Word boundaries only
```

### Hex Strings

```yara
$hex = { 4D 5A 90 00 }             // Exact bytes
$wild = { 4D 5A ?? ?? }            // Single-byte wildcards
$jump = { 4D 5A [2-4] 50 45 }      // Variable-length jump (bounded!)
$alt = { 4D 5A ( 90 00 | 00 00 ) } // Alternatives
```

### Regular Expressions

```yara
// ALWAYS bound your regex
$url = /https?:\/\/[a-z0-9]{5,50}\.onion/    // Good: bounded
$bad = /https?:\/\/.*/                        // BAD: unbounded
```

**YARA-X regex requirements:**
- Literal `{` must be escaped as `\{` (YARA-X strict mode)
- Invalid escape sequences error instead of becoming literals
- Use `yr check` to validate regex patterns before deployment

```yara
// BAD: Fails in YARA-X
$pattern = /config{key}/

// GOOD: Escape the brace
$pattern = /config\{key\}/
```

## Modifiers and Their Costs

| Modifier | Performance Impact | When to Use |
|----------|-------------------|-------------|
| `ascii` | None | Default, always included |
| `wide` | Minimal | Windows Unicode strings |
| `nocase` | **Doubles atoms** | Only when necessary |
| `fullword` | Minimal | Prevent substring matches |
| `xor` | **High (255x patterns)** | Only with specific range |
| `base64` | Moderate (3x patterns) | Encoded payloads (**3+ chars required in YARA-X**) |
| `private` | None | Hide pattern from scan output (YARA-X 1.3.0+) |

**Modifier judgment:**
- `nocase` — Only use for user-facing strings that might vary in case
- `xor(0x00-0xFF)` — Almost always too broad; find the actual key
- `xor(0x41)` — Specific key is acceptable
- `base64` — YARA-X requires strings of 3+ characters (won't match on shorter strings)

### Private Patterns (YARA-X 1.3.0+)

Mark helper patterns as private to exclude them from scan output:

```yara
strings:
    $public = "malware_marker"
    private $helper = "internal_pattern"  // Matches but not in output

condition:
    $public and $helper
```

## Bad String Sources (Always Reject)

### API Names

Every Windows program uses these:

```yara
// REJECT: Found in all executables
$bad = "VirtualAlloc"
$bad = "CreateRemoteThread"
$bad = "WriteProcessMemory"
$bad = "NtCreateThreadEx"
```

**Expert response:** Use hex pattern of the call site, not the import name.

### Common Paths

```yara
// REJECT: Found everywhere
$bad = "C:\\Windows\\System32"
$bad = "cmd.exe"
$bad = "powershell.exe"
$bad = "\\AppData\\Local"
```

**Expert response:** Find malware-specific full paths.

### Format Strings

```yara
// REJECT: Every C program
$bad = "%s"
$bad = "%d"
$bad = "Error: %s"
```

**Expert response:** Find unique format strings: `"Beacon initialized: %s:%d with key %08X"`

### Common Libraries

```yara
// REJECT: Every Windows program
$bad = "KERNEL32.dll"
$bad = "ntdll.dll"
$bad = "USER32.dll"
```

### JavaScript Framework Patterns

```yara
// REJECT: Every Node.js application
$bad = "require("
$bad = "fs.readFile"
$bad = "child_process"
$bad = "process.env"
$bad = "fetch("
$bad = "axios"
```

**Expert response:** Combine with suspicious context:

```yara
// child_process alone = every CLI tool
// child_process + base64 decode + network fetch = suspicious
strings:
    $exec = /child_process['"]\s*\)\.exec/
    $decode = /atob\s*\(|Buffer\.from\s*\([^)]+,\s*['"]base64/
    $exfil = /discord\.com\/api|telegram\.org\/bot/

condition:
    $exec and $decode and $exfil
```

## Stack Strings Pattern

Malware often builds strings on the stack to evade static analysis. These are almost always unique:

```yara
// Looking for stack-built "cmd.exe"
$stack_cmd = {
    C6 45 ?? 63    // mov byte ptr [ebp+?], 'c'
    C6 45 ?? 6D    // mov byte ptr [ebp+?], 'm'
    C6 45 ?? 64    // mov byte ptr [ebp+?], 'd'
    C6 45 ?? 2E    // mov byte ptr [ebp+?], '.'
    C6 45 ?? 65    // mov byte ptr [ebp+?], 'e'
    C6 45 ?? 78    // mov byte ptr [ebp+?], 'x'
    C6 45 ?? 65    // mov byte ptr [ebp+?], 'e'
}
```

**Expert heuristic:** If yarGen returns only API names, look for stack strings — the sample likely decodes sensitive strings at runtime.

## Hex String Best Practices

### Wildcards

```yara
// Single byte wildcard
{ 4D 5A ?? 00 }

// Nibble wildcard (half byte)
{ 4D 5? }              // Matches 4D 50 through 4D 5F

// BOUNDED jumps only
{ 4D 5A [2-4] 50 45 }  // 2-4 bytes between MZ and PE

// NEVER unbounded
{ 4D 5A [-] 50 45 }    // REJECT: unlimited = slow
```

### Leading Bytes Matter

```yara
// BAD: No stable atom at start
{ ?? ?? 4D 5A 90 00 }

// GOOD: Stable bytes first
{ 4D 5A 90 00 ?? ?? }
```

The first 4 bytes determine atom quality. Put your unique bytes there.

## Combining Strings Effectively

### Group by Purpose

```yara
strings:
    // Core identification (all required)
    $mutex = "Global\\MyMutex"
    $config = { 43 4F 4E 46 49 47 }

    // C2 indicators (any one)
    $c2_1 = "/api/beacon"
    $c2_2 = "/check_in"

condition:
    all of ($mutex, $config) and
    any of ($c2_*)
```

### False Positive Exclusions

```yara
strings:
    $malware = "SuspiciousString"
    $fp_legitimate = "Legitimate Vendor Inc"

condition:
    $malware and not $fp_legitimate
```

## Using yarGen Effectively

yarGen extracts candidate strings, but you must validate:

```bash
python yarGen.py -m /path/to/samples --excludegood
```

**Expert heuristic:** yarGen output needs 80% filtering. Most suggestions are:
- API names (reject)
- Common library strings (reject)
- Format strings (reject)
- Paths to common Windows directories (reject)

Keep only the unique mutex names, C2 paths, and configuration markers.

## JavaScript-Specific Patterns

For JavaScript/TypeScript malware (npm packages, VS Code extensions, browser extensions):

### Obfuscator Signatures

```yara
// javascript-obfuscator tool signature (hex variable names)
$hex_var = /_0x[a-fA-F0-9]{4,}/

// String.fromCharCode chains (hiding strings)
$fromcharcode = /String\.fromCharCode\s*\(\s*\d+(\s*,\s*\d+){5,}\)/

// Bracket notation chains (property access obfuscation)
$bracket_chain = /\[['"][a-zA-Z]+['"]\]\s*\[['"][a-zA-Z]+['"]\]\s*\[['"][a-zA-Z]+['"]\]/

// atob/btoa with concatenation (base64 evasion)
$atob_concat = /atob\s*\(\s*['"][^'"]+['"]\s*\+/
```

### Expert Patterns from Production Rules

These patterns come from Neo23x0 signature-base and Burp-Yara-Rules — battle-tested in production.

**javascript-obfuscator tool signature (Neo23x0):**

```yara
// Initialization pattern at file start
$init = "var a0_0x" at 0

// Infinite loop (self-defending code)
$loop = "while(!![])"

// Global scope access hack
$scope_hack = "{}.constructor(\"return this\")"

condition:
    $init at 0 or
    (filesize < 1MB and 3 of ($loop, $scope_hack, ...))
```

**Expert insight:** The `filesize < 1MB` constraint plus threshold (`3 of`) significantly reduces FPs.

**eval + decode combo (most common obfuscation):**

```yara
// nocase handles case variations in minified/obfuscated code
$eval_decode = /eval\s*\(\s*(unescape|atob)\s*\(/ nocase
$func_decode = /Function\s*\(\s*atob\s*\(/ nocase
```

**Hex-encoded string array:**

```yara
// Matches: var _0x1234 = ["\x48\x65\x6c\x6c\x6f", ...]
$hex_array = /var\s+\w+\s*=\s*\[\s*["']\\x[0-9a-fA-F]+/
```

### Invisible Unicode (Stealth)

Two Unicode ranges are commonly abused: standard Variation Selectors (U+FE00-FE0F) and Variation Selectors Supplement (U+E0100-E01EF). Detect both.

**Standard Variation Selectors (VS1-16):**

```yara
// UTF-8 variation selectors U+FE00-FE0F (invisible characters hiding code)
$vs_utf8 = { EF B8 (80|81|82|83|84|85|86|87|88|89|8A|8B|8C|8D|8E|8F) }

// Zero-width characters
$zwc = { E2 80 (8B|8C|8D|8E|8F|AA|AB|AC|AD|AE|AF) }

condition:
    #vs_utf8 > 5 and any of ($eval, $function)  // 5+ is suspicious per Veracode research
```

**Expert heuristic:** Legitimate i18n uses few variation selectors. 10+ in a JS file is suspicious.

### Unicode Steganography (Variation Selectors Supplement)

**Variation Selectors Supplement (U+E0100-E01EF):**

The `os-info-checker-es6` attack (2025) used this range — invisible nonspacing marks appended to visible characters with data encoded in the low byte.

**Byte pattern for detection:**

```yara
rule SUSP_JS_Unicode_Steganography
{
    strings:
        // UTF-8 encoding of Variation Selectors Supplement
        // U+E0100-E01EF encodes as: F3 A0 84 80 to F3 A0 87 AF
        $var_selectors = { F3 A0 (84|85|86|87) }
        $eval_decode = /eval\s*\(\s*atob\s*\(/

    condition:
        // 5+ variation selectors + eval/atob = highly suspicious
        // Legitimate i18n rarely uses these; 5+ is almost never accidental
        #var_selectors > 5 and $eval_decode
}
```

**Why this works:** Variation Selectors Supplement exists for specialized typography (CJK ideograph variants). JavaScript source code has no legitimate use for them. Any significant count combined with eval is malicious.

### Modern Exfiltration Channels

**Good indicators (specific, suspicious):**

```yara
$discord_webhook = /discord\.com\/api\/webhooks\/\d+\//
$telegram_bot = /api\.telegram\.org\/bot[0-9]+:[A-Za-z0-9_-]+/
$pastebin_raw = /pastebin\.com\/raw\//
$free_hosting = /(vercel\.app|netlify\.app|railway\.app|render\.com)\/api/
```

**Bad indicators (too common alone):**

```yara
// REJECT without additional context
$bad = "fetch("           // Every web app
$bad = "axios.post"       // Every API client
$bad = /https?:\/\//      // Every URL
```

**Combine for specificity:**

```yara
strings:
    $cred_path = /\.(npmrc|env|ssh\/id_rsa|aws\/credentials)/
    $read_file = /fs\.readFile|readFileSync/
    $discord = /discord\.com\/api\/webhooks/

condition:
    $cred_path and $read_file and $discord
```

### Credential Theft Patterns

```yara
// Browser credential databases
$chrome_login = "Login Data"
$firefox_logins = "logins.json"

// Config file paths
$npmrc = ".npmrc"
$ssh_key = /\.ssh\/(id_rsa|id_ed25519)/
$aws_creds = ".aws/credentials"
$env_file = /\.env(\.local)?/

// Combined with file read = suspicious
condition:
    any of ($chrome_*, $firefox_*, $npmrc, $ssh_*, $aws_*, $env_*) and
    any of ($read_file_*)
```

---

## Reference: Style Guide

# YARA Naming and Metadata

Consistent naming for maintainable rule sets.

## Naming Convention

```
{CATEGORY}_{PLATFORM}_{FAMILY}_{VARIANT}_{DATE}
```

| Component | Description | Examples |
|-----------|-------------|----------|
| CATEGORY | Threat classification | MAL, HKTL, WEBSHELL, EXPL, SUSP |
| PLATFORM | Target OS/environment | Win, Lnx, Mac, Android, Multi |
| FAMILY | Malware family name | Emotet, CobaltStrike, LockBit |
| VARIANT | Specific variant/component | Loader, Beacon, Config |
| DATE | Creation date (MonthYear format) | Jan25, May23 |

### Category Prefixes

| Prefix | Meaning | Use When |
|--------|---------|----------|
| `MAL_` | Confirmed malware | Verified malicious code |
| `HKTL_` | Hacking tool | Dual-use tools (Mimikatz, Cobalt Strike) |
| `WEBSHELL_` | Web shell | PHP/ASP/JSP backdoors |
| `EXPL_` | Exploit | Exploit code or shellcode |
| `VULN_` | Vulnerable | Vulnerable software patterns |
| `SUSP_` | Suspicious | Lower confidence, may FP |
| `PUA_` | Potentially unwanted | Adware, bundleware |
| `GEN_` | Generic | Broad detection category |

### Additional Classifiers

Append when relevant:

| Classifier | Meaning |
|------------|---------|
| `APT_` | APT-associated |
| `CRIME_` | Cybercrime operation |
| `RANSOM_` | Ransomware |
| `RAT_` | Remote access trojan |
| `MINER_` | Cryptominer |
| `STEALER_` | Information stealer |
| `LOADER_` | Loader/dropper |
| `C2_` | Command and control |

### Platform Indicators

| Indicator | Platform |
|-----------|----------|
| `Win_` | Windows |
| `Lnx_` | Linux |
| `Mac_` | macOS |
| `Android_` | Android |
| `iOS_` | iOS |
| `Multi_` | Cross-platform |
| `PE_` | PE file format |
| `ELF_` | ELF file format |
| `PS_` | PowerShell |
| `DOC_` | Office documents |
| `PDF_` | PDF files |
| `JAR_` | Java archives |

### Examples

```yara
// Good names (all include date suffix)
MAL_Win_Emotet_Loader_Jan25
HKTL_Win_CobaltStrike_Beacon_Jan25
WEBSHELL_PHP_Generic_Eval_Jan25
APT_Win_Lazarus_AppleJeus_Config_Jan25
RANSOM_Win_LockBit3_Decryptor_Jan25
SUSP_PE_Packed_UPX_Anomaly_Jan25

// Bad names
malware_detector              // Too vague
rule1                         // Meaningless
detect_bad_stuff              // Unprofessional
EMOTET_RULE                   // Missing category/platform/date
CobaltStrike_Beacon           // Missing category/date
```

## Metadata Requirements

### Required Fields

Every rule MUST have:

```yara
meta:
    description = "Detects X malware via Y unique feature"
    author = "Your Name <email@example.com>"  // OR "@twitter_handle"
    reference = "https://analysis-report-url.com"
    date = "2025-01-29"
```

### Description Guidelines

- **Start with "Detects"** — Consistent, scannable format
- **Length: 60-400 characters** — Brief but informative
- **Explain WHAT and HOW** — What it catches and the distinguishing feature

```yara
// Good descriptions
description = "Detects Emotet loader via unique XOR decryption routine and mutex pattern"
description = "Detects CobaltStrike beacon by watermark bytes in PE overlay"
description = "Detects generic PHP webshell using eval with base64_decode pattern"

// Bad descriptions
description = "Malware"                    // Too short
description = "This rule detects..."       // Redundant
description = "Catches bad stuff"          // Unprofessional
description = "Might be malware"           // Low confidence = use SUSP_ prefix
```

### Optional Fields

```yara
meta:
    // Sample identification (hash field can repeat)
    hash = "abc123def456..."               // SHA256 of reference sample
    hash = "789xyz..."                     // Additional samples (repeat field)

    // Confidence scoring
    score = 75                             // 0-100, use thresholds

    // Versioning
    modified = "2025-01-30"                // Last update date
    version = "1.2"                        // Rule version
    old_rule_name = "Previous_Rule_Name"   // For renamed rules (searchability)

    // Classification
    tags = "apt, lazarus, loader"          // Comma-separated
    tlp = "WHITE"                          // Traffic Light Protocol

    // MITRE ATT&CK
    mitre_attack = "T1055"                 // Technique ID
```

### Score Thresholds

| Score | Meaning | Action |
|-------|---------|--------|
| 0-25 | Low confidence | Hunting only, expect FPs |
| 26-50 | Medium | Investigate, don't auto-quarantine |
| 51-75 | High | Alert SOC, likely malicious |
| 76-100 | Critical | Auto-quarantine appropriate |

## Common Naming Mistakes

| Bad Name | Problem | Corrected |
|----------|---------|-----------|
| `Emotet_Detector` | Missing category, platform, date | `MAL_Win_Emotet_Loader_Jan25` |
| `MAL_Suspicious_File` | "Suspicious" is vague | `MAL_Win_Lazarus_Downloader_Jan25` |
| `rule1` | No semantic meaning | `HKTL_Multi_Mimikatz_CredDump_Jan25` |
| `MALWARE_windows_trojan` | Wrong case, wrong order | `MAL_Win_Trojan_Generic_Jan25` |
| `emotet_loader` | All lowercase | `MAL_Win_Emotet_Loader_Jan25` |
| `EmoteTLoader` | CamelCase | `MAL_Win_Emotet_Loader_Jan25` |
| `MAL Win Emotet` | Spaces | `MAL_Win_Emotet_Loader_Jan25` |
| `CobaltStrike_Beacon` | Missing category and date | `HKTL_Win_CobaltStrike_Beacon_Jan25` |

## Linter Error Codes

The `yara_lint.py` script produces these codes:

| Code | Severity | Issue | Fix |
|------|----------|-------|-----|
| E001 | Error | Missing required metadata | Add description, author, date, reference |
| E002 | Error | Invalid rule name format | Use CATEGORY_PLATFORM_FAMILY_DATE |
| E003 | Error | String under 4 bytes | Use longer strings or hex patterns |
| W001 | Warning | Name doesn't follow convention | Use standard prefix or justify custom |
| W002 | Warning | Description doesn't start with "Detects" | Rewrite description |
| W003 | Warning | Unbounded regex pattern | Add length bounds: `.{0,100}` not `.*` |
| W004 | Warning | Condition doesn't start with cheap check | Add `filesize <` or magic bytes first |
| I001 | Info | Unrecognized category prefix | Use standard prefix or document custom |
| I002 | Info | `nocase` modifier used | Consider if case variation is needed |

## PR Review Checklist

When reviewing YARA rules in PRs:

### Naming & Metadata
- [ ] Name matches `{CATEGORY}_{PLATFORM}_{FAMILY}_{DATE}` format
- [ ] Category prefix is from approved list (or justified)
- [ ] Description starts with "Detects" and is 60-400 chars
- [ ] Author includes contact (email or @handle)
- [ ] Reference URL is provided and accessible
- [ ] Date matches rule creation/modification date
- [ ] Hash field contains valid SHA256 of primary sample

### String Quality
- [ ] All strings ≥4 bytes
- [ ] No API names used as indicators
- [ ] No common paths or executables
- [ ] Regex patterns are bounded
- [ ] Base64 modifier only on 3+ char strings

### Condition Quality
- [ ] Starts with `filesize <` check
- [ ] Has magic bytes check before module use
- [ ] Uses `and` instead of implicit conjunction
- [ ] Expensive operations come last

### Testing Evidence
- [ ] Matches all target samples (list sample hashes)
- [ ] Zero matches on goodware corpus (state corpus tested)
- [ ] `yr check` passes
- [ ] `yr fmt --check` passes
- [ ] Linter passes

## Enforcing Style in CI

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: yara-lint
        name: YARA Lint
        entry: uv run yara_lint.py --strict
        language: system
        files: \.yar$
        types: [file]
```

### GitHub Actions

```yaml
- name: Lint YARA rules
  run: |
    uv run yara_lint.py --strict rules/
    yr check rules/
    yr fmt --check rules/
```

Block PRs that fail linting. No exceptions for "quick fixes."

## Anti-Patterns

### Naming

- All lowercase: `emotet_loader`
- CamelCase: `EmoteTLoader`
- No category: `Emotet_Jan25`
- Spaces or special chars: `MAL Win Emotet`
- Reserved words: `rule`, `strings`, `condition`

### Metadata

- Missing description
- Description doesn't start with "Detects"
- No author attribution
- No reference URL
- Outdated date (not updated when rule modified)

---

## Reference: Testing

# YARA-X Rule Testing

Testing is non-negotiable. Untested rules cause alert fatigue (false positives) or missed detections (false negatives).

## Testing Philosophy

Every rule needs three validation stages:

1. **Positive validation** — Matches all target samples
2. **Negative validation** — Zero matches on goodware
3. **Edge case validation** — Handles variants, packed versions, fragments

## Validation Workflow

```
┌──────────────────────┐
│ Write initial rule   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ yr check (validate)  │──── Fix issues ────┐
└──────────┬───────────┘                    │
           │                                │
           ▼                                │
┌──────────────────────┐                    │
│ Lint (style checks)  │──── Fix issues ────┤
└──────────┬───────────┘                    │
           │                                │
           ▼                                │
┌──────────────────────┐                    │
│ Test vs. samples     │──── Missing? ──────┤
└──────────┬───────────┘   (widen rule)     │
           │                                │
           ▼                                │
┌──────────────────────┐                    │
│ Test vs. goodware    │──── FPs? ──────────┤
└──────────┬───────────┘   (tighten rule)   │
           │                                │
           ▼                                │
┌──────────────────────┐                    │
│ Peer review          │──── Issues? ───────┘
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Deploy to production │
└──────────────────────┘
```

### Validation with yr check

Always validate rules before testing:

```bash
# Basic validation
yr check rule.yar

# Validate directory
yr check rules/

# Migration mode (identifies legacy YARA compatibility issues)
yr check --relaxed-re-syntax rules/
```

> **Note:** Use `--relaxed-re-syntax` only as a temporary diagnostic tool during migration.
> Fix all identified issues rather than relying on relaxed mode permanently.

YARA-X provides better error messages than legacy YARA, with precise source locations for issues.

## Goodware Testing

### Platform-Specific Goodware

Test against legitimate software in your target ecosystem, not just Windows binaries:

| Platform | Goodware Corpus |
|----------|-----------------|
| **PE files** | VirusTotal goodware, clean Windows installs |
| **JavaScript/Node** | Popular npm packages (lodash, react, express, axios) |
| **VS Code extensions** | Top 100 marketplace extensions by installs |
| **Browser extensions** | Chrome Web Store popular extensions |
| **npm packages** | Top 100+ packages by weekly downloads |
| **Python packages** | Top PyPI packages (requests, django, flask) |

**Critical:** A rule that fires on legitimate software in your target ecosystem is useless. VT's goodware corpus is PE-centric — supplement with ecosystem-appropriate files.

### Goodware Corpus Selection

Not all goodware is equal. Choose corpus that matches your rule's target:

| Rule Target | Minimum Goodware Corpus |
|-------------|------------------------|
| PE files | Chrome, Firefox, Adobe Reader, Microsoft Office, Python installer |
| JavaScript | lodash, react, express, webpack, electron |
| npm packages | Top 100 by weekly downloads + packages with postinstall scripts |
| Chrome extensions | Top 50 marketplace extensions |

**Expert baseline:** "Test against Chrome, Firefox, and Adobe Reader" — Kaspersky Applied YARA

### Interpreting Goodware Matches

```
Rule matched goodware — now what?
├─ Matched 1-2 files?
│  └─ Investigate: is the match legitimate? Add exclusion or tighten string
├─ Matched 3-5 files?
│  └─ Pattern is too common — find different indicators
├─ Matched 6+ files?
│  └─ Rule is fundamentally broken — start over
└─ Matched only one vendor's software?
   └─ Add vendor exclusion: `not $fp_vendor`
```

### VirusTotal Goodware Corpus (Recommended)

The gold standard. VirusTotal maintains a corpus of 1M+ clean files from major software vendors.

1. Upload your rule to [VirusTotal Intelligence](https://www.virustotal.com/gui/hunting)
2. Select "Goodware" corpus
3. Run retrohunt
4. Review any matches — each is a potential false positive

**Interpreting results:**

| Matches | Assessment | Action |
|---------|------------|--------|
| 0 | Excellent | Proceed to deployment |
| 1-2 | Investigate | Review matches, add exclusions or tighten strings |
| 3-5 | Too common | Find different indicators |
| 6+ | Broken | Start over with different indicators |

### Local Testing

```bash
# Should return zero matches
yr scan -r rules/ /path/to/goodware/

# Count matches (quiet mode)
yr scan -c rules/ /path/to/goodware/
```

### yarGen Database Lookup

Before deployment, check strings against yarGen's goodware database:

```bash
# Query strings against goodware database
python db-lookup.py -f strings.txt
```

Strings appearing in the database are likely to cause false positives.

### YARA-CI

[YARA-CI](https://yara-ci.cloud.virustotal.com/) provides cloud-based validation:

1. Connect GitHub repository
2. Each PR automatically tested
3. Reports syntax errors and performance issues
4. Integrates with VT goodware corpus

## Free Testing Alternatives

Not everyone has VirusTotal Intelligence access. Here are free alternatives:

### Free Online Tools

| Tool | Purpose | Access |
|------|---------|--------|
| **YARA-CI** | GitHub App tests PRs against 1M NIST goodware files | Free, [github.com/apps/virustotal-yara-ci](https://github.com/apps/virustotal-yara-ci) |
| **YaraDbg** | Web-based rule debugger with step-through execution | Free, [yaradbg.dev](https://yaradbg.dev) |
| **Klara** | Kaspersky's distributed YARA scanner | Open source, self-hosted |

### YARA-CI Setup

YARA-CI is the best free option for automated testing:

```bash
# 1. Install GitHub App from github.com/apps/virustotal-yara-ci
# 2. Connect your rules repository
# 3. Each PR automatically tested against 1M+ goodware files
# 4. View results at yara-ci.cloud.virustotal.com
```

Results include:
- Syntax validation
- Performance warnings
- Goodware matches (potential FPs)
- Slowloris detection (rules that timeout)

### Building a Local Goodware Corpus

For offline testing, build your own corpus:

**Windows PE files:**
```bash
# Fresh Windows 11 VM → export C:\Windows\System32\*.dll
# Download Chrome, Firefox, Adobe Reader installers
# Python/Node installers from official sources
```

**npm/JavaScript packages:**
```bash
# Download top packages
npm pack lodash react express axios webpack
# Extract for scanning
for f in *.tgz; do tar -xzf "$f"; done
```

**Chrome extensions:**
```bash
# Export installed extensions from chrome://extensions (Developer mode)
# Or download .crx files from Chrome Web Store using extension ID
```

**macOS applications:**
```bash
# Copy from /Applications/ on a fresh macOS install
# System binaries from /usr/bin/, /usr/sbin/
```

### NIST NSRL

The [NIST National Software Reference Library](https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl) provides hash sets of known-good files:

- **Size:** ~147GB compressed
- **Contains:** Hashes from legitimate software
- **Use:** Filter known-good files before scanning

```bash
# Download RDS (Reference Data Set)
# Available at: https://www.nist.gov/itl/ssd/software-quality-group/nsrl-download-links
# Use to exclude known-good files from your corpus
```

### macOS XProtect

Apple's built-in YARA rules are a good reference:

```bash
# Location on macOS
/System/Library/CoreServices/XProtect.bundle/Contents/Resources/XProtect.yara

# View rules (requires SIP disabled or extraction from DMG)
cat /System/Library/CoreServices/XProtect.bundle/Contents/Resources/XProtect.yara
```

XProtect rules demonstrate Apple's production patterns for macOS malware detection.

### Minimum Local Corpus by Platform

| Rule Target | Minimum Local Corpus |
|-------------|---------------------|
| PE files | Chrome.exe, Firefox.exe, python.exe (10+ files) |
| npm packages | lodash, react, express, webpack (top 50 by downloads) |
| Chrome extensions | uBlock Origin, React DevTools, Grammarly (top 20) |
| macOS | /Applications/* from fresh install |
| Android DEX | Top 10 Play Store apps (extracted APKs) |

## Malware Sample Testing

### Positive Testing

```bash
# Rule should match all target samples
yr scan -r MAL_Win_Emotet.yar samples/emotet/

# With matched strings shown
yr scan -s MAL_Win_Emotet.yar samples/emotet/

# Expected: all files listed
# If any missing: rule too narrow
```

### Variant Coverage

Test against:
- Multiple versions/builds
- Packed variants (UPX, custom packers)
- Different configurations
- Both 32-bit and 64-bit

## False Positive Investigation

When a rule matches goodware:

### 1. Identify the Match

```bash
yr scan -s rule.yar false_positive.exe
```

Shows which strings matched.

### 2. Analyze Why

Common causes:
- String too generic ("cmd.exe", API names)
- Shared library code
- Common development patterns
- Legitimate use of same techniques

### 3. Remediation Options

**Option A: Exclude the specific file**

```yara
strings:
    $fp_vendor = "Legitimate Software Inc"

condition:
    $malware_string and not $fp_vendor
```

**Option B: Add distinguishing string**

```yara
strings:
    $generic = "common_string"
    $specific = "unique_malware_marker"

condition:
    $generic and $specific  // Both required
```

**Option C: Tighten positional constraints**

```yara
condition:
    $marker in (0..1024) and  // Only in first 1KB
    filesize < 500KB          // Malware-typical size
```

**Option D: Replace the string**

Find a more unique indicator and remove the problematic string.

## Supply Chain Package Testing

For npm/PyPI/RubyGems rules, test against ecosystem-appropriate corpora:

### Recommended Test Corpora

| Corpus | Source | Purpose |
|--------|--------|---------|
| Top 1000 npm packages | `npm search --searchlimit=1000` | Avoid FPs on popular dependencies |
| Packages with postinstall scripts | Filter for `scripts.postinstall` in package.json | Common attack vector |
| Known malicious packages | [npm-shai-hulud-scanner](https://github.com/nickytonline/npm-shai-hulud-scanner) list | Positive validation |
| VS Code top extensions | Marketplace API | Extension-specific rules |

### Common Attack Pattern Testing

**Critical pattern:** `postinstall + network call + credential path` is the signature of supply chain attacks. Test that your rule catches this combo while ignoring legitimate build scripts.

```bash
# Build a test corpus from npm
mkdir -p test_corpus/legitimate test_corpus/suspicious

# Grab legitimate packages with postinstall (build tools)
npm pack webpack && tar -xzf webpack-*.tgz -C test_corpus/legitimate/
npm pack electron-builder && tar -xzf electron-builder-*.tgz -C test_corpus/legitimate/

# Your rule should NOT match legitimate postinstall scripts
yr scan -r supply_chain_rule.yar test_corpus/legitimate/
# Expected: zero matches
```

### Known Malicious Package Patterns

Rules targeting supply chain attacks should detect patterns from documented incidents:

| Incident | Key Indicators | Reference |
|----------|----------------|-----------|
| chalk/debug (Sept 2025) | `runmask`, `checkethereumw`, ERC-20 selectors | Stairwell |
| os-info-checker-es6 | Variation selectors, eval+atob | Veracode |
| event-stream | Flatmap dependency, Bitcoin wallet targeting | npm advisory |

**Positive validation:** Test your rule against recreated (defanged) versions of known malicious packages to ensure detection.

## Checklist

Before any rule goes to production:

- [ ] `yr check` passes (syntax and YARA-X compatibility)
- [ ] `yr fmt --check` passes (consistent formatting)
- [ ] Linter passes (`uv run yara_lint.py rule.yar`)
- [ ] Matches all target samples (positive testing)
- [ ] Zero matches on goodware corpus (negative testing)
- [ ] Tested against packed variants if applicable
- [ ] Performance acceptable (< 1s per file on average)
- [ ] Peer reviewed by second analyst
- [ ] Version and changelog updated

### Supply Chain Rule Additions

- [ ] Tested against top 100 packages in target ecosystem
- [ ] Does not match legitimate postinstall scripts (webpack, electron-builder, etc.)
- [ ] Validated against known malicious package patterns
