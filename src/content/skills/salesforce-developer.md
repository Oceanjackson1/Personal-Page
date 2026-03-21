---
title: "Salesforce 开发"
description: "Salesforce 平台开发，Apex 编程和 Lightning 组件构建"
category: "workflow"
source: "community"
author: "Community"
tags: ["salesforce", "developer"]
date: 2026-03-20
---

# Salesforce Developer

## Core Workflow

1. **Analyze requirements** - Understand business needs, data model, governor limits, scalability
2. **Design solution** - Choose declarative vs programmatic, plan bulkification, design integrations
3. **Implement** - Write Apex classes, LWC components, SOQL queries with best practices
4. **Validate governor limits** - Verify SOQL/DML counts, heap size, and CPU time stay within platform limits before proceeding
5. **Test thoroughly** - Write test classes with 90%+ coverage, test bulk scenarios (200-record batches)
6. **Deploy** - Use Salesforce DX, scratch orgs, CI/CD for metadata deployment

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Apex Development | `references/apex-development.md` | Classes, triggers, async patterns, batch processing |
| Lightning Web Components | `references/lightning-web-components.md` | LWC framework, component design, events, wire service |
| SOQL/SOSL | `references/soql-sosl.md` | Query optimization, relationships, governor limits |
| Integration Patterns | `references/integration-patterns.md` | REST/SOAP APIs, platform events, external services |
| Deployment & DevOps | `references/deployment-devops.md` | Salesforce DX, CI/CD, scratch orgs, metadata API |

## Constraints

### MUST DO
- Bulkify Apex code — collect IDs/records before loops, query/DML outside loops
- Write test classes with minimum 90% code coverage, including bulk scenarios
- Use selective SOQL queries with indexed fields; leverage relationship queries
- Use appropriate async processing (batch, queueable, future) for long-running work
- Implement proper error handling and logging; use `Database.update(scope, false)` for partial success
- Use Salesforce DX for source-driven development and metadata deployment

### MUST NOT DO
- Execute SOQL/DML inside loops (governor limit violation — see bulkified trigger pattern below)
- Hard-code IDs or credentials in code
- Create recursive triggers without safeguards
- Skip field-level security and sharing rules checks
- Use deprecated Salesforce APIs or components

## Code Patterns

### Bulkified Trigger (Correct Pattern)

```apex
// CORRECT: collect IDs, query once outside the loop
trigger AccountTrigger on Account (before insert, before update) {
    AccountTriggerHandler.handleBeforeInsert(Trigger.new);
}

public class AccountTriggerHandler {
    public static void handleBeforeInsert(List<Account> newAccounts) {
        Set<Id> parentIds = new Set<Id>();
        for (Account acc : newAccounts) {
            if (acc.ParentId != null) parentIds.add(acc.ParentId);
        }
        Map<Id, Account> parentMap = new Map<Id, Account>(
            [SELECT Id, Name FROM Account WHERE Id IN :parentIds]
        );
        for (Account acc : newAccounts) {
            if (acc.ParentId != null && parentMap.containsKey(acc.ParentId)) {
                acc.Description = 'Child of: ' + parentMap.get(acc.ParentId).Name;
            }
        }
    }
}
```

```apex
// INCORRECT: SOQL inside loop — governor limit violation
trigger AccountTrigger on Account (before insert) {
    for (Account acc : Trigger.new) {
        Account parent = [SELECT Id, Name FROM Account WHERE Id = :acc.ParentId]; // BAD
        acc.Description = 'Child of: ' + parent.Name;
    }
}
```

### Batch Apex

```apex
public class ContactBatchUpdate implements Database.Batchable<SObject> {
    public Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([SELECT Id, Email FROM Contact WHERE Email = null]);
    }
    public void execute(Database.BatchableContext bc, List<Contact> scope) {
        for (Contact c : scope) {
            c.Email = 'unknown@example.com';
        }
        Database.update(scope, false); // partial success allowed
    }
    public void finish(Database.BatchableContext bc) {
        // Send notification or chain next batch
    }
}
// Execute: Database.executeBatch(new ContactBatchUpdate(), 200);
```

### Test Class

```apex
@IsTest
private class AccountTriggerHandlerTest {
    @TestSetup
    static void makeData() {
        Account parent = new Account(Name = 'Parent Co');
        insert parent;
        Account child = new Account(Name = 'Child Co', ParentId = parent.Id);
        insert child;
    }

    @IsTest
    static void testBulkInsert() {
        Account parent = [SELECT Id FROM Account WHERE Name = 'Parent Co' LIMIT 1];
        List<Account> children = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            children.add(new Account(Name = 'Child ' + i, ParentId = parent.Id));
        }
        Test.startTest();
        insert children;
        Test.stopTest();

        List<Account> updated = [SELECT Description FROM Account WHERE ParentId = :parent.Id];
        System.assert(!updated.isEmpty(), 'Children should have descriptions set');
        System.assert(updated[0].Description.startsWith('Child of:'), 'Description format mismatch');
    }
}
```

### SOQL Best Practices

```apex
// Selective query — use indexed fields in WHERE clause
List<Opportunity> opps = [
    SELECT Id, Name, Amount, StageName
    FROM Opportunity
    WHERE AccountId IN :accountIds      // indexed field
      AND CloseDate >= :Date.today()    // indexed field
    ORDER BY CloseDate ASC
    LIMIT 200
];

// Relationship query to avoid extra round-trips
List<Account> accounts = [
    SELECT Id, Name,
           (SELECT Id, LastName, Email FROM Contacts WHERE Email != null)
    FROM Account
    WHERE Id IN :accountIds
];
```

### Lightning Web Component (Counter Example)

```html
<!-- counterComponent.html -->
<template>
    <lightning-card title="Counter">
        <div class="slds-p-around_medium">
            <p>Count: {count}</p>
            <lightning-button label="Increment" onclick={handleIncrement}></lightning-button>
        </div>
    </lightning-card>
</template>
```

```javascript
// counterComponent.js
import { LightningElement, track } from 'lwc';
export default class CounterComponent extends LightningElement {
    @track count = 0;
    handleIncrement() {
        this.count += 1;
    }
}
```

```xml
<!-- counterComponent.js-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>59.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__AppPage</target>
        <target>lightning__RecordPage</target>
    </targets>
</LightningComponentBundle>
```

---

## Reference: Apex Development

# Apex Development

---

## Apex Class Structure

### Service Layer Pattern

Separate business logic from triggers and controllers using service classes.

```apex
/**
 * AccountService - Business logic for Account operations
 * Follows Single Responsibility Principle
 */
public with sharing class AccountService {

    /**
     * Updates account ratings based on opportunity history
     * @param accountIds Set of Account IDs to process
     * @throws AccountServiceException on validation failure
     */
    public static void updateAccountRatings(Set<Id> accountIds) {
        if (accountIds == null || accountIds.isEmpty()) {
            return;
        }

        // Bulkified query - single SOQL for all records
        Map<Id, Account> accountsToUpdate = new Map<Id, Account>();

        for (Account acc : [
            SELECT Id, Rating,
                   (SELECT Amount, StageName FROM Opportunities
                    WHERE StageName = 'Closed Won')
            FROM Account
            WHERE Id IN :accountIds
        ]) {
            Decimal totalRevenue = 0;
            for (Opportunity opp : acc.Opportunities) {
                totalRevenue += opp.Amount != null ? opp.Amount : 0;
            }

            String newRating = calculateRating(totalRevenue);
            if (acc.Rating != newRating) {
                accountsToUpdate.put(acc.Id, new Account(
                    Id = acc.Id,
                    Rating = newRating
                ));
            }
        }

        if (!accountsToUpdate.isEmpty()) {
            update accountsToUpdate.values();
        }
    }

    private static String calculateRating(Decimal revenue) {
        if (revenue >= 1000000) return 'Hot';
        if (revenue >= 100000) return 'Warm';
        return 'Cold';
    }
}
```

### Domain Layer Pattern

Encapsulate object-specific logic in domain classes.

```apex
/**
 * Accounts Domain Class
 * Encapsulates Account-specific business rules
 */
public with sharing class Accounts {

    private List<Account> records;

    public Accounts(List<Account> records) {
        this.records = records;
    }

    public static Accounts newInstance(List<Account> records) {
        return new Accounts(records);
    }

    /**
     * Validates accounts before insert/update
     * @return List of validation errors
     */
    public List<String> validate() {
        List<String> errors = new List<String>();

        for (Account acc : records) {
            if (String.isBlank(acc.Name)) {
                errors.add('Account Name is required');
            }
            if (acc.AnnualRevenue != null && acc.AnnualRevenue < 0) {
                errors.add('Annual Revenue cannot be negative');
            }
        }

        return errors;
    }

    /**
     * Sets default values for new accounts
     */
    public void setDefaults() {
        for (Account acc : records) {
            if (String.isBlank(acc.Rating)) {
                acc.Rating = 'Cold';
            }
            if (acc.NumberOfEmployees == null) {
                acc.NumberOfEmployees = 0;
            }
        }
    }
}
```

---

## Trigger Framework

### Handler Pattern

Never put logic directly in triggers. Use a handler framework.

```apex
/**
 * AccountTrigger - Delegates all logic to handler
 */
trigger AccountTrigger on Account (
    before insert, before update, before delete,
    after insert, after update, after delete, after undelete
) {
    AccountTriggerHandler handler = new AccountTriggerHandler();

    switch on Trigger.operationType {
        when BEFORE_INSERT {
            handler.beforeInsert(Trigger.new);
        }
        when BEFORE_UPDATE {
            handler.beforeUpdate(Trigger.new, Trigger.oldMap);
        }
        when BEFORE_DELETE {
            handler.beforeDelete(Trigger.old, Trigger.oldMap);
        }
        when AFTER_INSERT {
            handler.afterInsert(Trigger.new, Trigger.newMap);
        }
        when AFTER_UPDATE {
            handler.afterUpdate(Trigger.new, Trigger.newMap, Trigger.old, Trigger.oldMap);
        }
        when AFTER_DELETE {
            handler.afterDelete(Trigger.old, Trigger.oldMap);
        }
        when AFTER_UNDELETE {
            handler.afterUndelete(Trigger.new, Trigger.newMap);
        }
    }
}
```

### Trigger Handler Class

```apex
/**
 * AccountTriggerHandler - Contains all trigger logic
 * Implements recursion prevention and bulkification
 */
public with sharing class AccountTriggerHandler {

    // Recursion prevention
    private static Boolean isExecuting = false;
    private static Set<Id> processedIds = new Set<Id>();

    public void beforeInsert(List<Account> newRecords) {
        Accounts domain = Accounts.newInstance(newRecords);
        domain.setDefaults();

        List<String> errors = domain.validate();
        if (!errors.isEmpty()) {
            for (Account acc : newRecords) {
                acc.addError(String.join(errors, '; '));
            }
        }
    }

    public void beforeUpdate(List<Account> newRecords, Map<Id, Account> oldMap) {
        // Field change detection
        for (Account acc : newRecords) {
            Account oldAcc = oldMap.get(acc.Id);

            if (acc.OwnerId != oldAcc.OwnerId) {
                // Owner changed - track for audit
                acc.Owner_Changed_Date__c = System.now();
            }
        }
    }

    public void afterInsert(List<Account> newRecords, Map<Id, Account> newMap) {
        if (isExecuting) return;
        isExecuting = true;

        try {
            // Create default contacts for new accounts
            createDefaultContacts(newRecords);
        } finally {
            isExecuting = false;
        }
    }

    public void afterUpdate(
        List<Account> newRecords,
        Map<Id, Account> newMap,
        List<Account> oldRecords,
        Map<Id, Account> oldMap
    ) {
        // Filter to only process records not already handled
        List<Account> toProcess = new List<Account>();
        for (Account acc : newRecords) {
            if (!processedIds.contains(acc.Id)) {
                toProcess.add(acc);
                processedIds.add(acc.Id);
            }
        }

        if (!toProcess.isEmpty()) {
            AccountService.updateAccountRatings(new Map<Id, Account>(toProcess).keySet());
        }
    }

    public void beforeDelete(List<Account> oldRecords, Map<Id, Account> oldMap) {
        // Prevent deletion of accounts with open opportunities
        Set<Id> accountIds = oldMap.keySet();
        Map<Id, Integer> openOppCounts = new Map<Id, Integer>();

        for (AggregateResult ar : [
            SELECT AccountId, COUNT(Id) cnt
            FROM Opportunity
            WHERE AccountId IN :accountIds
            AND IsClosed = false
            GROUP BY AccountId
        ]) {
            openOppCounts.put((Id)ar.get('AccountId'), (Integer)ar.get('cnt'));
        }

        for (Account acc : oldRecords) {
            if (openOppCounts.containsKey(acc.Id) && openOppCounts.get(acc.Id) > 0) {
                acc.addError('Cannot delete account with open opportunities');
            }
        }
    }

    public void afterDelete(List<Account> oldRecords, Map<Id, Account> oldMap) {
        // Audit logging for deleted accounts
        List<Account_Audit__c> auditRecords = new List<Account_Audit__c>();
        for (Account acc : oldRecords) {
            auditRecords.add(new Account_Audit__c(
                Account_Name__c = acc.Name,
                Action__c = 'Deleted',
                Deleted_Date__c = System.now(),
                Deleted_By__c = UserInfo.getUserId()
            ));
        }

        if (!auditRecords.isEmpty()) {
            insert auditRecords;
        }
    }

    public void afterUndelete(List<Account> newRecords, Map<Id, Account> newMap) {
        // Handle undelete scenarios
    }

    private void createDefaultContacts(List<Account> accounts) {
        List<Contact> contacts = new List<Contact>();
        for (Account acc : accounts) {
            contacts.add(new Contact(
                AccountId = acc.Id,
                LastName = 'Primary Contact',
                Email = 'primary@' + acc.Name.toLowerCase().replaceAll('[^a-z0-9]', '') + '.com'
            ));
        }

        if (!contacts.isEmpty()) {
            insert contacts;
        }
    }
}
```

