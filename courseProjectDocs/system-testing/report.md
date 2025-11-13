# System Testing Report

## Overview

This document highlights the system tests performed on MkDocs. System tests validate end-to-end workflows through black-box testing of the CLI interface, ensuring that user-facing functionality meets the specified functional requirements.

We utilize docker system to create a container which installed mkdocs and provides an isolate environment
for testing. 

**Test Approach:** Black-box testing using `subprocess` and requests (no internal MkDocs modules imported)  
**Test Framework:** pytest
**Test Environment**: Docker - Create a container with mkdocs installed in the container

---
## New Project Creation Workflow

### Test Design Summary

**Test Type:** Black-box system test  
**Test File:** `courseProjectCode/system-testing/test_mkdocs_cli_new.py`
**Execute The Test**:`docker compose run --rm mkdocs_system_test tests/test_mkdocs_cli_new.py`

**Modules Tested:**

- CLI interface (`mkdocs new` command)
- Project scaffolding system
- Default configuration generation

**Test Approach:**

```python
# Execute via subprocess (black-box)
subprocess.run(['mkdocs', 'new', project_name], cwd=temp_dir)

# Verify project structure
assert os.path.exists(project_path)
assert os.path.isfile('mkdocs.yml')
assert os.path.isdir('docs/')
assert os.path.isfile('docs/index.md')
```

### Test Data Preparation

- Create temporary directory for test execution
- Execute `mkdocs new test_project` with subprocess run
- Capture command output and exit code
- Verify system file and directory changes

### Test Case Details

 Workflow | Setup | Test Steps | Expected Results | Status
----------|-------|------------|------------------|--------
 New Project Creation | Temporary directory created | 1. Run `mkdocs new test_project`<br>2. Verify exit code = 0<br>3. Check project directory exists<br>4. Verify mkdocs.yml created<br>5. Verify docs/ directory created<br>6. Verify docs/index.md created<br>7. Check file contents | - Project directory created<br>- mkdocs.yml contains `site_name: My Docs`<br>- docs/ directory exists<br>- docs/index.md contains welcome content<br>- Command exits successfully | Passed

### Execution Results

```bash
# Test execution command
docker compose run --rm mkdocs_system_test tests/test_mkdocs_cli_new.py
```

![System Test Output](../images/system/system_test_1_output.png)

**Observations:**

The `mkdocs new` command created a complete project structure through the CLI interface. The test verifies:

- Command executes without errors (exit code 0)
- Project directory is created with the correct name
- Configuration file (`mkdocs.yml`) is generated with default `site_name: My Docs`
- Documentation directory (`docs/`) is created
- Default homepage (`docs/index.md`) is created including its welcome content and command reference
- All files contain expected default content

This black-box test validates the complete end-to-end workflow of the new project creation workflow without accessing internal implementation details.

---
---
## Serve Workflow

### Test Design Summary

**Test Type:** Black-box system test  
**Test File:** `courseProjectCode/system-testing/test_mkdocs_cli_serve.py`
**Execute The Test**:`docker compose run --rm mkdocs_system_test tests/test_mkdocs_cli_serve.py`

**Modules Tested:**

- CLI interface (`mkdocs serve` command)
- Spin up a web server and show the site contents from `mkdocs/docs`
- Byproduct command - `mkdoc new` to build a default new project with default configurations 

**Test Approach:**

```python
# Execute via subprocess (black-box)
process = subprocess.Popen(
    ["mkdocs", "serve", "-a", "0.0.0.0:8000"],
    cwd=mkdocs_dir,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Verify that we get 200 response and the default web page
assert response.status_code == 200, "Failed to response with status 200"
assert "Welcome to MkDocs" in response.text, "Homepage content does not contain Welcome to MkDocs"
```

### Test Data Preparation

- Create temporary directory for test execution
- Run `mkdocs new` to create a default project with the default configuration
- Execute `mkdocs serve -a 0.0.0.0:8000` to bind it to listen on all interface at port 8000
- Wait for the server to start. We will attempt up to 5 retries if need
- Make a HTTP resquest and capture the response
- Verify the response and content on the webpage is what is expected

### Test Case Details

 Workflow | Setup | Test Steps | Expected Results | Status
----------|-------|------------|------------------|--------
 Serve | Temporary directory created | 1. Run `mkdocs new mkdocs` to create a default project<br>2. Run `mkdocs serve -a 0.0.0.0:8000` to start the web server<br>3. Wait for the web server to start up. Max 5 retries check<br>4. Make HTTP requests to `localhost:8000`<br>5. Verify the response is 200<br>6. Verify that `Welcome to MkDocs` is in the index.html content<br>7. Send kill signal to terminate the web server<br>-  Command exits successfully | Passed


### Execution Results

```bash
# Test execution command
docker compose run --rm mkdocs_system_test tests/test_mkdocs_cli_serve.py
```

![System Test Output](../images/system/system_test_1_output.png)

**Observations:**

The `mkdocs new` command created a complete project structure through the CLI interface. The test verifies:

- Command executes without errors (exit code 0)
- Project directory is created with the correct name
- Configuration file (`mkdocs.yml`) is generated with default `site_name: My Docs`
- Documentation directory (`docs/`) is created
- Default homepage (`docs/index.md`) is created including its welcome content and command reference
- All files contain expected default content

This black-box test validates the complete end-to-end workflow of the new project creation workflow without accessing internal implementation details.
---

## Team Contributions

 Member | Task/Contribution | Test Cases Implemented
--------|------------------|----------------------
 AJ Barea | System testing infrastructure setup, created test file structure, implemented new project creation workflow system test using a black-box subprocess approach, created docs | New Project Creation Workflow
 Connor | - | -
 Kemoy | - | -

---

