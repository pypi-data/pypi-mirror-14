import unittest
from ubersmith_client.exceptions import UbersmithException


class ExceptionTestTest(unittest.TestCase):

    def test_UbersmithException_has_string_representation(self):
        ex = UbersmithException(code=42, message='Wubba Lubba Dub Dub')
        self.assertEquals("{0}".format(ex), "Error code 42 - message: Wubba Lubba Dub Dub")
