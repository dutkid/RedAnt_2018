#coding:utf-8
from RedAnt.forms import teamForm,myUEditorModelForm,FileUploadForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from RedAnt.models import ProjectTeam,Blog,LearningResources
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
import DUSite
from bs4 import BeautifulSoup
import urllib.request
import json
import re
import datetime
import random

@permission_required('RedAnt.add_projectteam')
@login_required
def teamAdd(request):
    name = '未命名'
    introduction = '请添加项目简介'
    team = ProjectTeam.objects.create(TeamName=name,Introduction=introduction)
    team.ShortName = team.id
    team.save()
    blog = Blog.objects.get(id=0)
    blog.id = None
    blog.Team = team
    blog.save()
    url = '/teams/major='+ str(team.id) + '/edit/'
    return HttpResponseRedirect(url)

@login_required
def teamMajor(request,name):
    try:
        team = ProjectTeam.objects.get(ShortName=name)
    except:
        return HttpResponse(u"项目组不存在")
    if request.method == 'POST':
        fileForm = FileUploadForm(request.POST, request.FILES)
        if fileForm.is_valid():
            file = LearningResources()
            file.Team = ProjectTeam.objects.get(ShortName=name)
            file.teamName = name
            file.fileField = fileForm.cleaned_data['file']
            file.name = file.fileField.name
            file.save()
        url = request.get_full_path()
        return HttpResponseRedirect(url)
    else:
        blogs = Blog.objects.filter(Team=team).order_by('-modify_time')
        teams = ProjectTeam.objects.all()
        fileForm = FileUploadForm()
        resourseList = LearningResources.objects.filter(Team=team).order_by('-date')
        return render(request, 'projectTeam.html', {'team': team,'teams': teams,
                                                    'blogs': blogs,'fileForm': fileForm,'resourseList':resourseList})

@permission_required('RedAnt.change_projectteam')
@login_required
def edit(request,name):
    if request.method == 'POST':
        form = teamForm(request.POST)
        if form.is_valid():
            try:
                team = ProjectTeam.objects.get(ShortName=name)
            except:
                team  =ProjectTeam.objects.get(id=int(name))
            blogs = Blog.objects.filter(Team=team)
            newTeam = form.save()
            for blog in blogs:
                blog.Team = newTeam
                blog.save()
            team.delete()
            url = '/teams/major=' + newTeam.ShortName + '/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(u"数据校验错误")
    else:
        try:
            team = ProjectTeam.objects.get(ShortName=name)
        except:
            team = ProjectTeam.objects.get(id=int(name))
        editor = teamForm(instance=team)
        teams = ProjectTeam.objects.all()
        return render(request, 'teamEdit.html', {'team': team,'teams': teams, 'editor': editor})

@permission_required('RedAnt.delete_projectteam')
@login_required
def delete(request, name):
    ProjectTeam.objects.get(ShortName=name).delete()
    url = '/index/'
    return HttpResponseRedirect(url)

@permission_required('RedAnt.change_blog')
@login_required
def editBlog(request, name, article):
    if article == 'new':
        blog = Blog()
        blog.Team = ProjectTeam.objects.get(ShortName=name)
        blog.save()
        url = '/teams/major=' + name + '/article='+str(blog.id)+'/'
        return HttpResponseRedirect(url)
    else:
        if request.method == 'POST':
            form = myUEditorModelForm(request.POST)
            Blog.objects.get(id=article).delete()
            if form.is_valid():
                blog = form.save()
                blog.Team = ProjectTeam.objects.get(ShortName=name)
                blog = transform(blog)
                blog.save()
                url = '/teams/major=' + name +'/'
                return HttpResponseRedirect(url)
            else:
                return HttpResponse(u"数据校验错误")
        else:
            article = Blog.objects.get(id=article)
            form = myUEditorModelForm(instance=article)
            teams = ProjectTeam.objects.all()
            return render(request, 'editBlog.html', {'form': form,'teams': teams})

@permission_required('RedAnt.delete_blog')
@login_required
def deleteBlog(request, name, article):
    Blog.objects.get(id=article).delete()
    url = '/teams/major=' + name + '/'
    return HttpResponseRedirect(url)

@permission_required('RedAnt.delete_learningresoures')
@login_required
def deleteResource(request, name, file):
    LearningResources.objects.get(fileField=file).delete()
    url = '/teams/major=' + name + '/'
    return HttpResponseRedirect(url)

def transform(blog):
    try:
        key = blog.Content
        soup = BeautifulSoup(key, "html5lib")
        blog.ImagePath = soup.img.get('src')
    except:
        blog.ImagePath = '/static/images/LOGO1.png'
    return blog
