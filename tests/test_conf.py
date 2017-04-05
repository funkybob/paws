import unittest

from paws.conf import Conf, env


class ConfTest(unittest.TestCase):

    def test_attr_name(self):
        class Config(Conf):
            FOO = env('FOO')

        self.assertEqual(Config.FOO.name, 'FOO')
