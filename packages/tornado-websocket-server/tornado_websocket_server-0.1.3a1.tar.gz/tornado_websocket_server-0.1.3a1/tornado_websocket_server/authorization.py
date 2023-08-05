import abc


class AbstractAuthorization:

    @abc.abstractmethod
    def authorize(self, handler):
        raise NotImplementedError()


class Dumb(AbstractAuthorization):
    def authorize(self, handler):
        return True
