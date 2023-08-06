
import json
import logging
import os
import readline

import click
import requests

from vins_cli.exceptions import VinsCfgParseError
import vins_cli.settings as settings


def command():
    uuid = get_random_uuid()

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

        token_client = cfg['app'].get('tokens').get('client')
        vins_url = cfg['app'].get('vins_url')
        app_id = cfg['app'].get('app_id')

        if token_client is None:
            raise VinsCfgParseError('"tokens->client" is missing')
        if vins_url is None:
            raise VinsCfgParseError('"vins_url" is missing')
        if app_id is None:
            raise VinsCfgParseError('"app_id" is missing')

    while True:
        utterance = raw_input(">>> ").decode('utf-8')
        if not utterance.strip():
            continue
        try:
            ans = vins_request(
                vins_url, app_id, token_client, uuid, utterance
            )

            for cmd in ans['commands']:
                if cmd['command'] == "say":
                    click.secho(cmd['text'], fg='red')
                if cmd['command'] == "device":
                    form = json.dumps(
                        cmd['form'], indent=2, ensure_ascii=False
                    )
                    click.secho(form, fg='green')
        except Exception as e:
            # logging.exception(e)
            raise


def vins_request(vins_url, app_id, token_client, uuid, utterance):
    js = {
        "utterance": utterance
    }
    js = json.dumps(js, indent=2, ensure_ascii=False)

    params = {
        'lang': 'ru-Ru',
        'uuid': uuid,
        'debug': 1
    }

    headers = {
        "x-vins-app-id": app_id,
        "x-vins-client-token": token_client
    }

    r = requests.post(
        vins_url + '/vins/json',
        params=params, data=dict(request=js), headers=headers
    )

    if not r.ok:
        raise Exception(
            (
                'connection failed with error: %s' +
                ' (http error code: %d) !'
            ) % (r.text, r.status_code)
        )

    return r.json()


def get_random_uuid():
    import random

    return ''.join(random.sample('1234567890abcdefg', 8))
