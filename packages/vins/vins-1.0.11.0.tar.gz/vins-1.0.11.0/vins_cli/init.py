
import json
import os

import click
import requests

from vins_cli.exceptions import VinsCfgParseError
import vins_cli.settings as settings
from vins_cli.default import DEFAULT_VINS_CFG_FILE_TPL
from vins_cli.default import DEFAULT_INTENT_DONT_UNDERSTAND_TPL
from vins_cli.default import DEFAULT_INTENT_GOODBYE_TPL
from vins_cli.default import DEFAULT_INTENT_GREETING_TPL
from vins_cli.default import DEFAULT_INTENT_HOW_ARE_YOU_TPL
from vins_cli.default import DEFAULT_INTENT_THANKS_TPL
from vins_cli.default import DEFAULT_NLG_DONT_UNDERSTAND_TPL
from vins_cli.default import DEFAULT_NLG_GOODBYE_TPL
from vins_cli.default import DEFAULT_NLG_GREETING_TPL
from vins_cli.default import DEFAULT_NLG_HOW_ARE_YOU_TPL
from vins_cli.default import DEFAULT_NLG_THANKS_TPL
from vins_cli.default import DEFAULT_NLU_GOODBYE_TPL
from vins_cli.default import DEFAULT_NLU_GREETING_TPL
from vins_cli.default import DEFAULT_NLU_HOW_ARE_YOU_TPL
from vins_cli.default import DEFAULT_NLU_THANKS_TPL


def command(api_key, vins_url):
    click.secho('Registering a new application...', fg='blue')
    js = register_app(api_key, vins_url)

    click.secho('Making Vinsfile...', fg='blue')
    cfg = DEFAULT_VINS_CFG_FILE_TPL % dict(
        app_id=js['app_id'],
        token_admin=js['tokens']['admin'],
        token_client=js['tokens']['client'],
        api_key=api_key,
        vins_url=vins_url
    )
    cfg = json.loads(cfg)

    with open(settings.VINS_CFG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

    click.secho('Making subfolders...', fg='blue')

    os.mkdir('intents')
    os.mkdir('nlu')
    os.mkdir('nlg')

    click.secho('Making default commands...', fg='blue')

    with open("intents/dont_understand.js", "w") as f:
        f.write(DEFAULT_INTENT_DONT_UNDERSTAND_TPL)
    with open("intents/goodbye.js", "w") as f:
        f.write(DEFAULT_INTENT_GOODBYE_TPL)
    with open("intents/greeting.js", "w") as f:
        f.write(DEFAULT_INTENT_GREETING_TPL)
    with open("intents/how_are_you.js", "w") as f:
        f.write(DEFAULT_INTENT_HOW_ARE_YOU_TPL)
    with open("intents/thanks.js", "w") as f:
        f.write(DEFAULT_INTENT_THANKS_TPL)

    with open("nlg/dont_understand.nlg", "w") as f:
        f.write(DEFAULT_NLG_DONT_UNDERSTAND_TPL)
    with open("nlg/goodbye.nlg", "w") as f:
        f.write(DEFAULT_NLG_GOODBYE_TPL)
    with open("nlg/greeting.nlg", "w") as f:
        f.write(DEFAULT_NLG_GREETING_TPL)
    with open("nlg/how_are_you.nlg", "w") as f:
        f.write(DEFAULT_NLG_HOW_ARE_YOU_TPL)
    with open("nlg/thanks.nlg", "w") as f:
        f.write(DEFAULT_NLG_THANKS_TPL)

    with open("nlu/goodbye.nlu", "w") as f:
        f.write(DEFAULT_NLU_GOODBYE_TPL)
    with open("nlu/greeting.nlu", "w") as f:
        f.write(DEFAULT_NLU_GREETING_TPL)
    with open("nlu/how_are_you.nlu", "w") as f:
        f.write(DEFAULT_NLU_HOW_ARE_YOU_TPL)
    with open("nlu/thanks.nlu", "w") as f:
        f.write(DEFAULT_NLU_THANKS_TPL)

    click.secho("Done !", fg='green')


def register_app(api_key, vins_url):
    headers = {
        "x-vins-api-key": api_key
    }
    r = requests.get(vins_url + "/reg_app", headers=headers)
    if not r.ok:
        raise VinsCfgParseError(
            'application registration failed' +
            ' (http error code: %d) !' % r.status_code,
        )

    return r.json()