---

## Asynchronous Apex Patterns

### When to Use Each Pattern

| Pattern | Use Case | Limits |
|---------|----------|--------|
| **Future** | Simple async callout, quick operations | 50 calls per transaction |
| **Queueable** | Chaining jobs, complex async logic | 50 jobs per transaction |
| **Batch** | Processing large data volumes | 5 active batches |
| **Scheduled** | Time-based execution | 100 scheduled jobs |

### Future Methods

Use for simple callouts or operations that don't need chaining.

```apex
public class AccountIntegration {

    /**
     * Sends account data to external system
     * @param accountIds Set of Account IDs to sync
     */
    @future(callout=true)
    public static void syncToExternalSystem(Set<Id> accountIds) {
        if (accountIds == null || accountIds.isEmpty()) {
            return;
        }

        List<Account> accounts = [
            SELECT Id, Name, BillingCity, BillingCountry, Industry
            FROM Account
            WHERE Id IN :accountIds
        ];

        Http http = new Http();
        HttpRequest request = new HttpRequest();
        request.setEndpoint('callout:External_System/api/accounts');
        request.setMethod('POST');
        request.setHeader('Content-Type', 'application/json');
        request.setBody(JSON.serialize(accounts));

        try {
            HttpResponse response = http.send(request);
            if (response.getStatusCode() != 200) {
                System.debug(LoggingLevel.ERROR,
                    'Sync failed: ' + response.getStatusCode() + ' ' + response.getBody());
            }
        } catch (Exception e) {
            System.debug(LoggingLevel.ERROR, 'Callout exception: ' + e.getMessage());
        }
    }
}
```

### Queueable Apex

Use for job chaining and passing complex data types.

```apex
/**
 * Queueable job for processing account hierarchies
 * Supports job chaining for large datasets
 */
public class AccountHierarchyProcessor implements Queueable, Database.AllowsCallouts {

    private List<Id> accountIds;
    private Integer depth;
    private static final Integer MAX_DEPTH = 5;
    private static final Integer BATCH_SIZE = 200;

    public AccountHierarchyProcessor(List<Id> accountIds, Integer depth) {
        this.accountIds = accountIds;
        this.depth = depth;
    }

    public void execute(QueueableContext context) {
        // Process current batch
        List<Account> accounts = [
            SELECT Id, Name, ParentId, Ultimate_Parent__c
            FROM Account
            WHERE Id IN :accountIds
        ];

        Set<Id> childAccountIds = new Set<Id>();
        List<Account> toUpdate = new List<Account>();

        for (Account acc : accounts) {
            if (acc.ParentId != null) {
                acc.Ultimate_Parent__c = findUltimateParent(acc.ParentId);
                toUpdate.add(acc);
            }

            // Collect child accounts for next iteration
            for (Account child : [
                SELECT Id FROM Account WHERE ParentId = :acc.Id
            ]) {
                childAccountIds.add(child.Id);
            }
        }

        if (!toUpdate.isEmpty()) {
            update toUpdate;
        }

        // Chain next job if there are child accounts and within depth limit
        if (!childAccountIds.isEmpty() && depth < MAX_DEPTH) {
            List<Id> nextBatch = new List<Id>(childAccountIds);
            if (nextBatch.size() > BATCH_SIZE) {
                nextBatch = new List<Id>();
                Integer count = 0;
                for (Id accId : childAccountIds) {
                    if (count++ >= BATCH_SIZE) break;
                    nextBatch.add(accId);
                }
            }

            if (!Test.isRunningTest()) {
                System.enqueueJob(new AccountHierarchyProcessor(nextBatch, depth + 1));
            }
        }
    }

    private Id findUltimateParent(Id parentId) {
        Account current = [SELECT Id, ParentId FROM Account WHERE Id = :parentId];
        while (current.ParentId != null) {
            current = [SELECT Id, ParentId FROM Account WHERE Id = :current.ParentId];
        }
        return current.Id;
    }
}

// Usage
// System.enqueueJob(new AccountHierarchyProcessor(accountIds, 0));
```

### Batch Apex

Use for processing large data volumes (millions of records).

```apex
/**
 * Batch job for annual account cleanup
 * Processes inactive accounts in configurable batch sizes
 */
public class AccountCleanupBatch implements
    Database.Batchable<SObject>,
    Database.Stateful,
    Database.AllowsCallouts {

    private Integer successCount = 0;
    private Integer failureCount = 0;
    private List<String> errors = new List<String>();
    private Date cutoffDate;

    public AccountCleanupBatch() {
        this.cutoffDate = Date.today().addYears(-2);
    }

    public AccountCleanupBatch(Date cutoffDate) {
        this.cutoffDate = cutoffDate;
    }

    /**
     * Query locator - defines records to process
     * Governor limit: 50 million records max
     */
    public Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Name, LastActivityDate,
                   (SELECT Id FROM Opportunities WHERE IsClosed = false LIMIT 1)
            FROM Account
            WHERE LastActivityDate < :cutoffDate
            AND IsActive__c = true
        ]);
    }

    /**
     * Execute - processes each batch of records
     * Default batch size: 200, configurable up to 2000
     */
    public void execute(Database.BatchableContext bc, List<Account> scope) {
        List<Account> toDeactivate = new List<Account>();

        for (Account acc : scope) {
            // Skip accounts with open opportunities
            if (acc.Opportunities != null && !acc.Opportunities.isEmpty()) {
                continue;
            }

            toDeactivate.add(new Account(
                Id = acc.Id,
                IsActive__c = false,
                Deactivated_Date__c = Date.today(),
                Deactivated_Reason__c = 'No activity for 2+ years'
            ));
        }

        if (!toDeactivate.isEmpty()) {
            Database.SaveResult[] results = Database.update(toDeactivate, false);

            for (Integer i = 0; i < results.size(); i++) {
                if (results[i].isSuccess()) {
                    successCount++;
                } else {
                    failureCount++;
                    for (Database.Error err : results[i].getErrors()) {
                        errors.add(toDeactivate[i].Id + ': ' + err.getMessage());
                    }
                }
            }
        }
    }

    /**
     * Finish - executes after all batches complete
     */
    public void finish(Database.BatchableContext bc) {
        // Send summary email
        Messaging.SingleEmailMessage email = new Messaging.SingleEmailMessage();
        email.setToAddresses(new List<String>{'admin@company.com'});
        email.setSubject('Account Cleanup Batch Complete');
        email.setPlainTextBody(
            'Batch Job Complete\n' +
            'Success: ' + successCount + '\n' +
            'Failures: ' + failureCount + '\n' +
            (errors.isEmpty() ? '' : '\nErrors:\n' + String.join(errors, '\n'))
        );

        Messaging.sendEmail(new List<Messaging.SingleEmailMessage>{email});

        // Log completion
        System.debug('Account Cleanup Complete - Success: ' + successCount + ', Failures: ' + failureCount);
    }
}

// Execute batch with custom size
// Database.executeBatch(new AccountCleanupBatch(), 100);
```

### Scheduled Apex

Use for time-based job execution.

```apex
/**
 * Scheduled job to run daily account maintenance
 */
public class DailyAccountMaintenance implements Schedulable {

    public void execute(SchedulableContext sc) {
        // Start batch job
        Database.executeBatch(new AccountCleanupBatch(), 200);

        // Queue additional maintenance
        System.enqueueJob(new AccountHierarchyProcessor(getTopLevelAccounts(), 0));
    }

    private List<Id> getTopLevelAccounts() {
        List<Id> topLevel = new List<Id>();
        for (Account acc : [
            SELECT Id FROM Account
            WHERE ParentId = null
            LIMIT 100
        ]) {
            topLevel.add(acc.Id);
        }
        return topLevel;
    }

    /**
     * Schedule helper - schedules job for daily 2 AM execution
     */
    public static void scheduleDaily() {
        // CRON: Seconds Minutes Hours Day_of_month Month Day_of_week Year
        String cronExp = '0 0 2 * * ?'; // 2 AM daily
        System.schedule('Daily Account Maintenance', cronExp, new DailyAccountMaintenance());
    }
}
```

---

## Governor Limit Management

### Key Limits to Monitor

| Limit | Synchronous | Asynchronous |
|-------|-------------|--------------|
| SOQL Queries | 100 | 200 |
| SOQL Rows | 50,000 | 50,000 |
| DML Statements | 150 | 150 |
| DML Rows | 10,000 | 10,000 |
| Heap Size | 6 MB | 12 MB |
| CPU Time | 10,000 ms | 60,000 ms |
| Callouts | 100 | 100 |

### Limit Checking Utility

```apex
/**
 * Utility class for monitoring governor limits
 */
public class LimitMonitor {

    public static void logLimits(String context) {
        System.debug(LoggingLevel.INFO, '=== Limits for: ' + context + ' ===');
        System.debug('SOQL Queries: ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
        System.debug('SOQL Rows: ' + Limits.getQueryRows() + '/' + Limits.getLimitQueryRows());
        System.debug('DML Statements: ' + Limits.getDmlStatements() + '/' + Limits.getLimitDmlStatements());
        System.debug('DML Rows: ' + Limits.getDmlRows() + '/' + Limits.getLimitDmlRows());
        System.debug('Heap Size: ' + Limits.getHeapSize() + '/' + Limits.getLimitHeapSize());
        System.debug('CPU Time: ' + Limits.getCpuTime() + '/' + Limits.getLimitCpuTime());
    }

    /**
     * Checks if approaching limit threshold
     * @param threshold Percentage (0-100) to trigger warning
     */
    public static Boolean isApproachingQueryLimit(Integer threshold) {
        return (Limits.getQueries() * 100 / Limits.getLimitQueries()) >= threshold;
    }

    public static Boolean isApproachingHeapLimit(Integer threshold) {
        return (Limits.getHeapSize() * 100 / Limits.getLimitHeapSize()) >= threshold;
    }
}
```

---

## Test Classes

### Test Best Practices

```apex
/**
 * Test class for AccountService
 * Demonstrates test patterns and best practices
 */
@isTest
private class AccountServiceTest {

    /**
     * Test data factory - create test records efficiently
     */
    @TestSetup
    static void setupTestData() {
        // Create test accounts
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            accounts.add(new Account(
                Name = 'Test Account ' + i,
                Industry = 'Technology'
            ));
        }
        insert accounts;

        // Create opportunities for some accounts
        List<Opportunity> opps = new List<Opportunity>();
        for (Integer i = 0; i < 50; i++) {
            opps.add(new Opportunity(
                Name = 'Test Opp ' + i,
                AccountId = accounts[i].Id,
                StageName = 'Closed Won',
                CloseDate = Date.today(),
                Amount = 100000 * (i + 1)
            ));
        }
        insert opps;
    }

    @isTest
    static void testUpdateAccountRatings_HotRating() {
        // Arrange
        Account acc = [SELECT Id FROM Account WHERE Name = 'Test Account 0' LIMIT 1];

        // Create high-value opportunity
        insert new Opportunity(
            Name = 'Big Deal',
            AccountId = acc.Id,
            StageName = 'Closed Won',
            CloseDate = Date.today(),
            Amount = 1500000
        );

        // Act
        Test.startTest();
        AccountService.updateAccountRatings(new Set<Id>{acc.Id});
        Test.stopTest();

        // Assert
        Account updated = [SELECT Rating FROM Account WHERE Id = :acc.Id];
        System.assertEquals('Hot', updated.Rating, 'Account with >$1M revenue should be Hot');
    }

    @isTest
    static void testUpdateAccountRatings_BulkOperation() {
        // Arrange - get all test accounts
        List<Account> accounts = [SELECT Id FROM Account];
        Set<Id> accountIds = new Map<Id, Account>(accounts).keySet();

        // Act
        Test.startTest();
        AccountService.updateAccountRatings(accountIds);
        Test.stopTest();

        // Assert - verify bulk processing didn't hit limits
        System.assert(Limits.getQueries() < Limits.getLimitQueries(),
            'Should not exhaust SOQL queries');
    }

    @isTest
    static void testUpdateAccountRatings_EmptySet() {
        // Act
        Test.startTest();
        AccountService.updateAccountRatings(new Set<Id>());
        AccountService.updateAccountRatings(null);
        Test.stopTest();

        // Assert - no exceptions thrown
        System.assert(true, 'Should handle empty/null input gracefully');
    }

    /**
     * Test async job execution
     */
    @isTest
    static void testAccountHierarchyProcessor() {
        // Arrange
        Account parent = new Account(Name = 'Parent Account');
        insert parent;

        Account child = new Account(Name = 'Child Account', ParentId = parent.Id);
        insert child;

        // Act
        Test.startTest();
        System.enqueueJob(new AccountHierarchyProcessor(
            new List<Id>{child.Id}, 0
        ));
        Test.stopTest();

        // Assert
        Account updated = [SELECT Ultimate_Parent__c FROM Account WHERE Id = :child.Id];
        System.assertEquals(parent.Id, updated.Ultimate_Parent__c,
            'Ultimate parent should be set');
    }

    /**
     * Test batch processing
     */
    @isTest
    static void testAccountCleanupBatch() {
        // Arrange - create old inactive account
        Account oldAccount = new Account(
            Name = 'Old Inactive Account',
            IsActive__c = true
        );
        insert oldAccount;

        // Backdate last activity
        Test.setCreatedDate(oldAccount.Id, DateTime.now().addYears(-3));

        // Act
        Test.startTest();
        Database.executeBatch(new AccountCleanupBatch(Date.today().addYears(-2)), 200);
        Test.stopTest();

        // Assert - batch job queued successfully
        System.assert(true, 'Batch should execute without errors');
    }
}
```

---

## When to Use

