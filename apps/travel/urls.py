from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.reg),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add),
    url(r'^travels/addproc$', views.addproc),
    url(r'^travels/destination/(?P<id>\d+)$', views.destinationshow),
    url(r'^travels/destination/join/(?P<id>\d+)$', views.join),
    
    
    
    

]