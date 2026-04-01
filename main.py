from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner(name="Jordan", available_time_minutes=90)

mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", category="exercise"))
mochi.add_task(Task(title="Feeding", duration_minutes=10, priority="high", category="nutrition"))
mochi.add_task(Task(title="Fetch in yard", duration_minutes=20, priority="medium", category="exercise"))

luna.add_task(Task(title="Brushing", duration_minutes=15, priority="low", category="grooming"))
luna.add_task(Task(title="Medication", duration_minutes=5, priority="high", category="health"))

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner)
scheduler.generate_schedule()

print(scheduler.explain_plan())
