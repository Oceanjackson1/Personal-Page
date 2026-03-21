---
title: "Senior Frontend"
description: "Frontend development skill for React, Next.js, TypeScript, and Tailwind CSS applications. Use when building React components, optimizing Next.js performance, analyzing bundle sizes, scaffolding frontend projects, implementing accessibility, or rev..."
category: "development"
source: "community"
author: "Community"
tags: ["senior", "frontend"]
date: 2026-03-20
---

# Senior Frontend

Frontend development patterns, performance optimization, and automation tools for React/Next.js applications.

## When to Use

- Use when scaffolding a new React or Next.js project with TypeScript and Tailwind CSS.
- Use when generating new components or custom hooks.
- Use when analyzing and optimizing bundle sizes for frontend applications.
- Use to implement or review advanced React patterns like Compound Components or Render Props.
- Use to ensure accessibility compliance and implement robust testing strategies.

## Table of Contents

- [Project Scaffolding](#project-scaffolding)
- [Component Generation](#component-generation)
- [Bundle Analysis](#bundle-analysis)
- [React Patterns](#react-patterns)
- [Next.js Optimization](#nextjs-optimization)
- [Accessibility and Testing](#accessibility-and-testing)

---

## Project Scaffolding

Generate a new Next.js or React project with TypeScript, Tailwind CSS, and best practice configurations.

### Workflow: Create New Frontend Project

1. Run the scaffolder with your project name and template:

   ```bash
   python scripts/frontend_scaffolder.py my-app --template nextjs
   ```

2. Add optional features (auth, api, forms, testing, storybook):

   ```bash
   python scripts/frontend_scaffolder.py dashboard --template nextjs --features auth,api
   ```

3. Navigate to the project and install dependencies:

   ```bash
   cd my-app && npm install
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Scaffolder Options

| Option               | Description                                       |
| -------------------- | ------------------------------------------------- |
| `--template nextjs`  | Next.js 14+ with App Router and Server Components |
| `--template react`   | React + Vite with TypeScript                      |
| `--features auth`    | Add NextAuth.js authentication                    |
| `--features api`     | Add React Query + API client                      |
| `--features forms`   | Add React Hook Form + Zod validation              |
| `--features testing` | Add Vitest + Testing Library                      |
| `--dry-run`          | Preview files without creating them               |

### Generated Structure (Next.js)

```
my-app/
├── app/
│   ├── layout.tsx        # Root layout with fonts
│   ├── page.tsx          # Home page
│   ├── globals.css       # Tailwind + CSS variables
│   └── api/health/route.ts
├── components/
│   ├── ui/               # Button, Input, Card
│   └── layout/           # Header, Footer, Sidebar
├── hooks/                # useDebounce, useLocalStorage
├── lib/                  # utils (cn), constants
├── types/                # TypeScript interfaces
├── tailwind.config.ts
├── next.config.js
└── package.json
```

---

## Component Generation

Generate React components with TypeScript, tests, and Storybook stories.

### Workflow: Create a New Component

1. Generate a client component:

   ```bash
   python scripts/component_generator.py Button --dir src/components/ui
   ```

2. Generate a server component:

   ```bash
   python scripts/component_generator.py ProductCard --type server
   ```

3. Generate with test and story files:

   ```bash
   python scripts/component_generator.py UserProfile --with-test --with-story
   ```

4. Generate a custom hook:
   ```bash
   python scripts/component_generator.py FormValidation --type hook
   ```

### Generator Options

| Option          | Description                                  |
| --------------- | -------------------------------------------- |
| `--type client` | Client component with 'use client' (default) |
| `--type server` | Async server component                       |
| `--type hook`   | Custom React hook                            |
| `--with-test`   | Include test file                            |
| `--with-story`  | Include Storybook story                      |
| `--flat`        | Create in output dir without subdirectory    |
| `--dry-run`     | Preview without creating files               |

### Generated Component Example

```tsx
"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

interface ButtonProps {
  className?: string;
  children?: React.ReactNode;
}

export function Button({ className, children }: ButtonProps) {
  return <div className={cn("", className)}>{children}</div>;
}
```

---

## Bundle Analysis

Analyze package.json and project structure for bundle optimization opportunities.

### Workflow: Optimize Bundle Size

1. Run the analyzer on your project:

   ```bash
   python scripts/bundle_analyzer.py /path/to/project
   ```

2. Review the health score and issues:

   ```
   Bundle Health Score: 75/100 (C)

   HEAVY DEPENDENCIES:
     moment (290KB)
       Alternative: date-fns (12KB) or dayjs (2KB)

     lodash (71KB)
       Alternative: lodash-es with tree-shaking
   ```

3. Apply the recommended fixes by replacing heavy dependencies.

4. Re-run with verbose mode to check import patterns:
   ```bash
   python scripts/bundle_analyzer.py . --verbose
   ```

### Bundle Score Interpretation

| Score  | Grade | Action                         |
| ------ | ----- | ------------------------------ |
| 90-100 | A     | Bundle is well-optimized       |
| 80-89  | B     | Minor optimizations available  |
| 70-79  | C     | Replace heavy dependencies     |
| 60-69  | D     | Multiple issues need attention |
| 0-59   | F     | Critical bundle size problems  |

### Heavy Dependencies Detected

The analyzer identifies these common heavy packages:

| Package       | Size  | Alternative                    |
| ------------- | ----- | ------------------------------ |
| moment        | 290KB | date-fns (12KB) or dayjs (2KB) |
| lodash        | 71KB  | lodash-es with tree-shaking    |
| axios         | 14KB  | Native fetch or ky (3KB)       |
| jquery        | 87KB  | Native DOM APIs                |
| @mui/material | Large | shadcn/ui or Radix UI          |

---

## React Patterns

Reference: `references/react_patterns.md`

### Compound Components

Share state between related components:

```tsx
const Tabs = ({ children }) => {
  const [active, setActive] = useState(0);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabList;
Tabs.Panel = TabPanel;

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab>One</Tabs.Tab>
    <Tabs.Tab>Two</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel>Content 1</Tabs.Panel>
  <Tabs.Panel>Content 2</Tabs.Panel>
</Tabs>;
```

### Custom Hooks

Extract reusable logic:

```tsx
function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 300);
```

### Render Props

Share rendering logic:

```tsx
function DataFetcher({ url, render }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url)
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, [url]);

  return render({ data, loading });
}

// Usage
<DataFetcher
  url="/api/users"
  render={({ data, loading }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
/>;
```

---

## Next.js Optimization

Reference: `references/nextjs_optimization_guide.md`

### Server vs Client Components

Use Server Components by default. Add 'use client' only when you need:

- Event handlers (onClick, onChange)
- State (useState, useReducer)
- Effects (useEffect)
- Browser APIs

```tsx
// Server Component (default) - no 'use client'
async function ProductPage({ params }) {
  const product = await getProduct(params.id); // Server-side fetch

  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} /> {/* Client component */}
    </div>
  );
}

// Client Component
("use client");
function AddToCartButton({ productId }) {
  const [adding, setAdding] = useState(false);
  return <button onClick={() => addToCart(productId)}>Add</button>;
}
```

### Image Optimization

```tsx
import Image from 'next/image';

// Above the fold - load immediately
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
/>

// Responsive image with fill
<div className="relative aspect-video">
  <Image
    src="/product.jpg"
    alt="Product"
    fill
    sizes="(max-width: 768px) 100vw, 50vw"
    className="object-cover"
  />
</div>
```

### Data Fetching Patterns

```tsx
// Parallel fetching
async function Dashboard() {
  const [user, stats] = await Promise.all([getUser(), getStats()]);
  return <div>...</div>;
}

// Streaming with Suspense
async function ProductPage({ params }) {
  return (
    <div>
      <ProductDetails id={params.id} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>
    </div>
  );
}
```

---

## Accessibility and Testing

Reference: `references/frontend_best_practices.md`

### Accessibility Checklist

1. **Semantic HTML**: Use proper elements (`<button>`, `<nav>`, `<main>`)
2. **Keyboard Navigation**: All interactive elements focusable
3. **ARIA Labels**: Provide labels for icons and complex widgets
4. **Color Contrast**: Minimum 4.5:1 for normal text
5. **Focus Indicators**: Visible focus states

```tsx
// Accessible button
<button
  type="button"
  aria-label="Close dialog"
  onClick={onClose}
  className="focus-visible:ring-2 focus-visible:ring-blue-500"
>
  <XIcon aria-hidden="true" />
</button>

// Skip link for keyboard users
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### Testing Strategy

```tsx
// Component test with React Testing Library
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("button triggers action on click", async () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click me</Button>);

  await userEvent.click(screen.getByRole("button"));
  expect(onClick).toHaveBeenCalledTimes(1);
});

// Test accessibility
test("dialog is accessible", async () => {
  render(<Dialog open={true} title="Confirm" />);

  expect(screen.getByRole("dialog")).toBeInTheDocument();
  expect(screen.getByRole("dialog")).toHaveAttribute("aria-labelledby");
});
```

---

## Quick Reference

### Common Next.js Config

```js
// next.config.js
const nextConfig = {
  images: {
    remotePatterns: [{ hostname: "cdn.example.com" }],
    formats: ["image/avif", "image/webp"],
  },
  experimental: {
    optimizePackageImports: ["lucide-react", "@heroicons/react"],
  },
};
```

### Tailwind CSS Utilities

```tsx
// Conditional classes with cn()
import { cn } from "@/lib/utils";

<button
  className={cn(
    "px-4 py-2 rounded",
    variant === "primary" && "bg-blue-500 text-white",
    disabled && "opacity-50 cursor-not-allowed",
  )}
/>;
```

### TypeScript Patterns

```tsx
// Props with children
interface CardProps {
  className?: string;
  children: React.ReactNode;
}

// Generic component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

---

## Resources

- React Patterns: `references/react_patterns.md`
- Next.js Optimization: `references/nextjs_optimization_guide.md`
- Best Practices: `references/frontend_best_practices.md`

---

## Reference: Frontend_Best_Practices

# Frontend Best Practices

Modern frontend development standards for accessibility, testing, TypeScript, and Tailwind CSS.

---

## Table of Contents

- [Accessibility (a11y)](#accessibility-a11y)
- [Testing Strategies](#testing-strategies)
- [TypeScript Patterns](#typescript-patterns)
- [Tailwind CSS](#tailwind-css)
- [Project Structure](#project-structure)
- [Security](#security)

---

## Accessibility (a11y)

### Semantic HTML

```tsx
// BAD - Divs for everything
<div onClick={handleClick}>Click me</div>
<div class="header">...</div>
<div class="nav">...</div>

// GOOD - Semantic elements
<button onClick={handleClick}>Click me</button>
<header>...</header>
<nav>...</nav>
<main>...</main>
<article>...</article>
<aside>...</aside>
<footer>...</footer>
```

### Keyboard Navigation

```tsx
// Ensure all interactive elements are keyboard accessible
function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      // Focus first focusable element
      const focusable = modalRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      (focusable?.[0] as HTMLElement)?.focus();

      // Trap focus within modal
      const handleTab = (e: KeyboardEvent) => {
        if (e.key === 'Tab' && focusable) {
          const first = focusable[0] as HTMLElement;
          const last = focusable[focusable.length - 1] as HTMLElement;

          if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
          } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }

        if (e.key === 'Escape') {
          onClose();
        }
      };

      document.addEventListener('keydown', handleTab);
      return () => document.removeEventListener('keydown', handleTab);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      {children}
    </div>
  );
}
```

### ARIA Attributes

```tsx
// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">
  {status && <p>{status}</p>}
</div>

// Loading states
<button disabled={isLoading} aria-busy={isLoading}>
  {isLoading ? 'Loading...' : 'Submit'}
</button>

// Form labels
<label htmlFor="email">Email address</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : undefined}
/>
{errors.email && (
  <p id="email-error" role="alert">
    {errors.email}
  </p>
)}

