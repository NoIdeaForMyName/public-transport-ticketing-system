import abc


class BaseView(abc.ABC):
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def handle_input(self, action):
        pass
