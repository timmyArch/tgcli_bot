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

import psycopg2
import sys
import ConfigParser

class BotDatabase(object):
	
	__database=	""
	__password=	""
	__user=			""
	__host=			""
	__con = 		None

	def __init__(self):
		self.__readConfig()
		self._connect()
			
	def __readConfig(self):
		try:
			config = ConfigParser.RawConfigParser()
			config.read('~/.bot.cfg')
			BotDatabase.__database=config.get('Database','db_name')
			BotDatabase.__password=config.get('Database','password')
			BotDatabase.__user		=config.get('Database','user')
			BotDatabase.__host		=config.get('Database','host')
		except:
			raise 'please check bot.cfg'

	def _connect(self):
		if not BotDatabase.__con:
			BotDatabase.__con = psycopg2.connect(
				database=BotDatabase.__database, 
				user=BotDatabase.__user, 
				password=BotDatabase.__password,
				host=BotDatabase.__host)

	def getAdmins(self):
		config = ConfigParser.RawConfigParser()
		config.read('~/.bot.cfg')
		return config.get('Roles','admin').split(',')

	def addMember(self,user):
		if not type(user) is tuple:
			raise TypeError('user must be a tuple (number, name)') 
		return self._insert_del("INSERT INTO members (number, name) VALUES (%s,%s)", user)

	def removeMember(self, user):
		if type(user) is int or (type(user) is str and user.isdigit()):
			a = self._insert_del("DELETE FROM members_commands WHERE members_id = %s", (user,)) 
			b = self._insert_del("DELETE FROM members WHERE members_id = %s ", (user,))
		else:
			a = self._insert_del("DELETE FROM members_commands WHERE members_id = ( " +
					"SELECT members_id FROM members WHERE name = %s " + 
				")", (user,))
			b = self._insert_del("DELETE FROM members WHERE name = %s ", (user,))
		return (False, True)[bool(a and b)]

	def getMemberById(self, user_id):
		return self._select("SELECT * FROM members WHERE members_id = %s ",(user_id,),False)

	def addMemberCommandByMemberId(self, user_id, command):
		if not type(command) is int and not (type(command) is str and command.isdigit()):
			command = self._select("SELECT commands_id FROM commands WHERE command = %s LIMIT 1" , (command,) , True)
		print((user_id, command))
		return self._insert_del("INSERT INTO members_commands (members_id, commands_id) VALUES ( %s , %s )", 
			(user_id, command))

	def removeMemberCommandByCommand(self, user_id, command):
		a = self._insert_del("DELETE FROM members_commands WHERE "+
			"commands_id = (SELECT commands_id FROM commands WHERE command = %s LIMIT 1)"+
			" and members_id = %s", (command, user_id)) 
		return (False, True)[bool(a)]
	
	def addMemberCommandByMemberName(self, user_name, command):
		user_id = self._select("SELECT members_id FROM members " +
			"WHERE name = %s LIMIT 1" , (user_name,), True)
		print(user_id)
		if user_id:
			return(False, True)[bool(self.addMemberCommandByMemberId(user_id[0],command))]
		return False

	def getCommands(self):
		return self._select("SELECT command FROM commands",False,False)
	
	def addCommand(self,dataset):
		if type(dataset) is tuple and len(dataset) == 3:
			return self._insert_del("INSERT INTO commands (command, short_hint, description) VALUES (%s,%s,%s)", dataset)
		else:
			raise TypeError('tuple needed (command, short_hint, descrition)')
	
	def removeCommand(self,command):
		if type(command) is int or (type(command) is str and command.isdigit()):
			a = self._insert_del("DELETE FROM members_commands WHERE commands_id = %s", (command,)) 
			b = self._insert_del("DELETE FROM commands WHERE commands_id = %s ", (command,))
		else:
			a = self._insert_del("DELETE FROM members_commands WHERE commands_id = ( " +
					"SELECT commands_id FROM commands WHERE command = %s " + 
				")", (command,))
			b = self._insert_del("DELETE FROM commands WHERE command = %s ", (command,))
		return (False, True)[bool(a and b)]

	def getHintByCommand(self,command):
		buf = self._select("SELECT short_hint FROM commands WHERE command = %s ", (command,), True)
		return (False , buf[0])[bool(buf[0])]
			
	def getDescriptionByCommand(self,command):
		buf = self._select("SELECT description FROM commands WHERE command = %s ", (command,),True)
		return (False , buf[0])[bool(buf[0])]

	def getTasksByMemberId(self,user_id):
		return self._select("SELECT * FROM tasks WHERE members_id = %s ", (user_id,), False)

	def getTasksByMemberName(self, user_name):
		a = self._select("SELECT member_id FROM members WHERE name = %s ", (user_name,), True)	
		if a:
			return self.getTasksByMemberName(a[1])
		return False

	def getMembers(self):
		return self._select("SELECT * FROM members", False, False)

	def getMemberCommandsByMemberId(self,user_id):
		retTuple = tuple()
		result = self._select("SELECT command FROM commands WHERE commands_id IN ( " + 
				"SELECT commands_id FROM members_commands WHERE members_id = %s " + 
			")", (user_id,) , False)
		if not result:
			return False
		for i in result:
			retTuple += (i[0],)
		return retTuple

	def getMemberCommandsByMemberNames(self,user_name):
		if type(user_name) is str:
			user_name = (user_name,)
		elif type(user_name) is list:
			True
		else:
			raise TypeError('check params')
		if len(user_name) == 1:
			res = self._select("SELECT members_id FROM members WHERE name = %s ", tuple(user_name), True)
			return self.getMemberCommandsByMemberId(res)
		else:
			user_command=dict()
			for i in user_name:
				buf = self._select("SELECT members_id FROM members WHERE name = %s ", (i,), True)
				user_command[i[0]] = self.getMemberCommandsByMemberId(buf)
			return user_command
		
	def getMembersWithCommands(self):
		buf = list()
		result = self._select("SELECT name FROM members", False, False)
		if not result:
			return False
		for i in result:
			 buf.append(i)
		return self.getMemberCommandsByMemberNames(buf)

	def select(self,query,values,onlyOneResult):
		return self._select(query,values,onlyOneResult)
	
	def _select (self, query, values, onlyOneResult ):
		try:
			cur = BotDatabase.__con.cursor()
			if values:
				cur.execute(query, values)
			else:
				cur.execute(query) 
			if onlyOneResult:
				return cur.fetchone()
			else:
				return cur.fetchall()
	
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			return False
	
	def _insert_del(self, query , values):
		try:
			cur = BotDatabase.__con.cursor()
			cur.execute(query, values) 
			result=BotDatabase.__con.commit()	
			return True
	
		except psycopg2.DatabaseError, e: 	
			if BotDatabase.__con:
				BotDatabase.__con.rollback()
			print(e)
			return False
						

