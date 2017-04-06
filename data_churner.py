import csv
import os
import requests
from collections import namedtuple


from config import DATA_FILE, GSHEET_KEY


Ride = namedtuple('Ride', ('id', 'title', 'results'))
Rider = namedtuple('Rider', ('id', 'name'))
Event = namedtuple('Event', ('id', 'cat', 'title', 'results'))


EVENT_CATS = ('kom', 'qom', 'sprint', 'gc')


def _idx_and_item(l):
    return zip(range(len(l)), l)


def _map_index(i):
    return lambda x: x[i]


def load_raw_data(data_file=DATA_FILE, gsheet_key=GSHEET_KEY):
    if data_file and os.path.exists(data_file):
        with open(data_file) as f:
            data_string = f.read()
    else:
        url = 'https://docs.google.com/spreadsheet/ccc?key={}&output=csv'
        r = requests.get(url.format(gsheet_key))
        r.raise_for_status()
        data_string = r.content.decode()

        if data_file:
            with open(data_file, 'w') as f:
                f.write(data_string)

    return data_string


def parse_data(data_file=DATA_FILE, gsheet_key=GSHEET_KEY):
    ''' Returns the tuple (riders, rides) where riders is a dict mapping id to
        name and rides is a dict mapping ride id to Ride namedtuple.

        The results dict of a Ride is a list of events and the
        results dict of an event is a dict mapping rider id to points.

        If data_file does not exist, this method attempts to download it from
        Google Sheets using the URI key for a public Google Sheet. This may
        take a few seconds (and prone to rate limiting) but the CSV is then
        saved as the given data_file for future use.
    '''
    rides = {}
    riders = {}
    events = {}

    data_string = load_raw_data(data_file, gsheet_key)
    reader = csv.reader(data_string.split('\n'))

    # contains ride title at or preceding first ride intermediate
    ride_row = next(reader)
    ride_row[0] = ''
    ride_row[1] = ''

    for ride in filter(_map_index(1), _idx_and_item(ride_row)):
        rides[ride[0]] = Ride(*ride, [])

    # should contain the ID and Name column headers for riders and
    # intermediate event types and names for each ride
    info_row = next(reader)
    if info_row[0].lower() != 'id' or info_row[1].lower() != 'name':
        raise Exception('Needs ID and name in row 2, col 1, 2 respectively')

    prev_name_hack = ''
    for idx, event in _idx_and_item(info_row):
        event = (event + ':' + prev_name_hack).split(':')
        prev_name_hack = event[1]
        event[0] = event[0].lower()

        if event[0] in ('kom', 'qom', 'sprint', 'gc'):
            if event[0] == 'gc':
                event[1] = 'GC'
            elif event[0] == 'qom':
                event[1] += ' (QOM)'

            ride_idx = max(filter(lambda i: i<= idx, rides))
            intermediate = Event(idx, event[0], event[1], {})
            events[intermediate.id] = intermediate
            rides[ride_idx].results.append(intermediate)

    # each subsequent row contains a unique rider ID, their name, and their
    # results on each ride event (blank is interpretted as 0)
    for rider in reader:
        rider_id = rider[0]
        rider_name = rider[1]

        if not rider_name:
            continue

        riders[rider_id] = Rider(rider[0], rider[1])

        for idx, result in list(_idx_and_item(rider))[2:]:
            if result:
                if rider_id not in events[idx].results:
                    events[idx].results[rider_id] = 0
                events[idx].results[rider_id] += int(result)

    return riders, list(rides.values())


def _add_rankings(l, nmax=5):
    ''' Sorta poorly named, this just adds numerical rankings to results l and
        limits to nmax results. If len(l) < nmax, fills in with dashes.
    '''
    if not l:
        return [('-', '-', '-')] * nmax

    l[0] = (1, *l[0])
    for i in range(1, len(l)):
        l[i] = (l[i-1][0] if l[i][-1] == l[i-1][-1] else i + 1, *l[i])
    l = (l + [('-', '-', '-')] * nmax)[:nmax]
    return l


def _rank_by_points(l, nmax=5):
    return _add_rankings(sorted(l, key=_map_index(-1), reverse=True), nmax)


def compute_all_ride_results(riders, rides, nmax=5):
    return [compute_ride_results(riders, ride, nmax) for ride in rides]


def compute_ride_results(riders, ride, nmax=5):
    ''' Returns the printable results for a given ride. Intermediate events
        (KOMs, QOMs, Sprint, GC) are returned as a tuple with type, event
        name, and a descending list of names and points. Totals for all events
        simply are the event type mapping to a descending list of point sums.
    '''
    events = []
    totals = {x: {} for x in EVENT_CATS}

    for event in ride.results:
        l = []

        for x in event.results.items():
            rider = riders[x[0]]
            if rider.name not in totals[event.cat]:
                totals[event.cat][rider.name] = 0
            totals[event.cat][rider.name] += x[1]

            l.append((rider.name, x[1]))

        l = _rank_by_points(l, nmax)
        events.append((event, l))

    totals = {x[0]: _rank_by_points(x[1].items(), nmax) for x in totals.items()}

    return ride, events, totals


def compute_overall_totals(rides_results, nmax=5):
    '''
    '''
    totals = {x: {} for x in EVENT_CATS}

    for total in rides_results:
        total = total[-1]
        for event_type in total:
            for rider in total[event_type]:
                if rider[0] == '-':
                    continue
                if rider[1] not in totals[event_type]:
                    totals[event_type][rider[1]] = 0
                totals[event_type][rider[1]] += rider[2]

    totals = {x[0]: _rank_by_points(x[1].items(), nmax) for x in totals.items()}

    return totals
