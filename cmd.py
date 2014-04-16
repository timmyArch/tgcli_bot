#!/usr/bin/env python2
"""

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

"""

import re
import psutil
import sys
import os
import pycurl
import random
from datetime import timedelta
from optparse import OptionParser
from StringIO import StringIO
from uptime import uptime
from db import BotTasks
botDatabase = BotTasks()

def __readTextfile(__sFileName):
	__buffer = []
	__fTxtFile = open(__sFileName, "r")
	for line in __fTxtFile:
		__buffer.append(line)
	return (__buffer)

def __checkSallutation(__sMessage, __sFileName):
	__lFileContent = __readTextfile(__sFileName)
	if any(__sMessage.lower() in __sElement.lower() for __sElement in __lFileContent):
		return True

def __getSallutation(__sFileName):
	return random.choice(__readTextfile(__sFileName))

def __getHttpTitle(sMessage):
	__content = __getHttpContent(sMessage)
	return re.search('<title>(.*)</title>',__content, re.DOTALL,).group(1)

def __checkHttpTitle(sMessage):
	__matchObj = re.match("(https?:\/\/.*\S+)", sMessage)
	if __matchObj:
		return True

def __getBOFH(__sFilename):
	return random.choice(__readTextfile(__sFilename))

def __listCommands(__sName):
	return (' ; '.join(botDatabase.getMemberCommandsByMemberNames(__sName)))

def __hint(__sMessage):
	__aArgs = __sMessage.split(" ")
	__lCommands = botDatabase.getCommands()
	if len(__aArgs) > 1 and  __aArgs[1] != "":
		for s in __lCommands:
			if __aArgs[1] == s[0]:
				return (str(botDatabase.getHintByCommand(__sMessage.split(" ")[1])))
	else:
		return ("Keine zulaessigen Parameter angegeben!")

def __getDiskUsage():
	return (str(round(psutil.disk_usage('/').percent))+"%")

def __getUsedMem():
	return str((psutil.used_phymem() / 1024**2))+" MB used ..."

def __getHttpContent (sMessage):
	__matchObj = re.match("(https?:\/\/.*\S+)", sMessage)
	storage = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, __matchObj.group(1))
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.setopt(pycurl.FOLLOWLOCATION, 1)
	c.perform()
	c.close()
	content = storage.getvalue()
	return content

def __ping(sIP):
	__sPing = os.system("ping -c1 " + sIP)
	return (sIP+" is down",sIP+" is up")[bool(__sPing == 0)]

def __getUptime():
	__sSeconds = uptime()
	return str(timedelta(seconds=__sSeconds))

def __getLoad():
	return (os.getloadavg())

#def __showAllTasks():
	

#def __showTasks(__sName):
	

#def __addTask():
	

#def __delTask(TaskID):
	

#def __listMemes():
	

#def __meme(__sMeme):
	
