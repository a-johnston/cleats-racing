import csv
import os


DEFAULT_DATA_DIR = 'data'
DEFAULT_RIDER_INFO_FILE = 'riders.csv'


def parse_rider_info(
    data_dir=DEFAULT_DATA_DIR,
    rider_info_file=DEFAULT_RIDER_INFO_FILE,
):
    ''' Returns rider info, importantly IDs and names, for use with ride CSVs.

        Returns dictionary mapping int ID to str name
    '''
    path = os.path.join(data_dir, rider_info_file)

    riders = {}

    reader = csv.reader(open(path))
    header = next(reader)

    if 'ID' not in header or 'Name' not in header:
        raise Exception('Malformed rider info header')

    idx = header.index('ID')
    name = header.index('Name')

    for entry in reader:
        if entry[name]:
            riders[int(entry[idx])] = entry[name]

    return riders


def parse_ride_info(
    ride_file,
    data_dir=DEFAULT_DATA_DIR,
):
    ''' Parses a CSV for a given ride and returns the intermediate sprint and
        KOM/QOM points as well as GC if provided.

        Returns a list of tuples identifying intermediate event type, name,
        and results. The results are a dict mapping rider ID to points.

        Example:

        [('Sprint', 'Unicorn', {2: 2, 6, 1}), ...]

        Rider 2 scored 2 points while rider 6 scored 1 point on the Unicorn
        sprint.
    '''
    path = os.path.join(data_dir, ride_file)

    reader = csv.reader(open(path))
    header = next(reader)

    if 'ID' not in header:
        raise Exception('Malformed ride info header')

    idx = header.index('ID')

    events = {}
    last_name_hack = ''
    for i, value in zip(range(len(header)), header):
        split = (value + ':' + last_name_hack).split(':')
        event_type = split[0]
        event_name = split[1]
        last_name_hack = event_name

        if event_type in ('Sprint', 'KOM', 'QOM', 'GC'):
            events[i] = (event_type, event_name, {})

    for rider in reader:
        rider_id = int(rider[idx])

        for event_id in events:
            if rider[event_id]:
                events[event_id][2][rider_id] = int(rider[event_id])

    return list(events.values())


def parse_all_data(
    data_dir=DEFAULT_DATA_DIR,
    rider_info_file=DEFAULT_RIDER_INFO_FILE,
):
    files = os.listdir(data_dir)
    files.remove(rider_info_file)

    riders = parse_rider_info(data_dir, rider_info_file)

    rides = {ride: parse_ride_info(ride) for ride in files}

    return riders, rides
