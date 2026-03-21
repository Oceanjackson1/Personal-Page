---
title: "Sanity Best Practices"
description: "Sanity development best practices for schema design, GROQ queries, TypeGen, Visual Editing, images, Portable Text, Studio structure, localization, migrations, and framework integrations such as Next.js, Nuxt, Astro, Remix, SvelteKit, Angular, Hydr..."
category: "development"
source: "community"
author: "Community"
tags: ["sanity"]
date: 2026-03-20
---

# Sanity Best Practices

Comprehensive best practices and integration guides for Sanity development, maintained by Sanity. Use the quick reference below to load only the one or two topic files that match the task.

## When to Apply

Reference these guidelines when:
- Setting up a new Sanity project or onboarding
- Integrating Sanity with a frontend framework (Next.js, Nuxt, Astro, Remix, SvelteKit, Hydrogen)
- Writing GROQ queries or optimizing performance
- Designing content schemas
- Implementing Visual Editing and live preview
- Working with images, Portable Text, or page builders
- Configuring Sanity Studio structure
- Setting up TypeGen for type safety
- Implementing localization
- Migrating content from other systems
- Building custom apps with the Sanity App SDK
- Managing infrastructure with Blueprints

## Quick Reference

### Integration Guides

- `get-started` - Interactive onboarding for new Sanity projects
- `nextjs` - Next.js App Router, Live Content API, embedded Studio
- `nuxt` - Nuxt integration with @nuxtjs/sanity
- `angular` - Angular integration with @sanity/client, signals, resource API
- `astro` - Astro integration with @sanity/astro
- `remix` - React Router / Remix integration
- `svelte` - SvelteKit integration with @sanity/svelte-loader
- `hydrogen` - Shopify Hydrogen with Sanity
- `project-structure` - Monorepo and embedded Studio patterns
- `app-sdk` - Custom applications with Sanity App SDK
- `blueprints` - Infrastructure as Code with Sanity Blueprints

### Topic Guides

- `groq` - GROQ query patterns, type safety, performance optimization
- `schema` - Schema design, field definitions, validation, deprecation patterns
- `visual-editing` - Presentation Tool, Stega, overlays, live preview
- `page-builder` - Page Builder arrays, block components, live editing
- `portable-text` - Rich text rendering and custom components
- `image` - Image schema, URL builder, hotspots, LQIP, Next.js Image
- `studio-structure` - Desk structure, singletons, navigation
- `typegen` - TypeGen configuration, workflow, type utilities
- `seo` - Metadata, sitemaps, Open Graph, JSON-LD
- `localization` - i18n patterns, document vs field-level, locale management
- `migration` - Content import overview (see also `migration-html-import`)
- `migration-html-import` - HTML to Portable Text with @portabletext/block-tools

## How to Use

Start with the single framework or topic guide that best matches the request, then read additional references only when the task crosses concerns. Use these reference files for detailed explanations and code examples:

```
references/groq.md
references/schema.md
references/nextjs.md
```

Each reference file contains:
- Comprehensive topic or integration coverage
- Incorrect and correct code examples
- Decision matrices and workflow guidance
- Framework-specific patterns where applicable

---

## Reference: Angular

# Angular & Sanity Integration Rules

Jump to the section that matches your Angular version or integration task instead of reading this guide straight through.

## Table of Contents

- Setup and configuration
- Client setup (service pattern)
- Data fetching patterns
- Routing
- Portable Text rendering
- Image optimization
- Modern Angular features
- SSR and prerendering
- Visual Editing
- Error handling

## 1. Setup & Configuration

Use the official template `sanity-template-angular-clean` as a starting point. It provides a monorepo structure:

```
project/
├── angular-app/    # Angular 19+ frontend
└── studio/         # Sanity Studio
```

Install dependencies in the Angular app:

```bash
npm install @sanity/client @sanity/image-url @portabletext/to-html
```

Configure environment files for Sanity credentials:

```typescript
// environments/environment.ts
export const environment = {
  production: false,
  sanity: {
    projectId: 'your-project-id',
    dataset: 'production',
    apiVersion: '2025-05-01',
  },
}
```

```typescript
// environments/environment.production.ts
export const environment = {
  production: true,
  sanity: {
    projectId: 'your-project-id',
    dataset: 'production',
    apiVersion: '2025-05-01',
  },
}
```

> There is no Angular-specific Sanity SDK. Use `@sanity/client` directly, wrapped in an Angular service.

### TypeGen in a Monorepo

Sanity TypeGen generates TypeScript types from your schema and GROQ queries. In the Angular monorepo template, TypeGen runs from the Studio side but scans your Angular app's source files. Ensure `studio/sanity.cli.ts` points at the Angular app:

```typescript
// studio/sanity.cli.ts
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  typegen: {
    enabled: true,
    path: '../angular-app/src/**/*.ts',
    generates: '../angular-app/sanity.types.ts',
  },
})
```

The remaining defaults (`overloadClientMethods: true`, `schema: "schema.json"`) work as-is. Include the generated types file in `angular-app/tsconfig.json` (usually covered by `"include": ["src/**/*.ts", "sanity.types.ts"]`). See `typegen.md` for the full TypeGen workflow, git strategy, and configuration options.

## 2. Client Setup (Service Pattern)

Create an injectable service wrapping `@sanity/client` and `@sanity/image-url`:

```typescript
import { Injectable } from '@angular/core'
import { createClient, type ClientReturn, type QueryParams, type SanityClient } from '@sanity/client'
import imageUrlBuilder, { type ImageUrlBuilder } from '@sanity/image-url'
import type { SanityImageSource } from '@sanity/image-url/lib/types/types'
import { environment } from '../environments/environment'

@Injectable({ providedIn: 'root' })
export class SanityService {
  private client: SanityClient
  private builder: ImageUrlBuilder

  constructor() {
    this.client = createClient({
      projectId: environment.sanity.projectId,
      dataset: environment.sanity.dataset,
      apiVersion: environment.sanity.apiVersion,
      useCdn: true,
    })
    this.builder = imageUrlBuilder(this.client)
  }

  // ClientReturn resolves TypeGen's declaration-merged overloads for defineQuery strings
  fetch<Query extends string>(query: Query, params?: QueryParams): Promise<ClientReturn<Query>> {
    return this.client.fetch(query, params)
  }

  getImageUrlBuilder(source: SanityImageSource) {
    return this.builder.image(source)
  }
}
```

For preview/draft content, create a second client instance with a token and `useCdn: false`. Never expose tokens in client-side bundles — use server-side rendering or a proxy endpoint for authenticated requests.

## 3. Data Fetching Patterns

### A. `resource` API (Angular 19+, Recommended)

The `resource` API works natively with promises and integrates with Angular signals:

```typescript
import { Component, input, resource, inject } from '@angular/core'
import { defineQuery } from 'groq'
import { SanityService } from '../sanity.service'

const POST_QUERY = defineQuery(`*[_type == "post" && slug.current == $slug][0]{
  title, body, mainImage, publishedAt
}`)

@Component({
  selector: 'app-post',
  standalone: true,
  template: `
    @if (post.value(); as p) {
      <h1>{{ p.title }}</h1>
      <time>{{ p.publishedAt | date }}</time>
    } @else if (post.isLoading()) {
      <p>Loading…</p>
    } @else if (post.error()) {
      <p>Error loading post</p>
    }
  `,
})
export default class PostComponent {
  slug = input.required<string>()
  private sanity = inject(SanityService)

  post = resource({
    params: () => ({ slug: this.slug() }),
    loader: ({ params }) => this.sanity.fetch(POST_QUERY, params),
  })
}
```

The `resource` automatically re-fetches when `slug` changes and exposes `value()`, `isLoading()`, and `error()` signals.

> **TypeGen:** Wrapping queries in `defineQuery` enables Sanity TypeGen to infer return types automatically — no manual type imports needed. See `typegen.md` for the full workflow.

### B. `rxResource` (Observable-based)

For teams using RxJS patterns or needing operators like `retry` and `debounceTime`:

```typescript
import { Component, input, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { defineQuery } from 'groq'
import { from } from 'rxjs'
import { SanityService } from '../sanity.service'

const POST_QUERY = defineQuery(`*[_type == "post" && slug.current == $slug][0]`)

@Component({ /* ... */ })
export default class PostComponent {
  slug = input.required<string>()
  private sanity = inject(SanityService)

  post = rxResource({
    params: () => ({ slug: this.slug() }),
    loader: ({ params }) => from(this.sanity.fetch(POST_QUERY, params)),
  })
}
```

### C. `toSignal` (Angular 17–18)

For apps not yet on Angular 19, convert observables to signals:

```typescript
import { Component, inject } from '@angular/core'
import { toSignal } from '@angular/core/rxjs-interop'
import { defineQuery } from 'groq'
import { from } from 'rxjs'
import { SanityService } from '../sanity.service'

const POSTS_QUERY = defineQuery(`*[_type == "post"] | order(publishedAt desc)`)

@Component({ /* ... */ })
export class HomeComponent {
  private sanity = inject(SanityService)
  posts = toSignal(from(this.sanity.fetch(POSTS_QUERY)), { initialValue: [] })
}
```

> **Note:** `toSignal` does not re-fetch on parameter changes. For dynamic queries, use `resource` or `rxResource`.

### Choosing a pattern

| Pattern | Angular Version | Reactivity | Best For |
|---|---|---|---|
| `resource` | 19+ | Signal-based, auto re-fetch | New projects, dynamic queries |
| `rxResource` | 19+ | RxJS + signals | Teams using RxJS operators |
| `toSignal` | 17+ | One-shot conversion | Static queries, legacy apps |

## 4. Routing

Use lazy-loaded routes with `withComponentInputBinding()` so route params bind directly to component inputs:

```typescript
// app.config.ts
import { provideRouter, withComponentInputBinding } from '@angular/router'
import { routes } from './app.routes'

export const appConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding()),
  ],
}
```

```typescript
// app.routes.ts
import { Routes } from '@angular/router'

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home.component'),
    pathMatch: 'full',
  },
  {
    path: 'post/:slug',
    loadComponent: () => import('./post/post.component'),
  },
]
```

With `withComponentInputBinding()`, the `:slug` route param is automatically bound to `slug = input.required<string>()` on the component — no need to inject `ActivatedRoute`.

## 5. Portable Text Rendering

### A. `@portabletext/to-html` with Angular Pipe (Recommended)

```typescript
import { Pipe, PipeTransform, inject } from '@angular/core'
import { toHTML, type PortableTextComponents } from '@portabletext/to-html'
import type { PortableTextBlock } from '@portabletext/types'
import { SanityService } from '../sanity.service'

@Pipe({ name: 'portableTextToHTML', standalone: true })
export class PortableTextToHTMLPipe implements PipeTransform {
  private sanity = inject(SanityService)

  private components: PortableTextComponents = {
    types: {
      image: ({ value }) => {
        const url = this.sanity.getImageUrlBuilder(value).width(800).auto('format').url()
        return `<img src="${url}" alt="${value.alt || ''}" loading="lazy" />`
      },
    },
    marks: {
      link: ({ children, value }) =>
        `<a href="${value.href}" rel="noopener noreferrer">${children}</a>`,
    },
  }

  transform(value: PortableTextBlock[] | undefined): string {
    if (!value) return ''
    return toHTML(value, { components: this.components })
  }
}
```

Usage in templates:

```html
<div [innerHTML]="post.body | portableTextToHTML"></div>
```

### B. `@limitless-angular/sanity` (Community, Component-based)

For full Angular component control over each block type, the community library `@limitless-angular/sanity` provides a component-based Portable Text renderer. This is useful when you need Angular-specific interactivity within rich text blocks.

See `portable-text.md` for Portable Text schema design and serialization rules.

## 6. Image Optimization

Create a pipe wrapping `@sanity/image-url`:

```typescript
import { Pipe, PipeTransform, inject } from '@angular/core'
import type { SanityImageSource } from '@sanity/image-url/lib/types/types'
import { SanityService } from '../sanity.service'

@Pipe({ name: 'sanityImage', standalone: true })
export class SanityImagePipe implements PipeTransform {
  private sanity = inject(SanityService)

  transform(value: SanityImageSource | undefined, width?: number): string | null {
    if (!value) return null
    const builder = this.sanity.getImageUrlBuilder(value)
    if (width) return builder.width(width).auto('format').url()
    return builder.auto('format').url()
  }
}
```

Combine with Angular's `NgOptimizedImage` for LCP images:

```html
<!-- Priority image with NgOptimizedImage -->
<img [ngSrc]="post.mainImage | sanityImage: 1200" width="1200" height="630" priority />

<!-- Lazy-loaded image -->
<img [src]="post.mainImage | sanityImage: 600" [alt]="post.mainImage.alt" loading="lazy" />
```

❌ **Bad:** Fetching full-size images without width constraints.

```html
<img [src]="post.mainImage | sanityImage" />
```

✅ **Good:** Specifying width and using `auto('format')` for WebP/AVIF delivery.

```html
<img [src]="post.mainImage | sanityImage: 800" loading="lazy" />
```

### LQIP with `NgOptimizedImage`

Sanity provides a base64 LQIP (Low Quality Image Placeholder) per image asset — but you must query it explicitly:

```groq
mainImage {
  // @sanity/image-url needs these to build URLs with hotspot/crop support
  asset,
  hotspot,
  crop,
  alt,
  // NgOptimizedImage needs these for placeholder and layout
  "lqip": asset->metadata.lqip,
  "width": asset->metadata.dimensions.width,
  "height": asset->metadata.dimensions.height
}
```

Feed the LQIP directly into `NgOptimizedImage`'s `placeholder` attribute:

```html
<img
  [ngSrc]="post.mainImage | sanityImage: 1200"
  [width]="post.mainImage.width"
  [height]="post.mainImage.height"
  [placeholder]="post.mainImage.lqip"
  [alt]="post.mainImage.alt"
  priority
/>
```

Angular applies a CSS blur to the LQIP and crossfades to the full image on load. No extra libraries needed.

> **Note:** LQIP strings are small (~200 bytes) so they're safe to inline in SSR HTML and `TransferState`. See `image.md` for the full image query patterns.

See `image.md` for image field schema patterns and hotspot/crop configuration.

## 7. Modern Angular Features

When building with Sanity, leverage these Angular 19+ features:

- **Standalone components** — Default in Angular 19. No `NgModule` boilerplate needed.
- **Signals and `resource`** — Preferred over RxJS for data fetching. Simpler, less boilerplate.
- **New control flow** — Use `@if`, `@for`, `@switch` with `@empty` for cleaner templates:

```html
@for (post of posts.value(); track post._id) {
  <app-post-card [post]="post" />
} @empty {
  <p>No posts found.</p>
}
```

- **`@defer` blocks** — Lazy-load below-fold content:

```html
@defer (on viewport) {
  <app-comments [postId]="post._id" />
} @placeholder {
  <p>Scroll to see comments…</p>
}
```

- **`inject()` function** — Preferred over constructor injection for cleaner code.
- **Zoneless change detection** — Experimental in Angular 19. Works well with signals-based data fetching since signals automatically notify the framework of changes.

## 8. SSR & Prerendering

Angular 17+ includes built-in SSR support (replacing Angular Universal):

```typescript
// app.config.server.ts
import { provideServerRendering } from '@angular/platform-server'
import { provideClientHydration } from '@angular/platform-browser'

export const serverConfig = {
  providers: [
    provideServerRendering(),
    provideClientHydration(),
  ],
}
```

Key considerations for Sanity + Angular SSR:

| Feature | Details |
|---|---|
| **Hydration** | `provideClientHydration()` preserves server-rendered DOM. The client reuses it instead of re-rendering. |
| **HTTP Transfer Cache** | Only works with Angular's `HttpClient`. Since `@sanity/client` uses its own HTTP transport, use `TransferState` manually (see below). |
| **Prerendering** | Use `getPrerenderParams` in route config to generate static pages at build time. |

### Transfer State for `@sanity/client`

Angular's built-in HTTP Transfer Cache does not cover `@sanity/client` requests. Without manual transfer, the client re-fetches every query during hydration. Add `TransferState` to the service from Section 2:

```typescript
+ async function hashQuery(query: string, params?: QueryParams): Promise<string> {
+   const input = query + JSON.stringify(params ?? {})
+   const buffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input))
+   return Array.from(new Uint8Array(buffer), b => b.toString(16).padStart(2, '0')).join('')
+ }

import { Injectable, inject } from '@angular/core'
+ import { isPlatformBrowser, isPlatformServer } from '@angular/common'
+ import { PLATFORM_ID, makeStateKey, TransferState } from '@angular/core'
import { createClient, type ClientReturn, type QueryParams, type SanityClient } from '@sanity/client'

export class SanityService {
  private client: SanityClient
+  private transferState = inject(TransferState)
+  private platformId = inject(PLATFORM_ID)

  async fetch<Query extends string>(query: Query, params?: QueryParams): Promise<ClientReturn<Query>> {
+    const key = makeStateKey<ClientReturn<Query>>(await hashQuery(query, params))
+
+    if (isPlatformBrowser(this.platformId)) {
+      const cached = this.transferState.get(key, null)
+      if (cached !== null) {
+        this.transferState.remove(key)
+        return cached
+      }
+    }
+
    const result = await this.client.fetch(query, params)
+
+    if (isPlatformServer(this.platformId)) {
+      this.transferState.set(key, result)
+    }
+
    return result
  }
}
```

The `hashQuery` helper keeps `TransferState` keys short (SHA-256 hex) instead of embedding raw GROQ strings in the serialized HTML.

Prerendering dynamic routes:

```typescript
// app.routes.server.ts
import { RenderMode, ServerRoute } from '@angular/ssr'

export const serverRoutes: ServerRoute[] = [
  {
    path: 'post/:slug',
    renderMode: RenderMode.Prerender,
    async getPrerenderParams() {
      // Fetch all slugs from Sanity at build time
      const client = createClient({ projectId: '...', dataset: '...', apiVersion: '...', useCdn: true })
      const slugs = await client.fetch<string[]>(`*[_type == "post"].slug.current`)
      return slugs.map((slug) => ({ slug }))
    },
  },
  { path: '**', renderMode: RenderMode.Server },
]
```

❌ **Bad:** Using `isPlatformBrowser()` in templates to conditionally render content — causes hydration mismatch.

✅ **Good:** Using `@defer` or `afterNextRender()` for browser-only code.

## 9. Visual Editing

> **Important:** Angular does not have official Sanity Visual Editing support. There is no `@sanity/visual-editing` integration, no Stega encoding, and no click-to-edit overlay for Angular applications. This is unlike Next.js, Nuxt, and SvelteKit which have first-party support.

### Preview Mode (Basic)

For draft content preview, create a separate preview client with an API token:

```typescript
@Injectable({ providedIn: 'root' })
export class SanityService {
  private client: SanityClient
  private previewClient: SanityClient

  constructor() {
    this.client = createClient({
      projectId: environment.sanity.projectId,
      dataset: environment.sanity.dataset,
      apiVersion: environment.sanity.apiVersion,
      useCdn: true,
    })

    this.previewClient = this.client.withConfig({
      useCdn: false,
      token: environment.sanity.previewToken, // Server-side only!
      perspective: 'drafts',
    })
  }

  fetch<Query extends string>(query: Query, params?: QueryParams, preview = false): Promise<ClientReturn<Query>> {
    const client = preview ? this.previewClient : this.client
    return client.fetch(query, params)
  }
}
```

> **Security:** Never expose the preview token in client-side bundles. Use this pattern only with SSR where the token stays on the server, or proxy preview requests through a backend API.

### Community Visual Editing

The community library `@limitless-angular/sanity` provides experimental Visual Editing support for Angular, including overlay click-to-edit functionality. Check its documentation for current status and limitations.

## 10. Error Handling

Common errors when integrating Angular with Sanity:

