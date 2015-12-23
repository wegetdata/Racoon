#!/usr/bin/python2
#
# slave checks
#

import socket
import socks

class PortCheck:

    def __init__( self, host, port ):

        self.host     = host
        self.port     = port
        self.result   = None
        self.checked = 0
        
        socks.setdefaultproxy( socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050 )
        socket.socket = socks.socksocket
        socket.create_connection = self._create_connection_
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.sock.settimeout( 3 )

    def _create_connection_( self, address, timeout=None, source_address=None ):
        
        sock = sock.socksocket()
        sock.connect( address )
        return sock


    def run( self ):

        try:
            self.sock.connect(( self.host, self.port ))
            self.result = "Open"
        except:
            self.result = "Closed"
	self.checked = 1
       