- **Service classes**: Complex business logic shared across multiple entry points
- **Domain classes**: Object-specific validation and behavior
- **Trigger handlers**: All trigger-based automation
- **Future methods**: Simple callouts, fire-and-forget operations
- **Queueable**: Job chaining, complex async operations
- **Batch**: Processing >10,000 records

## When NOT to Use

- **Triggers for simple updates**: Use Flow for declarative automation
- **Future for complex logic**: Use Queueable instead
- **Batch for small datasets**: Overhead not worth it for <1,000 records
- **SOQL in loops**: Always bulkify queries outside loops

---

## Reference: Deployment Devops

# Deployment and DevOps

---

## Salesforce DX Project Setup

### Project Structure

```
my-salesforce-project/
├── .forceignore              # Files to ignore in deployments
├── .gitignore                # Git ignore patterns
├── sfdx-project.json         # Project configuration
├── config/
│   └── project-scratch-def.json  # Scratch org definition
├── force-app/
│   └── main/
│       └── default/
│           ├── classes/      # Apex classes
│           ├── triggers/     # Apex triggers
│           ├── lwc/          # Lightning Web Components
│           ├── aura/         # Aura components
│           ├── objects/      # Custom objects
│           ├── layouts/      # Page layouts
│           ├── flows/        # Flows
│           ├── profiles/     # Profiles
│           ├── permissionsets/  # Permission sets
│           └── staticresources/ # Static resources
├── scripts/
│   └── apex/                 # Anonymous Apex scripts
├── data/                     # Sample data files
└── manifest/
    └── package.xml           # Deployment manifest
```

### sfdx-project.json

```json
{
  "packageDirectories": [
    {
      "path": "force-app",
      "default": true,
      "package": "MyPackage",
      "versionName": "ver 1.0",
      "versionNumber": "1.0.0.NEXT",
      "definitionFile": "config/project-scratch-def.json"
    },
    {
      "path": "unpackaged",
      "default": false
    }
  ],
  "name": "my-salesforce-project",
  "namespace": "",
  "sfdcLoginUrl": "https://login.salesforce.com",
  "sourceApiVersion": "59.0",
  "plugins": {
    "salesforcedx-templates": {
      "minApiVersion": "55.0"
    }
  }
}
```

### Scratch Org Definition

```json
{
  "orgName": "My Company Dev Org",
  "edition": "Developer",
  "features": [
    "EnableSetPasswordInApi",
    "Communities",
    "ServiceCloud",
    "SalesCloud",
    "MultiCurrency"
  ],
  "settings": {
    "lightningExperienceSettings": {
      "enableS1DesktopEnabled": true
    },
    "mobileSettings": {
      "enableS1EncryptedStoragePref2": false
    },
    "securitySettings": {
      "passwordPolicies": {
        "enableSetPasswordInApi": true
      }
    },
    "communitiesSettings": {
      "enableNetworksEnabled": true
    },
    "languageSettings": {
      "enableTranslationWorkbench": true
    }
  },
  "objectSettings": {
    "opportunity": {
      "sharingModel": "private"
    },
    "account": {
      "sharingModel": "readWrite"
    }
  }
}
```

### .forceignore

```
# Profiles (use Permission Sets instead)
**/profiles/**

# User-specific settings
**/settings/**

# Package installation
**/*-meta.xml.bak

# IDE files
.sfdx/
.sf/
.idea/
*.log

# OS files
.DS_Store
Thumbs.db

# Test data
**/test-data/**

# Ignore standard objects
**/objects/Account/fields/IsDeleted.field-meta.xml
**/objects/Account/fields/IsPersonAccount.field-meta.xml
```

---

## SF CLI Commands

### Authentication

```bash
# Login to Dev Hub (web browser)
sf org login web --set-default-dev-hub --alias mydevhub

# Login to production/sandbox
sf org login web --alias myprod --instance-url https://login.salesforce.com
sf org login web --alias mysandbox --instance-url https://test.salesforce.com

# Login with JWT (CI/CD)
sf org login jwt \
  --client-id YOUR_CONNECTED_APP_CLIENT_ID \
  --jwt-key-file server.key \
  --username admin@mycompany.com \
  --set-default-dev-hub \
  --alias mydevhub

# List authenticated orgs
sf org list

# Logout
sf org logout --target-org myalias
```

### Scratch Org Management

```bash
# Create scratch org (30-day expiration)
sf org create scratch \
  --definition-file config/project-scratch-def.json \
  --alias myscratch \
  --set-default \
  --duration-days 30

# Open scratch org in browser
sf org open --target-org myscratch

# Push source to scratch org
sf project deploy start --target-org myscratch

# Pull changes from scratch org
sf project retrieve start --target-org myscratch

# Delete scratch org
sf org delete scratch --target-org myscratch --no-prompt

# List scratch orgs
sf org list --all
```

### Source Deployment

```bash
# Deploy to target org
sf project deploy start --target-org myprod

# Deploy specific metadata
sf project deploy start \
  --target-org myprod \
  --source-dir force-app/main/default/classes

# Deploy with tests
sf project deploy start \
  --target-org myprod \
  --test-level RunLocalTests

# Deploy using manifest
sf project deploy start \
  --target-org myprod \
  --manifest manifest/package.xml

# Quick deploy (after validation)
sf project deploy quick --job-id 0Af...

# Check deploy status
sf project deploy report --job-id 0Af...

# Cancel deployment
sf project deploy cancel --job-id 0Af...
```

### Retrieve Metadata

```bash
# Retrieve all metadata
sf project retrieve start --target-org myprod

# Retrieve specific components
sf project retrieve start \
  --target-org myprod \
  --metadata ApexClass:AccountService

# Retrieve using package.xml
sf project retrieve start \
  --target-org myprod \
  --manifest manifest/package.xml

# Generate package.xml from org
sf project generate manifest \
  --from-org myprod \
  --output-dir manifest
```

### Running Tests

```bash
# Run all tests
sf apex run test --target-org myscratch --code-coverage --result-format human

# Run specific test classes
sf apex run test \
  --target-org myscratch \
  --class-names AccountServiceTest,ContactServiceTest \
  --code-coverage

# Run tests with output to file
sf apex run test \
  --target-org myscratch \
  --test-level RunLocalTests \
  --output-dir test-results \
  --wait 10

# Run async tests and check later
sf apex run test --target-org myscratch --synchronous false
sf apex get test --target-org myscratch --test-run-id 707...
```

### Data Operations

```bash
# Export data using SOQL
sf data query \
  --target-org myprod \
  --query "SELECT Id, Name FROM Account LIMIT 10" \
  --result-format csv \
  > accounts.csv

# Import data
sf data import tree \
  --target-org myscratch \
  --plan data/sample-data-plan.json

# Export data for reimport
sf data export tree \
  --target-org myprod \
  --query "SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account LIMIT 10" \
  --output-dir data

# Bulk upsert
sf data upsert bulk \
  --target-org myprod \
  --sobject Account \
  --file accounts.csv \
  --external-id External_Id__c
```

---

## Package.xml Manifest

### Complete Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>AccountService</members>
        <members>AccountTriggerHandler</members>
        <members>HttpCalloutService</members>
        <name>ApexClass</name>
    </types>
    <types>
        <members>AccountServiceTest</members>
        <name>ApexClass</name>
    </types>
    <types>
        <members>AccountTrigger</members>
        <name>ApexTrigger</name>
    </types>
    <types>
        <members>accountCard</members>
        <members>accountList</members>
        <name>LightningComponentBundle</name>
    </types>
    <types>
        <members>Account.External_System_Id__c</members>
        <members>Account.IsActive__c</members>
        <name>CustomField</name>
    </types>
    <types>
        <members>Integration_Log__c</members>
        <members>Account_Audit__c</members>
        <name>CustomObject</name>
    </types>
    <types>
        <members>Account_Manager</members>
        <members>Sales_Rep</members>
        <name>PermissionSet</name>
    </types>
    <types>
        <members>Order_Event__e</members>
        <name>PlatformEventChannel</name>
    </types>
    <types>
        <members>Account_Update_Flow</members>
        <name>Flow</name>
    </types>
    <types>
        <members>External_System</members>
        <name>NamedCredential</name>
    </types>
    <types>
        <members>CustomLabels</members>
        <name>CustomLabels</name>
    </types>
    <version>59.0</version>
</Package>
```

### Wildcard Retrieval

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>*</members>
        <name>ApexClass</name>
    </types>
    <types>
        <members>*</members>
        <name>ApexTrigger</name>
    </types>
    <types>
        <members>*</members>
        <name>LightningComponentBundle</name>
    </types>
    <types>
        <members>*</members>
        <name>CustomObject</name>
    </types>
    <types>
        <members>*</members>
        <name>Flow</name>
    </types>
    <version>59.0</version>
</Package>
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/salesforce-ci.yml
name: Salesforce CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'force-app/**'
      - 'manifest/**'
  pull_request:
    branches: [main, develop]

env:
  SFDX_CLI_URL: https://developer.salesforce.com/media/salesforce-cli/sf/channels/stable/sf-linux-x64.tar.xz

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Salesforce CLI
        run: |
          wget $SFDX_CLI_URL
          mkdir sfdx
          tar xJf sf-linux-x64.tar.xz -C sfdx --strip-components 1
          ./sfdx/bin/sf version

      - name: Authenticate to Dev Hub
        run: |
          echo "${{ secrets.SFDX_AUTH_URL }}" > auth.txt
          ./sfdx/bin/sf org login sfdx-url --sfdx-url-file auth.txt --alias devhub --set-default-dev-hub

      - name: Create Scratch Org
        run: |
          ./sfdx/bin/sf org create scratch \
            --definition-file config/project-scratch-def.json \
            --alias ci-scratch \
            --set-default \
            --duration-days 1

      - name: Push Source
        run: ./sfdx/bin/sf project deploy start --target-org ci-scratch

      - name: Run Apex Tests
        run: |
          ./sfdx/bin/sf apex run test \
            --target-org ci-scratch \
            --code-coverage \
            --result-format human \
            --wait 20 \
            --test-level RunLocalTests

      - name: Check Code Coverage
        run: |
          COVERAGE=$(./sfdx/bin/sf apex get test --target-org ci-scratch --code-coverage --json | jq '.result.summary.orgWideCoverage' | tr -d '"' | tr -d '%')
          echo "Code coverage: $COVERAGE%"
          if [ "$COVERAGE" -lt "75" ]; then
            echo "Code coverage is below 75%"
            exit 1
          fi

      - name: Delete Scratch Org
        if: always()
        run: ./sfdx/bin/sf org delete scratch --target-org ci-scratch --no-prompt

  deploy-staging:
    needs: validate
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Salesforce CLI
        run: |
          wget $SFDX_CLI_URL
          mkdir sfdx
          tar xJf sf-linux-x64.tar.xz -C sfdx --strip-components 1

      - name: Authenticate to Staging
        run: |
          echo "${{ secrets.STAGING_AUTH_URL }}" > auth.txt
          ./sfdx/bin/sf org login sfdx-url --sfdx-url-file auth.txt --alias staging

      - name: Deploy to Staging
        run: |
          ./sfdx/bin/sf project deploy start \
            --target-org staging \
            --test-level RunLocalTests \
            --wait 30

  deploy-production:
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Salesforce CLI
        run: |
          wget $SFDX_CLI_URL
          mkdir sfdx
          tar xJf sf-linux-x64.tar.xz -C sfdx --strip-components 1

      - name: Authenticate to Production
        run: |
          echo "${{ secrets.PROD_AUTH_URL }}" > auth.txt
          ./sfdx/bin/sf org login sfdx-url --sfdx-url-file auth.txt --alias prod

      - name: Validate Deployment
        run: |
          ./sfdx/bin/sf project deploy validate \
            --target-org prod \
            --test-level RunLocalTests \
            --wait 30

      - name: Quick Deploy
        run: |
          JOB_ID=$(./sfdx/bin/sf project deploy report --json | jq -r '.result.id')
          ./sfdx/bin/sf project deploy quick --job-id $JOB_ID --target-org prod
```

### GitLab CI Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - deploy

variables:
  SF_CLI_VERSION: "2.20.7"

.sf_base:
  image: salesforce/cli:${SF_CLI_VERSION}-full
  before_script:
    - sf --version

