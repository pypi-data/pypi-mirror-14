import os
from os.path import expanduser
import json

import requests
import click


default_config = {
    'base_url': "",
    'username': None,
    'password': None,
}


def _read_config():
    home = expanduser("~")
    path = os.path.join(home, '.frojd-intranet')

    if not os.path.exists(path):
        raise Exception('Missing config file at {0}'.format(path))

    with open(path, 'r') as config_file:
        raw_content = config_file.read()

    config_data = json.loads(raw_content)
    return config_data


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    user_config = _read_config()

    config = ctx.obj.copy()
    config.update(user_config)

    ctx.obj = config


@cli.command()
@click.option('--project')
@click.pass_context
def stages(ctx, project):
    '''
    List all stages containing to project

    Example:
        frojd-intranet stages --project="My project"

    Returns:
        Demo
        Stage
        Prod
    '''
    params = {
        'project': project,
    }

    config = ctx.obj

    method = 'stages'
    response = requests.get("{0}/wp-json/api-sarch/v1/{1}".format(
        config.get('base_url'), method),
        params=params, auth=(config.get('username'), config.get('password')))
    _handle_response(response)


def _handle_response(response):
    try:
        data = response.json()
    except Exception as e:
        pass

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:  # NOQA
        click.echo(data.get('message'))

    for value in data:
        click.echo(value)


@cli.command()
@click.option('--project')
@click.option('--stage', default="")
@click.option('--search', default="")
@click.pass_context
def search(ctx, project, stage, search):
    '''
    List all stages containing to project

    Example:
        frojd-intranet search --project="My project"

    Returns:
        My project
        My project 1

    ...Or show stage values

    Example:
        frojd-intranet search --project="My project" --stage="Prod"

    Returns:
        ### SSH
        Host: 127.0.0.1

    ...Or find field on stage

    Example:
        frojd-intranet search --project="My project" --stage="Prod" --search="SSH:Host"

    Returns:
        Host: 127.0.0.1
    '''
    config = ctx.obj

    section = ''
    field = ''

    if search:
        if ':' in search:
            section, field = search.split(":")
        else:
            field = search

    params = {
        'project': project,
    }

    if stage:
        params['stage'] = stage

    if section:
        params['section'] = section

    if field:
        params['field'] = field

    method = 'field'

    if set(params.keys()) == set(['project']):
        method = 'project'

    response = requests.get("{0}/wp-json/api-sarch/v1/{1}".format(
        config.get('base_url'), method),
        params=params, auth=(config.get('username'), config.get('password')))
    _handle_response(response)


def main():
    cli(obj=default_config)
