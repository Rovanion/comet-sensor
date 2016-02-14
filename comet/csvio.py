# -*- coding: utf-8 -*-
"""
Library for comet-sensor containing functions related to csv file io.
"""


import sys
import csv
import glob
import click
import codecs
import comet.time as time
from comet.config import pass_config


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
    return sorted(rows, key=time.datetime_from_row)


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
