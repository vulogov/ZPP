##
## Zabbix Python Proxy main file
##
import os
import sys

from zpp_config import Config
from zpp_log import Log
from zpp_zoo import Zookeeper
from zpp_clp import CLP

global MAIN

class Main(Config, Log, Zookeeper):
    def __init__(self):
        self.is_ready = True
        Config.__init__(self)
        Log.__init__(self)
        Zookeeper.__init__(self)
        if not self.is_ready:
            self.log("critical", "ZPP Error before CLP initialization")
            self.shutdown()
            sys.exit(52)
        try:
            self.clips = CLP(self,
                             bootstrap=self.bootstrap_file,
                             initial_facts=self.bootstrap_facts)
        except ValueError, msg:
            self.log("critical", "ZPP Error during CLP initialization: %s"%msg)
            sys.exit(53)
    def shutdown(self):
        if self.is_ready:
            self.clips.shutdown()
            Zookeeper.shutdown(self)
            Log.shutdown(self)
            Config.shutdown(self)
    def MAIN(self):
        if not self.is_ready:
            self.log("critical", "ZPP is not ready. Exit.")
            self.shutdown()
            sys.exit(50)
        self.shutdown()





def main():
    global MAIN
    MAIN = Main()
    MAIN.MAIN()

if __name__ == '__main__':
    main()

