# Performance Testing Configuration and Execution
This document outlines the configuration and execution of performance tests for the MkDocs project.
The performance tests included in this report are Load Test, Stress Test, and Spike Tests were performed using Docker
containers with Locust as the testing tool.

# Prerequisites
- Docker and Docker Compose installed on your machine.

# Test Architecture Structure
The tests are organized into the following structure within the project:
```courseProjectCode/
└── performance-testing/
    ├── compose/
    │   ├── locust-stress.yaml
    │   └── locust-spike.yaml
    └── tests/
        ├── stress_test.py
        └── spike_test.py
```

The `compose` directory contains Docker Compose files for setting up the testing environment, while the `tests` directory contains the Locust test scripts.

When executing the tests, the Docker Compose files will set up the necessary services, including the MkDocs server and the Locust generator in headless mode and store the results in HTML format under the `/tests/` directory.

## Spike Test Commands

### Change into the project root directory
```bash
cd mkdocs-AJ_Connor_Kemoy
```

### Run Tests
```bash
docker-compose -f courseProjectCode/performance-testing/compose/locust-spike.yaml up --build -d
```
### Accessing the Results
After the test completes, you will find the HTML report in `courseProjectCode/performance-testing/tests/spike_test_report.html`. Open this file in a web browser to view the detailed results of the spike test.

### Tearing down the test environment
To stop and remove the test environment, run the following command:
```bash
docker-compose -f courseProjectCode/performance-testing/compose/locust-spike.yaml down
```

# Stress Test Commands
### Change into the project root directory
```bash
cd mkdocs-AJ_Connor_Kemoy
```

### Run Tests
```bash
docker-compose -f courseProjectCode/performance-testing/compose/locust-stress.yaml up --build -d
```
### Accessing the Results
After the test completes, you will find the HTML report in `courseProjectCode/performance-testing/tests/stress_test_report.html`. Open this file in a web browser to view the detailed results of the stress test.

### Tearing down the test environment
To stop and remove the test environment, run the following command:
```bash
docker-compose -f courseProjectCode/performance-testing/compose/locust-stress.yaml down
```


