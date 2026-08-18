# CI Pipeline Overview — Task Manager API

## Purpose
This document explains the continuous integration (CI) pipeline configured
for the Task Manager API, why each stage exists, and how to read the results.

## Trigger
The pipeline (`.github/workflows/ci.yml`) runs automatically on:
- **Every push**, to any branch — catches problems as soon as code changes.
- **Every pull request into `main`** — acts as a gate before code merges.

This means no code reaches `main` without passing lint and tests first.

## Pipeline Stages

| # | Stage               | Tool               | Purpose                                                              |
|---|----------------------|---------------------|-----------------------------------------------------------------------|
| 1 | Checkout             | `actions/checkout`  | Pulls the repository code onto the CI runner.                        |
| 2 | Environment setup    | `actions/setup-python` | Installs Python 3.11 and enables pip dependency caching for speed. |
| 3 | Install dependencies | `pip`                | Installs Flask (runtime) plus pytest, flake8, and black (dev tools). |
| 4 | Lint                 | `flake8`             | Flags syntax errors, unused imports, and style violations (max 100-char lines). |
| 5 | Format check         | `black --check`      | Verifies code matches a consistent auto-formatting standard; does not modify files, only fails if they're non-compliant. |
| 6 | Automated tests      | `pytest`             | Runs the full test suite (13 tests) covering all CRUD endpoints, including error cases like missing fields and 404s. |

If any stage fails, the pipeline stops and GitHub marks the commit/PR with a
red "X" — the failure reason is visible directly in the Actions log for that
step, so a broken build is caught before it's reviewed or merged.

## Why This Order
Fast, cheap checks run first (lint takes seconds) so obvious mistakes are
caught before spending time on the fuller test run. This is a standard
"fail fast" pattern used in real CI/CD pipelines.

## Local Equivalent
Before pushing, the same checks can be run locally to catch issues early:

```bash
pip install -r requirements-dev.txt
flake8 app tests run.py
black --check app tests run.py
pytest -v
```

## Possible Extensions
- Add a `deploy` job that only runs on `main` after tests pass (e.g., deploy
  to Render, Fly.io, or AWS Elastic Beanstalk).
- Add a code coverage report (`pytest-cov`) with a minimum threshold.
- Add a Jenkins-equivalent `Jenkinsfile` mirroring these same stages to
  demonstrate pipeline-as-code outside of GitHub Actions specifically.
