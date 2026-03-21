---
title: "Rails Expert"
description: "Rails 7+ specialist that optimizes Active Record queries with includes/eager_load, implements Turbo Frames and Turbo Streams for partial page updates, configures Action Cable for WebSocket connections, sets up Sidekiq workers for background job pr..."
category: "development"
source: "community"
author: "Community"
tags: ["rails"]
date: 2026-03-20
---

# Rails Expert

## Core Workflow

1. **Analyze requirements** — Identify models, routes, real-time needs, background jobs
2. **Scaffold resources** — `rails generate model User name:string email:string`, `rails generate controller Users`
3. **Run migrations** — `rails db:migrate` and verify schema with `rails db:schema:dump`
   - If migration fails: inspect `db/schema.rb` for conflicts, rollback with `rails db:rollback`, fix and retry
4. **Implement** — Write controllers, models, add Hotwire (see Reference Guide below)
5. **Validate** — `bundle exec rspec` must pass; `bundle exec rubocop` for style
   - If specs fail: check error output, fix failing examples, re-run with `--format documentation` for detail
   - If N+1 queries surface during review: add `includes`/`eager_load` (see Common Patterns) and re-run specs
6. **Optimize** — Audit for N+1 queries, add missing indexes, add caching

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Hotwire/Turbo | `references/hotwire-turbo.md` | Turbo Frames, Streams, Stimulus controllers |
| Active Record | `references/active-record.md` | Models, associations, queries, performance |
| Background Jobs | `references/background-jobs.md` | Sidekiq, job design, queues, error handling |
| Testing | `references/rspec-testing.md` | Model/request/system specs, factories |
| API Development | `references/api-development.md` | API-only mode, serialization, authentication |

## Common Patterns

### N+1 Prevention with includes/eager_load

```ruby
# BAD — triggers N+1
posts = Post.all
posts.each { |post| puts post.author.name }

# GOOD — eager load association
posts = Post.includes(:author).all
posts.each { |post| puts post.author.name }

# GOOD — eager_load forces a JOIN (useful when filtering on association)
posts = Post.eager_load(:author).where(authors: { verified: true })
```

### Turbo Frame Setup (partial page update)

```erb
<%# app/views/posts/index.html.erb %>
<%= turbo_frame_tag "posts" do %>
  <%= render @posts %>
  <%= link_to "Load More", posts_path(page: @next_page) %>
<% end %>

<%# app/views/posts/_post.html.erb %>
<%= turbo_frame_tag dom_id(post) do %>
  <h2><%= post.title %></h2>
  <%= link_to "Edit", edit_post_path(post) %>
<% end %>
```

```ruby
# app/controllers/posts_controller.rb
def index
  @posts = Post.includes(:author).page(params[:page])
  @next_page = @posts.next_page
end
```

### Sidekiq Worker Template

```ruby
# app/jobs/send_welcome_email_job.rb
class SendWelcomeEmailJob < ApplicationJob
  queue_as :default
  sidekiq_options retry: 3, dead: false

  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  rescue ActiveRecord::RecordNotFound => e
    Rails.logger.warn("SendWelcomeEmailJob: user #{user_id} not found — #{e.message}")
    # Do not re-raise; record is gone, no point retrying
  end
end

# Enqueue from controller or model callback
SendWelcomeEmailJob.perform_later(user.id)
```

### Strong Parameters (controller template)

```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  before_action :set_post, only: %i[show edit update destroy]

  def create
    @post = Post.new(post_params)
    if @post.save
      redirect_to @post, notice: "Post created."
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def post_params
    params.require(:post).permit(:title, :body, :published_at)
  end
end
```

## Constraints

### MUST DO
- Prevent N+1 queries with `includes`/`eager_load` on every collection query involving associations
- Write comprehensive specs targeting >95% coverage
- Use service objects for complex business logic; keep controllers thin
- Add database indexes for every column used in `WHERE`, `ORDER BY`, or `JOIN`
- Offload slow operations to Sidekiq — never run them synchronously in a request cycle

### MUST NOT DO
- Skip migrations for schema changes
- Use raw SQL without sanitization (`sanitize_sql` or parameterized queries only)
- Expose internal IDs in URLs without consideration

## Output Templates

When implementing Rails features, provide:
1. Migration file (if schema changes needed)
2. Model file with associations and validations
3. Controller with RESTful actions and strong parameters
4. View files or Hotwire setup
5. Spec files for models and requests
6. Brief explanation of architectural decisions

---

## Reference: Active Record

# Active Record Patterns

## Model Associations

