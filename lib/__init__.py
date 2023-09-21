import logging
import os

from nagiosplugin import Context
from nagiosplugin.state import Critical, Ok, Unknown, Warn


class BooleanContext(Context):
    def __init__(self, name, expected=True, warning=False, critical=False):
        super().__init__(name)
        self.expected = expected
        self.warning = warning
        self.critical = critical

    def evaluate(self, metric, resource):
        if not metric.value is self.expected:
            result_type = Ok
            if self.critical:
                result_type = Critical
            elif self.warning:
                result_type = Warn
            return self.result_cls(
                result_type, f"{metric.name} is not {self.expected}", metric
            )
        else:
            return self.result_cls(Ok, None, metric)


def show_version():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "VERSION"), "r"
    ) as fd:
        print(fd.read().strip())


def setup_logging(args):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=args.loglevel)