// Navigation
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/" aria-current={isHome ? 'page' : undefined}>Home</a></li>
    <li><a href="/about" aria-current={isAbout ? 'page' : undefined}>About</a></li>
  </ul>
</nav>

// Toggle buttons
<button
  aria-pressed={isEnabled}
  onClick={() => setIsEnabled(!isEnabled)}
>
  {isEnabled ? 'Enabled' : 'Disabled'}
</button>

// Expandable sections
<button
  aria-expanded={isOpen}
  aria-controls="content-panel"
  onClick={() => setIsOpen(!isOpen)}
>
  Show details
</button>
<div id="content-panel" hidden={!isOpen}>
  Content here
</div>
```

### Color Contrast

```tsx
// Ensure 4.5:1 contrast ratio for text (WCAG AA)
// Use tools like @axe-core/react for testing

// tailwind.config.js - Define accessible colors
module.exports = {
  theme: {
    colors: {
      // Primary with proper contrast
      primary: {
        DEFAULT: '#2563eb', // Blue 600
        foreground: '#ffffff',
      },
      // Error state
      error: {
        DEFAULT: '#dc2626', // Red 600
        foreground: '#ffffff',
      },
      // Text colors with proper contrast
      foreground: '#0f172a', // Slate 900
      muted: '#64748b', // Slate 500 - minimum 4.5:1 on white
    },
  },
};

