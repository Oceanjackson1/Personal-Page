---
title: "SQL Pro"
description: "Optimizes SQL queries, designs database schemas, and troubleshoots performance issues. Use when a user asks why their query is slow, needs help writing complex joins or aggregations, mentions database performance issues, or wants to design or migr..."
category: "research"
source: "community"
author: "Community"
tags: ["sql"]
date: 2026-03-20
---

# SQL Pro

## Core Workflow

1. **Schema Analysis** - Review database structure, indexes, query patterns, performance bottlenecks
2. **Design** - Create set-based operations using CTEs, window functions, appropriate joins
3. **Optimize** - Analyze execution plans, implement covering indexes, eliminate table scans
4. **Verify** - Run `EXPLAIN ANALYZE` and confirm no sequential scans on large tables; if query does not meet sub-100ms target, iterate on index selection or query rewrite before proceeding
5. **Document** - Provide query explanations, index rationale, performance metrics

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Query Patterns | `references/query-patterns.md` | JOINs, CTEs, subqueries, recursive queries |
| Window Functions | `references/window-functions.md` | ROW_NUMBER, RANK, LAG/LEAD, analytics |
| Optimization | `references/optimization.md` | EXPLAIN plans, indexes, statistics, tuning |
| Database Design | `references/database-design.md` | Normalization, keys, constraints, schemas |
| Dialect Differences | `references/dialect-differences.md` | PostgreSQL vs MySQL vs SQL Server specifics |

## Quick-Reference Examples

### CTE Pattern
```sql
-- Isolate expensive subquery logic for reuse and readability
WITH ranked_orders AS (
    SELECT
        customer_id,
        order_id,
        total_amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM orders
    WHERE status = 'completed'          -- filter early, before the join
)
SELECT customer_id, order_id, total_amount
FROM ranked_orders
WHERE rn = 1;                           -- latest completed order per customer
```

### Window Function Pattern
```sql
-- Running total and rank within partition — no self-join required
SELECT
    department_id,
    employee_id,
    salary,
    SUM(salary)  OVER (PARTITION BY department_id ORDER BY hire_date) AS running_payroll,
    RANK()       OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank
FROM employees;
```

### EXPLAIN ANALYZE Interpretation
```sql
-- PostgreSQL: always use ANALYZE to see actual row counts vs. estimates
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT *
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at > NOW() - INTERVAL '30 days';
```
Key things to check in the output:
- **Seq Scan on large table** → add or fix an index
- **actual rows ≫ estimated rows** → run `ANALYZE <table>` to refresh statistics
- **Buffers: shared hit** vs **read** → high `read` count signals missing cache / index

### Before / After Optimization Example
```sql
-- BEFORE: correlated subquery, one execution per row (slow)
SELECT order_id,
       (SELECT SUM(quantity) FROM order_items oi WHERE oi.order_id = o.id) AS item_count
FROM orders o;

-- AFTER: single aggregation join (fast)
SELECT o.order_id, COALESCE(agg.item_count, 0) AS item_count
FROM orders o
LEFT JOIN (
    SELECT order_id, SUM(quantity) AS item_count
    FROM order_items
    GROUP BY order_id
) agg ON agg.order_id = o.id;

-- Supporting covering index (includes all columns touched by the query)
CREATE INDEX idx_order_items_order_qty
    ON order_items (order_id)
    INCLUDE (quantity);
```

## Constraints

### MUST DO
- Analyze execution plans before recommending optimizations
- Use set-based operations over row-by-row processing
- Apply filtering early in query execution (before joins where possible)
- Use EXISTS over COUNT for existence checks
- Handle NULLs explicitly in comparisons and aggregations
- Create covering indexes for frequent queries
- Test with production-scale data volumes

### MUST NOT DO
- Use SELECT * in production queries
- Use cursors when set-based operations work
- Ignore platform-specific optimizations when targeting a specific dialect
- Implement solutions without considering data volume and cardinality

## Output Templates

When implementing SQL solutions, provide:
1. Optimized query with inline comments
2. Required indexes with rationale
3. Execution plan analysis
4. Performance metrics (before/after)
5. Platform-specific notes if applicable

---

## Reference: Database Design

# Database Design

## Normalization Levels

```sql
-- 1NF: Atomic values, no repeating groups
-- Bad: Non-atomic phone column
CREATE TABLE customers_bad (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    phones VARCHAR(500)  -- "555-1234,555-5678,555-9012"
);

-- Good: Atomic values
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE customer_phones (
    phone_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    phone_number VARCHAR(20) NOT NULL,
    phone_type VARCHAR(20) CHECK (phone_type IN ('mobile', 'home', 'work'))
);

-- 2NF: No partial dependencies (all non-key attributes depend on entire key)
-- Bad: Partial dependency on composite key
CREATE TABLE order_items_bad (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id
    product_price DECIMAL(10,2),  -- Depends only on product_id
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- Good: Separate product attributes
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_price DECIMAL(10,2) NOT NULL CHECK (product_price >= 0)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL,  -- Snapshot at order time
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 3NF: No transitive dependencies
-- Bad: City/State depends on ZIP
CREATE TABLE addresses_bad (
    address_id INT PRIMARY KEY,
    street VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10)
);

-- Good: Separate ZIP code reference
CREATE TABLE zip_codes (
    zip_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    county VARCHAR(100)
);

CREATE TABLE addresses (
    address_id SERIAL PRIMARY KEY,
    street VARCHAR(200) NOT NULL,
    zip_code VARCHAR(10) NOT NULL REFERENCES zip_codes(zip_code)
);
```

## Primary and Foreign Keys

```sql
-- Natural vs Surrogate keys
-- Natural key (business meaning)
CREATE TABLE countries (
    country_code CHAR(2) PRIMARY KEY,  -- ISO 3166-1 alpha-2
    country_name VARCHAR(100) NOT NULL
);

-- Surrogate key (technical, no business meaning)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,  -- Auto-incrementing surrogate
    email VARCHAR(255) NOT NULL UNIQUE,  -- Natural candidate key
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Composite primary key
CREATE TABLE student_courses (
    student_id INT,
    course_id INT,
    enrollment_date DATE NOT NULL,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- UUID primary keys (distributed systems, no sequence conflicts)
CREATE TABLE events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Foreign key with cascading actions
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE  -- Delete orders when customer deleted
        ON UPDATE CASCADE  -- Update order.customer_id when customers.customer_id changes
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,  -- Delete items when order deleted
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE RESTRICT  -- Prevent deleting product if used in orders
);
```

