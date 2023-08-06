#!/usr/bin/env python2.7
# vim: set fileencoding=utf-8

import click

from vins_cli.exceptions import VinsCfgParseError


@click.group()
def main():
    """Voice INterfaces Service command line interface"""


@click.command()
@click.option(
    "--api-key",
    envvar='VINS_API_KEY',
    prompt="Enter VINS API key",
    help="VINS API key"
)
@click.option(
    "--vins-url",
    envvar='VINS_URL',
    prompt="Enter VINS url",
    help="VINS service url"
)
def init(api_key, vins_url):
    """initializes a new VINS environment by creating a Vinsfile"""

    import vins_cli.init

    try:
        vins_cli.init.command(api_key, vins_url)
    except VinsCfgParseError as e:
        click.secho('Error: %s !!!' % e.message, fg='red')
        exit(1)


@click.command()
def client():
    """connects to the server and tests the dialog"""

    import vins_cli.client

    try:
        vins_cli.client.command()
    except Exception as e:
        click.secho('Error: %s !!!' % e.message, fg='red')
        exit(1)


@click.command()
@click.option(
    "--force-register",
    is_flag=True,
    default=False,
    help="force register app_id and deploy"
)
def deploy(force_register):
    """deploy to the server"""

    import vins_cli.deploy

    try:
        vins_cli.deploy.command(force_register)
    except Exception as e:
        click.secho('Error: %s !!!' % e.message, fg='red')
        exit(1)


@click.command()
@click.option(
    "--add",
    help="add new intent"
)
def intent(add):
    """intent manipulations"""

    if add is not None:
        import vins_cli.intent.add
        try:
            vins_cli.intent.add.command(add)
        except Exception as e:
            click.secho('Error: %s !!!' % e.message, fg='red')
            exit(1)


def cli():
    main.add_command(init)
    main.add_command(client)
    main.add_command(deploy)
    main.add_command(intent)
    main(auto_envvar_prefix='VINSCLI')
