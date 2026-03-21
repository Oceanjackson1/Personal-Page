---
title: "Stitch UI Design"
description: "Expert guide for creating effective prompts for Google Stitch AI UI design tool. Use when user wants to design UI/UX in Stitch, create app interfaces, generate mobile/web designs, or needs help cra..."
category: "development"
source: "community"
author: "Community"
tags: ["stitch", "ui", "design"]
date: 2026-03-20
---

# Stitch UI Design Prompting

Expert guidance for crafting effective prompts in Google Stitch, the AI-powered UI design tool by Google Labs. This skill helps create precise, actionable prompts that generate high-quality UI designs for web and mobile applications.

## What is Google Stitch?

Google Stitch is an experimental AI UI generator powered by Gemini 2.5 Flash that transforms text prompts and visual references into functional UI designs. It supports:

- Text-to-UI generation from natural language prompts
- Image-to-UI conversion from sketches, wireframes, or screenshots
- Multi-screen app flows and responsive layouts
- Export to HTML/CSS, Figma, and code
- Iterative refinement with variants and annotations

## Core Prompting Principles

### 1. Be Specific and Detailed

Generic prompts yield generic results. Specific prompts with clear requirements produce tailored, professional designs.

**Poor prompt:**
```
Create a dashboard
```

**Effective prompt:**
```
Member dashboard with course modules grid, progress tracking bar, 
and community feed sidebar using purple theme and card-based layout
```

**Why it works:** Specifies components (modules, progress, feed), layout structure (grid, sidebar), visual style (purple theme, cards), and context (member dashboard).

### 2. Define Visual Style and Theme

Always include color schemes, design aesthetics, and visual direction to avoid generic AI outputs.

**Components to specify:**
- Color palette (primary colors, accent colors)
- Design style (minimalist, modern, playful, professional, glassmorphic)
- Typography preferences (if any)
- Spacing and density (compact, spacious, balanced)

**Example:**
```
E-commerce product page with hero image gallery, add-to-cart CTA, 
reviews section, and related products carousel. Use clean minimalist 
design with sage green accents and generous white space.
```

### 3. Structure Multi-Screen Flows Clearly

For apps with multiple screens, list each screen as bullet points before generation.

**Approach:**
```
Fitness tracking app with:
- Onboarding screen with goal selection
- Home dashboard with daily stats and activity rings
- Workout library with category filters
- Profile screen with achievements and settings
```

Stitch will ask for confirmation before generating multiple screens, ensuring alignment with your vision.

### 4. Specify Platform and Responsive Behavior

Indicate whether the design is for mobile, tablet, desktop, or responsive web.

**Examples:**
```
Mobile app login screen (iOS style) with email/password fields and social auth buttons

Responsive landing page that adapts from mobile (320px) to desktop (1440px) 
with collapsible navigation
```

### 5. Include Functional Requirements

Describe interactive elements, states, and user flows to generate more complete designs.

**Elements to specify:**
- Button actions and CTAs
- Form fields and validation
- Navigation patterns
- Loading states
- Empty states
- Error handling

**Example:**
```
Checkout flow with:
- Cart summary with quantity adjusters
- Shipping address form with validation
- Payment method selection (cards, PayPal, Apple Pay)
- Order confirmation with tracking number
```

## Prompt Structure Template

Use this template for comprehensive prompts:

```
[Screen/Component Type] for [User/Context]

Key Features:
- [Feature 1 with specific details]
- [Feature 2 with specific details]
- [Feature 3 with specific details]

Visual Style:
- [Color scheme]
- [Design aesthetic]
- [Layout approach]

Platform: [Mobile/Web/Responsive]
```

**Example:**
```
Dashboard for SaaS analytics platform

Key Features:
- Top metrics cards showing MRR, active users, churn rate
- Line chart for revenue trends (last 30 days)
- Recent activity feed with user actions
- Quick action buttons for reports and exports

Visual Style:
- Dark mode with blue/purple gradient accents
- Modern glassmorphic cards with subtle shadows
- Clean data visualization with accessible colors

Platform: Responsive web (desktop-first)
```

## Iteration Strategies

### Refine with Annotations

Use Stitch's "annotate to edit" feature to make targeted changes without rewriting the entire prompt.

**Workflow:**
1. Generate initial design from prompt
2. Annotate specific elements that need changes
3. Describe modifications in natural language
4. Stitch updates only the annotated areas

**Example annotations:**
- "Make this button larger and use primary color"
- "Add more spacing between these cards"
- "Change this to a horizontal layout"

### Generate Variants

