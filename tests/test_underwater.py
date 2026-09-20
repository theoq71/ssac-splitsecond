"""Tests for the underwater module. Owner: (put your name here)

The contract tests come from tests/helpers.py and must keep passing.
Add your own tests below for the real metrics as you build them.
"""

import unittest

from tests.helpers import ModuleContractTest, moving_dot_clip
from splitsecond.modules.underwater import UnderwaterModule


class UnderwaterModuleContractTest(ModuleContractTest, unittest.TestCase):
    module_class = UnderwaterModule


class UnderwaterModuleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = UnderwaterModule()

    def test_placeholder_runs(self) -> None:
        # Replace this with real checks once the module measures something.
        result = self.module.run(moving_dot_clip(), {})
        self.assertEqual(result.module, "underwater")


if __name__ == "__main__":
    unittest.main()
