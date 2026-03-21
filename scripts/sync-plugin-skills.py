#!/usr/bin/env python3
"""Sync skills from Claude plugin cache into blog, preserving blog frontmatter."""

import os
import re
import yaml
from pathlib import Path

BLOG_DIR = Path("/Users/ocean/Documents/Ocean个人主页/ocean-blog/src/content/skills")
PLUGIN_CACHE = Path(os.path.expanduser("~/.claude/plugins/cache"))

# Map blog slug → plugin cache path (use latest version)
SKILL_MAP = {
    # data plugin
    "airflow-hitl": "claude-plugins-official/data/0.1.0/skills/airflow-hitl",
    "analyzing-data": "claude-plugins-official/data/0.1.0/skills/analyzing-data",
    "annotating-task-lineage": "claude-plugins-official/data/0.1.0/skills/annotating-task-lineage",
    "authoring-dags": "claude-plugins-official/data/0.1.0/skills/authoring-dags",
    "checking-freshness": "claude-plugins-official/data/0.1.0/skills/checking-freshness",
    "cosmos-dbt-core": "claude-plugins-official/data/0.1.0/skills/cosmos-dbt-core",
    "cosmos-dbt-fusion": "claude-plugins-official/data/0.1.0/skills/cosmos-dbt-fusion",
    "creating-openlineage-extractors": "claude-plugins-official/data/0.1.0/skills/creating-openlineage-extractors",
    "debugging-dags": "claude-plugins-official/data/0.1.0/skills/debugging-dags",
    "deploying-airflow": "claude-plugins-official/data/0.1.0/skills/deploying-airflow",
    "managing-astro-local-env": "claude-plugins-official/data/0.1.0/skills/managing-astro-local-env",
    "managing-astro-deployments": "claude-plugins-official/data/0.1.0/skills/managing-astro-local-env",  # closest match
    "migrating-airflow-2-to-3": "claude-plugins-official/data/0.1.0/skills/migrating-airflow-2-to-3",
    "profiling-tables": "claude-plugins-official/data/0.1.0/skills/profiling-tables",
    "setting-up-astro-project": "claude-plugins-official/data/0.1.0/skills/setting-up-astro-project",
    "testing-dags": "claude-plugins-official/data/0.1.0/skills/testing-dags",
    "tracing-downstream-lineage": "claude-plugins-official/data/0.1.0/skills/tracing-downstream-lineage",
    "tracing-upstream-lineage": "claude-plugins-official/data/0.1.0/skills/tracing-upstream-lineage",
    "troubleshooting-astro-deployments": "claude-plugins-official/data/0.1.0/skills/setting-up-astro-project",  # closest
    "warehouse-init": "claude-plugins-official/data/0.1.0/skills/warehouse-init",
    # chrome-devtools-mcp
    "a11y-debugging": "claude-plugins-official/chrome-devtools-mcp/latest/skills/a11y-debugging",
    "chrome-devtools": "claude-plugins-official/chrome-devtools-mcp/latest/skills/chrome-devtools",
    "chrome-devtools-troubleshooting": "claude-plugins-official/chrome-devtools-mcp/latest/skills/troubleshooting",
    "debug-optimize-lcp": "claude-plugins-official/chrome-devtools-mcp/latest/skills/debug-optimize-lcp",
    # claude-code-setup
    "claude-automation-recommender": "claude-plugins-official/claude-code-setup/1.0.0/skills/claude-automation-recommender",
    # coderabbit
    "coderabbit-code-review": "claude-plugins-official/coderabbit/1.0.0/skills/code-review",
    # sourcegraph
    "searching-sourcegraph": "claude-plugins-official/sourcegraph/0.1.0/skills/searching-sourcegraph",
    # Notion
    "notion-knowledge-capture": "claude-plugins-official/Notion/0.1.0/skills/notion/knowledge-capture",
    "notion-meeting-intelligence": "claude-plugins-official/Notion/0.1.0/skills/notion/meeting-intelligence",
    "notion-research-documentation": "claude-plugins-official/Notion/0.1.0/skills/notion/research-documentation",
    "notion-spec-to-implementation": "claude-plugins-official/Notion/0.1.0/skills/notion/spec-to-implementation",
}

def extract_frontmatter_and_body(content: str):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, parts[2].strip()

def gather_references(skill_dir: Path) -> str:
    extra = []
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.glob("*.md")):
            ref_name = ref_file.stem.replace("-", " ").title()
            ref_content = ref_file.read_text(errors="replace").strip()
            _, ref_body = extract_frontmatter_and_body(ref_content)
            if not ref_body:
                ref_body = ref_content
            extra.append(f"\n---\n\n## Reference: {ref_name}\n\n{ref_body}")
    return "\n".join(extra)

updated = 0
skipped = 0

for blog_slug, cache_path in SKILL_MAP.items():
    blog_file = BLOG_DIR / f"{blog_slug}.md"
    source_dir = PLUGIN_CACHE / cache_path
    source_file = source_dir / "SKILL.md"

    if not blog_file.exists():
        print(f"SKIP (no blog file): {blog_slug}")
        skipped += 1
        continue

    if not source_file.exists():
        print(f"SKIP (no source): {blog_slug} → {source_file}")
        skipped += 1
        continue

    # Read blog frontmatter
    blog_content = blog_file.read_text(errors="replace")
    blog_parts = blog_content.split("---", 2)
    if len(blog_parts) < 3:
        print(f"SKIP (bad frontmatter): {blog_slug}")
        skipped += 1
        continue
    blog_frontmatter = f"---{blog_parts[1]}---"

    # Read source body
    source_content = source_file.read_text(errors="replace")
    _, source_body = extract_frontmatter_and_body(source_content)

    # Gather references
    extra = gather_references(source_dir)

    # Write combined file
    new_content = f"{blog_frontmatter}\n\n{source_body}\n{extra}\n"
    blog_file.write_text(new_content)

    old_lines = len(blog_content.splitlines())
    new_lines = len(new_content.splitlines())
    print(f"✅ {blog_slug}: {old_lines} → {new_lines} lines")
    updated += 1

print(f"\nDone: {updated} updated, {skipped} skipped")
