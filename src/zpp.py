##
## Zabbix Python Proxy main file
##
import os
import sys

from zpp_config import Config
from zpp_log import Log

class Main(Config, Log):
    def __init__(self):
        Config.__init__(self)
        Log.__init__(self)
    def run(self):
        pass



def main():
    m = Main()
    m.run()

if __name__ == '__main__':
    main()

