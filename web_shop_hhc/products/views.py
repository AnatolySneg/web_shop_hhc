from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.


def home_page(request):
    print('home-page from console')
    return HttpResponse('This is Home-page')


def product_list(request):
    products_all = Product.objects.all()
    return render(request, 'products/home_page.html', {
        'product_list': products_all,
    }
                  )