## Constraints and Validation

```sql
-- CHECK constraints
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    salary DECIMAL(12,2) NOT NULL,
    hire_date DATE NOT NULL,
    birth_date DATE NOT NULL,

    CONSTRAINT chk_salary_positive CHECK (salary > 0),
    CONSTRAINT chk_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}$'),
    CONSTRAINT chk_hire_after_birth CHECK (hire_date > birth_date + INTERVAL '16 years'),
    CONSTRAINT chk_hire_not_future CHECK (hire_date <= CURRENT_DATE)
);

-- Unique constraints (including composite)
CREATE TABLE user_preferences (
    user_id INT NOT NULL,
    preference_key VARCHAR(50) NOT NULL,
    preference_value TEXT,

    CONSTRAINT uq_user_preference UNIQUE (user_id, preference_key)
);

-- NOT NULL constraints with defaults
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Exclusion constraints (PostgreSQL - prevent overlapping ranges)
CREATE TABLE room_bookings (
    booking_id SERIAL PRIMARY KEY,
    room_id INT NOT NULL,
    booked_during TSTZRANGE NOT NULL,

    EXCLUDE USING GIST (
        room_id WITH =,
        booked_during WITH &&
    )  -- Prevent overlapping bookings for same room
);
```

## Indexing Strategy

```sql
-- Index foreign keys (critical for JOIN performance)
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Composite index for common queries
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date DESC);
-- Supports:
-- WHERE customer_id = ? AND order_date > ?
-- WHERE customer_id = ? ORDER BY order_date DESC

-- Partial index for common filters
CREATE INDEX idx_active_products ON products(category, price)
WHERE is_active = true AND deleted_at IS NULL;

-- Unique index for business rules
CREATE UNIQUE INDEX idx_users_active_email ON users(LOWER(email))
WHERE deleted_at IS NULL;
-- Ensures no duplicate emails among active users
```

## Common Design Patterns

```sql
-- Polymorphic associations (flexible but harder to enforce integrity)
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    commentable_type VARCHAR(50) NOT NULL,  -- 'Post', 'Photo', 'Video'
    commentable_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Cannot enforce FK without triggers/application logic
    CHECK (commentable_type IN ('Post', 'Photo', 'Video'))
);

-- Better: Separate tables with proper FKs
CREATE TABLE post_comments (
    comment_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL REFERENCES posts(post_id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE photo_comments (
    comment_id SERIAL PRIMARY KEY,
    photo_id INT NOT NULL REFERENCES photos(photo_id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Many-to-many with attributes (junction/bridge table)
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL
);

CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id),
    course_id INT NOT NULL REFERENCES courses(course_id),
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    grade CHAR(2),
    status VARCHAR(20) DEFAULT 'active',

    UNIQUE (student_id, course_id),
    CHECK (status IN ('active', 'completed', 'dropped'))
);

-- Self-referencing hierarchy
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INT REFERENCES categories(category_id),
    level INT NOT NULL DEFAULT 0,

    CHECK (category_id != parent_category_id)  -- Prevent self-reference
);

-- Adjacency list example
INSERT INTO categories VALUES
    (1, 'Electronics', NULL, 0),
    (2, 'Computers', 1, 1),
    (3, 'Laptops', 2, 2),
    (4, 'Desktops', 2, 2);
```

## Temporal/Historical Data

```sql
-- Slowly Changing Dimension Type 2 (SCD2) - Full history
CREATE TABLE customer_history (
    customer_history_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT,
    valid_from TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN NOT NULL DEFAULT true,

    CHECK (valid_to IS NULL OR valid_to > valid_from)
);

-- Ensure only one current record per customer
CREATE UNIQUE INDEX idx_customer_current ON customer_history(customer_id)
WHERE is_current = true;

-- Temporal tables (PostgreSQL system-versioning)
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    sys_period TSTZRANGE NOT NULL DEFAULT tstzrange(CURRENT_TIMESTAMP, NULL)
);

CREATE TABLE products_history (LIKE products);

CREATE TRIGGER versioning_trigger
BEFORE INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION versioning('sys_period', 'products_history', true);
```

## Soft Deletes

```sql
-- Soft delete pattern
CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INT NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,  -- NULL = active, non-NULL = deleted
    deleted_by INT REFERENCES users(user_id)
);

-- Index for filtering active records
CREATE INDEX idx_posts_active ON posts(created_at DESC)
WHERE deleted_at IS NULL;

-- View for active posts only
CREATE VIEW active_posts AS
SELECT post_id, title, content, author_id, created_at, updated_at
FROM posts
WHERE deleted_at IS NULL;
```

## Audit Trails

```sql
-- Audit table pattern
CREATE TABLE audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id BIGINT NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    changed_by INT REFERENCES users(user_id),
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_table_record ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_timestamp ON audit_log(changed_at DESC);

-- Trigger function for automatic auditing
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values)
        VALUES (TG_TABLE_NAME, OLD.product_id, 'DELETE', row_to_json(OLD));
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values, new_values)
        VALUES (TG_TABLE_NAME, NEW.product_id, 'UPDATE', row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_log (table_name, record_id, action, new_values)
        VALUES (TG_TABLE_NAME, NEW.product_id, 'INSERT', row_to_json(NEW));
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_audit
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

## Schema Design Best Practices

1. **Choose appropriate data types**: Use smallest type that fits (INT vs BIGINT, VARCHAR(50) vs TEXT)
2. **Index foreign keys**: Always index FK columns for JOIN performance
3. **Avoid NULLs when possible**: Use NOT NULL with defaults
4. **Use constraints**: Enforce data integrity at database level
5. **Normalize to 3NF**: Then denormalize strategically for performance
6. **Consider soft deletes**: For auditing and data recovery
7. **Plan for growth**: Use BIGINT for high-volume PKs
8. **Document schema**: Comment tables and complex constraints
9. **Version control**: Track schema changes with migrations
10. **Test with realistic data**: Validate design with production-scale data

---

## Reference: Dialect Differences

# Database Dialect Differences

## Auto-Incrementing Primary Keys

```sql
-- PostgreSQL
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,  -- or BIGSERIAL for BIGINT
    name VARCHAR(100)
);
-- Alternative (PostgreSQL 10+)
CREATE TABLE users (
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
);

