---
title: "Andrew Kane Gem Writer"
description: "This skill should be used when writing Ruby gems following Andrew Kane's proven patterns and philosophy. It applies when creating new Ruby gems, refactoring existing gems, designing gem APIs, or when clean, minimal, production-ready Ruby library c..."
category: "writing"
source: "community"
author: "Community"
tags: ["andrew", "kane", "gem", "writer"]
date: 2026-03-20
---

# Andrew Kane Gem Writer

Write Ruby gems following Andrew Kane's battle-tested patterns from 100+ gems with 374M+ downloads (Searchkick, PgHero, Chartkick, Strong Migrations, Lockbox, Ahoy, Blazer, Groupdate, Neighbor, Blind Index).

## Core Philosophy

**Simplicity over cleverness.** Zero or minimal dependencies. Explicit code over metaprogramming. Rails integration without Rails coupling. Every pattern serves production use cases.

## Entry Point Structure

Every gem follows this exact pattern in `lib/gemname.rb`:

```ruby
# 1. Dependencies (stdlib preferred)
require "forwardable"

# 2. Internal modules
require_relative "gemname/model"
require_relative "gemname/version"

# 3. Conditional Rails (CRITICAL - never require Rails directly)
require_relative "gemname/railtie" if defined?(Rails)

# 4. Module with config and errors
module GemName
  class Error < StandardError; end
  class InvalidConfigError < Error; end

  class << self
    attr_accessor :timeout, :logger
    attr_writer :client
  end

  self.timeout = 10  # Defaults set immediately
end
```

## Class Macro DSL Pattern

The signature Kane pattern—single method call configures everything:

```ruby
# Usage
class Product < ApplicationRecord
  searchkick word_start: [:name]
end

# Implementation
module GemName
  module Model
    def gemname(**options)
      unknown = options.keys - KNOWN_KEYWORDS
      raise ArgumentError, "unknown keywords: #{unknown.join(", ")}" if unknown.any?

      mod = Module.new
      mod.module_eval do
        define_method :some_method do
          # implementation
        end unless method_defined?(:some_method)
      end
      include mod

      class_eval do
        cattr_reader :gemname_options, instance_reader: false
        class_variable_set :@@gemname_options, options.dup
      end
    end
  end
end
```

## Rails Integration

**Always use `ActiveSupport.on_load`—never require Rails gems directly:**

```ruby
# WRONG
require "active_record"
ActiveRecord::Base.include(MyGem::Model)

# CORRECT
ActiveSupport.on_load(:active_record) do
  extend GemName::Model
end

# Use prepend for behavior modification
ActiveSupport.on_load(:active_record) do
  ActiveRecord::Migration.prepend(GemName::Migration)
end
```

## Configuration Pattern

Use `class << self` with `attr_accessor`, not Configuration objects:

```ruby
module GemName
  class << self
    attr_accessor :timeout, :logger
    attr_writer :master_key
  end

  def self.master_key
    @master_key ||= ENV["GEMNAME_MASTER_KEY"]
  end

  self.timeout = 10
  self.logger = nil
end
```

## Error Handling

Simple hierarchy with informative messages:

```ruby
module GemName
  class Error < StandardError; end
  class ConfigError < Error; end
  class ValidationError < Error; end
end

# Validate early with ArgumentError
def initialize(key:)
  raise ArgumentError, "Key must be 32 bytes" unless key&.bytesize == 32
end
```

## Testing (Minitest Only)

```ruby
# test/test_helper.rb
require "bundler/setup"
Bundler.require(:default)
require "minitest/autorun"
require "minitest/pride"

# test/model_test.rb
class ModelTest < Minitest::Test
  def test_basic_functionality
    assert_equal expected, actual
  end
end
```

## Gemspec Pattern

Zero runtime dependencies when possible:

```ruby
Gem::Specification.new do |spec|
  spec.name = "gemname"
  spec.version = GemName::VERSION
  spec.required_ruby_version = ">= 3.1"
  spec.files = Dir["*.{md,txt}", "{lib}/**/*"]
  spec.require_path = "lib"
  # NO add_dependency lines - dev deps go in Gemfile
end
```

## Anti-Patterns to Avoid

- `method_missing` (use `define_method` instead)
- Configuration objects (use class accessors)
- `@@class_variables` (use `class << self`)
- Requiring Rails gems directly
- Many runtime dependencies
- Committing Gemfile.lock in gems
- RSpec (use Minitest)
- Heavy DSLs (prefer explicit Ruby)

