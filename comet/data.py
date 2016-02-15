# -*- coding: utf-8 -*-
"""Functions related to the loaded data."""


import re
import datetime
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


def group(data, group_by, sample_width):
    """Groups the data columns into heaps of data."""
    import datetime

    groups = [[[]]]
    for i in range(4):
        groups[0].append([])

    cutoff = 'second'
    beginning_of_period = time.datetime_from_row(data[get_first_data_point_index(data)], cutoff)
    period = datetime.timedelta(days=1000000)
    if group_by == 'day':
        period = datetime.timedelta(days=1)
    elif group_by == 'week':
        period = datetime.timedelta(weeks=1)
    elif group_by == 'month':
        period = datetime.timedelta(months=1)
    sample_width = datetime.timedelta(minutes=sample_width)
    group_index = 0
    first_round = True

    for row in data:
        datetime_current_row = time.datetime_from_row(row, cutoff)
        # Is it time to start adding data from the beginning of the period again?
        if datetime_current_row - beginning_of_period >= period:
            beginning_of_period = datetime_current_row
            group_index = 0
            first_round = False
        # Did we just go outside the current sample? A sample is e.g. a singe box in a box plot.
        if datetime_current_row >= beginning_of_period + sample_width * (group_index+1):
            group_index += 1
            if first_round:
                groups.append([])
            if len(groups[group_index]) < 1:
                groups[group_index] = [[] for i in range(5)]
            for i in range(5):
                groups[group_index][i].append(row[i])
        else:
            for i in range(5):
                groups[group_index][i].append(row[i])

    return groups


def rotate(list, steps):
    """Rotate the data inside a list some number of steps."""
    return list[steps:] + list[:steps]


def rotate_group_with_time_to_start(groups, hour):
    """Given a list of grouped data points according to data.group() this function
    will return the same list but rotated so that the data at time hour is first.
    """
    index = 0
    if time.time_from_field(groups[0][0][0]).time() > hour:
        for i in range(len(groups)-1, 0, -1):
            if time.time_from_field(groups[i][0][0], 'second').time() <= hour:
                index = i
                break
    else:
        for i in range(len(groups)):
            if time.time_from_field(groups[i][0][0]).time() > hour:
                index = i
                break

    if index != 0:
        return rotate(groups, index)
    else:
        return groups
