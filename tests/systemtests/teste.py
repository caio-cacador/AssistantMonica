from abc import ABC, abstractmethod
from datetime import datetime
from time import sleep

reminder_types = {
    1: 'remider',
    2: 'despertador',
    3: 'correio',
}


class AbstracReminder(ABC):

    def __init__(self, type_):
        self.type_ = type_


class Remminder(AbstracReminder):

    def __init__(self):
        super().__init__(type_=1)
a
    def __hash__(self):
        return hash(self.type_)

    def __eq__(self, other):
        if isinstance(other, Remminder):
            return self.type_ == other.type_
        return NotImplemented


class Despertador(AbstracReminder):

    def __init__(self):
        super().__init__(type_=2)

    def __hash__(self):
        return hash(self.type_)

    def __eq__(self, other):
        if isinstance(other, Despertador):
            return self.type_ == other.type_
        return NotImplemented


class Correio(AbstracReminder):

    def __init__(self):
        super().__init__(type_=3)

    def __hash__(self):
        return hash(self.type_)

    def __eq__(self, other):
        if isinstance(other, Correio):
            return self.type_ == other.type_
        return NotImplemented


lembretes = [
    Remminder(),
    Despertador(),
    Correio()
]

while True:
    for item in lembretes:
        if isinstance(item, Remminder):
            print('Reminder')
        elif isinstance(item, Despertador):
            print('Despertador')
        elif isinstance(item, Correio):
            print('Correio')

        lembretes.remove(item)
        sleep(300)
