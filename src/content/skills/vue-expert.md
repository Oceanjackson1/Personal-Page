---
title: "Vue.js 专家"
description: "Vue.js 框架高级开发，组合式 API、状态管理和性能优化"
category: "development"
source: "community"
author: "Community"
tags: ["vue"]
date: 2026-03-20
---

# Vue Expert

Senior Vue specialist with deep expertise in Vue 3 Composition API, reactivity system, and modern Vue ecosystem.

## Core Workflow

1. **Analyze requirements** - Identify component hierarchy, state needs, routing
2. **Design architecture** - Plan composables, stores, component structure
3. **Implement** - Build components with Composition API and proper reactivity
4. **Validate** - Run `vue-tsc --noEmit` for type errors; verify reactivity with Vue DevTools. If type errors are found: fix each issue and re-run `vue-tsc --noEmit` until the output is clean before proceeding
5. **Optimize** - Minimize re-renders, optimize computed properties, lazy load
6. **Test** - Write component tests with Vue Test Utils and Vitest. If tests fail: inspect failure output, identify whether the root cause is a component bug or an incorrect test assertion, fix accordingly, and re-run until all tests pass

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Composition API | `references/composition-api.md` | ref, reactive, computed, watch, lifecycle |
| Components | `references/components.md` | Props, emits, slots, provide/inject |
| State Management | `references/state-management.md` | Pinia stores, actions, getters |
| Nuxt 3 | `references/nuxt.md` | SSR, file-based routing, useFetch, Fastify, hydration |
| TypeScript | `references/typescript.md` | Typing props, generic components, type safety |
| Mobile & Hybrid | `references/mobile-hybrid.md` | Quasar, Capacitor, PWA, service worker, mobile |
| Build Tooling | `references/build-tooling.md` | Vite config, sourcemaps, optimization, bundling |

## Quick Example

Minimal component demonstrating preferred patterns:

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{ initialCount?: number }>()

const count = ref(props.initialCount ?? 0)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
}
</script>

<template>
  <button @click="increment">Count: {{ count }} (doubled: {{ doubled }})</button>
</template>
```

## Constraints

### MUST DO
- Use Composition API (NOT Options API)
- Use `<script setup>` syntax for components
- Use type-safe props with TypeScript
- Use `ref()` for primitives, `reactive()` for objects
- Use `computed()` for derived state
- Use proper lifecycle hooks (onMounted, onUnmounted, etc.)
- Implement proper cleanup in composables
- Use Pinia for global state management

### MUST NOT DO
- Use Options API (data, methods, computed as object)
- Mix Composition API with Options API
- Mutate props directly
- Create reactive objects unnecessarily
- Use watch when computed is sufficient
- Forget to cleanup watchers and effects
- Access DOM before onMounted
- Use Vuex (deprecated in favor of Pinia)

## Output Templates

When implementing Vue features, provide:
1. Component file with `<script setup>` and TypeScript
2. Composable if reusable logic exists
3. Pinia store if global state needed
4. Brief explanation of reactivity decisions

## Knowledge Reference

Vue 3 Composition API, Pinia, Nuxt 3, Vue Router 4, Vite, VueUse, TypeScript, Vitest, Vue Test Utils, SSR/SSG, reactive programming, performance optimization

---

## Reference: Build Tooling

# Build Tooling & Vite

---

## Vite Configuration for Vue

### Basic Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
      '@composables': fileURLToPath(new URL('./src/composables', import.meta.url)),
      '@stores': fileURLToPath(new URL('./src/stores', import.meta.url))
    }
  }
})
```

### Essential Plugins

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import { QuasarResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),

    // Vue DevTools integration
    VueDevTools(),

    // Auto-import components
    Components({
      dirs: ['src/components'],
      resolvers: [QuasarResolver()],
      dts: 'src/components.d.ts'
    }),

    // Auto-import Vue APIs
    AutoImport({
      imports: ['vue', 'vue-router', 'pinia'],
      dts: 'src/auto-imports.d.ts',
      dirs: ['src/composables'],
      vueTemplate: true
    })
  ]
})
```

### Environment Variables

```typescript
// .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App

// .env.development
VITE_API_URL=http://localhost:3000

// .env.production
VITE_API_URL=https://api.production.com
```

```typescript
// Usage in code
const apiUrl = import.meta.env.VITE_API_URL
const isDev = import.meta.env.DEV
const isProd = import.meta.env.PROD
const mode = import.meta.env.MODE

// Type declarations (env.d.ts)
/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_TITLE: string
}
```

```typescript
// vite.config.ts - Define global constants
export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString())
  }
})
```

### Dev Server Proxy

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/ws': {
        target: 'ws://localhost:3000',
        ws: true
      }
    }
  }
})
```

---

## Sourcemaps Configuration

### Development Sourcemaps

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    // Full sourcemaps for development
    sourcemap: true
  }
})
```

### Production Sourcemaps

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    // Options: true | 'inline' | 'hidden' | false
    sourcemap: process.env.NODE_ENV === 'production' ? 'hidden' : true
  }
})
```

| Mode | Value | Use Case |
|------|-------|----------|
| Full | `true` | Development, staging |
| Hidden | `'hidden'` | Production with error tracking |
| Inline | `'inline'` | Single-file debugging |
| None | `false` | Production without debugging |

### VS Code Debugging

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Vue App",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src",
      "sourceMapPathOverrides": {
        "webpack:///./src/*": "${webRoot}/*"
      }
    }
  ]
}
```

### Sentry Error Tracking

```typescript
// vite.config.ts
import { sentryVitePlugin } from '@sentry/vite-plugin'

export default defineConfig({
  build: {
    sourcemap: true
  },
  plugins: [
    sentryVitePlugin({
      org: 'your-org',
      project: 'your-project',
      authToken: process.env.SENTRY_AUTH_TOKEN,
      sourcemaps: {
        assets: './dist/**',
        filesToDeleteAfterUpload: './dist/**/*.map'
      }
    })
  ]
})
```

---

## Build Optimization

### Tree Shaking Best Practices

```typescript
// Good: Named imports enable tree shaking
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { format, parseISO } from 'date-fns'

// Bad: Namespace imports include everything
import * as Vue from 'vue'
import * as dateFns from 'date-fns'
```

```typescript
// Ensure package.json has sideEffects for proper tree shaking
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "*.vue"
  ]
}
```

### Code Splitting & Lazy Loading

```typescript
// Route-based code splitting
const routes = [
  {
    path: '/dashboard',
    component: () => import('./views/Dashboard.vue')
  },
  {
    path: '/settings',
    component: () => import('./views/Settings.vue')
  }
]

// Component-level lazy loading
const HeavyChart = defineAsyncComponent(() =>
  import('./components/HeavyChart.vue')
)

// With loading/error states
const AsyncModal = defineAsyncComponent({
  loader: () => import('./components/Modal.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,
  timeout: 10000
})
```

### Manual Chunks Configuration

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunk for core dependencies
          'vendor': ['vue', 'vue-router', 'pinia'],

          // UI framework chunk
          'ui': ['quasar', '@quasar/extras'],

          // Utility libraries
          'utils': ['lodash-es', 'date-fns', 'axios']
        }
      }
    }
  }
})
```

```typescript
// Dynamic chunking by package
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // Split each package into its own chunk
            const packageName = id.split('node_modules/')[1].split('/')[0]
            return `vendor-${packageName}`
          }
        }
      }
    }
  }
})
```

### Chunk Size Optimization

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    // Warn if chunk exceeds 500KB
    chunkSizeWarningLimit: 500,

    rollupOptions: {
      output: {
        // Ensure CSS is extracted
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js'
      }
    }
  }
})
```

### Compression Plugins

```typescript
// vite.config.ts
import viteCompression from 'vite-plugin-compression'

export default defineConfig({
  plugins: [
    // Gzip compression
    viteCompression({
      algorithm: 'gzip',
      ext: '.gz',
      threshold: 1024
    }),

    // Brotli compression (better ratio)
    viteCompression({
      algorithm: 'brotliCompress',
      ext: '.br',
      threshold: 1024
    })
  ]
})
```

### Image Optimization

```typescript
// vite.config.ts
import viteImagemin from 'vite-plugin-imagemin'