validate:
  extends: .sf_base
  stage: validate
  script:
    - echo $SFDX_AUTH_URL > auth.txt
    - sf org login sfdx-url --sfdx-url-file auth.txt --alias devhub --set-default-dev-hub
    - sf org create scratch --definition-file config/project-scratch-def.json --alias ci-scratch --set-default --duration-days 1
    - sf project deploy start --target-org ci-scratch
    - sf apex run test --target-org ci-scratch --code-coverage --result-format junit --output-dir test-results --wait 20
  after_script:
    - sf org delete scratch --target-org ci-scratch --no-prompt || true
  artifacts:
    reports:
      junit: test-results/*.xml
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

deploy_staging:
  extends: .sf_base
  stage: deploy
  environment:
    name: staging
  script:
    - echo $STAGING_AUTH_URL > auth.txt
    - sf org login sfdx-url --sfdx-url-file auth.txt --alias staging
    - sf project deploy start --target-org staging --test-level RunLocalTests --wait 30
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy_production:
  extends: .sf_base
  stage: deploy
  environment:
    name: production
  script:
    - echo $PROD_AUTH_URL > auth.txt
    - sf org login sfdx-url --sfdx-url-file auth.txt --alias prod
    - sf project deploy start --target-org prod --test-level RunLocalTests --wait 30
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
```

---

## Deployment Scripts

### Pre-Deployment Validation

```bash
#!/bin/bash
# scripts/validate-deployment.sh

set -e

TARGET_ORG=${1:-"myscratch"}
TEST_LEVEL=${2:-"RunLocalTests"}

echo "=== Validating deployment to $TARGET_ORG ==="

# Check for uncommitted changes
if [[ $(git status --porcelain) ]]; then
    echo "Warning: Uncommitted changes detected"
fi

# Validate package.xml
if [ ! -f "manifest/package.xml" ]; then
    echo "Error: manifest/package.xml not found"
    exit 1
fi

# Run validation
echo "Starting validation deploy..."
sf project deploy validate \
    --target-org "$TARGET_ORG" \
    --manifest manifest/package.xml \
    --test-level "$TEST_LEVEL" \
    --wait 60

echo "=== Validation complete ==="
```

### Post-Deployment Script

```bash
#!/bin/bash
# scripts/post-deployment.sh

set -e

TARGET_ORG=${1:-"myprod"}

echo "=== Running post-deployment tasks ==="

# Run data migration scripts
echo "Running data migration..."
sf apex run \
    --target-org "$TARGET_ORG" \
    --file scripts/apex/data-migration.apex

# Assign permission sets
echo "Assigning permission sets..."
sf org assign permset \
    --target-org "$TARGET_ORG" \
    --name Sales_Manager \
    --on-behalf-of admin@company.com

# Clear cache
echo "Clearing org cache..."
sf apex run \
    --target-org "$TARGET_ORG" \
    --file scripts/apex/clear-cache.apex

echo "=== Post-deployment complete ==="
```

### Anonymous Apex for Deployment

```apex
// scripts/apex/data-migration.apex
// Run data migration after deployment

System.debug('Starting data migration...');

// Update existing records with new field values
List<Account> accounts = [
    SELECT Id, Legacy_Status__c
    FROM Account
    WHERE New_Status__c = null
    AND Legacy_Status__c != null
    LIMIT 10000
];

Map<String, String> statusMapping = new Map<String, String>{
    'A' => 'Active',
    'I' => 'Inactive',
    'P' => 'Pending'
};

for (Account acc : accounts) {
    acc.New_Status__c = statusMapping.get(acc.Legacy_Status__c);
}

if (!accounts.isEmpty()) {
    Database.update(accounts, false);
    System.debug('Updated ' + accounts.size() + ' accounts');
}

System.debug('Data migration complete');
```

---

## Metadata API Operations

### Programmatic Metadata Deployment

```apex
/**
 * Deploy metadata using Metadata API
 */
public class MetadataDeployer {

    public static Id deployZip(Blob zipFile, Boolean checkOnly) {
        Metadata.DeployContainer container = new Metadata.DeployContainer();

        // For zip deployment, use REST API instead
        HttpRequest req = new HttpRequest();
        req.setEndpoint(URL.getOrgDomainUrl().toExternalForm() +
            '/services/data/v59.0/metadata/deployRequest');
        req.setMethod('POST');
        req.setHeader('Authorization', 'Bearer ' + UserInfo.getSessionId());
        req.setHeader('Content-Type', 'application/zip');
        req.setBodyAsBlob(zipFile);

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() == 200) {
            Map<String, Object> result = (Map<String, Object>)JSON.deserializeUntyped(res.getBody());
            return (Id)result.get('id');
        }

        throw new MetadataException('Deployment failed: ' + res.getBody());
    }

    /**
     * Check deployment status
     */
    public static Metadata.DeployResult checkDeployStatus(Id deployId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint(URL.getOrgDomainUrl().toExternalForm() +
            '/services/data/v59.0/metadata/deployRequest/' + deployId + '?includeDetails=true');
        req.setMethod('GET');
        req.setHeader('Authorization', 'Bearer ' + UserInfo.getSessionId());

        Http http = new Http();
        HttpResponse res = http.send(req);

        // Parse response...
        return null;
    }

    public class MetadataException extends Exception {}
}
```

### Creating Metadata Programmatically

```apex
/**
 * Create custom field using Metadata API
 */
public class MetadataFieldCreator implements Metadata.DeployCallback {

    public void createCustomField(
        String objectName,
        String fieldName,
        String fieldLabel,
        String fieldType
    ) {
        Metadata.CustomField customField = new Metadata.CustomField();
        customField.fullName = objectName + '.' + fieldName;
        customField.label = fieldLabel;
        customField.type_x = Metadata.FieldType.valueOf(fieldType);

        if (fieldType == 'Text') {
            customField.length = 255;
        }

        Metadata.DeployContainer container = new Metadata.DeployContainer();
        container.addMetadata(customField);

        Id jobId = Metadata.Operations.enqueueDeployment(container, this);
        System.debug('Deployment job ID: ' + jobId);
    }

    public void handleResult(
        Metadata.DeployResult result,
        Metadata.DeployCallbackContext context
    ) {
        if (result.status == Metadata.DeployStatus.Succeeded) {
            System.debug('Deployment succeeded');
        } else {
            System.debug('Deployment failed: ' + result.errorMessage);
        }
    }
}
```

---

## Environment Management

### Sandbox Refresh Scripts

```bash
#!/bin/bash
# scripts/post-sandbox-refresh.sh

# Run after sandbox refresh to configure environment

TARGET_ORG=${1:-"sandbox"}

echo "=== Post-Sandbox Refresh Configuration ==="

# 1. Update custom settings
sf apex run --target-org "$TARGET_ORG" << 'EOF'
// Update environment-specific settings
Integration_Settings__c settings = Integration_Settings__c.getOrgDefaults();
settings.Endpoint_URL__c = 'https://sandbox-api.external-system.com';
settings.Environment__c = 'Sandbox';
upsert settings;
System.debug('Settings updated');
EOF

# 2. Deactivate production workflows
sf apex run --target-org "$TARGET_ORG" << 'EOF'
// Deactivate production-only processes
List<ProcessDefinition> processes = [
    SELECT Id, Name
    FROM ProcessDefinition
    WHERE Name LIKE 'PROD_%'
];
System.debug('Found ' + processes.size() + ' production processes to review');
// Note: ProcessDefinition activation must be done via Setup or Metadata API
EOF

# 3. Mask sensitive data
sf apex run --target-org "$TARGET_ORG" << 'EOF'
// Mask email addresses
List<Contact> contacts = [SELECT Id, Email FROM Contact WHERE Email != null LIMIT 10000];
for (Contact c : contacts) {
    c.Email = c.Id + '@sandbox.invalid';
}
update contacts;
System.debug('Masked ' + contacts.size() + ' contact emails');
EOF

echo "=== Post-refresh configuration complete ==="
```

---

## When to Use

- **Scratch orgs**: Development and testing of new features
- **Sandboxes**: Integration testing, UAT, training
- **Package.xml**: Selective metadata deployment
- **CI/CD pipelines**: Automated testing and deployment
- **Metadata API**: Programmatic org configuration

## When NOT to Use

- **Scratch orgs for production data**: Use sandboxes for data-dependent testing
- **Manual deployments in production**: Always use CI/CD for audit trail
- **Wildcard package.xml in production**: Explicitly list components
- **Deployment without tests**: Always run tests in production deployments
- **Direct changes in production**: Always deploy through version control

---

## Reference: Integration Patterns

# Integration Patterns

---

## REST API Integration

### Outbound REST Callouts

Calling external APIs from Salesforce.

```apex
/**
 * HTTP Callout Service
 * Handles outbound REST API calls with retry logic
 */
public class HttpCalloutService {

    private static final Integer MAX_RETRIES = 3;
    private static final Integer TIMEOUT_MS = 30000;

    /**
     * Performs GET request with retry logic
     */
    public static HttpResponse doGet(String endpoint, Map<String, String> headers) {
        return doCallout('GET', endpoint, headers, null);
    }

    /**
     * Performs POST request with JSON body
     */
    public static HttpResponse doPost(String endpoint, Map<String, String> headers, Object body) {
        return doCallout('POST', endpoint, headers, JSON.serialize(body));
    }

    /**
     * Generic callout method with retry logic
     */
    private static HttpResponse doCallout(
        String method,
        String endpoint,
        Map<String, String> headers,
        String body
    ) {
        HttpRequest request = new HttpRequest();
        request.setEndpoint(endpoint);
        request.setMethod(method);
        request.setTimeout(TIMEOUT_MS);

        // Set default headers
        request.setHeader('Content-Type', 'application/json');
        request.setHeader('Accept', 'application/json');

        // Set custom headers
        if (headers != null) {
            for (String key : headers.keySet()) {
                request.setHeader(key, headers.get(key));
            }
        }

        // Set body for POST/PUT/PATCH
        if (String.isNotBlank(body)) {
            request.setBody(body);
        }

        Http http = new Http();
        HttpResponse response;
        Integer retryCount = 0;

        while (retryCount < MAX_RETRIES) {
            try {
                response = http.send(request);

                // Success or client error - don't retry
                if (response.getStatusCode() < 500) {
                    break;
                }

                // Server error - retry
                retryCount++;
                if (retryCount < MAX_RETRIES) {
                    // Exponential backoff simulation via logging
                    System.debug('Retry ' + retryCount + ' after server error');
                }

            } catch (CalloutException e) {
                retryCount++;
                if (retryCount >= MAX_RETRIES) {
                    throw e;
                }
            }
        }

        return response;
    }
}
```

### Named Credentials

Always use Named Credentials for secure credential management.

```apex
/**
 * External API integration using Named Credentials
 */
public class ExternalApiService {

    // Named Credential endpoint (configured in Setup > Named Credentials)
    private static final String NAMED_CREDENTIAL = 'callout:External_API';

    /**
     * Get customer data from external system
     */
    public static CustomerResponse getCustomer(String customerId) {
        String endpoint = NAMED_CREDENTIAL + '/customers/' + customerId;

        HttpResponse response = HttpCalloutService.doGet(endpoint, null);

        if (response.getStatusCode() == 200) {
            return (CustomerResponse)JSON.deserialize(
                response.getBody(),
                CustomerResponse.class
            );
        } else {
            throw new IntegrationException(
                'Failed to get customer: ' + response.getStatusCode() +
                ' - ' + response.getBody()
            );
        }
    }

    /**
     * Create customer in external system
     */
    public static CustomerResponse createCustomer(CustomerRequest request) {
        String endpoint = NAMED_CREDENTIAL + '/customers';

        HttpResponse response = HttpCalloutService.doPost(endpoint, null, request);

        if (response.getStatusCode() == 201) {
            return (CustomerResponse)JSON.deserialize(
                response.getBody(),
                CustomerResponse.class
            );
        } else {
            throw new IntegrationException(
                'Failed to create customer: ' + response.getBody()
            );
        }
    }

    // Request/Response wrapper classes
    public class CustomerRequest {
        public String name;
        public String email;
        public String phone;
        public Address address;
    }

    public class CustomerResponse {
        public String id;
        public String name;
        public String email;
        public String status;
        public DateTime createdAt;
    }

    public class Address {
        public String street;
        public String city;
        public String state;
        public String country;
        public String postalCode;
    }

    public class IntegrationException extends Exception {}
}
```

### Inbound REST API

Exposing Salesforce as a REST API.

```apex
/**
 * Custom REST API endpoint
 * Endpoint: /services/apexrest/accounts
 */
@RestResource(urlMapping='/accounts/*')
global with sharing class AccountRestService {

    /**
     * GET /services/apexrest/accounts/{id}
     * Returns account by ID
     */
    @HttpGet
    global static AccountWrapper getAccount() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;

        // Extract ID from URL
        String accountId = req.requestURI.substringAfterLast('/');

        if (String.isBlank(accountId)) {
            res.statusCode = 400;
            return new AccountWrapper('Account ID is required', null);
        }

        try {
            Account acc = [
                SELECT Id, Name, Industry, AnnualRevenue, BillingCity, BillingCountry
                FROM Account
                WHERE Id = :accountId
                WITH SECURITY_ENFORCED
            ];

            res.statusCode = 200;
            return new AccountWrapper(null, acc);

        } catch (QueryException e) {
            res.statusCode = 404;
            return new AccountWrapper('Account not found', null);
        }
    }

    /**
     * POST /services/apexrest/accounts
     * Creates new account
     */
    @HttpPost
    global static AccountWrapper createAccount(AccountRequest request) {
        RestResponse res = RestContext.response;

        // Validate request
        if (String.isBlank(request.name)) {
            res.statusCode = 400;
            return new AccountWrapper('Name is required', null);
        }

        try {
            Account acc = new Account(
                Name = request.name,
                Industry = request.industry,
                AnnualRevenue = request.annualRevenue,
                BillingStreet = request.billingStreet,
                BillingCity = request.billingCity,
                BillingState = request.billingState,
                BillingCountry = request.billingCountry,
                BillingPostalCode = request.billingPostalCode
            );

            insert acc;

            res.statusCode = 201;
            return new AccountWrapper(null, acc);

        } catch (DmlException e) {
            res.statusCode = 400;
            return new AccountWrapper(e.getMessage(), null);
        }
    }

    /**
     * PATCH /services/apexrest/accounts/{id}
     * Updates existing account
     */
    @HttpPatch
    global static AccountWrapper updateAccount(AccountRequest request) {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;

        String accountId = req.requestURI.substringAfterLast('/');

        try {
            Account acc = [SELECT Id FROM Account WHERE Id = :accountId];

            if (String.isNotBlank(request.name)) acc.Name = request.name;
            if (String.isNotBlank(request.industry)) acc.Industry = request.industry;
            if (request.annualRevenue != null) acc.AnnualRevenue = request.annualRevenue;

            update acc;

            res.statusCode = 200;
            return new AccountWrapper(null, acc);

        } catch (QueryException e) {
            res.statusCode = 404;
            return new AccountWrapper('Account not found', null);
        }
    }

    /**
     * DELETE /services/apexrest/accounts/{id}
     * Deletes account
     */
    @HttpDelete
    global static AccountWrapper deleteAccount() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;

        String accountId = req.requestURI.substringAfterLast('/');

        try {
            Account acc = [SELECT Id FROM Account WHERE Id = :accountId];
            delete acc;

            res.statusCode = 200;
            return new AccountWrapper('Account deleted', null);

        } catch (QueryException e) {
            res.statusCode = 404;
            return new AccountWrapper('Account not found', null);
        }
    }

    // Wrapper classes
    global class AccountWrapper {
        public String error;
        public Account account;

        public AccountWrapper(String error, Account account) {
            this.error = error;
            this.account = account;
        }
    }

    global class AccountRequest {
        public String name;
        public String industry;
        public Decimal annualRevenue;
        public String billingStreet;
        public String billingCity;
        public String billingState;
        public String billingCountry;
        public String billingPostalCode;
    }
}
```

---

## Platform Events

### Event-Driven Architecture

Platform Events enable loosely-coupled, event-driven integrations.

### Publishing Events

```apex
/**
 * Platform Event: Order_Event__e
 * Fields: Order_Id__c, Customer_Id__c, Status__c, Amount__c, Payload__c
 */
