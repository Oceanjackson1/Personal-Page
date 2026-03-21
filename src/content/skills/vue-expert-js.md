---
title: "Vue Expert JS"
description: "Creates Vue 3 components, builds vanilla JS composables, configures Vite projects, and sets up routing and state management using JavaScript only — no TypeScript. Generates JSDoc-typed code with @typedef, @param, and @returns annotations for full ..."
category: "development"
source: "community"
author: "Community"
tags: ["vue", "js"]
date: 2026-03-20
---

# Vue Expert (JavaScript)

Senior Vue specialist building Vue 3 applications with JavaScript and JSDoc typing instead of TypeScript.

## Core Workflow

1. **Design architecture** — Plan component structure and composables with JSDoc type annotations
2. **Implement** — Build with `<script setup>` (no `lang="ts"`), `.mjs` modules where needed
3. **Annotate** — Add comprehensive JSDoc comments (`@typedef`, `@param`, `@returns`, `@type`) for full type coverage; then run ESLint with the JSDoc plugin (`eslint-plugin-jsdoc`) to verify coverage — fix any missing or malformed annotations before proceeding
4. **Test** — Verify with Vitest using JavaScript files; confirm JSDoc coverage on all public APIs; if tests fail, revisit the relevant composable or component, correct the logic or annotation, and re-run until the suite is green

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| JSDoc Typing | `references/jsdoc-typing.md` | JSDoc types, @typedef, @param, type hints |
| Composables | `references/composables-patterns.md` | custom composables, ref, reactive, lifecycle hooks |
| Components | `references/component-architecture.md` | props, emits, slots, provide/inject |
| State | `references/state-management.md` | Pinia, stores, reactive state |
| Testing | `references/testing-patterns.md` | Vitest, component testing, mocking |

**For shared Vue concepts, defer to vue-expert:**
- `vue-expert/references/composition-api.md` - Core reactivity patterns
- `vue-expert/references/components.md` - Props, emits, slots
- `vue-expert/references/state-management.md` - Pinia stores

## Code Patterns

### Component with JSDoc-typed props and emits

```vue
<script setup>
/**
 * @typedef {Object} UserCardProps
 * @property {string} name - Display name of the user
 * @property {number} age - User's age
 * @property {boolean} [isAdmin=false] - Whether the user has admin rights
 */

/** @type {UserCardProps} */
const props = defineProps({
  name:    { type: String,  required: true },
  age:     { type: Number,  required: true },
  isAdmin: { type: Boolean, default: false },
})

/**
 * @typedef {Object} UserCardEmits
 * @property {(id: string) => void} select - Emitted when the card is selected
 */
const emit = defineEmits(['select'])

/** @param {string} id */
function handleSelect(id) {
  emit('select', id)
}
</script>

<template>
  <div @click="handleSelect(props.name)">
    {{ props.name }} ({{ props.age }})
  </div>
</template>
```

### Composable with @typedef, @param, and @returns

```js
// composables/useCounter.mjs
import { ref, computed } from 'vue'

/**
 * @typedef {Object} CounterState
 * @property {import('vue').Ref<number>} count - Reactive count value
 * @property {import('vue').ComputedRef<boolean>} isPositive - True when count > 0
 * @property {() => void} increment - Increases count by step
 * @property {() => void} reset - Resets count to initial value
 */

/**
 * Composable for a simple counter with configurable step.
 * @param {number} [initial=0] - Starting value
 * @param {number} [step=1]    - Amount to increment per call
 * @returns {CounterState}
 */
export function useCounter(initial = 0, step = 1) {
  /** @type {import('vue').Ref<number>} */
  const count = ref(initial)

  const isPositive = computed(() => count.value > 0)

  function increment() {
    count.value += step
  }

  function reset() {
    count.value = initial
  }

  return { count, isPositive, increment, reset }
}
```

### @typedef for a complex object used across files

```js
// types/user.mjs

/**
 * @typedef {Object} User
 * @property {string}   id       - UUID
 * @property {string}   name     - Full display name
 * @property {string}   email    - Contact email
 * @property {'admin'|'viewer'} role - Access level
 */

// Import in other files with:
// /** @type {import('./types/user.mjs').User} */
```

## Constraints

