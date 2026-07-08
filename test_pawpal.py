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
