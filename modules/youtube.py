import urlparse, urllib, simplejson


inithooks = ["server", "chan", "lastpubmsg"]
args = ["youtube.com/watch", "youtu.be/"]


def GetInMS(seconds):
        minutes = seconds / 60
        seconds -= 60*minutes
        return "%02d:%02d" % (minutes, seconds)


def init(server, chan, lastpubmsg):
    if "http://" in lastpubmsg:
        yt = lastpubmsg.split('http://')[1]
    elif "https://" in lastpubmsg:
        yt = lastpubmsg.split('https://')[1]
    elif "www." in lastpubmsg:
        yt = lastpubmsg.split('www.')[1]
    if 'yt' in vars():
        if ' ' in yt:
            yt = yt.split(' ')[0]
        yt = urlparse.urlparse('http://'+ yt)
        query = urlparse.parse_qs(yt.query)
        if "youtube.com/watch" in lastpubmsg:
            vid = query["v"][0]
        elif "youtu.be/" in lastpubmsg:
            vid = yt.path[1:12]
        if len(vid) == 11:
            try:
                f = urllib.urlopen("http://gdata.youtube.com/feeds/api/videos/"+ vid +"?v=2&alt=jsonc")
                fd = simplejson.load(f)
                server.privmsg(chan, chr(3) + "07[YouTube]" + chr(3) + " Title: " + chr(3) + "07" + fd['data']['title'].encode('utf-8') +
                            chr(3) + " | Uploader: " + chr(3) + "07" + fd['data']['uploader'] + chr(3) +
                            "(" + chr(3) + "07" + fd['data']['uploaded'][:-14] + chr(3) + ")" +
                            chr(3) + " | Duration: " + chr(3) + "07" + GetInMS(fd['data']['duration']) +
                            chr(3) + " | Views: " + chr(3) + "07" + str(fd['data']['viewCount']) + chr(3))
            except Exception,e:
                server.privmsg("Syed", str(e))
                server.privmsg(chan, "Some sort of error.")
                pass
    else:
        server.privmsg(chan, "Broken youtube link.")
