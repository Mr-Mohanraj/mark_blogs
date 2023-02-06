from django.shortcuts import render
from .utils import get_random_quote


def home(request):
    return render(request, 'pages/home.html', {"quote": get_random_quote()})
