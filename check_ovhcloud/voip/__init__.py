#!/usr/bin/env python3

import argparse
import logging
import sys
import ovh
from datetime import datetime, timezone

from check_ovhcloud import setup_logging, show_version

from nagiosplugin import (
    Check,
    Metric,
    Resource,
    ScalarContext,
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

    parser.add_argument(
        "--registration-warning",
        "-w",
        dest="registration_warning",
        type=int,
        default=7200,
        help="Raise warning if last line registration time is higher than this threshold (in seconds)",
    )

    parser.add_argument(
        "--registration-critical",
        "-c",
        dest="registration_critical",
        type=int,
        default=86400,
        help="Raise critical if last line registration time is higher than this threshold (in seconds)",
    )

    args = parser.parse_args()
    return args


class Voip(Resource):
    def __init__(self, client):
        self.client = client

    def probe(self):
        metrics = []
        billing_accounts = self.client.get(f"/telephony")
        for billing_account in billing_accounts:
            service_names = self.client.get(f"/telephony/{billing_account}/line")
            for service_name in service_names:
                last_registration = self.client.get(
                    f"/telephony/{billing_account}/line/{service_name}/lastRegistrations"
                )[0]
                last_registration_delta = int(
                    (
                        datetime.now(tz=timezone.utc)
                        - datetime.fromisoformat(last_registration["datetime"])
                    ).total_seconds()
                )
                metrics.append(
                    Metric(
                        f"{service_name} last registration",
                        last_registration_delta,
                        context="last_registration",
                        uom="s",
                    )
                )
        return metrics


class VoipSummary(Summary):
    def problem(self, results):
        return ", ".join(
            [
                f"{result.metric.name} {result.state}: {result.hint}"
                for result in results
                if str(result.state) != "ok"
            ]
        )


def main():
    args = parse_arguments()
    setup_logging(args)

    if args.show_version:
        show_version()
        return

    try:
        check = Check(
            Voip(client=ovh.Client()),
            ScalarContext(
                "last_registration",
                warning=args.registration_warning,
                critical=args.registration_critical,
            ),
            VoipSummary(),
        )
        check.main()
    except Exception as err:
        print(f"Failed to execute check: {str(err)}")
        logger.debug(err, exc_info=True)
        sys.exit(Unknown.code)


if __name__ == "__main__":
    main()