-- MySQL
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- SQL Server
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100)
);

-- Oracle
CREATE TABLE users (
    user_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100)
);
-- Or using sequence (older approach)
CREATE SEQUENCE user_id_seq;
CREATE TABLE users (
    user_id NUMBER DEFAULT user_id_seq.NEXTVAL PRIMARY KEY,
    name VARCHAR2(100)
);
```

## String Concatenation

```sql
-- PostgreSQL (strict - automatic casting)
SELECT first_name || ' ' || last_name AS full_name FROM users;
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;  -- NULL-safe

-- MySQL (automatic type conversion)
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;
SELECT first_name + ' ' + last_name FROM users;  -- ERROR in MySQL

-- SQL Server
SELECT first_name + ' ' + last_name AS full_name FROM users;
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;  -- 2012+

-- Oracle
SELECT first_name || ' ' || last_name AS full_name FROM users;
SELECT CONCAT(first_name, last_name) FROM users;  -- Only 2 arguments!
```

## Date/Time Functions

```sql
-- Current timestamp
-- PostgreSQL
SELECT CURRENT_TIMESTAMP, NOW(), CURRENT_DATE, CURRENT_TIME;

-- MySQL
SELECT CURRENT_TIMESTAMP, NOW(), CURDATE(), CURTIME();

-- SQL Server
SELECT GETDATE(), SYSDATETIME(), CAST(GETDATE() AS DATE);

-- Oracle
SELECT SYSDATE, SYSTIMESTAMP, TRUNC(SYSDATE) FROM DUAL;

-- Date arithmetic
-- PostgreSQL
SELECT order_date + INTERVAL '7 days' FROM orders;
SELECT order_date - INTERVAL '1 month' FROM orders;
SELECT AGE(CURRENT_DATE, birth_date) FROM users;  -- Interval type

-- MySQL
SELECT DATE_ADD(order_date, INTERVAL 7 DAY) FROM orders;
SELECT DATE_SUB(order_date, INTERVAL 1 MONTH) FROM orders;
SELECT DATEDIFF(CURRENT_DATE, birth_date) FROM users;  -- Days only

-- SQL Server
SELECT DATEADD(day, 7, order_date) FROM orders;
SELECT DATEADD(month, -1, order_date) FROM orders;
SELECT DATEDIFF(year, birth_date, GETDATE()) FROM users;

-- Oracle
SELECT order_date + 7 FROM orders;  -- +7 days
SELECT ADD_MONTHS(order_date, -1) FROM orders;
SELECT MONTHS_BETWEEN(SYSDATE, birth_date) / 12 FROM users;

-- Date formatting
-- PostgreSQL
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') FROM orders;

-- MySQL
SELECT DATE_FORMAT(order_date, '%Y-%m-%d') FROM orders;

-- SQL Server
SELECT FORMAT(order_date, 'yyyy-MM-dd') FROM orders;
SELECT CONVERT(VARCHAR(10), order_date, 120) FROM orders;  -- Style 120 = yyyy-MM-dd

-- Oracle
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') FROM orders;
```

## LIMIT/OFFSET (Pagination)

```sql
-- PostgreSQL & MySQL
SELECT * FROM products
ORDER BY product_id
LIMIT 10 OFFSET 20;

-- SQL Server (2012+)
SELECT * FROM products
ORDER BY product_id
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;

-- SQL Server (older - ROW_NUMBER)
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (ORDER BY product_id) as rn
    FROM products
) x
WHERE rn BETWEEN 21 AND 30;

-- Oracle (12c+)
SELECT * FROM products
ORDER BY product_id
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;

-- Oracle (older - ROWNUM)
SELECT * FROM (
    SELECT a.*, ROWNUM rnum FROM (
        SELECT * FROM products ORDER BY product_id
    ) a
    WHERE ROWNUM <= 30
)
WHERE rnum > 20;
```

## Boolean Data Type

```sql
-- PostgreSQL (native BOOLEAN)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    is_active BOOLEAN DEFAULT true
);
SELECT * FROM users WHERE is_active = true;

-- MySQL (TINYINT(1) or BOOLEAN alias)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    is_active BOOLEAN DEFAULT 1  -- Stored as TINYINT(1)
);
SELECT * FROM users WHERE is_active = 1;

-- SQL Server (BIT)
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    is_active BIT DEFAULT 1
);
SELECT * FROM users WHERE is_active = 1;

-- Oracle (no native boolean in tables, use NUMBER or CHAR)
CREATE TABLE users (
    user_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    is_active NUMBER(1) DEFAULT 1 CHECK (is_active IN (0, 1))
);
SELECT * FROM users WHERE is_active = 1;
```

## JSON/JSONB Support

```sql
-- PostgreSQL (JSONB - binary, indexable)
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_data JSONB NOT NULL
);

INSERT INTO events (event_data) VALUES ('{"user_id": 123, "action": "login"}');

SELECT event_data->>'user_id' as user_id FROM events;
SELECT * FROM events WHERE event_data @> '{"action": "login"}';
SELECT * FROM events WHERE event_data->>'user_id' = '123';

CREATE INDEX idx_events_data ON events USING GIN (event_data);

-- MySQL (8.0+)
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_data JSON NOT NULL
);

SELECT JSON_EXTRACT(event_data, '$.user_id') as user_id FROM events;
SELECT * FROM events WHERE JSON_EXTRACT(event_data, '$.action') = 'login';

CREATE INDEX idx_events_user ON events ((CAST(event_data->>'$.user_id' AS UNSIGNED)));

-- SQL Server (2016+)
CREATE TABLE events (
    event_id INT IDENTITY(1,1) PRIMARY KEY,
    event_data NVARCHAR(MAX) CHECK (ISJSON(event_data) = 1)
);

SELECT JSON_VALUE(event_data, '$.user_id') as user_id FROM events;
SELECT * FROM events WHERE JSON_VALUE(event_data, '$.action') = 'login';

-- Oracle (12c+)
CREATE TABLE events (
    event_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_data CLOB CHECK (event_data IS JSON)
);

