import unittest
from utilinaut import commandline

class TestGetArgument(unittest.TestCase):
    args = ['-s', 's_value', '--long=l_value']

    def test_shortswitch_correct_return(self):
        arg_value = commandline.get_argument(self.args, '-s')
        self.assertEqual(arg_value, 's_value')

    def test_longswitch_correct_return(self):
        arg_value = commandline.get_argument(self.args, '--long')
        self.assertEqual(arg_value, 'l_value')

    def test_shortswitch_returns_none(self):
        arg_value = commandline.get_argument(self.args, '-n')
        self.assertEqual(arg_value, None)

    def test_longswitch_returns_none(self):
        arg_value = commandline.get_argument(self.args, '--not-there')
        self.assertEqual(arg_value, None)

    def test_shortswitch_raises_exc(self):
        self.assertRaises(AttributeError, commandline.get_argument, self.args, '-n', True)

    def test_longswitch_raises_exc(self):
        self.assertRaises(AttributeError, commandline.get_argument, self.args, '--not-there', True)
