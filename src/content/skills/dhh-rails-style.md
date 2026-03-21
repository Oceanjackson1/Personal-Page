---
title: "Dhh Rails Style"
description: "This skill should be used when writing Ruby and Rails code in DHH's distinctive 37signals style. It applies when writing Ruby code, Rails applications, creating models, controllers, or any Ruby file. Triggers on Ruby/Rails code generation, refacto..."
category: "writing"
source: "community"
author: "Community"
tags: ["dhh", "rails", "style"]
date: 2026-03-20
---

<objective>
Apply 37signals/DHH Rails conventions to Ruby and Rails code. This skill provides comprehensive domain expertise extracted from analyzing production 37signals codebases (Fizzy/Campfire) and DHH's code review patterns.
</objective>

<essential_principles>
## Core Philosophy

"The best code is the code you don't write. The second best is the code that's obviously correct."

**Vanilla Rails is plenty:**
- Rich domain models over service objects
- CRUD controllers over custom actions
- Concerns for horizontal code sharing
- Records as state instead of boolean columns
- Database-backed everything (no Redis)
- Build solutions before reaching for gems

**What they deliberately avoid:**
- devise (custom ~150-line auth instead)
- pundit/cancancan (simple role checks in models)
- sidekiq (Solid Queue uses database)
- redis (database for everything)
- view_component (partials work fine)
- GraphQL (REST with Turbo sufficient)
- factory_bot (fixtures are simpler)
- rspec (Minitest ships with Rails)
- Tailwind (native CSS with layers)

**Development Philosophy:**
- Ship, Validate, Refine - prototype-quality code to production to learn
- Fix root causes, not symptoms
- Write-time operations over read-time computations
- Database constraints over ActiveRecord validations
</essential_principles>

<intake>
What are you working on?

1. **Controllers** - REST mapping, concerns, Turbo responses, API patterns
2. **Models** - Concerns, state records, callbacks, scopes, POROs
3. **Views & Frontend** - Turbo, Stimulus, CSS, partials
4. **Architecture** - Routing, multi-tenancy, authentication, jobs, caching
5. **Testing** - Minitest, fixtures, integration tests
6. **Gems & Dependencies** - What to use vs avoid
7. **Code Review** - Review code against DHH style
8. **General Guidance** - Philosophy and conventions

**Specify a number or describe your task.**
</intake>

<routing>

| Response | Reference to Read |
|----------|-------------------|
| 1, controller | [controllers.md](./references/controllers.md) |
| 2, model | [models.md](./references/models.md) |
| 3, view, frontend, turbo, stimulus, css | [frontend.md](./references/frontend.md) |
| 4, architecture, routing, auth, job, cache | [architecture.md](./references/architecture.md) |
| 5, test, testing, minitest, fixture | [testing.md](./references/testing.md) |
| 6, gem, dependency, library | [gems.md](./references/gems.md) |
| 7, review | Read all references, then review code |
| 8, general task | Read relevant references based on context |

**After reading relevant references, apply patterns to the user's code.**
</routing>

<quick_reference>
## Naming Conventions

**Verbs:** `card.close`, `card.gild`, `board.publish` (not `set_style` methods)

**Predicates:** `card.closed?`, `card.golden?` (derived from presence of related record)

**Concerns:** Adjectives describing capability (`Closeable`, `Publishable`, `Watchable`)

**Controllers:** Nouns matching resources (`Cards::ClosuresController`)

**Scopes:**
- `chronologically`, `reverse_chronologically`, `alphabetically`, `latest`
- `preloaded` (standard eager loading name)
- `indexed_by`, `sorted_by` (parameterized)
- `active`, `unassigned` (business terms, not SQL-ish)

## REST Mapping

Instead of custom actions, create new resources:

```
POST /cards/:id/close    → POST /cards/:id/closure
DELETE /cards/:id/close  → DELETE /cards/:id/closure
POST /cards/:id/archive  → POST /cards/:id/archival
```

## Ruby Syntax Preferences

```ruby
# Symbol arrays with spaces inside brackets
before_action :set_message, only: %i[ show edit update destroy ]

# Private method indentation
  private
    def set_message
      @message = Message.find(params[:id])
    end

# Expression-less case for conditionals
case
when params[:before].present?
  messages.page_before(params[:before])
else
  messages.last_page
end

# Bang methods for fail-fast
@message = Message.create!(params)

# Ternaries for simple conditionals
@room.direct? ? @room.users : @message.mentionees
```

## Key Patterns

**State as Records:**
```ruby
Card.joins(:closure)         # closed cards
Card.where.missing(:closure) # open cards
```

**Current Attributes:**
```ruby
belongs_to :creator, default: -> { Current.user }
```

**Authorization on Models:**
```ruby
class User < ApplicationRecord
  def can_administer?(message)
    message.creator == self || admin?
  end
end
```
</quick_reference>

<reference_index>
## Domain Knowledge

All detailed patterns in `references/`:

| File | Topics |
|------|--------|
| [controllers.md](./references/controllers.md) | REST mapping, concerns, Turbo responses, API patterns, HTTP caching |
| [models.md](./references/models.md) | Concerns, state records, callbacks, scopes, POROs, authorization, broadcasting |
| [frontend.md](./references/frontend.md) | Turbo Streams, Stimulus controllers, CSS layers, OKLCH colors, partials |
| [architecture.md](./references/architecture.md) | Routing, authentication, jobs, Current attributes, caching, database patterns |
| [testing.md](./references/testing.md) | Minitest, fixtures, unit/integration/system tests, testing patterns |
| [gems.md](./references/gems.md) | What they use vs avoid, decision framework, Gemfile examples |
</reference_index>

<success_criteria>
Code follows DHH style when:
- Controllers map to CRUD verbs on resources
- Models use concerns for horizontal behavior
- State is tracked via records, not booleans
- No unnecessary service objects or abstractions
- Database-backed solutions preferred over external services
- Tests use Minitest with fixtures
- Turbo/Stimulus for interactivity (no heavy JS frameworks)
- Native CSS with modern features (layers, OKLCH, nesting)
- Authorization logic lives on User model
- Jobs are shallow wrappers calling model methods
</success_criteria>