SELECT JSON_VALUE(event_data, '$.user_id') as user_id FROM events;
SELECT * FROM events WHERE JSON_EXISTS(event_data, '$.action?(@ == "login")');
```

## String Comparison (Case Sensitivity)

```sql
-- PostgreSQL (case-sensitive by default)
SELECT * FROM users WHERE email = 'USER@EXAMPLE.COM';  -- Won't match 'user@example.com'
SELECT * FROM users WHERE LOWER(email) = LOWER('USER@EXAMPLE.COM');
SELECT * FROM users WHERE email ILIKE 'user@example.com';  -- Case-insensitive

-- MySQL (case-insensitive by default with utf8_general_ci collation)
SELECT * FROM users WHERE email = 'USER@EXAMPLE.COM';  -- Matches 'user@example.com'
SELECT * FROM users WHERE email COLLATE utf8_bin = 'user@example.com';  -- Case-sensitive

-- SQL Server (depends on collation, usually case-insensitive)
SELECT * FROM users WHERE email = 'USER@EXAMPLE.COM';  -- Usually matches
SELECT * FROM users WHERE email COLLATE Latin1_General_BIN = 'user@example.com';  -- Case-sensitive

-- Oracle (case-sensitive by default)
SELECT * FROM users WHERE email = 'USER@EXAMPLE.COM';  -- Won't match 'user@example.com'
SELECT * FROM users WHERE UPPER(email) = UPPER('user@example.com');
```

## Recursive CTEs

```sql
-- PostgreSQL
WITH RECURSIVE subordinates AS (
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.name, e.manager_id, s.level + 1
    FROM employees e
    INNER JOIN subordinates s ON e.manager_id = s.employee_id
)
SELECT * FROM subordinates;

-- MySQL (8.0+) - Same syntax as PostgreSQL
WITH RECURSIVE subordinates AS (
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.name, e.manager_id, s.level + 1
    FROM employees e
    INNER JOIN subordinates s ON e.manager_id = s.employee_id
)
SELECT * FROM subordinates;

-- SQL Server - No RECURSIVE keyword
WITH subordinates AS (
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.name, e.manager_id, s.level + 1
    FROM employees e
    INNER JOIN subordinates s ON e.manager_id = s.employee_id
)
SELECT * FROM subordinates;

-- Oracle - CONNECT BY (traditional hierarchical queries)
SELECT employee_id, name, manager_id, LEVEL
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR employee_id = manager_id;
```

## Window Functions - Frame Specifications

```sql
-- PostgreSQL - Full support
SELECT
    order_date,
    total,
    SUM(total) OVER (
        ORDER BY order_date
        RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
    ) as rolling_7day
FROM orders;

-- MySQL (8.0+) - Limited RANGE support (no intervals)
SELECT
    order_date,
    total,
    SUM(total) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as rolling_7rows
FROM orders;

-- SQL Server - Full support
SELECT
    order_date,
    total,
    SUM(total) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as rolling_7rows
FROM orders;

-- Oracle - Full support
SELECT
    order_date,
    total,
    SUM(total) OVER (
        ORDER BY order_date
        RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW
    ) as rolling_7day
FROM orders;
```

## UPSERT (Insert or Update)

```sql
-- PostgreSQL (ON CONFLICT)
INSERT INTO products (product_id, name, price)
VALUES (123, 'Widget', 29.99)
ON CONFLICT (product_id)
DO UPDATE SET name = EXCLUDED.name, price = EXCLUDED.price;

-- MySQL (ON DUPLICATE KEY)
INSERT INTO products (product_id, name, price)
VALUES (123, 'Widget', 29.99)
ON DUPLICATE KEY UPDATE name = VALUES(name), price = VALUES(price);

-- MySQL 8.0.19+ (alternative)
INSERT INTO products (product_id, name, price)
VALUES (123, 'Widget', 29.99) AS new
ON DUPLICATE KEY UPDATE name = new.name, price = new.price;

-- SQL Server (MERGE)
MERGE INTO products AS target
USING (SELECT 123 AS product_id, 'Widget' AS name, 29.99 AS price) AS source
ON target.product_id = source.product_id
WHEN MATCHED THEN
    UPDATE SET name = source.name, price = source.price
WHEN NOT MATCHED THEN
    INSERT (product_id, name, price)
    VALUES (source.product_id, source.name, source.price);

-- Oracle (MERGE)
MERGE INTO products target
USING (SELECT 123 AS product_id, 'Widget' AS name, 29.99 AS price FROM DUAL) source
ON (target.product_id = source.product_id)
WHEN MATCHED THEN
    UPDATE SET name = source.name, price = source.price
WHEN NOT MATCHED THEN
    INSERT (product_id, name, price)
    VALUES (source.product_id, source.name, source.price);
```

## Data Type Mapping

| Concept | PostgreSQL | MySQL | SQL Server | Oracle |
|---------|-----------|-------|------------|--------|
| Integer | INT, BIGINT | INT, BIGINT | INT, BIGINT | NUMBER(10), NUMBER(19) |
| Decimal | NUMERIC, DECIMAL | DECIMAL | DECIMAL, NUMERIC | NUMBER(p,s) |
| String | VARCHAR, TEXT | VARCHAR, TEXT | VARCHAR, NVARCHAR | VARCHAR2, CLOB |
| Binary | BYTEA | BLOB, BINARY | VARBINARY, IMAGE | BLOB, RAW |
| Boolean | BOOLEAN | BOOLEAN/TINYINT(1) | BIT | NUMBER(1) |
| Date | DATE | DATE | DATE | DATE |
| Timestamp | TIMESTAMP | DATETIME, TIMESTAMP | DATETIME, DATETIME2 | TIMESTAMP |
| UUID | UUID | CHAR(36), BINARY(16) | UNIQUEIDENTIFIER | RAW(16) |
| JSON | JSON, JSONB | JSON | NVARCHAR(MAX) | CLOB |
| Array | ARRAY | JSON | Table variable | VARRAY, nested table |

## Performance Tips by Database

**PostgreSQL:**
- Use EXPLAIN ANALYZE with BUFFERS
- Leverage JSONB with GIN indexes
- Use parallel query settings for large scans
- Vacuum and analyze regularly
- Consider table partitioning for 10M+ rows

**MySQL:**
- Choose InnoDB over MyISAM
- Optimize buffer pool size
- Use covering indexes aggressively
- Be aware of case-insensitive defaults
- Consider read replicas for scaling

**SQL Server:**
- Update statistics regularly
- Use columnstore indexes for warehousing
- Leverage query hints sparingly
- Monitor execution plans
- Use In-Memory OLTP for hot tables

**Oracle:**
- Use EXPLAIN PLAN
- Leverage partitioning features
- Use bind variables to avoid parsing
- Configure SGA/PGA appropriately
- Consider Real Application Clusters (RAC)

---

## Reference: Optimization

# Query Optimization

## EXPLAIN Plan Analysis

```sql
-- PostgreSQL EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) as order_count,
    SUM(o.total) as lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_at >= '2024-01-01'
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 5;

