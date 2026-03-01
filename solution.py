## Student Name:
## Student ID:

import datetime
from typing import List, Dict

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""


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
    dailySchedule = 0
    timeIncrement = 15
    postBufferTime = 15
    output = []
    bookedTimes = events[::]

    # Add lunch hour (12:00 to 12:45 so buffer lands it exactly at 13:00)
    bookedTimes.append({"start": "12:00", "end": "12:45"})
    # Restrict time outside of work
    bookedTimes.append({"start": "00:00", "end": "08:45"})
    bookedTimes.append({"start": "17:00", "end": "23:59"})

    for booked in bookedTimes:
        dailySchedule = dailySchedule | _convertEventToBinary(booked, postBufferTime)

    # Robustly determine if 'day' is a Friday
    is_friday = False
    try:
        # Try to parse as YYYY-MM-DD
        dt = datetime.datetime.strptime(day, "%Y-%m-%d")
        if dt.weekday() == 4:  # Monday is 0, Friday is 4
            is_friday = True
    except ValueError:
        # Fallback to string prefix checking
        if day.lower().startswith("fri"):
            is_friday = True

    # This starts from the end of the day
    for i in range(0, 1440 - meeting_duration, timeIncrement):
        if not (
            dailySchedule & (_convertMeetingDurationToBinary(meeting_duration) << i)
        ):

            start_time_str = _convertNumberToTime(meeting_duration, i)
            start_h, start_m = map(int, start_time_str.split(":"))

            # Friday Business Rule: Must not start AFTER 15:00
            if is_friday:
                if start_h > 15 or (start_h == 15 and start_m > 0):
                    continue  # Skip this slot

            output.append(start_time_str)

    return output[::-1]  # reverse because it is decrementing


# Helper functions remain exactly as you wrote them
def _convertEventToBinary(event: Dict[str, str], postBuffer: int) -> int:
    start = int(event["start"][:2]) * 60 + int(event["start"][3:])
    end = int(event["end"][:2]) * 60 + int(event["end"][3:]) + postBuffer
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
