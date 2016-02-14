# -*- coding: utf-8 -*-
"""Functions related to the loaded data."""


import re
import comet.time as time


DATE_MATCHER = re.compile(r'\d\d:\d\d:\d\d \d{4}-\d\d-\d\d')


def not_data_point(row):
    """Determine if the row is a data point from the comet sensor."""
    return not row or DATE_MATCHER.match(row[0]) is None


def get_first_data_point_index(rows):
    """Get the first data point in the given list of rows."""
    data_start = 0
    while not_data_point(rows[data_start]):
        data_start += 1
    return data_start


def get_labels(rows):
    """Get the column labels from the rows of a CSV file from the sensor."""
    return rows[get_first_data_point_index(rows) - 2]


def get_columns(rows):
    """Turn the rows passed into a list of columns."""
    columns = list()
    for i in range(5):
        columns.append([line[i] for line in rows])
    return columns


def group(data, group_by):
    """Groups the data columns into heaps of data."""
    import datetime

    groups = list()
    group_decr = 0
    beginning_of_period = time.datetime_from_row(data[get_first_data_point_index(data)])
    period = datetime.timedelta(days=100000)
    if group_by == 'day':
        period = datetime.timedelta(days=1)
    elif group_by == 'week':
        period = datetime.timedelta(weeks=1)
    elif group_by == 'month':
        period = datetime.timedelta(months=1)

    for i in range(len(data)):
        # Is it time to start adding data from the beginning of the period again?
        if time.datetime_from_row(data[i]) - beginning_of_period >= period:
            beginning_of_period = time.datetime_from_row(data[i])
            group_decr = i
            print("Group decr: " + str(group_decr))
        if group_decr == 0:
            groups.append([data[i]])
        else:
            print(str(time.datetime_from_row(data[i]) - beginning_of_period) +
                  ",  period: " + str(period) + ",  index: " + str(i))
            groups[i - group_decr].append(data[i])
    return groups
