import fs from 'fs';
import path from 'path';

const postsDir = './src/content/posts';
const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'));

const sentenceEndings = /[。，！？、；：……）""》】\.\,\!\?\;\:\)\]\>]$/;
const listOrSpecial = /^[\-\*\>\d\|·•►▶●○■□☆★✓✗→←↓↑「」『』【]/;

function isSubtitleCandidate(line) {
  if (!line || line.length === 0 || line.length > 30) return false;
  if (line.length <= 1) return false;
  if (line.startsWith('#')) return false;
  if (sentenceEndings.test(line)) return false;
  if (listOrSpecial.test(line)) return false;
  if (line.startsWith('```') || line.startsWith('http') || line.startsWith('[') || line.startsWith('!')) return false;
  return true;
}

let totalFixed = 0;

for (const file of files) {
  const filePath = path.join(postsDir, file);
  const raw = fs.readFileSync(filePath, 'utf-8');

  const parts = raw.split('---');
  if (parts.length < 3) continue;

  const frontmatter = parts[1];
  const content = parts.slice(2).join('---');

  const titleMatch = frontmatter.match(/title:\s*"(.+?)"/);
  const title = titleMatch ? titleMatch[1] : '';

  const lines = content.split('\n');
  const newLines = [];
  let fileChanges = 0;
  let firstNonEmpty = true;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const prevLine = i > 0 ? lines[i - 1].trim() : '';
    const nextLine = i < lines.length - 1 ? lines[i + 1].trim() : '';

    // Skip first non-empty line if it duplicates the title
    if (firstNonEmpty && line.length > 0) {
      firstNonEmpty = false;
      if (!line.startsWith('#')) {
        const cleanTitle = title.replace(/[｜\|].*/g, '').trim();
        const cleanLine = line.replace(/[｜\|].*/g, '').trim();
        if (cleanLine === cleanTitle || cleanTitle.includes(cleanLine) || cleanLine.includes(cleanTitle)) {
          newLines.push('');
          fileChanges++;
          continue;
        }
      }
    }

    // Already a heading — keep as is
    if (line.startsWith('#')) {
      newLines.push(lines[i]);
      continue;
    }

    // Empty line
    if (line.length === 0) {
      newLines.push(lines[i]);
      continue;
    }

    // Check subtitle conditions
    const candidate = isSubtitleCandidate(line);
    if (!candidate) {
      newLines.push(lines[i]);
      continue;
    }

    // Context checks - more relaxed
    const prevIsEmpty = prevLine === '';
    const prevIsHeading = prevLine.startsWith('#');
    const prevIsAlsoShort = isSubtitleCandidate(prevLine); // consecutive subtitles
    const nextIsEmpty = nextLine === '';
    const nextIsLongText = nextLine.length > 30;
    const nextIsAlsoShort = isSubtitleCandidate(nextLine);
    const nearStart = i <= 3;

    const validContext = (prevIsEmpty || prevIsHeading || prevIsAlsoShort || nearStart)
      && (nextIsEmpty || nextIsLongText || nextIsAlsoShort);

    if (validContext) {
      // If previous line was also converted to a subtitle, make this one ###
      const prevNewLine = newLines.length > 0 ? newLines[newLines.length - 1].trim() : '';
      if (prevNewLine.startsWith('## ') || prevIsAlsoShort) {
        newLines.push(`### ${line}`);
      } else {
        newLines.push(`## ${line}`);
      }
      fileChanges++;
    } else {
      newLines.push(lines[i]);
    }
  }

  if (fileChanges > 0) {
    const newContent = `---${frontmatter}---${newLines.join('\n')}`;
    fs.writeFileSync(filePath, newContent, 'utf-8');
    totalFixed++;
    console.log(`✓ ${file} — ${fileChanges} changes`);
  }
}

console.log(`\nDone: ${totalFixed}/${files.length} files modified`);
