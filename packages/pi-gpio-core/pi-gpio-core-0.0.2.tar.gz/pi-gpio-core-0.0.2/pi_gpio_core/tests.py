import unittest
import gpiozero
from .gpio import GpioZeroManager


class GpioTestCase(unittest.TestCase):

    def setUp(self):
        super(GpioTestCase, self).setUp()
        self.gpio_manager = GpioZeroManager(gpio_lib=gpiozero)

    def test_add_input(self):
        self.gpio_manager.add_input(pin=10)
        self.assertIsInstance(self.gpio_manager.pins[10], gpiozero.DigitalInputDevice)