/*
Key metrics to analyze:
- Planning Time: Time to generate plan
- Execution Time: Actual runtime
- Seq Scan: Table scans (bad for large tables)
- Index Scan: Using indexes (good)
- Rows: Estimated vs actual (large difference = stale stats)
- Buffers: shared hit = cache, read = disk I/O
- Loops: Nested loop iterations
*/

-- MySQL EXPLAIN
EXPLAIN FORMAT=JSON
SELECT * FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
  AND c.country = 'US';

-- SQL Server execution plan
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT ...;

-- Check actual vs estimated rows
SELECT * FROM sys.dm_exec_query_stats;
```

## Index Design and Optimization

```sql
-- Covering index (all columns in index)
CREATE INDEX idx_orders_covering ON orders (
    customer_id,
    order_date
) INCLUDE (total, status);

-- Query uses index-only scan (no table access needed)
SELECT customer_id, order_date, total, status
FROM orders
WHERE customer_id = 123
  AND order_date >= '2024-01-01';

-- Composite index (order matters!)
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date DESC);
-- Good: WHERE customer_id = X AND order_date > Y
-- Good: WHERE customer_id = X
-- Bad: WHERE order_date > Y (doesn't use index)

-- Partial/Filtered index (smaller, faster)
CREATE INDEX idx_active_orders ON orders (customer_id, order_date)
WHERE status = 'active';

-- Only used when query includes the filter
SELECT * FROM orders
WHERE customer_id = 123
  AND status = 'active'
  AND order_date >= '2024-01-01';

-- Expression/Function-based index
CREATE INDEX idx_users_lower_email ON users (LOWER(email));

-- Now this uses the index
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- GIN index for arrays/JSONB (PostgreSQL)
CREATE INDEX idx_products_tags ON products USING GIN (tags);
SELECT * FROM products WHERE tags @> ARRAY['electronics', 'sale'];

CREATE INDEX idx_orders_metadata ON orders USING GIN (metadata jsonb_path_ops);
SELECT * FROM orders WHERE metadata @> '{"priority": "high"}';
```

## Index Maintenance

```sql
-- PostgreSQL: Find missing indexes
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan as avg_seq_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
  AND seq_tup_read / seq_scan > 10000
ORDER BY seq_tup_read DESC;

-- Find unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE 'pg_toast%'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find duplicate indexes
SELECT
    pg_size_pretty(SUM(pg_relation_size(idx))::BIGINT) as size,
    (array_agg(idx))[1] as idx1,
    (array_agg(idx))[2] as idx2,
    (array_agg(idx))[3] as idx3
FROM (
    SELECT
        indexrelid::regclass as idx,
        (indrelid::text ||E'\n'|| indclass::text ||E'\n'||
         indkey::text ||E'\n'|| COALESCE(indexprs::text,'')||E'\n'||
         COALESCE(indpred::text,'')) as key
    FROM pg_index
) sub
GROUP BY key
HAVING COUNT(*) > 1
ORDER BY SUM(pg_relation_size(idx)) DESC;

-- Reindex to reduce bloat
REINDEX INDEX CONCURRENTLY idx_orders_customer_date;

-- Update statistics
ANALYZE orders;
ANALYZE VERBOSE;  -- Show progress
```

## Query Rewriting Patterns

```sql
-- Avoid SELECT DISTINCT when possible
-- Bad: Forces sort/dedup
SELECT DISTINCT customer_id FROM orders WHERE status = 'active';

-- Good: Use EXISTS
SELECT customer_id FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.customer_id
      AND o.status = 'active'
);

-- Avoid NOT IN with NULLs
-- Bad: NULL handling issues and poor performance
SELECT * FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);

-- Good: Use NOT EXISTS
SELECT * FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);

-- Push down filtering early
-- Bad: Filter after JOIN
SELECT c.*, o.*
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'US' AND o.order_date >= '2024-01-01';

-- Good: Use WHERE in subquery/CTE to reduce JOIN size
WITH us_customers AS (
    SELECT customer_id, name
    FROM customers
    WHERE country = 'US'
),
recent_orders AS (
    SELECT customer_id, order_id, total
    FROM orders
    WHERE order_date >= '2024-01-01'
)
SELECT c.*, o.*
FROM us_customers c
JOIN recent_orders o ON c.customer_id = o.customer_id;

-- Avoid scalar subqueries in SELECT
-- Bad: N+1 problem
SELECT
    p.product_id,
    p.name,
    (SELECT COUNT(*) FROM reviews WHERE product_id = p.product_id) as review_count
FROM products p;

-- Good: Single JOIN with GROUP BY
SELECT
    p.product_id,
    p.name,
    COUNT(r.review_id) as review_count
