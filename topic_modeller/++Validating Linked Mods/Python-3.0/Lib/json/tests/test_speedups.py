import decimal
from unittest import TestCase

from json import decoder
from json import encoder

class TestSpeedups(TestCase):
    def test_scanstring(self):
        self.assertEqual(decoder.scanstring.__module__, "_json")
        self.assertTrue(decoder.scanstring is decoder.c_scanstring)

    def test_encode_basestring_ascii(self):
        self.assertEqual(encoder.encode_basestring_ascii.__module__, "_json")
        self.assertTrue(encoder.encode_basestring_ascii is
                          encoder.c_encode_basestring_ascii)