Request multiple variations to explore different design directions:

```
Generate 3 variants of this hero section:
1. Image-focused with minimal text
2. Text-heavy with supporting graphics
3. Video background with overlay content
```

### Progressive Refinement

Start broad, then add specificity in follow-up prompts:

**Initial:**
```
E-commerce homepage
```

**Refinement 1:**
```
Add featured products section with 4-column grid and hover effects
```

**Refinement 2:**
```
Update color scheme to earth tones (terracotta, sage, cream) 
and add promotional banner at top
```

## Common Use Cases

### Landing Pages

```
SaaS landing page for [product name]

Sections:
- Hero with headline, subheadline, CTA, and product screenshot
- Social proof with customer logos
- Features grid (3 columns) with icons
- Testimonials carousel
- Pricing table (3 tiers)
- FAQ accordion
- Footer with links and newsletter signup

Style: Modern, professional, trust-building
Colors: Navy blue primary, light blue accents, white background
```

### Mobile Apps

```
Food delivery app home screen

Components:
- Search bar with location selector
- Category chips (Pizza, Burgers, Sushi, etc.)
- Restaurant cards with image, name, rating, delivery time, and price range
- Bottom navigation (Home, Search, Orders, Profile)

Style: Vibrant, appetite-appealing, easy to scan
Colors: Orange primary, white background, food photography
Platform: iOS mobile (375px width)
```

### Dashboards

```
Admin dashboard for content management system

Layout:
- Left sidebar navigation with collapsible menu
- Top bar with search, notifications, and user profile
- Main content area with:
  - Stats overview (4 metric cards)
  - Recent posts table with actions
  - Activity timeline
  - Quick actions panel

Style: Clean, data-focused, professional
Colors: Neutral grays with blue accents
Platform: Desktop web (1440px)
```

### Forms and Inputs

```
Multi-step signup form for B2B platform

Steps:
1. Account details (company name, email, password)
2. Company information (industry, size, role)
3. Team setup (invite members)
4. Confirmation with success message

Features:
- Progress indicator at top
- Field validation with inline errors
- Back/Next navigation
- Skip option for step 3

Style: Minimal, focused, low-friction
Colors: White background, green for success states
```

## Design-to-Code Workflow

### Export Options

Stitch provides multiple export formats:

1. **HTML/CSS** - Clean, semantic markup for web projects
2. **Figma** - "Paste to Figma" for design system integration
3. **Code snippets** - Component-level exports for frameworks

### Best Practices for Export

**Before exporting:**
- Verify responsive breakpoints
- Check color contrast for accessibility
- Ensure interactive states are defined
- Review component naming and structure

**After export:**
- Refactor generated code for production standards
- Add proper semantic HTML tags
- Implement accessibility attributes (ARIA labels, alt text)
- Optimize images and assets
- Add animations and micro-interactions

## Anti-Patterns to Avoid

### ❌ Vague Prompts
```
Make a nice website
```

### ✅ Specific Prompts
```
Portfolio website for photographer with full-screen image gallery, 
project case studies, and contact form. Minimalist black and white 
aesthetic with serif typography.
```

---

### ❌ Missing Context
```
Create a login page
```

### ✅ Context-Rich Prompts
```
Login page for healthcare portal with email/password fields, 
"Remember me" checkbox, "Forgot password" link, and SSO options 
(Google, Microsoft). Professional, trustworthy design with 
blue medical theme.
```

---

### ❌ No Visual Direction
```
Design an app for task management
```

### ✅ Clear Visual Direction
```
Task management app with kanban board layout, drag-and-drop cards, 
priority labels, and due date indicators. Modern, productivity-focused 
design with purple/teal gradient accents and dark mode support.
```

## Tips for Better Results

1. **Reference existing designs** - Upload screenshots or sketches as visual references alongside text prompts

2. **Use design terminology** - Terms like "hero section," "card layout," "glassmorphic," "bento grid" help Stitch understand your intent

3. **Specify interactions** - Describe hover states, click actions, and transitions for more complete designs

4. **Think in components** - Break complex screens into reusable components (header, card, form, etc.)

5. **Iterate incrementally** - Make small, focused changes rather than complete redesigns

6. **Test responsiveness** - Always verify designs at multiple breakpoints (mobile, tablet, desktop)

7. **Consider accessibility** - Mention color contrast, font sizes, and touch target sizes in prompts

8. **Leverage variants** - Generate multiple options to explore different design directions quickly

## Integration with Development Workflow

