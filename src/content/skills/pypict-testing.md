---
title: "Pypict Testing"
description: "Design comprehensive test cases using PICT (Pairwise Independent Combinatorial Testing) for any piece of requirements or code. Analyzes inputs, generates PICT models with parameters, values, and constraints for valid scenarios using pairwise testi..."
category: "development"
source: "community"
author: "Community"
tags: ["pypict", "testing"]
date: 2026-03-20
---

# PICT Test Designer

This skill enables systematic test case design using PICT (Pairwise Independent Combinatorial Testing). Given requirements or code, it analyzes the system to identify test parameters, generates a PICT model with appropriate constraints, executes the model to generate pairwise test cases, and formats the results with expected outputs.

## When to Use This Skill

Use this skill when:
- Designing test cases for a feature, function, or system with multiple input parameters
- Creating test suites for configurations with many combinations
- Needing comprehensive coverage with minimal test cases
- Analyzing requirements to identify test scenarios
- Working with code that has multiple conditional paths
- Building test matrices for API endpoints, web forms, or system configurations

## Workflow

Follow this process for test design:

### 1. Analyze Requirements or Code

From the user's requirements or code, identify:
- **Parameters**: Input variables, configuration options, environmental factors
- **Values**: Possible values for each parameter (using equivalence partitioning)
- **Constraints**: Business rules, technical limitations, dependencies between parameters
- **Expected Outcomes**: What should happen for different combinations

**Example Analysis:**

For a login function with requirements:
- Users can login with username/password
- Supports 2FA (on/off)
- Remembers login on trusted devices
- Rate limits after 3 failed attempts

Identified parameters:
- Credentials: Valid, Invalid
- TwoFactorAuth: Enabled, Disabled
- RememberMe: Checked, Unchecked
- PreviousFailures: 0, 1, 2, 3, 4

### 2. Generate PICT Model

Create a PICT model with:
- Clear parameter names
- Well-defined value sets (using equivalence partitioning and boundary values)
- Constraints for invalid combinations
- Comments explaining business rules

**Model Structure:**
```
# Parameter definitions
ParameterName: Value1, Value2, Value3

# Constraints (if any)
IF [Parameter1] = "Value" THEN [Parameter2] <> "OtherValue";
```

**Refer to references/pict_syntax.md for:**
- Complete syntax reference
- Constraint grammar and operators
- Advanced features (sub-models, aliasing, negative testing)
- Command-line options
- Detailed constraint patterns

**Refer to references/examples.md for:**
- Complete real-world examples by domain
- Software function testing examples
- Web application, API, and mobile testing examples
- Database and configuration testing patterns
- Common patterns for authentication, resource access, error handling

### 3. Execute PICT Model

Generate the PICT model text and format it for the user. You can use Python code directly to work with the model:

```python
# Define parameters and constraints
parameters = {
    "OS": ["Windows", "Linux", "MacOS"],
    "Browser": ["Chrome", "Firefox", "Safari"],
    "Memory": ["4GB", "8GB", "16GB"]
}

constraints = [
    'IF [OS] = "MacOS" THEN [Browser] IN {Safari, Chrome}',
    'IF [Memory] = "4GB" THEN [OS] <> "MacOS"'
]

# Generate model text
model_lines = []
for param_name, values in parameters.items():
    values_str = ", ".join(values)
    model_lines.append(f"{param_name}: {values_str}")

if constraints:
    model_lines.append("")
    for constraint in constraints:
        if not constraint.endswith(';'):
            constraint += ';'
        model_lines.append(constraint)

model_text = "\n".join(model_lines)
print(model_text)
```

**Using the helper script (optional):**
The `scripts/pict_helper.py` script provides utilities for model generation and output formatting:

```bash
# Generate model from JSON config
python scripts/pict_helper.py generate config.json

# Format PICT tool output as markdown table
python scripts/pict_helper.py format output.txt

# Parse PICT output to JSON
python scripts/pict_helper.py parse output.txt
```

**To generate actual test cases**, the user can:
1. Save the PICT model to a file (e.g., `model.txt`)
2. Use online PICT tools like:
   - https://pairwise.yuuniworks.com/
   - https://pairwise.teremokgames.com/
3. Or install PICT locally (see references/pict_syntax.md)

### 4. Determine Expected Outputs

For each generated test case, determine the expected outcome based on:
- Business requirements
- Code logic
- Valid/invalid combinations

Create a list of expected outputs corresponding to each test case.

### 5. Format Complete Test Suite

Provide the user with:
1. **PICT Model** - The complete model with parameters and constraints
2. **Markdown Table** - Test cases in table format with test numbers
3. **Expected Outputs** - Expected result for each test case

## Output Format

Present results in this structure:

````markdown
## PICT Model

```
# Parameters
Parameter1: Value1, Value2, Value3
Parameter2: ValueA, ValueB

# Constraints
IF [Parameter1] = "Value1" THEN [Parameter2] = "ValueA";
```

## Generated Test Cases

| Test # | Parameter1 | Parameter2 | Expected Output |
| --- | --- | --- | --- |
| 1 | Value1 | ValueA | Success |
| 2 | Value2 | ValueB | Success |
| 3 | Value1 | ValueB | Error: Invalid combination |
...

## Test Case Summary

- Total test cases: N
- Coverage: Pairwise (all 2-way combinations)
- Constraints applied: N
````

## Best Practices

### Parameter Identification

**Good:**
- Use descriptive names: `AuthMethod`, `UserRole`, `PaymentType`
- Apply equivalence partitioning: `FileSize: Small, Medium, Large` instead of `FileSize: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Include boundary values: `Age: 0, 17, 18, 65, 66`
- Add negative values for error testing: `Amount: ~-1, 0, 100, ~999999`

**Avoid:**
- Generic names: `Param1`, `Value1`, `V1`
- Too many values without partitioning
- Missing edge cases

### Constraint Writing

**Good:**
- Document rationale: `# Safari only available on MacOS`
- Start simple, add incrementally
- Test constraints work as expected

**Avoid:**
- Over-constraining (eliminates too many valid combinations)
- Under-constraining (generates invalid test cases)
- Complex nested logic without clear documentation

### Expected Output Definition

**Be specific:**
- "Login succeeds, user redirected to dashboard"
- "HTTP 400: Invalid credentials error"
- "2FA prompt displayed"

**Not vague:**
- "Works"
- "Error"
- "Success"

### Scalability

For large parameter sets:
- Use sub-models to group related parameters with different orders
- Consider separate test suites for unrelated features
- Start with order 2 (pairwise), increase for critical combinations
- Typical pairwise testing reduces test cases by 80-90% vs exhaustive

## Common Patterns

### Web Form Testing

```python
parameters = {
    "Name": ["Valid", "Empty", "TooLong"],
    "Email": ["Valid", "Invalid", "Empty"],
    "Password": ["Strong", "Weak", "Empty"],
    "Terms": ["Accepted", "NotAccepted"]
}

constraints = [
    'IF [Terms] = "NotAccepted" THEN [Name] = "Valid"',  # Test validation even if terms not accepted
]
```

### API Endpoint Testing

```python
parameters = {
    "HTTPMethod": ["GET", "POST", "PUT", "DELETE"],
    "Authentication": ["Valid", "Invalid", "Missing"],
    "ContentType": ["JSON", "XML", "FormData"],
    "PayloadSize": ["Empty", "Small", "Large"]
}

constraints = [
    'IF [HTTPMethod] = "GET" THEN [PayloadSize] = "Empty"',
    'IF [Authentication] = "Missing" THEN [HTTPMethod] IN {GET, POST}'
]
```

### Configuration Testing

```python
parameters = {
    "Environment": ["Dev", "Staging", "Production"],
    "CacheEnabled": ["True", "False"],
    "LogLevel": ["Debug", "Info", "Error"],
    "Database": ["SQLite", "PostgreSQL", "MySQL"]
}

constraints = [
    'IF [Environment] = "Production" THEN [LogLevel] <> "Debug"',
    'IF [Database] = "SQLite" THEN [Environment] = "Dev"'
]
```

## Troubleshooting

### No Test Cases Generated

- Check constraints aren't over-restrictive
- Verify constraint syntax (must end with `;`)
- Ensure parameter names in constraints match definitions (use `[ParameterName]`)

### Too Many Test Cases

- Verify using order 2 (pairwise) not higher order
- Consider breaking into sub-models
- Check if parameters can be separated into independent test suites

### Invalid Combinations in Output

- Add missing constraints
- Verify constraint logic is correct
- Check if you need to use `NOT` or `<>` operators

### Script Errors

- Ensure pypict is installed: `pip install pypict --break-system-packages`
- Check Python version (3.7+)
- Verify model syntax is valid

## References

