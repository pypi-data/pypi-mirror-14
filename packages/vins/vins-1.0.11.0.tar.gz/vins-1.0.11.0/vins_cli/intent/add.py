
import json
import logging
import os

import click

from vins_cli.exceptions import VinsCfgParseError
import vins_cli.settings as settings
from vins_cli.default import NEW_INTENT_TPL
from vins_cli.default import NEW_INTENT_NLU_TPL
from vins_cli.default import NEW_INTENT_NLG_TPL


def command(intent_name):
    click.secho('Creating intent %s...' % intent_name, fg='blue')

    if not os.path.exists(settings.VINS_CFG_PATH):
        raise VinsCfgParseError(
            "file %s does not exist" % settings.VINS_CFG_PATH
        )

    with open(settings.VINS_CFG_PATH, "r") as f:
        cfg = json.load(f)

        # - checking app section -

        if cfg.get('app') is None:
            raise VinsCfgParseError('"app" section is missing')

        api_key = cfg['app'].get('api_key')
        vins_url = cfg['app'].get('vins_url')
        app_id = cfg['app'].get('app_id')

        if api_key is None:
            raise VinsCfgParseError('"api_key" is missing')
        if vins_url is None:
            raise VinsCfgParseError('"vins_url" is missing')
        if app_id is None:
            raise VinsCfgParseError('"app_id" is missing')

        intent_path = "intents/%s.js" % intent_name
        nlg_path = "nlg/%s.nlg" % intent_name
        nlu_path = "nlu/%s.nlu" % intent_name

        click.secho('Creating files...', fg='blue')

        with open(intent_path, "w") as f_intent:
            f_intent.write(NEW_INTENT_TPL % dict(intent=intent_name))
        with open(nlg_path, "w") as f_nlg:
            f_nlg.write(NEW_INTENT_NLG_TPL)
        with open(nlu_path, "w") as f_nlu:
            f_nlu.write(NEW_INTENT_NLU_TPL)

        click.secho('Registering files into Vinsfile...', fg='blue')

        cfg['dm']['intents'].append({
            "intent": intent_name,
            "path": intent_path
        })
        cfg['nlg']['intents'].append({
            "intent": intent_name,
            "path": nlg_path
        })
        cfg['nlu']['intents'].append({
            "intent": intent_name,
            "path": nlu_path
        })

    with open(settings.VINS_CFG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

    click.secho('Done!', fg='green')