export default defineConfig({
  plugins: [
    viteImagemin({
      gifsicle: { optimizationLevel: 3 },
      optipng: { optimizationLevel: 7 },
      mozjpeg: { quality: 80 },
      svgo: {
        plugins: [
          { name: 'removeViewBox', active: false },
          { name: 'removeEmptyAttrs', active: true }
        ]
      },
      webp: { quality: 80 }
    })
  ]
})
```

---

## Performance Analysis

### Bundle Analyzer

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    visualizer({
      filename: 'stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true,
      template: 'treemap' // or 'sunburst', 'network'
    })
  ]
})
```

```bash
# Generate analysis report
npm run build
# Opens stats.html automatically
```

### Build Performance

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    // Faster builds with esbuild minification
    minify: 'esbuild',

    // Target modern browsers only
    target: 'esnext',

    // Disable CSS code splitting for faster builds
    cssCodeSplit: false
  },

  // Optimize dependency pre-bundling
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', 'axios'],
    exclude: ['your-local-package']
  }
})
```

### Web Vitals Monitoring

```typescript
// src/utils/vitals.ts
import { onCLS, onFID, onLCP, onFCP, onTTFB } from 'web-vitals'

type VitalMetric = {
  name: string
  value: number
  rating: 'good' | 'needs-improvement' | 'poor'
}

function sendToAnalytics(metric: VitalMetric) {
  // Send to your analytics endpoint
  console.log(metric)
}

export function initVitals() {
  onCLS(sendToAnalytics)
  onFID(sendToAnalytics)
  onLCP(sendToAnalytics)
  onFCP(sendToAnalytics)
  onTTFB(sendToAnalytics)
}
```

```typescript
// main.ts
import { initVitals } from './utils/vitals'

if (import.meta.env.PROD) {
  initVitals()
}
```

---

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `@vitejs/plugin-vue` | Vue 3 SFC support |
| `unplugin-vue-components` | Auto-import components |
| `unplugin-auto-import` | Auto-import Vue APIs |
| `manualChunks` | Vendor code splitting |
| `sourcemap: 'hidden'` | Production error tracking |
| `vite-plugin-compression` | Gzip/Brotli compression |
| `rollup-plugin-visualizer` | Bundle size analysis |
| `import.meta.env.VITE_*` | Environment variables |
| `defineAsyncComponent` | Component lazy loading |
| `web-vitals` | Core Web Vitals monitoring |

---

## Reference: Components

# Components

## Props with TypeScript

```vue
<script setup lang="ts">
// Simple props
interface Props {
  title: string
  count?: number
  items: string[]
}

const props = defineProps<Props>()

// Props with defaults
const propsWithDefaults = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => []
})

// Runtime props (without TypeScript)
const runtimeProps = defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: Number,
    default: 0,
    validator: (value: number) => value >= 0
  },
  items: {
    type: Array as PropType<string[]>,
    default: () => []
  }
})

// Access props
console.log(props.title)
console.log(props.count)
</script>

<template>
  <div>
    <h1>{{ title }}</h1>
    <p>Count: {{ count }}</p>
  </div>
</template>
```

## Emits (Events)

```vue
<script setup lang="ts">
// TypeScript emits
interface Emits {
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
  (e: 'submit', payload: { name: string; email: string }): void
}

const emit = defineEmits<Emits>()

// Emit events
function handleUpdate() {
  emit('update', 'new value')
}

function handleDelete(id: number) {
  emit('delete', id)
}

function handleSubmit() {
  emit('submit', { name: 'John', email: 'john@example.com' })
}

// Runtime emits with validation
const runtimeEmit = defineEmits({
  update: (value: string) => {
    return value.length > 0
  },
  delete: (id: number) => {
    return id > 0
  }
})
</script>

<template>
  <button @click="handleUpdate">Update</button>
  <button @click="handleDelete(123)">Delete</button>
</template>
```

## v-model (Two-way Binding)

```vue
<!-- Parent Component -->
<script setup lang="ts">
import { ref } from 'vue'
import CustomInput from './CustomInput.vue'

const searchQuery = ref('')
const filters = ref({ category: '', price: 0 })
</script>

<template>
  <!-- Single v-model -->
  <CustomInput v-model="searchQuery" />

  <!-- Multiple v-models -->
  <FilterPanel
    v-model:category="filters.category"
    v-model:price="filters.price"
  />
</template>

<!-- CustomInput.vue -->
<script setup lang="ts">
interface Props {
  modelValue: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <input :value="modelValue" @input="handleInput" />
</template>

<!-- FilterPanel.vue with multiple v-models -->
<script setup lang="ts">
interface Props {
  category: string
  price: number
}

interface Emits {
  (e: 'update:category', value: string): void
  (e: 'update:price', value: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
</script>

<template>
  <select
    :value="category"
    @change="emit('update:category', ($event.target as HTMLSelectElement).value)"
  >
    <option value="books">Books</option>
    <option value="electronics">Electronics</option>
  </select>
  <input
    type="number"
    :value="price"
    @input="emit('update:price', Number(($event.target as HTMLInputElement).value))"
  />
</template>
```

## Slots

```vue
<!-- Parent Component -->
<template>
  <Card>
    <template #header>
      <h2>Card Title</h2>
    </template>

    <template #default>
      <p>Main content goes here</p>
    </template>

    <template #footer="{ close }">
      <button @click="close">Close</button>
    </template>
  </Card>
</template>

<!-- Card.vue -->
<script setup lang="ts">
import { useSlots } from 'vue'

const slots = useSlots()

// Check if slot exists
const hasHeader = !!slots.header
const hasFooter = !!slots.footer

function close() {
  console.log('Closing card')
}
</script>

<template>
  <div class="card">
    <div v-if="hasHeader" class="card-header">
      <slot name="header"></slot>
    </div>

    <div class="card-body">
      <slot></slot> <!-- Default slot -->
    </div>

    <div v-if="hasFooter" class="card-footer">
      <slot name="footer" :close="close"></slot> <!-- Scoped slot -->
    </div>
  </div>
</template>
```

## Scoped Slots (Advanced)

```vue
<!-- List Component with Scoped Slot -->
<script setup lang="ts" generic="T">
interface Props {
  items: T[]
}

const props = defineProps<Props>()
</script>

<template>
  <div class="list">
    <div v-for="(item, index) in items" :key="index">
      <slot :item="item" :index="index"></slot>
    </div>
  </div>
</template>

<!-- Usage -->
<template>
  <List :items="users">
    <template #default="{ item, index }">
      <div>{{ index }}: {{ item.name }}</div>
    </template>
  </List>
</template>
```

## Provide/Inject

```vue
<!-- Parent Component (Provider) -->
<script setup lang="ts">
import { provide, ref, readonly, InjectionKey } from 'vue'

// Type-safe injection key
interface UserData {
  name: string
  email: string
}

export const userKey = Symbol() as InjectionKey<UserData>

const user = ref<UserData>({
  name: 'John Doe',
  email: 'john@example.com'
})

function updateUser(newUser: UserData) {
  user.value = newUser
}

// Provide data
provide(userKey, readonly(user.value))
provide('updateUser', updateUser)
</script>

<!-- Child Component (Injector) -->
<script setup lang="ts">
import { inject } from 'vue'
import { userKey } from './Parent.vue'

// Inject with type safety
const user = inject(userKey)
const updateUser = inject<(user: UserData) => void>('updateUser')

// Inject with default value
const theme = inject('theme', 'light')

function handleUpdate() {
  if (updateUser) {
    updateUser({ name: 'Jane', email: 'jane@example.com' })
  }
}
</script>

<template>
  <div>
    <p>User: {{ user?.name }}</p>
    <p>Theme: {{ theme }}</p>
    <button @click="handleUpdate">Update User</button>
  </div>
</template>
```

## Teleport

```vue
<script setup lang="ts">
import { ref } from 'vue'

const showModal = ref(false)
</script>

<template>
  <button @click="showModal = true">Show Modal</button>

  <!-- Teleport to body -->
  <Teleport to="body">
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>Modal Title</h2>
        <p>Modal content</p>
        <button @click="showModal = false">Close</button>
      </div>
    </div>
  </Teleport>

  <!-- Teleport to specific element -->
  <Teleport to="#modal-container">
    <div class="notification">Notification message</div>
  </Teleport>

  <!-- Conditional teleport -->
  <Teleport to="body" :disabled="!isMobile">
    <div>Only teleported on mobile</div>
  </Teleport>
</template>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
}
</style>
```

## Dynamic Components

```vue
<script setup lang="ts">
import { ref, shallowRef, Component } from 'vue'
import HomeView from './HomeView.vue'
import AboutView from './AboutView.vue'
import ContactView from './ContactView.vue'

// Use shallowRef for component references (performance)
const currentView = shallowRef<Component>(HomeView)

const components = {
  home: HomeView,
  about: AboutView,
  contact: ContactView
}

function switchView(view: keyof typeof components) {
  currentView.value = components[view]
}
</script>

<template>
  <button @click="switchView('home')">Home</button>
  <button @click="switchView('about')">About</button>
  <button @click="switchView('contact')">Contact</button>

