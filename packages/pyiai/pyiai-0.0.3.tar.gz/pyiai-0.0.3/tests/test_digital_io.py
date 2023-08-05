from iai import Controller, DigitalIO
import unittest
from mock import MagicMock


class TestDigitalIO_out(unittest.TestCase):
    def setUp(self):
        self.controller = Controller.Controller()
        self.controller._serial = MagicMock()

    def test_set(self):
        self.controller._serial.readline.return_value = \
            b"#99OUT0200000000000000000000000000000000000000000000000000000000000000000000000F\r\n"
        self.out_io = DigitalIO.DigitalIO(self.controller, 587, "out")
        self.out_io.set(1)
        self.controller._serial.write.assert_called_with(b"!99OTS358059\r\n")

        self.out_io = DigitalIO.DigitalIO(self.controller, 301, "out")
        self.out_io.set(1)
        self.controller._serial.write.assert_called_with(b"!99OTS 0 22B\r\n")

        self.out_io = DigitalIO.DigitalIO(self.controller, 300, "out")
        self.out_io.set(1)
        self.controller._serial.write.assert_called_with(b"!99OTS 0 32C\r\n")

    def test_get(self):
        self.controller._serial.readline.return_value = \
            b"#99OUT0200000000000000000000000000000000000000000000000000000000000000000000000F\r\n"
        self.out_io = DigitalIO.DigitalIO(self.controller, 301, "out")
        self.assertEqual(self.out_io.get(), 1)

        self.out_io = DigitalIO.DigitalIO(self.controller, 300, "out")
        self.assertEqual(self.out_io.get(), 0)

    def test__get_byte(self):
        self.out_io = DigitalIO.DigitalIO(self.controller, 587, "out")
        self.controller._serial.readline.return_value = \
            b"#99OUT02000000000000000000000000000000000000000000000000000000000000000000008017\r\n"
        self.assertEqual(self.out_io._get_byte(), 0x80 )

        self.controller._serial.readline.return_value = \
            b"#99OUT02000000000000000000000000000000000000000000000000000000000000000000002011\r\n"
        self.assertEqual(self.out_io._get_byte(), 0x20 )

        self.out_io = DigitalIO.DigitalIO(self.controller, 0, "out")
        pass




