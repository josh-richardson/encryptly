from abc import ABCMeta, abstractmethod


class BaseIntent(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    def validate(self, intent):
        return intent == self.name

    @abstractmethod
    def execute(self, message, message_data):
        pass
