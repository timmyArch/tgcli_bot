from django.shortcuts import render, render_to_response
from django.contrib import messages
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext

import sys

sys.path.append('/home/timmy/tgcli_bot/')
sys.path.append('/home/timmy/tgcli_bot/bot_panel/panel/templates/')

from db import BotDatabase
from db import BotTasks

import string
import random

class Auth(TemplateView):
	template_name="login.html"

	def login(self,request):
		if request.method == 'POST':
			a = BotDatabase()
			member = a.select("SELECT members_id,name FROM members WHERE name = %s", 
				(request.POST["username"],), False)
			if type(member) is list:
				member=member[0]
			if len(member) == 2:
				token = ''.join([random.choice(string.ascii_letters+string.digits+'_-') 
					for _ in range(10)])
				a._insert_del("INSERT INTO members_auth (members_id,token) "+
					"VALUES (%s,%s) ", (member[0],token))
				f = open('/tmp/luabot.tmp', 'a+')
				f.write(repr(member[1]+","+token+"\n"))
				f.close()
				request.session["username"] = request.POST["username"]
				request.session["user_id"] = member[0]
				return render_to_response("login.html", 
					dict(member=request.POST["username"], verify=True),
					context_instance=RequestContext(request))
		return render_to_response("login.html", dict(fail=True), 
			context_instance=RequestContext(request))

	def verify(self,request):
		if request.method == 'POST' and request.session["username"] and request.session["user_id"]:
			a = BotDatabase()
			result = a.select("SELECT 1 FROM members_auth WHERE members_id = %s and"+
				" now()  created_at <= now() and expired_at >= now() and token = %s " +
				" order by members_auth_id desc limit 1",
				(request.session["user_id"] , request.session["username"]) ,True)
			request.session["verified"] = (False,True)[bool(result)]
			return render_to_response("login.html", dict(verified=request.session["verified"]),
      	context_instance=RequestContext(request))
		else:
			return render_to_response("login.html", {},
      	context_instance=RequestContext(request))
	
	def logout(self, request):
		request.session["verified"] = False
		

			
			