### MUST DO
- Use Composition API with `<script setup>`
- Use JSDoc comments for type documentation
- Use `.mjs` extension for ES modules when needed
- Annotate every public function with `@param` and `@returns`
- Use `@typedef` for complex object shapes shared across files
- Use `@type` annotations for reactive variables
- Follow vue-expert patterns adapted for JavaScript

### MUST NOT DO
- Use TypeScript syntax (no `<script setup lang="ts">`)
- Use `.ts` file extensions
- Skip JSDoc types for public APIs
- Use CommonJS `require()` in Vue files
- Ignore type safety entirely
- Mix TypeScript files with JavaScript in the same component

## Output Templates

When implementing Vue features in JavaScript:
1. Component file with `<script setup>` (no lang attribute) and JSDoc-typed props/emits
2. `@typedef` definitions for complex prop or state shapes
3. Composable with `@param` and `@returns` annotations
4. Brief note on type coverage

## Knowledge Reference

Vue 3 Composition API, JSDoc, ESM modules, Pinia, Vue Router 4, Vite, VueUse, Vitest, Vue Test Utils, JavaScript ES2022+

---

## Reference: Component Architecture

# Component Architecture

---

## Props

```vue
<script setup>
/**
 * @typedef {Object} Props
 * @property {string} title - Required
 * @property {string} [subtitle] - Optional
 * @property {number} [count=0] - With default
 */

const props = defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  count: { type: Number, default: 0 },
  // Complex types
  items: { type: Array, default: () => [] },
  user: { type: Object, required: true },
  // Validator
  size: {
    type: String,
    default: 'medium',
    validator: (v) => ['small', 'medium', 'large'].includes(v)
  }
})
</script>
```

---

## Emits

```vue
<script setup>
const emit = defineEmits(['update', 'delete', 'close'])

// With validation
const emit = defineEmits({
  /** @param {string} value */
  update: (value) => typeof value === 'string',
  /** @param {{ id: number }} payload */
  delete: (payload) => typeof payload?.id === 'number',
  close: null
})

// Usage
emit('update', 'new value')
emit('delete', { id: 1 })
</script>
```

---

## v-model

```vue
<!-- Single v-model -->
<script setup>
const props = defineProps({ modelValue: { type: String, required: true } })
const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <input :value="modelValue" @input="emit('update:modelValue', $event.target.value)" />
</template>
```

```vue
<!-- Multiple v-models: v-model:firstName, v-model:lastName -->
<script setup>
defineProps({ firstName: String, lastName: String })
defineEmits(['update:firstName', 'update:lastName'])
</script>
```

---

## Slots

```vue
<!-- Card.vue -->
<template>
  <div class="card">
    <header v-if="$slots.header"><slot name="header" /></header>
    <div class="card-body"><slot /></div>
    <footer v-if="$slots.footer"><slot name="footer" /></footer>
  </div>
</template>
```

```vue
<!-- Scoped slot -->
<template>
  <ul>
    <li v-for="(item, index) in items" :key="item.id">
      <slot name="item" :item="item" :index="index">
        {{ item.name }}
      </slot>
    </li>
  </ul>
</template>

<!-- Usage -->
<DataList :items="users">
  <template #item="{ item, index }">
    {{ index + 1 }}. {{ item.name }}
  </template>
</DataList>
```

---

## Provide / Inject

```vue
<!-- Provider.vue -->
<script setup>
import { provide, ref, readonly } from 'vue'

const theme = ref('light')
provide('theme', readonly(theme))
provide('setTheme', (t) => { theme.value = t })
</script>
```

```vue
<!-- Consumer.vue -->
<script setup>
import { inject, ref } from 'vue'

const theme = inject('theme', ref('light'))
const setTheme = inject('setTheme', () => {})
</script>
```

```javascript
// Composable pattern
// composables/useTheme.js
import { ref, provide, inject, readonly, computed } from 'vue'

const ThemeSymbol = Symbol('theme')

export function provideTheme(initial = 'light') {
  const theme = ref(initial)
  const isDark = computed(() => theme.value === 'dark')
  const toggle = () => { theme.value = theme.value === 'light' ? 'dark' : 'light' }

  provide(ThemeSymbol, { theme: readonly(theme), isDark, toggle })
  return { theme, isDark, toggle }
}

export function useTheme() {
  const ctx = inject(ThemeSymbol)
  if (!ctx) throw new Error('useTheme requires ThemeProvider')
  return ctx
}
```

