from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: str = ""
    completed: bool = False

    def mark_complete(self):
        pass


class Pet:
    def __init__(self, name, species, age, health_notes=""):
        self.name = name
        self.species = species
        self.age = age
        self.health_notes = health_notes
        self.tasks = []

    def add_task(self, task):
        pass

    def get_tasks(self):
        pass

    def remove_task(self, task_title):
        pass


class Owner:
    def __init__(self, name, available_time_minutes, preferences=None):
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.preferences = preferences or []
        self.pets = []

    def add_pet(self, pet):
        pass

    def get_pets(self):
        pass

    def set_available_time(self, minutes):
        pass


class Scheduler:
    def __init__(self, owner, pet):
        self.owner = owner
        self.pet = pet
        self.scheduled_tasks = []

    def prioritize_tasks(self, tasks):
        pass

    def generate_schedule(self):
        pass

    def explain_plan(self):
        pass
