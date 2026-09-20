"""Registry of analysis modules.

Adding a module: create a folder here (copy an existing one), then add one
line to MODULES below. Everything else (CLI, tests, future web page) finds
it through this dict.
"""

from splitsecond.modules.base import AnalysisModule
from splitsecond.modules.dive import DiveModule
from splitsecond.modules.swim import SwimModule
from splitsecond.modules.turn import TurnModule
from splitsecond.modules.underwater import UnderwaterModule

MODULES: dict[str, type[AnalysisModule]] = {
    DiveModule.name: DiveModule,
    UnderwaterModule.name: UnderwaterModule,
    SwimModule.name: SwimModule,
    TurnModule.name: TurnModule,
}


def get_module(name: str) -> AnalysisModule:
    try:
        return MODULES[name]()
    except KeyError:
        raise KeyError(f"no module called '{name}'; choose from {', '.join(MODULES)}") from None


def module_names() -> list[str]:
    return list(MODULES)