| Error | Cause | Solution |
|---|---|---|
| `401 Unauthorized` | Invalid or missing API token | Verify token in Sanity management console. Ensure it has correct permissions. |
| `403 Forbidden` | CORS origin not allowed | Add your Angular dev/production URL to CORS origins in `sanity.io/manage`. |
| `422 Invalid query` | GROQ syntax error | Test queries in Vision plugin or Sanity's GROQ playground. See `groq.md`. |
| Hydration mismatch | Conditional rendering based on platform | Use `@defer` or `afterNextRender()` instead of `isPlatformBrowser()` checks. |
| Empty response | Missing dataset or wrong `apiVersion` | Verify environment config. Use a date-based `apiVersion` (e.g., `'2025-05-01'`). |
| Images not loading | Missing `@sanity/image-url` setup | Ensure `getImageUrlBuilder` is called with a valid image reference. See `image.md`. |

For GROQ query patterns and best practices, see `groq.md`. For schema design, see `schema.md`.

---

## Reference: App Sdk

# Sanity App SDK

Build custom React applications that interact with Sanity content in real-time.

## Tech Stack

- **Framework:** React 19+, TypeScript
- **Packages:** `@sanity/sdk`, `@sanity/sdk-react`
- **Optional UI:** `@sanity/ui`, `styled-components`
- **Runtime:** Node.js 20+

## Commands

```bash
# Basic quickstart
npx sanity@latest init --template app-quickstart --organization <your-org-id> --output-path . --typescript --skip-mcp

# With Sanity UI components
npx sanity@latest init --template app-sanity-ui --organization <your-org-id> --output-path . --typescript --skip-mcp

# Start development server
npm run dev

# Deploy to Sanity
npx sanity@latest deploy

# Install Sanity UI
npm install @sanity/ui styled-components
```

## Project Structure

```
my-app/
├── sanity.cli.ts        # CLI config (org ID, entry point)
├── src/
│   ├── App.tsx          # Root component with SanityApp provider
│   ├── App.css          # Global styles
│   └── components/      # Your components
├── package.json
└── tsconfig.json
```

## Boundaries

- **Always:** Wrap data-fetching components in `<Suspense>`, use `documentId` as React `key`, read/write directly to Content Lake (not local state)
- **Always:** Use `useDocuments` for lists, `useDocumentProjection` for display, `useDocument` + `useEditDocument` for editing
- **Ask first:** Before using `useQuery` with raw GROQ (prefer `useDocuments` + `useDocumentProjection`)
- **Ask first:** Before adding multiple data-fetching hooks in a single component
- **Never:** Use `useState` for form values that should sync with Content Lake
- **Never:** Use array index as React `key` for document lists (breaks real-time updates)
- **Never:** Forget the `fallback` prop on `<SanityApp>` and `<Suspense>` boundaries

---

## Configuration

### CLI Config (`sanity.cli.ts`)

```typescript
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  app: {
    organizationId: 'your-org-id',
    entry: './src/App.tsx',
  },
})
```

### App Root (`src/App.tsx`)

```typescript
import { SanityApp, type SanityConfig } from '@sanity/sdk-react'

export default function App() {
  const config: SanityConfig[] = [
    {
      projectId: 'your-project-id',
      dataset: 'production',
    },
  ]

  return (
    <SanityApp config={config} fallback={<div>Loading...</div>}>
      <YourComponents />
    </SanityApp>
  )
}
```

### With Sanity UI

```typescript
import { SanityApp, type SanityConfig } from '@sanity/sdk-react'
import { ThemeProvider } from '@sanity/ui'
import { buildTheme } from '@sanity/ui/theme'

const theme = buildTheme()

export default function App() {
  const config: SanityConfig[] = [
    { projectId: 'your-project-id', dataset: 'production' },
  ]

  return (
    <ThemeProvider theme={theme}>
      <SanityApp config={config} fallback={<div>Loading...</div>}>
        <YourComponents />
      </SanityApp>
    </ThemeProvider>
  )
}
```

### Environment Variables

Prefix with `SANITY_APP_` for automatic bundling:

```bash
SANITY_APP_PROJECT_ID=abc123
SANITY_APP_DATASET=production
```

Access: `process.env.SANITY_APP_PROJECT_ID`

---

## Document Handles

Lightweight references to documents. Fetch handles first, then load content as needed.

```typescript
interface DocumentHandle {
  documentId: string
  documentType: string
  projectId?: string
  dataset?: string
}
```

### Creating Handles

```typescript
// Best: From useDocuments hook
const { data: handles } = useDocuments({ documentType: 'article' })

// Good: With helper (preserves literal types for TypeGen)
import { createDocumentHandle } from '@sanity/sdk'
const handle = createDocumentHandle({
  documentId: 'my-doc-id',
  documentType: 'article',
})

// Good: With as const (preserves literal types)
const handle = {
  documentId: 'my-doc-id',
  documentType: 'article',
} as const
```

---

## Hook Selection

| Hook | Use Case | Returns |
|------|----------|---------|
| `useDocuments` | List of documents (infinite scroll) | Document handles |
| `usePaginatedDocuments` | Paginated lists with page controls | Document handles |
| `useDocument` | Single document, real-time editing | Full document or field |
| `useDocumentProjection` | Specific fields, display only | Projected data |
| `useQuery` | Complex GROQ queries (use sparingly) | Raw query results |

---

## Code Patterns

### Fetching a Document List

```typescript
// Good: Fetch handles, render items with Suspense
import { Suspense } from 'react'
import { useDocuments } from '@sanity/sdk-react'

function ArticleList() {
  const { data, hasMore, loadMore, isPending } = useDocuments({
    documentType: 'article',
    batchSize: 10,
    orderings: [{ field: '_updatedAt', direction: 'desc' }],
  })

  return (
    <>
      <ul>
        {data.map((handle) => (
          <Suspense key={handle.documentId} fallback={<li>Loading...</li>}>
            <ArticleItem {...handle} />
          </Suspense>
        ))}
      </ul>
      {hasMore && (
        <button onClick={loadMore} disabled={isPending}>
          Load More
        </button>
      )}
    </>
  )
}
```

```typescript
// Bad: Over-fetching with raw GROQ, no pagination
function BadArticleList() {
  const { data } = useQuery(`*[_type == "article"]`)
  return data?.map((doc, i) => <li key={i}>{doc.title}</li>)
}
```

### Projecting Content from a Handle

```typescript
// Good: Project only needed fields
import { useDocumentProjection, type DocumentHandle } from '@sanity/sdk-react'

function ArticleItem(handle: DocumentHandle) {
  const { data } = useDocumentProjection({
    ...handle,
    projection: `{
      title,
      "authorName": author->name,
      "imageUrl": image.asset->url
    }`,
  })

  if (!data) return null

  return (
    <li>
      <h2>{data.title}</h2>
      <p>By {data.authorName}</p>
    </li>
  )
}
```

### Real-time Editing

```typescript
// Good: Read and write directly to Content Lake
import { useDocument, useEditDocument, type DocumentHandle } from '@sanity/sdk-react'

function TitleInput(handle: DocumentHandle) {
  const { data: title } = useDocument({ ...handle, path: 'title' })
  const editTitle = useEditDocument({ ...handle, path: 'title' })

  return (
    <input
      type="text"
      value={title ?? ''}
      onChange={(e) => editTitle(e.currentTarget.value)}
    />
  )
}
```

```typescript
// Bad: Local state with submit button - causes stale data
function BadTitleForm(handle: DocumentHandle) {
  const [value, setValue] = useState('')
  const editTitle = useEditDocument({ ...handle, path: 'title' })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    editTitle(value) // Only writes on submit!
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={value} onChange={(e) => setValue(e.target.value)} />
      <button type="submit">Save</button>
    </form>
  )
}
```

### Document Actions

```typescript
import {
  useApplyDocumentActions,
  publishDocument,
  unpublishDocument,
  deleteDocument,
} from '@sanity/sdk-react'

function DocumentActions({ handle }: { handle: DocumentHandle }) {
  const apply = useApplyDocumentActions()

  return (
    <div>
      <button onClick={() => apply(publishDocument(handle))}>Publish</button>
      <button onClick={() => apply(unpublishDocument(handle))}>Unpublish</button>
      <button onClick={() => apply(deleteDocument(handle))}>Delete</button>
    </div>
  )
}
```

---

## Suspense Patterns

The App SDK uses React Suspense. Every data-fetching component must be wrapped.

### One Hook Per Component

```typescript
// Good: Separate fetchers into separate components
function EventsAndVenues() {
  return (
    <>
      <Suspense fallback="Loading events...">
        <EventsList />
      </Suspense>
      <Suspense fallback="Loading venues...">
        <VenuesList />
      </Suspense>
    </>
  )
}

function EventsList() {
  const { data } = useDocuments({ documentType: 'event' })
  return <List items={data} />
}

function VenuesList() {
  const { data } = useDocuments({ documentType: 'venue' })
  return <List items={data} />
}
```

```typescript
// Bad: Multiple fetchers in one component
function BadComponent() {
  const { data: events } = useDocuments({ documentType: 'event' })
  const { data: venues } = useDocuments({ documentType: 'venue' })
  // Both trigger Suspense together, causing unnecessary re-renders
}
```

### Prevent Layout Shift

```typescript
// Good: Fallback matches final component dimensions
const BUTTON_TEXT = 'Open in Studio'

export function OpenInStudio({ handle }: { handle: DocumentHandle }) {
  return (
    <Suspense fallback={<Button text={BUTTON_TEXT} disabled />}>
      <OpenInStudioButton handle={handle} />
    </Suspense>
  )
}

function OpenInStudioButton({ handle }: { handle: DocumentHandle }) {
  const { navigateToStudioDocument } = useNavigateToStudioDocument(handle)
  return <Button onClick={navigateToStudioDocument} text={BUTTON_TEXT} />
}
```

---

## Event Handling

```typescript
import { useDocumentEvent, DocumentEvent } from '@sanity/sdk-react'

function DocumentWatcher(handle: DocumentHandle) {
  useDocumentEvent({
    ...handle,
    onEvent: (event) => {
      switch (event.type) {
        case 'edited':
          console.log('Edited:', event.documentId)
          break
        case 'published':
          console.log('Published:', event.documentId)
          break
        case 'deleted':
          console.log('Deleted:', event.documentId)
          break
      }
    },
  })

  return null
}
```

---

## Multi-Project Apps

```typescript
const config: SanityConfig[] = [
  { projectId: 'project-1', dataset: 'production' },
  { projectId: 'project-2', dataset: 'staging' },
]

// Handles include project/dataset info
const handle: DocumentHandle = {
  documentId: 'doc-123',
  documentType: 'article',
  projectId: 'project-1',
  dataset: 'production',
}
```

---

## Lazy Loading with Refs

```typescript
function LazyContent(handle: DocumentHandle) {
  const ref = useRef(null)

  const { data } = useDocumentProjection({
    ...handle,
    ref, // Only loads when element enters viewport
    projection: '{ title, body }',
  })

  return <div ref={ref}>{data?.title}</div>
}
```

---

## What's NOT Included

The App SDK provides hooks and data stores. You bring:

- UI components (use Sanity UI or your own)
- Router
- Form validation
- Schema validation

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Safari dev issues | Use Chrome or Firefox during development |
| Port 3333 in use | `npm run dev -- --port 3334` |
| Auth errors | `npx sanity@latest logout && npx sanity@latest login` |

---

## Reference: Astro

# Astro & Sanity Integration Rules

## 1. Setup & Configuration

### Configuration (`astro.config.mjs`)
Use the official `@sanity/astro` integration.

```javascript
import { defineConfig } from "astro/config";
import sanity from "@sanity/astro";

export default defineConfig({
  integrations: [
    sanity({
      projectId: "YOUR_PROJECT_ID",
      dataset: "production",
      useCdn: false, // False for static builds
      studioBasePath: "/admin", // If embedding Studio
    }),
  ],
});
```

### Client Type Safety
Enable types in `tsconfig.json`.

```json
{
  "compilerOptions": {
    "types": ["@sanity/astro/module"]
  }
}
```

## 2. Data Fetching

### Basic Fetching
Use `sanityClient` from `sanity:client` in the frontmatter of your `.astro` files.

```astro
---
import { sanityClient } from "sanity:client";
import { defineQuery } from "groq";

const POSTS_QUERY = defineQuery(`*[_type == "post"]{title, slug}`);
const posts = await sanityClient.fetch(POSTS_QUERY);
---
<ul>
  {posts.map(post => <li>{post.title}</li>)}
</ul>
```

### Helper Functions
It's best practice to abstract queries into a utility file (e.g., `src/utils/sanity.ts`).

```typescript
import { sanityClient } from "sanity:client";
import { defineQuery } from "groq";

const POSTS_QUERY = defineQuery(`*[_type == "post" && defined(slug.current)]`);

export async function getPosts() {
  return await sanityClient.fetch(POSTS_QUERY);
}
```

## 3. Portable Text
Use `astro-portabletext` for rendering rich text.

```astro
---
import { PortableText } from "astro-portabletext";
const { body } = Astro.props;
---
<div class="prose">
  <PortableText value={body} />
</div>
```

## 4. Image Handling
Use `@sanity/image-url` to generate optimized image URLs.

```typescript
import imageUrlBuilder from "@sanity/image-url";
import { sanityClient } from "sanity:client";

const builder = imageUrlBuilder(sanityClient);

export function urlFor(source) {
  return builder.image(source);
}
```

## 5. Visual Editing (Live Preview)
Astro handles visual editing slightly differently depending on if you are using Hybrid or Static mode.

### Setup
Ensure `stega` is enabled in your client configuration if you want clickable overlays.