import re
import time 

class BotTasks(BotDatabase):
	
	__instance 	= None
	__fifo 			= None

	def __init__(self):
		BotTasks.__instance = BotDatabase()
		BotTasks.__instance._connect()
		self.__readConfig()

	def __readConfig(self):
		try:
			config = ConfigParser.RawConfigParser()
			config.read('~/.bot.cfg')
			BotTasks.__fifo=config.get('Fifo','path')
		except:
			raise 'please check bot.cfg'

	def __prepareTime(self,timer):
		timer = str(timer)
		parsed = re.search('(^\d\d?\.\d\d?\.\d{4}\s+\d\d?:\d\d$)', timer)
		if parsed:
			return (parsed.group(0), 0)
		parsed = re.search('(^\d\d?:\d\d$)', timer)
		if parsed:
			return (parsed.group(0), 1)
		if timer.isdigit():
			return (timer, 2)
		return False
	
	def taskScheduler(self):	
		BotTasks.__instance._select("SELECT command_exec FROM tasks "+
			"WHERE (exec_period = true and exec_second)" )	
	
	def getTaskById(self, task_id):
		return BotTasks.__instance._select("SELECT * FROM tasks WHERE tasks_id = %s", (task_id,), False)
		
	def delTask(self,task_id):
		return BotTasks.__instance._insert_del("DELETE FROM tasks WHERE tasks_id = %s", (task_id,))

	def addTimer(self, member_id ,exec_command , timer, period=True):
		if self.__prepareTime(timer):
			a , b = self.__prepareTime(timer)
			if b == 0:
				return BotTasks.__instance._insert_del("INSERT INTO tasks (members_id,exec_command,exec_time) "+
					" VALUES (%s,%s,%s::timestamptz)", (member_id,exec_command, a))
			elif b == 1:
				a = time.strftime("%d.%m.%Y")+' '+a
				return BotTasks.__instance._insert_del("INSERT INTO tasks (members_id,exec_command,exec_time,exec_period) "+
					" VALUES (%s,%s,%s::timestamptz,%s)", (member_id,exec_command, a, period))
			elif b == 2:
				return BotTasks.__instance._insert_del("INSERT INTO tasks (members_id,exec_command, "+
					" exec_second,exec_period, exec_time) "+
					" VALUES (%s,%s,%s,%s,now())", (member_id,exec_command, a, period))
		return False
				

