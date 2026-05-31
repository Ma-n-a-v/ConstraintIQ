# ConstraintIQ

> Pure algorithm based (No AI wrapper) Sudoku Solver Visualization Platform using CSP, AC3, MRV, LCV, and Backtracking Algorithms

ConstraintIQ is an interactive Sudoku-solving visualization platform built with Python and Django.
The project demonstrates how different Constraint Satisfaction Problem (CSP) algorithms solve Sudoku puzzles in real time through animated decision tracing, live code visualization, and algorithmic reasoning.

Unlike traditional Sudoku solvers that instantly output the final solution, ConstraintIQ focuses on showing *how the AI thinks* while solving the puzzle.

---

# Features

## Real-Time AI Visualization

* Watch the solver make decisions live
* See assignments, backtracking, and constraint propagation
* Interactive algorithm animation system

## Multiple CSP Algorithms

Implemented algorithms include:

* Backtracking
* AC3 + Backtracking
* AC3 + LCV
* AC3 + MRV
* AC3 + MRV + LCV

## Live Decision Trace

ConstraintIQ explains solver reasoning using natural-language AI traces such as:

```txt
MRV selected row 4, column 7 because it has only 2 legal values remaining.

LCV prioritized values from least restrictive to most restrictive.

AI backtracked because this path led to a contradiction.
```

## Interactive Dashboard

* Live Sudoku board
* Algorithm controls
* Dynamic code visualization
* Step counter
* Backtrack counter
* Runtime metrics

## Developer-Focused UI

Inspired by:

* VSCode
* Linear
* Raycast
* Modern developer tools

---

# Tech Stack

## Backend

* Python
* Django

## Frontend

* HTML
* CSS
* JavaScript

## AI / CSP Concepts

* Constraint Satisfaction Problems
* Arc Consistency
* Recursive Backtracking
* Heuristic Search
* Constraint Propagation

---

# Project Structure

```txt
ConstraintIQ/
│
├── config/
│
├── solver/
│   ├── algorithms/
│   │   ├── ac3.py
│   │   ├── backtracking.py
│   │   ├── heuristics.py
│   │   ├── metrics.py
│   │   └── sudoku_solver.py
│   │
│   ├── templates/
│   │   └── solver/
│   │       └── index.html
│   │
│   ├── views.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# Algorithms Explained

# 1. Backtracking

Backtracking is the foundational recursive search algorithm used to solve Sudoku.

The solver:

1. Finds the next empty cell
2. Tries values from 1–9
3. Checks if the value is valid
4. Recursively continues
5. Backtracks if a contradiction occurs

### Pseudocode

```python
def backtrack(cell):

    if all cells solved:
        return True

    select next empty cell

    for value in 1..9:

        if value is valid:

            place value

            if backtrack(next):
                return True

            remove value  # backtrack

    return False
```

### Characteristics

* Complete search algorithm
* Guarantees solution if one exists
* Can become computationally expensive on difficult puzzles

---

# 2. AC3 (Arc Consistency Algorithm)

AC3 is a constraint propagation algorithm used to reduce possible values before search begins.

Instead of blindly trying numbers, AC3 removes values from domains that violate Sudoku constraints.

### Example

If:

* Row already contains 5
* Column already contains 5
* Box already contains 5

Then 5 is removed from that cell’s domain.

### Benefits

* Reduces search space
* Improves efficiency
* Minimizes unnecessary backtracking

---

# 3. MRV (Minimum Remaining Values)

MRV selects the most constrained variable first.

Instead of randomly selecting an empty cell:

```txt
Choose the cell with the fewest legal values remaining.
```

### Why it works

A highly constrained cell is more likely to fail early.

This reduces:

* Search depth
* Branching factor
* Total recursive calls

### Example

```txt
Cell A → {1,2,3,4}
Cell B → {7}

MRV selects Cell B first.
```

---

# 4. LCV (Least Constraining Value)

LCV chooses the value that restricts neighboring cells the least.

### Goal

Leave as many future possibilities open as possible.

### Example

If:

* Value 4 removes many neighbor options
* Value 7 removes very few

LCV tries 7 first.

### Benefits

* Reduces future conflicts
* Produces smoother search paths
* Minimizes backtracking

---

# 5. AC3 + MRV + LCV

This is the most optimized solver implemented in ConstraintIQ.

It combines:

* Constraint propagation (AC3)
* Smart variable selection (MRV)
* Smart value ordering (LCV)

### Solving Pipeline

```txt
1. Apply AC3
2. Select most constrained cell (MRV)
3. Order values intelligently (LCV)
4. Assign value
5. Propagate constraints again
6. Continue recursively
```

### Outcome

* Fastest solving strategy
* Fewest backtracks
* Strongest pruning capability

---

# AI Decision Trace System

ConstraintIQ includes a custom AI reasoning engine that converts algorithmic decisions into human-readable explanations.

### Example Trace

```txt
AI selected row 3, column 5 as the next empty cell.

MRV selected row 6, column 2 because it has only 2 legal values remaining.

LCV prioritized values from least restrictive to most restrictive.

AI backtracked because this path caused a contradiction.
```

This makes the platform educational and visually explainable.

---

# Metrics Tracked

ConstraintIQ tracks:

* Total steps
* Assignments
* Backtracks
* Recursive calls
* Constraint reductions
* Solve time

These metrics help compare algorithm efficiency visually.

---

# How to Run Locally

# 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ConstraintIQ.git
```

# 2. Move Into Project

```bash
cd ConstraintIQ
```

# 3. Create Virtual Environment

```bash
python -m venv venv
```

# 4. Activate Virtual Environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

# 5. Install Dependencies

```bash
pip install -r requirements.txt
```

# 6. Run Server

```bash
python manage.py runserver
```

# 7. Open Browser

```txt
http://127.0.0.1:8000
```

---

# Future Improvements

This project is just for the demonstration purposes.
This will help user to understand how AI thinks using algorithms.
We might have come across these algorithms in our daily lives.

Planned upgrades include:

* Live recursive tree visualization
* Domain heatmaps
* Constraint graph visualization
* Algorithm benchmarking charts
* Puzzle difficulty analysis
* Sudoku generation engine
* AI difficulty prediction
* WebSocket live streaming
* Multiplayer solving race mode

---

# Why This Project Matters

ConstraintIQ is not just a Sudoku solver.

It demonstrates:

* Artificial Intelligence concepts
* Constraint Satisfaction Problems
* Heuristic optimization
* Search algorithms
* Interactive visualization
* Full-stack development
* Educational AI interfaces

This project combines:

* AI
* algorithms
* visualization
* software engineering
* frontend interaction

into one portfolio-ready system.

---

# Author

Manav B. Patel


Interested in:

* Artificial Intelligence
* Machine Learning
* Full-Stack Development
* Algorithm Visualization
* Software Engineering

---