// Never rely on color alone
<span className="text-red-600">
  <ErrorIcon aria-hidden="true" />
  <span>Error: Invalid input</span>
</span>
```

### Screen Reader Only Content

```tsx
// Visually hidden but accessible to screen readers
const srOnly = 'absolute w-px h-px p-0 -m-px overflow-hidden whitespace-nowrap border-0';

// Skip link for keyboard users
<a href="#main-content" className={srOnly + ' focus:not-sr-only focus:absolute focus:top-0'}>
  Skip to main content
</a>

// Icon buttons need labels
<button aria-label="Close menu">
  <XIcon aria-hidden="true" />
</button>

// Or use visually hidden text
<button>
  <XIcon aria-hidden="true" />
  <span className={srOnly}>Close menu</span>
</button>
```

---

## Testing Strategies

### Component Testing with Testing Library

```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = jest.fn();

    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
  });

  it('shows loading text when loading', () => {
    render(<Button isLoading loadingText="Submitting...">Submit</Button>);
    expect(screen.getByText('Submitting...')).toBeInTheDocument();
  });
});
```

### Hook Testing

```tsx
// useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.count).toBe(5);
  });
});
```

### Integration Testing

```tsx
// LoginForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';
import { AuthProvider } from '@/contexts/AuthContext';

const mockLogin = jest.fn();

jest.mock('@/lib/auth', () => ({
  login: (...args: unknown[]) => mockLogin(...args),
}));

describe('LoginForm', () => {
  beforeEach(() => {
    mockLogin.mockReset();
  });

  it('submits form with valid credentials', async () => {
    const user = userEvent.setup();
    mockLogin.mockResolvedValueOnce({ user: { id: '1', name: 'Test' } });

    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });

  it('shows validation errors for empty fields', async () => {
    const user = userEvent.setup();

    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );

    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/password is required/i)).toBeInTheDocument();
    expect(mockLogin).not.toHaveBeenCalled();
  });
});
```

### E2E Testing with Playwright

```typescript
// e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Checkout flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="product-1"] button');
    await page.click('[data-testid="cart-button"]');
  });

  test('completes checkout with valid payment', async ({ page }) => {
    await page.click('text=Proceed to Checkout');

    // Fill shipping info
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="address"]', '123 Test St');
    await page.fill('[name="city"]', 'Test City');
    await page.selectOption('[name="state"]', 'CA');
    await page.fill('[name="zip"]', '90210');

    await page.click('text=Continue to Payment');
    await page.click('text=Place Order');

    // Verify success
    await expect(page).toHaveURL(/\/order\/confirmation/);
    await expect(page.locator('h1')).toHaveText('Order Confirmed!');
  });
});
```

---

## TypeScript Patterns

### Component Props

```tsx
// Use interface for component props
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

// Extend HTML attributes
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  isLoading?: boolean;
}