FROM products p
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.name;
```

## Partitioning Strategies

```sql
-- Range partitioning by date (PostgreSQL)
CREATE TABLE orders (
    order_id SERIAL,
    customer_id INT,
    order_date DATE NOT NULL,
    total DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Partition pruning in action
EXPLAIN SELECT * FROM orders WHERE order_date >= '2024-02-01' AND order_date < '2024-03-01';
-- Only scans orders_2024_q1 partition

-- List partitioning by category
CREATE TABLE products (
    product_id SERIAL,
    category VARCHAR(50) NOT NULL,
    name VARCHAR(200)
) PARTITION BY LIST (category);

CREATE TABLE products_electronics PARTITION OF products
    FOR VALUES IN ('electronics', 'computers', 'phones');

CREATE TABLE products_clothing PARTITION OF products
    FOR VALUES IN ('clothing', 'shoes', 'accessories');

-- Hash partitioning for even distribution
CREATE TABLE users (
    user_id SERIAL,
    email VARCHAR(255)
) PARTITION BY HASH (user_id);

CREATE TABLE users_p0 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p1 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

## Materialized Views

```sql
-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT
    DATE_TRUNC('day', order_date) as day,
    COUNT(*) as order_count,
    SUM(total) as revenue,
    AVG(total) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM orders
GROUP BY DATE_TRUNC('day', order_date);

CREATE UNIQUE INDEX idx_daily_sales_day ON daily_sales_summary (day);

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;

-- Auto-refresh with trigger (PostgreSQL)
CREATE OR REPLACE FUNCTION refresh_daily_sales()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_refresh_daily_sales
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_daily_sales();
```

## Query Hints and Optimization

```sql
-- PostgreSQL: Force index usage (use sparingly)
SET enable_seqscan = OFF;
SELECT /*+ IndexScan(orders idx_orders_customer) */ * FROM orders WHERE customer_id = 123;
SET enable_seqscan = ON;

-- SQL Server: Query hints
SELECT * FROM orders WITH (INDEX(idx_orders_customer_date))
WHERE customer_id = 123;

-- Force specific join type
SELECT * FROM customers c
INNER MERGE JOIN orders o ON c.customer_id = o.customer_id;

-- MySQL: Index hints
SELECT * FROM orders USE INDEX (idx_orders_customer_date)
WHERE customer_id = 123;

SELECT * FROM orders FORCE INDEX (idx_orders_customer_date)
WHERE customer_id = 123;

-- PostgreSQL: Parallel query tuning
SET max_parallel_workers_per_gather = 4;
ALTER TABLE large_table SET (parallel_workers = 4);
```

## Performance Monitoring Queries

```sql
-- PostgreSQL: Find slow queries
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time,
    rows / calls as avg_rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Find blocking queries
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- Table bloat detection
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Best Practices Checklist

1. Always run EXPLAIN ANALYZE before optimizing
2. Create indexes on foreign keys and WHERE/JOIN columns
3. Use covering indexes for frequent queries
4. Keep statistics up to date (ANALYZE regularly)
5. Avoid SELECT *, specify needed columns
6. Use EXISTS instead of IN for subqueries
7. Filter early, aggregate late
8. Consider partitioning for large tables (>10M rows)
9. Use materialized views for expensive aggregations
10. Monitor slow query log and pg_stat_statements

---

## Reference: Query Patterns

# Query Patterns

## Common Table Expressions (CTEs)

```sql
-- Basic CTE for readability
WITH active_users AS (
    SELECT user_id, username, created_at
    FROM users
    WHERE is_active = true
      AND last_login >= CURRENT_DATE - INTERVAL '30 days'
),
user_orders AS (
    SELECT user_id, COUNT(*) as order_count, SUM(total) as total_spent
    FROM orders
    WHERE status = 'completed'
    GROUP BY user_id
)
SELECT
    u.username,
    u.created_at,
    COALESCE(o.order_count, 0) as orders,
    COALESCE(o.total_spent, 0) as lifetime_value
FROM active_users u
LEFT JOIN user_orders o ON u.user_id = o.user_id
WHERE COALESCE(o.order_count, 0) > 0
ORDER BY o.total_spent DESC;

-- CTE with multiple references (avoiding duplicate computation)
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', sale_date) as month,
        product_id,
        SUM(quantity) as total_quantity,
        SUM(amount) as total_amount
    FROM sales
    WHERE sale_date >= '2024-01-01'
    GROUP BY DATE_TRUNC('month', sale_date), product_id
)
SELECT
    current.month,
    current.product_id,
    current.total_amount,
    current.total_amount - COALESCE(previous.total_amount, 0) as growth,
    ROUND(100.0 * (current.total_amount - COALESCE(previous.total_amount, 0))
        / NULLIF(previous.total_amount, 0), 2) as growth_pct
FROM monthly_sales current
LEFT JOIN monthly_sales previous
    ON current.product_id = previous.product_id
    AND current.month = previous.month + INTERVAL '1 month';
```

## Recursive CTEs

```sql
-- Organizational hierarchy traversal
WITH RECURSIVE org_hierarchy AS (
    -- Anchor member: top-level managers
    SELECT
        employee_id,
        name,
        manager_id,
        1 as level,
        ARRAY[employee_id] as path,
        name as hierarchy_path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive member: employees reporting to current level
    SELECT
        e.employee_id,
        e.name,
        e.manager_id,
        h.level + 1,
        h.path || e.employee_id,
        h.hierarchy_path || ' > ' || e.name
    FROM employees e
    INNER JOIN org_hierarchy h ON e.manager_id = h.employee_id
    WHERE NOT e.employee_id = ANY(h.path)  -- Prevent cycles
)
SELECT
    employee_id,
    REPEAT('  ', level - 1) || name as indented_name,
    level,
    hierarchy_path
FROM org_hierarchy
ORDER BY path;

-- Bill of materials (parts explosion)
WITH RECURSIVE parts_explosion AS (
    SELECT
        part_id,
        component_id,
        quantity,
        1 as level,
        ARRAY[part_id] as path
    FROM bill_of_materials
    WHERE part_id = 'PRODUCT-123'

    UNION ALL

    SELECT
        pe.part_id,
        bom.component_id,
        pe.quantity * bom.quantity,
        pe.level + 1,
        pe.path || bom.part_id
    FROM parts_explosion pe
    INNER JOIN bill_of_materials bom ON pe.component_id = bom.part_id
    WHERE NOT bom.part_id = ANY(pe.path)
)
SELECT
    component_id,
    SUM(quantity) as total_quantity,
    MAX(level) as max_depth
FROM parts_explosion
GROUP BY component_id;
```

## Advanced JOIN Patterns

```sql
-- Self-join for finding gaps in sequences
SELECT
    a.order_id as current_id,
    MIN(b.order_id) as next_id,
    MIN(b.order_id) - a.order_id - 1 as gap_size
FROM orders a
LEFT JOIN orders b ON b.order_id > a.order_id
GROUP BY a.order_id
HAVING MIN(b.order_id) - a.order_id > 1;

-- LATERAL join for correlated subqueries (PostgreSQL)
SELECT
    c.customer_id,
    c.name,
    recent.order_date,
    recent.total
FROM customers c
CROSS JOIN LATERAL (
    SELECT order_date, total
    FROM orders o
    WHERE o.customer_id = c.customer_id
    ORDER BY order_date DESC
    LIMIT 3
) recent;

-- Anti-join pattern (records in A not in B)
SELECT u.user_id, u.email
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL;

