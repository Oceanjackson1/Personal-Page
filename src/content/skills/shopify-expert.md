---
title: "Shopify Expert"
description: "Builds and debugs Shopify themes (.liquid files, theme.json, sections), develops custom Shopify apps (shopify.app.toml, OAuth, webhooks), and implements Storefront API integrations for headless storefronts. Use when building or customizing Shopify..."
category: "development"
source: "community"
author: "Community"
tags: ["shopify"]
date: 2026-03-20
---

# Shopify Expert

Senior Shopify developer with expertise in theme development, headless commerce, app architecture, and custom checkout solutions.

## Core Workflow

1. **Requirements analysis** — Identify if theme, app, or headless approach fits needs
2. **Architecture setup** — Scaffold with `shopify theme init` or `shopify app create`; configure `shopify.app.toml` and theme schema
3. **Implementation** — Build Liquid templates, write GraphQL queries, or develop app features (see examples below)
4. **Validation** — Run `shopify theme check` for Liquid linting; if errors are found, fix them and re-run before proceeding. Run `shopify app dev` to verify app locally; test checkout extensions in sandbox. If validation fails at any step, resolve all reported issues before moving to deployment
5. **Deploy and monitor** — `shopify theme push` for themes; `shopify app deploy` for apps; watch Shopify error logs and performance metrics post-deploy

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Liquid Templating | `references/liquid-templating.md` | Theme development, template customization |
| Storefront API | `references/storefront-api.md` | Headless commerce, Hydrogen, custom frontends |
| App Development | `references/app-development.md` | Building Shopify apps, OAuth, webhooks |
| Checkout Extensions | `references/checkout-customization.md` | Checkout UI extensions, Shopify Functions |
| Performance | `references/performance-optimization.md` | Theme speed, asset optimization, caching |

## Code Examples

### Liquid — Product template with metafield access
```liquid
{% comment %} templates/product.liquid {% endcomment %}
<h1>{{ product.title }}</h1>
<p>{{ product.metafields.custom.care_instructions.value }}</p>

{% for variant in product.variants %}
  <option
    value="{{ variant.id }}"
    {% unless variant.available %}disabled{% endunless %}
  >
    {{ variant.title }} — {{ variant.price | money }}
  </option>
{% endfor %}

{{ product.description | metafield_tag }}
```

### Liquid — Collection filtering (Online Store 2.0)
```liquid
{% comment %} sections/collection-filters.liquid {% endcomment %}
{% for filter in collection.filters %}
  <details>
    <summary>{{ filter.label }}</summary>
    {% for value in filter.values %}
      <label>
        <input
          type="checkbox"
          name="{{ value.param_name }}"
          value="{{ value.value }}"
          {% if value.active %}checked{% endif %}
        >
        {{ value.label }} ({{ value.count }})
      </label>
    {% endfor %}
  </details>
{% endfor %}
```

### Storefront API — GraphQL product query
```graphql
query ProductByHandle($handle: String!) {
  product(handle: $handle) {
    id
    title
    descriptionHtml
    featuredImage {
      url(transform: { maxWidth: 800, preferredContentType: WEBP })
      altText
    }
    variants(first: 10) {
      edges {
        node {
          id
          title
          price { amount currencyCode }
          availableForSale
          selectedOptions { name value }
        }
      }
    }
    metafield(namespace: "custom", key: "care_instructions") {
      value
      type
    }
  }
}
```

### Shopify CLI — Common commands
```bash
# Theme development
shopify theme dev --store=your-store.myshopify.com   # Live preview with hot reload
shopify theme check                                   # Lint Liquid for errors/warnings
shopify theme push --only templates/ sections/        # Partial push
shopify theme pull                                    # Sync remote changes locally

# App development
shopify app create node                               # Scaffold Node.js app
shopify app dev                                       # Local dev with ngrok tunnel
shopify app deploy                                    # Submit app version
shopify app generate extension                        # Add checkout UI extension

# GraphQL
shopify app generate graphql                          # Generate typed GraphQL hooks
```

### App — Authenticated Admin API fetch (TypeScript)
```typescript
import { authenticate } from "../shopify.server";
import type { LoaderFunctionArgs } from "@remix-run/node";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin } = await authenticate.admin(request);

  const response = await admin.graphql(`
    query {
      shop { name myshopifyDomain plan { displayName } }
    }
  `);

  const { data } = await response.json();
  return data.shop;
};
```

## Constraints

### MUST DO
- Use Liquid 2.0 syntax for themes
- Implement proper metafield handling
- Use Storefront API 2024-10 or newer
- Optimize images with Shopify CDN filters
- Follow Shopify CLI workflows
- Use App Bridge for embedded apps
- Implement proper error handling for API calls
- Follow Shopify theme architecture patterns
- Use TypeScript for app development
- Test checkout extensions in sandbox
- Run `shopify theme check` before every theme deployment

### MUST NOT DO
- Hardcode API credentials in theme code
- Exceed Storefront API rate limits (2000 points/sec)
- Use deprecated REST Admin API endpoints
- Skip GDPR compliance for customer data
- Deploy untested checkout extensions
- Use synchronous API calls in Liquid (deprecated)
- Ignore theme performance metrics
- Store sensitive data in metafields without encryption

## Output Templates

When implementing Shopify solutions, provide:
1. Complete file structure with proper naming
2. Liquid/GraphQL/TypeScript code with types
3. Configuration files (shopify.app.toml, schema settings)
4. API scopes and permissions needed
5. Testing approach and deployment steps

## Knowledge Reference

Shopify CLI 3.x, Liquid 2.0, Storefront API 2024-10, Admin API, GraphQL, Hydrogen 2024, Remix, Oxygen, Polaris, App Bridge 4.0, Checkout UI Extensions, Shopify Functions, metafields, metaobjects, theme architecture, Shopify Plus features

---

## Reference: App Development

# App Development

---

## When to Use

- Building custom Shopify apps for merchants
- Creating public apps for the Shopify App Store
- Integrating third-party services with Shopify
- Automating merchant workflows
- Building embedded admin experiences

## When NOT to Use

- Theme customization (use Liquid)
- Customer-facing storefronts (use Storefront API)
- Simple product displays (use Liquid or Storefront API)
- Checkout-only customizations (use Checkout Extensions)

---

## App Architecture Overview

### App Types

| Type | Use Case | Distribution |
|------|----------|--------------|
| Custom App | Single merchant, private | Manual install |
| Public App | App Store listing | Shopify review |
| Sales Channel | Custom storefront | App Store |
| Embedded App | Admin integration | Either |

### Modern Stack (2024+)

```bash
# Create new Shopify app with Remix template
npm create @shopify/app@latest

# Project structure
shopify-app/
├── app/
│   ├── routes/              # Remix routes
│   │   ├── app._index.tsx   # Main app page
│   │   ├── app.products.tsx # Products page
│   │   └── webhooks.tsx     # Webhook handlers
│   ├── shopify.server.ts    # Shopify API client
│   └── db.server.ts         # Database client
├── extensions/              # App extensions
├── prisma/                  # Database schema
├── shopify.app.toml         # App configuration
└── package.json
```

---

## App Configuration

### shopify.app.toml

```toml
# shopify.app.toml
scopes = "read_products,write_products,read_orders,write_orders,read_customers"

[access_scopes]
# Use optional scopes for granular permissions
optional = ["read_inventory", "write_inventory"]

[auth]
redirect_urls = [
  "https://your-app.com/auth/callback",
  "https://your-app.com/auth/shopify/callback"
]

[webhooks]
api_version = "2024-10"

  [[webhooks.subscriptions]]
  topics = ["products/create", "products/update", "products/delete"]
  uri = "/webhooks"

  [[webhooks.subscriptions]]
  topics = ["orders/create"]
  uri = "/webhooks"

  [[webhooks.subscriptions]]
  topics = ["app/uninstalled"]
  uri = "/webhooks"

[app_proxy]
url = "https://your-app.com/api/proxy"
subpath = "apps"
prefix = "your-app"

[pos]
embedded = false

[build]
automatically_update_urls_on_dev = true
dev_store_url = "your-dev-store.myshopify.com"

[app]
name = "Your App Name"
handle = "your-app-handle"
```

---

## OAuth Implementation

### Authentication Flow

```typescript
// app/shopify.server.ts
import "@shopify/shopify-app-remix/adapters/node";
import {
  ApiVersion,
  AppDistribution,
  shopifyApp,
  DeliveryMethod,
} from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";

const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY!,
  apiSecretKey: process.env.SHOPIFY_API_SECRET!,
  appUrl: process.env.SHOPIFY_APP_URL!,
  scopes: process.env.SCOPES?.split(","),
  apiVersion: ApiVersion.October24,
  distribution: AppDistribution.AppStore,
  sessionStorage: new PrismaSessionStorage(prisma),
  webhooks: {
    APP_UNINSTALLED: {
      deliveryMethod: DeliveryMethod.Http,
      callbackUrl: "/webhooks",
    },
    PRODUCTS_CREATE: {
      deliveryMethod: DeliveryMethod.Http,
      callbackUrl: "/webhooks",
    },
    ORDERS_CREATE: {
      deliveryMethod: DeliveryMethod.Http,
      callbackUrl: "/webhooks",
    },
  },
  hooks: {
    afterAuth: async ({ session, admin }) => {
      // Register webhooks after OAuth
      shopify.registerWebhooks({ session });

      // Perform post-install setup
      await setupShop(session, admin);
    },
  },
});

async function setupShop(session: Session, admin: AdminApiContext) {
  // Store merchant data
  await prisma.shop.upsert({
    where: { shopDomain: session.shop },
    update: { accessToken: session.accessToken },
    create: {
      shopDomain: session.shop,
      accessToken: session.accessToken!,
      installedAt: new Date(),
    },
  });
}

export default shopify;
export const apiVersion = ApiVersion.October24;
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;
export const authenticate = shopify.authenticate;
export const unauthenticated = shopify.unauthenticated;
export const login = shopify.login;
export const registerWebhooks = shopify.registerWebhooks;
export const sessionStorage = shopify.sessionStorage;
```

### Protected Routes

```typescript
// app/routes/app._index.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { Page, Layout, Card, DataTable } from "@shopify/polaris";
import { authenticate } from "../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
  const { admin, session } = await authenticate.admin(request);

  // Make Admin API requests
  const response = await admin.graphql(`
    query {
      shop {
        name
        email
        myshopifyDomain
        plan {
          displayName
        }
      }
      products(first: 10) {
        edges {
          node {
            id
            title
            status
            totalInventory
          }
        }
      }
    }
  `);

  const data = await response.json();

  return json({
    shop: data.data.shop,
    products: data.data.products.edges.map((edge: any) => edge.node),
  });
}

export default function Index() {
  const { shop, products } = useLoaderData<typeof loader>();

  const rows = products.map((product: any) => [
    product.title,
    product.status,
    product.totalInventory,
  ]);

  return (
    <Page title={`Welcome to ${shop.name}`}>
      <Layout>
        <Layout.Section>
          <Card>
            <DataTable
              columnContentTypes={["text", "text", "numeric"]}
              headings={["Product", "Status", "Inventory"]}
              rows={rows}
            />
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

---

## Admin API (GraphQL)

### Products CRUD

```typescript
// Create product
const CREATE_PRODUCT = `
  mutation productCreate($input: ProductInput!) {
    productCreate(input: $input) {
      product {
        id
        title
        handle
        variants(first: 10) {
          edges {
            node {
              id
              price
              sku
            }
          }
        }
      }
      userErrors {
        field
        message
      }
    }
  }
`;

// Usage
const response = await admin.graphql(CREATE_PRODUCT, {
  variables: {
    input: {
      title: "New Product",
      descriptionHtml: "<p>Product description</p>",
      vendor: "Your Brand",
      productType: "T-Shirt",
      tags: ["new", "featured"],
      variants: [
        {
          price: "29.99",
          sku: "SKU-001",
          inventoryManagement: "SHOPIFY",
          inventoryPolicy: "DENY",
          options: ["Small", "Blue"],
        },
        {
          price: "29.99",
          sku: "SKU-002",
          options: ["Medium", "Blue"],
        },
      ],
      options: ["Size", "Color"],
    },
  },
});

