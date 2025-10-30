# Inference Service Tests

This repository contains a minimal inference service and a test suite that
exercises main and fallback-model behavior. The tests use `sample_input.json`
to provide input vectors for the different code paths.

Quick start (POSIX):

1. ./setup.sh
2. ./run_tests.sh

Quick start (Windows PowerShell/pwsh):

1. .\setup.ps1
2. .\run_tests.ps1

Or use the Makefile (POSIX) to run setup and tests in one command:

1. make test

The test runner will generate an HTML coverage report at `coverage_html/index.html`.

Continuous Integration:

A GitHub Actions workflow (`.github/workflows/ci.yml`) is included and runs the test matrix
on push and pull request events. The workflow uploads an HTML coverage artifact.