### Stitch → Figma → Code
1. Generate UI in Stitch with detailed prompts
2. Export to Figma for design system integration
3. Hand off to developers with design specs
4. Implement with production-ready code

### Stitch → HTML → Framework
1. Generate and refine UI in Stitch
2. Export HTML/CSS code
3. Convert to React/Vue/Svelte components
4. Integrate into application codebase

### Rapid Prototyping
1. Create multiple screen variations quickly
2. Test with users or stakeholders
3. Iterate based on feedback
4. Finalize design for development

## Conclusion

Effective Stitch prompts are specific, context-rich, and visually descriptive. By following these principles and templates, you can generate professional UI designs that serve as strong foundations for production applications.

**Remember:** Stitch is a starting point, not a final product. Use it to accelerate the design process, explore ideas quickly, and establish visual direction—then refine with human judgment and production standards.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Advanced Techniques

# Advanced Stitch Techniques

Advanced strategies for maximizing Stitch's capabilities and creating production-ready designs.

## Table of Contents

1. [Image-to-UI Workflows](#image-to-ui-workflows)
2. [Design System Integration](#design-system-integration)
3. [Responsive Design Strategies](#responsive-design-strategies)
4. [Accessibility Considerations](#accessibility-considerations)
5. [Performance Optimization](#performance-optimization)
6. [Component Reusability](#component-reusability)

---

## Image-to-UI Workflows

### Converting Sketches to Digital UI

Stitch can interpret hand-drawn sketches, wireframes, and rough mockups.

**Best practices:**

1. **Clear structure** - Draw distinct boxes for components
2. **Label elements** - Annotate buttons, inputs, sections
3. **Show hierarchy** - Use size and position to indicate importance
4. **Include notes** - Add text describing interactions or states

**Example workflow:**
```
1. Sketch wireframe on paper or tablet
2. Take clear photo or scan
3. Upload to Stitch with prompt:
   "Convert this wireframe to a modern web interface with 
   glassmorphic design and purple gradient accents"
4. Refine generated design with annotations
```

### Reference-Based Design

Upload screenshots of existing designs to create similar layouts with your own branding.

**Prompt structure:**
```
Create a [type] similar to this reference image, but with:
- [Your color scheme]
- [Your content/copy]
- [Your brand style]
- [Specific modifications]
```

**Example:**
```
Create a pricing page similar to this reference, but with:
- Navy blue and gold color scheme
- 4 pricing tiers instead of 3
- Annual/monthly toggle
- Feature comparison table below
- Testimonials section at bottom
```

---

## Design System Integration

### Establishing Design Tokens

Define reusable design tokens in your initial prompt for consistency across screens.

**Token categories:**
- Colors (primary, secondary, accent, neutral, semantic)
- Typography (font families, sizes, weights, line heights)
- Spacing (scale: 4px, 8px, 16px, 24px, 32px, 48px, 64px)
- Border radius (none, sm, md, lg, full)
- Shadows (elevation levels)

**Example prompt:**
```
Dashboard using this design system:

Colors:
- Primary: #2563EB (blue)
- Secondary: #7C3AED (purple)
- Success: #10B981 (green)
- Warning: #F59E0B (amber)
- Error: #EF4444 (red)
- Neutral: #6B7280 (gray)

Typography:
- Headings: Inter Bold
- Body: Inter Regular
- Code: JetBrains Mono

Spacing: 8px base unit
Border radius: 8px for cards, 4px for buttons
Shadows: Subtle elevation with 0 4px 6px rgba(0,0,0,0.1)
```

### Component Library Approach

Create a component library by generating individual components first, then composing them into full screens.

**Workflow:**
```
1. Generate base components:
   - Button variants (primary, secondary, outline, ghost)
   - Input fields (text, email, password, search)
   - Cards (basic, with image, with actions)
   - Navigation (header, sidebar, tabs)

2. Document component specs:
   - States (default, hover, active, disabled)
   - Sizes (sm, md, lg)
   - Variants

3. Compose screens using established components:
   "Create a settings page using the button and input 
   components from previous generations"
```

---

## Responsive Design Strategies

### Mobile-First Approach

Start with mobile design, then scale up to tablet and desktop.

**Prompt sequence:**

**Step 1 - Mobile (375px):**
```
Mobile app home screen for recipe platform

Layout:
- Stacked vertical sections
- Full-width cards
- Bottom navigation
- Hamburger menu

Content:
- Search bar at top
- Featured recipe hero card
- Category chips (horizontal scroll)
- Recipe grid (1 column)
```

**Step 2 - Tablet (768px):**
```
Adapt the mobile recipe home screen for tablet:
- 2-column recipe grid
- Persistent sidebar navigation (replaces hamburger)
- Larger featured hero with side-by-side layout
- Category chips remain scrollable
```

**Step 3 - Desktop (1440px):**
```
Adapt for desktop:
- 3-column recipe grid
- Full sidebar with categories expanded
- Hero section with 3 featured recipes
- Top navigation bar with search and user menu
```

### Breakpoint-Specific Prompts

Specify exact breakpoints and layout changes.

**Example:**
```
Responsive product grid:

Mobile (< 640px):
- 1 column
- Full-width cards
- Vertical image orientation

Tablet (640px - 1024px):
- 2 columns
- Square images
- Compact card layout

Desktop (> 1024px):
- 4 columns
- Hover effects with overlay
- Quick view button
```

---

## Accessibility Considerations

### WCAG Compliance Prompts

Include accessibility requirements directly in prompts.

**Key areas to specify:**

1. **Color Contrast**
```
Ensure all text meets WCAG AA standards:
- Normal text: 4.5:1 contrast ratio minimum
- Large text (18pt+): 3:1 contrast ratio minimum
- Interactive elements: clear focus states with 3:1 contrast
```

2. **Touch Targets**
```
All interactive elements minimum 44x44px touch target size
Adequate spacing between clickable elements (8px minimum)
```

3. **Keyboard Navigation**
```
Clear focus indicators on all interactive elements
Logical tab order following visual flow
Skip navigation link for keyboard users
```

4. **Screen Reader Support**
```
Descriptive button labels (not just "Click here")
Alt text for all meaningful images
Form labels properly associated with inputs
Heading hierarchy (H1 → H2 → H3)
```

**Comprehensive accessibility prompt:**
```
Create an accessible contact form:

Fields:
- Name (required, with aria-required)
- Email (required, with validation and error message)
- Subject (dropdown with clear labels)
- Message (textarea with character count)

Accessibility features:
- All inputs have visible labels
- Required fields marked with asterisk and aria-required
- Error messages with role="alert"
- Submit button with descriptive text
- Focus indicators with 3px blue outline
- Color contrast meets WCAG AA
- Touch targets 44x44px minimum

Style: Clean, form-focused, high contrast
Colors: Dark text on light background, red for errors
```

### Inclusive Design Patterns

**Consider diverse users:**

```
Design a video player interface that supports:
- Captions/subtitles toggle
- Audio description option
- Keyboard shortcuts (space to play/pause, arrows to seek)
- Playback speed control
- High contrast mode
- Reduced motion option (disable animations)
```

---

## Performance Optimization

### Optimized Asset Prompts

Request performance-conscious designs from the start.

**Image optimization:**
```
E-commerce product gallery with performance optimization:
- Lazy loading for images below fold
- Thumbnail images (200x200px) for grid
- Full-size images (1200x1200px) only on click
- WebP format with JPEG fallback
- Blur placeholder while loading
```

**Code efficiency:**
```
Generate lightweight HTML/CSS without:
- Unnecessary wrapper divs
- Inline styles (use classes)
- Large external dependencies
- Redundant CSS rules
```

### Progressive Enhancement

Design for core functionality first, then enhance.

**Example:**
```
Create a filterable product list with progressive enhancement:

Base (no JavaScript):
- Server-rendered product grid
- Form-based filters with submit button
- Pagination links

Enhanced (with JavaScript):
- AJAX filter updates without page reload
- Infinite scroll
- Smooth animations
- Real-time search
```

---

## Component Reusability

### Atomic Design Methodology

Build from atoms → molecules → organisms → templates → pages.

**Atoms (basic elements):**
```
Generate design system atoms:
- Button (primary, secondary, outline, ghost, danger)
- Input field (text, email, password, search, textarea)
- Label, Badge, Tag
- Icon set (24x24px, consistent style)
- Avatar (circle, square, with status indicator)
```

**Molecules (simple combinations):**
```
Create molecules using atoms:
- Search bar (input + button + icon)
- Form field (label + input + error message)
- Card header (avatar + name + timestamp + menu)
- Stat card (icon + label + value + trend)
```

**Organisms (complex components):**
```
Build organisms from molecules:
- Navigation bar (logo + search bar + user menu)
- Product card (image + title + price + rating + button)
- Comment thread (avatar + name + timestamp + text + actions)
- Data table (headers + rows + pagination + filters)
```

**Templates (page layouts):**
```
Compose templates from organisms:
- Dashboard layout (sidebar + header + content grid)
- Article layout (header + hero + content + sidebar)
- Checkout flow (progress + form + summary)
```

### Variant Generation

Create systematic variations of components.

**Button variants prompt:**
```
Generate button component with all variants:

Sizes: Small (32px), Medium (40px), Large (48px)

Types:
- Primary (filled, brand color)
- Secondary (filled, gray)
- Outline (border only)
- Ghost (transparent, hover background)
- Danger (filled, red)

States for each:
- Default
- Hover
- Active (pressed)
- Disabled
- Loading (with spinner)

Include: Icon support (left/right), full-width option
```

---

## Advanced Iteration Techniques

### Conditional Variations

Generate multiple versions based on different conditions.

**Example:**
```
Create 3 hero section variants for A/B testing:

Variant A - Image-focused:
- Large background image
- Minimal text overlay
- Single CTA button

Variant B - Text-focused:
- Solid color background
- Detailed copy with bullet points
- Two CTA buttons (primary + secondary)

Variant C - Video-focused:
- Background video
- Minimal text
- Play button + CTA

All variants use same brand colors and maintain mobile responsiveness
```

### State-Based Design

Design for all possible states, not just the happy path.

**Comprehensive state prompt:**
```
Design a data table with all states:

Default state:
- 10 rows of data
- Sortable columns
- Pagination

Loading state:
- Skeleton loaders for rows
- Disabled controls

Empty state:
- Illustration
- "No data found" message
- "Add new" CTA button

Error state:
- Error icon
- Error message
- "Retry" button

Search/Filter active:
- Applied filters shown as chips
- Clear filters option
- Result count

Selected rows:
- Checkbox selection
- Bulk action toolbar
- Select all option
```

---

## Export and Handoff Best Practices

### Preparing for Development

Before exporting, ensure designs are developer-ready.

**Pre-export checklist:**

1. **Naming conventions**
   - Use semantic class names
   - Follow BEM or consistent methodology
   - Name components clearly

2. **Documentation**
   - Add comments for complex interactions
   - Document responsive breakpoints
   - Note any required JavaScript behavior

3. **Asset organization**
   - Export images at correct sizes
   - Provide SVG for icons
   - Include font files or CDN links

4. **Specifications**
   - Document spacing values
   - List color hex codes
   - Specify font sizes and weights

### Figma Integration

Optimize Stitch → Figma workflow.

**Steps:**
```
1. Generate design in Stitch with detailed specifications
2. Use "Paste to Figma" export
3. In Figma:
   - Organize layers with clear naming
   - Create components from repeated elements
   - Set up auto-layout for responsive behavior
   - Define color and text styles
   - Add design system documentation
4. Share with developers using Figma's inspect mode
```

### Code Export Refinement

Improve exported HTML/CSS for production.

**Post-export tasks:**

1. **Semantic HTML**
   - Replace divs with semantic tags (header, nav, main, article, section, footer)
   - Add ARIA labels where needed
   - Ensure proper heading hierarchy

2. **CSS optimization**
   - Extract repeated styles into utility classes
   - Use CSS custom properties for theme values
   - Organize with methodology (BEM, SMACSS, etc.)
   - Add responsive media queries if missing

3. **Accessibility**
   - Add alt text to images
   - Ensure form labels are associated
   - Add focus styles
   - Test with screen reader

4. **Performance**
   - Optimize images
   - Minify CSS
   - Remove unused styles
   - Add loading strategies

---

## Conclusion

These advanced techniques help you move beyond basic Stitch usage to create production-ready, accessible, and performant designs. Combine these strategies with the core prompting principles to maximize your efficiency and output quality.

**Key takeaways:**
- Use images and references to accelerate design
- Establish design systems early for consistency
- Design responsively from the start
- Prioritize accessibility in every prompt
- Think in reusable components
- Plan for all states, not just happy paths
- Refine exports before production use

---

## Reference: Prompt Examples

# Stitch Prompt Examples Library

Comprehensive collection of effective Stitch prompts organized by use case and complexity level.

## Table of Contents

1. [Landing Pages](#landing-pages)
2. [Mobile Apps](#mobile-apps)
3. [Dashboards](#dashboards)
4. [E-commerce](#e-commerce)
5. [Forms & Authentication](#forms--authentication)
6. [Content Platforms](#content-platforms)
7. [SaaS Applications](#saas-applications)

---

## Landing Pages

### Startup Landing Page

```
Landing page for AI writing assistant startup

Hero Section:
- Bold headline: "Write Better, Faster with AI"
- Subheadline explaining value proposition
- Primary CTA button "Start Free Trial"
- Secondary CTA "Watch Demo"
- Hero illustration showing product interface

Features Section:
- 3-column grid with icons
- Feature 1: AI-powered suggestions
- Feature 2: Multi-language support
- Feature 3: Team collaboration

Social Proof:
- Customer logos (6 companies)
- Testimonial cards with photos and quotes

Pricing:
- 3-tier pricing table (Free, Pro, Enterprise)
- Feature comparison
- Annual/Monthly toggle

Style: Modern, tech-forward, trustworthy
Colors: Deep purple primary, cyan accents, white background
Typography: Sans-serif, clean and readable
Platform: Responsive web
```

### Service Business Landing

```
Landing page for boutique yoga studio

Above Fold:
- Full-width hero image of studio space
- Centered headline: "Find Your Balance"
- Class schedule CTA button
- Location and hours overlay

Class Offerings:
- Card grid (2x3) with class types
- Each card: class name, duration, difficulty level, instructor photo
- Hover effect reveals class description

Instructor Profiles:
- Horizontal scrolling carousel
- Circular photos with names and specialties

Testimonials:
- Large quote format with student photos
- 5-star ratings

Call-to-Action:
- "Book Your First Class Free" banner
- Contact form with name, email, phone

Style: Calm, organic, welcoming
Colors: Sage green, warm beige, soft white
Typography: Serif headings, sans-serif body
Platform: Responsive web with mobile-first approach
```

---

## Mobile Apps

### Fitness Tracking App

```
Fitness tracking app - Home screen (iOS)

Top Section:
- Greeting with user name and current date
- Daily goal progress ring (calories, steps, active minutes)
- Motivational message based on progress

Quick Stats Cards:
- Today's steps with trend arrow
- Active calories burned
- Distance covered
- Active time

Recent Workouts:
- List of last 3 workouts with type, duration, calories
- Thumbnail icons for workout type
- Swipe actions for details/delete

Bottom Section:
- "Start Workout" prominent button
- Quick access to workout types (Run, Cycle, Strength, Yoga)

Bottom Navigation:
- Home (active), Workouts, Progress, Profile

Style: Energetic, motivating, data-focused
Colors: Vibrant orange primary, dark mode background, neon accents
Typography: Bold headings, clear metrics
Platform: iOS mobile (375x812px)
```

### Food Delivery App

```
Restaurant detail screen for food delivery app

Header:
- Restaurant cover photo
- Back button and favorite icon
- Restaurant name, rating (4.5 stars), delivery time (25-35 min)
- Cuisine tags (Italian, Pizza, Pasta)

Info Bar:
- Delivery fee, minimum order, distance
- Promo badge if applicable

Menu Categories:
- Sticky horizontal scroll tabs (Popular, Pizza, Pasta, Salads, Drinks)

Menu Items:
- Card layout with food photo, name, description, price
- Add button with quantity selector
- Dietary icons (vegetarian, spicy, etc.)

Floating Cart:
- Bottom sheet showing cart summary
- Item count and total price
- "View Cart" button

Style: Appetite-appealing, easy to scan, vibrant
Colors: Red primary (hunger-inducing), white background, food photography
Typography: Friendly sans-serif
Platform: Android mobile (360x800px)
```

---

## Dashboards

### Analytics Dashboard

```
Web analytics dashboard for marketing team

Top Bar:
- Date range selector (last 7 days, 30 days, custom)
- Export button
- Notification bell
- User profile dropdown

Key Metrics Row:
- 4 metric cards in a row
- Card 1: Total visitors (with % change)
- Card 2: Conversion rate (with trend sparkline)
- Card 3: Bounce rate (with comparison to previous period)
- Card 4: Average session duration

Main Chart:
- Line chart showing traffic over time
- Multiple lines for different sources (Organic, Paid, Social, Direct)
- Interactive legend to toggle lines
- Hover tooltips with exact values

Secondary Panels:
- Left: Top pages table (page, views, avg time, bounce rate)
- Right: Traffic sources pie chart with percentages

Bottom Section:
- Recent conversions table with user, source, value, timestamp

Style: Clean, data-focused, professional
Colors: Navy blue sidebar, white main area, colorful chart lines
Typography: Monospace for numbers, sans-serif for labels
Platform: Desktop web (1440px+)
```

### Project Management Dashboard

```
Project management dashboard - Team view

Sidebar:
- Workspace selector dropdown
- Navigation: Dashboard, Projects, Tasks, Team, Reports
- Create new project button

Header:
- Project name and status badge
- Team member avatars (max 5, then +N)
- Search bar
- View options (Board, List, Calendar)

Kanban Board:
- 4 columns: To Do, In Progress, Review, Done
- Drag-and-drop cards
- Each card shows: title, assignee avatar, due date, priority label, comment count
- Add card button at bottom of each column

Right Panel:
- Task details when card is selected
- Description, attachments, comments, activity log

Quick Stats:
- Progress bar showing completion percentage
- Tasks by status mini chart
- Upcoming deadlines list

Style: Modern, organized, collaborative
Colors: Purple primary, light gray background, status color coding
Typography: Clear sans-serif, readable at all sizes
Platform: Desktop web (1280px+)
```

---

## E-commerce

### Product Detail Page

```
Product detail page for fashion e-commerce

Image Gallery:
- Main product image (large, zoomable)
- Thumbnail strip below (5-6 images)
- 360° view option
- Video thumbnail if available

Product Info:
- Brand name
- Product title
- Star rating (4.8) with review count (234 reviews)
- Price with original price struck through if on sale
- Sale badge if applicable

Options:
- Size selector (XS, S, M, L, XL) with availability indicators
- Color swatches with product image preview on hover
- Quantity selector

Actions:
- Add to Cart button (prominent)
- Add to Wishlist button (outline)
- Size guide link
- Shipping calculator

Product Details:
- Tabbed interface (Description, Specifications, Reviews, Shipping)
- Expandable sections on mobile

Recommendations:
- "You May Also Like" carousel
- "Complete the Look" suggestions

Style: Clean, product-focused, trustworthy
Colors: Black and white with brand accent color (burgundy)
Typography: Elegant serif for headings, sans-serif for body
Platform: Responsive web
```

### Shopping Cart

```
Shopping cart page with checkout flow

Cart Items:
- List of products with thumbnail, name, size/color, price
- Quantity adjuster (+/- buttons)
- Remove item link
- Save for later option

Order Summary:
- Sticky sidebar on desktop, bottom sheet on mobile
- Subtotal
- Shipping (calculated or "Free over $50")
- Tax (estimated)
- Discount code input field
- Total (prominent)
- Checkout button (large, primary color)

Trust Signals:
- Secure checkout badge
- Free returns policy
- Customer service contact

Recommendations:
- "Frequently Bought Together" section
- Promotional banner for free shipping threshold

Empty State:
- Illustration
- "Your cart is empty" message
- "Continue Shopping" button
- Recently viewed items

Style: Clean, conversion-focused, reassuring
Colors: Green for checkout CTA, neutral grays, trust badges
Typography: Clear pricing, readable product names
Platform: Responsive web
```

---

## Forms & Authentication

### Multi-Step Signup Form

```
B2B SaaS signup flow - 3 steps

Progress Indicator:
- Step 1: Account (active)
- Step 2: Company
- Step 3: Team

Step 1 - Account Details:
- Email input with validation
- Password input with strength indicator
- Confirm password
- Terms and conditions checkbox
- "Continue" button
- "Already have an account? Sign in" link

Step 2 - Company Information:
- Company name
- Industry dropdown
- Company size radio buttons (1-10, 11-50, 51-200, 201+)
- Role/Title input
- "Back" and "Continue" buttons

Step 3 - Invite Team:
- Email input fields (dynamic, add more)
- Role selector for each invite
- "Skip for now" option
- "Finish Setup" button

Success State:
- Checkmark animation
- "Welcome to [Product]!" message
- "Go to Dashboard" button

Style: Minimal, focused, low-friction
Colors: Blue primary, white background, green success states
Typography: Clear labels, helpful microcopy
Platform: Responsive web, mobile-optimized
```

### Login Page

```
Login page for enterprise software

Left Panel (Desktop):
- Brand logo
- Hero image or illustration
- Value proposition headline
- Key benefits (3 bullet points)

Right Panel (Form):
- "Welcome back" heading
- Email input field
- Password input field with show/hide toggle
- "Remember me" checkbox
- "Forgot password?" link
- "Sign In" button (full width)
- Divider with "OR"
- SSO options (Google, Microsoft, Okta) as buttons with logos
- "Don't have an account? Sign up" link at bottom

Security Indicators:
- SSL badge
- "Your data is secure" message

Style: Professional, trustworthy, enterprise-grade
Colors: Corporate blue, white, subtle grays
Typography: Professional sans-serif
Platform: Responsive (left panel hidden on mobile)
```

---

## Content Platforms

### Blog Post Layout

```
Blog article page for tech publication

Header:
- Site navigation (logo, categories, search, subscribe)

Article Header:
- Category tag
- Article title (large, bold)
- Subtitle/excerpt
- Author info (photo, name, bio link, publish date)
- Social share buttons
- Reading time estimate

Article Body:
- Readable column width (max 680px)
- Paragraph text with proper line height
- H2 and H3 subheadings
- Pull quotes (styled distinctly)
- Inline images with captions
- Code blocks with syntax highlighting
- Embedded videos
- Table of contents (sticky sidebar on desktop)

Article Footer:
- Tags
- Share buttons
- Author card (expanded)
- Related articles (3 cards)
- Comments section

Sidebar (Desktop):
- Newsletter signup
- Popular posts
- Ad placement

Style: Editorial, readable, content-first
Colors: Black text on white, accent color for links
Typography: Serif for body text, sans-serif for UI
Platform: Responsive web
```

### Video Platform Interface

```
Video streaming platform - Watch page

Video Player:
- Full-width video player with controls
- Quality selector, playback speed, captions, fullscreen
- Progress bar with thumbnail preview on hover

Video Info:
- Video title
- View count and upload date
- Like/Dislike buttons
- Share button
- Save to playlist button

Channel Info:
- Channel avatar and name
- Subscriber count
- Subscribe button (prominent if not subscribed)

Description:
- Expandable description text
- Show more/less toggle
- Hashtags and links

Comments Section:
- Sort options (Top, Newest)
- Comment input with user avatar
- Comment cards with avatar, name, timestamp, text
- Like/Reply buttons
- Nested replies (indented)

Sidebar:
- Up next autoplay preview
- Recommended videos list (thumbnail, title, channel, views)

Style: Dark mode, video-focused, minimal distractions
Colors: Dark gray background, white text, red accent for CTAs
Typography: Sans-serif, readable at distance
Platform: Responsive web
```

---

## SaaS Applications

### Email Client Interface

```
Email client - Inbox view

Left Sidebar:
- Compose button (prominent)
- Folder list (Inbox, Sent, Drafts, Spam, Trash)
- Labels/Tags with color coding
- Storage usage indicator

Email List (Center):
- Search bar with filters
- Sort and view options
- Email rows showing:
  - Sender avatar/initial
  - Sender name (bold if unread)
  - Subject line
  - Preview text (truncated)
  - Timestamp
  - Attachment icon if present
  - Star/flag icons
- Checkbox for bulk actions
- Pagination or infinite scroll

Email Detail (Right):
- Email header (from, to, cc, timestamp)
- Subject line
- Email body with formatting preserved
- Attachments section
- Action buttons (Reply, Reply All, Forward, Archive, Delete)
- Previous emails in thread (collapsed)

Top Bar:
- Refresh button
- Settings icon
- User profile dropdown

Style: Clean, productivity-focused, organized
Colors: Blue accents, white background, gray dividers
Typography: Sans-serif, scannable
Platform: Desktop web (1280px+)
```

### CRM Contact Detail

```
CRM contact detail page

Header:
- Contact name and company
- Contact photo/avatar
- Status badge (Lead, Customer, Inactive)
- Quick actions (Email, Call, Schedule Meeting, Edit)

Info Tabs:
- Overview (active), Activity, Deals, Notes, Files

Overview Tab:
- Contact information card (email, phone, address, social links)
- Company information card
- Tags and custom fields
- Assigned to (team member)

Activity Timeline:
- Chronological list of interactions
- Icons for type (email, call, meeting, note)
- Timestamp and description
- Filter by activity type

Deals Section:
- Active deals table (deal name, value, stage, close date)
- Won/Lost deals summary

Notes Section:
- Add note input with rich text editor
- Note cards with author, timestamp, content
- Pin important notes

Right Sidebar:
- Next scheduled activity
- Recent emails
- Related contacts
- Deal pipeline stage

Style: Professional, data-rich, organized
Colors: Navy blue, white, status color coding
Typography: Clear hierarchy, readable data
Platform: Desktop web (1440px+)
```

---

## Tips for Using These Examples

1. **Customize for your needs** - Replace placeholder content with your specific requirements
2. **Combine elements** - Mix and match components from different examples
3. **Adjust complexity** - Simplify or expand based on your project scope
4. **Specify your brand** - Add your color palette, fonts, and visual style
5. **Consider platform** - Adapt layouts for your target device (mobile/desktop)
6. **Add context** - Include user personas or use cases for better results
7. **Iterate** - Start with a basic prompt, then refine with annotations

Remember: These are starting points. Stitch works best when you provide specific details relevant to your unique project.