  <!-- Dynamic component with KeepAlive -->
  <KeepAlive>
    <component :is="currentView" />
  </KeepAlive>
</template>
```

## Async Components

```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

// Lazy load component
const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)

// With loading and error states
const AdminPanel = defineAsyncComponent({
  loader: () => import('./AdminPanel.vue'),
  loadingComponent: () => import('./LoadingSpinner.vue'),
  errorComponent: () => import('./ErrorDisplay.vue'),
  delay: 200, // Delay before showing loading component
  timeout: 3000 // Timeout before showing error
})
</script>

<template>
  <Suspense>
    <template #default>
      <HeavyComponent />
    </template>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </Suspense>
</template>
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `defineProps<T>()` | Type-safe props with TypeScript |
| `withDefaults()` | Props with default values |
| `defineEmits<T>()` | Type-safe event emitters |
| `v-model` | Two-way data binding |
| `<slot>` | Content distribution |
| Scoped slots | Pass data from child to parent |
| `provide/inject` | Dependency injection (avoid prop drilling) |
| `<Teleport>` | Render DOM outside component hierarchy |
| `<component :is>` | Dynamic component switching |
| `defineAsyncComponent()` | Lazy load components |

---

## Reference: Composition Api

# Composition API

## Script Setup Syntax

```vue
<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'

// Automatic component registration - no need to register in components option
import UserCard from './UserCard.vue'

// Props with TypeScript
interface Props {
  userId: number
  optional?: string
}
const props = withDefaults(defineProps<Props>(), {
  optional: 'default value'
})

// Emits with TypeScript
interface Emits {
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
}
const emit = defineEmits<Emits>()

// Reactive state
const count = ref(0)
const user = reactive({
  name: 'John',
  age: 30
})

// Computed
const doubled = computed(() => count.value * 2)

// Methods
function increment() {
  count.value++
  emit('update', count.value.toString())
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted')
})
</script>
```

## Ref vs Reactive

```typescript
import { ref, reactive, toRefs } from 'vue'

// Use ref() for primitives
const count = ref(0)
const message = ref('hello')
const isActive = ref(true)

// Access/modify with .value
count.value++
console.log(message.value)

// Use reactive() for objects
const state = reactive({
  count: 0,
  user: {
    name: 'John',
    email: 'john@example.com'
  }
})

// No .value needed for reactive
state.count++
state.user.name = 'Jane'

// Convert reactive to refs for destructuring
const { count: refCount, user } = toRefs(state)
// Now refCount.value works
```

## Computed Properties

```typescript
import { ref, computed } from 'vue'

const firstName = ref('John')
const lastName = ref('Doe')

// Read-only computed
const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`
})

// Writable computed
const fullNameWritable = computed({
  get() {
    return `${firstName.value} ${lastName.value}`
  },
  set(value: string) {
    const [first, last] = value.split(' ')
    firstName.value = first
    lastName.value = last
  }
})

