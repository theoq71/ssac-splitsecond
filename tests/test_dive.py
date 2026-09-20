"""Tests for the dive module. Owner: (put your name here)

The contract tests come from tests/helpers.py and must keep passing.
Add your own tests below for the real metrics as you build them.
"""

import unittest

from tests.helpers import ModuleContractTest, moving_dot_clip
from splitsecond.modules.dive import DiveModule


class DiveModuleContractTest(ModuleContractTest, unittest.TestCase):
    module_class = DiveModule


class DiveModuleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = DiveModule()

    def test_placeholder_runs(self) -> None:
        # Replace this with real checks once the module measures something.
        result = self.module.run(moving_dot_clip(), {})
        self.assertEqual(result.module, "dive")


if __name__ == "__main__":
    unittest.main()
