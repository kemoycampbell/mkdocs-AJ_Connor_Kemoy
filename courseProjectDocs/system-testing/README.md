# System Testing Setup

## Overview

This documentation contains instructions for running the system tests for MkDocs. System tests validate end-to-end workflows through black-box testing of the CLI interface.

## Prerequisites

- Clone the project from `https://github.com/kemoycampbell/mkdocs-AJ_Connor_Kemoy`
- Download and install docker for your system from `https://www.docker.com/products/docker-desktop/`

## Test Locations
The black box tests are located in
```bash
courseProjectCode/system-testing/tests
```

## How to run the tests
### Change directory into the correct directory
```bash
cd courseProjectCode/system-testing/
```

### Build the docker environment
```bash
docker-compose build --no-cache
```

### Running all tests
```bash
docker-compose run --rm mkdocs_system_test tests/
```

### Running a specific test file
```bash
docker-compose run --rm mkdocs_system_test tests/<name of the test file>
eg. 
docker-compose run --rm mkdocs_system_test tests/test_mkdocs_cli_new.py
```


## Expected Results

- All tests should pass
- Tests execute quickly
- Each test creates temporary directories that are automatically cleaned up

## Notes

- System tests use black-box testing
- Tests invoke MkDocs via subprocess (CLI interface)
- Tests involves HTTP calls using python requests
- No internal MkDocs modules are imported
