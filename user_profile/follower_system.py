from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from authentication.models import User
from django.contrib import messages
from django.http.response import Http404


def remove_follower(request, author):
    # who is go to follow author person
    currentUserObj = User.objects.get(username=request.user.username)
    authorObj = User.objects.get(
        username=author)  # who is want a follow person
    # for getting all follower belong to the author person
    followers = authorObj.followers.all()
    if currentUserObj.is_authenticated:
        if authorObj != currentUserObj:
            if currentUserObj in followers:
                authorObj.followers.remove(currentUserObj)
                currentUserObj.followings.remove(authorObj)
                authorObj.save()
                currentUserObj.save()
                messages.success(request, f"un follow is  successfully!")
                return redirect('profile:profile', pk=currentUserObj.id)
                # return render(request, 'user_profile/add_follower.html', {"users": currentUserObj, "following": followers})
            else:
                messages.success(
                    request, f"you don't follow this person this person")
                return render(request, 'user_profile/add_follower.html', {"users": currentUserObj, "following": followers})
        else:
            messages.info(request, "This is a your profile")
            return render(request, 'user_profile/add_follower.html', {"users": currentUserObj, "following": followers})
    else:
        messages.error(request, "please login first!")
        return render(request, 'user_profile/add_follower.html', {"users": currentUserObj, "following": followers})


def add_follower(request, author):
    # who is go to follow author person
    currentUserObj = User.objects.get(username=request.user.username)
    authorObj = User.objects.get(
        username=author)  # who is want a follow person
    # for getting all follower belong to the author person
    followers = authorObj.followers.all()
    if currentUserObj.is_authenticated:
        if authorObj != currentUserObj:
            if currentUserObj in followers:
                messages.success(
                    request, f"you are already in the followers list successfully!")
                return render(request, 'user_profile/add_follower.html', {"users": currentUserObj, "following": followers})
            else:
                messages.success(request, f"follow successfully!")
                authorObj.followers.add(currentUserObj)
                currentUserObj.followings.add(authorObj)
                authorObj.save()
                currentUserObj.save()
                return redirect('profile:profile', pk=currentUserObj.id)
                # return render(request, 'user_profile/add_follower.html', {"users": currentUserObj, "following": followers})
        else:
            messages.info(request, "Can't follow your own profile")
            return render(request, 'user_profile/add_follower.html', {"users": currentUserObj, "following": followers})
    else:
        messages.error(request, "please login first!")
        return render(request, 'user_profile/add_follower.html', {"users": currentUserObj, "following": followers})


def view_follower(request, pk):
    print("pk #####", pk)
    try:
        print("inside the try")
        users = get_object_or_404(User, pk=pk)
        followers = users.followers.all()
        for i in followers:
            print(dir(i))
            if i in followers and i.id == request.user.id:
                print("follower unfollow")
            else:
                print("follow")

        if len(followers) <= 0:
            messages.error(request, "you don't have a followers")
        return render(request, 'user_profile/add_follower.html', {"users": users, "followers": followers})
    except Http404:
        print("Inside the except")
        return render(request, '404.html', {"error": "User not found please login or signup"})


def view_following(request, pk):
    print("pk #####", pk)
    try:
        print("inside the try")
        users = get_object_or_404(User, pk=pk)
        followings = users.followings.all()
        print("following", followings)
        if len(followings) > 0:
            fun = "view_following"
        else:
            fun = "profile"
            messages.error(request, "you don't have a following")

        return render(request, 'user_profile/add_following.html', {"users": users, "following": followings, "choose": fun})
    except Http404:
        print("Inside the except")
        return render(request, 'user_profile/add_following.html', {"users": users, "following": followings, "choose": "view_following"})