## Reference Files

For deeper patterns, see:
- **[references/module-organization.md](references/module-organization.md)** - Directory layouts, method decomposition
- **[references/rails-integration.md](references/rails-integration.md)** - Railtie, Engine, on_load patterns
- **[references/database-adapters.md](references/database-adapters.md)** - Multi-database support patterns
- **[references/testing-patterns.md](references/testing-patterns.md)** - Multi-version testing, CI setup
- **[references/resources.md](references/resources.md)** - Links to Kane's repos and articles

---

## Reference: Database Adapters

# Database Adapter Patterns

## Abstract Base Class Pattern

```ruby
# lib/strong_migrations/adapters/abstract_adapter.rb
module StrongMigrations
  module Adapters
    class AbstractAdapter
      def initialize(checker)
        @checker = checker
      end

      def min_version
        nil
      end

      def set_statement_timeout(timeout)
        # no-op by default
      end

      def check_lock_timeout
        # no-op by default
      end

      private

      def connection
        @checker.send(:connection)
      end

      def quote(value)
        connection.quote(value)
      end
    end
  end
end
```

## PostgreSQL Adapter

```ruby
# lib/strong_migrations/adapters/postgresql_adapter.rb
module StrongMigrations
  module Adapters
    class PostgreSQLAdapter < AbstractAdapter
      def min_version
        "12"
      end

      def set_statement_timeout(timeout)
        select_all("SET statement_timeout = #{timeout.to_i * 1000}")
      end

      def set_lock_timeout(timeout)
        select_all("SET lock_timeout = #{timeout.to_i * 1000}")
      end

      def check_lock_timeout
        lock_timeout = connection.select_value("SHOW lock_timeout")
        lock_timeout_sec = timeout_to_sec(lock_timeout)
        # validation logic
      end

      private

      def select_all(sql)
        connection.select_all(sql)
      end

      def timeout_to_sec(timeout)
        units = {"us" => 1e-6, "ms" => 1e-3, "s" => 1, "min" => 60}
        timeout.to_f * (units[timeout.gsub(/\d+/, "")] || 1e-3)
      end
    end
  end
end
```

## MySQL Adapter

```ruby
# lib/strong_migrations/adapters/mysql_adapter.rb
module StrongMigrations
  module Adapters
    class MySQLAdapter < AbstractAdapter
      def min_version
        "8.0"
      end

      def set_statement_timeout(timeout)
        select_all("SET max_execution_time = #{timeout.to_i * 1000}")
      end

      def check_lock_timeout
        lock_timeout = connection.select_value("SELECT @@lock_wait_timeout")
        # validation logic
      end
    end
  end
end
```

## MariaDB Adapter (MySQL variant)

```ruby
# lib/strong_migrations/adapters/mariadb_adapter.rb
module StrongMigrations
  module Adapters
    class MariaDBAdapter < MySQLAdapter
      def min_version
        "10.5"
      end

      # Override MySQL-specific behavior
      def set_statement_timeout(timeout)
        select_all("SET max_statement_time = #{timeout.to_i}")
      end
    end
  end
end
```

## Adapter Detection Pattern

Use regex matching on adapter name:

```ruby
def adapter
  @adapter ||= case connection.adapter_name
    when /postg/i
      Adapters::PostgreSQLAdapter.new(self)
    when /mysql|trilogy/i
      if connection.try(:mariadb?)
        Adapters::MariaDBAdapter.new(self)
      else
        Adapters::MySQLAdapter.new(self)
      end
    when /sqlite/i
      Adapters::SQLiteAdapter.new(self)
    else
      Adapters::AbstractAdapter.new(self)
    end
end
```

## Multi-Database Support (PgHero pattern)

```ruby
module PgHero
  class << self
    attr_accessor :databases
  end

  self.databases = {}

  def self.primary_database
    databases.values.first
  end

  def self.capture_query_stats(database: nil)
    db = database ? databases[database] : primary_database
    db.capture_query_stats
  end

  class Database
    attr_reader :id, :config

    def initialize(id, config)
      @id = id
      @config = config
    end

    def connection_model
      @connection_model ||= begin
        Class.new(ActiveRecord::Base) do
          self.abstract_class = true
        end.tap do |model|
          model.establish_connection(config)
        end
      end
    end

    def connection
      connection_model.connection
    end
  end
end
```

