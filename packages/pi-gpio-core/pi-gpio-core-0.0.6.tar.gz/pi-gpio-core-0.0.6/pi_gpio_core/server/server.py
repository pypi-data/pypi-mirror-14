import gpiozero
from jsonrpc import JSONRPCResponseManager
from jsonrpc.dispatcher import Dispatcher
import zmq
from pi_gpio_core.gpio import GpioZeroManager


gpio_manager = GpioZeroManager(gpio_lib=gpiozero)
gpio_dispatcher = Dispatcher()
gpio_dispatcher.add_method(gpio_manager.add_input)
gpio_dispatcher.add_method(gpio_manager.add_output)
gpio_dispatcher.add_method(gpio_manager.pin_read)
gpio_dispatcher.add_method(gpio_manager.pin_on)
gpio_dispatcher.add_method(gpio_manager.pin_off)


class GpioCore:

    def __init__(self, port):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind('tcp://127.0.0.1:{0}'.format(self.port))

    def run(self):
        try:
            while True:
                message = self.socket.recv_string()
                response = JSONRPCResponseManager.handle(message, gpio_dispatcher)
                self.socket.send_string(response.json)
        finally:
            gpio_manager.clean_up()
