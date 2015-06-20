#coding=utf8
__author__ = 'abnerzheng'


from django.contrib.auth import *
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from ueditor.app.ECommunity.models import Customer,Article, Channel
import json
import uuid

def ser(model, param, serflag=True):  # model:待序列化的模型 param:待序列化的参数
        json_obj = []
        for item in model:  # 将特殊对象转化成普通map对象
            obj = {}
            for atr in param:
                # if(type(getattr(item,atr)) ==)
                obj[atr] = getattr(item, atr)
            json_obj.append(obj)  # 将普通map对象转化成json格式
        if serflag:
            return json.dumps(json_obj)  # 转化为json对象
        else:
            return json_obj

@login_required
def index(request):
    return render_to_response('index.html')



@login_required
def getArticles(request):
    user = request.user
    custome =  Customer.objects.filter(user=user)

    if custome and custome[0].type == "E":
        articles = custome[0].articles.all()
        p = Paginator(articles,10)
        page = int(request.GET.get("page", 1))
        ma = max(p.page_range)
        if 1<=page<=ma:
            page = page
        else:
            page = 1
        articles = p.page(page)
        articles_count = p.count
        return HttpResponse(json.dumps({'articles':ser(articles,['id','title'],False),
                                        'name':custome[0].nickname,
                                        'count':articles_count}))
    else:
        return HttpResponse(json.dumps({"state":"fail"}))


def getArticleInfo(request):
    articleId = request.GET['id']
    article = Article.objects.filter(id=articleId)
    if article:
        request.session['article_id'] = articleId
        serObj = ser(article,
            ['title','author','body','desc','image']
                                           ,False)[0]
        serObj['channel'] = article[0].channel.title
        return HttpResponse(json.dumps(serObj))
    else:

        return HttpResponse(json.dumps({"state":"fail"}))

def getChannels(request):
    channels = Channel.objects.filter(type=1).only('title')
    rt = [{'title': e.title} for e in channels]
    return HttpResponse(json.dumps(rt))

@csrf_exempt
def modify(request):
    id = request.POST["id"]
    if request.session['article_id'] != id:
        return HttpResponse(json.dumps({"state":"fail"}))
    else:
        if 'content' not in request.POST or 'title' not in request.POST or \
                    'image' not in request.POST:
            return HttpResponse(json.dumps({'status': 'fail'}))

        title = request.POST['title']
        desc = request.POST['desc']
        content = request.POST['content']
        imagesrc = request.POST['image']
        text = request.POST['text']
        channel = request.POST['channel']
        channel = Channel.objects.get(title=channel)

        article = Article.objects.get(id=id)
        article.desc = desc
        article.title= title
        article.body = content
        article.image = imagesrc
        article.channel = channel
        article.text = text

        article.save()

        return HttpResponse(json.dumps({"status":"success"}))


