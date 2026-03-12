# Gym Tracker Test Framework (Portfolio Project)

**Kristina Glushkova** — SDET

Automation for the Gym Tracker app (Spring Boot backend, React frontend). Python + Playwright + pytest, with API tests generated from the OpenAPI spec and optional LLM exploratory tests.

---

## What's in here

- **UI** — Playwright, Page Object Model, Google OAuth
- **API** — Rule-based tests from spec + Claude exploratory edge cases
- **CI** — Runs on push, PR, nightly, and when BE/FE repos push; creates bug reports on nightly failures

---

## Stack

Python, Playwright, pytest, requests, Faker, Anthropic (Claude), Docker Compose

---

## Layout

```
api/          # API tests, OpenAPI parser, test generator
ui/           # UI tests, page objects
.github/      # Workflows
config.py     # .env loader
Makefile      # Commands
```

---

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

Copy `.env.example` to `.env` and add your keys.

---

## Run

```bash
make docker-up
make test              # UI headless
make test-headed       # UI visible
make test-api          # API + exploratory
make generate-tests    # Regenerate from spec
```

---

## Coverage

**UI:** Login, add client (validation, success, cancel)

**API:** Happy path, 401, 404, missing required, invalid format. Exploratory: type mismatch, null, empty string, extra fields.

---

*Portfolio project. Tests Gym Tracker only.*
