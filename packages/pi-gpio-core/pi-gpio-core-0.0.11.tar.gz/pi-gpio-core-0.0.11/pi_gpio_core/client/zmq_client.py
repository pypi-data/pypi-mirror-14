import abc
from abc import ABCMeta


class ZmqClientError(Exception):
    pass


class ZmqClient(metaclass=ABCMeta):

    def __init__(self, context, server_addr):
        self._server_addr = server_addr
        self._context = context

    @abc.abstractmethod
    def _connect(self):
        pass

    @abc.abstractmethod
    def _disconnect(self):
        pass
