#!/usr/bin/env python3

import click
import urllib.request
from datetime import datetime

class Config(object):
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def cli(config, verbose):
    """Command line tool for managing data from Comet Web Sensors."""
    config.verbose = verbose


@cli.command()
@click.option('--url', default='http://192.168.1.213/',
              help='The base url of your web sensor.')
@pass_config
def fetch(config, url):
    """Fetches metrics from Sensor."""
    dataPath = 'data/' + datetime.now().strftime('%Y-%m-%d_%H:%:M%S')

    if config.verbose:
        click.echo('Fetching data from' + url + 'and saving it in' + dataPath)

    try:
        urllib.request.urlretrieve(url, dataPath)
    except urllib.error.URLError as e:
        click.echo('Failed to establish an HTTP connection.')
        click.echo(e.reason)
    except urllib.error.HTTPError as e:
        click.echo('Managed to connect but failed with HTTP Error code: ' + e.code)
        click.echo(e.reason);
