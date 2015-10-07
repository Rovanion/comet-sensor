import click
import urllib.request
import csv
import glob
import codecs
from config import passConfig
from datetime import datetime



@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.option('-d', '--data-folder', default='./data/',
              help='The folder in which data from the climate sensor is stored.')
@passConfig
def cli(config, verbose, data_folder):
    """Command line tool for managing data from Comet Web Sensors."""
    if verbose:
        config.verbose = verbose
    if data_folder:
        config.dataFolder = data_folder



@cli.command()
@click.argument('url')
@passConfig
def fetch(config, url):
    """Fetches and stores metrics from Sensor at the URL given."""
    dataPath = 'data/' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S.csv')
    if not url.startswith('http://'):
        url = 'http://' + url
    url += '/export_comma.csv'

    if config.verbose:
        click.echo('Fetching data from' + url + 'and saving it in' + dataPath)

    try:
        urllib.request.urlretrieve(url, dataPath)
    except urllib.error.URLError as e:
        click.echo('Failed to establish an HTTP connection.')
        click.echo(e.reason)
        exit(1)
    except urllib.error.HTTPError as e:
        click.echo('Managed to connect but failed with HTTP Error code: ' + e.code)
        click.echo(e.reason);
        exit(1)



@cli.command()
@click.option( '-o', '--out-path', default='./all_data.csv',
              help='Specifies which path to output to.')
@passConfig
def dump(config, out_path):
    """Output one big csv file containing all the data gathered thus far."""
    if config.verbose:
        click.echo('Dumping to' + outpath)

    rows = []
    reader = None
    for path in glob.iglob(config.dataFolder + '*.csv'):
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
