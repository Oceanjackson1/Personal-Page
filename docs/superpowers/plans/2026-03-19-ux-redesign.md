# Ocean's Blog UX/UI Redesign Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the blog from a generic "bootstrap feel" to a polished, editorial Apple-style personal blog with visual rhythm, personality, and refined micro-interactions.

**Architecture:** Keep Astro 6 + Tailwind 4 stack unchanged. Redesign is CSS/template-level only — no new dependencies. Focus on layout rhythm, typography contrast, whitespace control, and visual storytelling. All changes are in `.astro` components and `global.css`.

**Tech Stack:** Astro 6, Tailwind CSS 4, CSS custom properties, vanilla JS (IntersectionObserver)

---

## Current Problems Diagnosed

| # | Problem | Where | Impact |
|---|---------|-------|--------|
| 1 | **Scroll-animate elements invisible** — 3 post cards + code section start `opacity:0` and never become visible because IntersectionObserver doesn't trigger on elements already in/near viewport on page load | `index.astro`, `global.css` | Homepage looks broken — only 1 card shows, huge empty space |
| 2 | **Hero is lifeless** — Avatar + name + motto stacked vertically in center with too much padding, feels like a template placeholder | `index.astro` | First impression is "unfinished" |
| 3 | **No visual rhythm** — Every section has identical white background, same padding, same card borders. No dark/light alternation Apple uses | All pages | Monotonous, no sense of journey |
| 4 | **Cards are generic boxes** — Thin border + white fill, no depth or texture difference between featured and normal cards | `PostCard.astro` | Nothing draws the eye |
| 5 | **Typography lacks punch** — Section headings ("最新文章", "代码库") are regular weight, no size contrast with body text | `index.astro`, list pages | Flat hierarchy, hard to scan |
| 6 | **Posts list is a text wall** — Pure text list with thin dividers, no visual anchors or hover delight | `posts/index.astro` | Boring to browse |
| 7 | **Footer is bare** — Just 3 icons + copyright, feels unfinished | `Footer.astro` | Abrupt page ending |
| 8 | **ecommerce category added but not fully wired** — Not in Nav dropdown, no dedicated category page, not in categoryLabels everywhere | Multiple files | 404 or missing category |
| 9 | **Mobile nav has no animation** — Just `hidden`/shown toggle, no slide or fade | `Nav.astro` | Jarring state change |
| 10 | **Code section on homepage too sparse** — Two big cards with just project names listed, wastes space | `index.astro` | Doesn't showcase projects well |

---

## File Structure (files to modify)

```
src/
├── styles/global.css              ← Fix animations, add section styles, improve prose
├── components/
│   ├── Nav.astro                  ← Add ecommerce, improve mobile menu animation
│   ├── Footer.astro               ← Richer footer with columns
│   ├── PostCard.astro             ← Redesign: featured vs compact variants
│   └── ProjectCard.astro          ← Add subtle gradient border effect
├── pages/
│   ├── index.astro                ← Major redesign: hero, sections, rhythm
│   ├── posts/index.astro          ← Card grid layout, better filtering
│   ├── posts/[slug].astro         ← Refine reading experience
│   └── posts/ecommerce.astro      ← NEW: ecommerce category page
├── content.config.ts              ← Already updated (ecommerce added) ✓
└── i18n/
    ├── zh.json                    ← Add ecommerce translations
    └── en.json                    ← Add ecommerce translations
```

---

## Task 1: Fix scroll-animate + improve animation system

**Files:**
- Modify: `src/styles/global.css`
- Modify: `src/pages/index.astro`

**Problem:** Elements with `.scroll-animate` start at `opacity:0` and rely on IntersectionObserver, but elements near the viewport on page load never trigger because they aren't "intersecting" at observation time. This makes the homepage look broken.

- [ ] **Step 1: Fix global.css animation classes**

Replace the current scroll-animate system with one that handles above-the-fold elements:

```css
/* Replace existing .scroll-animate block with: */

/* Elements that animate on page load (hero area) */
.animate-fade-in-up {
  animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.animate-scale-in {
  animation: scaleIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

/* Elements that animate on scroll (below the fold) */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger children */
.stagger-children > .reveal:nth-child(1) { transition-delay: 0ms; }
.stagger-children > .reveal:nth-child(2) { transition-delay: 80ms; }
.stagger-children > .reveal:nth-child(3) { transition-delay: 160ms; }
.stagger-children > .reveal:nth-child(4) { transition-delay: 240ms; }
```

Key change: Use `cubic-bezier(0.16, 1, 0.3, 1)` — Apple's spring-like easing that starts fast and decelerates smoothly, instead of generic `ease-out`.

- [ ] **Step 2: Fix IntersectionObserver in index.astro**

Replace the current observer script with a more reliable version:

```html
<script>
  // Trigger reveal for elements already in viewport + future scrolls
  function initReveal() {
    const els = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.05, rootMargin: '0px 0px -40px 0px' }
    );
    els.forEach((el) => observer.observe(el));
  }
  // Run immediately (not waiting for scroll)
  initReveal();
</script>
```

Key fixes: Lower threshold (0.05 vs 0.1), negative bottom rootMargin triggers earlier, rename class from `scroll-animate` to `reveal`.

- [ ] **Step 3: Update all `scroll-animate` references in index.astro to `reveal`**

- [ ] **Step 4: Verify in browser — all sections should be visible on scroll**

---

## Task 2: Redesign homepage hero section

**Files:**
- Modify: `src/pages/index.astro`
- Modify: `src/styles/global.css`

**Design direction:** Instead of everything centered vertically, use a more editorial layout. Avatar left, text right on desktop. Add a subtle background gradient to create depth. Make it feel personal, not template-like.

- [ ] **Step 1: Redesign hero layout in index.astro**

Replace the current hero `<section>` with:

```astro
<!-- Hero Section -->
<section class="relative overflow-hidden">
  <!-- Subtle gradient background -->
  <div class="absolute inset-0 bg-gradient-to-b from-[color-mix(in_srgb,var(--color-accent)_5%,var(--color-bg))] to-[var(--color-bg)]"></div>

  <div class="relative max-w-[var(--width-wide)] mx-auto px-6 py-20 sm:py-28">
    <div class="flex flex-col sm:flex-row items-center sm:items-start gap-8 sm:gap-12">
      <!-- Avatar -->
      <div class="animate-scale-in shrink-0">
        <img
          src="/avatar.jpg"
          alt="Ocean"
          class="w-28 h-28 sm:w-36 sm:h-36 rounded-full object-cover shadow-xl ring-4 ring-white/80 dark:ring-white/10"
        />
      </div>

      <!-- Text content -->
      <div class="text-center sm:text-left">
        <h1 class="animate-fade-in-up text-4xl sm:text-5xl font-semibold tracking-tight mb-3" style="animation-delay: 80ms;">
          Ocean
        </h1>
        <p class="animate-fade-in-up text-xl text-[color:var(--color-text-secondary)] mb-6 font-light" style="animation-delay: 160ms;"
           data-i18n-zh="「找到一个最长的雪坡，滚雪球」"
           data-i18n-en="「Find the longest slope, roll the snowball」">
          「找到一个最长的雪坡，滚雪球」
        </p>

        <!-- Social as pill buttons -->
        <div class="animate-fade-in-up flex flex-wrap items-center justify-center sm:justify-start gap-3" style="animation-delay: 240ms;">
          <a href="https://x.com/Ocean_Jackon" target="_blank" rel="noopener noreferrer"
             class="inline-flex items-center gap-1.5 px-4 py-1.5 text-sm rounded-full border border-[var(--color-border)] text-[color:var(--color-text-secondary)] hover:text-[color:var(--color-text-primary)] hover:border-[var(--color-text-tertiary)] transition-all">
            <!-- X icon SVG -->
            @Ocean_Jackon
          </a>
          <a href="https://github.com/Oceanjackson1" target="_blank" rel="noopener noreferrer"
             class="inline-flex items-center gap-1.5 px-4 py-1.5 text-sm rounded-full border border-[var(--color-border)] text-[color:var(--color-text-secondary)] hover:text-[color:var(--color-text-primary)] hover:border-[var(--color-text-tertiary)] transition-all">
            <!-- GitHub icon SVG -->
            GitHub
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
```

