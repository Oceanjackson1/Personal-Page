---
title: "Insecure Defaults"
description: "Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production. Use when auditing security, reviewing config management, or analyzing environment variable handling."
category: "development"
source: "community"
author: "Community"
tags: ["insecure", "defaults"]
date: 2026-03-20
---

# Insecure Defaults Detection

Finds **fail-open** vulnerabilities where apps run insecurely with missing configuration. Distinguishes exploitable defaults from fail-secure patterns that crash safely.

- **Fail-open (CRITICAL):** `SECRET = env.get('KEY') or 'default'` → App runs with weak secret
- **Fail-secure (SAFE):** `SECRET = env['KEY']` → App crashes if missing

## When to Use

- **Security audits** of production applications (auth, crypto, API security)
- **Configuration review** of deployment files, IaC templates, Docker configs
- **Code review** of environment variable handling and secrets management
- **Pre-deployment checks** for hardcoded credentials or weak defaults

## When NOT to Use

Do not use this skill for:
- **Test fixtures** explicitly scoped to test environments (files in `test/`, `spec/`, `__tests__/`)
- **Example/template files** (`.example`, `.template`, `.sample` suffixes)
- **Development-only tools** (local Docker Compose for dev, debug scripts)
- **Documentation examples** in README.md or docs/ directories
- **Build-time configuration** that gets replaced during deployment
- **Crash-on-missing behavior** where app won't start without proper config (fail-secure)

When in doubt: trace the code path to determine if the app runs with the default or crashes.

## Rationalizations to Reject

- **"It's just a development default"** → If it reaches production code, it's a finding
- **"The production config overrides it"** → Verify prod config exists; code-level vulnerability remains if not
- **"This would never run without proper config"** → Prove it with code trace; many apps fail silently
- **"It's behind authentication"** → Defense in depth; compromised session still exploits weak defaults
- **"We'll fix it before release"** → Document now; "later" rarely comes

## Workflow

Follow this workflow for every potential finding:

### 1. SEARCH: Perform Project Discovery and Find Insecure Defaults

Determine language, framework, and project conventions. Use this information to further discover things like secret storage locations, secret usage patterns, credentialed third-party integrations, cryptography, and any other relevant configuration. Further use information to analyze insecure default configurations.

**Example**
Search for patterns in `**/config/`, `**/auth/`, `**/database/`, and env files:
- **Fallback secrets:** `getenv.*\) or ['"]`, `process\.env\.[A-Z_]+ \|\| ['"]`, `ENV\.fetch.*default:`
- **Hardcoded credentials:** `password.*=.*['"][^'"]{8,}['"]`, `api[_-]?key.*=.*['"][^'"]+['"]`
- **Weak defaults:** `DEBUG.*=.*true`, `AUTH.*=.*false`, `CORS.*=.*\*`
- **Crypto algorithms:** `MD5|SHA1|DES|RC4|ECB` in security contexts

Tailor search approach based on discovery results.

Focus on production-reachable code, not test fixtures or example files.

### 2. VERIFY: Actual Behavior
For each match, trace the code path to understand runtime behavior.

**Questions to answer:**
- When is this code executed? (Startup vs. runtime)
- What happens if a configuration variable is missing?
- Is there validation that enforces secure configuration?

### 3. CONFIRM: Production Impact
Determine if this issue reaches production:

If production config provides the variable → Lower severity (but still a code-level vulnerability)
If production config missing or uses default → CRITICAL

### 4. REPORT: with Evidence

**Example report:**
```
Finding: Hardcoded JWT Secret Fallback
Location: src/auth/jwt.ts:15
Pattern: const secret = process.env.JWT_SECRET || 'default';

Verification: App starts without JWT_SECRET; secret used in jwt.sign() at line 42
Production Impact: Dockerfile missing JWT_SECRET
Exploitation: Attacker forges JWTs using 'default', gains unauthorized access
```

## Quick Verification Checklist

**Fallback Secrets:** `SECRET = env.get(X) or Y`
→ Verify: App starts without env var? Secret used in crypto/auth?
→ Skip: Test fixtures, example files

**Default Credentials:** Hardcoded `username`/`password` pairs
→ Verify: Active in deployed config? No runtime override?
→ Skip: Disabled accounts, documentation examples

**Fail-Open Security:** `AUTH_REQUIRED = env.get(X, 'false')`
→ Verify: Default is insecure (false/disabled/permissive)?
→ Safe: App crashes or default is secure (true/enabled/restricted)

**Weak Crypto:** MD5/SHA1/DES/RC4/ECB in security contexts
→ Verify: Used for passwords, encryption, or tokens?
→ Skip: Checksums, non-security hashing

**Permissive Access:** CORS `*`, permissions `0777`, public-by-default
→ Verify: Default allows unauthorized access?
→ Skip: Explicitly configured permissiveness with justification

**Debug Features:** Stack traces, introspection, verbose errors
→ Verify: Enabled by default? Exposed in responses?
→ Skip: Logging-only, not user-facing

