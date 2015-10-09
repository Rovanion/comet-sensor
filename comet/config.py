import click

class Config(object):
    def __init__(self):
        self.verbose = False

passConfig = click.make_pass_decorator(Config, ensure=True)
