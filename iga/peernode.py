import xmlrpclib
from socket import setdefaulttimeout
setdefaulttimeout(2.)
import pickle

#-------------------------------------------#
class PeerNode:
    def __init__(self, ip_address, app_name, port = 55800):
        self.ip_address = ip_address
        self.app_name = app_name
        self.proxy = None
        self.connected = False
        self.port = port

        self.connect()

    def getName(self):
        if self.local:
            return self.port
        else:
            return self.ip_address

    def connect(self):
        self.proxy = xmlrpclib.Server("http://%s:%i" % 
                        (self.ip_address, self.port))
        try:
            self.proxy.test()
            self.connected = True
        except:
            self.connected = False
            self.proxy = None

        return self.connected


    def getGenomes(self):
        '''
        Check if genomes from peers are the same type as my genomes.
        '''
        peer_data = self.proxy.getGenomes()
        genomes, app_name = pickle.loads(peer_data)
        if app_name == self.app_name:
            return genomes
        else:
            return []

    def isDone(self):
        '''
        Check if genomes from peers are the same type as my genomes.
        '''
        return self.proxy.isDone()

    def online(self):
        '''
        Test if node is connected. 
        If the node is online, then do a test call.
        If not online, then try to reconnect.
        '''
        if self.connected:
            try:
                self.proxy.test()
                return True
            except:
                self.connected = False
                self.proxy = None
                return False
        else:
            # try to connect
            result = self.connect()
            return result