// Update product
const UPDATE_PRODUCT = `
  mutation productUpdate($input: ProductInput!) {
    productUpdate(input: $input) {
      product {
        id
        title
      }
      userErrors {
        field
        message
      }
    }
  }
`;

// Bulk operations for large datasets
const BULK_MUTATION = `
  mutation bulkOperationRunMutation($mutation: String!, $stagedUploadPath: String!) {
    bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
      bulkOperation {
        id
        status
      }
      userErrors {
        field
        message
      }
    }
  }
`;
```

### Orders Management

```typescript
// Fetch orders with fulfillment status
const GET_ORDERS = `
  query getOrders($first: Int!, $query: String) {
    orders(first: $first, query: $query, sortKey: CREATED_AT, reverse: true) {
      edges {
        node {
          id
          name
          createdAt
          displayFinancialStatus
          displayFulfillmentStatus
          totalPriceSet {
            shopMoney {
              amount
              currencyCode
            }
          }
          customer {
            firstName
            lastName
            email
          }
          lineItems(first: 5) {
            edges {
              node {
                title
                quantity
                variant {
                  id
                  sku
                }
              }
            }
          }
          shippingAddress {
            address1
            city
            province
            country
            zip
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
`;

// Create fulfillment
const CREATE_FULFILLMENT = `
  mutation fulfillmentCreate($fulfillment: FulfillmentInput!) {
    fulfillmentCreate(fulfillment: $fulfillment) {
      fulfillment {
        id
        status
        trackingInfo {
          number
          url
        }
      }
      userErrors {
        field
        message
      }
    }
  }
`;
```

### Metafields

```typescript
// Set product metafields
const SET_METAFIELDS = `
  mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
    metafieldsSet(metafields: $metafields) {
      metafields {
        id
        namespace
        key
        value
        type
      }
      userErrors {
        field
        message
      }
    }
  }
`;

// Usage
await admin.graphql(SET_METAFIELDS, {
  variables: {
    metafields: [
      {
        ownerId: "gid://shopify/Product/123456789",
        namespace: "custom",
        key: "care_instructions",
        value: "Machine wash cold",
        type: "single_line_text_field",
      },
      {
        ownerId: "gid://shopify/Product/123456789",
        namespace: "custom",
        key: "features",
        value: JSON.stringify(["Organic cotton", "Fair trade", "Eco-friendly"]),
        type: "list.single_line_text_field",
      },
    ],
  },
});

// Read metafields
const GET_PRODUCT_METAFIELDS = `
  query getProductMetafields($id: ID!) {
    product(id: $id) {
      metafields(first: 20) {
        edges {
          node {
            id
            namespace
            key
            value
            type
          }
        }
      }
    }
  }
`;
```

---

## Webhook Handling

### Webhook Route

```typescript
// app/routes/webhooks.tsx
import type { ActionFunctionArgs } from "@remix-run/node";
import { authenticate } from "../shopify.server";
import db from "../db.server";

export async function action({ request }: ActionFunctionArgs) {
  const { topic, shop, session, admin, payload } =
    await authenticate.webhook(request);

  console.log(`Received ${topic} webhook for ${shop}`);

  switch (topic) {
    case "APP_UNINSTALLED":
      await handleAppUninstalled(shop);
      break;

    case "PRODUCTS_CREATE":
      await handleProductCreate(shop, payload);
      break;

    case "PRODUCTS_UPDATE":
      await handleProductUpdate(shop, payload);
      break;

    case "ORDERS_CREATE":
      await handleOrderCreate(shop, payload, admin);
      break;

    case "CUSTOMERS_DATA_REQUEST":
      await handleDataRequest(shop, payload);
      break;

    case "CUSTOMERS_REDACT":
      await handleCustomerRedact(shop, payload);
      break;

    case "SHOP_REDACT":
      await handleShopRedact(shop, payload);
      break;

    default:
      console.log(`Unhandled webhook topic: ${topic}`);
  }

  return new Response("OK", { status: 200 });
}

async function handleAppUninstalled(shop: string) {
  // Clean up shop data
  await db.shop.delete({
    where: { shopDomain: shop },
  });
}

async function handleProductCreate(shop: string, payload: any) {
  // Sync product to your database
  await db.product.create({
    data: {
      shopDomain: shop,
      shopifyId: payload.admin_graphql_api_id,
      title: payload.title,
      handle: payload.handle,
      status: payload.status,
    },
  });
}

async function handleOrderCreate(shop: string, payload: any, admin: any) {
  // Process new order
  const order = {
    id: payload.admin_graphql_api_id,
    orderNumber: payload.order_number,
    totalPrice: payload.total_price,
    customer: payload.customer,
    lineItems: payload.line_items,
  };

  // Example: Add order note
  await admin.graphql(`
    mutation addOrderNote($id: ID!, $note: String!) {
      orderUpdate(input: { id: $id, note: $note }) {
        order { id }
        userErrors { field message }
      }
    }
  `, {
    variables: {
      id: order.id,
      note: "Processed by Your App",
    },
  });
}

// GDPR webhooks (required for public apps)
async function handleDataRequest(shop: string, payload: any) {
  // Return customer data
  const customerId = payload.customer.id;
  // Gather and return all customer data
}

async function handleCustomerRedact(shop: string, payload: any) {
  // Delete customer data
  const customerId = payload.customer.id;
  await db.customerData.deleteMany({
    where: { shopDomain: shop, customerId: String(customerId) },
  });
}

async function handleShopRedact(shop: string, payload: any) {
  // Delete all shop data (48 hours after uninstall)
  await db.shop.delete({ where: { shopDomain: shop } });
}
```

---

## App Bridge 4.0

### Setup

```typescript
// app/root.tsx
import { AppProvider } from "@shopify/shopify-app-remix/react";
import polarisStyles from "@shopify/polaris/build/esm/styles.css?url";

export const links = () => [{ rel: "stylesheet", href: polarisStyles }];

export default function App() {
  const { apiKey } = useLoaderData<typeof loader>();

  return (
    <html>
      <head>
        <Meta />
        <Links />
      </head>
      <body>
        <AppProvider isEmbeddedApp apiKey={apiKey}>
          <Outlet />
        </AppProvider>
        <Scripts />
      </body>
    </html>
  );
}
```

### App Bridge Actions

```typescript
// Using App Bridge in components
import { useAppBridge } from "@shopify/app-bridge-react";
import { Redirect } from "@shopify/app-bridge/actions";

function MyComponent() {
  const app = useAppBridge();

  const redirectToProduct = (productId: string) => {
    const redirect = Redirect.create(app);
    redirect.dispatch(Redirect.Action.ADMIN_PATH, {
      path: `/products/${productId}`,
    });
  };

  const openResourcePicker = async () => {
    const selection = await app.resourcePicker({
      type: "product",
      multiple: true,
      filter: {
        variants: false,
        archived: false,
      },
    });

    if (selection) {
      console.log("Selected products:", selection);
    }
  };

  return (
    <Button onClick={openResourcePicker}>Select Products</Button>
  );
}
```

### Toast Notifications

```typescript
import { useAppBridge } from "@shopify/app-bridge-react";
import { Toast } from "@shopify/app-bridge/actions";

function SaveButton() {
  const app = useAppBridge();

  const handleSave = async () => {
    try {
      await saveData();
      const toast = Toast.create(app, {
        message: "Settings saved successfully",
        duration: 3000,
      });
      toast.dispatch(Toast.Action.SHOW);
    } catch (error) {
      const toast = Toast.create(app, {
        message: "Error saving settings",
        duration: 5000,
        isError: true,
      });
      toast.dispatch(Toast.Action.SHOW);
    }
  };

  return <Button primary onClick={handleSave}>Save</Button>;
}
```

---

## Polaris Design System

### Common Patterns

```typescript
import {
  Page,
  Layout,
  Card,
  FormLayout,
  TextField,
  Select,
  Button,
  Banner,
  Modal,
  ResourceList,
  ResourceItem,
  Avatar,
  TextStyle,
  Stack,
  Badge,
  Pagination,
} from "@shopify/polaris";

function SettingsPage() {
  const [formState, setFormState] = useState({
    apiKey: "",
    environment: "production",
  });
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  return (
    <Page
      title="App Settings"
      primaryAction={{
        content: "Save",
        loading: loading,
        onAction: handleSave,
      }}
      secondaryActions={[
        { content: "Reset", onAction: handleReset },
      ]}
    >
      <Layout>
        <Layout.Section>
          <Banner
            title="Configuration required"
            status="warning"
            action={{ content: "Learn more", url: "/docs" }}
          >
            Please configure your API settings to enable all features.
          </Banner>
        </Layout.Section>

        <Layout.AnnotatedSection
          title="API Configuration"
          description="Configure your external API connection."
        >
          <Card>
            <Card.Section>
              <FormLayout>
                <TextField
                  label="API Key"
                  value={formState.apiKey}
                  onChange={(value) => setFormState({ ...formState, apiKey: value })}
                  type="password"
                  autoComplete="off"
                />
                <Select
                  label="Environment"
                  options={[
                    { label: "Production", value: "production" },
                    { label: "Sandbox", value: "sandbox" },
                  ]}
                  value={formState.environment}
                  onChange={(value) => setFormState({ ...formState, environment: value })}
                />
              </FormLayout>
            </Card.Section>
          </Card>
        </Layout.AnnotatedSection>

        <Layout.Section>
          <Card title="Connected Products">
            <ResourceList
              items={products}
              renderItem={(item) => (
                <ResourceItem
                  id={item.id}
                  media={<Avatar customer size="medium" source={item.image} />}
                  accessibilityLabel={`View details for ${item.title}`}
                >
                  <Stack>
                    <Stack.Item fill>
                      <TextStyle variation="strong">{item.title}</TextStyle>
                    </Stack.Item>
                    <Badge status={item.synced ? "success" : "warning"}>
                      {item.synced ? "Synced" : "Pending"}
                    </Badge>
                  </Stack>
                </ResourceItem>
              )}
            />
          </Card>
        </Layout.Section>
      </Layout>

      <Modal
        open={showModal}
        onClose={() => setShowModal(false)}
        title="Confirm action"
        primaryAction={{
          content: "Confirm",
          destructive: true,
          onAction: handleConfirm,
        }}
        secondaryActions={[
          { content: "Cancel", onAction: () => setShowModal(false) },
        ]}
      >
        <Modal.Section>
          Are you sure you want to proceed?
        </Modal.Section>
      </Modal>
    </Page>
  );
}
```

---

## Testing

### Unit Tests

```typescript
// tests/webhooks.test.ts
import { describe, it, expect, vi } from "vitest";
import { action } from "../app/routes/webhooks";

describe("Webhook handlers", () => {
  it("handles product create webhook", async () => {
    const mockRequest = new Request("https://app.com/webhooks", {
      method: "POST",
      headers: {
        "X-Shopify-Topic": "products/create",
        "X-Shopify-Shop-Domain": "test-shop.myshopify.com",
        "X-Shopify-Hmac-Sha256": "valid-hmac",
      },
      body: JSON.stringify({
        id: 123456789,
        title: "Test Product",
        handle: "test-product",
      }),
    });

    const response = await action({ request: mockRequest, params: {}, context: {} });
    expect(response.status).toBe(200);
  });
});
```

### Development

```bash
# Start development server with hot reload
npm run dev

# Generate GraphQL types
npm run shopify app generate types

# Test webhooks locally
npm run shopify app webhook trigger --topic PRODUCTS_CREATE