// Computed with complex logic (cached until dependencies change)
const filteredItems = computed(() => {
  return items.value.filter(item =>
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
```

## Watchers

```typescript
import { ref, watch, watchEffect } from 'vue'

const count = ref(0)
const user = ref({ name: 'John', age: 30 })

// Watch single source
watch(count, (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`)
})

// Watch multiple sources
watch([count, user], ([newCount, newUser], [oldCount, oldUser]) => {
  console.log('Count or user changed')
})

// Watch with options
watch(
  () => user.value.name, // Getter function
  (newName) => {
    console.log(`Name changed to ${newName}`)
  },
  {
    immediate: true, // Run immediately
    deep: true // Deep watch for objects
  }
)

// watchEffect - automatically tracks dependencies
watchEffect(() => {
  console.log(`Count is ${count.value}`)
  // Automatically re-runs when count changes
})

// Cleanup and stop watching
const stop = watchEffect((onCleanup) => {
  const timer = setInterval(() => console.log('tick'), 1000)

  onCleanup(() => {
    clearInterval(timer)
  })
})

// Stop watching when needed
stop()
```

## Lifecycle Hooks

```typescript
import {
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
  onErrorCaptured
} from 'vue'

// Before component is mounted
onBeforeMount(() => {
  console.log('Before mount')
})

// After component is mounted (DOM is ready)
onMounted(() => {
  console.log('Mounted - DOM is ready')
  // Fetch data, setup event listeners, etc.
})

// Before component updates
onBeforeUpdate(() => {
  console.log('Before update')
})

// After component updates
onUpdated(() => {
  console.log('Updated')
})

// Before component is unmounted
onBeforeUnmount(() => {
  console.log('Before unmount - cleanup here')
})

// After component is unmounted
onUnmounted(() => {
  console.log('Unmounted')
  // Cleanup: remove event listeners, cancel timers, etc.
})

// Error handling
onErrorCaptured((err, instance, info) => {
  console.error('Error captured:', err, info)
  return false // Prevent error from propagating
})
```

## Composables Pattern

```typescript
// composables/useCounter.ts
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  const doubled = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = initialValue
  }

  return {
    count,
    doubled,
    increment,
    decrement,
    reset
  }
}

// Usage in component
<script setup lang="ts">
import { useCounter } from './composables/useCounter'

const { count, doubled, increment, decrement } = useCounter(10)
</script>
```

## Advanced Composable with Cleanup

```typescript
// composables/useEventListener.ts
import { onMounted, onUnmounted } from 'vue'

export function useEventListener(
  target: EventTarget,
  event: string,
  handler: EventListener
) {
  onMounted(() => {
    target.addEventListener(event, handler)
  })

  onUnmounted(() => {
    target.removeEventListener(event, handler)
  })
}

// Usage
<script setup lang="ts">
import { useEventListener } from './composables/useEventListener'

function handleClick(e: MouseEvent) {
  console.log('Clicked at:', e.clientX, e.clientY)
}

useEventListener(window, 'click', handleClick)
</script>
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `ref()` | Primitives (string, number, boolean) |
| `reactive()` | Objects and arrays |
| `computed()` | Derived state (cached) |
| `watch()` | Side effects on specific changes |
| `watchEffect()` | Auto-tracked side effects |
| `onMounted()` | DOM-dependent operations |
| `onUnmounted()` | Cleanup (timers, listeners) |
| Composables | Reusable stateful logic |

---

## Reference: Mobile Hybrid

# Mobile & Hybrid Apps

---

## Quasar Framework

### Project Setup

```bash
# Create new Quasar project
npm init quasar

# Add Quasar to existing Vue project
npm install quasar @quasar/extras
npm install -D @quasar/vite-plugin
```

```typescript
// vite.config.ts - Quasar plugin setup
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'

export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),
    quasar({
      sassVariables: 'src/quasar-variables.scss'
    })
  ]
})
```

### Quasar Configuration

```javascript
// quasar.config.js
export default configure((ctx) => ({
  // Build modes: spa, pwa, ssr, capacitor, electron, bex
  boot: ['axios', 'i18n'],

  css: ['app.scss'],

  extras: [
    'roboto-font',
    'material-icons'
  ],

  framework: {
    plugins: ['Notify', 'Dialog', 'Loading', 'LocalStorage'],
    config: {
      notify: { position: 'top-right' },
      loading: { spinnerColor: 'primary' }
    }
  },

  build: {
    target: { browser: ['es2022', 'firefox115', 'chrome115', 'safari14'] },
    vueRouterMode: 'history'
  }
}))
```

### Quasar Components with Composition API

```vue
<script setup lang="ts">
import { useQuasar } from 'quasar'

const $q = useQuasar()

function showNotification() {
  $q.notify({
    message: 'Action completed successfully',
    type: 'positive',
    position: 'top',
    timeout: 3000
  })
}

function showConfirmDialog() {
  $q.dialog({
    title: 'Confirm',
    message: 'Are you sure you want to proceed?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    // User confirmed
  })
}

async function showLoading() {
  $q.loading.show({ message: 'Processing...' })
  await doAsyncWork()
  $q.loading.hide()
}
</script>
```

### Layout System

```vue
<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="toggleLeftDrawer" />
        <q-toolbar-title>My App</q-toolbar-title>
        <q-btn flat round icon="person" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item clickable v-ripple to="/dashboard">
          <q-item-section avatar>
            <q-icon name="dashboard" />
          </q-item-section>
          <q-item-section>Dashboard</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
```

### Platform Detection

```vue
<script setup lang="ts">
import { useQuasar } from 'quasar'

const $q = useQuasar()

// Platform detection
const isMobile = $q.platform.is.mobile
const isIOS = $q.platform.is.ios
const isAndroid = $q.platform.is.android
const isDesktop = $q.platform.is.desktop
const isCapacitor = $q.platform.is.capacitor

// Screen utilities
const isSmallScreen = $q.screen.lt.md
const screenWidth = $q.screen.width
</script>

<template>
  <div>
    <MobileNav v-if="isMobile" />
    <DesktopNav v-else />
  </div>
</template>
```

---

## Capacitor Integration

### Setup

```bash
# Add Capacitor to Quasar
quasar mode add capacitor

# Initialize Capacitor
cd src-capacitor
npx cap init "App Name" "com.example.app"

# Add platforms
npx cap add android
npx cap add ios

# Sync and run
npx cap sync
npx cap open android
```

### Capacitor Configuration

```typescript
// capacitor.config.ts
import type { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.example.myapp',
  appName: 'My App',
  webDir: 'dist/spa',
  server: {
    androidScheme: 'https',
    // For development
    url: 'http://192.168.1.100:9000',
    cleartext: true
  },
  plugins: {
    SplashScreen: {
      launchAutoHide: false,
      showSpinner: true
    },
    PushNotifications: {
      presentationOptions: ['badge', 'sound', 'alert']
    }
  }
}

export default config
```

### Native Plugins with TypeScript

```typescript
// composables/useCamera.ts
import { ref } from 'vue'
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera'

export function useCamera() {
  const photo = ref<string | null>(null)
  const error = ref<string | null>(null)

  async function takePhoto() {
    try {
      const image = await Camera.getPhoto({
        resultType: CameraResultType.Uri,
        source: CameraSource.Camera,
        quality: 90
      })
      photo.value = image.webPath ?? null
    } catch (e) {
      error.value = (e as Error).message
    }
  }

  async function pickFromGallery() {
    try {
      const image = await Camera.getPhoto({
        resultType: CameraResultType.Uri,
        source: CameraSource.Photos,
        quality: 90
      })
      photo.value = image.webPath ?? null
    } catch (e) {
      error.value = (e as Error).message
    }
  }

  return { photo, error, takePhoto, pickFromGallery }
}
```

```typescript
// composables/useGeolocation.ts
import { ref, onMounted, onUnmounted } from 'vue'
import { Geolocation, Position } from '@capacitor/geolocation'

export function useGeolocation() {
  const position = ref<Position | null>(null)
  const error = ref<string | null>(null)
  let watchId: string | null = null

  async function getCurrentPosition() {
    try {
      position.value = await Geolocation.getCurrentPosition({
        enableHighAccuracy: true
      })
    } catch (e) {
      error.value = (e as Error).message
    }
  }

  async function watchPosition() {
    watchId = await Geolocation.watchPosition(
      { enableHighAccuracy: true },
      (pos, err) => {
        if (err) {
          error.value = err.message
        } else if (pos) {
          position.value = pos
        }
      }
    )
  }

  function stopWatching() {
    if (watchId) {
      Geolocation.clearWatch({ id: watchId })
      watchId = null
    }
  }

  onUnmounted(stopWatching)

  return { position, error, getCurrentPosition, watchPosition, stopWatching }
}
```

### Push Notifications

```typescript
// composables/usePushNotifications.ts
import { ref, onMounted } from 'vue'
import { PushNotifications, Token, PushNotificationSchema } from '@capacitor/push-notifications'
import { Capacitor } from '@capacitor/core'

export function usePushNotifications() {
  const token = ref<string | null>(null)
  const notifications = ref<PushNotificationSchema[]>([])

  async function register() {
    if (!Capacitor.isNativePlatform()) return

    const permission = await PushNotifications.requestPermissions()
    if (permission.receive !== 'granted') return

    await PushNotifications.register()
  }

  onMounted(() => {
    if (!Capacitor.isNativePlatform()) return

    PushNotifications.addListener('registration', (t: Token) => {
      token.value = t.value
    })

    PushNotifications.addListener('pushNotificationReceived', (notification) => {
      notifications.value.push(notification)
    })

    PushNotifications.addListener('pushNotificationActionPerformed', (action) => {
      // Handle notification tap
      console.log('Action:', action.actionId)
    })
  })

  return { token, notifications, register }
}
```

### App Lifecycle

```typescript
// composables/useAppLifecycle.ts
import { onMounted, onUnmounted } from 'vue'
import { App } from '@capacitor/app'
import { Capacitor } from '@capacitor/core'

export function useAppLifecycle() {
  onMounted(() => {
    if (!Capacitor.isNativePlatform()) return

    App.addListener('appStateChange', ({ isActive }) => {
      if (isActive) {
        // App came to foreground
        refreshData()
      } else {
        // App went to background
        saveState()
      }
    })

    App.addListener('backButton', ({ canGoBack }) => {
      if (!canGoBack) {
        App.exitApp()
      } else {
        window.history.back()
      }
    })
  })

  onUnmounted(() => {
    App.removeAllListeners()
  })
}
```

---

## PWA & Service Workers

### Workbox Configuration

```javascript
// quasar.config.js
export default configure((ctx) => ({
  pwa: {
    workboxMode: 'GenerateSW', // or 'InjectManifest'

    workboxOptions: {
      skipWaiting: true,
      clientsClaim: true,
      cleanupOutdatedCaches: true,

      // Cache strategies
      runtimeCaching: [
        {
          // Cache API responses
          urlPattern: /^https:\/\/api\./,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            networkTimeoutSeconds: 10,
            expiration: {
              maxEntries: 100,
              maxAgeSeconds: 60 * 60 * 24 // 24 hours
            }
          }
        },
        {
          // Cache images
          urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
          handler: 'CacheFirst',
          options: {
            cacheName: 'image-cache',
            expiration: {
              maxEntries: 50,
              maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
            }
          }
        },
        {
          // Cache fonts
          urlPattern: /\.(?:woff|woff2|ttf|eot)$/,
          handler: 'CacheFirst',
          options: {
            cacheName: 'font-cache',
            expiration: {
              maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
            }
          }
        }
      ]
    }
  }
}))
```

### Web App Manifest

```javascript
// quasar.config.js
export default configure((ctx) => ({
  pwa: {
    manifest: {
      name: 'My Progressive App',
      short_name: 'MyApp',
      description: 'A Progressive Web Application',
      display: 'standalone',
      orientation: 'portrait',
      background_color: '#ffffff',
      theme_color: '#1976D2',
      start_url: '/',
      icons: [
        {
          src: 'icons/icon-128x128.png',
          sizes: '128x128',
          type: 'image/png'
        },
        {
          src: 'icons/icon-512x512.png',
          sizes: '512x512',
          type: 'image/png'
        }
      ]
    }
  }
}))
```

### Install Prompt Handling

```typescript
// composables/usePWAInstall.ts
import { ref, onMounted } from 'vue'

interface BeforeInstallPromptEvent extends Event {
  prompt(): Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
}

export function usePWAInstall() {
  const canInstall = ref(false)
  const isInstalled = ref(false)
  let deferredPrompt: BeforeInstallPromptEvent | null = null

  onMounted(() => {
    // Check if already installed
    isInstalled.value = window.matchMedia('(display-mode: standalone)').matches

    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault()
      deferredPrompt = e as BeforeInstallPromptEvent
      canInstall.value = true
    })

    window.addEventListener('appinstalled', () => {
      isInstalled.value = true
      canInstall.value = false
      deferredPrompt = null
    })
  })

  async function install() {
    if (!deferredPrompt) return false

    await deferredPrompt.prompt()
    const { outcome } = await deferredPrompt.userChoice

    deferredPrompt = null
    canInstall.value = false

    return outcome === 'accepted'
  }

  return { canInstall, isInstalled, install }
}
```

### PWA Update Flow

```typescript
// composables/usePWAUpdate.ts
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'

