from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


# Create your views here.


def product_list(request):
    products = Product.objects.all()
    print(request)
    return render(request, 'products/home_page.html', {
        'products': products,
    }
                  )


def contacts_page(request):
    print('contacts_page from console')
    print(request)
    test_string = "This string was rendered from views.contacts_page()"
    return render(request, 'products/about_us.html', {
        "test_string": test_string,
    }
                  )


def login_page(request):
    print('login_page from console')
    test_string = "This string was rendered from views.login_page()"
    return render(request, 'products/login_page.html', {
        "test_string": test_string,
    }
                  )


def logout(request):
    print('logout_process from console')
    return HttpResponse('This is logout_process')


def user_page(request):
    print('user_page from console')
    print(request)
    test_string = "USER PAGE"
    return render(request, 'products/user_page.html', {
        "test_string": test_string,
    }
                  )


def bucket(request):
    print('Bucket_page from console')
    print(request)
    test_string = "This string was rendered from views.bucket()"
    return render(request, 'products/bucket_page_gest.html', {
        "test_string": test_string,
    }
                  )