## Connection Switching

```ruby
def with_connection(database_name)
  db = databases[database_name.to_s]
  raise Error, "Unknown database: #{database_name}" unless db

  yield db.connection
end

# Usage
PgHero.with_connection(:replica) do |conn|
  conn.execute("SELECT * FROM users")
end
```

## SQL Dialect Handling

```ruby
def quote_column(column)
  case adapter_name
  when /postg/i
    %("#{column}")
  when /mysql/i
    "`#{column}`"
  else
    column
  end
end

def boolean_value(value)
  case adapter_name
  when /postg/i
    value ? "true" : "false"
  when /mysql/i
    value ? "1" : "0"
  else
    value.to_s
  end
end
```

---

## Reference: Module Organization

# Module Organization Patterns

## Simple Gem Layout

```
lib/
├── gemname.rb          # Entry point, config, errors
└── gemname/
    ├── helper.rb       # Core functionality
    ├── engine.rb       # Rails engine (if needed)
    └── version.rb      # VERSION constant only
```

## Complex Gem Layout (PgHero pattern)

```
lib/
├── pghero.rb
└── pghero/
    ├── database.rb     # Main class
    ├── engine.rb       # Rails engine
    └── methods/        # Functional decomposition
        ├── basic.rb
        ├── connections.rb
        ├── indexes.rb
        ├── queries.rb
        └── replication.rb
```

## Method Decomposition Pattern

Break large classes into includable modules by feature:

```ruby
# lib/pghero/database.rb
module PgHero
  class Database
    include Methods::Basic
    include Methods::Connections
    include Methods::Indexes
    include Methods::Queries
  end
end

# lib/pghero/methods/indexes.rb
module PgHero
  module Methods
    module Indexes
      def index_hit_rate
        # implementation
      end

      def unused_indexes
        # implementation
      end
    end
  end
end
```

## Version File Pattern

Keep version.rb minimal:

```ruby
# lib/gemname/version.rb
module GemName
  VERSION = "2.0.0"
end
```

## Require Order in Entry Point

```ruby
# lib/searchkick.rb

# 1. Standard library
require "forwardable"
require "json"

# 2. External dependencies (minimal)
require "active_support"

# 3. Internal files via require_relative
require_relative "searchkick/index"
require_relative "searchkick/model"
require_relative "searchkick/query"
require_relative "searchkick/version"

# 4. Conditional Rails loading (LAST)
require_relative "searchkick/railtie" if defined?(Rails)
```

## Autoload vs Require

Kane uses explicit `require_relative`, not autoload:

```ruby
# CORRECT
require_relative "gemname/model"
require_relative "gemname/query"

# AVOID
autoload :Model, "gemname/model"
autoload :Query, "gemname/query"
```

## Comments Style

Minimal section headers only:

```ruby
# dependencies
require "active_support"

# adapters
require_relative "adapters/postgresql_adapter"

# modules
require_relative "migration"
```

---

## Reference: Rails Integration

# Rails Integration Patterns

## The Golden Rule

**Never require Rails gems directly.** This causes loading order issues.

```ruby
# WRONG - causes premature loading
require "active_record"
ActiveRecord::Base.include(MyGem::Model)

# CORRECT - lazy loading
ActiveSupport.on_load(:active_record) do
  extend MyGem::Model
end
```

## ActiveSupport.on_load Hooks

Common hooks and their uses:

```ruby
# Models
ActiveSupport.on_load(:active_record) do
  extend GemName::Model        # Add class methods (searchkick, has_encrypted)
  include GemName::Callbacks   # Add instance methods
end

# Controllers
ActiveSupport.on_load(:action_controller) do
  include Ahoy::Controller
end

# Jobs
ActiveSupport.on_load(:active_job) do
  include GemName::JobExtensions
end

# Mailers
ActiveSupport.on_load(:action_mailer) do
  include GemName::MailerExtensions
end
```

## Prepend for Behavior Modification

When overriding existing Rails methods:

```ruby
ActiveSupport.on_load(:active_record) do
  ActiveRecord::Migration.prepend(StrongMigrations::Migration)
  ActiveRecord::Migrator.prepend(StrongMigrations::Migrator)