export function usePWAUpdate() {
  const $q = useQuasar()
  const needsUpdate = ref(false)
  let registration: ServiceWorkerRegistration | null = null

  onMounted(() => {
    if (!('serviceWorker' in navigator)) return

    navigator.serviceWorker.ready.then((reg) => {
      registration = reg

      reg.addEventListener('updatefound', () => {
        const newWorker = reg.installing
        if (!newWorker) return

        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            needsUpdate.value = true
            promptUpdate()
          }
        })
      })
    })
  })

  function promptUpdate() {
    $q.notify({
      message: 'A new version is available',
      timeout: 0,
      actions: [
        {
          label: 'Update',
          color: 'white',
          handler: updateApp
        },
        {
          label: 'Later',
          color: 'white'
        }
      ]
    })
  }

  function updateApp() {
    if (registration?.waiting) {
      registration.waiting.postMessage({ type: 'SKIP_WAITING' })
    }
    window.location.reload()
  }

  return { needsUpdate, updateApp }
}
```

### Offline Detection

```typescript
// composables/useOnlineStatus.ts
import { ref, onMounted, onUnmounted } from 'vue'

export function useOnlineStatus() {
  const isOnline = ref(navigator.onLine)

  function updateOnlineStatus() {
    isOnline.value = navigator.onLine
  }

  onMounted(() => {
    window.addEventListener('online', updateOnlineStatus)
    window.addEventListener('offline', updateOnlineStatus)
  })

  onUnmounted(() => {
    window.removeEventListener('online', updateOnlineStatus)
    window.removeEventListener('offline', updateOnlineStatus)
  })

  return { isOnline }
}
```

---

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `useQuasar()` | Access Quasar plugins ($q) |
| `$q.platform.is.*` | Platform detection |
| `$q.notify()` | Toast notifications |
| `$q.dialog()` | Modal dialogs |
| `@capacitor/camera` | Native camera access |
| `@capacitor/geolocation` | GPS location |
| `@capacitor/push-notifications` | Push notifications |
| `workboxMode: 'GenerateSW'` | Auto-generate service worker |
| `runtimeCaching` | Workbox cache strategies |
| `beforeinstallprompt` | PWA install prompt |
| `navigator.serviceWorker.ready` | Service worker lifecycle |

---

## Reference: Nuxt

# Nuxt 3

## Project Structure

```
my-nuxt-app/
├── app.vue              # Root component (optional)
├── nuxt.config.ts       # Nuxt configuration
├── package.json
├── tsconfig.json
├── .output/             # Build output
├── assets/              # Uncompiled assets (CSS, images)
├── public/              # Static files (served at root)
├── components/          # Auto-imported components
│   ├── AppHeader.vue
│   └── base/
│       └── Button.vue   # Used as <BaseButton>
├── composables/         # Auto-imported composables
│   └── useAuth.ts
├── layouts/             # Layout components
│   ├── default.vue
│   └── admin.vue
├── middleware/          # Route middleware
│   └── auth.ts
├── pages/               # File-based routing
│   ├── index.vue        # /
│   ├── about.vue        # /about
│   ├── users/
│   │   ├── index.vue    # /users
│   │   └── [id].vue     # /users/:id
│   └── [...slug].vue    # Catch-all route
├── plugins/             # Plugins
│   └── api.ts
├── server/              # Server API routes
│   ├── api/
│   │   └── users.ts     # /api/users
│   └── middleware/
│       └── log.ts
└── stores/              # Pinia stores
    └── user.ts
```

## File-based Routing

```vue
<!-- pages/index.vue -->
<script setup lang="ts">
definePageMeta({
  title: 'Home',
  layout: 'default'
})
</script>

<template>
  <div>
    <h1>Home Page</h1>
  </div>
</template>

<!-- pages/about.vue -->
<template>
  <div>About Page</div>
</template>

<!-- pages/users/[id].vue - Dynamic route -->
<script setup lang="ts">
const route = useRoute()
const userId = computed(() => route.params.id)

const { data: user } = await useFetch(`/api/users/${userId.value}`)
</script>

<template>
  <div>
    <h1>User: {{ user?.name }}</h1>
  </div>
</template>

<!-- pages/blog/[...slug].vue - Catch-all route -->
<script setup lang="ts">
const route = useRoute()
const slug = route.params.slug // ['2024', '12', 'my-post']
</script>

<template>
  <div>Blog post: {{ slug }}</div>
</template>
```

## Layouts

```vue
<!-- layouts/default.vue -->
<template>
  <div>
    <header>
      <nav>Navigation</nav>
    </header>
    <main>
      <slot /> <!-- Page content goes here -->
    </main>
    <footer>Footer</footer>
  </div>
</template>

<!-- layouts/admin.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: 'auth' // Protect with middleware
})
</script>

<template>
  <div class="admin-layout">
    <aside>Admin Sidebar</aside>
    <main>
      <slot />
    </main>
  </div>
</template>

<!-- pages/admin/dashboard.vue -->
<script setup lang="ts">
definePageMeta({
  layout: 'admin'
})
</script>

<template>
  <div>Admin Dashboard</div>
</template>
```

## Data Fetching

```vue
<script setup lang="ts">
interface User {
  id: number
  name: string
  email: string
}

// useFetch - SSR-safe, auto-imports
const { data: users, pending, error, refresh } = await useFetch<User[]>('/api/users')

// With options
const { data } = await useFetch('/api/users', {
  method: 'POST',
  body: { name: 'John' },
  headers: {
    'Authorization': 'Bearer token'
  },
  query: { page: 1, limit: 10 },
  // Transform response
  transform: (data) => data.map(u => ({ ...u, fullName: u.firstName + ' ' + u.lastName })),
  // Pick specific keys
  pick: ['id', 'name'],
  // Watch for changes
  watch: [page, limit]
})

// useAsyncData - More control
const { data: user } = await useAsyncData(
  'user-123', // Unique key for caching
  async () => {
    const response = await fetch('/api/users/123')
    return response.json()
  },
  {
    server: true, // Fetch on server
    lazy: false, // Don't block navigation
    default: () => null // Default value while loading
  }
)

// useLazyFetch - Non-blocking
const { data: posts } = await useLazyFetch('/api/posts')

// useLazyAsyncData - Non-blocking with custom fetcher
const { data: comments } = await useLazyAsyncData('comments', () =>
  $fetch('/api/comments')
)

// Manual refresh
function handleRefresh() {
  refresh() // Re-fetch data
}
</script>

<template>
  <div>
    <div v-if="pending">Loading...</div>
    <div v-else-if="error">Error: {{ error.message }}</div>
    <div v-else>
      <div v-for="user in users" :key="user.id">
        {{ user.name }}
      </div>
      <button @click="handleRefresh">Refresh</button>
    </div>
  </div>
</template>
```

## Server API Routes

```typescript
// server/api/users.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const page = Number(query.page) || 1
  const limit = Number(query.limit) || 10

  // Fetch from database
  const users = await prisma.user.findMany({
    skip: (page - 1) * limit,
    take: limit
  })

  return users
})

// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')

  const user = await prisma.user.findUnique({
    where: { id: Number(id) }
  })

  if (!user) {
    throw createError({
      statusCode: 404,
      message: 'User not found'
    })
  }

  return user
})

// server/api/users.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  // Validate
  if (!body.email || !body.name) {
    throw createError({
      statusCode: 400,
      message: 'Email and name are required'
    })
  }

  const user = await prisma.user.create({
    data: {
      email: body.email,
      name: body.name
    }
  })

  return user
})

// server/api/auth/login.post.ts
export default defineEventHandler(async (event) => {
  const { email, password } = await readBody(event)

  // Verify credentials
  const user = await verifyCredentials(email, password)

  if (!user) {
    throw createError({
      statusCode: 401,
      message: 'Invalid credentials'
    })
  }

  // Set session cookie
  setCookie(event, 'session', user.sessionToken, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 60 * 60 * 24 * 7 // 7 days
  })

  return { success: true, user }
})
```

## Middleware

```typescript
// middleware/auth.ts - Route middleware
export default defineNuxtRouteMiddleware((to, from) => {
  const { isLoggedIn } = useAuthStore()

  if (!isLoggedIn) {
    return navigateTo('/login')
  }
})