public class OrderEventPublisher {

    /**
     * Publishes order events
     * @param orders List of orders to publish
     * @return List of publish results
     */
    public static List<Database.SaveResult> publishOrderEvents(List<Order> orders) {
        List<Order_Event__e> events = new List<Order_Event__e>();

        for (Order ord : orders) {
            events.add(new Order_Event__e(
                Order_Id__c = ord.Id,
                Customer_Id__c = ord.AccountId,
                Status__c = ord.Status,
                Amount__c = ord.TotalAmount,
                Payload__c = JSON.serialize(new OrderPayload(ord))
            ));
        }

        // Publish events
        List<Database.SaveResult> results = EventBus.publish(events);

        // Check results
        for (Integer i = 0; i < results.size(); i++) {
            if (!results[i].isSuccess()) {
                for (Database.Error err : results[i].getErrors()) {
                    System.debug(LoggingLevel.ERROR,
                        'Error publishing event: ' + err.getMessage());
                }
            }
        }

        return results;
    }

    /**
     * Publishes single event immediately
     */
    public static void publishOrderStatusChange(Id orderId, String newStatus) {
        Order_Event__e event = new Order_Event__e(
            Order_Id__c = orderId,
            Status__c = newStatus
        );

        Database.SaveResult result = EventBus.publish(event);

        if (!result.isSuccess()) {
            throw new EventPublishException('Failed to publish order event');
        }
    }

    private class OrderPayload {
        public String orderId;
        public String orderNumber;
        public String status;
        public Decimal amount;
        public List<OrderItemPayload> items;

        public OrderPayload(Order ord) {
            this.orderId = ord.Id;
            this.orderNumber = ord.OrderNumber;
            this.status = ord.Status;
            this.amount = ord.TotalAmount;
        }
    }

    private class OrderItemPayload {
        public String productId;
        public Integer quantity;
        public Decimal unitPrice;
    }

    public class EventPublishException extends Exception {}
}
```

### Subscribing to Events (Apex Trigger)

```apex
/**
 * Platform Event Trigger
 * Subscribes to Order_Event__e
 */
trigger OrderEventTrigger on Order_Event__e (after insert) {
    OrderEventHandler handler = new OrderEventHandler();
    handler.handleEvents(Trigger.new);
}
```

```apex
/**
 * Platform Event Handler
 */
public class OrderEventHandler {

    public void handleEvents(List<Order_Event__e> events) {
        List<Order_Sync__c> syncs = new List<Order_Sync__c>();
        List<Id> orderIds = new List<Id>();

        for (Order_Event__e event : events) {
            // Track replay ID for debugging
            System.debug('Processing event with replay ID: ' + event.ReplayId);

            orderIds.add(event.Order_Id__c);

            // Create sync record
            syncs.add(new Order_Sync__c(
                Order_Id__c = event.Order_Id__c,
                Status__c = event.Status__c,
                Event_Replay_Id__c = String.valueOf(event.ReplayId),
                Processed_Date__c = DateTime.now()
            ));
        }

        // Process in bulk
        if (!syncs.isEmpty()) {
            insert syncs;
        }

        // Call external system asynchronously
        if (!orderIds.isEmpty() && !System.isBatch() && !System.isFuture()) {
            syncOrdersToExternalSystem(orderIds);
        }
    }

    @future(callout=true)
    private static void syncOrdersToExternalSystem(List<Id> orderIds) {
        // Callout to external system
    }
}
```

### Subscribing via CometD (External Systems)

```javascript
// Node.js CometD client for Platform Events
const cometd = require('cometd');
const jsforce = require('jsforce');

async function subscribeToEvents() {
    const conn = new jsforce.Connection({
        loginUrl: process.env.SF_LOGIN_URL
    });

    await conn.login(process.env.SF_USERNAME, process.env.SF_PASSWORD);

    const client = new cometd.CometD();

    client.configure({
        url: conn.instanceUrl + '/cometd/58.0',
        requestHeaders: {
            Authorization: 'Bearer ' + conn.accessToken
        }
    });

    client.handshake((status) => {
        if (status.successful) {
            // Subscribe to platform event channel
            client.subscribe('/event/Order_Event__e', (message) => {
                console.log('Received event:', message.data.payload);

                const orderId = message.data.payload.Order_Id__c;
                const status = message.data.payload.Status__c;

                // Process event
                processOrderEvent(orderId, status);
            });
        }
    });
}
```

---

## Change Data Capture

### Subscribing to Change Events

```apex
/**
 * Change Data Capture Trigger for Account changes
 * Object must have CDC enabled in Setup
 */
trigger AccountChangeEventTrigger on AccountChangeEvent (after insert) {
    AccountChangeEventHandler handler = new AccountChangeEventHandler();
    handler.handleChanges(Trigger.new);
}
```

```apex
/**
 * Change Data Capture Handler
 */
public class AccountChangeEventHandler {

    public void handleChanges(List<AccountChangeEvent> changes) {
        List<Account_Audit__c> auditRecords = new List<Account_Audit__c>();

        for (AccountChangeEvent event : changes) {
            EventBus.ChangeEventHeader header = event.ChangeEventHeader;

            String changeType = header.getChangeType();
            List<String> changedFields = header.getChangedFields();
            String recordIds = String.join(header.getRecordIds(), ',');

            System.debug('Change Type: ' + changeType);
            System.debug('Changed Fields: ' + changedFields);
            System.debug('Record IDs: ' + recordIds);

            // Create audit record
            auditRecords.add(new Account_Audit__c(
                Account_Ids__c = recordIds,
                Change_Type__c = changeType,
                Changed_Fields__c = String.join(changedFields, ', '),
                Change_User__c = header.getCommitUser(),
                Change_Timestamp__c = header.getCommitTimestamp()
            ));

            // Handle specific change types
            if (changeType == 'CREATE') {
                handleCreate(event, header.getRecordIds());
            } else if (changeType == 'UPDATE') {
                handleUpdate(event, changedFields);
            } else if (changeType == 'DELETE') {
                handleDelete(header.getRecordIds());
            }
        }

        if (!auditRecords.isEmpty()) {
            insert auditRecords;
        }
    }

    private void handleCreate(AccountChangeEvent event, List<String> recordIds) {
        // New account created - trigger onboarding workflow
        System.debug('New accounts created: ' + recordIds);
    }

    private void handleUpdate(AccountChangeEvent event, List<String> changedFields) {
        // Check for specific field changes
        if (changedFields.contains('OwnerId')) {
            System.debug('Account ownership changed');
            // Notify new owner
        }

        if (changedFields.contains('Rating')) {
            System.debug('Account rating changed to: ' + event.Rating);
            // Update related records
        }
    }

    private void handleDelete(List<String> recordIds) {
        System.debug('Accounts deleted: ' + recordIds);
        // Clean up related external systems
    }
}
```

---

## External Services

### Using External Services

External Services auto-generate Apex classes from OpenAPI specifications.

```apex
/**
 * Using auto-generated External Service class
 * External Service name: PaymentGateway
 */
public class PaymentService {

    public static PaymentResult processPayment(
        String orderId,
        Decimal amount,
        String currency_x
    ) {
        // Get External Service instance
        ExternalService.PaymentGateway service = new ExternalService.PaymentGateway();

        // Build request using generated request class
        ExternalService.PaymentGateway_PaymentRequest request =
            new ExternalService.PaymentGateway_PaymentRequest();
        request.orderId = orderId;
        request.amount = amount;
        request.currency_x = currency_x;

        try {
            // Call external service
            ExternalService.PaymentGateway_PaymentResponse response =
                service.processPayment(request);

            return new PaymentResult(
                response.transactionId,
                response.status,
                null
            );

        } catch (ExternalService.PaymentGateway_Exception e) {
            return new PaymentResult(null, 'FAILED', e.getMessage());
        }
    }

    public class PaymentResult {
        public String transactionId;
        public String status;
        public String errorMessage;

        public PaymentResult(String txnId, String status, String error) {
            this.transactionId = txnId;
            this.status = status;
            this.errorMessage = error;
        }
    }
}
```

---

## Async Integration Patterns

### Queueable for Callouts

```apex
/**
 * Queueable class for async callouts
 * Supports chaining for multi-step integrations
 */
public class OrderSyncQueueable implements Queueable, Database.AllowsCallouts {

    private List<Id> orderIds;
    private Integer batchNumber;
    private static final Integer BATCH_SIZE = 50;

    public OrderSyncQueueable(List<Id> orderIds) {
        this(orderIds, 0);
    }

    public OrderSyncQueueable(List<Id> orderIds, Integer batchNumber) {
        this.orderIds = orderIds;
        this.batchNumber = batchNumber;
    }

    public void execute(QueueableContext context) {
        // Get batch to process
        Integer startIndex = batchNumber * BATCH_SIZE;
        Integer endIndex = Math.min(startIndex + BATCH_SIZE, orderIds.size());

        List<Id> batchIds = new List<Id>();
        for (Integer i = startIndex; i < endIndex; i++) {
            batchIds.add(orderIds[i]);
        }

        // Process batch
        List<Order> orders = [
            SELECT Id, OrderNumber, Status, TotalAmount, Account.Name
            FROM Order
            WHERE Id IN :batchIds
        ];

        // Sync to external system
        HttpResponse response = syncOrders(orders);

        if (response.getStatusCode() == 200) {
            // Update sync status
            List<Order> toUpdate = new List<Order>();
            for (Order ord : orders) {
                toUpdate.add(new Order(
                    Id = ord.Id,
                    External_Sync_Status__c = 'Synced',
                    External_Sync_Date__c = DateTime.now()
                ));
            }
            update toUpdate;
        }

        // Chain next batch if more records
        if (endIndex < orderIds.size() && !Test.isRunningTest()) {
            System.enqueueJob(new OrderSyncQueueable(orderIds, batchNumber + 1));
        }
    }

    private HttpResponse syncOrders(List<Order> orders) {
        HttpRequest request = new HttpRequest();
        request.setEndpoint('callout:Order_System/api/orders/batch');
        request.setMethod('POST');
        request.setHeader('Content-Type', 'application/json');
        request.setBody(JSON.serialize(orders));

        Http http = new Http();
        return http.send(request);
    }
}
```

### Continuation for Long-Running Callouts

```apex
/**
 * Continuation for async callouts in Visualforce/LWC
 * Avoids timeout issues with long-running external calls
 */
public class LongRunningCalloutController {

    @AuraEnabled
    public static Object startCallout(String accountId) {
        Continuation cont = new Continuation(120); // 120 second timeout
        cont.continuationMethod = 'processResponse';

        HttpRequest request = new HttpRequest();
        request.setEndpoint('callout:Slow_External_API/analyze/' + accountId);
        request.setMethod('GET');

        cont.addHttpRequest(request);

        return cont;
    }

    @AuraEnabled
    public static Object processResponse(List<String> labels, Object state) {
        HttpResponse response = Continuation.getResponse(labels[0]);

        if (response.getStatusCode() == 200) {
            return JSON.deserializeUntyped(response.getBody());
        } else {
            throw new AuraHandledException(
                'Callout failed: ' + response.getStatusCode()
            );
        }
    }
}
```

---

## Error Handling Patterns

### Robust Integration Error Handling

```apex
/**
 * Integration service with comprehensive error handling
 */
public class RobustIntegrationService {

    public static IntegrationResult syncAccount(Id accountId) {
        IntegrationResult result = new IntegrationResult();

        try {
            Account acc = [
                SELECT Id, Name, Industry, AnnualRevenue
                FROM Account
                WHERE Id = :accountId
            ];

            HttpResponse response = callExternalApi(acc);
            result = processResponse(response, acc);

        } catch (QueryException e) {
            result.success = false;
            result.errorCode = 'RECORD_NOT_FOUND';
            result.errorMessage = 'Account not found: ' + accountId;
            logError('QueryException', e.getMessage(), accountId);

        } catch (CalloutException e) {
            result.success = false;
            result.errorCode = 'CALLOUT_FAILED';
            result.errorMessage = 'Unable to reach external system';
            logError('CalloutException', e.getMessage(), accountId);

            // Queue for retry
            queueForRetry(accountId);

        } catch (JSONException e) {
            result.success = false;
            result.errorCode = 'PARSE_ERROR';
            result.errorMessage = 'Invalid response from external system';
            logError('JSONException', e.getMessage(), accountId);

        } catch (Exception e) {
            result.success = false;
            result.errorCode = 'UNKNOWN_ERROR';
            result.errorMessage = e.getMessage();
            logError('Exception', e.getMessage() + '\n' + e.getStackTraceString(), accountId);
        }

        return result;
    }

    private static HttpResponse callExternalApi(Account acc) {
        HttpRequest request = new HttpRequest();
        request.setEndpoint('callout:External_System/accounts');
        request.setMethod('POST');
        request.setHeader('Content-Type', 'application/json');
        request.setBody(JSON.serialize(acc));
        request.setTimeout(30000);

        Http http = new Http();
        return http.send(request);
    }