For real-time updates in the presentation tool, you typically need a React component wrapper (since Astro components don't re-render on the client) or use the View Transitions API with a loader.

*Note: The `@sanity/astro` integration is evolving. Check the latest docs for "Visual Editing" support.*

---

## Reference: Blueprints

# Sanity Blueprints

## What is Blueprints?

Blueprints is Sanity's **Infrastructure as Code (IaC)** solution. It lets you define Sanity infrastructure declaratively in code, track it in version control, and deploy it programmatically.

Configure Sanity resources in a Blueprint file and deploy with a single command.

## Mental Model

```
Blueprint (code) → Stack (deployed state) → Resources (real infrastructure)
```

| Concept | What it is |
|---------|------------|
| **Blueprint** | A declarative configuration file (`sanity.blueprint.ts`) that describes your desired infrastructure |
| **Stack** | The deployed, real-world collection of resources managed by Blueprints |
| **Resources** | Individual Sanity components: CORS origins, webhooks, datasets, functions, roles, robots |
| **Operation** | A deployment execution that applies Blueprint changes to resources in a Stack |

### How it works

1. Initialize and edit a Blueprint file describing desired resources
2. Run `sanity blueprints deploy` to apply changes to resources in a Stack
3. Blueprints creates/updates a Stack with your resources
4. The Stack persists — future deploys update it based on Blueprint changes

**Key insight:** The Blueprint is your *intent*. The Stack is *reality*. Blueprints reconciles the two.

## Why use Blueprints?

- **Reproducibility** — Same Blueprint = same infrastructure, every time
- **Version control** — Track infrastructure changes alongside code
- **Automation** — No manual clicking through dashboards
- **Multi-environment** — Spin up dev/staging/prod with consistent configuration
- **Collaboration** — Review infrastructure changes in PRs

## Available Resources

Blueprints can manage these Sanity components:

- Document Functions
- Media Library Asset Functions

More resources are coming soon.

## CLI Commands

```bash
sanity blueprints init <name>    # Initialize a new blueprint project
sanity blueprints info           # Show current stack status and resources
sanity blueprints plan           # Preview changes before deploying
sanity blueprints deploy         # Deploy the blueprint (creates/updates stack)
sanity blueprints config         # Configure the blueprint (edit project and stack)
sanity blueprints logs           # View deployment logs
sanity blueprints doctor         # Check for potential issues
sanity blueprints stacks         # List all stacks for the project
sanity blueprints destroy        # Destroy all resources in the stack
```

## Basic Workflow

### 1. Initialize

```bash
sanity blueprints init my-infra
cd my-infra
sanity blueprints info
```

This creates a `sanity.blueprint.ts` file and links it to a Sanity project.

### 2. Define resources

Edit `sanity.blueprint.ts` to add resources using typed helper functions from `@sanity/blueprints`.

### 3. Preview and deploy

```bash
sanity blueprints plan    # See what will change
sanity blueprints deploy  # Apply changes
```

### 4. Iterate

Modify your Blueprint and redeploy. Blueprints handles creating, updating, or removing resources to match your definition.

## Key Behaviors

- **Additive by default** — New resources in the Blueprint are created
- **Updates in place** — Changed resources are updated when possible
- **Removal = destruction** — Resources removed from the Blueprint are destroyed from the Stack
- **References** — Resources can reference each other (e.g., a webhook can reference a dataset)
- **Rollback on failure** — If a deployment fails partway through, Blueprints attempts to rollback

---

## Reference: Get Started

# Sanity Getting Started Guide

## Overview

Getting started with Sanity follows three phases:
1. **Studio & Schema** — Set up Sanity Studio and define your content model
2. **Content** — Import existing content or generate placeholder content via MCP
3. **Frontend** — Integrate with your application (framework-specific)

## Communication Style

**Keep responses succinct:**

- Tell the user what you did: "Created post schema with title, body, and slug"
- Ask direct questions: "What kind of content are you building?"
- Avoid verbose explanations of what you're about to do
- Don't explain every step unless the user asks

**Examples:**

- **Good**: "Schema deployed. Ready to add some content?"
- **Bad**: "I'm going to deploy your schema to the Content Lake so that the MCP server can recognize your new document types. This will allow..."

---

## Get Started with Sanity (Interactive Guide)

**TRIGGER PHRASE:** When the user says "Get started with Sanity" or similar, follow these steps.

**Before starting:** Let the user know they can pause and resume anytime by saying "Continue Sanity setup".

**RESUME TRIGGER:** If the user says "Continue Sanity setup", check what's already configured:
- Does `sanity.config.ts` exist? → Studio is set up
- Are there files in `schemaTypes/`? → Schema exists
- Is there a frontend framework in `package.json`? → May need integration

Resume from where they left off.

---

## Phase 1: Studio & Schema

### Step 1: Check for Existing Studio

**Look for `sanity.config.ts` or `sanity.cli.ts`:**

**If NO Studio found:**
- Ask: "Want to create a new Sanity Studio?"
- If yes, run:
  ```bash
  npm create sanity@latest -- --template clean --typescript
  ```

**If Studio exists:**
- Read the config to get `projectId` and `dataset`
- Proceed to Step 2

### Step 2: Check for Existing Schema

**Look in `schemaTypes/`, `schemas/`, or `src/sanity/schemaTypes/`:**

**If NO schema found:**
- Ask: "What kind of content are you building? (e.g., Blog, E-commerce, Portfolio)"
- Create appropriate schema types based on their answer
- See `schema.md` for patterns

**If schema exists:**
- Show them what you found
- Ask: "Want to add more content types or modify existing ones?"

**If they want a quick example:**
Create a basic blog schema:
```typescript
// schemaTypes/post.ts
import { defineType, defineField } from 'sanity'

export const post = defineType({
  name: 'post',
  title: 'Post',
  type: 'document',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'slug', type: 'slug', options: { source: 'title' } }),
    defineField({ name: 'body', type: 'array', of: [{ type: 'block' }] }),
  ],
})
```

### Step 3: Deploy Schema

**Required before Phase 2:**

```bash
npx sanity schema deploy
```

This uploads your schema to the Content Lake so MCP tools can work with it.

---

## Phase 2: Content

### Step 1: Check for Existing Content

**Use MCP `query_documents` to check:**
```
*[_type == "post"][0...5]
```

**If content exists:**
- Show them a summary
- Ask: "Want to add more content or move to frontend integration?"

**If NO content:**
- Ask: "Do you want to:
  1. Import existing content (from another CMS, markdown, etc.)
  2. Generate sample content with AI
  3. Skip this and add content manually in the Studio"

### Step 2a: Import Existing Content

If migrating from another CMS or files:
- See `migration.md`
- Use MCP `migrate_content` tool for guidance

### Step 2b: Generate Sample Content (MCP)

Use the Sanity MCP Server:
```
Tool: create_document
Type: post
Content: Create a sample blog post about getting started with Sanity
```

**If MCP fails:** Remind them to run `npx sanity schema deploy` first.

### MCP Setup (If Not Configured)

**Quick start via Sanity CLI:**
```bash
npx sanity@latest mcp configure
```

**Cursor:** [One-click install →](cursor://anysphere.cursor-deeplink/mcp/install?name=Sanity&config=eyJ1cmwiOiJodHRwczovL21jcC5zYW5pdHkuaW8iLCJ0eXBlIjoiaHR0cCJ9Cg==)

Or add to `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "Sanity": {
      "type": "http",
      "url": "https://mcp.sanity.io"
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add Sanity -t http https://mcp.sanity.io --scope user
```

**VS Code:** Command Palette → `MCP: Open User Configuration` → add:
```json
{
  "servers": {
    "Sanity": {
      "type": "http",
      "url": "https://mcp.sanity.io"
    }
  }
}
```

---

## Phase 3: Frontend Integration

### Step 1: Detect Framework

**Check `package.json` dependencies:**

| Dependency | Framework | Rule File |
|------------|-----------|-----------|
| `next` | Next.js | `nextjs.md` |
| `@remix-run/react` or `react-router` | React Router / Remix | `remix.md` |
| `svelte` or `@sveltejs/kit` | SvelteKit | `svelte.md` |
| `nuxt` | Nuxt | `nuxt.md` |
| `astro` | Astro | `astro.md` |

**If NO framework found:**
- Ask: "Which framework are you using, or would you like to create a new app?"
- Guide them to create one or specify their choice

### Step 2: Next.js Integration (Inline)

If Next.js is detected, follow these essential steps:

**Install dependencies:**
```bash
npm install @sanity/client @sanity/image-url @portabletext/react
```

**Create the client (`src/sanity/client.ts`):**
```typescript
import { createClient } from "@sanity/client";

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET!,
  apiVersion: "2026-02-01", // Use current date for new projects
  useCdn: false, // Use API directly for server-side rendering; set true for client-side reads
});
```

**Fetch content in a Server Component:**
```typescript
// app/posts/page.tsx
import { client } from "@/sanity/client";

import { defineQuery } from "groq";

const POSTS_QUERY = defineQuery(`*[_type == "post"]{ _id, title, slug }`);

export default async function PostsPage() {
  const posts = await client.fetch(POSTS_QUERY);

  return (
    <ul>
      {posts.map((post) => (
        <li key={post._id}>
          <a href={`/posts/${post.slug.current}`}>{post.title}</a>
        </li>
      ))}
    </ul>
  );
}
```

**Add environment variables (`.env.local`):**
```
NEXT_PUBLIC_SANITY_PROJECT_ID=your-project-id
NEXT_PUBLIC_SANITY_DATASET=production
```

For advanced patterns (TypeGen, Visual Editing, `defineLive`), see `nextjs.md`.

### Step 3: Other Frameworks

For non-Next.js frameworks, read the corresponding rule file and follow its integration guide:

- **React Router / Remix:** `remix.md`
- **SvelteKit:** `svelte.md`
- **Nuxt:** `nuxt.md`
- **Astro:** `astro.md`

Each rule file contains framework-specific patterns for data fetching, Portable Text rendering, and Visual Editing.

---

## What's Next

Once setup is complete, let the user know:

"You're all set! Here are some things I can help with:

- **Visual Editing** — Click-to-edit in the Presentation tool (`visual-editing.md`)
- **TypeGen** — Type-safe queries with generated types (`typegen.md`)
- **Studio Structure** — Customize the Studio sidebar (`studio-structure.md`)
- **SEO** — Metadata, sitemaps, and Open Graph (`seo.md`)
- **i18n** — Multi-language content (`localization.md`)

Just ask about any of these!"

---

## Environment Variables

### Framework-Specific Prefixes

| Framework | Client-Side Prefix | Example |
|-----------|-------------------|---------|
| Next.js | `NEXT_PUBLIC_` | `NEXT_PUBLIC_SANITY_PROJECT_ID` |
| React Router / Remix | None (use loader) | `SANITY_PROJECT_ID` |
| SvelteKit | `PUBLIC_` | `PUBLIC_SANITY_PROJECT_ID` |
| Nuxt | `NUXT_PUBLIC_` | `NUXT_PUBLIC_SANITY_PROJECT_ID` |
| Astro | `PUBLIC_` | `PUBLIC_SANITY_PROJECT_ID` |

---

## Common Commands

```bash
npx sanity@latest mcp configure  # Configure MCP for your editor
npx sanity dev                   # Start Studio locally
npx sanity schema deploy         # Deploy schema (required for MCP!)
npx sanity deploy                # Deploy Studio to Sanity hosting
npx sanity manage                # Open project settings
npm run typegen                  # Generate TypeScript types
```

---

## Important Notes

- **Be succinct** — Guide step-by-step without over-explaining
- **Check context first** — Read existing files before suggesting changes
- **Don't give up** — If something fails, give the user a way to complete manually
- **Deploy schema early** — MCP tools won't work without it
- **One phase at a time** — Complete each phase before moving to the next

---

## Reference: Groq

# GROQ Query Maintenance & Best Practices

Use this contents list to jump to the query concern you need to solve.

## Table of Contents

- Query definition and imports
- Query fragments
- Expansion patterns
- Maintenance workflow
- Common patterns
- Performance rules
- API version best practices

## 1. Query Definition & Imports

### The `defineQuery` Function
**ALWAYS** wrap GROQ queries in `defineQuery` for TypeGen support. The import location depends on your framework:

```typescript
// Framework-agnostic (Angular, Remix, SvelteKit, Astro, vanilla)
import { defineQuery } from "groq";

// Next.js (re-exported for convenience)
import { defineQuery } from "next-sanity";
```

### Syntax Highlighting
For VS Code syntax highlighting, either:
1. Use the `groq` tagged template (recommended): `groq\`...\``
2. Or prefix with `/* groq */` comment when using `defineQuery`

```typescript
import { defineQuery } from "groq";

// ✅ Option A: groq tag (provides highlighting automatically)
import groq from "groq";
const QUERY = defineQuery(groq`*[_type == "post"]`);

// ✅ Option B: Comment prefix (for plain template literals)
const QUERY = defineQuery(/* groq */ `*[_type == "post"]`);

// ✅ Also valid: Just defineQuery (TypeGen works, but no editor highlighting)
const QUERY = defineQuery(`*[_type == "post"]`);
```

## 2. Query Fragments
Use string interpolation to reuse query logic and keep queries maintainable.

```typescript
// src/sanity/fragments/image.ts
export const imageFragment = /* groq */ `
  asset->{
    _id,
    url,
    metadata { lqip, dimensions }
  },
  alt
`;

// src/sanity/queries/post.ts
import { defineQuery } from "groq";
import { imageFragment } from "../fragments/image";

export const POST_QUERY = defineQuery(/* groq */ `
  *[_type == "post"][0] {
    title,
    mainImage {
      ${imageFragment}
    }
  }
`);
```

## 3. Expansion Patterns (Page Builder)
When building a Page Builder query, expand all potential component types.

**Best Practice:** Use a `pageFields` fragment or similar strategy to keep the main query clean.

```typescript
const pageBuilderExpansion = /* groq */ `
  pageBuilder[] {
    ...,
    _type == "hero" => {
      ...,
      cta[] { link, label }
    },
    _type == "gallery" => {
      images[] { ${imageFragment} }
    }
  }
`;
```

## 4. Maintenance Workflow
When you add a new field or component to the Schema:
1.  **Update the Query:** Add the new field/expansion to the relevant GROQ query immediately.
2.  **Run TypeGen:** If you have `typegen.enabled: true` in `sanity.cli.ts`, types regenerate automatically during `sanity dev`/`sanity build`. Otherwise, run `npm run typegen` manually.
3.  **Verify:** Ensure the new field is available in the generated types.

## 5. Common Patterns

### Ordering
```groq
// Single field
*[_type == "post"] | order(publishedAt desc)

// Multiple fields (tiebreaker)
*[_type == "post"] | order(featured desc, publishedAt desc)

// ⚠️ Order BEFORE slice, not after!
*[_type == "post"] | order(publishedAt desc)[0...10]  // ✅ Correct
*[_type == "post"][0...10] | order(publishedAt desc)  // ❌ Wrong order
```

### Slice Notation
```groq
*[_type == "post"][0]       // Single document (object, not array)
*[_type == "post"][0...5]   // First 5 (exclusive) ← Most common
*[_type == "post"][$start...$end]  // Pagination with params
```

### Default Values with `coalesce()`
```groq
*[_type == "page"]{
  "title": coalesce(seoTitle, title, "Untitled"),
  "image": coalesce(ogImage, mainImage, defaultImage)
}
```

### Conditionals with `select()`
```groq
*[_type == "product"]{
  title,
  "badge": select(
    stock == 0 => "Out of Stock",
    stock < 5 => "Low Stock",
    "In Stock"
  )
}
```

### Aggregation with `count()`
```groq
// Total count
count(*[_type == "post" && defined(slug.current)])

// Count per document
*[_type == "category"]{
  title,
  "postCount": count(*[_type == "post" && references(^._id)])
}
```

### Reverse References
```groq
*[_type == "author"]{
  name,
  "posts": *[_type == "post" && references(^._id)]{ title, slug }
}
```

### Array Filtering
```groq
*[_type == "movie"]{
  title,
  "mainCast": castMembers[role == "lead"]->{name}
}

// Check if value exists in array
*[_type == "post" && "tech" in categories[]->slug.current]
```

### Special Variables
```groq
// ^ = parent document (in nested queries)
*[_type == "author"]{
  name,
  "posts": *[_type == "post" && author._ref == ^._id]
}

// @ = current item (in array operations)
*[_type == "post"]{
  "tagCount": count(tags[@ != null])
}
```

## 6. Performance Rules

### Optimizable vs Non-Optimizable Filters
GROQ uses indexes for **optimizable** filters. Non-optimizable filters scan ALL documents.

| Pattern | Optimizable | Example |
|---------|-------------|---------|
| `_type == "x"` | ✅ Yes | `*[_type == "post"]` |
| `_id == "x"` | ✅ Yes | `*[_id == "abc123"]` |
| `slug.current == $slug` | ✅ Yes | `*[slug.current == "hello"]` |
| `defined(field)` | ✅ Yes | `*[defined(publishedAt)]` |
| `references($id)` | ✅ Yes | `*[references("author-123")]` |
| `field->attr == x` | ❌ No | Resolves reference for every doc |
| `fieldA < fieldB` | ❌ No | Compares two attributes |

**Fix non-optimizable filters by stacking:**
```groq
// Stack optimizable filters FIRST to reduce search space
*[_type == "product" && defined(salePrice) && salePrice < displayPrice]
```

### Avoid Joins in Filters
Reference resolution (`->`) in filters is expensive. Use `_ref` instead:

```groq
// ❌ Slow: Resolves reference for every document
*[_type == "post" && author->name == "Bob Woodward"]

// ✅ Fast: Direct _ref comparison
*[_type == "post" && author._ref == "author-bob-woodward-id"]
```

**When you need dynamic lookups** (don't know the ID upfront):

```groq
// Two-step approach:
// 1. Get the reference ID first
*[_type == "author" && name == "Bob Woodward"][0]._id

// 2. Use that ID in your main query
*[_type == "post" && author._ref == $authorId]

// Or use a subquery (still better than -> in filter):
*[_type == "post" && author._ref in *[_type == "author" && name == "Bob Woodward"]._id]
```

### Merge Repeated Reference Resolutions
Each `->` is a subquery. Don't repeat it:

```groq
// ❌ Slow: Two separate subqueries
*[_type == "category"]{
  "parentTitle": parent->title,
  "parentSlug": parent->slug.current
}

// ✅ Fast: Single subquery, merged
*[_type == "category"]{
  ...(parent->{ "parentTitle": title, "parentSlug": slug.current })
}
```

### Cursor-Based Pagination (Not Deep Slicing)
Deep slices are slow because all skipped docs must be sorted first.

```groq
// ❌ Slow: Must sort and skip 10,000 docs
*[_type == "article"] | order(_id)[10000...10020]

// ✅ Fast: Cursor-based, only fetches 20
*[_type == "article" && _id > $lastId] | order(_id)[0...20]
```

**For custom sort orders**, include the sort field in the cursor:

```groq
// Compound cursor: publishedAt + _id for deterministic pagination
*[_type == "article" && (
  publishedAt < $lastDate || 
  (publishedAt == $lastDate && _id > $lastId)
)] | order(publishedAt desc, _id)[0...20]
```

### Always Project Fields
Always use projections to return only the fields your application needs. Fetching entire documents wastes bandwidth and processing time.

```groq
// ❌ Returns ALL fields including unused ones, metadata, revisions
*[_type == "post"]

// ✅ Only fetch what the component needs
*[_type == "post"]{
  _id,
  title,
  "slug": slug.current,
  publishedAt,
  excerpt
}
```

Apply projections at every level, including nested references:

```groq
*[_type == "post"]{
  title,
  author->{ name, "avatar": image.asset->url },
  categories[]->{ title, "slug": slug.current }
}
```

Use conditional projections for different contexts:

```groq
*[_type == "post"]{
  title,
  slug,
  // Only include body for single post view
  $includeBody == true => { body }
}
```

### Don't Filter/Sort on Projected Values
Computed attributes can't use indexes:

```groq
// ❌ Not optimizable (computed attribute)
*[_type == "person"]{
  "fullName": firstName + " " + lastName
} | order(fullName)

// ✅ Optimizable (original attribute)
*[_type == "person"] | order(firstName, lastName)
```

### Quick Checklist
| Rule | Why |
|------|-----|
| Always project `{ fields }` | Reduces data returned |
| Use `defined()` checks | Filters use indexes |
| Use `$params` not interpolation | Prevents query manipulation + enables caching |
| Order BEFORE slice | `order()[0...N]` not `[0...N] order()` |
| Use `_ref` not `->field` in filters | Avoids expensive joins |
| Merge repeated `->` calls | Single subquery vs many |
| Cursor pagination for deep pages | Avoids sorting entire dataset |

## 7. API Version Best Practices

Always use dated versions (`YYYY-MM-DD`) for consistent behavior:

```typescript
const client = createClient({
  apiVersion: '2026-02-01', // Use current date for new projects
})
```

- **New projects:** Use current date (e.g., `2026-02-01`)
- **Existing projects:** Keep current version unless you need new features
- Dated versions lock behavior; `v1` or `vX` may change unexpectedly

---

## Reference: Hydrogen

# Sanity + Shopify + Hydrogen Rules

**Package:** [`hydrogen-sanity`](https://github.com/sanity-io/hydrogen-sanity) — requires `@shopify/hydrogen >= 2025.5.0`

## 1. Architecture Overview

| Component | Purpose |
|-----------|---------|
| **Shopify** | Product catalog, inventory, checkout (source of truth for commerce) |
| **Sanity Connect** | Syncs Shopify data to Sanity in real-time |
| **Sanity Studio** | Editorial content, rich descriptions, media (enhances Shopify data) |
| **Hydrogen** | React Router 7 front-end optimized for Shopify |

**Project Structure:**
```
./
├── /studio    # Sanity Studio
└── /web       # Hydrogen front-end
```

## 2. Environment Variables

```bash
# web/.env
PUBLIC_STOREFRONT_API_TOKEN="your-public-storefront-token"
PRIVATE_STOREFRONT_API_TOKEN="your-private-storefront-token"
PUBLIC_STORE_DOMAIN="your-store.myshopify.com"
SESSION_SECRET="your-random-session-secret"

# Sanity
SANITY_PROJECT_ID="your-project-id"
SANITY_DATASET="production"
SANITY_API_VERSION="2026-02-01"
SANITY_PREVIEW_TOKEN="your-sanity-viewer-token"  # Viewer token for previews
```

## 3. Sanity Client Setup

### Vite Config
```typescript
// web/vite.config.ts
import {hydrogen} from '@shopify/hydrogen/vite'
import {sanity} from 'hydrogen-sanity/vite'

export default defineConfig({
  plugins: [hydrogen(), sanity()],
})
```

### Context Setup
```typescript
// web/app/lib/context.ts
import {createSanityContext, type SanityContext} from 'hydrogen-sanity'
import {PreviewSession} from 'hydrogen-sanity/preview/session'
import {isPreviewEnabled} from 'hydrogen-sanity/preview'

const sanity = await createSanityContext({
  request,
  cache,
  waitUntil,
  client: {
    projectId: env.SANITY_PROJECT_ID,
    dataset: env.SANITY_DATASET,
    apiVersion: env.SANITY_API_VERSION || '2026-02-01',
    useCdn: true,
    stega: {
      enabled: isPreviewEnabled(env.SANITY_PROJECT_ID, previewSession),
      studioUrl: 'http://localhost:3333',
    }
  },
  preview: {
    token: env.SANITY_PREVIEW_TOKEN,
    session: previewSession,
  }
})
```

### Provider Setup (entry.server.tsx)
```typescript
const {SanityProvider} = context.sanity

const body = await renderToReadableStream(
  <NonceProvider>
    <SanityProvider>
      <ServerRouter context={reactRouterContext} url={request.url} nonce={nonce} />
    </SanityProvider>
  </NonceProvider>,
)
```

### Root Layout (root.tsx)
```typescript
import {Sanity} from 'hydrogen-sanity'

export function Layout({children}) {
  const nonce = useNonce()
  return (
    <html>
      <body>
        {children}
        <Sanity nonce={nonce} />  {/* Required for client-side */}
        <Scripts nonce={nonce} />
      </body>
    </html>
  )
}
```

## 4. Data Fetching

Fetch from **both** Shopify (GraphQL) and Sanity (GROQ). Use `defineQuery` for TypeGen support.

### Recommended: `query` + `Query` component
```typescript
import {defineQuery} from 'groq'
import {Query} from 'hydrogen-sanity'

const PRODUCT_QUERY = defineQuery(`*[_type == "product" && store.slug.current == $handle][0]{ body }`)

// Loader
export async function loader({params, context: {sanity}}: LoaderFunctionArgs) {
  const initial = await context.sanity.query(PRODUCT_QUERY, params)
  return {initial}
}

// Component - auto-enables live preview when active
export default function ProductPage({loaderData}) {
  return (
    <Query query={PRODUCT_QUERY} options={{initial: loaderData.initial}}>
      {(data) => <div>{data?.body}</div>}
    </Query>
  )
}
```

### Alternative methods
| Method | Use Case |
|--------|----------|
| `sanity.query()` + `Query` | Recommended - auto preview mode |
| `sanity.loadQuery()` | Manual loader integration |
| `sanity.fetch()` | No preview needed, lightweight |
| `sanity.client` | Mutations in actions |

### Images
```typescript
import {useImageUrl} from 'hydrogen-sanity'

function Hero({image}) {
  const imageUrl = useImageUrl(image)
  return <img src={imageUrl.width(1200).height(600).url()} />
}
```

**Key Insight:** Shopify fields synced via Sanity Connect are `readOnly`. Use Sanity for editorial enhancements only.

## 5. Visual Editing Setup

### Root Layout
```typescript
// web/app/root.tsx
import {usePreviewMode} from 'hydrogen-sanity/preview'
import {VisualEditing} from 'hydrogen-sanity/visual-editing'

export function Layout({children}: {children?: React.ReactNode}) {
  const previewMode = usePreviewMode()

  return (
    <html>
      <body>
        {children}
        {previewMode ? <VisualEditing action="/api/preview" /> : null}
      </body>
    </html>
  )
}
```

### Preview Route
```typescript
// web/app/routes/api.preview.ts
export {action, loader} from 'hydrogen-sanity/preview/route'
```

### Content Security Policy
```typescript
// web/entry.server.tsx
const {nonce, header, NonceProvider} = createContentSecurityPolicy({
  frameAncestors: isPreviewEnabled ? [studioHostname] : [],
  connectSrc: [
    `https://${projectId}.api.sanity.io`,
    `wss://${projectId}.api.sanity.io`,
  ],
})
```

## 6. Studio: Presentation Tool

```typescript
// studio/sanity.config.ts
import {presentationTool} from 'sanity/presentation'

export default defineConfig({
  plugins: [
    presentationTool({
      resolve: {
        locations: {
          product: defineLocations({
            select: { title: 'store.title', slug: 'store.slug.current' },
            resolve: (doc) => ({
              locations: [
                { title: doc?.title || 'Untitled', href: `/products/${doc?.slug}` },
                { title: 'Products', href: `/collections/all` },
              ],
            }),
          }),
        },
      },
      previewUrl: {
        origin: 'http://localhost:3000',
        previewMode: { enable: '/api/preview' },
      },
    }),
  ],
})
```

## 7. Commands

```bash
# Install dependencies
pnpm add hydrogen-sanity @sanity/client @portabletext/react

# Development (run in separate terminals)
cd studio && pnpm dev    # Studio at localhost:3333
cd web && pnpm dev       # Hydrogen at localhost:3000

# Sanity Manage (CORS, tokens)
pnpm dlx sanity manage
```

## 8. Boundaries

- Always:
  - Query Shopify for commerce data (price, inventory, variants)
  - Query Sanity for editorial content (rich text, custom fields)
  - Use `hydrogen-sanity` package for Visual Editing
  - Add Hydrogen URL to CORS origins in Sanity Manage

- Ask First:
  - Before modifying Sanity Connect sync settings
  - Before changing CSP configuration

- Never:
  - Edit Shopify-synced fields in Sanity (they're `readOnly`)
  - Expose `SANITY_API_TOKEN` to client-side code
  - Query Sanity for commerce data that should come from Shopify

---

## Reference: Image

# Sanity Image Rules

## 1. Schema Definition
**Always** enable `hotspot: true`. This allows editors to control cropping and the focal point.

```typescript
defineField({
  name: 'mainImage',
  title: 'Main Image',
  type: 'image',
  options: {
    hotspot: true // CRITICAL
  },
  fields: [
    defineField({
      name: 'alt',
      type: 'string',
      title: 'Alternative Text',
      validation: rule => rule.required().warning('Alt text is important for SEO')
    })
  ]
})
```

## 2. URL Builder (`urlFor`)
Use the Sanity Image URL Builder to generate optimized URLs (resize, crop, format).

**Setup (`sanity/lib/image.ts`):**
```typescript
import createImageUrlBuilder from '@sanity/image-url'
import { dataset, projectId } from '../env'

const builder = createImageUrlBuilder({ projectId, dataset })

export const urlFor = (source: any) => {
  return builder.image(source)
}
```

**Usage:** The URL builder automatically uses hotspot/crop data when available:
```typescript
const imageUrl = urlFor(mainImage)
  .width(800)
  .height(600)
  .fit('crop')  // Respects hotspot when cropping
  .url()
```

## 3. Next.js Image Component Pattern
Create a reusable `SanityImage` component that handles the `urlFor` logic and `next/image` props.

```typescript
import Image from 'next/image'
import { urlFor } from '@/sanity/lib/image'

interface SanityImageProps {
  value: any // SanityImageSource
  width?: number
  height?: number
  className?: string
  priority?: boolean
}

export function SanityImage({ value, width = 800, height, className, priority }: SanityImageProps) {
  if (!value?.asset) return null

  return (
    <Image
      className={className}
      src={urlFor(value)
        .width(width)
        .height(height || Math.round(width / 1.5)) // Default aspect ratio if no height
        .url()}
      alt={value.alt || ''}
      width={width}
      height={height || Math.round(width / 1.5)}
      priority={priority}
      // Optional: Use LQIP (Low Quality Image Placeholder)
      placeholder={value.asset.metadata?.lqip ? 'blur' : 'empty'}
      blurDataURL={value.asset.metadata?.lqip}
    />
  )
}
```

## 4. Querying Images

**Critical:** LQIP (Low Quality Image Placeholder) is **not automatic**. You must explicitly query it via `asset->{ metadata { lqip } }`.

### Minimal Query (No LQIP)
```groq
mainImage {
  asset->{ _id, url },
  alt
}
```

### Full Query (With LQIP & Dimensions)
```groq
mainImage {
  asset->{
    _id,
    url,
    metadata {
      lqip,                          // Base64 blur placeholder
      dimensions { width, height }   // For aspect ratio
    }
  },
  alt,
  hotspot,  // Include if using hotspot cropping
  crop      // Include if using cropping
}
```

**Why this matters:** Without querying `metadata.lqip`, the `blurDataURL` in your component will be `undefined` and the blur effect won't work.

## 5. Performance Tips
- **Auto Format:** Sanity CDN automatically serves WebP/AVIF if the browser supports it (no need to specify `.format('webp')` manually in most cases, but `next/image` handles this too).
- **Sizing:** Always request the exact size you need using `.width()` and `.height()` in `urlFor`. Don't download a 4000px image for a thumbnail.

---

## Reference: Localization

# Sanity Localization Rules

Use the contents list to jump directly to the localization pattern you need.

## Table of Contents

- Guiding principles
- Terminology
- Locale content type
- Choosing document-level vs field-level localization
- Document-level localization
- Localized singletons
- Field-level localization
- AI-powered translation
- UI enhancement
- Frontend URL best practices

## 1. Guiding Principles

### Priority: Easy Authoring Experience
The structured nature of Sanity schemas and GROQ make it easy to parse localized content for your frontend. **Never** let frontend architecture dictate your localization approach — prioritize the editor experience.

### Avoid Content Duplication
Don't create nearly identical copies with slight differences (e.g., US vs British English). Use Portable Text marks and custom blocks to swap out words or sections as needed.

## 2. Terminology

| Term | Definition |
|------|------------|
| **Internationalization (i18n)** | Designing your frontend to support multiple languages |
| **Localization** | Adapting content for a specific language/region |
| **Language Tag** | Code like `en`, `en-US`, `zh-Hant-TW` (per IETF RFC 5646) |
| **Locale** | A language tag with region info (e.g., `en-US`) |

## 3. Create a Locale Content Type

**Best Practice:** Store locales in Sanity, not just in code. This allows sharing between Studio and frontend.

```typescript
// schemaTypes/locale.ts
import { TranslateIcon } from '@sanity/icons'
import { defineField, defineType } from 'sanity'

export const localeType = defineType({
  name: 'locale',
  icon: TranslateIcon,
  type: 'document',
  fields: [
    defineField({ name: 'name', type: 'string', validation: (r) => r.required() }),
    defineField({ name: 'tag', type: 'string', description: 'IANA tag (en, en-US)', validation: (r) => r.required() }),
    defineField({ name: 'fallback', type: 'reference', to: [{ type: 'locale' }] }),
    defineField({ name: 'default', type: 'boolean' }),
  ],
  preview: { select: { title: 'name', subtitle: 'tag' } },
})
```

**Tip:** Restrict locale editing to admins via Structure by filtering `locale` from non-admin users.

## 4. Choose Your Localization Method

| Content Type | Examples | Recommended Method |
|--------------|----------|-------------------|
| **Structured** (things) | Products, People, Locations, Categories | Field-level |
| **Presentation** (UI) | Pages, Posts, Components | Document-level |

### Decision Questions
1. **Are fields shared across languages?** → Field-level
2. **Should changes be "global" for all locales?** (e.g., reordering components) → Field-level
3. **Is content mostly the same except regional differences?** → Field-level with PT marks
4. **Need to publish language versions independently?** → Document-level

## 5. Document-Level Localization

Use the **@sanity/document-internationalization** plugin.

```bash
npm install @sanity/document-internationalization
```

### Configuration
```typescript
// sanity.config.ts
import { documentInternationalization } from '@sanity/document-internationalization'

export default defineConfig({
  plugins: [
    documentInternationalization({
      // Fetch from Content Lake
      supportedLanguages: (client) =>
        client.fetch(`*[_type == "locale"]{ "id": tag, "title": name }`),
      // Document types to localize
      schemaTypes: ['post', 'page'],
    }),
  ],
})
```

### Add Language Field to Schema
```typescript
// In each schema type listed in schemaTypes
defineField({
  name: 'language',
  type: 'string',
  readOnly: true,
  hidden: true,
})
```

### Initial Value Templates
Pre-set language when creating documents outside the translation UI:

```typescript
// sanity.config.ts
import { template } from 'sanity'

export default defineConfig({
  // ...
  document: {
    newDocumentOptions: (prev, { creationContext }) => {
      // Filter to only show base language in "New document" menu
      // The plugin handles creating translations from there
      return prev.filter((item) =>
        !['post', 'page'].includes(item.templateId) ||
        item.parameters?.language === 'en'
      )
    },
  },
  // Initial value templates for each language
  templates: (prev) => [
    ...prev,
    template.initial({
      id: 'post-en',
      title: 'Post (English)',
      schemaType: 'post',
      parameters: [{name: 'language', type: 'string'}],
      value: ({language}) => ({language}),
    }),
  ],
})
```

### Querying Translated Documents
```groq
// Get document in specific language
*[_type == "post" && language == $locale && slug.current == $slug][0]

// Get all translations via metadata document
*[_type == "translation.metadata" && references($docId)][0] {
  translations[] {
    _key,
    value-> { title, slug, language }
  }
}
```

## 6. Localized Singletons (Homepage per Locale)

For singletons like homepages that need a separate document per locale, combine document-level localization with the singleton pattern.

### Schema Definition

```typescript
// schemaTypes/homePage.ts
import { HomeIcon } from '@sanity/icons'
import { defineType, defineField } from 'sanity'

export const homePageType = defineType({
  name: 'homePage',
  title: 'Home Page',
  type: 'document',
  icon: HomeIcon,
  fields: [
    defineField({
      name: 'language',
      type: 'string',
      readOnly: true,
      hidden: true,
    }),
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'pageBuilder', type: 'pageBuilder' }),
    // ... other fields
  ],
  preview: {
    select: { language: 'language' },
    prepare({ language }) {
      return {
        title: 'Home Page',
        subtitle: language?.toUpperCase() || 'No language',
      }
    },
  },
})
```

### Initial Value Templates

Create templates that pre-set the language for each locale:

```typescript
// sanity.config.ts
import { defineConfig, Template } from 'sanity'

