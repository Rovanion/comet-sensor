# -*- coding: utf-8 -*-
"""
The entry point of the comet-sensor cli program.
"""
import os
import sys
import glob
import click
import datetime
import urllib.request
import comet.time as time
import comet.data as data
import comet.csvio as csvio
import comet.plot as plotter
from datetime import timedelta
from comet.config import pass_config


@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-d', '--data-folder', type=click.Path(exists=True),
              help='The folder in which data from the climate sensor is stored.')
@click.option('-c', '--config-file', type=click.File(mode='r'),
              help='Specifies a config file for this program to read.')
@pass_config
def cli(config, verbose, data_folder, config_file):
    """Command line tool for managing data from Comet Web Sensors."""
    config.read_conf(config_file)
    config.verbose = verbose
    if data_folder is not None:
        config.data_folder = data_folder


@cli.command()
@click.argument('url')
@pass_config
def fetch(config, url):
    """Fetches and stores metrics from Sensor at the URL given."""
    new_path = os.path.join(config.data_folder, datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.csv'))
    new_temp_path = new_path + 'temp'
    if not url.startswith('http://'):
        url = 'http://' + url
    url += '/export.csv'

    if config.verbose:
        click.echo('Fetching data from ' + url + ' and saving it in ' + new_temp_path)

    try:
        previous_path = sorted(glob.glob(config.data_folder + '/*.csv'))[-1]
    except IndexError:
        previous_path = None

    try:
        urllib.request.urlretrieve(url, new_temp_path)
    except urllib.error.URLError as e:
        click.echo('Failed to establish an HTTP connection.')
        click.echo(e.reason)
        sys.exit(1)
    except urllib.error.HTTPError as e:
        click.echo('Managed to connect but failed with HTTP Error code: ' + e.code)
        click.echo(e.reason)
        sys.exit(2)

    try:
        new_rows = csvio.loadOne(new_temp_path)
        if not new_rows[0][0] == "Device:":
            click.echo('Managed to connect and fetch data from something, '
                       'but it was not a CSV from a Comet Web Sensor.')
            click.echo((new_rows[0][0]))
            sys.exit(3)

        # Here we'll try to remove overlapping data points with the last file.
        # It get's nasty due to time ajustments done by the sensor.
        if previous_path is not None:
            previous_rows = csvio.loadOne(previous_path)
            data_start = data.get_first_data_point_index(previous_rows)
            print(data_start)
            print(previous_rows[:data_start])
            time_of_newest_data_in_previous = time.datetime_from_row(previous_rows[data_start], 'second')
            filtered_rows = []
            for row in new_rows:
                if data.not_data_point(row):
                    continue
                time_of_row = time.datetime_from_row(row)
                if time_of_newest_data_in_previous < time_of_row:
                    filtered_rows.append(row)

            if not filtered_rows:
                if config.verbose:
                    click.echo('No new rows found in fetched data.')
                sys.exit(0)
        else:
            filtered_rows = new_rows

        if config.verbose:
            click.echo('Rewriting treated CSV to: ' + new_path)
        csvio.writeRows(filtered_rows, new_path)
    finally:
        os.remove(new_temp_path)


@cli.command()
@click.option('-o', '--out-path', default='./all_data.csv',
              help='Specifies which path to output to.')
@pass_config
def dump(config, out_path):
    """Output one big csv file containing all the data gathered thus far."""
    if config.verbose:
        click.echo('Dumping to' + out_path)
    rows = csvio.loadAll()
    csvio.writeRows(rows, out_path)


@cli.command()
@click.argument('out-path', type=click.Path(), required=False)
@pass_config
def write_conf(config, out_path):
    """Write a config file based on the given arguments to out-path.
    Defaults to the standard config file location for your operating system."""
    config.write_conf(out_path)


@cli.command()
@click.option('-t', '--type', type=click.Choice(['scatter', 'line', 'box']),
              help='The style of the plot.', prompt=True, default='scatter')
@click.option('-g', '--group-by', type=click.Choice(['none', 'day', 'week']),
              help='Whether to group data by any length.', prompt=True)
@click.option('-e', '--exclude', type=click.IntRange(1, 4), multiple=True,
              help="Exclude certain data channels from the plot.")
@click.option('-i', '--include', type=click.IntRange(1, 4), multiple=True,
              help="Include only the specified data channels in the plot.")
@click.option('-s', '--sample-width', type=click.IntRange(1, 1440), default=10,
              help="The with of each sample for statistical graphs in minutes.")
@click.option('-b', '--business-days-only', flag_value=True,
              help="Only include business days into the graph.")
@click.option('-w', '--weekends-only', flag_value=True,
              help="Only include week days into the graph.")
@click.option('-n', '--no-outliers', flag_value=True,
              help="Don't plot outliers when doing statistical plots.")
@click.option('-o', '--out-file', type=click.Path(),
              help="The file to which the graph is written.")
@pass_config
def plot(config, type, group_by, sample_width, exclude, include, weekends_only,
         business_days_only, no_outliers, out_file):
    """Plot the stored data.
    """
    if exclude:
        include = [i for i in include if i not in exclude]
    plotter.plot(config, type, group_by, sample_width, weekends_only,
                 business_days_only, no_outliers, out_file, list(set(include)))