# Deploy to Shopify
npm run deploy
```

---

## Related References

- **Storefront API** - For customer-facing features
- **Checkout Customization** - For checkout extensions
- **Liquid Templating** - For theme app extensions

---

## Reference: Checkout Customization

# Checkout Customization

---

## When to Use

- Adding custom UI to checkout (banners, fields, upsells)
- Implementing custom discount logic with Shopify Functions
- Building post-purchase experiences
- Customizing shipping and payment options
- Checkout branding and localization

## When NOT to Use

- Full checkout replacement (not possible on Shopify)
- Theme-level cart customization (use Liquid)
- Pre-checkout flows (use theme or headless)
- Admin-side order processing (use Admin API)

---

## Checkout Extensibility Overview

### Extension Points

| Extension | Purpose | API Version |
|-----------|---------|-------------|
| `Checkout::Dynamic::Render` | Add UI anywhere in checkout | 2024.10+ |
| `Checkout::CartLineDetails::RenderAfter` | Below cart line items | 2024.10+ |
| `Checkout::DeliveryAddress::RenderBefore` | Before delivery address | 2024.10+ |
| `purchase.checkout.block.render` | Custom blocks in checkout | 2024.10+ |
| `purchase.thank-you.block.render` | Thank you page | 2024.10+ |
| `purchase.post-purchase.render` | Post-purchase upsell | 2024.10+ |

### Project Setup

```bash
# Create checkout extension
npm run shopify app generate extension -- --type checkout_ui

# Extension structure
extensions/
└── checkout-ui/
    ├── src/
    │   └── Checkout.tsx    # Main extension component
    ├── locales/
    │   └── en.default.json # Translations
    ├── shopify.extension.toml
    └── package.json
```

---

## Checkout UI Extensions

### Configuration

```toml
# extensions/checkout-ui/shopify.extension.toml
api_version = "2024-10"

[[extensions]]
type = "ui_extension"
name = "Custom Checkout Banner"
handle = "custom-checkout-banner"

[[extensions.targeting]]
module = "./src/Checkout.tsx"
target = "purchase.checkout.block.render"

[extensions.capabilities]
api_access = true
network_access = true
block_progress = true

[extensions.settings]
  [[extensions.settings.fields]]
  key = "banner_text"
  type = "single_line_text_field"
  name = "Banner Text"
  description = "Text to display in the banner"

  [[extensions.settings.fields]]
  key = "banner_status"
  type = "single_line_text_field"
  name = "Banner Status"
  description = "info, warning, success, or critical"
```

### Basic Extension Component

```tsx
// extensions/checkout-ui/src/Checkout.tsx
import {
  reactExtension,
  Banner,
  useSettings,
  useTranslate,
  BlockStack,
  Text,
  useExtensionCapability,
  useBuyerJourneyIntercept,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => (
  <CheckoutBanner />
));

function CheckoutBanner() {
  const translate = useTranslate();
  const { banner_text, banner_status } = useSettings();

  return (
    <Banner
      status={banner_status || "info"}
      title={banner_text || translate("default_banner_title")}
    />
  );
}
```

### Cart Line Item Extension

```tsx
// extensions/cart-upsell/src/CartLineUpsell.tsx
import {
  reactExtension,
  useCartLines,
  useApplyCartLinesChange,
  Button,
  Text,
  InlineStack,
  Image,
  BlockStack,
  Divider,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension(
  "purchase.checkout.cart-line-list.render-after",
  () => <CartUpsell />
);

function CartUpsell() {
  const cartLines = useCartLines();
  const applyCartLinesChange = useApplyCartLinesChange();

  // Example: Suggest complementary product based on cart contents
  const upsellProduct = getUpsellRecommendation(cartLines);

  if (!upsellProduct) return null;

  const handleAddToCart = async () => {
    const result = await applyCartLinesChange({
      type: "addCartLine",
      merchandiseId: upsellProduct.variantId,
      quantity: 1,
    });

    if (result.type === "error") {
      console.error("Failed to add item:", result.message);
    }
  };

  return (
    <BlockStack spacing="loose">
      <Divider />
      <Text emphasis="bold">Complete your order</Text>
      <InlineStack spacing="base" blockAlignment="center">
        <Image
          source={upsellProduct.image}
          accessibilityDescription={upsellProduct.title}
          aspectRatio={1}
          cornerRadius="base"
        />
        <BlockStack spacing="none">
          <Text>{upsellProduct.title}</Text>
          <Text appearance="subdued">{upsellProduct.price}</Text>
        </BlockStack>
        <Button kind="secondary" onPress={handleAddToCart}>
          Add
        </Button>
      </InlineStack>
    </BlockStack>
  );
}

function getUpsellRecommendation(cartLines: CartLine[]) {
  // Logic to determine upsell based on cart contents
  // This would typically call your backend or use metafields
  return null; // Implement based on your business logic
}
```

### Custom Form Fields

```tsx
// extensions/custom-fields/src/CustomFields.tsx
import {
  reactExtension,
  useApplyMetafieldsChange,
  useMetafield,
  TextField,
  Checkbox,
  BlockStack,
  Text,
  useBuyerJourneyIntercept,
} from "@shopify/ui-extensions-react/checkout";
import { useState } from "react";

export default reactExtension(
  "purchase.checkout.delivery-address.render-before",
  () => <DeliveryInstructions />
);

function DeliveryInstructions() {
  const [instructions, setInstructions] = useState("");
  const [leaveAtDoor, setLeaveAtDoor] = useState(false);
  const [error, setError] = useState("");

  const applyMetafieldsChange = useApplyMetafieldsChange();

  // Block checkout if validation fails
  useBuyerJourneyIntercept(({ canBlockProgress }) => {
    if (canBlockProgress && leaveAtDoor && !instructions) {
      return {
        behavior: "block",
        reason: "Please provide delivery instructions when leaving at door",
        errors: [
          {
            message: "Delivery instructions required",
            target: "$.cart.deliveryInstructions",
          },
        ],
      };
    }
    return { behavior: "allow" };
  });

  const handleInstructionsChange = async (value: string) => {
    setInstructions(value);
    setError("");

    await applyMetafieldsChange({
      type: "updateMetafield",
      namespace: "custom",
      key: "delivery_instructions",
      valueType: "string",
      value,
    });
  };

  const handleLeaveAtDoorChange = async (checked: boolean) => {
    setLeaveAtDoor(checked);

    await applyMetafieldsChange({
      type: "updateMetafield",
      namespace: "custom",
      key: "leave_at_door",
      valueType: "boolean",
      value: String(checked),
    });
  };

  return (
    <BlockStack spacing="base">
      <Text emphasis="bold">Delivery Preferences</Text>

      <Checkbox checked={leaveAtDoor} onChange={handleLeaveAtDoorChange}>
        Leave package at door
      </Checkbox>

      <TextField
        label="Delivery Instructions"
        value={instructions}
        onChange={handleInstructionsChange}
        error={error}
        multiline={3}
        maxLength={250}
      />
    </BlockStack>
  );
}
```

---

## Shopify Functions

### Discount Function

```bash
# Generate discount function
npm run shopify app generate extension -- --type product_discounts
```

```toml
# extensions/volume-discount/shopify.extension.toml
api_version = "2024-10"

[[extensions]]
name = "Volume Discount"
handle = "volume-discount"
type = "function"
description = "Apply discounts based on quantity"

[extensions.build]
command = "cargo wasi build --release"
path = "target/wasm32-wasip1/release/volume-discount.wasm"
watch = ["src/**/*.rs", "Cargo.toml"]

[extensions.ui]
enable_create = true

[[extensions.ui.paths]]
path = "create"
module = "./src/CreateDiscount.tsx"

[[extensions.ui.paths]]
path = "details"
module = "./src/DiscountDetails.tsx"

[extensions.input.variables]
namespace = "$app:volume-discount"
key = "config"
```

```rust
// extensions/volume-discount/src/main.rs
use shopify_function::prelude::*;
use shopify_function::Result;

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, PartialEq)]
#[serde(rename_all = "camelCase")]
struct Config {
    tiers: Vec<Tier>,
}

#[derive(Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "camelCase")]
struct Tier {
    quantity: i64,
    percentage: f64,
}

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<output::FunctionRunResult> {
    let config: Config = input
        .discount_node
        .metafield
        .as_ref()
        .map(|m| serde_json::from_str(&m.value).unwrap_or_default())
        .unwrap_or_default();

    let mut discounts = vec![];

    for line in input.cart.lines {
        if let input::InputCartLinesMerchandise::ProductVariant(variant) = &line.merchandise {
            let quantity = line.quantity;

            // Find applicable tier
            let applicable_tier = config
                .tiers
                .iter()
                .filter(|t| quantity >= t.quantity)
                .max_by_key(|t| t.quantity);

            if let Some(tier) = applicable_tier {
                discounts.push(output::Discount {
                    value: output::Value::Percentage(output::Percentage {
                        value: Decimal(tier.percentage),
                    }),
                    targets: vec![output::Target::CartLine(output::CartLineTarget {
                        id: line.id.clone(),
                        quantity: None,
                    })],
                    message: Some(format!("{}% off for buying {} or more", tier.percentage, tier.quantity)),
                });
            }
        }
    }

    Ok(output::FunctionRunResult {
        discounts,
        discount_application_strategy: output::DiscountApplicationStrategy::FIRST,
    })
}
```

```graphql
# extensions/volume-discount/src/run.graphql
query RunInput {
  cart {
    lines {
      id
      quantity
      merchandise {
        ... on ProductVariant {
          id
          product {
            id
            handle
          }
        }
      }
    }
  }
  discountNode {
    metafield(namespace: "$app:volume-discount", key: "config") {
      value
    }
  }
}
```

### Shipping Customization Function

```rust
// extensions/shipping-customization/src/main.rs
use shopify_function::prelude::*;
use shopify_function::Result;

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<output::FunctionRunResult> {
    let mut operations = vec![];

    // Example: Hide express shipping for PO Box addresses
    let is_po_box = input
        .cart
        .delivery_groups
        .iter()
        .any(|group| {
            group.delivery_address.as_ref().map_or(false, |addr| {
                addr.address1.as_ref().map_or(false, |a| {
                    a.to_lowercase().contains("po box") ||
                    a.to_lowercase().contains("p.o. box")
                })
            })
        });

    if is_po_box {
        for group in &input.cart.delivery_groups {
            for option in &group.delivery_options {
                if option.title.as_ref().map_or(false, |t| t.contains("Express")) {
                    operations.push(output::Operation::Hide(output::HideOperation {
                        delivery_option_handle: option.handle.clone(),
                    }));
                }
            }
        }
    }

    // Example: Rename shipping option based on cart value
    let cart_total: f64 = input.cart.cost.subtotal_amount.amount.parse().unwrap_or(0.0);

    if cart_total >= 100.0 {
        for group in &input.cart.delivery_groups {
            for option in &group.delivery_options {
                if option.title.as_ref().map_or(false, |t| t.contains("Standard")) {
                    operations.push(output::Operation::Rename(output::RenameOperation {
                        delivery_option_handle: option.handle.clone(),
                        title: Some("Free Standard Shipping".to_string()),
                    }));
                }
            }
        }
    }

    Ok(output::FunctionRunResult { operations })
}
```

### Payment Customization Function

```rust
// extensions/payment-customization/src/main.rs
use shopify_function::prelude::*;
use shopify_function::Result;

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<output::FunctionRunResult> {
    let mut operations = vec![];

    // Example: Hide Cash on Delivery for international orders
    let is_international = input
        .cart
        .delivery_groups
        .iter()
        .any(|group| {
            group.delivery_address.as_ref().map_or(false, |addr| {
                addr.country_code.as_ref().map_or(false, |c| c != "US")
            })
        });

    if is_international {
        for method in &input.payment_methods {
            if method.name.contains("Cash on Delivery") || method.name.contains("COD") {
                operations.push(output::Operation::Hide(output::HideOperation {
                    payment_method_id: method.id.clone(),
                }));
            }
        }
    }

    // Example: Reorder payment methods based on cart total
    let cart_total: f64 = input.cart.cost.subtotal_amount.amount.parse().unwrap_or(0.0);

    if cart_total >= 500.0 {
        // Move "Pay Later" options to top for high-value orders
        for method in &input.payment_methods {
            if method.name.contains("Affirm") || method.name.contains("Klarna") {
                operations.push(output::Operation::Move(output::MoveOperation {
                    payment_method_id: method.id.clone(),
                    index: 0,
                }));
            }
        }
    }

    Ok(output::FunctionRunResult { operations })
}
```

---

## Post-Purchase Extensions

### Post-Purchase Upsell

```tsx
// extensions/post-purchase/src/PostPurchase.tsx
import {
  extend,
  render,
  useExtensionInput,
  BlockStack,
  Button,
  CalloutBanner,
  Heading,
  Image,
  Text,
  TextContainer,
  Layout,
  View,
} from "@shopify/post-purchase-ui-extensions-react";

