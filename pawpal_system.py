from dataclasses import dataclass, field
from datetime import datetime


def _parse_time(time_str: str) -> datetime:
    """Parse a task's time string, falling back to datetime.max if unparseable."""
    try:
        return datetime.strptime(time_str.strip(), "%I:%M %p")
    except ValueError:
        return datetime.max


@dataclass
class Task:
    task_type: str
    description: str
    time: str
    frequency: str
    is_complete: bool = False

    def prioritize(self, pet, owner):
        """Order this task by pet need first, then owner preference."""
        pet_needs = [pet.diet_needs, pet.med_needs, pet.enrichment_needs]
        if self.description in pet_needs:
            return 1
        if self.description in owner.owner_preferences:
            return 2
        return 3

    def mark_complete(self):
        """Mark this task as done."""
        self.is_complete = True

    def is_recurring(self) -> bool:
        """Whether this task's frequency should generate a new occurrence when completed."""
        return self.frequency.strip().lower() in {"daily", "weekly"}

    def next_occurrence(self) -> "Task":
        """Build a fresh, incomplete task for this task's next occurrence."""
        return Task(
            task_type=self.task_type,
            description=self.description,
            time=self.time,
            frequency=self.frequency,
        )


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
        return self.tasks


@dataclass
class Owner:
    time_availability: str
    owner_preferences: list = field(default_factory=list)
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's roster."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    schedule_name: str
    tasks: list = field(default_factory=list)

    def get_all_tasks(self, owner: Owner) -> list:
        """Collect all tasks from every pet the owner has."""
        return owner.get_all_tasks()

    @staticmethod
    def mark_task_complete(task: Task):
        """Mark a task done."""
        task.mark_complete()

    def roll_over_completed_tasks(self, owner: Owner):
        """Clear completed tasks off each pet's list; recurring ones leave behind their next occurrence."""
        for pet in owner.pets:
            for task in [t for t in pet.tasks if t.is_complete]:
                pet.tasks.remove(task)
                if task.is_recurring():
                    pet.add_task(task.next_occurrence())

    def sort_by_time(self, tasks: list = None) -> list:
        """Sort tasks by their time attribute, soonest first."""
        if tasks is None:
            tasks = self.tasks
        return sorted(tasks, key=lambda t: _parse_time(t.time))

    def organize_tasks(self) -> list:
        """Sort and group tasks into a logical schedule order."""
        return self.sort_by_time()

    def create_plan(self, owner: Owner):
        """Build a full daily plan based on the owner's pets and availability."""
        self.roll_over_completed_tasks(owner)
        self.tasks = self.get_all_tasks(owner)

    def fit_task_by_availability(self, task: Task, owner: Owner) -> bool:
        """Check whether a task's time falls within the owner's available window(s)."""
        windows = {
            "morning": (5, 12),
            "afternoon": (12, 17),
            "evening": (17, 21),
            "night": (21, 5),
        }
        availability = owner.time_availability.lower()
        available_windows = [name for name in windows if name in availability]
        if not available_windows:
            return True

        hour = _parse_time(task.time).hour
        for name in available_windows:
            start, end = windows[name]
            if start < end:
                if start <= hour < end:
                    return True
            elif hour >= start or hour < end:
                return True
        return False

    @staticmethod
    def check_conflict(pet: Pet, task: Task) -> str:
        """Lightweight check for an existing task at the same time; returns a warning message or None."""
        clashing = [t.description for t in pet.tasks if _parse_time(t.time) == _parse_time(task.time)]
        if not clashing:
            return None
        return f"⚠️ {pet.name} already has a task at {task.time}: {', '.join(clashing)}"

    def find_conflicts(self, owner: Owner) -> list:
        """Find pets with more than one task scheduled at the same time."""
        groups = {}
        for pet in owner.pets:
            for task in pet.tasks:
                key = (pet.name, _parse_time(task.time))
                groups.setdefault(key, []).append(task)

        conflicts = []
        for (pet_name, _), tasks in groups.items():
            if len(tasks) > 1:
                conflicts.append({
                    "pet": pet_name,
                    "time": tasks[0].time,
                    "descriptions": [t.description for t in tasks],
                })
        return conflicts

    def filter_tasks(self, owner: Owner, is_complete: bool = None, pet_name: str = None) -> list:
        """Filter an owner's tasks by completion status and/or pet name."""
        matches = []
        for pet in owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if is_complete is not None and task.is_complete != is_complete:
                    continue
                matches.append(task)
        return matches

    def remind_owner(self, owner: Owner) -> list:
        """Send a reminder to the owner about upcoming tasks, soonest first."""
        incomplete = [t for t in self.get_all_tasks(owner) if not t.is_complete]
        return self.sort_by_time(incomplete)
