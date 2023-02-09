from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home_page(request):
    print('home-page from console')
    return HttpResponse('This is Home-page')
