import json
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post, User, Follower
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http.response import Http404
import jwt
import random
from django.conf import settings


def home(request):
    return render(request, 'blog/home.html', {"quote": get_random_quote()})
    '''
    without inbuilt login function
    if request.session.has_key('user'):
        username = request.session['user']
        print(username)
        print(request.user)
        s = request.user = username
        print(s)
        return render(request, 'blog/home.html', {"username" : username})
    else:
    print(request.user)
    res = HttpResponse(render(request, 'blog/home.html'))
    username = request.COOKIES.get('user', 'guest')
    print(username)
    if username == 'guest':
        return HttpResponse(render(request, 'blog/home.html', {"user": username}))
    else:
        print("welcome brother")
        user = User.objects.get(username=username)
        return HttpResponse(render(request, 'blog/home.html', {"user": user}))
    '''


def blog_list(request):
    post = Post.objects.all()
    return render(request, 'blog/blog_list.html', {"posts": post})

    '''
    without inbuilt login function
    username = request.COOKIES.get('user', 'guest')
    if username == 'guest':
        return render(request, 'blog/blog_list.html', {"posts": post})
    else:
        user = get_object_or_404(User, username=username)
        return render(request, 'blog/blog_list.html', {"posts": post})
    '''


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
        return render(request, 'blog/blog_detail.html', {"post": post, "instance": obj})
    else:
        return render(request, 'blog/blog_detail.html', {"post": post, "instance": post})

    '''
    without inbuilt login function
    try:
        post = Post.objects.get(pk=pk)
        user = get_object_or_404(User, pk=pk)
    except ObjectDoesNotExist:
        return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})
    return render(request, 'blog/blog_detail.html', {"post": post, "user":user})
    '''


def blog_edit(request, pk):
    if request.method == 'POST':
        try:
            post = Post.objects.get(pk=pk)
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.save()
            return render(request, 'blog/blog_detail.html', {"post": post})
        except ObjectDoesNotExist:
            return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})
    else:
        try:
            post = Post.objects.get(pk=pk)
            return render(request, 'blog/blog_edit.html', {"post": post})
        except ObjectDoesNotExist:
            return render(request, 'blog/404.html', {"error": ObjectDoesNotExist})


def blog_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        messages.success(
            request, f"{post.title} was delete successfully! by {post.author.username}")
        post.delete()
        return redirect('blog:home')
    except ObjectDoesNotExist:
        return render(request, 'blog/404.html')


