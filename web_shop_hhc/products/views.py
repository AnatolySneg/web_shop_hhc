from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Image
# Create your views here.


def home_page(request):
    print('home-page from console')
    return HttpResponse('This is Home-page')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/home_page.html', {
        'products': products,
    }
                  )
