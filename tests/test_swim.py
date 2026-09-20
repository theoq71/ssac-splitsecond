"""Tests for the swim module. Owner: (put your name here)

The contract tests come from tests/helpers.py and must keep passing.
Add your own tests below for the real metrics as you build them.
"""

import unittest

from tests.helpers import ModuleContractTest, moving_dot_clip
from splitsecond.modules.swim import SwimModule


class SwimModuleContractTest(ModuleContractTest, unittest.TestCase):
    module_class = SwimModule


class SwimModuleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = SwimModule()

    def test_placeholder_runs(self) -> None:
        # Replace this with real checks once the module measures something.
        result = self.module.run(moving_dot_clip(), {})
        self.assertEqual(result.module, "swim")


if __name__ == "__main__":
    unittest.main()
