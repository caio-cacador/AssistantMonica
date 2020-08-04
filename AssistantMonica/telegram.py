from collections import namedtuple

from telepot import Bot, exception
from telepot.loop import MessageLoop
from AssistantMonica import utils
from AssistantMonica.camera import Buffer

MessageNamedTuple = namedtuple('message', ['chat_id', 'text', 'user_name', 'user_id'])


class Telegram:

    def __init__(self, configs: dict):
        self.bot = Bot(configs['token'])
        self._default_chat_id = configs['default_chat_id']
        self._bot_name = configs['bot_name']
        self._admin_users = configs['authorized_users']['admin']
        self._master_users = configs['authorized_users']['master']

        self.last_message = None
        MessageLoop(self.bot, self._handle).run_as_thread()

    @staticmethod
    def _compare_messages(text1: str, text2: str) -> bool:
        return utils.normalize_str(text1.lower()) == utils.normalize_str(text2.lower())

    def _handle(self, msg):
        if msg:
            chat_id = msg['chat']['id']
            first_name = msg['from']['first_name']
            message = str(msg.get('text', ''))
            first_world = message[:len(self._bot_name)] if len(message) > len(self._bot_name) else ''

            print(f"[-] ({chat_id}: ') >> {first_name} sent: {message}")

            if self._compare_messages(first_world, self._bot_name):
                message = message[len(self._bot_name)+1:]
                print(f'message to monica >> {message}')
                self.last_message = MessageNamedTuple(chat_id, message.strip(), first_name, msg['from'].get('id', ''))

    def send_photo(self, image, name: str = 'photo.png', _type: str = '.PNG', chat_id: int = None):
        if not chat_id:
            chat_id = self._default_chat_id
        self.bot.sendPhoto(chat_id, (name, Buffer(_type=_type, image=image)))

    def send_message(self, text: str = '', chat_id: int = None):
        if not chat_id:
            chat_id = self._default_chat_id
        try:
            self.bot.sendMessage(chat_id, text)
        except exception.TelegramError:
            print(f'[-] Chat not found: {chat_id}')

    def send_bool_question(self, question: str, chat_id: int = None):
        attempts = 3
        self.last_message = None
        self.send_message(text=question, chat_id=chat_id)
        while attempts > 0:
            if self.last_message:
                attempts -= 1
                response = utils.normalize_str(self.last_message.lower)
                if response in ['sim', 'pode']:
                    return True
                elif response in ['nao', 'nao pode']:
                    return False
                else:
                    self.send_message(text="Por favor, responda com 'sim' ou 'nao'.", chat_id=chat_id)
                    self.last_message = None
        return False

    def have_admin_permission(self, user):
        if user in self._admin_users:
            return True
        return False

    def have_master_permission(self, user):
        if user in self._master_users:
            return True
        return False
