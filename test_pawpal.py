from pawpal_system import Task, Pet, Owner, Scheduler


def test_check_conflict_returns_warning_for_clashing_time():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    pet.add_task(Task(task_type="Enrichment", description="Morning walk", time="7:00 AM", frequency="Daily"))
    new_task = Task(task_type="Medical", description="Give pill", time="7:00 AM", frequency="Daily")

    message = Scheduler.check_conflict(pet, new_task)

    assert message is not None
    assert "Morning walk" in message


def test_check_conflict_returns_none_when_no_clash():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    pet.add_task(Task(task_type="Enrichment", description="Morning walk", time="7:00 AM", frequency="Daily"))
    new_task = Task(task_type="Diet", description="Dinner", time="6:00 PM", frequency="Daily")

    assert Scheduler.check_conflict(pet, new_task) is None


def test_mark_complete_changes_status():
    task = Task(
        task_type="Enrichment",
        description="Morning walk",
        time="7:00 AM",
        frequency="Daily",
    )
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    task = Task(
        task_type="Diet",
        description="Serve dinner",
        time="6:00 PM",
        frequency="Daily",
    )
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_mark_task_complete_keeps_task_visible_as_done():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    task = Task(
        task_type="Enrichment",
        description="Morning walk",
        time="7:00 AM",
        frequency="Daily",
    )
    pet.add_task(task)

    Scheduler.mark_task_complete(task)

    assert task.is_complete is True
    assert pet.tasks == [task]


def test_roll_over_completed_tasks_replaces_recurring_task_with_next_occurrence():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    task = Task(
        task_type="Enrichment",
        description="Morning walk",
        time="7:00 AM",
        frequency="Daily",
    )
    pet.add_task(task)
    Scheduler.mark_task_complete(task)
    owner = Owner(time_availability="morning", pets=[pet])

    Scheduler(schedule_name="test").roll_over_completed_tasks(owner)

    assert len(pet.tasks) == 1
    next_task = pet.tasks[0]
    assert next_task is not task
    assert next_task.is_complete is False
    assert next_task.time == task.time
    assert next_task.frequency == task.frequency
    assert task not in pet.tasks


def test_roll_over_completed_tasks_drops_non_recurring_task():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    task = Task(
        task_type="Medical",
        description="Vet visit",
        time="3:00 PM",
        frequency="as-needed",
    )
    pet.add_task(task)
    Scheduler.mark_task_complete(task)
    owner = Owner(time_availability="morning", pets=[pet])

    Scheduler(schedule_name="test").roll_over_completed_tasks(owner)

    assert pet.tasks == []


# --- Sorting correctness ---


def test_sort_by_time_returns_chronological_order_regardless_of_insertion_order():
    evening = Task(task_type="Diet", description="Dinner", time="6:00 PM", frequency="Daily")
    morning = Task(task_type="Enrichment", description="Walk", time="7:00 AM", frequency="Daily")
    midday = Task(task_type="Medical", description="Pill", time="12:00 PM", frequency="Daily")

    ordered = Scheduler(schedule_name="test").sort_by_time([evening, morning, midday])

    assert ordered == [morning, midday, evening]


def test_sort_by_time_places_unparseable_times_last():
    valid = Task(task_type="Diet", description="Dinner", time="6:00 PM", frequency="Daily")
    invalid = Task(task_type="Enrichment", description="Whenever", time="not a time", frequency="Daily")

    ordered = Scheduler(schedule_name="test").sort_by_time([invalid, valid])

    assert ordered == [valid, invalid]


def test_organize_tasks_returns_all_pets_tasks_in_chronological_order():
    luna = Pet(name="Luna", breed="x", diet_needs="", med_needs="", enrichment_needs="")
    luna.tasks = [
        Task(task_type="Diet", description="Dinner", time="6:00 PM", frequency="Daily"),
        Task(task_type="Enrichment", description="Walk", time="7:00 AM", frequency="Daily"),
    ]
    mochi = Pet(name="Mochi", breed="x", diet_needs="", med_needs="", enrichment_needs="")
    mochi.tasks = [Task(task_type="Medical", description="Pill", time="12:00 PM", frequency="Daily")]
    owner = Owner(time_availability="morning", pets=[luna, mochi])
    scheduler = Scheduler(schedule_name="test")
    scheduler.create_plan(owner)

    ordered_times = [task.time for task in scheduler.organize_tasks()]

    assert ordered_times == ["7:00 AM", "12:00 PM", "6:00 PM"]


# --- Prioritization matching ---