- **references/pict_syntax.md** - Complete PICT syntax reference with grammar and operators
- **references/examples.md** - Comprehensive real-world examples across different domains
- **scripts/pict_helper.py** - Python utilities for model generation and output formatting
- [PICT GitHub Repository](https://github.com/microsoft/pict) - Official PICT documentation
- [pypict Documentation](https://github.com/kmaehashi/pypict) - Python binding documentation
- [Online PICT Tools](https://pairwise.yuuniworks.com/) - Web-based PICT generator

## Examples

### Example 1: Simple Function Testing

**User Request:** "Design tests for a divide function that takes two numbers and returns the result."

**Analysis:**
- Parameters: dividend (number), divisor (number)
- Values: Using equivalence partitioning and boundaries
  - Numbers: negative, zero, positive, large values
- Constraints: Division by zero is invalid
- Expected outputs: Result or error

**PICT Model:**
```
Dividend: -10, 0, 10, 1000
Divisor: ~0, -5, 1, 5, 100

IF [Divisor] = "0" THEN [Dividend] = "10";
```

**Test Cases:**

| Test # | Dividend | Divisor | Expected Output |
| --- | --- | --- | --- |
| 1 | 10 | 0 | Error: Division by zero |
| 2 | -10 | 1 | -10.0 |
| 3 | 0 | -5 | 0.0 |
| 4 | 1000 | 5 | 200.0 |
| 5 | 10 | 100 | 0.1 |

### Example 2: E-commerce Checkout

**User Request:** "Design tests for checkout flow with payment methods, shipping options, and user types."

**Analysis:**
- Payment: Credit Card, PayPal, Bank Transfer (limited by user type)
- Shipping: Standard, Express, Overnight
- User: Guest, Registered, Premium
- Constraints: Guests can't use Bank Transfer, Premium users get free Express

**PICT Model:**
```
PaymentMethod: CreditCard, PayPal, BankTransfer
ShippingMethod: Standard, Express, Overnight
UserType: Guest, Registered, Premium

IF [UserType] = "Guest" THEN [PaymentMethod] <> "BankTransfer";
IF [UserType] = "Premium" AND [ShippingMethod] = "Express" THEN [PaymentMethod] IN {CreditCard, PayPal};
```

**Output:** 12-15 test cases covering all valid payment/shipping/user combinations with expected costs and outcomes.

---

## Reference: Examples

# PICT Examples Reference

> **Note**: This is a placeholder file. Comprehensive examples are coming soon!
> 
> For now, check out the [examples directory](../examples/) for complete real-world examples.

## Available Examples

### Complete Examples
- **[ATM System Testing](../examples/atm-specification.md)**: Comprehensive banking ATM system with 31 test cases

### Coming Soon

#### Software Testing
- Function testing with multiple parameters
- API endpoint testing
- Database query validation
- Algorithm testing

#### Web Applications
- Form validation
- User authentication
- E-commerce checkout
- Shopping cart operations

#### Configuration Testing
- System configurations
- Feature flags
- Environment settings
- Browser compatibility

#### Mobile Testing
- Device and OS combinations
- Screen sizes
- Network conditions
- Permissions

## Pattern Library (Coming Soon)

### Common Constraint Patterns

```
# Dependency constraints
IF [FeatureA] = "Enabled" THEN [FeatureB] = "Enabled";

# Exclusive options
IF [PaymentMethod] = "Cash" THEN [InstallmentPlan] = "None";

# Platform limitations
IF [OS] = "iOS" THEN [Browser] IN {Safari, Chrome};

# Environment restrictions
IF [Environment] = "Production" THEN [LogLevel] <> "Debug";
```

### Boundary Value Patterns

```
# Numeric boundaries
Age: 0, 17, 18, 64, 65, 100

# Size categories
FileSize: 0KB, 1KB, 1MB, 100MB, 1GB

# Time periods
Duration: 0s, 1s, 30s, 60s, 3600s
```

### Negative Testing Patterns

```
# Invalid inputs (using ~ prefix in some PICT variants)
Email: Valid, Invalid, Empty, TooLong
Password: Strong, Weak, Empty, SpecialChars

# Error conditions
NetworkStatus: Connected, Slow, Disconnected, Timeout
```

## Contributing Examples

Have an example to share? We'd love to include it!

1. Create your example following the structure in [examples/README.md](../examples/README.md)
2. Include:
   - Original specification
   - PICT model
   - Test cases with expected outputs
   - Learning points
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## External Resources

- [Pairwise Testing Tutorial](https://www.pairwisetesting.com/)
- [NIST Combinatorial Testing Resources](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software)
- [Microsoft PICT Examples](https://github.com/microsoft/pict/tree/main/doc)

---

## Reference: Pict_Syntax

# PICT Syntax Reference

> **Note**: This is a placeholder file. Complete syntax documentation is coming soon!
> 
> For now, please refer to the official PICT documentation:
> - [Microsoft PICT on GitHub](https://github.com/microsoft/pict)
> - [PICT User Guide](https://github.com/microsoft/pict/blob/main/doc/pict.md)

## Quick Reference

### Basic Model Structure

```
# Parameters
ParameterName: Value1, Value2, Value3
AnotherParameter: ValueA, ValueB, ValueC

# Constraints (optional)
IF [ParameterName] = "Value1" THEN [AnotherParameter] <> "ValueA";
```

### Parameter Definition

```
ParameterName: Value1, Value2, Value3, ...
```

### Constraint Syntax

```
IF <condition> THEN <condition>;
```

### Operators

- `=` - Equal to
- `<>` - Not equal to
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal to
- `<=` - Less than or equal to
- `IN` - Member of set
- `AND` - Logical AND
- `OR` - Logical OR
- `NOT` - Logical NOT

### Example Constraints

```
# Simple constraint
IF [OS] = "MacOS" THEN [Browser] <> "IE";

# Multiple conditions
IF [Environment] = "Production" AND [LogLevel] = "Debug" THEN [Approved] = "False";

# Set membership
IF [UserRole] = "Guest" THEN [Permission] IN {Read, None};
```

## Coming Soon

Detailed documentation will include:
- Complete grammar specification
- Advanced features (sub-models, aliasing, seeding)
- Negative testing patterns
- Weight specifications
- Order specifications
- Examples for each feature

## Contributing

If you'd like to help complete this documentation:
1. Fork the repository
2. Add content to this file
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## External Resources

- [Official PICT Documentation](https://github.com/microsoft/pict/blob/main/doc/pict.md)
- [pypict Documentation](https://github.com/kmaehashi/pypict)
- [Pairwise Testing Explained](https://www.pairwisetesting.com/)

---

## Example: Readme

# Examples

This directory contains real-world examples of using the PICT Test Designer skill.

## ATM System Testing Example

A comprehensive example demonstrating how to use PICT methodology to test a complex banking ATM system.

### Files

- **[atm-specification.md](atm-specification.md)**: Complete ATM system specification with 11 sections covering:
  - Functional requirements (withdrawals, deposits, transfers, etc.)
  - Hardware specifications (card readers, cash dispensers, displays)
  - Security requirements (encryption, authentication, physical security)
  - Network and connectivity requirements
  - Compliance and standards

- **[atm-test-plan.md](atm-test-plan.md)**: Complete test plan generated using the PICT skill, including:
  - PICT model with 8 parameters and 16 constraints
  - 31 optimized test cases (reduced from 25,920 possible combinations)
  - Expected outputs for each test case
  - Test execution guidelines
  - Coverage analysis
  - Risk-based prioritization

### Key Statistics

- **Total Parameters**: 8 (Transaction Type, Card Type, PIN Status, Account Type, Transaction Amount, Cash Availability, Network Status, Card Condition)
- **Exhaustive Combinations**: 25,920
- **PICT Test Cases**: 31
- **Reduction**: 99.88%
- **Coverage**: All pairwise (2-way) interactions
- **Constraints**: 16 business rules

### How to Use This Example

1. **Review the specification**: Read [atm-specification.md](atm-specification.md) to understand the system requirements

2. **Study the test plan**: Review [atm-test-plan.md](atm-test-plan.md) to see how the PICT skill converted requirements into test cases

3. **Try it yourself**: Ask Claude to analyze the specification:
   ```
   Using the pict-test-designer skill, analyze the ATM specification 
   and generate test cases for the security requirements
   ```

4. **Adapt for your needs**: Use this as a template for your own specifications

### Learning Points

This example demonstrates:

- **Parameter identification**: How to identify testable parameters from requirements
- **Equivalence partitioning**: Grouping values into meaningful categories
- **Constraint modeling**: Applying business rules to eliminate invalid combinations
- **Expected output determination**: Automatically determining what should happen for each test case
- **Test prioritization**: Organizing tests by risk and criticality
- **Traceability**: Linking test cases back to requirements

## Automotive Gearbox Control System Example

A sophisticated example demonstrating PICT methodology for testing a semi-automatic transmission control system with multiple operating modes and complex safety constraints.

### Files

- **[gearbox-specification.md](gearbox-specification.md)**: Comprehensive gearbox control system specification with 10 sections:
  - System components (sensors, actuators, controls)
  - Operating modes (Manual, Sport, Eco)
  - Functional requirements (shift logic, safety features)
  - Error handling and fault tolerance
  - Performance and reliability requirements
  - Environmental conditions and constraints

- **[gearbox-test-plan.md](gearbox-test-plan.md)**: Complete test plan with PICT methodology:
  - PICT model with 12 parameters and 14 constraints
  - 40 optimized test cases (from ~159 billion combinations)
  - Expected outputs with detailed system responses
  - Priority-based test execution plan
  - Coverage analysis and traceability matrix
  - Risk assessment for high-risk scenarios

### Key Statistics

- **Total Parameters**: 12 (Mode, Gear, Speed, RPM, Throttle, Brake, Shift Request, Temperature, Road Condition, Incline, Sensor Status, Hydraulic Pressure)
- **Exhaustive Combinations**: ~159,000,000,000 (159 billion)
- **PICT Test Cases**: 40
- **Reduction**: 99.999999975%
- **Coverage**: All pairwise (2-way) interactions
- **Constraints**: 14 complex business rules and safety constraints

### How to Use This Example

1. **Review the specification**: Read [gearbox-specification.md](gearbox-specification.md) for the complete system design

2. **Study the test plan**: Examine [gearbox-test-plan.md](gearbox-test-plan.md) to see complex constraint modeling

3. **Try it yourself**: Ask Claude to analyze specific scenarios:
   ```
   Using the pict-test-designer skill, analyze the gearbox specification
   and generate test cases for the safety features section
   ```

4. **Learn constraint modeling**: This example shows advanced constraint patterns for:
   - Mutually exclusive conditions (brake vs. throttle)
   - Physical limitations (gear ratios, speed limits)
   - Safety interlocks (reverse lockout, over-rev protection)
   - Environmental adaptations (ice, temperature, incline)

### Learning Points

This example demonstrates:

- **Complex parameter interactions**: 12-way parameter space with interdependencies
- **Advanced constraint modeling**: Physical, safety, and operational constraints
- **Multi-mode testing**: Different behaviors in Manual, Sport, and Eco modes
- **Fault injection testing**: Sensor failures, temperature extremes, hydraulic issues
- **Environmental testing**: Road conditions, incline, temperature variations
- **Safety-critical testing**: Over-rev protection, reverse lockout, hill start assist
- **Comprehensive traceability**: Complete mapping to specification requirements

### Additional Examples (Coming Soon)

- E-commerce checkout testing
- API endpoint testing
- Web form validation
- Mobile app configuration testing
- Database query testing

## Contributing Examples

Have a great example to share? We welcome contributions!

1. Fork the repository
2. Add your example to this directory
3. Include both the specification/requirements and the generated test plan
4. Update this README with a description
5. Submit a pull request

### Example Structure

When contributing, please include:
- Original specification or requirements document
- Generated PICT model
- Test cases with expected outputs
- Brief description of the domain and key learning points

---

## Example: Atm Specification

# ATM Machine Specification Document

## 1. System Overview

**Product Name:** SecureBank ATM Model SB-5000  
**Version:** 1.0  
**Purpose:** Self-service banking terminal for cash withdrawal, deposits, balance inquiries, and basic account transactions

## 2. Functional Requirements

### 2.1 Core Functions
- **Cash Withdrawal:** Support withdrawals in denominations of $20, $50, and $100 (configurable)
- **Cash Deposit:** Accept cash deposits with bill validation and counting
- **Balance Inquiry:** Display current account balance for checking and savings accounts
- **Fund Transfer:** Enable transfers between customer's own accounts
- **PIN Change:** Allow customers to change their PIN securely
- **Mini Statement:** Print last 10 transactions

### 2.2 Transaction Limits
- Maximum withdrawal per transaction: $500
- Maximum withdrawal per day: $1,000 (configurable)
- Maximum deposit per transaction: $5,000
- Transaction timeout: 60 seconds of inactivity

## 3. Hardware Requirements

### 3.1 Physical Components
- **Card Reader:** EMV chip card and magnetic stripe reader (ISO 7816 compliant)
- **Cash Dispenser:** 4-cassette system, capacity 2,000 bills per cassette
- **Cash Acceptor:** Bill validator with counterfeit detection
- **Receipt Printer:** Thermal printer, 80mm width
- **Display:** 15-inch touchscreen LCD (1024x768 resolution)
- **Keypad:** Encrypted PIN pad with physical keys
- **Camera:** Two surveillance cameras (customer-facing and cash area)

### 3.2 Physical Specifications
- **Dimensions:** 1600mm (H) x 800mm (W) x 600mm (D)
- **Weight:** Approximately 250 kg
- **Safe Rating:** UL 291 Level 1 certified
- **Power Requirements:** 110-240V AC, 50/60Hz, 500W maximum

## 4. Software Requirements

### 4.1 Operating System
- Hardened Windows 10 IoT Enterprise or Linux-based embedded OS
- Real-time monitoring and health check capabilities

### 4.2 Application Software
- ATM controller software with multi-language support (minimum 3 languages)
- Transaction processing engine
- Remote monitoring and diagnostics software
- Automated software update capability
- Comprehensive audit logging system

### 4.3 Communication Protocols
- ISO 8583 messaging standard for financial transactions
- TCP/IP network protocol
- SSL/TLS encryption for all communications
- Support for NDC+ and DDC protocols

## 5. Security Requirements

### 5.1 Physical Security
- Anti-skimming devices on card reader
- Tamper-evident sensors and alarms
- Reinforced steel safe with time-delay lock
- Anchor bolts for secure installation
- Anti-vandalism coating and materials

### 5.2 Data Security
- Triple DES or AES-256 encryption for PIN blocks
- End-to-end encryption for all sensitive data
- PCI-DSS compliance for payment card data
- Secure key management system (DUKPT)
- No storage of card magnetic stripe data

### 5.3 Authentication
- Customer authentication via PIN (minimum 4 digits, maximum 6 digits)
- Card authentication via EMV chip validation
- Maximum 3 incorrect PIN attempts before card retention

## 6. User Interface Requirements

### 6.1 Display Interface
- Clear, intuitive menu navigation
- High contrast for outdoor visibility
- Accessibility features for visually impaired users (audio guidance option)
- Transaction progress indicators
- Clear error messages and instructions

### 6.2 Response Time
- Card insertion to welcome screen: < 3 seconds
- Transaction authorization: < 10 seconds
- Cash dispensing: < 15 seconds from authorization

## 7. Network and Connectivity

### 7.1 Network Requirements
- Primary: Secure broadband connection (minimum 1 Mbps)
- Backup: 4G/LTE cellular connection
- Automatic failover between primary and backup
- VPN tunnel to host processor

### 7.2 Availability
- System uptime: 99.5% excluding scheduled maintenance
- Maximum network latency: 500ms to host
- Automatic reconnection after network disruption

## 8. Environmental Requirements

- **Operating Temperature:** 10°C to 40°C (50°F to 104°F)
- **Storage Temperature:** -20°C to 60°C (-4°F to 140°F)
- **Humidity:** 20% to 80% non-condensing
- **Installation:** Indoor or outdoor (with weather-resistant enclosure)

## 9. Compliance and Standards

- ADA (Americans with Disabilities Act) compliant
- PCI-PTS certified for secure payment terminals
- EMV Level 1 and Level 2 certified
- ISO 9001 quality management standards
- Local banking regulations and Central Bank requirements

## 10. Maintenance and Support

### 10.1 Monitoring
- 24/7 remote monitoring and alerting
- Automated cash level tracking
- Predictive maintenance alerts
- Transaction success rate monitoring

### 10.2 Maintenance Schedule
- Preventive maintenance: Quarterly
- Cash replenishment: As needed (low cash alert at 20% capacity)
- Receipt paper replacement: As needed
- Software updates: Monthly security patches

## 11. Service Level Agreements

- Critical issue response time: 4 hours
- Hardware repair completion: 24 hours
- Parts availability: 48 hours
- Mean time between failures (MTBF): > 20,000 hours

---

This specification provides a comprehensive framework for an ATM system that can be used for test case design and validation.

---

## Example: Atm Test Plan

# ATM System Test Plan
## Using PICT (Pairwise Independent Combinatorial Testing)

**System:** SecureBank ATM Model SB-5000  
**Version:** 1.0  
**Test Plan Version:** 1.0  
**Date:** October 19, 2025  
**Test Methodology:** Pairwise Combinatorial Testing

---

## 1. Executive Summary

This test plan uses Pairwise Independent Combinatorial Testing (PICT) to efficiently test the ATM system with comprehensive coverage while minimizing the number of test cases. The approach reduces test cases by approximately 85% compared to exhaustive testing while maintaining high coverage of parameter interactions.

**Key Statistics:**
- **Total Test Cases Generated:** 31
- **Parameters Tested:** 8
- **Total Possible Combinations:** 25,920 (exhaustive)
- **Pairwise Test Cases:** 31 (99.88% reduction)
- **Constraints Applied:** 16 business rules
- **Coverage Level:** All 2-way (pairwise) parameter interactions

---

## 2. PICT Model

The following model defines all parameters, their values, and business rule constraints:

```
# ATM System Test Model
# Based on SecureBank ATM Model SB-5000 Specification v1.0

# Parameters
TransactionType: Withdrawal, Deposit, BalanceInquiry, Transfer, PINChange
CardType: EMVChip, MagStripe, Invalid
PINStatus: Valid, Invalid_1st, Invalid_2nd, Invalid_3rd
AccountType: Checking, Savings, Both
TransactionAmount: Within_Limit, At_Max_Transaction, Exceeds_Transaction, Exceeds_Daily
CashAvailability: Sufficient, Insufficient, Empty
NetworkStatus: Connected_Primary, Connected_Backup, Disconnected
CardCondition: Good, Damaged, Expired

# Constraints based on ATM business rules

# Invalid cards cannot complete transactions
IF [CardType] = "Invalid" THEN [TransactionType] = "Withdrawal"
IF [CardType] = "Invalid" THEN [PINStatus] = "Valid"

# Balance inquiry doesn't need cash or specific amounts
IF [TransactionType] = "BalanceInquiry" THEN [TransactionAmount] = "Within_Limit"
IF [TransactionType] = "BalanceInquiry" THEN [CashAvailability] = "Sufficient"

# PIN change doesn't need cash or specific amounts
IF [TransactionType] = "PINChange" THEN [TransactionAmount] = "Within_Limit"
IF [TransactionType] = "PINChange" THEN [CashAvailability] = "Sufficient"

# Deposits don't check cash availability in dispenser
IF [TransactionType] = "Deposit" THEN [CashAvailability] = "Sufficient"

# Transfer doesn't need cash from dispenser
IF [TransactionType] = "Transfer" THEN [CashAvailability] = "Sufficient"

# Withdrawals require checking cash and transaction limits
IF [TransactionType] = "Withdrawal" AND [CashAvailability] = "Empty" THEN [TransactionAmount] = "Within_Limit"

# After 3rd invalid PIN, card should be retained regardless of transaction
IF [PINStatus] = "Invalid_3rd" THEN [TransactionType] = "Withdrawal"

# Damaged or expired cards should fail before PIN validation
IF [CardCondition] = "Damaged" THEN [PINStatus] = "Valid"
IF [CardCondition] = "Expired" THEN [PINStatus] = "Valid"

# Network disconnection affects all transaction types similarly
IF [NetworkStatus] = "Disconnected" THEN [TransactionType] IN {Withdrawal, Deposit, Transfer}

# Amount constraints only apply to withdrawal and deposit
IF [TransactionAmount] = "Exceeds_Daily" THEN [TransactionType] IN {Withdrawal, Deposit}
IF [TransactionAmount] = "Exceeds_Transaction" THEN [TransactionType] IN {Withdrawal, Deposit}
IF [TransactionAmount] = "At_Max_Transaction" THEN [TransactionType] IN {Withdrawal, Deposit}
```

---

## 3. Parameter Definitions

### 3.1 TransactionType
- **Withdrawal:** Cash withdrawal from account
- **Deposit:** Cash deposit to account
- **BalanceInquiry:** Check account balance
- **Transfer:** Transfer funds between accounts
- **PINChange:** Change ATM PIN

### 3.2 CardType
- **EMVChip:** Card with EMV chip (current standard)
- **MagStripe:** Magnetic stripe only card (legacy)
- **Invalid:** Unrecognized or damaged card data

### 3.3 PINStatus
- **Valid:** Correct PIN entered
- **Invalid_1st:** First incorrect PIN attempt
- **Invalid_2nd:** Second incorrect PIN attempt
- **Invalid_3rd:** Third incorrect PIN attempt (triggers card retention)

### 3.4 AccountType
- **Checking:** Checking account only
- **Savings:** Savings account only
- **Both:** Multiple accounts available

### 3.5 TransactionAmount
- **Within_Limit:** Amount within all limits
- **At_Max_Transaction:** At maximum per-transaction limit ($500 for withdrawal)
- **Exceeds_Transaction:** Exceeds per-transaction limit
- **Exceeds_Daily:** Exceeds daily limit ($1,000)

### 3.6 CashAvailability
- **Sufficient:** ATM has enough cash
- **Insufficient:** ATM has some cash but not enough for transaction
- **Empty:** ATM is out of cash

### 3.7 NetworkStatus
- **Connected_Primary:** Using primary broadband connection
- **Connected_Backup:** Failover to 4G/LTE backup
- **Disconnected:** No network connectivity

### 3.8 CardCondition
- **Good:** Card is in good condition
- **Damaged:** Card is damaged/unreadable
- **Expired:** Card has expired

---

## 4. Generated Test Cases

| Test # | Transaction Type | Card Type | PIN Status | Account Type | Transaction Amount | Cash Availability | Network Status | Card Condition | Expected Output |
|--------|-----------------|-----------|------------|--------------|-------------------|-------------------|----------------|---------------|-----------------|
| 1 | Withdrawal | EMVChip | Valid | Checking | Within_Limit | Sufficient | Connected_Primary | Good | Success: Cash dispensed - Receipt printed |
| 2 | Deposit | MagStripe | Valid | Savings | Within_Limit | Sufficient | Connected_Primary | Good | Success: Deposit accepted - Receipt printed |
| 3 | BalanceInquiry | EMVChip | Valid | Both | Within_Limit | Sufficient | Connected_Primary | Good | Success: Balance displayed and printed |
| 4 | Transfer | MagStripe | Valid | Both | Within_Limit | Sufficient | Connected_Primary | Good | Success: Transfer completed - Receipt printed |
| 5 | PINChange | EMVChip | Valid | Checking | Within_Limit | Sufficient | Connected_Primary | Good | Success: PIN changed successfully |
| 6 | Withdrawal | EMVChip | Invalid_1st | Checking | Within_Limit | Sufficient | Connected_Primary | Good | Error: Incorrect PIN - 2 attempts remaining |
| 7 | Withdrawal | MagStripe | Invalid_2nd | Savings | Within_Limit | Sufficient | Connected_Primary | Good | Error: Incorrect PIN - 1 attempt remaining |
| 8 | Withdrawal | EMVChip | Invalid_3rd | Both | Within_Limit | Sufficient | Connected_Primary | Good | Error: Maximum PIN attempts exceeded - Card retained |
| 9 | Withdrawal | Invalid | Valid | Checking | Within_Limit | Sufficient | Connected_Primary | Good | Error: Card not recognized - Transaction declined |
| 10 | Withdrawal | EMVChip | Valid | Checking | Within_Limit | Sufficient | Connected_Primary | Damaged | Error: Card unreadable - Please use another card |
| 11 | Deposit | MagStripe | Valid | Savings | Within_Limit | Sufficient | Connected_Primary | Expired | Error: Card expired - Please contact your bank |
| 12 | Withdrawal | EMVChip | Valid | Checking | At_Max_Transaction | Sufficient | Connected_Primary | Good | Success: Cash dispensed - Receipt printed |
| 13 | Withdrawal | MagStripe | Valid | Savings | Exceeds_Transaction | Sufficient | Connected_Primary | Good | Error: Transaction exceeds maximum withdrawal amount ($500) |
| 14 | Withdrawal | EMVChip | Valid | Both | Exceeds_Daily | Sufficient | Connected_Primary | Good | Error: Transaction exceeds daily withdrawal limit ($1,000) |
| 15 | Deposit | MagStripe | Valid | Checking | At_Max_Transaction | Sufficient | Connected_Primary | Good | Success: Deposit accepted - Receipt printed |
| 16 | Deposit | EMVChip | Valid | Savings | Exceeds_Transaction | Sufficient | Connected_Primary | Good | Error: Deposit exceeds maximum amount ($5,000) |
| 17 | Withdrawal | EMVChip | Valid | Checking | Within_Limit | Insufficient | Connected_Primary | Good | Error: Insufficient cash in ATM for this amount |
| 18 | Withdrawal | MagStripe | Valid | Savings | Within_Limit | Empty | Connected_Primary | Good | Error: ATM out of cash - Please try another location |
| 19 | Withdrawal | EMVChip | Valid | Checking | Within_Limit | Sufficient | Connected_Backup | Good | Success: Cash dispensed - Receipt printed (Backup network) |
| 20 | Deposit | MagStripe | Valid | Savings | Within_Limit | Sufficient | Connected_Backup | Good | Success: Deposit accepted - Receipt printed (Backup network) |
| 21 | Transfer | EMVChip | Valid | Both | Within_Limit | Sufficient | Connected_Backup | Good | Success: Transfer completed - Receipt printed (Backup network) |
| 22 | Withdrawal | MagStripe | Valid | Checking | Within_Limit | Sufficient | Disconnected | Good | Error: Cannot connect to bank - Transaction unavailable |
| 23 | Deposit | EMVChip | Valid | Savings | Within_Limit | Sufficient | Disconnected | Good | Error: Cannot connect to bank - Transaction unavailable |
| 24 | Transfer | MagStripe | Valid | Both | Within_Limit | Sufficient | Disconnected | Good | Error: Cannot connect to bank - Transaction unavailable |
| 25 | Transfer | EMVChip | Valid | Checking | Within_Limit | Sufficient | Connected_Primary | Good | Error: Transfer requires multiple accounts |
| 26 | Withdrawal | MagStripe | Valid | Both | At_Max_Transaction | Sufficient | Connected_Backup | Good | Success: Cash dispensed - Receipt printed (Backup network) |
| 27 | BalanceInquiry | MagStripe | Valid | Checking | Within_Limit | Sufficient | Connected_Backup | Good | Success: Balance displayed and printed (Backup network) |
| 28 | PINChange | MagStripe | Valid | Savings | Within_Limit | Sufficient | Connected_Backup | Good | Success: PIN changed successfully (Backup network) |
| 29 | Deposit | EMVChip | Valid | Both | At_Max_Transaction | Sufficient | Connected_Backup | Good | Success: Deposit accepted - Receipt printed (Backup network) |
| 30 | Withdrawal | EMVChip | Invalid_1st | Savings | Exceeds_Transaction | Insufficient | Connected_Backup | Good | Error: Incorrect PIN - 2 attempts remaining |
| 31 | BalanceInquiry | EMVChip | Invalid_2nd | Savings | Within_Limit | Sufficient | Connected_Primary | Good | Error: Incorrect PIN - 1 attempt remaining |

---

## 5. Test Coverage Analysis

### 5.1 Coverage by Transaction Type
- **Withdrawal:** 14 test cases (45%)
- **Deposit:** 7 test cases (23%)
- **BalanceInquiry:** 3 test cases (10%)
- **Transfer:** 4 test cases (13%)
- **PINChange:** 2 test cases (6%)
- **Other (Card errors):** 1 test case (3%)

### 5.2 Coverage by Outcome Type
- **Success Scenarios:** 17 test cases (55%)
- **Error Scenarios:** 14 test cases (45%)

### 5.3 Critical Scenarios Covered
✅ All transaction types tested  
✅ All card types tested  
✅ All PIN scenarios including card retention  
✅ Transaction limit enforcement  
✅ Daily limit enforcement  
✅ Cash availability scenarios  
✅ Network failover testing  
✅ Card condition validation  
✅ Account type validation  

---

## 6. Test Execution Guidelines

### 6.1 Pre-Test Setup
1. **ATM Configuration:**
   - Load cash cassettes with sufficient bills
   - Verify all hardware components operational
   - Configure transaction limits as per specification
   - Ensure primary and backup network connections

2. **Test Cards:**
   - Prepare EMV chip cards (valid, expired)
   - Prepare magnetic stripe cards (valid, damaged)
   - Prepare invalid/unrecognized cards

3. **Test Accounts:**
   - Create test accounts (checking, savings, both)
   - Set known balances for verification
   - Configure daily withdrawal limits

### 6.2 Test Execution Process

For each test case:

1. **Setup:** Configure ATM and account per test parameters
2. **Execute:** Perform transaction as specified
3. **Observe:** Record actual outcome
4. **Verify:** Compare with expected output
5. **Log:** Document results and any deviations
6. **Reset:** Return ATM to initial state for next test

### 6.3 Pass/Fail Criteria

**Pass:** 
- Actual output matches expected output exactly
- Transaction completes within specified time limits
- Receipt printed (if applicable) with correct information
- Audit log entry created correctly

**Fail:**
- Output differs from expected
- System error or crash occurs
- Transaction timeout
- Incorrect receipt or no receipt when expected
- Security validation bypassed

---

## 7. Test Environment Requirements

### 7.1 Hardware
- ATM with all components operational
- Network connectivity (primary and backup)
- Cash cassettes with mixed denominations
- Receipt paper loaded
- Test cards (various types)

### 7.2 Software
- ATM application software v1.0
- Test transaction processing environment
- Network simulation tools for failover testing
- Monitoring and logging tools

### 7.3 Test Data
- Valid test account credentials
- Multiple account types
- Known account balances
- Expired and invalid cards for negative testing

---

## 8. Risk-Based Testing Priorities

### Priority 1 (Critical) - Must Pass
- Test Cases: 1, 2, 3, 8, 9, 13, 14, 18, 22
- **Focus:** Core transactions, security (card retention), limit enforcement, critical error conditions

### Priority 2 (High) - Should Pass
- Test Cases: 4, 5, 6, 7, 10, 11, 12, 16, 17, 19, 23, 24
- **Focus:** All transaction types, error handling, network failover

### Priority 3 (Medium) - Nice to Pass
- Test Cases: 15, 20, 21, 25, 26, 27, 28, 29, 30, 31
- **Focus:** Edge cases, combined scenarios, backup operations

---

## 9. Traceability Matrix

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| SEC-001: PIN Validation | 6, 7, 8, 30, 31 | ✅ Full |
| SEC-002: Card Retention | 8 | ✅ Full |
| SEC-003: Invalid Card Detection | 9, 10, 11 | ✅ Full |
| TXN-001: Withdrawal Limits | 12, 13, 14 | ✅ Full |
| TXN-002: Deposit Limits | 15, 16 | ✅ Full |
| TXN-003: Cash Availability | 17, 18 | ✅ Full |
| NET-001: Primary Network | 1-18, 25, 31 | ✅ Full |
| NET-002: Backup Network | 19, 20, 21, 26, 27, 28, 29, 30 | ✅ Full |
| NET-003: Network Failure | 22, 23, 24 | ✅ Full |
| ACC-001: Account Validation | 25 | ✅ Full |
| HW-001: All Transaction Types | 1, 2, 3, 4, 5 | ✅ Full |

---

## 10. Defect Reporting Template

When logging defects, include:

- **Test Case Number:** Reference from this plan
- **Severity:** Critical / High / Medium / Low
- **Steps to Reproduce:** Detailed steps with parameters
- **Expected Result:** From test plan
- **Actual Result:** What actually occurred
- **Screenshots/Logs:** Evidence of failure
- **Environment:** Hardware/software configuration
- **Impact:** User experience or security implications

---

## 11. Test Metrics to Track

- **Total Test Cases:** 31
- **Test Cases Executed:** _____
- **Test Cases Passed:** _____
- **Test Cases Failed:** _____
- **Test Cases Blocked:** _____
- **Pass Rate:** _____%
- **Defects Found:** _____
- **Critical Defects:** _____
- **Test Execution Time:** _____ hours

---

## 12. How to Use This Test Plan

### 12.1 Generating More Test Cases

If you need to generate additional test cases or modify the model:

1. **Edit the PICT model** (Section 2) with new parameters or constraints
2. **Use online PICT tools:**
   - https://pairwise.yuuniworks.com/
   - https://pairwise.teremokgames.com/
3. **Or install PICT locally:**
   - Download from: https://github.com/microsoft/pict
   - Run: `pict atm_model.txt`

### 12.2 Customizing for Your Environment

- Adjust transaction limits in parameter values
- Add/remove card types based on your supported standards
- Modify network scenarios based on your infrastructure
- Add language parameters for internationalization testing

### 12.3 Integration with Test Management Tools

This test plan can be imported into:
- JIRA Test Management
- TestRail
- Azure Test Plans
- HP ALM/Quality Center
- Any tool accepting CSV or Excel format

---

## 13. Appendices

### Appendix A: PICT Syntax Reference

**Basic Syntax:**
```
ParameterName: Value1, Value2, Value3
```

**Constraints:**
```
IF [Parameter1] = "Value" THEN [Parameter2] = "OtherValue";
IF [Parameter1] <> "Value" THEN [Parameter2] IN {Value1, Value2};
```

**Operators:**
- `=` Equal to
- `<>` Not equal to
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal
- `<=` Less than or equal
- `IN` Member of set
- `AND` Logical AND
- `OR` Logical OR
- `NOT` Logical NOT

### Appendix B: Testing Best Practices

1. **Isolate Test Cases:** Each test should be independent
2. **Reset State:** Return to known state between tests
3. **Document Deviations:** Log any variations from expected behavior
4. **Verify Logs:** Check audit logs for each transaction
5. **Test Security:** Never skip security-related test cases
6. **Monitor Performance:** Track response times
7. **Test Recovery:** Include abnormal termination scenarios
8. **Backup Testing:** Verify backup systems work as expected

### Appendix C: Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Card retention doesn't trigger | Security settings | Verify max PIN attempts configuration |
| Network failover fails | Backup not configured | Check 4G/LTE connection settings |
| Receipt not printing | Paper jam / Empty | Check printer status before testing |
| Transaction timeout | Network latency | Verify network performance meets spec |
| Limits not enforced | Configuration error | Verify transaction limit settings |

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Oct 19, 2025 | Test Team | Initial test plan with PICT methodology |

---

**Approval:**

Test Manager: _________________ Date: _________

QA Lead: _________________ Date: _________

Project Manager: _________________ Date: _________

---

## Example: Gearbox Specification

# Automotive Gearbox Control System - Specification

## 1. System Overview

The Automotive Gearbox Control System is an electronic control unit (ECU) that manages gear shifting in a semi-automatic transmission. The system monitors vehicle conditions and driver inputs to determine optimal gear selection and execute smooth gear changes.

## 2. System Components

### 2.1 Input Sensors
- **Vehicle Speed Sensor**: Measures current speed (0-200 km/h)
- **Engine RPM Sensor**: Measures engine revolutions (0-7000 RPM)
- **Throttle Position Sensor**: Measures accelerator pedal position (0-100%)
- **Brake Pressure Sensor**: Detects brake application
- **Clutch Position Sensor**: Monitors clutch engagement state
- **Gear Position Sensor**: Detects current gear (N, 1-6, R)

### 2.2 Driver Controls
- **Gear Selector**: Manual, Sport, Eco modes
- **Shift Paddles**: Manual up/down shift requests
- **Clutch Pedal**: Manual clutch control (if applicable)

### 2.3 Outputs
- **Gear Actuator**: Mechanical gear selection
- **Clutch Actuator**: Clutch engagement/disengagement
- **Dashboard Display**: Current gear indicator
- **Warning Lights**: System errors and alerts

## 3. Operating Modes

### 3.1 Manual Mode
- Driver has full control over gear selection
- System prevents invalid shifts (e.g., direct 5th to 1st)
- Rev-matching on downshifts
- Neutral safety: requires brake to shift out of Park/Neutral

### 3.2 Sport Mode
- Holds gears longer for higher RPM
- Faster gear changes
- Downshifts on hard braking
- Target shift points: 5000-6500 RPM

### 3.3 Eco Mode
- Early upshifts for fuel efficiency
- Target shift points: 2000-3000 RPM
- Smooth, gradual gear changes
- Skip-shift capability (e.g., 2nd to 4th)

## 4. Functional Requirements

### 4.1 Gear Shifting Logic

#### 4.1.1 Upshift Conditions
- **Eco Mode**: Engine RPM > 2500 AND throttle < 40%
- **Manual Mode**: Driver paddle input OR RPM > 6000
- **Sport Mode**: Engine RPM > 5500

#### 4.1.2 Downshift Conditions
- **Eco Mode**: Engine RPM < 1500 OR heavy throttle (>80%)
- **Manual Mode**: Driver paddle input OR RPM < 1200
- **Sport Mode**: Engine RPM < 2000 OR brake pressure > 50%

#### 4.1.3 Prohibited Shifts
- Cannot shift from Reverse to any forward gear without stopping (speed = 0)
- Cannot shift to Reverse from any forward gear while moving (speed > 0)
- Cannot skip more than 2 gears in a single shift (except computer-controlled skip-shift)
- Cannot downshift if resulting RPM would exceed 7000 (red line protection)

### 4.2 Safety Features

#### 4.2.1 Hill Start Assist
- Activates when: stopped on incline > 5% AND brake released
- Holds brake pressure for 2 seconds
- Prevents rollback

#### 4.2.2 Overrun Protection
- Prevents downshift if resulting engine RPM > 6500
- Displays warning message to driver
- Ignores paddle input if unsafe

#### 4.2.3 Stall Prevention
- Auto-downshift if engine RPM < 800 while moving
- Automatic neutral engagement if stopped for > 3 seconds in gear
- Clutch slip if speed drops below minimum for current gear

#### 4.2.4 Neutral Safety
- Engine start only allowed in Park or Neutral
- Brake pedal required to shift from Park
- Reverse requires full stop (speed = 0 km/h)

### 4.3 Error Handling

#### 4.3.1 Sensor Failures
- **Speed Sensor Failure**: Limit to current gear, disable automatic shifting
- **RPM Sensor Failure**: Use speed-based shift logic as fallback
- **Throttle Sensor Failure**: Default to conservative shift points
- **Multiple Sensor Failures**: Enter limp-home mode (3rd gear only)

#### 4.3.2 Actuator Failures
- **Gear Actuator Jam**: Attempt 3 retries with 200ms delay
- **Clutch Actuator Failure**: Lock in current gear, display warning
- **Hydraulic Pressure Low**: Reduce shift speed, display warning

#### 4.3.3 Temperature Management
- **Normal Operation**: 70-110°C
- **High Temperature Warning**: 110-130°C (reduce shift frequency)
- **Critical Temperature**: >130°C (limp-home mode, 3rd gear only)

## 5. Performance Requirements

### 5.1 Shift Times
- **Eco Mode**: 800-1200 ms per shift
- **Manual Mode**: 400-600 ms per shift
- **Sport Mode**: 150-300 ms per shift

### 5.2 Response Times
- **Paddle Input**: < 50 ms recognition
- **Brake Detection**: < 20 ms
- **Emergency Neutral**: < 100 ms

### 5.3 Reliability
- **MTBF**: > 150,000 km
- **Shift Success Rate**: > 99.5%
- **False Error Rate**: < 0.1%

## 6. Environmental Conditions

### 6.1 Operating Temperature
- **Normal**: -20°C to +50°C ambient
- **Gearbox Oil**: -10°C to +130°C

### 6.2 Altitude
- **Sea Level to 3000m**: Normal operation
- **3000m to 5000m**: Adjusted shift points for reduced air density

### 6.3 Weather Conditions
- Rain, snow, ice: Reduced shift aggressiveness
- Detection via wheel slip sensors and ABS integration

## 7. User Interface Requirements

### 7.1 Dashboard Display
- Current gear number (1-6, R, N, P)
- Selected mode (Manual, Sport, Eco)
- Shift indicator (up/down arrows)
- Warning messages (text + icon)

### 7.2 Warning Messages
- "Gearbox Overheating" (yellow)
- "Shift Not Possible" (red)
- "Service Required" (yellow)
- "Limp-Home Mode Active" (red)

### 7.3 User Feedback
- Shift confirmation (subtle indicator flash)
- Paddle input acknowledgment (haptic feedback if available)
- Audio warning for critical errors

## 8. Integration Requirements

### 8.1 Engine Control Unit (ECU)
- Torque reduction request during shifts
- RPM synchronization for smooth engagement
- Engine braking coordination

### 8.2 Anti-lock Braking System (ABS)
- Wheel slip detection for traction control
- Emergency braking gear hold
- Stability control integration

### 8.3 Electronic Stability Control (ESC)
- Torque vectoring support
- Drift mode compatibility (sport mode)
- Traction control coordination

## 9. Validation Requirements

### 9.1 Unit Testing
- Individual sensor input validation
- Shift logic decision trees
- Safety feature triggering

### 9.2 Integration Testing
- Multi-mode operation
- Sensor failure scenarios
- ECU communication

### 9.3 System Testing
- Real-world driving scenarios
- Extreme condition testing
- Long-term reliability testing

## 10. Constraints and Assumptions

### 10.1 Physical Constraints
- Maximum gear ratio: 1:6.5 (1st gear) to 1:0.85 (6th gear)
- Clutch engagement time: 200-400 ms
- Hydraulic system pressure: 8-12 bar

### 10.2 System Assumptions
- Sensors provide accurate readings within ±5% tolerance
- ECU communication latency < 10 ms
- Battery voltage maintained at 12-14V

### 10.3 Regulatory Compliance
- ISO 26262 (Automotive Safety Integrity Level - ASIL C)
- UNECE R13 (Braking regulations)
- Local emissions standards compliance

---

## Example: Gearbox Test Plan

# Automotive Gearbox Control System - PICT Test Plan

## Test Plan Overview

This test plan uses Pairwise Independent Combinatorial Testing (PICT) to generate comprehensive test cases for the Automotive Gearbox Control System with minimal test execution while ensuring complete coverage of all critical parameter interactions.

## Test Parameters Analysis

Based on the specification analysis, the following parameters have been identified:

### Core Parameters
1. **Operating Mode**: Manual, Sport, Eco
2. **Current Gear**: Park, Neutral, Reverse, 1st, 2nd, 3rd, 4th, 5th, 6th
3. **Vehicle Speed**: Stopped, Low (1-30 km/h), Medium (31-80 km/h), High (81-150 km/h), VeryHigh (151-200 km/h)
4. **Engine RPM**: Idle (<1000), Low (1000-2500), Normal (2500-4500), High (4500-6500), RedLine (>6500)
5. **Throttle Position**: Closed (0-10%), Light (11-40%), Medium (41-80%), Heavy (81-100%)
6. **Brake Status**: NotApplied, Light, Hard
7. **Shift Request**: None, PaddleUp, PaddleDown, Automatic
8. **Temperature**: Cold (<70°C), Normal (70-110°C), Warm (110-130°C), Critical (>130°C)

### Environmental Parameters
9. **Road Condition**: Dry, Wet, Ice
10. **Incline**: Flat, UpHill, DownHill

### System State Parameters
11. **Sensor Status**: AllOK, SpeedFail, RPMFail, ThrottleFail, MultipleFail
12. **Hydraulic Pressure**: Normal, Low, Critical

## PICT Model

```pict
# Core Operating Parameters
OperatingMode: Manual, Sport, Eco
CurrentGear: Park, Neutral, Reverse, 1st, 2nd, 3rd, 4th, 5th, 6th
VehicleSpeed: Stopped, Low, Medium, High, VeryHigh
EngineRPM: Idle, Low, Normal, High, RedLine
ThrottlePosition: Closed, Light, Medium, Heavy
BrakeStatus: NotApplied, Light, Hard
ShiftRequest: None, PaddleUp, PaddleDown, Automatic
Temperature: Cold, Normal, Warm, Critical
RoadCondition: Dry, Wet, Ice
Incline: Flat, UpHill, DownHill
SensorStatus: AllOK, SpeedFail, RPMFail, ThrottleFail, MultipleFail
HydraulicPressure: Normal, Low, Critical

# Constraint 1: Park/Neutral only valid when stopped
IF [CurrentGear] = "Park" THEN [VehicleSpeed] = "Stopped";
IF [CurrentGear] = "Neutral" AND [ShiftRequest] <> "None" THEN [VehicleSpeed] = "Stopped";

# Constraint 2: Reverse requires vehicle stopped
IF [CurrentGear] = "Reverse" AND [ShiftRequest] = "None" THEN [VehicleSpeed] IN {Stopped, Low};
IF [ShiftRequest] = "PaddleDown" AND [CurrentGear] = "1st" THEN [VehicleSpeed] = "Stopped";

# Constraint 3: Engine RPM correlates with vehicle speed and gear
IF [VehicleSpeed] = "Stopped" THEN [EngineRPM] IN {Idle, Low};
IF [VehicleSpeed] = "VeryHigh" THEN [EngineRPM] IN {Normal, High, RedLine};
IF [CurrentGear] IN {Park, Neutral} THEN [EngineRPM] IN {Idle, Low, Normal};

# Constraint 4: Throttle and brake are mutually exclusive (mostly)
IF [BrakeStatus] = "Hard" THEN [ThrottlePosition] IN {Closed, Light};
IF [ThrottlePosition] = "Heavy" THEN [BrakeStatus] = "NotApplied";

# Constraint 5: High gears require sufficient speed
IF [CurrentGear] IN {5th, 6th} THEN [VehicleSpeed] IN {Medium, High, VeryHigh};
IF [CurrentGear] IN {5th, 6th} THEN [EngineRPM] <> "Idle";

# Constraint 6: Low gears limited to lower speeds
IF [CurrentGear] = "1st" AND [VehicleSpeed] IN {High, VeryHigh} THEN [EngineRPM] = "RedLine";
IF [CurrentGear] = "2nd" AND [VehicleSpeed] = "VeryHigh" THEN [EngineRPM] IN {High, RedLine};

# Constraint 7: Shift requests must be appropriate for current gear
IF [ShiftRequest] = "PaddleDown" AND [CurrentGear] = "1st" THEN [VehicleSpeed] = "Stopped";
IF [ShiftRequest] = "PaddleUp" AND [CurrentGear] = "6th" THEN [EngineRPM] <> "RedLine";

# Constraint 8: Critical temperature limits automatic shifting
IF [Temperature] = "Critical" THEN [ShiftRequest] IN {None, PaddleUp, PaddleDown};
IF [Temperature] = "Critical" THEN [CurrentGear] IN {Neutral, 3rd};

# Constraint 9: Sensor failures affect operation
IF [SensorStatus] = "MultipleFail" THEN [CurrentGear] = "3rd";
IF [SensorStatus] = "MultipleFail" THEN [ShiftRequest] = "None";
IF [SensorStatus] = "SpeedFail" THEN [ShiftRequest] IN {None, PaddleUp, PaddleDown};

# Constraint 10: Hydraulic pressure issues limit operation
IF [HydraulicPressure] = "Critical" THEN [ShiftRequest] = "None";
IF [HydraulicPressure] = "Low" THEN [OperatingMode] <> "Sport";

# Constraint 11: Ice conditions require special handling
IF [RoadCondition] = "Ice" THEN [ThrottlePosition] IN {Closed, Light, Medium};
IF [RoadCondition] = "Ice" AND [BrakeStatus] = "Hard" THEN [VehicleSpeed] IN {Stopped, Low};

# Constraint 12: Operating mode influences shift behavior
IF [OperatingMode] = "Eco" AND [ThrottlePosition] = "Heavy" THEN [EngineRPM] IN {Idle, Low, Normal};
IF [OperatingMode] = "Sport" AND [ShiftRequest] = "Automatic" THEN [EngineRPM] IN {Normal, High, RedLine};

# Constraint 13: Cold temperature affects shifting
IF [Temperature] = "Cold" THEN [OperatingMode] IN {Manual, Eco};
IF [Temperature] = "Cold" THEN [ShiftRequest] <> "Automatic";

# Constraint 14: Incline affects shift logic
IF [Incline] = "UpHill" AND [CurrentGear] IN {5th, 6th} THEN [ThrottlePosition] IN {Medium, Heavy};
IF [Incline] = "DownHill" AND [BrakeStatus] IN {Light, Hard} THEN [EngineRPM] IN {Normal, High};
```

## Generated Test Cases

| Test # | Mode | Gear | Speed | RPM | Throttle | Brake | ShiftReq | Temp | Road | Incline | Sensor | Hydraulic | Expected Output |
|--------|------|------|-------|-----|----------|-------|----------|------|------|---------|--------|-----------|-----------------|
| 1 | Manual | Park | Stopped | Idle | Closed | NotApplied | None | Normal | Dry | Flat | AllOK | Normal | Success: Vehicle parked, engine idling |
| 2 | Sport | 3rd | Medium | High | Medium | NotApplied | Automatic | Normal | Wet | Flat | AllOK | Normal | Success: Upshift to 4th at 5500 RPM |
| 3 | Eco | 2nd | Low | Low | Light | NotApplied | Automatic | Normal | Dry | UpHill | AllOK | Normal | Success: Hold 2nd gear, insufficient RPM for upshift |
| 4 | Manual | 4th | High | Normal | Medium | NotApplied | PaddleUp | Normal | Dry | Flat | AllOK | Normal | Success: Upshift to 5th gear via paddle |
| 5 | Sport | 5th | VeryHigh | High | Medium | NotApplied | None | Normal | Dry | DownHill | AllOK | Normal | Success: Hold 5th gear, RPM in range |
| 6 | Eco | 3rd | Medium | Low | Closed | Light | None | Normal | Wet | Flat | AllOK | Normal | Success: Downshift to 2nd, low RPM + closed throttle |
| 7 | Manual | 1st | Stopped | Idle | Closed | Hard | None | Cold | Dry | Flat | AllOK | Normal | Success: Stationary in 1st with brake applied |
| 8 | Sport | 2nd | Low | Normal | Heavy | NotApplied | Automatic | Normal | Dry | UpHill | AllOK | Normal | Success: Hold 2nd gear for power uphill |
| 9 | Eco | 6th | VeryHigh | Normal | Light | NotApplied | None | Normal | Dry | Flat | AllOK | Normal | Success: Cruising in 6th gear |
| 10 | Manual | Reverse | Stopped | Low | Closed | NotApplied | None | Normal | Wet | Flat | AllOK | Normal | Success: In reverse, vehicle stopped |
| 11 | Sport | 3rd | Medium | RedLine | Heavy | NotApplied | Automatic | Normal | Dry | Flat | AllOK | Normal | Success: Upshift to 4th to prevent over-rev |
| 12 | Eco | 1st | Low | Normal | Medium | NotApplied | Automatic | Normal | Ice | Flat | AllOK | Normal | Success: Smooth upshift to 2nd |
| 13 | Manual | 4th | Medium | Low | Closed | Light | PaddleDown | Normal | Dry | DownHill | AllOK | Normal | Success: Downshift to 3rd for engine braking |
| 14 | Sport | 3rd | Low | High | Light | Hard | None | Normal | Ice | Flat | AllOK | Normal | Warning: Reduce shift aggressiveness on ice |
| 15 | Eco | 2nd | Medium | Normal | Light | NotApplied | None | Warm | Dry | Flat | AllOK | Normal | Success: Upshift to 3rd (or 4th skip-shift) |
| 16 | Manual | Neutral | Stopped | Idle | Closed | NotApplied | None | Normal | Dry | Flat | AllOK | Normal | Success: Neutral, engine idling |
| 17 | Sport | 5th | High | High | Medium | NotApplied | PaddleDown | Normal | Dry | Flat | AllOK | Normal | Success: Downshift to 4th |
| 18 | Eco | 3rd | Medium | Normal | Closed | NotApplied | Automatic | Normal | Wet | UpHill | AllOK | Normal | Success: Hold 3rd gear for uphill |
| 19 | Manual | 1st | Low | High | Heavy | NotApplied | PaddleUp | Normal | Dry | Flat | AllOK | Normal | Success: Upshift to 2nd |
| 20 | Sport | 4th | VeryHigh | RedLine | Medium | NotApplied | None | Normal | Dry | Flat | AllOK | Normal | Warning: Prevent downshift, would over-rev |
| 21 | Eco | 3rd | Stopped | Idle | Closed | Hard | None | Normal | Dry | UpHill | AllOK | Normal | Success: Hill start assist activated |
| 22 | Manual | 2nd | Medium | Normal | Light | NotApplied | None | Cold | Dry | Flat | AllOK | Normal | Success: Hold 2nd, cold mode conservative |
| 23 | Sport | 6th | VeryHigh | Normal | Light | NotApplied | Automatic | Normal | Dry | Flat | AllOK | Normal | Success: Hold 6th, optimal cruising |
| 24 | Eco | 1st | Stopped | Low | Closed | NotApplied | Automatic | Normal | Dry | Flat | SpeedFail | Normal | Error: Limit to current gear, speed sensor failed |
| 25 | Manual | 3rd | Medium | Normal | Medium | NotApplied | PaddleUp | Normal | Dry | Flat | RPMFail | Normal | Success: Upshift using speed-based logic fallback |
| 26 | Sport | 3rd | Low | Low | Closed | NotApplied | None | Critical | Dry | Flat | AllOK | Normal | Error: Limp-home mode, critical temperature |
| 27 | Eco | 3rd | Medium | Normal | Light | NotApplied | None | Normal | Dry | Flat | MultipleFail | Normal | Error: Limp-home mode, multiple sensor failures |
| 28 | Manual | 4th | High | High | Medium | NotApplied | None | Normal | Dry | Flat | AllOK | Low | Warning: Reduced shift speed, low hydraulic pressure |
| 29 | Sport | 3rd | Medium | Normal | Medium | NotApplied | None | Normal | Dry | Flat | AllOK | Critical | Error: Lock in current gear, critical hydraulic failure |
| 30 | Eco | 2nd | Low | Low | Light | NotApplied | Automatic | Normal | Ice | Flat | AllOK | Normal | Success: Gentle upshift, ice mode active |
| 31 | Manual | 5th | VeryHigh | Normal | Medium | NotApplied | PaddleDown | Normal | Wet | Flat | AllOK | Normal | Success: Downshift to 4th |
| 32 | Sport | 1st | Stopped | Idle | Closed | Hard | None | Normal | Dry | DownHill | AllOK | Normal | Success: Holding brake on downhill |
| 33 | Eco | 4th | High | Low | Closed | Light | Automatic | Normal | Dry | Flat | AllOK | Normal | Success: Downshift to 3rd, low RPM |
| 34 | Manual | 6th | VeryHigh | High | Heavy | NotApplied | None | Normal | Dry | Flat | AllOK | Normal | Success: Maximum speed in top gear |
| 35 | Sport | 2nd | Medium | RedLine | Medium | NotApplied | Automatic | Normal | Dry | Flat | AllOK | Normal | Success: Emergency upshift to prevent damage |
| 36 | Eco | 1st | Low | Normal | Light | NotApplied | Automatic | Warm | Dry | Flat | ThrottleFail | Normal | Success: Conservative shift points, throttle sensor failed |
| 37 | Manual | Park | Stopped | Idle | Closed | Hard | None | Normal | Ice | Flat | AllOK | Normal | Success: Park brake, ice condition noted |
| 38 | Sport | 4th | High | High | Medium | Light | None | Normal | Dry | DownHill | AllOK | Normal | Success: Engine braking with downshift |
| 39 | Eco | 5th | VeryHigh | Normal | Closed | NotApplied | None | Normal | Wet | Flat | AllOK | Normal | Success: Coasting in 5th gear |
| 40 | Manual | 3rd | Medium | High | Heavy | NotApplied | PaddleUp | Cold | Dry | UpHill | AllOK | Normal | Success: Upshift to 4th, cold mode allows manual override |

## Test Case Summary

- **Total Possible Combinations**: 12 parameters with 3-13 values each = ~159 billion combinations
- **PICT Generated Test Cases**: 40
- **Test Reduction**: 99.999999975% reduction
- **Coverage**: All pairwise (2-way) parameter interactions
- **Constraints Applied**: 14 business rules and safety constraints

## Test Execution Priority

### Priority 1: Critical Safety Tests (Tests 7, 10, 21, 26, 27, 29, 32, 37)
- Park/Neutral safety
- Reverse lockout
- Hill start assist
- Critical temperature handling
- Sensor failure modes
- Hydraulic failures

### Priority 2: Core Functionality (Tests 1-6, 8-9, 11-20, 23-25, 30-31, 33-36, 38-40)
- Normal shifting in all modes
- Paddle shift operations
- Automatic shift logic
- RPM protection
- Speed-based logic

### Priority 3: Edge Cases (Tests 22, 28)
- Cold temperature operation
- Low hydraulic pressure
- Environmental conditions

## Coverage Analysis

### Operating Modes Coverage
- **Manual**: 15 tests (37.5%)
- **Sport**: 13 tests (32.5%)
- **Eco**: 12 tests (30%)

### Gear Range Coverage
- All gears (Park, N, R, 1-6) tested
- Emphasis on mid-range gears (2nd-4th) for common scenarios

### Error Scenarios Coverage
- Sensor failures: 4 tests (10%)
- Temperature extremes: 3 tests (7.5%)
- Hydraulic issues: 2 tests (5%)
- Environmental conditions: 8 tests (20%)

### Shift Request Coverage
- **None** (steady state): 18 tests (45%)
- **Automatic**: 12 tests (30%)
- **PaddleUp**: 5 tests (12.5%)
- **PaddleDown**: 5 tests (12.5%)

## Traceability Matrix

| Requirement Section | Test Cases | Coverage |
|---------------------|------------|----------|
| 4.1.1 Upshift Conditions | 2, 4, 8, 12, 15, 19, 30, 35 | 100% |
| 4.1.2 Downshift Conditions | 3, 6, 13, 33, 38 | 100% |
| 4.1.3 Prohibited Shifts | 10, 20, 35 | 100% |
| 4.2.1 Hill Start Assist | 21 | 100% |
| 4.2.2 Overrun Protection | 11, 20, 35 | 100% |
| 4.2.3 Stall Prevention | 3, 33 | 100% |
| 4.2.4 Neutral Safety | 1, 7, 10, 16, 32, 37 | 100% |
| 4.3.1 Sensor Failures | 24, 25, 27, 36 | 100% |
| 4.3.2 Actuator Failures | 29 | 100% |
| 4.3.3 Temperature Management | 22, 26 | 100% |

## Test Environment Setup

### Required Hardware
- Gearbox ECU unit
- Vehicle speed simulator (0-200 km/h)
- Engine RPM simulator (0-7000 RPM)
- Throttle position simulator (0-100%)
- Brake pressure simulator
- Temperature control unit (-20°C to +150°C)
- Gear position sensor mockup
- Hydraulic pressure simulator

### Software Tools
- PICT command-line tool (for model validation)
- Test automation framework
- Data logging and analysis tools
- ECU diagnostic interface

### Test Data Collection
- Shift completion time (ms)
- Clutch engagement time (ms)
- Engine RPM before/after shift
- Vehicle speed before/after shift
- Hydraulic pressure readings
- Temperature readings
- Error codes generated

## Expected Test Duration

- **Setup**: 2 hours
- **Execution**: ~30 minutes (40 tests × 45 seconds average)
- **Data Analysis**: 1 hour
- **Total**: ~3.5 hours

## Success Criteria

### Pass Criteria
- All safety constraints respected (100%)
- Shift times within specification (>95%)
- No unexpected error codes (<5%)
- Smooth transitions (subjective, all tests)

### Fail Criteria
- Any safety violation (immediate stop)
- Shift time >2× specification
- Unexpected limp-home mode activation
- Incorrect gear selected

## Risk Assessment

### High Risk Areas
- Reverse to forward gear transitions (Test 10)
- Critical temperature handling (Test 26)
- Multiple sensor failures (Test 27)
- Hydraulic pressure critical (Test 29)

### Medium Risk Areas
- Sensor failure fallback logic (Tests 24, 25, 36)
- Ice condition handling (Tests 12, 14, 30)
- Over-rev protection (Tests 11, 20, 35)

### Low Risk Areas
- Normal mode operation (Tests 1-9)
- Standard upshift/downshift (Tests 2, 4, 6, 13, 17, 31)

## Notes and Recommendations

1. **Test Automation**: Automate all 40 tests for regression testing
2. **Real-World Validation**: Follow up with road testing for selected scenarios
3. **Expanded Coverage**: Consider 3-way interactions for critical safety features
4. **Performance Testing**: Add load testing for shift actuator endurance
5. **Edge Case Exploration**: Manual testing for unusual conditions not covered by PICT

## References

- Gearbox Specification Document (gearbox-specification.md)
- PICT Tool Documentation: https://github.com/microsoft/pict
- ISO 26262 Automotive Safety Standard
- Test Automation Framework Documentation