// middleware/logger.global.ts - Global middleware
export default defineNuxtRouteMiddleware((to, from) => {
  console.log(`Navigating from ${from.path} to ${to.path}`)
})

// server/middleware/log.ts - Server middleware
export default defineEventHandler((event) => {
  console.log(`[${event.method}] ${event.path}`)
})
```

## Composables

```typescript
// composables/useAuth.ts - Auto-imported
export const useAuth = () => {
  const user = useState<User | null>('user', () => null)
  const isLoggedIn = computed(() => user.value !== null)

  async function login(email: string, password: string) {
    const { data, error } = await useFetch('/api/auth/login', {
      method: 'POST',
      body: { email, password }
    })

    if (data.value) {
      user.value = data.value.user
    }

    return { data, error }
  }

  async function logout() {
    await useFetch('/api/auth/logout', { method: 'POST' })
    user.value = null
    navigateTo('/login')
  }

  async function fetchUser() {
    const { data } = await useFetch('/api/auth/me')
    user.value = data.value
  }

  return {
    user,
    isLoggedIn,
    login,
    logout,
    fetchUser
  }
}

// Usage in component (auto-imported)
<script setup lang="ts">
const { user, isLoggedIn, login, logout } = useAuth()
</script>
```

## Plugins

```typescript
// plugins/api.ts
export default defineNuxtPlugin((nuxtApp) => {
  const api = $fetch.create({
    baseURL: '/api',
    onRequest({ options }) {
      // Add auth token
      const token = useCookie('token')
      if (token.value) {
        options.headers = options.headers || {}
        options.headers.Authorization = `Bearer ${token.value}`
      }
    },
    onResponseError({ response }) {
      if (response.status === 401) {
        navigateTo('/login')
      }
    }
  })

  return {
    provide: {
      api
    }
  }
})

// Usage in component
<script setup lang="ts">
const { $api } = useNuxtApp()
const users = await $api('/users')
</script>
```

## Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
    '@vueuse/nuxt'
  ],

  runtimeConfig: {
    // Server-only (never exposed to client)
    apiSecret: process.env.API_SECRET,

    // Exposed to client
    public: {
      apiBase: process.env.API_BASE || '/api'
    }
  },

  app: {
    head: {
      title: 'My App',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'My amazing site' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  },

  css: ['~/assets/css/main.css'],

  typescript: {
    strict: true,
    typeCheck: true
  },

  // Vite is the default bundler in Nuxt 3
  // Note: webpack is deprecated - use Vite for all new projects
  vite: {
    optimizeDeps: {
      include: ['vue', 'vue-router', 'pinia']
    },
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            'vendor': ['vue', 'pinia']
          }
        }
      }
    }
  },

  nitro: {
    preset: 'vercel' // or 'node-server', 'cloudflare', 'bun', etc.
  }
})
```

## SEO and Meta Tags

```vue
<script setup lang="ts">
const route = useRoute()
const title = computed(() => `User ${route.params.id}`)

useHead({
  title,
  meta: [
    { name: 'description', content: 'User profile page' },
    { property: 'og:title', content: title },
    { property: 'og:description', content: 'User profile' }
  ]
})

// Or use useSeoMeta
useSeoMeta({
  title: 'My Page',
  ogTitle: 'My Page',
  description: 'Page description',
  ogDescription: 'Page description',
  ogImage: 'https://example.com/image.png'
})
</script>
```

## Custom SSR with Fastify (Non-Nuxt)

For custom Vue 3 SSR without Nuxt, using Fastify as the server:

```typescript
// server.ts
import Fastify from 'fastify'
import { createSSRApp } from 'vue'
import { renderToString } from 'vue/server-renderer'
import App from './App.vue'

const fastify = Fastify({ logger: true })

fastify.get('*', async (request, reply) => {
  const app = createSSRApp(App)

  // Server-side data fetching
  const initialState = await fetchInitialData(request.url)

  const html = await renderToString(app)

  reply.type('text/html').send(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Vue SSR</title>
        <script>window.__INITIAL_STATE__ = ${JSON.stringify(initialState)}</script>
      </head>
      <body>
        <div id="app">${html}</div>
        <script type="module" src="/src/entry-client.ts"></script>
      </body>
    </html>
  `)
})

fastify.listen({ port: 3000 })
```

```typescript
// entry-client.ts
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

// Hydrate with server state
if (window.__INITIAL_STATE__) {
  app.provide('initialState', window.__INITIAL_STATE__)
}

app.mount('#app')
```

```typescript
// vite.config.ts for SSR
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    ssr: true,
    rollupOptions: {
      input: {
        server: './server.ts',
        client: './src/entry-client.ts'
      }
    }
  }
})
```

## Hydration Patterns

### Lazy Hydration with ClientOnly

```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

// Heavy component loaded only on client
const HeavyChart = defineAsyncComponent(() =>
  import('./components/HeavyChart.vue')
)
</script>

<template>
  <ClientOnly>
    <HeavyChart />
    <template #fallback>
      <div class="chart-skeleton">Loading chart...</div>
    </template>
  </ClientOnly>
</template>
```

### Hydration Mismatch Prevention

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Avoid hydration mismatch for client-only values
const currentTime = ref<string | null>(null)
const windowWidth = ref<number | null>(null)

onMounted(() => {
  // These values differ between server and client
  currentTime.value = new Date().toLocaleTimeString()
  windowWidth.value = window.innerWidth
})
</script>

<template>
  <div>
    <!-- Use v-if to prevent mismatch -->
    <span v-if="currentTime">{{ currentTime }}</span>
    <span v-else>--:--:--</span>

    <!-- Or use ClientOnly -->
    <ClientOnly>
      <span>Width: {{ windowWidth }}px</span>
    </ClientOnly>
  </div>
</template>
```

### Progressive Hydration

```vue
<script setup lang="ts">
// Use nuxt-delay-hydration for non-critical content
definePageMeta({
  // Delay hydration until visible or idle
  hydration: 'when-visible' // or 'on-idle'
})
</script>

<template>
  <div>
    <!-- Critical content hydrates immediately -->
    <header>Navigation</header>

    <!-- Non-critical content can wait -->
    <LazyBelowFoldContent />
  </div>
</template>
```