Key changes:
- Horizontal layout on desktop (avatar left, text right) — more editorial
- Subtle top gradient background creates depth separation from nav
- Avatar larger (36 → 144px on desktop), white ring for polish
- Social links as pill buttons instead of plain text
- `font-light` on motto creates weight contrast

- [ ] **Step 2: Add hero gradient support for dark mode in global.css**

```css
.dark .hero-gradient {
  background: linear-gradient(to bottom,
    color-mix(in srgb, var(--color-accent) 3%, var(--color-bg)),
    var(--color-bg));
}
```

- [ ] **Step 3: Verify hero renders correctly on both mobile and desktop viewports**

---

## Task 3: Redesign latest posts section with visual rhythm

**Files:**
- Modify: `src/pages/index.astro`
- Modify: `src/components/PostCard.astro`

**Design direction:** Featured post gets a prominent "hero card" with category-colored left accent stripe. Small cards become a denser, more scannable grid. Add section divider texture.

- [ ] **Step 1: Redesign PostCard.astro with two distinct variants**

**Featured variant** — large card with colored accent bar on left:
```astro
<!-- Featured: accent bar + spacious padding -->
<a class="block rounded-[var(--radius-card)] bg-[var(--color-surface)] border border-[var(--color-border)] overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:shadow-[var(--shadow-card-hover)] group">
  <div class="flex">
    <div class="w-1 shrink-0 rounded-l-[var(--radius-card)]" style={`background: ${cat.color}`}></div>
    <div class="p-6 sm:p-8">
      <span class="category-badge">...</span>
      <h3 class="text-xl sm:text-2xl font-semibold mt-3 mb-2 group-hover:text-[color:var(--color-accent)] transition-colors">
        {title}
      </h3>
      <p class="text-base text-[color:var(--color-text-secondary)] mb-4 line-clamp-2">{description}</p>
      <time>...</time>
    </div>
  </div>
</a>
```

**Compact variant** — minimal card for grid:
```astro
<a class="block p-5 rounded-[var(--radius-card)] bg-[var(--color-surface)] border border-[var(--color-border)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[var(--shadow-card-hover)] group">
  <span class="category-badge">...</span>
  <h3 class="text-base font-semibold mt-2 mb-1 group-hover:text-[color:var(--color-accent)] transition-colors">
    {title}
  </h3>
  <time>...</time>
</a>
```

Key: `group-hover` on title creates a connected hover feel — hovering the card highlights the title.

- [ ] **Step 2: Restructure latest posts in index.astro**

Use a featured + grid layout with the `reveal` class and `stagger-children`:

