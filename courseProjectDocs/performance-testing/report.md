# Performance Testing

This document reports on performance testing performed on the MkDocs project.

## Load Test

## Stress Test
### 1. Test Scope and Design
| Attribute | Value |
|-----------|-------|
| **Component Tested** | `mkdocs serve` HTTP server |
| **Tools Used** | [Locust](https://docs.locust.io/en/stable/quickstart.html)  and [Docker Compose container](../../courseProjectCode/performance-testing/compose/locust-stress.yaml)|
| **Endpoints Tested** | `/` , `/getting-started/`, `/nugets/`, `/nethereum-managed-accounts/`, `/nethereum-creating-a-new-account-using-geth/`, `/contracts/deploying/`, `/unity3d-smartcontracts-getting-started/` |
| **Test Type** | Stress Test |

### 2. Configuration
| Parameter | Value |
|-----------|-------|
| **Max Users** | 2000 |
| **Spawn Rate** | 200/sec |
| **Duration** | 5 minutes |
![Stress Test Configuration](../images/performance-testing/stress-config.png)

### 3. Results
![Stress Test Results](../images/performance-testing/stress-test.png)
![Stress Test More](../images/performance-testing/stress-test-contd.png)
[Full Locust HTML Report](../../courseProjectCode/performance-testing/stress-test.html)

### 4. Performance Finding
**Finding:** Serve performance degraded as concurrent users increase with response times increased significantly and failures  occurred.

- **Observation:** As users increased to around 2,000 concurrent users, it begans to choke and take around 15-36 seconds to serve the requests. Based on the test results, the server can handle 200-220 req/sec before it becomes saturated and response times increase significantly with failures occurring. The number of failures remains low relatively to the total requests made.

- **Throughput:** The RPS remains between 165-220 RPS and this is expected due to serve not designed
production use and utilize a single process.

- **Things to keep in mind:**
  - MkDocs serve is not intended for production use and is single-threaded.
  - The perfomance measurements here depends on the host machine's hardware and network conditions.
  This was tested on a machine that contains 64 GB of RAM with NVIDIA GeForce RTX 3080 GPU and 12th Gen Intel(R) Core(TM) i9-12900K CPU @ 3.20GHz with 16 cores. So the result may vary on different hardware.

## Spike Test

### 1. Test Scope and Design

| Attribute | Value |
|-----------|-------|
| **Component Tested** | `mkdocs serve` HTTP server |
| **Tools Used** | [Locust](https://docs.locust.io/en/stable/quickstart.html) and [Docker Compose container](../../courseProjectCode/performance-testing/compose/locust-spike.yaml) |
| **Endpoint Tested** | `/` (Homepage) |
| **Test Type** | Spike Test |

### 2. Configuration

| Parameter | Value |
|-----------|-------|
| **Baseline Users** | 25 |
| **Spike Users** | 125 |
| **Spawn Rate** | 125/sec (instant spike) |
| **Pattern** | Baseline → Spike → Recovery |

![Spike Test Configuration](../images/performance-testing/spike-config.png)

### 3. Results

![Spike Test Results](../images/performance-testing/spike-test.png)

[Full Locust HTML Report](../../courseProjectCode/performance-testing/spike-test.html)

### 4. Performance Finding

**Finding:** Response time increased during spike but server remained stable with 0% failures.

- **Observation:** During the spike from 25 to 125 users, the 95th percentile response time increased from ~5ms to ~85ms
- **Throughput:** RPS increased from ~20 to ~80 requests/second during peak load
- **Recovery:** Server recovered immediately when load decreased, response times returned to baseline

## Team Contributions

 Member | Task/Contribution | Notes
--------|------------------|--------
 AJ Barea | Spike Test | Designed and executed Homepage spike test using Locust
 Connor | | 
 Kemoy |Stress test, create docker containers, update the document | Designed and executed stress test using Locust, created Docker containers for testing environment & automation in headless modes