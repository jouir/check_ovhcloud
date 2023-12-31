#!/usr/bin/env python3

import argparse
import logging
import sys
import ovh

from check_ovhcloud import setup_logging, show_version, BooleanContext

from nagiosplugin import (
    Check,
    Metric,
    Resource,
    Summary,
)
from nagiosplugin.state import Unknown

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        action="store_const",
        const=logging.INFO,
        help="Print more output",
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="loglevel",
        action="store_const",
        const=logging.DEBUG,
        default=logging.WARNING,
        help="Print even more output",
    )

    parser.add_argument(
        "--version",
        dest="show_version",
        action="store_true",
        help="Print version and exit",
    )

    args = parser.parse_args()
    return args


class Ping(Resource):
    def __init__(self, client):
        self.client = client

    def probe(self):
        try:
            me = self.client.get(f"/me")
            return [Metric(me["firstname"], True, context="ping")]
        except Exception as err:
            return [Metric(str(err), False, context="ping")]


def main():
    args = parse_arguments()
    setup_logging(args)

    if args.show_version:
        show_version()
        return

    try:
        check = Check(
            Ping(client=ovh.Client()),
            BooleanContext("ping", expected=True, critical=True),
            Summary(),
        )
        check.main()
    except Exception as err:
        print(f"Failed to execute check: {str(err)}")
        logger.debug(err, exc_info=True)
        sys.exit(Unknown.code)
