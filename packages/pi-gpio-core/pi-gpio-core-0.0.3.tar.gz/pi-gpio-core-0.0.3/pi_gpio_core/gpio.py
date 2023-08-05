from .exceptions import PinError


class GpioZeroManager:

    def __init__(self, gpio_lib):
        self.gpio_lib = gpio_lib
        self.pins = {}

    def _lookup_pin(self, pin):
        try:
            return self.pins[pin]
        except KeyError:
            raise PinError('Pin not active')

    def add_input(self, pin, pull_up=False, bounce_time=None):
        self.pins[pin] = self.gpio_lib.DigitalInputDevice(pin, pull_up=pull_up, bounce_time=bounce_time)

    def add_output(self, pin, active_high=True, initial_value=False):
        self.pins[pin] = self.gpio_lib.DigitalOutputDevice(pin, active_high=active_high, initial_value=initial_value)

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

    def clean_up(self):
        for _, pin in self.pins.items():
            pin.close()