end
```

## Railtie Pattern

Minimal Railtie for non-mountable gems:

```ruby
# lib/gemname/railtie.rb
module GemName
  class Railtie < Rails::Railtie
    initializer "gemname.configure" do
      ActiveSupport.on_load(:active_record) do
        extend GemName::Model
      end
    end

    # Optional: Add to controller runtime logging
    initializer "gemname.log_runtime" do
      require_relative "controller_runtime"
      ActiveSupport.on_load(:action_controller) do
        include GemName::ControllerRuntime
      end
    end

    # Optional: Rake tasks
    rake_tasks do
      load "tasks/gemname.rake"
    end
  end
end
```

## Engine Pattern (Mountable Gems)

For gems with web interfaces (PgHero, Blazer, Ahoy):

```ruby
# lib/pghero/engine.rb
module PgHero
  class Engine < ::Rails::Engine
    isolate_namespace PgHero

    initializer "pghero.assets", group: :all do |app|
      if app.config.respond_to?(:assets) && defined?(Sprockets)
        app.config.assets.precompile << "pghero/application.js"
        app.config.assets.precompile << "pghero/application.css"
      end
    end

    initializer "pghero.config" do
      PgHero.config = Rails.application.config_for(:pghero) rescue {}
    end
  end
end
```

## Routes for Engines

```ruby
# config/routes.rb (in engine)
PgHero::Engine.routes.draw do
  root to: "home#index"
  resources :databases, only: [:show]
end
```

Mount in app:

```ruby
# config/routes.rb (in app)
mount PgHero::Engine, at: "pghero"
```

## YAML Configuration with ERB

For complex gems needing config files:

```ruby
def self.settings
  @settings ||= begin
    path = Rails.root.join("config", "blazer.yml")
    if path.exist?
      YAML.safe_load(ERB.new(File.read(path)).result, aliases: true)
    else
      {}
    end
  end
end
```

## Generator Pattern

```ruby
# lib/generators/gemname/install_generator.rb
module GemName
  module Generators
    class InstallGenerator < Rails::Generators::Base
      source_root File.expand_path("templates", __dir__)

      def copy_initializer
        template "initializer.rb", "config/initializers/gemname.rb"
      end

      def copy_migration
        migration_template "migration.rb", "db/migrate/create_gemname_tables.rb"
      end
    end
  end
end
```

## Conditional Feature Detection

```ruby
# Check for specific Rails versions
if ActiveRecord.version >= Gem::Version.new("7.0")
  # Rails 7+ specific code
end

# Check for optional dependencies
def self.client
  @client ||= if defined?(OpenSearch::Client)
    OpenSearch::Client.new
  elsif defined?(Elasticsearch::Client)
    Elasticsearch::Client.new
  else
    raise Error, "Install elasticsearch or opensearch-ruby"
  end
