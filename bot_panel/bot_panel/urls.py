from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from panel.views import Auth

a = Auth()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bot_panel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
		#url(r'^auth/', Auth.as_view()),
		url(r'^auth/login', a.login),
		url(r'^auth/verify', a.verify),
)