```ruby
# app/models/user.rb
class User < ApplicationRecord
  has_many :posts, dependent: :destroy
  has_many :comments, dependent: :destroy
  has_many :commented_posts, through: :comments, source: :post

  has_one :profile, dependent: :destroy
  has_one_attached :avatar
  has_many_attached :documents

  validates :email, presence: true, uniqueness: true
  validates :username, presence: true, length: { minimum: 3, maximum: 50 }

  before_save :normalize_email

  private

  def normalize_email
    self.email = email.downcase.strip
  end
end

# app/models/post.rb
class Post < ApplicationRecord
  belongs_to :user
  has_many :comments, dependent: :destroy
  has_many :taggings, dependent: :destroy
  has_many :tags, through: :taggings

  scope :published, -> { where(published: true) }
  scope :recent, -> { order(created_at: :desc) }
  scope :by_user, ->(user) { where(user: user) }

  validates :title, presence: true, length: { maximum: 200 }
  validates :body, presence: true
end
```

## Query Optimization

Prevent N+1 queries:

```ruby
# Bad - N+1 query
@posts = Post.all
@posts.each { |post| puts post.user.name }

# Good - eager loading
@posts = Post.includes(:user)
@posts.each { |post| puts post.user.name }

# Multiple associations
@posts = Post.includes(:user, :comments, :tags)

# Nested associations
@posts = Post.includes(comments: :user)

# Use joins when you don't need the associated records
@posts = Post.joins(:user).where(users: { active: true })
```

Query scopes:

```ruby
class Post < ApplicationRecord
  scope :published, -> { where(published: true) }
  scope :recent, ->(limit = 10) { order(created_at: :desc).limit(limit) }
  scope :by_tag, ->(tag) { joins(:tags).where(tags: { name: tag }) }
  scope :search, ->(query) { where("title ILIKE ?", "%#{sanitize_sql_like(query)}%") }

  # Class method for complex logic
  def self.trending(days = 7)
    where("created_at > ?", days.days.ago)
      .joins(:comments)
      .group(:id)
      .order("COUNT(comments.id) DESC")
  end
end

# Usage
Post.published.recent(5)
Post.by_tag("rails").search("hotwire")
```

## Advanced Queries

```ruby
# Select specific columns
Post.select(:id, :title, :created_at)

# Count and group
User.joins(:posts).group(:id).count
User.joins(:posts).group("users.id").select("users.*, COUNT(posts.id) as posts_count")

# Pluck for arrays
User.pluck(:email)
User.pluck(:id, :email) # Returns array of arrays

# Find by SQL
Post.find_by_sql("SELECT * FROM posts WHERE title ILIKE '%rails%'")

# Exists?
Post.where(published: true).exists?

# Batch processing
User.find_each(batch_size: 1000) do |user|
  user.process_something
end
```

## Callbacks

```ruby
class User < ApplicationRecord
  before_validation :normalize_email
  after_validation :log_errors

  before_create :generate_token
  after_create :send_welcome_email

  before_save :update_slug
  after_save :clear_cache

  before_destroy :cleanup_associations
  after_destroy :log_deletion

  # Avoid callbacks for business logic - use service objects instead

  private

  def normalize_email
    self.email = email.downcase.strip if email.present?
  end

  def generate_token
    self.token = SecureRandom.hex(32)
  end
end
```

## Validations

```ruby
class Article < ApplicationRecord
  validates :title, presence: true, length: { minimum: 5, maximum: 200 }
  validates :slug, uniqueness: { case_sensitive: false }
  validates :published_at, comparison: { greater_than: Time.current }, if: :published?

  validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :age, numericality: { greater_than_or_equal_to: 18 }

  validate :validate_future_date

  private

  def validate_future_date
    if published_at.present? && published_at < Time.current
      errors.add(:published_at, "must be in the future")
    end
  end
end
```

## Migrations

```ruby
# db/migrate/20231214_create_posts.rb
class CreatePosts < ActiveRecord::Migration[7.1]
  def change
    create_table :posts do |t|
      t.string :title, null: false
      t.text :body, null: false
      t.boolean :published, default: false, null: false
      t.references :user, null: false, foreign_key: true

      t.timestamps
    end

    add_index :posts, :published
    add_index :posts, [:user_id, :created_at]
  end
end

# Adding columns
class AddSlugToPosts < ActiveRecord::Migration[7.1]
  def change
    add_column :posts, :slug, :string
    add_index :posts, :slug, unique: true
  end
end

# Data migration
class BackfillUsernames < ActiveRecord::Migration[7.1]
  def up
    User.where(username: nil).find_each do |user|
      user.update_column(:username, "user_#{user.id}")
    end
  end

  def down
    # Usually not needed for data migrations
  end
end
```

## Concerns

