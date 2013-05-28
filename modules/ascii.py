# -*- coding: utf-8 -*-


inithooks = ["server", "chan", "lastpubmsg"]
args = ["!asc"]

def init(server, chan, la):
    s = la.split("!asc ")[1]
    ascii = []
    for char in s:
        ascii.append("&#" + str(ord(char)) + ";")
    server.privmsg(chan, "Here's the ascii character version of the text inputted: %s " % "".join(ascii))