from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post
from authentication.models import User
from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .utils import _checker

def blog_list(request):
    post = Post.objects.all()
    return render(request, 'article/blog_list.html', {"posts": post})


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        result = _checker(request.POST)
        if result == "like":
            obj = add_likes(request, post.id)
        elif result == "dislike":
            obj = add_dislikes(request, post.id)
        elif result == "Error":
            print("Something is wrong")
        return render(request, 'article/blog_detail.html', {"post": post, "instance": obj})
    else:
        return render(request, 'article/blog_detail.html', {"post": post, "instance": post})



def blog_edit(request, pk):
    if request.method == 'POST':
        try:
            post = Post.objects.get(pk=pk)
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.save()
            return render(request, 'article/blog_detail.html', {"post": post})
        except ObjectDoesNotExist:
            return render(request, '404.html', {"error": ObjectDoesNotExist})
    else:
        try:
            post = Post.objects.get(pk=pk)
            return render(request, 'article/blog_edit.html', {"post": post})
        except ObjectDoesNotExist:
            return render(request, '404.html', {"error": ObjectDoesNotExist})


def blog_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        messages.success(
            request, f"{post.title} was delete successfully! by {post.author.username}")
        post.delete()
        return redirect('pages:home')
    except ObjectDoesNotExist:
        return render(request, '404.html')


def blog_add(request, username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            title = request.POST['title']
            body = request.POST['body']
            post = Post(title=title, body=body, author=user)
            messages.success(request, f"post add successfully!")
            post.save()
            return redirect("article:blog_detail", pk=post.id)
        except ObjectDoesNotExist:
            return render(request, '404.html', {"error": ObjectDoesNotExist})
    else:
        return render(request, "article/blog_new.html",)

def user_blog(request, user_id):
    try:
        posts = get_list_or_404(Post, author=user_id)
        return render(request, 'article/blog_list.html', {"posts": posts})
    except Http404:
        messages.error(
            request, "There is no article now add it use the add new article button")
        return render(request, 'pages/home.html', {})


def add_dislikes(request, pk):
    like_obj = get_object_or_404(Post, pk=pk)
    user = request.user
    if not (str(user) == str(like_obj.author.username)):
        if user.is_authenticated:
            if user in like_obj.dislikes.all():
                like_obj.dislikes.remove(user)
                return like_obj
            else:
                like_obj.dislikes.add(user)
                return like_obj
        else:
            return like_obj
    else:
        messages.error("can't dislike your own post")
        return like_obj


def add_likes(request, pk):
    like_obj = get_object_or_404(Post, pk=pk)
    user = request.user
    if not (str(user.username) == str(like_obj.author.username)):
        if user.is_authenticated:
            if user in like_obj.likes.all():
                like_obj.likes.remove(user)
                return like_obj
            else:
                like_obj.likes.add(user)
                return like_obj
        else:
            return redirect("auth:login")
    else:
        messages.error("can't like your own post")
        return like_obj
