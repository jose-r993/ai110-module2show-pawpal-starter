from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete():
    task = Task(title="Walk", duration_minutes=20, priority="high")
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="medium"))
    assert len(pet.get_tasks()) == 1


def test_sort_by_time_orders_chronologically():
    owner = Owner(name="Jordan", available_time_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task(title="Late task", duration_minutes=10, priority="high", start_time="10:00"))
    pet.add_task(Task(title="Early task", duration_minutes=10, priority="low", start_time="07:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    scheduler.sort_by_time()

    times = [task.start_time for _, task in scheduler.scheduled_tasks]
    assert times == sorted(times)


def test_recurring_task_readded_after_complete():
    owner = Owner(name="Jordan", available_time_minutes=60)
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(title="Walk", duration_minutes=20, priority="high", frequency="daily")
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(pet, task)

    tasks = pet.get_tasks()
    assert task.completed is True
    assert len(tasks) == 2
    assert tasks[-1].completed is False


def test_non_recurring_task_not_readded():
    owner = Owner(name="Jordan", available_time_minutes=60)
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(title="Vet visit", duration_minutes=60, priority="high", frequency="none")
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(pet, task)

    assert len(pet.get_tasks()) == 1


def test_conflict_detection_flags_same_time():
    owner = Owner(name="Jordan", available_time_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high", start_time="08:00"))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high", start_time="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_no_conflict_when_times_differ():
    owner = Owner(name="Jordan", available_time_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high", start_time="08:00"))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high", start_time="09:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 0


def test_pet_with_no_tasks_produces_empty_schedule():
    owner = Owner(name="Jordan", available_time_minutes=60)
    pet = Pet(name="Luna", species="cat", age=2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.generate_schedule()

    assert result == []


def test_filter_by_pet_name():
    owner = Owner(name="Jordan", available_time_minutes=120)
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=2)
    mochi.add_task(Task(title="Walk", duration_minutes=20, priority="high"))
    luna.add_task(Task(title="Brushing", duration_minutes=10, priority="low"))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    results = scheduler.filter_tasks(pet_name="Mochi")

    assert len(results) == 1
    assert results[0][1].title == "Walk"
