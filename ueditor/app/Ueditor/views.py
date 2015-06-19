# coding:utf-8
'''
Created on 2012-8-29
@author: Administrator
'''
server_address = "http://www.funpeach.com:8001"
from ueditor import settings

from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
import Image
import base64
import os
import time
import urllib2
import uuid
from ueditor.app.ECommunity.models import Article, Channel, Customer, AppSeting
import datetime
import json
from django.contrib.auth import *

from django.contrib.auth.decorators import login_required

@login_required
def testueditor(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('editor.html', context, context_instance=RequestContext(request))


def __myuploadfile(fileObj, source_pictitle, source_filename, fileorpic='pic'):
    """ 一个公用的上传文件的处理 """
    myresponse = ""
    if fileObj:
        filename = fileObj.name.decode('utf-8', 'ignore')
        fileExt = filename.split('.')[1]
        file_name = str(uuid.uuid1())
        subfolder = time.strftime("%Y%m")
        if not os.path.exists(settings.MEDIA_ROOT[0] + subfolder):
            os.makedirs(settings.MEDIA_ROOT[0] + subfolder)
        path = str(subfolder + '/' + file_name + '.' + fileExt)

        if fileExt.lower() in (
        'jpg', 'jpeg', 'bmp', 'gif', 'png', "rar", "doc", "docx", "zip", "pdf", "txt", "swf", "wmv"):

            phisypath = settings.MEDIA_ROOT[0] + path
            destination = open(phisypath, 'wb+')
            for chunk in fileObj.chunks():
                destination.write(chunk)
            destination.close()

            if fileorpic == 'pic':
                if fileExt.lower() in ('jpg', 'jpeg', 'bmp', 'gif', 'png'):
                    im = Image.open(phisypath)
                    im.thumbnail((720, 720))
                    im.save(phisypath)

            real_url = server_address +  '/static/upload/' + subfolder + '/' + file_name + '.' + fileExt
            myresponse = "{'original':'%s','url':'%s','title':'%s','state':'%s'}" % (
            source_filename, real_url, source_pictitle, 'SUCCESS')
    return myresponse


@csrf_exempt
def ueditor_ImgUp(request):
    """ 上传图片 """
    fileObj = request.FILES.get('upfile', None)
    source_pictitle = request.POST.get('pictitle', '')
    source_filename = request.POST.get('fileName', '')
    response = HttpResponse()
    myresponse = __myuploadfile(fileObj, source_pictitle, source_filename, 'pic')
    response.write(myresponse)
    return response


@csrf_exempt
def ueditor_FileUp(request):
    """ 上传文件 """
    fileObj = request.FILES.get('upfile', None)
    source_pictitle = request.POST.get('pictitle', '')
    source_filename = request.POST.get('fileName', '')
    response = HttpResponse()
    myresponse = __myuploadfile(fileObj, source_pictitle, source_filename, 'file')
    response.write(myresponse)
    return response


@csrf_exempt
def ueditor_ScrawUp(request):
    """ 涂鸦文件,处理 """
    print request
    param = request.POST.get("action", '')
    fileType = [".gif", ".png", ".jpg", ".jpeg", ".bmp"];

    if param == 'tmpImg':
        fileObj = request.FILES.get('upfile', None)
        source_pictitle = request.POST.get('pictitle', '')
        source_filename = request.POST.get('fileName', '')
        response = HttpResponse()
        myresponse = __myuploadfile(fileObj, source_pictitle, source_filename, 'pic')
        myresponsedict = dict(myresponse)
        url = myresponsedict.get('url', '')
        response.write("<script>parent.ue_callback('%s','%s')</script>" % (url, 'SUCCESS'))
        return response
    else:
        #========================base64上传的文件======================= 
        base64Data = request.POST.get('content', '')
        subfolder = time.strftime("%Y%m")
        if not os.path.exists(settings.MEDIA_ROOT[0] + subfolder):
            os.makedirs(settings.MEDIA_ROOT[0] + subfolder)
        file_name = str(uuid.uuid1())
        path = str(subfolder + '/' + file_name + '.' + 'png')
        phisypath = settings.MEDIA_ROOT[0] + path
        f = open(phisypath, 'wb+')
        f.write(base64.decodestring(base64Data))
        f.close()
        response = HttpResponse()
        response.write(
            "{'url':'%s',state:'%s'}" % ('/static/upload/' + subfolder + '/' + file_name + '.' + 'png', 'SUCCESS'));
        return response


@csrf_exempt
def ueditor_getRemoteImage(request):
    print request
    """ 把远程的图抓到本地,爬图 """
    file_name = str(uuid.uuid1())
    subfolder = time.strftime("%Y%m")
    if not os.path.exists(settings.MEDIA_ROOT[0] + subfolder):
        os.makedirs(settings.MEDIA_ROOT[0] + subfolder)
        #====get request params=================================
    urls = str(request.POST.get("upfile"));
    urllist = urls.split("ue_separate_ue")
    outlist = []
    #====request params end=================================    
    fileType = [".gif", ".png", ".jpg", ".jpeg", ".bmp"];
    for url in urllist:
        fileExt = ""
        for suffix in fileType:
            if url.endswith(suffix):
                fileExt = suffix
                break;
        if fileExt == '':
            continue
        else:
            path = str(subfolder + '/' + file_name + '.' + fileExt)
            phisypath = settings.MEDIA_ROOT[0] + path
            piccontent = urllib2.urlopen(url).read()
            picfile = open(phisypath, 'wb')
            picfile.write(piccontent)
            picfile.close()
            outlist.append( server_address+'/static/upload/' + subfolder + '/' + file_name + '.' + fileExt)
    outlist = "ue_separate_ue".join(outlist)

    response = HttpResponse()
    myresponse = "{'url':'%s','tip':'%s','srcUrl':'%s'}" % (outlist, '成功', urls)
    response.write(myresponse);
    return response


def listdir(path, filelist):
    """ 递归 得到所有图片文件信息 """
    phisypath = settings.MEDIA_ROOT[0]
    if os.path.isfile(path):
        return '[]'
    allFiles = os.listdir(path)
    retlist = []
    for cfile in allFiles:
        fileinfo = {}
        filepath = (path + os.path.sep + cfile).replace("\\", "/").replace('//', '/')

        if os.path.isdir(filepath):
            listdir(filepath, filelist)
        else:
            if cfile.endswith('.gif') or cfile.endswith('.png') or cfile.endswith('.jpg') or cfile.endswith('.bmp'):
                filelist.append(filepath.replace(phisypath, '/static/upload/').replace("//", "/"))


@csrf_exempt
def ueditor_imageManager(request):
    """ 图片在线管理  """
    filelist = []
    phisypath = settings.MEDIA_ROOT[0]
    listdir(phisypath, filelist)
    imgStr = "ue_separate_ue".join(filelist)
    response = HttpResponse()
    response.write(imgStr)
    return response


@csrf_exempt
def ueditor_getMovie(request):
    """ 获取视频数据的地址 """
    content = "";
    searchkey = request.POST.get("searchKey");
    videotype = request.POST.get("videoType");
    try:
        url = "http://api.tudou.com/v3/gw?method=item.search&appKey=myKey&format=json&kw=" + searchkey + "&pageNo=1&pageSize=20&channelId=" + videotype + "&inDays=7&media=v&sort=s";
        content = urllib2.urlopen(url).read()
    except Exception, e:
        pass
    response = HttpResponse()
    response.write(content);
    return response

@login_required
@csrf_exempt
def save(request):
    #保存文章
    if 'content' not in request.POST or 'title' not in request.POST or \
                    'image' not in request.POST:
        return HttpResponse(json.dumps({'status': 'fail'}))

    customer = Customer.objects.filter(user=request.user)[0]

    title = request.POST['title']
    desc = request.POST['desc']
    content = request.POST['content']
    text = request.POST['text']
    imagesrc = request.POST['image']
    time = datetime.datetime.now().date()
    channel = request.POST['channel']
    channel_object = Channel.objects.get(title=channel)
    article = Article.objects.create(author="",
                                     title=title,
                                     body=content,
                                     text=text,
                                     image=imagesrc,
                                     channel=channel_object,
                                     type="1",
                                     create_time=time,
                                     url="",
                                     desc= desc,
                                     day="1")
    article.url = 'http://www.funpeach.com/article.html?p=' + str(article.id)
    article.save()
    customer.articles.add(article)
    return HttpResponse(json.dumps({"status":"success"}))

@csrf_exempt
def app_imgUp(request):
    # APP首页图片上传
    fileObj = request.FILES.get('upfile', None)

    phone = request.POST.get('phone', '')
    password = request.POST.get('password', '')
    pictitle = "app" + "_pic"
    source_filename = "app" + "_pic"

    user = authenticate(username=phone, password=password)
    myresponse = __myuploadfile_2(fileObj, pictitle, source_filename, 'pic')
    st = AppSeting.objects.all()[0]
    st.image = myresponse['real_url']
    st.save()
    res = HttpResponse(json.dumps({"state":"success"}))
    res["Access-Control-Allow-Origin"] = "*" #todo 得防止一下
    return res


@csrf_exempt
def user_imgUp(request):
    """ 个人图片上传 """
    fileObj = request.FILES.get('upfile', None)

    phone = request.POST.get('phone', '')
    password = request.POST.get('password', '')
    pictitle = phone + "_pic"
    source_filename = phone + "_pic"

    user = authenticate(username=phone,password=password)

    if user is not None:
        customer = Customer.objects.get(user=user)
        myresponse = __myuploadfile_2(fileObj, pictitle, source_filename, 'pic')
        customer.icon = myresponse["real_url"]
        customer.save()

        return HttpResponse(json.dumps({"state":"success", "url":myresponse["real_url"] }))

    return HttpResponse(json.dumps({"state":"fail"}))


def __myuploadfile_2(fileObj, source_pictitle, source_filename, fileorpic='pic'):
    """ 一个公用的上传文件的处理 """
    myresponse = ""
    if fileObj:
        filename = fileObj.name.decode('utf-8', 'ignore')
        fileExt = filename.split('.')[1]
        file_name = str(uuid.uuid1())
        subfolder = time.strftime("%Y%m")
        if not os.path.exists(settings.MEDIA_ROOT[0] + subfolder):
            os.makedirs(settings.MEDIA_ROOT[0] + subfolder)
        path = str(subfolder + '/' + file_name + '.' + fileExt)

        if fileExt.lower() in (
        'jpg', 'jpeg', 'bmp', 'gif', 'png', "rar", "doc", "docx", "zip", "pdf", "txt", "swf", "wmv"):

            phisypath = settings.MEDIA_ROOT[0] + path
            destination = open(phisypath, 'wb+')
            for chunk in fileObj.chunks():
                destination.write(chunk)
            destination.close()

            if fileorpic == 'pic':
                if fileExt.lower() in ('jpg', 'jpeg', 'bmp', 'gif', 'png'):
                    im = Image.open(phisypath)
                    im.thumbnail((720, 720))
                    im.save(phisypath)

            real_url = server_address +  '/static/upload/' + subfolder + '/' + file_name + '.' + fileExt
            myresponse =  {
                "source_filename":source_filename, "real_url":real_url, "source_pictitle":source_pictitle,
                "state":'SUCCESS'
            }
    return myresponse
