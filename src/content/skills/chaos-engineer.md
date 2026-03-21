---
title: "Chaos Engineer"
description: "Designs chaos experiments, creates failure injection frameworks, and facilitates game day exercises for distributed systems — producing runbooks, experiment manifests, rollback procedures, and post-mortem templates. Use when designing chaos experi..."
category: "devops"
source: "community"
author: "Community"
tags: ["chaos", "engineer"]
date: 2026-03-20
---

# Chaos Engineer

## When to Use This Skill

- Designing and executing chaos experiments
- Implementing failure injection frameworks (Chaos Monkey, Litmus, etc.)
- Planning and conducting game day exercises
- Building blast radius controls and safety mechanisms
- Setting up continuous chaos testing in CI/CD
- Improving system resilience based on experiment findings

## Core Workflow

1. **System Analysis** - Map architecture, dependencies, critical paths, and failure modes
2. **Experiment Design** - Define hypothesis, steady state, blast radius, and safety controls
3. **Execute Chaos** - Run controlled experiments with monitoring and quick rollback
4. **Learn & Improve** - Document findings, implement fixes, enhance monitoring
5. **Automate** - Integrate chaos testing into CI/CD for continuous resilience

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Experiments | `references/experiment-design.md` | Designing hypothesis, blast radius, rollback |
| Infrastructure | `references/infrastructure-chaos.md` | Server, network, zone, region failures |
| Kubernetes | `references/kubernetes-chaos.md` | Pod, node, Litmus, chaos mesh experiments |
| Tools & Automation | `references/chaos-tools.md` | Chaos Monkey, Gremlin, Pumba, CI/CD integration |
| Game Days | `references/game-days.md` | Planning, executing, learning from game days |

## Safety Checklist

Non-obvious constraints that must be enforced on every experiment:

- **Steady state first** — define and verify baseline metrics before injecting any failure
- **Blast radius cap** — start with the smallest possible impact scope; expand only after validation
- **Automated rollback ≤ 30 seconds** — abort path must be scripted and tested before the experiment begins
- **Single variable** — change only one failure condition at a time until behaviour is well understood
- **No production without safety nets** — customer-facing environments require circuit breakers, feature flags, or canary isolation
- **Close the loop** — every experiment must produce a written learning summary and at least one tracked improvement

## Output Templates

When implementing chaos engineering, provide:
1. Experiment design document (hypothesis, metrics, blast radius)
2. Implementation code (failure injection scripts/manifests)
3. Monitoring setup and alert configuration
4. Rollback procedures and safety controls
5. Learning summary and improvement recommendations

## Concrete Example: Pod Failure Experiment (Litmus Chaos)

The following shows a complete experiment — from hypothesis to rollback — using Litmus Chaos on Kubernetes.

### Step 1 — Define steady state and apply the experiment

```bash
# Verify baseline: p99 latency < 200ms, error rate < 0.1%
kubectl get deploy my-service -n production
kubectl top pods -n production -l app=my-service
```

### Step 2 — Create and apply a Litmus ChaosEngine manifest

```yaml
# chaos-pod-delete.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: my-service-pod-delete
  namespace: production
spec:
  appinfo:
    appns: production
    applabel: "app=my-service"
    appkind: deployment
  # Limit blast radius: only 1 replica at a time
  engineState: active
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "60"          # seconds
            - name: CHAOS_INTERVAL
              value: "20"          # delete one pod every 20s
            - name: FORCE
              value: "false"
            - name: PODS_AFFECTED_PERC
              value: "33"          # max 33% of replicas affected
```

```bash
# Apply the experiment
kubectl apply -f chaos-pod-delete.yaml

# Watch experiment status
kubectl describe chaosengine my-service-pod-delete -n production
kubectl get chaosresult my-service-pod-delete-pod-delete -n production -w
```

### Step 3 — Monitor during the experiment

```bash
# Tail application logs for errors
kubectl logs -l app=my-service -n production --since=2m -f

# Check ChaosResult verdict when complete
kubectl get chaosresult my-service-pod-delete-pod-delete \
  -n production -o jsonpath='{.status.experimentStatus.verdict}'
```

### Step 4 — Rollback / abort if steady state is violated

```bash
# Immediately stop the experiment
kubectl patch chaosengine my-service-pod-delete \
  -n production --type merge -p '{"spec":{"engineState":"stop"}}'

# Confirm all pods are healthy
kubectl rollout status deployment/my-service -n production
```

## Concrete Example: Network Latency with toxiproxy

```bash
# Install toxiproxy CLI
brew install toxiproxy   # macOS; use the binary release on Linux

# Start toxiproxy server (runs alongside your service)
toxiproxy-server &

# Create a proxy for your downstream dependency
toxiproxy-cli create -l 0.0.0.0:22222 -u downstream-db:5432 db-proxy

# Inject 300ms latency with 10% jitter — blast radius: this proxy only
toxiproxy-cli toxic add db-proxy -t latency -a latency=300 -a jitter=30

# Run your load test / observe metrics here ...

# Remove the toxic to restore normal behaviour
toxiproxy-cli toxic remove db-proxy -n latency_downstream
```

## Concrete Example: Chaos Monkey (Spinnaker / standalone)

```bash
# chaos-monkey-config.yml — restrict to a single ASG
deployment:
  enabled: true
  regionIndependence: false
chaos:
  enabled: true
  meanTimeBetweenKillsInWorkDays: 2
  minTimeBetweenKillsInWorkDays: 1
  grouping: APP           # kill one instance per app, not per cluster
  exceptions:
    - account: production
      region: us-east-1
      detail: "*-canary"  # never kill canary instances

# Apply and trigger a manual kill for testing
chaos-monkey --app my-service --account staging --dry-run false
```

---

## Reference: Chaos Tools

# Chaos Engineering Tools & Automation

## Chaos Monkey (Netflix)

```python
# Chaos Monkey configuration for Spinnaker
{
  "enabled": true,
  "schedule": {
    "enabled": true,
    "frequency": 1,  # Run once per day
    "frequencyUnit": "DAYS",
    "start": "09:00",
    "end": "15:00",
    "timezone": "America/Los_Angeles"
  },
  "grouping": "cluster",
  "regionsAreIndependent": true,
  "exceptions": [
    {
      "type": "Opt-In",
      "account": "production",
      "stack": "*",
      "detail": "*"
    }
  ],
  "minTimeBetweenKillsInWorkDays": 2,
  "maxAppsPerDay": 5,
  "clusters": [
    {
      "app": "myapp",
      "stack": "production",
      "enabled": true,
      "regions": ["us-east-1", "us-west-2"],
      "meanTimeBetweenKillsInWorkDays": 2,
      "minTimeBetweenKillsInWorkDays": 1,
      "maxTerminationsPerDay": 1
    }
  ]
}
```

