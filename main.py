"""
Version 0.1
"""

import json
import datetime
import os
import time
import logging as log

log.basicConfig(filename='debug.log', level=log.INFO)


def main():
    events = get_events('timed_bosses.json')
    longest_title = 0
    DAY = 86400  # A full 24 hours in seconds
    ACTIVE = 450  # Sets the number of seconds to leave an event active 600 = 10 minutes

    while True:

        timer = []

        for boss in events:
            # Set the longest_title variable to the length of the longest title for spacing
            if len(boss) > longest_title:
                longest_title = len(boss)

            times = get_utc_times(events[boss]["times"])
            deltas = get_spawn_delta(times)

            # DEBUG
            log.debug("Unsorted Deltas\n===================")
            log.debug("Unsorted Deltas::%s [%s]" % (boss, ', '.join(str(i.seconds) for i in deltas)))
            log.debug("===================")

            # Populate the timer list with the current event
            if deltas[-1].seconds > DAY - ACTIVE:
                timer.append((boss, -deltas[-1].seconds))
            else:
                timer.append((boss, deltas[0].seconds))

        # Sort the timer so that the next event floats to the top
        timer = sorted(timer, key=lambda t: t[1])

        # Print the times to the console
        for t in timer:
            spacing = (longest_title - len(t[0]))
            if t[1] < 0:
                print(t[0], " " * spacing, "Active(%s)" % format_seconds(ACTIVE - (DAY + t[1])))
            else:
                print(t[0], " " * spacing, format_seconds(t[1]))

        # Refresh rate and screen clear
        time.sleep(1)
        os.system('cls')


def format_seconds(s):
    """
    Returns seconds in the following string format HH:MM:SS
    :param s:
    :return:
    """
    return '{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60)


def get_utc_times(times):
    """
    Takes a list of times in string format HH:MM and returns a list of utc datetime objects
    :param times:
    :return:
    """
    utc_times = []

    for t in times:
        # Takes the str time and unpacks it as ints
        hours, minutes = map(int, t.split(":"))
        # Converts the raw minutes and hours to a UTC datetime object
        dt = datetime.datetime.combine(datetime.datetime.utcnow().date(), datetime.time(hours, minutes))
        utc_times.append(dt)
    # Sort the times in case they are out of order
    utc_times.sort()

    return utc_times


def get_spawn_delta(times):
    """
    Takes in a list of UTC spawn times and returns a list of the deltas from the current UTC time
    :param times:
    :return:
    """

    deltas = []
    now = datetime.datetime.utcnow()
    for t in times:
        delta = t - now
        deltas.append(delta)

    deltas = sorted(deltas, key=lambda d: d.seconds)

    # DEBUG
    log.debug("Getting deltas for %s" % (" ".join(str(t.time()) for t in times)))
    log.debug("Deltas for %s" % (" ".join(str(d.seconds) for d in deltas)))
    log.debug("Sorted Deltas for %s" % (" ".join(str(d.seconds) for d in deltas)))

    return deltas


def get_events(file):
    """
    Opens a file and returns it as a json object
    :param file:
    :return:
    """
    with open(file, 'r') as f:
        data = f.read()
        json_data = json.loads(data)
    return json_data

if __name__ == '__main__':
    main()