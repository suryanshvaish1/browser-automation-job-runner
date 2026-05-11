# Kustodian Browser Automation Job Runner

## Overview

This project is a browser automation job runner built using:

- FastAPI (Python)
- PostgreSQL
- Playwright
- WebSockets
- Next.js + React + TypeScript

The system allows users to:
- Submit a URL and automation goal
- Execute browser automation using Playwright
- Capture screenshots
- Extract structured data
- Stream automation events
- Persist job state and results

---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Playwright

## Frontend
- Next.js
- React
- TypeScript

---

# Features

- REST API job submission
- Concurrent job execution
- Playwright browser automation
- Screenshot capture
- Structured data extraction
- Real-time execution logs
- PostgreSQL persistence
- Browser cleanup after execution

---

# Project Structure

backend/ → FastAPI backend  
frontend/ → Next.js frontend  
docs/ → schema and reasoning documents  

---

# Backend Setup

## Create Virtual Environment

```bash
py -3.11 -m venv venv
Activate
.\venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Install Playwright
playwright install
Run Backend
python -m uvicorn app.main:app --reload

Backend runs on:

http://127.0.0.1:8000

Frontend Setup
npm install
npm run dev
Frontend runs on:

http://localhost:3000

Automation Target

https://books.toscrape.com

Sample Goal

extract product titles and prices

Database

PostgreSQL is used for:

job state
logs
results
errors
Concurrency

Jobs are executed using background threads to support multiple concurrent automation runs.

Browser Cleanup

Each browser instance is explicitly closed after:
success
failure
exception

to prevent zombie Playwright processes.

---

# docs/reasoning.md

Paste:

```md id="r4"
# Engineering Reasoning

## Architecture Overview

The system follows a client-server architecture.

Frontend:
- Next.js
- React
- TypeScript

Backend:
- FastAPI
- PostgreSQL
- Playwright

The frontend submits automation jobs to the backend using REST APIs.

The backend creates a job record, executes browser automation using Playwright, and streams execution events.

---

# Job Lifecycle

The job lifecycle contains the following states:

- queued
- running
- completed
- failed

These states were selected to keep the execution flow meaningful while avoiding unnecessary complexity.

---

# Automation Design

The automation target used is:

https://books.toscrape.com

The automation performs:
- browser launch
- page navigation
- scrolling
- hover interaction
- data extraction
- screenshot capture

These actions emit meaningful execution events.

---

# Event Design

Events are emitted only when real browser actions occur.

Examples:
- browser.launched
- page.navigating
- page.loaded
- action.taken
- data.extracted
- screenshot.captured
- job.completed
- job.failed

No artificial delays or fake progress events were used.

---

# Concurrency Handling

Jobs are executed in background threads.

This allows:
- multiple simultaneous jobs
- isolated browser execution
- non-blocking API responses

A thread-based approach was chosen because it simplified Windows compatibility issues with Playwright subprocess execution.

---

# Browser Cleanup Strategy

Each Playwright browser instance is explicitly closed after:
- successful execution
- failures
- exceptions

This prevents orphaned browser processes.

---

# Database Design

PostgreSQL stores:
- job metadata
- execution status
- logs
- extracted results
- errors

This allows traceability and recovery of execution history.

---

# Failure Handling

Failures are persisted to the database and exposed through job status updates.

The system captures:
- exception messages
- failed states
- execution step visibility

This improves observability and debugging.

---

# Frontend Design

The frontend was intentionally kept minimal.

It provides:
- URL input
- goal input
- live execution logs
- automation visibility

The focus was placed on execution transparency rather than UI complexity.