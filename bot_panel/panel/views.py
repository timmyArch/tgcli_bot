# -*- coding: utf-8 -*-

from django.shortcuts import *
from django.contrib import messages
from django.views.generic import TemplateView
from django.template.context import RequestContext
from django.contrib import messages

import sys

sys.path.append('/root/tgcli_bot/')
sys.path.append('/root/tgcli_bot/bot_panel/panel/templates/')

from db import BotDatabase
from db import BotTasks

import string
import random

class Tasks():
	
	def list(self, request):
		if 'verified' in request.session and request.session['verified']:
			a = BotDatabase()
			tasks = a.select("SELECT * FROM tasks WHERE members_id = %s",(request.session['user_id'],), False)
			return render_to_response("tasks.html", dict(tasks=tasks), context_instance=RequestContext(request))
		return redirect('/auth/login')
	
	def show(self, request, task):	
		if 'verified' in request.session and request.session['verified']:
			a = BotTasks()
			tasks = a.getTaskById(task)
			return render_to_response("task.html", dict(task=tasks, info=True), context_instance=RequestContext(request))	
		return redirect('/auth/login')

	def add(self, request):
		if 'verified' in request.session and request.session['verified']:
			a = BotTasks()
			if request.method == 'POST':
				if request.POST['exec_command'] in a.getMemberCommandsByMemberId(request.session['user_id']):
					if request.POST['exec_time'] != '':
						timer = request.POST['exec_time']
					elif request.POST['exec_second'] != '':
						timer = request.POST['exec_second']
					else:
						return redirect('/tasks/add')
					a.addTimer(
						request.session['user_id'],
						request.POST['exec_command']+" "+request.POST['exec_params'],
						timer,
						(False,True)[bool(request.POST['exec_period'])]
					)
					return render_to_response("tasks.html", dict(task_added=True), context_instance=RequestContext(request))	
				else:
					return redirect('/tasks/list')
			commands = a.getMemberCommandsByMemberId(request.session['user_id'])
			if not commands:
				messages.add_message(request, messages.INFO, 'Es stehen noch keine Kommandos bereit.')
			return render_to_response("task.html", dict(commands=commands), context_instance=RequestContext(request))	
		return redirect('/auth/login')
	
class Commands():

	def list(self,request):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			commands = a.select("SELECT * FROM commands", False, False)
			return render_to_response("commands.html", dict(commands=commands), context_instance=RequestContext(request))	
		return redirect('/auth/login')
	
	def remove(self,request,command_id):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			user = a.removeCommand(str(command_id))
			if user: 
				messages.add_message(request, messages.SUCCESS, 'Das Kommando wurde entfernt.')
			else:
				messages.add_message(request, messages.SUCCESS, 'Das Kommando wurde nicht entfernt.')
		return redirect('/commands/list')

	def add(self,request):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			if request.method == 'POST':
				if a.addCommand((request.POST['name'], request.POST['hint'], request.POST['description'])):
					msg = 'Das Kommando wurder erfolgreich angelegt.'
					messages.add_message(request, messages.SUCCESS, msg)
				else:
					messages.add_message(request, messages.ERROR, 'Fehler beim Anlegen des Kommandos')
				return redirect('/commands/list')
			return render_to_response("command.html", 
				dict(commands=a.getCommands()), context_instance=RequestContext(request))	
		return redirect('/auth/login')

