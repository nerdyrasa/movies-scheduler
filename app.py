import argparse
import csv
import os
from collections import namedtuple
from datetime import datetime, timedelta
import yaml

VALIDFILEEXT = 'csv'
FIELDS = ('movie_title', 'release_year', 'mpaa_rating', 'run_time')
WEEKEND = ['Friday', 'Saturday', 'Sunday']


def get_movies(filename):
    """ Read in a csv file of movies
    :param filename: name of movie file entered in command line
    :return: list of movies
    """

    movies = []

    with open(filename, newline="", encoding='UTF-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        movie = namedtuple("Movie", FIELDS)
        for data in map(movie._make, reader):
            movies.append(data)

    return movies


def parse_actual_run_time(run_time):
    """ Pass the run time as hh:mm and return it as a tuple of integers
    :param run_time: is in the format of hh:mm
    :return: a tuple of integers : h, m
    """
    x, y = run_time.split(":")
    return int(x), int(y)


def calculate_adjusted_run_time(run_time):
    """ Take in run time and adjust it according to business rules.
    Movies should start at easy to read times that end in 0 or 5.
    Examples:
    Run time of 1:00 (1 hour,  0 min), will return adjusted run time of 1:00
    Run time of 1:01 (1 hour,  1 min), will return adjusted run time of 1:05
    Run time of 1:05 (1 hour,  5 min), will return adjusted run time of 1:05
    Run time of 1:06 (1 hour,  6 min), will return adjusted run time of 1:10
    Run time of 1:10 (1 hour, 10 min), will return adjusted run time of 1:10
    an adjusted run time of 1:05.
    :param run_time: The actual run time as hh:mm
    :return: run time as an integer tuple h, m adjusted for business rules
    """
    x, y = run_time.split(':')

    z = int(y) % 10

    if 0 < z < 5:
        new_y = int(y) + 5 - z
        new_x = int(x)

        if int(y) < 5:
            new_y = 5
    elif 5 < z < 10:
        new_x = int(x)
        new_y = int(y) + 10 - z
        if new_y == 60:
            new_x = int(x) + 1
            new_y = 0
    else:
        new_x, new_y = int(x), int(y)

    return new_x, new_y


def get_day_of_week(dt):
    """  Convert datetime value to a string value of the day that datetime value represents
    :param dt: datetime value
    :return: a str that is the day as locale’s full name (for example, Monday
    """
    return datetime.strftime(dt, '%A')


def get_starting_point_date():
    """  Calculate the day for which the schedule is being generated. This
    day depends on the value in the config file. To generate a schedule for the next day,
    the config['day'] is set to 1. For same day, it is set to 0, etc.
    :return: returns the day for which the schedule is being generated
    """
    return datetime.now() + timedelta(days=config['days'])


def get_formatted_date(dt):
    """ Transfrom datetime value into a string
    :param dt: datetime
    :return: string in the format of day name month as number/day as number/full year( for example, 2016)
    """
    return datetime.strftime(dt, '%A %m/%d/%Y')


def get_month(dt):
    """ Transform datetime into numeric month
    :param dt: datetime
    :return: int value of the month
    """
    return int(datetime.strftime(dt, '%m'))


def get_year(dt):
    """ Transform datetime to numeric year
    :param dt: datetime
    :return: int value of year (YYYY)
    """
    return int(datetime.strftime(dt, '%Y'))


def get_day(dt):
    """ Transform datetime to numeric day
    :param dt: datetime
    :return: int value of day
    """
    return int(datetime.strftime(dt, '%d'))


def get_show_time(reference_time, duration):
    """ Show times are calculated from a reference time.
    The duration is subtracted from the reference time to give the show time.
    For example, if the reference time is 2016-01-11 23:00:00 and duration is
    <class 'datetime.timedelta'> of 1:00:00, the value returned is
    datetime object 2016-01-11 22:00:00
    :param reference_time: datetime
    :param duration: datetime.timedelta
    :return: datetime that represents the show time
    """
    return reference_time - duration


def get_duration(h, m):
    """  Transform hours and minute values into a timedelta object
    :param h: hours
    :param m: minutes
    :return: timedelta object
    """
    return timedelta(hours=h, minutes=m)


def valid_file_ext(filename):
    """ Check if the filename has a valid extension
    :param filename: filename entered at the command line
    :return: filename if it has a valid extension
    """
    ext = os.path.splitext(filename)[1][1:]

    if ext != VALIDFILEEXT:
        print("Please submit a csv file")

    return filename


def format_time_to_twelve_hour_clock(dt):
    """ The program calculates using a 24 hour clock. Display output in 12-hour clock format
    :param dt: datetime
    :return: string of datetime passed in the format of Hour (12-hour clock) as a zero-padded decimal number, min
    then am or pm
    """
    return datetime.strftime(dt, '%I:%M %p')


def get_movie_end_time(starttime, hr, min):
    """ Calculate the end time of a movie by adding the movie duratio to the start time
    :param starttime: datetime of when movie starts
    :param hr: hour portion of the duration of the movie
    :param min: min portion of the duration of the movie
    :return: str of the movie end time
    """
    return format_time_to_twelve_hour_clock(starttime + timedelta(hours=hr, minutes=min))


def generate_schedule(movies, target_time, show_time, setup_time, show_date):
    """
    :param movies: list of movies for which to generate schedule
    :param target_time: the earliest possible show time
    :param show_time: initially show_time is the closing time. This is what we use to start calculating
     show times.
    :param setup_time:
    :param show_date:
    :return: a dictionary of the schedule
    """
    opening_time = target_time
    closing_time = show_time
    master_schedule = {}
    schedule = []

    for movie in movies:
        hr_actual, min_actual = parse_actual_run_time(movie.run_time)
        hr_adjusted, min_adjusted = calculate_adjusted_run_time(movie.run_time)
        duration = get_duration(hr_adjusted, min_adjusted)
        show_time = get_show_time(show_time, duration)
        schedule.append((format_time_to_twelve_hour_clock(show_time),
                         get_movie_end_time(show_time, hr_actual, min_actual)))

        while show_time > target_time:
            show_time = get_show_time(show_time, duration + timedelta(minutes=setup_time))
            if show_time > target_time:
                schedule.append((format_time_to_twelve_hour_clock(show_time),
                                 get_movie_end_time(show_time, hr_actual, min_actual)))
            master_schedule[movie] = schedule[::-1]
        target_time = opening_time
        show_time = closing_time
        schedule.clear()

    return {show_date: master_schedule}


def load_config():
    """ Load the configuration file
    :return: dictionary of configuration file
    """
    with open("app.yaml") as stream:
        return yaml.load(stream)


def get_filename():
    """ Parse command line arguments and check that filename is valied
    :return: valid file name
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=lambda s: valid_file_ext(s.lower()))
    return parser.parse_args().filename


def print_master_schedule(master_schedule):
    """ Print master schedule to the console
    :param master_schedule:
    :return: no return value
    """
    for key, value in master_schedule.items():
        print("{0} \n".format(get_formatted_date(key)))
        for movie in master_schedule[key]:
            print("{0} - Rated {1}, {2}".format(movie.movie_title, movie.mpaa_rating, movie.run_time))
            for movie_times in master_schedule[key][movie]:
                print("\t{0} = {1}".format(movie_times[0], movie_times[1]))
            print()
    return

def main(filename):
    """ main program controller
    :param filename: the filename that contains movies for scheduling
    :return: no return value
    """
    opening_time, closing_time, setup_time, schedule_dt = setup()
    movies = get_movies(filename)
    master_schedule = generate_schedule(movies, opening_time, closing_time, setup_time, schedule_dt)
    print_master_schedule(master_schedule)
    print("Successfully processed {0}".format(filename))
    return

def get_config_file_values(weekend_or_weekday, dt):
    """
    :param weekend_or_weekday: str that is weekend or weekday to load the
    appropriate config value
    :param dt: datetime to generate schedule for
    :return: tuple of
                    opening_time - datetime - adjusted to allow morning setup
                    closing_time - datetime - closing time
                    setup_time - interval in minutes to allow cleanup between movie showings
                    dt - datetime for the day that is being scheduled
    """
    hr = config[weekend_or_weekday]["open-hr"]
    min = config[weekend_or_weekday]["open-min"]
    opening_offset = config[weekend_or_weekday]["open-offset"]
    opening_time = datetime(get_year(dt), get_month(dt), get_day(dt), hr, min) + timedelta(minutes=opening_offset)
    hr = config[weekend_or_weekday]["close-hr"]
    min = config[weekend_or_weekday]["close-min"]
    closing_time = datetime(get_year(dt), get_month(dt), get_day(dt), hr, min)
    setup_time = config[weekend_or_weekday]["setup-time"]
    return opening_time, closing_time, setup_time, dt


def setup():
    """ setup values from configuration file depending on whether the day to be scheduled is
    a weekend or weekday
    :return: tuple of
                    opening_time - datetime - adjusted to allow morning setup
                    closing_time - datetime - closing time
                    setup_time - interval in minutes to allow cleanup between movie showings
                    dt - datetime for the day that is being scheduled
    """
    dt = get_starting_point_date()
    if get_day_of_week(dt) in WEEKEND:
        return get_config_file_values("weekend", dt)
    else:
        return get_config_file_values("weekday", dt)


if __name__ == '__main__':
    config = load_config()
    main(get_filename())
