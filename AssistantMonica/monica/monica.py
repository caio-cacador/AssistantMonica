import random

from google import google

from AssistantMonica.monica import interpreters
from AssistantMonica.services.arduino import Arduino
from AssistantMonica.services.camera import Camera
from AssistantMonica.monica.constants import LINK_FILTER, NORMAL_GREETING, INFORMAL_GREETING, GREETING_WITH_QUESTION, \
    COMPLIMENT_RESPONSE, LOCK_DOOR, OPEN_DOOR, GET_BEDROOM_IMAGE, PERMISSION_DENIED_TO_EXECUTE_COMMAND, \
    GET_CORREIO_TRACKING
from AssistantMonica.services.correio import Correio

from AssistantMonica.services.telegram import Telegram, MessageNamedTuple
from AssistantMonica.utils.utils import request, get_answer_clean, normalize_str


class Monica:

    def __init__(self, telegram: Telegram, arduino: Arduino, camera: Camera):
        self.camera = camera
        self.telegram = telegram
        self.arduino = arduino
        self.correioService = Correio()

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

    def check_admin_permission(self, user_id):
        if not self.telegram.have_admin_permission(user_id):
            self.telegram.send_message(PERMISSION_DENIED_TO_EXECUTE_COMMAND)

    def check_master_permission(self, user_id):
        if not (self.telegram.have_admin_permission(user_id) or self.telegram.have_master_permission(user_id)):
            self.telegram.send_message(PERMISSION_DENIED_TO_EXECUTE_COMMAND)

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

        else:
            self.execute_command(message)

    def _check_permission(self, user_id: str, check_admin: bool = False, check_master: bool = False):
        if check_admin:
            if not self.telegram.have_admin_permission(user_id):
                self.telegram.send_message(PERMISSION_DENIED_TO_EXECUTE_COMMAND)
                return False
        elif check_master:
            if not (self.telegram.have_admin_permission(user_id) or self.telegram.have_master_permission(user_id)):
                self.telegram.send_message(PERMISSION_DENIED_TO_EXECUTE_COMMAND)
                return False
        return True

    def execute_command(self, message: MessageNamedTuple):
        command = normalize_str(message.text)

        if command in OPEN_DOOR:
            if not self._check_permission(check_admin=True, user_id=message.user_id):
                self.arduino.unlock_door()

        elif command in LOCK_DOOR:
            if self._check_permission(check_admin=True, user_id=message.user_id):
                self.arduino.lock_door()

        elif command in GET_BEDROOM_IMAGE:
            if self._check_permission(check_admin=True, user_id=message.user_id):
                self.telegram.send_photo(image=self.camera.get_current_frame())

        elif any([item in command for item in GET_CORREIO_TRACKING]):
            tracking_code = message.text.split(':')[1].strip()
            res = self.correioService.get_last_tracking_info(tracking_code=tracking_code)
            self.telegram.send_message(text=res)
