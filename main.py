"""
Version 0.1
"""

import json
import datetime
import os
import time
import logging as log
import sys
import colorama


class GW2EVENTS:
    def __init__(self):
        log.basicConfig(filename='debug.log', level=log.INFO)
        self.events = self.get_events('timed_bosses.json')
        self.longest_title = 0
        self.DAY = 86400  # A full 24 hours in seconds
        self.ACTIVE = 450  # Sets the number of seconds to leave an event active 600 = 10 minutes

    def build_events(self, console_out=False):
        timer = []

        for boss in self.events:
            # Set the longest_title variable to the length of the longest title for spacing
            if len(boss) > self.longest_title:
                self.longest_title = len(boss)

            times = self.get_utc_times(self.events[boss]["times"])
            average_time = int(self.events[boss]["average_time"])
            deltas = self.get_spawn_delta(times)

            # Make sure there is an average tim
            if not average_time:
                average_time = self.ACTIVE

            # DEBUG
            log.debug("Unsorted Deltas\n===================")
            log.debug("Unsorted Deltas::%s [%s]" % (boss, ', '.join(str(i.seconds) for i in deltas)))
            log.debug("===================")

            # Populate the timer list with the current event
            if deltas[-1].seconds > self.DAY - average_time:
                timer.append((boss, -deltas[-1].seconds, average_time))
            else:
                timer.append((boss, deltas[0].seconds, average_time))

        # Sort the timer so that the next event floats to the top
        timer = sorted(timer, key=lambda t: t[1])

        if console_out:
            self.print_events(timer)
        else:
            return timer

    def format_seconds(self, s):
        """
        Returns seconds in the following string format HH:MM:SS
        :param s:
        :return:
        """
        return '{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60)

    def get_utc_times(self, times):
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

    def get_spawn_delta(self, times):
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

    def get_events(self, file):
        """
        Opens a file and returns it as a json object
        :param file:
        :return:
        """
        with open(file, 'r') as f:
            data = f.read()
            json_data = json.loads(data)
        return json_data

    def print_events(self, events):
        """
        Output the given event list to the console
        :param events:
        :return:
        """
        for event in events:
            boss = event[0]
            t = event[1]
            average_time = event[2]
            spacing = (self.longest_title - len(boss))

            if t < 900:
                color = "yellow"
            else:
                color = None

            if t < 0:
                self.print_color("red", boss, " " * spacing, "Active(%s)" % self.format_seconds(average_time - (self.DAY + t)))
            else:
                self.print_color(color, boss, " " * spacing, self.format_seconds(t))

    def clear_console(self):
        os.system('cls')

    def print_color(self, color, *args):
        c = {None: 30, "red": 31, "yellow": 33, "green": 32}
        print('\033[1;%sm%s\033[1;m' % (c[color], " ".join(args)))



if __name__ == '__main__':
    colorama.init()  # Enables colored console print
    gw2events = GW2EVENTS()
    while True:
        gw2events.build_events(console_out=True)
        time.sleep(1)
        gw2events.clear_console()