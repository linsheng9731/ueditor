# coding:utf8 #
__author__ = 'damon_lin'

from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Channel(models.Model):
    # 标题 #
    title = models.CharField(u'标题', max_length=100)
    # 正文 #
    content = models.CharField(u'正文', max_length=300)
    # 缩略图 #
    image = models.CharField(u'缩略图', max_length=300)
    # 一级目录的顺序 #
    cata = models.CharField(u'一级目录顺序', max_length=100)
    # 表示二级目录的顺序 #
    num = models.CharField(u'二级目录顺序', max_length=100)
    # 描述 #
    desc = models.TextField(u'描述')
    # 表示是一级还是二级 #
    type = models.CharField(u'0 表示一级目录，1 表示二级目录', max_length=100)

    def __unicode__(self):
        return u"%s" % (self.title)


# 文章
class Article(models.Model):
    # Article_ID

    author = models.CharField(u'作者', max_length=100)

    title = models.CharField(u'标题', max_length=100)

    body = models.TextField(u'正文')

    text = models.TextField(u'纯文本', default='')

    image = models.CharField(u'标题图', max_length=100)

    # which channel the article belong to #
    channel = models.ForeignKey(Channel, verbose_name=u'频道')

    type = models.TextField(u'类型')

    create_time = models.CharField(u'创建时间', max_length=100)

    url = models.CharField(u'分享地址', max_length=300, default=None)

    desc = models.TextField(u'描述', default="")

    day = models.CharField(u'分页哟怒', max_length=100, default=1)

    def __unicode__(self):
        return u"%s" % (self.title)


# 用户
class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户权限', default=1)

    phone = models.CharField(u'电话号码', max_length=100)

    nickname = models.CharField(u'昵称', max_length=300)

    sex = models.CharField(u'性别', max_length=100)

    icon = models.CharField(u'头像', max_length=300)

    grade = models.CharField(u'积分', max_length=100)

    channels = models.ManyToManyField(Channel, verbose_name='channel')

    articles = models.ManyToManyField(Article, verbose_name='article')

    type = models.CharField('类型',max_length=300,default="C")

    def __unicode__(self):
        return u"phone:%s nickname:%s " % (self.phone,self.nickname)

class Collection(models.Model):
    # 标题 #
    title = models.CharField(u'标题', max_length=100)
    # 缩略图 #
    image = models.CharField(u'缩略图', max_length=300)
    # 描述 #
    desc = models.TextField(u'描述')
    # 创建时间 #
    create_time = models.CharField(u'创建时间', max_length=100)
    # 文章 #
    articles = models.ManyToManyField(Article, verbose_name=u'article')
    # 编辑 #
    author = models.ManyToManyField(Customer,verbose_name=u"authors")

    def __unicode__(self):
        return u"%s" % (self.title)

class Comment(models.Model):
    # 评论的用户 #
    customer = models.ForeignKey(Customer)
    # 评论的内容 #
    content = models.TextField()
    # 评论的文章 #
    article = models.ForeignKey(Article)



# #频道
# class Channel(models.Model):
#
#     #Channel_ID = models.CharField(max_length=100)
#
#     Channel_Name = models.CharField(max_length=100)
#
#     Type_ID = models.CharField(max_length=100)
#
#     Channel_Num = models.CharField(max_length=100)
#
#     Channel_Cata = models.CharField(max_length=100)
#
#     Channel_Desc = models.CharField(max_length=100)
#
#     Channel_PicURL = models.CharField(max_length=100)