class User():
	
	def list(self,request):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			users = a.getMembers()
			return render_to_response("users.html", dict(users=users), context_instance=RequestContext(request))	
		return redirect('/auth/login')
	
	def show(self,request,user_id):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			user = a.getMemberById(user_id)
			if user:
				user=user[0]
			else:
				messages.add_message(request, messages.ERROR, 'Es konnte ein Benutzer gefunden werden.')
				return redirect('/users/list')
			allCommands=list()
			commands = a.getMemberCommandsByMemberId(user_id)
			buf=list(a.getCommands())
			if commands:
				for i, command in enumerate(buf):
					if command and not command[0] in commands:
						allCommands.append(command[0])
			else:
				allCommands=buf
			return render_to_response("user.html", 
				dict(commands=commands,allCommands=allCommands,info=True,user_id=user_id,username=user[2],number=user[1]), 
					context_instance=RequestContext(request))	
		return redirect('/auth/login')

	def remove(self,request,user_id):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			user = a.removeMember(str(user_id))
			if user: 
				messages.add_message(request, messages.SUCCESS, 'Der Nutzer wurde entfernt.')
			else:
				messages.add_message(request, messages.SUCCESS, 'Der Nutzer wurde nicht entfernt.')
		return redirect('/users/list')

	def add(self,request):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			if request.method == 'POST':
				if a.addMember((request.POST['number'], request.POST['member'])):
					if 'exec_command' in request.POST:
						dic = dict(request.POST.lists())
						for i in dic['exec_command']:
							a.addMemberCommandByMemberName(request.POST['member'],i)
					msg = 'Der Benutzer wurder erfolgreich angelegt.'
					messages.add_message(request, messages.SUCCESS, msg)
					return redirect('/users/list')
				else:
					messages.add_message(request, messages.ERROR, 'Fehler beim Anlegen des Nutzers')
					return redirect('/users/list')
			commands = a.getCommands()
			if not commands:
				messages.add_message(request, messages.ERROR, 'Es konnten keine Kommandos gefunden werden.')
				return redirect('/users/list')
			y = list()
			for x in commands:
				y.append(x[0])
			return render_to_response("user.html", 
				dict(commands=y), context_instance=RequestContext(request))	
		return redirect('/auth/login')
	
	def addCommand(self,request,user_id,command):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			msg = 'Das Kommando wurde '+('nicht ','')[a.addMemberCommandByMemberId(user_id,command)]+'hinzugefuegt'
			messages.add_message(request, messages.INFO, msg)
			return redirect('/users/'+str(user_id))
		return redirect('/auth/login')
			
	def delCommand(self,request,user_id,command):
		if 'verified' in request.session and request.session['verified'] and request.session['is_admin']:
			a = BotTasks()
			msg = 'Das Kommando wurde '+('nicht ','')[a.removeMemberCommandByCommand(user_id,command)]+'entfernt'
			messages.add_message(request, messages.INFO, msg)
			return redirect('/users/'+str(user_id))
		return redirect('/auth/login')

class Auth():

	def login(self,request):
		if 'verified' in request.session and request.session["verified"]:
			return render_to_response("overview.html", dict(verified=request.session["verified"]),
				context_instance=RequestContext(request))
		if request.method == 'POST':
			a = BotDatabase()
			member = a.select("SELECT members_id,name FROM members WHERE name = %s", 
				(request.POST["username"],), False)
			if type(member) is list and len(member) == 1:
				member=member[0]
			if len(member) == 2:
				token = ''.join([random.choice(string.ascii_letters+string.digits+'_-') for _ in range(10)])
				a._insert_del("INSERT INTO members_auth (members_id,token) "+
					"VALUES (%s,%s) ", (member[0],token))
				f = open('/tmp/luabot.tmp', 'a+')
				f.write(str(member[1])+", Dein Token: "+token+"\n")
				f.close()
				request.session["username"] = request.POST["username"]
				request.session["user_id"] = member[0]
				request.session["is_admin"] = (False,True)[bool(request.POST['username'] in a.getAdmins())]
				return render_to_response("login.html", 
					dict(member=request.POST["username"], verify=True),
					context_instance=RequestContext(request))
		return render_to_response("login.html", dict(fail=True), 
			context_instance=RequestContext(request))

	def verify(self,request):
		if 'verified' in request.session and request.session["verified"]:
			return render_to_response("overview.html", dict(),
				context_instance=RequestContext(request))
		if request.method == 'POST' and request.session["username"] and request.session["user_id"]:
			a = BotDatabase()
			result = a.select("SELECT 1 FROM members_auth WHERE members_id = %s and"+
				" created_at <= now() and expired_at >= now() and token = %s " +
				" order by members_auth_id desc limit 1",
				(request.session["user_id"] , request.POST['token']) ,True)
			request.session["verified"] = (False,True)[bool(result)]
			if result:
				return render_to_response("overview.html", dict(),
      		context_instance=RequestContext(request))
			return render_to_response("login.html", dict(),
      	context_instance=RequestContext(request))
		else:
			return render_to_response("login.html", dict(fail=True),
      	context_instance=RequestContext(request))
	
	def logout(self, request):
		request.session["verified"] = False
		request.session["username"] = False
		request.session["user_id"] = False
		request.session["is_admin"] = False
		return render_to_response("login.html", dict(fail=True),
			context_instance=RequestContext(request))	

			
			
