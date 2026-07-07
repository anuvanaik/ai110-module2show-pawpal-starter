from dataclasses import dataclass, field


@dataclass
class Task:
    task_type: str
    description: str
    time: str
    frequency: str
    is_complete: bool = False

    def prioritize(self, pet, owner):
        """Order this task by pet need first, then owner preference."""
        pass

    def mark_complete(self):
        """Mark this task as done."""
        self.is_complete = True


@dataclass
class Pet:
    name: str
    breed: str
    diet_needs: str
    med_needs: str
    enrichment_needs: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list:
        """Return all tasks assigned to this pet."""
        pass


@dataclass
class Owner:
    time_availability: str
    owner_preferences: list = field(default_factory=list)
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's roster."""
        pass

    def get_all_tasks(self) -> list:
        """Return every task across all of this owner's pets."""
        pass


@dataclass
class Scheduler:
    schedule_name: str
    tasks: list = field(default_factory=list)

    def get_all_tasks(self, owner: Owner) -> list:
        """Collect all tasks from every pet the owner has."""
        pass

    def organize_tasks(self) -> list:
        """Sort and group tasks into a logical schedule order."""
        pass

    def create_plan(self, owner: Owner):
        """Build a full daily plan based on the owner's pets and availability."""
        pass

    def fit_task_by_availability(self, task: Task, owner: Owner):
        """Slot a task into a time window that matches the owner's availability."""
        pass

    def remind_owner(self, owner: Owner):
        """Send a reminder to the owner about upcoming tasks."""
        pass
