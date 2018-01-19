from django.conf.urls import patterns, url

from asasbulkysys import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   
   url(r'^jsondata/(?P<command_id>\w+)/$', views.dataloader, name='dataloader'),
   #url(r'^facebook/dataupdate/(?P<command_id>\w+)/$', views.dataupdate, name='dataupdate'),
   )