```ruby
# app/models/concerns/sluggable.rb
module Sluggable
  extend ActiveSupport::Concern

  included do
    before_validation :generate_slug
    validates :slug, presence: true, uniqueness: true
  end

  private

  def generate_slug
    self.slug ||= title.parameterize if title.present?
  end
end

# Usage in model
class Post < ApplicationRecord
  include Sluggable
end
```

## Performance Tips

- Add database indexes for frequently queried columns
- Use `counter_cache` for associations
- Use `select` to limit columns returned
- Use `pluck` instead of `map` for single attributes
- Use `find_each` for batch processing large datasets
- Use database views for complex queries
- Consider materialized views for expensive aggregations

---

## Reference: Api Development

# API Development

## API-Only Rails Application

```ruby
# Generate API-only app
rails new myapp --api

# config/application.rb
module MyApp
  class Application < Rails::Application
    config.api_only = true
    config.load_defaults 7.1
  end
end

# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  include ActionController::HttpAuthentication::Token::ControllerMethods

  before_action :authenticate

  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity

  private

  def authenticate
    authenticate_token || render_unauthorized
  end

  def authenticate_token
    authenticate_with_http_token do |token, options|
      @current_user = User.find_by(api_token: token)
    end
  end

  def render_unauthorized
    render json: { error: 'Unauthorized' }, status: :unauthorized
  end

  def not_found
    render json: { error: 'Not found' }, status: :not_found
  end

  def unprocessable_entity(exception)
    render json: { errors: exception.record.errors }, status: :unprocessable_entity
  end
end
```

## RESTful API Controller

```ruby
# app/controllers/api/v1/posts_controller.rb
module Api
  module V1
    class PostsController < ApplicationController
      before_action :set_post, only: [:show, :update, :destroy]

      # GET /api/v1/posts
      def index
        @posts = Post.includes(:user)
                    .page(params[:page])
                    .per(params[:per_page] || 20)

        render json: @posts, meta: pagination_meta(@posts)
      end

      # GET /api/v1/posts/:id
      def show
        render json: @post, include: [:user, :comments]
      end

      # POST /api/v1/posts
      def create
        @post = current_user.posts.build(post_params)

        if @post.save
          render json: @post, status: :created, location: api_v1_post_url(@post)
        else
          render json: { errors: @post.errors }, status: :unprocessable_entity
        end
      end

      # PATCH/PUT /api/v1/posts/:id
      def update
        if @post.update(post_params)
          render json: @post
        else
          render json: { errors: @post.errors }, status: :unprocessable_entity
        end
      end

      # DELETE /api/v1/posts/:id
      def destroy
        @post.destroy
        head :no_content
      end

      private

      def set_post
        @post = Post.find(params[:id])
      end

      def post_params
        params.require(:post).permit(:title, :body, :published)
      end

      def pagination_meta(collection)
        {
          current_page: collection.current_page,
          total_pages: collection.total_pages,
          total_count: collection.total_count
        }
      end
    end
  end
end
```

## Serialization with ActiveModel::Serializers

```ruby
# Gemfile
gem 'active_model_serializers'

# app/serializers/post_serializer.rb
class PostSerializer < ActiveModel::Serializer
  attributes :id, :title, :body, :published, :created_at

  belongs_to :user
  has_many :comments

  # Conditional attributes
  attribute :draft_content, if: :current_user_is_author?

  # Custom attributes
  def published_date
    object.created_at.strftime("%Y-%m-%d")
  end

  private

  def current_user_is_author?
    current_user == object.user
  end
end

# app/serializers/user_serializer.rb
class UserSerializer < ActiveModel::Serializer
  attributes :id, :username, :email

  # Exclude sensitive data
  def email
    return nil unless current_user&.admin?
    object.email
  end
end
```

## JWT Authentication

```ruby
# Gemfile
gem 'jwt'

# app/lib/json_web_token.rb
class JsonWebToken
  SECRET_KEY = Rails.application.credentials.secret_key_base

  def self.encode(payload, exp = 24.hours.from_now)
    payload[:exp] = exp.to_i
    JWT.encode(payload, SECRET_KEY)
  end

  def self.decode(token)
    decoded = JWT.decode(token, SECRET_KEY)[0]
    HashWithIndifferentAccess.new(decoded)
  rescue JWT::DecodeError
    nil
  end
end

# app/controllers/api/v1/authentication_controller.rb
module Api
  module V1
    class AuthenticationController < ApplicationController
      skip_before_action :authenticate, only: [:create]

      # POST /api/v1/auth/login
      def create
        user = User.find_by(email: params[:email])

        if user&.authenticate(params[:password])
          token = JsonWebToken.encode(user_id: user.id)
          render json: { token: token, user: UserSerializer.new(user) }
        else
          render json: { error: 'Invalid credentials' }, status: :unauthorized
        end
      end
    end
  end
end

# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  before_action :authenticate_request

  attr_reader :current_user

  private

  def authenticate_request
    header = request.headers['Authorization']
    token = header.split(' ').last if header

    decoded = JsonWebToken.decode(token)
    @current_user = User.find(decoded[:user_id]) if decoded

    render json: { error: 'Unauthorized' }, status: :unauthorized unless @current_user
  rescue ActiveRecord::RecordNotFound
    render json: { error: 'Unauthorized' }, status: :unauthorized
  end
end
```

