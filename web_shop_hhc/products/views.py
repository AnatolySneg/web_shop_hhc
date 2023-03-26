from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


# Create your views here.


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/home_page.html', {
        'products': products,
    }
                  )


def contacts_page(request):
    print('contacts_page from console')
    return HttpResponse('This is Contacts_page')


def login_page(request):
    print('login_page from console')
    return HttpResponse('This is login_page')


def logout(request):
    print('logout_process from console')
    return HttpResponse('This is logout_process')


def user_page(request):
    print('user_page from console')
    return HttpResponse('This is user_page')


def bucket(request):
    print('Bucket_page from console')
    return HttpResponse('This is Bucket_page')
