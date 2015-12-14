#!/usr/bin/env python

import logging

class logclass(object):
    def __init__(self,level=logging.INFO,logfile='offlinelab.log'):
        self.level = level
        self.logfile = logfile
          
    def logInit(self):
        logging.basicConfig(level=self.level)
        self.handler = logging.FileHandler(self.logfile, mode='w')
        # Create logging format and bind to root logging object
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
        # Create file handler
        self.handler.setFormatter(formatter)