// Define your supported locales
const LOCALES = [
  { id: 'en', title: 'English' },
  { id: 'fr', title: 'French' },
  { id: 'de', title: 'German' },
]

export default defineConfig({
  // ...
  templates: (prev) => {
    // Create a template for each locale
    const homePageTemplates: Template[] = LOCALES.map((locale) => ({
      id: `homePage-${locale.id}`,
      title: `Home Page (${locale.title})`,
      schemaType: 'homePage',
      parameters: [{ name: 'language', type: 'string' }],
      value: { language: locale.id },
    }))

    return [...prev, ...homePageTemplates]
  },
})
```

### Structure: Localized Singleton Helper

Create a helper to show one singleton per locale in the Structure:

```typescript
// src/structure/index.ts
import { StructureBuilder, StructureResolver } from 'sanity/structure'
import { HomeIcon } from '@sanity/icons'

const LOCALES = ['en', 'fr', 'de']

function createLocalizedSingleton(
  S: StructureBuilder,
  typeName: string,
  title: string,
  icon?: React.ComponentType
) {
  return S.listItem()
    .title(title)
    .icon(icon)
    .child(
      S.list()
        .title(title)
        .items(
          LOCALES.map((locale) =>
            S.listItem()
              .title(`${title} (${locale.toUpperCase()})`)
              .icon(icon)
              .child(
                S.document()
                  .schemaType(typeName)
                  .documentId(`${typeName}-${locale}`) // Fixed ID per locale
                  .title(`${title} (${locale.toUpperCase()})`)
              )
          )
        )
    )
}

export const structure: StructureResolver = (S) =>
  S.list()
    .title('Content')
    .items([
      // Localized singletons
      createLocalizedSingleton(S, 'homePage', 'Home Page', HomeIcon),

      S.divider(),

      // Filter localized singletons from default list
      ...S.documentTypeListItems().filter(
        (item) => !['homePage'].includes(item.getId() as string)
      ),
    ])
```

### Querying Localized Singletons

```groq
// Get homepage for specific locale
*[_type == "homePage" && language == $locale][0]{
  title,
  pageBuilder[]{...}
}

// Or by fixed document ID
*[_id == "homePage-" + $locale][0]{...}
```

### Key Points

- **Fixed IDs:** Use `${typeName}-${locale}` pattern for predictable document IDs
- **Initial Value Templates:** Essential for the "New document" menu to work correctly
- **Structure:** Group all locale versions under one list item for cleaner navigation
- **See also:** `studio-structure.md` for more singleton patterns

## 7. Field-Level Localization

Use **sanity-plugin-internationalized-array** (NOT localized objects — they hit attribute limits).

```bash
npm install sanity-plugin-internationalized-array
```

### Configuration
```typescript
// sanity.config.ts
import { internationalizedArray } from 'sanity-plugin-internationalized-array'

export default defineConfig({
  plugins: [
    internationalizedArray({
      languages: (client) =>
        client.fetch(`*[_type == "locale"]{ "id": tag, "title": name }`),
      fieldTypes: ['string', 'text', 'simpleBlockContent'],
    }),
  ],
})
```

### Usage in Schema
```typescript
// The plugin creates types like `internationalizedArrayString`
defineField({
  name: 'jobTitle',
  type: 'internationalizedArrayString', // Localized string field
})
```

### Portable Text Localization
Create a reusable block content type, then add it to `fieldTypes`:

```typescript
// schemaTypes/simpleBlockContent.ts
export default defineType({
  name: 'simpleBlockContent',
  type: 'array',
  of: [
    {
      type: 'block',
      styles: [{ title: 'Normal', value: 'normal' }],
      lists: [],
    },
  ],
})

// sanity.config.ts
fieldTypes: ['string', 'simpleBlockContent']

// In your schema
defineField({
  name: 'bio',
  type: 'internationalizedArraySimpleBlockContent',
})
```

### Querying Internationalized Arrays
```groq
// Get specific locale value
*[_type == "author"][0] {
  "jobTitle": jobTitle[_key == $locale][0].value
}

// With fallback
*[_type == "author"][0] {
  "jobTitle": coalesce(
    jobTitle[_key == $locale][0].value,
    jobTitle[_key == "en"][0].value
  )
}
```

## 8. AI-Powered Translation

Use **@sanity/assist** for automated translations.

```bash
npm install @sanity/assist
```

```typescript
// sanity.config.ts
import { assist } from '@sanity/assist'

export default defineConfig({
  plugins: [
    assist({
      translate: {
        // For document-level localization
        document: {
          languageField: 'language',
        },
        // For field-level localization
        field: {
          languages: (client) =>
            client.fetch(`*[_type == "locale"]{ "id": tag, "title": name }`),
          documentTypes: ['author', 'category'],
        },
      },
    }),
  ],
})
```

## 9. UI Enhancement

Use **@sanity/language-filter** to let editors show/hide locales:

```bash
npm install @sanity/language-filter
```

## 10. Frontend URL Best Practices

**Always include locale in the URL** for SEO:
- `yoursite.com/en/my-page` → `yoursite.com/fr/my-page`
- `yoursite.com/my-page` → redirects to default locale

**Avoid:** Having the default locale at root without prefix — causes SEO edge cases.

Use Next.js middleware (or framework equivalent) to redirect paths missing a locale prefix to the default locale.

---

## Reference: Migration Html Import

## Import HTML to Portable Text

Use `@portabletext/block-tools` with `JSDOM` to convert HTML from legacy CMSs to Portable Text.

### Setup

```bash
npm install @portabletext/block-tools jsdom
```

### Basic Conversion

```typescript
import { htmlToBlocks } from '@portabletext/block-tools'
import { JSDOM } from 'jsdom'

// Get block content type from your schema
const blockContentType = schema.get('blockContent')

const blocks = htmlToBlocks(htmlString, blockContentType, {
  parseHtml: html => new JSDOM(html).window.document,
})
```

### Custom Deserializers

Handle specific HTML patterns:

```javascript
const blocks = htmlToBlocks(htmlString, blockContentType, {
  parseHtml: html => new JSDOM(html).window.document,
  rules: [
    {
      deserialize(el, next, block) {
        // Custom link handling
        if (el.tagName.toLowerCase() === 'a') {
          return {
            _type: 'link',
            href: el.getAttribute('href'),
            blank: el.getAttribute('target') === '_blank'
          }
        }
        // Custom image handling
        if (el.tagName.toLowerCase() === 'img') {
          return {
            _type: 'image',
            // Upload image separately, store reference
            _sanityAsset: `image@${el.getAttribute('src')}`
          }
        }
        return undefined  // Fall through to default handling
      }
    }
  ]
})
```

### Pre-Processing HTML

Clean HTML before conversion:

```javascript
function cleanHtml(html) {
  const dom = new JSDOM(html)
  const doc = dom.window.document
  
  // Remove layout elements
  doc.querySelectorAll('header, footer, nav, .sidebar').forEach(el => el.remove())
  
  // Extract metadata before processing body
  const title = doc.querySelector('title')?.textContent
  const description = doc.querySelector('meta[name="description"]')?.content
  
  return {
    body: doc.body.innerHTML,
    metadata: { title, description }
  }
}
```

### Image Upload

Don't just link external images—upload them:

```javascript
async function uploadImage(client, imageUrl) {
  const response = await fetch(imageUrl)
  const buffer = await response.arrayBuffer()
  
  const asset = await client.assets.upload('image', Buffer.from(buffer), {
    filename: imageUrl.split('/').pop()
  })
  
  return {
    _type: 'image',
    asset: { _type: 'reference', _ref: asset._id }
  }
}
```

### Using in a Migration

Wrap this in `defineMigration` for reproducible imports:

```typescript
// migrations/import-wordpress-posts/index.ts
import {defineMigration, createOrReplace} from 'sanity/migrate'
import {htmlToBlocks} from '@portabletext/block-tools'

