from pyfirmata import Arduino as PyfirmataArduino, util
from time import sleep


class Arduino:

    _UNLOCK_POSITION = 85
    _LOCK_POSITION = 180

    def __init__(self, configs: dict):
        self._arduino = PyfirmataArduino(configs['usb_port'])
        print('arduino is online!')
        it = util.Iterator(self._arduino)
        it.start()

        self._btn_door = self._arduino.get_pin('d:5:i')
        self._btn_door.enable_reporting()
        self._btn_outside = self._arduino.get_pin('d:4:i')
        self._btn_outside.enable_reporting()
        self._btn_inside = self._arduino.get_pin('d:6:i')
        self._btn_inside.enable_reporting()

        self._servo_motor = self._arduino.get_pin('d:9:s')
        self._servo_motor.write(self._UNLOCK_POSITION)
        self._servo_position = self._UNLOCK_POSITION
        self._servo_is_in_use = False

    def close_connection(self):
        self._arduino.exit()

    def get_btn_door_status(self) -> bool:
        return self._btn_door.read()

    def get_btn_outside_status(self) -> bool:
        return self._btn_outside.read()

    def get_btn_inside_status(self) -> bool:
        return self._btn_inside.read()

    def unlock_door(self):
        if self._servo_is_in_use is False:
            self._servo_is_in_use = True
            if self._servo_position > self._UNLOCK_POSITION:
                print('[-] Destrancando a porta')
                while self._servo_position > self._UNLOCK_POSITION:
                    self._servo_position -= 2
                    self._servo_motor.write(self._servo_position)
                    sleep(0.02)
                sleep(3)
            else:
                print('[-] A porta ja esta destrancada')
            self._servo_is_in_use = False

    def lock_door(self):
        if self._servo_is_in_use is False:
            self._servo_is_in_use = True
            if self._servo_position < self._LOCK_POSITION:
                print('[-] Trancando a porta')
                while self._servo_position < self._LOCK_POSITION:
                    self._servo_position += 2
                    self._servo_motor.write(self._servo_position)
                    sleep(0.02)
                sleep(1)
            else:
                print('[-] Porta ja esta trancada')
            self._servo_is_in_use = False
