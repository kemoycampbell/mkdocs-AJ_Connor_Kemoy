# Integration Testing Setup

## Overview

This documentation contain the overview of how to run the integration tests

## Prerequisites

- Follow the setup instructions in `CourseProjectDocs/Setup`.
- Ensure that all dependencies are installed as described in the setup

## Running Integration Test 1

`pytest mkdocs/tests/integration_build_tests.py::TestBuildTemplate::test_build_template -v`

## Running Integration Test 2

`pytest mkdocs/tests/integration_build_tests.py::TestBuildTemplateWithPlugin::test_build_template_with_plugin -v`

## Running Integration Test 3

`pytest mkdocs/tests/integration_build_tests.py::test_missing_nav_files -v`

## Running All Integration Tests

`pytest mkdocs/tests/integration_build_tests.py -v`
