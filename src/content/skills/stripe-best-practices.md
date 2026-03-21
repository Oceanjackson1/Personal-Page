---
title: "Stripe Best Practices"
description: "构建 Stripe 集成的最佳实践，涵盖支付处理、结账流程和 Webhooks"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Stripe"
tags: ["stripe", "payments", "checkout", "integration"]
date: 2026-03-20
---


Latest Stripe API version: **2026-02-25.clover**. Always use the latest API version and SDK unless the user specifies otherwise.

## Integration routing

| Building... | Recommended API | Details |
|---|---|---|
| One-time payments | Checkout Sessions | [references/payments.md](references/payments.md) |
| Custom payment form with embedded UI | Checkout Sessions + Payment Element | [references/payments.md](references/payments.md) |
| Saving a payment method for later | Setup Intents | [references/payments.md](references/payments.md) |
| Connect platform or marketplace | Accounts v2 (`/v2/core/accounts`) | [references/connect.md](references/connect.md) |
| Subscriptions or recurring billing | Billing APIs + Checkout Sessions | [references/billing.md](references/billing.md) |
| Embedded financial accounts / banking | v2 Financial Accounts | [references/treasury.md](references/treasury.md) |

Read the relevant reference file before answering any integration question or writing code.

## Key documentation

When the user's request does not clearly fit a single domain above, consult:

