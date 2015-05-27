# coding:utf8 #
__author__ = 'damon_lin'

from django.db import models

class Channel(models.Model):
    # 标题 #
    title = models.CharField(max_length=100)
    # 正文 #
    content = models.CharField(max_length=300)
    # 缩略图 #
    image = models.CharField(max_length=300)
    # 一级目录的顺序 #
    cata = models.CharField(max_length=100)
    # 表示二级目录的顺序 #
    num = models.CharField(max_length=100)
    # 描述 #
    desc = models.TextField()
    # 表示是一级还是二级 #
    type = models.CharField(max_length=100)

#文章
class Article(models.Model):

    #Article_ID

    author = models.CharField(max_length=100)

    title = models.CharField(max_length=100)

    body = models.TextField()

    image = models.CharField(max_length=100)

    # which channel the article belong to #
    channel = models.ForeignKey(Channel)

    type = models.TextField()

    create_time = models.CharField(max_length=100)

    url = models.CharField(max_length=300,default=None)

    desc = models.TextField(default="")

    day = models.CharField(max_length=100,default=1)

#用户
class Customer(models.Model):

    phone = models.CharField(max_length=100)

    nickname = models.CharField(max_length=100)

    sex = models.CharField(max_length=100)

    icon = models.CharField(max_length=300)

    grade = models.CharField(max_length=100)

    channels = models.ManyToManyField(Channel)

    articles = models.ManyToManyField(Article)

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



