import logging

class Events:
    def __init__(self):
        self.__events = {}
        self.__once = {}

    def on(self, event, listener):
        if not event in self.__events:
            self.__events[event] = []
        self.__events[event].append(listener)

    def emit(self, event, *arg, **keywords):
        if event in self.__events:
            for listener in self.__events[event]:
                listener(*arg, **keywords)
        elif event in self.__once:
            for listener in self.__once[event]:
                listener(*arg, **keywords)
            del self.__once[event]
        else:
            logging.getLogger().error('There is no event: %s', event)

    def once(self, event, listener):
        if not event in self.__events:
            self.__events[event] = []
        self.__evnets[event].append(listener)

    def off(self, event):
        if event in self.__events:
            del self.__events[event]
        elif event in self.__once:
            del self.__events[event]
        else:
            logging.getLogger().error('There is no event: %s', event)