def blog_add(request, username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            title = request.POST['title']
            body = request.POST['body']
            post = Post(title=title, body=body, author=user)
            messages.success(request, f"post add successfully!")
            post.save()
            return redirect("blog:blog_detail", pk=post.id)
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

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("blog:signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email id already taken")
            return redirect("blog:signup")

        if not ((password and password_confirm) and (password == password_confirm)):
            messages.error(request, "password are does not match")
            return redirect("blog:signup")

        user = User.objects.create(
            username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        url = request.build_absolute_uri('/')
        send_activation_code(user, url)
        messages.success(request, f"Activation code set your {email}")
        return render(request, 'blog/account_activation.html')
    else:
        return render(request, 'blog/signup_form.html')


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
                            return redirect('blog:home')
                        else:
                            messages.error(
                                request, "please activate your account use your activation code, we are send to your account")
                            return redirect('blog:home')
                    else:
                        messages.error(request, "password are incorrect")
                        return redirect("blog:login")
                else:
                    messages.error(request, "username are wrong")
                    return redirect("blog:login")
        except Exception as e:
            return render(request, 'blog/404.html', {"error": e})
    else:
        return render(request, "blog/login_form.html")

        '''
        # custom user login function
            try:
                user = User.objects.get(username=username)
                if user.username == username:
                    messages.info(request, "username is correct")
                    if user.check_password(password):
                        messages.info(request, "password is correct")
                        user.is_login = True
                        request.user = User()
                        user.save()
                        request.session['user'] = user
                        res = HttpResponse(
                            render(request, 'blog/home.html', {"user": user}))
                        res.set_cookie('user', user.username)
                        return res
                    return render(request, 'blog/404.html', {"error": [username, password]})
            except Exception as e:
                return render(request, 'blog/404.html', {"error": e})
        '''


def logout_user(request, username):
    logout(request)
    messages.success(request, "logout successfully!!")
    return redirect('blog:home')

    '''
    custom logout function
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
    '''


def user_blog(request, user_id):
    try:
        posts = get_list_or_404(Post, author=user_id)
        return render(request, 'blog/blog_list.html', {"posts": posts})
    except Http404:
        messages.error(
            request, "There is no blog now add it use the add new blog button")
        return render(request, 'blog/home.html', {})

    '''
    # custom uer blog get function
    user = get_object_or_404(User, id=user_id)
    try:
        posts = get_list_or_404(Post, author=user_id)
        return render(request, 'blog/blog_list.html', {"posts": posts, "user":user})
    except Http404:
        messages.error(request, "There is no blog now add it")
        return render(request, 'blog/home.html',{"user":user})
    '''


def upload_blog(request, user_id):
    title = request.POST['title']
    body = request.POST['body']
    post = get_object_or_404(Post, author=user_id)
    post.title = title
    post.body = body
    post.save()


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
                return redirect('blog:login')
            else:
                messages.error(request, "Password are not match")
                return redirect('blog:password_change')
        else:
            messages.error(request, "old Password are not match")
            return redirect('blog:password_change')
    else:
        return render(request, 'blog/password_change.html')


def generate_token(key, mode, hide_data: dict = "", token="",):
    """mode: 'encode' for encode the values
            'decode' for decode the values
        key: 'secure key for encoding and decode'
        hide_data: what data you want to encode
        token: the encode the data
        ``` For decoding values are token,key```
        ``` For encode values are hide_data, key ```
        """
    if mode == 'encode':
        encoded_data = jwt.encode(hide_data, key, algorithm="HS256")
        return encoded_data
    elif mode == 'decode':
        decoded_data = jwt.decode(token, key, algorithms=['HS256'])
        return decoded_data


def password_forgot(request, username):
    if request.method == 'POST':
        email = request.POST['email']
        token = generate_token(key="mohanraj", hide_data={'username': username},
                               mode='encode')
        send_mail(
            'Your password change token',
            f"Click the link to verified to change your password {username} => {request.build_absolute_uri('/')}password/{token}/forgot/change/",
            'mohanraj@markblogs.com',
            [email],
            fail_silently=True,
        )
        messages.success(
            request, f"SEND forgot email link to your {email}")
        return redirect('blog:home')
    else:
        return render(request, 'blog/password_forgot.html', {"password_forgot": True})


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
            return redirect('blog:login')
        else:
            messages.error(request, "Password are does not match")
            return redirect('blog:password_forgot_change')
    else:
        return render(request, 'blog/password_forgot.html', {"password_forgot_change": True})


def send_activation_code(user, url):
    encode_data = generate_token(
        hide_data={"username": user.username}, key="activation key", mode='encode')
    send_mail(
        "For your activate account in mark_blogs",
        "activation click the link :" f"{url}user/{encode_data}/activation/",
        "mohanraj@markblogs.com",
        [user.email],
        fail_silently=True,
    )


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
            return redirect("blog:login")
        else:
            messages.success(request, "your account is already activation")
            return redirect("blog:login")
    else:
        return render(request, 'blog/account_activation.html')


def profile(request, pk):
    user_info = get_object_or_404(User, pk=pk)
    return render(request, "blog/profile.html", {"user": user_info})


def get_random_quote():
    with open(settings.BASE_DIR/'static/sample.json', 'r') as file:
        file_data = json.load(file)
        quote = {"quote": "", "author": ""}
        if random.randint(1, 99) == 41:
            pass
        else:
            quote = file_data[f"quote {random.randint(1,99)}"]
    return quote['quote'], quote['author']


def add_follower(request, pk):
    # follower = get_object_or_404(Follower, pk=pk)
    return render(request, "blog/add_follower.html")


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
            return redirect("blog:login")
    else:
        messages.error("can't like your own post")
        return like_obj

# def search_user(request):
#     try:
#         username = request.POST.get("q")
#         user = get_object_or_404(User, username=username)
#         return render(request, "blog/search_result.html", {"result":user})
#     except Http404:
#         messages.error(request, "Invalid username, please enter correct username")
#         return render(request, "blog/search_result.html", {"result":user})


def search_user(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('q', None)
        print(query_name)
        if query_name:
            results = User.objects.filter(username__contains=query_name)
            print("results", results)
            return render(request, 'blog/search_result.html', {"results": results})
    return render(request, 'blog/search_result.html')


def all_users(request):
    users = User.objects.all()
    return render(request, "blog/users_page.html", {"users": users})


def profile(request, pk):
    user = get_object_or_404(User, pk)
    return redirect("blog:profile",pk=user.pk)


def add_follower(request, pk):
    try:
        follow = get_object_or_404(Follower, pk=pk)
        users = get_object_or_404(User, pk=pk)
    except Http404:
        follow = Follower(pk=pk)
        follow.save()

    user = request.user
    if user.is_authenticated:
        if user in follow.follower.all():
            messages.error(request, "You already follow this person")
            return render(request, "blog/profile.html", {"users": users, "follow": follow, "choose": "add_follower"})
        else:
            follow.follower.add(user)
            messages.success(request, "follower is successfully")
            return render(request, "blog/profile.html", {"users": users, "follow": follow, "choose": "add_follower"})
    else:
        messages.success(request, "Login first")
        return render(request, "blog/profile.html", {"users": users, "follow": follow, "choose": "add_follower"})


def add_following(request, pk):
    try:
        follow = get_object_or_404(Follower, pk=pk)
    except Http404:
        follow = Follower(pk=pk)
        follow.save()
    user = request.user
    if user.is_authenticated:
        if user in follow.following.all():
            messages.error(request, "You already following this person")
            return render(request, "blog/profile.html", {"following": follow, "choose": "add_following"})
        else:
            follow.follower.add(user)
            messages.success(request, "following is successfully")
            return render(request, "blog/profile.html", {"following": follow, "choose": "add_following"})
    else:
        messages.success(request, "Login first")
        return render(request, "blog/profile.html", {"following": follow, "choose": "add_following"})
    # return render(request, "blog/profile.html", {"instance":follow,"choose":"add_following"})


def remove_follower(request, pk):
    follow = get_object_or_404(Follower, pk=pk)
    user = request.user
    if user.is_authenticated:
        if user in follow.follower.all():
            follow.follower.remove(user)
            messages.success(request, "un following is successfully")
            return render(request, "blog/profile.html", {"following": follow, "choose": "remove_follower"})
        else:
            messages.error(request, "Your not follow the person")
            return render(request, "blog/profile.html", {"following": follow, "choose": "remove_follower"})
    else:
        return render(request, "blog/profile.html", {"instance": follow, "choose": "remove_follower"})


def remove_following(request, pk):
    follow = get_object_or_404(Follower, pk=pk)
    user = request.user
    if user.is_authenticated:
        if user in follow.following.all():
            follow.following.remove(user)
            messages.success(request, "Un following is successfully")
            return render(request, "blog/profile.html", {"instance": follow, "choose": "remove_following"})
        else:
            messages.success(request, "you not follow the person")
            return render(request, "blog/profile.html", {"instance": follow, "choose": "remove_following"})
    else:
        return render(request, "blog/profile.html", {"instance": follow, "choose": "remove_following"})


def view_follower(request, pk):
    print("pk #####", pk)
    try:
        print("inside the try")
        users = get_object_or_404(User, pk=pk)
        obj = get_object_or_404(Follower, pk=pk)
        followers = obj.follower.all()
        return render(request, 'blog/profile.html', {"users": users, "instance": obj, "followers": followers, "choose": "view_follower"})
    except Http404:
        print("Inside the except")
        obj = Follower(pk=pk)
        obj.save()
        followers = obj.follower.all()
        return render(request, 'blog/profile.html', {"users": users, "instance": obj, "followers": followers, "choose": "view_follower"})


def view_following(request, pk):
    print("pk #####", pk)
    try:
        print("inside the try")
        users = get_object_or_404(User, pk=pk)
        obj = get_object_or_404(Follower, pk=pk)
        following = obj.following.all()
        return render(request, 'blog/profile.html', {"users": users, "instance": obj, "following": following, "choose": "view_following"})
    except Http404:
        print("Inside the except")
        obj = Follower(pk=pk)
        obj.save()
        following = obj.follower.all()
        return render(request, 'blog/profile.html', {"users": users, "instance": obj, "following": following, "choose": "view_following"})

    # print("value",value)
    # print(bool(value))
    # cur_user = user
    # like_user = ""
    # request.COOKIES["count"] = 0
    # if not (cur_user == like_user):
    #     print("inside the logic")
    #     count += 1
    #     like_user = user
    # if count == 1:
    #     count = 0
    #     #     print("you already like this post")
    #     # print("count", count)
    #     if not (str(user) == str(like_obj.author.username)):
    #         if value:
    #             try:
    #                 print("Inside the try")
    #                 if value['like'] == "likebutton":
    #                     like_obj.like = like_obj.like + 1
    #                     like_obj.save()
    #                     print("like",like_obj.like)
    #                     return like_obj
    #                 elif value['like'] == "dislikebutton":
    #                     print("inside the dislike button")
    #                     like_obj.dislike = like_obj.dislike + 1
    #                     like_obj.save()
    #                     print("dislike",like_obj.dislike)
    #                     return like_obj
    #                     # return render(request, "blog/blog_detail.html", {"likes":like_obj})
    #             except MultiValueDictKeyError:
    #                 print("error")
    #         else:
    #             print("inside the else")
    #             return like_obj
    #     else:
    #         print("You can't add likes i your blog")
    #         return like_obj
    # else:
    #     print("likeeeeeee#########################")
    #     return like_obj


def _checker(value):
    try:
        if value['like'] == "likebutton":
            return "like"
        elif value['like'] == "dislikebutton":
            return "dislike"
            # return render(request, "blog/blog_detail.html", {"likes":like_obj})
    except MultiValueDictKeyError:
        return "Error"

    # return render(request, "blog/blog_detail.html", {"likes":like_obj})
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
