from .reqrep_client import ReqRepClient
from .sub_client import SubClient


class GpioCoreClientError(Exception):

    def __init__(self, message, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(message)


class GpioCoreRpcClient(ReqRepClient):

    def __init__(self, port=5555):
        super().__init__(server_addr='tcp://127.0.0.1:{0}'.format(port))
        self._last_id = None

    def _next_payload_id(self):
        if self._last_id is None:
            self._last_id = 0
        else:
            self._last_id += 1
        return self._last_id

    def request(self, method, params):
        payload = {
            'id': self._next_payload_id(),
            'method': method,
            'params': params,
            'jsonrpc': '2.0'
        }
        resp = super().request(obj=payload)
        try:
            return resp['result']
        except KeyError:
            resp['error'].pop('message')
            raise GpioCoreClientError(resp['error']['data']['message'], **resp['error'])

    def add_input(self, pin, pull_up=False, bounce_time=None):
        return self.request(method='add_input', params=[pin, pull_up, bounce_time])

    def add_output(self, pin):
        return self.request(method='add_output', params=[pin])

    def pin_read(self, pin):
        return self.request(method='pin_read', params=[pin])

    def pin_on(self, pin):
        return self.request(method='pin_on', params=[pin])

    def pin_off(self, pin):
        return self.request(method='pin_off', params=[pin])

    def enable_pub_when_activated(self, pin):
        return self.request(method='enable_pub_when_activated', params=[pin])

    def disable_pub_when_activated(self, pin):
        return self.request(method='disable_pub_when_activated', params=[pin])

    def enable_pub_when_deactivated(self, pin):
        return self.request(method='enable_pub_when_deactivated', params=[pin])

    def disable_pub_when_deactivated(self, pin):
        return self.request(method='disable_pub_when_deactivated', params=[pin])


class GpioCoreSubClient(SubClient):

    def __init__(self, port=5556):
        super().__init__(server_addr='tcp://127.0.0.1:{0}'.format(port))