export default defineMigration({
  title: 'Import WordPress posts',
  async *migrate(documents, context) {
    const posts = await fetchWordPressPosts() // Your import source
    
    for (const post of posts) {
      const blocks = htmlToBlocks(post.content, blockContentType, {
        parseHtml: html => new JSDOM(html).window.document,
      })
      
      yield createOrReplace({
        _id: `post-${post.slug}`,
        _type: 'post',
        title: post.title,
        body: blocks,
      })
    }
  }
})
```

Run with: `sanity migration run import-wordpress-posts --no-dry-run`

Reference: [Schema and Content Migrations](https://www.sanity.io/docs/content-lake/schema-and-content-migrations)

---

## Reference: Migration

# Sanity Content Migration Rules

## 1. HTML Import (Legacy CMS)
Use `@portabletext/block-tools` with `JSDOM` to convert HTML to Portable Text. This covers setup, custom deserializers, pre-processing, image uploads, and wrapping in `defineMigration`.

**See `migration-html-import.md` for the full guide with working examples.**

## 2. Markdown Import (Static Sites)
Use `@sanity/block-content-to-markdown` (legacy name, often used in reverse) OR use a dedicated parser like `remark` to convert Markdown to HTML, then use `block-tools`.

**Recommended Path: Markdown -> HTML -> Portable Text**
This is often more robust than direct Markdown-to-PT parsers because `block-tools` handles schema validation better.

1.  **Parse:** `marked` or `remark` to convert MD to HTML.
2.  **Convert:** Use `htmlToBlocks` (see above).

**Alternative: Direct Parsing**
If using a library like `markdown-to-sanity` or writing a custom `remark` serializer:
-   Ensure you handle "inline" vs "block" nodes correctly.
-   Map images to Sanity asset uploads.

## 3. Image Handling (Universal)
Don't just link to external images. Download them and upload to Sanity Asset Pipeline.

1.  **Extract:** Find `<img>` tags or Markdown image syntax.
2.  **Download:** Fetch the image buffer.
3.  **Upload:** `client.assets.upload('image', buffer)`
4.  **Replace:** Return a Sanity Image block with the new asset reference.

## 4. Schema Validation
Ensure your destination schema allows the structures you are importing.
-   **Tables:** Need a `table` type (HTML `<table>` or GFM tables).
-   **Code:** Need a `code` type (HTML `<pre><code>` or MD code fences).

---

## Reference: Nextjs

# Next.js & Sanity Integration Rules

Jump to the section that matches the task instead of reading this guide end-to-end.

## Table of Contents

- Architecture patterns
- Data fetching (Live Content API)
- Caching and revalidation
- Visual Editing and clean data
- Embedded Studio setup
- Draft Mode setup
- Error handling
- Presentation queries
- Pagination pattern

## 1. Architecture Patterns

### Option A: Embedded Studio (Recommended)
**Best for:** Most Next.js projects. Unified deployment, simpler setup.

The Studio lives inside your Next.js app at `/app/studio/[[...tool]]/page.tsx`.
- **Config:** `sanity.config.ts` lives in the project root.
- See `project-structure.md` rule for detailed structure.

### Option B: Monorepo (Alternative)
**Best for:** Separation of concerns, multiple frontends, or strict dependency isolation.

The Studio and Next.js app live in separate folders:
```
apps/
├── studio/     # Sanity Studio (standalone)
└── web/        # Next.js frontend
```

- **Config:** Add your Next.js app URL to **CORS Origins** in Sanity project settings.
- See `project-structure.md` rule for detailed structure.

## 2. Data Fetching (Live Content API)

We use `defineLive` (next-sanity v11+) to enable real-time content updates and Visual Editing automatically.

### Setup (`src/sanity/lib/live.ts`)

```typescript
import { defineLive } from 'next-sanity'
import { client } from './client'

export const { sanityFetch, SanityLive } = defineLive({
  client: client.withConfig({
    apiVersion: '2026-02-01'
  }),
  serverToken: process.env.SANITY_API_READ_TOKEN,
  browserToken: process.env.SANITY_API_READ_TOKEN,
})
```

### Rendering (`src/app/layout.tsx`)

You **must** render `<SanityLive />` in the root layout to enable real-time updates.

```typescript
import { SanityLive } from '@/sanity/lib/live'
import { VisualEditing } from 'next-sanity/visual-editing'
import { draftMode } from 'next/headers'

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <SanityLive />
        {(await draftMode()).isEnabled && <VisualEditing />}
      </body>
    </html>
  )
}
```

## 3. Caching & Revalidation

### Prefer Live Content API (Default)

**Use `defineLive` by default.** It handles fetching, caching, and invalidation automatically. Only implement manual caching when you need fine-grained control.

### When to Use Manual Caching

| Scenario | Approach |
|----------|----------|
| Real-time updates, Visual Editing | `defineLive` (default) |
| Static marketing pages, rarely updated | Time-based revalidation |
| Blog posts, products with frequent edits | Tag-based revalidation |
| Critical accuracy (stock levels, prices) | Path-based + short revalidation |

### Debugging: Enable Fetch Logging

See every fetch with cache HIT/MISS status:

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
};
```

Console output shows cache status:
```text
GET /posts 200 in 39ms
 │ GET https://...apicdn.sanity.io/... 200 in 5ms (cache hit)
```

### Sanity CDN vs API

| Setting | Speed | Freshness | Use When |
|---------|-------|-----------|----------|
| `useCdn: true` | Fast | May have brief delay | Default for all runtime fetches |
| `useCdn: false` | Slower | Guaranteed fresh | `generateStaticParams`, webhooks |

Override per-request:
```typescript
// For static generation, use API directly
export async function generateStaticParams() {
  const slugs = await client
    .withConfig({ useCdn: false })
    .fetch(SLUGS_QUERY);
  return slugs;
}
```

### Manual `sanityFetch` Helper (Advanced)

For manual caching control, create a wrapper:

```typescript
// src/sanity/lib/client.ts
export async function sanityFetch<const QueryString extends string>({
  query,
  params = {},
  revalidate = 60,
  tags = [],
}: {
  query: QueryString;
  params?: QueryParams;
  revalidate?: number | false;
  tags?: string[];
}) {
  return client.fetch(query, params, {
    next: {
      revalidate: tags.length ? false : revalidate,
      tags,
    },
  });
}
```

### Time-Based Revalidation

Simple and predictable. Good for content that changes infrequently.

```typescript
const posts = await sanityFetch({
  query: POSTS_QUERY,
  revalidate: 3600, // Revalidate every hour
});
```

**The "Typo Problem":** With time-based only, content authors may wait up to an hour to see changes. Use webhooks for instant updates.

### Path-Based Revalidation

Surgically revalidate specific routes when documents change.

**1. Create API Route:**
```typescript
// src/app/api/revalidate/path/route.ts
import { revalidatePath } from 'next/cache';
import { type NextRequest, NextResponse } from 'next/server';
import { parseBody } from 'next-sanity/webhook';

type WebhookPayload = { path?: string };

export async function POST(req: NextRequest) {
  try {
    const { isValidSignature, body } = await parseBody<WebhookPayload>(
      req,
      process.env.SANITY_REVALIDATE_SECRET,
      true // Add delay to allow CDN to update
    );

    if (!isValidSignature) {
      return new Response('Invalid signature', { status: 401 });
    }
    if (!body?.path) {
      return new Response('Missing path', { status: 400 });
    }

    revalidatePath(body.path);
    return NextResponse.json({ revalidated: body.path });
  } catch (err) {
    return new Response((err as Error).message, { status: 500 });
  }
}
```

**2. Create GROQ-Powered Webhook:**
- URL: `https://yoursite.com/api/revalidate/path`
- Filter: `_type in ["post"]`
- Projection: `{ "path": "/posts/" + slug.current }`
- Add `SANITY_REVALIDATE_SECRET` to webhook and `.env.local`

### Tag-Based Revalidation

"Update once, revalidate everywhere" — best for referenced content.

**1. Tag Your Queries:**
```typescript
// Posts index - revalidate when ANY post, author, or category changes
const posts = await sanityFetch({
  query: POSTS_QUERY,
  tags: ['post', 'author', 'category'],
});

// Individual post - more granular, includes slug-specific tag
const post = await sanityFetch({
  query: POST_QUERY,
  params,
  tags: [`post:${params.slug}`, 'author', 'category'],
});
```

**2. Create API Route:**
```typescript
// src/app/api/revalidate/tag/route.ts
import { revalidateTag } from 'next/cache';
import { type NextRequest, NextResponse } from 'next/server';
import { parseBody } from 'next-sanity/webhook';

type WebhookPayload = { tags: string[] };

export async function POST(req: NextRequest) {
  try {
    const { isValidSignature, body } = await parseBody<WebhookPayload>(
      req,
      process.env.SANITY_REVALIDATE_SECRET,
      true
    );

    if (!isValidSignature) {
      return new Response('Invalid signature', { status: 401 });
    }
    if (!Array.isArray(body?.tags) || !body.tags.length) {
      return new Response('Missing tags', { status: 400 });
    }

    body.tags.forEach((tag) => revalidateTag(tag));
    return NextResponse.json({ revalidated: body.tags });
  } catch (err) {
    return new Response((err as Error).message, { status: 500 });
  }
}
```

**3. Create GROQ-Powered Webhook:**
- URL: `https://yoursite.com/api/revalidate/tag`
- Filter: `_type in ["post", "author", "category"]`
- Projection: `{ "tags": [_type, _type + ":" + slug.current] }`

### Stale Data After Webhook?

Webhooks fire *before* Sanity CDN updates. If you see stale data:

1. **Add delay** — Pass `true` as third arg to `parseBody`
2. **Or bypass CDN** — Set `useCdn: false` in client config (use sparingly)

## 4. Visual Editing (Stega) & Clean Data

Visual Editing injects invisible characters into strings to enable click-to-edit.

### A. The Golden Rule of Stega

If a string field controls logic (alignment, colors, IDs), you **must** clean it before comparing.

```typescript
import { stegaClean } from "@sanity/client/stega";

export function Layout({ align }: { align: string }) {
  // ❌ Bad: Will fail in Edit Mode due to invisible chars
  // if (align === 'center') ...

  // ✅ Good: Clean the value first
  const cleanAlign = stegaClean(align);
  return <div className={cleanAlign === 'center' ? 'mx-auto' : ''} />
}
```

### B. Metadata & SEO (Critical)

**Never** let Stega characters leak into `<head>` tags. Always set `stega: false` for metadata fetching.

```typescript
export async function generateMetadata({ params }) {
  const { data } = await sanityFetch({
    query: SEO_QUERY,
    params: await params,
    stega: false // 👈 Critical for SEO
  })
  return { title: data?.title }
}
```

### C. Static Params

When generating static params, fetch only published content and disable stega.

```typescript
export async function generateStaticParams() {
  const { data } = await sanityFetch({
    query: SLUGS_QUERY,
    perspective: 'published', // 👈 No drafts
    stega: false
  })
  return data
}
```

## 5. Setup: Embedded Studio

Mount the Studio on a Next.js route.

**`src/app/studio/[[...tool]]/page.tsx`:**

```typescript
import { NextStudio } from 'next-sanity/studio'
import config from '../../../../sanity.config'

export const dynamic = 'force-static'
export { metadata, viewport } from 'next-sanity/studio'

export default function StudioPage() {
  return <NextStudio config={config} />
}
```

## 6. Setup: Draft Mode

Enable Presentation Tool and Visual Editing by setting up a draft mode route.

**`src/app/api/draft-mode/enable/route.ts`:**

```typescript
import { client } from '@/sanity/lib/client'
import { defineEnableDraftMode } from 'next-sanity/draft-mode'
import { token } from '@/sanity/lib/token' // Helper to get token

export const { GET } = defineEnableDraftMode({
  client: client.withConfig({ token }),
})
```

## 7. Error Handling

Use `notFound()` for missing documents. Common errors:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/missing token | Check `SANITY_API_READ_TOKEN` |
| 403 Forbidden | CORS not configured | Add URL to CORS origins |
| Query syntax error | Invalid GROQ | Test in Vision plugin first |
| Empty result | Wrong filter/params | Log params, check `_type` spelling |

```typescript
import { notFound } from 'next/navigation'

export default async function PostPage({ params }: Props) {
  const { data } = await sanityFetch({ query: POST_QUERY, params: await params })
  if (!data) notFound()
  return <Post data={data} />
}
```

## 8. Presentation Queries (`usePresentationQuery`)

For faster live editing in the Presentation Tool, use `usePresentationQuery` to fetch only the specific block being edited, rather than re-rendering the entire page.

### Why Use This

- **Without:** Editing a hero title re-fetches the whole page, re-renders all blocks
- **With:** Only the hero block re-fetches and re-renders

This is especially valuable for pages with many Page Builder blocks or complex Portable Text.

### Basic Pattern

```typescript
'use client'
import { usePresentationQuery } from 'next-sanity/hooks'
import { HERO_PRESENTATION_QUERY } from '@/sanity/lib/queries'

type HeroProps = {
  _key: string
  documentId: string
  title: string
  subtitle?: string
  // ... other initial props from page query
}

export function Hero({ _key, documentId, title, subtitle, ...rest }: HeroProps) {
  // Fetch block-specific data for faster updates in Presentation Tool
  const { data } = usePresentationQuery({
    query: HERO_PRESENTATION_QUERY,
    params: { documentId, blockKey: _key },
  })

  // Use presentation data if available, fallback to initial server props
  const blockData = data?.heroBlock || { title, subtitle, ...rest }

  return (
    <section>
      <h1>{blockData.title}</h1>
      {blockData.subtitle && <p>{blockData.subtitle}</p>}
    </section>
  )
}
```

### The Presentation Query

Create a query that targets the specific block by `_key`:

```typescript
// queries.ts
export const HERO_PRESENTATION_QUERY = defineQuery(`
  *[_id == $documentId][0]{
    _id,
    _type,
    "heroBlock": pageBuilder[_key == $blockKey && _type == "hero"][0]{
      title,
      subtitle,
      image,
      theme,
      // Include all fields the component needs
    }
  }
`)
```

### Passing Document Context

Your PageBuilder component needs to pass `documentId` to each block:

```typescript
export function PageBuilder({ content, documentId }: { content: Block[]; documentId: string }) {
  return (
    <main>
      {content.map((block) => {
        switch (block._type) {
          case "hero":
            return <Hero key={block._key} documentId={documentId} {...block} />
          // ... other blocks
        }
      })}
    </main>
  )
}
```

### For Portable Text Blocks

The same pattern works for custom blocks inside Portable Text:

```typescript
export const PTE_IMAGE_PRESENTATION_QUERY = defineQuery(`
  *[_id == $documentId][0]{
    "pteImageBlock": body[_key == $blockKey && _type == "pteImage"][0]{
      image,
      caption,
      alt
    }
  }
`)
```

**See also:** `visual-editing.md` for the conceptual overview and `page-builder.md` for full Page Builder patterns.

## 9. Pagination Pattern

For listing pages with many entries, use offset-based pagination with a count query.

### Queries
```typescript
// Paginated listing
export const ARTICLES_QUERY = defineQuery(`
  *[_type == "article" && defined(slug.current)]
  | order(date desc) [$start...$end] {
    _id, title, "slug": slug.current, date
  }
`);

// Total count for pagination UI
export const ARTICLES_COUNT_QUERY = defineQuery(`
  count(*[_type == "article" && defined(slug.current)])
`);
```

### Listing Page
```typescript
const ENTRIES_PER_PAGE = 10;

export default async function BlogPage({
  searchParams
}: {
  searchParams: Promise<{ page?: string }>
}) {
  const { page: pageParam } = await searchParams;
  const page = parseInt(pageParam || "1");
  const start = (page - 1) * ENTRIES_PER_PAGE;
  const end = start + ENTRIES_PER_PAGE;

  const [{ data: articles }, { data: total }] = await Promise.all([
    sanityFetch({ query: ARTICLES_QUERY, params: { start, end } }),
    sanityFetch({ query: ARTICLES_COUNT_QUERY })
  ]);

  const totalPages = Math.ceil(total / ENTRIES_PER_PAGE);

  return (
    <main>
      {articles.map(article => (
        <ArticleCard key={article._id} article={article} />
      ))}
      <Pagination current={page} total={totalPages} />
    </main>
  );
}
```

---

## Reference: Nuxt

# Nuxt & Sanity Integration Rules

## 1. Setup & Configuration

### Configuration (`nuxt.config.ts`)
Use the official `@nuxtjs/sanity` module.

**Important:** Ensure the `minimal` client is NOT enabled if you want full features.

```typescript
export default defineNuxtConfig({
  modules: ["@nuxtjs/sanity"],
  sanity: {
    projectId: process.env.NUXT_SANITY_PROJECT_ID,
    dataset: process.env.NUXT_SANITY_DATASET,
    apiVersion: "2026-02-01",
    // Live Visual Editing Configuration
    visualEditing: {
      studioUrl: process.env.NUXT_SANITY_STUDIO_URL,
      token: process.env.NUXT_SANITY_API_READ_TOKEN, // Required for fetching drafts
      stega: true, // Enable stega for visual editing
      mode: 'live-visual-editing', // Default: enables live updates
    },
  },
});
```

## 2. Data Fetching

### `useSanityQuery`
Use the composable provided by the module for reactive fetching. It automatically handles preview state when configured.

```vue
<script setup lang="ts">
const query = groq`*[_type == "post"]{title, slug}`;
const { data: posts } = await useSanityQuery(query);
</script>

<template>
  <ul>
    <li v-for="post in posts" :key="post._id">{{ post.title }}</li>
  </ul>
</template>
```

## 3. Visual Editing (Live Preview)

### Automatic Setup
When `visualEditing` is configured in `nuxt.config.ts`, the module handles:
1.  Injecting the Visual Editing overlays.
2.  Refreshing data when content changes in the Studio.
3.  Enabling Stega encoding.

### Handling Stega in Logic
Just like Next.js, if you use stega-encoded strings in logic (e.g. `v-if="post.layout === 'full'"`), you must clean them.

```typescript
import { stegaClean } from "@sanity/client/stega";

const layout = computed(() => stegaClean(props.layout));
```

## 4. Components

### Portable Text
Use the `<PortableText>` component (if installed via `@portabletext/vue` or provided by the module).

```vue
<PortableText :value="post.body" :components="customComponents" />
```

### Images
Use `@sanity/image-url` helper or a dedicated image component.

```typescript
import imageUrlBuilder from '@sanity/image-url'
const builder = imageUrlBuilder(useSanity().client)
// ... url generation logic
```

---

## Reference: Page Builder

# Sanity Page Builder Patterns

This guide covers **Page Builder** patterns—arrays of block objects that allow content teams to compose flexible page layouts. For Portable Text (rich text within documents), see `portable-text.md`.

## 1. What is a Page Builder?

A page builder is an **array of objects** (`pageBuilder[]`) that allows content teams to compose pages from reusable blocks without developer intervention.

**When to use:**
- Flexible layouts needed (marketing pages, landing pages)
- Content can be reordered
- Different components on different pages

**When NOT to use:**
- Rigid, formulaic content (blog posts, product pages)
- Highly structured data that doesn't change layout
- Rich text within a document body—use Portable Text instead

## 2. Schema Organization

### Directory Structure
```
schemaTypes/
├── blocks/           # Page builder blocks (objects)
│   ├── heroType.ts
│   ├── featuresType.ts
│   └── faqsType.ts
├── pageBuilderType.ts  # The array definition
└── pageType.ts         # Document using the page builder
```

### Objects vs References

| Use **Objects** | Use **References** |
|-----------------|-------------------|
| Content is unique to this page | Content reused across many pages |
| Simpler queries | Needs central management |
| Default choice | FAQs, CTAs, testimonials |

**Rule:** Use references sparingly. Most blocks should be objects.

### Page Builder Array
```typescript
// pageBuilderType.ts
import { defineType, defineArrayMember } from "sanity";

export const pageBuilderType = defineType({
  name: "pageBuilder",
  type: "array",
  of: [
    defineArrayMember({ type: "hero" }),
    defineArrayMember({ type: "splitImage" }),
    defineArrayMember({ type: "features" }),
    defineArrayMember({ type: "faqs" }),
  ],
  options: {
    insertMenu: {
      views: [
        // Optional: Show visual thumbnails in the insert menu grid
        { name: "grid", previewImageUrl: (type) => `/block-previews/${type}.png` },
      ],
    },
  },
});
```

### Block Preview Pattern
Every block should have consistent previews:

```typescript
import { defineType } from "sanity";
import { BlockContentIcon } from "@sanity/icons";

export const splitImageType = defineType({
  name: "splitImage",
  type: "object",
  icon: BlockContentIcon,
  fields: [/* ... */],
  preview: {
    select: { title: "title", media: "image" },
    prepare({ title, media }) {
      return {
        title: title || "Untitled",
        subtitle: "Split Image", // Block type name
        media: media ?? BlockContentIcon, // Fallback to icon
      };
    },
  },
});
```

## 3. Querying Page Builders

Expand references only for blocks that need them:

```groq
*[_type == "page" && slug.current == $slug][0]{
  ...,
  content[]{
    ...,
    _type == "faqs" => {
      ...,
      faqs[]->  // Expand only FAQ references
    }
  }
}
```

## 4. Rendering Page Builders

### TypeScript Typing
Use `Extract` to type individual blocks from the query result:

```typescript
import { PAGE_QUERYResult } from "@/sanity/types";

type HeroProps = Extract<
  NonNullable<NonNullable<PAGE_QUERYResult>["content"]>[number],
  { _type: "hero" }
>;

export function Hero({ title, image }: HeroProps) {
  // Fully typed!
}
```

### Switch-Based Rendering
```typescript
export function PageBuilder({ content }: { content: Block[] }) {
  if (!Array.isArray(content)) return null;

  return (
    <main>
      {content.map((block) => {
        switch (block._type) {
          case "hero":
            return <Hero key={block._key} {...block} />;
          case "features":
            return <Features key={block._key} {...block} />;
          case "splitImage":
            return <SplitImage key={block._key} {...block} />;
          default:
            return <div key={block._key}>Unknown: {block._type}</div>;
        }
      })}
    </main>
  );
}
```

**Always use `_key` for React keys:**
```typescript
// Breaks Visual Editing and causes hydration issues
{items.map((item, i) => <Component key={i} {...item} />)}

// Always use Sanity's _key
{items.map((item) => <Component key={item._key} {...item} />)}
```

### Cleaning Values for Logic
Use `stegaClean` when block fields control rendering logic:

```typescript
import { stegaClean } from "next-sanity";

function SplitImage({ orientation, title, image }) {
  return (
    <section data-orientation={stegaClean(orientation) || "imageLeft"}>
      {/* ... */}
    </section>
  );
}
```

## 5. Presentation Queries for Live Editing (Next.js)

For faster live updates in the Presentation Tool, use **presentation queries** that fetch only the specific block being edited, rather than re-fetching the entire page.

> **Note:** This pattern uses `usePresentationQuery` from `next-sanity/hooks`. For other frameworks, check your loader package for equivalent functionality.

### The Pattern

1. **Create a block-specific presentation query:**

```typescript
// queries.ts
export const HERO_PRESENTATION_QUERY = defineQuery(`
  *[_id == $documentId][0]{
    _id,
    _type,
    "heroBlock": pageBuilder[_key == $blockKey && _type == "hero"][0]{
      title,
      subtitle,
      image,
      // ... all fields the component needs
    }
  }
`)
```

2. **Use `usePresentationQuery` in your component:**

```typescript
'use client'
import { usePresentationQuery } from 'next-sanity/hooks'
import { HERO_PRESENTATION_QUERY } from '@/sanity/lib/queries'

type HeroProps = {
  _key: string
  documentId: string
  // ... initial props from page query
}

export function Hero({ _key, documentId, ...initialProps }: HeroProps) {
  // Fetch block-specific data for faster updates
  const { data } = usePresentationQuery({
    query: HERO_PRESENTATION_QUERY,
    params: { documentId, blockKey: _key },
  })

  // Use presentation data if available, fallback to initial props
  const blockData = data?.heroBlock || initialProps

  return (
    <section>
      <h1>{blockData.title}</h1>
      {/* ... */}
    </section>
  )
}
```

### Why This Is Faster

- **Without:** Editing a field triggers a full page re-render with all blocks
- **With:** Only the specific block re-renders with its targeted query

This pattern is especially valuable for pages with many blocks or complex nested data.

**Note:** See `nextjs.md` for more details on `usePresentationQuery` and `visual-editing.md` for the conceptual overview.

## 6. Page Builder Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too many block variations | Split into separate blocks if >2 variants |
| Paradox of choice | Limit blocks per document type |
| Overusing references | Default to objects; references only for truly shared content |
| Unused blocks accumulate | Prune regularly; see deprecation patterns |
| Inconsistent previews | Always set title, subtitle (block name), and media/icon |

## 7. Component Alignment Pattern
Map Sanity "alignment" fields (usually string/select) to CSS classes using utility functions.

**Schema:**
```typescript
defineField({
  name: 'align',
  type: 'string',
  options: { list: ['left', 'center', 'right'], layout: 'radio' }
})
```

**Implementation (Utility):**
```typescript
import { stegaClean } from "@sanity/client/stega";

export function getTextAlign(align?: string) {
  // CLEAN the value before switching!
  switch (stegaClean(align)) {
    case 'left': return 'text-left';
    case 'right': return 'text-right';
    default: return 'text-center';
  }
}
```

## 8. Semantic Heading Levels
**Rule:** Do NOT store heading levels (h1, h2) in Sanity schema options. Determine them dynamically in the frontend to ensure accessibility.

**Bad Schema:**
```typescript
// Don't do this
{ name: 'level', type: 'string', options: { list: ['h1', 'h2'] } }
```

**Good Component:**
Pass a `semanticLevel` prop based on the component's context/nesting.

```typescript
type Props = {
  block: HeroBlock;
  level?: 'h1' | 'h2' | 'h3'; // Default to h2 if undefined
}

export default function Section({ block, level = 'h2' }: Props) {
  const Tag = level;
  return <Tag>{block.title}</Tag>;
}
```

*Note: For Image patterns, see `image.md`. For Portable Text patterns, see `portable-text.md`.*

---

## Reference: Portable Text

# Sanity Portable Text Rules

Portable Text is Sanity's rich text format, used for content like article bodies (`body[]`). This guide covers rendering and creating custom PTE components.

**Note:** For page-level layout blocks (`pageBuilder[]`), see `page-builder.md`.

## 1. The Component
Use the `PortableText` component from `next-sanity` (or `@portabletext/react`).

```typescript
import { PortableText } from "next-sanity";
// or import { PortableText } from "@portabletext/react";

export function Content({ value }: { value: any }) {
  return <PortableText value={value} components={components} />;
}
```

## 2. Custom Components (`components` prop)
**Always** define a typed components object to handle custom blocks, marks, and list styles.

```typescript
import { PortableTextComponents } from "next-sanity";

const components: PortableTextComponents = {
  // 1. Block styles (paragraphs, headings)
  block: {
    h1: ({ children }) => <h1 className="text-4xl font-bold">{children}</h1>,
    h2: ({ children }) => <h2 className="text-3xl font-bold">{children}</h2>,
    blockquote: ({ children }) => <blockquote className="border-l-4 pl-4">{children}</blockquote>,
  },

  // 2. Custom types (non-text blocks like images, videos)
  types: {
    image: ({ value }) => <SanityImage value={value} />,
    callToAction: ({ value }) => <Button href={value.url}>{value.text}</Button>,
  },

  // 3. Marks (inline decorators and annotations)
  marks: {
    strong: ({ children }) => <strong className="font-bold">{children}</strong>,
    em: ({ children }) => <em className="italic">{children}</em>,
    link: ({ children, value }) => {
      const rel = !value.href.startsWith("/") ? "noreferrer noopener" : undefined;
      return <a href={value.href} rel={rel} className="underline text-blue-600">{children}</a>;
    },
  },

  // 4. Lists
  list: {
    bullet: ({ children }) => <ul className="list-disc ml-4">{children}</ul>,
    number: ({ children }) => <ol className="list-decimal ml-4">{children}</ol>,
  },
};
```

## 3. Component Categories

Portable Text has three types of custom components, each with different patterns:

| Type | Examples | Pattern |
|------|----------|---------|
| **Block styles** | h1, h2, blockquote, normal | Text blocks with `children` prop |
| **Custom types** | image, video, callToAction | Non-text blocks with `value` prop |
| **Marks** | link, strong, productRef | Inline annotations wrapping text |

## 4. Creating Block Style Components

Block styles are text blocks like headings and paragraphs. For simple styling, inline components work fine:

```typescript
block: {
  h2: ({ children }) => <h2 className="mt-8 mb-4 text-3xl font-bold">{children}</h2>,
  normal: ({ children }) => <p className="mb-4 leading-relaxed">{children}</p>,
}
```

### With Visual Editing Support

For live editing in the Presentation Tool, block style components may need **both** a client and server version:

```typescript
// Heading2.tsx (Server - simple SSR for production)
export function Heading2({ children }: { children: React.ReactNode }) {
  return <h2 className="mt-8 mb-4 text-3xl font-bold">{children}</h2>;
}

// Heading2Client.tsx (Client - for visual editing context)
'use client'
export function Heading2Client({ children, value }: { children: React.ReactNode; value: any }) {
  // Can access block data via `value` for advanced patterns
  return <h2 className="mt-8 mb-4 text-3xl font-bold">{children}</h2>;
}
```

Use `useIsPresentationTool` to conditionally render the client version:

```typescript
import { useIsPresentationTool } from 'next-sanity/hooks'

function Heading2Wrapper(props) {
  const isPresentationTool = useIsPresentationTool()

  if (isPresentationTool) {
    return <Heading2Client {...props} />
  }
  return <Heading2 {...props} />
}
```

## 5. Creating Custom Type Components

Custom types are non-text blocks like images, videos, or CTAs embedded in rich text.

### Schema Definition

```typescript
// schemaTypes/blocks/pteImageBlock.ts
import { defineType, defineField } from 'sanity'

export const pteImageBlock = defineType({
  name: 'pteImage',
  title: 'Image',
  type: 'object',
  fields: [
    defineField({ name: 'image', type: 'image', options: { hotspot: true } }),
    defineField({ name: 'caption', type: 'string' }),
    defineField({ name: 'alt', type: 'string', validation: (r) => r.required() }),
  ],
  preview: {
    select: { title: 'caption', media: 'image' },
  },
})
```

### Register in Body Schema

```typescript
defineField({
  name: 'body',
  type: 'array',
  of: [
    { type: 'block' },      // Standard text
    { type: 'pteImage' },   // Custom image block
    { type: 'pteVideo' },   // Custom video block
  ],
})
```

### Frontend Component

```typescript
// PteImageComponent.tsx
'use client'

type PteImageProps = {
  value: {
    _key: string
    image: any
    caption?: string
    alt: string
  }
}

export function PteImageComponent({ value }: PteImageProps) {
  if (!value.image) return null

  return (
    <figure className="my-8">
      <SanityImage value={value.image} alt={value.alt} />
      {value.caption && (
        <figcaption className="text-sm text-gray-600 mt-2">{value.caption}</figcaption>
      )}
    </figure>
  )
}

// Register in components
const components: PortableTextComponents = {
  types: {
    pteImage: PteImageComponent,
  },
}
```

## 6. Creating Mark Components

Marks are inline annotations that wrap text—links, highlights, or custom references.

### Schema Definition (Annotation)

```typescript
// In your block configuration
defineField({
  name: 'body',
  type: 'array',
  of: [
    {
      type: 'block',
      marks: {
        decorators: [
          { title: 'Strong', value: 'strong' },
          { title: 'Emphasis', value: 'em' },
          { title: 'Highlight', value: 'highlight' },
        ],
        annotations: [
          {
            name: 'link',
            type: 'object',
            title: 'Link',
            fields: [
              { name: 'href', type: 'url', title: 'URL' },
              { name: 'openInNewTab', type: 'boolean', title: 'Open in new tab' },
            ],
          },
          {
            name: 'productRef',
            type: 'object',
            title: 'Product Reference',
            fields: [
              { name: 'product', type: 'reference', to: [{ type: 'product' }] },
            ],
          },
        ],
      },
    },
  ],
})
```

### Frontend Component

```typescript
// LinkMark.tsx
type LinkMarkProps = {
  children: React.ReactNode
  value: {
    href: string
    openInNewTab?: boolean
  }
}

export function LinkMark({ children, value }: LinkMarkProps) {
  const { href, openInNewTab } = value
  const target = openInNewTab ? '_blank' : undefined
  const rel = openInNewTab ? 'noopener noreferrer' : undefined

  return (
    <a href={href} target={target} rel={rel} className="text-blue-600 underline">
      {children}
    </a>
  )
}

// Register in components
const components: PortableTextComponents = {
  marks: {
    link: LinkMark,
    highlight: ({ children }) => <mark className="bg-yellow-200">{children}</mark>,
  },
}
```

## 7. Presentation Queries for PTE Blocks

For faster live editing of custom PTE blocks, use presentation queries that fetch only the specific block:

```typescript
// queries.ts
export const PTE_IMAGE_PRESENTATION_QUERY = defineQuery(`
  *[_id == $documentId][0]{
    _id,
    _type,
    "pteImageBlock": body[_key == $blockKey && _type == "pteImage"][0]{
      _key,
      image,
      caption,
      alt
    }
  }
`)
```

Then in your component:

```typescript
'use client'
import { usePresentationQuery } from 'next-sanity/hooks'

export function PteImageComponent({ value, documentId }: { value: any; documentId?: string }) {
  const { data } = usePresentationQuery({
    query: PTE_IMAGE_PRESENTATION_QUERY,
    params: { documentId, blockKey: value._key },
  })

  const blockData = data?.pteImageBlock || value

  // ... render with blockData
}
```

**Note:** You'll need to pass `documentId` through to your PTE components. See `visual-editing.md` for context patterns.

## 8. GROQ Fragment for PTE

When querying documents with Portable Text, expand custom blocks:

```groq
*[_type == "article" && slug.current == $slug][0]{
  ...,
  body[]{
    ...,
    _type == "pteImage" => {
      ...,
      "imageUrl": image.asset->url
    },
    _type == "pteVideo" => {
      ...,
      video->{ title, url }
    }
  }
}
```

## 9. Stega and Visual Editing

When Visual Editing is enabled, text content contains invisible stega characters for click-to-edit functionality.

**For text rendering:** Let stega characters pass through—they enable overlays:
```typescript
// Good - stega preserved for click-to-edit
<h2>{children}</h2>
```

**For logic/comparisons:** Clean the values first:
```typescript
import { stegaClean } from '@sanity/client/stega'

// Clean before using in logic
const cleanedStyle = stegaClean(block.style)
if (cleanedStyle === 'h2') { ... }
```

## 10. Type Safety
When using TypeGen, the Portable Text value usually has a complex generated type. You can often use `any` or `PortableTextBlock[]` for the *prop*, but cast specific blocks if needed.

```typescript
import { PortableTextBlock } from "next-sanity";

type Props = {
  value: PortableTextBlock[];
};
```

## 11. Best Practices

- **Tailwind Typography:** For simple blogs, wrap `<PortableText />` in a `<div className="prose">` (from `@tailwindcss/typography`) instead of manually styling every block.
- **Handling Nulls:** Always check if `value` exists and is an array before rendering.
- **Keys:** The `PortableText` component handles React keys automatically using the `_key` from Sanity. Do not add keys manually.
- **Separate from Page Builder:** PTE blocks live in `body[]` (rich text fields), not `pageBuilder[]` (page layout). Keep these patterns separate.

---

## Reference: Project Structure

# Sanity Project Structure

## Standalone Studio

Best for content-only projects, API-first architectures, or when frontend is managed separately.

```
your-project/
├── schemaTypes/
│   ├── index.ts
│   ├── documents/
│   ├── objects/
│   └── blocks/
├── sanity.config.ts
├── sanity.cli.ts
└── package.json
```

**Use cases:**
- Content modeling with MCP/AI tools (no frontend needed)
- Headless CMS with external consumers
- Prototyping and content design

## Embedded Studio (Recommended for Next.js)

Best for most Next.js projects. Unified deployment, simpler setup.

```
your-project/
├── src/
│   ├── app/                    # Next.js App Router
│   │   └── studio/[[...tool]]/ # Embedded Studio route
│   └── sanity/
│       ├── lib/
│       │   ├── client.ts
│       │   ├── live.ts         # defineLive setup
│       │   └── queries.ts
│       └── schemaTypes/
│           ├── index.ts
│           ├── documents/
│           ├── objects/
│           └── blocks/
├── sanity.config.ts
├── sanity.cli.ts               # CLI + TypeGen configuration
└── sanity.types.ts             # Generated types (from TypeGen)
```

## Monorepo

Best when you need separation of concerns, multiple frontends, or strict dependency isolation.

```
your-project/
├── apps/
│   ├── studio/                 # Sanity Studio (standalone)
│   │   ├── src/
│   │   │   └── schemaTypes/
│   │   │       ├── index.ts
│   │   │       ├── documents/
│   │   │       ├── objects/
│   │   │       └── blocks/
│   │   ├── sanity.config.ts
│   │   ├── sanity.cli.ts
│   │   └── package.json
│   └── web/                    # Next.js (or other framework)
│       ├── src/
│       │   ├── app/
│       │   └── sanity/
│       │       ├── client.ts
│       │       ├── live.ts
│       │       └── queries.ts
│       └── package.json
├── pnpm-workspace.yaml
└── package.json
```

**Setup:**
1. Add web app URL to CORS origins in Sanity project settings
2. Configure `typegen` in `sanity.cli.ts` to read schema from `apps/studio` and output types to `apps/web`

## File Naming Conventions

- **kebab-case** for all files: `user-profile.ts`, `hero-block.ts`
- `.ts` for schemas/utilities, `.tsx` for React components
- Each schema exports a named const matching filename

## Schema Directory Structure

```
schemaTypes/
├── index.ts              # Exports all types
├── documents/            # Standalone content types
│   ├── post.ts
│   └── author.ts
├── objects/              # Embeddable/reusable types
│   ├── seo.ts
│   └── link.ts
├── blocks/               # Portable Text blocks
│   ├── hero.ts
│   └── callout.ts
└── shared/               # Shared field definitions
    └── seoFields.ts
```

## Key Files

| File | Purpose |
|------|---------|
| `sanity.config.ts` | Studio configuration (plugins, schema, structure) |
| `sanity.cli.ts` | CLI configuration (project ID, dataset, TypeGen config) |
| `structure.ts` | Custom desk structure |

---

## Reference: Remix

# React Router (Remix) & Sanity Integration Rules

## Version Note

This guide covers both:
- **Remix v2** (`@remix-run/*` packages)
- **React Router v7** (the successor to Remix, `react-router` package)

The Sanity integration pattern is the same for both. Import paths differ slightly:

| Remix v2 | React Router v7 |
|----------|-----------------|
| `@remix-run/node` | `react-router` |
| `@remix-run/react` | `react-router` |
| `remix.config.js` | `react-router.config.ts` |

The examples below use Remix v2 imports. Adjust if using React Router v7.

## 1. Setup & Client Pattern

To support both server-side fetching and client-side live previews, use the **Split Loader Pattern**.

### A. Shared Loader (`app/sanity/loader.ts`)
Defines the store config (SSR enabled, client deferred).

```typescript
import { createQueryStore } from '@sanity/react-loader'

export const {
  loadQuery,
  setServerClient,
  useQuery,
  useLiveMode,
} = createQueryStore({ client: false, ssr: true })
```

### B. Server Loader (`app/sanity/loader.server.ts`)
Initializes the server client.

```typescript
import { createClient } from '@sanity/client'
import { loadQuery, setServerClient } from './loader'

const client = createClient({
  projectId: process.env.SANITY_PROJECT_ID,
  dataset: process.env.SANITY_DATASET,
  useCdn: true,
  apiVersion: '2026-02-01',
  stega: {
    enabled: true,
    studioUrl: 'https://my-studio-url.com',
  },
})

setServerClient(client)

export { loadQuery }
```

## 2. Data Fetching (Loaders)

Use `loadQuery` from your **server** file in route loaders.

```typescript
import type { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { loadQuery } from "~/sanity/loader.server";
import { POSTS_QUERY } from "~/sanity/queries";

export async function loader({ params }: LoaderFunctionArgs) {
  const initial = await loadQuery(POSTS_QUERY, params);
  return { initial, query: POSTS_QUERY, params };
}

export default function Index() {
  const { initial, query, params } = useLoaderData<typeof loader>();
  // ... pass to component
}
```

## 3. Real-time Preview & Visual Editing

### A. Use `useQuery` in Components
Import `useQuery` from your **shared** loader file.

```typescript
import { useQuery } from "~/sanity/loader";

export default function Page() {
  const { initial, query, params } = useLoaderData<typeof loader>();

  const { data, encodeDataAttribute } = useQuery(query, params, {
    initial
  });

  return (
    <h1 data-sanity={encodeDataAttribute('title')}>
      {data?.title}
    </h1>
  );
}
```