function Button({ variant = 'primary', isLoading, children, ...props }: ButtonProps) {
  return (
    <button
      {...props}
      disabled={props.disabled || isLoading}
      className={cn(variants[variant], props.className)}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
}

// Polymorphic components
type PolymorphicProps<E extends React.ElementType> = {
  as?: E;
} & React.ComponentPropsWithoutRef<E>;

function Box<E extends React.ElementType = 'div'>({
  as,
  children,
  ...props
}: PolymorphicProps<E>) {
  const Component = as || 'div';
  return <Component {...props}>{children}</Component>;
}

// Usage
<Box as="section" id="hero">Content</Box>
<Box as="article">Article content</Box>
```

### Discriminated Unions

```tsx
// State machines with exhaustive type checking
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function DataDisplay<T>({ state, render }: {
  state: AsyncState<T>;
  render: (data: T) => React.ReactNode;
}) {
  switch (state.status) {
    case 'idle':
      return null;
    case 'loading':
      return <Spinner />;
    case 'success':
      return <>{render(state.data)}</>;
    case 'error':
      return <ErrorMessage error={state.error} />;
    // TypeScript ensures all cases are handled
  }
}
```

### Generic Components

```tsx
// Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

function List<T>({ items, renderItem, keyExtractor, emptyMessage }: ListProps<T>) {
  if (items.length === 0) {
    return <p className="text-muted">{emptyMessage || 'No items'}</p>;
  }

  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  keyExtractor={(user) => user.id}
  renderItem={(user) => <UserCard user={user} />}
/>
```

### Type Guards

```tsx
// User-defined type guards
interface User {
  id: string;
  name: string;
  email: string;
}

interface Admin extends User {
  role: 'admin';
  permissions: string[];
}

function isAdmin(user: User): user is Admin {
  return 'role' in user && user.role === 'admin';
}

function UserBadge({ user }: { user: User }) {
  if (isAdmin(user)) {
    // TypeScript knows user is Admin here
    return <Badge variant="admin">Admin ({user.permissions.length} perms)</Badge>;
  }

  return <Badge>User</Badge>;
}

// API response type guards
interface ApiSuccess<T> {
  success: true;
  data: T;
}

interface ApiError {
  success: false;
  error: string;
}

type ApiResponse<T> = ApiSuccess<T> | ApiError;

function isApiSuccess<T>(response: ApiResponse<T>): response is ApiSuccess<T> {
  return response.success === true;
}
```

---

## Tailwind CSS

### Component Variants with CVA

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500',
        ghost: 'hover:bg-gray-100 hover:text-gray-900',
        destructive: 'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-sm',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  );
}

// Usage
<Button variant="primary" size="lg">Large Primary</Button>
<Button variant="ghost" size="icon"><MenuIcon /></Button>
```

### Responsive Design

```tsx
// Mobile-first responsive design
<div className="
  grid
  grid-cols-1          {/* Mobile: 1 column */}
  sm:grid-cols-2       {/* 640px+: 2 columns */}
  lg:grid-cols-3       {/* 1024px+: 3 columns */}
  xl:grid-cols-4       {/* 1280px+: 4 columns */}
  gap-4
  sm:gap-6
  lg:gap-8
">
  {products.map(product => <ProductCard key={product.id} product={product} />)}
</div>

// Container with responsive padding
<div className="container mx-auto px-4 sm:px-6 lg:px-8">
  Content
</div>

// Hide/show based on breakpoint
<nav className="hidden md:flex">Desktop nav</nav>
<button className="md:hidden">Mobile menu</button>
```

### Animation Utilities

```tsx
// Skeleton loading
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-gray-200 rounded w-3/4" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
</div>

// Transitions
<button className="
  transition-all
  duration-200
  ease-in-out
  hover:scale-105
  active:scale-95
">
  Hover me
</button>

// Custom animations in tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
};

// Usage
<div className="animate-fade-in">Fading in</div>
```

---

## Project Structure

### Feature-Based Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/             # Auth route group
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   │   ├── page.tsx
│   │   └── layout.tsx
│   └── layout.tsx
├── components/
│   ├── ui/                 # Shared UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── index.ts
│   └── features/           # Feature-specific components
│       ├── auth/
│       │   ├── LoginForm.tsx
│       │   └── RegisterForm.tsx
│       └── dashboard/
│           ├── StatsCard.tsx
│           └── RecentActivity.tsx
├── hooks/                  # Custom React hooks
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   └── useLocalStorage.ts
├── lib/                    # Utilities and configs
│   ├── utils.ts
│   ├── api.ts
│   └── constants.ts
├── types/                  # TypeScript types
│   ├── user.ts
│   └── api.ts
└── styles/
    └── globals.css
```

### Barrel Exports

```tsx
// components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Card, CardHeader, CardContent, CardFooter } from './Card';
export { Dialog, DialogTrigger, DialogContent } from './Dialog';

// Usage
import { Button, Input, Card } from '@/components/ui';
```

---

## Security

### XSS Prevention

React escapes content by default, which prevents most XSS attacks. When you need to render HTML content:

1. **Avoid rendering raw HTML** when possible
2. **Sanitize with DOMPurify** for trusted content sources
3. **Use allow-lists** for permitted tags and attributes

```tsx
// React escapes by default - this is safe
<div>{userInput}</div>

// When you must render HTML, sanitize first
import DOMPurify from 'dompurify';

function SafeHTML({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href'],
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

### Input Validation

```tsx
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type FormData = z.infer<typeof schema>;

function RegisterForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input {...register('email')} error={errors.email?.message} />
      <Input type="password" {...register('password')} error={errors.password?.message} />
      <Input type="password" {...register('confirmPassword')} error={errors.confirmPassword?.message} />
      <Button type="submit">Register</Button>
    </form>
  );
}
```

### Secure API Calls

```tsx
// Use environment variables for API endpoints
const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Never include secrets in client code - use server-side API routes
// app/api/data/route.ts
export async function GET() {
  const response = await fetch('https://api.example.com/data', {
    headers: {
      'Authorization': `Bearer ${process.env.API_SECRET}`, // Server-side only
    },
  });

  return Response.json(await response.json());
}
```

---

## Reference: Nextjs_Optimization_Guide

# Next.js Optimization Guide

Performance optimization techniques for Next.js 14+ applications.

---

## Table of Contents

- [Rendering Strategies](#rendering-strategies)
- [Image Optimization](#image-optimization)
- [Code Splitting](#code-splitting)
- [Data Fetching](#data-fetching)
- [Caching Strategies](#caching-strategies)
- [Bundle Optimization](#bundle-optimization)
- [Core Web Vitals](#core-web-vitals)

---

## Rendering Strategies

### Server Components (Default)

Server Components render on the server and send HTML to the client. Use for data-heavy, non-interactive content.

```tsx
// app/products/page.tsx - Server Component (default)
async function ProductsPage() {
  // This runs on the server - no client bundle impact
  const products = await db.products.findMany();

  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

### Client Components

Use `'use client'` only when you need:
- Event handlers (onClick, onChange)
- State (useState, useReducer)
- Effects (useEffect)
- Browser APIs (window, document)

```tsx
'use client';

import { useState } from 'react';

function AddToCartButton({ productId }: { productId: string }) {
  const [isAdding, setIsAdding] = useState(false);

  async function handleClick() {
    setIsAdding(true);
    await addToCart(productId);
    setIsAdding(false);
  }

  return (
    <button onClick={handleClick} disabled={isAdding}>
      {isAdding ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}
```

### Mixing Server and Client Components

```tsx
// app/products/[id]/page.tsx - Server Component
async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);

  return (
    <div>
      {/* Server-rendered content */}
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      {/* Client component for interactivity */}
      <AddToCartButton productId={product.id} />

      {/* Server component for reviews */}
      <ProductReviews productId={product.id} />
    </div>
  );
}
```

### Static vs Dynamic Rendering

```tsx
// Force static generation at build time
export const dynamic = 'force-static';

// Force dynamic rendering at request time
export const dynamic = 'force-dynamic';

// Revalidate every 60 seconds (ISR)
export const revalidate = 60;

// Revalidate on-demand
import { revalidatePath, revalidateTag } from 'next/cache';

async function updateProduct(id: string, data: ProductData) {
  await db.products.update({ where: { id }, data });

  // Revalidate specific path
  revalidatePath(`/products/${id}`);

  // Or revalidate by tag
  revalidateTag('products');
}
```

---

## Image Optimization

### Next.js Image Component

```tsx
import Image from 'next/image';

// Basic optimized image
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // Load immediately for LCP
/>

// Responsive image
<Image
  src="/product.jpg"
  alt="Product"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="object-cover"
/>

// With placeholder blur
import productImage from '@/public/product.jpg';

<Image
  src={productImage}
  alt="Product"
  placeholder="blur" // Uses imported image data
/>
```

### Remote Images Configuration

```js
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        pathname: '/images/**',
      },
      {
        protocol: 'https',
        hostname: '*.cloudinary.com',
      },
    ],
    // Image formats (webp is default)
    formats: ['image/avif', 'image/webp'],
    // Device sizes for srcset
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    // Image sizes for srcset
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
};
```

### Lazy Loading Patterns

```tsx
// Images below the fold - lazy load (default)
<Image
  src="/gallery/photo1.jpg"
  alt="Gallery photo"
  width={400}
  height={300}
  loading="lazy" // Default behavior
/>

// Above the fold - load immediately
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
  loading="eager"
/>
```

---

## Code Splitting

### Dynamic Imports

```tsx
import dynamic from 'next/dynamic';

// Basic dynamic import
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartSkeleton />,
});

// Disable SSR for client-only components
const MapComponent = dynamic(() => import('@/components/Map'), {
  ssr: false,
  loading: () => <div className="h-[400px] bg-gray-100" />,
});

// Named exports
const Modal = dynamic(() =>
  import('@/components/ui').then(mod => mod.Modal)
);

// With suspense
const DashboardCharts = dynamic(() => import('@/components/DashboardCharts'), {
  loading: () => <Suspense fallback={<ChartsSkeleton />} />,
});
```

### Route-Based Splitting

```tsx
// app/dashboard/analytics/page.tsx
// This page only loads when /dashboard/analytics is visited
import { Suspense } from 'react';
import AnalyticsCharts from './AnalyticsCharts';

export default function AnalyticsPage() {
  return (
    <Suspense fallback={<AnalyticsSkeleton />}>
      <AnalyticsCharts />
    </Suspense>
  );
}
```

### Parallel Routes for Code Splitting

```
app/
├── dashboard/
│   ├── @analytics/
│   │   └── page.tsx    # Loaded in parallel
│   ├── @metrics/
│   │   └── page.tsx    # Loaded in parallel
│   ├── layout.tsx
│   └── page.tsx
```

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  metrics,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  metrics: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-2 gap-4">
      {children}
      <Suspense fallback={<AnalyticsSkeleton />}>{analytics}</Suspense>
      <Suspense fallback={<MetricsSkeleton />}>{metrics}</Suspense>
    </div>
  );
}
```

---

## Data Fetching

### Server-Side Data Fetching

```tsx
// Parallel data fetching
async function Dashboard() {
  // Start both requests simultaneously
  const [user, stats, notifications] = await Promise.all([
    getUser(),
    getStats(),
    getNotifications(),
  ]);

  return (
    <div>
      <UserHeader user={user} />
      <StatsPanel stats={stats} />
      <NotificationList notifications={notifications} />
    </div>
  );
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react';

async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);

  return (
    <div>
      {/* Immediate content */}
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      {/* Stream reviews - don't block page */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>

      {/* Stream recommendations */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations productId={params.id} />
      </Suspense>
    </div>
  );
}

// Slow data component
async function Reviews({ productId }: { productId: string }) {
  const reviews = await getReviews(productId); // Slow query
  return <ReviewList reviews={reviews} />;
}
```

### Request Memoization

```tsx
// Next.js automatically dedupes identical requests
async function Layout({ children }) {
  const user = await getUser(); // Request 1
  return <div>{children}</div>;
}

async function Header() {
  const user = await getUser(); // Same request - cached!
  return <div>Hello, {user.name}</div>;
}

// Both components call getUser() but only one request is made
```

---

## Caching Strategies

### Fetch Cache Options

```tsx
// Cache indefinitely (default for static)
fetch('https://api.example.com/data');

// No cache - always fresh
fetch('https://api.example.com/data', { cache: 'no-store' });

// Revalidate after time
fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // 1 hour
});

// Tag-based revalidation
fetch('https://api.example.com/products', {
  next: { tags: ['products'] }
});

// Later, revalidate by tag
import { revalidateTag } from 'next/cache';
revalidateTag('products');
```

### Route Segment Config

```tsx
// app/products/page.tsx

// Revalidate every hour
export const revalidate = 3600;

// Or force dynamic
export const dynamic = 'force-dynamic';

// Generate static params at build
export async function generateStaticParams() {
  const products = await getProducts();
  return products.map(p => ({ id: p.id }));
}
```

### unstable_cache for Custom Caching

```tsx
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (userId: string) => {
    const user = await db.users.findUnique({ where: { id: userId } });
    return user;
  },
  ['user-cache'],
  {
    revalidate: 3600, // 1 hour
    tags: ['users'],
  }
);

// Usage
const user = await getCachedUser(userId);
```

---

## Bundle Optimization

### Analyze Bundle Size

```bash
# Install analyzer
npm install @next/bundle-analyzer

# Update next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // config
});

# Run analysis
ANALYZE=true npm run build
```

### Tree Shaking Imports

```tsx
// BAD - Imports entire library
import _ from 'lodash';
const result = _.debounce(fn, 300);

// GOOD - Import only what you need
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// GOOD - Named imports (tree-shakeable)
import { debounce } from 'lodash-es';
```

### Optimize Dependencies

```js
// next.config.js
module.exports = {
  // Transpile specific packages
  transpilePackages: ['ui-library', 'shared-utils'],

  // Optimize package imports
  experimental: {
    optimizePackageImports: ['lucide-react', '@heroicons/react'],
  },

  // External packages for server
  serverExternalPackages: ['sharp', 'bcrypt'],
};
```

### Font Optimization

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```

---

## Core Web Vitals

### Largest Contentful Paint (LCP)

```tsx
// Optimize LCP hero image
import Image from 'next/image';

export default function Hero() {
  return (
    <section className="relative h-[600px]">
      <Image
        src="/hero.jpg"
        alt="Hero"
        fill
        priority // Preload for LCP
        sizes="100vw"
        className="object-cover"
      />
      <div className="relative z-10">
        <h1>Welcome</h1>
      </div>
    </section>
  );
}

// Preload critical resources in layout
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <link rel="preload" href="/hero.jpg" as="image" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Cumulative Layout Shift (CLS)

```tsx
// Prevent CLS with explicit dimensions
<Image
  src="/product.jpg"
  alt="Product"
  width={400}
  height={300}
/>

// Or use aspect ratio
<div className="aspect-video relative">
  <Image src="/video-thumb.jpg" alt="Video" fill />
</div>

// Skeleton placeholders
function ProductCard({ product }: { product?: Product }) {
  if (!product) {
    return (
      <div className="animate-pulse">
        <div className="h-48 bg-gray-200 rounded" />
        <div className="h-4 bg-gray-200 rounded mt-2 w-3/4" />
        <div className="h-4 bg-gray-200 rounded mt-1 w-1/2" />
      </div>
    );
  }

  return (
    <div>
      <Image src={product.image} alt={product.name} width={300} height={200} />
      <h3>{product.name}</h3>
      <p>{product.price}</p>
    </div>
  );
}
```

### First Input Delay (FID) / Interaction to Next Paint (INP)

```tsx
// Defer non-critical JavaScript
import Script from 'next/script';

export default function Layout({ children }) {
  return (
    <html>
      <body>
        {children}

        {/* Load analytics after page is interactive */}
        <Script
          src="https://analytics.example.com/script.js"
          strategy="afterInteractive"
        />

        {/* Load chat widget when idle */}
        <Script
          src="https://chat.example.com/widget.js"
          strategy="lazyOnload"
        />
      </body>
    </html>
  );
}

// Use web workers for heavy computation
// app/components/DataProcessor.tsx
'use client';

import { useEffect, useState } from 'react';

function DataProcessor({ data }: { data: number[] }) {
  const [result, setResult] = useState<number | null>(null);

  useEffect(() => {
    const worker = new Worker(new URL('../workers/processor.js', import.meta.url));

    worker.postMessage(data);
    worker.onmessage = (e) => setResult(e.data);

    return () => worker.terminate();
  }, [data]);

  return <div>Result: {result}</div>;
}
```

### Measuring Performance

```tsx
// app/components/PerformanceMonitor.tsx
'use client';

import { useReportWebVitals } from 'next/web-vitals';

export function PerformanceMonitor() {
  useReportWebVitals((metric) => {
    switch (metric.name) {
      case 'LCP':
        console.log('LCP:', metric.value);
        break;
      case 'FID':
        console.log('FID:', metric.value);
        break;
      case 'CLS':
        console.log('CLS:', metric.value);
        break;
      case 'TTFB':
        console.log('TTFB:', metric.value);
        break;
    }

    // Send to analytics
    analytics.track('web-vital', {
      name: metric.name,
      value: metric.value,
      id: metric.id,
    });
  });

  return null;
}
```

---

## Quick Reference

### Performance Checklist

| Area | Optimization | Impact |
|------|-------------|--------|
| Images | Use next/image with priority for LCP | High |
| Fonts | Use next/font with display: swap | Medium |
| Code | Dynamic imports for heavy components | High |
| Data | Parallel fetching with Promise.all | High |
| Render | Server Components by default | High |
| Cache | Configure revalidate appropriately | Medium |
| Bundle | Tree-shake imports, analyze size | Medium |

### Config Template

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [{ hostname: 'cdn.example.com' }],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  headers: async () => [
    {
      source: '/(.*)',
      headers: [
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'X-Frame-Options', value: 'DENY' },
      ],
    },
  ],
};

module.exports = nextConfig;
```

---

## Reference: React_Patterns

# React Patterns

Production-ready patterns for building scalable React applications with TypeScript.

---

## Table of Contents

- [Component Composition](#component-composition)
- [Custom Hooks](#custom-hooks)
- [State Management](#state-management)
- [Performance Patterns](#performance-patterns)
- [Error Boundaries](#error-boundaries)
- [Anti-Patterns](#anti-patterns)

---

## Component Composition

### Compound Components

Use compound components when building reusable UI components with multiple related parts.

```tsx
// Compound component pattern for a Select
interface SelectContextType {
  value: string;
  onChange: (value: string) => void;
}

const SelectContext = createContext<SelectContextType | null>(null);

function Select({ children, value, onChange }: {
  children: React.ReactNode;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <SelectContext.Provider value={{ value, onChange }}>
      <div className="relative">{children}</div>
    </SelectContext.Provider>
  );
}

function SelectTrigger({ children }: { children: React.ReactNode }) {
  const context = useContext(SelectContext);
  if (!context) throw new Error('SelectTrigger must be used within Select');

  return (
    <button className="flex items-center gap-2 px-4 py-2 border rounded">
      {children}
    </button>
  );
}

function SelectOption({ value, children }: { value: string; children: React.ReactNode }) {
  const context = useContext(SelectContext);
  if (!context) throw new Error('SelectOption must be used within Select');

  return (
    <div
      onClick={() => context.onChange(value)}
      className={`px-4 py-2 cursor-pointer hover:bg-gray-100 ${
        context.value === value ? 'bg-blue-50' : ''
      }`}
    >
      {children}
    </div>
  );
}

// Attach sub-components
Select.Trigger = SelectTrigger;
Select.Option = SelectOption;

// Usage
<Select value={selected} onChange={setSelected}>
  <Select.Trigger>Choose option</Select.Trigger>
  <Select.Option value="a">Option A</Select.Option>
  <Select.Option value="b">Option B</Select.Option>
</Select>
```

### Render Props

Use render props when you need to share behavior with flexible rendering.

```tsx
interface MousePosition {
  x: number;
  y: number;
}

function MouseTracker({ render }: { render: (pos: MousePosition) => React.ReactNode }) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{render(position)}</>;
}

// Usage
<MouseTracker
  render={({ x, y }) => (
    <div>Mouse position: {x}, {y}</div>
  )}
/>
```

### Higher-Order Components (HOC)

Use HOCs for cross-cutting concerns like authentication or logging.

```tsx
function withAuth<P extends object>(WrappedComponent: React.ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const { user, isLoading } = useAuth();

    if (isLoading) return <LoadingSpinner />;
    if (!user) return <Navigate to="/login" />;

    return <WrappedComponent {...props} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

---

## Custom Hooks

### useAsync - Handle async operations

```tsx
interface AsyncState<T> {
  data: T | null;
  error: Error | null;
  status: 'idle' | 'loading' | 'success' | 'error';
}

function useAsync<T>(asyncFn: () => Promise<T>, deps: any[] = []) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    error: null,
    status: 'idle',
  });

  const execute = useCallback(async () => {
    setState({ data: null, error: null, status: 'loading' });
    try {
      const data = await asyncFn();
      setState({ data, error: null, status: 'success' });
    } catch (error) {
      setState({ data: null, error: error as Error, status: 'error' });
    }
  }, deps);

  useEffect(() => {
    execute();
  }, [execute]);

  return { ...state, refetch: execute };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, status, error, refetch } = useAsync(
    () => fetchUser(userId),
    [userId]
  );

  if (status === 'loading') return <Spinner />;
  if (status === 'error') return <Error message={error?.message} />;
  if (!user) return null;

  return <Profile user={user} />;
}
```

### useDebounce - Debounce values

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchInput() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery);
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

### useLocalStorage - Persist state

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue;
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      }
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}

// Usage
const [theme, setTheme] = useLocalStorage('theme', 'light');
```

### useMediaQuery - Responsive design

```tsx
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [query]);

  return matches;
}

