import argparse
import csv
import os

from collections import namedtuple
from datetime import datetime, timedelta

import pyyaml

TESTFILENAME = 'movies.csv'
VALIDFILEEXT = 'csv'
fields =  ('movie_title', 'release_year', 'mpaa_rating', 'run_time')


def get_movies(filename):
    """ Read in a csv file of movies
    :param filename: name of movie file entered in command line
    :return: list of movies
    """
    Movie = namedtuple('Movie', fields)
    movies = []

    with open(filename, newline="" ) as infile:
        reader = csv.reader(infile)
        header = next(reader)
        Movie = namedtuple("Movie", fields)
        for data in map(Movie._make, reader):
            movies.append(data)

    return movies

def open_time():
    return datetime(2016, 1, 8, 12, 0)

def close_time():
    return datetime(2016, 1, 8, 23, 0)

def get_the_time(h, m):
    return datetime(2016, 1, 8, h, m)

def parse_real_run_time(the_time):
    x, y = the_time.split(":")
    return int(x), int(y)

def parse_run_time(close):
    x, y = close.split(':')
    #new_y = y[:]
    z = int(y)%10

    if z < 5:
        new_y = int(y) + 5 - z
        new_x = int(x)

        if int(y) < 5:
            new_y = 5

    elif 5 < z < 10:
        new_x = int(x)
        new_y = int(y) + 10 - z
        if new_y == 60:
            new_x = int(x)+1
            new_y = 0

    #print (x, y, new_x, new_y, z)

    return new_x, new_y
#    print (x)

def to_datetime_object(date_string, date_format):
    s = datetime.strptime(date_string, date_format)
    return s

def go_back(movie, close):
    h, m = parse_run_time(movie)
    #print(h, m)
    goBack = close - timedelta(hours=h, minutes=m)
    #print(goBack)
    return goBack

def valid_file_ext(filename):
    """ Check if the filename has a valid extension
    :param filename: filename entered at the command line
    :return: filename if it has a valid extension
    """
    ext = os.path.splitext(filename)[1][1:]

    if ext != VALIDFILEEXT:
       parser.error("Please submit a csv file")

    return filename

def format_movie_over_time(movie_over):
    return datetime.strftime(movie_over, '%I:%M %p')

def generate_schedule(movies):
    time_compare = open_time()

    show_time = close_time()

    schedule = []

    for movie in movies:
        print (movie)
        h_r , m_r = parse_real_run_time(movie.run_time)
        print (h_r, m_r)
        h, m = parse_run_time(movie.run_time)
        show_time = go_back(movie.run_time, show_time)
        schedule.append((datetime.strftime(show_time, '%I:%M %p'), format_movie_over_time(show_time + timedelta(hours=h_r, minutes=m_r))))
        while show_time > time_compare:
            show_time = show_time - timedelta(minutes=35)
            show_time = go_back(movie.run_time, show_time)
            if show_time > time_compare:
                #print(show_time, time_compare)
                schedule.append((datetime.strftime(show_time, '%I:%M %p'),
                          format_movie_over_time(show_time + timedelta(hours=h_r, minutes=m_r))))

        print(schedule[::-1])
        time_compare = open_time()
        show_time = close_time()
        schedule.clear()

    return schedule[::-1]



def print_schedule(schedule):
    pass


def main(filename):
    movies = get_movies(filename)

    generate_schedule(movies)
    print("Successfully processed {}".format(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',type=lambda s:valid_file_ext(s.lower()))
    args = parser.parse_args()
    main(args.filename)
