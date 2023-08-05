from iai import Controller, Axis, utilities
import unittest
from mock import MagicMock


class Testutilities(unittest.TestCase):
    def test_calculate_check_sum(self):
        check_sum = utilities.calculate_check_sum("#99234")
        self.assertEqual(check_sum, 0x2e)
        self.assertEqual(utilities.calculate_check_sum("!99PSE   5 30.30 100  100.000  200.000"), 0xf4)

    def test_byte_to_upper_hex(self):
        self.assertEqual(utilities.int_to_upper_hex(0xab), "AB")
        self.assertEqual(utilities.int_to_upper_hex(0x01), "01")
        self.assertEqual(utilities.int_to_upper_hex(0xA0), "A0")
        self.assertEqual(utilities.int_to_upper_hex(0xA0, 4), "00A0")
        self.assertEqual(utilities.int_to_upper_hex(0xABA), "0ABA")
        self.assertEqual(utilities.int_to_upper_hex(0xABA, 2), "BA")

    def test_worker(self):
        import time
        worker = utilities.SimpleAsyncWorker()
        test_job = MagicMock()
        test_job.return_value = "return"
        test_callback = MagicMock()
        worker.add_job(test_job, test_callback, "start")
        worker.add_job(time.sleep, None, 1)
        worker.add_job(test_job, None, "end")
        worker.join()
        test_job[0].assert_called_wite("start")
        test_job[1].assert_called_wite("end")
        test_callback.assert_called_once_with("return")


