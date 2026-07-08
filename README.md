# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

========================================
        TODAY'S SCHEDULE - PawPal+
========================================

Luna (Golden Retriever)
------------------------------
  [Pending] 7:00 AM � Enrichment: Morning walk around the block
  [Pending] 6:00 PM � Diet: Serve measured dinner portion

Mochi (Shih Tzu)
------------------------------
  [Pending] 12:00 PM � Medication: Give allergy pill with food

========================================
Owner: Alex  |  Available: Mornings and evenings
========================================

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```
=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.14.6-final-0 _______________

Name               Stmts   Miss  Cover   Missing
------------------------------------------------
pawpal_system.py     106     27    75%   63, 74, 120-139, 169-177, 181-182
------------------------------------------------
TOTAL                106     27    75%
============================= 26 passed in 0.19s ==============================

Sample test output:

```
# Paste your pytest output here
```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\anuva\OneDrive\Documents\GitHub\ai110-module2show-pawpal-starter\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\anuva\OneDrive\Documents\GitHub\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collecting ... collected 26 items

test_pawpal.py::test_check_conflict_returns_warning_for_clashing_time PASSED [  3%]
test_pawpal.py::test_check_conflict_returns_none_when_no_clash PASSED    [  7%]
test_pawpal.py::test_mark_complete_changes_status PASSED                 [ 11%]
test_pawpal.py::test_add_task_increases_pet_task_count PASSED            [ 15%]
test_pawpal.py::test_mark_task_complete_keeps_task_visible_as_done PASSED [ 19%]
test_pawpal.py::test_roll_over_completed_tasks_replaces_recurring_task_with_next_occurrence PASSED [ 23%]
test_pawpal.py::test_roll_over_completed_tasks_drops_non_recurring_task PASSED [ 26%]
test_pawpal.py::test_sort_by_time_returns_chronological_order_regardless_of_insertion_order PASSED [ 30%]
test_pawpal.py::test_sort_by_time_places_unparseable_times_last PASSED   [ 34%]
test_pawpal.py::test_organize_tasks_returns_all_pets_tasks_in_chronological_order PASSED [ 38%]
test_pawpal.py::test_prioritize_ranks_pet_need_match_highest PASSED      [ 42%]
test_pawpal.py::test_prioritize_ranks_owner_preference_when_no_pet_need_matches PASSED [ 46%]
test_pawpal.py::test_prioritize_falls_back_to_general_when_no_match PASSED [ 50%]
test_pawpal.py::test_prioritize_is_case_and_whitespace_sensitive PASSED  [ 53%]
test_pawpal.py::test_stale_id_based_task_lookup_becomes_invalid_after_rollover PASSED [ 57%]
test_pawpal.py::test_task_to_pet_lookup_is_correct_when_rebuilt_after_create_plan PASSED [ 61%]
test_pawpal.py::test_find_conflicts_detects_two_tasks_same_pet_same_time PASSED [ 65%]
test_pawpal.py::test_find_conflicts_ignores_tasks_at_different_times PASSED [ 69%]
test_pawpal.py::test_find_conflicts_does_not_flag_different_pets_at_same_time PASSED [ 73%]
test_pawpal.py::test_find_conflicts_merges_pets_that_share_a_name PASSED [ 76%]
test_pawpal.py::test_find_conflicts_groups_unparseable_times_together PASSED [ 80%]
test_pawpal.py::test_is_recurring_true_for_daily_and_weekly_case_insensitive PASSED [ 84%]
test_pawpal.py::test_is_recurring_false_for_as_needed_and_empty_frequency PASSED [ 88%]
test_pawpal.py::test_next_occurrence_returns_fresh_incomplete_copy PASSED [ 92%]
test_pawpal.py::test_create_plan_called_twice_does_not_duplicate_tasks PASSED [ 96%]
test_pawpal.py::test_roll_over_completed_tasks_leaves_incomplete_tasks_untouched PASSED [100%]

============================= 26 passed in 0.16s ==============================

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time(tasks=None)|sorts tasks by time|
| Filtering | Scheduler.filter_tasks(owner, is_complete=None, pet_name=None)|by completion status and/or pet name|
| Conflict handling |Scheduler.check_conflict(pet, task), Scheduler.find_conflicts(owner), check_conflict()| returns warning message |
| Recurring tasks | Task.is_recurring() , Task.next_occurrence(), Scheduler.mark_task_complete(task), Scheduler.roll_over_completed_tasks(owner) |Completing a recurring task auto-schedules its next task when new task is new generated|

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step --> Add info about user 
2. <!-- Describe this step --> Add pet information
3. <!-- Describe this step --> Repeat step 2 if you have another pet (optional)
4. <!-- Describe this step --> Then add several tasks for the pet(s)
5. <!-- Add more steps as needed --> Then generate your schedule
6. If there is tasks that are assigned at the same schedule it will show that there is a conflict with double booking.

'''
Scheduling Luna's ear drops...
  [WARNING] Luna already has a task at 7:00 AM: Morning walk around the block
========================================
        TODAY'S SCHEDULE - PawPal+
Owner: Alex  |  Available: Mornings and evenings
========================================
  [CONFLICT] Luna has two tasks scheduled at 7:00 AM: Morning walk around the block, Give ear drops
  [Pending] 7:00 AM � Luna: enrichment: Morning walk around the block
           Why: general task, no specific match
  [Pending] 7:00 AM � Luna: medical: Give ear drops
           Why: general task, no specific match
  [Pending] 12:00 PM � Mochi: medical: Give allergy pill with food
           Why: general task, no specific match
           [WARNING] outside your available window
  [Pending] 6:00 PM � Luna: diet: Serve measured dinner portion
           Why: general task, no specific match

Upcoming Reminders
  - 7:00 AM � Luna: Morning walk around the block
  - 7:00 AM � Luna: Give ear drops
  - 12:00 PM � Mochi: Give allergy pill with food
  - 6:00 PM � Luna: Serve measured dinner portion

Completing Luna's morning walk (daily)...
Luna now has 3 task(s):
  [Done] 7:00 AM � enrichment: Morning walk around the block
  [Pending] 7:00 AM � medical: Give ear drops
  [Pending] 6:00 PM � diet: Serve measured dinner portion

Generating a new plan...
Luna now has 3 task(s):
  [Pending] 7:00 AM � medical: Give ear drops
  [Pending] 7:00 AM � enrichment: Morning walk around the block
  [Pending] 6:00 PM � diet: Serve measured dinner portion
  '''

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
