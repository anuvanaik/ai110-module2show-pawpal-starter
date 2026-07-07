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

# --- Pets ---
luna = Pet(
    name="Luna",
    breed="Golden Retriever",
    diet_needs="2 cups kibble twice daily",
    med_needs="Allergy pill with lunch",
    enrichment_needs="1 hour exercise daily",
)
luna.tasks = [morning_walk, evening_feed]

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
scheduler.tasks = luna.tasks + mochi.tasks

# --- Print Today's Schedule ---
print("=" * 40)
print("        TODAY'S SCHEDULE - PawPal+")
print("=" * 40)

for pet in alex.pets:
    print(f"\n{pet.name} ({pet.breed})")
    print("-" * 30)
    for task in pet.tasks:
        status = "Done" if task.is_complete else "Pending"
        print(f"  [{status}] {task.time} — {task.task_type}: {task.description}")

print("\n" + "=" * 40)
print(f"Owner: Alex  |  Available: {alex.time_availability}")
print("=" * 40)
