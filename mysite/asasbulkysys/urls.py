from django.conf.urls import patterns, url

from asasbulkysys import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   
   url(r'^jsondata/(?P<command_id>\w+)/$', views.dataloader, name='dataloader'),
   url(r'^jsonupdate/(?P<command_id>\w+)/$', views.dataupdate, name='dataupdate'),
   url('signup/', views.SignUp.as_view(), name='signup'),
   #url(r'^facebook/dataupdate/(?P<command_id>\w+)/$', views.dataupdate, name='dataupdate'),
   )

