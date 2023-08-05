from jsonrpc import JSONRPCResponseManager
from jsonrpc.dispatcher import Dispatcher
import zmq
from pi_gpio_core.gpio import GpioZeroManager


class GpioCoreServer:

    def __init__(self, rpc_socket, gpio_manager):
        self.rpc_socket = rpc_socket
        self.gpio_manager = gpio_manager
        self.dispatcher = Dispatcher()
        self.dispatcher.add_method(self.gpio_manager.add_input)
        self.dispatcher.add_method(self.gpio_manager.add_output)
        self.dispatcher.add_method(self.gpio_manager.pin_read)
        self.dispatcher.add_method(self.gpio_manager.pin_on)
        self.dispatcher.add_method(self.gpio_manager.pin_off)
        self.dispatcher.add_method(self.gpio_manager.enable_pub_when_activated)
        self.dispatcher.add_method(self.gpio_manager.disable_pub_when_activated)
        self.dispatcher.add_method(self.gpio_manager.enable_pub_when_deactivated)
        self.dispatcher.add_method(self.gpio_manager.disable_pub_when_deactivated)

    def run(self):
        try:
            while True:
                message = self.rpc_socket.recv_string()
                response = JSONRPCResponseManager.handle(message, self.dispatcher)
                self.rpc_socket.send_string(response.json)
        finally:
            self.gpio_manager.clean_up()


def gpio_core_server(rpc_port=5555, pub_port=5556):
    context = zmq.Context()
    rpc_socket = context.socket(zmq.REP)
    rpc_socket.bind('tcp://127.0.0.1:{0}'.format(rpc_port))
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind('tcp://127.0.0.1:{0}'.format(pub_port))
    gpio_manager = GpioZeroManager(pub_socket=pub_socket)
    return GpioCoreServer(rpc_socket=rpc_socket, gpio_manager=gpio_manager)
