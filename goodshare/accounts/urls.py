from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('goodshare.accounts.views',
    # Examples:
    # url(r'^$', 'goodshare.views.home', name='home'),
    # url(r'^goodshare/', include('goodshare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login', 'login_account'),
    url(r'^logout', 'logout_account'),
    url(r'^register', 'register'),
    url(r'^p(?P<account_id>\d+)/$', 'profile'),
)
