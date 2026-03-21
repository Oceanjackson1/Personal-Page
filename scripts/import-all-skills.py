#!/usr/bin/env python3
"""Batch import all skills from source directory into blog format."""

import os
import re
import yaml
from pathlib import Path

SOURCE_DIR = Path("/Users/ocean/Documents/Claude Skill")
BLOG_DIR = Path("/Users/ocean/Documents/Ocean个人主页/ocean-blog/src/content/skills")
DATE = "2026-03-20"

CATEGORY_RULES = [
    ("devops", r'docker|kubernetes|k8s|helm|terraform|ansible|cicd|ci.cd|pipeline|deploy|devops|cloudflare|aws|gcp|azure|infrastructure|monitoring|observability|prometheus|grafana|jenkins|gitlab.ci|github.actions|serverless|nginx|linux|bash.script|shell|sre|incident|runbook|cloud|istio|linkerd|service.mesh|datadog|sentry|loki|fluentbit|container'),
    ("research", r'research|database(?!.migrat)|data.sci|machine.learn|ml.pipe|deep.learn|neural|nlp|llm(?!.app)|ai.(?:agent|engineer|product|native)|embedding|rag(?!.impl)|vector.(?:db|index)|pandas|scipy|numpy|statist|bioinform|genomic|protein|chemical|medical|clinical|scientific|paper|arxiv|pubmed|phylo|metabol'),
    ("writing", r'writing|blog.writ|article.writ|content.(?:creat|market|engine)|copywriting|documentation(?!.gen)|proofreader|seo.content|email.sequence|podcast|ebook|book.architect|speech|slides|presentation|latex|diary|prose|copy.edit'),
    ("workflow", r'automation|workflow(?!.orch)|slack|discord|telegram|notion|jira|linear(?!.alg)|asana|trello|calendar|outlook|zoom|teams|hubspot|salesforce|zapier|make.auto|n8n|airtable|clickup|todoist|pipedrive|intercom|zendesk|freshdesk|monday|basecamp|figma|canva|miro|google.docs|google.sheets|google.drive|one.drive|box.auto|dropbox|reddit.auto|youtube.auto|instagram|tiktok|twitter.auto|linkedin.auto|shopify.auto|stripe.auto'),
    ("development", r'react|vue|angular|svelte|next|nuxt|typescript|javascript|python|rust|golang|java|kotlin|swift|ruby|rails|laravel|django|flask|fastapi|express|nest|spring|dotnet|csharp|cpp|php|elixir|scala|haskell|perl|sql|graphql|api|rest|grpc|websocket|testing|test|tdd|debug|refactor|architect|pattern|security|auth|crypto|blockchain|solidity|web3|mobile|ios|android|flutter|react.native|game|unity|unreal|godot|frontend|backend|fullstack|component|hook|plugin|skill|agent|mcp|claude|prompt|coding|code|developer|engineer'),
]

def categorize(name: str, desc: str) -> str:
    combined = f"{name} {desc}".lower()
    for cat, pattern in CATEGORY_RULES:
        if re.search(pattern, combined):
            return cat
    return "other"

def make_title(slug: str) -> str:
    words = slug.replace("-", " ").split()
    # Capitalize each word, keep acronyms
    result = []
    for w in words:
        if len(w) <= 3 and w.isalpha():
            result.append(w.upper() if w in ('api', 'cli', 'sdk', 'ui', 'ux', 'sql', 'css', 'html', 'mcp', 'llm', 'ai', 'ml', 'seo', 'ddd', 'tdd', 'k8s', 'aws', 'gcp', 'sre', 'rag', 'jwt', 'ssh', 'dns', 'cdn', 'ssr', 'xss', 'ci', 'cd', 'fp', 'go', 'ts', 'js', 'py') else w.capitalize())
        else:
            result.append(w.capitalize())
    return " ".join(result)

def make_tags(slug: str) -> list:
    words = slug.split("-")
    stop = {'a', 'an', 'the', 'and', 'or', 'for', 'in', 'on', 'to', 'of', 'with', 'pro', 'expert', 'best', 'practices', 'patterns', 'skills', 'guide', 'tutorial', 'v2', 'v3'}
    return [w for w in words if w not in stop and len(w) > 1][:6]

def extract_frontmatter(content: str) -> tuple:
    """Extract frontmatter dict and body from SKILL.md content."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        fm = {}

    body = parts[2].strip()
    return fm, body

def safe_yaml_string(s: str) -> str:
    """Make a string safe for YAML double-quoted value."""
    if not s:
        return ""
    # Remove problematic characters
    s = s.replace("\\", "")
    s = s.replace('"', "'")
    # Truncate long descriptions
    if len(s) > 250:
        s = s[:247] + "..."
    # Remove newlines
    s = s.replace("\n", " ").replace("\r", "")
    return s.strip()

def gather_extra_content(skill_dir: Path) -> str:
    """Gather content from references/ and examples/ subdirectories."""
    extra = []

    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.glob("*.md")):
            ref_name = ref_file.stem.replace("-", " ").title()
            ref_content = ref_file.read_text(errors="replace").strip()
            # Strip frontmatter if present
            _, ref_body = extract_frontmatter(ref_content)
            if not ref_body:
                ref_body = ref_content
            extra.append(f"\n---\n\n## Reference: {ref_name}\n\n{ref_body}")

    examples_dir = skill_dir / "examples"
    if examples_dir.is_dir():
        for ex_file in sorted(examples_dir.glob("*.md")):
            ex_name = ex_file.stem.replace("-", " ").title()
            ex_content = ex_file.read_text(errors="replace").strip()
            extra.append(f"\n---\n\n## Example: {ex_name}\n\n{ex_content}")

    return "\n".join(extra)

def main():
    imported = 0
    skipped = 0
    errors = 0

    for skill_dir in sorted(SOURCE_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        slug = skill_dir.name
        source_file = skill_dir / "SKILL.md"
        blog_file = BLOG_DIR / f"{slug}.md"

        # Skip if already exists
        if blog_file.exists():
            skipped += 1
            continue

        if not source_file.exists():
            continue

        try:
            content = source_file.read_text(errors="replace")
            fm, body = extract_frontmatter(content)

            # Get description
            desc = fm.get("description", "") or ""
            if isinstance(desc, str):
                desc = safe_yaml_string(desc)
            else:
                desc = str(desc)[:200]

            if len(desc) < 5:
                desc = f"Claude Code Skill for {make_title(slug)}"

            # Get source
            src = fm.get("source", "community")
            if src not in ("official", "community"):
                src = "community"

            category = categorize(slug, desc)
            title = make_title(slug)
            tags = make_tags(slug)

            # Gather extra content
            extra = gather_extra_content(skill_dir)

            # Build blog file
            tags_str = ", ".join(f'"{t}"' for t in tags)

            blog_content = f"""---
title: "{safe_yaml_string(title)}"
description: "{desc}"
category: "{category}"
source: "{src}"
author: "Community"
tags: [{tags_str}]
date: {DATE}
---

{body}
{extra}
"""
            blog_file.write_text(blog_content)
            imported += 1

        except Exception as e:
            print(f"ERROR {slug}: {e}")
            errors += 1

    print(f"Imported: {imported}, Skipped: {skipped}, Errors: {errors}")

if __name__ == "__main__":
    main()
