# Sample Tracker (MVP)

A lightweight Python application for tracking laboratory samples with persistent storage, structured logging, and a modular architecture.

This project demonstrates how a minimal backend system can evolve from a command-line tool into a graphical application while preserving the same core logic and data model.

The repository contains two versions that share the same backend but expose different user interfaces.

---

## Purpose

This project serves as a compact demonstration of building a maintainable application with structured data handling, audit logging, and layered architecture using Python.

---

## Key Characteristics

* Object-Oriented application design
* Unique identifier generation using UUID
* Persistent JSON data storage
* Timestamped event logging
* Separation of interface and business logic
* Incremental evolution from CLI → GUI

All operations are recorded with structured timestamps, enabling traceability of actions such as creation, status updates, and deletion.

---

## Version 1 — CLI MVP

The first version implements a minimal command-line interface to interact with the sample tracking backend.

### Features

* Create solid or liquid samples
* Automatic UUID assignment
* Update sample status
* Delete samples
* Persistent storage in `samples.json`
* Timestamped event logging in `sample_log.json`

### Run

```bash
python v1-cli/sample_app.py
```

---

## Version 2 — GUI MVP

The second version introduces a graphical interface using Tkinter while reusing the exact same backend logic as the first version.

This demonstrates how interface layers can change without modifying the core data model or persistence system.

### Features

* Popup dialogs for sample data entry
* Button-based application workflow
* Access to the same backend classes and storage system
* Consistent logging and data persistence

### Run

```bash
python v2-gui/sample_app_gui.py
```

---

## Architecture Overview

The system is organized into clearly separated components:

| Component       | Responsibility                         |
| --------------- | -------------------------------------- |
| Sample Classes  | Define sample structure and properties |
| SampleManager   | Handles loading, saving, and searching |
| SampleLogger    | Records timestamped events             |
| Interface Layer | CLI or GUI user interaction            |

This separation allows the application to evolve without rewriting core logic.

---

## Example Logged Event

```json
{
    "Timestamp": "2026-03-06T14:22:01",
    "Event": "CREATED",
    "Sample ID": "2e2f6a10-9e4d-4e32-bc91-98d5c1c0b77f",
    "Message": "Sample Sodium chloride created"
}
```

---

## Future Extensions

Potential improvements include:

* Database backend (SQLite / PostgreSQL)
* Search and filtering tools
* Data export utilities
* User authentication
* API or mobile interface