---

## Dynamic Components

```vue
<script setup>
import { shallowRef, markRaw } from 'vue'
import TabHome from './TabHome.vue'
import TabProfile from './TabProfile.vue'

const tabs = [
  { name: 'Home', component: markRaw(TabHome) },
  { name: 'Profile', component: markRaw(TabProfile) }
]

const currentTab = shallowRef(tabs[0].component)
</script>

<template>
  <button v-for="tab in tabs" :key="tab.name" @click="currentTab = tab.component">
    {{ tab.name }}
  </button>
  <KeepAlive>
    <component :is="currentTab" />
  </KeepAlive>
</template>
```

```javascript
// Async component
import { defineAsyncComponent } from 'vue'

const AsyncModal = defineAsyncComponent({
  loader: () => import('./Modal.vue'),
  delay: 200,
  timeout: 10000
})
```

---

## Quick Reference

| Feature | Syntax |
|---------|--------|
| Required prop | `{ type: String, required: true }` |
| Default prop | `{ type: Number, default: 0 }` |
| Array/Object default | `{ type: Array, default: () => [] }` |
| Emit event | `emit('eventName', payload)` |
| v-model | `modelValue` prop + `update:modelValue` emit |
| Named v-model | `v-model:name` → `name` prop + `update:name` emit |
| Default slot | `<slot />` |
| Named slot | `<slot name="header" />` → `#header` |
| Scoped slot | `<slot :item="item" />` → `#default="{ item }"` |
| Provide | `provide('key', value)` |
| Inject | `inject('key', defaultValue)` |
| Dynamic component | `<component :is="comp" />` |

---

## Reference: Composables Patterns

# Composables Patterns

---

## Basic Composable Structure

```javascript
// composables/useToggle.js
import { ref } from 'vue'

/**
 * @typedef {Object} UseToggleReturn
 * @property {import('vue').Ref<boolean>} value
 * @property {() => void} toggle
 */

/**
 * @param {boolean} [initialValue=false]
 * @returns {UseToggleReturn}
 */
export function useToggle(initialValue = false) {
  const value = ref(initialValue)
  const toggle = () => { value.value = !value.value }
  return { value, toggle }
}
```

---

## Ref vs Reactive

```javascript
import { ref, reactive, toRefs, toValue } from 'vue'

// Use ref for: primitives, reassignable values, composable returns
/** @type {import('vue').Ref<number>} */
const count = ref(0)

// Use reactive for: complex objects with nested properties
/** @type {{ email: string, password: string }} */
const form = reactive({ email: '', password: '' })

// Convert reactive to refs for destructuring
const { email, password } = toRefs(form)

// Unwrap ref or return plain value
/** @param {number | import('vue').Ref<number>} maybeRef */
function double(maybeRef) {
  return toValue(maybeRef) * 2
}
```

---

## Lifecycle Hooks

```javascript
// composables/useEventListener.js
import { onMounted, onUnmounted, toValue } from 'vue'

/**
 * @template {keyof WindowEventMap} K
 * @param {K} event
 * @param {(ev: WindowEventMap[K]) => void} handler
 * @param {EventTarget | import('vue').Ref<EventTarget>} [target=window]
 */
export function useEventListener(event, handler, target = window) {
  onMounted(() => toValue(target).addEventListener(event, handler))
  onUnmounted(() => toValue(target).removeEventListener(event, handler))
}
```

```javascript
// Lifecycle-aware async (prevents state updates after unmount)
import { ref, onUnmounted } from 'vue'

export function useAsyncState(fn) {
  const data = ref(null)
  const loading = ref(false)
  let isMounted = true

  onUnmounted(() => { isMounted = false })

  async function execute() {
    loading.value = true
    try {
      const result = await fn()
      if (isMounted) data.value = result
    } finally {
      if (isMounted) loading.value = false
    }
  }

  return { data, loading, execute }
}
```

---

## Shared State (Singleton)

