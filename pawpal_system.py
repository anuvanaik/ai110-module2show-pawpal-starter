from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    breed: str
    diet_needs: str
    med_needs: str
    enrichment_needs: str

    def assign_to_task(self, task):
        pass


@dataclass
class Task:
    task_type: str

    def prioritize(self, pet, owner):
        pass


@dataclass
class Scheduler:
    schedule_name: str
    tasks: list = field(default_factory=list)

    def create_plan(self, owner):
        pass

    def fit_task_by_availability(self, task, owner):
        pass

    def remind_owner(self, owner):
        pass


@dataclass
class Owner:
    time_availability: str
    owner_preferences: list = field(default_factory=list)
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        pass

    def add_task_to_schedule(self, task, scheduler):
        pass