extend("Checkout::PostPurchase::ShouldRender", async ({ inputData, storage }) => {
  // Decide whether to show post-purchase page
  const { initialPurchase } = inputData;

  // Skip for orders under $50
  const orderTotal = parseFloat(initialPurchase.totalPriceSet.shopMoney.amount);
  if (orderTotal < 50) {
    return { render: false };
  }

  // Fetch upsell offer from your backend
  const response = await fetch("https://your-app.com/api/upsell", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      orderId: initialPurchase.referenceId,
      lineItems: initialPurchase.lineItems,
    }),
  });

  const { offer } = await response.json();

  if (!offer) {
    return { render: false };
  }

  // Store offer data for render phase
  await storage.update({ offer });

  return { render: true };
});

render("Checkout::PostPurchase::Render", () => <PostPurchaseOffer />);

function PostPurchaseOffer() {
  const {
    storage,
    inputData,
    calculateChangeset,
    applyChangeset,
    done,
  } = useExtensionInput();

  const [loading, setLoading] = useState(false);
  const [accepted, setAccepted] = useState(false);

  const offer = storage.initialData.offer;

  const handleAccept = async () => {
    setLoading(true);

    // Calculate price with the upsell item
    const changeset = await calculateChangeset({
      changes: [
        {
          type: "add_variant",
          variantId: offer.variantId,
          quantity: 1,
          discount: {
            value: offer.discountPercentage,
            valueType: "percentage",
            title: "Post-purchase discount",
          },
        },
      ],
    });

    // Apply the upsell to the order
    await applyChangeset(changeset.token);

    setAccepted(true);
    setLoading(false);

    // Track conversion
    await fetch("https://your-app.com/api/upsell/accepted", {
      method: "POST",
      body: JSON.stringify({ orderId: inputData.initialPurchase.referenceId }),
    });

    // Wait a moment then proceed
    setTimeout(() => done(), 2000);
  };

  const handleDecline = () => {
    done();
  };

  if (accepted) {
    return (
      <BlockStack spacing="loose" alignment="center">
        <CalloutBanner title="Added to your order!">
          <Text>{offer.title} has been added to your order.</Text>
        </CalloutBanner>
      </BlockStack>
    );
  }

  return (
    <BlockStack spacing="loose">
      <CalloutBanner title="Exclusive offer just for you!">
        <Text>Get {offer.discountPercentage}% off this item when you add it now.</Text>
      </CalloutBanner>

      <Layout
        media={[
          { viewportSize: "small", sizes: [1, 1] },
          { viewportSize: "medium", sizes: [1, 1] },
          { viewportSize: "large", sizes: [1, 1] },
        ]}
      >
        <View>
          <Image source={offer.image} />
        </View>
        <View>
          <BlockStack spacing="base">
            <Heading>{offer.title}</Heading>
            <TextContainer>
              <Text>{offer.description}</Text>
            </TextContainer>
            <Text emphasis="bold">
              <Text appearance="subdued" role="deletion">
                {offer.originalPrice}
              </Text>{" "}
              {offer.discountedPrice}
            </Text>
            <BlockStack spacing="tight">
              <Button onPress={handleAccept} loading={loading}>
                Add to order - {offer.discountedPrice}
              </Button>
              <Button plain onPress={handleDecline}>
                No thanks
              </Button>
            </BlockStack>
          </BlockStack>
        </View>
      </Layout>
    </BlockStack>
  );
}
```

---

## Checkout Branding API

### Customize Checkout Appearance

```typescript
// Using Admin API to set checkout branding
const UPDATE_CHECKOUT_BRANDING = `
  mutation checkoutBrandingUpsert($checkoutBrandingInput: CheckoutBrandingInput!, $checkoutProfileId: ID!) {
    checkoutBrandingUpsert(checkoutBrandingInput: $checkoutBrandingInput, checkoutProfileId: $checkoutProfileId) {
      checkoutBranding {
        customizations {
          headingLevel1 {
            typography {
              font
              size
              weight
            }
          }
          primaryButton {
            background
            cornerRadius
            blockPadding
          }
          control {
            cornerRadius
            border
          }
        }
        designSystem {
          colors {
            schemes {
              scheme1 {
                base {
                  background
                  text
                  accent
                }
                primaryButton {
                  background
                  text
                }
              }
            }
          }
          typography {
            primary {
              shopifyFontGroup {
                name
              }
            }
            secondary {
              shopifyFontGroup {
                name
              }
            }
          }
          cornerRadius {
            base
            small
            large
          }
        }
      }
      userErrors {
        field
        message
      }
    }
  }
`;

// Example branding configuration
const brandingInput = {
  designSystem: {
    colors: {
      schemes: {
        scheme1: {
          base: {
            background: "#FFFFFF",
            text: "#1A1A1A",
            accent: "#0066CC",
          },
          primaryButton: {
            background: "#0066CC",
            text: "#FFFFFF",
          },
          control: {
            background: "#F5F5F5",
            border: "#CCCCCC",
          },
        },
      },
    },
    typography: {
      primary: {
        shopifyFontGroup: {
          name: "Inter",
        },
      },
    },
    cornerRadius: {
      base: 8,
      small: 4,
      large: 16,
    },
  },
  customizations: {
    primaryButton: {
      cornerRadius: "LARGE",
      blockPadding: "BASE",
    },
    headingLevel1: {
      typography: {
        size: "EXTRA_LARGE",
        weight: "BOLD",
      },
    },
  },
};
```

---

## Testing Extensions

### Local Development

```bash
# Start development server with extension preview
npm run shopify app dev

# Test specific extension
npm run shopify app dev --checkout-cart-url="https://your-store.myshopify.com/cart/123:1"

# Generate preview URL
npm run shopify app dev --tunnel-url="https://your-ngrok-url.ngrok.io"
```

### Extension Testing Best Practices

1. **Use sandbox checkout profiles** - Test without affecting production
2. **Test all buyer journeys** - Guest, logged in, express checkout
3. **Test error states** - Network failures, validation errors
4. **Test internationalization** - Multiple languages and currencies
5. **Performance test** - Extension should load in <100ms

```typescript
// Test file for checkout extension
import { describe, it, expect } from "vitest";
import { render } from "@shopify/ui-extensions/test-utilities";
import { CheckoutBanner } from "./Checkout";

describe("CheckoutBanner", () => {
  it("renders with default settings", () => {
    const { root } = render(<CheckoutBanner />);

    expect(root).toContainReactComponent("Banner", {
      status: "info",
    });
  });

  it("displays custom banner text from settings", () => {
    const { root } = render(<CheckoutBanner />, {
      settings: {
        banner_text: "Free shipping on orders over $50!",
        banner_status: "success",
      },
    });

    expect(root).toContainReactComponent("Banner", {
      title: "Free shipping on orders over $50!",
      status: "success",
    });
  });
});
```

---

## Related References

- **App Development** - For backend webhook handling
- **Storefront API** - For headless checkout flows
- **Liquid Templating** - For pre-checkout cart customization

---

## Reference: Liquid Templating

# Liquid Templating

---

## When to Use

- Building or customizing Shopify Online Store 2.0 themes
- Creating custom sections and blocks with JSON schemas
- Implementing product, collection, and page templates
- Working with metafields and metaobjects in templates
- Building dynamic content with Liquid logic

## When NOT to Use

- Headless commerce (use Storefront API instead)
- App development (use Remix/React with Admin API)
- Complex business logic (use Shopify Functions)

---

## Theme Architecture (Online Store 2.0)

### Directory Structure

```
theme/
├── assets/               # CSS, JS, images
├── config/
│   ├── settings_schema.json  # Theme settings
│   └── settings_data.json    # Setting values
├── layout/
│   ├── theme.liquid      # Main layout
│   └── password.liquid   # Password page layout
├── locales/              # Translation files
├── sections/             # Reusable sections
├── snippets/             # Reusable partials
├── templates/
│   ├── customers/        # Account templates
│   ├── index.json        # Homepage
│   ├── product.json      # Product pages
│   ├── collection.json   # Collection pages
│   └── page.json         # Custom pages
└── blocks/               # App blocks (optional)
```

### JSON Templates (Online Store 2.0)

```json
// templates/product.json
{
  "sections": {
    "main": {
      "type": "main-product",
      "settings": {
        "enable_sticky_info": true,
        "media_size": "large"
      },
      "blocks": {
        "title": { "type": "title" },
        "price": { "type": "price" },
        "variant_picker": { "type": "variant_picker" },
        "buy_buttons": { "type": "buy_buttons" }
      },
      "block_order": ["title", "price", "variant_picker", "buy_buttons"]
    },
    "recommendations": {
      "type": "product-recommendations",
      "settings": {
        "heading": "You may also like",
        "products_to_show": 4
      }
    }
  },
  "order": ["main", "recommendations"]
}
```

---

## Section Schema Patterns

### Complete Section with Blocks

```liquid
{% comment %}
  sections/featured-collection.liquid
{% endcomment %}

<section class="featured-collection section-{{ section.id }}">
  <div class="container">
    {% if section.settings.heading != blank %}
      <h2 class="section-heading">{{ section.settings.heading }}</h2>
    {% endif %}

    <div class="product-grid columns-{{ section.settings.columns }}">
      {% for product in section.settings.collection.products limit: section.settings.products_to_show %}
        {% render 'product-card', product: product, show_vendor: section.settings.show_vendor %}
      {% endfor %}
    </div>

    {% for block in section.blocks %}
      {% case block.type %}
        {% when 'custom_badge' %}
          <div class="custom-badge" {{ block.shopify_attributes }}>
            {{ block.settings.badge_text }}
          </div>
        {% when 'countdown' %}
          <div class="countdown-timer"
               data-end-date="{{ block.settings.end_date }}"
               {{ block.shopify_attributes }}>
          </div>
      {% endcase %}
    {% endfor %}
  </div>
</section>