end
```

---

## Reference: Resources

# Andrew Kane Resources

## Primary Documentation

- **Gem Patterns Article**: https://ankane.org/gem-patterns
  - Kane's own documentation of patterns used across his gems
  - Covers configuration, Rails integration, error handling

## Top Ruby Gems by Stars

### Search & Data

| Gem | Stars | Description | Source |
|-----|-------|-------------|--------|
| **Searchkick** | 6.6k+ | Intelligent search for Rails | https://github.com/ankane/searchkick |
| **Chartkick** | 6.4k+ | Beautiful charts in Ruby | https://github.com/ankane/chartkick |
| **Groupdate** | 3.8k+ | Group by day, week, month | https://github.com/ankane/groupdate |
| **Blazer** | 4.6k+ | SQL dashboard for Rails | https://github.com/ankane/blazer |

### Database & Migrations

| Gem | Stars | Description | Source |
|-----|-------|-------------|--------|
| **PgHero** | 8.2k+ | PostgreSQL insights | https://github.com/ankane/pghero |
| **Strong Migrations** | 4.1k+ | Safe migration checks | https://github.com/ankane/strong_migrations |
| **Dexter** | 1.8k+ | Auto index advisor | https://github.com/ankane/dexter |
| **PgSync** | 1.5k+ | Sync Postgres data | https://github.com/ankane/pgsync |

### Security & Encryption

| Gem | Stars | Description | Source |
|-----|-------|-------------|--------|
| **Lockbox** | 1.5k+ | Application-level encryption | https://github.com/ankane/lockbox |
| **Blind Index** | 1.0k+ | Encrypted search | https://github.com/ankane/blind_index |
| **Secure Headers** | — | Contributed patterns | Referenced in gems |

### Analytics & ML

| Gem | Stars | Description | Source |
|-----|-------|-------------|--------|
| **Ahoy** | 4.2k+ | Analytics for Rails | https://github.com/ankane/ahoy |
| **Neighbor** | 1.1k+ | Vector search for Rails | https://github.com/ankane/neighbor |
| **Rover** | 700+ | DataFrames for Ruby | https://github.com/ankane/rover |
| **Tomoto** | 200+ | Topic modeling | https://github.com/ankane/tomoto-ruby |

### Utilities

| Gem | Stars | Description | Source |
|-----|-------|-------------|--------|
| **Pretender** | 2.0k+ | Login as another user | https://github.com/ankane/pretender |
| **Authtrail** | 900+ | Login activity tracking | https://github.com/ankane/authtrail |
| **Notable** | 200+ | Track notable requests | https://github.com/ankane/notable |
| **Logstop** | 200+ | Filter sensitive logs | https://github.com/ankane/logstop |

## Key Source Files to Study

### Entry Point Patterns
- https://github.com/ankane/searchkick/blob/master/lib/searchkick.rb
- https://github.com/ankane/pghero/blob/master/lib/pghero.rb
- https://github.com/ankane/strong_migrations/blob/master/lib/strong_migrations.rb
- https://github.com/ankane/lockbox/blob/master/lib/lockbox.rb

### Class Macro Implementations
- https://github.com/ankane/searchkick/blob/master/lib/searchkick/model.rb
- https://github.com/ankane/lockbox/blob/master/lib/lockbox/model.rb
- https://github.com/ankane/neighbor/blob/master/lib/neighbor/model.rb
- https://github.com/ankane/blind_index/blob/master/lib/blind_index/model.rb

### Rails Integration (Railtie/Engine)
- https://github.com/ankane/pghero/blob/master/lib/pghero/engine.rb
- https://github.com/ankane/searchkick/blob/master/lib/searchkick/railtie.rb
- https://github.com/ankane/ahoy/blob/master/lib/ahoy/engine.rb
- https://github.com/ankane/blazer/blob/master/lib/blazer/engine.rb

### Database Adapters
- https://github.com/ankane/strong_migrations/tree/master/lib/strong_migrations/adapters
- https://github.com/ankane/groupdate/tree/master/lib/groupdate/adapters
- https://github.com/ankane/neighbor/tree/master/lib/neighbor

### Error Messages (Template Pattern)
- https://github.com/ankane/strong_migrations/blob/master/lib/strong_migrations/error_messages.rb

### Gemspec Examples
- https://github.com/ankane/searchkick/blob/master/searchkick.gemspec
- https://github.com/ankane/neighbor/blob/master/neighbor.gemspec
- https://github.com/ankane/ahoy/blob/master/ahoy_matey.gemspec

### Test Setups
- https://github.com/ankane/searchkick/tree/master/test
- https://github.com/ankane/lockbox/tree/master/test
- https://github.com/ankane/strong_migrations/tree/master/test

## GitHub Profile

- **Profile**: https://github.com/ankane
- **All Ruby Repos**: https://github.com/ankane?tab=repositories&q=&type=&language=ruby&sort=stargazers
- **RubyGems Profile**: https://rubygems.org/profiles/ankane

## Blog Posts & Articles

- **ankane.org**: https://ankane.org/
- **Gem Patterns**: https://ankane.org/gem-patterns (essential reading)
- **Postgres Performance**: https://ankane.org/introducing-pghero
- **Search Tips**: https://ankane.org/search-rails

## Design Philosophy Summary

From studying 100+ gems, Kane's consistent principles:

1. **Zero dependencies when possible** - Each dep is a maintenance burden
2. **ActiveSupport.on_load always** - Never require Rails gems directly
3. **Class macro DSLs** - Single method configures everything
4. **Explicit over magic** - No method_missing, define methods directly
5. **Minitest only** - Simple, sufficient, no RSpec
6. **Multi-version testing** - Support broad Rails/Ruby versions
7. **Helpful errors** - Template-based messages with fix suggestions
8. **Abstract adapters** - Clean multi-database support
9. **Engine isolation** - isolate_namespace for mountable gems
10. **Minimal documentation** - Code is self-documenting, README is examples

---

## Reference: Testing Patterns

# Testing Patterns

## Minitest Setup

Kane exclusively uses Minitest—never RSpec.

```ruby
# test/test_helper.rb
require "bundler/setup"
Bundler.require(:default)
require "minitest/autorun"
require "minitest/pride"

# Load the gem
require "gemname"

