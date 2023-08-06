import click

class DiDataCLIPreArguments(object):
    def __init__(self):
        self.verbose = False

pass_prearguments = click.make_pass_decorator(DiDataCLIPreArguments, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@pass_prearguments
def cli(config, verbose):
    if verbose:
        click.echo('Verbose mode enabled')

@cli.command()
@click.option('--string', default='World')
@pass_prearguments
def say(config, string):
    click.echo(string)

@cli.group()
@click.option('--new_string', default='Hello')
@pass_prearguments
def new_say(config, new_string):
   click.echo(new_string)

@new_say.command()
@click.option('--new_string', default='Hello')
@pass_prearguments
def new_say(config, new_string):
   click.echo(new_string)

