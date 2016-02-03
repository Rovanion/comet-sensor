"""
Library for comet-sensor containing functions related to csv file io.
"""
import re
import sys
import csv
import glob
import click
import codecs
import datetime
from comet.config import pass_config


DATE_MATCHER = re.compile(r'\d\d:\d\d:\d\d \d{4}-\d\d-\d\d')


@pass_config
def loadAll(config):
    rows = []
    reader = None
    for path in sorted(glob.iglob(config.data_folder + '/*.csv')):
        with codecs.open(path, 'r', encoding='latin1') as in_file:
            reader = csv.reader(in_file)
            for row in reader:
                if row:
                    rows.append(row)
    if reader is None:
        click.echo('No csv files found in ' + config.data_folder + ', nothing to do.')
        sys.exit(4)
    # Deduplication.
    seen = set()
    rows = [x for x in rows if not (x[0] in seen or seen.add(x[0]))]
    return sorted(rows, key=date_from_row)


def loadOne(path):
    rows = []
    with codecs.open(path, 'r', encoding='latin1') as in_file:
        reader = csv.reader(in_file)
        for row in reader:
            rows.append(row)
    if not rows:
        click.echo('No data found in: ' + path)
        sys.exit(5)
    return rows


def writeRows(rows, out_path):
    with open(out_path, 'w') as out_file:
        writer = csv.writer(out_file)
        for row in rows:
            writer.writerow(row)


def not_data_point(row):
    """Determine if the row is a data point from the comet sensor."""
    return not row or DATE_MATCHER.match(row[0]) is None


def get_first_data_point_index(rows):
    """Get the first data point in the given list of rows."""
    data_start = 0
    while not_data_point(rows[data_start]):
        data_start += 1
    return data_start


def date_from_row(row):
    """Get the date from the data point row."""
    if not_data_point(row):
        return datetime.datetime(1970, 1, 1)
    return datetime.datetime.strptime(row[0], '%H:%M:%S %Y-%m-%d')


def get_labels(rows):
    """Get the labels of a CSV file from the sensor."""
    return rows[get_first_data_point_index(rows) - 2]
