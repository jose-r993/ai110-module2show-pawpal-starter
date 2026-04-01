from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner(name="Jordan", available_time_minutes=90)

mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", category="exercise", start_time="08:00", frequency="daily"))
mochi.add_task(Task(title="Feeding", duration_minutes=10, priority="high", category="nutrition", start_time="09:00"))
mochi.add_task(Task(title="Fetch in yard", duration_minutes=20, priority="medium", category="exercise", start_time="08:00"))

luna.add_task(Task(title="Brushing", duration_minutes=15, priority="low", category="grooming", start_time="10:00"))
luna.add_task(Task(title="Medication", duration_minutes=5, priority="high", category="health", start_time="09:30"))

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner)
scheduler.generate_schedule()

print("--- Sorted by time ---")
scheduler.sort_by_time()
print(scheduler.explain_plan())

print("\n--- Conflict detection ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")

print("\n--- Mochi's tasks only ---")
for pet, task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {task.title} ({task.priority})")

print("\n--- Recurring task demo ---")
walk = mochi.get_tasks()[0]
print(f"  Before: '{walk.title}' completed={walk.completed}, frequency={walk.frequency}")
scheduler.mark_task_complete(mochi, walk)
print(f"  After mark_complete: completed={walk.completed}")
print(f"  New recurring task added: '{mochi.get_tasks()[-1].title}' completed={mochi.get_tasks()[-1].completed}")
