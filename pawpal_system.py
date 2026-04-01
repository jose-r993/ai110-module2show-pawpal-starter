from dataclasses import dataclass, replace


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """A single pet care activity."""
    title: str
    duration_minutes: int
    priority: str
    category: str = ""
    completed: bool = False
    start_time: str = ""
    frequency: str = "none"

    def mark_complete(self):
        """Mark this task done. Returns a new Task if it recurs, otherwise None."""
        self.completed = True
        if self.frequency != "none":
            return replace(self, completed=False)
        return None


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
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes))

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

    def sort_by_time(self):
        """Sort scheduled tasks by start_time. Tasks with no start_time go last."""
        self.scheduled_tasks.sort(key=lambda pair: pair[1].start_time if pair[1].start_time else "99:99")
        return self.scheduled_tasks

    def filter_tasks(self, pet_name=None, completed=None):
        """Return tasks filtered by pet name and/or completion status."""
        results = []
        for pet in self.owner.get_pets():
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                results.append((pet, task))
        return results

    def detect_conflicts(self):
        """Return a list of warnings for tasks scheduled at the same time."""
        warnings = []
        seen = {}
        for pet, task in self.scheduled_tasks:
            if not task.start_time:
                continue
            if task.start_time in seen:
                other_pet, other_task = seen[task.start_time]
                warnings.append(
                    f"Conflict at {task.start_time}: '{task.title}' ({pet.name}) and '{other_task.title}' ({other_pet.name})"
                )
            else:
                seen[task.start_time] = (pet, task)
        return warnings

    def mark_task_complete(self, pet, task):
        """Mark a task complete and re-add it to the pet if it recurs."""
        new_task = task.mark_complete()
        if new_task is not None:
            pet.add_task(new_task)

    def explain_plan(self):
        """Return a readable summary of the scheduled tasks."""
        if not self.scheduled_tasks:
            return "No tasks scheduled."

        total = sum(task.duration_minutes for _, task in self.scheduled_tasks)
        lines = [f"Daily plan for {self.owner.name} ({total} min total)\n"]

        for pet, task in self.scheduled_tasks:
            time_label = f" @ {task.start_time}" if task.start_time else ""
            lines.append(f"  [{task.priority.upper()}] {task.title} - {task.duration_minutes} min ({pet.name}){time_label}")

        return "\n".join(lines)
