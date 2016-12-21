##
## ZPP Logging utility
##

import sys
import os
import logging
from logging.handlers import *

class Log:
    def __init__(self):
        if self.ready != 0:
            print "ZPP not ready to open log. Exit."
            sys.exit(98)
        if self.log_level > 0 and self.log_path and not self.args.stdout:
            self.log_file = "%s/zpp.%d.%s.log"%(self.log_path, time.time(), time.strftime("%d.%m.%Y@%H:%M"))
            self.trace_file = "%s/zpp.%d.%s.trace" % (self.log_path, time.time(), time.strftime("%d.%m.%Y@%H:%M"))
            self.logger = logging.getLogger('zpp')
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%d.%m.%Y@%H:%M:%S")
            rhandler = RotatingFileHandler(self.log_file, maxBytes=self.log_size,backupCount=self.log_max)
            rhandler.setFormatter(formatter)
            self.logger.addHandler(rhandler)
            self.logger.setLevel(self.log_level)
        elif self.log_level > 0 and self.args.stdout:
            self.logger = logging.getLogger('zpp')
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%d.%m.%Y@%H:%M:%S")
            rhandler = logging.StreamHandler()
            rhandler.setFormatter(formatter)
            self.logger.addHandler(rhandler)
            self.logger.setLevel(self.log_level)
        else:
            self.log_level = 0
    def log(self, mode, msg, **kw):
        if self.log_level > 0:
            _msg = msg%kw
            if mode[0].lower() == 'c':
                self.logger.critical(_msg, exc_info=True)
            elif mode[0].lower() == 'w':
                self.logger.warn(_msg)
            elif mode[0].lower() == 'e':
                self.logger.error(_msg, exc_info=True)
            elif mode[0].lower() == 'i':
                self.logger.info(_msg)
            elif mode[0].lower() == 't':
                self.logger.exception(_msg)
            else:
                self.logger.debug(_msg)

    def shutdown(self):
        self.log("info", "Log shutdown")
        pass
