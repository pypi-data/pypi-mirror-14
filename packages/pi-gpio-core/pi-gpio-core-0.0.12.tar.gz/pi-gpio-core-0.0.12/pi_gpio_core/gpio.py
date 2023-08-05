import gpiozero
from .exceptions import PinError


class GpioZeroManager:

    def __init__(self, pub_socket):
        self.pub_socket = pub_socket
        self.pins = {}

    def _lookup_pin(self, pin):
        try:
            return self.pins[pin]
        except KeyError:
            raise PinError('Pin not active')

    def _pin_pub_callback(self, event):
        def callback(device):
            message = {
                'pin': device.pin.number,
                'event': event
            }
            self.pub_socket.send_json(obj=message)
        return callback

    def add_input(self, pin, pull_up=False, bounce_time=None):
        self.pins[pin] = gpiozero.DigitalInputDevice(pin, pull_up=pull_up, bounce_time=bounce_time)

    def add_output(self, pin, active_high=True, initial_value=False):
        self.pins[pin] = gpiozero.DigitalOutputDevice(pin, active_high=active_high, initial_value=initial_value)

    def pin_read(self, pin):
        pin = self._lookup_pin(pin=pin)
        return pin.value

    def pin_on(self, pin):
        pin = self._lookup_pin(pin=pin)
        pin.on()
        return pin.value

    def pin_off(self, pin):
        pin = self._lookup_pin(pin=pin)
        pin.off()
        return pin.value

    def enable_pub_when_activated(self, pin):
        pin = self._lookup_pin(pin=pin)
        pin.when_activated = self._pin_pub_callback(event='activated')

    def enable_pub_when_deactivated(self, pin):
        pin = self._lookup_pin(pin=pin)
        pin.when_deactivated = self._pin_pub_callback(event='deactivated')

    def disable_pub_when_activated(self, pin):
        pin = self._lookup_pin(pin=pin)
        pin.when_activated = None

    def disable_pub_when_deactivated(self, pin):
        pin = self._lookup_pin(pin=pin)
        pin.when_deactivated = None

    def clean_up(self):
        for _, pin in self.pins.items():
            pin.close()
