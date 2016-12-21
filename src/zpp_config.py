##
## ZPP configuration loader
##
import sys
import logging
from zpp_lib import *
from zpp_hb_lib import *

_DESC="""Zabbix Python Proxy"""
_EPILOG="""ZPP will interact with Zabbix Server and Zabbix Proxies providing you a smart and programmable connector for all purposes."""
_MAXATTEMPTS=100


class PyConfig:
    def __init__(self):
        self.parser.add_argument("-n", "--python", type=str, default=".", help="Semi-colon separated list of the directories added to a PYTHONPATH")
        self.ready -= 1
    def process(self):
        for d in self.args.python.split(";"):
            if not check_directory(d):
                print "Directory %s can not be added to a PYTHONPATH"%d
                self.ready += 1
            else:
                sys.path.append(d)
class ClipsConfig:
    def __init__(self):
        self.parser.add_argument("-c", "--config", type=str, default="/etc/zpp",
                                 help="Path to the config (bootstrap) directory")
        self.parser.add_argument("-m", "--models", type=str, default="/etc/zpp/models",
                                 help="Path to the models directory")
        self.parser.add_argument("--trace", "-t", action="store_true")
        self.ready -= 1
    def process(self):
        self.bootstrap_file = "%s/bootstrap.clp"%self.args.config
        self.bootstrap_facts = "%s/bootstrap.facts" % self.args.config
        if not check_directory(self.args.config):
            print "Can not find bootstrap directory %s"%self.args.config
            self.ready += 1
        if not check_file_read(self.bootstrap_file):
            print "Can not find bootstrap file %s" % self.bootstrap_file
            self.ready += 1
        if not check_file_read(self.bootstrap_facts):
            print "Can not find bootstrap facts %s" % self.bootstrap_facts
            self.ready += 1
        self.models_path = self.args.models
        self.trace = self.args.trace
        if not check_directory(self.args.models):
            print "Can not find models directory %s" % self.models_path
            self.ready += 1



class RunConfig:
    def __init__(self):
        self.parser.add_argument("-i", "--id", type=str, required=True,
                                 help="ZPP Instance ID")
        self.parser.add_argument('model', metavar='N', type=str, nargs='*',help='Make of the model to process')
        self.parser.add_argument("--attempts", type=int, default=5,
                                 help="Number of repeated attempts for the failed operation")
        self.parser.add_argument("--verbose", "-v", action='count')
        self.parser.add_argument("--stdout", action='store_true',
                                 help="Send log to STDOUT")
        self.parser.add_argument("-l", "--log", type=str,
                                 help="Directory for the log files")
        self.parser.add_argument("--log_backup", type=int, default=5,
                                 help="Maximum number of log files")
        self.parser.add_argument("--log_size", type=str, default="10M",
                                 help = "Maximum size of log file")
        self.parser.add_argument("-p", "--pid", default="/tmp", type=str,
                                 help="Directory for the PID files")
        self.parser.add_argument("--zoo_cfg", default="/etc/mesos/zk.cfg", type=str,
                                 help="Path to the file, holding Zookeeper URL")
        self.parser.add_argument("--zookeeper", default="zk://127.0.0.1:2181/zpp", type=str,
                                 help="Zookeeper URI")

        self.ready -= 1
    def process(self):
        if len(self.args.model) == 0:
            print "You did not specified any model to run"
            self.ready += 1
        self.log_path = self.args.log
        if self.log_path and not check_directory_write(self.log_path):
            print "You can not write logs to the directory %s" % self.log_path
            self.ready += 1

        if self.args.verbose == 1:
            self.log_level = logging.CRITICAL
        elif self.args.verbose == 2:
            self.log_level = logging.ERROR
        elif self.args.verbose == 3:
            self.log_level = logging.WARNING
        elif self.args.verbose == 4:
            self.log_level = logging.INFO
        elif self.args.verbose >= 5:
            self.log_level = logging.DEBUG
        else:
            self.log_level = logging.NOTSET
        try:
            self.log_size = human2bytes(self.args.log_size)
        except:
            print "Log file size %s is invalid"%self.args.log_size
            self.ready += 1
        self.log_max = self.args.log_backup
        if self.args.zoo_cfg and check_file_read(self.args.zoo_cfg):
            try:
                self.zoo = open(self.args.zoo_cfg).read().strip()
            except:
                print "Can not read Zookeeper URI file %s"%self.args.zoo_cfg
                self.ready += 1
        else:
            self.zoo = self.args.zookeeper
        self.attempts = self.args.attempts
        if self.attempts > _MAXATTEMPTS:
            print "You specified too many attempts %s vs %s" % (bytes2human(self.attempts),_MAXATTEMPTS)
            self.ready += 1
        self.instance = self.args.id
        if not self.instance:
            print "You did not specified ZPP Instance ID"
            self.ready += 1


class Config(PyConfig, RunConfig,ClipsConfig):
    def __init__(self):
        import argparse
        self.parser = argparse.ArgumentParser(prog='zpp', description=_DESC, epilog=_EPILOG)
        self.ready = 3
        PyConfig.__init__(self)
        ClipsConfig.__init__(self)
        RunConfig.__init__(self)
        if self.ready != 0:
            print "Argument parsing and checking is unsatisfactory. Exit."
            sys.exit(99)
        self.parse_args()
        PyConfig.process(self)
        ClipsConfig.process(self)
        RunConfig.process(self)
        if self.ready != 0:
            print "Argument processing is unsatisfactory. Exit."
            sys.exit(97)
    def parse_args(self):
        self.args = self.parser.parse_args()
        print self.args
    def shutdown(self):
        self.log("info", "Config shutdown")
        pass
