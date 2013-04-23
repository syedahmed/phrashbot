import BeautifulSoup, urllib

inithooks = ["server", "chan", "lastpubmsg"]
args = ["http://", "https://", "www."]

def init(server, chan, lastpubmsg):
    tld = ['ac','ad','ae','aero','af','ag','ai','al','am','an','ao','aq','ar','arpa','as','asia','at','au','aw','ax','az','ba','bb','bd','be','bf','bg','bh','bi','biz','bj','bm','bn','bo','br','bs','bt','bv','bw','by','bz','ca','cat','cc','cd','cf','cg','ch','ci','ck','cl','cm','cn','co','com','coop','cr','cu','cv','cw','cx','cy','cz','de','dj','dk','dm','do','dz','ec','edu','ee','eg','er','es','et','eu','fi','fj','fk','fm','fo','fr','ga','gb','gd','ge','gf','gg','gh','gi','gl','gm','gn','gov','gp','gq','gr','gs','gt','gu','gw','gy','hk','hm','hn','hr','ht','hu','id','ie','il','im','in','info','int','io','iq','ir','is','it','je','jm','jo','jobs','jp','ke','kg','kh','ki','km','kn','kp','kr','kw','ky','kz','la','lb','lc','li','lk','lr','ls','lt','lu','lv','ly','ma','mc','md','me','mg','mh','mil','mk','ml','mm','mn','mo','mobi','mp','mq','mr','ms','mt','mu','museum','mv','mw','mx','my','mz','na','name','nc','ne','net','nf','ng','ni','nl','no','np','nr','nu','nz','om','org','pa','pe','pf','pg','ph','pk','pl','pm','pn','post','pr','pro','ps','pt','pw','py','qa','re','ro','rs','ru','rw','sa','sb','sc','sd','se','sg','sh','si','sj','sk','sl','sm','sn','so','sr','st','su','sv','sx','sy','sz','tc','td','tel','tf','tg','th','tj','tk','tl','tm','tn','to','tp','tr','travel','tt','tv','tw','tz','ua','ug','uk','us','uy','uz','va','vc','ve','vg','vi','vn','vu','wf','ws','xxx','ye','yt','za','zm','zw'];
    if "www." in lastpubmsg and "." in lastpubmsg:
        split1 = lastpubmsg.split("www.")[1]
    elif "http://" in lastpubmsg and "." in lastpubmsg:
        split1 = lastpubmsg.split("http://")[1]
    elif "https://" in lastpubmsg and "." in lastpubmsg:
        split1 = lastpubmsg.split("https://")[1]
    if " " in split1: 
        split1 = split1.split(" ")[0]
    if "." in lastpubmsg and "split1" in vars():
        ndots = len(split1.split(".")) - 1
        if ndots == 2:
            tldcheck = split1.split(".")[ndots - 1][:4]
        else:
            tldcheck = split1.split(".")[ndots][:4]
        if "/" in tldcheck:
            tldcheck = tldcheck.split("/")[0]
    if "tldcheck" in vars() and tldcheck in tld: 
        if 'split1' in locals():
            imgformats = ["gif", "png", "jpg", "jpeg", "tif"]
            if split1.rsplit('.', 1)[1] not in imgformats and "sythe.org/" not in split1 and "puu.sh" not in split1 and "youtube.com" not in split1 and "youtu.be" not in split1:
                try:  
                    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen("http://"+ split1))
                    urltitle = soup.title.string.encode("utf-8")
                    server.privmsg(chan, "URL title: %s" % urltitle)
                except IOError: 
                    server.privmsg(chan, "Error: Could not get URL title because it doesn't load.")
                    pass