// Usage
function ResponsiveNav() {
  const isMobile = useMediaQuery('(max-width: 768px)');
  return isMobile ? <MobileNav /> : <DesktopNav />;
}
```

### usePrevious - Track previous values

```tsx
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Usage
function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      Current: {count}, Previous: {prevCount}
    </div>
  );
}
```

---

## State Management

### Context with Reducer

For complex state that multiple components need to access.

```tsx
// types.ts
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  total: number;
}

type CartAction =
  | { type: 'ADD_ITEM'; payload: CartItem }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'CLEAR_CART' };

// reducer.ts
function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existingItem = state.items.find(i => i.id === action.payload.id);
      if (existingItem) {
        return {
          ...state,
          items: state.items.map(item =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          ),
        };
      }
      return {
        ...state,
        items: [...state.items, { ...action.payload, quantity: 1 }],
      };
    }
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload),
      };
    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ),
      };
    case 'CLEAR_CART':
      return { items: [], total: 0 };
    default:
      return state;
  }
}

// context.tsx
const CartContext = createContext<{
  state: CartState;
  dispatch: React.Dispatch<CartAction>;
} | null>(null);

function CartProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [], total: 0 });

  // Compute total whenever items change
  const stateWithTotal = useMemo(() => ({
    ...state,
    total: state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
  }), [state.items]);

  return (
    <CartContext.Provider value={{ state: stateWithTotal, dispatch }}>
      {children}
    </CartContext.Provider>
  );
}

