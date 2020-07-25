import random

from google import google

from AssistantMonica import interpreters
from AssistantMonica.constants import LINK_FILTER, NORMAL_GREETING, INFORMAL_GREETING, GREETING_WITH_QUESTION, COMPLIMENT_RESPONSE

from AssistantMonica.telegram import Telegram, MessageNamedTuple
from AssistantMonica.utils import request, get_answer_clean


class Monica:

    def __init__(self, telegram: Telegram):
        self.telegram = telegram

    def message_interpreter(self, message: MessageNamedTuple):

        if message.user_name == 'Adriano':
            self.telegram.send_message('Desculpe Adriano, não posso conversar com nóias por enquanto.', message.chat_id)

        if interpreters.is_what_is_question(message.text):
            self.telegram.send_message('Deixe me ver...', message.chat_id)
            self.telegram.send_message(self._what_is(message.text), message.chat_id)

        elif interpreters.is_who_is_question(message.text):
            self.telegram.send_message('Deixe me ver...', message.chat_id)
            self.telegram.send_message(self._who_is(message.text), message.chat_id)

        elif interpreters.is_it_a_conversation(message.text):
            response = self._talk(message.text)
            self.telegram.send_message(response, message.chat_id)

        elif interpreters.is_it_a_compliment(message.text):
            self.telegram.send_message(random.choice(COMPLIMENT_RESPONSE), message.chat_id)

    def _what_is(self, question):
        theme = interpreters.what_is_interpreter(question)
        try:
            search = 'o que é ' + theme
            print('[+] Searching: ', search)
            links = (res.link if res.link not in LINK_FILTER else '' for res in google.search(search))
            for link in links:
                content = request(url=link)
                if content:
                    clear_answer = get_answer_clean(theme=theme, content=content)
                    if clear_answer:
                        return clear_answer

            return "Por favor, tente especificar a sua pergunta..."

        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print('Error >>>', ex)

    def _who_is(self, question):
        theme = interpreters.who_is_interpreter(question)
        try:
            search = 'quem é ' + theme
            print('[+] Searching: ', search)
            links = (res.link if res.link not in LINK_FILTER else '' for res in google.search(search))
            for link in links:
                content = request(url=link)
                if content:
                    clear_answer = get_answer_clean(theme=theme, content=content)
                    if clear_answer:
                        return clear_answer

            return "Por favor, tente especificar a sua pergunta..."

        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print('Error >>>', ex)

    @staticmethod
    def _talk(phrase):
        for gretting in NORMAL_GREETING:
            if gretting in phrase:
                return random.choice(NORMAL_GREETING).capitalize()
        for gretting in INFORMAL_GREETING:
            if gretting in phrase:
                return random.choice(INFORMAL_GREETING).capitalize()
        for gretting in GREETING_WITH_QUESTION:
            if gretting in phrase:
                return 'Estou bem, e você, ' + random.choice(GREETING_WITH_QUESTION) + '?'