def test_prioritize_ranks_pet_need_match_highest():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="Allergy pill",
        enrichment_needs="1 hour exercise",
    )
    owner = Owner(time_availability="morning", owner_preferences=["Group tasks when possible"])
    task = Task(task_type="Medical", description="Allergy pill", time="12:00 PM", frequency="Daily")

    assert task.prioritize(pet, owner) == 1


def test_prioritize_ranks_owner_preference_when_no_pet_need_matches():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="Allergy pill",
        enrichment_needs="1 hour exercise",
    )
    owner = Owner(time_availability="morning", owner_preferences=["Group tasks when possible"])
    task = Task(task_type="Enrichment", description="Group tasks when possible", time="7:00 AM", frequency="Daily")

    assert task.prioritize(pet, owner) == 2


def test_prioritize_falls_back_to_general_when_no_match():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="Allergy pill",
        enrichment_needs="1 hour exercise",
    )
    owner = Owner(time_availability="morning", owner_preferences=["Group tasks when possible"])
    task = Task(task_type="Enrichment", description="Belly rubs", time="7:00 AM", frequency="Daily")

    assert task.prioritize(pet, owner) == 3


def test_prioritize_is_case_and_whitespace_sensitive():
    """Matching is exact string equality, so a near-match (case/whitespace) should
    NOT be promoted to rank 1/2 - it should silently fall through to rank 3."""
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="Allergy pill",
        enrichment_needs="1 hour exercise",
    )
    owner = Owner(time_availability="morning", owner_preferences=[])
    task = Task(task_type="Medical", description=" allergy pill ", time="12:00 PM", frequency="Daily")

    assert task.prioritize(pet, owner) == 3


# --- id()-based task lookup (main.py / app.py build task_to_pet via id(task)) ---


def test_stale_id_based_task_lookup_becomes_invalid_after_rollover():
    """main.py and app.py map id(task) -> pet to look up which pet a task belongs to.
    Once create_plan() rolls a completed recurring task into its next occurrence, the
    old id key no longer corresponds to any live task. A stale map must be rebuilt
    after every create_plan() call - reusing it risks misattributing a task to the
    wrong pet if Python later reuses the freed id for a new Task object."""
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    task = Task(task_type="Enrichment", description="Morning walk", time="7:00 AM", frequency="Daily")
    pet.add_task(task)
    owner = Owner(time_availability="morning", pets=[pet])
    scheduler = Scheduler(schedule_name="test")

    task_to_pet = {id(t): p for p in owner.pets for t in p.tasks}
    Scheduler.mark_task_complete(task)
    scheduler.create_plan(owner)

    current_ids = {id(t) for t in pet.tasks}
    assert id(task) not in current_ids
    assert id(task) in task_to_pet


def test_task_to_pet_lookup_is_correct_when_rebuilt_after_create_plan():
    """The safe pattern: rebuild task_to_pet from the current tasks after create_plan()."""
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    task = Task(task_type="Enrichment", description="Morning walk", time="7:00 AM", frequency="Daily")
    pet.add_task(task)
    owner = Owner(time_availability="morning", pets=[pet])
    scheduler = Scheduler(schedule_name="test")

    Scheduler.mark_task_complete(task)
    scheduler.create_plan(owner)
    task_to_pet = {id(t): p for p in owner.pets for t in p.tasks}

    for current_task in pet.tasks:
        assert task_to_pet[id(current_task)] is pet


# --- Conflict detection ---


def test_find_conflicts_detects_two_tasks_same_pet_same_time():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    pet.tasks = [
        Task(task_type="Enrichment", description="Morning walk", time="7:00 AM", frequency="Daily"),
        Task(task_type="Medical", description="Ear drops", time="7:00 AM", frequency="Daily"),
    ]
    owner = Owner(time_availability="morning", pets=[pet])

    conflicts = Scheduler(schedule_name="test").find_conflicts(owner)

    assert len(conflicts) == 1
    assert conflicts[0]["pet"] == "Luna"
    assert set(conflicts[0]["descriptions"]) == {"Morning walk", "Ear drops"}


def test_find_conflicts_ignores_tasks_at_different_times():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    pet.tasks = [
        Task(task_type="Enrichment", description="Morning walk", time="7:00 AM", frequency="Daily"),
        Task(task_type="Diet", description="Dinner", time="6:00 PM", frequency="Daily"),
    ]
    owner = Owner(time_availability="morning", pets=[pet])

    assert Scheduler(schedule_name="test").find_conflicts(owner) == []


