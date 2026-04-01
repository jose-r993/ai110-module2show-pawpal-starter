from dataclasses import dataclass, field


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """A single pet care activity."""
    title: str
    duration_minutes: int
    priority: str
    category: str = ""
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True


class Pet:
    """Stores pet info and its list of care tasks."""

    def __init__(self, name, species, age, health_notes=""):
        self.name = name
        self.species = species
        self.age = age
        self.health_notes = health_notes
        self.tasks = []

    def add_task(self, task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks

    def remove_task(self, task_title):
        """Remove a task by title."""
        self.tasks = [t for t in self.tasks if t.title != task_title]


class Owner:
    """Manages owner info and their pets."""

    def __init__(self, name, available_time_minutes, preferences=None):
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.preferences = preferences or []
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pets(self):
        """Return all pets belonging to this owner."""
        return self.pets

    def set_available_time(self, minutes):
        """Update how much time the owner has today."""
        self.available_time_minutes = minutes


class Scheduler:
    """Builds a daily care plan from all tasks across an owner's pets."""

    def __init__(self, owner):
        self.owner = owner
        self.scheduled_tasks = []

    def prioritize_tasks(self, tasks):
        """Sort tasks by priority (high first) then by duration."""
        sorted_tasks = sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes))
        return sorted_tasks

    def generate_schedule(self):
        """Fill the schedule with tasks that fit within the owner's available time."""
        all_pairs = []
        for pet in self.owner.get_pets():
            for task in pet.get_tasks():
                all_pairs.append((pet, task))

        all_pairs.sort(key=lambda pair: (PRIORITY_ORDER.get(pair[1].priority, 99), pair[1].duration_minutes))

        self.scheduled_tasks = []
        time_used = 0

        for pet, task in all_pairs:
            if time_used + task.duration_minutes <= self.owner.available_time_minutes:
                self.scheduled_tasks.append((pet, task))
                time_used += task.duration_minutes

        return self.scheduled_tasks

    def explain_plan(self):
        """Return a readable summary of the scheduled tasks."""
        if not self.scheduled_tasks:
            return "No tasks scheduled."

        total = sum(task.duration_minutes for _, task in self.scheduled_tasks)
        lines = [f"Daily plan for {self.owner.name} ({total} min total)\n"]

        for pet, task in self.scheduled_tasks:
            lines.append(f"  [{task.priority.upper()}] {task.title} - {task.duration_minutes} min ({pet.name})")

        return "\n".join(lines)
