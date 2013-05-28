# -*- coding: utf-8 -*-

import src.irclib as irclib
import sys, os, thread
from settings import *
import modules

irc = irclib.IRC()
server = irc.server()
server.connect(network, port, nick, ircname=name)

unmods = list()

def getmodules():
    global hooks, pmhooks, args, pmargs, mods
    hooks, pmhooks, args, pmargs = dict(), dict(), dict(), dict()
    mods = list()
    reload(modules)
    loads(None, None)
    for mod in dir(modules):
        if "__" not in mod and "os" not in mod and "modules." + mod not in unmods:
            mod = "modules." + mod
            mods.append(mod)
            modu = sys.modules[mod]
            hooks[mod] = modu.inithooks
            args[mod] = modu.args
            try:
                pmhooks[mod] = modu.initpmhooks
                pmargs[mod] = modu.pmargs
            except:
                pass


def initmodule(last, type, pers):
    inithooks, initpmhooks = list(), list()
    for mod in mods:
        counter = 0
        for x in args[mod]:
            inithooks = []
            if x in last:
                counter = counter + 1
                x = 0
                for hook in hooks[mod]:
                    if hooks[mod][x]:
                        inithooks.append(globals()[hooks[mod][x]])
                        x = x + 1
                if counter == 1:
                    try:
                        inithooks = tuple(inithooks)
                        thread.start_new_thread(sys.modules[mod].init, (inithooks))
                    except Exception as e:
                        server.privmsg(chan, mod + " failed because of the following error: %s: %s" % (e.__class__.__name__, str(e)))
                        server.privmsg(admin, mod + " failed because of the following error: %s: %s" % (e.__class__.__name__, str(e)))
        if mod in pmargs and type == "pm" and not pmer is None:
            for x in pmargs[mod]:
                initpmhooks = []
                if x in last:
                    x = 0
                    for hook in pmhooks[mod]:
                        if pmhooks[mod][x]:
                            initpmhooks.append(globals()[pmhooks[mod][x]])
                            x = x + 1
                    try:
                        inithooks = tuple(initpmhooks)
                        thread.start_new_thread(sys.modules[mod].init, (initpmhooks))
                    except Exception as e:
                        server.privmsg(pmer, mod + " failed because of the following error: %s: %s" % (e.__class__.__name__, str(e)))
                        server.privmsg(admin, mod + " failed because of the following error: %s: %s" % (e.__class__.__name__, str(e)))


def loads(mod, type):
    global unmods
    update = open('src/unloaded.txt', 'w')
    if mod is None and type is None:
        unloads = open('src/unloaded.txt', 'r').readline()
        if ":" in unloads:
            unmods = unloads.split(':')
        elif len(unloads) > 3:
            unmods.append(unloads)
    elif not mod is None and type == "unload":
        try:
            if mod in sys.modules: del sys.modules[mod]
            if mod in hooks: del hooks[mod]
            if mod in pmhooks: del pmhooks[mod]
            if mod in args: del args[mod]
            if mod in pmargs: del pmargs[mod]
            if mod in mods:
                mods.remove(mod)
                unmods.append(mod)
                server.privmsg(chan, "Unloaded %s" % mod)
        except Exception, e:
            server.privmsg(chan, "The module: " + mod + " failed because: " + str(e))
            pass
    elif not mod is None and type == "load":
        if mod in unmods:
            unmods.remove(mod)
            update.write(":".join(unmods))
            server.privmsg(chan, "The module: %s has now been loaded." % mod)
            getmodules()
        elif mod in mods:
            server.privmsg(chan, "The module: %s is already loaded." % mod)
    elif not mod is None and type == "loadall":
        del unmods[:]
    update.write(":".join(unmods))


def modsettings(lm, ls, lh):
    if ' ' in lm:
        mod = lm.split(' ')[1]
        mod = "modules." + mod
    if ls == admin and lh == adminhost:
        if "!unload " in lm[:8]:
            loads(mod, "unload")
        if "!renderuseless" in lm[:14]:
            del mods[:]
            server.privmsg(chan, "All modules unloaded. Only admin commands remain.")
        if "!loadall" in lm[:8]:
            loads(None, "loadall")
            getmodules()
            server.privmsg(chan, "Loaded all unloaded modules.")
        if "!reload " in lm[:8]:
            if mod in mods and mod not in unmods:
                try:
                    reload(sys.modules[mod])
                    server.privmsg(chan, "Module %s reloaded." % mod)
                except Exception, e:
                    server.privmsg(chan, "The module: " + mod + " failed because: " + str(e))
                    pass
        if "!reload" in lm[:7] and " " not in lm:
            try:
                getmodules()
                server.privmsg(chan, "Modules reloaded.")
            except Exception, e:
                server.privmsg(chan, "Modules failed to reload because: " + str(e))
        if "!listmods" in lm[:9]:
            listunmods = ""
            if len(unmods) > 0:
                listunmods = " | Unloaded modules: " + ", ".join(unmods).replace('modules.', '')
            server.privmsg(chan, "Loaded modules: " + ", ".join(mods).replace('modules.', '') + listunmods)
        if "!load " in lm[:6]:
            loads(mod, "load")


def handleEndMotd(connection, event):
        print "You have properly connected to " + network
        if not nickpass is None:
            server.privmsg("Nickserv", "id " + nickpass)
        if not operpass is None:
            server.send_raw("OPER " + nick + " " + operpass)
        server.send_raw("UMODE2 " + modes)
        server.join(chan)
        getmodules()


def handlePubMessage(connection, event):
        global lastpubmsg, lasthost, lastspeaker, chan
        target = event.target()
        del chan  # Remove the channel from settings(MULTI-CHAN SUPPORT)
        chan = target
        speaker = event.source().split('!')[0]
        lasthost = event.source().split('!')[1]
        lastpubmsg = event.arguments()[0].decode('utf8')
        print target, ">", speaker, ":", lastpubmsg.encode('utf-8').strip()
        lastspeaker = speaker
        if speaker != lastspeaker:
            print (speaker + " says ")
        initmodule(lastpubmsg, "pubmsg", None)
        modsettings(lastpubmsg, lastspeaker, lasthost)


def handleprivmsg(connection, event):
    global pm, pmer
    pm = event.arguments()[0]
    pmer = event.source().split('!')[0]
    print pmer, ":", pm
    initmodule(pm, "pm", pmer)


def handledc(connection, event):
    python = sys.executable
    os.execl(python, python, * sys.argv)

irc.add_global_handler('endofmotd', handleEndMotd)
irc.add_global_handler('pubmsg', handlePubMessage)
irc.add_global_handler('privmsg', handleprivmsg)
irc.add_global_handler('disconnect', handledc)
irc.process_forever()
