from time import sleep
import ujson

from AssistantMonica.monica.monica import Monica
from AssistantMonica.services.arduino import Arduino
from AssistantMonica.services.camera import Camera
from AssistantMonica.services.telegram import Telegram
import traceback


def run():
    print(' - Loading configs')
    configs = ujson.load(open('configs.json', 'r'))
    arduino = Arduino(configs=configs['arduino_configs'])
    print(' - Arduino Online')
    telegram = Telegram(configs=configs['telegram_configs'])
    print(' - Telegram Online')
    camera = Camera(cam_configs=configs['cam_configs'])
    camera.start_update()
    print(' - Camera Online')
    monica = Monica(telegram=telegram, arduino=arduino, camera=camera)
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


if __name__ == "__main__":
    while True:
        try:
            run()
        except Exception as ex:
            traceback.print_exc()
            retry = 10
            print(f' --- Erro ao iniciar >> {ex}')
            print(f' --- Tentando novamente em {retry} segundoss.')
            sleep(retry)
