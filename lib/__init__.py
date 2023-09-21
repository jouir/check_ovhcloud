import logging
import os


def show_version():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "VERSION"), "r"
    ) as fd:
        print(fd.read().strip())


def setup_logging(args):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=args.loglevel)
