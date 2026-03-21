---
title: "Shopify Development"
description: "Build Shopify apps, extensions, themes using GraphQL Admin API, Shopify CLI, Polaris UI, and Liquid."
category: "development"
source: "community"
author: "Community"
tags: ["shopify", "development"]
date: 2026-03-20
---

# Shopify Development Skill

Use this skill when the user asks about:

- Building Shopify apps or extensions
- Creating checkout/admin/POS UI customizations
- Developing themes with Liquid templating
- Integrating with Shopify GraphQL or REST APIs
- Implementing webhooks or billing
- Working with metafields or Shopify Functions

---

## ROUTING: What to Build

**IF user wants to integrate external services OR build merchant tools OR charge for features:**
→ Build an **App** (see `references/app-development.md`)

**IF user wants to customize checkout OR add admin UI OR create POS actions OR implement discount rules:**
→ Build an **Extension** (see `references/extensions.md`)

**IF user wants to customize storefront design OR modify product/collection pages:**
→ Build a **Theme** (see `references/themes.md`)

**IF user needs both backend logic AND storefront UI:**
→ Build **App + Theme Extension** combination

---

## Shopify CLI Commands

Install CLI:

```bash
npm install -g @shopify/cli@latest
```

Create and run app:

```bash
shopify app init          # Create new app
shopify app dev           # Start dev server with tunnel
shopify app deploy        # Build and upload to Shopify
```

Generate extension:

```bash
shopify app generate extension --type checkout_ui_extension
shopify app generate extension --type admin_action
shopify app generate extension --type admin_block
shopify app generate extension --type pos_ui_extension
shopify app generate extension --type function
```

Theme development:

```bash
shopify theme init        # Create new theme
shopify theme dev         # Start local preview at localhost:9292
shopify theme pull --live # Pull live theme
shopify theme push --development  # Push to dev theme
```

---

## Access Scopes

Configure in `shopify.app.toml`:

```toml
[access_scopes]
scopes = "read_products,write_products,read_orders,write_orders,read_customers"
```

Common scopes:

- `read_products`, `write_products` - Product catalog access
- `read_orders`, `write_orders` - Order management
- `read_customers`, `write_customers` - Customer data
- `read_inventory`, `write_inventory` - Stock levels
- `read_fulfillments`, `write_fulfillments` - Order fulfillment

---

## GraphQL Patterns (Validated against API 2026-01)

### Query Products

```graphql
query GetProducts($first: Int!, $query: String) {
  products(first: $first, query: $query) {
    edges {
      node {
        id
        title
        handle
        status
        variants(first: 5) {
          edges {
            node {
              id
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Query Orders

```graphql
query GetOrders($first: Int!) {
  orders(first: $first) {
    edges {
      node {
        id
        name
        createdAt
        displayFinancialStatus
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
      }
    }
  }
}
```

### Set Metafields

```graphql
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables example:

```json
{
  "metafields": [
    {
      "ownerId": "gid://shopify/Product/123",
      "namespace": "custom",
      "key": "care_instructions",
      "value": "Handle with care",
      "type": "single_line_text_field"
    }
  ]
}
```

---

## Checkout Extension Example

```tsx
import {
  reactExtension,
  BlockStack,
  TextField,
  Checkbox,
  useApplyAttributeChange,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => (
  <GiftMessage />
));

function GiftMessage() {
  const [isGift, setIsGift] = useState(false);
  const [message, setMessage] = useState("");
  const applyAttributeChange = useApplyAttributeChange();

  useEffect(() => {
    if (isGift && message) {
      applyAttributeChange({
        type: "updateAttribute",
        key: "gift_message",
        value: message,
      });
    }
  }, [isGift, message]);

  return (
    <BlockStack spacing="loose">
      <Checkbox checked={isGift} onChange={setIsGift}>
        This is a gift
      </Checkbox>
      {isGift && (
        <TextField
          label="Gift Message"
          value={message}
          onChange={setMessage}
          multiline={3}
        />
      )}
    </BlockStack>
  );
}
```

---

## Liquid Template Example

```liquid
{% comment %} Product Card Snippet {% endcomment %}
<div class="product-card">
  <a href="{{ product.url }}">
    {% if product.featured_image %}
      <img
        src="{{ product.featured_image | img_url: 'medium' }}"
        alt="{{ product.title | escape }}"
        loading="lazy"
      >
    {% endif %}
    <h3>{{ product.title }}</h3>
    <p class="price">{{ product.price | money }}</p>
    {% if product.compare_at_price > product.price %}
      <p class="sale-badge">Sale</p>
    {% endif %}
  </a>
</div>
```

---

## Webhook Configuration

In `shopify.app.toml`:

```toml
[webhooks]
api_version = "2026-01"

[[webhooks.subscriptions]]
topics = ["orders/create", "orders/updated"]
uri = "/webhooks/orders"

[[webhooks.subscriptions]]
topics = ["products/update"]
uri = "/webhooks/products"

# GDPR mandatory webhooks (required for app approval)
[webhooks.privacy_compliance]
customer_data_request_url = "/webhooks/gdpr/data-request"
customer_deletion_url = "/webhooks/gdpr/customer-deletion"
shop_deletion_url = "/webhooks/gdpr/shop-deletion"
```

---

## Best Practices

### API Usage

- Use GraphQL over REST for new development
- Request only fields you need (reduces query cost)
- Implement cursor-based pagination with `pageInfo.endCursor`
- Use bulk operations for processing more than 250 items
- Handle rate limits with exponential backoff

### Security

- Store API credentials in environment variables
- Always verify webhook HMAC signatures before processing
- Validate OAuth state parameter to prevent CSRF
- Request minimal access scopes
- Use session tokens for embedded apps

### Performance

- Cache API responses when data doesn't change frequently
- Use lazy loading in extensions
- Optimize images in themes using `img_url` filter
- Monitor GraphQL query costs via response headers

---

## Troubleshooting

**IF you see rate limit errors:**
→ Implement exponential backoff retry logic
→ Switch to bulk operations for large datasets
→ Monitor `X-Shopify-Shop-Api-Call-Limit` header

**IF authentication fails:**
→ Verify the access token is still valid
→ Check that all required scopes were granted
→ Ensure OAuth flow completed successfully

**IF extension is not appearing:**
→ Verify the extension target is correct
→ Check that extension is published via `shopify app deploy`
→ Confirm the app is installed on the test store

**IF webhook is not receiving events:**
→ Verify the webhook URL is publicly accessible
→ Check HMAC signature validation logic
→ Review webhook logs in Partner Dashboard

**IF GraphQL query fails:**
→ Validate query against schema (use GraphiQL explorer)
→ Check for deprecated fields in error message
→ Verify you have required access scopes

---

## Reference Files

For detailed implementation guides, read these files:

- `references/app-development.md` - OAuth authentication flow, GraphQL mutations for products/orders/billing, webhook handlers, billing API integration
- `references/extensions.md` - Checkout UI components, Admin UI extensions, POS extensions, Shopify Functions for discounts/payment/delivery
- `references/themes.md` - Liquid syntax reference, theme directory structure, sections and snippets, common patterns

---

## Scripts

- `scripts/shopify_init.py` - Interactive project scaffolding. Run: `python scripts/shopify_init.py`
- `scripts/shopify_graphql.py` - GraphQL utilities with query templates, pagination, rate limiting. Import: `from shopify_graphql import ShopifyGraphQL`

---

## Official Documentation Links

- Shopify Developer Docs: https://shopify.dev/docs
- GraphQL Admin API Reference: https://shopify.dev/docs/api/admin-graphql
- Shopify CLI Reference: https://shopify.dev/docs/api/shopify-cli
- Polaris Design System: https://polaris.shopify.com

API Version: 2026-01 (quarterly releases, 12-month deprecation window)

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: App Development

# App Development Reference

Guide for building Shopify apps with OAuth, GraphQL/REST APIs, webhooks, and billing.

## OAuth Authentication

### OAuth 2.0 Flow

**1. Redirect to Authorization URL:**

```
https://{shop}.myshopify.com/admin/oauth/authorize?
  client_id={api_key}&
  scope={scopes}&
  redirect_uri={redirect_uri}&
  state={nonce}
```

**2. Handle Callback:**