```javascript
// composables/useNotifications.js
import { ref, readonly } from 'vue'

// Module-level state = singleton shared across all components
/** @type {import('vue').Ref<Array<{id: string, message: string}>>} */
const notifications = ref([])

export function useNotifications() {
  /** @param {string} message */
  function notify(message) {
    const id = Date.now().toString()
    notifications.value.push({ id, message })
    setTimeout(() => dismiss(id), 5000)
  }

  /** @param {string} id */
  function dismiss(id) {
    notifications.value = notifications.value.filter(n => n.id !== id)
  }

  return {
    notifications: readonly(notifications),
    notify,
    dismiss
  }
}
```

---

## Async with Cancellation

```javascript
// composables/useCancellableFetch.js
import { ref, onUnmounted } from 'vue'

export function useCancellableFetch() {
  const data = ref(null)
  const error = ref(null)
  const loading = ref(false)
  /** @type {AbortController | null} */
  let controller = null

  /** @param {string} url */
  async function execute(url) {
    controller?.abort()
    controller = new AbortController()
    loading.value = true
    error.value = null

    try {
      const res = await fetch(url, { signal: controller.signal })
      data.value = await res.json()
    } catch (e) {
      if (/** @type {Error} */ (e).name !== 'AbortError') {
        error.value = /** @type {Error} */ (e)
      }
    } finally {
      loading.value = false
    }
  }

  onUnmounted(() => controller?.abort())

  return { data, error, loading, execute }
}
```

---

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `ref()` | Primitives, values passed to/from composables |
| `reactive()` | Objects with nested reactivity |
| `toRefs()` | Destructure reactive while keeping reactivity |
| `toValue()` | Unwrap ref or return plain value |
| Module-level ref | Singleton shared state |
| Factory function | New instance per component |
| `onUnmounted` | Cleanup timers, listeners, abort controllers |

---

## Reference: Jsdoc Typing

# JSDoc Typing for Vue

---

## Basic JSDoc with Vue

### Typing Refs

```vue
<script setup>
import { ref, computed } from 'vue'

/**
 * @typedef {Object} User
 * @property {number} id
 * @property {string} name
 * @property {string} email
 * @property {boolean} [isActive] - Optional property
 */

/** @type {import('vue').Ref<User | null>} */
const user = ref(null)

/** @type {import('vue').Ref<User[]>} */
const users = ref([])

/** @type {import('vue').Ref<string>} */
const searchQuery = ref('')

/** @type {import('vue').Ref<number>} */
const count = ref(0)
</script>
```

### Typing Computed

```vue
<script setup>
import { ref, computed } from 'vue'

/** @type {import('vue').Ref<User | null>} */
const user = ref(null)

/** @type {import('vue').ComputedRef<string>} */
const userName = computed(() => user.value?.name ?? 'Anonymous')

/** @type {import('vue').ComputedRef<boolean>} */
const isLoggedIn = computed(() => user.value !== null)

/** @type {import('vue').ComputedRef<User[]>} */
const activeUsers = computed(() =>
  users.value.filter(u => u.isActive)
)
</script>
```

### Typing Reactive

```vue
<script setup>
import { reactive } from 'vue'

/**
 * @typedef {Object} FormState
 * @property {string} email
 * @property {string} password
 * @property {boolean} rememberMe
 * @property {string[]} errors
 */

/** @type {FormState} */
const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
  errors: []
})
</script>
```

---

## Props with JSDoc

### Basic Props

```vue
<script setup>
/**
 * @typedef {Object} Props
 * @property {string} title - The card title
 * @property {string} [subtitle] - Optional subtitle
 * @property {number} [count=0] - Counter with default value
 * @property {boolean} [disabled=false] - Disabled state
 */

/** @type {Props} */
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  count: {
    type: Number,
    default: 0
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>
```

### Complex Props

```vue
<script setup>
/**
 * @typedef {Object} MenuItem
 * @property {string} id
 * @property {string} label
 * @property {string} [icon]
 * @property {MenuItem[]} [children]
 */

/**
 * @typedef {'primary' | 'secondary' | 'danger'} ButtonVariant
 */

/**
 * @typedef {Object} Props
 * @property {MenuItem[]} items - Menu items
 * @property {ButtonVariant} [variant='primary'] - Button style
 * @property {(item: MenuItem) => void} [onSelect] - Selection callback
 */

const props = defineProps({
  items: {
    type: Array,
    required: true,
    /** @param {MenuItem[]} value */
    validator: (value) => value.every(item => item.id && item.label)
  },
  variant: {
    type: String,
    default: 'primary',
    /** @param {string} value */
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value)
  },
  onSelect: {
    type: Function,
    default: null
  }
})
</script>
```

