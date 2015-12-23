#!/usr/bin/python2

import socket, sys, string
from threading import Thread
from time import gmtime, strftime
from random import choice, randint

class Client:

    def __init__( self, conn, addr, sessionid ):
        
        self.state = {
            "conn"      : conn,
            "addr"      : addr,
            "sessionid" : sessionid,
            "timestamp" : strftime( "%m|%d|%Y %H:%M", gmtime() ),
            "thread"    : None,
            "active"    : False,
            "authed"    : False,
            "threshold" : 3,
            "lockout"   : 18000,
            "finished"  : False,
            "data"      : None
        }
        
        self.state["thread"] = Thread( target=self._start_session_ )
        self.state["active"] = True
        self.state["thread"].start()

    def _start_session_( self ):

        print "[+] New connection || {}".format( self.state["timestamp"] )
        
        while True:

            self.state["data"] = self.state["conn"].recv( 4096 )
            if not self.state["data"]:

                break

            print self.state["data"]

        self.state["conn"].close()
        self.state["thread"].join()
        self.state["active"] = False
        self.state["finished"] = True

class Serv:
    
    def __init__( self, host, port ):
        """ setup """
        self.state = {
            "host"     : host,
            "port"     : int( port ),
            "password" : "".join( choice( 
                                string.ascii_lowercase + 
                                string.digits + 
                                string.ascii_uppercase ) 
                            for x in range( 12 ) ),
            "running"  : False,
            "active"   : [],
            "sessions" : 0,
            "total"    : 0
        }

    def run( self ):

        """ build sock """
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.sock.settimeout( 3 )
        self.sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.sock.bind(( self.state["host"], self.state["port"] ))
        self.state["running"] = True

        """ start listener """
        print "[+] Running"
        while True:
        
            try:
                self.sock.listen( 10 )
                conn, addr = self.sock.accept()
                client = Client( conn, addr, str( randint( 100, 999 ) ) )
                self.state["active"].append( client )
                self.state["sessions"] += 1
                self.state["total"] += 1

                for client in self.state["active"]:
                    """ clear off dead sessions """
                    if client.state["finished"] is True:
                        self.state["clients"].remove( client )
                        self.state["session"] -= 1
            except:
                continue
