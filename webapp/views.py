from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    Home page of website
    :param  request: Django request object
    :return render:
    """
    return render(request, 'webapp/index.html')