-- Using EXISTS (more efficient than IN for large sets)
SELECT u.user_id, u.email
FROM users u
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.user_id
);
```

## Subquery Optimization

```sql
-- Scalar subquery in SELECT (use sparingly - can cause N+1)
SELECT
    p.product_id,
    p.name,
    (SELECT COUNT(*) FROM reviews r WHERE r.product_id = p.product_id) as review_count,
    (SELECT AVG(rating) FROM reviews r WHERE r.product_id = p.product_id) as avg_rating
FROM products p;

-- Better: Use JOINs with aggregation
SELECT
    p.product_id,
    p.name,
    COALESCE(r.review_count, 0) as review_count,
    r.avg_rating
FROM products p
LEFT JOIN (
    SELECT
        product_id,
        COUNT(*) as review_count,
        AVG(rating) as avg_rating
    FROM reviews
    GROUP BY product_id
) r ON p.product_id = r.product_id;

-- Correlated subquery for filtering
SELECT
    order_id,
    customer_id,
    total
FROM orders o1
WHERE total > (
    SELECT AVG(total)
    FROM orders o2
    WHERE o2.customer_id = o1.customer_id
);

-- Better: Use window functions
SELECT
    order_id,
    customer_id,
    total
FROM (
    SELECT
        order_id,
        customer_id,
        total,
        AVG(total) OVER (PARTITION BY customer_id) as avg_customer_total
    FROM orders
) x
WHERE total > avg_customer_total;
```

## PIVOT/UNPIVOT Operations

```sql
-- PostgreSQL CROSSTAB (requires tablefunc extension)
CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT * FROM crosstab(
    'SELECT customer_id, product_category, SUM(amount)
     FROM sales
     GROUP BY customer_id, product_category
     ORDER BY customer_id, product_category',
    'SELECT DISTINCT product_category FROM sales ORDER BY 1'
) AS ct(customer_id INT, electronics NUMERIC, clothing NUMERIC, food NUMERIC);

-- Manual PIVOT with CASE
SELECT
    customer_id,
    SUM(CASE WHEN product_category = 'electronics' THEN amount ELSE 0 END) as electronics,
    SUM(CASE WHEN product_category = 'clothing' THEN amount ELSE 0 END) as clothing,
    SUM(CASE WHEN product_category = 'food' THEN amount ELSE 0 END) as food
FROM sales
GROUP BY customer_id;

-- UNPIVOT pattern (row to column)
SELECT customer_id, 'electronics' as category, electronics as amount
FROM customer_sales WHERE electronics > 0
UNION ALL
SELECT customer_id, 'clothing', clothing
FROM customer_sales WHERE clothing > 0
UNION ALL
SELECT customer_id, 'food', food
FROM customer_sales WHERE food > 0;
```

## Set Operations

```sql
-- UNION for combining distinct results
SELECT product_id FROM active_products
UNION
SELECT product_id FROM featured_products;

-- UNION ALL for better performance (includes duplicates)
SELECT user_id, 'signup' as event FROM signups WHERE date = CURRENT_DATE
UNION ALL
SELECT user_id, 'purchase' as event FROM purchases WHERE date = CURRENT_DATE;

-- INTERSECT for common records
SELECT email FROM newsletter_subscribers
INTERSECT
SELECT email FROM premium_members;

-- EXCEPT for difference (A - B)
SELECT email FROM all_users
EXCEPT
SELECT email FROM unsubscribed_users;
```

## Performance Tips

1. **CTE Materialization**: PostgreSQL 12+ materializes CTEs by default. Use `WITH cte AS MATERIALIZED` or `NOT MATERIALIZED` to control
2. **JOIN Order**: Database optimizers handle this, but put smaller tables first in manual optimization
3. **EXISTS vs IN**: Use EXISTS for correlated checks, IN for small static lists
4. **Subquery vs JOIN**: Prefer JOINs for readability and optimizer friendliness
5. **UNION ALL vs UNION**: Use UNION ALL when duplicates are acceptable (no deduplication cost)

---

## Reference: Window Functions

# Window Functions

## Ranking Functions

```sql
-- ROW_NUMBER: Sequential numbering within partition
SELECT
    customer_id,
    order_date,
    total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as row_num
FROM orders;

-- Get most recent order per customer
SELECT *
FROM (
    SELECT
        customer_id,
        order_id,
        order_date,
        total,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as rn
    FROM orders
) ranked
WHERE rn = 1;

-- RANK: Same values get same rank, gaps in sequence
SELECT
    student_id,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num
FROM exam_results;
/*
score=100: rank=1, dense_rank=1, row_num=1
score=100: rank=1, dense_rank=1, row_num=2
score=95:  rank=3, dense_rank=2, row_num=3
*/

-- NTILE: Divide into N buckets
SELECT
    customer_id,
    total_spent,
    NTILE(4) OVER (ORDER BY total_spent DESC) as quartile
FROM customer_lifetime_value;
```

## Aggregate Window Functions

```sql
-- Running totals and cumulative sums
SELECT
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY order_date) as cumulative_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as rolling_7day_avg
FROM daily_sales;

-- Moving average with RANGE
SELECT
    sale_date,
    amount,
    AVG(amount) OVER (
        ORDER BY sale_date
        RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
    ) as avg_last_7_days
FROM sales;

-- Partition-specific aggregates
SELECT
    product_id,
    sale_date,
    quantity,
    SUM(quantity) OVER (PARTITION BY product_id ORDER BY sale_date) as cumulative_qty,
    AVG(quantity) OVER (PARTITION BY product_id) as avg_qty_for_product,
    quantity::FLOAT / SUM(quantity) OVER (PARTITION BY product_id) as pct_of_total
FROM product_sales;
```

## LAG and LEAD Functions

```sql
-- Compare with previous/next row
SELECT
    order_date,
    total,
    LAG(total) OVER (ORDER BY order_date) as previous_day_total,
    LEAD(total) OVER (ORDER BY order_date) as next_day_total,
    total - LAG(total) OVER (ORDER BY order_date) as day_over_day_change
FROM daily_orders;

-- Find gaps in time series
SELECT
    event_date,
    LAG(event_date) OVER (ORDER BY event_date) as prev_date,
    event_date - LAG(event_date) OVER (ORDER BY event_date) as days_since_last
FROM events
WHERE event_date - LAG(event_date) OVER (ORDER BY event_date) > 7;

