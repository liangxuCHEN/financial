from django.conf.urls import patterns, include, url
from django.contrib import admin
from store import views

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'Financial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^item$',  views.item_index, name='item_index'),
    url(r'^item_creat$',  views.add_one_item, name='add_one_item'),
    url(r'^multitem_creat$',  views.add_multitems, name='add_multitems'),
    url(r'^admin/', include(admin.site.urls)),
)