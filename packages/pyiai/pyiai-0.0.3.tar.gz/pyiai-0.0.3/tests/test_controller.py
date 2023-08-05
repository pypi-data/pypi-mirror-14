import unittest
from iai import Controller
from mock import MagicMock

class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller.Controller()
        self.controller._serial = MagicMock()

    def test_init_command(self):
        self.controller._serial.ReadLine.return_value = b"#99212010C000000000049B2@@\r\n"
        self.controller.send_init_command()
        self.controller._serial.write.assert_called_with(b"?99VERM01B\r\n")

class TestCONController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller.CONController()
        self.controller._serial = MagicMock()

    def test_send_command(self):
        self.controller.send_command("00039000000A")
        self.controller._serial.write.assert_called_with(b":00039000000A63\r\n")