```bash
#!/bin/bash
# Simpl Chaos Monkey implementation

INSTANCE_COUNT=5
KILL_PERCENTAGE=20

# Get running instances from ASG
INSTANCES=$(aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names my-asg \
  --query 'AutoScalingGroups[0].Instances[?LifecycleState==`InService`].InstanceId' \
  --output text)

# Calculate number to terminate
TOTAL=$(echo "$INSTANCES" | wc -w)
TO_KILL=$(( TOTAL * KILL_PERCENTAGE / 100 ))

if [ $TO_KILL -eq 0 ]; then
  TO_KILL=1
fi

# Randomly select and terminate instances
echo "$INSTANCES" | tr ' ' '\n' | shuf | head -n $TO_KILL | while read instance; do
  echo "Terminating instance: $instance"
  aws ec2 terminate-instances --instance-ids "$instance"
  sleep 30  # Wait between terminations
done
```

## Gremlin Integration

```python
import requests
from typing import Literal

class GremlinClient:
    def __init__(self, api_key: str, team_id: str):
        self.api_key = api_key
        self.team_id = team_id
        self.base_url = "https://api.gremlin.com/v1"
        self.headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }

    def create_cpu_attack(
        self,
        targets: list[str],
        length: int = 60,
        cores: int = 1,
        percent: int = 50
    ):
        """Launch CPU resource attack."""
        payload = {
            "command": {
                "type": "cpu",
                "args": [
                    "-l", str(length),
                    "-c", str(cores),
                    "-p", str(percent)
                ]
            },
            "target": {
                "type": "Exact",
                "exact": targets
            }
        }

        response = requests.post(
            f"{self.base_url}/attacks/new",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def create_network_attack(
        self,
        targets: list[str],
        attack_type: Literal["latency", "packet_loss", "blackhole"],
        length: int = 60,
        **kwargs
    ):
        """Launch network attack."""
        args = ["-l", str(length)]

        if attack_type == "latency":
            # kwargs: delay_ms, jitter_ms
            args.extend(["-m", str(kwargs.get('delay_ms', 100))])
            if 'jitter_ms' in kwargs:
                args.extend(["-j", str(kwargs['jitter_ms'])])

        elif attack_type == "packet_loss":
            # kwargs: percent
            args.extend(["-p", str(kwargs.get('percent', 10))])

        elif attack_type == "blackhole":
            # kwargs: port, protocol
            if 'port' in kwargs:
                args.extend(["--port", str(kwargs['port'])])
            if 'protocol' in kwargs:
                args.extend(["--protocol", kwargs['protocol']])

        payload = {
            "command": {
                "type": attack_type,
                "args": args
            },
            "target": {
                "type": "Exact",
                "exact": targets
            }
        }

        response = requests.post(
            f"{self.base_url}/attacks/new",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def halt_attack(self, attack_id: str):
        """Stop running attack."""
        response = requests.delete(
            f"{self.base_url}/attacks/{attack_id}",
            headers=self.headers
        )
        return response.status_code == 200

    def create_scenario(self, name: str, attacks: list[dict]):
        """Create reusable attack scenario."""
        payload = {
            "name": name,
            "description": f"Chaos scenario: {name}",
            "graph": {
                "nodes": attacks
            }
        }

        response = requests.post(
            f"{self.base_url}/scenarios",
            headers=self.headers,
            json=payload
        )
        return response.json()

# Example usage
gremlin = GremlinClient(api_key="...", team_id="...")

# CPU attack on specific containers
gremlin.create_cpu_attack(
    targets=["container-id-123", "container-id-456"],
    length=300,  # 5 minutes
    cores=2,
    percent=80
)

# Network latency attack
gremlin.create_network_attack(
    targets=["host-abc"],
    attack_type="latency",
    length=180,
    delay_ms=500,
    jitter_ms=100
)
```

## CI/CD Integration

```yaml
# GitHub Actions workflow for chaos testing
name: Chaos Engineering Tests

on:
  schedule:
    - cron: '0 10 * * 1-5'  # Weekdays at 10 AM
  workflow_dispatch:  # Manual trigger

jobs:
  chaos-tests:
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name staging-cluster --region us-east-1

      - name: Install Litmus
        run: |
          kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-v2.14.0.yaml
          kubectl wait --for=condition=Ready pods -l app.kubernetes.io/component=operator --timeout=300s

      - name: Run pod-delete chaos experiment
        run: |
          kubectl apply -f .github/chaos/pod-delete-experiment.yaml
          kubectl wait --for=condition=Complete chaosengine/pod-delete-chaos --timeout=600s

      - name: Verify system recovery
        run: |
          # Check all pods are running
          kubectl wait --for=condition=Ready pods -l app=myapp --timeout=300s

          # Verify no error rate spike
          ERROR_RATE=$(curl -s "http://prometheus/api/v1/query?query=rate(http_requests_total{status=~\"5..\"}[5m])" | jq -r '.data.result[0].value[1]')

          if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
            echo "Error rate too high: $ERROR_RATE"
            exit 1
          fi

      - name: Cleanup chaos resources
        if: always()
        run: |
          kubectl delete chaosengine --all
          kubectl delete chaosexperiments --all

      - name: Report results to Slack
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Chaos test failed in staging",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Chaos engineering test failed. System did not recover properly."
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Jenkins Pipeline

```groovy
// Jenkinsfile for chaos testing
pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging'],
            description: 'Target environment'
        )
        choice(
            name: 'CHAOS_TYPE',
            choices: ['pod-delete', 'network-latency', 'cpu-stress'],
            description: 'Type of chaos experiment'
        )
        string(
            name: 'DURATION',
            defaultValue: '300',
            description: 'Chaos duration in seconds'
        )
    }

    stages {
        stage('Pre-flight Check') {
            steps {
                script {
                    // Verify steady state before chaos
                    def errorRate = sh(
                        script: '''
                            curl -s "http://prometheus/api/v1/query?query=rate(http_requests_total{status=~\\"5..\\"}[5m])" | jq -r '.data.result[0].value[1]'
                        ''',
                        returnStdout: true
                    ).trim()

                    if (errorRate.toFloat() > 0.01) {
                        error("System not in steady state. Error rate: ${errorRate}")
                    }
                }
            }
        }

        stage('Run Chaos Experiment') {
            steps {
                script {
                    def chaosManifest = """
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: jenkins-chaos-${env.BUILD_NUMBER}
  namespace: ${params.ENVIRONMENT}
spec:
  appinfo:
    appns: '${params.ENVIRONMENT}'
    applabel: 'app=myapp'
    appkind: 'deployment'
  chaosServiceAccount: litmus-admin
  experiments:
    - name: ${params.CHAOS_TYPE}
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '${params.DURATION}'
"""

                    writeFile file: 'chaos-manifest.yaml', text: chaosManifest

                    sh '''
                        kubectl apply -f chaos-manifest.yaml
                        kubectl wait --for=condition=Complete chaosengine/jenkins-chaos-${BUILD_NUMBER} --timeout=900s
                    '''
                }
            }
        }

        stage('Verify Recovery') {
            steps {
                sh '''
                    # Wait for system to stabilize
                    sleep 60

                    # Check pod status
                    kubectl get pods -n ${ENVIRONMENT} -l app=myapp

                    # Verify all pods running
                    READY_PODS=$(kubectl get pods -n ${ENVIRONMENT} -l app=myapp -o json | jq '[.items[] | select(.status.phase=="Running")] | length')
                    TOTAL_PODS=$(kubectl get pods -n ${ENVIRONMENT} -l app=myapp -o json | jq '.items | length')

                    if [ "$READY_PODS" -ne "$TOTAL_PODS" ]; then
                        echo "Not all pods recovered: $READY_PODS/$TOTAL_PODS ready"
                        exit 1
                    fi
                '''
            }
        }

        stage('Extract Learnings') {
            steps {
                script {
                    // Get chaos result
                    def chaosResult = sh(
                        script: "kubectl get chaosresult -n ${params.ENVIRONMENT} -o json",
                        returnStdout: true
                    )

                    // Parse and store results
                    writeFile file: "chaos-result-${env.BUILD_NUMBER}.json", text: chaosResult

                    // Archive results
                    archiveArtifacts artifacts: "chaos-result-${env.BUILD_NUMBER}.json"
                }
            }
        }
    }

    post {
        always {
            // Cleanup
            sh '''
                kubectl delete chaosengine jenkins-chaos-${BUILD_NUMBER} -n ${ENVIRONMENT} || true
            '''
        }

        failure {
            // Notify team
            slackSend(
                color: 'danger',
                message: "Chaos test failed: ${params.CHAOS_TYPE} in ${params.ENVIRONMENT}"
            )
        }

        success {
            slackSend(
                color: 'good',
                message: "Chaos test passed: ${params.CHAOS_TYPE} in ${params.ENVIRONMENT}. System recovered successfully."
            )
        }
    }
}
```

## Continuous Chaos Dashboard

```python
# Flask app for chaos monitoring dashboard
from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

