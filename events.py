import json
import datetime
import os

from build_utils import resource_path


class GW2Events(object):
    def __init__(self):
        self.events = self.get_events(resource_path('timed_bosses.json'))
        self.longest_title = 0
        self.DAY = 86400  # A full 24 hours in seconds
        self.ACTIVE = 450  # Sets the number of seconds to leave an event active 600 = 10 minutes

    def build_events(self, console_out=False, format_out=False):
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

            # Populate the timer list with the current event in the format (boss, time, active)
            if deltas[-1].seconds > self.DAY - average_time:
                timer.append((boss, -deltas[-1].seconds, True))
            else:
                timer.append((boss, deltas[0].seconds, False))

        # Sort the timer so that the next event floats to the top
        timer = sorted(timer, key=lambda t: t[1])

        if console_out:
            self.print_events(timer)
        else:
            return timer

    def format_seconds(self, s, average_time):
        """
        Returns seconds in the following string format HH:MM:SS
        :param s:
        :return:
        """
        if s < 0:
            s = int(average_time) - (self.DAY + s)

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
            active = event[2]
            average_time = int(self.events[event[0]]["average_time"])
            spacing = (self.longest_title - len(boss))

            if t < 900:
                color = "yellow"
            else:
                color = None

            if active:
                self.print_color("red", boss, " " * spacing, "Active(%s)" % self.format_seconds(t, average_time))
            else:
                self.print_color(color, boss, " " * spacing, self.format_seconds(t, average_time))

    def clear_console(self):
        os.system('cls')

    def print_color(self, color, *args):
        c = {None: 30, "red": 31, "yellow": 33, "green": 32}
        print('\033[1;%sm%s\033[1;m' % (c[color], " ".join(args)))



if __name__ == '__main__':

    import colorama
    import time
    colorama.init()  # Enables colored console print

    gw2events = GW2EVENTS()
    while True:
        gw2events.build_events(console_out=True)
        time.sleep(1)
        gw2events.clear_console()