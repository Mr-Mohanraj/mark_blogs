from django.shortcuts import render, redirect
from .models import Post, User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import logout

def home(request):
    name = "mohanraj"
    return render(request, 'blog/home.html', {"name":name})

def blog_list(request):
    post = Post.objects.all()
    return render(request, 'blog/blog_list.html', {"posts":post})

def blog_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return render(request, 'blog/404.html', {"error":ObjectDoesNotExist})
    
    return render(request, 'blog/blog_detail.html', {"post":post})

def blog_edit(request, pk):
    if request.method == 'POST':
        try:
            post = Post.objects.get(pk=pk)
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.save()
            return render(request, 'blog/blog_detail.html', {"post":post})
        except ObjectDoesNotExist:
            return render(request, 'blog/404.html', {"error":ObjectDoesNotExist})
    else:
        try:
            post = Post.objects.get(pk=pk)
            return render(request, 'blog/blog_edit.html', {"post":post})
        except ObjectDoesNotExist:
            return render(request, 'blog/404.html', {"error":ObjectDoesNotExist})

def blog_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        return render(request, 'blog/blog_delete.html', {"post":post, "msg":"post successfully delete"})
    except ObjectDoesNotExist:
        return redirect('blog:blog_list')


def blog_add(request, username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            title = request.POST['title']
            body = request.POST['body']
            post = Post(title=title, body=body, author=user)
            post.save()
            return render(request, 'blog/blog_detail.html', {"post":post})
        except ObjectDoesNotExist:
            return render(request, 'blog/404.html', {"error":ObjectDoesNotExist})
    else:
        return render(request,"blog/blog_new.html",)


def signup_user(request):
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        email = request.POST['email']
        
        if username and not None:
            username = username
            
        if email and not None:
            email = email
        
        if (password and password_confirm) and password == password_confirm:
            password = password
        
        user = User.objects.create_user(username=username, email=email, password=password)
        if User.objects.filter(username=username).first() == username:
            messages.error(request, "Username is already taken.")
        
        if User.objects.filter(email=email).first() == email:
            messages.error(request, "Email id already taken")
        
        user.save()
        return render(request, 'blog/login_form.html', {"user":user})
    else:
        return render(request, 'blog/signup_form.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.username == username:
                messages.info(request, "username is correct")
                if user.password == password:
                    messages.info(request, "password is correct")
                    user.is_staff = False
                    user.is_superuser = False
                    user.is_login = True
                    user.save()
                    return redirect('blog:home.html', {"user":user, "msg":"successfully login"})
                return render(request, 'blog/404.html', {"error":[username, password]})
        except Exception as e:
            return render(request, 'blog/404.html', {"error":e})
    else:
        return render(request, 'blog/login_form.html')


def logout_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.is_login = False
        user.save()
        messages.success(request, f"successfully logout {user.username}")
        return redirect('blog:home')
    except ObjectDoesNotExist:
        return render(request, 'blog/404.html', {"error":ObjectDoesNotExist})

# def blog_update(request, pk):
#     if request.method == 'POST':
#         try:
#             post = Post.objects.get(pk=pk)
#             post.title = request.POST['title']
#             post.body = request.POST['body']
#             post.save()
#         except ObjectDoesNotExist:
#             return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})
#         return render(request, 'blog/blog_detail.html', {"post":post})
#     else:
#         return render(request, 'blog/blog_update.html')

    # if request.method == 'POST':
    #     try:
    #         title = request.POST['title']
    #         body = request.POST['body']
    #         post = Post(title=title, body=body, author=User)
    #         post.save()
    #         return render(request, 'blog/blog_detail.html', {"post":post})
    #     except Exception as e:
    #         return render(request, 'blog/404.html', {"error":e})
    # else:
    #     return render(request,"blog/blog_new.html", {"error":"Unable to create a new post try again! "})
