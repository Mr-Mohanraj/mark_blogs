from django.shortcuts import render, redirect, get_object_or_404
from .models import  User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http.response import Http404
from .utils import (password_forgot_mail,
                    generate_token, send_activation_code)



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

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("auth:signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email id already taken")
            return redirect("auth:signup")

        if not ((password and password_confirm) and (password == password_confirm)):
            messages.error(request, "password are does not match")
            return redirect("auth:signup")

        user = User.objects.create(
            username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        url = request.build_absolute_uri('/')
        send_activation_code(user, url)
        messages.success(request, f"Activation code set your {email}")
        return render(request, 'authentication/account_activation.html')
    else:
        return render(request, 'authentication/signup_form.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user is not None:
                if User.objects.filter(username=username).exists() and user.username == username:
                    messages.info(request, "username is correct")
                    if user.check_password(password):
                        # messages.info(request, "password is correct"
                        if user.is_active:
                            login(request, user)
                            messages.success(
                                request, "your login successfully!")
                            return redirect('pages:home')
                        else:
                            messages.error(
                                request, "please activate your account use your activation code, we are send to your account")
                            return redirect('auth:home')
                    else:
                        messages.error(request, "password are incorrect")
                        return redirect("auth:login")
                else:
                    messages.error(request, "username are wrong")
                    return redirect("auth:login")
        except Exception as e:
            return render(request, 'authentication/404.html', {"error": e})
    else:
        return render(request, "authentication/login_form.html")


def logout_user(request, username):
    logout(request)
    messages.success(request, "logout successfully!!")
    return redirect('auth:home')


# def upload_authentication(request, user_id):
#     title = request.POST['title']
#     body = request.POST['body']
#     post = get_object_or_404(Post, authenticationor=user_id)
#     post.title = title
#     post.body = body
#     post.save()


def password_change(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        old_password = request.POST['old_password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if user.check_password(old_password):
            if password1 == password2:
                user.set_password(password1)
                user.save()
                logout(request)
                messages.success(
                    request,  "Password change successfully, please login again")
                return redirect('auth:login')
            else:
                messages.error(request, "Password are not match")
                return redirect('auth:password_change')
        else:
            messages.error(request, "old Password are not match")
            return redirect('auth:password_change')
    else:
        return render(request, 'authentication/password_change.html')


def password_forgot(request, username):
    if request.method == 'POST':
        email = request.POST['email']
        token = generate_token(key="mohanraj", hide_data={'username': username},
                               mode='encode')
        password_forgot_mail(request, username, email, token)
        messages.success(
            request, f"SEND forgot email link to your {email}")
        return redirect('auth:home')
    else:
        return render(request, 'authentication/password_forgot.html', {"password_forgot": True})


def forgot_password_change(request, token):
    username = generate_token(token=token, key="mohanraj", mode='decode')
    user = get_object_or_404(User, username=username['username'])
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user.set_password(password1)
            user.save()
            logout(request)
            messages.success(
                request,  "Password change successfully, please login again")
            return redirect('auth:login')
        else:
            messages.error(request, "Password are does not match")
            return redirect('auth:password_forgot_change')
    else:
        return render(request, 'authentication/password_forgot.html', {"password_forgot_change": True})


def activation(request, token):
    username = generate_token(key="activation key",
                              mode='decode', token=token)['username']
    url = request.build_absolute_uri('/')
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(
                request, "your account activation successfully!!!")
            return redirect("auth:login")
        else:
            messages.success(request, "your account is already activation")
            return redirect("auth:login")
    else:
        return render(request, 'authentication/account_activation.html')


# def profile(request, pk):
#     user_info = get_object_or_404(User, pk=pk)
#     return render(request, "authentication/profile.html", {"user": user_info})


def search_user(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('q', None)
        print(query_name)
        if query_name:
            results = User.objects.filter(username__contains=query_name)
            print("results", results)
            return render(request, 'authentication/search_result.html', {"results": results})
    return render(request, 'authentication/search_result.html')


def all_users(request):
    users = User.objects.all()
    return render(request, "authentication/users_page.html", {"users": users})


def profile(request, pk):
    try:
        print("inside the try")
        users = get_object_or_404(User, pk=pk)
        followers = users.followers.all()
        return render(request, 'authentication/profile.html', {"users": users,  "followers": followers, "choose": "view_profile"})
    except (Http404,UnboundLocalError):
        print("Inside the except")
        return render(request, '404.html', {"error": "User cannot find"})
