# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('ueditor.app.Ueditor',
    # Examples:
    url(r'^accounts/login', 'login.login_view'),
    url(r'^auth$', 'login.auth'),
    url(r'^unAuth', 'login.unAuth'),
    url(r'^getArticles', 'paperAdmin.getArticles'),
    url(r'^getChannels', 'paperAdmin.getChannels'),
    url(r'^modify', 'paperAdmin.modify'),
    url(r'^$', 'paperAdmin.index'),
    url(r'getArticleInfo', 'paperAdmin.getArticleInfo'),
    url(r'^editor$', 'views.testueditor'),
    url(r'^save','views.save'),
    url(r'^appImgUp','views.app_imgUp'),
    url(r'^user_imgUp$', 'views.user_imgUp'),
    url(r'^ueditor_imgup$','views.ueditor_ImgUp'),
    url(r'^ueditor_fileup$','views.ueditor_FileUp'),
    url(r'^ueditor_getRemoteImage$','views.ueditor_getRemoteImage'),
    url(r'^ueditor_scrawlUp$','views.ueditor_ScrawUp'),
    url(r'^ueditor_getMovie$','views.ueditor_getMovie'),
    url(r'^ueditor_imageManager$','views.ueditor_imageManager'),
)