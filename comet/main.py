"""
The entry point of the comet cli program.
"""
import click
import os
import urllib.request
import csv
import glob
import codecs
from comet.config import passConfig
from datetime import datetime



@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-d', '--data-folder', type=click.Path(exists=True),
              help='The folder in which data from the climate sensor is stored.')
@click.option('-c', '--config-file', type=click.File(mode='r'),
              help='Specifies a config file for this program to read.')
@passConfig
def cli(config, verbose, data_folder, config_file):
    """Command line tool for managing data from Comet Web Sensors."""
    config.read_conf(config_file)
    config.verbose = verbose
    if data_folder is not None:
        config.dataFolder = data_folder





@cli.command()
@click.argument('url')
@passConfig
def fetch(config, url):
    """Fetches and stores metrics from Sensor at the URL given."""
    new_file = config.data_folder + datetime.now().strftime('%Y-%m-%d_%H:%M:%S.csv')
    if not url.startswith('http://'):
        url = 'http://' + url
    url += '/export_comma.csv'

    if config.verbose:
        click.echo('Fetching data from' + url + 'and saving it in' + new_file)

    previous_file = sorted(os.listdir(config.data_folder))[-1]

    try:
        urllib.request.urlretrieve(url, new_file)
    except urllib.error.URLError as e:
        click.echo('Failed to establish an HTTP connection.')
        click.echo(e.reason)
        exit(1)
    except urllib.error.HTTPError as e:
        click.echo('Managed to connect but failed with HTTP Error code: ' + e.code)
        click.echo(e.reason)
        exit(1)

    # Here we'll try to remove overlapping data points.




@cli.command()
@click.option('-o', '--out-path', default='./all_data.csv',
              help='Specifies which path to output to.')
@passConfig
def dump(config, out_path):
    """Output one big csv file containing all the data gathered thus far."""
    if config.verbose:
        click.echo('Dumping to' + outpath)

    rows = []
    reader = None
    for path in glob.iglob(config.data_folder + '*.csv'):
        with codecs.open(path, 'r', encoding='latin1') as inFile:
            reader = csv.reader(inFile)
            for row in reader:
                if row not in rows:
                    rows.append(row)

    if not reader:
            click.echo('No csv files found, nothing to do')
            exit(1)

    with open(out_path, 'w') as outFile:
        writer = csv.writer(outFile)
        for row in rows:
            writer.writerow(row)

@cli.command()
@click.argument('out-path', type=click.Path(), required=False)
@passConfig
def write_conf(config, out_path):
    """Write a config file based on the given arguments to out-path.
    Defaults to the standard config file location for your operating system."""
    config.write_conf(out_path)
