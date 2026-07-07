from pawpal_system import Task, Pet


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
