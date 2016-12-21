##
##
##
import time
from zpp_lib import *

class ZookeeperCmd:
    def ensure(self, path):
        if self.is_ready:
            try:
                return self.retry(self.zk.ensure_path, "Ensuring %s" % path, path)
            except:
                self.is_ready = False
        return None
    def __setitem__(self, key, value):
        self.ensure(key)
        if self.is_ready:
            try:
                return self.retry(self.zk.set, "Storing %s = %s" % (key,value), key, value)
            except:
                self.is_ready = False
        return None
    def __getitem__(self, key):
        if self.is_ready:
            try:
                res = self.retry(self.zk.get, "Reading %s " % key, key)
                return res[0]
            except:
                self.is_ready = False
        return None
class ZookeeperMetaCmd:
    def heartbeat(self):
        self["%s/servers/%s/heartbeat"%(self.zoo_path, self.instance)] = str(time.time())
    def getHeartbeat(self):
        return float(self["%s/servers/%s/heartbeat"%(self.zoo_path, self.instance)])
class ZookeeperEnv:
    def __init__(self):
        from kazoo.retry import KazooRetry
        try:
            self.zoo_hosts, self.zoo_path = self.uri2hosts(self.zoo)
        except:
            self.log("critical", "Can not parse Zookeeper URI %s"%self.zoo)
            self.is_ready = False
        if not self.zoo_hosts or not self.zoo_path:
            self.log("critical", "Malformed Zookeeper URI %s" % self.zoo)
            self.is_ready = False
        self.zoo_retry = KazooRetry(max_tries=self.attempts, ignore_expire=False)
        self.connect()
    def retry(self, cmd, msg, *args):
        arg = tuple([cmd,] + list(args))
        self.log("debug", msg)
        try:
            return apply(self.zoo_retry, arg, {})
        except:
            self.log("traceback", "Error in executing %s "%repr(arg))
    def uri2hosts(self, uri):
        from urlparse import urlparse
        try:
            res = urlparse(self.zoo)
        except:
            return (None, None)
        return (res.netloc, res.path)
    def _connect(self):
        from kazoo.client import KazooClient
        try:
            self.zk = KazooClient(hosts=self.zoo_hosts)
            self.zk.start()
        except:
            return False
        return True
    def _shutdown(self):
        try:
            self.zk.stop()
        except:
            return False
        return True
    def connect(self):
        self.log("info", "Trying to connect to ZK bus %s"%self.zoo)
        if repeat(self._connect, self.log, self.attempts, "Connecting to ZK") == True:
            self.log("info", "Connected to ZK")
        else:
            self.log("critical", "Connection to ZK had failed")
            self.is_ready = False
        self.ensure(self.zoo_path)
        self.ensure("%s/servers"%self.zoo_path)
        self.heartbeat()
        print self.getHeartbeat()
    def shutdown(self):
        self.log("info", "Zookeeper shutdown")
        if repeat(self._shutdown, self.log, self.attempts, "Disconnection from ZK") == True:
            self.log("info", "ZK has been disconnected")
        else:
            self.log("critical", "Disconnection attempts from ZK bus had failed")
            self.is_ready = False


class Zookeeper(ZookeeperEnv, ZookeeperCmd, ZookeeperMetaCmd):
    pass