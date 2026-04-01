import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.subheader("Owner & Pet Info")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
available_time = st.number_input("Available time today (minutes)", min_value=10, max_value=480, value=90)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time_minutes=available_time)
    st.session_state.pet = Pet(name=pet_name, species=species, age=0)
    st.session_state.owner.add_pet(st.session_state.pet)

st.divider()

st.subheader("Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    start_time = st.text_input("Start time (HH:MM, optional)", value="")
with col5:
    frequency = st.selectbox("Frequency", ["none", "daily", "weekly"])

if st.button("Add task"):
    new_task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority,
        start_time=start_time.strip(),
        frequency=frequency,
    )
    st.session_state.pet.add_task(new_task)

current_tasks = st.session_state.pet.get_tasks()
if current_tasks:
    st.write("Current tasks:")
    task_rows = [
        {
            "title": t.title,
            "duration (min)": t.duration_minutes,
            "priority": t.priority,
            "start time": t.start_time or "-",
            "frequency": t.frequency,
        }
        for t in current_tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    st.session_state.owner.set_available_time(available_time)
    scheduler = Scheduler(st.session_state.owner)
    scheduler.generate_schedule()
    scheduler.sort_by_time()

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts found.")

    if scheduler.scheduled_tasks:
        schedule_rows = [
            {
                "task": task.title,
                "pet": pet.name,
                "priority": task.priority,
                "duration (min)": task.duration_minutes,
                "start time": task.start_time or "-",
                "recurring": task.frequency,
            }
            for pet, task in scheduler.scheduled_tasks
        ]
        st.table(schedule_rows)
        total = sum(t.duration_minutes for _, t in scheduler.scheduled_tasks)
        st.caption(f"Total time: {total} min of {available_time} min available")
    else:
        st.info("No tasks fit in the available time.")
