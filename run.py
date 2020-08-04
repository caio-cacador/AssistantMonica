from time import sleep

import ujson

from AssistantMonica.arduino import Arduino
from AssistantMonica.camera import Camera
from AssistantMonica.monica import Monica
from AssistantMonica.telegram import Telegram

if __name__ == "__main__":

    configs = ujson.load(open('configs.json', 'r'))
    telegram_configs = configs['telegram_configs']
    arduino = Arduino(configs=configs['arduino_configs'])
    telegram = Telegram(configs=telegram_configs)
    camera = Camera(cam_configs=configs['cam_configs'])
    monica = Monica(telegram=telegram, arduino=arduino, camera=camera)

    camera.start_update()

    print(' - Assistant Monica is Online.')
    telegram.send_message(text=' - Assistant Monica is Online.')

    while True:

        if telegram.last_message:
            monica.message_interpreter(telegram.last_message)

        if arduino.get_btn_door_status():

            if arduino.get_btn_inside_status():
                arduino.unlock_door()

            else:
                arduino.lock_door()

        telegram.last_message = None
        sleep(0.3)