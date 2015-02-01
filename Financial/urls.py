from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from store import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    # url(r'^blog/', include('blog.urls')),
    url(r'^item$',  views.item_index, name='item_index'),
    url(r'^item_creat$',  views.add_one_item, name='add_one_item'),
    url(r'^multitem_creat$',  views.add_multitems, name='add_multitems'),
    url(r'^bill_table$',  views.bill_table_index, name='bill_table_index'),
    url(r'^bill_table_create$',  views.add_bill_table, name='add_bill_table'),
    url(r'^bill_table_detail/(?P<table_id>\d+)/$', views.bill_table_detail, name='bill_table_detail'),
    url(r'^edit_bill_table/(?P<table_id>\d+)/$', views.edit_bill_table, name='edit_bill_table'),
    url(r'^add_bill', views.add_bill, name='add_bill'),
    url(r'^delete_bill/(?P<bill_id>\d+)/(?P<table_id>\d+)/$', views.delete_bill, name='delete_bill'),
    url(r'^download_bill/(?P<table_id>\d+)/$', views.download_bill, name='download_bill'),
    url(r'^admin/', include(admin.site.urls)),
)
