import re, urllib, simplejson


inithooks = ["server", "chan", "lastpubmsg", "lastspeaker"]
args = ["!ud ", "@ud "]

def init(server, chan, lastpubmsg, lastspeaker):
    il = re.compile("[^\W]+", re.UNICODE)
    if "!ud " in lastpubmsg[:4] or "@ud " in lastpubmsg[:4]:
        ud = lastpubmsg.split('ud ')[1]
        ud = ud.replace(' ', '+')
        if "@ud" in lastpubmsg:
            pub = True
        else:
            pub = False
        if il.findall(ud):
            udopen = urllib.urlopen('http://api.urbandictionary.com/v0/define?term='+ ud)
            udsearch = simplejson.load(udopen)
            if udsearch['result_type'] != "no_results":
                definition = udsearch['list'][0]['definition'].encode('utf-8')
                if len(definition) > 400:
                    definition = definition[:430].rsplit(' ', 1)[0]
                    definition += "..."
                if pub == True:
                    server.privmsg(chan, chr(3) + "07[UD]" + chr(3) + ' Permalink: ' + chr(3) + "07http://www.urbandictionary.com/define.php?term=" + ud)
                    server.privmsg(chan, chr(3) + "07[UD]" + chr(3) + " Definition: " + chr(3) + "07" + definition)
                else:
                    server.notice(lastspeaker, chr(3) + "07[UD]" + chr(3) + ' Permalink: ' + chr(3) + "07http://www.urbandictionary.com/define.php?term=" + ud)
                    server.notice(lastspeaker, chr(3) + "07[UD]" + chr(3) + " Definition: " + chr(3) + "07" + definition)
            elif pub:
                server.privmsg(chan, chr(3) + "07[UD]" + chr(3) + " No results found.")
            else:
                server.notice(lastspeaker, chr(3) + "07[UD]" + chr(3) + " No results found.")