```astro
<section class="py-16 sm:py-20">
  <div class="max-w-[var(--width-wide)] mx-auto px-6">
    <div class="reveal flex items-baseline justify-between mb-10">
      <h2 class="text-3xl font-semibold tracking-tight">最新文章</h2>
      <a href="/posts/" class="text-sm text-[color:var(--color-accent)]">查看全部 →</a>
    </div>

    <!-- Featured -->
    <div class="reveal mb-6">
      <PostCard ... featured={true} />
    </div>

    <!-- Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 stagger-children">
      {recentPosts.map(post => (
        <div class="reveal">
          <PostCard ... />
        </div>
      ))}
    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify cards render correctly with hover effects**

---

## Task 4: Redesign code section on homepage

**Files:**
- Modify: `src/pages/index.astro`

**Design direction:** Instead of two big empty cards, show a compact grid of actual project cards directly on the homepage. More information density, less wasted space.

- [ ] **Step 1: Replace code section with inline project showcase**

```astro
<!-- Code Section — dark alternating background -->
<section class="py-16 sm:py-20 bg-[var(--color-surface)]">
  <div class="max-w-[var(--width-wide)] mx-auto px-6">
    <div class="reveal flex items-baseline justify-between mb-10">
      <h2 class="text-3xl font-semibold tracking-tight">代码库</h2>
      <a href="/code/" class="text-sm text-[color:var(--color-accent)]">查看全部 →</a>
    </div>

    <!-- Show top 4 projects directly as cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 stagger-children">
      {topProjects.map(project => (
        <div class="reveal">
          <ProjectCard ... />
        </div>
      ))}
    </div>
  </div>
</section>
```

Key: Use `bg-[var(--color-surface)]` to create Apple-style light/dark section alternation — this section has a slightly different background, creating visual rhythm.

- [ ] **Step 2: Add query for top 4 projects in frontmatter**

```astro
const topProjects = allProjects.sort((a, b) => a.data.order - b.data.order).slice(0, 4);
```

- [ ] **Step 3: Verify section renders with alternating background**

---

## Task 5: Redesign posts list page

**Files:**
- Modify: `src/pages/posts/index.astro`

**Design direction:** Switch from pure text list to a card grid that's visually richer but still scannable. Better tab design.

- [ ] **Step 1: Redesign category tabs**

Apple-style pill selector instead of underline tabs:

```astro
<div class="flex flex-wrap gap-2 mb-10" id="category-tabs">
  {categories.map((cat) => (
    <button
      class="category-tab px-4 py-2 text-sm font-medium rounded-full border border-[var(--color-border)] text-[color:var(--color-text-secondary)] transition-all hover:text-[color:var(--color-text-primary)] hover:border-[var(--color-text-tertiary)]"
      data-category={cat.id}>
      {cat.zh}
    </button>
  ))}
</div>
```

Active state JS:
```js
tab.classList.add('bg-[var(--color-text-primary)]', 'text-[var(--color-bg)]', 'border-transparent');
```

- [ ] **Step 2: Switch to 2-column card grid for posts**

Instead of text list with dividers, use a 2-column grid of compact PostCards:

```astro
<div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="posts-grid">
  {sortedPosts.map((post) => (
    <div class="post-item" data-category={post.data.category}>
      <PostCard
        title={post.data.title}
        description={post.data.description}
        category={post.data.category}
        date={post.data.date}
        slug={post.id}
      />
    </div>
  ))}
</div>
```

- [ ] **Step 3: Update filter JS to show/hide grid items**

- [ ] **Step 4: Add ecommerce to categoryLabels in this file**

---

## Task 6: Wire ecommerce category fully

**Files:**
- Create: `src/pages/posts/ecommerce.astro`
- Modify: `src/components/Nav.astro` (add to dropdown)
- Modify: `src/i18n/zh.json` and `src/i18n/en.json`
- Modify: `src/pages/posts/[slug].astro` (already has ecommerce in labels ✓)

- [ ] **Step 1: Create ecommerce category page**

Copy the pattern from `stories.astro`, change filter to `'ecommerce'`:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';
const posts = (await getCollection('posts')).filter(p => p.data.category === 'ecommerce').sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
---
<BaseLayout title="电商运营">
  <!-- same structure as other category pages -->
</BaseLayout>
```

- [ ] **Step 2: Add ecommerce to Nav.astro dropdown**

