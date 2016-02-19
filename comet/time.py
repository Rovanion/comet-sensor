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
    return cut_datetime(datetime.datetime.strptime(field, '%H:%M:%S %Y-%m-%d'), cutoff)


def time_from_field(field, cutoff=None):
    """Return only the hour, minute and second part of a field."""
    return cut_datetime(datetime.datetime.strptime(field.split(' ')[0], '%H:%M:%S'), cutoff)


def cut_datetime(time, cutoff):
    """Cut off some detail in a datetime."""
    if cutoff is None:
        return time
    elif cutoff == 'second':
        return time.replace(second=0)
    elif cutoff == 'minute':
        return time.replace(second=0, minute=0)
    elif cutoff == 'hour':
        return time.replace(second=0, minute=0, hour=0)
    else:
        raise ValueError("The specified cutoff is not a legal option.")


def dow_as_string(date):
    """Return the day of week expressed as a string."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[date.weekday()]
