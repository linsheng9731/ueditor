# coding:utf8 #
__author__ = 'damon_lin'

from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Channel(models.Model):
    # 标题 #
    title = models.CharField('标题', max_length=100)
    # 正文 #
    content = models.CharField('正文', max_length=300)
    # 缩略图 #
    image = models.CharField('缩略图', max_length=300)
    # 一级目录的顺序 #
    cata = models.CharField('一级目录顺序', max_length=100)
    # 表示二级目录的顺序 #
    num = models.CharField('二级目录顺序', max_length=100)
    # 描述 #
    desc = models.TextField('描述')
    # 表示是一级还是二级 #
    type = models.CharField('0 表示一级目录，1 表示二级目录', max_length=100)

    def __unicode__(self):
        return u"%s" % (self.title)


# 文章
class Article(models.Model):
    # Article_ID

    author = models.CharField('作者', max_length=100)

    title = models.CharField('标题', max_length=100)

    body = models.TextField('正文')

    text = models.TextField('纯文本', default='')

    image = models.CharField('标题图', max_length=100)

    # which channel the article belong to #
    channel = models.ForeignKey(Channel, verbose_name='频道')

    type = models.TextField('类型',default="A")

    create_time = models.CharField('创建时间', max_length=100)

    url = models.CharField('分享地址', max_length=300, default=None)

    desc = models.TextField('描述', default="")

    day = models.CharField('分页哟怒', max_length=100, default=1)

    read_times = models.IntegerField('阅读次数',default=0)

    def __unicode__(self):
        return u"%s" % (self.title)


# 用户
class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='用户权限', default=1)

    phone = models.CharField('电话号码', max_length=100)

    nickname = models.CharField('昵称', max_length=300)

    sex = models.CharField('性别', max_length=100)

    icon = models.CharField('头像', max_length=300)

    grade = models.CharField('积分', max_length=100)

    type = models.CharField('用户类型',max_length=100,default="C")

    channels = models.ManyToManyField(Channel, verbose_name='channel')

    articles = models.ManyToManyField(Article, verbose_name='article')

    def __unicode__(self):
        return u"phone:%s nickname:%s " % (self.phone, self.nickname)


class Collection(models.Model):
    # 标题 #
    title = models.CharField('标题', max_length=100)
    # 缩略图 #
    image = models.CharField('缩略图', max_length=300)
    # 描述 #
    desc = models.TextField('描述')
    # 类型 #
    type = models.CharField('类型',max_length=300,default="C")
    # 创建时间 #
    create_time = models.CharField('创建时间', max_length=100)
    # 文章 #
    articles = models.ManyToManyField(Article, verbose_name='article')
    # 编辑 #
    author = models.CharField(max_length=300,default="None")
    # 所属频道 #
    channel = models.ForeignKey(Channel, verbose_name="频道", default=1)

    def __unicode__(self):
        return u"%s" % (self.title)


class Comment(models.Model):
    # 评论的用户 #
    customer = models.ForeignKey(Customer)
    # 评论的内容 #
    content = models.TextField()
    # 评论的文章 #
    article = models.ForeignKey(Article)

class Search(models.Model):
    # 用户输入提炼的关键字
    keyword =  models.CharField(max_length=30)

    # 频率
    freq = models.IntegerField()

class AppSeting(models.Model):
    # app首页
    image = models.CharField("首页图片", max_length=100)

class Record(models.Model):
    # 用户 #
    customer = models.ForeignKey(Customer, default=4)
    # 时间戳 #
    timestamp = models.CharField(max_length=100)
    # 持续时间 #
    duration = models.CharField(max_length=400)

# #频道
# class Channel(models.Model):
#
# #Channel_ID = models.CharField(max_length=100)
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