function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
}
```

### Zustand (Lightweight Alternative)

```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthStore {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: async (email, password) => {
        const { user, token } = await authAPI.login(email, password);
        set({ user, token });
      },
      logout: () => set({ user: null, token: null }),
    }),
    { name: 'auth-storage' }
  )
);

// Usage
function Profile() {
  const { user, logout } = useAuthStore();
  return user ? <div>{user.name} <button onClick={logout}>Logout</button></div> : null;
}
```

---

## Performance Patterns

### React.memo with Custom Comparison

```tsx
interface ListItemProps {
  item: { id: string; name: string; count: number };
  onSelect: (id: string) => void;
}

const ListItem = React.memo(
  function ListItem({ item, onSelect }: ListItemProps) {
    return (
      <div onClick={() => onSelect(item.id)}>
        {item.name} ({item.count})
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Only re-render if item data changed
    return (
      prevProps.item.id === nextProps.item.id &&
      prevProps.item.name === nextProps.item.name &&
      prevProps.item.count === nextProps.item.count
    );
  }
);
```

### useMemo for Expensive Calculations

```tsx
function DataTable({ data, sortColumn, filterText }: {
  data: Item[];
  sortColumn: string;
  filterText: string;
}) {
  const processedData = useMemo(() => {
    // Filter
    let result = data.filter(item =>
      item.name.toLowerCase().includes(filterText.toLowerCase())
    );

    // Sort
    result = [...result].sort((a, b) => {
      const aVal = a[sortColumn as keyof Item];
      const bVal = b[sortColumn as keyof Item];
      return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
    });

    return result;
  }, [data, sortColumn, filterText]);

  return (
    <table>
      {processedData.map(item => (
        <tr key={item.id}>{/* ... */}</tr>
      ))}
    </table>
  );
}
```

### useCallback for Stable References

```tsx
function ParentComponent() {
  const [items, setItems] = useState<Item[]>([]);

  // Stable reference - won't cause child re-renders
  const handleItemClick = useCallback((id: string) => {
    setItems(prev => prev.map(item =>
      item.id === id ? { ...item, selected: !item.selected } : item
    ));
  }, []);

  const handleAddItem = useCallback((newItem: Item) => {
    setItems(prev => [...prev, newItem]);
  }, []);

  return (
    <>
      <ItemList items={items} onItemClick={handleItemClick} />
      <AddItemForm onAdd={handleAddItem} />
    </>
  );
}
```

### Virtualization for Long Lists

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // estimated row height
    overscan: 5,
  });

  return (
    <div ref={parentRef} className="h-[400px] overflow-auto">
      <div
        style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Error Boundaries

### Class-Based Error Boundary

```tsx
interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    this.props.onError?.(error, errorInfo);
    // Log to error reporting service
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-4 bg-red-50 border border-red-200 rounded">
          <h2 className="text-red-800 font-bold">Something went wrong</h2>
          <p className="text-red-600">{this.state.error?.message}</p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded"
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary
  fallback={<ErrorFallback />}
  onError={(error) => trackError(error)}
>
  <MyComponent />
</ErrorBoundary>
```

### Suspense with Error Boundary

```tsx
function DataComponent() {
  return (
    <ErrorBoundary fallback={<ErrorMessage />}>
      <Suspense fallback={<LoadingSpinner />}>
        <AsyncDataLoader />
      </Suspense>
    </ErrorBoundary>
  );
}
```

---

## Anti-Patterns

### Avoid: Inline Object/Array Creation in JSX

```tsx
// BAD - Creates new object every render, causes re-renders
<Component style={{ color: 'red' }} items={[1, 2, 3]} />

// GOOD - Define outside or use useMemo
const style = { color: 'red' };
const items = [1, 2, 3];
<Component style={style} items={items} />

// Or with useMemo for dynamic values
const style = useMemo(() => ({ color: theme.primary }), [theme.primary]);
```

### Avoid: Index as Key for Dynamic Lists

```tsx
// BAD - Index keys break with reordering/filtering
{items.map((item, index) => (
  <Item key={index} data={item} />
))}

// GOOD - Use stable unique ID
{items.map(item => (
  <Item key={item.id} data={item} />
))}
```

### Avoid: Prop Drilling

```tsx
// BAD - Passing props through many levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserInfo user={user} />
    </Sidebar>
  </Layout>
</App>

// GOOD - Use Context
const UserContext = createContext<User | null>(null);

function App() {
  return (
    <UserContext.Provider value={user}>
      <Layout>
        <Sidebar>
          <UserInfo />
        </Sidebar>
      </Layout>
    </UserContext.Provider>
  );
}

function UserInfo() {
  const user = useContext(UserContext);
  return <div>{user?.name}</div>;
}
```

### Avoid: Mutating State Directly

```tsx
// BAD - Mutates state directly
const addItem = (item: Item) => {
  items.push(item); // WRONG
  setItems(items);  // Won't trigger re-render
};

// GOOD - Create new array
const addItem = (item: Item) => {
  setItems(prev => [...prev, item]);
};

// GOOD - For objects
const updateUser = (field: string, value: string) => {
  setUser(prev => ({ ...prev, [field]: value }));
};
```

### Avoid: useEffect for Derived State

```tsx
// BAD - Unnecessary effect and extra render
const [items, setItems] = useState<Item[]>([]);
const [total, setTotal] = useState(0);

useEffect(() => {
  setTotal(items.reduce((sum, item) => sum + item.price, 0));
}, [items]);

// GOOD - Compute during render
const [items, setItems] = useState<Item[]>([]);
const total = items.reduce((sum, item) => sum + item.price, 0);

// Or useMemo for expensive calculations
const total = useMemo(
  () => items.reduce((sum, item) => sum + item.price, 0),
  [items]
);
```
