import unittest

from paws.conf import Config, env


class ConfTest(unittest.TestCase):

    def test_attr(self):
        class Config(Conf):
            FOO : int = 0

        self.assertEqual(Config.FOO, 0)