{% schema %}
{
  "name": "Featured Collection",
  "tag": "section",
  "class": "featured-collection-section",
  "limit": 3,
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Featured Products"
    },
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 4,
      "label": "Products to show"
    },
    {
      "type": "select",
      "id": "columns",
      "label": "Columns",
      "options": [
        { "value": "2", "label": "2 columns" },
        { "value": "3", "label": "3 columns" },
        { "value": "4", "label": "4 columns" }
      ],
      "default": "4"
    },
    {
      "type": "checkbox",
      "id": "show_vendor",
      "label": "Show vendor",
      "default": false
    }
  ],
  "blocks": [
    {
      "type": "custom_badge",
      "name": "Custom Badge",
      "limit": 1,
      "settings": [
        {
          "type": "text",
          "id": "badge_text",
          "label": "Badge Text",
          "default": "Sale"
        }
      ]
    },
    {
      "type": "countdown",
      "name": "Countdown Timer",
      "limit": 1,
      "settings": [
        {
          "type": "text",
          "id": "end_date",
          "label": "End Date (ISO format)",
          "info": "Example: 2025-12-31T23:59:59"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Featured Collection",
      "blocks": []
    }
  ]
}
{% endschema %}

{% stylesheet %}
  .featured-collection {
    padding: 40px 0;
  }
{% endstylesheet %}

{% javascript %}
  // Section-specific JavaScript
{% endjavascript %}
```

---

## Liquid Filters and Tags

### Essential Object Access

```liquid
{% comment %} Product object {% endcomment %}
{{ product.title }}
{{ product.description }}
{{ product.price | money }}
{{ product.compare_at_price | money }}
{{ product.featured_image | image_url: width: 600 }}
{{ product.url }}
{{ product.vendor }}
{{ product.type }}
{{ product.tags | join: ', ' }}

{% comment %} Variant handling {% endcomment %}
{% for variant in product.variants %}
  <option
    value="{{ variant.id }}"
    {% if variant.available == false %}disabled{% endif %}
    data-price="{{ variant.price }}"
  >
    {{ variant.title }} - {{ variant.price | money }}
  </option>
{% endfor %}

{% comment %} Check availability {% endcomment %}
{% if product.available %}
  {% if product.variants.size > 1 %}
    {% comment %} Show variant picker {% endcomment %}
  {% else %}
    {% comment %} Show add to cart {% endcomment %}
  {% endif %}
{% else %}
  <span class="sold-out">Sold Out</span>
{% endif %}
```

### Image Handling (Modern Syntax)

```liquid
{% comment %} Responsive images with srcset {% endcomment %}
{{ product.featured_image | image_url: width: 800 | image_tag:
  srcset: product.featured_image | image_url: width: 400 | append: ' 400w, ' |
          append: product.featured_image | image_url: width: 800 | append: ' 800w, ' |
          append: product.featured_image | image_url: width: 1200 | append: ' 1200w',
  sizes: '(max-width: 768px) 100vw, 50vw',
  loading: 'lazy',
  alt: product.featured_image.alt | escape
}}

{% comment %} Simple responsive image {% endcomment %}
{{
  product.featured_image | image_url: width: 600 | image_tag:
    loading: 'lazy',
    widths: '200, 400, 600, 800',
    alt: product.title
}}

{% comment %} Background image with focal point {% endcomment %}
<div
  class="hero-image"
  style="background-image: url('{{ section.settings.image | image_url: width: 1920 }}');
         background-position: {{ section.settings.image.presentation.focal_point }};"
>
</div>
```

### Metafield Access

```liquid
{% comment %} Product metafields {% endcomment %}
{% assign care_instructions = product.metafields.custom.care_instructions %}
{% if care_instructions %}
  <div class="care-instructions">
    {{ care_instructions.value }}
  </div>
{% endif %}

{% comment %} Metafield with type checking {% endcomment %}
{% assign size_chart = product.metafields.custom.size_chart %}
{% if size_chart.type == 'file_reference' %}
  <img src="{{ size_chart.value | image_url: width: 800 }}" alt="Size Chart">
{% endif %}

{% comment %} List metafield {% endcomment %}
{% assign features = product.metafields.custom.features.value %}
{% if features.size > 0 %}
  <ul class="product-features">
    {% for feature in features %}
      <li>{{ feature }}</li>
    {% endfor %}
  </ul>
{% endif %}

{% comment %} Metaobject reference {% endcomment %}
{% assign designer = product.metafields.custom.designer.value %}
{% if designer %}
  <div class="designer-info">
    <h4>{{ designer.name.value }}</h4>
    <p>{{ designer.bio.value }}</p>
    {% if designer.photo.value %}
      {{ designer.photo.value | image_url: width: 200 | image_tag }}
    {% endif %}
  </div>
{% endif %}
```

### Collection Filtering and Sorting

```liquid
{% comment %} Active filters display {% endcomment %}
{% for filter in collection.filters %}
  {% if filter.active_values.size > 0 %}
    <div class="active-filter">
      <strong>{{ filter.label }}:</strong>
      {% for value in filter.active_values %}
        <a href="{{ value.url_to_remove }}" class="remove-filter">
          {{ value.label }} &times;
        </a>
      {% endfor %}
    </div>
  {% endif %}
{% endfor %}

{% comment %} Filter form {% endcomment %}
<form id="filters-form">
  {% for filter in collection.filters %}
    <div class="filter-group">
      <h4>{{ filter.label }}</h4>

      {% case filter.type %}
        {% when 'list' %}
          {% for value in filter.values %}
            <label>
              <input
                type="checkbox"
                name="{{ filter.param_name }}"
                value="{{ value.value }}"
                {% if value.active %}checked{% endif %}
                {% if value.count == 0 %}disabled{% endif %}
              >
              {{ value.label }} ({{ value.count }})
            </label>
          {% endfor %}

        {% when 'price_range' %}
          <input
            type="range"
            name="{{ filter.param_name }}"
            min="{{ filter.range_min | money_without_currency }}"
            max="{{ filter.range_max | money_without_currency }}"
            value="{{ filter.max_value.value | money_without_currency }}"
          >
      {% endcase %}
    </div>
  {% endfor %}
</form>

{% comment %} Sort options {% endcomment %}
<select name="sort_by" id="sort-by">
  {% for option in collection.sort_options %}
    <option
      value="{{ option.value }}"
      {% if collection.sort_by == option.value %}selected{% endif %}
    >
      {{ option.name }}
    </option>
  {% endfor %}
</select>
```

---

## Cart and Checkout Integration

### Cart Form Pattern

```liquid
{% comment %} snippets/product-form.liquid {% endcomment %}

{% form 'product', product, id: 'product-form', class: 'product-form', data-product-form: '' %}
  <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}">

  {% unless product.has_only_default_variant %}
    {% for option in product.options_with_values %}
      <div class="product-option">
        <label for="Option-{{ option.name | handleize }}">
          {{ option.name }}
        </label>

        <select
          id="Option-{{ option.name | handleize }}"
          name="options[{{ option.name }}]"
          data-option-index="{{ forloop.index0 }}"
        >
          {% for value in option.values %}
            <option
              value="{{ value }}"
              {% if option.selected_value == value %}selected{% endif %}
            >
              {{ value }}
            </option>
          {% endfor %}
        </select>
      </div>
    {% endfor %}
  {% endunless %}

  <div class="quantity-selector">
    <label for="Quantity">Quantity</label>
    <input
      type="number"
      id="Quantity"
      name="quantity"
      value="1"
      min="1"
      max="{{ product.selected_or_first_available_variant.inventory_quantity | default: 99 }}"
    >
  </div>

  {% comment %} Line item properties {% endcomment %}
  {% if product.metafields.custom.enable_personalization %}
    <div class="personalization">
      <label for="personalization-text">Add personalization</label>
      <input
        type="text"
        id="personalization-text"
        name="properties[Personalization]"
        maxlength="50"
      >
    </div>
  {% endif %}

  <button
    type="submit"
    name="add"
    {% unless product.available %}disabled{% endunless %}
    class="add-to-cart-button"
  >
    {% if product.available %}
      Add to Cart - {{ product.selected_or_first_available_variant.price | money }}
    {% else %}
      Sold Out
    {% endif %}
  </button>
{% endform %}

<script type="application/json" id="product-json">
  {{ product | json }}
</script>
```

### AJAX Cart Updates

```liquid
{% comment %} snippets/cart-drawer.liquid {% endcomment %}

<div id="cart-drawer" class="cart-drawer" aria-hidden="true">
  <div class="cart-drawer__header">
    <h2>Your Cart ({{ cart.item_count }})</h2>
    <button type="button" class="cart-drawer__close" aria-label="Close cart">
      &times;
    </button>
  </div>

  <div class="cart-drawer__content">
    {% if cart.item_count > 0 %}
      <form action="{{ routes.cart_url }}" method="post" id="cart-drawer-form">
        {% for item in cart.items %}
          <div class="cart-item" data-line="{{ forloop.index }}">
            <img
              src="{{ item.image | image_url: width: 150 }}"
              alt="{{ item.title | escape }}"
              width="75"
              height="75"
              loading="lazy"
            >

            <div class="cart-item__details">
              <a href="{{ item.url }}">{{ item.product.title }}</a>
              {% unless item.product.has_only_default_variant %}
                <span class="cart-item__variant">{{ item.variant.title }}</span>
              {% endunless %}

              {% if item.properties.size > 0 %}
                {% for property in item.properties %}
                  {% unless property.last == blank %}
                    <span class="cart-item__property">
                      {{ property.first }}: {{ property.last }}
                    </span>
                  {% endunless %}
                {% endfor %}
              {% endif %}

              <div class="cart-item__quantity">
                <button type="button" data-quantity-minus>-</button>
                <input
                  type="number"
                  name="updates[]"
                  value="{{ item.quantity }}"
                  min="0"
                  data-line="{{ forloop.index }}"
                >
                <button type="button" data-quantity-plus>+</button>
              </div>

              <span class="cart-item__price">{{ item.final_line_price | money }}</span>
            </div>

            <a href="{{ item.url_to_remove }}" class="cart-item__remove" aria-label="Remove">
              Remove
            </a>
          </div>
        {% endfor %}

        <div class="cart-drawer__footer">
          {% if cart.cart_level_discount_applications.size > 0 %}
            <div class="cart-discounts">
              {% for discount in cart.cart_level_discount_applications %}
                <span class="discount">
                  {{ discount.title }}: -{{ discount.total_allocated_amount | money }}
                </span>
              {% endfor %}
            </div>
          {% endif %}

          <div class="cart-subtotal">
            <span>Subtotal</span>
            <span>{{ cart.total_price | money }}</span>
          </div>

          <p class="cart-note">Shipping and taxes calculated at checkout</p>

          <button type="submit" name="checkout" class="checkout-button">
            Checkout
          </button>
        </div>
      </form>
    {% else %}
      <p class="cart-empty">Your cart is empty</p>
      <a href="{{ routes.all_products_collection_url }}" class="continue-shopping">
        Continue Shopping
      </a>
    {% endif %}
  </div>
</div>
```

---

## Localization and Markets

### Multi-language Support

```liquid
{% comment %} Language/currency selector {% endcomment %}
{% form 'localization', id: 'localization-form' %}
  {% if localization.available_languages.size > 1 %}
    <div class="language-selector">
      <label for="language-select">{{ 'general.language' | t }}</label>
      <select id="language-select" name="locale_code">
        {% for language in localization.available_languages %}
          <option
            value="{{ language.iso_code }}"
            {% if language.iso_code == localization.language.iso_code %}selected{% endif %}
          >
            {{ language.endonym_name | capitalize }}
          </option>
        {% endfor %}
      </select>
    </div>
  {% endif %}

  {% if localization.available_countries.size > 1 %}
    <div class="country-selector">
      <label for="country-select">{{ 'general.country' | t }}</label>
      <select id="country-select" name="country_code">
        {% for country in localization.available_countries %}
          <option
            value="{{ country.iso_code }}"
            {% if country.iso_code == localization.country.iso_code %}selected{% endif %}
          >
            {{ country.name }} ({{ country.currency.iso_code }} {{ country.currency.symbol }})
          </option>
        {% endfor %}
      </select>
    </div>
  {% endif %}

  <button type="submit">{{ 'general.update' | t }}</button>
{% endform %}

{% comment %} Using translations {% endcomment %}
<h1>{{ 'products.product.add_to_cart' | t }}</h1>
<p>{{ 'products.product.quantity' | t: quantity: product.quantity }}</p>

{% comment %} Pluralization {% endcomment %}
{{ 'cart.items_count' | t: count: cart.item_count }}
```

---

## Performance Best Practices

### Lazy Loading Sections

```liquid
{% comment %} Defer non-critical sections {% endcomment %}
<div
  id="product-recommendations"
  data-url="{{ routes.product_recommendations_url }}?product_id={{ product.id }}&limit=4"
>
  {% comment %} Content loaded via JavaScript {% endcomment %}
</div>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('product-recommendations');
    if (container && 'IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            fetch(container.dataset.url)
              .then(response => response.text())
              .then(html => {
                container.innerHTML = html;
              });
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: '200px' });
      observer.observe(container);
    }
  });
</script>
```

### Avoiding Common Mistakes

```liquid
{% comment %} BAD: N+1 queries in loop {% endcomment %}
{% for product in collection.products %}
  {% assign designer = product.metafields.custom.designer.value %}
  {{ designer.name }} {%- comment -%} Each iteration queries metaobject {%- endcomment -%}
{% endfor %}

{% comment %} GOOD: Use includes with proper caching {% endcomment %}
{% for product in collection.products %}
  {% render 'product-card', product: product %}
{% endfor %}

{% comment %} BAD: Unnecessary assigns {% endcomment %}
{% assign title = product.title %}
{{ title }}

