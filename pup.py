#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import signal
import sys

from multiprocessing import Process
from random import randint
from connection import *
from checks import PortCheck

nick      = "Pup[{}]".format( str( randint( 100, 999 ) ) )
server    = "irc.blackcatz.org"
channel   = "#Tanuki"
password  = "ohlookyouknowthepassword"
usessl    = True
owner     = "Racoon@blackcatz-d4j.irl.us70sb.IP"
jobs      = []

def signal_handler( signal, frame ):
    """ Gracefully exit on SIGINT """
    print "\n[+] Quitting"
    sys.exit( 0 )

pup = Connection( server, 6697, usessl )
pup.ident( nick, nick, nick )
pup.set_nick( nick )

while 1:
    
    signal.signal( signal.SIGINT, signal_handler )
    text  = pup.recv( 4096 )
    
    if "PRIVMSG #Tanuki :{}:".format( nick ) in text:

        if owner in text:
            """ parse command """
            target = ":".join( [ x for x in text.split( ":" )[3:] ] ).lstrip()
            match  = re.match( r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', target )
            hello  = re.match( r'こんにちは', target )

            if hello:
                pup.msg_channel( channel, "\033[1;34m[+] こんにちは\033[0m" )

            elif match:
                targethost = target.split( ":" )[0]
                targetport = int( target.split( ":" )[1] )
                pc = PortCheck( targethost, targetport )
                proc = Process( pc.run() ).start()
    	        while pc.checked is 0:
		    pass

                if pc.result is "Open":

                    pup.msg_channel( channel, "\033[1;32m[+] {}:{} - Open\033[0m".format( targethost, str( targetport ) ) )

                elif pc.result is "Closed":

                    pup.msg_channel( channel, "\033[1;31m[!] {}:{} - Closed\033[0m".format( targethost, str( targetport ) ) )

            else:
                pup.msg_channel( channel, "\033[1;33m[!] Invalid target\033[0m" )

        else:
            pup.msg_channel( channel, "\033[1;33m[!] 我々はタヌキです\033[0m" )

    if text.find( "396" ) != -1:
        """ join after opcode """
        pup.join_channel( channel, password )

    if text.find( "PING" ) != -1:
	"""kinda need this"""
        pup.ping( text.split()[1]+"\r\n" )


