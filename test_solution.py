## Student Name:
## Student ID:

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from solution import suggest_slots


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots


def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots


def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert slots[1] == "10:15"
    assert "09:30" not in slots


def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots


"""TODO: Add at least 5 additional test cases to test your implementation."""


def test_post_meeting_buffer_is_enforced():
    """
    Constraint:
    A 15-minute buffer must be respected after an event ends before a new one can begin.
    """
    events = [{"start": "09:00", "end": "09:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    # The event ends at 09:30, but the 15-minute wrap-up buffer means the next free slot is 09:45
    assert "09:30" not in slots
    assert "09:45" in slots


def test_meeting_must_end_before_work_day_ends():
    """
    Constraint:
    Meetings cannot be scheduled if they would end after working hours (17:00).
    """
    events = []
    # Requesting a 60-minute meeting
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    # The latest a 60-minute meeting can start is 16:00 to end at 17:00
    assert "16:00" in slots
    assert "16:15" not in slots


def test_fully_booked_day_returns_no_slots():
    """
    Constraint:
    If there is no free time available, the function should return an empty list.
    """
    # Booking the entire morning and afternoon (ignoring lunch since it's hardcoded)
    events = [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert len(slots) == 0


def test_meeting_duration_longer_than_gaps():
    """
    Constraint:
    Slots should not be suggested if the free gap between events is smaller than the meeting duration.
    """
    events = [
        {"start": "09:00", "end": "10:00"},
        # Gap is only 15 minutes (10:15 to 10:30) because of the 15-min post-buffer
        {"start": "10:30", "end": "11:30"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    # The 10:15 slot is free, but a 30-minute meeting won't fit before the 10:30 event
    assert "10:15" not in slots


def test_overlapping_events_merge_correctly():
    """
    Constraint:
    Events that overlap in the input should correctly merge their blocked time without leaving accidental gaps.
    """
    events = [{"start": "14:00", "end": "15:00"}, {"start": "14:30", "end": "15:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    # The merged event runs effectively from 14:00 to 15:30 + 15 min buffer = 15:45
    assert "14:00" not in slots
    assert "15:30" not in slots
    assert "15:45" in slots