---

## Emits with JSDoc

### Basic Emits

```vue
<script setup>
/**
 * @typedef {Object} Emits
 * @property {(value: string) => void} update - Emitted on value change
 * @property {(id: number) => void} delete - Emitted on delete
 * @property {() => void} close - Emitted on close
 */

const emit = defineEmits(['update', 'delete', 'close'])

/**
 * Handle input change
 * @param {string} value - The new value
 */
function handleChange(value) {
  emit('update', value)
}

/**
 * Handle delete action
 * @param {number} id - The item ID to delete
 */
function handleDelete(id) {
  emit('delete', id)
}

function handleClose() {
  emit('close')
}
</script>
```

### With Validation

```vue
<script setup>
const emit = defineEmits({
  /**
   * @param {string} value
   * @returns {boolean}
   */
  update: (value) => typeof value === 'string',

  /**
   * @param {{ id: number, reason: string }} payload
   * @returns {boolean}
   */
  delete: (payload) => typeof payload.id === 'number'
})
</script>
```

---

## Composables with JSDoc

### Basic Composable

```javascript
// composables/useCounter.js
import { ref, computed } from 'vue'

/**
 * @typedef {Object} UseCounterReturn
 * @property {import('vue').Ref<number>} count - Current count
 * @property {import('vue').ComputedRef<number>} doubled - Doubled value
 * @property {() => void} increment - Increment count
 * @property {() => void} decrement - Decrement count
 * @property {(value: number) => void} set - Set count to value
 */

/**
 * Counter composable with increment/decrement
 * @param {number} [initialValue=0] - Starting value
 * @returns {UseCounterReturn}
 */
export function useCounter(initialValue = 0) {
  /** @type {import('vue').Ref<number>} */
  const count = ref(initialValue)

  const doubled = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  /**
   * @param {number} value
   */
  function set(value) {
    count.value = value
  }

  return { count, doubled, increment, decrement, set }
}
```

### Async Composable

```javascript
// composables/useFetch.js
import { ref, watchEffect, toValue } from 'vue'

/**
 * @template T
 * @typedef {Object} UseFetchReturn
 * @property {import('vue').Ref<T | null>} data - Fetched data
 * @property {import('vue').Ref<Error | null>} error - Error if any
 * @property {import('vue').Ref<boolean>} loading - Loading state
 * @property {() => Promise<void>} refresh - Refetch data
 */

/**
 * Composable for fetching data
 * @template T
 * @param {string | import('vue').Ref<string>} url - URL to fetch
 * @param {RequestInit} [options] - Fetch options
 * @returns {UseFetchReturn<T>}
 */
export function useFetch(url, options = {}) {
  /** @type {import('vue').Ref<T | null>} */
  const data = ref(null)

  /** @type {import('vue').Ref<Error | null>} */
  const error = ref(null)

  /** @type {import('vue').Ref<boolean>} */
  const loading = ref(false)

  async function refresh() {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(toValue(url), options)
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`)
      }
      data.value = await response.json()
    } catch (e) {
      error.value = /** @type {Error} */ (e)
    } finally {
      loading.value = false
    }
  }

  watchEffect(() => {
    refresh()
  })

  return { data, error, loading, refresh }
}
```

### Composable with Options

```javascript
// composables/useLocalStorage.js
import { ref, watch } from 'vue'

/**
 * @template T
 * @typedef {Object} UseLocalStorageOptions
 * @property {(value: T) => string} [serialize] - Custom serializer
 * @property {(value: string) => T} [deserialize] - Custom deserializer
 */

/**
 * Reactive localStorage composable
 * @template T
 * @param {string} key - Storage key
 * @param {T} defaultValue - Default value if key not found
 * @param {UseLocalStorageOptions<T>} [options] - Options
 * @returns {import('vue').Ref<T>}
 */
