import requests


inithooks = ["server", "chan", "lastpubmsg"]
args = ["!isup"]


def init(server, chan, la):
    if '!isup' in la[:5]:
        la = la.split(' ')[1]
        if "https://" in la:
            la = la[8:]
        if "http://" not in la:
            la = "http://" + la
        if "." in la:
            try:
                stat = requests.get(la, timeout=10)
                if stat.status_code == 200 and stat.text is not None:
                    server.privmsg(chan, la + " is up and serving content, try another by doing !isup site")
                elif stat.status_code == 200 and stat.text is None:
                    server.privmsg(chan, la + " is up, but not serving content, try another by doing !isup site")
                else:
                    server.privmsg(chan, la + " is down, try another by doing !isup site")
            except requests.exceptions.ConnectionError:
                server.privmsg(chan, "DNS issues.")
                pass
            except requests.exceptions.Timeout:
                server.privmsg(chan, "Request timed out.")
                pass
        else:
            server.privmsg(chan, "Enter a valid website in the following format: website.tld")
