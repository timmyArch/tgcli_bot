from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from panel.views import *

a = Auth()
b = Tasks()
c = User()
d = Commands()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
		url(r'^auth/login', a.login),
		url(r'^auth/verify', a.verify),
		url(r'^auth/logout', a.logout),
		url(r'^tasks/list', b.list),
		url(r'^tasks/add', b.add),
		url(r'^tasks/(?P<task_id>\w+)/del$', b.remove),
		url(r'^tasks/(?P<task>\w+)/$', b.show),
		url(r'^users/list', c.list),
		url(r'^users/add', c.add),
		url(r'^users/(?P<user_id>\w+)/del/(?P<command>\w+)$', c.delCommand),
		url(r'^users/(?P<user_id>\w+)/add/(?P<command>\w+)$', c.addCommand),
		url(r'^users/(?P<user_id>\w+)/del$', c.remove),
		url(r'^users/(?P<user_id>\w+)/$', c.show),
		url(r'^commands/list', d.list),
		url(r'^commands/add', d.add),
		url(r'^commands/(?P<command_id>\w+)/del$', d.remove),
    url(r'^$', a.login),
)