export function useLocalStorage(key, defaultValue, options = {}) {
  const serialize = options.serialize ?? JSON.stringify
  const deserialize = options.deserialize ?? JSON.parse

  /** @type {import('vue').Ref<T>} */
  const data = ref(defaultValue)

  // Load from storage
  const stored = localStorage.getItem(key)
  if (stored) {
    try {
      data.value = deserialize(stored)
    } catch {
      data.value = defaultValue
    }
  }

  // Persist on change
  watch(data, (value) => {
    localStorage.setItem(key, serialize(value))
  }, { deep: true })

  return data
}
```

---

## Type Imports and Shared Types

### Shared Type Definitions

```javascript
// types.js - Shared type definitions
/**
 * @typedef {Object} User
 * @property {number} id
 * @property {string} name
 * @property {string} email
 * @property {UserRole} role
 */

/**
 * @typedef {'admin' | 'user' | 'guest'} UserRole
 */

/**
 * @typedef {Object} Post
 * @property {number} id
 * @property {string} title
 * @property {string} content
 * @property {User} author
 * @property {string} createdAt
 */

/**
 * @typedef {Object} PaginatedResponse
 * @template T
 * @property {T[]} data
 * @property {number} total
 * @property {number} page
 * @property {number} pageSize
 */

// Export empty object for IDE import support
export const Types = {}
```

### Importing Types

```vue
<script setup>
/** @typedef {import('./types.js').User} User */
/** @typedef {import('./types.js').Post} Post */

import { ref } from 'vue'

/** @type {import('vue').Ref<User | null>} */
const currentUser = ref(null)

/** @type {import('vue').Ref<Post[]>} */
const posts = ref([])
</script>
```

### Global Type Definitions

```javascript
// types/global.d.js (for IDE support)
/**
 * @typedef {Object} ApiResponse
 * @template T
 * @property {boolean} success
 * @property {T} [data]
 * @property {string} [error]
 */

/**
 * @typedef {Object} ValidationError
 * @property {string} field
 * @property {string} message
 */
```

---

## Pinia Stores with JSDoc

```javascript
// stores/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/** @typedef {import('../types.js').User} User */

/**
 * @typedef {Object} UserStoreState
 * @property {User | null} currentUser
 * @property {boolean} isLoading
 */

export const useUserStore = defineStore('user', () => {
  /** @type {import('vue').Ref<User | null>} */
  const currentUser = ref(null)

  /** @type {import('vue').Ref<boolean>} */
  const isLoading = ref(false)

  const isLoggedIn = computed(() => currentUser.value !== null)
  const userName = computed(() => currentUser.value?.name ?? 'Guest')

  /**
   * Login user
   * @param {string} email
   * @param {string} password
   * @returns {Promise<boolean>}
   */
  async function login(email, password) {
    isLoading.value = true
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })
      const data = await response.json()
      currentUser.value = data.user
      return true
    } catch {
      return false
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    currentUser.value = null
  }

  return {
    currentUser,
    isLoading,
    isLoggedIn,
    userName,
    login,
    logout
  }
})
```

---

## Quick Reference

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| `@typedef` | `@typedef {Object} Name` | Define object shapes |
| `@property` | `@property {type} name` | Object properties |
| `@type` | `@type {Type}` | Annotate variables |
| `@param` | `@param {type} name` | Function parameters |
| `@returns` | `@returns {type}` | Function return type |
| `@template` | `@template T` | Generic types |
| Optional | `{type} [name]` | Optional property |
| Default | `{type} [name=value]` | With default value |
| Union | `{type1 \| type2}` | Multiple types |
| Import | `import('./file').Type` | Import from file |
| Vue Ref | `import('vue').Ref<T>` | Typed ref |
| Vue Computed | `import('vue').ComputedRef<T>` | Typed computed |

---

## Reference: State Management

# State Management

---

## Setup

```javascript
// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

createApp(App).use(createPinia()).mount('#app')
```

---

## Options Store Syntax

```javascript
// stores/counter.js
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Counter'
  }),

  getters: {
    doubleCount: (state) => state.count * 2,
    // Getter with parameter
    countPlusN: (state) => (n) => state.count + n
  },

  actions: {
    increment() {
      this.count++
    },
    /** @param {number} amount */
    incrementBy(amount) {
      this.count += amount
    }
  }
})
```

---

## Setup Store Syntax (Composition API)

```javascript
// stores/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * @typedef {Object} User
 * @property {number} id
 * @property {string} name
 * @property {string} email
 */

