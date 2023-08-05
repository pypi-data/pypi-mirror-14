from iai import Controller, Axis, Space
import unittest
from mock import MagicMock


class TestSpace(unittest.TestCase):
    def setUp(self):
        self.axis1 = MagicMock()
        self.axis2 = MagicMock()
        self.space = Space.Space([self.axis1, self.axis2])

    def test_helper(self):
        pass

    def test_go_home(self):
        self.space.go_home()
        self.axis1.go_home.assert_called_once_with()
        self.axis2.go_home.assert_called_once_with()

    def test_wait(self):
        self.space.wait()
        self.axis1.wait_for_axis_is_using.assert_called_once_with()
        self.axis2.wait_for_axis_is_using.assert_called_once_with()

    def test_move(self):
        self.space.move([100, 200])
        self.axis1.move_absolute.assert_called_once_with(100, 0.3, 0.3, 100)
        self.axis2.move_absolute.assert_called_once_with(200, 0.3, 0.3, 100)



