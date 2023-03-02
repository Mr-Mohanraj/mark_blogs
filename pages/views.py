from django.shortcuts import render
from .utils import get_random_quote


def home(request):
    quote = get_random_quote()
    return render(request, 'pages/home.html', {"quote": quote[0], "author":quote[1]})
