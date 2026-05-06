# Autonomous Dev System

Autonomous Dev System is an early-stage scaffold for an AI-assisted **Figma → Code → Pull Request** pipeline. The repository models a multi-agent software delivery flow where planner, database, API, UI, QA, validation, review, and GitHub automation components can collaborate to turn a feature request into generated artifacts, quality-gate decisions, and pull-request automation.

> **Project status:** scaffold/prototype. Most modules currently return deterministic placeholder output and are intended to be extended with real model providers, repository indexing, Figma ingestion, code generation, CI execution, and GitHub write operations.

## Table of Contents

- [Basic Introduction](#basic-introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Architecture Overview](#architecture-overview)
- [Repository Structure](#repository-structure)
- [Features and Status](#features-and-status)
- [Configuration](#configuration)
- [Testing Guide](#testing-guide)
- [Development Workflow](#development-workflow)
- [CI/CD](#cicd)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## Basic Introduction

The project explores how AI agents can coordinate the implementation lifecycle for product features:

1. Accept a feature request or design-driven task.
2. Break the request into implementation work.
3. Generate database, API, and UI artifacts.
4. Extract and validate contracts between generated layers.
5. Generate tests from contracts.
6. Run quality gates and AI review checks.
7. Feed failures back into a self-healing loop.
8. Optionally create or merge GitHub pull requests.

The current codebase is intentionally lightweight. It provides module boundaries and orchestration patterns rather than production-ready generation logic.

## Prerequisites

### Required

- **Python 3.10+** — GitHub Actions currently configures Python 3.10.
- **Git** — for cloning, branching, committing, and pull-request workflows.
- **pip** and optionally **venv** — for local dependency installation.

### Optional, depending on which modules you run

Some prototype modules import optional third-party libraries that are not yet captured in a requirements file:

- **pytest** — for local test discovery and CI parity.
- **requests** — required by GitHub service modules.
- **numpy**, **faiss** or **faiss-cpu**, and **sentence-transformers** — required by the embedding/vector-store based context engine.
- A model provider SDK/API key — needed when replacing placeholder agents with real LLM calls.
- A GitHub token with appropriate repository permissions — needed for GitHub branch, file, PR, or merge automation.

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd figma-code-gen-pr
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install local dependencies

There is no committed `requirements.txt` yet. For the currently wired CI path, install pytest:

```bash
python -m pip install --upgrade pip
python -m pip install pytest
```

If you plan to use GitHub service helpers or the vector context engine, install the optional dependencies you need:

```bash
python -m pip install requests numpy sentence-transformers faiss-cpu
```

### 4. Run a basic orchestrator smoke test

```bash
python - <<'PY'
from ai.workflows.contract_orchestrator import run_feature

result = run_feature("Create a signup form")
print(result)
PY
```

### 5. Run validation and test-generation flow

```bash
python - <<'PY'
from ai.workflows.contract_orchestrator import run_feature
from ai.workflows.validation_orchestrator import validate_and_generate_tests

result = run_feature("Create a signup form")
validation = validate_and_generate_tests(
    result["schema"],
    result["api_contracts"],
    result["ui_contracts"],
)
print(validation)
PY
```

## Architecture Overview

The system is organized as layered orchestration around specialized agents:

```text
Feature request / design task
        │
        ▼
Planner / Sprint manager
        │
        ▼
DB Agent ──► Schema Extractor
        │             │
        ▼             ▼
API Contract Generator ──► API Agent
        │                    │
        ▼                    ▼
UI Contract Generator  ──► UI Agent
        │
        ▼
Contract Validator + Test Generator
        │
        ▼
Gate Orchestrator + LLM Judge
        │
        ├── pass ──► GitHub PR / merge services
        │
        └── fail ──► QA self-healing feedback loop
```

### Key layers

- **Agents (`ai/agents`)**: Specialized generators and reviewers for planning, DB, API, UI, development, and QA feedback.
- **Contracts (`ai/contracts`)**: Converts generated database schema information into API contracts and UI bindings.
- **Workflows (`ai/workflows`)**: Coordinates agent execution for single-feature, dependency-aware, contract-aware, validation, and self-healing flows.
- **Agile orchestration (`ai/agile`)**: Adds sprint/backlog decomposition, quality gates, retry loops, and merge decisions.
- **Context (`ai/context`)**: Provides repository-awareness scaffolding with a naive in-memory engine and a vector-store-based variant.
- **Validation and testing (`ai/validation`, `ai/testing`)**: Checks cross-layer contract consistency and emits generated test skeletons.
- **Review and observability (`ai/review`, `ai/observability`)**: Provides placeholder LLM scoring and event logging.
- **GitHub services (`ai/services`)**: Contains helper classes for GitHub branch, file, PR, and merge API operations.
- **CI (`.github/workflows`)**: Runs pull-request validation scaffolding.

## Repository Structure

```text
.
├── .github/workflows/
│   ├── ai_pipeline.yml        # Pull-request AI validation scaffold
│   └── ci.yml                 # Basic pull-request CI scaffold
├── ai/
│   ├── agents/                # Planner, developer, DB, API, UI, and QA agents
│   ├── agile/                 # Sprint, pipeline, and quality-gate orchestration
│   ├── context/               # Repo context/RAG and vector-store prototypes
│   ├── contracts/             # Schema, API contract, and UI contract generators
│   ├── observability/         # Event monitoring helper
│   ├── prompts/               # Prompt templates
│   ├── review/                # LLM judge placeholder
│   ├── services/              # GitHub automation helpers
│   ├── testing/               # Test-generation helper
│   ├── validation/            # Contract validation logic
│   └── workflows/             # End-to-end and focused workflow orchestrators
└── README.md
```

## Features and Status

| Feature | Status | Notes |
| --- | --- | --- |
| Multi-agent module layout | In progress | Core agent boundaries exist for planner, DB, API, UI, developer, and QA roles. |
| Figma-to-code pipeline | Planned | The repository describes the pipeline goal, but Figma API ingestion and design parsing are not implemented yet. |
| Planner agent | Prototype | Returns a simple one-task plan. |
| DB generation | Prototype | Returns placeholder SQL text for a task. |
| API generation | Prototype | Returns placeholder API code for a task. |
| UI generation | Prototype | Returns placeholder UI code for a task. |
| Contract-aware orchestration | Prototype | Coordinates DB, schema extraction, API contracts, UI contracts, and generated artifacts. |
| Schema extraction | Prototype | Parses simple SQL-like `CREATE TABLE` output. |
| API contract generation | Prototype | Builds basic POST endpoint contracts from extracted schema tables. |
| UI contract generation | Prototype | Builds form bindings from API contracts. |
| Contract validation | Prototype | Checks API fields against schema and UI fields against API contracts. |
| Test generation | Prototype | Emits API/UI test skeleton strings from contracts. |
| Quality gates | Prototype | Provides contract, test, and placeholder LLM-judge gates. |
| Self-healing QA loop | Prototype | Converts failures into fix prompts for a developer agent placeholder. |
| Repository context engine | Prototype | Includes naive in-memory search and a vector-store variant. |
| LLM judge | Placeholder | Returns a fixed score until connected to a real model provider. |
| GitHub PR automation | Prototype | Contains GitHub API helper methods; production encoding, error handling, and authentication flow need hardening. |
| GitHub auto-merge | Prototype | Contains a merge helper; should be guarded by policy, checks, and permissions before production use. |
| Observability | Prototype | Prints structured event dictionaries with UTC timestamps. |
| CI workflow | Scaffolded | Pull-request workflows exist; AI gate currently echoes a success message. |
| Dependency management | Planned | A pinned dependency file is not yet present. |
| Unit/integration tests | Planned | No committed test suite is present yet. |

Legend:

- **Planned**: Intended capability with little or no implementation.
- **Placeholder**: Stub behavior that returns fixed or deterministic mock data.
- **Prototype**: Minimal implementation useful for local experimentation but not production hardened.
- **In progress**: Foundational implementation exists and is expected to evolve.

## Configuration

The scaffold currently avoids hard-coding runtime configuration. As production integrations are added, prefer environment variables and local `.env` files that are excluded from Git.

Suggested future environment variables:

| Variable | Purpose |
| --- | --- |
| `GITHUB_TOKEN` | Authenticate GitHub API branch, file, PR, and merge operations. |
| `GITHUB_REPOSITORY` | Target repository in `owner/name` format. |
| `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or provider-specific keys | Authenticate model calls for generation, review, and self-healing loops. |
| `FIGMA_TOKEN` | Authenticate Figma API reads when Figma ingestion is implemented. |
| `FIGMA_FILE_KEY` | Identify the Figma source file for design-to-code runs. |
| `VECTOR_INDEX_PATH` | Persist or load local vector indexes when context storage is expanded. |

## Testing Guide

### Run all tests

```bash
pytest
```

At the moment, the repository does not include committed test files, so pytest may report that no tests were collected. This is expected until a test suite is added.

### Run Python syntax checks

```bash
python -m compileall ai
```

This verifies that the Python modules can be parsed and byte-compiled in the current environment.

### Run targeted smoke checks

Contract-aware workflow:

```bash
python - <<'PY'
from ai.workflows.contract_orchestrator import run_feature
print(run_feature("Create a todo list"))
PY
```

Validation workflow:

```bash
python - <<'PY'
from ai.workflows.validation_orchestrator import validate_and_generate_tests

schema = {"users": ["email", "name"]}
api_contracts = [{"endpoint": "/users", "method": "POST", "request": ["email", "name"], "response": ["id", "email", "name"]}]
ui_contracts = [{"form": "/users", "fields": ["email", "name"], "submit_to": "/users"}]
print(validate_and_generate_tests(schema, api_contracts, ui_contracts))
PY
```

Quality gate workflow:

```bash
python - <<'PY'
from ai.agile.gate_orchestrator import GateOrchestrator

validation = {"api_errors": [], "ui_errors": [], "api_tests": "test api", "ui_tests": "test ui"}
print(GateOrchestrator().decide(validation, artifacts={}))
PY
```

### Suggested future test coverage

- Unit tests for schema extraction edge cases.
- Unit tests for API and UI contract generation.
- Contract validator success and failure cases.
- Generated-test format checks.
- Pipeline orchestrator retry and gate-decision behavior.
- GitHub service tests with mocked HTTP responses.
- Context engine search and vector-store behavior.

## Development Workflow

1. Create a branch for your change.
2. Update or add modules under the relevant `ai/` package.
3. Add or update tests for the behavior you changed.
4. Run `python -m compileall ai` and `pytest` locally.
5. Open a pull request.
6. Use the AI pipeline and CI results to review failures.
7. Iterate until quality gates pass.

Recommended standards as the project matures:

- Add type hints to public APIs.
- Keep agent interfaces small and explicit.
- Avoid side effects during imports.
- Add dependency pins before relying on third-party packages in CI.
- Mock external APIs in tests.
- Treat auto-merge as a protected operation requiring explicit policy gates.

## CI/CD

The repository includes two pull-request workflows:

- **CI**: A minimal workflow that currently checks out the repository and prints a CI message.
- **AI Pipeline**: Installs Python 3.10 and pytest, runs pytest, and executes a placeholder AI gate check.

These workflows should be expanded with dependency installation, linting, type checking, unit tests, integration tests, coverage reporting, generated-artifact validation, and real gate enforcement.

## Roadmap

Potential next steps:

- Add `requirements.txt` or `pyproject.toml` with pinned dependencies.
- Add a first unit test suite.
- Implement real Figma file ingestion and node extraction.
- Replace placeholder agents with provider-backed model calls.
- Persist generated artifacts to a workspace before committing them.
- Harden GitHub API helpers with proper Base64 content encoding, response validation, retries, and typed errors.
- Add structured logging and trace IDs across orchestrators.
- Add policy controls for auto-merge and production repository writes.
- Add examples for common feature-generation scenarios.

## Contributing

Contributions should preserve the scaffold's clear separation between agents, contracts, workflows, gates, and services. When adding a production integration, include tests and document any required configuration.

Before opening a pull request, run:

```bash
python -m compileall ai
pytest
```

## Troubleshooting

### `ModuleNotFoundError` for `requests`, `faiss`, `numpy`, or `sentence_transformers`

Install only the optional dependencies required for the modules you are running. For example:

```bash
python -m pip install requests numpy sentence-transformers faiss-cpu
```

### `pytest` reports no tests collected

No test suite is currently committed. Use the smoke-test commands in this README until unit tests are added.

### GitHub API calls fail

Confirm that your token has the required repository permissions, that `repo` is passed in `owner/name` format, and that the target branch or pull request exists.

### Vector context engine fails to initialize

The vector engine depends on optional native and ML packages. Start with the simple `ContextEngine` if you only need in-memory text search, or install `faiss-cpu`, `numpy`, and `sentence-transformers` for `ContextEngineV2`.