{% comment %} GOOD: Direct access {% endcomment %}
{{ product.title }}

{% comment %} BAD: String concatenation in loop {% endcomment %}
{% assign classes = '' %}
{% for tag in product.tags %}
  {% assign classes = classes | append: ' tag-' | append: tag | handleize %}
{% endfor %}

{% comment %} GOOD: Use capture {% endcomment %}
{% capture classes %}
  {% for tag in product.tags %} tag-{{ tag | handleize }}{% endfor %}
{% endcapture %}
```

---

## Related References

- **Storefront API** - For headless implementations
- **Performance Optimization** - Detailed performance patterns
- **Checkout Customization** - Post-purchase and checkout extensions

---

## Reference: Performance Optimization

# Performance Optimization

---

## When to Use

- Improving Shopify store speed scores
- Optimizing Core Web Vitals (LCP, FID, CLS)
- Reducing page load times
- Optimizing images and assets
- Implementing lazy loading strategies
- Analyzing and fixing performance bottlenecks

## When NOT to Use

- Checkout performance (mostly controlled by Shopify)
- Server-side API optimization (use Admin API best practices)
- Headless performance (use Hydrogen/framework-specific patterns)

---

## Performance Metrics Overview

### Target Benchmarks

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s - 4s | > 4s |
| FID (First Input Delay) | < 100ms | 100ms - 300ms | > 300ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| TTFB (Time to First Byte) | < 600ms | 600ms - 1800ms | > 1800ms |
| Speed Index | < 3.4s | 3.4s - 5.8s | > 5.8s |

### Measuring Performance

```bash
# Shopify Theme Inspector Chrome Extension
# Install from Chrome Web Store

# Lighthouse CI
npm install -g @lhci/cli
lhci autorun --collect.url=https://your-store.myshopify.com

# Web Vitals JavaScript
npm install web-vitals
```

```javascript
// Track Core Web Vitals
import { onCLS, onFID, onLCP, onTTFB, onINP } from 'web-vitals';

function sendToAnalytics({ name, delta, id }) {
  // Send to your analytics service
  gtag('event', name, {
    event_category: 'Web Vitals',
    event_label: id,
    value: Math.round(name === 'CLS' ? delta * 1000 : delta),
    non_interaction: true,
  });
}

onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
onTTFB(sendToAnalytics);
onINP(sendToAnalytics); // Replaces FID in 2024
```

---

## Image Optimization

### Responsive Images with Shopify CDN

```liquid
{% comment %} Modern responsive image pattern {% endcomment %}
{% liquid
  assign image = product.featured_image
  assign image_widths = '180, 360, 540, 720, 900, 1080, 1296, 1512, 1728, 1944, 2160'
%}

<img
  srcset="
    {%- for width in image_widths -%}
      {{ image | image_url: width: width }} {{ width }}w{% unless forloop.last %}, {% endunless %}
    {%- endfor -%}
  "
  sizes="(min-width: 1200px) 50vw, (min-width: 768px) 75vw, 100vw"
  src="{{ image | image_url: width: 720 }}"
  alt="{{ image.alt | escape }}"
  width="{{ image.width }}"
  height="{{ image.height }}"
  loading="lazy"
  decoding="async"
>

{% comment %} For hero/above-the-fold images - no lazy loading {% endcomment %}
<img
  srcset="{{ image | image_url: width: 1080 }} 1080w,
          {{ image | image_url: width: 1920 }} 1920w,
          {{ image | image_url: width: 2560 }} 2560w"
  sizes="100vw"
  src="{{ image | image_url: width: 1920 }}"
  alt="{{ image.alt | escape }}"
  width="{{ image.width }}"
  height="{{ image.height }}"
  loading="eager"
  fetchpriority="high"
  decoding="sync"
>
```

### Picture Element for Art Direction

```liquid
{% comment %} Different crops for mobile vs desktop {% endcomment %}
<picture>
  <source
    media="(max-width: 749px)"
    srcset="{{ section.settings.mobile_image | image_url: width: 750 }}"
  >
  <source
    media="(min-width: 750px)"
    srcset="{{ section.settings.desktop_image | image_url: width: 1500 }} 1x,
            {{ section.settings.desktop_image | image_url: width: 3000 }} 2x"
  >
  <img
    src="{{ section.settings.desktop_image | image_url: width: 1500 }}"
    alt="{{ section.settings.desktop_image.alt | escape }}"
    width="1500"
    height="600"
    loading="lazy"
  >
</picture>
```

### Background Images with CSS

```liquid
{% comment %} Background images should still use srcset pattern {% endcomment %}
{% style %}
  .hero-banner {
    background-image: url('{{ section.settings.image | image_url: width: 750 }}');
  }

  @media screen and (min-width: 750px) {
    .hero-banner {
      background-image: url('{{ section.settings.image | image_url: width: 1500 }}');
    }
  }

  @media screen and (min-width: 1200px) {
    .hero-banner {
      background-image: url('{{ section.settings.image | image_url: width: 2000 }}');
    }
  }
{% endstyle %}
```

---

## JavaScript Optimization

### Defer Non-Critical JavaScript

```liquid
{% comment %} layout/theme.liquid {% endcomment %}

{% comment %} Critical JS - loaded sync {% endcomment %}
<script src="{{ 'critical.js' | asset_url }}"></script>

{% comment %} Non-critical JS - deferred {% endcomment %}
<script src="{{ 'theme.js' | asset_url }}" defer></script>
<script src="{{ 'cart.js' | asset_url }}" defer></script>

{% comment %} Third-party scripts - load after page {% endcomment %}
<script>
  window.addEventListener('load', function() {
    // Load analytics, chat widgets, etc.
    var script = document.createElement('script');
    script.src = 'https://third-party.com/widget.js';
    script.async = true;
    document.body.appendChild(script);
  });
</script>
```

### Module Pattern for Code Splitting

```javascript
// assets/product.js
const ProductForm = {
  init() {
    const form = document.querySelector('[data-product-form]');
    if (!form) return;

    this.form = form;
    this.bindEvents();
  },

  bindEvents() {
    this.form.addEventListener('submit', this.handleSubmit.bind(this));
  },

  async handleSubmit(e) {
    e.preventDefault();

    // Lazy load cart functionality when needed
    const { Cart } = await import('./cart.js');
    Cart.add(new FormData(this.form));
  }
};

document.addEventListener('DOMContentLoaded', () => ProductForm.init());
```

### Intersection Observer for Lazy Loading

```javascript
// assets/lazy-load.js
const lazyLoad = {
  init() {
    if ('IntersectionObserver' in window) {
      this.observer = new IntersectionObserver(this.handleIntersect.bind(this), {
        rootMargin: '200px 0px', // Load 200px before viewport
        threshold: 0.01
      });

      document.querySelectorAll('[data-lazy]').forEach(el => {
        this.observer.observe(el);
      });
    } else {
      // Fallback for older browsers
      this.loadAll();
    }
  },

  handleIntersect(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        this.load(entry.target);
        this.observer.unobserve(entry.target);
      }
    });
  },

  load(element) {
    const type = element.dataset.lazy;

    switch (type) {
      case 'image':
        element.src = element.dataset.src;
        if (element.dataset.srcset) {
          element.srcset = element.dataset.srcset;
        }
        break;

      case 'section':
        this.loadSection(element);
        break;

      case 'video':
        element.src = element.dataset.src;
        break;
    }

    element.removeAttribute('data-lazy');
  },

  async loadSection(element) {
    const url = element.dataset.url;
    const response = await fetch(url);
    const html = await response.text();
    element.innerHTML = html;
  },

  loadAll() {
    document.querySelectorAll('[data-lazy]').forEach(el => this.load(el));
  }
};

document.addEventListener('DOMContentLoaded', () => lazyLoad.init());
```

---

## CSS Optimization

### Critical CSS Extraction

```liquid
{% comment %} layout/theme.liquid {% endcomment %}
<head>
  {% comment %} Inline critical CSS {% endcomment %}
  <style>
    {% render 'critical-css' %}
  </style>

  {% comment %} Preload full stylesheet {% endcomment %}
  <link rel="preload" href="{{ 'theme.css' | asset_url }}" as="style">

  {% comment %} Load full stylesheet with low priority {% endcomment %}
  <link
    rel="stylesheet"
    href="{{ 'theme.css' | asset_url }}"
    media="print"
    onload="this.media='all'"
  >
  <noscript>
    <link rel="stylesheet" href="{{ 'theme.css' | asset_url }}">
  </noscript>
</head>
```

```liquid
{% comment %} snippets/critical-css.liquid {% endcomment %}
/* Reset and base styles */
*,*::before,*::after{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,sans-serif;line-height:1.5}
img{max-width:100%;height:auto;display:block}

/* Header layout */
.header{position:sticky;top:0;z-index:100;background:#fff}
.header__wrapper{display:flex;align-items:center;justify-content:space-between;padding:1rem}

/* Hero section */
.hero{position:relative;min-height:50vh;display:flex;align-items:center}
.hero__content{max-width:600px;padding:2rem}

/* Product grid skeleton */
.product-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1rem}
.product-card{aspect-ratio:1}
```

### Prevent Layout Shift

```liquid
{% comment %} Always define dimensions {% endcomment %}
<img
  src="{{ image | image_url: width: 400 }}"
  width="{{ image.width }}"
  height="{{ image.height }}"
  alt="{{ image.alt | escape }}"
  loading="lazy"
>

{% comment %} Use aspect-ratio CSS {% endcomment %}
<style>
  .product-card__image {
    aspect-ratio: 1 / 1;
    object-fit: cover;
    width: 100%;
    height: auto;
  }

  .hero__image {
    aspect-ratio: 16 / 9;
    object-fit: cover;
  }
</style>

{% comment %} Reserve space for dynamic content {% endcomment %}
<div class="reviews-container" style="min-height: 200px;">
  {% comment %} Reviews loaded via JS {% endcomment %}
</div>
```

### Font Optimization

```liquid
{% comment %} layout/theme.liquid head section {% endcomment %}

{% comment %} Preconnect to font providers {% endcomment %}
<link rel="preconnect" href="https://fonts.shopifycdn.com" crossorigin>

{% comment %} Preload critical fonts {% endcomment %}
{% if settings.type_header_font.system? == false %}
  <link
    rel="preload"
    href="{{ settings.type_header_font | font_url }}"
    as="font"
    type="font/woff2"
    crossorigin
  >
{% endif %}

{% comment %} Use font-display: swap {% endcomment %}
<style>
  {{ settings.type_header_font | font_face: font_display: 'swap' }}
  {{ settings.type_body_font | font_face: font_display: 'swap' }}
</style>

{% comment %} System font stack fallback {% endcomment %}
<style>
  :root {
    --font-body: {{ settings.type_body_font.family }}, {{ settings.type_body_font.fallback_families }};
    --font-heading: {{ settings.type_header_font.family }}, {{ settings.type_header_font.fallback_families }};
  }

  body {
    font-family: var(--font-body);
  }

  h1, h2, h3 {
    font-family: var(--font-heading);
  }
</style>
```

---

## Resource Loading Strategy

### Preload Critical Resources

```liquid
{% comment %} layout/theme.liquid head {% endcomment %}

{% comment %} DNS prefetch for third-party domains {% endcomment %}
<link rel="dns-prefetch" href="https://cdn.shopify.com">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">

{% comment %} Preconnect for critical third-parties {% endcomment %}
<link rel="preconnect" href="https://cdn.shopify.com" crossorigin>

{% comment %} Preload hero image (above the fold) {% endcomment %}
{% if template == 'index' %}
  {% assign hero_image = sections['hero'].settings.image %}
  {% if hero_image %}
    <link
      rel="preload"
      as="image"
      href="{{ hero_image | image_url: width: 1500 }}"
      imagesrcset="{{ hero_image | image_url: width: 750 }} 750w,
                   {{ hero_image | image_url: width: 1500 }} 1500w,
                   {{ hero_image | image_url: width: 3000 }} 3000w"
      imagesizes="100vw"
    >
  {% endif %}
{% endif %}

