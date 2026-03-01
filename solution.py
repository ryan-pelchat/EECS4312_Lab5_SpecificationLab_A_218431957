## Student Name:
## Student ID:

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict


def suggest_slots(
    events: List[Dict[str, str]], meeting_duration: int, day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    # CONSTRAINT FROM TEST CASE: No meeting may start during the lunch break (12:00–13:00).
    # Idea:
    # Since the day of the week has no impact on the events (because events are day agnostic)
    # we only need to represent a single day
    # We will represent a single day as a string of bits where each position is a single minute
    # Then we can easily mask and check if periods of time are free
    # There are 1440 minutes in 24 hours
    # Gemini suggested that perhaps it is 15 minute increments
    # Gemini suggested start and end hours
    # Gemini suggested to not modify input values
    # Gemini suggested that there is a transition time buffer (before or after a meeting)
    # We will add a post meeting buffer time
    dailySchedule = 0
    timeIncrement = 15
    postBufferTime = 15
    output = []
    bookedTimes = events[::]
    # add restricted time zones
    # add lunch hour
    bookedTimes.append({"start": "12:00", "end": "12:45"})
    # restrict time outside of work
    bookedTimes.append({"start": "00:00", "end": "08:45"})
    bookedTimes.append({"start": "17:00", "end": "23:59"})

    for booked in bookedTimes:
        dailySchedule = dailySchedule | _convertEventToBinary(booked, postBufferTime)

    # this starts from the end of the day
    for i in range(0, 1440 - meeting_duration, timeIncrement):
        if not (
            dailySchedule & (_convertMeetingDurationToBinary(meeting_duration) << i)
        ):
            if (
                day.lower() != "fri"
                or int(_convertNumberToTime(meeting_duration, i)[:2]) < 15
            ):
                output.append(_convertNumberToTime(meeting_duration, i))

    return output[::-1]  # reverse because it is decrementing

    # raise NotImplementedError("suggest_slots function has not been implemented yet")


def _convertEventToBinary(event: Dict[str, str], postBuffer: int) -> int:
    start = int(event["start"][:2]) * 60 + int(event["start"][3:])
    end = int(event["end"][:2]) * 60 + int(event["end"][3:]) + postBuffer
    # cap at midnight before the next day
    if end > 1440:
        end = 1440
    duration = end - start
    bits = (1 << duration) - 1
    bits = bits << (1440 - end)
    return bits


def _convertMeetingDurationToBinary(duration: int) -> int:
    return (1 << duration) - 1


def _convertNumberToTime(duration: int, number: int) -> str:
    minutes = 1440 - duration - number
    return f"{(minutes//60):02d}:{(minutes%60):02d}"


# events = [
#     {"start": "13:00", "end": "14:00"},
#     {"start": "09:30", "end": "10:00"},
#     {"start": "11:00", "end": "12:00"},
# ]
# slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

# events = [{"start": "07:00", "end": "08:00"}]
# slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")
# print(slots)
# def _convertBinToTime(binaryNumber: int) -> str:

#     return ""

# print(bin(_convertEventToBinary({"start": "01:00", "end": "02:00"})))
