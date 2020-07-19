import ujson

from AssistantMonica.arduino import Arduino
from AssistantMonica.monica import Monica
from AssistantMonica.telegram import Telegram

if __name__ == "__main__":

    configs = ujson.load(open('configs.json', 'r'))
    telegram_configs = configs['telegram_configs']
    # arduino = Arduino(configs=configs['arduino_configs'])
    telegram = Telegram(configs=telegram_configs)
    monica = Monica(telegram=telegram)

    print(' - Assistant Monica is Online.')
    telegram.send_message(text=' - Assistant Monica is Online.')

    while True:

        if telegram.last_message:
            monica.message_interpreter(telegram.last_message)
            # elif telegram.last_message.user_id in telegram_configs.get('authorized_users', []):

        telegram.last_message = None
