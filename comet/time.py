"""Is it really that time again, Mr. Freeman?"""


import datetime


def datetime_from_row(row, cutoff=None):
    """Get the full date and time from the data point row."""
    from comet.data import not_data_point
    if not_data_point(row):
        return datetime.datetime(1970, 1, 1)
    return datetime_from_field(row[0], cutoff)


def datetime_from_field(field, cutoff=None):
    """Get the full date and time from the format given by the comet sensor."""
    time = datetime.datetime.strptime(field, '%H:%M:%S %Y-%m-%d')
    if cutoff is None:
        return time
    elif cutoff == 'second':
        return time.replace(second=0)
    elif cutoff == 'minute':
        return time.replace(second=0, minute=0)
    elif cutoff == 'hour':
        return time.replace(second=0, minute=0, hour=0)
