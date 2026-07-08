from pawpal_system import Task, Pet, Owner, Scheduler

# --- Tasks ---
morning_walk = Task(
    task_type="Enrichment",
    description="Morning walk around the block",
    time="7:00 AM",
    frequency="Daily",
)

lunch_meds = Task(
    task_type="Medication",
    description="Give allergy pill with food",
    time="12:00 PM",
    frequency="Daily",
)

evening_feed = Task(
    task_type="Diet",
    description="Serve measured dinner portion",
    time="6:00 PM",
    frequency="Daily",
)

# Scheduled at the same time as morning_walk on purpose, to demonstrate conflict detection.
ear_drops = Task(
    task_type="Medication",
    description="Give ear drops",
    time="7:00 AM",
    frequency="Daily",
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
luna.tasks = [evening_feed, ear_drops, morning_walk]

mochi = Pet(
    name="Mochi",
    breed="Shih Tzu",
    diet_needs="1 cup kibble twice daily",
    med_needs="None",
    enrichment_needs="Short walks and indoor play",
)
mochi.tasks = [lunch_meds]

# --- Owner ---
alex = Owner(
    time_availability="Mornings and evenings",
    owner_preferences=["No tasks before 7 AM", "Group tasks when possible"],
    pets=[luna, mochi],
)

# --- Scheduler ---
scheduler = Scheduler(schedule_name="Alex's Daily Plan")
scheduler.create_plan(alex)
task_to_pet = {id(task): pet for pet in alex.pets for task in pet.tasks}

# --- Print Today's Schedule (sorted by time, not insertion order) ---
print("=" * 40)
print("        TODAY'S SCHEDULE - PawPal+")
print("=" * 40)

for task in scheduler.organize_tasks():
    pet = task_to_pet[id(task)]
    status = "Done" if task.is_complete else "Pending"
    print(f"  [{status}] {task.time} — {pet.name}: {task.task_type}: {task.description}")

print("\n" + "=" * 40)
print(f"Owner: Alex  |  Available: {alex.time_availability}")
print("=" * 40)

# --- Verify the Scheduler catches the double-booked 7:00 AM slot ---
print("\nChecking for scheduling conflicts...")
conflicts = scheduler.find_conflicts(alex)
if conflicts:
    for conflict in conflicts:
        print(
            f"  [CONFLICT] {conflict['pet']} has two tasks scheduled at {conflict['time']}: "
            f"{', '.join(conflict['descriptions'])}"
        )
else:
    print("  No conflicts found.")

# --- Demonstrate recurring tasks: completing a "Daily" task stays visible as Done ---
print("\nCompleting Luna's morning walk (Daily)...")
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
