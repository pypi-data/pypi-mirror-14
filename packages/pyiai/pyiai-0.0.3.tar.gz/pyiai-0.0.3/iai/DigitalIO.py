from iai.Controller import Controller
from iai.utilities import *
import re


class DigitalIO(object):
    def __init__(self, controller, No, io_type="out"):
        """
        @type controller: Controller
        """
        if type(controller) is Controller:
            self._controller = controller
        if io_type == "out":
            No -= 300   # The out io No is large than 300
            self.No_in_byte = int(No / 8)
            self.mask_in_bits = 1 << (No % 8)
        elif io_type == "in":
            raise NotImplementedError
        else:
            raise NotImplementedError
        self.io_type = io_type

    def _get_byte(self):
        if self.io_type == "out":
            command = "?[station]OUT"
            self.send_command(command)
            temp = self.receive_command()
            temp = re.findall("OUT(.*)\r\n", temp)[0]
            temp = list(zip(temp[0::2], temp[1::2]))
            temp = temp[self.No_in_byte]
            temp = temp[0] + temp[1]
            return int(temp, 16)
        else:
            pass

    def get(self):
        if self._get_byte() & self.mask_in_bits > 0:
            return 1
        return 0

    def set(self, data):
        assert(data == 1 or data == 0)
        if self.io_type == "out":
            current_state = self._get_byte()
            command = "![station]OTS"
            command += ("% 2i" % self.No_in_byte)[-2:]
            if data == 1:
                current_state = current_state | self.mask_in_bits
                command += ("% 2x" % current_state)[-2:]
            else:
                current_state = current_state & ~self.mask_in_bits
                command += ("% 2x" % current_state)[-2:]
        else:
            raise NotImplementedError
        self.send_command(command)
        self.receive_command()
        # debug_print(self.receive_command())

    def send_command(self, command):
        self._controller.send_command(command)

    def receive_command(self):
        return self._controller.receive_command()