class ChaosDashboard:
    def __init__(self, prometheus_url: str):
        self.prometheus = prometheus_url

    def get_experiment_metrics(self, hours: int = 24):
        """Get chaos experiment results from last N hours."""
        end = datetime.now()
        start = end - timedelta(hours=hours)

        query = f'''
            sum by (experiment, verdict) (
                increase(litmuschaos_experiment_verdict[{hours}h])
            )
        '''

        response = requests.get(
            f"{self.prometheus}/api/v1/query",
            params={"query": query}
        )

        return response.json()

    def get_mttr_trend(self):
        """Get MTTR trend over time."""
        query = '''
            avg_over_time(
                avg(
                    time() - timestamp(
                        kube_pod_status_phase{phase="Running"} == 1
                    )
                )[7d:]
            )
        '''

        response = requests.get(
            f"{self.prometheus}/api/v1/query",
            params={"query": query}
        )

        return response.json()

@app.route('/api/chaos-summary')
def chaos_summary():
    dashboard = ChaosDashboard(prometheus_url="http://prometheus:9090")

    return jsonify({
        "experiments": dashboard.get_experiment_metrics(hours=24),
        "mttr_trend": dashboard.get_mttr_trend(),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Quick Reference

| Tool | Use Case | Integration |
|------|----------|-------------|
| Chaos Monkey | Random instance termination | Spinnaker/AWS ASG |
| Gremlin | SaaS chaos platform | API/Web UI |
| Litmus | Kubernetes chaos | Kubectl/Helm |
| Chaos Mesh | Advanced K8s chaos | CRDs/Dashboard |
| Toxiproxy | Network proxy chaos | Docker/API |
| Pumba | Container chaos | Docker CLI |

---

## Reference: Experiment Design

# Chaos Experiment Design

## Experiment Template

```yaml
name: "Database Connection Pool Exhaustion"
hypothesis: "When the database connection pool is exhausted, the application will gracefully degrade and return 503 errors without cascading failures"

steady_state:
  metrics:
    - name: "Error Rate"
      threshold: "< 0.1%"
      source: "prometheus"
      query: "rate(http_requests_total{status=~'5..'}[5m])"
    - name: "Latency P99"
      threshold: "< 500ms"
      source: "datadog"
    - name: "Active Connections"
      threshold: "> 10"
      query: "pg_stat_activity_count"

blast_radius:
  environment: "staging"
  traffic_percentage: 10
  duration_seconds: 300
  max_error_rate: "5%"
  auto_rollback: true

injection:
  type: "resource_exhaustion"
  target: "database_connections"
  method: "connection_leak"
  parameters:
    leak_rate: 5  # connections per second
    max_leaked: 50

safety:
  rollback_triggers:
    - "error_rate > 5%"
    - "manual_kill_switch"
    - "duration_exceeded"
  rollback_time_limit_seconds: 30
  alerts:
    - slack: "#chaos-engineering"
    - pagerduty: "chaos-team"

success_criteria:
  - "Circuit breakers activate within 10s"
  - "503 errors returned (not 500)"
  - "No cascading failures to other services"
  - "System recovers within 60s of rollback"
```

## Hypothesis Formulation

```python
def create_hypothesis(component: str, failure: str, expected_behavior: str) -> dict:
    """
    Create well-formed chaos hypothesis.

    Format: "Given [normal state], when [failure occurs],
             then [expected behavior], measured by [metrics]"
    """
    return {
        "given": f"System is in steady state with {component} functioning normally",
        "when": f"{failure} occurs",
        "then": expected_behavior,
        "measured_by": [
            "Error rate remains below threshold",
            "Latency stays within SLO",
            "No data loss or corruption",
            "Recovery time within RTO"
        ]
    }

# Example
hypothesis = create_hypothesis(
    component="payment service",
    failure="50% packet loss to payment gateway",
    expected_behavior="Requests timeout gracefully, retry queue activates, "
                     "users see clear error messages"
)
```

## Blast Radius Control

```python
from dataclasses import dataclass
from enum import Enum

class BlastRadiusLevel(Enum):
    MINIMAL = "single_instance_dev"
    LOW = "single_instance_staging"
    MEDIUM = "percentage_staging"
    HIGH = "percentage_production"
    CRITICAL = "full_production"

@dataclass
class BlastRadiusConfig:
    level: BlastRadiusLevel
    environment: str
    target_percentage: float  # 0-100
    canary_users: list[str]
    feature_flag: str
    auto_rollback: bool
    max_duration_seconds: int

    def validate(self):
        """Enforce safety rules."""
        if self.level == BlastRadiusLevel.CRITICAL:
            raise ValueError("CRITICAL blast radius requires explicit approval")

        if self.environment == "production" and self.target_percentage > 10:
            if not self.feature_flag or not self.auto_rollback:
                raise ValueError("Production >10% requires feature flag AND auto-rollback")

        if self.max_duration_seconds > 600:
            raise ValueError("Max duration cannot exceed 10 minutes without approval")

# Progressive blast radius expansion
def progressive_rollout() -> list[BlastRadiusConfig]:
    return [
        BlastRadiusConfig(
            level=BlastRadiusLevel.MINIMAL,
            environment="dev",
            target_percentage=100,
            canary_users=[],
            feature_flag="chaos_dev",
            auto_rollback=True,
            max_duration_seconds=300
        ),
        BlastRadiusConfig(
            level=BlastRadiusLevel.LOW,
            environment="staging",
            target_percentage=100,
            canary_users=[],
            feature_flag="chaos_staging",
            auto_rollback=True,
            max_duration_seconds=600
        ),
        BlastRadiusConfig(
            level=BlastRadiusLevel.MEDIUM,
            environment="production",
            target_percentage=1,
            canary_users=["internal_team"],
            feature_flag="chaos_prod_canary",
            auto_rollback=True,
            max_duration_seconds=300
        )
    ]
```

## Safety Mechanisms

```python
import asyncio
from typing import Callable

class ChaosExperimentSafety:
    def __init__(self, config: dict):
        self.config = config
        self.kill_switch_active = False
        self.metrics = {}

    async def run_with_safety(self, chaos_fn: Callable):
        """Execute chaos with automatic safety checks."""
        # Pre-flight checks
        if not await self.verify_steady_state():
            raise Exception("System not in steady state - aborting")

        # Set up rollback trigger
        rollback_task = asyncio.create_task(self.monitor_for_rollback())
        chaos_task = asyncio.create_task(chaos_fn())

        try:
            # Wait for either chaos completion or rollback trigger
            done, pending = await asyncio.wait(
                [chaos_task, rollback_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            if rollback_task in done:
                # Rollback triggered - cancel chaos
                chaos_task.cancel()
                await self.rollback()

        finally:
            await self.ensure_system_recovery()

    async def verify_steady_state(self) -> bool:
        """Check all steady state metrics are within threshold."""
        for metric in self.config['steady_state']['metrics']:
            value = await self.query_metric(metric['query'])
            if not self.within_threshold(value, metric['threshold']):
                return False
        return True

    async def monitor_for_rollback(self):
        """Continuously monitor for rollback triggers."""
        start_time = asyncio.get_event_loop().time()

        while True:
            # Check duration limit
            if asyncio.get_event_loop().time() - start_time > \
               self.config['blast_radius']['duration_seconds']:
                return "duration_exceeded"

            # Check manual kill switch
            if self.kill_switch_active:
                return "manual_kill_switch"

            # Check error rate
            error_rate = await self.query_metric("error_rate")
            if error_rate > float(self.config['blast_radius']['max_error_rate'].strip('%')):
                return "error_rate_exceeded"

            await asyncio.sleep(5)  # Check every 5 seconds
```

## Quick Reference

| Phase | Key Actions | Time Limit |
|-------|-------------|------------|
| Design | Hypothesis, metrics, blast radius | 1 hour |
| Review | Team review, safety check | 30 min |
| Prepare | Setup monitoring, rollback | 1 hour |
| Execute | Run experiment, monitor | 5-10 min |
| Rollback | Restore steady state | < 30 sec |
| Learn | Document findings, plan fixes | 2 hours |

---

## Reference: Game Days

# Game Day Planning & Execution

## Game Day Planning Template

```yaml
game_day:
  name: "Database Failover Drill"
  date: "2025-01-15"
  time: "10:00-12:00 PST"
  environment: "staging"  # Start in staging

  objectives:
    - "Verify RDS failover to standby in under 2 minutes"
    - "Validate application auto-reconnect logic"
    - "Test monitoring and alerting effectiveness"
    - "Practice incident response procedures"

  participants:
    facilitator: "chaos-engineer@company.com"
    observers:
      - "sre-team@company.com"
      - "dev-team@company.com"
    responders:
      - "on-call-engineer@company.com"
      - "database-admin@company.com"
    stakeholders:
      - "engineering-manager@company.com"

  scenarios:
    - name: "Primary database instance failure"
      duration_minutes: 30
      steps:
        - action: "Force RDS instance reboot with failover"
          expected: "Failover to standby in <2 min"
          success_criteria:
            - "Downtime < 2 minutes"
            - "No data loss"
            - "Alerts fired correctly"

    - name: "Network partition to database"
      duration_minutes: 20
      steps:
        - action: "Block network traffic to RDS security group"
          expected: "Application switches to read replica"
          success_criteria:
            - "Read-only mode activated"
            - "User-facing error messages clear"

  communication_plan:
    announcement_channel: "#game-day-announcements"
    war_room: "Zoom link: https://..."
    status_updates_every: "5 minutes"
    escalation_contacts:
      - name: "VP Engineering"
        phone: "+1-555-0100"
        threshold: "downtime > 5 minutes"

  rollback_plan:
    automatic_rollback_triggers:
      - "production traffic affected"
      - "customer complaints received"
      - "error_rate > 10%"
    manual_rollback_command: "aws rds reboot-db-instance --db-instance-identifier primary --force-failover"
    rollback_time_limit_seconds: 60

  success_metrics:
    - metric: "RTO (Recovery Time Objective)"
      target: "< 2 minutes"
      measurement: "time between failure and full recovery"
    - metric: "Alert accuracy"
      target: "100%"
      measurement: "all expected alerts fired"
    - metric: "Team response time"
      target: "< 5 minutes"
      measurement: "time to acknowledge incident"

  post_mortem:
    scheduled_for: "2025-01-16 14:00"
    template: "game-day-retro.md"
    required_attendees: "all participants"
```

## Game Day Runbook

```markdown
# Database Failover Game Day Runbook

**Date**: January 15, 2025
**Duration**: 2 hours
**Environment**: Staging

## Pre-Game Checklist (T-30 min)

- [ ] Verify all participants joined war room
- [ ] Confirm monitoring dashboards accessible
- [ ] Test rollback procedures work
- [ ] Announce game day start in #engineering
- [ ] Verify staging environment healthy
- [ ] Set up screen recording for timeline
- [ ] Prepare incident timeline spreadsheet

## Timeline

### 10:00 - Introduction (10 min)
- Facilitator explains objectives
- Review scenarios and success criteria
- Confirm roles and communication channels
- Remind everyone: this is a learning exercise

### 10:10 - Scenario 1: Primary DB Failure (30 min)

**T+0 (10:10)** - Inject failure
```bash
aws rds reboot-db-instance \
  --db-instance-identifier staging-primary \
  --force-failover
```

**Expected Timeline**:
- T+0: Reboot initiated
- T+30s: Primary becomes unavailable
- T+60s: DNS updated to standby
- T+90s: Application reconnects
- T+120s: Full recovery

**Observer Tasks**:
- [ ] Record exact time of failure injection
- [ ] Monitor application error logs
- [ ] Track alert notifications
- [ ] Document team response actions
- [ ] Screenshot dashboard states

**Questions to Answer**:
- How long until first alert?
- Did application auto-reconnect?
- Were customers impacted?
- What manual interventions needed?

### 10:40 - Debrief Scenario 1 (10 min)
- What went well?
- What could improve?
- Any surprises?
- Action items identified

### 10:50 - Scenario 2: Network Partition (20 min)

**T+0 (10:50)** - Inject failure
```bash
# Block database security group ingress
aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 5432 \
  --cidr 10.0.0.0/16
```

**Expected Behavior**:
- Connection timeouts occur
- Circuit breaker opens
- Read-only mode activates
- Clear error messages shown

**Observer Tasks**:
- [ ] Monitor circuit breaker state
- [ ] Verify read-replica failover
- [ ] Check user-facing error messages
- [ ] Track degraded service duration

### 11:10 - Debrief Scenario 2 (10 min)

### 11:20 - Scenario 3: Surprise! (20 min)

**Facilitator Note**: Don't announce this scenario details beforehand.
Test true incident response capability.

**Hidden Scenario**: Combination failure
1. Database connection pool leak
2. Simultaneous cache invalidation

```python
# Connection leak simulator
import psycopg2
connections = []
for i in range(100):
    conn = psycopg2.connect(DATABASE_URL)
    connections.append(conn)
    # Intentionally don't close
```

**Observer Tasks**:
- [ ] How long to identify root cause?
- [ ] Communication effectiveness
- [ ] Cross-team coordination
- [ ] Escalation decisions

### 11:40 - Final Debrief & Wrap-up (20 min)

**Debrief Questions**:
1. What worked well?
2. What didn't work?
3. What surprised us?
4. What are our top 3 action items?
5. When should we run this again?

## Post-Game Checklist

- [ ] Restore all services to normal state
- [ ] Verify no lingering issues
- [ ] Collect all observer notes
- [ ] Export metrics and dashboards
- [ ] Schedule post-mortem meeting
- [ ] Send thank-you to participants
- [ ] Create action item tickets
- [ ] Update runbooks based on learnings
```

## Game Day Observation Template

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class GameDayObservation:
    timestamp: datetime
    observer: str
    scenario: str
    observation: str
    category: str  # technical, process, communication, surprise
    severity: str  # info, concern, critical
    photo_url: str = ""

@dataclass
class GameDayMetrics:
    scenario_name: str
    start_time: datetime
    end_time: datetime

    # Technical metrics
    time_to_detect_seconds: float
    time_to_respond_seconds: float
    time_to_recover_seconds: float
    error_rate_peak: float
    alerts_fired: List[str] = field(default_factory=list)
    alerts_missed: List[str] = field(default_factory=list)

    # Team metrics
    responders_involved: int
    escalations_needed: int
    communication_gaps: List[str] = field(default_factory=list)

    # Success criteria
    met_rto: bool = False
    met_rpo: bool = False
    zero_customer_impact: bool = False

    def calculate_mttr(self) -> float:
        """Mean Time To Recovery"""
        return (self.end_time - self.start_time).total_seconds()

    def success_rate(self) -> float:
        """Percentage of success criteria met"""
        criteria = [
            self.met_rto,
            self.met_rpo,
            self.zero_customer_impact,
            len(self.alerts_missed) == 0
        ]
        return sum(criteria) / len(criteria) * 100

# Example usage
metrics = GameDayMetrics(
    scenario_name="Database Failover",
    start_time=datetime(2025, 1, 15, 10, 10, 0),
    end_time=datetime(2025, 1, 15, 10, 12, 30),
    time_to_detect_seconds=15.0,
    time_to_respond_seconds=45.0,
    time_to_recover_seconds=150.0,
    error_rate_peak=0.05,
    alerts_fired=["DatabaseConnectionError", "HighLatency"],
    alerts_missed=["FailoverInitiated"],
    responders_involved=3,
    escalations_needed=0,
    met_rto=True,
    met_rpo=True,
    zero_customer_impact=True
)

print(f"MTTR: {metrics.calculate_mttr()}s")
print(f"Success Rate: {metrics.success_rate()}%")
```

## Surprise Scenarios Library

```yaml
# Keep these secret until game day!
surprise_scenarios:
  - name: "Cascading Failure"
    description: "Primary failure triggers secondary issue"
    injection:
      - "Database failover (expected)"
      - "Cache eviction due to new primary IP (surprise!)"
    learning_goals:
      - "Do we understand our dependencies?"
      - "Can we handle multiple simultaneous issues?"

  - name: "Monitoring Blind Spot"
    description: "Failure that doesn't trigger alerts"
    injection:
      - "Gradual connection pool leak"
      - "No immediate alerts fire"
    learning_goals:
      - "How do we discover issues without alerts?"
      - "Do we have adequate monitoring coverage?"

  - name: "Documentation Failure"
    description: "Runbook is outdated or incorrect"
    setup:
      - "Modify runbook to have incorrect commands"
      - "Or remove runbook entirely"
    learning_goals:
      - "Can team problem-solve without docs?"
      - "How quickly can we update documentation?"

  - name: "Key Person Unavailable"
    description: "Subject matter expert is unreachable"
    setup:
      - "Ask SME to not respond for 15 minutes"
    learning_goals:
      - "Is knowledge properly distributed?"
      - "Can team succeed without specific person?"

  - name: "Partial Degradation"
    description: "Service works but slowly"
    injection:
      - "Add 5 second latency instead of complete failure"
    learning_goals:
      - "Do we detect performance degradation?"
      - "What are our latency SLOs?"
```

## Post-Game Report Template

```markdown
# Game Day Report: Database Failover

**Date**: January 15, 2025
**Participants**: 12
**Duration**: 2 hours
**Environment**: Staging

## Executive Summary

Conducted database failover game day to test RDS high availability and
application resilience. Successfully failed over database in 2.5 minutes
(target: 2 min). Discovered 3 critical gaps in monitoring and 2 process
improvements needed.

## Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Time to Detect | < 30s | 15s | PASS |
| Time to Respond | < 5min | 4min 20s | PASS |
| Time to Recover | < 2min | 2min 30s | FAIL |
| Alert Accuracy | 100% | 66% | FAIL |
| Zero Customer Impact | Yes | Yes | PASS |

## What Went Well

1. Team responded quickly (4m 20s vs 5m target)
2. Runbooks were accurate and helpful
3. Communication was clear and frequent
4. No customer impact during any scenario
5. Application auto-reconnect worked perfectly

## What Didn't Go Well

1. Missing alert for failover initiation
2. Took 30s longer than target to recover
3. Connection pool exhaustion not detected
4. Dashboard didn't show replica lag clearly
5. Escalation contacts list was outdated

## Surprises

1. Cache invalidation cascaded from DB failover (unexpected)
2. Read replica had 45s replication lag we didn't know about
3. Application retried too aggressively during failover
4. Team found a workaround we hadn't documented

## Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| Add alert for RDS failover events | @sre-team | Jan 20 | P0 |
| Update dashboard with replica lag | @platform | Jan 22 | P1 |
| Document cache invalidation behavior | @dev-team | Jan 25 | P1 |
| Add connection pool monitoring | @sre-team | Jan 27 | P0 |
| Update escalation contact list | @manager | Jan 18 | P2 |
| Tune application retry backoff | @dev-team | Feb 1 | P1 |

## Lessons Learned

1. **Monitoring Gaps**: We had blind spots in replica monitoring
2. **Cascading Effects**: DB changes affect cache in non-obvious ways
3. **Team Knowledge**: Cross-training is working well
4. **Documentation**: Runbooks saved time, keep them updated

## Next Game Day

**Proposed Date**: March 15, 2025
**Scenario**: Multi-region failover
**Scope**: Production (with safeguards)

## Appendix

- Full timeline spreadsheet: [link]
- Screen recordings: [link]
- Metrics dashboard export: [link]
- Raw observation notes: [link]
```

## Quick Reference

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| Planning | 2 weeks | Define scenarios, invite participants |
| Pre-game | 30 min | Setup, verify environment, brief team |
| Execution | 2 hours | Run scenarios, observe, document |
| Debrief | 30 min | Immediate learnings, quick wins |
| Post-mortem | 1 week later | Detailed analysis, action items |
| Follow-up | 1 month | Verify improvements, plan next game day |

---

## Reference: Infrastructure Chaos

# Infrastructure Chaos Engineering

## Network Latency Injection

```python
# Using toxiproxy for network chaos
import requests
from typing import Literal

class ToxiproxyClient:
    def __init__(self, host: str = "localhost:8474"):
        self.base_url = f"http://{host}"

    def create_proxy(self, name: str, listen: str, upstream: str):
        """Create proxy to inject failures."""
        response = requests.post(f"{self.base_url}/proxies", json={
            "name": name,
            "listen": listen,
            "upstream": upstream,
            "enabled": True
        })
        return response.json()

    def add_latency(self, proxy: str, latency_ms: int, jitter_ms: int = 0):
        """Add latency toxic."""
        return requests.post(
            f"{self.base_url}/proxies/{proxy}/toxics",
            json={
                "name": "latency",
                "type": "latency",
                "attributes": {
                    "latency": latency_ms,
                    "jitter": jitter_ms
                }
            }
        )

    def add_bandwidth_limit(self, proxy: str, rate_kb: int):
        """Limit bandwidth."""
        return requests.post(
            f"{self.base_url}/proxies/{proxy}/toxics",
            json={
                "name": "bandwidth",
                "type": "bandwidth",
                "attributes": {"rate": rate_kb}
            }
        )

    def add_timeout(self, proxy: str, timeout_ms: int):
        """Add connection timeout."""
        return requests.post(
            f"{self.base_url}/proxies/{proxy}/toxics",
            json={
                "name": "timeout",
                "type": "timeout",
                "attributes": {"timeout": timeout_ms}
            }
        )

# Example usage
toxiproxy = ToxiproxyClient()

# Create proxy to database
toxiproxy.create_proxy(
    name="postgres",
    listen="0.0.0.0:5433",
    upstream="postgres:5432"
)

# Inject 200ms latency with 50ms jitter
toxiproxy.add_latency("postgres", latency_ms=200, jitter_ms=50)
```

## AWS Zone Failure Simulation

```python
import boto3
from datetime import datetime, timedelta

class AWSChaosSimulator:
    def __init__(self, region: str):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.asg = boto3.client('autoscaling', region_name=region)
        self.elb = boto3.client('elbv2', region_name=region)

    def simulate_az_failure(
        self,
        availability_zone: str,
        asg_name: str,
        duration_minutes: int = 10
    ):
        """
        Simulate AZ failure by terminating instances in specific AZ.
        Auto Scaling Group will launch replacements in other AZs.
        """
        # Find instances in target AZ
        instances = self.ec2.describe_instances(Filters=[
            {'Name': 'tag:aws:autoscaling:groupName', 'Values': [asg_name]},
            {'Name': 'availability-zone', 'Values': [availability_zone]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ])

        instance_ids = [
            i['InstanceId']
            for r in instances['Reservations']
            for i in r['Instances']
        ]

        if not instance_ids:
            return {"status": "no_instances", "instances": []}

        # Suspend AZ-specific scaling activities
        self.asg.suspend_processes(
            AutoScalingGroupName=asg_name,
            ScalingProcesses=['AZRebalance']
        )

        # Terminate instances to simulate AZ failure
        self.ec2.terminate_instances(InstanceIds=instance_ids)

        return {
            "status": "simulated",
            "availability_zone": availability_zone,
            "terminated_instances": instance_ids,
            "recovery_time": datetime.now() + timedelta(minutes=duration_minutes)
        }

    def drain_az_from_load_balancer(
        self,
        target_group_arn: str,
        availability_zone: str
    ):
        """Remove AZ from load balancer to simulate zone failure."""
        # Get current target health
        health = self.elb.describe_target_health(
            TargetGroupArn=target_group_arn
        )

        # Find targets in AZ
        targets_to_deregister = []
        for target in health['TargetHealthDescriptions']:
            # Get instance details
            instance = self.ec2.describe_instances(
                InstanceIds=[target['Target']['Id']]
            )
            if instance['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone'] == availability_zone:
                targets_to_deregister.append(target['Target'])

        # Deregister targets
        if targets_to_deregister:
            self.elb.deregister_targets(
                TargetGroupArn=target_group_arn,
                Targets=targets_to_deregister
            )

        return {
            "deregistered_targets": len(targets_to_deregister),
            "availability_zone": availability_zone
        }
```

## Server Resource Exhaustion

```bash
#!/bin/bash
# CPU stress test using stress-ng

# Install stress-ng
sudo apt-get install -y stress-ng

# Stress CPU - use 80% of available cores for 5 minutes
stress-ng --cpu $(nproc --all) --cpu-load 80 --timeout 5m

# Memory stress - consume 70% of available memory
TOTAL_MEM_MB=$(free -m | awk 'NR==2{print $2}')
STRESS_MEM_MB=$((TOTAL_MEM_MB * 70 / 100))
stress-ng --vm 1 --vm-bytes ${STRESS_MEM_MB}M --timeout 5m

# Disk I/O stress - 4 workers doing sequential writes
stress-ng --hdd 4 --hdd-bytes 1G --timeout 5m

# Network bandwidth saturation
# Using iperf3 to saturate network
iperf3 -c target-server -t 300 -P 10  # 10 parallel streams for 5 minutes
```

## Docker Container Chaos with Pumba

```bash
#!/bin/bash
# Pumba - chaos testing for Docker

# Kill random container every 30 seconds
pumba --interval 30s kill --signal SIGKILL "re2:^myapp"

# Pause container for 15 seconds, then resume
pumba pause --duration 15s myapp-container

# Add network delay to container
pumba netem \
  --duration 5m \
  --interface eth0 \
  delay \
    --time 300 \
    --jitter 50 \
  myapp-container

# Packet loss - drop 20% of packets
pumba netem \
  --duration 5m \
  loss \
    --percent 20 \
  myapp-container

# Limit bandwidth to 1Mbps
pumba netem \
  --duration 5m \
  rate \
    --rate 1mbit \
  myapp-container

# Stop all containers matching pattern for 2 minutes
pumba stop --duration 2m "re2:^production-.*"
```

## DNS Failure Simulation

```python
# Using dnsmasq or editing /etc/hosts for DNS chaos

import subprocess
import time
from contextlib import contextmanager

class DNSChaos:
    @staticmethod
    @contextmanager
    def block_domain(domain: str, duration_seconds: int = 60):
        """Block DNS resolution for domain by pointing to localhost."""
        try:
            # Add entry to /etc/hosts
            subprocess.run([
                'sudo', 'sh', '-c',
                f'echo "127.0.0.1 {domain}" >> /etc/hosts'
            ], check=True)

            print(f"Blocked DNS for {domain}")
            yield

        finally:
            # Wait for duration
            time.sleep(duration_seconds)

            # Remove entry from /etc/hosts
            subprocess.run([
                'sudo', 'sed', '-i',
                f'/127.0.0.1 {domain}/d',
                '/etc/hosts'
            ], check=True)

            print(f"Restored DNS for {domain}")

    @staticmethod
    def add_dns_latency(domain: str, latency_ms: int):
        """Add latency to DNS queries using dnsmasq."""
        config = f"""
        # Add to /etc/dnsmasq.conf
        address=/{domain}/127.0.0.1
        min-cache-ttl=0

        # Restart dnsmasq with delay
        """
        return config

# Usage
with DNSChaos.block_domain('api.external-service.com', duration_seconds=120):
    # Run tests while DNS is blocked
    print("DNS blocked - testing fallback behavior")
```

## Certificate Expiry Simulation

```python
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def create_expired_certificate(
    common_name: str,
    expired_days_ago: int = 1
) -> tuple[bytes, bytes]:
    """
    Create an expired TLS certificate for chaos testing.
    Returns (certificate_pem, private_key_pem)
    """
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Certificate valid from 365 days ago to `expired_days_ago` ago
    not_valid_before = datetime.utcnow() - timedelta(days=365)
    not_valid_after = datetime.utcnow() - timedelta(days=expired_days_ago)

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name)
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        not_valid_before
    ).not_valid_after(
        not_valid_after
    ).sign(private_key, hashes.SHA256())

    # Serialize to PEM
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return cert_pem, key_pem
```

## Quick Reference

| Failure Type | Tool | Command/Method |
|--------------|------|----------------|
| Network latency | toxiproxy | `add_latency(proxy, ms)` |
| Packet loss | toxiproxy/pumba | `loss --percent 20` |
| AZ failure | AWS API | `simulate_az_failure(az, asg)` |
| CPU stress | stress-ng | `--cpu N --cpu-load 80` |
| Memory exhaustion | stress-ng | `--vm 1 --vm-bytes XG` |
| Container kill | pumba | `kill --signal SIGKILL` |
| DNS failure | /etc/hosts | Block domain resolution |
| Cert expiry | cryptography | Generate expired cert |

---

## Reference: Kubernetes Chaos

# Kubernetes Chaos Engineering

## Litmus Chaos - ChaosEngine

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  # Application information
  appinfo:
    appns: 'default'
    applabel: 'app=nginx'
    appkind: 'deployment'

  # Chaos service account
  chaosServiceAccount: litmus-admin

  # Experiments to run
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            # Total chaos duration
            - name: TOTAL_CHAOS_DURATION
              value: '60'

            # Chaos interval (delete pod every X seconds)
            - name: CHAOS_INTERVAL
              value: '10'

            # Force delete pods
            - name: FORCE
              value: 'true'

            # Number of pods to delete
            - name: PODS_AFFECTED_PERC
              value: '50'

    - name: pod-network-latency
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'
            - name: NETWORK_LATENCY
              value: '2000'  # 2 second latency
            - name: JITTER
              value: '200'   # 200ms jitter
            - name: CONTAINER_RUNTIME
              value: 'containerd'

    - name: pod-cpu-hog
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'
            - name: CPU_CORES
              value: '2'
            - name: PODS_AFFECTED_PERC
              value: '50'

  # Monitor application during chaos
  monitoring: true

  # Job cleanup policy
  jobCleanUpPolicy: 'delete'
```

## Chaos Mesh Experiments

```yaml
# Network partition between services
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: partition-frontend-backend
  namespace: chaos-testing
spec:
  action: partition
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      'app': 'frontend'
  direction: to
  target:
    mode: all
    selector:
      namespaces:
        - production
      labelSelectors:
        'app': 'backend'
  duration: '5m'

---
# Pod failure - kill random pods
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-failure
  namespace: chaos-testing
spec:
  action: pod-failure
  mode: one  # one, all, fixed, fixed-percent, random-max-percent
  duration: '30s'
  selector:
    namespaces:
      - production
    labelSelectors:
      'app': 'payment-service'
  scheduler:
    cron: '@every 10m'  # Run every 10 minutes

---
# Network bandwidth limitation
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: bandwidth-limit
spec:
  action: bandwidth
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      'tier': 'backend'
  bandwidth:
    rate: '1mbps'
    limit: 20000
    buffer: 10000
  duration: '5m'

---
# Disk I/O stress
apiVersion: chaos-mesh.org/v1alpha1
kind: IOChaos
metadata:
  name: io-latency
spec:
  action: latency
  mode: one
  selector:
    namespaces:
      - production
    labelSelectors:
      'app': 'database'
  volumePath: /var/lib/postgresql/data
  path: /var/lib/postgresql/data/**/*
  delay: '100ms'
  percent: 50  # 50% of I/O operations affected
  duration: '5m'

---
# DNS chaos - random DNS errors
apiVersion: chaos-mesh.org/v1alpha1
kind: DNSChaos
metadata:
  name: dns-random-error
spec:
  action: random
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      'app': 'api-gateway'
  patterns:
    - external-api.example.com
    - *.third-party-service.com
  duration: '3m'
```

## Node Drain Simulation

```python
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time

class K8sNodeChaos:
    def __init__(self):
        config.load_kube_config()
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def cordon_node(self, node_name: str):
        """Mark node as unschedulable."""
        body = {
            "spec": {
                "unschedulable": True
            }
        }
        try:
            self.core_v1.patch_node(node_name, body)
            print(f"Node {node_name} cordoned")
        except ApiException as e:
            print(f"Failed to cordon node: {e}")

    def drain_node(
        self,
        node_name: str,
        grace_period_seconds: int = 30,
        delete_local_data: bool = True
    ):
        """
        Drain node by evicting all pods.
        Simulates node failure or maintenance.
        """
        # First, cordon the node
        self.cordon_node(node_name)

        # Get all pods on the node
        field_selector = f"spec.nodeName={node_name}"
        pods = self.core_v1.list_pod_for_all_namespaces(
            field_selector=field_selector
        )

        # Evict each pod
        for pod in pods.items:
            # Skip DaemonSet pods and mirror pods
            if pod.metadata.owner_references:
                for owner in pod.metadata.owner_references:
                    if owner.kind in ['DaemonSet', 'Node']:
                        continue

            # Create eviction
            eviction = client.V1Eviction(
                metadata=client.V1ObjectMeta(
                    name=pod.metadata.name,
                    namespace=pod.metadata.namespace
                ),
                delete_options=client.V1DeleteOptions(
                    grace_period_seconds=grace_period_seconds
                )
            )

            try:
                self.core_v1.create_namespaced_pod_eviction(
                    name=pod.metadata.name,
                    namespace=pod.metadata.namespace,
                    body=eviction
                )
                print(f"Evicted pod {pod.metadata.name}")
            except ApiException as e:
                if e.status == 429:  # Too many requests
                    print(f"Pod {pod.metadata.name} protected by PDB")
                else:
                    print(f"Failed to evict {pod.metadata.name}: {e}")

        return {"node": node_name, "status": "drained"}

    def uncordon_node(self, node_name: str):
        """Mark node as schedulable again."""
        body = {
            "spec": {
                "unschedulable": False
            }
        }
        self.core_v1.patch_node(node_name, body)
        print(f"Node {node_name} uncordoned")

    def simulate_node_failure(
        self,
        node_name: str,
        duration_seconds: int = 300
    ):
        """
        Simulate complete node failure.
        Drain node, wait, then restore.
        """
        print(f"Simulating failure of node {node_name}")

        # Drain the node
        self.drain_node(node_name)

        # Wait for duration
        print(f"Node failed for {duration_seconds} seconds")
        time.sleep(duration_seconds)

        # Restore node
        self.uncordon_node(node_name)
        print("Node restored")
```

## Pod Autoscaling Chaos

```yaml
# Test HPA behavior under load
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: stress-hpa-trigger
spec:
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      'app': 'web-server'
  stressors:
    cpu:
      workers: 2
      load: 80  # 80% CPU load
  duration: '10m'

---
# Verify HPA scaling response
apiVersion: v1
kind: Pod
metadata:
  name: chaos-verification
spec:
  containers:
  - name: verifier
    image: bitnami/kubectl:latest
    command:
      - /bin/bash
      - -c
      - |
        # Monitor HPA scaling
        while true; do
          echo "=== HPA Status ==="
          kubectl get hpa web-server -o json | \
            jq '.status | {current: .currentReplicas, desired: .desiredReplicas, cpu: .currentCPUUtilizationPercentage}'

          echo "=== Pod Count ==="
          kubectl get pods -l app=web-server --no-headers | wc -l

          sleep 10
        done
```

## Custom Resource Chaos

```python
# Python script to test custom CRD resilience
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import random
import time

def chaos_delete_custom_resources(
    group: str,
    version: str,
    plural: str,
    namespace: str,
    percentage: int = 30
):
    """
    Randomly delete custom resources to test operator resilience.

    Args:
        group: API group (e.g., 'app.example.com')
        version: API version (e.g., 'v1')
        plural: Resource plural name (e.g., 'myapps')
        namespace: Namespace to target
        percentage: Percentage of resources to delete (0-100)
    """
    config.load_kube_config()
    custom_api = client.CustomObjectsApi()

    try:
        # List all custom resources
        resources = custom_api.list_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural
        )

        items = resources.get('items', [])
        if not items:
            print("No resources found")
            return

        # Calculate number to delete
        count_to_delete = max(1, int(len(items) * percentage / 100))

        # Randomly select resources
        to_delete = random.sample(items, count_to_delete)

        print(f"Deleting {count_to_delete} of {len(items)} {plural}")

        # Delete selected resources
        for resource in to_delete:
            name = resource['metadata']['name']
            try:
                custom_api.delete_namespaced_custom_object(
                    group=group,
                    version=version,
                    namespace=namespace,
                    plural=plural,
                    name=name,
                    body=client.V1DeleteOptions()
                )
                print(f"Deleted {plural}/{name}")
                time.sleep(1)  # Rate limit deletions
            except ApiException as e:
                print(f"Failed to delete {name}: {e}")

    except ApiException as e:
        print(f"Error listing resources: {e}")

# Example: Delete 30% of MyApp custom resources
chaos_delete_custom_resources(
    group='app.example.com',
    version='v1',
    plural='myapps',
    namespace='production',
    percentage=30
)
```

## Quick Reference

| Chaos Type | Tool | YAML/Command |
|------------|------|--------------|
| Pod delete | Litmus | `pod-delete` experiment |
| Network latency | Chaos Mesh | `NetworkChaos` with action: delay |
| Node drain | kubectl/API | `kubectl drain <node>` |
| CPU stress | Chaos Mesh | `StressChaos` with cpu stressor |
| DNS failure | Chaos Mesh | `DNSChaos` random/error action |
| I/O latency | Chaos Mesh | `IOChaos` with latency action |
| Network partition | Chaos Mesh | `NetworkChaos` partition |
| Pod failure | Chaos Mesh | `PodChaos` pod-failure |
