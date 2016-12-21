##
## Zabbix Python Proxy main file
##
import os
import sys

from zpp_config import Config
from zpp_log import Log
from zpp_zoo import Zookeeper

class Main(Config, Log, Zookeeper):
    def __init__(self):
        self.is_ready = True
        Config.__init__(self)
        Log.__init__(self)
        Zookeeper.__init__(self)
    def shutdown(self):
        if self.is_ready:
            Zookeeper.shutdown(self)
            Log.shutdown(self)
            Config.shutdown(self)
    def run(self):
        if not self.is_ready:
            self.log("critical", "ZPP is not ready. Exit.")
            self.shutdown()
            sys.exit(50)
        self.shutdown()





def main():
    m = Main()
    m.run()

if __name__ == '__main__':
    main()

