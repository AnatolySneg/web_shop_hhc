from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import *
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .forms import *


# Create your views here.


def product_list(request):
    products = Product.objects.all()
    print(request.user)
    print(request.user.is_authenticated)
    print(request.META.get('HTTP_REFERER'))
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


# def login_page(request):
#     print('login_page from console')
#     if request.method=="POST":
#         print('POST!!!  POST!!!  POST!!!  POST!!!  POST!!!  ')
#         print(request.POST['phone'])
#         for key in request.POST:
#             print(key, ' - ', request.POST[key])
#         print('POST!!!  POST!!!  POST!!!  POST!!!  POST!!!  ')
#
#     return render(request, 'products/pages/login_page.html', {
#         'active_page': "login_page"
#     }
#                   )


def login_page(request):
    ctx = {}
    if request.method == "POST":
        phone_number = request.POST['phone']
        # TODO: make validator for signs of phone number
        if len(phone_number) == 10:
            phone_number = '+38' + phone_number
        username = Customer.objects.get(phone_number=phone_number).user.username
        password = request.POST['password']
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            django_login(request, auth_user)
            return redirect('/')
        else:
            # TODO: raise error if no user or incorrect password
            ctx['error'] = 'User not found!'
    ctx['active_page'] = "login_page"
    return render(request, 'products/pages/login_page.html', ctx)


def logout(request):
    django_logout(request)
    return redirect('/')


def user_page(request):
    print('user_page from console')
    print(request)
    test_string = "USER PAGE"
    return render(request, 'products/pages/user_page.html', {
        "test_string": test_string,
        'active_page': "user_page"
    }
                  )


def signup(request):
    # TODO: register only unique phones and emails
    if request.method == 'POST':
        print("request.POST", request.POST)
        user_form = UserSignupForm(request.POST)
        customer_form = CustomerSignupForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            username = user.username
            password = request.POST.get('password')
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                django_login(request, auth_user)
            return redirect('/')
    else:
        user_form = UserSignupForm()
        customer_form = CustomerSignupForm()
    return render(request, 'products/pages/signup_page.html', {
        'user_form': user_form,
        'customer_form': customer_form,
        'active_page': "signup_page"
    }
                  )


"""
Bucket functions for Gest (Anonim Users) Start
"""


def bucket(request):
    context = {'active_page': "bucket"}
    try:
        bucket_ids = request.session.get('products')
        product_quantity = {}
        for id_number in bucket_ids:
            product_quantity[id_number] = bucket_ids.count(id_number)
        bucket_products = Product.objects.filter(id__in=bucket_ids)
        context['bucket_products'] = bucket_products
        context['product_quantity'] = product_quantity
    except TypeError:
        context['product_quantity'] = []
    return render(request, 'products/pages/bucket_page_gest.html', context)


def add_to_bucket(request, product_id):
    if request.META.get('HTTP_REFERER'):
        bucket_products = request.session.get('products')
        if not bucket_products:
            request.session['products'] = [product_id]
        else:
            products = request.session['products']
            products.append(product_id)
            request.session['products'] = products
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/')


def remove_from_bucket(request, product_pk):
    bucket_products = request.session.get('products')
    new_bucket_list = bucket_products.copy()
    for bucket_pk in bucket_products:
        if bucket_pk == product_pk:
            new_bucket_list.remove(bucket_pk)
    request.session['products'] = new_bucket_list
    return redirect(bucket)


def more_to_bucket(request, product_pk):
    product_in_bucket = request.session['products']
    product_in_bucket.append(product_pk)
    request.session['products'] = product_in_bucket
    return redirect(bucket)


def less_to_bucket(request, product_pk):
    product_in_bucket = request.session['products']
    product_in_bucket.remove(product_pk)
    request.session['products'] = product_in_bucket
    return redirect(bucket)


"""
Bucket functions for Gest (Anonim Users) End
"""



"""
Bucket functions for Autorised User Start
"""

def user_bucket(request):
    context = {'active_page': "bucket"}
    try:
        bucket_ids = request.session.get('products')
        product_quantity = {}
        for id_number in bucket_ids:
            product_quantity[id_number] = bucket_ids.count(id_number)
        bucket_products = Product.objects.filter(id__in=bucket_ids)
        context['bucket_products'] = bucket_products
        context['product_quantity'] = product_quantity
    except TypeError:
        context['product_quantity'] = []
    return render(request, 'products/pages/bucket_page_gest.html', context)

"""
Bucket functions for Autorised User End
"""


"""
phone number = "+380441234567"
password = "JS-password"

if Customer.objects.filter(phone_number=str(phone_number)):

find its user.username and threw it as arg (username) in authenticate(username=username,
                                     password=password)
    

"""

# def login(request):
#     ctx = {}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         auth_user = authenticate(username=username, password=password)
#         if auth_user:
#             django_login(request, auth_user)
#             return redirect('/')
#         else:
#             ctx['error'] = 'User not found!'
#     return render(request, 'users/auth/login.html', ctx)
