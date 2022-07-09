import copy
from typing import Callable

is_debug_mode = True


class Observable:
    def __init__(self):
        self._data = None
        self._observers = {}
        self._cache = None

    def attach(self, observer_method: Callable):
        self._observers[observer_method] = 1

    def cache_data(self):
        self._cache = copy.deepcopy(self._data)

    @property
    def notification(self) -> dict:
        return {'notifier': self.__class__.__name__, 'data': copy.deepcopy(self._data), 'cache': self._cache}

    @property
    def cache(self):
        return self._cache

    def notify(self, method_name=''):
        if self._cache != self._data:
            for observer in self._observers:
                notification = self.notification
                notification.update({'method': method_name})
                observer(**notification)

    def reset(self):
        self._data = None
        self.notify()

    @property
    def data(self):
        return self._data

    def set_data(self, value):
        self._data = value


def notify(f: Callable):
    def wrapper(*args, **kwargs):
        if is_debug_mode:
            entity: Observable = args[0]
            entity.cache_data()  # Expensive!
            return_value = f(*args, **kwargs)
            entity.notify(f.__name__)
        else:
            return_value = f(*args, **kwargs)
        return return_value

    return wrapper