## API Versioning

```ruby
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :posts
      resources :users

      post '/auth/login', to: 'authentication#create'
    end

    namespace :v2 do
      resources :posts
    end
  end
end

# app/controllers/api/v1/base_controller.rb
module Api
  module V1
    class BaseController < ApplicationController
      # V1 specific logic
    end
  end
end
```

## Rate Limiting

```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
class Rack::Attack
  # Throttle all requests by IP
  throttle('req/ip', limit: 300, period: 5.minutes) do |req|
    req.ip
  end

  # Throttle login attempts by email
  throttle('logins/email', limit: 5, period: 20.seconds) do |req|
    if req.path == '/api/v1/auth/login' && req.post?
      req.params['email'].to_s.downcase.gsub(/\s+/, "")
    end
  end

  # Block suspicious requests
  blocklist('block bad IPs') do |req|
    # Requests are blocked if the return value is truthy
    BadIpList.include?(req.ip)
  end
end

# config/application.rb
config.middleware.use Rack::Attack
```

## CORS Configuration

```ruby
# Gemfile
gem 'rack-cors'

# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'localhost:3000', 'example.com'

    resource '*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head],
      credentials: true
  end
end
```

## API Documentation with RSwag

```ruby
# Gemfile
gem 'rswag'

# spec/requests/api/v1/posts_spec.rb
require 'swagger_helper'

RSpec.describe 'Posts API', type: :request do
  path '/api/v1/posts' do
    get 'Retrieves posts' do
      tags 'Posts'
      produces 'application/json'
      parameter name: :page, in: :query, type: :integer, required: false

      response '200', 'posts found' do
        schema type: :array,
          items: {
            type: :object,
            properties: {
              id: { type: :integer },
              title: { type: :string },
              body: { type: :string }
            }
          }

        run_test!
      end
    end

    post 'Creates a post' do
      tags 'Posts'
      consumes 'application/json'
      parameter name: :post, in: :body, schema: {
        type: :object,
        properties: {
          title: { type: :string },
          body: { type: :string }
        },
        required: ['title', 'body']
      }

      response '201', 'post created' do
        let(:post) { { title: 'Test', body: 'Content' } }
        run_test!
      end
    end
  end
end
```

## Error Handling

```ruby
# app/controllers/concerns/error_handler.rb
module ErrorHandler
  extend ActiveSupport::Concern

  included do
    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
    rescue_from ActionController::ParameterMissing, with: :bad_request
  end

  private

  def not_found(exception)
    render json: { error: exception.message }, status: :not_found
  end

  def unprocessable_entity(exception)
    render json: { errors: exception.record.errors.full_messages },
           status: :unprocessable_entity
  end

  def bad_request(exception)
    render json: { error: exception.message }, status: :bad_request
  end
end
```

## Best Practices

- Use semantic versioning for API versions
- Return proper HTTP status codes
- Include pagination for list endpoints
- Use JSON:API or similar standard format
- Document API with OpenAPI/Swagger
- Implement rate limiting and throttling
- Use HTTPS in production
- Validate and sanitize all inputs
- Include API versioning in URL or headers
- Provide helpful error messages

---

## Reference: Background Jobs

# Background Jobs with Sidekiq

## Sidekiq Setup

```ruby
# Gemfile
gem 'sidekiq'
gem 'sidekiq-cron' # Optional: scheduled jobs

# config/initializers/sidekiq.rb
Sidekiq.configure_server do |config|
  config.redis = { url: ENV['REDIS_URL'] || 'redis://localhost:6379/0' }
end

Sidekiq.configure_client do |config|
  config.redis = { url: ENV['REDIS_URL'] || 'redis://localhost:6379/0' }
end

# config/sidekiq.yml
:concurrency: 5
:queues:
  - critical
  - default
  - low
```

## Basic Job Design

```ruby
# app/jobs/email_sender_job.rb
class EmailSenderJob < ApplicationJob
  queue_as :default

  def perform(user_id, email_type)
    user = User.find(user_id)
    UserMailer.send(email_type, user).deliver_now
  end
end

# Usage
EmailSenderJob.perform_later(user.id, :welcome)

# Perform at specific time
EmailSenderJob.set(wait: 1.hour).perform_later(user.id, :reminder)
EmailSenderJob.set(wait_until: Date.tomorrow.noon).perform_later(user.id, :digest)
```