### B. Enable Live Mode (`VisualEditing.tsx`)
Create a component to handle the connection.

```typescript
import { enableVisualEditing } from '@sanity/visual-editing'
import { useLiveMode } from '~/sanity/loader'
import { client } from '~/sanity/client' // Your browser-safe client
import { useEffect } from 'react'

export default function VisualEditing() {
  useEffect(() => enableVisualEditing(), [])
  useLiveMode({ client })
  return null
}
```

Render this component in `root.tsx` only when valid (e.g., check env vars or user session).

## 4. Stega Cleaning
When using data for logic (routing, classNames), use `stegaClean`.

```typescript
import { stegaClean } from "@sanity/client/stega"
// ...
if (stegaClean(slug) === 'home') { ... }
```

---

## Reference: Schema

# Sanity Schema Best Practices

Use this contents list to jump to the schema design decision you are making.

## Table of Contents

- Core philosophy: data over presentation
- Strict definition syntax
- Shared fields pattern
- Field patterns
- References vs nested objects
- Safe schema updates
- Validation patterns

## 1. Core Philosophy: Data > Presentation
Model **what things are**, not **what they look like**.
- ❌ **Bad:** `bigHeroText`, `redButton`, `threeColumnRow`, `color`, `fontSize`
- ✅ **Good:** `heroStatement`, `callToAction`, `featuresSection`, `status`, `role`

**The test:** "If we redesigned the site, would this field name still make sense?"
- `threeColumnLayout` → ❌ Fails (what if we go to 2 columns?)
- `features` → ✅ Passes (features are features regardless of layout)

## 2. Strict Definition Syntax
Always use the helper functions from `sanity` for type safety and autocompletion.

- **ALWAYS** use `defineType` for the root export.
- **ALWAYS** use `defineField` for fields.
- **ALWAYS** use `defineArrayMember` for items inside arrays.

```typescript
import { defineType, defineField, defineArrayMember } from 'sanity'
import { TagIcon } from '@sanity/icons'

export const article = defineType({
  name: 'article',
  title: 'Article',
  type: 'document',
  icon: TagIcon,
  fields: [
    defineField({
      name: 'title',
      type: 'string',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'tags',
      type: 'array',
      of: [
        // ALWAYS use defineArrayMember for array items
        defineArrayMember({ type: 'reference', to: [{ type: 'tag' }] })
      ]
    })
  ]
})
```

## 3. Shared Fields Pattern
Export arrays of fields to reuse common patterns (e.g., SEO, standard page headers).

```typescript
// src/schemaTypes/shared/seoFields.ts
export const seoFields = [
  defineField({ name: 'seoTitle', type: 'string', title: 'SEO Title' }),
  defineField({ name: 'seoDesc', type: 'text', title: 'SEO Description' })
]

// Usage
defineType({
  name: 'page',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    ...seoFields // Spread shared fields
  ]
})
```

## 4. Field Patterns

### A. Array Keys (`_key`)
Every item in a Sanity array automatically gets a `_key` property. This is **critical** for:
- React reconciliation (use as `key` prop)
- Visual Editing overlays (click-to-edit)
- Portable Text rendering

**Schema:** Sanity auto-generates `_key` for array items. You don't define it.

**Frontend:** Always use `_key` as React's `key`:
```typescript
// ✅ Correct
{items.map((item) => <Component key={item._key} {...item} />)}

// ❌ Wrong - index keys break Visual Editing
{items.map((item, i) => <Component key={i} {...item} />)}
```

**Querying:** Always include `_key` in array projections:
```groq
*[_type == "page"][0]{
  pageBuilder[]{
    _key,  // Always include _key in queries
    _type,
    ...
  }
}
```