-- Session analysis with time gaps
SELECT
    user_id,
    action_time,
    LAG(action_time) OVER (PARTITION BY user_id ORDER BY action_time) as prev_action,
    EXTRACT(EPOCH FROM (
        action_time - LAG(action_time) OVER (PARTITION BY user_id ORDER BY action_time)
    )) / 60 as minutes_since_last_action,
    CASE
        WHEN EXTRACT(EPOCH FROM (
            action_time - LAG(action_time) OVER (PARTITION BY user_id ORDER BY action_time)
        )) / 60 > 30 THEN 1
        ELSE 0
    END as new_session
FROM user_actions;
```

## FIRST_VALUE and LAST_VALUE

```sql
-- Compare each row to first/last in partition
SELECT
    product_id,
    price_date,
    price,
    FIRST_VALUE(price) OVER (
        PARTITION BY product_id
        ORDER BY price_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as initial_price,
    LAST_VALUE(price) OVER (
        PARTITION BY product_id
        ORDER BY price_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as current_price,
    price - FIRST_VALUE(price) OVER (
        PARTITION BY product_id
        ORDER BY price_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as price_change_from_start
FROM product_price_history;

-- NTH_VALUE: Get specific positioned value
SELECT
    sale_date,
    amount,
    NTH_VALUE(amount, 2) OVER (
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as second_day_amount
FROM daily_sales;
```

## Frame Specifications

```sql
-- ROWS vs RANGE difference
SELECT
    order_date,
    amount,
    -- ROWS: Physical row offset
    SUM(amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
    ) as sum_5_rows,
    -- RANGE: Logical value range
    SUM(amount) OVER (
        ORDER BY order_date
        RANGE BETWEEN INTERVAL '2 days' PRECEDING AND INTERVAL '2 days' FOLLOWING
    ) as sum_5_day_range
FROM orders;

-- Common frame patterns
SELECT
    sale_date,
    revenue,
    -- All preceding rows
    SUM(revenue) OVER (
        ORDER BY sale_date
        ROWS UNBOUNDED PRECEDING
    ) as running_total,
    -- Last 3 rows including current
    AVG(revenue) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as ma_3,
    -- Entire partition
    SUM(revenue) OVER (
        PARTITION BY EXTRACT(YEAR FROM sale_date)
    ) as yearly_total,
    -- Centered window
    AVG(revenue) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
    ) as centered_ma_7
FROM sales;
```

## Advanced Analytics

```sql
-- Percentile calculations
SELECT
    employee_id,
    salary,
    PERCENT_RANK() OVER (ORDER BY salary) as pct_rank,
    CUME_DIST() OVER (ORDER BY salary) as cumulative_dist,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) OVER () as median_salary,
    PERCENTILE_DISC(0.9) WITHIN GROUP (ORDER BY salary) OVER () as p90_salary
FROM employees;

-- Cohort retention analysis
WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) as cohort_month,
        DATE_TRUNC('month', activity_date) as activity_month
    FROM user_activity
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT user_id) as cohort_size
    FROM user_cohorts
    GROUP BY cohort_month
)
SELECT
    uc.cohort_month,
    uc.activity_month,
    EXTRACT(MONTH FROM AGE(uc.activity_month, uc.cohort_month)) as months_since_signup,
    COUNT(DISTINCT uc.user_id) as active_users,
    cs.cohort_size,
    ROUND(100.0 * COUNT(DISTINCT uc.user_id) / cs.cohort_size, 2) as retention_pct
FROM user_cohorts uc
JOIN cohort_sizes cs ON uc.cohort_month = cs.cohort_month
GROUP BY uc.cohort_month, uc.activity_month, cs.cohort_size
ORDER BY uc.cohort_month, months_since_signup;

-- Time-series gap filling
SELECT
    date_series.date,
    COALESCE(s.revenue, 0) as revenue,
    AVG(s.revenue) OVER (
        ORDER BY date_series.date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7day
FROM generate_series(
    '2024-01-01'::DATE,
    '2024-12-31'::DATE,
    '1 day'::INTERVAL
) AS date_series(date)
LEFT JOIN sales s ON date_series.date = s.sale_date;
```

## Conditional Aggregation with Windows

```sql
-- Filter within window function
SELECT
    product_id,
    sale_date,
    quantity,
    SUM(quantity) FILTER (WHERE quantity > 10) OVER (
        PARTITION BY product_id
        ORDER BY sale_date
    ) as cumulative_large_orders,
    COUNT(*) FILTER (WHERE quantity > 100) OVER (
        PARTITION BY product_id
    ) as total_bulk_orders
FROM sales;

-- Multiple conditions
SELECT
    customer_id,
    order_date,
    total,
    COUNT(*) FILTER (WHERE total > 1000) OVER (
        PARTITION BY customer_id
    ) as high_value_order_count,
    AVG(total) FILTER (WHERE total < 100) OVER (
        PARTITION BY customer_id
    ) as avg_small_order_value
FROM orders;
```

## Performance Considerations

```sql
-- Avoid multiple window passes - combine into one
-- Bad: Multiple scans
SELECT
    product_id,
    (SELECT AVG(price) FROM products) as avg_price,
    (SELECT MAX(price) FROM products) as max_price
FROM products;

-- Good: Single window pass
SELECT DISTINCT
    AVG(price) OVER () as avg_price,
    MAX(price) OVER () as max_price
FROM products;

-- Materialize expensive windows
CREATE MATERIALIZED VIEW product_rankings AS
SELECT
    product_id,
    category,
    sales_count,
    RANK() OVER (PARTITION BY category ORDER BY sales_count DESC) as category_rank,
    PERCENT_RANK() OVER (ORDER BY sales_count DESC) as overall_percentile
FROM product_sales_summary;

CREATE INDEX idx_product_rankings_category ON product_rankings(category, category_rank);
```

## Common Patterns

1. **Top N per Group**: Use ROW_NUMBER() with WHERE rn <= N
2. **Running Totals**: SUM() OVER (ORDER BY date)
3. **Moving Averages**: AVG() with ROWS BETWEEN N PRECEDING
4. **Session Analysis**: LAG() to detect time gaps
5. **Deduplication**: ROW_NUMBER() OVER (PARTITION BY key ORDER BY priority) WHERE rn = 1
6. **Percentiles**: PERCENT_RANK() or PERCENTILE_CONT()
7. **Year-over-Year**: LAG(value, 12) OVER (ORDER BY month)
8. **Cohort Analysis**: PARTITION BY cohort_date, aggregate over activity periods
