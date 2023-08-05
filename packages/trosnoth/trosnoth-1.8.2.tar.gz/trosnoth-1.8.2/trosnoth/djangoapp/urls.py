from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^u/?$', views.userList, name='userlist'),
    url(r'^u/(?P<userId>\d+)/?$', views.userProfile, name='profile'),
    url(
        r'^u/(?P<userId>\d+)/(?P<nick>[^/]+)/?$',
        views.userProfile, name='profile'),
    url(r'^g/?$', views.gameList, name='gamelist'),
    url(r'^g/(?P<gameId>\d+)/?$', views.viewGame, name='viewgame'),
)

