#!/usr/bin/python2
# stripped from SCOUT by anticore
#

import socket
import sys
import ssl

class Connection:
    """ connection class, every bot instance has one """

    def __init__(self, host, port, useSsl):
        """ starts a new connection """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            #SSL connection
            if useSsl is True:
                #self.sock = ssl.wrap_socket(self.sock, ssl_version=ssl.PROTOCOL_TLSv1)
                self.sock = ssl.wrap_socket(self.sock)
                
            self.sock.connect((host, port))

        except socket.error, e:
            print "Socket error. %s" % (e)

    def send(self, data):
        """ sends a data string through the socket """
        self.sock.send(data)

    def set_nick(self, nick):
        """ sets/changes nickname of the bot """
        self.send("NICK %s\r\n" % (nick))

    def ident(self, ident, host, realname):
        """ ident the user """
        self.send("USER %s %s r :%s\r\n" % (ident, host, realname))

    def nickserv_identify(self, passwd):
        """ identifies using NickServ """
        self.send("PRIVMSG Nickserv :IDENTIFY %s\r\n" % (passwd))

    def ping(self, response):
        """ respond to pings """
        self.send("PONG %s\r\n" % (response))

    def msg_channel(self, channel, message):
        """ send message to a channel """
        self.send("PRIVMSG %s :%s\r\n" % (channel, message))

    def msg_user(self, user, message):
        """ send message to a user """
        self.send("PRIVMSG %s :%s\r\n" % (user, message))

    def get_names(self, channel):
        """ request user list for channel """
        self.send("NAMES %s\r\n" % (channel))
    
    def get_whois(self, nick):
        """ request whois info """
        self.send("WHOIS %s\r\n" % (nick))

    def join_channel(self, channel, password):
        """ join a new channel """
        self.send("JOIN %s %s\n" % (channel, password))

    def part_channel(self, channel):
        """ join a new channel """
        self.send("PART %s\n" % (channel))

    def recv(self, b ):
        """ receive data from the server """
        msg = self.sock.recv( b )
        return msg

    def end(self):
        """ end this connection """
        self.sock.close()
