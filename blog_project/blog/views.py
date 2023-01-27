from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post, User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http.response import Http404
import jwt


def home(request):
    res = HttpResponse(render(request, 'blog/home.html'))
    username = request.COOKIES.get('user', 'guest')
    print(username)
    if username == 'guest':
        return HttpResponse(render(request, 'blog/home.html', {"user": username}))
    else:
        print("welcome brother")
        user = User.objects.get(username=username)
        return HttpResponse(render(request, 'blog/home.html', {"user": user}))


def blog_list(request):
    post = Post.objects.all()
    username = request.COOKIES.get('user', 'guest')
    if username == 'guest':
        return render(request, 'blog/blog_list.html', {"posts": post})
    else:
        user = get_object_or_404(User, username=username)
        return render(request, 'blog/blog_list.html', {"posts": post, "user":user})


def blog_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        user = get_object_or_404(User, pk=pk)
    except ObjectDoesNotExist:
        return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})
    
    return render(request, 'blog/blog_detail.html', {"post": post, "user":user})


def blog_edit(request, pk):
    if request.method == 'POST':
        try:
            post = Post.objects.get(pk=pk)
            user = get_object_or_404(User,pk=pk)
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.save()
            return render(request, 'blog/blog_detail.html', {"post": post, "user":user})
        except ObjectDoesNotExist:
            return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})
    else:
        try:
            post = Post.objects.get(pk=pk)
            user = get_object_or_404(User, pk=pk)
            return render(request, 'blog/blog_edit.html', {"post": post, "user":user})
        except ObjectDoesNotExist:
            return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})


def blog_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('blog:blog_list')
    except ObjectDoesNotExist:
        return redirect('blog/404.html')


def blog_add(request, username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            title = request.POST['title']
            body = request.POST['body']
            post = Post(title=title, body=body, author=user)
            post.save()
            return render(request, 'blog/blog_detail.html', {"post": post, 'user':user})
        except ObjectDoesNotExist:
            return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})
    else:
        return render(request, "blog/blog_new.html",)


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

        # user = User.objects.create(
        #     username=username, email=email, password=password)
        
        # if User.objects.filter(username=username).first() == username:
        #     messages.error(request, "Username is already taken.")
        #     return redirect("blog:signup")

        # if User.objects.filter(email=email).first() == email:
        #     messages.error(request, "Email id already taken")
        #     return redirect("blog:signup")

        # user.save()
        send_activation_code(username)
        return render(request, 'blog/account_activation.html', {"user":True})
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
                if user.check_password(password):
                    messages.info(request, "password is correct")
                    user.is_login = True
                    user.save()
                    res = HttpResponse(
                        render(request, 'blog/home.html', {"user": user}))
                    res.set_cookie('user', user.username)
                    return res
                return render(request, 'blog/404.html', {"error": [username, password]})
        except Exception as e:
            return render(request, 'blog/404.html', {"error": e})
    else:
        return render(request, 'blog/login_form.html')


def logout_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.is_login = False
        user.save()
        messages.success(request, f"successfully logout {user.username}")
        res = HttpResponse(render(request, 'blog/logout.html', {"user": user}))
        res.delete_cookie('user')
        return res
    except ObjectDoesNotExist:
        return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})


def user_blog(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        posts = get_list_or_404(Post, author=user_id)
        return render(request, 'blog/blog_list.html', {"posts": posts, "user":user})
    except Http404:
        messages.error(request, "There is no blog now add it")
        return render(request, 'blog/home.html',{"user":user})


def upload_blog(request, user_id):
    title = request.POST['title']
    body = request.POST['body']
    post = get_object_or_404(Post, author=user_id)
    post.title = title
    post.body = body
    post.save()

def password_change(request, username):
    username = generate_token(token=username,key="mohanraj", mode='decode')
    user = get_object_or_404(User, username=username['username'])
    if request.method == 'POST':
        old_password = request.POST['old_password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if user.check_password(old_password):
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request,  "Password change successfully" )
            else:
                messages.error(request, "Password are not match" )
        else:
            messages.error(request, "Password are not match" )
        return redirect('blog:login')
        # return render(request, 'blog/password_change.html', {"user":user,"msg":msg})
    else:
        return render(request, 'blog/password_change.html', {"user":user})

# def password_reset(request, username):
    
#     msg = ""
#     return render(request, 'blog/password_reset.html', {'msg':msg})

def generate_token(key, mode ,hide_data:dict = "",token="",):
    """mode: 'encode' for encode the values
            'decode' for decode the values
        key: 'secure key for encoding and decode'
        hide_data: what data you want to encode
        token: the encode the data
        """
    if mode == 'encode':
        encoded_data = jwt.encode(hide_data, key, algorithm="HS256")
        return encoded_data
    elif mode == 'decode':
        decoded_data = jwt.decode(token, key, algorithms=['HS256'])
        return decoded_data



def password_forgot(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        email = request.POST['email']
        # send_mail(subject, message, from_email, recipient_list,\
        #     fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
        token = generate_token({'username':username},key="mohanraj",mode='encode')
        send_mail(
            'Your password change token',
            f"Click the link to verified to change your password {username} http://localhost:8080/password/{token}/change/",
            'mohanraj@markblogs.com',
            [email],
            fail_silently=False,
            )
        messages.success(request,"SEND forgot email link to your email %s", email)
        print("decode value",generate_token(token=token,key="mohanraj",mode='decode'))
        return redirect('blog:home')
        # return render(request, 'blog/account_activation.html', {"user":user,'msg':msg})
    else:
        return render(request, 'blog/password_forgot.html')

    # return HttpResponse("<p>Password rest view</p>")

def send_activation_code(username):
    encode_data = generate_token(hide_data={"username":username}, key="activation key", mode='encode')
    send_mail(
        "For your activate account in mark_blogs",
        "activation click the link :" f"http://localhost:8080/user/{encode_data}/activation/",
        "mohanraj@markblogs.com",
        ["someone@gmail.com"],
        fail_silently=True
    )
    print(encode_data)

def activation(request, username):
    print('begging')
    send_activation_code(username)
    user = generate_token(key="activation key", mode='decode', token=username)['username']
    print(user)
    if User.objects.filter(username=user).exists():
        return login_user(request)
    else:
        return render(request, 'blog/account_activation.html')



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


# def set_cookie(
#         response: HttpResponse,
#         key: str,
#         value: str,
#         cookie_host: str,
#         days_expire: int = 365,):
#     max_age = days_expire * 24 * 60 * 60
#     expires = datetime.datetime.strftime(
#         datetime.datetime.utcnow() +
#         datetime.timedelta(days=days_expire), "%a, %d-%b-%Y %H:%M:%S GMT",
#     )
#     domain = cookie_host.split(":")[0]
#     response.set_cookie(
#         key,
#         value,
#         max_age=max_age,
#         expires=expires,
#         domain=domain,
#         secure=False,
#     )