```typescript
// nuxt.config.ts - Configure delay hydration
export default defineNuxtConfig({
  modules: ['nuxt-delay-hydration'],

  delayHydration: {
    mode: 'init', // or 'mount'
    debug: process.env.NODE_ENV === 'development'
  }
})
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `useFetch()` | Fetch data (SSR-safe) |
| `useAsyncData()` | Custom async operations |
| `useLazyFetch()` | Non-blocking fetch |
| `useState()` | Shared state across components |
| `useRoute()` | Access route params/query |
| `useRouter()` | Navigate programmatically |
| `navigateTo()` | Navigate to route |
| `definePageMeta()` | Page-level metadata |
| `useHead()` | Dynamic meta tags |
| Server routes | `/server/api/*.ts` |
| Auto-imports | Components, composables, utils |
| `<ClientOnly>` | Client-only rendering, prevent hydration mismatch |
| `renderToString()` | Custom SSR with Fastify/Express |
| `vite: {}` | Vite configuration in nuxt.config.ts |
| `nuxt-delay-hydration` | Progressive hydration for performance |

---

## Reference: State Management

# State Management with Pinia

## Basic Store Setup

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Setup Stores (Composition API style) - RECOMMENDED
export const useCounterStore = defineStore('counter', () => {
  // State
  const count = ref(0)
  const name = ref('Counter')

  // Getters (computed)
  const doubleCount = computed(() => count.value * 2)
  const isEven = computed(() => count.value % 2 === 0)

  // Actions
  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = 0
  }

  async function incrementAsync() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    count.value++
  }

  return {
    // State
    count,
    name,
    // Getters
    doubleCount,
    isEven,
    // Actions
    increment,
    decrement,
    reset,
    incrementAsync
  }
})

// Usage in component
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'
import { storeToRefs } from 'pinia'

const counter = useCounterStore()

// Use storeToRefs to maintain reactivity when destructuring
const { count, doubleCount, isEven } = storeToRefs(counter)

// Actions can be destructured directly (they don't need refs)
const { increment, decrement } = counter
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Double: {{ doubleCount }}</p>
    <p>Is Even: {{ isEven }}</p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
  </div>
</template>
```

## Options Store (Alternative Style)

```typescript
// stores/user.ts
import { defineStore } from 'pinia'

interface User {
  id: number
  name: string
  email: string
}

interface UserState {
  user: User | null
  users: User[]
  loading: boolean
}

export const useUserStore = defineStore('user', {
  // State
  state: (): UserState => ({
    user: null,
    users: [],
    loading: false
  }),

  // Getters
  getters: {
    isLoggedIn: (state) => state.user !== null,
    userCount: (state) => state.users.length,

    // Getter with parameters
    getUserById: (state) => {
      return (userId: number) => state.users.find(u => u.id === userId)
    },

    // Getter accessing other getters
    activeUserCount(): number {
      return this.users.filter(u => u.isActive).length
    }
  },

  // Actions
  actions: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await fetch('/api/users')
        this.users = await response.json()
      } catch (error) {
        console.error('Failed to fetch users:', error)
      } finally {
        this.loading = false
      }
    },

    async login(email: string, password: string) {
      this.loading = true
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        })
        this.user = await response.json()
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
    },

    // Action calling another action
    async refreshUserData() {
      if (this.user) {
        await this.fetchUsers()
      }
    }
  }
})
```

## Store with TypeScript

```typescript
// stores/todos.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface Todo {
  id: number
  title: string
  completed: boolean
  createdAt: Date
}

type TodoFilter = 'all' | 'active' | 'completed'

export const useTodoStore = defineStore('todos', () => {
  // State
  const todos = ref<Todo[]>([])
  const filter = ref<TodoFilter>('all')
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const filteredTodos = computed(() => {
    switch (filter.value) {
      case 'active':
        return todos.value.filter(t => !t.completed)
      case 'completed':
        return todos.value.filter(t => t.completed)
      default:
        return todos.value
    }
  })

  const completedCount = computed(() =>
    todos.value.filter(t => t.completed).length
  )

  const activeCount = computed(() =>
    todos.value.filter(t => !t.completed).length
  )

  // Actions
  async function fetchTodos() {
    loading.value = true
    error.value = null
    try {
      const response = await fetch('/api/todos')
      if (!response.ok) throw new Error('Failed to fetch todos')
      todos.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  function addTodo(title: string) {
    const newTodo: Todo = {
      id: Date.now(),
      title,
      completed: false,
      createdAt: new Date()
    }
    todos.value.push(newTodo)
  }

  function toggleTodo(id: number) {
    const todo = todos.value.find(t => t.id === id)
    if (todo) {
      todo.completed = !todo.completed
    }
  }

  function deleteTodo(id: number) {
    const index = todos.value.findIndex(t => t.id === id)
    if (index > -1) {
      todos.value.splice(index, 1)
    }
  }

  function setFilter(newFilter: TodoFilter) {
    filter.value = newFilter
  }

  function clearCompleted() {
    todos.value = todos.value.filter(t => !t.completed)
  }

  return {
    // State
    todos,
    filter,
    loading,
    error,
    // Getters
    filteredTodos,
    completedCount,
    activeCount,
    // Actions
    fetchTodos,
    addTodo,
    toggleTodo,
    deleteTodo,
    setFilter,
    clearCompleted
  }
})
```

## Accessing Other Stores

```typescript
// stores/cart.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useUserStore } from './user'
import { useProductStore } from './product'

interface CartItem {
  productId: number
  quantity: number
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])

  const userStore = useUserStore()
  const productStore = useProductStore()

  const total = computed(() => {
    return items.value.reduce((sum, item) => {
      const product = productStore.getProductById(item.productId)
      return sum + (product?.price || 0) * item.quantity
    }, 0)
  })

  function addItem(productId: number, quantity = 1) {
    const existingItem = items.value.find(i => i.productId === productId)
    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      items.value.push({ productId, quantity })
    }
  }

  async function checkout() {
    if (!userStore.isLoggedIn) {
      throw new Error('User must be logged in to checkout')
    }

    // Checkout logic
    const order = {
      userId: userStore.user?.id,
      items: items.value,
      total: total.value
    }

    // Make API call
    await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(order)
    })

    items.value = []
  }

  return { items, total, addItem, checkout }
})
```

## Store Plugins

```typescript
// plugins/pinia-logger.ts
import { PiniaPluginContext } from 'pinia'

export function piniaLogger({ store }: PiniaPluginContext) {
  store.$subscribe((mutation, state) => {
    console.log(`[${store.$id}]:`, mutation.type, mutation.payload)
    console.log('New state:', state)
  })
}

// main.ts
import { createPinia } from 'pinia'
import { piniaLogger } from './plugins/pinia-logger'

const pinia = createPinia()
pinia.use(piniaLogger)

app.use(pinia)
```

## Persistence Plugin

```typescript
// Install: npm install pinia-plugin-persistedstate

// main.ts
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// stores/settings.ts
export const useSettingsStore = defineStore('settings', () => {
  const theme = ref<'light' | 'dark'>('light')
  const language = ref('en')

  function setTheme(newTheme: 'light' | 'dark') {
    theme.value = newTheme
  }

  return { theme, language, setTheme }
}, {
  persist: true // Auto-persist to localStorage
})

// Advanced persistence
export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<User | null>(null)

  return { token, user }
}, {
  persist: {
    key: 'auth-storage',
    storage: sessionStorage,
    paths: ['token'] // Only persist token, not user
  }
})
```

## Store Testing

```typescript
// stores/__tests__/counter.spec.ts
import { setActivePinia, createPinia } from 'pinia'
import { describe, it, expect, beforeEach } from 'vitest'
import { useCounterStore } from '../counter'

describe('Counter Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('increments count', () => {
    const counter = useCounterStore()
    expect(counter.count).toBe(0)
    counter.increment()
    expect(counter.count).toBe(1)
  })

  it('doubles count', () => {
    const counter = useCounterStore()
    counter.count = 5
    expect(counter.doubleCount).toBe(10)
  })

  it('resets count', () => {
    const counter = useCounterStore()
    counter.count = 10
    counter.reset()
    expect(counter.count).toBe(0)
  })
})
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| Setup stores | Composition API style (recommended) |
| Options stores | Traditional Vuex-like syntax |
| `storeToRefs()` | Maintain reactivity when destructuring |
| `store.$subscribe()` | Watch for state changes |
| `store.$patch()` | Batch state updates |
| `store.$reset()` | Reset state to initial |
| Plugins | Add global functionality (logger, persistence) |
| Accessing stores | Use other stores in actions |
| Testing | Use `setActivePinia()` for isolated tests |

---

## Reference: Typescript

# TypeScript with Vue 3

## Component Props Typing

```vue
<script setup lang="ts">
// Basic interface
interface Props {
  title: string
  count: number
  items: string[]
  optional?: boolean
}

const props = defineProps<Props>()

// Props with defaults
const propsWithDefaults = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => [],
  optional: false
})

// Union types
interface PropsWithUnion {
  status: 'success' | 'error' | 'warning'
  size: 'sm' | 'md' | 'lg'
}

// Complex types
interface User {
  id: number
  name: string
  email: string
}

interface ComplexProps {
  user: User
  users: User[]
  callback: (id: number) => void
  config: Record<string, unknown>
}

const complexProps = defineProps<ComplexProps>()
</script>
```

## Emits Typing

```vue
<script setup lang="ts">
// Type-safe emits
interface Emits {
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
  (e: 'submit', payload: { name: string; email: string }): void
}

const emit = defineEmits<Emits>()

// Usage
function handleUpdate(value: string) {
  emit('update', value) // Type-safe
  // emit('update', 123) // Error: number not assignable to string
}

// Alternative syntax
type EmitsType = {
  update: [value: string]
  delete: [id: number]
  submit: [payload: { name: string; email: string }]
}

const emit2 = defineEmits<EmitsType>()
</script>
```

## Ref Typing

```vue
<script setup lang="ts">
import { ref, Ref } from 'vue'

// Type inference
const count = ref(0) // Ref<number>
const message = ref('hello') // Ref<string>

// Explicit typing
const user = ref<User | null>(null)
const items = ref<string[]>([])

// Complex types
interface FormData {
  username: string
  email: string
  age: number
}

const form = ref<FormData>({
  username: '',
  email: '',
  age: 0
})

// Ref as function parameter
function updateCount(countRef: Ref<number>) {
  countRef.value++
}

updateCount(count)
</script>
```

## Reactive Typing

```vue
<script setup lang="ts">
import { reactive } from 'vue'

interface State {
  count: number
  user: {
    name: string
    email: string
  }
  items: string[]
}

// Explicit typing
const state = reactive<State>({
  count: 0,
  user: {
    name: '',
    email: ''
  },
  items: []
})

// Type inference
const inferredState = reactive({
  count: 0, // number
  message: 'hello', // string
  active: true // boolean
})
</script>
```

## Computed Typing

```vue
<script setup lang="ts">
import { ref, computed, ComputedRef } from 'vue'

const count = ref(0)

// Type inference
const doubled = computed(() => count.value * 2) // ComputedRef<number>

// Explicit typing
const tripled = computed<number>(() => count.value * 3)

// Complex computed
interface User {
  firstName: string
  lastName: string
}

const user = ref<User>({ firstName: 'John', lastName: 'Doe' })

const fullName = computed<string>(() => {
  return `${user.value.firstName} ${user.value.lastName}`
})

// Writable computed with typing
const fullNameWritable = computed<string>({
  get() {
    return `${user.value.firstName} ${user.value.lastName}`
  },
  set(value: string) {
    const [first, last] = value.split(' ')
    user.value.firstName = first
    user.value.lastName = last
  }
})
</script>
```

## Template Ref Typing

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

// HTML element refs
const inputRef = ref<HTMLInputElement | null>(null)
const divRef = ref<HTMLDivElement | null>(null)

onMounted(() => {
  inputRef.value?.focus()
  if (divRef.value) {
    divRef.value.scrollTop = 100
  }
})

// Component refs
import ChildComponent from './ChildComponent.vue'

const childRef = ref<InstanceType<typeof ChildComponent> | null>(null)

onMounted(() => {
  childRef.value?.someMethod()
})
</script>

<template>
  <input ref="inputRef" />
  <div ref="divRef">Content</div>
  <ChildComponent ref="childRef" />
</template>
```

## Composables Typing

```typescript
// composables/useCounter.ts
import { ref, computed, Ref, ComputedRef } from 'vue'

interface UseCounterReturn {
  count: Ref<number>
  doubled: ComputedRef<number>
  increment: () => void
  decrement: () => void
  reset: () => void
}

export function useCounter(initialValue = 0): UseCounterReturn {
  const count = ref(initialValue)
  const doubled = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = initialValue
  }

  return {
    count,
    doubled,
    increment,
    decrement,
    reset
  }
}

// composables/useFetch.ts
interface UseFetchOptions<T> {
  immediate?: boolean
  transform?: (data: unknown) => T
}

interface UseFetchReturn<T> {
  data: Ref<T | null>
  error: Ref<Error | null>
  loading: Ref<boolean>
  execute: () => Promise<void>
}

export function useFetch<T = unknown>(
  url: string,
  options: UseFetchOptions<T> = {}
): UseFetchReturn<T> {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  async function execute() {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(url)
      const json = await response.json()
      data.value = options.transform ? options.transform(json) : json
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  if (options.immediate !== false) {
    execute()
  }

  return { data, error, loading, execute }
}

// Usage
<script setup lang="ts">
interface User {
  id: number
  name: string
}

const { data, error, loading } = useFetch<User>('/api/user')
</script>
```

## Generic Components

```vue
<!-- GenericList.vue -->
<script setup lang="ts" generic="T extends { id: number }">
interface Props {
  items: T[]
  selected?: T
}

interface Emits {
  (e: 'select', item: T): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

function handleSelect(item: T) {
  emit('select', item)
}
</script>

<template>
  <div>
    <div
      v-for="item in items"
      :key="item.id"
      @click="handleSelect(item)"
    >
      <slot :item="item"></slot>
    </div>
  </div>
</template>

<!-- Usage -->
<script setup lang="ts">
interface User {
  id: number
  name: string
  email: string
}

const users: User[] = [
  { id: 1, name: 'John', email: 'john@example.com' }
]

function handleUserSelect(user: User) {
  console.log('Selected user:', user.name)
}
</script>

<template>
  <GenericList :items="users" @select="handleUserSelect">
    <template #default="{ item }">
      <div>{{ item.name }} - {{ item.email }}</div>
    </template>
  </GenericList>
</template>
```

## Event Handlers Typing

```vue
<script setup lang="ts">
// DOM events
function handleClick(event: MouseEvent) {
  console.log(event.clientX, event.clientY)
}

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  console.log(target.value)
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Enter') {
    console.log('Enter pressed')
  }
}

// Custom events from child components
interface CustomPayload {
  id: number
  value: string
}

function handleCustomEvent(payload: CustomPayload) {
  console.log(payload.id, payload.value)
}
</script>

<template>
  <button @click="handleClick">Click me</button>
  <input @input="handleInput" @keydown="handleKeydown" />
  <ChildComponent @custom="handleCustomEvent" />
</template>
```

## Provide/Inject Typing

```vue
<!-- Parent.vue -->
<script setup lang="ts">
import { provide, InjectionKey, Ref, ref } from 'vue'

interface UserContext {
  user: Ref<User>
  updateUser: (user: User) => void
}

// Create typed injection key
export const userContextKey = Symbol() as InjectionKey<UserContext>

const user = ref<User>({ id: 1, name: 'John', email: 'john@example.com' })

function updateUser(newUser: User) {
  user.value = newUser
}

// Provide with type safety
provide(userContextKey, {
  user,
  updateUser
})
</script>

<!-- Child.vue -->
<script setup lang="ts">
import { inject } from 'vue'
import { userContextKey } from './Parent.vue'

// Inject with type safety
const userContext = inject(userContextKey)

// With default value
const defaultContext: UserContext = {
  user: ref({ id: 0, name: '', email: '' }),
  updateUser: () => {}
}

const contextWithDefault = inject(userContextKey, defaultContext)

// Or throw if not provided
const requiredContext = inject(userContextKey)
if (!requiredContext) {
  throw new Error('User context not provided')
}
</script>
```

## Store Typing (Pinia)

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface User {
  id: number
  name: string
  email: string
  role: 'admin' | 'user'
}

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const users = ref<User[]>([])

  // Getters
  const isAdmin = computed(() => user.value?.role === 'admin')
  const userCount = computed(() => users.value.length)

  // Actions
  async function fetchUser(id: number): Promise<User> {
    const response = await fetch(`/api/users/${id}`)
    const data = await response.json()
    user.value = data
    return data
  }

  function logout() {
    user.value = null
  }

  return {
    user,
    users,
    isAdmin,
    userCount,
    fetchUser,
    logout
  }
})

// Typed store instance
export type UserStore = ReturnType<typeof useUserStore>
```

## Global Properties Typing

```typescript
// plugins/api.ts
export default defineNuxtPlugin(() => {
  const api = {
    async get<T>(url: string): Promise<T> {
      const response = await fetch(url)
      return response.json()
    },
    async post<T>(url: string, data: unknown): Promise<T> {
      const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data)
      })
      return response.json()
    }
  }

  return {
    provide: {
      api
    }
  }
})

// types/nuxt.d.ts - Augment types
declare module '#app' {
  interface NuxtApp {
    $api: {
      get<T>(url: string): Promise<T>
      post<T>(url: string, data: unknown): Promise<T>
    }
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $api: {
      get<T>(url: string): Promise<T>
      post<T>(url: string, data: unknown): Promise<T>
    }
  }
}

// Usage
<script setup lang="ts">
interface User {
  id: number
  name: string
}

const { $api } = useNuxtApp()
const user = await $api.get<User>('/api/user')
</script>
```

## Quick Reference

| Pattern | Type |
|---------|------|
| `defineProps<T>()` | Interface for props |
| `defineEmits<T>()` | Interface for emits |
| `ref<T>()` | Typed ref |
| `reactive<T>()` | Typed reactive object |
| `computed<T>()` | Typed computed |
| `ref<HTMLElement \| null>` | Template refs |
| `generic="T"` | Generic components |
| `InjectionKey<T>` | Typed provide/inject |
| Type guards | Runtime type checking |
| `as` assertions | Type assertions |