## Queue Priority

```ruby
class CriticalJob < ApplicationJob
  queue_as :critical

  def perform
    # High priority work
  end
end

class ReportGenerationJob < ApplicationJob
  queue_as :low

  def perform
    # Can wait
  end
end
```

## Retry Strategy

```ruby
class ImportJob < ApplicationJob
  # Retry up to 5 times with exponential backoff
  sidekiq_options retry: 5

  # Custom retry logic
  sidekiq_retry_in do |count, exception|
    case exception
    when NetworkError
      10 * (count + 1) # 10, 20, 30 seconds
    when RateLimitError
      1.hour
    else
      :default # Use Sidekiq's default exponential backoff
    end
  end

  def perform(data_url)
    # Import logic
  end
end
```

## Error Handling

```ruby
class ProcessPaymentJob < ApplicationJob
  sidekiq_options retry: 3

  # Called when job fails after all retries
  sidekiq_retries_exhausted do |msg, exception|
    Rails.logger.error("Payment job failed: #{msg}")

    # Notify admin
    AdminMailer.job_failed(msg, exception).deliver_now

    # Store failure record
    FailedPayment.create(
      user_id: msg['args'][0],
      error: exception.message
    )
  end

  def perform(user_id, amount)
    user = User.find(user_id)
    PaymentProcessor.charge(user, amount)
  rescue PaymentError => e
    # Log and re-raise to trigger retry
    Rails.logger.warn("Payment failed: #{e.message}")
    raise
  end
end
```

## Batch Processing

```ruby
class BulkEmailJob < ApplicationJob
  def perform(user_ids)
    # Process in batches to avoid memory issues
    user_ids.in_groups_of(100, false) do |batch|
      batch.each do |user_id|
        user = User.find(user_id)
        UserMailer.newsletter(user).deliver_now
      end
    end
  end
end

# Better: Use Sidekiq::Batch (requires sidekiq-pro)
class ParentJob < ApplicationJob
  def perform(user_ids)
    batch = Sidekiq::Batch.new
    batch.on(:success, self.class, 'user_ids' => user_ids)

    batch.jobs do
      user_ids.each do |user_id|
        ChildJob.perform_later(user_id)
      end
    end
  end

  def on_success(status, options)
    # All child jobs completed
    Rails.logger.info("Processed #{options['user_ids'].length} users")
  end
end
```

## Scheduled Jobs

```ruby
# Using sidekiq-cron
# config/initializers/sidekiq.rb
schedule_file = "config/schedule.yml"

if File.exist?(schedule_file) && Sidekiq.server?
  Sidekiq::Cron::Job.load_from_hash YAML.load_file(schedule_file)
end

# config/schedule.yml
daily_report:
  cron: "0 6 * * *"
  class: "DailyReportJob"
  queue: default

cleanup_old_records:
  cron: "0 2 * * 0" # Sunday at 2am
  class: "CleanupJob"
  queue: low
```

## Job Patterns

Idempotent jobs:

```ruby
class ProcessOrderJob < ApplicationJob
  def perform(order_id)
    order = Order.find(order_id)

    # Check if already processed
    return if order.processed?

    # Process order
    order.process!
  end
end
```

Unique jobs (requires sidekiq-unique-jobs gem):

```ruby
class GenerateReportJob < ApplicationJob
  sidekiq_options lock: :until_executed,
                   on_conflict: :log

  def perform(user_id, report_type)
    # Only one instance of this job per user+report_type
  end
end
```

## Testing

```ruby
# spec/jobs/email_sender_job_spec.rb
require 'rails_helper'

RSpec.describe EmailSenderJob, type: :job do
  let(:user) { create(:user) }

  describe "#perform" do
    it "sends welcome email" do
      expect {
        described_class.perform_now(user.id, :welcome)
      }.to change { ActionMailer::Base.deliveries.count }.by(1)
    end

    it "enqueues job" do
      expect {
        described_class.perform_later(user.id, :welcome)
      }.to have_enqueued_job(described_class)
        .with(user.id, :welcome)
        .on_queue("default")
    end
  end
end

# Test inline in development
# config/environments/test.rb
config.active_job.queue_adapter = :inline
```

## Monitoring

```ruby
# Check queue size
Sidekiq::Queue.new("default").size

# Check scheduled jobs
Sidekiq::ScheduledSet.new.size

# Check retry set
Sidekiq::RetrySet.new.size

# Check dead jobs
Sidekiq::DeadSet.new.size

# Clear queues (use with caution)
Sidekiq::Queue.new("default").clear
```

