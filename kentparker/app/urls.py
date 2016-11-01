from django.conf.urls import url
from . import views

import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^kentparker$',views.home),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^login_google/(?P<email>.*)$', views.login_google, name='login_google'),
    url(r'^login_facebook/(?P<userid>.*)$', views.login_facebook, name='login_facebook'),
    url(r'^publish_pitch$', views.publish_pitch, name='publish_pitch'),
]
