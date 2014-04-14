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
from datetime import timedelta
from optparse import OptionParser
from uptime import uptime
from db import BotTasks
botDatabase = BotTasks()

def __readTextfile(__sFileName):
	__fTxtFile = open(__sFileName, "r")
	return (__lFileContent)

def __checkSallutation(__sMessage, __sFileName):
	__lFileContent = __readTextfile(__sFileName)
	if "hi" in __lFileContent.lower() or "huhu" in __lFileContent.lower():
		return True

def __getSallutation(__sFileName):
	return random.choice(__readTextfile(__sFileName))

def __getBOFH(__sFilename):
	return random.choice(__readTextfile(__sFileName))

def __getHttpTitle ():
	__title = cmd.__getHttpContent(sMessage)
	return re.search('<title>(.*)</title>',title, re.DOTALL, re.IGNORECASE).group(1)

def __listCommands(__sName):
	return (str(botDatabase.getMemberCommandsByMemberNames(__sName)))

def __hint(__sCommand):
	return (str(botDatabase.getHintHyCommand(__sCommand)))

def __getDiskUsage():
	return (str(round(psutil.disk_usage('/').percent))+"%")

def __getUsedMem():
	return str((psutil.used_phymem() / 1024**2))+" MB used ..."

def __getHttpContent (sMessage):
	__matchObj = re.match("(https?:\/\/.*\S+)", sMessage)
	if __matchObj:
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
	

#def __bofh():
#	__htmlContent = __getHttpContent("URL")
#	return re.search('<td bgcolor="#ffffff"><pre>(.*)</pre></td>',__htmlContent, re.DOTALL, re.IGNORECASE).group(1)

#def __listMemes():
	

#def __meme(__sMeme):
	
