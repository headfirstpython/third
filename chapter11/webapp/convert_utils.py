import hfpy_utils

import json
import statistics


CONVERSIONS = {
    "Free": "freestyle",
    "Back": "backstroke",
    "Breast": "breaststroke",
    "Fly": "butterfly",
    "IM": "individual medley",
}
COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
JSONDATA = "records.json"


def get_worlds(distance, stroke):
    """Given an event distance and stroke, return the list of the four
    world records at that distance and stroke."""
    with open(JSONDATA) as jf:
        records = json.load(jf)
    return [records[course][f"{distance} {CONVERSIONS[stroke]}"] for course in COURSES]


def perform_conversions(times):
    """Given a list of swim times as strings, return the average time as a string,
    as well as the reversed list of times and a list of scaled swim times as
    numbers (floats)."""
    converts = []
    for t in times:
        # The minutes value might be missing, so guard against this causing a crash.
        if ":" in t:
            minutes, rest = t.split(":")
            seconds, hundredths = rest.split(".")
        else:
            minutes = 0
            seconds, hundredths = t.split(".")
        converts.append(int(minutes) * 60 * 100 + int(seconds) * 100 + int(hundredths))
    average = statistics.mean(converts)
    mins_secs, hundredths = f"{(average / 100):.2f}".split(".")
    mins_secs = int(mins_secs)
    minutes = mins_secs // 60
    seconds = mins_secs - minutes * 60
    average = f"{minutes}:{seconds:0>2}.{hundredths}"
    converts.reverse()
    times.reverse()
    from_max = max(converts)
    scaled = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]
    return average, times, scaled  # Returned as a tuple.