export const useUserStore = defineStore('user', () => {
  // State
  /** @type {import('vue').Ref<User | null>} */
  const currentUser = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const isLoggedIn = computed(() => currentUser.value !== null)
  const userName = computed(() => currentUser.value?.name ?? 'Guest')

  // Actions
  async function login(email, password) {
    isLoading.value = true
    error.value = null
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      currentUser.value = (await res.json()).user
      return true
    } catch (e) {
      error.value = e.message
      return false
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    currentUser.value = null
  }

  return { currentUser, isLoading, error, isLoggedIn, userName, login, logout }
})
```

---

## Using Stores

```vue
<script setup>
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()

// Use storeToRefs for reactive state/getters
const { currentUser, isLoggedIn, isLoading } = storeToRefs(userStore)

// Actions can be destructured directly
const { login, logout } = userStore
</script>

<template>
  <div v-if="isLoading">Loading...</div>
  <div v-else-if="isLoggedIn">
    Welcome, {{ currentUser?.name }}
    <button @click="logout">Logout</button>
  </div>
</template>
```

---

## Store Composition

```javascript
// stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useProductsStore } from './products'
import { useUserStore } from './user'

export const useCartStore = defineStore('cart', () => {
  const items = ref([]) // [{ productId, quantity }]

  // Access other stores
  const productsStore = useProductsStore()
  const userStore = useUserStore()

  const total = computed(() =>
    items.value.reduce((sum, item) => {
      const product = productsStore.items.find(p => p.id === item.productId)
      return sum + (product?.price ?? 0) * item.quantity
    }, 0)
  )

  function addItem(productId, quantity = 1) {
    const existing = items.value.find(i => i.productId === productId)
    if (existing) existing.quantity += quantity
    else items.value.push({ productId, quantity })
  }

  async function checkout() {
    if (!userStore.isLoggedIn) throw new Error('Must be logged in')
    await fetch('/api/checkout', {
      method: 'POST',
      body: JSON.stringify({ userId: userStore.currentUser.id, items: items.value })
    })
    items.value = []
  }

  return { items, total, addItem, checkout }
})
```

---

## Persistence

```javascript
// stores/settings.js
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STORAGE_KEY = 'app-settings'

function loadFromStorage() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) ?? {}
  } catch {
    return {}
  }
}

export const useSettingsStore = defineStore('settings', () => {
  const saved = loadFromStorage()

  const theme = ref(saved.theme ?? 'light')
  const language = ref(saved.language ?? 'en')

  watch([theme, language], () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      theme: theme.value,
      language: language.value
    }))
  })

  return { theme, language }
})
```

---

## Testing Stores

```javascript
// stores/__tests__/counter.test.js
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCounterStore } from '../counter'

describe('Counter Store', () => {
  beforeEach(() => setActivePinia(createPinia()))

  it('increments count', () => {
    const store = useCounterStore()
    store.increment()
    expect(store.count).toBe(1)
  })

  it('computes double count', () => {
    const store = useCounterStore()
    store.count = 5
    expect(store.doubleCount).toBe(10)
  })
})
```

---

## Quick Reference

| Feature | Options Syntax | Setup Syntax |
|---------|---------------|--------------|
| State | `state: () => ({})` | `const x = ref()` |
| Getter | `getters: { x: (state) => }` | `const x = computed()` |
| Action | `actions: { fn() {} }` | `function fn() {}` |
| Use in component | `storeToRefs()` for state | Same |
| Reset state | `store.$reset()` | Manual reset function |
| Subscribe | `store.$subscribe((mutation, state) => {})` | Same |
| Other stores | Use in actions | Call at setup top level |

---

## Reference: Testing Patterns

# Testing Patterns

---

## Setup

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.js']
  }
})
```

```javascript
// vitest.setup.js
import { config } from '@vue/test-utils'
import { vi } from 'vitest'

vi.stubGlobal('fetch', vi.fn())

config.global.stubs = {
  'router-link': { template: '<a><slot /></a>' }
}
```

---

## Component Testing Basics

