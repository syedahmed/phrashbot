import subprocess, os
from settings import admin, adminhost


inithooks = ["server", "chan", "lastpubmsg", "lastspeaker", "lasthost"]
args = ["!gitupdate"]


def init(server, chan, lastpubmsg, ls, lh):
    if os.name != "nt" and "!gitupdate" in lastpubmsg[:10] and ls == admin and lh == adminhost:
        p = subprocess.Popen(["git", "pull", "origin", "master"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=256*1024*1024)
        output, errors = p.communicate()
        if p.returncode:
            errlist = errors.split('\n')
            for line in errlist:
                if "error:" in line:
                    err = line
            server.privmsg(chan, "Encountered errors, my brother: %s" % err)
        elif "Already up-to-date." in output:
            server.privmsg(chan, "Current local repository is up to date.")
        else:
            changes = []
            outlist = output.split('\n')
            for line in outlist:
                if "|" in line:
                    changes.append(line.split("|")[0].replace(" ", ""))
                if "files changed" in line:
                    fchanges = line
            server.privmsg(chan, "The following files were altered: " + ", ".join(changes))
            server.privmsg(chan, fchanges)
    elif os.name == "nt":
        server.privmsg(chan, "You can't update on Windows at the moment. (Works via git repo, may add windows support later.)")