# Test database setup (if needed)
ActiveRecord::Base.establish_connection(
  adapter: "postgresql",
  database: "gemname_test"
)

# Base test class
class Minitest::Test
  def setup
    # Reset state before each test
  end
end
```

## Test File Structure

```ruby
# test/model_test.rb
require_relative "test_helper"

class ModelTest < Minitest::Test
  def setup
    User.delete_all
  end

  def test_basic_functionality
    user = User.create!(email: "test@example.org")
    assert_equal "test@example.org", user.email
  end

  def test_with_invalid_input
    error = assert_raises(ArgumentError) do
      User.create!(email: nil)
    end
    assert_match /email/, error.message
  end

  def test_class_method
    result = User.search("test")
    assert_kind_of Array, result
  end
end
```

## Multi-Version Testing

Test against multiple Rails/Ruby versions using gemfiles:

```
test/
├── test_helper.rb
└── gemfiles/
    ├── activerecord70.gemfile
    ├── activerecord71.gemfile
    └── activerecord72.gemfile
```

```ruby
# test/gemfiles/activerecord70.gemfile
source "https://rubygems.org"
gemspec path: "../../"

gem "activerecord", "~> 7.0.0"
gem "sqlite3"
```

```ruby
# test/gemfiles/activerecord72.gemfile
source "https://rubygems.org"
gemspec path: "../../"

gem "activerecord", "~> 7.2.0"
gem "sqlite3"
```

Run with specific gemfile:

```bash
BUNDLE_GEMFILE=test/gemfiles/activerecord70.gemfile bundle install
BUNDLE_GEMFILE=test/gemfiles/activerecord70.gemfile bundle exec rake test
```

## Rakefile

```ruby
# Rakefile
require "bundler/gem_tasks"
require "rake/testtask"

Rake::TestTask.new(:test) do |t|
  t.libs << "test"
  t.pattern = "test/**/*_test.rb"
end

task default: :test
```

## GitHub Actions CI

```yaml
# .github/workflows/build.yml
name: build

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        include:
          - ruby: "3.2"
            gemfile: activerecord70
          - ruby: "3.3"
            gemfile: activerecord71
          - ruby: "3.3"
            gemfile: activerecord72

    env:
      BUNDLE_GEMFILE: test/gemfiles/${{ matrix.gemfile }}.gemfile

    steps:
      - uses: actions/checkout@v4

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: ${{ matrix.ruby }}
          bundler-cache: true

      - run: bundle exec rake test
```

## Database-Specific Testing

```yaml
# .github/workflows/build.yml (with services)
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5

env:
  DATABASE_URL: postgres://postgres:postgres@localhost/gemname_test
```

## Test Database Setup

```ruby
# test/test_helper.rb
require "active_record"

# Connect to database
ActiveRecord::Base.establish_connection(
  ENV["DATABASE_URL"] || {
    adapter: "postgresql",
    database: "gemname_test"
  }
)

# Create tables
ActiveRecord::Schema.define do
  create_table :users, force: true do |t|
    t.string :email
    t.text :encrypted_data
    t.timestamps
  end
end

# Define models
class User < ActiveRecord::Base
  gemname_feature :email
end
```

## Assertion Patterns

```ruby
# Basic assertions
assert result
assert_equal expected, actual
assert_nil value
assert_empty array

# Exception testing
assert_raises(ArgumentError) { bad_code }

error = assert_raises(GemName::Error) do
  risky_operation
end
assert_match /expected message/, error.message

# Refutations
refute condition
refute_equal unexpected, actual
refute_nil value
```

## Test Helpers

```ruby
# test/test_helper.rb
class Minitest::Test
  def with_options(options)
    original = GemName.options.dup
    GemName.options.merge!(options)
    yield
  ensure
    GemName.options = original
  end

  def assert_queries(expected_count)
    queries = []
    callback = ->(*, payload) { queries << payload[:sql] }
    ActiveSupport::Notifications.subscribe("sql.active_record", callback)
    yield
    assert_equal expected_count, queries.size, "Expected #{expected_count} queries, got #{queries.size}"
  ensure
    ActiveSupport::Notifications.unsubscribe(callback)
  end
end
```

## Skipping Tests

```ruby
def test_postgresql_specific
  skip "PostgreSQL only" unless postgresql?
  # test code
end

def postgresql?
  ActiveRecord::Base.connection.adapter_name =~ /postg/i
end
```
