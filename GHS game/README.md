# GHS Hazard Identification Game

A lightweight educational desktop game built with Python and Pygame that challenges players to identify the correct Globally Harmonized System (GHS) hazard symbols for various chemicals.

The game presents a chemical name and formula, and the player must select the correct hazard pictograms based on standard chemical safety classifications.

This project demonstrates how structured data, object-oriented programming, and interactive user interfaces can be combined into a functional application.

---

## Overview

The **Globally Harmonized System of Classification and Labelling of Chemicals (GHS)** is an international standard used to communicate chemical hazards through pictograms.

This game tests the player's ability to recognize hazard classifications by matching chemicals with the correct pictograms.

Features include:

- Interactive hazard symbol selection
- Support for chemicals with **multiple hazard symbols**
- Handling of **chemicals with no hazard classification**
- Immediate visual feedback for correct and incorrect selections
- Score tracking
- Restartable game session
- Automatic game termination after repeated incorrect attempts

---

## Minimum Viable Product (MVP)

This project represents a **minimum viable product** demonstrating the core functionality of a hazard identification training tool.

The MVP includes:

- A working graphical interface
- A data-driven chemical hazard database
- Clickable pictogram interactions
- Real-time visual feedback
- Basic game state management
- Restart and termination logic

The application focuses on validating the **core interaction loop**:

1. Display a chemical
2. Select the correct hazard symbols
3. Provide feedback
4. Track score
5. Progress to the next chemical

Future iterations could expand the dataset, introduce scoring tiers, animations, or persistent score tracking.

---

## Gameplay

### Rules

1. Click the correct **GHS hazard symbols** for the displayed chemical.
2. Some chemicals may have **multiple hazard symbols**.
3. If a chemical has **no hazard classification**, click **"No GHS Symbol"**.
4. Correct selections are highlighted in **green**.
5. Incorrect selections are highlighted in **red**.
6. Each correct answer increases the score.
7. The game ends after **two incorrect questions**.

---

## Screens

### Gameplay Screen

Displays:

- Chemical name and formula
- Hazard pictograms
- "No GHS Symbol" option
- Current score

### Game Over Screen

Displays:

- Final score
- Restart button
- Automatic exit after 10 seconds

---

## Technical Design

### Object-Oriented Architecture

The game separates responsibilities into classes:

**GHSSymbol**

Handles:

- Rendering pictograms
- Click detection
- Highlight states
- Temporary and persistent visual feedback

**ChemistryGame**

Controls:

- Game state
- UI rendering
- Event handling
- Score tracking
- Question progression

This structure improves readability, extensibility, and testing.

---

### Data-Driven Chemical Database

Chemical information is stored externally in:

```

chemicals.json

```

Each entry contains:

```json
{
"name": "Sulfuric acid",
"formula": "H2SO4",
"ghs": ["Corrosive", "Health Hazard"]
}