## Performance Tips

- Keep jobs small and focused
- Pass IDs, not objects (serialize/deserialize issue)
- Use appropriate queue priorities
- Set realistic retry limits
- Monitor queue depth and latency
- Scale workers based on load
- Use Redis persistence for job durability
- Consider job uniqueness to prevent duplicates

---

## Reference: Hotwire Turbo

# Hotwire & Turbo

## Turbo Drive

Turbo Drive automatically converts link clicks and form submissions into AJAX requests:

```ruby
# app/controllers/articles_controller.rb
class ArticlesController < ApplicationController
  def create
    @article = Article.new(article_params)

    if @article.save
      redirect_to @article, notice: "Article created!"
    else
      render :new, status: :unprocessable_entity
    end
  end
end
```

```erb
<!-- app/views/articles/new.html.erb -->
<%= form_with model: @article do |f| %>
  <%= f.text_field :title %>
  <%= f.text_area :body %>
  <%= f.submit %>
<% end %>
```

## Turbo Frames

Turbo Frames enable scoped page updates:

```erb
<!-- app/views/articles/show.html.erb -->
<%= turbo_frame_tag "article_#{@article.id}" do %>
  <h1><%= @article.title %></h1>
  <p><%= @article.body %></p>
  <%= link_to "Edit", edit_article_path(@article) %>
<% end %>

<!-- app/views/articles/edit.html.erb -->
<%= turbo_frame_tag "article_#{@article.id}" do %>
  <%= form_with model: @article do |f| %>
    <%= f.text_field :title %>
    <%= f.text_area :body %>
    <%= f.submit %>
  <% end %>
<% end %>
```

Lazy loading with Turbo Frames:

```erb
<%= turbo_frame_tag "expensive_content", src: expensive_content_path, loading: :lazy %>
```

## Turbo Streams

Real-time updates with Turbo Streams:

```ruby
# app/controllers/comments_controller.rb
class CommentsController < ApplicationController
  def create
    @comment = @article.comments.create(comment_params)

    respond_to do |format|
      format.turbo_stream
      format.html { redirect_to @article }
    end
  end
end
```

```erb
<!-- app/views/comments/create.turbo_stream.erb -->
<%= turbo_stream.append "comments" do %>
  <%= render @comment %>
<% end %>

<%= turbo_stream.update "comment_form" do %>
  <%= render "comments/form", comment: Comment.new %>
<% end %>
```

Broadcasting with Action Cable:

```ruby
# app/models/comment.rb
class Comment < ApplicationRecord
  belongs_to :article

  after_create_commit -> { broadcast_append_to article, target: "comments" }
  after_update_commit -> { broadcast_replace_to article }
  after_destroy_commit -> { broadcast_remove_to article }
end
```

```erb
<!-- app/views/articles/show.html.erb -->
<%= turbo_stream_from @article %>

<div id="comments">
  <%= render @article.comments %>
</div>
```

## Stimulus Controllers

JavaScript sprinkles with Stimulus:

```javascript
// app/javascript/controllers/dropdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["menu"]

  toggle() {
    this.menuTarget.classList.toggle("hidden")
  }

  hide(event) {
    if (!this.element.contains(event.target)) {
      this.menuTarget.classList.add("hidden")
    }
  }
}
```

```erb
<!-- app/views/shared/_dropdown.html.erb -->
<div data-controller="dropdown" data-action="click@window->dropdown#hide">
  <button data-action="dropdown#toggle">Menu</button>
  <div data-dropdown-target="menu" class="hidden">
    <a href="#">Item 1</a>
    <a href="#">Item 2</a>
  </div>
</div>
```

## Form Validation with Stimulus

```javascript
// app/javascript/controllers/form_validator_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "error"]

  validate() {
    const value = this.inputTarget.value

    if (value.length < 3) {
      this.errorTarget.textContent = "Must be at least 3 characters"
      this.inputTarget.classList.add("border-red-500")
    } else {
      this.errorTarget.textContent = ""
      this.inputTarget.classList.remove("border-red-500")
    }
  }
}
```

## Turbo Stream Actions

Seven core actions:

```ruby
# append, prepend, replace, update, remove, before, after
turbo_stream.append "target_id", partial: "item", locals: { item: @item }
turbo_stream.prepend "target_id", html: content
turbo_stream.replace "target_id", @item
turbo_stream.update "target_id", html: "<p>Updated</p>"
turbo_stream.remove "target_id"
turbo_stream.before "target_id", partial: "item"
turbo_stream.after "target_id", partial: "item"
```

## Progressive Enhancement

Start with working HTML, enhance with Turbo:

