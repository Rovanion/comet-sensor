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
            data_start = csvio.get_first_data_point_index(previous_rows)
            latest_previous_date = previous_rows[data_start][0].split(' ')[1]
            latest_previous_H_M = ':'.join(previous_rows[data_start][0].split(' ')[0].split(':')[0:2])
            time_of_newest_data_in_previous = datetime.datetime.strptime(
                latest_previous_date + ' ' + latest_previous_H_M,
                '%Y-%m-%d %H:%M') + timedelta(minutes=1)

            filtered_rows = []
            for row in new_rows:
                if csvio.not_data_point(row):
                    continue
                time_of_row = csvio.date_from_row(row)
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
@click.option('-t', '--type', type=click.Choice(['scatter', 'line']),
              help='The style of the plot.', prompt=True, default='scatter')
@click.option('-g', '--group-by', type=click.Choice(['none', 'day', 'week', 'month']),
              help='Whether to group data by any length.', prompt=True)
@pass_config
def plot(config, type, group_by):
    """Plot the stored data.
    """
    plotter.plot(config, type, group_by)
