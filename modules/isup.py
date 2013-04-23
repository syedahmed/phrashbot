import requests

inithooks = ["server", "chan", "lastpubmsg"]
args = ["!isup"]

def init(server, chan, la):
    tld = ['ac','ad','ae','aero','af','ag','ai','al','am','an','ao','aq','ar','arpa','as','asia','at','au','aw','ax','az','ba','bb','bd','be','bf','bg','bh','bi','biz','bj','bm','bn','bo','br','bs','bt','bv','bw','by','bz','ca','cat','cc','cd','cf','cg','ch','ci','ck','cl','cm','cn','co','com','coop','cr','cu','cv','cw','cx','cy','cz','de','dj','dk','dm','do','dz','ec','edu','ee','eg','er','es','et','eu','fi','fj','fk','fm','fo','fr','ga','gb','gd','ge','gf','gg','gh','gi','gl','gm','gn','gov','gp','gq','gr','gs','gt','gu','gw','gy','hk','hm','hn','hr','ht','hu','id','ie','il','im','in','info','int','io','iq','ir','is','it','je','jm','jo','jobs','jp','ke','kg','kh','ki','km','kn','kp','kr','kw','ky','kz','la','lb','lc','li','lk','lr','ls','lt','lu','lv','ly','ma','mc','md','me','mg','mh','mil','mk','ml','mm','mn','mo','mobi','mp','mq','mr','ms','mt','mu','museum','mv','mw','mx','my','mz','na','name','nc','ne','net','nf','ng','ni','nl','no','np','nr','nu','nz','om','org','pa','pe','pf','pg','ph','pk','pl','pm','pn','post','pr','pro','ps','pt','pw','py','qa','re','ro','rs','ru','rw','sa','sb','sc','sd','se','sg','sh','si','sj','sk','sl','sm','sn','so','sr','st','su','sv','sx','sy','sz','tc','td','tel','tf','tg','th','tj','tk','tl','tm','tn','to','tp','tr','travel','tt','tv','tw','tz','ua','ug','uk','us','uy','uz','va','vc','ve','vg','vi','vn','vu','wf','ws','xxx','ye','yt','za','zm','zw'];
    if '!isup' in la[:5]:
        la = la.split(' ')[1]
        if "https://" in la:
            la = la[8:]
        if "http://" not in la:
            la = "http://" + la 
        dots = len(la.split('.'))
        ndots = dots - 1
        if "." in la:
            tldcheck = la.split('.')[ndots]
            try:
                if tldcheck in tld:
                    stat = requests.get(la, timeout=10)
                    if stat.status_code == 200 and stat.text is not None:
                        server.privmsg(chan, la +" is up and serving content, try another by doing !isup site")
                    elif stat.status_code == 200 and stat.text is None:
                        server.privmsg(chan, la +" is up, but not serving content, try another by doing !isup site")
                    else: 
                        server.privmsg(chan, la +" is down, try another by doing !isup site")
                else:
                    server.privmsg(chan, "Use a valid TLD and try again.")
            except requests.exceptions.ConnectionError:
                server.privmsg(chan, "I do believe that the domain: "+la +" is not registered or is undergoing DNS issues.")
                pass
            except requests.exceptions.Timeout:
                server.privmsg(chan, "Request timed out.")
                pass
            except Exception,e: 
                server.privmsg("Syed", str(e))
                server.privmsg(chan, "Some sort of error.")
                pass
        else:
            server.privmsg(chan, "Enter a valid website in the following format: website.tld")