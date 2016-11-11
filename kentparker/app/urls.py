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
    url(r'^profile/(?P<name>.*)$', views.profile),
    url(r'^get_photo/(?P<name>.*)$',views.get_photo,name='get_photo'),
    url(r'^edit_profile/(?P<name>.*)$', views.edit_profile, name='edit_profile'),
    url(r'^change_password/(?P<name>.*)$', views.change_password, name='change_password'),
    url(r'^favorite/(?P<name>.*)$',views.favorite, name='favorite'),
    url(r'^confirm_registration/(?P<name>.*)/(?P<token>.*)$',views.confirm_registration,name='confirm_registration'),
    url(r'^request_reset_password$',views.request_reset_password,name='request_reset_password'),
    url(r'^reset_password/(?P<name>.*)/(?P<token>.*)$',views.reset_password,name='reset_password'),
    # newsmaker
    url(r'^create_pitch$', views.create_pitch, name='create_pitch'),
    url(r'^manage_pitch$', views.manage_pitch, name='manage_pitch'),
    url(r'^show_drafts$',views.show_drafts,name='show_drafts'),
    url(r'^edit_pitch/(?P<pitch_id>.*)$', views.edit_pitch, name='edit_pitch'),
    url(r'^draft_pitch$', views.draft_pitch, name='draft_pitch'),
    url(r'^show_pitches$', views.show_pitches, name='show_pitches'),
    url(r'^journalist/(?P<tags>.*)$', views.filter_pitch, name='filter_pitch'),
]
