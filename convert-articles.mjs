import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join, basename } from 'path';

const ARTICLES_DIR = '/Users/ocean/Documents/Ocean个人主页/articles';
const OUTPUT_DIR = '/Users/ocean/Documents/Ocean个人主页/ocean-blog/src/content/posts';

// Category mapping rules
// Directory-based defaults + title keyword overrides
const STORY_KEYWORDS = [
  '清迈', '曼谷', '京都', '马尼拉', '新加坡', '东南亚', '宁波', '上海',
  '摩托车', '冲浪', '旅行', '散文', '鬼故事', '怪谈', '糖醋鱼',
  '访谈', '对话', '围炉', '告别', '在路上', '出发的岁月',
  '我的大学', '泰康东路', '火种', '作结',
  '清真寺', '母语', '藏头', '红与白', '另一面', '凉季',
  '香蕉煎饼', '答案在风中', '河南',
];

const AI_KEYWORDS = [
  'AI Agent', 'AI Model', 'AI编程', 'Vibe Coding', 'AI 时代',
];

const REFLECTIONS_KEYWORDS = [
  '思考', '择业', '职业', '随笔', '成长', '复利', '信息',
  '社会分层', '生产关系', '品牌出海', '风口', '命运', '勇敢',
  '非对称', '大力出奇迹', '写在23岁', '资本主义', '告别2024',
  '文科生', 'CAPM', '贝塔', '阿法', '小团队', '贝索斯',
  '自我的进化', '斩杀线', '无耻之徒',
];

function categorize(title, dirCategory) {
  // AI keywords take highest priority
  for (const kw of AI_KEYWORDS) {
    if (title.includes(kw)) return 'ai';
  }

  // ecommerce directory articles stay as ecommerce
  if (dirCategory === 'ecommerce') return 'ecommerce';

  // university → stories
  if (dirCategory === 'university') return 'stories';

  // Story keywords
  for (const kw of STORY_KEYWORDS) {
    if (title.includes(kw)) return 'stories';
  }

  // crypto directory → web3
  if (dirCategory === 'crypto') return 'web3';

  // life directory: check for reflections keywords first
  if (dirCategory === 'life') {
    for (const kw of REFLECTIONS_KEYWORDS) {
      if (title.includes(kw)) return 'reflections';
    }
    // Default life articles to stories (most are essays/travel)
    return 'stories';
  }

  return 'reflections';
}

function parseDate(dateStr) {
  if (!dateStr) return null;
  // Parse "2025年1月16日 11:03" format
  const match = dateStr.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/);
  if (match) {
    const [, year, month, day] = match;
    return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
  }
  return null;
}

function slugify(title) {
  // Create a URL-friendly slug from Chinese title
  return title
    .replace(/[｜|]/g, '-')
    .replace(/[\/\\:*?"<>，。、；：！？""''「」【】（）·\s]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-')
    .toLowerCase()
    .substring(0, 100);
}

function extractDescription(content) {
  // Get first meaningful paragraph as description
  const lines = content.split('\n').filter(l => l.trim().length > 10);
  const desc = lines[0] || '';
  return desc.substring(0, 120).replace(/"/g, '\\"');
}

function escapeForMdx(content) {
  // Escape characters that are problematic in MDX
  return content
    // Escape curly braces (JSX expression syntax in MDX)
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    // Escape < and > that aren't part of HTML tags (JSX in MDX)
    .replace(/<(?![a-zA-Z\/!])/g, '&lt;')
    .replace(/(?<![a-zA-Z"'\s\/])>/g, '&gt;');
}

const usedSlugs = new Set();
let totalConverted = 0;
let skipped = 0;

const dirs = ['crypto', 'life', 'ecommerce', 'university'];

for (const dir of dirs) {
  const dirPath = join(ARTICLES_DIR, dir);
  let files;
  try {
    files = readdirSync(dirPath).filter(f => f.endsWith('.md'));
  } catch {
    continue;
  }

  for (const file of files) {
    const filePath = join(dirPath, file);
    const raw = readFileSync(filePath, 'utf-8');

    // Parse the article
    const titleMatch = raw.match(/^# (.+)$/m);
    const dateMatch = raw.match(/\*\*日期\*\*: (.+)$/m);
    const urlMatch = raw.match(/\*\*原文链接\*\*: (.+)$/m);

    const title = titleMatch ? titleMatch[1].trim() : file.replace('.md', '');
    const dateStr = dateMatch ? dateMatch[1].trim() : '';
    const url = urlMatch ? urlMatch[1].trim() : '';

    // Extract content after the --- separator
    const contentParts = raw.split('---');
    const articleContent = contentParts.length > 1 ? contentParts.slice(1).join('---').trim() : raw;

    const category = categorize(title, dir);
    const date = parseDate(dateStr) || '2024-06-01';
    const description = extractDescription(articleContent);

    // Generate unique slug
    let slug = slugify(title);
    if (!slug || slug.length < 2) slug = `article-${totalConverted}`;
    if (usedSlugs.has(slug)) {
      slug = slug + '-' + totalConverted;
    }
    usedSlugs.add(slug);

    // Use .md instead of .mdx to avoid JSX parsing issues
    const frontmatter = `---
title: "${title.replace(/"/g, '\\"')}"
description: "${description}"
category: "${category}"
date: ${date}
---`;

    const mdxContent = `${frontmatter}

${articleContent}
`;

    const outputPath = join(OUTPUT_DIR, `${slug}.md`);
    writeFileSync(outputPath, mdxContent, 'utf-8');
    totalConverted++;
    console.log(`[${totalConverted}] ${category.padEnd(12)} ${title}`);
  }
}

console.log(`\n========== CONVERSION DONE ==========`);
console.log(`Total converted: ${totalConverted}`);
console.log(`Output: ${OUTPUT_DIR}`);
