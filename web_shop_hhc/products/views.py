from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Image
from .forms import *


# Create your views here.


def product_list(request):
    products = Product.objects.all()
    print(request.user)
    return render(request, 'products/pages/home_page.html', {
        'products': products,
        'active_page': "home_page"
    }
                  )


def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    images = Image.objects.filter(product_id=product_pk)
    return render(request, 'products/pages/product_detail.html', {
        'active_page': "home_page",
        'product': product,
        'images': images,
    }
                  )


def contacts_page(request):
    print('contacts_page from console')
    print(request)
    test_string = "This string was rendered from views.contacts_page()"
    return render(request, 'products/pages/about_us.html', {
        "test_string": test_string,
        'active_page': "contacts_page"
    }
                  )


def login_page(request):
    print('login_page from console')
    test_string = "This string was rendered from views.login_page()"
    return render(request, 'products/pages/login_page.html', {
        "test_string": test_string,
        'active_page': "login_page"
    }
                  )


def logout(request):
    print('logout_process from console')
    return HttpResponse('This is logout_process')


def user_page(request):
    print('user_page from console')
    print(request)
    test_string = "USER PAGE"
    return render(request, 'products/pages/user_page.html', {
        "test_string": test_string,
        'active_page': "user_page"
    }
                  )


def bucket(request):
    print('Bucket_page from console')
    print(request)
    test_string = "This string was rendered from views.bucket()"
    return render(request, 'products/pages/bucket_page_gest.html', {
        "test_string": test_string,
        'active_page': "bucket"
    }
                  )


def signup(request):
    if request.method == 'POST':
        user_form = UserSignupForm(request.POST)
        customer_form = CustomerSignupForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            # customer.user = user
            customer.save()
            return redirect('/')
    else:
        user_form = UserSignupForm()
        customer_form = CustomerSignupForm()
    return render(request, 'products/pages/signup_page.html', {
        'user_form': user_form,
        'customer_form': customer_form,
    }
                  )
