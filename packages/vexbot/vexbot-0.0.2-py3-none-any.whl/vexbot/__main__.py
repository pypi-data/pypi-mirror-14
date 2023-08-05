#!/usr/bin/env python3
# -*- coding: utf-8-*-
import sys
import logging
import argparse
from vexbot.robot import Robot


def main(*args, **kwargs):
    logging.basicConfig()
    logger = logging.getLogger()
    logger.getChild("client.stt").setLevel(logging.INFO)

    """
    if args.debug:
        logger.setLevel(logging.DEBUG)
    """

    try:
        app = Robot()
    except Exception:
        logger.error("Error occured!", exc_info=True)
        sys.exit(1)

    app.run()


def _get_kargs():
    parser = argparse.ArgumentParser(description='Vex, personal assistant')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Show debug messages')

    args = parser.parse_args()
    return vars(args)

if __name__ == "__main__":
    kwargs = _get_kargs()
    main(**kwargs)
