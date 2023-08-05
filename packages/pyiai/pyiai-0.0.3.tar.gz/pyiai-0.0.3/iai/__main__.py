from time import sleep
from iai.Controller import XSELController, RCPController, CONController
from iai.Axis import SSELAxis, XSELAxis, RCPAxis, CONAxis
from iai.Space import Space
from iai.DigitalIO import DigitalIO
from iai.utilities import *
import serial
def self_test():
    controller = CONController("COM19", 38400, 3)
    axis1 = CONAxis(controller, 1)
    axis1.reset_error()
    axis1.servo = True
    axis1.go_home()
    axis1.wait_while_axis_is_using()
    for i in range(5):
        axis1.move_absolute(20, 150, 0.3)
        axis1.wait_while_axis_is_using()
        axis1.move_absolute(40, 150, 0.3)
        axis1.wait_while_axis_is_using()

if __name__ == "__main__":
    self_test()

