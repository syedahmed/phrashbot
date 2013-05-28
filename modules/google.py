import urllib, simplejson


inithooks = ['server', 'chan', 'lastpubmsg']
args = ['!g ']

def init(server, chan, lastpubmsg):
    if "!g " in lastpubmsg[:3]:
        gn = lastpubmsg.split(args[0])[1]
        gq = gn
        if " " in gn:
            gq = gn.replace(' ', '+')
        if len(gq) > 0:
            gurl = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='+ gq
            f = urllib.urlopen(gurl)
            fq = simplejson.load(f)
            x = 0
            if fq['responseData']['results'] == []:
                server.privmsg(chan, chr(3) + "07[Google]" + chr(3) + " No Results Found for: %s" % gn)
            else:
                for result in fq['responseData']['results']:
                    server.privmsg(chan, chr(3) + "07[Google]" + chr(3) + " Title: " + chr(3) + "07" + urllib.unquote(result['title']).encode('utf-8').replace("<b>", "").replace("</b>", "") +
                                         chr(3) + " | URL: " + chr(3) + "07" + urllib.unquote(result['url']) + chr(3))
                    x = x + 1
                    if x >= 1:
                        break