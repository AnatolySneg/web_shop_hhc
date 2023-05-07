from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import *
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .forms import *
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.utils import timezone
from .logic.products import Bucket
from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
@require_GET
def product_list(request):
    context = {'active_page': "home_page", 'header_bucket_counter': header_bucket_counter(request)}
    # TODO: Fielters and Sorting products !!!!
    context['products'] = Product.objects.all()
    print(request.user)
    print(request.user.id)
    return render(request, 'products/pages/home_page.html', context)


@require_GET
def product_detail(request, product_pk):
    context = {'active_page': "home_page", 'header_bucket_counter': header_bucket_counter(request)}
    product = get_object_or_404(Product, pk=product_pk)
    images = Image.objects.filter(product_id=product_pk)
    # TODO: change pk to id in all files
    context['product'] = product
    context['images'] = images
    return render(request, 'products/pages/product_detail.html', context)


@require_GET
def contacts_page(request):
    context = {'active_page': "contacts_page", 'header_bucket_counter': header_bucket_counter(request)}
    test_string = "This string was rendered from views.contacts_page()"
    context['test_string'] = test_string
    return render(request, 'products/pages/about_us.html', context)


@require_http_methods(["GET", "POST"])
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


@require_GET
def logout(request):
    django_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


@require_GET
def user_page(request):
    context = {'active_page': "user_page"}
    context['test_string'] = "USER PAGE"
    return render(request, 'products/pages/user_page.html', context)


@require_http_methods(["GET", "POST"])
def signup(request):
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


@require_GET
def bucket_page(request):
    context = {'active_page': "bucket", 'header_bucket_counter': header_bucket_counter(request)}
    bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
    if bucket.product_ids:
        bucket_products = Product.objects.filter(id__in=bucket.product_ids)
    else:
        bucket_products = []
    request.session['products'] = bucket.product_ids
    context['bucket_products'] = bucket_products
    context['product_quantity'] = bucket.product_quantity
    # TODO: maybe should put below row in adding or removing views
    # request.session['products_for_order'] = bucket.product_quantity
    return render(request, 'products/pages/bucket_page.html', context)


@require_GET
def add_to_bucket(request, product_id):
    if request.META.get('HTTP_REFERER'):
        bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
        bucket.add_product(product_id)
        request.session['products'] = bucket.product_ids
        request.session['products_for_order'] = bucket.product_quantity
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(product_list)


@require_GET
def remove_from_bucket(request, product_id):
    bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
    bucket.remove_products(product_id)
    request.session['products'] = bucket.product_ids
    request.session['products_for_order'] = bucket.product_quantity
    return redirect(bucket_page)


@require_GET
def more_to_bucket(request, product_id):
    bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
    bucket.add_product(product_id)
    request.session['products'] = bucket.product_ids
    request.session['products_for_order'] = bucket.product_quantity
    return redirect(bucket_page)


@require_GET
def less_to_bucket(request, product_id):
    bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
    bucket.decrease_product(product_id)
    request.session['products'] = bucket.product_ids
    request.session['products_for_order'] = bucket.product_quantity
    return redirect(bucket_page)


@require_GET
def clear_bucket(request):
    bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
    bucket.clear()
    request.session['products'] = bucket.product_ids
    request.session['products_for_order'] = bucket.product_quantity
    return redirect(bucket_page)


@require_http_methods(["GET", "POST"])
def order(request):
    context = {}
    if request.method == 'POST':
        initiated_order = OrderFirstCreationForm(request.POST)
        if initiated_order.is_valid():
            order = initiated_order.save(commit=False)
            order.created_date = timezone.now()
            bucket_products = request.session.get('products_for_order')
            order.products = {'products': bucket_products}
            if request.user.is_authenticated:
                user = request.user
                order.user = user
            order.save()
            return redirect(order_confirm, order_id=order.id)
    else:
        context = {'initiated_order_form': OrderFirstCreationForm(), 'active_page': "bucket",
                   'header_bucket_counter': header_bucket_counter(request)}
    return render(request, 'products/pages/initiate_order.html', context)


@require_http_methods(["GET", "POST"])
def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        if order.delivery_option == Order.PICKUP:
            order_options = OrderSecondPickupCreationForm(request.POST, instance=order)
        elif order.delivery_option == Order.STORE_COURIER:
            order_options = OrderSecondCourierCreationForm(request.POST, instance=order)
        else:
            order_options = OrderSecondDeliveryCreationForm(request.POST, instance=order)
        if order_options.is_valid():
            confirm_order = order_options.save(commit=False)
            confirm_order.status = Order.CONFIRM
            confirm_order.order_date = timezone.now()
            confirm_order.save()
        return redirect(order_page, confirm_order_id=confirm_order.id)
    else:
        if order.delivery_option == Order.PICKUP:
            order_options = OrderSecondPickupCreationForm(instance=order)
        elif order.delivery_option == Order.STORE_COURIER:
            order_options = OrderSecondCourierCreationForm(instance=order)
        else:
            order_options = OrderSecondDeliveryCreationForm(instance=order)
        context = {'order_options_form': order_options, 'active_page': "bucket",
                   'header_bucket_counter': header_bucket_counter(request)}
    return render(request, 'products/pages/order_confirm.html', context)


@require_GET
def order_page(request, confirm_order_id):
    if request.user.is_authenticated:
        UserBucketProducts.objects.get(user_id=request.user.id).delete()
    else:
        request.session['products_for_order'] = {}
        request.session['products'] = []
    order = Order.objects.get(id=confirm_order_id)
    context = {'active_page': "bucket", 'header_bucket_counter': header_bucket_counter(request),
               "order": order}
    return render(request, 'products/pages/order_page.html', context)
