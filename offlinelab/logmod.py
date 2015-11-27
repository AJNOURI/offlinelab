#!/usr/bin/env python

import logging


def logInit(level):
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('initconfig.log', mode='w')
    # Create logging format and bind to root logging object
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
    # Create file handler
    handler.setFormatter(formatter)
    return handler