For detailed examples and counter-examples, see [examples.md](references/examples.md).

---

## Reference: Examples

# Insecure Defaults: Examples and Counter-Examples

This document provides detailed examples for each category in the Quick Verification Checklist, showing both vulnerable patterns (report these) and secure patterns (skip these).

## Fallback Secrets

### ❌ VULNERABLE - Report These

**Python: Environment variable with fallback**
```python
# File: src/auth/jwt.py
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

# Used in security context
def create_token(user_id):
    return jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
```
**Why vulnerable:** App runs with known secret if `SECRET_KEY` is missing. Attacker can forge tokens.

**JavaScript: Logical OR fallback**
```javascript
// File: config/database.js
const DB_PASSWORD = process.env.DB_PASSWORD || 'admin123';

const pool = new Pool({
  user: 'admin',
  password: DB_PASSWORD,
  database: 'production'
});
```
**Why vulnerable:** Database accepts hardcoded password in production if env var missing.

**Ruby: fetch with default**
```ruby
# File: config/secrets.rb
Rails.application.credentials.secret_key_base =
  ENV.fetch('SECRET_KEY_BASE', 'fallback-secret-base')
```
**Why vulnerable:** Rails session encryption uses weak known key as fallback.

### ✅ SECURE - Skip These

**Fail-secure: Crashes without config**
```python
# File: src/auth/jwt.py
SECRET_KEY = os.environ['SECRET_KEY']  # Raises KeyError if missing

# App won't start without SECRET_KEY - fail-secure
```

**Explicit validation**
```javascript
// File: config/database.js
if (!process.env.DB_PASSWORD) {
  throw new Error('DB_PASSWORD environment variable required');
}
const DB_PASSWORD = process.env.DB_PASSWORD;
```

**Test fixtures (clearly scoped)**
```python
# File: tests/fixtures/auth.py
TEST_SECRET = 'test-secret-key-123'  # OK - test-only

# Usage in test
def test_token_creation():
    token = create_token('user1', secret=TEST_SECRET)
```

---

## Default Credentials

### ❌ VULNERABLE - Report These

**Hardcoded admin account**
```python
# File: src/models/user.py
def bootstrap_admin():
    """Create default admin account if none exists"""
    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='admin',
            password=hash_password('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
```
**Why vulnerable:** Default admin account created on first run with known credentials.

**API key in code**
```javascript
// File: src/integrations/payment.js
const STRIPE_API_KEY = process.env.STRIPE_KEY || 'sk_tes...';

const stripe = require('stripe')(STRIPE_API_KEY);
```
**Why vulnerable:** Uses test API key if env var missing. Might reach production.

**Database connection string**
```java
// File: DatabaseConfig.java
private static final String DB_URL = System.getenv().getOrDefault(
    "DATABASE_URL",
    "postgresql://admin:password@localhost:5432/prod"
);
```
**Why vulnerable:** Hardcoded database credentials as fallback.

### ✅ SECURE - Skip These

**Disabled default account**
```python
# File: src/models/user.py
def bootstrap_admin():
    """Admin account MUST be configured via environment"""
    username = os.environ['ADMIN_USERNAME']
    password = os.environ['ADMIN_PASSWORD']

    if not User.query.filter_by(username=username).first():
        admin = User(username=username, password=hash_password(password), role='admin')
        db.session.add(admin)
```

**Example/documentation credentials**
```bash
# File: README.md
## Setup

Configure your API key:
```bash
export STRIPE_KEY='sk_tes...'  # Example only
```
```

**Test fixture credentials**
```python
# File: tests/conftest.py
@pytest.fixture
def test_user():
    return User(username='test_user', password='test_pass')  # OK - test scope
```

---

## Fail-Open Security

### ❌ VULNERABLE - Report These

**Authentication disabled by default**
```python
# File: config/security.py
REQUIRE_AUTH = os.getenv('REQUIRE_AUTH', 'false').lower() == 'true'

@app.before_request
def check_auth():
    if not REQUIRE_AUTH:
        return  # Skip auth check
    # ... auth logic
```
**Why vulnerable:** Default is no authentication. App runs insecurely if env var missing.

**CORS allows all origins**
```javascript
// File: server.js
const allowedOrigins = process.env.ALLOWED_ORIGINS || '*';

app.use(cors({ origin: allowedOrigins }));
```
**Why vulnerable:** Default allows requests from any origin. XSS/CSRF risk.

**Debug mode enabled by default**
```python
# File: config.py
DEBUG = os.getenv('DEBUG', 'true').lower() != 'false'  # Default: true

if DEBUG:
    app.config['DEBUG'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
```
**Why vulnerable:** Debug mode default. Stack traces leak sensitive info in production.

### ✅ SECURE - Skip These

**Authentication required by default**
```python
# File: config/security.py
REQUIRE_AUTH = os.getenv('REQUIRE_AUTH', 'true').lower() == 'true'  # Default: true

# Or better - crash if not explicitly configured
REQUIRE_AUTH = os.environ['REQUIRE_AUTH'].lower() == 'true'
```

