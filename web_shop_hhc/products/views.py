from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import *
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .forms import *
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
# @require_GET
def product_list(request):
    context = {'active_page': "home_page", 'header_bucket_counter': header_bucket_counter(request)}
    # TODO: Fielters and Sorting products !!!!
    context['products'] = Product.objects.all()
    return render(request, 'products/pages/home_page.html', context)


def product_detail(request, product_pk):
    context = {'active_page': "home_page", 'header_bucket_counter': header_bucket_counter(request)}
    product = get_object_or_404(Product, pk=product_pk)
    images = Image.objects.filter(product_id=product_pk)
    # TODO: change pk to id in all files
    context['product'] = product
    context['images'] = images
    return render(request, 'products/pages/product_detail.html', context)


def contacts_page(request):
    context = {'active_page': "contacts_page", 'header_bucket_counter': header_bucket_counter(request)}
    test_string = "This string was rendered from views.contacts_page()"
    context['test_string'] = test_string
    return render(request, 'products/pages/about_us.html', context)


def login_page(request):
    context = {'header_bucket_counter': header_bucket_counter(request)}
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
            return redirect(product_list)
        else:
            # TODO: raise error if no user or incorrect password
            context['error'] = 'User not found!'
    context['active_page'] = "login_page"
    return render(request, 'products/pages/login_page.html', context)


def logout(request):
    django_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def user_page(request):
    context = {'active_page': "user_page"}
    context['test_string'] = "USER PAGE"
    return render(request, 'products/pages/user_page.html', context)


@require_http_methods(["GET", "POST"])
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
            return redirect(product_list)
    else:
        user_form = UserSignupForm()
        customer_form = CustomerSignupForm()
    return render(request, 'products/pages/signup_page.html', {
        'user_form': user_form,
        'customer_form': customer_form,
        'active_page': "signup_page",
        'header_bucket_counter': header_bucket_counter(request),
    }
                  )


def bucket(request):
    context = {'active_page': "bucket", 'header_bucket_counter': header_bucket_counter(request)}
    user_id = request.session.get('_auth_user_id')
    if user_id:
        try:
            personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
            bucket_ids = personal_bucket.user_bucket['products_in_bucket']
        except UserBucketProducts.DoesNotExist:
            bucket_ids = None

    else:
        bucket_ids = request.session.get('products')
    product_quantity = {}
    try:
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
        if request.user.is_authenticated:
            user_id = request.session.get('_auth_user_id')
            bucket_updater(user_id, product_id)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                products = request.session['products']
                products.append(product_id)
                request.session['products'] = products
            except KeyError:
                request.session['products'] = [product_id]
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(product_list)


def remove_from_bucket(request, product_pk):
    user_id = request.session.get('_auth_user_id')

    def cleare_list(bucket_products, new_bucket_list):
        for bucket_id in bucket_products:
            if bucket_id == product_pk:
                new_bucket_list.remove(bucket_id)
        return new_bucket_list

    if user_id:
        personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
        bucket_products = personal_bucket.user_bucket['products_in_bucket']
        new_bucket_list = bucket_products.copy()
        personal_bucket.user_bucket['products_in_bucket'] = cleare_list(bucket_products, new_bucket_list)
        personal_bucket.save()
    else:
        bucket_products = request.session.get('products')
        new_bucket_list = bucket_products.copy()
        request.session['products'] = cleare_list(bucket_products, new_bucket_list)
    return redirect(bucket)


def more_to_bucket(request, product_pk):
    user_id = request.session.get('_auth_user_id')
    if user_id:
        personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
        personal_bucket.user_bucket['products_in_bucket'].append(product_pk)
        personal_bucket.save()
    else:
        product_in_bucket = request.session['products']
        product_in_bucket.append(product_pk)
        request.session['products'] = product_in_bucket
    return redirect(bucket)


def less_to_bucket(request, product_pk):
    user_id = request.session.get('_auth_user_id')
    if user_id:
        personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
        personal_bucket.user_bucket['products_in_bucket'].remove(product_pk)
        personal_bucket.save()
    else:
        product_in_bucket = request.session['products']
        product_in_bucket.remove(product_pk)
        request.session['products'] = product_in_bucket
    return redirect(bucket)

