# System Testing Setup

## Overview

This documentation contains instructions for running the system tests for MkDocs. System tests validate end-to-end workflows through black-box testing of the CLI interface.

## Prerequisites

- Follow the setup instructions in `courseProjectDocs/setup`.
- Ensure that all dependencies are installed as described in the setup
- MkDocs must be installed and available on PATH
- Python virtual environment must be activated

## Running Tests

To run the new project creation system test:

```bash
pytest courseProjectCode/system-testing/system_tests.py::test_mkdocs_new_creates_project -v
```

## Running All System Tests

To run all system tests at once:

```bash
pytest courseProjectCode/system-testing/system_tests.py -v
```

## Expected Results

- All tests should pass
- Tests execute quickly (< 3 seconds total)
- Each test creates temporary directories that are automatically cleaned up

## Notes

- System tests use black-box testing
- Tests invoke MkDocs via subprocess (CLI interface)
- No internal MkDocs modules are imported
