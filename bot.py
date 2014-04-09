import ConfigParser
import os
import random
import re
import psutil
import sys
import os
import pycurl
from StringIO import StringIO
from datetime import timedelta
from optparse import OptionParser
from uptime import uptime
from db import BotTasks


#variable declaration
lSallutations = ['Hy', 'Ahoi', 'Huhu', 'Hiho', 'Moin', 'Nabend',
                 'Hallo', 'Hi', 'Halli, Hallo, Halloechen.',
                 'Na?', 'Na, wie gehts?', 'Na du?', 'Salut.',
                 'Tach', 'Gruesse', 'Ach herrjieei', 'Sei gegruesst',
                 'Servus', 'Tag.']
botDatabase = BotTasks()
parser = OptionParser(usage = "usage: %prog [options] arg1 arg2")
parser.add_option("-n",
		  "--name",
		  dest="name",
		  type="string",
		  default=False,
		  help="name of the sender")
parser.add_option("-m",
		  "--message",
		  dest="message",
		  type="string",
		  default=False,
		  help="message from telegram")
(options, args) = parser.parse_args()
sName = options.name
sMessage = options.message

def __checkMessage():
	if sMessage.split(' ')[0][1:] in botDatabase.getMemberCommandsByMemberNames(sName):
		return __performCommand(sMessage)
	else:
		if sMessage in botDatabase.getCommands():
			return "Permission denied!"
		else:
			if __checkSallutation(sMessage):
				return __getSallutation()
			elif __checkURL(sMessage):
				return __getHttpTitle(sMessage)

def __performCommand(sMessage):
	__aArgs = sMessage.split(" ")
	if __aArgs[0] == ",ping":
		return(__ping(__aArgs[1]))
	elif __aArgs[0] == ",uptime":
		return(__getUptime())
	elif __aArgs[0] == ",load":
		return(__getLoad())
	elif __aArgs[0] == ",mem":
		return(__getUsedMem())
	elif __aArgs[0] == ",disk":
		return(__getDiskUsage())

def __checkSallutation(sLocalMessage):
	if "hi" in sLocalMessage.lower() or "huhu" in sLocalMessage.lower():
		return True

def __checkURL(sMessage):
		__matchObj = re.match("(https?:\/\/.*\S+)", sMessage)
		if __matchObj:
			return True

def __getSallutation():
        return random.choice(lSallutations)

def __getDiskUsage():
	return (str(round(psutil.disk_usage('/').percent))+"%")

def __getUsedMem():
	return str((psutil.used_phymem() / 1024**2))+" MB used ..."

def __getHttpTitle (url):
	storage = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.setopt(pycurl.FOLLOWLOCATION, 1)
	c.perform()
	c.close()
	content = storage.getvalue()
	return re.search('<title>(.*)</title>',content, re.DOTALL).group(1)

def __ping(sIP):
	__sPing = os.system("ping -c1 " + sIP)
	return (sIP+" is down",sIP+" is up")[bool(__sPing == 0)]

def __getUptime():
	__sSeconds = uptime()
	return str(timedelta(seconds=__sSeconds))

def __getLoad():
	return (os.getloadavg())		

a=__checkMessage()
if a and not a == "":
	print(a)