```javascript
// Button.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Button from './Button.vue'

describe('Button', () => {
  it('renders slot content', () => {
    const wrapper = mount(Button, { slots: { default: 'Click me' } })
    expect(wrapper.text()).toBe('Click me')
  })

  it('applies variant class', () => {
    const wrapper = mount(Button, { props: { variant: 'danger' } })
    expect(wrapper.classes()).toContain('btn--danger')
  })

  it('emits click event', async () => {
    const wrapper = mount(Button)
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toHaveLength(1)
  })

  it('is disabled when prop is true', () => {
    const wrapper = mount(Button, { props: { disabled: true } })
    expect(wrapper.attributes('disabled')).toBeDefined()
  })
})
```

---

## Testing v-model

```javascript
// TextInput.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TextInput from './TextInput.vue'

describe('TextInput', () => {
  it('emits update:modelValue on input', async () => {
    const wrapper = mount(TextInput, { props: { modelValue: '' } })
    await wrapper.find('input').setValue('new value')
    expect(wrapper.emitted('update:modelValue')).toEqual([['new value']])
  })
})
```

---

## Testing Async

```javascript
// UserList.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import UserList from './UserList.vue'

describe('UserList', () => {
  beforeEach(() => vi.resetAllMocks())

  it('renders users after fetch', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([{ id: 1, name: 'Alice' }])
    })

    const wrapper = mount(UserList)
    await flushPromises()

    expect(wrapper.text()).toContain('Alice')
  })

  it('shows error on failure', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('Network error'))

    const wrapper = mount(UserList)
    await flushPromises()

    expect(wrapper.find('[data-test="error"]').exists()).toBe(true)
  })
})
```

---

## Mocking Composables

```javascript
// Header.test.js
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref, computed } from 'vue'
import Header from './Header.vue'
import * as useAuthModule from '@/composables/useAuth'

describe('Header', () => {
  it('shows login button when logged out', () => {
    vi.spyOn(useAuthModule, 'useAuth').mockReturnValue({
      user: ref(null),
      isLoggedIn: computed(() => false),
      login: vi.fn(),
      logout: vi.fn()
    })

    const wrapper = mount(Header)
    expect(wrapper.find('[data-test="login-btn"]').exists()).toBe(true)
  })

  it('shows user menu when logged in', () => {
    vi.spyOn(useAuthModule, 'useAuth').mockReturnValue({
      user: ref({ id: 1, name: 'John' }),
      isLoggedIn: computed(() => true),
      login: vi.fn(),
      logout: vi.fn()
    })

    const wrapper = mount(Header)
    expect(wrapper.find('[data-test="user-menu"]').exists()).toBe(true)
  })
})
```

---

## Testing with Pinia

```javascript
// CartSummary.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import CartSummary from './CartSummary.vue'
import { useCartStore } from '@/stores/cart'

describe('CartSummary', () => {
  it('displays cart total', () => {
    const wrapper = mount(CartSummary, {
      global: {
        plugins: [createTestingPinia({
          initialState: {
            cart: { items: [{ productId: 1, quantity: 2, price: 100 }] }
          }
        })]
      }
    })

    expect(wrapper.text()).toContain('$200')
  })

  it('calls checkout action', async () => {
    const wrapper = mount(CartSummary, {
      global: { plugins: [createTestingPinia()] }
    })

    await wrapper.find('[data-test="checkout-btn"]').trigger('click')
    expect(useCartStore().checkout).toHaveBeenCalled()
  })
})
```

---

## Testing Provide/Inject

```javascript
// ChildComponent.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import ChildComponent from './ChildComponent.vue'

describe('ChildComponent', () => {
  it('uses injected theme', () => {
    const wrapper = mount(ChildComponent, {
      global: { provide: { theme: ref('dark') } }
    })
    expect(wrapper.classes()).toContain('theme-dark')
  })
})
```

---

## Quick Reference

| Task | Code |
|------|------|
| Mount | `mount(Component, { props, slots, global })` |
| Find | `wrapper.find('[data-test="x"]')` |
| Trigger | `await wrapper.trigger('click')` |
| Check emitted | `wrapper.emitted('event')` |
| Set input | `await wrapper.find('input').setValue('x')` |
| Wait async | `await flushPromises()` |
| Mock composable | `vi.spyOn(module, 'fn').mockReturnValue()` |
| Mock fetch | `global.fetch = vi.fn().mockResolvedValue()` |
| Test Pinia | `createTestingPinia({ initialState })` |
| Provide | `global: { provide: { key: value } }` |
| Stub component | `global: { stubs: { Comp: true } }` |