    private static IntegrationResult processResponse(HttpResponse response, Account acc) {
        IntegrationResult result = new IntegrationResult();

        Integer statusCode = response.getStatusCode();

        if (statusCode >= 200 && statusCode < 300) {
            result.success = true;
            result.externalId = parseExternalId(response.getBody());

            // Update account with external ID
            acc.External_System_Id__c = result.externalId;
            update acc;

        } else if (statusCode == 400) {
            result.success = false;
            result.errorCode = 'VALIDATION_ERROR';
            result.errorMessage = response.getBody();

        } else if (statusCode == 401 || statusCode == 403) {
            result.success = false;
            result.errorCode = 'AUTH_ERROR';
            result.errorMessage = 'Authentication failed';

        } else if (statusCode == 404) {
            result.success = false;
            result.errorCode = 'NOT_FOUND';
            result.errorMessage = 'Endpoint not found';

        } else if (statusCode >= 500) {
            result.success = false;
            result.errorCode = 'SERVER_ERROR';
            result.errorMessage = 'External system error';
            queueForRetry(acc.Id);
        }

        return result;
    }

    private static String parseExternalId(String responseBody) {
        Map<String, Object> body = (Map<String, Object>)JSON.deserializeUntyped(responseBody);
        return (String)body.get('id');
    }

    private static void logError(String errorType, String message, Id recordId) {
        Integration_Log__c log = new Integration_Log__c(
            Error_Type__c = errorType,
            Error_Message__c = message.left(32000),
            Record_Id__c = recordId,
            Timestamp__c = DateTime.now()
        );
        insert log;
    }

    private static void queueForRetry(Id accountId) {
        // Queue for retry with exponential backoff
        Integration_Retry__c retry = new Integration_Retry__c(
            Record_Id__c = accountId,
            Object_Type__c = 'Account',
            Retry_Count__c = 0,
            Next_Retry__c = DateTime.now().addMinutes(5)
        );
        insert retry;
    }

    public class IntegrationResult {
        @AuraEnabled public Boolean success = false;
        @AuraEnabled public String errorCode;
        @AuraEnabled public String errorMessage;
        @AuraEnabled public String externalId;
    }
}
```

---

## When to Use

- **REST callouts**: Real-time sync with external APIs
- **Platform Events**: Event-driven architecture, decoupled integrations
- **Change Data Capture**: Audit trails, external sync on data changes
- **External Services**: OpenAPI-defined integrations with auto-generated code
- **Queueable**: Async callouts needing chaining or complex logic
- **Continuation**: Long-running callouts in UI context

## When NOT to Use

- **Synchronous callouts in triggers**: Use future/queueable instead
- **Callouts during DML operations**: Salesforce prevents mixed DML/callout
- **Platform Events for guaranteed delivery**: Use external queues for critical data
- **Raw HTTP for well-defined APIs**: Use External Services for OpenAPI specs
- **Continuation for batch processing**: Use Batch Apex with Database.AllowsCallouts

---

## Reference: Lightning Web Components

# Lightning Web Components

---

## Component Structure

### Basic LWC Anatomy

Every Lightning Web Component consists of three files:

```
myComponent/
├── myComponent.html     # Template
├── myComponent.js       # JavaScript controller
└── myComponent.js-meta.xml  # Configuration
```

### HTML Template

```html
<!-- accountCard.html -->
<template>
    <lightning-card title={cardTitle} icon-name="standard:account">
        <div class="slds-p-around_medium">
            <!-- Conditional rendering -->
            <template lwc:if={isLoading}>
                <lightning-spinner alternative-text="Loading"></lightning-spinner>
            </template>

            <template lwc:else>
                <!-- Iteration -->
                <template for:each={accounts} for:item="account">
                    <div key={account.Id} class="slds-m-bottom_small">
                        <lightning-tile
                            label={account.Name}
                            href={account.recordUrl}>
                            <p class="slds-truncate">{account.Industry}</p>
                            <p class="slds-text-body_small">
                                Revenue: <lightning-formatted-number
                                    value={account.AnnualRevenue}
                                    format-style="currency"
                                    currency-code="USD">
                                </lightning-formatted-number>
                            </p>
                        </lightning-tile>
                    </div>
                </template>

                <!-- Empty state -->
                <template lwc:if={isEmpty}>
                    <div class="slds-align_absolute-center slds-p-around_large">
                        <p>No accounts found</p>
                    </div>
                </template>
            </template>
        </div>

        <!-- Footer slot -->
        <div slot="footer">
            <lightning-button
                label="Refresh"
                onclick={handleRefresh}
                disabled={isLoading}>
            </lightning-button>
        </div>
    </lightning-card>
</template>
```

### JavaScript Controller

```javascript
// accountCard.js
import { LightningElement, api, wire, track } from 'lwc';
import { NavigationMixin } from 'lightning/navigation';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { refreshApex } from '@salesforce/apex';
import getAccounts from '@salesforce/apex/AccountController.getAccounts';

export default class AccountCard extends NavigationMixin(LightningElement) {

    // Public properties - exposed to parent components
    @api recordId;
    @api maxRecords = 10;

    // Private reactive properties
    accounts = [];
    error;
    isLoading = true;

    // Cached wire result for refresh
    wiredAccountsResult;

    // Computed properties
    get cardTitle() {
        return `Accounts (${this.accounts.length})`;
    }

    get isEmpty() {
        return this.accounts.length === 0;
    }

    // Wire service - reactive data binding
    @wire(getAccounts, { recordId: '$recordId', maxRecords: '$maxRecords' })
    wiredAccounts(result) {
        this.wiredAccountsResult = result;
        const { data, error } = result;

        if (data) {
            this.accounts = data.map(account => ({
                ...account,
                recordUrl: `/lightning/r/Account/${account.Id}/view`
            }));
            this.error = undefined;
        } else if (error) {
            this.error = error;
            this.accounts = [];
            this.showError('Error loading accounts', this.reduceErrors(error));
        }

        this.isLoading = false;
    }

    // Lifecycle hooks
    connectedCallback() {
        console.log('Component connected, recordId:', this.recordId);
    }

    disconnectedCallback() {
        console.log('Component disconnected');
    }

    renderedCallback() {
        // Called after every render
    }

    errorCallback(error, stack) {
        console.error('Component error:', error, stack);
    }

    // Event handlers
    handleRefresh() {
        this.isLoading = true;
        refreshApex(this.wiredAccountsResult)
            .finally(() => {
                this.isLoading = false;
            });
    }

    // Helper methods
    showError(title, message) {
        this.dispatchEvent(new ShowToastEvent({
            title,
            message,
            variant: 'error'
        }));
    }

    reduceErrors(errors) {
        if (!Array.isArray(errors)) {
            errors = [errors];
        }

        return errors
            .filter(error => !!error)
            .map(error => {
                if (typeof error === 'string') {
                    return error;
                }
                if (error.body?.message) {
                    return error.body.message;
                }
                if (error.message) {
                    return error.message;
                }
                return JSON.stringify(error);
            })
            .join(', ');
    }
}
```

### Meta Configuration

```xml
<!-- accountCard.js-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>59.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>Account Card</masterLabel>
    <description>Displays account information in a card format</description>

    <targets>
        <target>lightning__RecordPage</target>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
        <target>lightningCommunity__Page</target>
    </targets>

    <targetConfigs>
        <targetConfig targets="lightning__RecordPage">
            <objects>
                <object>Account</object>
                <object>Contact</object>
            </objects>
            <property name="maxRecords" type="Integer" default="10"
                      label="Maximum Records" description="Max accounts to display" />
        </targetConfig>
        <targetConfig targets="lightning__AppPage,lightning__HomePage">
            <property name="maxRecords" type="Integer" default="10"
                      label="Maximum Records" />
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

---

## Wire Service Patterns

### Wire with Apex Methods

```javascript
// Apex Controller
public with sharing class AccountController {

    @AuraEnabled(cacheable=true)
    public static List<Account> getAccounts(Id recordId, Integer maxRecords) {
        return [
            SELECT Id, Name, Industry, AnnualRevenue
            FROM Account
            WHERE Id != :recordId
            ORDER BY AnnualRevenue DESC NULLS LAST
            LIMIT :maxRecords
        ];
    }

    @AuraEnabled
    public static Account updateAccount(Id accountId, Map<String, Object> fields) {
        Account acc = new Account(Id = accountId);
        for (String fieldName : fields.keySet()) {
            acc.put(fieldName, fields.get(fieldName));
        }
        update acc;
        return acc;
    }
}
```

```javascript
// LWC using wire service
import { LightningElement, wire } from 'lwc';
import { getRecord, getFieldValue, updateRecord } from 'lightning/uiRecordApi';
import ACCOUNT_NAME from '@salesforce/schema/Account.Name';
import ACCOUNT_INDUSTRY from '@salesforce/schema/Account.Industry';
import ACCOUNT_REVENUE from '@salesforce/schema/Account.AnnualRevenue';

const FIELDS = [ACCOUNT_NAME, ACCOUNT_INDUSTRY, ACCOUNT_REVENUE];

export default class AccountDetail extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    account;

    get accountName() {
        return getFieldValue(this.account.data, ACCOUNT_NAME);
    }

    get industry() {
        return getFieldValue(this.account.data, ACCOUNT_INDUSTRY);
    }

    async handleUpdate() {
        const fields = {};
        fields.Id = this.recordId;
        fields[ACCOUNT_INDUSTRY.fieldApiName] = 'Technology';

        try {
            await updateRecord({ fields });
            this.dispatchEvent(new ShowToastEvent({
                title: 'Success',
                message: 'Account updated',
                variant: 'success'
            }));
        } catch (error) {
            this.dispatchEvent(new ShowToastEvent({
                title: 'Error',
                message: error.body.message,
                variant: 'error'
            }));
        }
    }
}
```

### Imperative Apex Calls

Use when you need control over when data is fetched.

```javascript
import { LightningElement, api } from 'lwc';
import searchAccounts from '@salesforce/apex/AccountController.searchAccounts';

export default class AccountSearch extends LightningElement {
    searchTerm = '';
    accounts = [];
    isSearching = false;

    handleSearchChange(event) {
        this.searchTerm = event.target.value;
    }

    async handleSearch() {
        if (this.searchTerm.length < 2) {
            return;
        }

        this.isSearching = true;

        try {
            this.accounts = await searchAccounts({ searchTerm: this.searchTerm });
        } catch (error) {
            console.error('Search error:', error);
            this.accounts = [];
        } finally {
            this.isSearching = false;
        }
    }

    // Debounced search for better UX
    debounceTimeout;
    handleSearchInput(event) {
        clearTimeout(this.debounceTimeout);
        this.searchTerm = event.target.value;

        this.debounceTimeout = setTimeout(() => {
            this.handleSearch();
        }, 300);
    }
}
```

---

## Component Communication

### Parent to Child (Public Properties)

```javascript
// Parent component
// parent.html
<template>
    <c-child-component
        account-id={selectedAccountId}
        display-mode="compact"
        onselect={handleChildSelect}>
    </c-child-component>
</template>
```

```javascript
// Child component
// childComponent.js
import { LightningElement, api } from 'lwc';

export default class ChildComponent extends LightningElement {
    @api accountId;
    @api displayMode = 'full'; // Default value

    // Public method callable by parent
    @api
    refresh() {
        // Refresh logic
    }

    @api
    validate() {
        const input = this.template.querySelector('lightning-input');
        return input.reportValidity();
    }
}
```

### Child to Parent (Custom Events)

```javascript
// Child component dispatching event
export default class ChildComponent extends LightningElement {

    handleAccountSelect(event) {
        const accountId = event.target.dataset.id;

        // Simple event
        this.dispatchEvent(new CustomEvent('select', {
            detail: { accountId }
        }));

        // Bubbling event (crosses shadow DOM)
        this.dispatchEvent(new CustomEvent('accountselected', {
            detail: { accountId, accountName: this.accountName },
            bubbles: true,
            composed: true
        }));
    }
}
```

```javascript
// Parent component handling event
// parent.html
<template>
    <c-child-component onselect={handleSelect}></c-child-component>
</template>

// parent.js
handleSelect(event) {
    const { accountId } = event.detail;
    console.log('Selected account:', accountId);
}
```

### Sibling Communication (Lightning Message Service)

```javascript
// messageChannel/AccountSelected.messageChannel-meta.xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningMessageChannel xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>Account Selected</masterLabel>
    <isExposed>true</isExposed>
    <description>Channel for account selection events</description>
    <lightningMessageFields>
        <fieldName>accountId</fieldName>
        <description>Selected Account ID</description>
    </lightningMessageFields>
    <lightningMessageFields>
        <fieldName>source</fieldName>
        <description>Component that sent message</description>
    </lightningMessageFields>
</LightningMessageChannel>
```

```javascript
// Publisher component
import { LightningElement, wire } from 'lwc';
import { publish, MessageContext } from 'lightning/messageService';
import ACCOUNT_SELECTED from '@salesforce/messageChannel/AccountSelected__c';

export default class AccountPublisher extends LightningElement {
    @wire(MessageContext)
    messageContext;

    handleAccountClick(event) {
        const accountId = event.target.dataset.id;

        const payload = {
            accountId: accountId,
            source: 'AccountPublisher'
        };

        publish(this.messageContext, ACCOUNT_SELECTED, payload);
    }
}
```

```javascript
// Subscriber component
import { LightningElement, wire } from 'lwc';
import { subscribe, unsubscribe, MessageContext } from 'lightning/messageService';
import ACCOUNT_SELECTED from '@salesforce/messageChannel/AccountSelected__c';

export default class AccountSubscriber extends LightningElement {
    subscription = null;
    selectedAccountId;

    @wire(MessageContext)
    messageContext;

    connectedCallback() {
        this.subscribeToMessageChannel();
    }

    disconnectedCallback() {
        this.unsubscribeFromMessageChannel();
    }

    subscribeToMessageChannel() {
        if (!this.subscription) {
            this.subscription = subscribe(
                this.messageContext,
                ACCOUNT_SELECTED,
                (message) => this.handleMessage(message)
            );
        }
    }

    unsubscribeFromMessageChannel() {
        unsubscribe(this.subscription);
        this.subscription = null;
    }

    handleMessage(message) {
        this.selectedAccountId = message.accountId;
        console.log('Received from:', message.source);
    }
}
```

