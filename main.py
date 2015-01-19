'''
Version 0.1
'''

import json
import datetime
import os
import time

def main():
    raw_data = get_times('timed_bosses.json')
    times = []
    for boss in raw_data:
        raw_times = raw_data[boss]["times"]
        for t in raw_times:
            hours = int(t.split(":")[0])
            minutes = int(t.split(":")[1])
            dt = datetime.datetime.combine(datetime.datetime.utcnow().date(), datetime.time(hours, minutes))
            times.append((boss, dt))


    sorted_times = sorted(times, key = lambda time: time[1])


    while(True):
        upcoming_events = []
        now = datetime.datetime.utcnow()
        for t in sorted_times:
            time_till = t[1] - now
            if time_till.days == 0:
                upcoming_events.append((t[0], time_till))

        for event in upcoming_events[:5]:
            s = event[1].seconds
            print(event[0], '{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))

        time.sleep(1)
        os.system('cls')


def get_times(file):
    """
    Opens a file and returns it as a json object
    :param file:
    :return:
    """
    with open(file, 'r') as f:
        data = f.read()
        json_data = json.loads(data)
    return(json_data)

if __name__ == '__main__':
    main()