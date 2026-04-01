# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

The scheduler includes a few extra features beyond a basic priority sort:

- **Sort by time** — tasks with a `start_time` (HH:MM) get ordered chronologically. Tasks without one go last.
- **Filter tasks** — filter by pet name or completion status to get a focused view of what's done or pending.
- **Recurring tasks** — tasks with `frequency="daily"` or `frequency="weekly"` automatically re-add themselves when marked complete.
- **Conflict detection** — the scheduler scans for tasks assigned to the same start time and returns a warning instead of crashing.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests cover:

- Marking a task complete updates its status
- Adding a task to a pet increases the task count
- Tasks sort into chronological order by start time
- Daily tasks re-add themselves after being marked complete
- One-off tasks do not re-add after completion
- Conflict detection flags two tasks at the same time
- No false conflict warnings when times are different
- A pet with no tasks produces an empty schedule
- Filtering by pet name returns only that pet's tasks

Confidence level: ★★★★☆ — core behaviors are well covered. Overlapping duration conflicts and multi-day scheduling are not tested yet.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
