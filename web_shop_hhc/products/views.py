from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Category, Type, Product, Order, Image, ShopContacts, ShopAddress, rate_updater, \
    comment_saver, new_order_updater, confirm_order_updater
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .forms import UserSignupForm, CustomerSignupForm, CustomerLoginForm, CustomerEmailForm, ResetPasswordForm, \
    OrderFirstCreationForm
from django.views.decorators.http import require_GET, require_http_methods
from .logic.products import Bucket, Ordering
from .logic.text_message import RessetPasswordMail
from .logic.customers import PasswordReset
from .logic.list_products import ProductListing
from django.utils.datastructures import MultiValueDictKeyError


@require_GET
def product_list(request):
    context = {'active_page': "home_page",
               'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}

    category_id = request.GET.get('category')
    type_id = request.GET.get('type')
    search_value = request.GET.get('search')
    product_sorting_value = request.GET.get('sorting')

    context["category"] = None
    if category_id:
        category_obj = Category.objects.get(id=category_id)
        context["category"] = category_obj

    context["type"] = None
    if type_id:
        type_obj = Type.objects.get(id=type_id)
        context["type"] = type_obj

    product_sorting = None
    if product_sorting_value:
        product_sorting = product_sorting_value

    search = None
    if search_value:
        search = search_value
        category_id = None
        type_id = None

    products = ProductListing(category_id=category_id, type_id=type_id,
                              product_sorting=product_sorting,
                              search=search)
    context['products'] = products.sorted_product_list_available
    context['out_of_stock'] = products.sorted_product_list_unavailable
    context['search'] = search
    context['sorting_options'] = products.sorting_option.keys()
    context['selected_sorting_option'] = product_sorting
    context["categories"] = Category.objects.all()

    return render(request, 'products/pages/home_page.html', context)


@require_GET
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'active_page': "home_page",
               'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}
    images = Image.objects.filter(product_id=product_id)
    context['product'] = product
    context['images'] = images
    return render(request, 'products/pages/product_detail.html', context)


@require_GET
def set_rating(request, product_id):
    try:
        rate_value = int(request.GET['rate'])
        user_id = request.user.id
        rate_updater(product_id=product_id, user_id=user_id, rate_value=rate_value)
    except MultiValueDictKeyError:
        pass
    except ValueError:
        pass
    except KeyError:
        pass
    return redirect(product_detail, product_id=product_id)


@require_GET
def leave_a_comment(request, product_id):
    comment = request.GET.get('comment')
    user_id = request.user.id
    comment_saver(product_id=product_id, user_id=user_id, comment=comment)
    return redirect(product_detail, product_id=product_id)


@require_GET
def contacts_page(request):
    context = {'active_page': "contacts_page",
               'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}
    shop_addresses = ShopAddress.objects.all()
    contacts = ShopContacts.objects.all()
    context['shop_addresses'] = shop_addresses
    context['contacts'] = contacts
    return render(request, 'products/pages/about_us.html', context)


@require_http_methods(["GET", "POST"])
def login_page(request):
    context = {'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}
    if request.method == "POST":
        login_form = CustomerLoginForm(request.POST)
        if login_form.is_valid():
            customer = login_form.save(commit=False)
            username = User.objects.get(email=customer.email)
            password = customer.password
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                django_login(request, auth_user)
                return redirect(product_list)

    login_form = CustomerLoginForm()
    context['login_form'] = login_form
    context['active_page'] = "login_page"
    return render(request, 'products/pages/login_page.html', context)


@require_GET
def logout(request):
    django_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


@require_http_methods(["GET", "POST"])
def forgot_password_page(request):
    context = {'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}
    if request.method == "POST":
        email_form = CustomerEmailForm(request.POST)
        if email_form.is_valid():
            customer_email = email_form.save(commit=False)
            customer = User.objects.get(email=customer_email.email)
            return redirect(get_reset_password_link, customer_id=customer.id)

    email_form = CustomerEmailForm()
    context['email_form'] = email_form
    context['active_page'] = "login_page"
    return render(request, 'products/pages/forgot_password.html', context)


@require_GET
def get_reset_password_link(request, customer_id):
    context = {'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}
    path = request.build_absolute_uri()
    instance = RessetPasswordMail(customer_id=customer_id, path=path)
    instance.send()
    email = instance.customer.email
    context['email'] = email
    return render(request, 'products/pages/reset_instructions.html', context)


@require_http_methods(["GET", "POST"])
def reset_password(request, secret_string):
    context = {'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}
    context['active_page'] = "login_page"
    pas = PasswordReset(secret_string=secret_string)
    if not pas.secret_is_valid:
        return redirect(product_list)
    if request.method == "POST":
        password_form = ResetPasswordForm(data=request.POST, user=pas.user_reset_password)
        if password_form.is_valid():
            password_form.save()
            return render(request, 'products/pages/password_reset_success.html', context)

    password_form = ResetPasswordForm(user=pas.user_reset_password)
    context['password_form'] = password_form
    return render(request, 'products/pages/reset_password_form.html', context)


@require_GET
def user_page(request):
    context = {'active_page': "user_page"}
    orders_query = Order.objects.filter(user_id=request.user.id).order_by('-order_date')
    context['orders'] = orders_query
    return render(request, 'products/pages/user_page.html', context)


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
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
    user_form = UserSignupForm()
    customer_form = CustomerSignupForm()
    return render(request, 'products/pages/signup_page.html', {
        'user_form': user_form,
        'customer_form': customer_form,
        'active_page': "signup_page",
        'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products')),
    }
                  )


@require_GET
def bucket_page(request):
    bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
    context = {'active_page': "bucket", 'header_bucket_counter': len(bucket.product_ids)}
    if bucket.product_ids:
        bucket_products = Product.objects.filter(id__in=bucket.product_ids)
    else:
        bucket_products = []
    request.session['products'] = bucket.product_ids
    context['bucket_products'] = bucket_products
    context['product_quantity'] = bucket.product_quantity
    context['product_price'] = bucket.product_quantity_price
    context['total_price'] = bucket.product_quantity_total_price
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
def order_new(request):
    if request.method == 'POST':
        initiated_order = OrderFirstCreationForm(request.POST)
        if initiated_order.is_valid():
            bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
            new_order = new_order_updater(initiated_order, request.user, bucket.product_quantity)
            return redirect(order_confirm, order_id=new_order.id)
    context = {'initiated_order_form': OrderFirstCreationForm(), 'active_page': "bucket",
               'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}
    return render(request, 'products/pages/initiate_order.html', context)


@require_http_methods(["GET", "POST"])
def order_confirm(request, order_id):
    new_order = Ordering(order_id)
    form = new_order.get_optional_form()
    if request.method == 'POST':
        order_form = form(request.POST, instance=new_order.order)
        if order_form.is_valid():
            confirm_order = confirm_order_updater(order_form)
            return redirect(order_page, confirm_order_id=confirm_order.id)
    else:
        order_form = form(instance=new_order.order)
    context = {'order_options_form': order_form, 'active_page': "bucket",
               'header_bucket_counter': Bucket.header_bucket_counter(request.session.get('products'))}
    return render(request, 'products/pages/order_confirm.html', context)


@require_GET
def order_page(request, confirm_order_id):
    bucket = Bucket(user_id=request.user.id, session_products_ids=request.session.get('products'))
    bucket.clear()
    confirmed_order = Ordering(confirm_order_id)
    order = confirmed_order.order
    confirmed_order.send_order_mail_report()

    request.session['products_for_order'] = bucket.product_quantity
    request.session['products'] = bucket.product_ids
    context = {'active_page': "bucket", 'header_bucket_counter': len(bucket.product_ids),
               "order": order}
    return render(request, 'products/pages/order_page.html', context)
