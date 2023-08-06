
DEFAULT_VINS_CFG_FILE_TPL = """
{
  "app": {
    "comment": "add your comment here",
    "vins_url": "%(vins_url)s",
    "api_key": "%(api_key)s",
    "tokens": {
      "admin": "%(token_admin)s",
      "client": "%(token_client)s"
    },
    "app_id": "%(app_id)s"
  },
  "dm": {
    "engine": "form_filler",
    "intents": [{
      "intent": "dont_understand",
      "path": "intents/dont_understand.js"
    }, {
      "intent": "greeting",
      "path": "intents/greeting.js"
    }, {
      "intent": "thanks",
      "path": "intents/thanks.js"
    }, {
      "intent": "goodbye",
      "path": "intents/goodbye.js"
    }, {
      "intent": "how_are_you",
      "path": "intents/how_are_you.js"
    }]
  },
  "nlu": {
    "engine": "fuzzy",
    "intents": [{
      "intent": "greeting",
      "path": "nlu/greeting.nlu"
    }, {
      "intent": "thanks",
      "path": "nlu/thanks.nlu"
    }, {
      "intent": "goodbye",
      "path": "nlu/goodbye.nlu"
    }, {
      "intent": "how_are_you",
      "path": "nlu/how_are_you.nlu"
    }]
  },
  "nlg": {
    "engine": "fuzzy",
    "intents": [{
      "intent": "dont_understand",
      "path": "nlg/dont_understand.nlg"
    }, {
      "intent": "greeting",
      "path": "nlg/greeting.nlg"
    }, {
      "intent": "thanks",
      "path": "nlg/thanks.nlg"
    }, {
      "intent": "goodbye",
      "path": "nlg/goodbye.nlg"
    }, {
      "intent": "how_are_you",
      "path": "nlg/how_are_you.nlg"
    }]
  }
}
"""

DEFAULT_INTENT_DONT_UNDERSTAND_TPL = """
{
    "form": "dont_understand",
    "comment": "если команда не понятна, то активируется этот intent",
    "events": [
        {
            "event": "submit",
            "handler": "nlg",
            "phrase_id": "i_dont_undestand_you"
        }
    ],
    "slots": [
        {
          "slot": "utterance",
          "type": "string",
          "optional": true,
          "events": []
        }
    ]
}
"""

DEFAULT_INTENT_GOODBYE_TPL = """
{
    "form": "goodbye",
    "comment": "клиент прощается",
    "events": [
        {
            "event": "submit",
            "handler": "nlg",
            "phrase_id": "goodbye"
        }
    ]
}
"""

DEFAULT_INTENT_GREETING_TPL = """
{
    "form": "greeting",
    "comment": "клиент здоровается",
    "events": [
        {
            "event": "submit",
            "handler": "nlg",
            "phrase_id": "greeting"
        }
    ]
}
"""

DEFAULT_INTENT_HOW_ARE_YOU_TPL = """
{
    "form": "how_are_you",
    "comment": "клиент спрашивает как дела?",
    "events": [
        {
            "event": "submit",
            "handler": "nlg",
            "phrase_id": "fine_thanks"
        }
    ]
}
"""

DEFAULT_INTENT_THANKS_TPL = """
{
    "form": "thanks",
    "comment": "клиент благодарит",
    "events": [
        {
            "event": "submit",
            "handler": "nlg",
            "phrase_id": "you_are_wellcome"
        }
    ]
}

"""

DEFAULT_NLG_DONT_UNDERSTAND_TPL = """
[i_dont_undestand_you]
я тебя не понимаю
повтори пожалуйста
Что ты имеешь ввиду?
Прости, не понимаю
я тебя не понимаю, ты сказал 'aaa'(utterance)
"""

DEFAULT_NLG_GOODBYE_TPL = """
[goodbye]
пока
удачи!
всего доброго!
"""

DEFAULT_NLG_GREETING_TPL = """
[greeting]
привет
приветик
здарова
"""

DEFAULT_NLG_HOW_ARE_YOU_TPL = """
[fine_thanks]
спасибо всё хорошо
у меня всё прекрасно
замечательно
"""

DEFAULT_NLG_THANKS_TPL = """
[you_are_wellcome]
всегда пожалуйста
всегда рада помочь
не стоит благодаростей
не, не надо. не люблю похвалу
это моя работа. служить тебе
"""

DEFAULT_NLU_GOODBYE_TPL = """
# - классификация -

пока
покеда
покедова
спасибо пока
"""

DEFAULT_NLU_GREETING_TPL = """
# - классификация -

привет
приветик
здорова
хай
"""

DEFAULT_NLU_HOW_ARE_YOU_TPL = """
# - классификация -

как дела
как делишки
"""

DEFAULT_NLU_THANKS_TPL = """
# - классификация -

спасиб
спасибо
благодарю
ты лучший
ты лучшая
"""

NEW_INTENT_TPL = """
{
  "form": "%(intent)s",
  "events": [],
  "slots": []
}
"""

NEW_INTENT_NLU_TPL = """
# закажи мне такси
# мне нужна тачка
# отвезите меня
#
# закажи мне такси на '8 утра'(when)
# мне нужна машина на 'улицу маршала неделина дом 6'(location_from) на 7 утра(when)
"""

NEW_INTENT_NLG_TPL = """
# [order_taxi_finished_successfully]
# заказ сформирован
# заказ создан. спасибо что воспользовались сервисом такси!
#
# [get_taxi_status]
# к вам едет 'жёлтый'(color) 'citroen'(brand) гос. номер 'a345mp197'(number)
# ожидайте машину 'жёлтый'(color) 'citroen'(brand) гос. номер 'a345mp197'(number)
"""