{% comment %} Preload critical scripts {% endcomment %}
<link rel="modulepreload" href="{{ 'theme.js' | asset_url }}">
```

### Lazy Load Sections

```liquid
{% comment %} templates/index.json - defer below-the-fold sections {% endcomment %}

{% comment %} In section file {% endcomment %}
{% if section.index > 3 %}
  <div
    class="lazy-section"
    data-section-url="{{ section.id | prepend: '?section_id=' | prepend: request.path }}"
    data-lazy="section"
  >
    <div class="section-placeholder" style="min-height: 400px;">
      {% comment %} Loading skeleton {% endcomment %}
      <div class="skeleton-loader"></div>
    </div>
  </div>
{% else %}
  {% comment %} Render normally for above-the-fold {% endcomment %}
  {% render 'section-content' %}
{% endif %}
```

```javascript
// assets/lazy-sections.js
document.addEventListener('DOMContentLoaded', () => {
  const lazySections = document.querySelectorAll('[data-lazy="section"]');

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(async (entry) => {
        if (entry.isIntersecting) {
          const section = entry.target;
          const url = section.dataset.sectionUrl;

          try {
            const response = await fetch(url);
            const html = await response.text();
            section.innerHTML = html;
            section.removeAttribute('data-lazy');
          } catch (error) {
            console.error('Failed to load section:', error);
          }

          observer.unobserve(section);
        }
      });
    }, { rootMargin: '400px' });

    lazySections.forEach(section => observer.observe(section));
  }
});
```

---

## Caching Strategies

### Browser Cache Headers

```liquid
{% comment %} Shopify handles most caching automatically {% endcomment %}
{% comment %} For custom apps, set proper headers {% endcomment %}
```

```typescript
// For Hydrogen/custom storefronts
export async function loader({ context }: LoaderFunctionArgs) {
  const { storefront } = context;

  // Cache product data for 1 hour
  const products = await storefront.query(PRODUCTS_QUERY, {
    cache: storefront.CacheLong(), // ~1 hour
  });

  // Short cache for inventory
  const inventory = await storefront.query(INVENTORY_QUERY, {
    cache: storefront.CacheShort(), // ~1 minute
  });

  return json({ products, inventory }, {
    headers: {
      'Cache-Control': 'public, max-age=3600, stale-while-revalidate=86400',
    },
  });
}
```

### Local Storage Caching

```javascript
// assets/cache.js
const Cache = {
  prefix: 'shopify_',
  ttl: 5 * 60 * 1000, // 5 minutes

  set(key, value, customTtl) {
    const item = {
      value,
      expiry: Date.now() + (customTtl || this.ttl),
    };
    try {
      localStorage.setItem(this.prefix + key, JSON.stringify(item));
    } catch (e) {
      // Handle quota exceeded
      this.cleanup();
    }
  },

  get(key) {
    try {
      const item = JSON.parse(localStorage.getItem(this.prefix + key));
      if (!item) return null;
      if (Date.now() > item.expiry) {
        localStorage.removeItem(this.prefix + key);
        return null;
      }
      return item.value;
    } catch (e) {
      return null;
    }
  },

  cleanup() {
    const keys = Object.keys(localStorage).filter(k => k.startsWith(this.prefix));
    keys.forEach(key => {
      try {
        const item = JSON.parse(localStorage.getItem(key));
        if (Date.now() > item.expiry) {
          localStorage.removeItem(key);
        }
      } catch (e) {
        localStorage.removeItem(key);
      }
    });
  }
};

// Usage: Cache product recommendations
async function getRecommendations(productId) {
  const cacheKey = `recommendations_${productId}`;
  const cached = Cache.get(cacheKey);

  if (cached) return cached;

  const response = await fetch(`/recommendations/products.json?product_id=${productId}&limit=4`);
  const data = await response.json();

  Cache.set(cacheKey, data.products);
  return data.products;
}
```

---

## Third-Party Script Management

### Script Loading Strategy

```liquid
{% comment %} snippets/third-party-scripts.liquid {% endcomment %}

{% comment %} Load after user interaction {% endcomment %}
<script>
  (function() {
    var loaded = false;

    function loadScripts() {
      if (loaded) return;
      loaded = true;

      // Google Analytics
      var ga = document.createElement('script');
      ga.src = 'https://www.googletagmanager.com/gtag/js?id={{ settings.ga_id }}';
      ga.async = true;
      document.body.appendChild(ga);

      // Chat widget
      {% if settings.enable_chat %}
        var chat = document.createElement('script');
        chat.src = '{{ settings.chat_script_url }}';
        chat.async = true;
        document.body.appendChild(chat);
      {% endif %}

      // Reviews widget
      {% if settings.enable_reviews %}
        setTimeout(function() {
          var reviews = document.createElement('script');
          reviews.src = '{{ settings.reviews_script_url }}';
          reviews.async = true;
          document.body.appendChild(reviews);
        }, 2000); // Delay reviews by 2 seconds
      {% endif %}
    }

    // Load on user interaction
    ['mousedown', 'mousemove', 'touchstart', 'scroll', 'keydown'].forEach(function(event) {
      window.addEventListener(event, loadScripts, { once: true, passive: true });
    });

    // Fallback: load after 5 seconds
    setTimeout(loadScripts, 5000);
  })();
</script>
```

### Partytown for Third-Party Scripts

```html
<!-- Move third-party scripts to web worker -->
<script>
  partytown = {
    forward: ['dataLayer.push', 'fbq'],
  };
</script>
<script src="/~partytown/partytown.js"></script>

<!-- Scripts run in worker -->
<script type="text/partytown">
  // Google Analytics runs in web worker
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## Performance Checklist

### Pre-Launch Audit

```markdown
## Images
- [ ] All images use responsive srcset
- [ ] Above-fold images have fetchpriority="high"
- [ ] Below-fold images have loading="lazy"
- [ ] All images have width/height attributes
- [ ] WebP format used where supported

## JavaScript
- [ ] Non-critical JS is deferred
- [ ] Third-party scripts load on interaction
- [ ] No render-blocking scripts
- [ ] Code splitting for large modules
- [ ] Console errors resolved

## CSS
- [ ] Critical CSS inlined
- [ ] Non-critical CSS loaded async
- [ ] No unused CSS in critical path
- [ ] Font-display: swap for all fonts
- [ ] No layout shift from fonts

## Resources
- [ ] Preconnect to critical origins
- [ ] Preload critical assets
- [ ] DNS prefetch for third parties
- [ ] HTTP/2 server push configured

## Metrics
- [ ] LCP < 2.5s on mobile
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] Speed Index < 3.4s
- [ ] Total page weight < 2MB
```

---

## Related References

- **Liquid Templating** - For theme-level optimizations
- **Storefront API** - For headless performance patterns
- **Checkout Customization** - Checkout extension performance

---

## Reference: Storefront Api

# Storefront API

---

## When to Use

- Building headless storefronts with React, Next.js, or Hydrogen
- Creating custom checkout experiences
- Building mobile apps that connect to Shopify
- Implementing real-time inventory or pricing
- Creating PWAs with Shopify backend

## When NOT to Use

- Standard theme customization (use Liquid)
- Admin operations (use Admin API)
- Backend webhook processing (use Admin API)
- Simple product displays (Liquid is faster)

---

## API Fundamentals

### Authentication

```typescript
// Storefront API uses public access tokens (safe for client-side)
const STOREFRONT_ACCESS_TOKEN = 'your-storefront-access-token';
const SHOP_DOMAIN = 'your-store.myshopify.com';
const API_VERSION = '2024-10'; // Use latest stable version

// GraphQL endpoint
const endpoint = `https://${SHOP_DOMAIN}/api/${API_VERSION}/graphql.json`;

// Basic fetch wrapper
async function storefrontFetch<T>(query: string, variables?: Record<string, unknown>): Promise<T> {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Shopify-Storefront-Access-Token': STOREFRONT_ACCESS_TOKEN,
    },
    body: JSON.stringify({ query, variables }),
  });

  const json = await response.json();

  if (json.errors) {
    throw new Error(json.errors.map((e: { message: string }) => e.message).join(', '));
  }

  return json.data;
}
```

### Rate Limits

- **Buyer-facing**: 2000 cost points per second (shared across all clients)
- **Each query has a cost**: Simple queries ~1-10 points, complex ~50-100+
- **Check cost in response**:

```typescript
// Include cost in query
const query = `
  query Products @inContext(country: US, language: EN) {
    products(first: 10) {
      edges { node { id title } }
    }
  }
`;

// Response includes:
// "extensions": {
//   "cost": {
//     "requestedQueryCost": 12,
//     "actualQueryCost": 12,
//     "throttleStatus": {
//       "maximumAvailable": 2000,
//       "currentlyAvailable": 1988,
//       "restoreRate": 100
//     }
//   }
// }
```

---

## Hydrogen 2024 (Remix-based)

### Project Setup

```bash
# Create new Hydrogen project
npm create @shopify/hydrogen@latest -- --template demo-store

# Project structure
hydrogen-storefront/
├── app/
│   ├── components/      # React components
│   ├── lib/             # Utilities, fragments
│   ├── routes/          # Remix routes
│   └── styles/          # CSS
├── public/              # Static assets
├── server.ts            # Entry point
└── hydrogen.config.ts   # Hydrogen config
```

### Hydrogen Configuration

```typescript
// hydrogen.config.ts
import {defineConfig} from '@shopify/hydrogen/config';

export default defineConfig({
  shopify: {
    storeDomain: 'your-store.myshopify.com',
    storefrontToken: process.env.PUBLIC_STOREFRONT_API_TOKEN!,
    storefrontApiVersion: '2024-10',
  },
  session: {
    storage: 'cookie', // or 'memory' for development
  },
});
```

### Route with Data Loading

```typescript
// app/routes/products.$handle.tsx
import {useLoaderData, type MetaFunction} from '@remix-run/react';
import {json, type LoaderFunctionArgs} from '@shopify/remix-oxygen';
import {
  Image,
  Money,
  VariantSelector,
  getSelectedProductOptions,
} from '@shopify/hydrogen';
import type {ProductQuery} from 'storefrontapi.generated';

export const meta: MetaFunction<typeof loader> = ({data}) => {
  return [{title: data?.product?.title ?? 'Product'}];
};

export async function loader({params, request, context}: LoaderFunctionArgs) {
  const {handle} = params;
  const {storefront} = context;

  const selectedOptions = getSelectedProductOptions(request);

  const {product} = await storefront.query<ProductQuery>(PRODUCT_QUERY, {
    variables: {
      handle,
      selectedOptions,
      country: context.storefront.i18n.country,
      language: context.storefront.i18n.language,
    },
  });

  if (!product?.id) {
    throw new Response('Product not found', {status: 404});
  }

  return json({product});
}

export default function Product() {
  const {product} = useLoaderData<typeof loader>();
  const {title, descriptionHtml, featuredImage, variants} = product;

  return (
    <div className="product-page">
      <div className="product-image">
        {featuredImage && (
          <Image
            data={featuredImage}
            sizes="(min-width: 768px) 50vw, 100vw"
            aspectRatio="1/1"
          />
        )}
      </div>

      <div className="product-info">
        <h1>{title}</h1>

        <VariantSelector
          handle={product.handle}
          options={product.options}
          variants={variants}
        >
          {({option}) => (
            <div key={option.name} className="option-group">
              <h3>{option.name}</h3>
              <div className="option-values">
                {option.values.map(({value, isAvailable, to}) => (
                  <a
                    key={value}
                    href={to}
                    className={`option-value ${!isAvailable ? 'unavailable' : ''}`}
                  >
                    {value}
                  </a>
                ))}
              </div>
            </div>
          )}
        </VariantSelector>

        <ProductPrice selectedVariant={product.selectedVariant} />

        <AddToCartButton
          lines={[
            {
              merchandiseId: product.selectedVariant?.id,
              quantity: 1,
            },
          ]}
          disabled={!product.selectedVariant?.availableForSale}
        />

        <div
          className="product-description"
          dangerouslySetInnerHTML={{__html: descriptionHtml}}
        />
      </div>
    </div>
  );
}