# def add_following(request, pk):
#     try:
#         follow = get_object_or_404(Follower, pk=pk)
#     except Http404:
#         follow = Follower(pk=pk)
#         follow.save()
#     user = request.user
#     if user.is_authenticated:
#         if user in follow.following.all():
#             messages.error(request, "You already following this person")
#             return render(request, "user_profile/profile.html", {"following": follow, "choose": "add_following"})
#         else:
#             follow.following.add(user)
#             follow.save()
#             messages.success(request, "following is successfully")
#             return render(request, "user_profile/profile.html", {"following": follow, "choose": "add_following"})
#     else:
#         messages.success(request, "Login please")
#         return render(request, "user_profile/profile.html", {"following": follow, "choose": "add_following"})
#     # return render(request, "user_profile/profile.html", {"instance":follow,"choose":"add_following"})


# def remove_follower(request, pk):
#     follow = get_object_or_404(Follower, pk=pk)
#     user = request.user
#     users = get_object_or_404(User, pk=pk)
#     if user.is_authenticated:
#         if user in follow.follower.all():
#             follow.follower.remove(user)
#             follow.save()
#             messages.success(request, "un following is successfully")
#             return render(request, "user_profile/profile.html", {"users": users, "following": follow, "choose": "remove_follower"})
#         else:
#             messages.error(request, "Your not follow the person")
#             return render(request, "user_profile/profile.html", {"users": users, "following": follow, "choose": "remove_follower"})
#     else:
#         messages.error(request, "please login !!!")
#         return render(request, "user_profile/profile.html", {"users": users, "following": follow, "choose": "remove_follower"})


# def remove_following(request, pk):
#     follow = get_object_or_404(Follower, pk=pk)
#     user = request.user
#     users = get_object_or_404(User, pk=pk)
#     if user.is_authenticated:
#         if user in follow.following.all():
#             follow.following.remove(user)
#             follow.save()
#             messages.success(request, "Un following is successfully")
#             return render(request, "user_profile/profile.html", {"users": users, "instance": follow, "choose": "remove_following"})
#         else:
#             messages.success(request, "you not follow the person")
#             return render(request, "user_profile/profile.html", {"users": users, "instance": follow, "choose": "remove_following"})
#     else:
#         messages.error(request, "please login !!!")
#         return render(request, "user_profile/profile.html", {"users": users, "instance": follow, "choose": "remove_following"})


# 9

# def add_remove_following(request, author):
#     is_followed = False
#     # who is go to follow author person
#     currentUserObj = User.objects.get(username=request.user.username)
#     authorObj = User.objects.get(
#         username=author)  # who is want a follow person
#     # for getting all follower belong to the author person
#     followings = authorObj.followings.all()

#     if currentUserObj.is_authenticated:
#         if authorObj != currentUserObj:
#             if currentUserObj in followings:
#                 messages.success(request, f"un following remove successfully!")
#                 authorObj.followings.remove(currentUserObj)
#                 authorObj.save()
#                 return render(request, 'user_profile/add_following.html', {"users": currentUserObj, "following": followings, "choose": "view_following"})
#             else:
#                 messages.success(request, f"following add successfully!")
#                 authorObj.followings.add(currentUserObj)
#                 authorObj.save()
#                 return render(request, 'user_profile/add_following.html', {"users": currentUserObj, "following": followings, "choose": "view_following"})
#         else:
#             messages.info(request, "you can't follow")
#             return render(request, 'user_profile/add_following.html', {"users": currentUserObj, "following": followings, "choose": "view_following"})

#     else:
#         messages.error(request, "please login first!")
#         return render(request, 'user_profile/add_following.html', {"users": currentUserObj, "following": followings, "choose": "view_following"})


# def add_follower(request, pk):
#     # follower = get_object_or_404(Follower, pk=pk)
#     return render(request, "user_profile/add_follower.html")


# def add_remove_follower(request, author):
#     authorObj = Follower.objects.get(username=author)
#     currentUserObj = User.objects.get(username=request.user.username)
#     following = authorObj.following.all()
#     if request.user.is_authenticated:
#         if author != currentUserObj.username:
#             if currentUserObj in following:
#                 authorObj.following.remove(currentUserObj.id)
#             else:
#                 authorObj.following.add(currentUserObj.id)
#     else:
#         return "somthhig"
