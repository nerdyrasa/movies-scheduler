import argparse
import csv
import os

from collections import namedtuple

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


def valid_file_ext(filename):
    """ Check if the filename has a valid extension
    :param filename: filename entered at the command line
    :return: filename if it has a valid extension
    """
    ext = os.path.splitext(filename)[1][1:]

    if ext != VALIDFILEEXT:
       parser.error("Please submit a csv file")

    return filename


def main(filename):
    movies = get_movies(filename)
    print("Successfully processed {}".format(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',type=lambda s:valid_file_ext(s.lower()))
    args = parser.parse_args()
    main(args.filename)
