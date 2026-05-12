# Browser Automation Job Runner – Reasoning

## Overview

This project implements a browser automation job runner using FastAPI, PostgreSQL, Playwright, WebSockets, and Next.js.

The system accepts a URL and automation goal from the frontend, creates a job record, executes browser automation using Playwright, emits real-time events, stores execution state in PostgreSQL, and captures screenshots/results.

The target website used for automation is:

https://books.toscrape.com

The automation extracts product titles and prices from the page.

---

# Architecture Decisions

## Backend

The backend was implemented using FastAPI because:
- it provides async support
- it works well with WebSockets
- it is lightweight and easy to structure

PostgreSQL was used to persist:
- job metadata
- execution status
- results
- errors
- logs

Playwright was selected because:
- it provides reliable browser automation
- supports Chromium headless execution
- handles modern web pages better than traditional scraping tools

---

# Job Lifecycle

Each submitted job moves through the following states:

- queued
- running
- completed
- failed

These states were chosen to keep execution tracking simple and meaningful without adding unnecessary state complexity.

---

# Real-Time Event Design

The automation emits meaningful execution events based on actual browser actions.

Events implemented:
- browser.launched
- page.navigating
- page.loaded
- action.taken
- data.extracted
- screenshot.captured
- browser.closed
- job.completed
- job.failed

These events are generated only when actual actions occur during automation execution.

No artificial delays or fake progress events are used.

---

# Concurrency Handling

The system supports multiple simultaneous jobs using background execution threads.

This allows multiple browser automation tasks to execute independently without blocking the API server.

A lightweight concurrency model was intentionally used to keep the implementation simple and focused for the assignment scope.

---

# Browser Cleanup and Failure Handling

Browser instances are always closed using browser.close() to prevent zombie Playwright processes.

Errors during automation are captured and stored in the database, and failed jobs are marked with:
- failure state
- error message
- last known execution step

---

# Frontend Design

The frontend was implemented using:
- Next.js
- React
- TypeScript

The UI allows users to:
- submit automation jobs
- observe execution logs
- view extracted results
- view screenshots captured during automation

The UI was intentionally kept minimal to focus on execution observability and backend integration.

---

# Tradeoffs

The implementation prioritizes:
- observability
- simplicity
- clear execution flow
- reliability of automation

instead of building a fully distributed queueing system.

For production scale, improvements could include:
- Redis/Celery based queueing
- containerized browser workers
- authentication
- retry policies
- distributed event streaming

---

# Conclusion

The project demonstrates:
- browser automation orchestration
- real-time execution tracking
- backend/frontend communication
- PostgreSQL persistence
- concurrent job execution
- failure-aware automation workflows