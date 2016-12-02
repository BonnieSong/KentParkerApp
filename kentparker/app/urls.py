from django.conf.urls import url
from . import views

import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^kentparker$',views.home),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^register_newsmaker$', views.register_newsmaker, name='register_newsmaker'),
    url(r'^register_journalist$', views.register_journalist, name='register_journalist'),
    url(r'^register_mediaoutlet$', views.register_mediaoutlet, name='register_mediaoutlet'),
    url(r'^login_google/(?P<email>.*)$', views.login_google, name='login_google'),
    url(r'^login_facebook/(?P<userid>.*)$', views.login_facebook, name='login_facebook'),
    url(r'^profile/(?P<name>.*)$', views.profile,name='profile'),
    url(r'^get_photo/(?P<name>.*)$',views.get_photo,name='get_photo'),
    url(r'^edit_profile/(?P<name>.*)$', views.edit_profile, name='edit_profile'),
    url(r'^change_password/(?P<name>.*)$', views.change_password, name='change_password'),
    url(r'^favorite/(?P<name>.*)$',views.favorite, name='favorite'),
    url(r'^confirm_registration/(?P<name>.*)/(?P<token>.*)$',views.confirm_registration,name='confirm_registration'),
    url(r'^request_reset_password$',views.request_reset_password,name='request_reset_password'),
    url(r'^reset_password/(?P<name>.*)/(?P<token>.*)$',views.reset_password,name='reset_password'),
    # newsmaker related urls
    url(r'^create_pitch$', views.create_pitch, name='create_pitch'),
    url(r'^manage_pitch$', views.manage_pitch, name='manage_pitch'),
    url(r'^contacts$', views.contacts, name='contacts'),
    # media_outlet
    url(r'^manage_journalists$', views.manage_journalists, name='manage_journalists'),
    url(r'^mediaoutlet_articles', views.mediaoutlet_articles, name='mediaoutlet_articles'),
    # journalist related urls
    url(r'^journalist/favNewsMakers$', views.favNewsMakers_pitch, name='favNewsMakers_pitch'),
    url(r'^bookmarked_pitch', views.bookmarked_pitch, name='bookmarked_pitch'),
    url(r'^embargo_pitch', views.embargo_pitch, name='embargo_pitch'),
    url(r'^journalist/(?P<tags>.*)$', views.filterTags_pitch, name='filterTags_pitch'),
    url(r'^journalist_Articles', views.journalist_Articles, name='journalist_Articles'),
    # pitch related urls
    url(r'^pitch_detail/(?P<pitchId>.*)$', views.pitch_detail, name='pitch_detail'),
    url(r'^create_article$', views.create_article, name='create_article'),
    # article related urls
    url(r'^article_detail/(?P<articleId>.*)$', views.article_detail, name='article_detail'),
]
