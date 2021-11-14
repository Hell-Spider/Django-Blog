import django
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse
from django import template
from django.template.defaultfilters import register, truncatewords, safe

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import *
from .forms import *

def userRegister(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account was created for " + form.cleaned_data.get('username'))
                return redirect('userLogin')
    context = {
        'form':form,
    }
    return render(request, 'Custom/register.html', context)

def userLogin(request):
    if request.user.is_authenticated:
            return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect!')
    context = {
        
    }
    return render(request, 'Custom/login.html', context)

def userLogout(request):
    logout(request)
    return redirect('home')

@register.filter
def body(value):
    return truncatewords(safe(value), 10)

def home(request):
    posts = Post.objects.all()
    posts_count = posts.count()
    pages = Paginator(posts, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = pages.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = pages.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = pages.page(pages.num_pages)
    current_user = request.user
    context = {
        'user' : current_user,
        'page_obj' : page_obj,
        'posts_count' : posts_count
    }
    return render(request, 'Custom/home.html', context)

@login_required(login_url='userLogin')
def create(request):
    update = False
    form = Postform()
    if request.method == "POST":
        form = Postform(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('home')
    context = {
        'form': form,
        'update': update
    }
    return render(request, 'Custom/create.html', context)

@login_required(login_url='userLogin')
def updatePost(request, pk):
    update = True
    post = Post.objects.get(id=pk)
    if request.user == post.author:
        form = Postform(instance=post)
        if request.method == "POST":
            form = Postform(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('user_post', request.user.id)
        context={
        'form':form,
        'update' : update
    }
    else:
        return redirect('home')
    return render(request, 'Custom/create.html', context)

@login_required(login_url='userLogin')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user == post.author:
        if request.method == "POST":
            post.delete()
            return redirect('user_post', request.user.id)
        context = {
            'item' : post,
        }
    else:
        return redirect('home')
    return render(request, 'Custom/delete.html', context)

@login_required(login_url='userLogin')
def detail_post(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post' : post,
    }
    return render(request, 'Custom/sample_post.html', context)

def sample_post(request):
    post = Post.objects.get(title='Sample Post')
    context = {
        'post' : post,
    }
    return render(request, 'Custom/sample_post.html', context)

@login_required(login_url='userLogin')
def user_post(request, pk):
    user = User.objects.get(id=pk)
    posts =user.post_set.all()
    posts_count = posts.count()
    pages = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = pages.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = pages.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = pages.page(pages.num_pages)
    current_user = request.user
    context = {
        'page_obj' : page_obj,
        'posts_count' : posts_count,
        'user' : user
    }
    return render(request, 'Custom/user_post.html', context)