```javascript
app.get("/auth/callback", async (req, res) => {
  const { code, shop, state } = req.query;

  // Verify state to prevent CSRF
  if (state !== storedState) {
    return res.status(403).send("Invalid state");
  }

  // Exchange code for access token
  const accessToken = await exchangeCodeForToken(shop, code);

  // Store token securely
  await storeAccessToken(shop, accessToken);

  res.redirect(`https://${shop}/admin/apps/${appHandle}`);
});
```

**3. Exchange Code for Token:**

```javascript
async function exchangeCodeForToken(shop, code) {
  const response = await fetch(`https://${shop}/admin/oauth/access_token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      client_id: process.env.SHOPIFY_API_KEY,
      client_secret: process.env.SHOPIFY_API_SECRET,
      code,
    }),
  });

  const { access_token } = await response.json();
  return access_token;
}
```

### Access Scopes

**Common Scopes:**

- `read_products`, `write_products` - Product catalog
- `read_orders`, `write_orders` - Order management
- `read_customers`, `write_customers` - Customer data
- `read_inventory`, `write_inventory` - Stock levels
- `read_fulfillments`, `write_fulfillments` - Order fulfillment
- `read_shipping`, `write_shipping` - Shipping rates
- `read_analytics` - Store analytics
- `read_checkouts`, `write_checkouts` - Checkout data

Full list: https://shopify.dev/api/usage/access-scopes

### Session Tokens (Embedded Apps)

For embedded apps using App Bridge:

```javascript
import { getSessionToken } from '@shopify/app-bridge/utilities';

async function authenticatedFetch(url, options = {}) {
  const app = createApp({ ... });
  const token = await getSessionToken(app);

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    }
  });
}
```

## GraphQL Admin API

### Making Requests

```javascript
async function graphqlRequest(shop, accessToken, query, variables = {}) {
  const response = await fetch(
    `https://${shop}/admin/api/2026-01/graphql.json`,
    {
      method: "POST",
      headers: {
        "X-Shopify-Access-Token": accessToken,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query, variables }),
    },
  );

  const data = await response.json();

  if (data.errors) {
    throw new Error(`GraphQL errors: ${JSON.stringify(data.errors)}`);
  }

  return data.data;
}
```

### Product Operations

**Create Product:**

```graphql
mutation CreateProduct($input: ProductInput!) {
  productCreate(input: $input) {
    product {
      id
      title
      handle
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "input": {
    "title": "New Product",
    "productType": "Apparel",
    "vendor": "Brand",
    "status": "ACTIVE",
    "variants": [
      { "price": "29.99", "sku": "SKU-001", "inventoryQuantity": 100 }
    ]
  }
}
```

**Update Product:**

```graphql
mutation UpdateProduct($input: ProductInput!) {
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
```

**Query Products:**

```graphql
query GetProducts($first: Int!, $query: String) {
  products(first: $first, query: $query) {
    edges {
      node {
        id
        title
        status
        variants(first: 5) {
          edges {
            node {
              id
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Order Operations

**Query Orders:**

```graphql
query GetOrders($first: Int!) {
  orders(first: $first) {
    edges {
      node {
        id
        name
        createdAt
        displayFinancialStatus
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        customer {
          email
          firstName
          lastName
        }
      }
    }
  }
}
```

**Fulfill Order:**

```graphql
mutation FulfillOrder($fulfillment: FulfillmentInput!) {
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
```

## Webhooks

### Configuration

In `shopify.app.toml`:

```toml
[webhooks]
api_version = "2025-01"

[[webhooks.subscriptions]]
topics = ["orders/create"]
uri = "/webhooks/orders/create"

[[webhooks.subscriptions]]
topics = ["products/update"]
uri = "/webhooks/products/update"

[[webhooks.subscriptions]]
topics = ["app/uninstalled"]
uri = "/webhooks/app/uninstalled"

# GDPR mandatory webhooks
[webhooks.privacy_compliance]
customer_data_request_url = "/webhooks/gdpr/data-request"
customer_deletion_url = "/webhooks/gdpr/customer-deletion"
shop_deletion_url = "/webhooks/gdpr/shop-deletion"
```

### Webhook Handler

```javascript
import crypto from "crypto";

function verifyWebhook(req) {
  const hmac = req.headers["x-shopify-hmac-sha256"];
  const body = req.rawBody; // Raw body buffer

  const hash = crypto
    .createHmac("sha256", process.env.SHOPIFY_API_SECRET)
    .update(body, "utf8")
    .digest("base64");

  return hmac === hash;
}

app.post("/webhooks/orders/create", async (req, res) => {
  if (!verifyWebhook(req)) {
    return res.status(401).send("Unauthorized");
  }

  const order = req.body;
  console.log("New order:", order.id, order.name);

  // Process order...

  res.status(200).send("OK");
});
```

### Common Webhook Topics

**Orders:**

- `orders/create`, `orders/updated`, `orders/delete`
- `orders/paid`, `orders/cancelled`, `orders/fulfilled`

**Products:**

- `products/create`, `products/update`, `products/delete`

**Customers:**

- `customers/create`, `customers/update`, `customers/delete`

**Inventory:**

- `inventory_levels/update`

**App:**

- `app/uninstalled` (critical for cleanup)

## Billing Integration

### App Charges

**One-time Charge:**

```graphql
mutation CreateCharge($input: AppPurchaseOneTimeInput!) {
  appPurchaseOneTimeCreate(input: $input) {
    appPurchaseOneTime {
      id
      name
      price {
        amount
      }
      status
      confirmationUrl
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "input": {
    "name": "Premium Feature",
    "price": { "amount": 49.99, "currencyCode": "USD" },
    "returnUrl": "https://your-app.com/billing/callback"
  }
}
```

**Recurring Charge (Subscription):**

```graphql
mutation CreateSubscription(
  $name: String!
  $returnUrl: URL!
  $lineItems: [AppSubscriptionLineItemInput!]!
  $trialDays: Int
) {
  appSubscriptionCreate(
    name: $name
    returnUrl: $returnUrl
    lineItems: $lineItems
    trialDays: $trialDays
  ) {
    appSubscription {
      id
      name
      status
    }
    confirmationUrl
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "name": "Monthly Subscription",
  "returnUrl": "https://your-app.com/billing/callback",
  "trialDays": 7,
  "lineItems": [
    {
      "plan": {
        "appRecurringPricingDetails": {
          "price": { "amount": 29.99, "currencyCode": "USD" },
          "interval": "EVERY_30_DAYS"
        }
      }
    }
  ]
}
```

**Usage-based Billing:**

```graphql
mutation CreateUsageCharge(
  $subscriptionLineItemId: ID!
  $price: MoneyInput!
  $description: String!
) {
  appUsageRecordCreate(
    subscriptionLineItemId: $subscriptionLineItemId
    price: $price
    description: $description
  ) {
    appUsageRecord {
      id
      price {
        amount
        currencyCode
      }
      description
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "subscriptionLineItemId": "gid://shopify/AppSubscriptionLineItem/123",
  "price": { "amount": "5.00", "currencyCode": "USD" },
  "description": "100 API calls used"
}
```

## Metafields

### Create/Update Metafields

```graphql
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "metafields": [
    {
      "ownerId": "gid://shopify/Product/123",
      "namespace": "custom",
      "key": "instructions",
      "value": "Handle with care",
      "type": "single_line_text_field"
    }
  ]
}
```

**Metafield Types:**

- `single_line_text_field`, `multi_line_text_field`
- `number_integer`, `number_decimal`
- `date`, `date_time`
- `url`, `json`
- `file_reference`, `product_reference`

## Rate Limiting

### GraphQL Cost-Based Limits

**Limits:**

- Available points: 2000
- Restore rate: 100 points/second
- Max query cost: 2000

**Check Cost:**

```javascript
const response = await graphqlRequest(shop, token, query);
const cost = response.extensions?.cost;

console.log(
  `Cost: ${cost.actualQueryCost}/${cost.throttleStatus.maximumAvailable}`,
);
```

**Handle Throttling:**

```javascript
async function graphqlWithRetry(shop, token, query, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await graphqlRequest(shop, token, query);
    } catch (error) {
      if (error.message.includes("Throttled") && i < retries - 1) {
        await sleep(Math.pow(2, i) * 1000); // Exponential backoff
        continue;
      }
      throw error;
    }
  }
}
```

## Best Practices

**Security:**

- Store credentials in environment variables
- Verify webhook HMAC signatures
- Validate OAuth state parameter
- Use HTTPS for all endpoints
- Implement rate limiting on your endpoints

**Performance:**

- Cache access tokens securely
- Use bulk operations for large datasets
- Implement pagination for queries
- Monitor GraphQL query costs

**Reliability:**

- Implement exponential backoff for retries
- Handle webhook delivery failures
- Log errors for debugging
- Monitor app health metrics

**Compliance:**

- Implement GDPR webhooks (mandatory)
- Handle customer data deletion requests
- Provide data export functionality
- Follow data retention policies

---

## Reference: Extensions

# Extensions Reference

Guide for building UI extensions and Shopify Functions.

## Checkout UI Extensions

Customize checkout and thank-you pages with native-rendered components.

### Extension Points

**Block Targets (Merchant-Configurable):**

- `purchase.checkout.block.render` - Main checkout
- `purchase.thank-you.block.render` - Thank you page

**Static Targets (Fixed Position):**

- `purchase.checkout.header.render-after`
- `purchase.checkout.contact.render-before`
- `purchase.checkout.shipping-option-list.render-after`
- `purchase.checkout.payment-method-list.render-after`
- `purchase.checkout.footer.render-before`

### Setup

```bash
shopify app generate extension --type checkout_ui_extension
```

Configuration (`shopify.extension.toml`):

```toml
api_version = "2026-01"
name = "gift-message"
type = "ui_extension"

[[extensions.targeting]]
target = "purchase.checkout.block.render"

[capabilities]
network_access = true
api_access = true
```

### Basic Example

```javascript
import {
  reactExtension,
  BlockStack,
  TextField,
  Checkbox,
  useApi,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => (
  <Extension />
));

function Extension() {
  const [message, setMessage] = useState("");
  const [isGift, setIsGift] = useState(false);
  const { applyAttributeChange } = useApi();

  useEffect(() => {
    if (isGift) {
      applyAttributeChange({
        type: "updateAttribute",
        key: "gift_message",
        value: message,
      });
    }
  }, [message, isGift]);

  return (
    <BlockStack spacing="loose">
      <Checkbox checked={isGift} onChange={setIsGift}>
        This is a gift
      </Checkbox>
      {isGift && (
        <TextField
          label="Gift Message"
          value={message}
          onChange={setMessage}
          multiline={3}
        />
      )}
    </BlockStack>
  );
}
```

### Common Hooks

**useApi:**

```javascript
const { extensionPoint, shop, storefront, i18n, sessionToken } = useApi();
```

**useCartLines:**

```javascript
const lines = useCartLines();
lines.forEach((line) => {
  console.log(line.merchandise.product.title, line.quantity);
});
```

**useShippingAddress:**

```javascript
const address = useShippingAddress();
console.log(address.city, address.countryCode);
```

**useApplyCartLinesChange:**

```javascript
const applyChange = useApplyCartLinesChange();

async function addItem() {
  await applyChange({
    type: "addCartLine",
    merchandiseId: "gid://shopify/ProductVariant/123",
    quantity: 1,
  });
}
```

### Core Components

**Layout:**

- `BlockStack` - Vertical stacking
- `InlineStack` - Horizontal layout
- `Grid`, `GridItem` - Grid layout
- `View` - Container
- `Divider` - Separator

**Input:**

- `TextField` - Text input
- `Checkbox` - Boolean
- `Select` - Dropdown
- `DatePicker` - Date selection
- `Form` - Form wrapper

**Display:**

- `Text`, `Heading` - Typography
- `Banner` - Messages
- `Badge` - Status
- `Image` - Images
- `Link` - Hyperlinks
- `List`, `ListItem` - Lists

**Interactive:**

- `Button` - Actions
- `Modal` - Overlays
- `Pressable` - Click areas

## Admin UI Extensions

Extend Shopify admin interface.

### Admin Action

Custom actions on resource pages.

```bash
shopify app generate extension --type admin_action
```

```javascript
import {
  reactExtension,
  AdminAction,
  Button,
} from "@shopify/ui-extensions-react/admin";

export default reactExtension("admin.product-details.action.render", () => (
  <Extension />
));

function Extension() {
  const { data } = useData();

  async function handleExport() {
    const response = await fetch("/api/export", {
      method: "POST",
      body: JSON.stringify({ productId: data.product.id }),
    });
    console.log("Exported:", await response.json());
  }

  return (
    <AdminAction
      title="Export Product"
      primaryAction={<Button onPress={handleExport}>Export</Button>}
    />
  );
}
```

**Targets:**

- `admin.product-details.action.render`
- `admin.order-details.action.render`
- `admin.customer-details.action.render`

### Admin Block

Embedded content in admin pages.

```javascript
import {
  reactExtension,
  BlockStack,
  Text,
  Badge,
} from "@shopify/ui-extensions-react/admin";

export default reactExtension("admin.product-details.block.render", () => (
  <Extension />
));

function Extension() {
  const { data } = useData();
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetchAnalytics(data.product.id).then(setAnalytics);
  }, []);

  return (
    <BlockStack>
      <Text variant="headingMd">Product Analytics</Text>
      <Text>Views: {analytics?.views || 0}</Text>
      <Text>Conversions: {analytics?.conversions || 0}</Text>
      <Badge tone={analytics?.trending ? "success" : "info"}>
        {analytics?.trending ? "Trending" : "Normal"}
      </Badge>
    </BlockStack>
  );
}
```

**Targets:**

- `admin.product-details.block.render`
- `admin.order-details.block.render`
- `admin.customer-details.block.render`

## POS UI Extensions

Customize Point of Sale experience.

### Smart Grid Tile

Quick access action on POS home screen.

```javascript
import {
  reactExtension,
  SmartGridTile,
} from "@shopify/ui-extensions-react/pos";

export default reactExtension("pos.home.tile.render", () => <Extension />);

function Extension() {
  function handlePress() {
    // Navigate to custom workflow
  }

  return (
    <SmartGridTile
      title="Gift Cards"
      subtitle="Manage gift cards"
      onPress={handlePress}
    />
  );
}
```

### POS Modal

Full-screen workflow.

```javascript
import {
  reactExtension,
  Screen,
  BlockStack,
  Button,
  TextField,
} from "@shopify/ui-extensions-react/pos";

export default reactExtension("pos.home.modal.render", () => <Extension />);

function Extension() {
  const { navigation } = useApi();
  const [amount, setAmount] = useState("");

  function handleIssue() {
    // Issue gift card
    navigation.pop();
  }

  return (
    <Screen name="Gift Card" title="Issue Gift Card">
      <BlockStack>
        <TextField label="Amount" value={amount} onChange={setAmount} />
        <TextField label="Recipient Email" />
        <Button onPress={handleIssue}>Issue</Button>
      </BlockStack>
    </Screen>
  );
}
```

## Customer Account Extensions

Customize customer account pages.

### Order Status Extension

```javascript
import {
  reactExtension,
  BlockStack,
  Text,
  Button,
} from "@shopify/ui-extensions-react/customer-account";

export default reactExtension(
  "customer-account.order-status.block.render",
  () => <Extension />,
);

function Extension() {
  const { order } = useApi();

  function handleReturn() {
    // Initiate return
  }

  return (
    <BlockStack>
      <Text variant="headingMd">Need to return?</Text>
      <Text>Start return for order {order.name}</Text>
      <Button onPress={handleReturn}>Start Return</Button>
    </BlockStack>
  );
}
```

**Targets:**

- `customer-account.order-status.block.render`
- `customer-account.order-index.block.render`
- `customer-account.profile.block.render`

## Shopify Functions

Serverless backend customization.

### Function Types

**Discounts:**

- `order_discount` - Order-level discounts
- `product_discount` - Product-specific discounts
- `shipping_discount` - Shipping discounts

**Payment Customization:**

- Hide/rename/reorder payment methods

**Delivery Customization:**

- Custom shipping options
- Delivery rules

**Validation:**

- Cart validation rules
- Checkout validation

### Create Function

```bash
shopify app generate extension --type function
```

### Order Discount Function

```javascript
// input.graphql
query Input {
  cart {
    lines {
      quantity
      merchandise {
        ... on ProductVariant {
          product {
            hasTag(tag: "bulk-discount")
          }
        }
      }
    }
  }
}

// function.js
export default function orderDiscount(input) {
  const targets = input.cart.lines
    .filter(line => line.merchandise.product.hasTag)
    .map(line => ({
      productVariant: { id: line.merchandise.id }
    }));

  if (targets.length === 0) {
    return { discounts: [] };
  }

  return {
    discounts: [{
      targets,
      value: {
        percentage: {
          value: 10  // 10% discount
        }
      }
    }]
  };
}
```

### Payment Customization Function

```javascript
export default function paymentCustomization(input) {
  const hidePaymentMethods = input.cart.lines.some(
    (line) => line.merchandise.product.hasTag,
  );

  if (!hidePaymentMethods) {
    return { operations: [] };
  }

  return {
    operations: [
      {
        hide: {
          paymentMethodId: "gid://shopify/PaymentMethod/123",
        },
      },
    ],
  };
}
```

### Validation Function

```javascript
export default function cartValidation(input) {
  const errors = [];

  // Max 5 items per cart
  if (input.cart.lines.length > 5) {
    errors.push({
      localizedMessage: "Maximum 5 items allowed per order",
      target: "cart",
    });
  }

  // Min $50 for wholesale
  const isWholesale = input.cart.lines.some(
    (line) => line.merchandise.product.hasTag,
  );

  if (isWholesale && input.cart.cost.totalAmount.amount < 50) {
    errors.push({
      localizedMessage: "Wholesale orders require $50 minimum",
      target: "cart",
    });
  }

  return { errors };
}
```

## Network Requests

Extensions can call external APIs.

```javascript
import { useApi } from "@shopify/ui-extensions-react/checkout";

function Extension() {
  const { sessionToken } = useApi();

  async function fetchData() {
    const token = await sessionToken.get();

    const response = await fetch("https://your-app.com/api/data", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    return await response.json();
  }
}
```

## Best Practices

**Performance:**

- Lazy load data
- Memoize expensive computations
- Use loading states
- Minimize re-renders

**UX:**

- Provide clear error messages
- Show loading indicators
- Validate inputs
- Support keyboard navigation

**Security:**

- Verify session tokens on backend
- Sanitize user input
- Use HTTPS for all requests
- Don't expose sensitive data

**Testing:**

- Test on development stores
- Verify mobile/desktop
- Check accessibility
- Test edge cases

## Resources

- Checkout Extensions: https://shopify.dev/docs/api/checkout-extensions
- Admin Extensions: https://shopify.dev/docs/apps/admin/extensions
- Functions: https://shopify.dev/docs/apps/functions
- Components: https://shopify.dev/docs/api/checkout-ui-extensions/components

---

## Reference: Themes

# Themes Reference

Guide for developing Shopify themes with Liquid templating.

## Liquid Templating

### Syntax Basics

**Objects (Output):**
```liquid
{{ product.title }}
{{ product.price | money }}
{{ customer.email }}
```

**Tags (Logic):**
```liquid
{% if product.available %}
  <button>Add to Cart</button>
{% else %}
  <p>Sold Out</p>
{% endif %}

{% for product in collection.products %}
  {{ product.title }}
{% endfor %}

{% case product.type %}
  {% when 'Clothing' %}
    <span>Apparel</span>
  {% when 'Shoes' %}
    <span>Footwear</span>
  {% else %}
    <span>Other</span>
{% endcase %}
```

**Filters (Transform):**
```liquid
{{ product.title | upcase }}
{{ product.price | money }}
{{ product.description | strip_html | truncate: 100 }}
{{ product.image | img_url: 'medium' }}
{{ 'now' | date: '%B %d, %Y' }}
```

### Common Objects

**Product:**
```liquid
{{ product.id }}
{{ product.title }}
{{ product.handle }}
{{ product.description }}
{{ product.price }}
{{ product.compare_at_price }}
{{ product.available }}
{{ product.type }}
{{ product.vendor }}
{{ product.tags }}
{{ product.images }}
{{ product.variants }}
{{ product.featured_image }}
{{ product.url }}
```

**Collection:**
```liquid
{{ collection.title }}
{{ collection.handle }}
{{ collection.description }}
{{ collection.products }}
{{ collection.products_count }}
{{ collection.image }}
{{ collection.url }}
```

**Cart:**
```liquid
{{ cart.item_count }}
{{ cart.total_price }}
{{ cart.items }}
{{ cart.note }}
{{ cart.attributes }}
```

**Customer:**
```liquid
{{ customer.email }}
{{ customer.first_name }}
{{ customer.last_name }}
{{ customer.orders_count }}
{{ customer.total_spent }}
{{ customer.addresses }}
{{ customer.default_address }}
```

**Shop:**
```liquid
{{ shop.name }}
{{ shop.email }}
{{ shop.domain }}
{{ shop.currency }}
{{ shop.money_format }}
{{ shop.enabled_payment_types }}
```

### Common Filters

**String:**
- `upcase`, `downcase`, `capitalize`
- `strip_html`, `strip_newlines`
- `truncate: 100`, `truncatewords: 20`
- `replace: 'old', 'new'`

**Number:**
- `money` - Format currency
- `round`, `ceil`, `floor`
- `times`, `divided_by`, `plus`, `minus`

**Array:**
- `join: ', '`
- `first`, `last`
- `size`
- `map: 'property'`
- `where: 'property', 'value'`

**URL:**
- `img_url: 'size'` - Image URL
- `url_for_type`, `url_for_vendor`
- `link_to`, `link_to_type`

**Date:**
- `date: '%B %d, %Y'`

## Theme Architecture

### Directory Structure

```
theme/
├── assets/              # CSS, JS, images
├── config/              # Theme settings
│   ├── settings_schema.json
│   └── settings_data.json
├── layout/              # Base templates
│   └── theme.liquid
├── locales/             # Translations
│   └── en.default.json
├── sections/            # Reusable blocks
│   ├── header.liquid
│   ├── footer.liquid
│   └── product-grid.liquid
├── snippets/            # Small components
│   ├── product-card.liquid
│   └── icon.liquid
└── templates/           # Page templates
    ├── index.json
    ├── product.json
    ├── collection.json
    └── cart.liquid
```

### Layout

Base template wrapping all pages (`layout/theme.liquid`):

```liquid
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ page_title }}</title>

  {{ content_for_header }}

  <link rel="stylesheet" href="{{ 'theme.css' | asset_url }}">
</head>
<body>
  {% section 'header' %}

  <main>
    {{ content_for_layout }}
  </main>

  {% section 'footer' %}

  <script src="{{ 'theme.js' | asset_url }}"></script>
</body>
</html>
```

### Templates

Page-specific structures (`templates/product.json`):

```json
{
  "sections": {
    "main": {
      "type": "product-template",
      "settings": {
        "show_vendor": true,
        "show_quantity_selector": true
      }
    },
    "recommendations": {
      "type": "product-recommendations"
    }
  },
  "order": ["main", "recommendations"]
}
```

Legacy format (`templates/product.liquid`):
```liquid
<div class="product">
  <div class="product-images">
    <img src="{{ product.featured_image | img_url: 'large' }}" alt="{{ product.title }}">
  </div>

  <div class="product-details">
    <h1>{{ product.title }}</h1>
    <p class="price">{{ product.price | money }}</p>

    {% form 'product', product %}
      <select name="id">
        {% for variant in product.variants %}
          <option value="{{ variant.id }}">{{ variant.title }} - {{ variant.price | money }}</option>
        {% endfor %}
      </select>

      <button type="submit">Add to Cart</button>
    {% endform %}
  </div>
</div>
```

### Sections

Reusable content blocks (`sections/product-grid.liquid`):

```liquid
<div class="product-grid">
  {% for product in section.settings.collection.products %}
    <div class="product-card">
      <a href="{{ product.url }}">
        <img src="{{ product.featured_image | img_url: 'medium' }}" alt="{{ product.title }}">
        <h3>{{ product.title }}</h3>
        <p>{{ product.price | money }}</p>
      </a>
    </div>
  {% endfor %}
</div>

{% schema %}
{
  "name": "Product Grid",
  "settings": [
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_per_row",
      "min": 2,
      "max": 5,
      "step": 1,
      "default": 4,
      "label": "Products per row"
    }
  ],
  "presets": [
    {
      "name": "Product Grid"
    }
  ]
}
{% endschema %}
```

### Snippets

Small reusable components (`snippets/product-card.liquid`):

```liquid
<div class="product-card">
  <a href="{{ product.url }}">
    {% if product.featured_image %}
      <img src="{{ product.featured_image | img_url: 'medium' }}" alt="{{ product.title }}">
    {% endif %}
    <h3>{{ product.title }}</h3>
    <p class="price">{{ product.price | money }}</p>
    {% if product.compare_at_price > product.price %}
      <p class="sale-price">{{ product.compare_at_price | money }}</p>
    {% endif %}
  </a>
</div>
```

Include snippet:
```liquid
{% render 'product-card', product: product %}
```

## Development Workflow

### Setup

```bash
# Initialize new theme
shopify theme init

# Choose Dawn (reference theme) or blank
```

### Local Development

```bash
# Start local server
shopify theme dev

# Preview at http://localhost:9292
# Changes auto-sync to development theme
```

### Pull Theme

```bash
# Pull live theme
shopify theme pull --live

# Pull specific theme
shopify theme pull --theme=123456789

# Pull only templates
shopify theme pull --only=templates
```

### Push Theme

```bash
# Push to development theme
shopify theme push --development

# Create new unpublished theme
shopify theme push --unpublished

# Push specific files
shopify theme push --only=sections,snippets
```

### Theme Check

Lint theme code:
```bash
shopify theme check
shopify theme check --auto-correct
```

## Common Patterns

### Product Form with Variants

```liquid
{% form 'product', product %}
  {% unless product.has_only_default_variant %}
    {% for option in product.options_with_values %}
      <div class="product-option">
        <label>{{ option.name }}</label>
        <select name="options[{{ option.name }}]">
          {% for value in option.values %}
            <option value="{{ value }}">{{ value }}</option>
          {% endfor %}
        </select>
      </div>
    {% endfor %}
  {% endunless %}

  <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}">
  <input type="number" name="quantity" value="1" min="1">

  <button type="submit" {% unless product.available %}disabled{% endunless %}>
    {% if product.available %}Add to Cart{% else %}Sold Out{% endif %}
  </button>
{% endform %}
```

### Pagination

```liquid
{% paginate collection.products by 12 %}
  {% for product in collection.products %}
    {% render 'product-card', product: product %}
  {% endfor %}

  {% if paginate.pages > 1 %}
    <div class="pagination">
      {% if paginate.previous %}
        <a href="{{ paginate.previous.url }}">Previous</a>
      {% endif %}

      {% for part in paginate.parts %}
        {% if part.is_link %}
          <a href="{{ part.url }}">{{ part.title }}</a>
        {% else %}
          <span class="current">{{ part.title }}</span>
        {% endif %}
      {% endfor %}

      {% if paginate.next %}
        <a href="{{ paginate.next.url }}">Next</a>
      {% endif %}
    </div>
  {% endif %}
{% endpaginate %}
```

### Cart AJAX

```javascript
// Add to cart
fetch('/cart/add.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: variantId,
    quantity: 1
  })
})
.then(res => res.json())
.then(item => console.log('Added:', item));

// Get cart
fetch('/cart.js')
  .then(res => res.json())
  .then(cart => console.log('Cart:', cart));

// Update cart
fetch('/cart/change.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: lineItemKey,
    quantity: 2
  })
})
.then(res => res.json());
```

## Metafields in Themes

Access custom data:

```liquid
{{ product.metafields.custom.care_instructions }}
{{ product.metafields.custom.material.value }}

{% if product.metafields.custom.featured %}
  <span class="badge">Featured</span>
{% endif %}
```

## Best Practices

**Performance:**
- Optimize images (use appropriate sizes)
- Minimize Liquid logic complexity
- Use lazy loading for images
- Defer non-critical JavaScript

**Accessibility:**
- Use semantic HTML
- Include alt text for images
- Support keyboard navigation
- Ensure sufficient color contrast

**SEO:**
- Use descriptive page titles
- Include meta descriptions
- Structure content with headings
- Implement schema markup

**Code Quality:**
- Follow Shopify theme guidelines
- Use consistent naming conventions
- Comment complex logic
- Keep sections focused and reusable

## Resources

- Theme Development: https://shopify.dev/docs/themes
- Liquid Reference: https://shopify.dev/docs/api/liquid
- Dawn Theme: https://github.com/Shopify/dawn
- Theme Check: https://shopify.dev/docs/themes/tools/theme-check