### B. Icons
Always assign an icon from `@sanity/icons` to documents and objects. This improves the Studio UX significantly. Browse all icons at [icons.sanity.build](https://icons.sanity.build/all).

| Content Type | Icon |
|--------------|------|
| Article, Post | `DocumentTextIcon` |
| Author, Person | `UserIcon` |
| Category, Tag | `TagIcon` |
| Settings | `CogIcon` |
| Page | `DocumentIcon` |
| Image block | `ImageIcon` |
| Video block | `PlayIcon` |
| FAQ | `HelpCircleIcon` |
| Link | `LinkIcon` |

### C. Boolean vs. List
Avoid boolean fields for binary states that might expand later.
- **Prefer:** `options.list` with "radio" layout.

```typescript
defineField({
  name: 'status',
  type: 'string',
  options: {
    list: [
      { title: 'Draft', value: 'draft' },
      { title: 'Published', value: 'published' }
    ],
    layout: 'radio'
  }
})
```

### D. The "Toggle" Pattern (Conditional Fields)
Use a radio/boolean field to toggle visibility of other fields (often grouped in fieldsets).

```typescript
defineField({
  name: 'linkType',
  type: 'string',
  options: { list: ['internal', 'external'], layout: 'radio' }
}),
defineField({
  name: 'internalLink',
  type: 'reference',
  hidden: ({ parent }) => parent?.linkType !== 'internal'
}),
defineField({
  name: 'externalUrl',
  type: 'url',
  hidden: ({ parent }) => parent?.linkType !== 'external'
})
```

## 5. References vs Nested Objects

A **critical modeling decision**: when to use `reference` vs embedding an `object`.

### Use References When:
- Content is **reusable** across documents (authors, categories, products)
- Content needs its **own editing interface** in Studio
- You need to query/filter by the related content independently
- Multiple documents should share the **same instance** (update once, reflect everywhere)

```typescript
// ✅ Author is reusable and independently editable
defineField({
  name: 'author',
  type: 'reference',
  to: [{ type: 'author' }]
})
```

### Use Nested Objects When:
- Content is **specific to this document** (not shared)
- Content doesn't make sense on its own (address, SEO metadata)
- You want **simpler editing** (all fields in one place)
- You need the data to be **copied** not linked

```typescript
// ✅ SEO is document-specific, not shared
defineField({
  name: 'seo',
  type: 'object',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'description', type: 'text' })
  ]
})
```

### Quick Decision Matrix

| Scenario | Use |
|----------|-----|
| Blog post author | `reference` (reusable) |
| Product category | `reference` (shared taxonomy) |
| Page SEO fields | `object` (page-specific) |
| Hero section content | `object` (page-specific) |
| Team member on About page | `reference` (might be used elsewhere) |
| Call-to-action button | `object` (usually page-specific) |

### Querying Differences
```groq
// Reference requires expansion
*[_type == "post"]{ author->{ name, bio } }

// Object is already inline
*[_type == "post"]{ seo { title, description } }
```

## 6. Safe Schema Updates (The Deprecation Pattern)

**NEVER** delete a field that contains production data. It will cause data loss or Studio crashes. Instead, follow the **ReadOnly -> Hidden -> Deprecated** lifecycle.

### The Pattern
1.  **`deprecated`**: Adds a visual warning and reason.
2.  **`readOnly: true`**: Prevents new edits but keeps data visible.
3.  **`hidden`**: Hides it from *new* documents (where value is undefined).
4.  **`initialValue: undefined`**: Ensures new documents don't get this field.

```typescript
defineField({
  name: 'oldTitle', // The field you want to remove
  title: 'Article Title (Deprecated)',
  type: 'string',
  deprecated: {
    reason: 'Use the new "seoTitle" field instead. This will be removed in v2.'
  },
  readOnly: true,
  hidden: ({ value }) => value === undefined,
  initialValue: undefined
})
```

### Migration Workflow

**Phase 1: Deprecate** — Apply the deprecation pattern above. Deploy.

**Phase 2: Migrate** — Update frontend to use new fields (with `coalesce()` fallbacks). Create a migration:

```typescript
// migrations/rename-oldTitle-to-newTitle/index.ts
import {defineMigration, at, setIfMissing, unset} from 'sanity/migrate'

export default defineMigration({
  title: 'Rename oldTitle to newTitle',
  documentTypes: ['article'],
  filter: 'defined(oldTitle) && !defined(newTitle)',
  migrate: {
    document(doc) {
      if (!doc.oldTitle || doc.newTitle) return
      return [
        at('newTitle', setIfMissing(doc.oldTitle)),
        at('oldTitle', unset())
      ]
    }
  }
})
```

```bash
# Dry run first (default)
sanity migration run rename-oldTitle-to-newTitle

# Execute when ready
sanity migration run rename-oldTitle-to-newTitle --no-dry-run
```

**Phase 3: Remove** — Once `oldTitle` is undefined for all documents, delete the field definition.

## 7. Validation Patterns

Beyond `rule.required()`, Sanity offers powerful validation options.

### Common Patterns

```typescript
// Email validation
defineField({
  name: 'email',
  type: 'string',
  validation: (rule) => rule.email().required()
})

// URL validation (with custom message)
defineField({
  name: 'website',
  type: 'url',
  validation: (rule) => rule.uri({
    scheme: ['http', 'https']
  }).error('Must be a valid URL starting with http:// or https://')
})

// Length constraints
defineField({
  name: 'excerpt',
  type: 'text',
  validation: (rule) => rule.max(200).warning('Keep it under 200 characters for best SEO')
})

// Regex pattern
defineField({
  name: 'slug',
  type: 'slug',
  validation: (rule) => rule.required().custom((slug) => {
    if (!slug?.current) return 'Required'
    if (!/^[a-z0-9-]+$/.test(slug.current)) {
      return 'Slug must be lowercase with hyphens only'
    }
    return true
  })
})
```

### Cross-Field Validation

```typescript
defineField({
  name: 'endDate',
  type: 'datetime',
  validation: (rule) => rule.custom((endDate, context) => {
    const startDate = context.document?.startDate
    if (startDate && endDate && new Date(endDate) < new Date(startDate)) {
      return 'End date must be after start date'
    }
    return true
  })
})
```

### Array Validation

```typescript
defineField({
  name: 'tags',
  type: 'array',
  of: [{ type: 'string' }],
  validation: (rule) => rule
    .min(1).error('Add at least one tag')
    .max(10).warning('Too many tags may hurt SEO')
    .unique()
})
```

### Async Validation (Uniqueness Check)

```typescript
defineField({
  name: 'slug',
  type: 'slug',
  validation: (rule) => rule.required().custom(async (slug, context) => {
    if (!slug?.current) return true

    const client = context.getClient({ apiVersion: '2026-02-01' })
    const id = context.document?._id?.replace(/^drafts\./, '')

    const existing = await client.fetch(
      `count(*[_type == "post" && slug.current == $slug && _id != $id])`,
      { slug: slug.current, id }
    )

    return existing === 0 || 'Slug already exists'
  })
})
```

---

## Reference: Seo

# Sanity SEO Best Practices

## 1. Core Philosophy

SEO doesn't require complex configurations. A few core principles, applied consistently:

- **Smart defaults with optional overrides** — Don't require SEO fields; use existing content as fallback
- **Use GROQ for fallback logic** — Move conditional logic into queries, not components
- **Leverage Next.js APIs** — Use `generateMetadata`, `sitemap.ts`, not manual `<meta>` tags
- **Structured content = structured data** — Your content model is already SEO-ready

## 2. SEO Schema Type (Reusable)

Create a reusable SEO object type for consistent metadata across document types.

```typescript
// schemaTypes/seoType.ts
import { defineField, defineType } from "sanity";

export const seoType = defineType({
  name: "seo",
  title: "SEO",
  type: "object",
  fields: [
    defineField({
      name: "title",
      description: "Overrides the page title if provided",
      type: "string",
    }),
    defineField({
      name: "description",
      type: "text",
      rows: 3,
    }),
    defineField({
      name: "image",
      description: "Image for social sharing (1200x630 recommended)",
      type: "image",
      options: { hotspot: true },
    }),
    defineField({
      name: "noIndex",
      description: "Hide this page from search engines",
      type: "boolean",
      initialValue: false,
    }),
  ],
});
```

**Usage in document types:**
```typescript
defineField({
  name: "seo",
  type: "seo",
})
```

## 3. GROQ Queries with Fallbacks

Use `coalesce()` to provide fallback values. This keeps frontend logic clean.

```groq
*[_type == "page" && slug.current == $slug][0]{
  ...,
  "seo": {
    // Use SEO field if provided, otherwise fall back to main title
    "title": coalesce(seo.title, title, ""),
    "description": coalesce(seo.description, ""),
    "image": seo.image,
    "noIndex": seo.noIndex == true
  }
}
```

**Key principle:** `seo.title` will never be `null` — it contains either the SEO override, the page title, or empty string.

## 4. Next.js Metadata (The Right Way)

Use `generateMetadata` — never render `<title>` or `<meta>` tags directly in components.

```typescript
// app/(frontend)/[slug]/page.tsx
import type { Metadata } from "next";
import { urlFor } from "@/sanity/lib/image";

type RouteProps = {
  params: Promise<{ slug: string }>;
};

// Extract fetch to reuse in both functions
const getPage = async (params: RouteProps["params"]) =>
  sanityFetch({
    query: PAGE_QUERY,
    params: await params,
    stega: false, // Critical for SEO!
  });

export async function generateMetadata({ params }: RouteProps): Promise<Metadata> {
  const { data: page } = await getPage(params);

  if (!page) return {};

  const metadata: Metadata = {
    title: page.seo.title,
    description: page.seo.description,
  };

  // Open Graph image
  if (page.seo.image) {
    metadata.openGraph = {
      images: {
        url: urlFor(page.seo.image).width(1200).height(630).url(),
        width: 1200,
        height: 630,
      },
    };
  }

  // noIndex robots directive
  if (page.seo.noIndex) {
    metadata.robots = "noindex";
  }

  return metadata;
}

export default async function Page({ params }: RouteProps) {
  const { data: page } = await getPage(params);
  // ... render page
}
```

**Critical:** Always set `stega: false` when fetching for metadata. Stega characters in `<title>` destroy SEO.

## 5. Dynamic Sitemap

Use Next.js `sitemap.ts` convention to auto-generate from Sanity content.

### GROQ Query
```groq
*[_type in ["page", "post"] && defined(slug.current) && seo.noIndex != true] {
  "href": select(
    _type == "page" => "/" + slug.current,
    _type == "post" => "/posts/" + slug.current,
    slug.current
  ),
  _updatedAt
}
```

### Route Implementation
```typescript
// app/sitemap.ts
import { MetadataRoute } from "next";
import { client } from "@/sanity/lib/client";
import { SITEMAP_QUERY } from "@/sanity/lib/queries";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : "http://localhost:3000";

  try {
    const paths = await client.fetch(SITEMAP_QUERY);
    if (!paths) return [];

    return paths.map((path) => ({
      url: new URL(path.href!, baseUrl).toString(),
      lastModified: new Date(path._updatedAt),
      changeFrequency: "weekly",
      priority: 1,
    }));
  } catch (error) {
    console.error("Sitemap generation failed:", error);
    return [];
  }
}
```

**Note:** Sitemap limit is 50,000 URLs per file. For larger sites, use sitemap index.

## 6. Redirects (Managed in Sanity)

Create a redirect document type for content team management.

### Schema
```typescript
// schemaTypes/redirectType.ts
import { defineField, defineType, SanityDocumentLike } from "sanity";
import { LinkIcon } from "@sanity/icons";

function isValidPath(value: string | undefined) {
  if (!value) return "Required";
  if (!value.startsWith("/")) return "Must start with /";
  if (/[^a-zA-Z0-9\-_/:]/.test(value)) return "Invalid characters";
  return true;
}

export const redirectType = defineType({
  name: "redirect",
  title: "Redirect",
  type: "document",
  icon: LinkIcon,
  validation: (Rule) =>
    Rule.custom((doc: SanityDocumentLike | undefined) => {
      if (doc?.source === doc?.destination) {
        return "Source and destination cannot be the same";
      }
      return true;
    }),
  fields: [
    defineField({
      name: "source",
      type: "string",
      validation: (Rule) => Rule.required().custom(isValidPath),
    }),
    defineField({
      name: "destination",
      type: "string",
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: "permanent",
      description: "301 (permanent) or 302 (temporary)",
      type: "boolean",
      initialValue: true,
    }),
    defineField({
      name: "isEnabled",
      type: "boolean",
      initialValue: true,
    }),
  ],
});
```

### Next.js Config
```typescript
// next.config.ts
import { fetchRedirects } from "@/sanity/lib/fetchRedirects";

const nextConfig: NextConfig = {
  async redirects() {
    return await fetchRedirects();
  },
};
```

**Limits:** Vercel allows max 1,024 redirects in `next.config`. For more, use middleware.

## 7. Dynamic Open Graph Images

Generate OG images on-the-fly using Next.js Edge Runtime at `/api/og`.

```typescript
// app/api/og/route.tsx
import { ImageResponse } from "next/og";
export const runtime = "edge";

export async function GET(request: Request) {
  const id = new URL(request.url).searchParams.get("id");
  if (!id) return new Response("Missing id", { status: 400 });

  const data = await client.fetch(`*[_id == $id][0]{ title }`, { id });

  return new ImageResponse(
    <div tw="flex w-full h-full bg-blue-500 text-white p-10">
      <h1 tw="text-6xl font-bold">{data?.title || "Untitled"}</h1>
    </div>,
    { width: 1200, height: 630 }
  );
}
```

Use as fallback in metadata: `url: page.seo.image ? urlFor(page.seo.image).url() : \`/api/og?id=\${page._id}\``

## 8. JSON-LD Structured Data

Use `schema-dts` for type-safe structured data.

```bash
npm install schema-dts
```

### FAQ Example
```typescript
import { FAQPage, WithContext } from "schema-dts";

const generateFaqData = (faqs: FAQ[]): WithContext<FAQPage> => ({
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faqs.map((faq) => ({
    "@type": "Question",
    name: faq.title,
    acceptedAnswer: {
      "@type": "Answer",
      text: faq.text, // Use pt::text() in GROQ to get plain text
    },
  })),
});

// In component
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(generateFaqData(faqs)) }}
/>
```

### GROQ for Plain Text
```groq
faqs[]->{
  _id,
  title,
  body,
  "text": pt::text(body)  // Convert Portable Text to plain string
}
```

## 9. Testing Tools

- **Open Graph:** [opengraph.ing](https://opengraph.ing/)
- **Facebook:** [Sharing Debugger](https://developers.facebook.com/tools/debug/)
- **Twitter:** [Card Validator](https://cards-dev.twitter.com/validator)
- **LinkedIn:** [Post Inspector](https://www.linkedin.com/post-inspector/)
- **Sitemap:** [XML Sitemaps Validator](https://www.xml-sitemaps.com/validate-xml-sitemap.html)

---

## Reference: Studio Structure

# Sanity Studio Structure Rules

## 1. Setup
Custom structure is defined in `sanity.config.ts` using the `structureTool`.

```typescript
import { structureTool } from 'sanity/structure'
import { structure } from './src/structure'

export default defineConfig({
  // ...
  plugins: [
    structureTool({ structure })
  ]
})
```

## 2. Structure Definition
**Location:** `src/structure/index.ts`

Use a function that receives `S` (StructureBuilder).

```typescript
import type { StructureResolver } from 'sanity/structure'

export const structure: StructureResolver = (S) =>
  S.list()
    .title('Content')
    .items([
      // ... items
    ])
```

## 3. Organization Principles
1.  **Singletons First:** Place critical site-wide settings (Global Settings, Homepage) at the top.
2.  **Dividers:** Use `S.divider()` to visually separate logical groups.
3.  **Filtered Lists:** Always exclude Singleton documents from generic `documentTypeList` items to avoid duplication.

## 4. Singleton Pattern (Critical)

**Singletons are enforced via Structure, NOT schema options.** There is no `singleton: true` schema option.

### How Singletons Work
1. Use `S.document().documentId('fixed-id')` to lock the document to a specific ID.
2. Filter the type from generic lists to prevent duplicate entries.

### Singleton Helper Function
```typescript
// Helper to create singleton list items
function createSingleton(S: StructureBuilder, typeName: string, title: string, icon?: ComponentType) {
  return S.listItem()
    .title(title)
    .icon(icon)
    .child(
      S.document()
        .schemaType(typeName)
        .documentId(typeName) // Fixed ID = singleton
        .title(title)
    )
}

// Usage
createSingleton(S, 'settings', 'Site Settings', CogIcon)
```

### Querying Singletons
```groq
// By fixed ID (most efficient)
*[_id == "settings"][0]

// By type (works but slower)
*[_type == "settings"][0]
```

**For localized singletons** (e.g., homepage per language), see `localization.md` Section 6.

## 5. Implementation Pattern

```typescript
// Define singleton types to exclude from generic lists
const SINGLETONS = ['settings', 'homePage']

export const structure: StructureResolver = (S) =>
  S.list()
    .title('Website Content')
    .items([
      // 1. Singletons
      S.listItem()
        .title('Site Settings')
        .icon(CogIcon)
        .child(S.document().schemaType('settings').documentId('settings')),

      S.divider(),

      // 2. Content Verticals
      S.listItem()
        .title('Blog')
        .child(
          S.list()
            .title('Blog Content')
            .items([
              S.documentTypeListItem('post').title('Posts'),
              S.documentTypeListItem('author').title('Authors'),
            ])
        ),

      S.divider(),

      // 3. Remaining Documents (Filtered)
      ...S.documentTypeListItems().filter(
        (listItem) => !SINGLETONS.includes(listItem.getId() as string)
      )
    ])
```

## 6. Views (Split Pane)
Add "Web Preview" or other views to documents.

```typescript
export const defaultDocumentNode: DefaultDocumentNodeResolver = (S, { schemaType }) => {
  switch (schemaType) {
    case `post`:
      return S.document().views([
        S.view.form(), // Default form
        S.view.component(PreviewComponent).title('Preview') // Custom view
      ])
    default:
      return S.document().views([S.view.form()])
  }
}
```

---

## Reference: Svelte

# SvelteKit & Sanity Integration Rules

## 1. Setup & Configuration

### Installation
```bash
npm install @sanity/svelte-loader @sanity/client @sanity/visual-editing
```

### Client Configuration (`src/lib/sanity.ts`)
Define the client with `stega` enabled for the studio URL.

```typescript
import { createClient } from '@sanity/client'
import { PUBLIC_SANITY_PROJECT_ID, PUBLIC_SANITY_DATASET, PUBLIC_SANITY_API_VERSION, PUBLIC_SANITY_STUDIO_URL } from '$env/static/public'

export const client = createClient({
  projectId: PUBLIC_SANITY_PROJECT_ID,
  dataset: PUBLIC_SANITY_DATASET,
  apiVersion: PUBLIC_SANITY_API_VERSION,
  useCdn: true,
  stega: {
    studioUrl: PUBLIC_SANITY_STUDIO_URL,
  },
})
```

### Server Client (`src/lib/server/sanity.ts`)
Use the read token for fetching preview content.

```typescript
import { SANITY_API_READ_TOKEN } from '$env/static/private'
import { client } from '$lib/sanity'

export const serverClient = client.withConfig({
  token: SANITY_API_READ_TOKEN,
  stega: true, // Optional: enable stega on server too if needed
})
```

## 2. Hooks & Request Handler (Critical)

You **must** configure `createRequestHandler` in `src/hooks.server.ts` to handle preview sessions and inject `loadQuery` into locals.

```typescript
// src/hooks.server.ts
import { createRequestHandler, setServerClient } from '@sanity/svelte-loader'
import { serverClient } from '$lib/server/sanity'

setServerClient(serverClient)

export const handle = createRequestHandler()
```

**Update `app.d.ts` types:**
```typescript
import type { LoaderLocals } from '@sanity/svelte-loader'

declare global {
  namespace App {
    interface Locals extends LoaderLocals {}
  }
}
```

## 3. Preview State Propagation

Pass the preview state from the server to the client via the root layout.

**Server Layout (`src/routes/+layout.server.ts`):**
```typescript
import type { LayoutServerLoad } from './$types'

export const load: LayoutServerLoad = ({ locals: { preview } }) => {
  return { preview }
}
```

**Client Layout (`src/routes/+layout.ts`):**
```typescript
import { setPreviewing } from '@sanity/svelte-loader'
import type { LayoutLoad } from './$types'

export const load: LayoutLoad = ({ data: { preview } }) => {
  setPreviewing(preview)
}
```

## 4. Data Fetching (Loaders)

Use `locals.loadQuery` in your page server loaders.

```typescript
// src/routes/[slug]/+page.server.ts
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ locals: { loadQuery }, params }) => {
  const initial = await loadQuery(QUERY, params)
  return { initial }
}
```

## 5. Real-time Preview & Visual Editing

### Component Usage (`useQuery`)
Use `useQuery` in your Svelte component to handle real-time updates.

```svelte
<!-- src/routes/[slug]/+page.svelte -->
<script lang="ts">
  import { useQuery } from '@sanity/svelte-loader'
  import type { PageData } from './$types'

  export let data: PageData
  const { initial } = data

  // Hydrate with initial data
  const query = useQuery(initial)

  // Reactive data access
  $: ({ data: post, loading, encodeDataAttribute } = $query)
</script>

{#if !loading && post}
  <!-- Use encodeDataAttribute for overlays -->
  <h1 data-sanity={encodeDataAttribute('title')}>
    {post.title}
  </h1>
{/if}
```

### Enable Visual Editing (`+layout.svelte`)
Enable Visual Editing and Live Mode in your root layout.

```svelte
<script lang="ts">
  import { useLiveMode } from '@sanity/svelte-loader'
  import { enableVisualEditing } from '@sanity/visual-editing'
  import { PUBLIC_SANITY_STUDIO_URL } from '$env/static/public'
  import { onMount } from 'svelte'

  onMount(() => enableVisualEditing())

  onMount(() => useLiveMode({
    studioUrl: PUBLIC_SANITY_STUDIO_URL
  }))
</script>

<slot />
```

---

## Reference: Typegen

# Sanity TypeGen Rules

## 1. The Workflow
Sanity TypeGen generates TypeScript types from your schema and GROQ queries. Types can be generated automatically or manually.

### Automatic (Recommended)
Enable in `sanity.cli.ts` — types regenerate during `sanity dev` and `sanity build`:

```typescript
// sanity.cli.ts
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  typegen: {
    enabled: true,
  },
})
```

### Manual
Run the extract + generate cycle whenever schema or queries change:

1.  **Extract:** Converts your Schema (TS/JS) into a static JSON representation.
2.  **Generate:** Scans your codebase for GROQ queries and generates TypeScript types.

```bash
npx sanity schema extract && npx sanity typegen generate
```

### Watch Mode (for separate frontends)
If your frontend is in a separate repo from the Studio, use watch mode:

```bash
npx sanity typegen generate --watch
```

## 2. The "Update Types" Pattern
For manual workflows, implement a single script:

**package.json:**
```json
"scripts": {
  "typegen": "sanity schema extract && sanity typegen generate"
}
```

### Git Strategy for Generated Files

**Option A: Commit generated types (Recommended for most teams)**
- Types available immediately after `git pull`
- CI/CD doesn't need to run typegen
- Can cause merge conflicts

**Option B: Generate in CI (Recommended for larger teams)**
Add to `.gitignore`:
```gitignore
# Sanity TypeGen (generated)
sanity.types.ts
schema.json
```

Then ensure CI runs typegen before build:
```yaml
# Example GitHub Actions
- run: npm run typegen
- run: npm run build
```

## 3. Configuration (`sanity.cli.ts`)

> **Note:** `sanity-typegen.json` is deprecated. Move your configuration to `sanity.cli.ts`.

```typescript
// sanity.cli.ts
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  typegen: {
    enabled: true, // Auto-generate during sanity dev/build
    path: "./src/**/*.{ts,tsx,js,jsx,astro,svelte,vue}", // Glob to find queries
    schema: "schema.json", // Schema file from extract
    generates: "./sanity.types.ts", // Output file
    overloadClientMethods: true, // Auto-type client.fetch() calls
  },
})
```

### Project Structure Examples

**Single Repo / Embedded Studio (most common):**
Use defaults — no extra config needed.

**Monorepo** (Studio in `apps/studio`, Frontend in `apps/web`):
```typescript
export default defineCliConfig({
  typegen: {
    path: "../web/src/**/*.{ts,tsx,js,jsx}",
    schema: "schema.json",
    generates: "../web/sanity.types.ts",
  },
})
```

**Separate Repos:**
Use `--watch` mode in your frontend: `sanity typegen generate --watch`

## 4. Usage in Code

### Automatic Type Inference (Recommended)
With `overloadClientMethods: true` (default), `client.fetch()` automatically returns typed results when you use `defineQuery`:

```typescript
import { defineQuery } from "groq";
import { createClient } from "@sanity/client";

const client = createClient({...});

const POSTS_QUERY = defineQuery(`*[_type == "post"]{ title, slug }`);

// Return type is automatically inferred — no manual type import needed!
const posts = await client.fetch(POSTS_QUERY);
```

### Manual Type Import (Alternative)
You can also import generated types directly:

```typescript
import { defineQuery } from "groq";
// Next.js re-exports defineQuery for convenience:
// import { defineQuery } from "next-sanity";

const AUTHOR_QUERY = defineQuery(`*[_type == "author" && slug.current == $slug][0]{ name, bio }`);

import type { AUTHOR_QUERYResult } from "@/sanity.types";

export default function Author({ data }: { data: AUTHOR_QUERYResult }) {
  return <h1>{data.name}</h1>
}
```

### Required Fields
Use `--enforce-required-fields` during extraction to translate `validation: rule => rule.required()` into non-optional types:

```bash
npx sanity schema extract --enforce-required-fields
npx sanity typegen generate
```

> **Warning:** If you use draft previews, fields may still be `undefined` even with required validation, since drafts can be in an invalid state.

### Type Utilities
TypeGen provides utilities for working with complex types:

```typescript
import type { Get, FilterByType } from 'sanity'
import type { Page, PageBuilder } from './sanity.types'

// Extract deeply nested type (up to 20 levels)
type HeroSection = Get<Page, 'sections', number, 'hero'>

// Filter specific types from unions using _type discriminator
type HeroBlock = FilterByType<PageBuilder, 'hero'>
```

### Unique Query Names
All queries must have unique variable names. Duplicate names across files will cause TypeGen to silently overwrite types. Use descriptive, scoped names:

```typescript
// Unique names
const POSTS_INDEX_QUERY = defineQuery(`*[_type == "post"]{ title }`)
const POST_DETAIL_QUERY = defineQuery(`*[_type == "post" && slug.current == $slug][0]`)

// Duplicate names will conflict
const QUERY = defineQuery(`*[_type == "post"]`)  // file-a.ts
const QUERY = defineQuery(`*[_type == "author"]`) // file-b.ts — overwrites!
```

### Supported Query Formats
Queries must be assigned to a variable using `groq` or `defineQuery`:

```typescript
// Works — groq template tag
const query = groq`*[_type == "post"]`

// Works — defineQuery
const query = defineQuery(`*[_type == "post"]`)

// Won't work — inline query
await client.fetch(groq`*[_type == "post"]`)
```

### Supported File Types
TypeGen parses queries from: `.ts`, `.tsx`, `.js`, `.jsx`, `.astro`, `.svelte`, `.vue`

### tsconfig Requirements
Ensure `sanity.types.ts` is included in your `tsconfig.json`'s `include` array. If your config restricts includes (e.g., `["src/**/*"]`) and the types file is at the project root, TypeScript won't pick up the generated types:

```json
{
  "include": ["src/**/*", "sanity.types.ts"]
}
```

### Skipping Individual Queries
Add `@sanity-typegen-ignore` in a comment before a query to skip type generation:

```typescript
// @sanity-typegen-ignore
const debugQuery = groq`*[_type == "debug"]`
```

---

## Reference: Visual Editing

# Sanity Visual Editing Rules

## 1. Concepts

### Presentation Tool
The Studio plugin (`sanity/presentation`) that renders your front-end application inside an iframe in the Studio. It enables the "Edit" overlay and bidirectional navigation.

### Content Source Maps (Stega)
Invisible characters embedded in strings that tell the Presentation Tool which field in which document the content comes from.
- **Mechanism:** Sanity encodes document ID, field path, and dataset info into string values.
- **Result:** Click-to-edit functionality in the preview.

### Loaders
Framework-agnostic or specific libraries that handle:
1.  Fetching data (production vs. preview).
2.  Subscribing to real-time updates (Live Content API).
3.  Encoding Stega strings (if not handled by the Content Lake automatically).

## 2. The Golden Rule of Stega (Clean Data)

When Visual Editing is enabled, string fields will contain invisible characters. You **MUST** clean them before using the value for logic.

| Scenario | Clean? | Why |
|----------|--------|-----|
| Comparing strings (`if (x === 'y')`) | ✅ Yes | Stega breaks equality |
| Using as object keys | ✅ Yes | Keys won't match |
| Using as HTML IDs | ✅ Yes | Invalid characters |
| Passing to third-party libraries | ✅ Yes | May validate input |
| Rendering text (`<h1>{title}</h1>`) | ❌ No | Breaks click-to-edit |
| Passing to `<PortableText />` | ❌ No | Handles internally |
| Passing to image helpers | ❌ No | Handles internally |

```typescript
import { stegaClean } from "@sanity/client/stega";

export function Layout({ align }: { align: string }) {
  // Good: Clean before comparison
  const cleanAlign = stegaClean(align);
  return <div className={cleanAlign === 'center' ? 'mx-auto' : ''} />
}
```

## 3. Token Handling (Security)

Store your read token in a dedicated file that throws if missing:

```typescript
// src/sanity/lib/token.ts
export const token = process.env.SANITY_API_READ_TOKEN

if (!token) {
  throw new Error('Missing SANITY_API_READ_TOKEN')
}
```

**Never** expose tokens in client bundles. Pass to `defineLive` for server/browser use only when Draft Mode is enabled.

## 4. Setup: Presentation Tool

**File:** `sanity.config.ts`

```typescript
import { defineConfig } from 'sanity'
import { presentationTool } from 'sanity/presentation'
import { resolve } from '@/sanity/presentation/resolve'

export default defineConfig({
  // ...
  plugins: [
    presentationTool({
      resolve, // Document locations (see below)
      previewUrl: {
        previewMode: {
          enable: '/api/draft-mode/enable',
        },
      },
    }),
  ],
})
```

### Document Locations

Show where documents appear in the front-end — enables quick navigation between Structure and Presentation tools.

```typescript
// src/sanity/presentation/resolve.ts
import { defineLocations, PresentationPluginOptions } from 'sanity/presentation'

export const resolve: PresentationPluginOptions['resolve'] = {
  locations: {
    post: defineLocations({
      select: { title: 'title', slug: 'slug.current' },
      resolve: (doc) => ({
        locations: [
          { title: doc?.title || 'Untitled', href: `/posts/${doc?.slug}` },
          { title: 'Posts index', href: `/posts` },
        ],
      }),
    }),
    // Add more document types as needed
  },
}
```

## 5. Visual Editing Overlays

Render `<VisualEditing />` in Draft Mode for click-to-edit overlays.

**Next.js (App Router):**
```typescript
// layout.tsx
import { VisualEditing } from 'next-sanity/visual-editing'
import { draftMode } from 'next/headers'
import { DisableDraftMode } from '@/components/disable-draft-mode'

export default async function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        {(await draftMode()).isEnabled && (
          <>
            <DisableDraftMode />
            <VisualEditing />
          </>
        )}
      </body>
    </html>
  )
}
```

### Disable Draft Mode Button

Useful for content authors to exit preview and see published content:

```typescript
// src/components/disable-draft-mode.tsx
'use client'
import { useDraftModeEnvironment } from 'next-sanity/hooks'

export function DisableDraftMode() {
  const environment = useDraftModeEnvironment()
  // Only show outside of Presentation Tool
  if (environment !== 'live' && environment !== 'unknown') return null

  return (
    <a href="/api/draft-mode/disable" className="fixed bottom-4 right-4 bg-gray-50 px-4 py-2">
      Disable Draft Mode
    </a>
  )
}
```

**Remix/Svelte:** See framework-specific rules for `useLiveMode` and `enableVisualEditing` patterns.

## 6. SEO & Metadata (Critical)

**NEVER** allow Stega strings in `<head>` tags (Title, Description, Canonical URLs). It destroys SEO rankings and looks broken in search results.

-   **Next.js:** Set `stega: false` in `generateMetadata`.
-   **General:** Explicitly clean fields used in `<title>` or `<meta>`.

```typescript
// Next.js Example — disable stega at fetch level
export async function generateMetadata({ params }) {
  const { data } = await sanityFetch({
    query: SEO_QUERY,
    stega: false // Critical
  })
  return { title: data.title }
}
```

**Alternative:** If you can't disable stega at the fetch level, clean explicitly:

```typescript
import { stegaClean } from "@sanity/client/stega";

export async function generateMetadata({ params }) {
  const { data } = await sanityFetch({ query: PAGE_QUERY })
  return { 
    title: stegaClean(data.title),
    description: stegaClean(data.description),
    openGraph: { url: stegaClean(data.canonicalUrl) }
  }
}
```

## 7. Drag-and-Drop Reordering (Advanced)

For arrays (e.g., "Related Posts"), enable drag-and-drop in the preview using `data-sanity` attributes and `useOptimistic`:

```typescript
import { createDataAttribute } from 'next-sanity'
import { useOptimistic } from 'next-sanity/hooks'

// Add data-sanity to array container
<ul data-sanity={createDataAttribute({ id: documentId, type: 'post', path: 'relatedPosts' }).toString()}>
  {items.map((item) => (
    <li key={item._key} data-sanity={createDataAttribute({
      id: documentId, type: 'post', path: `relatedPosts[_key=="${item._key}"]`
    }).toString()}>
      {item.title}
    </li>
  ))}
</ul>
```

**Key requirements:**
- Query must include `_key` for array items
- Use `useOptimistic` hook for instant UI updates during mutations

## 8. Optimistic Updates for Faster Editing

By default, editing a field in the Presentation Tool triggers a full page re-render. For pages with many components, this can feel sluggish. **Presentation queries** solve this by fetching only the specific block being edited.

### The Concept

Instead of:
1. User edits a field -> Full page query re-runs -> All components re-render

You get:
1. User edits a field -> Block-specific query runs -> Only that component re-renders

### How It Works

1. **Create a targeted query** that fetches just the block data using `_key`:

```groq
*[_id == $documentId][0]{
  "heroBlock": pageBuilder[_key == $blockKey && _type == "hero"][0]{
    title, subtitle, image
  }
}
```

2. **Use a presentation query hook** in your component (e.g., `usePresentationQuery` in Next.js)

3. **Fall back to initial props** when not in presentation mode

This pattern works for both Page Builder blocks (`pageBuilder[]`) and Portable Text blocks (`body[]`).

**See framework-specific rules for implementation:**
- Next.js: `nextjs.md` (Section 9)
- Page Builder: `page-builder.md` (Section 5)
- Portable Text: `portable-text.md` (Section 7)

## 9. Framework Specifics

| Framework | Loader Package | Key Components |
| :--- | :--- | :--- |
| **Next.js** | `next-sanity` | `<VisualEditing />`, `defineLive`, `usePresentationQuery` |
| **Remix** | `@sanity/react-loader` | `createQueryStore`, `useLiveMode`, `enableVisualEditing` |
| **Svelte** | `@sanity/svelte-loader` | `createRequestHandler`, `useLiveMode`, `enableVisualEditing` |
| **Nuxt** | `@nuxtjs/sanity` | Automatic via module config (`visualEditing: {}`) |
| **Astro** | `@sanity/astro` | `sanity({ useCdn: false, stega: true })` |