```erb
<!-- Works without JavaScript -->
<%= form_with model: @article, url: articles_path do |f| %>
  <%= f.text_field :title %>
  <%= f.submit %>
<% end %>

<!-- Enhanced with Turbo Frame -->
<%= turbo_frame_tag "article_form" do %>
  <%= form_with model: @article do |f| %>
    <%= f.text_field :title %>
    <%= f.submit %>
  <% end %>
<% end %>
```

## Common Patterns

Inline editing:

```erb
<%= turbo_frame_tag dom_id(@article, :title) do %>
  <%= link_to @article.title, edit_article_path(@article),
              data: { turbo_frame: dom_id(@article, :title) } %>
<% end %>
```

Modal dialogs:

```erb
<%= turbo_frame_tag "modal" %>

<%= link_to "Open Modal", new_article_path,
            data: { turbo_frame: "modal" } %>
```

## Performance Tips

- Use lazy loading for off-screen frames
- Debounce Stimulus actions for search/autocomplete
- Cache Turbo Stream partials
- Use morphing for minimal DOM updates
- Minimize frame nesting depth

---

## Reference: Rspec Testing

# RSpec Testing

## RSpec Setup

```ruby
# Gemfile
group :development, :test do
  gem 'rspec-rails'
  gem 'factory_bot_rails'
  gem 'faker'
end

group :test do
  gem 'shoulda-matchers'
  gem 'simplecov', require: false
  gem 'capybara'
  gem 'selenium-webdriver'
end

# spec/rails_helper.rb
require 'simplecov'
SimpleCov.start 'rails' do
  add_filter '/spec/'
  add_filter '/config/'
  minimum_coverage 95
end

RSpec.configure do |config|
  config.include FactoryBot::Syntax::Methods

  config.before(:suite) do
    DatabaseCleaner.strategy = :transaction
    DatabaseCleaner.clean_with(:truncation)
  end

  config.around(:each) do |example|
    DatabaseCleaner.cleaning do
      example.run
    end
  end
end

# spec/support/shoulda_matchers.rb
Shoulda::Matchers.configure do |config|
  config.integrate do |with|
    with.test_framework :rspec
    with.library :rails
  end
end
```

## Model Specs

```ruby
# spec/models/user_spec.rb
require 'rails_helper'

RSpec.describe User, type: :model do
  describe "associations" do
    it { should have_many(:posts).dependent(:destroy) }
    it { should have_one(:profile).dependent(:destroy) }
    it { should have_many(:comments) }
  end

  describe "validations" do
    it { should validate_presence_of(:email) }
    it { should validate_uniqueness_of(:email).case_insensitive }
    it { should validate_length_of(:username).is_at_least(3).is_at_most(50) }

    it "validates email format" do
      user = build(:user, email: "invalid")
      expect(user).not_to be_valid
      expect(user.errors[:email]).to include("is invalid")
    end
  end

  describe "callbacks" do
    it "normalizes email before save" do
      user = create(:user, email: "USER@EXAMPLE.COM")
      expect(user.reload.email).to eq("user@example.com")
    end
  end

  describe "#full_name" do
    it "returns first and last name" do
      user = build(:user, first_name: "John", last_name: "Doe")
      expect(user.full_name).to eq("John Doe")
    end
  end

  describe "scopes" do
    let!(:active_user) { create(:user, active: true) }
    let!(:inactive_user) { create(:user, active: false) }

    it "returns only active users" do
      expect(User.active).to include(active_user)
      expect(User.active).not_to include(inactive_user)
    end
  end
end
```

## Request Specs

```ruby
# spec/requests/posts_spec.rb
require 'rails_helper'

RSpec.describe "/posts", type: :request do
  let(:user) { create(:user) }
  let(:valid_attributes) { { title: "Test Post", body: "Content" } }
  let(:invalid_attributes) { { title: "", body: "" } }

  before { sign_in user } # Using Devise helper

  describe "GET /index" do
    it "renders a successful response" do
      create_list(:post, 3)
      get posts_url
      expect(response).to be_successful
    end
  end

  describe "GET /show" do
    it "renders a successful response" do
      post = create(:post)
      get post_url(post)
      expect(response).to be_successful
    end
  end

  describe "POST /create" do
    context "with valid parameters" do
      it "creates a new Post" do
        expect {
          post posts_url, params: { post: valid_attributes }
        }.to change(Post, :count).by(1)
      end

      it "redirects to the created post" do
        post posts_url, params: { post: valid_attributes }
        expect(response).to redirect_to(post_url(Post.last))
      end
    end

    context "with invalid parameters" do
      it "does not create a new Post" do
        expect {
          post posts_url, params: { post: invalid_attributes }
        }.not_to change(Post, :count)
      end

      it "renders unprocessable entity response" do
        post posts_url, params: { post: invalid_attributes }
        expect(response).to have_http_status(:unprocessable_entity)
      end
    end
  end

  describe "PATCH /update" do
    let(:post_record) { create(:post, user: user) }
    let(:new_attributes) { { title: "Updated Title" } }

    it "updates the requested post" do
      patch post_url(post_record), params: { post: new_attributes }
      post_record.reload
      expect(post_record.title).to eq("Updated Title")
    end

    it "redirects to the post" do
      patch post_url(post_record), params: { post: new_attributes }
      expect(response).to redirect_to(post_url(post_record))
    end
  end

  describe "DELETE /destroy" do
    it "destroys the requested post" do
      post_record = create(:post, user: user)
      expect {
        delete post_url(post_record)
      }.to change(Post, :count).by(-1)
    end
  end
end
```

