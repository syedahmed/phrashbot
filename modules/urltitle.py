import BeautifulSoup
import urllib


inithooks = ["server", "chan", "lastpubmsg"]
args = ["http://", "https://", "www."]


def init(server, chan, lastpubmsg):
    if not "." in lastpubmsg:
        return
    if "www." in lastpubmsg:
        split1 = lastpubmsg.split("www.")[1]
    elif "http://" in lastpubmsg:
        split1 = lastpubmsg.split("http://")[1]
    elif "https://" in lastpubmsg:
        split1 = lastpubmsg.split("https://")[1]
    imgformats = ["gif", "png", "jpg", "jpeg", "tif"]
    skip = ['sythe.org/', 'puu.sh', 'youtube.com', 'youtu.be']
    if split1.rsplit('.', 1)[1] not in imgformats and not any(e in split1 for e in skip):
        try:
            soup = BeautifulSoup.BeautifulSoup(urllib.urlopen("http://" + split1))
            urltitle = soup.title.string.encode("utf-8")
            server.privmsg(chan, "URL title: %s" % urltitle)
        except IOError:
            server.privmsg(chan, "Error: Could not get URL title because it doesn't load.")
            pass
