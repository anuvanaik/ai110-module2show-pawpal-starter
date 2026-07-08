import streamlit as st

from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
time_availability = st.text_input(
    "Owner time availability", value="morning", help="Used to match tasks to when the owner is free."
)
owner_preferences_raw = st.text_input("Owner preferences (comma-separated)", value="walk, playtime")

st.divider()

st.subheader("Adding a Pet")

if "pets" not in st.session_state:
    st.session_state.pets = []

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Shiba Inu")
with col2:
    diet_needs = st.text_input("Diet needs", value="grain-free food")
    med_needs = st.text_input("Medical needs", value="daily allergy medication")
    enrichment_needs = st.text_input("Enrichment needs", value="puzzle toy")

if st.button("Add Pet"):
    st.session_state.pets.append(
        Pet(
            name=pet_name,
            breed=breed,
            diet_needs=diet_needs,
            med_needs=med_needs,
            enrichment_needs=enrichment_needs,
        )
    )

if st.session_state.pets:
    st.write("Pets added so far:")
    for pet in st.session_state.pets:
        st.write(f"- **{pet.name}** ({pet.breed}) — {len(pet.tasks)} task(s) scheduled")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Scheduling a Task")

if not st.session_state.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    pet_index = st.selectbox(
        "Pet",
        options=range(len(st.session_state.pets)),
        format_func=lambda i: st.session_state.pets[i].name,
    )
    selected_pet = st.session_state.pets[pet_index]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_type = st.selectbox("Task type", ["diet", "medical", "enrichment", "exercise", "other"])
    with col2:
        description = st.text_input("Description", value="grain-free food")
    with col3:
        task_time = st.time_input("Time")
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])

    if st.button("Schedule Task"):
        new_task = Task(
            task_type=task_type,
            description=description,
            time=task_time.strftime("%I:%M %p"),
            frequency=frequency,
        )
        conflict_message = Scheduler.check_conflict(selected_pet, new_task)
        selected_pet.add_task(new_task)
        if conflict_message:
            st.warning(conflict_message)

    if selected_pet.tasks:
        st.write(f"Tasks scheduled for {selected_pet.name}:")
        for t in selected_pet.tasks:
            cols = st.columns([2, 3, 2, 2, 2])
            cols[0].write(t.task_type)
            cols[1].write(t.description)
            cols[2].write(t.time)
            cols[3].write(t.frequency)
            if t.is_complete:
                cols[4].write("✅ Done")
            elif cols[4].button("Mark complete", key=f"complete-{id(t)}"):
                Scheduler.mark_task_complete(t)
                st.rerun()
    else:
        st.info(f"No tasks scheduled for {selected_pet.name} yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("Combines every pet added above into one owner and runs the scheduler.")

if st.button("Generate schedule"):
    if not st.session_state.pets:
        st.warning("Add at least one pet (with tasks) before generating a schedule.")
    else:
        owner_preferences = [p.strip() for p in owner_preferences_raw.split(",") if p.strip()]
        owner = Owner(time_availability=time_availability, owner_preferences=owner_preferences)
        for pet in st.session_state.pets:
            owner.add_pet(pet)

        scheduler = Scheduler(schedule_name=f"{owner_name}'s Daily Plan")
        scheduler.create_plan(owner)
        ordered_tasks = scheduler.organize_tasks()

        if not ordered_tasks:
            st.warning("None of the added pets have tasks scheduled yet.")
        else:
            task_to_pet = {id(task): pet for pet in owner.pets for task in pet.tasks}
            reason_by_rank = {
                1: lambda pet: f"matches one of {pet.name}'s core needs (diet/medical/enrichment)",
                2: lambda pet: f"matches {owner_name}'s stated preference",
                3: lambda pet: "general task, no specific match",
            }

            for conflict in scheduler.find_conflicts(owner):
                st.warning(
                    f"⚠️ {conflict['pet']} has two tasks scheduled at {conflict['time']}: "
                    f"{', '.join(conflict['descriptions'])}"
                )

            st.success(f"Schedule generated for {owner_name}")
            for task in ordered_tasks:
                pet = task_to_pet[id(task)]
                rank = task.prioritize(pet, owner)
                availability_note = ""
                if not scheduler.fit_task_by_availability(task, owner):
                    availability_note = "  \n⚠️ outside your available window"
                st.markdown(
                    f"**{task.time}** — {pet.name}: {task.description} "
                    f"({task.task_type}, {task.frequency})  \n"
                    f"_Why: {reason_by_rank[rank](pet)}_"
                    f"{availability_note}"
                )

            reminders = scheduler.remind_owner(owner)
            if reminders:
                st.subheader("Upcoming Reminders")
                for task in reminders:
                    pet = task_to_pet[id(task)]
                    st.write(f"- **{task.time}** — {pet.name}: {task.description}")