## System Specs (Feature Tests)

```ruby
# spec/system/posts_spec.rb
require 'rails_helper'

RSpec.describe "Posts", type: :system do
  before do
    driven_by(:selenium_chrome_headless)
  end

  let(:user) { create(:user) }

  describe "creating a post" do
    it "allows user to create a new post" do
      sign_in user
      visit new_post_path

      fill_in "Title", with: "My New Post"
      fill_in "Body", with: "This is the content"
      click_button "Create Post"

      expect(page).to have_content("Post was successfully created")
      expect(page).to have_content("My New Post")
    end
  end

  describe "editing a post", js: true do
    it "updates post via Turbo Frame" do
      post = create(:post, user: user)
      sign_in user
      visit post_path(post)

      click_link "Edit"
      fill_in "Title", with: "Updated Title"
      click_button "Update Post"

      expect(page).to have_content("Updated Title")
      expect(page).not_to have_selector("form")
    end
  end
end
```

## FactoryBot

```ruby
# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    email { Faker::Internet.email }
    username { Faker::Internet.username(specifier: 3..50) }
    password { "Password123!" }

    trait :admin do
      role { :admin }
    end

    trait :with_posts do
      transient do
        posts_count { 3 }
      end

      after(:create) do |user, evaluator|
        create_list(:post, evaluator.posts_count, user: user)
      end
    end
  end

  factory :post do
    title { Faker::Lorem.sentence }
    body { Faker::Lorem.paragraph }
    association :user

    trait :published do
      published { true }
      published_at { Time.current }
    end
  end
end

# Usage
user = create(:user)
admin = create(:user, :admin)
user_with_posts = create(:user, :with_posts, posts_count: 5)
published_post = create(:post, :published)
```

## Shared Examples

```ruby
# spec/support/shared_examples/authenticatable.rb
RSpec.shared_examples "authenticatable" do
  describe "authentication" do
    context "when not signed in" do
      it "redirects to sign in page" do
        make_request
        expect(response).to redirect_to(new_user_session_path)
      end
    end

    context "when signed in" do
      before { sign_in create(:user) }

      it "allows access" do
        make_request
        expect(response).to be_successful
      end
    end
  end
end

# Usage in request spec
RSpec.describe "/admin/posts", type: :request do
  include_examples "authenticatable" do
    let(:make_request) { get admin_posts_path }
  end
end
```

## Testing Jobs

```ruby
# spec/jobs/email_sender_job_spec.rb
require 'rails_helper'

RSpec.describe EmailSenderJob, type: :job do
  describe "#perform" do
    let(:user) { create(:user) }

    it "sends email" do
      expect {
        described_class.perform_now(user.id, :welcome)
      }.to change { ActionMailer::Base.deliveries.count }.by(1)
    end

    it "enqueues job" do
      expect {
        described_class.perform_later(user.id, :welcome)
      }.to have_enqueued_job(described_class)
        .with(user.id, :welcome)
        .on_queue("default")
    end
  end
end
```

## Testing Mailers

```ruby
# spec/mailers/user_mailer_spec.rb
require 'rails_helper'

RSpec.describe UserMailer, type: :mailer do
  describe "welcome_email" do
    let(:user) { create(:user) }
    let(:mail) { UserMailer.welcome_email(user) }

    it "renders the headers" do
      expect(mail.subject).to eq("Welcome to Our App")
      expect(mail.to).to eq([user.email])
      expect(mail.from).to eq(["noreply@example.com"])
    end

    it "renders the body" do
      expect(mail.body.encoded).to match(user.username)
    end
  end
end
```

## Best Practices

- Use `let` and `let!` for DRY specs
- Use factories, not fixtures
- One assertion per example when possible
- Use descriptive test names
- Test edge cases and error conditions
- Keep tests fast (use build instead of create when possible)
- Use `travel_to` for time-dependent tests
- Mock external API calls
