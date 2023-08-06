

import json
import os

import click
import requests

from vins_cli.exceptions import VinsCfgParseError
import vins_cli.settings as settings


def command(force_register):
    if force_register:
        click.secho('Registering a new application (force)...', fg='blue')

        with open(settings.VINS_CFG_PATH, "r") as f:
            cfg = json.load(f)

            if cfg.get('app') is None:
                raise VinsCfgParseError('"app" section is missing')
            if cfg.get('app').get('tokens') is None:
                raise VinsCfgParseError('"tokens" section is missing')

            api_key = cfg['app'].get('api_key')
            vins_url = cfg['app'].get('vins_url')
            app_id = cfg['app'].get('app_id')
            tokens = dict(
                admin=cfg['app']['tokens'].get('admin'),
                client=cfg['app']['tokens'].get('client')
            )

            if api_key is None:
                raise VinsCfgParseError('"api_key" is missing')
            if vins_url is None:
                raise VinsCfgParseError('"vins_url" is missing')
            if app_id is None:
                raise VinsCfgParseError('"app_id" is missing')
            if tokens['admin'] is None:
                raise VinsCfgParseError('"admin token" is missing')
            if tokens['client'] is None:
                raise VinsCfgParseError('"client token" is missing')

            register_app(api_key, vins_url, app_id, tokens)

            click.secho('Done!', fg='green')

    click.secho("Deploying...", fg='blue')

    if not os.path.exists(settings.VINS_CFG_PATH):
        raise VinsCfgParseError(
            "file %s does not exist" % settings.VINS_CFG_PATH
        )

    with open(settings.VINS_CFG_PATH, "r") as f:
        cfg = json.load(f)

        # - checking app section -

        if cfg.get('app') is None:
            raise VinsCfgParseError('"app" section is missing')
        if cfg.get('app').get('tokens') is None:
            raise VinsCfgParseError('"tokens" section is missing')

        api_key = cfg['app'].get('api_key')
        tokens = dict(
            admin=cfg['app']['tokens']['admin'],
            client=cfg['app']['tokens']['client']
        )
        vins_url = cfg['app'].get('vins_url')
        app_id = cfg['app'].get('app_id')

        # if api_key is None:
        #     raise VinsCfgParseError('"api_key" is missing')
        if tokens['admin'] is None:
            raise VinsCfgParseError('"admin token" is missing')
        if tokens['client'] is None:
            raise VinsCfgParseError('"client token" is missing')
        if vins_url is None:
            raise VinsCfgParseError('"vins_url" is missing')
        if app_id is None:
            raise VinsCfgParseError('"app_id" is missing')

        # - checking dm section -

        if cfg.get('dm') is None:
            raise VinsCfgParseError('"dm" section is missing')

        if cfg['dm'].get('intents') is None:
            raise VinsCfgParseError('"dm.intents" section is missing')

        if not isinstance(cfg['dm']['intents'], list):
            raise VinsCfgParseError('"dm.intents" must be a list')

        # - checking nlu section -

        if cfg.get('nlu') is None:
            raise VinsCfgParseError('"nlu" section is missing')

        if cfg['nlu'].get('intents') is None:
            raise VinsCfgParseError('"nlu.intents" section is missing')

        if not isinstance(cfg['nlu']['intents'], list):
            raise VinsCfgParseError('"nlu.intents" must be a list')

        # - checking nlg section -

        if cfg.get('nlg') is None:
            raise VinsCfgParseError('"nlg" section is missing')

        if cfg['nlg'].get('intents') is None:
            raise VinsCfgParseError('"nlg.intents" section is missing')

        if not isinstance(cfg['nlg']['intents'], list):
            raise VinsCfgParseError('"nlg.intents" must be a list')

        # - sending files -

        files = {
            'config': open(settings.VINS_CFG_PATH, 'rb')
        }

        for m in cfg['dm']['intents']:
            path = m['path']
            files[path] = open(path, 'rb')
        for m in cfg['nlu']['intents']:
            path = m['path']
            files[path] = open(path, 'rb')
        for m in cfg['nlg']['intents']:
            path = m['path']
            files[path] = open(path, 'rb')

        headers = {
            "x-vins-app-id": app_id,
            "x-vins-api-key": api_key,
            "x-vins-admin-token": tokens['admin']
        }

        r = requests.post(vins_url + "/deploy", files=files, headers=headers)
        if not r.ok:
            raise VinsCfgParseError(
                (
                    'deploy failed with error: %s' +
                    ' (http error code: %d) !'
                ) % (r.text, r.status_code)
            )

        # - done -

    click.secho("Done !", fg='green')


def register_app(api_key, vins_url, app_id, tokens):
    headers = {
        "x-vins-api-key": api_key,
        "x-vins-app-id": app_id,
        "x-vins-admin-token": tokens['admin'],
        "x-vins-client-token": tokens['client']
    }
    r = requests.get(vins_url + "/force_reg_app", headers=headers)
    if not r.ok:
        raise VinsCfgParseError(
            'application registration failed (force)' +
            ' (http error code: %d) !' % r.status_code,
        )