<credits>
Based on [The Unofficial 37signals/DHH Rails Style Guide](https://github.com/marckohlbrugge/unofficial-37signals-coding-style-guide) by [Marc Köhlbrugge](https://x.com/marckohlbrugge), generated through deep analysis of 265 pull requests from the Fizzy codebase.

**Important Disclaimers:**
- LLM-generated guide - may contain inaccuracies
- Code examples from Fizzy are licensed under the O'Saasy License
- Not affiliated with or endorsed by 37signals
</credits>

---

## Reference: Architecture

# Architecture - DHH Rails Style

<routing>
## Routing

Everything maps to CRUD. Nested resources for related actions:

```ruby
Rails.application.routes.draw do
  resources :boards do
    resources :cards do
      resource :closure
      resource :goldness
      resource :not_now
      resources :assignments
      resources :comments
    end
  end
end
```

**Verb-to-noun conversion:**
| Action | Resource |
|--------|----------|
| close a card | `card.closure` |
| watch a board | `board.watching` |
| mark as golden | `card.goldness` |
| archive a card | `card.archival` |

**Shallow nesting** - avoid deep URLs:
```ruby
resources :boards do
  resources :cards, shallow: true  # /boards/:id/cards, but /cards/:id
end
```

**Singular resources** for one-per-parent:
```ruby
resource :closure   # not resources
resource :goldness
```

**Resolve for URL generation:**
```ruby
# config/routes.rb
resolve("Comment") { |comment| [comment.card, anchor: dom_id(comment)] }

# Now url_for(@comment) works correctly
```
</routing>

<multi_tenancy>
## Multi-Tenancy (Path-Based)

**Middleware extracts tenant** from URL prefix:

```ruby
# lib/tenant_extractor.rb
class TenantExtractor
  def initialize(app)
    @app = app
  end

  def call(env)
    path = env["PATH_INFO"]
    if match = path.match(%r{^/(\d+)(/.*)?$})
      env["SCRIPT_NAME"] = "/#{match[1]}"
      env["PATH_INFO"] = match[2] || "/"
    end
    @app.call(env)
  end
end
```

**Cookie scoping** per tenant:
```ruby
# Cookies scoped to tenant path
cookies.signed[:session_id] = {
  value: session.id,
  path: "/#{Current.account.id}"
}
```

**Background job context** - serialize tenant:
```ruby
class ApplicationJob < ActiveJob::Base
  around_perform do |job, block|
    Current.set(account: job.arguments.first.account) { block.call }
  end
end
```

**Recurring jobs** must iterate all tenants:
```ruby
class DailyDigestJob < ApplicationJob
  def perform
    Account.find_each do |account|
      Current.set(account: account) do
        send_digest_for(account)
      end
    end
  end
end
```

**Controller security** - always scope through tenant:
```ruby
# Good - scoped through user's accessible records
@card = Current.user.accessible_cards.find(params[:id])

# Avoid - direct lookup
@card = Card.find(params[:id])
```
</multi_tenancy>

<authentication>
## Authentication

Custom passwordless magic link auth (~150 lines total):

```ruby
# app/models/session.rb
class Session < ApplicationRecord
  belongs_to :user

  before_create { self.token = SecureRandom.urlsafe_base64(32) }
end

# app/models/magic_link.rb
class MagicLink < ApplicationRecord
  belongs_to :user

  before_create do
    self.code = SecureRandom.random_number(100_000..999_999).to_s
    self.expires_at = 15.minutes.from_now
  end

  def expired?
    expires_at < Time.current
  end
end
```

**Why not Devise:**
- ~150 lines vs massive dependency
- No password storage liability
- Simpler UX for users
- Full control over flow

**Bearer token** for APIs:
```ruby
module Authentication
  extend ActiveSupport::Concern

  included do
    before_action :authenticate
  end

  private
    def authenticate
      if bearer_token = request.headers["Authorization"]&.split(" ")&.last
        Current.session = Session.find_by(token: bearer_token)
      else
        Current.session = Session.find_by(id: cookies.signed[:session_id])
      end

      redirect_to login_path unless Current.session
    end
end
```
</authentication>

<background_jobs>
## Background Jobs

Jobs are shallow wrappers calling model methods:

```ruby
class NotifyWatchersJob < ApplicationJob
  def perform(card)
    card.notify_watchers
  end
end
```

**Naming convention:**
- `_later` suffix for async: `card.notify_watchers_later`
- `_now` suffix for immediate: `card.notify_watchers_now`

```ruby
module Watchable
  def notify_watchers_later
    NotifyWatchersJob.perform_later(self)
  end

  def notify_watchers_now
    NotifyWatchersJob.perform_now(self)
  end

  def notify_watchers
    watchers.each do |watcher|
      WatcherMailer.notification(watcher, self).deliver_later
    end
  end
end
```

**Database-backed** with Solid Queue:
- No Redis required
- Same transactional guarantees as your data
- Simpler infrastructure

**Transaction safety:**
```ruby
# config/application.rb
config.active_job.enqueue_after_transaction_commit = true
```

**Error handling** by type:
```ruby
class DeliveryJob < ApplicationJob
  # Transient errors - retry with backoff
  retry_on Net::OpenTimeout, Net::ReadTimeout,
           Resolv::ResolvError,
           wait: :polynomially_longer

  # Permanent errors - log and discard
  discard_on Net::SMTPSyntaxError do |job, error|
    Sentry.capture_exception(error, level: :info)
  end
end
```

**Batch processing** with continuable:
```ruby
class ProcessCardsJob < ApplicationJob
  include ActiveJob::Continuable

  def perform
    Card.in_batches.each_record do |card|
      checkpoint!  # Resume from here if interrupted
      process(card)
    end
  end
end
```
</background_jobs>

<database_patterns>
## Database Patterns

**UUIDs as primary keys** (time-sortable UUIDv7):
```ruby
# migration
create_table :cards, id: :uuid do |t|
  t.references :board, type: :uuid, foreign_key: true
end
```

Benefits: No ID enumeration, distributed-friendly, client-side generation.

**State as records** (not booleans):
```ruby
# Instead of closed: boolean
class Card::Closure < ApplicationRecord
  belongs_to :card
  belongs_to :creator, class_name: "User"
end

# Queries become joins
Card.joins(:closure)          # closed
Card.where.missing(:closure)  # open
```

**Hard deletes** - no soft delete:
```ruby
# Just destroy
card.destroy!

# Use events for history
card.record_event(:deleted, by: Current.user)
```

Simplifies queries, uses event logs for auditing.

**Counter caches** for performance:
```ruby
class Comment < ApplicationRecord
  belongs_to :card, counter_cache: true
end

# card.comments_count available without query
```

**Account scoping** on every table:
```ruby
class Card < ApplicationRecord
  belongs_to :account
  default_scope { where(account: Current.account) }
end
```
</database_patterns>

<current_attributes>
## Current Attributes

Use `Current` for request-scoped state:

```ruby
# app/models/current.rb
class Current < ActiveSupport::CurrentAttributes
  attribute :session, :user, :account, :request_id

  delegate :user, to: :session, allow_nil: true

  def account=(account)
    super
    Time.zone = account&.time_zone || "UTC"
  end
end
```

Set in controller:
```ruby
class ApplicationController < ActionController::Base
  before_action :set_current_request

  private
    def set_current_request
      Current.session = authenticated_session
      Current.account = Account.find(params[:account_id])
      Current.request_id = request.request_id
    end
end
```

Use throughout app:
```ruby
class Card < ApplicationRecord
  belongs_to :creator, default: -> { Current.user }
end
```
</current_attributes>

<caching>
## Caching

**HTTP caching** with ETags:
```ruby
fresh_when etag: [@card, Current.user.timezone]
```

**Fragment caching:**
```erb
<% cache card do %>
  <%= render card %>
<% end %>
```

**Russian doll caching:**
```erb
<% cache @board do %>
  <% @board.cards.each do |card| %>
    <% cache card do %>
      <%= render card %>
    <% end %>
  <% end %>
<% end %>
```

**Cache invalidation** via `touch: true`:
```ruby
class Card < ApplicationRecord
  belongs_to :board, touch: true
end
```

**Solid Cache** - database-backed:
- No Redis required
- Consistent with application data
- Simpler infrastructure
</caching>

<configuration>
## Configuration

**ENV.fetch with defaults:**
```ruby
# config/application.rb
config.active_job.queue_adapter = ENV.fetch("QUEUE_ADAPTER", "solid_queue").to_sym
config.cache_store = ENV.fetch("CACHE_STORE", "solid_cache").to_sym
```

**Multiple databases:**
```yaml
# config/database.yml
production:
  primary:
    <<: *default
  cable:
    <<: *default
    migrations_paths: db/cable_migrate
  queue:
    <<: *default
    migrations_paths: db/queue_migrate
  cache:
    <<: *default
    migrations_paths: db/cache_migrate
```

**Switch between SQLite and MySQL via ENV:**
```ruby
adapter = ENV.fetch("DATABASE_ADAPTER", "sqlite3")
```

**CSP extensible via ENV:**
```ruby
config.content_security_policy do |policy|
  policy.default_src :self
  policy.script_src :self, *ENV.fetch("CSP_SCRIPT_SRC", "").split(",")
end
```
</configuration>

<testing>
## Testing

**Minitest**, not RSpec:
```ruby
class CardTest < ActiveSupport::TestCase
  test "closing a card creates a closure" do
    card = cards(:one)

    card.close

    assert card.closed?
    assert_not_nil card.closure
  end
end
```

**Fixtures** instead of factories:
```yaml
# test/fixtures/cards.yml
one:
  title: First Card
  board: main
  creator: alice

two:
  title: Second Card
  board: main
  creator: bob
```

**Integration tests** for controllers:
```ruby
class CardsControllerTest < ActionDispatch::IntegrationTest
  test "closing a card" do
    card = cards(:one)
    sign_in users(:alice)

    post card_closure_path(card)

    assert_response :success
    assert card.reload.closed?
  end
end
```

**Tests ship with features** - same commit, not TDD-first but together.

**Regression tests for security fixes** - always.
</testing>

<events>
## Event Tracking

Events are the single source of truth:

```ruby
class Event < ApplicationRecord
  belongs_to :creator, class_name: "User"
  belongs_to :eventable, polymorphic: true

  serialize :particulars, coder: JSON
end
```

**Eventable concern:**
```ruby
module Eventable
  extend ActiveSupport::Concern

  included do
    has_many :events, as: :eventable, dependent: :destroy
  end

  def record_event(action, particulars = {})
    events.create!(
      creator: Current.user,
      action: action,
      particulars: particulars
    )
  end
end
```

**Webhooks driven by events** - events are the canonical source.
</events>

<email_patterns>
## Email Patterns

**Multi-tenant URL helpers:**
```ruby
class ApplicationMailer < ActionMailer::Base
  def default_url_options
    options = super
    if Current.account
      options[:script_name] = "/#{Current.account.id}"
    end
    options
  end
end
```

**Timezone-aware delivery:**
```ruby
class NotificationMailer < ApplicationMailer
  def daily_digest(user)
    Time.use_zone(user.timezone) do
      @user = user
      @digest = user.digest_for_today
      mail(to: user.email, subject: "Daily Digest")
    end
  end
end
```

**Batch delivery:**
```ruby
emails = users.map { |user| NotificationMailer.digest(user) }
ActiveJob.perform_all_later(emails.map(&:deliver_later))
```

**One-click unsubscribe (RFC 8058):**
```ruby
class ApplicationMailer < ActionMailer::Base
  after_action :set_unsubscribe_headers

  private
    def set_unsubscribe_headers
      headers["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
      headers["List-Unsubscribe"] = "<#{unsubscribe_url}>"
    end
end
```
</email_patterns>

<security_patterns>
## Security Patterns

**XSS prevention** - escape in helpers:
```ruby
def formatted_content(text)
  # Escape first, then mark safe
  simple_format(h(text)).html_safe
end
```

**SSRF protection:**
```ruby
# Resolve DNS once, pin the IP
def fetch_safely(url)
  uri = URI.parse(url)
  ip = Resolv.getaddress(uri.host)

  # Block private networks
  raise "Private IP" if private_ip?(ip)

  # Use pinned IP for request
  Net::HTTP.start(uri.host, uri.port, ipaddr: ip) { |http| ... }
end

def private_ip?(ip)
  ip.start_with?("127.", "10.", "192.168.") ||
    ip.match?(/^172\.(1[6-9]|2[0-9]|3[0-1])\./)
end
```

**Content Security Policy:**
```ruby
# config/initializers/content_security_policy.rb
Rails.application.configure do
  config.content_security_policy do |policy|
    policy.default_src :self
    policy.script_src :self
    policy.style_src :self, :unsafe_inline
    policy.base_uri :none
    policy.form_action :self
    policy.frame_ancestors :self
  end
end
```

**ActionText sanitization:**
```ruby
# config/initializers/action_text.rb
Rails.application.config.after_initialize do
  ActionText::ContentHelper.allowed_tags = %w[
    strong em a ul ol li p br h1 h2 h3 h4 blockquote
  ]
end
```
</security_patterns>

<active_storage>
## Active Storage Patterns

**Variant preprocessing:**
```ruby
class User < ApplicationRecord
  has_one_attached :avatar do |attachable|
    attachable.variant :thumb, resize_to_limit: [100, 100], preprocessed: true
    attachable.variant :medium, resize_to_limit: [300, 300], preprocessed: true
  end
end
```

**Direct upload expiry** - extend for slow connections:
```ruby
# config/initializers/active_storage.rb
Rails.application.config.active_storage.service_urls_expire_in = 48.hours
```

**Avatar optimization** - redirect to blob:
```ruby
def show
  expires_in 1.year, public: true
  redirect_to @user.avatar.variant(:thumb).processed.url, allow_other_host: true
end
```

**Mirror service** for migrations:
```yaml
# config/storage.yml
production:
  service: Mirror
  primary: amazon
  mirrors: [google]
```
</active_storage>

---

## Reference: Controllers

# Controllers - DHH Rails Style

<rest_mapping>
## Everything Maps to CRUD

Custom actions become new resources. Instead of verbs on existing resources, create noun resources:

```ruby
# Instead of this:
POST /cards/:id/close
DELETE /cards/:id/close
POST /cards/:id/archive

# Do this:
POST /cards/:id/closure      # create closure
DELETE /cards/:id/closure    # destroy closure
POST /cards/:id/archival     # create archival
```

**Real examples from 37signals:**
```ruby
resources :cards do
  resource :closure       # closing/reopening
  resource :goldness      # marking important
  resource :not_now       # postponing
  resources :assignments  # managing assignees
end
```

Each resource gets its own controller with standard CRUD actions.
</rest_mapping>

<controller_concerns>
## Concerns for Shared Behavior

Controllers use concerns extensively. Common patterns:

**CardScoped** - loads @card, @board, provides render_card_replacement
```ruby
module CardScoped
  extend ActiveSupport::Concern

  included do
    before_action :set_card
  end

  private
    def set_card
      @card = Card.find(params[:card_id])
      @board = @card.board
    end

    def render_card_replacement
      render turbo_stream: turbo_stream.replace(@card)
    end
end
```

**BoardScoped** - loads @board
**CurrentRequest** - populates Current with request data
**CurrentTimezone** - wraps requests in user's timezone
**FilterScoped** - handles complex filtering
**TurboFlash** - flash messages via Turbo Stream
**ViewTransitions** - disables on page refresh
**BlockSearchEngineIndexing** - sets X-Robots-Tag header
**RequestForgeryProtection** - Sec-Fetch-Site CSRF (modern browsers)
</controller_concerns>

<authorization_patterns>
## Authorization Patterns

Controllers check permissions via before_action, models define what permissions mean:

```ruby
# Controller concern
module Authorization
  extend ActiveSupport::Concern

  private
    def ensure_can_administer
      head :forbidden unless Current.user.admin?
    end

    def ensure_is_staff_member
      head :forbidden unless Current.user.staff?
    end
end

# Usage
class BoardsController < ApplicationController
  before_action :ensure_can_administer, only: [:destroy]
end
```

**Model-level authorization:**
```ruby
class Board < ApplicationRecord
  def editable_by?(user)
    user.admin? || user == creator
  end

  def publishable_by?(user)
    editable_by?(user) && !published?
  end
end
```

Keep authorization simple, readable, colocated with domain.
</authorization_patterns>

<security_concerns>
## Security Concerns

**Sec-Fetch-Site CSRF Protection:**
Modern browsers send Sec-Fetch-Site header. Use it for defense in depth:

```ruby
module RequestForgeryProtection
  extend ActiveSupport::Concern

  included do
    before_action :verify_request_origin
  end

  private
    def verify_request_origin
      return if request.get? || request.head?
      return if %w[same-origin same-site].include?(
        request.headers["Sec-Fetch-Site"]&.downcase
      )
      # Fall back to token verification for older browsers
      verify_authenticity_token
    end
end
```

**Rate Limiting (Rails 8+):**
```ruby
class MagicLinksController < ApplicationController
  rate_limit to: 10, within: 15.minutes, only: :create
end
```

Apply to: auth endpoints, email sending, external API calls, resource creation.
</security_concerns>

<request_context>
## Request Context Concerns

**CurrentRequest** - populates Current with HTTP metadata:
```ruby
module CurrentRequest
  extend ActiveSupport::Concern

  included do
    before_action :set_current_request
  end

  private
    def set_current_request
      Current.request_id = request.request_id
      Current.user_agent = request.user_agent
      Current.ip_address = request.remote_ip
      Current.referrer = request.referrer
    end
end
```

**CurrentTimezone** - wraps requests in user's timezone:
```ruby
module CurrentTimezone
  extend ActiveSupport::Concern

  included do
    around_action :set_timezone
    helper_method :timezone_from_cookie
  end

  private
    def set_timezone
      Time.use_zone(timezone_from_cookie) { yield }
    end

    def timezone_from_cookie
      cookies[:timezone] || "UTC"
    end
end
```

**SetPlatform** - detects mobile/desktop:
```ruby
module SetPlatform
  extend ActiveSupport::Concern

  included do
    helper_method :platform
  end

  def platform
    @platform ||= request.user_agent&.match?(/Mobile|Android/) ? :mobile : :desktop
  end
end
```
</request_context>

<turbo_responses>
## Turbo Stream Responses

Use Turbo Streams for partial updates:

```ruby
class Cards::ClosuresController < ApplicationController
  include CardScoped

  def create
    @card.close
    render_card_replacement
  end

  def destroy
    @card.reopen
    render_card_replacement
  end
end
```

For complex updates, use morphing:
```ruby
render turbo_stream: turbo_stream.morph(@card)
```
</turbo_responses>

<api_patterns>
## API Design

Same controllers, different format. Convention for responses:

```ruby
def create
  @card = Card.create!(card_params)

  respond_to do |format|
    format.html { redirect_to @card }
    format.json { head :created, location: @card }
  end
end

def update
  @card.update!(card_params)

  respond_to do |format|
    format.html { redirect_to @card }
    format.json { head :no_content }
  end
end

def destroy
  @card.destroy

  respond_to do |format|
    format.html { redirect_to cards_path }
    format.json { head :no_content }
  end
end
```

**Status codes:**
- Create: 201 Created + Location header
- Update: 204 No Content
- Delete: 204 No Content
- Bearer token authentication
</api_patterns>

<http_caching>
## HTTP Caching

Extensive use of ETags and conditional GETs:

```ruby
class CardsController < ApplicationController
  def show
    @card = Card.find(params[:id])
    fresh_when etag: [@card, Current.user.timezone]
  end

  def index
    @cards = @board.cards.preloaded
    fresh_when etag: [@cards, @board.updated_at]
  end
end
```

Key insight: Times render server-side in user's timezone, so timezone must affect the ETag to prevent serving wrong times to other timezones.

**ApplicationController global etag:**
```ruby
class ApplicationController < ActionController::Base
  etag { "v1" }  # Bump to invalidate all caches
end
```

Use `touch: true` on associations for cache invalidation.
</http_caching>

---

## Reference: Frontend

# Frontend - DHH Rails Style

<turbo_patterns>
## Turbo Patterns

**Turbo Streams** for partial updates:
```erb
<%# app/views/cards/closures/create.turbo_stream.erb %>
<%= turbo_stream.replace @card %>
```

**Morphing** for complex updates:
```ruby
render turbo_stream: turbo_stream.morph(@card)
```

**Global morphing** - enable in layout:
```ruby
turbo_refreshes_with method: :morph, scroll: :preserve
```

**Fragment caching** with `cached: true`:
```erb
<%= render partial: "card", collection: @cards, cached: true %>
```

**No ViewComponents** - standard partials work fine.
</turbo_patterns>

<turbo_morphing>
## Turbo Morphing Best Practices

**Listen for morph events** to restore client state:
```javascript
document.addEventListener("turbo:morph-element", (event) => {
  // Restore any client-side state after morph
})
```

**Permanent elements** - skip morphing with data attribute:
```erb
<div data-turbo-permanent id="notification-count">
  <%= @count %>
</div>
```

**Frame morphing** - add refresh attribute:
```erb
<%= turbo_frame_tag :assignment, src: path, refresh: :morph %>
```

**Common issues and solutions:**

| Problem | Solution |
|---------|----------|
| Timers not updating | Clear/restart in morph event listener |
| Forms resetting | Wrap form sections in turbo frames |
| Pagination breaking | Use turbo frames with `refresh: :morph` |
| Flickering on replace | Switch to morph instead of replace |
| localStorage loss | Listen to `turbo:morph-element`, restore state |
</turbo_morphing>

<turbo_frames>
## Turbo Frames

**Lazy loading** with spinner:
```erb
<%= turbo_frame_tag "menu",
      src: menu_path,
      loading: :lazy do %>
  <div class="spinner">Loading...</div>
<% end %>
```

**Inline editing** with edit/view toggle:
```erb
<%= turbo_frame_tag dom_id(card, :edit) do %>
  <%= link_to "Edit", edit_card_path(card),
        data: { turbo_frame: dom_id(card, :edit) } %>
<% end %>
```

**Target parent frame** without hardcoding:
```erb
<%= form_with model: @card, data: { turbo_frame: "_parent" } do |f| %>
```

**Real-time subscriptions:**
```erb
<%= turbo_stream_from @card %>
<%= turbo_stream_from @card, :activity %>
```
</turbo_frames>

<stimulus_controllers>
## Stimulus Controllers

52 controllers in Fizzy, split 62% reusable, 38% domain-specific.

**Characteristics:**
- Single responsibility per controller
- Configuration via values/classes
- Events for communication
- Private methods with #
- Most under 50 lines

**Examples:**

```javascript
// copy-to-clipboard (25 lines)
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { content: String }

  copy() {
    navigator.clipboard.writeText(this.contentValue)
    this.#showFeedback()
  }

  #showFeedback() {
    this.element.classList.add("copied")
    setTimeout(() => this.element.classList.remove("copied"), 1500)
  }
}
```

```javascript
// auto-click (7 lines)
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    this.element.click()
  }
}
```

```javascript
// toggle-class (31 lines)
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static classes = ["toggle"]
  static values = { open: { type: Boolean, default: false } }

  toggle() {
    this.openValue = !this.openValue
  }

  openValueChanged() {
    this.element.classList.toggle(this.toggleClass, this.openValue)
  }
}
```

```javascript
// auto-submit (28 lines) - debounced form submission
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { delay: { type: Number, default: 300 } }

  connect() {
    this.timeout = null
  }

  submit() {
    clearTimeout(this.timeout)
    this.timeout = setTimeout(() => {
      this.element.requestSubmit()
    }, this.delayValue)
  }

  disconnect() {
    clearTimeout(this.timeout)
  }
}
```

```javascript
// dialog (45 lines) - native HTML dialog management
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  open() {
    this.element.showModal()
  }

  close() {
    this.element.close()
    this.dispatch("closed")
  }

  clickOutside(event) {
    if (event.target === this.element) this.close()
  }
}
```

```javascript
// local-time (40 lines) - relative time display
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { datetime: String }

  connect() {
    this.#updateTime()
  }

  #updateTime() {
    const date = new Date(this.datetimeValue)
    const now = new Date()
    const diffMinutes = Math.floor((now - date) / 60000)

    if (diffMinutes < 60) {
      this.element.textContent = `${diffMinutes}m ago`
    } else if (diffMinutes < 1440) {
      this.element.textContent = `${Math.floor(diffMinutes / 60)}h ago`
    } else {
      this.element.textContent = `${Math.floor(diffMinutes / 1440)}d ago`
    }
  }
}
```
</stimulus_controllers>

<stimulus_best_practices>
## Stimulus Best Practices

**Values API** over getAttribute:
```javascript
// Good
static values = { delay: { type: Number, default: 300 } }

// Avoid
this.element.getAttribute("data-delay")
```

**Cleanup in disconnect:**
```javascript
disconnect() {
  clearTimeout(this.timeout)
  this.observer?.disconnect()
  document.removeEventListener("keydown", this.boundHandler)
}
```

**Action filters** - `:self` prevents bubbling:
```erb
<div data-action="click->menu#toggle:self">
```

**Helper extraction** - shared utilities in separate modules:
```javascript
// app/javascript/helpers/timing.js
export function debounce(fn, delay) {
  let timeout
  return (...args) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => fn(...args), delay)
  }
}
```

**Event dispatching** for loose coupling:
```javascript
this.dispatch("selected", { detail: { id: this.idValue } })
```
</stimulus_best_practices>

<view_helpers>
## View Helpers (Stimulus-Integrated)

**Dialog helper:**
```ruby
def dialog_tag(id, &block)
  tag.dialog(
    id: id,
    data: {
      controller: "dialog",
      action: "click->dialog#clickOutside keydown.esc->dialog#close"
    },
    &block
  )
end
```

**Auto-submit form helper:**
```ruby
def auto_submit_form_with(model:, delay: 300, **options, &block)
  form_with(
    model: model,
    data: {
      controller: "auto-submit",
      auto_submit_delay_value: delay,
      action: "input->auto-submit#submit"
    },
    **options,
    &block
  )
end
```

**Copy button helper:**
```ruby
def copy_button(content:, label: "Copy")
  tag.button(
    label,
    data: {
      controller: "copy",
      copy_content_value: content,
      action: "click->copy#copy"
    }
  )
end
```
</view_helpers>

<css_architecture>
## CSS Architecture

Vanilla CSS with modern features, no preprocessors.

**CSS @layer** for cascade control:
```css
@layer reset, base, components, modules, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
}

@layer base {
  body { font-family: var(--font-sans); }
}

@layer components {
  .btn { /* button styles */ }
}

@layer modules {
  .card { /* card module styles */ }
}

@layer utilities {
  .hidden { display: none; }
}
```

**OKLCH color system** for perceptual uniformity:
```css
:root {
  --color-primary: oklch(60% 0.15 250);
  --color-success: oklch(65% 0.2 145);
  --color-warning: oklch(75% 0.15 85);
  --color-danger: oklch(55% 0.2 25);
}
```

**Dark mode** via CSS variables:
```css
:root {
  --bg: oklch(98% 0 0);
  --text: oklch(20% 0 0);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: oklch(15% 0 0);
    --text: oklch(90% 0 0);
  }
}
```

**Native CSS nesting:**
```css
.card {
  padding: var(--space-4);

  & .title {
    font-weight: bold;
  }

  &:hover {
    background: var(--bg-hover);
  }
}
```

**~60 minimal utilities** vs Tailwind's hundreds.

**Modern features used:**
- `@starting-style` for enter animations
- `color-mix()` for color manipulation
- `:has()` for parent selection
- Logical properties (`margin-inline`, `padding-block`)
- Container queries
</css_architecture>

<view_patterns>
## View Patterns

**Standard partials** - no ViewComponents:
```erb
<%# app/views/cards/_card.html.erb %>
<article id="<%= dom_id(card) %>" class="card">
  <%= render "cards/header", card: card %>
  <%= render "cards/body", card: card %>
  <%= render "cards/footer", card: card %>
</article>
```

**Fragment caching:**
```erb
<% cache card do %>
  <%= render "cards/card", card: card %>
<% end %>
```

**Collection caching:**
```erb
<%= render partial: "card", collection: @cards, cached: true %>
```

**Simple component naming** - no strict BEM:
```css
.card { }
.card .title { }
.card .actions { }
.card.golden { }
.card.closed { }
```
</view_patterns>

<caching_with_personalization>
## User-Specific Content in Caches

Move personalization to client-side JavaScript to preserve caching:

```erb
<%# Cacheable fragment %>
<% cache card do %>
  <article class="card"
           data-creator-id="<%= card.creator_id %>"
           data-controller="ownership"
           data-ownership-current-user-value="<%= Current.user.id %>">
    <button data-ownership-target="ownerOnly" class="hidden">Delete</button>
  </article>
<% end %>
```

```javascript
// Reveal user-specific elements after cache hit
export default class extends Controller {
  static values = { currentUser: Number }
  static targets = ["ownerOnly"]

  connect() {
    const creatorId = parseInt(this.element.dataset.creatorId)
    if (creatorId === this.currentUserValue) {
      this.ownerOnlyTargets.forEach(el => el.classList.remove("hidden"))
    }
  }
}
```

**Extract dynamic content** to separate frames:
```erb
<% cache [card, board] do %>
  <article class="card">
    <%= turbo_frame_tag card, :assignment,
          src: card_assignment_path(card),
          refresh: :morph %>
  </article>
<% end %>
```

Assignment dropdown updates independently without invalidating parent cache.
</caching_with_personalization>

<broadcasting>
## Broadcasting with Turbo Streams

**Model callbacks** for real-time updates:
```ruby
class Card < ApplicationRecord
  include Broadcastable

  after_create_commit :broadcast_created
  after_update_commit :broadcast_updated
  after_destroy_commit :broadcast_removed

  private
    def broadcast_created
      broadcast_append_to [Current.account, board], :cards
    end

    def broadcast_updated
      broadcast_replace_to [Current.account, board], :cards
    end

    def broadcast_removed
      broadcast_remove_to [Current.account, board], :cards
    end
end
```

**Scope by tenant** using `[Current.account, resource]` pattern.
</broadcasting>

---

## Reference: Gems

# Gems - DHH Rails Style

<what_they_use>
## What 37signals Uses

**Core Rails stack:**
- turbo-rails, stimulus-rails, importmap-rails
- propshaft (asset pipeline)

**Database-backed services (Solid suite):**
- solid_queue - background jobs
- solid_cache - caching
- solid_cable - WebSockets/Action Cable

**Authentication & Security:**
- bcrypt (for any password hashing needed)

**Their own gems:**
- geared_pagination (cursor-based pagination)
- lexxy (rich text editor)
- mittens (mailer utilities)

**Utilities:**
- rqrcode (QR code generation)
- redcarpet + rouge (Markdown rendering)
- web-push (push notifications)

**Deployment & Operations:**
- kamal (Docker deployment)
- thruster (HTTP/2 proxy)
- mission_control-jobs (job monitoring)
- autotuner (GC tuning)
</what_they_use>

<what_they_avoid>
## What They Deliberately Avoid

**Authentication:**
```
devise → Custom ~150-line auth
```
Why: Full control, no password liability with magic links, simpler.

**Authorization:**
```
pundit/cancancan → Simple role checks in models
```
Why: Most apps don't need policy objects. A method on the model suffices:
```ruby
class Board < ApplicationRecord
  def editable_by?(user)
    user.admin? || user == creator
  end
end
```

**Background Jobs:**
```
sidekiq → Solid Queue
```
Why: Database-backed means no Redis, same transactional guarantees.

**Caching:**
```
redis → Solid Cache
```
Why: Database is already there, simpler infrastructure.

**Search:**
```
elasticsearch → Custom sharded search
```
Why: Built exactly what they need, no external service dependency.

**View Layer:**
```
view_component → Standard partials
```
Why: Partials work fine. ViewComponents add complexity without clear benefit for their use case.

**API:**
```
GraphQL → REST with Turbo
```
Why: REST is sufficient when you control both ends. GraphQL complexity not justified.

**Factories:**
```
factory_bot → Fixtures
```
Why: Fixtures are simpler, faster, and encourage thinking about data relationships upfront.

**Service Objects:**
```
Interactor, Trailblazer → Fat models
```
Why: Business logic stays in models. Methods like `card.close` instead of `CardCloser.call(card)`.

**Form Objects:**
```
Reform, dry-validation → params.expect + model validations
```
Why: Rails 7.1's `params.expect` is clean enough. Contextual validations on model.

**Decorators:**
```
Draper → View helpers + partials
```
Why: Helpers and partials are simpler. No decorator indirection.

**CSS:**
```
Tailwind, Sass → Native CSS
```
Why: Modern CSS has nesting, variables, layers. No build step needed.

**Frontend:**
```
React, Vue, SPAs → Turbo + Stimulus
```
Why: Server-rendered HTML with sprinkles of JS. SPA complexity not justified.

**Testing:**
```
RSpec → Minitest
```
Why: Simpler, faster boot, less DSL magic, ships with Rails.
</what_they_avoid>

<testing_philosophy>
## Testing Philosophy

**Minitest** - simpler, faster:
```ruby
class CardTest < ActiveSupport::TestCase
  test "closing creates closure" do
    card = cards(:one)
    assert_difference -> { Card::Closure.count } do
      card.close
    end
    assert card.closed?
  end
end
```

**Fixtures** - loaded once, deterministic:
```yaml
# test/fixtures/cards.yml
open_card:
  title: Open Card
  board: main
  creator: alice

closed_card:
  title: Closed Card
  board: main
  creator: bob
```

**Dynamic timestamps** with ERB:
```yaml
recent:
  title: Recent
  created_at: <%= 1.hour.ago %>

old:
  title: Old
  created_at: <%= 1.month.ago %>
```

**Time travel** for time-dependent tests:
```ruby
test "expires after 15 minutes" do
  magic_link = MagicLink.create!(user: users(:alice))

  travel 16.minutes

  assert magic_link.expired?
end
```

**VCR** for external APIs:
```ruby
VCR.use_cassette("stripe/charge") do
  charge = Stripe::Charge.create(amount: 1000)
  assert charge.paid
end
```

**Tests ship with features** - same commit, not before or after.
</testing_philosophy>

<decision_framework>
## Decision Framework

Before adding a gem, ask:

1. **Can vanilla Rails do this?**
   - ActiveRecord can do most things Sequel can
   - ActionMailer handles email fine
   - ActiveJob works for most job needs

2. **Is the complexity worth it?**
   - 150 lines of custom code vs. 10,000-line gem
   - You'll understand your code better
   - Fewer upgrade headaches

3. **Does it add infrastructure?**
   - Redis? Consider database-backed alternatives
   - External service? Consider building in-house
   - Simpler infrastructure = fewer failure modes

4. **Is it from someone you trust?**
   - 37signals gems: battle-tested at scale
   - Well-maintained, focused gems: usually fine
   - Kitchen-sink gems: probably overkill

**The philosophy:**
> "Build solutions before reaching for gems."

Not anti-gem, but pro-understanding. Use gems when they genuinely solve a problem you have, not a problem you might have.
</decision_framework>

<gem_patterns>
## Gem Usage Patterns

**Pagination:**
```ruby
# geared_pagination - cursor-based
class CardsController < ApplicationController
  def index
    @cards = @board.cards.geared(page: params[:page])
  end
end
```

**Markdown:**
```ruby
# redcarpet + rouge
class MarkdownRenderer
  def self.render(text)
    Redcarpet::Markdown.new(
      Redcarpet::Render::HTML.new(filter_html: true),
      autolink: true,
      fenced_code_blocks: true
    ).render(text)
  end
end
```

**Background jobs:**
```ruby
# solid_queue - no Redis
class ApplicationJob < ActiveJob::Base
  queue_as :default
  # Just works, backed by database
end
```

**Caching:**
```ruby
# solid_cache - no Redis
# config/environments/production.rb
config.cache_store = :solid_cache_store
```
</gem_patterns>

---

## Reference: Models

# Models - DHH Rails Style

<model_concerns>
## Concerns for Horizontal Behavior

Models heavily use concerns. A typical Card model includes 14+ concerns:

```ruby
class Card < ApplicationRecord
  include Assignable
  include Attachments
  include Broadcastable
  include Closeable
  include Colored
  include Eventable
  include Golden
  include Mentions
  include Multistep
  include Pinnable
  include Postponable
  include Readable
  include Searchable
  include Taggable
  include Watchable
end
```

Each concern is self-contained with associations, scopes, and methods.

**Naming:** Adjectives describing capability (`Closeable`, `Publishable`, `Watchable`)
</model_concerns>

<state_records>
## State as Records, Not Booleans

Instead of boolean columns, create separate records:

```ruby
# Instead of:
closed: boolean
is_golden: boolean
postponed: boolean

# Create records:
class Card::Closure < ApplicationRecord
  belongs_to :card
  belongs_to :creator, class_name: "User"
end

class Card::Goldness < ApplicationRecord
  belongs_to :card
  belongs_to :creator, class_name: "User"
end

class Card::NotNow < ApplicationRecord
  belongs_to :card
  belongs_to :creator, class_name: "User"
end
```

**Benefits:**
- Automatic timestamps (when it happened)
- Track who made changes
- Easy filtering via joins and `where.missing`
- Enables rich UI showing when/who

**In the model:**
```ruby
module Closeable
  extend ActiveSupport::Concern

  included do
    has_one :closure, dependent: :destroy
  end

  def closed?
    closure.present?
  end

  def close(creator: Current.user)
    create_closure!(creator: creator)
  end

  def reopen
    closure&.destroy
  end
end
```

**Querying:**
```ruby
Card.joins(:closure)         # closed cards
Card.where.missing(:closure) # open cards
```
</state_records>

<callbacks>
## Callbacks - Used Sparingly

Only 38 callback occurrences across 30 files in Fizzy. Guidelines:

**Use for:**
- `after_commit` for async work
- `before_save` for derived data
- `after_create_commit` for side effects

**Avoid:**
- Complex callback chains
- Business logic in callbacks
- Synchronous external calls

```ruby
class Card < ApplicationRecord
  after_create_commit :notify_watchers_later
  before_save :update_search_index, if: :title_changed?

  private
    def notify_watchers_later
      NotifyWatchersJob.perform_later(self)
    end
end
```
</callbacks>

<scopes>
## Scope Naming

Standard scope names:

```ruby
class Card < ApplicationRecord
  scope :chronologically, -> { order(created_at: :asc) }
  scope :reverse_chronologically, -> { order(created_at: :desc) }
  scope :alphabetically, -> { order(title: :asc) }
  scope :latest, -> { reverse_chronologically.limit(10) }

  # Standard eager loading
  scope :preloaded, -> { includes(:creator, :assignees, :tags) }

  # Parameterized
  scope :indexed_by, ->(column) { order(column => :asc) }
  scope :sorted_by, ->(column, direction = :asc) { order(column => direction) }
end
```
</scopes>

<poros>
## Plain Old Ruby Objects

POROs namespaced under parent models:

```ruby
# app/models/event/description.rb
class Event::Description
  def initialize(event)
    @event = event
  end

  def to_s
    # Presentation logic for event description
  end
end

# app/models/card/eventable/system_commenter.rb
class Card::Eventable::SystemCommenter
  def initialize(card)
    @card = card
  end

  def comment(message)
    # Business logic
  end
end

# app/models/user/filtering.rb
class User::Filtering
  # View context bundling
end
```

**NOT used for service objects.** Business logic stays in models.
</poros>

<verbs_predicates>
## Method Naming

**Verbs** - Actions that change state:
```ruby
card.close
card.reopen
card.gild      # make golden
card.ungild
board.publish
board.archive
```

**Predicates** - Queries derived from state:
```ruby
card.closed?    # closure.present?
card.golden?    # goldness.present?
board.published?
```

**Avoid** generic setters:
```ruby
# Bad
card.set_closed(true)
card.update_golden_status(false)

# Good
card.close
card.ungild
```
</verbs_predicates>

<validation_philosophy>
## Validation Philosophy

Minimal validations on models. Use contextual validations on form/operation objects:

```ruby
# Model - minimal
class User < ApplicationRecord
  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
end

# Form object - contextual
class Signup
  include ActiveModel::Model

  attr_accessor :email, :name, :terms_accepted

  validates :email, :name, presence: true
  validates :terms_accepted, acceptance: true

  def save
    return false unless valid?
    User.create!(email: email, name: name)
  end
end
```

**Prefer database constraints** over model validations for data integrity:
```ruby
# migration
add_index :users, :email, unique: true
add_foreign_key :cards, :boards
```
</validation_philosophy>

<error_handling>
## Let It Crash Philosophy

Use bang methods that raise exceptions on failure:

```ruby
# Preferred - raises on failure
@card = Card.create!(card_params)
@card.update!(title: new_title)
@comment.destroy!

# Avoid - silent failures
@card = Card.create(card_params)  # returns false on failure
if @card.save
  # ...
end
```

Let errors propagate naturally. Rails handles ActiveRecord::RecordInvalid with 422 responses.
</error_handling>

<default_values>
## Default Values with Lambdas

Use lambda defaults for associations with Current:

```ruby
class Card < ApplicationRecord
  belongs_to :creator, class_name: "User", default: -> { Current.user }
  belongs_to :account, default: -> { Current.account }
end

class Comment < ApplicationRecord
  belongs_to :commenter, class_name: "User", default: -> { Current.user }
end
```

Lambdas ensure dynamic resolution at creation time.
</default_values>

<rails_71_patterns>
## Rails 7.1+ Model Patterns

**Normalizes** - clean data before validation:
```ruby
class User < ApplicationRecord
  normalizes :email, with: ->(email) { email.strip.downcase }
  normalizes :phone, with: ->(phone) { phone.gsub(/\D/, "") }
end
```

**Delegated Types** - replace polymorphic associations:
```ruby
class Message < ApplicationRecord
  delegated_type :messageable, types: %w[Comment Reply Announcement]
end

# Now you get:
message.comment?        # true if Comment
message.comment         # returns the Comment
Message.comments        # scope for Comment messages
```

**Store Accessor** - structured JSON storage:
```ruby
class User < ApplicationRecord
  store :settings, accessors: [:theme, :notifications_enabled], coder: JSON
end

user.theme = "dark"
user.notifications_enabled = true
```
</rails_71_patterns>

<concern_guidelines>
## Concern Guidelines

- **50-150 lines** per concern (most are ~100)
- **Cohesive** - related functionality only
- **Named for capabilities** - `Closeable`, `Watchable`, not `CardHelpers`
- **Self-contained** - associations, scopes, methods together
- **Not for mere organization** - create when genuine reuse needed

**Touch chains** for cache invalidation:
```ruby
class Comment < ApplicationRecord
  belongs_to :card, touch: true
end

class Card < ApplicationRecord
  belongs_to :board, touch: true
end
```

When comment updates, card's `updated_at` changes, which cascades to board.

**Transaction wrapping** for related updates:
```ruby
class Card < ApplicationRecord
  def close(creator: Current.user)
    transaction do
      create_closure!(creator: creator)
      record_event(:closed)
      notify_watchers_later
    end
  end
end
```
</concern_guidelines>

---

## Reference: Testing

# Testing - DHH Rails Style

## Core Philosophy

"Minitest with fixtures - simple, fast, deterministic." The approach prioritizes pragmatism over convention.

## Why Minitest Over RSpec

- **Simpler**: Less DSL magic, plain Ruby assertions
- **Ships with Rails**: No additional dependencies
- **Faster boot times**: Less overhead
- **Plain Ruby**: No specialized syntax to learn

## Fixtures as Test Data

Rather than factories, fixtures provide preloaded data:
- Loaded once, reused across tests
- No runtime object creation overhead
- Explicit relationship visibility
- Deterministic IDs for easier debugging

### Fixture Structure
```yaml
# test/fixtures/users.yml
david:
  identity: david
  account: basecamp
  role: admin

jason:
  identity: jason
  account: basecamp
  role: member

# test/fixtures/rooms.yml
watercooler:
  name: Water Cooler
  creator: david
  direct: false

# test/fixtures/messages.yml
greeting:
  body: Hello everyone!
  room: watercooler
  creator: david
```

### Using Fixtures in Tests
```ruby
test "sending a message" do
  user = users(:david)
  room = rooms(:watercooler)

  # Test with fixture data
end
```

### Dynamic Fixture Values
ERB enables time-sensitive data:
```yaml
recent_card:
  title: Recent Card
  created_at: <%= 1.hour.ago %>

old_card:
  title: Old Card
  created_at: <%= 1.month.ago %>
```

## Test Organization

### Unit Tests
Verify business logic using setup blocks and standard assertions:

```ruby
class CardTest < ActiveSupport::TestCase
  setup do
    @card = cards(:one)
    @user = users(:david)
  end

  test "closing a card creates a closure" do
    assert_difference -> { Card::Closure.count } do
      @card.close(creator: @user)
    end

    assert @card.closed?
    assert_equal @user, @card.closure.creator
  end

  test "reopening a card destroys the closure" do
    @card.close(creator: @user)

    assert_difference -> { Card::Closure.count }, -1 do
      @card.reopen
    end

    refute @card.closed?
  end
end
```

### Integration Tests
Test full request/response cycles:

```ruby
class CardsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @user = users(:david)
    sign_in @user
  end

  test "closing a card" do
    card = cards(:one)

    post card_closure_path(card)

    assert_response :success
    assert card.reload.closed?
  end

  test "unauthorized user cannot close card" do
    sign_in users(:guest)
    card = cards(:one)

    post card_closure_path(card)

    assert_response :forbidden
    refute card.reload.closed?
  end
end
```

### System Tests
Browser-based tests using Capybara:

```ruby
class MessagesTest < ApplicationSystemTestCase
  test "sending a message" do
    sign_in users(:david)
    visit room_path(rooms(:watercooler))

    fill_in "Message", with: "Hello, world!"
    click_button "Send"

    assert_text "Hello, world!"
  end

  test "editing own message" do
    sign_in users(:david)
    visit room_path(rooms(:watercooler))

    within "#message_#{messages(:greeting).id}" do
      click_on "Edit"
    end

    fill_in "Message", with: "Updated message"
    click_button "Save"

    assert_text "Updated message"
  end

  test "drag and drop card to new column" do
    sign_in users(:david)
    visit board_path(boards(:main))

    card = find("#card_#{cards(:one).id}")
    target = find("#column_#{columns(:done).id}")

    card.drag_to target

    assert_selector "#column_#{columns(:done).id} #card_#{cards(:one).id}"
  end
end
```

## Advanced Patterns

### Time Testing
Use `travel_to` for deterministic time-dependent assertions:

```ruby
test "card expires after 30 days" do
  card = cards(:one)

  travel_to 31.days.from_now do
    assert card.expired?
  end
end
```

### External API Testing with VCR
Record and replay HTTP interactions:

```ruby
test "fetches user data from API" do
  VCR.use_cassette("user_api") do
    user_data = ExternalApi.fetch_user(123)

    assert_equal "John", user_data[:name]
  end
end
```

### Background Job Testing
Assert job enqueueing and email delivery:

```ruby
test "closing card enqueues notification job" do
  card = cards(:one)

  assert_enqueued_with(job: NotifyWatchersJob, args: [card]) do
    card.close
  end
end

test "welcome email is sent on signup" do
  assert_emails 1 do
    Identity.create!(email: "new@example.com")
  end
end
```

### Testing Turbo Streams
```ruby
test "message creation broadcasts to room" do
  room = rooms(:watercooler)

  assert_turbo_stream_broadcasts [room, :messages] do
    room.messages.create!(body: "Test", creator: users(:david))
  end
end
```

## Testing Principles

### 1. Test Observable Behavior
Focus on what the code does, not how it does it:

```ruby
# ❌ Testing implementation
test "calls notify method on each watcher" do
  card.expects(:notify).times(3)
  card.close
end

# ✅ Testing behavior
test "watchers receive notifications when card closes" do
  assert_difference -> { Notification.count }, 3 do
    card.close
  end
end
```

### 2. Don't Mock Everything

```ruby
# ❌ Over-mocked test
test "sending message" do
  room = mock("room")
  user = mock("user")
  message = mock("message")

  room.expects(:messages).returns(stub(create!: message))
  message.expects(:broadcast_create)

  MessagesController.new.create
end

# ✅ Test the real thing
test "sending message" do
  sign_in users(:david)
  post room_messages_url(rooms(:watercooler)),
    params: { message: { body: "Hello" } }

  assert_response :success
  assert Message.exists?(body: "Hello")
end
```

### 3. Tests Ship with Features
Same commit, not TDD-first but together. Neither before (strict TDD) nor after (deferred testing).

### 4. Security Fixes Always Include Regression Tests
Every security fix must include a test that would have caught the vulnerability.

### 5. Integration Tests Validate Complete Workflows
Don't just test individual pieces - test that they work together.

## File Organization

```
test/
├── controllers/         # Integration tests for controllers
├── fixtures/           # YAML fixtures for all models
├── helpers/            # Helper method tests
├── integration/        # API integration tests
├── jobs/               # Background job tests
├── mailers/            # Mailer tests
├── models/             # Unit tests for models
├── system/             # Browser-based system tests
└── test_helper.rb      # Test configuration
```

## Test Helper Setup

```ruby
# test/test_helper.rb
ENV["RAILS_ENV"] ||= "test"
require_relative "../config/environment"
require "rails/test_help"

class ActiveSupport::TestCase
  fixtures :all

  parallelize(workers: :number_of_processors)
end

class ActionDispatch::IntegrationTest
  include SignInHelper
end

class ApplicationSystemTestCase < ActionDispatch::SystemTestCase
  driven_by :selenium, using: :headless_chrome
end
```

## Sign In Helper

```ruby
# test/support/sign_in_helper.rb
module SignInHelper
  def sign_in(user)
    session = user.identity.sessions.create!
    cookies.signed[:session_id] = session.id
  end
end
```
