#!/bin/bash
# Sync full SKILL.md content from source into blog skill files
# Preserves blog frontmatter, replaces body with full source content

SOURCE_DIR="/Users/ocean/Documents/Claude Skill"
BLOG_DIR="/Users/ocean/Documents/Ocean个人主页/ocean-blog/src/content/skills"

updated=0
skipped=0

for blog_file in "$BLOG_DIR"/*.md; do
  slug=$(basename "$blog_file" .md)
  source_skill="$SOURCE_DIR/$slug/SKILL.md"

  if [ ! -f "$source_skill" ]; then
    skipped=$((skipped+1))
    continue
  fi

  # Extract blog frontmatter (everything between first --- and second ---)
  blog_frontmatter=$(awk '/^---$/{n++; if(n==2){print; exit}} {print}' "$blog_file")

  # Extract source content (everything after the second ---)
  source_body=$(awk 'BEGIN{n=0} /^---$/{n++; if(n==2){found=1; next}} found{print}' "$source_skill")

  # Also gather content from references/ and examples/ subdirs
  extra_content=""

  # Add references
  if [ -d "$SOURCE_DIR/$slug/references" ]; then
    for ref_file in "$SOURCE_DIR/$slug/references"/*.md; do
      [ -f "$ref_file" ] || continue
      ref_name=$(basename "$ref_file" .md | sed 's/-/ /g; s/\b\(.\)/\u\1/g')
      ref_body=$(awk 'BEGIN{n=0} /^---$/{n++; if(n==2){found=1; next}} found{print}' "$ref_file")
      # If no frontmatter, use whole file
      if [ -z "$ref_body" ]; then
        ref_body=$(cat "$ref_file")
      fi
      extra_content="$extra_content

---

## Reference: $ref_name

$ref_body"
    done
  fi

  # Add examples
  if [ -d "$SOURCE_DIR/$slug/examples" ]; then
    for ex_file in "$SOURCE_DIR/$slug/examples"/*.md; do
      [ -f "$ex_file" ] || continue
      ex_name=$(basename "$ex_file" .md | sed 's/-/ /g; s/\b\(.\)/\u\1/g')
      ex_body=$(cat "$ex_file")
      extra_content="$extra_content

---

## Example: $ex_name

$ex_body"
    done
  fi

  # Combine: blog frontmatter + source body + extra content
  {
    echo "$blog_frontmatter"
    echo ""
    echo "$source_body"
    if [ -n "$extra_content" ]; then
      echo "$extra_content"
    fi
  } > "$blog_file"

  old_lines=$(wc -l < "$blog_file" 2>/dev/null)
  echo "✅ $slug: synced (now $(wc -l < "$blog_file") lines)"
  updated=$((updated+1))
done

echo ""
echo "Done: $updated updated, $skipped skipped (no source)"