const PRODUCT_QUERY = `#graphql
  query Product(
    $handle: String!
    $selectedOptions: [SelectedOptionInput!]!
    $country: CountryCode
    $language: LanguageCode
  ) @inContext(country: $country, language: $language) {
    product(handle: $handle) {
      id
      title
      handle
      descriptionHtml
      featuredImage {
        url
        altText
        width
        height
      }
      options {
        name
        values
      }
      selectedVariant: variantBySelectedOptions(selectedOptions: $selectedOptions) {
        id
        availableForSale
        price {
          amount
          currencyCode
        }
        compareAtPrice {
          amount
          currencyCode
        }
        selectedOptions {
          name
          value
        }
      }
      variants(first: 100) {
        nodes {
          id
          availableForSale
          selectedOptions {
            name
            value
          }
        }
      }
    }
  }
`;
```

---

## Core GraphQL Patterns

### Products Query with Pagination

```graphql
query Products(
  $first: Int!
  $after: String
  $query: String
  $sortKey: ProductSortKeys
  $reverse: Boolean
  $country: CountryCode
  $language: LanguageCode
) @inContext(country: $country, language: $language) {
  products(
    first: $first
    after: $after
    query: $query
    sortKey: $sortKey
    reverse: $reverse
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        handle
        title
        description
        priceRange {
          minVariantPrice {
            amount
            currencyCode
          }
          maxVariantPrice {
            amount
            currencyCode
          }
        }
        featuredImage {
          url(transform: { maxWidth: 400, maxHeight: 400 })
          altText
        }
        variants(first: 1) {
          nodes {
            id
            availableForSale
          }
        }
      }
    }
  }
}
```

### Collection with Filters

```graphql
query Collection(
  $handle: String!
  $first: Int!
  $after: String
  $filters: [ProductFilter!]
  $sortKey: ProductCollectionSortKeys
  $reverse: Boolean
  $country: CountryCode
  $language: LanguageCode
) @inContext(country: $country, language: $language) {
  collection(handle: $handle) {
    id
    title
    description
    image {
      url
      altText
    }
    products(
      first: $first
      after: $after
      filters: $filters
      sortKey: $sortKey
      reverse: $reverse
    ) {
      filters {
        id
        label
        type
        values {
          id
          label
          count
          input
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        ...ProductCard
      }
    }
  }
}

fragment ProductCard on Product {
  id
  handle
  title
  featuredImage {
    url(transform: { maxWidth: 300 })
    altText
  }
  priceRange {
    minVariantPrice {
      amount
      currencyCode
    }
  }
  variants(first: 1) {
    nodes {
      availableForSale
    }
  }
}
```

### Cart Operations

```typescript
// Create cart
const CREATE_CART = `#graphql
  mutation CartCreate($input: CartInput!, $country: CountryCode, $language: LanguageCode)
  @inContext(country: $country, language: $language) {
    cartCreate(input: $input) {
      cart {
        ...CartFragment
      }
      userErrors {
        field
        message
      }
    }
  }
`;

// Add to cart
const ADD_TO_CART = `#graphql
  mutation CartLinesAdd($cartId: ID!, $lines: [CartLineInput!]!, $country: CountryCode, $language: LanguageCode)
  @inContext(country: $country, language: $language) {
    cartLinesAdd(cartId: $cartId, lines: $lines) {
      cart {
        ...CartFragment
      }
      userErrors {
        field
        message
      }
    }
  }
`;

// Update cart line
const UPDATE_CART_LINES = `#graphql
  mutation CartLinesUpdate($cartId: ID!, $lines: [CartLineUpdateInput!]!, $country: CountryCode, $language: LanguageCode)
  @inContext(country: $country, language: $language) {
    cartLinesUpdate(cartId: $cartId, lines: $lines) {
      cart {
        ...CartFragment
      }
      userErrors {
        field
        message
      }
    }
  }
`;

// Remove from cart
const REMOVE_FROM_CART = `#graphql
  mutation CartLinesRemove($cartId: ID!, $lineIds: [ID!]!, $country: CountryCode, $language: LanguageCode)
  @inContext(country: $country, language: $language) {
    cartLinesRemove(cartId: $cartId, lineIds: $lineIds) {
      cart {
        ...CartFragment
      }
      userErrors {
        field
        message
      }
    }
  }
`;

// Cart fragment for consistent data
const CART_FRAGMENT = `#graphql
  fragment CartFragment on Cart {
    id
    checkoutUrl
    totalQuantity
    cost {
      subtotalAmount {
        amount
        currencyCode
      }
      totalAmount {
        amount
        currencyCode
      }
      totalTaxAmount {
        amount
        currencyCode
      }
    }
    lines(first: 100) {
      nodes {
        id
        quantity
        cost {
          totalAmount {
            amount
            currencyCode
          }
        }
        merchandise {
          ... on ProductVariant {
            id
            title
            image {
              url(transform: { maxWidth: 100 })
              altText
            }
            product {
              title
              handle
            }
            price {
              amount
              currencyCode
            }
          }
        }
        attributes {
          key
          value
        }
      }
    }
    discountCodes {
      code
      applicable
    }
  }
`;
```

---

## Customer Authentication

### Customer Account API (2024+)

```typescript
// New Customer Account API for headless auth
const CUSTOMER_LOGIN = `#graphql
  mutation CustomerAccessTokenCreate($input: CustomerAccessTokenCreateInput!) {
    customerAccessTokenCreate(input: $input) {
      customerAccessToken {
        accessToken
        expiresAt
      }
      customerUserErrors {
        code
        field
        message
      }
    }
  }
`;

// Get customer with token
const GET_CUSTOMER = `#graphql
  query Customer($customerAccessToken: String!) {
    customer(customerAccessToken: $customerAccessToken) {
      id
      firstName
      lastName
      email
      phone
      acceptsMarketing
      defaultAddress {
        ...AddressFragment
      }
      addresses(first: 10) {
        nodes {
          ...AddressFragment
        }
      }
      orders(first: 10, sortKey: PROCESSED_AT, reverse: true) {
        nodes {
          id
          orderNumber
          processedAt
          financialStatus
          fulfillmentStatus
          totalPrice {
            amount
            currencyCode
          }
          lineItems(first: 5) {
            nodes {
              title
              quantity
              variant {
                image {
                  url(transform: { maxWidth: 100 })
                }
              }
            }
          }
        }
      }
    }
  }

  fragment AddressFragment on MailingAddress {
    id
    address1
    address2
    city
    province
    country
    zip
    phone
  }
`;

// Customer registration
const CUSTOMER_CREATE = `#graphql
  mutation CustomerCreate($input: CustomerCreateInput!) {
    customerCreate(input: $input) {
      customer {
        id
        email
        firstName
        lastName
      }
      customerUserErrors {
        code
        field
        message
      }
    }
  }
`;
```

---

## Internationalization

### Market-Aware Queries

```typescript
// Always use @inContext directive for localization
const LOCALIZED_PRODUCTS = `#graphql
  query Products($country: CountryCode!, $language: LanguageCode!)
  @inContext(country: $country, language: $language) {
    products(first: 10) {
      nodes {
        title  # Returns translated title
        priceRange {
          minVariantPrice {
            amount      # Returns price in local currency
            currencyCode
          }
        }
      }
    }
  }
`;

// Get available markets
const GET_LOCALIZATION = `#graphql
  query Localization {
    localization {
      availableCountries {
        isoCode
        name
        currency {
          isoCode
          name
          symbol
        }
        availableLanguages {
          isoCode
          name
        }
      }
      country {
        isoCode
        name
        currency {
          isoCode
          symbol
        }
      }
      language {
        isoCode
        name
      }
    }
  }
`;
```

### Hydrogen Localization

```typescript
// app/routes/($locale).products._index.tsx
import {type LoaderFunctionArgs} from '@shopify/remix-oxygen';

export async function loader({params, context}: LoaderFunctionArgs) {
  const {locale} = params;
  const {storefront} = context;

  // Storefront client automatically handles locale from route
  const {products} = await storefront.query(PRODUCTS_QUERY, {
    variables: {
      country: storefront.i18n.country,
      language: storefront.i18n.language,
    },
  });

  return json({products});
}

// server.ts - Configure i18n
const i18n = {
  default: {language: 'EN', country: 'US'},
  subfolders: [
    {language: 'FR', country: 'FR', pathPrefix: '/fr-fr'},
    {language: 'DE', country: 'DE', pathPrefix: '/de-de'},
    {language: 'EN', country: 'GB', pathPrefix: '/en-gb'},
  ],
};
```

---

## Search and Predictive Search

```graphql
# Full search
query Search($query: String!, $first: Int!, $types: [SearchType!]) {
  search(query: $query, first: $first, types: $types) {
    totalCount
    nodes {
      ... on Product {
        __typename
        id
        handle
        title
        featuredImage {
          url(transform: { maxWidth: 200 })
        }
        priceRange {
          minVariantPrice {
            amount
            currencyCode
          }
        }
      }
      ... on Article {
        __typename
        id
        handle
        title
        blog {
          handle
        }
      }
      ... on Page {
        __typename
        id
        handle
        title
      }
    }
  }
}

# Predictive search (faster, for autocomplete)
query PredictiveSearch($query: String!, $limit: Int!) {
  predictiveSearch(query: $query, limit: $limit, limitScope: EACH) {
    products {
      id
      handle
      title
      featuredImage {
        url(transform: { maxWidth: 100 })
      }
      priceRange {
        minVariantPrice {
          amount
          currencyCode
        }
      }
    }
    collections {
      id
      handle
      title
    }
    queries {
      text
      styledText
    }
  }
}
```

---

## Performance Optimization

### Query Best Practices

```typescript
// BAD: Over-fetching
const BAD_QUERY = `#graphql
  query Product($handle: String!) {
    product(handle: $handle) {
      id
      title
      description
      descriptionHtml
      vendor
      productType
      tags
      # Fetching ALL variants when you only need first
      variants(first: 250) {
        nodes {
          id
          title
          price { amount currencyCode }
          compareAtPrice { amount currencyCode }
          image { url altText width height }
          selectedOptions { name value }
          sku
          barcode
          weight
          weightUnit
        }
      }
      # Fetching ALL images
      images(first: 250) {
        nodes {
          url
          altText
          width
          height
        }
      }
    }
  }
`;

// GOOD: Fetch only what you need
const GOOD_QUERY = `#graphql
  query Product($handle: String!) {
    product(handle: $handle) {
      id
      title
      descriptionHtml
      featuredImage {
        url(transform: { maxWidth: 800 })
        altText
      }
      # Only fetch what's visible
      variants(first: 10) {
        nodes {
          id
          availableForSale
          price { amount currencyCode }
          selectedOptions { name value }
        }
      }
    }
  }
`;

// Use fragments for reusability and consistency
const PRODUCT_CARD_FRAGMENT = `#graphql
  fragment ProductCard on Product {
    id
    handle
    title
    featuredImage {
      url(transform: { maxWidth: 300, maxHeight: 300 })
      altText
    }
    priceRange {
      minVariantPrice {
        amount
        currencyCode
      }
    }
    variants(first: 1) {
      nodes {
        availableForSale
      }
    }
  }
`;
```

### Caching Strategies

```typescript
// Hydrogen caching
export async function loader({context}: LoaderFunctionArgs) {
  const {storefront} = context;

  // Short cache for frequently changing data
  const {products} = await storefront.query(PRODUCTS_QUERY, {
    cache: storefront.CacheShort(), // ~1 minute
  });

  // Long cache for static content
  const {menu} = await storefront.query(MENU_QUERY, {
    cache: storefront.CacheLong(), // ~1 hour
  });

  // No cache for user-specific data
  const {customer} = await storefront.query(CUSTOMER_QUERY, {
    cache: storefront.CacheNone(),
  });

  return json({products, menu, customer});
}
```

---

## Related References

- **Liquid Templating** - For theme-based implementations
- **App Development** - For Admin API and backend integration
- **Checkout Customization** - For checkout extensions with Storefront API
- **Performance Optimization** - Detailed performance patterns