- [Integration Options](https://docs.stripe.com/payments/payment-methods/integration-options.md) — Start here when designing any integration.
- [API Tour](https://docs.stripe.com/payments-api/tour.md) — Overview of Stripe's API surface.
- [Go Live Checklist](https://docs.stripe.com/get-started/checklist/go-live.md) — Review before launching.


---

## Reference: uilling

# Billing / Subscriptions

## Table of contents
- When to use Billing APIs
- Recommended frontend pairing
- Traps to avoid

## When to use Billing APIs

If the user has a recurring revenue model (subscriptions, usage-based billing, seat-based pricing), use the Billing APIs to [plan their integration](https://docs.stripe.com/billing/subscriptions/designing-integration.md) instead of a direct PaymentIntent integration.

Review the [Subscription Use Cases](https://docs.stripe.com/billing/subscriptions/use-cases.md) and [SaaS guide](https://docs.stripe.com/saas.md) to find the right pattern for the user's pricing model.

## Recommended frontend pairing

Combine Billing APIs with Stripe Checkout for the payment frontend. Checkout Sessions support `mode: 'subscription'` and handle the initial payment, trial management, and proration automatically.

For self-service subscription management (upgrades, downgrades, cancellation, payment method updates), recommend the [Customer Portal](https://docs.stripe.com/customer-management/integrate-customer-portal.md).

## Traps to avoid

- Do not build manual subscription renewal loops using raw PaymentIntents. Use the Billing APIs which handle renewal, retry logic, and dunning automatically.
- Do not use the deprecated `plan` object. Use [Prices](https://docs.stripe.com/api/prices.md) instead.

---

## Reference: connect

# Connect / Platforms

## Table of contents
- Accounts v2 API
- Controller properties
- Charge types
- Integration guides

## Accounts v2 API

For new Connect platforms, ALWAYS use the [Accounts v2 API](https://docs.stripe.com/connect/accounts-v2.md) (`POST /v2/core/accounts`). This is Stripe's actively invested path and ensures long-term support.

**Traps to avoid:** Do not use the legacy `type` parameter (`type: 'express'`, `type: 'custom'`, `type: 'standard'`) in `POST /v1/accounts` for new platforms unless the user has explicitly requested v1.

## Controller properties

Configure connected accounts using `controller` properties instead of legacy account types:

| Property | Controls |
|---|---|
| `controller.losses.payments` | Who is liable for negative balances |
| `controller.fees.payer` | Who pays Stripe fees |
| `controller.stripe_dashboard.type` | Dashboard access (`full`, `express`, `none`) |
| `controller.requirement_collection` | Who collects onboarding requirements |

Use `defaults.responsibilities`, `dashboard`, and `configuration` as described in [connected account configuration](https://docs.stripe.com/connect/accounts-v2/connected-account-configuration.md).

Always describe accounts in terms of their responsibility settings, dashboard access, and [capabilities](https://docs.stripe.com/connect/account-capabilities.md) to describe what connected accounts can do.

**Traps to avoid:** Do not use the terms "Standard", "Express", or "Custom" as account types. These are legacy categories that bundle together responsibility, dashboard, and requirement decisions into opaque labels. Controller properties give explicit control over each dimension.

## Charge types

Choose one charge type per integration — do not mix them. For most platforms, start with destination charges:

- **Destination charges** — Use when the platform accepts liability for negative balances. Funds route to the connected account via `transfer_data.destination`.
- **Direct charges** — Use when the platform wants Stripe to take risk on the connected account. The charge is created on the connected account directly.

Use `on_behalf_of` to control the merchant of record, but only after reading [how charges work in Connect](https://docs.stripe.com/connect/charges.md).

**Traps to avoid:** Do not use the Charges API for Connect fund flows — use PaymentIntents or Checkout Sessions with `transfer_data` or `on_behalf_of`. Do not mix charge types within a single integration.

## Integration guides

- [SaaS platforms and marketplaces guide](https://docs.stripe.com/connect/saas-platforms-and-marketplaces.md) — Choosing the right integration shape.
- [Interactive platform guide](https://docs.stripe.com/connect/interactive-platform-guide.md) — Step-by-step platform builder.
- [Design an integration](https://docs.stripe.com/connect/design-an-integration.md) — Detailed risk and responsibility decisions.

---

## Reference: payments

# Payments

## Table of contents
- API hierarchy
- Integration surfaces
- Payment Element guidance
- Saving payment methods
- Dynamic payment methods
- Deprecated APIs and migration paths
- PCI compliance

## API hierarchy

Use the [Checkout Sessions API](https://docs.stripe.com/api/checkout/sessions.md) (`checkout.sessions.create`) for on-session payments. It supports one-time payments and subscriptions and handles taxes, discounts, shipping, and adaptive pricing automatically.

Use the [PaymentIntents API](https://docs.stripe.com/payments/paymentintents/lifecycle.md) for off-session payments, or when the merchant needs to model checkout state independently and just create a charge.

**Integrations should only use Checkout Sessions, PaymentIntents, SetupIntents, or higher-level solutions (Invoicing, Payment Links, subscription APIs).**

## Integration surfaces

Prioritize Stripe-hosted or embedded Checkout where possible. Use in this order of preference:

1. **Payment Links** — No-code. Best for simple products.
2. **Checkout** ([docs](https://docs.stripe.com/payments/checkout.md)) — Stripe-hosted or embedded form. Best for most web apps.
3. **Payment Element** ([docs](https://docs.stripe.com/payments/payment-element.md)) — Embedded UI component for advanced customization.
   - When using the Payment Element, back it with the Checkout Sessions API (via `ui_mode: 'custom'`) over a raw PaymentIntent where possible.

**Traps to avoid:** Do not recommend the legacy Card Element or the Payment Element in card-only mode. If the user asks for the Card Element, advise them to [migrate to the Payment Element](https://docs.stripe.com/payments/payment-element/migration.md).

## Payment Element guidance

For surcharging or inspecting card details before payment (e.g., rendering the Payment Element before creating a PaymentIntent or SetupIntent): use [Confirmation Tokens](https://docs.stripe.com/payments/finalize-payments-on-the-server.md). Do not recommend `createPaymentMethod` or `createToken` from Stripe.js.

## Saving payment methods

Use the [Setup Intents API](https://docs.stripe.com/api/setup_intents.md) to save a payment method for later use.

**Traps to avoid:** Do not use the Sources API to save cards to customers. The Sources API is deprecated — Setup Intents is the correct approach.

## Dynamic payment methods

Advise users to enable dynamic payment methods in the Stripe Dashboard rather than passing specific [`payment_method_types`](https://docs.stripe.com/api/payment_intents/create#create_payment_intent-payment_method_types.md) in the PaymentIntent or SetupIntent. Stripe automatically selects payment methods based on the customer's location, wallets, and preferences when the Payment Element is used.

## Deprecated APIs and migration paths

Never recommend the Charges API. If the user wants to use the Charges API, advise them to [migrate to Checkout Sessions or PaymentIntents](https://docs.stripe.com/payments/payment-intents/migration/charges.md).

Do not call other deprecated or outdated API endpoints unless there is a specific need and absolutely no other way.

| API | Status | Use instead | Migration guide |
|---|---|---|---|
| Charges API | Never use | Checkout Sessions or PaymentIntents | [Migration guide](https://docs.stripe.com/payments/payment-intents/migration/charges.md) |
| Sources API | Deprecated | Setup Intents | [Setup Intents docs](https://docs.stripe.com/api/setup_intents.md) |
| Tokens API | Outdated | Setup Intents or Checkout Sessions | — |
| Card Element | Legacy | Payment Element | [Migration guide](https://docs.stripe.com/payments/payment-element/migration.md) |

## PCI compliance

If a PCI-compliant user asks about sending server-side raw PAN data, advise them that they may need to prove PCI compliance to access options like [payment_method_data](https://docs.stripe.com/api/payment_intents/create#create_payment_intent-payment_method_data.md).

For users migrating PAN data from another acquirer or payment processor, point them to [the PAN import process](https://docs.stripe.com/get-started/data-migrations/pan-import.md).

---

## Reference: treasury

# Treasury / Financial Accounts

## Table of contents
- v2 Financial Accounts API
- Legacy v1 Treasury

## v2 Financial Accounts API

For embedded financial accounts (bank accounts, account and routing numbers, money movement), use the [v2 Financial Accounts API](https://docs.stripe.com/api/v2/core/vault/financial-accounts.md) (`POST /v2/core/vault/financial_accounts`). This is required for new integrations.

For Treasury concepts and guides, see the [Treasury overview](https://docs.stripe.com/treasury.md).

## Legacy v1 Treasury

Do not use the [v1 Treasury Financial Accounts API](https://docs.stripe.com/api/treasury/financial_accounts.md) (`POST /v1/treasury/financial_accounts`) for new integrations. Existing v1 integrations continue to work.
