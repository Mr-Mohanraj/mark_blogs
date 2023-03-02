from django.shortcuts import render
from authentication.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import Http404


def search_user(request):
    """ search function  """
    query_name = request.GET.get('q', None)
    print(query_name)
    if ((query_name != None) and (query_name)):
        results = User.objects.filter(username__contains=query_name)
        print("results", results)
        return render(request, 'user_profile/search_result.html', {"results": results})
    return render(request, 'user_profile/search_result.html')


def all_users(request):
    users = User.objects.all()
    return render(request, "user_profile/users_page.html", {"users": users})


def profile(request, pk):
    try:
        print("inside the try")
        users = get_object_or_404(User, pk=pk)
        followers = users.followers.all()
        return render(request, 'user_profile/profile.html', {"users": users,  "followers": followers, "choose": "view_profile"})
    except (Http404,UnboundLocalError):
        print("Inside the except")
        return render(request, '404.html', {"error": "User cannot find"})