---

## Form Handling

### Lightning Record Edit Form

```html
<template>
    <lightning-record-edit-form
        record-id={recordId}
        object-api-name="Account"
        onsuccess={handleSuccess}
        onerror={handleError}
        onsubmit={handleSubmit}>

        <lightning-messages></lightning-messages>

        <lightning-input-field field-name="Name"></lightning-input-field>
        <lightning-input-field field-name="Industry"></lightning-input-field>
        <lightning-input-field field-name="AnnualRevenue"></lightning-input-field>

        <div class="slds-m-top_medium">
            <lightning-button
                type="submit"
                variant="brand"
                label="Save">
            </lightning-button>
        </div>
    </lightning-record-edit-form>
</template>
```

```javascript
import { LightningElement, api } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class AccountForm extends LightningElement {
    @api recordId;

    handleSubmit(event) {
        event.preventDefault();
        const fields = event.detail.fields;

        // Modify fields before submission
        fields.Description = `Updated on ${new Date().toISOString()}`;

        this.template.querySelector('lightning-record-edit-form').submit(fields);
    }

    handleSuccess(event) {
        const updatedRecord = event.detail.id;
        this.dispatchEvent(new ShowToastEvent({
            title: 'Success',
            message: 'Account saved successfully',
            variant: 'success'
        }));
    }

    handleError(event) {
        console.error('Form error:', event.detail);
    }
}
```

### Custom Form Validation

```html
<template>
    <lightning-card title="Custom Form">
        <div class="slds-p-around_medium">
            <lightning-input
                label="Account Name"
                value={accountName}
                onchange={handleNameChange}
                required
                class="validate">
            </lightning-input>

            <lightning-combobox
                label="Industry"
                value={industry}
                options={industryOptions}
                onchange={handleIndustryChange}
                required
                class="validate">
            </lightning-combobox>

            <lightning-input
                type="number"
                label="Annual Revenue"
                value={revenue}
                onchange={handleRevenueChange}
                min="0"
                formatter="currency"
                class="validate">
            </lightning-input>

            <div class="slds-m-top_medium">
                <lightning-button
                    label="Save"
                    variant="brand"
                    onclick={handleSave}>
                </lightning-button>
            </div>
        </div>
    </lightning-card>
</template>
```

```javascript
import { LightningElement } from 'lwc';
import createAccount from '@salesforce/apex/AccountController.createAccount';

export default class CustomAccountForm extends LightningElement {
    accountName = '';
    industry = '';
    revenue = 0;

    industryOptions = [
        { label: 'Technology', value: 'Technology' },
        { label: 'Healthcare', value: 'Healthcare' },
        { label: 'Finance', value: 'Finance' },
        { label: 'Manufacturing', value: 'Manufacturing' }
    ];

    handleNameChange(event) {
        this.accountName = event.target.value;
    }

    handleIndustryChange(event) {
        this.industry = event.detail.value;
    }

    handleRevenueChange(event) {
        this.revenue = event.target.value;
    }

    validateForm() {
        const inputs = [...this.template.querySelectorAll('.validate')];
        const isValid = inputs.reduce((valid, input) => {
            input.reportValidity();
            return valid && input.checkValidity();
        }, true);

        return isValid;
    }

    async handleSave() {
        if (!this.validateForm()) {
            return;
        }

        try {
            const account = await createAccount({
                name: this.accountName,
                industry: this.industry,
                revenue: this.revenue
            });

            this.dispatchEvent(new ShowToastEvent({
                title: 'Success',
                message: `Account ${account.Name} created`,
                variant: 'success'
            }));

            this.resetForm();
        } catch (error) {
            this.dispatchEvent(new ShowToastEvent({
                title: 'Error',
                message: error.body.message,
                variant: 'error'
            }));
        }
    }

    resetForm() {
        this.accountName = '';
        this.industry = '';
        this.revenue = 0;
    }
}
```

---

## Data Tables

### Lightning Datatable

```html
<template>
    <lightning-card title="Accounts">
        <lightning-datatable
            key-field="Id"
            data={accounts}
            columns={columns}
            sorted-by={sortedBy}
            sorted-direction={sortedDirection}
            onsort={handleSort}
            onrowaction={handleRowAction}
            show-row-number-column
            hide-checkbox-column={hideCheckbox}
            selected-rows={selectedRows}
            onrowselection={handleRowSelection}
            default-sort-direction="asc"
            enable-infinite-loading
            onloadmore={loadMoreData}>
        </lightning-datatable>
    </lightning-card>
</template>
```

```javascript
import { LightningElement, wire } from 'lwc';
import getAccounts from '@salesforce/apex/AccountController.getAccounts';

const COLUMNS = [
    {
        label: 'Account Name',
        fieldName: 'accountUrl',
        type: 'url',
        typeAttributes: {
            label: { fieldName: 'Name' },
            target: '_blank'
        },
        sortable: true
    },
    { label: 'Industry', fieldName: 'Industry', sortable: true },
    {
        label: 'Annual Revenue',
        fieldName: 'AnnualRevenue',
        type: 'currency',
        sortable: true,
        cellAttributes: { alignment: 'right' }
    },
    {
        label: 'Created Date',
        fieldName: 'CreatedDate',
        type: 'date',
        typeAttributes: {
            year: 'numeric',
            month: 'short',
            day: '2-digit'
        }
    },
    {
        type: 'action',
        typeAttributes: {
            rowActions: [
                { label: 'View', name: 'view' },
                { label: 'Edit', name: 'edit' },
                { label: 'Delete', name: 'delete' }
            ]
        }
    }
];

export default class AccountTable extends LightningElement {
    columns = COLUMNS;
    accounts = [];
    selectedRows = [];
    sortedBy = 'Name';
    sortedDirection = 'asc';
    hideCheckbox = false;

    @wire(getAccounts)
    wiredAccounts({ data, error }) {
        if (data) {
            this.accounts = data.map(account => ({
                ...account,
                accountUrl: `/lightning/r/Account/${account.Id}/view`
            }));
        }
    }

    handleSort(event) {
        const { fieldName, sortDirection } = event.detail;
        this.sortedBy = fieldName;
        this.sortedDirection = sortDirection;

        this.sortData(fieldName, sortDirection);
    }

    sortData(fieldName, direction) {
        const parseValue = (value) => {
            if (typeof value === 'string') return value.toLowerCase();
            return value || '';
        };

        const data = [...this.accounts];
        const reverse = direction === 'asc' ? 1 : -1;

        data.sort((a, b) => {
            const aValue = parseValue(a[fieldName]);
            const bValue = parseValue(b[fieldName]);
            return reverse * ((aValue > bValue) - (bValue > aValue));
        });

        this.accounts = data;
    }

    handleRowAction(event) {
        const action = event.detail.action;
        const row = event.detail.row;

        switch (action.name) {
            case 'view':
                this.navigateToRecord(row.Id);
                break;
            case 'edit':
                this.editRecord(row.Id);
                break;
            case 'delete':
                this.deleteRecord(row.Id);
                break;
        }
    }

    handleRowSelection(event) {
        this.selectedRows = event.detail.selectedRows;
    }

    loadMoreData(event) {
        // Implement infinite scrolling
    }
}
```

---

## Performance Optimization

### Best Practices

```javascript
// 1. Use wire service for cacheable data
@wire(getAccounts, { recordId: '$recordId' })
accounts;

// 2. Avoid unnecessary re-renders
// Bad - creates new array every render
get processedAccounts() {
    return this.accounts.map(a => ({ ...a, processed: true }));
}

// Good - cache computed values
_processedAccounts;
@api
get accounts() {
    return this._accounts;
}
set accounts(value) {
    this._accounts = value;
    this._processedAccounts = value.map(a => ({ ...a, processed: true }));
}
get processedAccounts() {
    return this._processedAccounts;
}

// 3. Debounce frequent operations
handleInput(event) {
    window.clearTimeout(this.delayTimeout);
    const searchKey = event.target.value;
    this.delayTimeout = setTimeout(() => {
        this.searchKey = searchKey;
    }, 300);
}

// 4. Use loading states
isLoading = true;
async loadData() {
    this.isLoading = true;
    try {
        this.data = await getData();
    } finally {
        this.isLoading = false;
    }
}
```

---

## When to Use

- **Wire service**: Read-only data that should be cached
- **Imperative calls**: User-triggered actions, data mutations
- **Custom events**: Parent-child communication
- **Lightning Message Service**: Cross-component communication, sibling components
- **Lightning Data Service**: Single record CRUD operations

## When NOT to Use

- **LWC for simple displays**: Use formula fields or Flow screen components
- **Complex forms**: Consider Screen Flow for admin-configurable forms
- **Heavy computation**: Move to Apex to avoid client-side performance issues
- **Non-reactive data**: Don't use @track for simple primitives (automatic since API v59)

---

## Reference: Soql Sosl

# SOQL and SOSL

---

## SOQL Fundamentals

### Basic Query Structure

```sql
SELECT Id, Name, Industry, AnnualRevenue
FROM Account
WHERE Industry = 'Technology'
AND AnnualRevenue > 1000000
ORDER BY AnnualRevenue DESC NULLS LAST
LIMIT 100
OFFSET 0
```

### Governor Limits

| Limit | Synchronous | Asynchronous |
|-------|-------------|--------------|
| Total SOQL queries | 100 | 200 |
| Total records retrieved | 50,000 | 50,000 |
| Query rows in aggregate | 50,000 | 50,000 |
| SOSL queries | 20 | 20 |

---

## Query Optimization

### Selective Queries

Queries must be selective to avoid full table scans. A query is selective when it uses indexed fields that filter to less than 10% of records (or 333,333 records for large objects).

**Standard Indexed Fields:**
- Id
- Name
- OwnerId
- CreatedDate
- SystemModstamp
- RecordTypeId
- External ID fields
- Lookup/Master-Detail fields

```apex
// GOOD - Uses indexed field (Id)
List<Account> accounts = [
    SELECT Id, Name
    FROM Account
    WHERE Id IN :accountIds
];

// GOOD - Uses indexed field (OwnerId)
List<Account> accounts = [
    SELECT Id, Name
    FROM Account
    WHERE OwnerId = :UserInfo.getUserId()
];

// BAD - Non-indexed field with leading wildcard
List<Account> accounts = [
    SELECT Id, Name
    FROM Account
    WHERE Name LIKE '%Corp'
];

// BETTER - Trailing wildcard is acceptable
List<Account> accounts = [
    SELECT Id, Name
    FROM Account
    WHERE Name LIKE 'Acme%'
];
```

### Bulkification Patterns

```apex
// BAD - SOQL inside loop (will hit governor limits)
for (Contact c : contacts) {
    Account acc = [SELECT Id, Name FROM Account WHERE Id = :c.AccountId];
    // Process account
}

// GOOD - Bulkified query
Set<Id> accountIds = new Set<Id>();
for (Contact c : contacts) {
    accountIds.add(c.AccountId);
}

Map<Id, Account> accountMap = new Map<Id, Account>([
    SELECT Id, Name
    FROM Account
    WHERE Id IN :accountIds
]);

for (Contact c : contacts) {
    Account acc = accountMap.get(c.AccountId);
    // Process account
}
```

### Query Plan Analysis

Use the Query Plan tool in Developer Console to analyze query performance.

```apex
// Check if query is selective
String query = 'SELECT Id FROM Account WHERE Industry = \'Technology\'';

// In Developer Console: Query Editor > Query Plan
// Look for:
// - Cost < 1 (selective)
// - Leading operation type (Index vs TableScan)
// - Cardinality (estimated rows)
```

---

## Relationship Queries

### Parent-to-Child (Subquery)

Query child records from parent object.

```apex
// Query Accounts with their Contacts
List<Account> accounts = [
    SELECT Id, Name,
           (SELECT Id, FirstName, LastName, Email
            FROM Contacts
            WHERE IsActive__c = true
            ORDER BY LastName
            LIMIT 100)
    FROM Account
    WHERE Industry = 'Technology'
];

// Access child records
for (Account acc : accounts) {
    System.debug('Account: ' + acc.Name);
    for (Contact c : acc.Contacts) {
        System.debug('  Contact: ' + c.FirstName + ' ' + c.LastName);
    }
}
```

### Child-to-Parent (Dot Notation)

Query parent fields from child object.

```apex
// Query Contacts with Account information
List<Contact> contacts = [
    SELECT Id, FirstName, LastName,
           Account.Name,
           Account.Industry,
           Account.Owner.Name,
           Account.Parent.Name
    FROM Contact
    WHERE Account.Industry = 'Technology'
];

// Access parent fields
for (Contact c : contacts) {
    System.debug('Contact: ' + c.FirstName + ' ' + c.LastName);
    System.debug('  Account: ' + c.Account.Name);
    System.debug('  Owner: ' + c.Account.Owner.Name);
}
```

### Multi-Level Relationships

```apex
// Up to 5 levels of parent relationships
// Up to 1 level of child relationship per query

// Complex relationship query
List<Contact> contacts = [
    SELECT Id, Name,
           Account.Name,
           Account.Parent.Name,
           Account.Parent.Parent.Name,
           Account.Owner.Profile.Name,
           (SELECT Id, Subject FROM Tasks WHERE IsClosed = false LIMIT 5)
    FROM Contact
    WHERE Account.Industry = 'Technology'
    AND Account.Parent.AnnualRevenue > 1000000
];
```

### Polymorphic Relationships

Handle fields that can reference multiple object types (e.g., WhoId, WhatId).

