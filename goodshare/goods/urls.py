from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('goodshare.goods.views',
    # Examples:
    # url(r'^$', 'goodshare.views.home', name='home'),
    # url(r'^goodshare/', include('goodshare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^g(?P<good_id>\d+)/$', 'good'),
    url(r'^add_good/$', 'add_good'),
    url(r'^goods_search/$', 'good_list_search'),
    url(r'^add_to_account_(?P<good_id>\d+)_(?P<user_id>\d+)/$', 'add_good_to_user'),
)