```js
const postCategories = [
  { href: '/posts/reflections/', labelZh: '个人深思', labelEn: 'Reflections' },
  { href: '/posts/web3/', labelZh: 'Web3 相关', labelEn: 'Web3' },
  { href: '/posts/ai/', labelZh: 'AI 相关', labelEn: 'AI' },
  { href: '/posts/stories/', labelZh: '故事集', labelEn: 'Stories' },
  { href: '/posts/ecommerce/', labelZh: '电商运营', labelEn: 'E-commerce' },  // NEW
];
```

- [ ] **Step 3: Add i18n translations**

zh.json: `"ecommerce": "电商运营"`
en.json: `"ecommerce": "E-commerce"`

- [ ] **Step 4: Verify navigation dropdown shows ecommerce and page loads**

---

## Task 7: Improve Footer

**Files:**
- Modify: `src/components/Footer.astro`

- [ ] **Step 1: Redesign footer with navigation columns**

```astro
<footer class="border-t border-[var(--color-border)] bg-[var(--color-surface)]">
  <div class="max-w-[var(--width-wide)] mx-auto px-6 py-16">
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-8 mb-12">
      <!-- Column 1: About -->
      <div>
        <div class="flex items-center gap-2 mb-4">
          <img src="/avatar.jpg" alt="Ocean" class="w-8 h-8 rounded-full object-cover" />
          <span class="font-semibold">Ocean</span>
        </div>
        <p class="text-sm text-[color:var(--color-text-secondary)]"
           data-i18n-zh="找到一个最长的雪坡，滚雪球"
           data-i18n-en="Find the longest slope, roll the snowball">
          找到一个最长的雪坡，滚雪球
        </p>
      </div>

      <!-- Column 2: Posts categories -->
      <div>
        <p class="text-xs font-medium text-[color:var(--color-text-tertiary)] uppercase tracking-wider mb-3">文章</p>
        <nav class="space-y-2">
          <a href="/posts/reflections/" class="block text-sm text-[color:var(--color-text-secondary)] hover:text-[color:var(--color-text-primary)]">个人深思</a>
          <a href="/posts/web3/" class="...">Web3</a>
          <a href="/posts/ai/" class="...">AI</a>
          <a href="/posts/stories/" class="...">故事集</a>
          <a href="/posts/ecommerce/" class="...">电商运营</a>
        </nav>
      </div>

      <!-- Column 3: Code -->
      <div>
        <p class="text-xs font-medium text-[color:var(--color-text-tertiary)] uppercase tracking-wider mb-3">代码库</p>
        <nav class="space-y-2">
          <a href="/code/infra/" class="...">基建相关</a>
          <a href="/code/products/" class="...">产品与工作流</a>
        </nav>
      </div>

      <!-- Column 4: Social + RSS -->
      <div>
        <p class="text-xs font-medium text-[color:var(--color-text-tertiary)] uppercase tracking-wider mb-3">社交</p>
        <nav class="space-y-2">
          <a href="https://x.com/Ocean_Jackon" target="_blank">𝕏 Twitter</a>
          <a href="https://github.com/Oceanjackson1" target="_blank">GitHub</a>
          <a href="/rss.xml" target="_blank">RSS 订阅</a>
        </nav>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="pt-6 border-t border-[var(--color-border)] text-center">
      <p class="text-xs text-[color:var(--color-text-tertiary)]">© Ocean 2026</p>
    </div>
  </div>
</footer>
```

- [ ] **Step 2: Verify footer renders correctly on mobile (2 cols) and desktop (4 cols)**

---

## Task 8: Improve mobile nav animation

**Files:**
- Modify: `src/components/Nav.astro`

- [ ] **Step 1: Add slide-in animation for mobile menu**

Replace `hidden` toggle with CSS transition:

```css
/* In Nav.astro <style> */
#mobile-menu {
  transform: translateY(-10px);
  opacity: 0;
  pointer-events: none;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
              opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
#mobile-menu.open {
  transform: translateY(0);
  opacity: 1;
  pointer-events: auto;
}
```