**CORS requires explicit configuration**
```javascript
// File: server.js
if (!process.env.ALLOWED_ORIGINS) {
  throw new Error('ALLOWED_ORIGINS must be configured');
}
const allowedOrigins = process.env.ALLOWED_ORIGINS.split(',');

app.use(cors({ origin: allowedOrigins }));
```

**Debug mode disabled by default**
```python
# File: config.py
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'  # Default: false
```

---

## Weak Crypto

### ❌ VULNERABLE - Report These

**MD5 for password hashing**
```python
# File: src/auth/passwords.py
import hashlib

def hash_password(password):
    """Hash user password"""
    return hashlib.md5(password.encode()).hexdigest()
```
**Why vulnerable:** MD5 is cryptographically broken. Rainbow tables exist. Use bcrypt/Argon2.

**DES encryption for sensitive data**
```java
// File: Encryption.java
public static byte[] encrypt(String data, byte[] key) {
    Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
    SecretKeySpec secretKey = new SecretKeySpec(key, "DES");
    cipher.init(Cipher.ENCRYPT_MODE, secretKey);
    return cipher.doFinal(data.getBytes());
}
```
**Why vulnerable:** DES has 56-bit keys (brute-forceable). ECB mode leaks patterns.

**SHA1 for signature verification**
```javascript
// File: webhooks.js
function verifySignature(payload, signature) {
  const hmac = crypto.createHmac('sha1', WEBHOOK_SECRET);
  const computed = hmac.update(payload).digest('hex');
  return computed === signature;
}
```
**Why vulnerable:** SHA1 collisions exist. Use SHA256 or better.

### ✅ SECURE - Skip These

**Weak crypto for non-security checksums**
```python
# File: src/utils/cache.py
import hashlib

def cache_key(data):
    """Generate cache key - not security-sensitive"""
    return hashlib.md5(data.encode()).hexdigest()  # OK - just for cache lookup
```

**Modern crypto for passwords**
```python
# File: src/auth/passwords.py
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

**Strong encryption**
```java
// File: Encryption.java
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
// 256-bit key, authenticated encryption
```

---

## Permissive Access

### ❌ VULNERABLE - Report These

**File permissions world-writable**
```python
# File: src/storage/files.py
def create_secure_file(path):
    fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0o666)  # rw-rw-rw-
    return fd
```
**Why vulnerable:** Any user can write to file. Should be 0o600 or 0o644.

**S3 bucket public by default**
```python
# File: infrastructure/storage.py
def create_storage_bucket(name):
    bucket = s3.create_bucket(
        Bucket=name,
        ACL='public-read'  # Publicly readable by default
    )
```
**Why vulnerable:** Sensitive data exposed publicly. Should require explicit configuration.

**API allows any origin**
```python
# File: app.py
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
```
**Why vulnerable:** CORS misconfiguration. Allows credential theft from any site.

### ✅ SECURE - Skip These

**Explicitly configured permissiveness with justification**
```python
# File: src/storage/public_assets.py
def create_public_asset(path):
    """Create world-readable asset for CDN distribution"""
    # Intentionally public - static assets only
    fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0o644)
    return fd
```

**Restrictive by default**
```python
# File: infrastructure/storage.py
def create_storage_bucket(name, public=False):
    acl = 'public-read' if public else 'private'
    if public:
        logger.warning(f'Creating PUBLIC bucket: {name}')
    bucket = s3.create_bucket(Bucket=name, ACL=acl)
```

---

## Debug Features

### ❌ VULNERABLE - Report These

**Stack traces in API responses**
```python
# File: app.py
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'error': str(error),
        'traceback': traceback.format_exc()  # Leaks internal paths, library versions
    }), 500
```
**Why vulnerable:** Exposes internal implementation details to attackers.

**GraphQL introspection enabled**
```javascript
// File: server.js
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: true,  // Enabled in production
  playground: true
});
```
**Why vulnerable:** Attackers can discover entire API schema, including admin-only fields.

**Verbose error messages**
```java
// File: UserController.java
catch (SQLException e) {
    return ResponseEntity.status(500).body(
        "Database error: " + e.getMessage()  // Leaks table names, constraints
    );
}
```
**Why vulnerable:** SQL error messages reveal database structure.

### ✅ SECURE - Skip These

**Debug features in logging only**
```python
# File: app.py
@app.errorhandler(Exception)
def handle_error(error):
    logger.exception('Request failed', exc_info=error)  # Logs full trace
    return jsonify({'error': 'Internal server error'}), 500  # Generic to user
```

**Environment-aware debug settings**
```javascript
// File: server.js
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  playground: process.env.NODE_ENV !== 'production'
});
```

**Generic user-facing errors**
```java
// File: UserController.java
catch (SQLException e) {
    logger.error("Database error", e);  // Full details to logs
    return ResponseEntity.status(500).body("Unable to process request");  // Generic
}
```
