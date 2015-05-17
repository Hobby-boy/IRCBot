#! python2
import socket
import time
from sys import exit

server = "irc.esper.net"
port = 6667
channel = "#Epic"
botnick = "Hobbybot"
prefix = ","


def main():
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to: " + server
    irc.connect((server, port))
    irc.send("NICK " + botnick + "\r\n")
    irc.send("USER " + botnick + " " + botnick + " " + botnick + " :This is a bot\r\n")
    buf = ""

    while 1:
        recvd = irc.recv(4096)
        text = recvd.split('\n')
        text[0] = buf + text[0]
        last = len(text)
        last -= 1
        if not text[last].count('\r'):
            buf = text.pop()
        for line in text:
            print line
            msg = line.split(':')
            if msg[0].count('PING'):
                irc.send('PONG :' + msg[1] + '\r\n')
            elif len(msg) > 2 and (msg[2].count("End of /MOTD command.") or msg[2].count("End of message of the day.")):
                irc.send("JOIN " + channel + "\r\n")
            # elif len(msg) > 2 and msg[2].count("End of message of the day."):
            #                               irc.send("JOIN "+ channel +"\r\n")
        if recvd.find(':' + prefix + 'about') != -1:
            irc.send("PRIVMSG " + channel + " :This is my very basic IRC bot, which doesn't have much functionality. This is a work in progress.\r\n")

        if recvd.find(':' + prefix + 'help') != -1:
            irc.send("PRIVMSG " + channel + " :Current commands: ,about, ,help, ,info, ,test, ,version\r\n")

        if recvd.find(':' + prefix + 'test\r\n') != -1:
            irc.send("PRIVMSG " + channel + " :It works! (just)\r\n")

        if recvd.find(':' + prefix + 'info') != -1:
            irc.send("PRIVMSG " + channel + " :This bot is really buggy, and I have no idea what I am doing\r\n")

        if recvd.find(':' + prefix + 'version') != -1:
            irc.send("PRIVMSG " + channel + " :Very alpha. I need to rewrite parts of it, and port to Python 3.\r\n")
			
        if recvd.find(':' + prefix + 'code') != -1:
            irc.send("PRIVMSG " + channel + " :The source code is at: https://github.com/Hobby-boy/IRCBot \r\n")

        if recvd.find(':' + prefix + 'whoami') != -1:
            irc.send("PRIVMSG " + channel + " :You are \r\n")
            
        if recvd.find(':' + prefix + 'action') != -1:
            irc.send("PRIVMSG " + channel + " :\x01ACTION Test\001\r\n")
            
        if recvd.find(':' + prefix + 'ctcptest') != -1:
            irc.send("PRIVMSG " + channel + " :\x01Test\001\r\n")

        if recvd.find(':' + prefix + 'quit') != -1:
            irc.send("PRIVMSG " + channel + " :Goodbye!\r\n")
            irc.send("QUIT :Leaving")
            time.sleep(2)
            exit()


if __name__ == "__main__":
    main()