Update JS:
```js
mobileBtn?.addEventListener('click', () => {
  mobileMenu?.classList.toggle('open');
});
```

- [ ] **Step 2: Verify mobile menu animates smoothly**

---

## Task 9: Refine article detail page

**Files:**
- Modify: `src/pages/posts/[slug].astro`
- Modify: `src/styles/global.css`

- [ ] **Step 1: Add copy button to code blocks**

Add a script at the bottom of the post layout:

```html
<script>
  document.querySelectorAll('.prose pre').forEach((pre) => {
    const btn = document.createElement('button');
    btn.textContent = 'Copy';
    btn.className = 'copy-btn absolute top-3 right-3 text-xs px-2 py-1 rounded-md bg-[var(--color-border)] text-[color:var(--color-text-tertiary)] hover:text-[color:var(--color-text-primary)] transition-colors';
    btn.addEventListener('click', () => {
      const code = pre.querySelector('code');
      navigator.clipboard.writeText(code?.textContent || '');
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = 'Copy', 2000);
    });
    pre.style.position = 'relative';
    pre.appendChild(btn);
  });
</script>
```

- [ ] **Step 2: Add global.css style for copy button**

```css
.copy-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  background: var(--color-border);
  color: var(--color-text-tertiary);
  cursor: pointer;
  border: none;
  transition: color 0.15s, background 0.15s;
}
.copy-btn:hover {
  color: var(--color-text-primary);
}
```

- [ ] **Step 3: Improve TOC styling — highlight active section on scroll**

Add scroll-spy to the TOC:

```html
<script>
  const tocLinks = document.querySelectorAll('#toc a');
  const headings = document.querySelectorAll('#article-content h2, #article-content h3');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          tocLinks.forEach(link => link.classList.remove('text-[color:var(--color-accent)]', 'font-medium'));
          const active = document.querySelector(`#toc a[href="#${entry.target.id}"]`);
          active?.classList.add('text-[color:var(--color-accent)]', 'font-medium');
        }
      });
    },
    { rootMargin: '-80px 0px -60% 0px' }
  );

  headings.forEach(h => observer.observe(h));
</script>
```

- [ ] **Step 4: Verify copy button and TOC highlighting work**

---

## Task 10: Final polish — ProjectCard hover effect

**Files:**
- Modify: `src/components/ProjectCard.astro`

- [ ] **Step 1: Add gradient border glow on hover**

```astro
<div class="group relative p-6 rounded-[var(--radius-card)] bg-[var(--color-surface)] border border-[var(--color-border)] transition-all duration-300 hover:-translate-y-1 hover:shadow-[var(--shadow-card-hover)] hover:border-[color-mix(in_srgb,var(--color-accent)_30%,var(--color-border))]">
  ...
</div>
```

The `hover:border-[color-mix(...)]` creates a subtle accent-tinted border on hover — more refined than generic shadow.

- [ ] **Step 2: Verify hover effect on code page**

---

## Task 11: Build and verify full site

- [ ] **Step 1: Run `npm run build` — should succeed with 0 errors**

- [ ] **Step 2: Run dev server and screenshot all pages (light + dark)**

- [ ] **Step 3: Test mobile viewport (375px width)**

- [ ] **Step 4: Verify all links work (nav dropdowns, category pages, post detail, code pages)**

---

## Summary of Visual Changes

| Before | After |
|--------|-------|
| Centered hero, small avatar | Left-aligned editorial hero, larger avatar, pill social buttons |
| All white sections | Alternating bg colors for visual rhythm |
| Generic bordered cards | Featured card with accent stripe, compact cards for grid |
| Text list for posts | 2-column card grid with pill filter tabs |
| Bare footer (3 icons) | 4-column footer with navigation and branding |
| Broken scroll animations | Reliable reveal system with spring easing |
| No code copy button | Copy button on all code blocks |
| Static TOC | Scroll-spy highlighted TOC |
| No ecommerce page | Full ecommerce category support |
