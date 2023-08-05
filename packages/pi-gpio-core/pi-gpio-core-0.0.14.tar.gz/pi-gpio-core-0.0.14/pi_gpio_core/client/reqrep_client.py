import json
import zmq
from .zmq_client import ZmqClient, ZmqClientError


class ReqRepClient(ZmqClient):

    def __init__(self, server_addr, max_retries=3, timeout=3000):
        context = zmq.Context()
        super().__init__(context=context, server_addr=server_addr)
        self.max_retries = max_retries
        self.remaining_retries = self.max_retries
        self.timeout = timeout
        self._connect()

    def _connect(self):
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(self._server_addr)
        self._poll = zmq.Poller()
        self._poll.register(self._socket, zmq.POLLIN)

    def _disconnect(self):
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.close()
        self._poll.unregister(self._socket)

    def request(self, obj):
        while self.remaining_retries:
            json_data = json.dumps(obj=obj)
            self._socket.send_string(json_data)
            expect_reply = True
            while expect_reply:
                socks = dict(self._poll.poll(self.timeout))
                if socks.get(self._socket) == zmq.POLLIN:
                    response = self._socket.recv_string()
                    if not response:
                        break
                    else:
                        self.remaining_retries = self.max_retries
                        expect_reply = False
                        return json.loads(response)
                else:
                    self._disconnect()
                    self.remaining_retries -= 1
                    if self.remaining_retries == 0:
                        # server is not online so stop trying
                        break
                    self._connect()
                    self._socket.send_string(json_data)
        else:
            self._context.term()
            raise ZmqClientError('Max reconnect attempts exceeded')
