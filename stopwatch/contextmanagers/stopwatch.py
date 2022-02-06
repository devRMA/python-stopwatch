import sys
from typing import Any, Optional

from termcolor import colored

from ..stopwatch import Stopwatch
from . import Caller, format_elapsed_time, inspect_caller


# pylint: disable=invalid-name
class stopwatch:
    _message: Optional[str]
    _caller: Caller
    _stopwatch: Stopwatch

    def __init__(self, message: Optional[str] = None) -> None:
        self._message = message
        self._caller = inspect_caller()
        self._stopwatch = Stopwatch()

    def __enter__(self) -> None:
        self._stopwatch.start()

    def __exit__(self, exc_type: Any, exc_value: Any,
                 exc_traceback: Any) -> None:
        self._stopwatch.stop()
        print(self._format(self._message, self._caller,
                           self._stopwatch.elapsed),
              file=sys.stderr)

    @staticmethod
    def _format(message: Optional[str], caller: Caller, elapsed: float) -> str:
        items = [
            colored(
                f'[{caller.module}:{caller.function}:{caller.line_number}]',
                color='blue',
                attrs=['bold']), ' ~ ',
            colored(format_elapsed_time(elapsed),
                    color='magenta',
                    attrs=['bold'])
        ]

        if message is not None:
            items += [' - ', message]

        return ''.join(items)
