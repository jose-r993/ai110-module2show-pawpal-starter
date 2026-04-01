from pawpal_system import Task, Pet


def test_mark_complete():
    task = Task(title="Walk", duration_minutes=20, priority="high")
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="medium"))
    assert len(pet.get_tasks()) == 1
