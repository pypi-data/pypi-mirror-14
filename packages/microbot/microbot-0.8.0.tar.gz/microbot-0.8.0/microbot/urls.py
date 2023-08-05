from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from microbot import views

urlpatterns = [
    url(r'^telegrambot/(?P<token>[-_:a-zA-Z0-9]+)/$', csrf_exempt(views.WebhookView.as_view()), name='telegrambot'),
    url(r'^hook/(?P<key>\w+)/$', csrf_exempt(views.HookView.as_view()), name='hook'),
    url(r'^api/bots/$', views.BotList.as_view(), name='bot-list'),
    url(r'^api/bots/(?P<pk>[0-9]+)/$', views.BotDetail.as_view(), name='bot-detail'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/env/$', views.EnvironmentVarList.as_view(), name='env-list'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/env/(?P<pk>[0-9]+)/$', views.EnvironmentVarDetail.as_view(), name='env-list'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/handlers/$', views.HandlerList.as_view(), name='handler-list'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/handlers/(?P<pk>[0-9]+)/$', views.HandlerDetail.as_view(), name='handler-detail'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/handlers/(?P<pk>[0-9]+)/urlparams/$', views.UrlParameterList.as_view(), name='handler-urlparameter-list'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/handlers/(?P<handler_pk>[0-9]+)/urlparams/(?P<pk>[0-9]+)/$', views.UrlParameterDetail.as_view(), 
        name='handler-urlparameter-detail'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/handlers/(?P<pk>[0-9]+)/headerparams/$', views.HeaderParameterList.as_view(), name='handler-headerparameter-list'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/handlers/(?P<handler_pk>[0-9]+)/headerparams/(?P<pk>[0-9]+)/$', views.HeaderParameterDetail.as_view(), 
        name='handler-headerparameter-detail'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/hooks/$', views.HookList.as_view(), name='hook-list'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/hooks/(?P<pk>[0-9]+)/$', views.HookDetail.as_view(), name='hook-detail'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/hooks/(?P<pk>[0-9]+)/recipients/$', views.RecipientList.as_view(), name='hook-recipient-list'),
    url(r'^api/bots/(?P<bot_pk>[0-9]+)/hooks/(?P<hook_pk>[0-9]+)/recipients/(?P<pk>[0-9]+)/$', views.RecipientDetail.as_view(), name='hook-recipient-list'),
    
]