```apex
// Query Tasks with polymorphic WhoId
List<Task> tasks = [
    SELECT Id, Subject,
           Who.Type,
           Who.Name,
           TYPEOF Who
               WHEN Contact THEN FirstName, LastName, Account.Name
               WHEN Lead THEN FirstName, LastName, Company
           END
    FROM Task
    WHERE CreatedDate = TODAY
];

for (Task t : tasks) {
    if (t.Who instanceof Contact) {
        Contact c = (Contact)t.Who;
        System.debug('Contact: ' + c.FirstName + ' ' + c.LastName);
    } else if (t.Who instanceof Lead) {
        Lead l = (Lead)t.Who;
        System.debug('Lead: ' + l.FirstName + ' ' + l.LastName);
    }
}
```

---

## Aggregate Queries

### COUNT, SUM, AVG, MIN, MAX

```apex
// Simple count
Integer accountCount = [SELECT COUNT() FROM Account WHERE Industry = 'Technology'];

// Aggregate functions with GROUP BY
List<AggregateResult> results = [
    SELECT Industry,
           COUNT(Id) recordCount,
           SUM(AnnualRevenue) totalRevenue,
           AVG(AnnualRevenue) avgRevenue,
           MIN(AnnualRevenue) minRevenue,
           MAX(AnnualRevenue) maxRevenue
    FROM Account
    WHERE AnnualRevenue != null
    GROUP BY Industry
    HAVING COUNT(Id) > 5
    ORDER BY SUM(AnnualRevenue) DESC
];

for (AggregateResult ar : results) {
    String industry = (String)ar.get('Industry');
    Integer count = (Integer)ar.get('recordCount');
    Decimal totalRevenue = (Decimal)ar.get('totalRevenue');

    System.debug(industry + ': ' + count + ' accounts, $' + totalRevenue);
}
```

### GROUP BY with ROLLUP and CUBE

```apex
// GROUP BY ROLLUP - hierarchical subtotals
List<AggregateResult> results = [
    SELECT Industry, Type,
           COUNT(Id) cnt,
           SUM(AnnualRevenue) revenue
    FROM Account
    GROUP BY ROLLUP(Industry, Type)
];

// GROUP BY CUBE - all combinations
List<AggregateResult> results = [
    SELECT Industry, Rating,
           COUNT(Id) cnt
    FROM Account
    GROUP BY CUBE(Industry, Rating)
];
```

### COUNT_DISTINCT

```apex
// Count unique values
List<AggregateResult> results = [
    SELECT COUNT_DISTINCT(Industry) uniqueIndustries,
           COUNT_DISTINCT(OwnerId) uniqueOwners
    FROM Account
];
```

---

## Dynamic SOQL

### Building Queries Dynamically

```apex
public class DynamicQueryBuilder {

    public static List<SObject> search(
        String objectName,
        List<String> fields,
        Map<String, Object> filters,
        String orderBy,
        Integer limitCount
    ) {
        // Build SELECT clause
        String query = 'SELECT ' + String.join(fields, ', ');
        query += ' FROM ' + String.escapeSingleQuotes(objectName);

        // Build WHERE clause
        List<String> conditions = new List<String>();
        for (String field : filters.keySet()) {
            Object value = filters.get(field);

            if (value instanceof String) {
                conditions.add(field + ' = \'' + String.escapeSingleQuotes((String)value) + '\'');
            } else if (value instanceof Set<Id>) {
                conditions.add(field + ' IN :filterIds');
            } else if (value instanceof Date) {
                conditions.add(field + ' = ' + ((Date)value).format());
            } else if (value != null) {
                conditions.add(field + ' = ' + value);
            }
        }

        if (!conditions.isEmpty()) {
            query += ' WHERE ' + String.join(conditions, ' AND ');
        }

        // Add ORDER BY
        if (String.isNotBlank(orderBy)) {
            query += ' ORDER BY ' + String.escapeSingleQuotes(orderBy);
        }

        // Add LIMIT
        if (limitCount != null && limitCount > 0) {
            query += ' LIMIT ' + limitCount;
        }

        System.debug('Dynamic Query: ' + query);

        // Execute query
        return Database.query(query);
    }
}

// Usage
Map<String, Object> filters = new Map<String, Object>{
    'Industry' => 'Technology',
    'AnnualRevenue' => 1000000
};

List<Account> accounts = (List<Account>)DynamicQueryBuilder.search(
    'Account',
    new List<String>{'Id', 'Name', 'Industry'},
    filters,
    'Name ASC',
    100
);
```

### Security with Dynamic SOQL

```apex
public with sharing class SecureDynamicQuery {

    public static List<SObject> queryWithFLS(
        String objectName,
        List<String> fields,
        String whereClause
    ) {
        // Check object accessibility
        Schema.DescribeSObjectResult objDescribe =
            Schema.getGlobalDescribe().get(objectName).getDescribe();

        if (!objDescribe.isAccessible()) {
            throw new SecurityException('No access to object: ' + objectName);
        }

        // Filter to accessible fields only
        Map<String, Schema.SObjectField> fieldMap = objDescribe.fields.getMap();
        List<String> accessibleFields = new List<String>();

        for (String field : fields) {
            Schema.SObjectField fieldToken = fieldMap.get(field);
            if (fieldToken != null && fieldToken.getDescribe().isAccessible()) {
                accessibleFields.add(field);
            }
        }

        if (accessibleFields.isEmpty()) {
            throw new SecurityException('No accessible fields');
        }

        String query = 'SELECT ' + String.join(accessibleFields, ', ');
        query += ' FROM ' + String.escapeSingleQuotes(objectName);

        if (String.isNotBlank(whereClause)) {
            query += ' WHERE ' + whereClause;
        }

        // WITH SECURITY_ENFORCED ensures FLS/CRUD
        query += ' WITH SECURITY_ENFORCED';

        return Database.query(query);
    }
}
```

---

## SOSL (Salesforce Object Search Language)

### Basic SOSL Syntax

```apex
// Search across multiple objects
List<List<SObject>> searchResults = [
    FIND 'Acme*' IN ALL FIELDS
    RETURNING
        Account(Id, Name, Industry WHERE Industry = 'Technology'),
        Contact(Id, FirstName, LastName, Email),
        Opportunity(Id, Name, Amount)
    LIMIT 100
];

List<Account> accounts = (List<Account>)searchResults[0];
List<Contact> contacts = (List<Contact>)searchResults[1];
List<Opportunity> opportunities = (List<Opportunity>)searchResults[2];
```

### Search Scope Options

```apex
// ALL FIELDS - Search all searchable text fields
FIND 'Acme' IN ALL FIELDS

// NAME FIELDS - Search only name fields
FIND 'Acme' IN NAME FIELDS

// EMAIL FIELDS - Search only email fields
FIND 'john@acme.com' IN EMAIL FIELDS

// PHONE FIELDS - Search only phone fields
FIND '555-1234' IN PHONE FIELDS

// SIDEBAR FIELDS - Search fields displayed in sidebar
FIND 'Acme' IN SIDEBAR FIELDS
```

### Search Term Syntax

```apex
// Wildcard search (trailing only for SOSL)
FIND 'Acme*'

// Phrase search (exact match)
FIND '"Acme Corporation"'

// Boolean operators
FIND 'Acme AND Technology'
FIND 'Acme OR Technology'
FIND 'Acme AND NOT Closed'

// Grouping
FIND '(Acme OR Globex) AND Technology'
```

### Dynamic SOSL

```apex
public class GlobalSearch {

    public static Map<String, List<SObject>> search(
        String searchTerm,
        List<String> objectNames
    ) {
        if (String.isBlank(searchTerm) || searchTerm.length() < 2) {
            return new Map<String, List<SObject>>();
        }

        // Sanitize search term
        String sanitized = String.escapeSingleQuotes(searchTerm);

        // Build RETURNING clause
        List<String> returningClauses = new List<String>();
        for (String objName : objectNames) {
            returningClauses.add(objName + '(Id, Name LIMIT 20)');
        }

        String sosl = 'FIND \'' + sanitized + '*\' IN ALL FIELDS RETURNING ' +
                      String.join(returningClauses, ', ') +
                      ' LIMIT 100';

        List<List<SObject>> results = Search.query(sosl);

        // Map results to object names
        Map<String, List<SObject>> resultMap = new Map<String, List<SObject>>();
        for (Integer i = 0; i < objectNames.size(); i++) {
            resultMap.put(objectNames[i], results[i]);
        }

        return resultMap;
    }
}

// Usage
Map<String, List<SObject>> results = GlobalSearch.search(
    'Acme',
    new List<String>{'Account', 'Contact', 'Opportunity'}
);
```

---

## Performance Patterns

### Avoiding Common Anti-Patterns

```apex
// ANTI-PATTERN 1: SOQL in loops
// BAD
for (Contact c : contacts) {
    Account acc = [SELECT Id FROM Account WHERE Id = :c.AccountId];
}

// GOOD
Map<Id, Account> accounts = new Map<Id, Account>([
    SELECT Id FROM Account WHERE Id IN :contactAccountIds
]);

// ANTI-PATTERN 2: Querying all fields
// BAD
List<Account> accounts = [SELECT FIELDS(ALL) FROM Account LIMIT 100];

// GOOD - Query only needed fields
List<Account> accounts = [SELECT Id, Name, Industry FROM Account LIMIT 100];

// ANTI-PATTERN 3: Not using bind variables
// BAD - Risk of SOQL injection
String query = 'SELECT Id FROM Account WHERE Name = \'' + userInput + '\'';

// GOOD - Use bind variables
String accountName = userInput;
List<Account> accounts = [SELECT Id FROM Account WHERE Name = :accountName];

// ANTI-PATTERN 4: Querying without limits on unbounded queries
// BAD
List<Account> allAccounts = [SELECT Id FROM Account];

// GOOD
List<Account> accounts = [SELECT Id FROM Account LIMIT 10000];
```

### Large Data Volume Strategies

```apex
public class LargeDataVolumeQuery {

    // Strategy 1: Query with date ranges
    public static List<Account> getRecentAccounts() {
        return [
            SELECT Id, Name
            FROM Account
            WHERE CreatedDate = LAST_N_DAYS:30
            ORDER BY CreatedDate DESC
            LIMIT 1000
        ];
    }

    // Strategy 2: Use QueryLocator for batch processing
    public Database.QueryLocator getQueryLocator() {
        return Database.getQueryLocator([
            SELECT Id, Name, Industry
            FROM Account
            WHERE Industry = 'Technology'
        ]);
    }

    // Strategy 3: Skinny tables for specific fields
    // (Must be enabled by Salesforce Support for the object)

    // Strategy 4: Custom indexes on frequently queried fields
    // (Request via Salesforce Support)

    // Strategy 5: Archive old records
    // Use Big Objects for historical data
}
```

### Query Locator vs List

```apex
// Use QueryLocator for Batch Apex (up to 50 million records)
public Database.QueryLocator start(Database.BatchableContext bc) {
    return Database.getQueryLocator([
        SELECT Id, Name FROM Account
    ]);
}

// Use List for smaller datasets (up to 50,000 records)
public List<Account> start(Database.BatchableContext bc) {
    return [SELECT Id, Name FROM Account LIMIT 50000];
}
```

---

## Date Functions and Literals

### Date Literals

```apex
// Relative date literals
WHERE CreatedDate = TODAY
WHERE CreatedDate = YESTERDAY
WHERE CreatedDate = TOMORROW
WHERE CreatedDate = LAST_WEEK
WHERE CreatedDate = THIS_WEEK
WHERE CreatedDate = NEXT_WEEK
WHERE CreatedDate = LAST_MONTH
WHERE CreatedDate = THIS_MONTH
WHERE CreatedDate = NEXT_MONTH
WHERE CreatedDate = LAST_90_DAYS
WHERE CreatedDate = NEXT_90_DAYS
WHERE CreatedDate = LAST_N_DAYS:30
WHERE CreatedDate = NEXT_N_DAYS:30
WHERE CreatedDate = THIS_QUARTER
WHERE CreatedDate = LAST_QUARTER
WHERE CreatedDate = NEXT_QUARTER
WHERE CreatedDate = THIS_YEAR
WHERE CreatedDate = LAST_YEAR
WHERE CreatedDate = NEXT_YEAR
WHERE CreatedDate = THIS_FISCAL_QUARTER
WHERE CreatedDate = THIS_FISCAL_YEAR
```

### Date Functions

```apex
// Calendar functions in GROUP BY
SELECT CALENDAR_MONTH(CreatedDate) month, COUNT(Id) cnt
FROM Account
GROUP BY CALENDAR_MONTH(CreatedDate)

SELECT CALENDAR_YEAR(CloseDate) year, SUM(Amount) total
FROM Opportunity
WHERE IsWon = true
GROUP BY CALENDAR_YEAR(CloseDate)

// Fiscal functions
SELECT FISCAL_QUARTER(CloseDate) quarter, SUM(Amount)
FROM Opportunity
GROUP BY FISCAL_QUARTER(CloseDate)

// Week functions
SELECT WEEK_IN_MONTH(CreatedDate) week, COUNT(Id)
FROM Lead
GROUP BY WEEK_IN_MONTH(CreatedDate)

// Hour functions (for DateTime fields)
SELECT HOUR_IN_DAY(CreatedDate) hour, COUNT(Id)
FROM Case
GROUP BY HOUR_IN_DAY(CreatedDate)
```

---

## When to Use

- **SOQL**: Retrieving specific records with known criteria
- **SOSL**: Full-text search across multiple objects
- **Aggregate queries**: Reports, dashboards, summary calculations
- **Dynamic SOQL**: User-configurable queries, generic utilities
- **Relationship queries**: Parent-child data in single query

## When NOT to Use

- **SOQL in loops**: Always bulkify outside loops
- **SELECT ***: Query only needed fields
- **Non-selective queries**: Add indexed field filters
- **SOSL for exact matches**: Use SOQL for precise criteria
- **Aggregate for single records**: Use standard queries for individual records
