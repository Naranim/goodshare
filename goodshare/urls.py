from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goodshare.views.home', name='home'),
    # url(r'^goodshare/', include('goodshare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'goodshare.views.index'),
    url(r'^index', 'goodshare.views.index'),
    url(r'accounts/', include('goodshare.accounts.urls')),
    url(r'goods/', include('goodshare.goods.urls')),
)
