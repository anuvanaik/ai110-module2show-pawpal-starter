from pawpal_system import Task, Pet, Owner, Scheduler

# --- Tasks ---
# task_type/frequency values match the options offered in app.py's Streamlit UI
# (diet, medical, enrichment, exercise, other / daily, weekly, as-needed).
morning_walk = Task(
    task_type="enrichment",
    description="Morning walk around the block",
    time="7:00 AM",
    frequency="daily",
)

lunch_meds = Task(
    task_type="medical",
    description="Give allergy pill with food",
    time="12:00 PM",
    frequency="daily",
)

evening_feed = Task(
    task_type="diet",
    description="Serve measured dinner portion",
    time="6:00 PM",
    frequency="daily",
)

# Scheduled at the same time as morning_walk on purpose, to demonstrate conflict detection.
ear_drops = Task(
    task_type="medical",
    description="Give ear drops",
    time="7:00 AM",
    frequency="daily",
)

# --- Pets ---
luna = Pet(
    name="Luna",
    breed="Golden Retriever",
    diet_needs="2 cups kibble twice daily",
    med_needs="Allergy pill with lunch",
    enrichment_needs="1 hour exercise daily",
)
# Tasks added out of chronological order (evening before morning) to
# demonstrate that the scheduler sorts by time regardless of insertion order.
luna.tasks = [evening_feed, morning_walk]

mochi = Pet(
    name="Mochi",
    breed="Shih Tzu",
    diet_needs="1 cup kibble twice daily",
    med_needs="None",
    enrichment_needs="Short walks and indoor play",
)
mochi.tasks = [lunch_meds]

# --- Owner ---
owner_name = "Alex"
alex = Owner(
    time_availability="Mornings and evenings",
    owner_preferences=["No tasks before 7 AM", "Group tasks when possible"],
    pets=[luna, mochi],
)

# --- Scheduling a Task ---
# Mirrors app.py's "Schedule Task" flow: check_conflict() runs before the task is
# added, so the same-time clash with morning_walk (both 7:00 AM) is flagged here.
print("Scheduling Luna's ear drops...")
conflict_message = Scheduler.check_conflict(luna, ear_drops)
luna.add_task(ear_drops)
if conflict_message:
    # check_conflict() prefixes its message with an emoji for the Streamlit UI;
    # strip it here since this console doesn't support the character.
    print(f"  [WARNING] {conflict_message.removeprefix('⚠️ ')}")

# --- Scheduler ---
scheduler = Scheduler(schedule_name=f"{owner_name}'s Daily Plan")
scheduler.create_plan(alex)
task_to_pet = {id(task): pet for pet in alex.pets for task in pet.tasks}

# --- Print Today's Schedule ---
# Mirrors the "Generate schedule" output in app.py: same ordering, conflict
# warnings, prioritization reasoning, and availability check.
print("=" * 40)
print("        TODAY'S SCHEDULE - PawPal+")
print(f"Owner: {owner_name}  |  Available: {alex.time_availability}")
print("=" * 40)

conflicts = scheduler.find_conflicts(alex)
if conflicts:
    for conflict in conflicts:
        print(
            f"  [CONFLICT] {conflict['pet']} has two tasks scheduled at {conflict['time']}: "
            f"{', '.join(conflict['descriptions'])}"
        )

reason_by_rank = {
    1: lambda pet: f"matches one of {pet.name}'s core needs (diet/medical/enrichment)",
    2: lambda pet: f"matches {owner_name}'s stated preference",
    3: lambda pet: "general task, no specific match",
}

for task in scheduler.organize_tasks():
    pet = task_to_pet[id(task)]
    status = "Done" if task.is_complete else "Pending"
    rank = task.prioritize(pet, alex)
    print(f"  [{status}] {task.time} — {pet.name}: {task.task_type}: {task.description}")
    print(f"           Why: {reason_by_rank[rank](pet)}")
    if not scheduler.fit_task_by_availability(task, alex):
        print("           [WARNING] outside your available window")

print("\nUpcoming Reminders")
reminders = scheduler.remind_owner(alex)
if reminders:
    for task in reminders:
        pet = task_to_pet[id(task)]
        print(f"  - {task.time} — {pet.name}: {task.description}")
else:
    print("  No pending tasks.")

# --- Demonstrate recurring tasks: completing a "daily" task stays visible as Done ---
print("\nCompleting Luna's morning walk (daily)...")
Scheduler.mark_task_complete(morning_walk)
print(f"Luna now has {len(luna.tasks)} task(s):")
for task in scheduler.sort_by_time(luna.tasks):
    status = "Done" if task.is_complete else "Pending"
    print(f"  [{status}] {task.time} — {task.task_type}: {task.description}")

# --- Building the next plan rolls the completed daily task into its next occurrence ---
print("\nGenerating a new plan...")
scheduler.create_plan(alex)
print(f"Luna now has {len(luna.tasks)} task(s):")
for task in scheduler.sort_by_time(luna.tasks):
    status = "Done" if task.is_complete else "Pending"
    print(f"  [{status}] {task.time} — {task.task_type}: {task.description}")