def test_find_conflicts_does_not_flag_different_pets_at_same_time():
    luna = Pet(name="Luna", breed="x", diet_needs="", med_needs="", enrichment_needs="")
    luna.tasks = [Task(task_type="Enrichment", description="Walk", time="7:00 AM", frequency="Daily")]
    mochi = Pet(name="Mochi", breed="x", diet_needs="", med_needs="", enrichment_needs="")
    mochi.tasks = [Task(task_type="Diet", description="Breakfast", time="7:00 AM", frequency="Daily")]
    owner = Owner(time_availability="morning", pets=[luna, mochi])

    assert Scheduler(schedule_name="test").find_conflicts(owner) == []


def test_find_conflicts_merges_pets_that_share_a_name():
    """Known gap: find_conflicts() groups by (pet.name, time), so two distinct Pet
    objects that happen to share a name are treated as one pet and falsely reported
    as a conflict even though each task belongs to a different animal."""
    twin_a = Pet(name="Buddy", breed="x", diet_needs="", med_needs="", enrichment_needs="")
    twin_a.tasks = [Task(task_type="Enrichment", description="Walk", time="7:00 AM", frequency="Daily")]
    twin_b = Pet(name="Buddy", breed="x", diet_needs="", med_needs="", enrichment_needs="")
    twin_b.tasks = [Task(task_type="Diet", description="Breakfast", time="7:00 AM", frequency="Daily")]
    owner = Owner(time_availability="morning", pets=[twin_a, twin_b])

    conflicts = Scheduler(schedule_name="test").find_conflicts(owner)

    assert len(conflicts) == 1
    assert set(conflicts[0]["descriptions"]) == {"Walk", "Breakfast"}


def test_find_conflicts_groups_unparseable_times_together():
    """Tasks with unparseable time strings all fall back to datetime.max, so two
    unrelated malformed-time tasks on the same pet are falsely reported as a conflict."""
    pet = Pet(name="Luna", breed="x", diet_needs="", med_needs="", enrichment_needs="")
    pet.tasks = [
        Task(task_type="Enrichment", description="Walk", time="whenever", frequency="Daily"),
        Task(task_type="Diet", description="Snack", time="not a time", frequency="Daily"),
    ]
    owner = Owner(time_availability="morning", pets=[pet])

    conflicts = Scheduler(schedule_name="test").find_conflicts(owner)

    assert len(conflicts) == 1
    assert set(conflicts[0]["descriptions"]) == {"Walk", "Snack"}


# --- Recurring tasks ---


def test_is_recurring_true_for_daily_and_weekly_case_insensitive():
    daily = Task(task_type="Diet", description="Dinner", time="6:00 PM", frequency=" Daily ")
    weekly = Task(task_type="Enrichment", description="Groom", time="6:00 PM", frequency="WEEKLY")

    assert daily.is_recurring() is True
    assert weekly.is_recurring() is True


def test_is_recurring_false_for_as_needed_and_empty_frequency():
    as_needed = Task(task_type="Medical", description="Vet visit", time="3:00 PM", frequency="as-needed")
    blank = Task(task_type="Medical", description="Vet visit", time="3:00 PM", frequency="")

    assert as_needed.is_recurring() is False
    assert blank.is_recurring() is False


def test_next_occurrence_returns_fresh_incomplete_copy():
    task = Task(task_type="Diet", description="Dinner", time="6:00 PM", frequency="Daily")
    task.mark_complete()

    next_task = task.next_occurrence()

    assert next_task is not task
    assert next_task.is_complete is False
    assert next_task.task_type == task.task_type
    assert next_task.description == task.description
    assert next_task.time == task.time
    assert next_task.frequency == task.frequency


def test_create_plan_called_twice_does_not_duplicate_tasks():
    """Calling create_plan() repeatedly should be idempotent for task counts -
    a completed recurring task should roll over exactly once, not accumulate copies."""
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    task = Task(task_type="Enrichment", description="Morning walk", time="7:00 AM", frequency="Daily")
    pet.add_task(task)
    owner = Owner(time_availability="morning", pets=[pet])
    scheduler = Scheduler(schedule_name="test")

    Scheduler.mark_task_complete(task)
    scheduler.create_plan(owner)
    scheduler.create_plan(owner)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].is_complete is False


def test_roll_over_completed_tasks_leaves_incomplete_tasks_untouched():
    pet = Pet(
        name="Luna",
        breed="Golden Retriever",
        diet_needs="2 cups kibble",
        med_needs="None",
        enrichment_needs="1 hour exercise",
    )
    incomplete_task = Task(task_type="Diet", description="Dinner", time="6:00 PM", frequency="Daily")
    pet.add_task(incomplete_task)
    owner = Owner(time_availability="morning", pets=[pet])

    Scheduler(schedule_name="test").roll_over_completed_tasks(owner)

    assert pet.tasks == [incomplete_task]
