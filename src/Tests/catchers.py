class NotificationCatcher:
    def __init__(self):
        self._notifications = []
        self._n = 0

    def observer(self, *args, **kwargs):
        self._notifications.append((args, kwargs))
        self._n += 1

    @property
    def counter(self) -> int:
        return self._n

    @property
    def notifications(self):
        return self._notifications

    @property
    def args(self) -> list:
        return [a for (a, kw) in self._notifications]

    @property
    def kwargs(self) -> list:
        return [kw for (a, kw) in self._notifications]

    def get_kwargs(self, option: str, value) -> list:
        return [kw for (a, kw) in self._notifications if kw[option] == value]


class ResponseModelCatcher:
    def __init__(self):
        self._response_models_caught = []

    def presenter_method(self, response_model):
        self._response_models_caught.append(response_model)

    @property
    def response_models_caught(self) -> list:
        return self._response_models_caught


class ViewResponseModelCatcher:
    def __init__(self):
        self._view_model_passed = []

    def view_method(self, view_model):
        self._view_model_passed.append(view_model)

    @property
    def view_model_passed(self) -> list:
        return self._view_model_passed
