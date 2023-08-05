# This file is here more for the sake of total coverage than for actual testing. Many of the methods in the
# environment module can't be effectively tested, because they are machine-specific and change every time the machine
# does. This means the tests can't easily be written to assert equalities, because those equalities change each time.
# Most of these tests simply run the method once to check that it doesn't throw any exceptions.

import unittest
from utilinaut import environment

class TestUntestableEnvironmentMethods(unittest.TestCase):
    def test_os_name_no_exc(self):
        environment.os_name()

    def test_machine_name_no_exc(self):
        environment.machine_name()

    def test_get_username_no_exc(self):
        environment.get_username()
