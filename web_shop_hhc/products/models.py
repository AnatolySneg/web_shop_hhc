import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.db.utils import IntegrityError
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_type(self):
        return Type.objects.filter(category=self)


class Type(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_products(self):
        return Product.objects.filter(type=self)


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    price = models.FloatField()
    is_sale = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True, null=True)
    available_quantity = models.PositiveIntegerField(default=0)
    type = models.ForeignKey(Type, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, product id - {self.id}'

    def get_images(self):
        return Image.objects.filter(product=self)

    def get_title_image(self):
        return Image.objects.get(product=self, title_image=True)

    def get_price(self):
        if self.is_sale:
            return self.price * (100 - self.discount) / 100
        return self.price

    def get_available_status(self):
        if self.available_quantity <= 0:
            return "not_in_stock"
        elif 0 < self.available_quantity <= 10:
            return "running_out"
        else:
            return "in_stock"

    def average_rating(self):
        product_rating = Rating.objects.filter(product=self)
        return product_rating.aggregate(Avg('rate'))['rate__avg'] or 0

    def get_comments(self):
        return Comments.objects.filter(product=self).order_by('-published_date')


"""
Methods Image.save() and Image.delete() was made for making only one title image for each product. 
Also, it working, when we add new image, deleting title image or changing title image amon other 
product images, from Django admin panel. 
"""


class Image(models.Model):
    image = models.ImageField(upload_to='upload/')
    title_image = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'image id - {self.id}'

    def save(self, *args, **kwargs):
        product_images = Image.objects.filter(product=self.product)
        if self.title_image:
            try:
                previous_title_image = product_images.get(title_image=True)
                previous_title_image.title_image = False
                super(Image, previous_title_image).save()
            except ObjectDoesNotExist:
                pass
        if not product_images and not self.title_image:
            self.title_image = True
        super(Image, self).save()

    def delete(self, *args, **kwargs):
        product_images = Image.objects.filter(product=self.product)
        if len(product_images) > 1 and self.title_image:
            try:
                non_title_images = product_images.filter(title_image=False)
                non_title_images[0].title_image = True
                super(Image, non_title_images[0]).save()
            except ObjectDoesNotExist:
                pass
        super(Image, self).delete(args, kwargs)


class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True, max_length=1000)


def comment_saver(product_id, user_id, comment):
    comment = Comments.objects.create(product_id=product_id, author_id=user_id, comment=comment)
    comment.save()


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


def rate_updater(product_id, user_id, rate_value):
    rating, created = Rating.objects.get_or_create(product_id=product_id, author_id=user_id)
    rating.rate = rate_value
    rating.save()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True, region="UA")


class SecretString(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    secret_string = models.CharField(max_length=50)
    creation_time = models.DateTimeField(auto_now=True)


def secret_string_saver(secret_string, user_id):
    secret = SecretString(user_id=user_id, secret_string=secret_string)
    try:
        secret.save()
    except IntegrityError:
        secret_raw = SecretString.objects.get(user_id=user_id)
        secret_raw.secret_string = secret_string
        secret_raw.creation_time = datetime.datetime.now()
        secret_raw.save()


class ShopContacts(models.Model):
    service = models.CharField(max_length=50, null=True)
    email = models.EmailField(default=None, blank=True, null=True)
    email_2 = models.EmailField(default=None, blank=True, null=True)
    email_3 = models.EmailField(default=None, blank=True, null=True)
    email_4 = models.EmailField(default=None, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, region="UA", blank=True, null=True)
    phone_number_2 = PhoneNumberField(unique=True, region="UA", blank=True, null=True)
    phone_number_3 = PhoneNumberField(unique=True, region="UA", blank=True, null=True)
    phone_number_4 = PhoneNumberField(unique=True, region="UA", blank=True, null=True)

    def __str__(self):
        return '{} contacts.'.format(self.service)


class ShopAddress(models.Model):
    address = models.CharField(max_length=100)

    def __str__(self):
        return 'shop address: {}.'.format(self.address)


class UserBucketProducts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_bucket = models.JSONField(null=True)

    def __str__(self):
        return "{}'s bucket".format(self.user.username)


class Order(models.Model):
    NEW = 'NEW'
    CONFIRM = 'CONFIRM'
    EXECUTION = 'EXECUTION'
    COMPLETE = 'COMPLETE'
    REJECT = 'REJECT'

    ORDER_STATUS = [
        (NEW, 'New order'),
        (CONFIRM, 'Confirmed order'),
        (EXECUTION, 'Executing order'),
        (COMPLETE, 'Completed order'),
        (REJECT, 'Rejected order'),
    ]

    ONLINE_PAYMENT = 'ONLINE_PAYMENT'
    PAYMENT_BY_CARD_ON_RECEIPT = 'PAYMENT_BY_CARD'
    PAYMENT_IN_CASH_ON_RECEIPT = 'PAYMENT_IN_CASH'
    CASH_ON_DELIVERY = 'CASH_ON_DELIVERY'

    PAYMENT_OPTIONS = [
        (ONLINE_PAYMENT, 'Online payment'),
        (PAYMENT_BY_CARD_ON_RECEIPT, 'Payment by card upon receipt'),
        (PAYMENT_IN_CASH_ON_RECEIPT, 'Cash payment'),
        (CASH_ON_DELIVERY, 'Cash on delivery'),
    ]

    PICKUP = 'PICKUP'
    STORE_COURIER = 'STORE_COURIER'
    DELIVERY_SERVICE_1 = 'DELIVERY_SERVICE_1'
    DELIVERY_SERVICE_2 = 'DELIVERY_SERVICE_2'
    DELIVERY_SERVICE_3 = 'DELIVERY_SERVICE_3'

    DELIVERY_OPTIONS = [
        (PICKUP, 'Pickup'),
        (STORE_COURIER, 'Store courier'),
        (DELIVERY_SERVICE_1, 'Delivery service 1'),
        (DELIVERY_SERVICE_2, 'Delivery service 2'),
        (DELIVERY_SERVICE_3, 'Delivery service 3'),
    ]

    status = models.CharField(choices=ORDER_STATUS, default=NEW, max_length=50)
    created_date = models.DateTimeField(auto_now=True)
    products = models.JSONField('Products in order', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(default=None)
    phone_number = PhoneNumberField(region="UA")
    delivery_option = models.CharField(choices=DELIVERY_OPTIONS, default=PICKUP, max_length=50)

    payment_option = models.CharField(choices=PAYMENT_OPTIONS, default=ONLINE_PAYMENT, max_length=50)
    destination_region = models.CharField(max_length=100, blank=True, null=True)
    destination_country = models.CharField(max_length=50, blank=True, null=True)
    destination_delivery_service = models.CharField(max_length=100, blank=True, null=True)
    destination_street = models.CharField(max_length=100, blank=True, null=True)
    destination_house = models.CharField(max_length=20, blank=True, null=True)
    destination_apartment = models.CharField(max_length=20, blank=True, null=True)
    order_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{}, user - {}, full name: {} {}, delivery option: {}'.format(self.status, self.user,
                                                                             self.first_name, self.last_name,
                                                                             self.delivery_option)

    def get_products_and_quantity(self):
        product_quantity = self.products['products']
        products_queryset = Product.objects.filter(id__in=product_quantity).order_by('id')
        product_obj_quantity_dict = {}
        for product in products_queryset:
            product_obj_quantity_dict[product] = self.products['products'][str(product.id)]
        return product_obj_quantity_dict

    def save(self, *args, **kwargs):
        if self.status == self.REJECT:
            product_db_quantity_updater(product_quantity=self.products['products'], rejected_order=True)
        super(Order, self).save(*args, **kwargs)


def product_db_quantity_updater(product_quantity, rejected_order=False):
    products = Product.objects.filter(id__in=product_quantity)
    if not rejected_order:
        for product in products:
            product.available_quantity -= product_quantity[str(product.id)]
            product.save()
    else:
        for product in products:
            product.available_quantity += product_quantity[str(product.id)]
            product.save()


def new_order_updater(initiated_order, user, product_quantity):
    new_order = initiated_order.save(commit=False)
    new_order.created_date = timezone.now()
    bucket_products = product_quantity
    new_order.products = {'products': bucket_products}
    if user.is_authenticated:
        new_order.user = user
    new_order.save()
    return new_order


def confirm_order_updater(order_form):
    confirm_order = order_form.save(commit=False)
    confirm_order.status = Order.CONFIRM
    confirm_order.order_date = timezone.now()
    confirm_order.save()
    product_db_quantity_updater(confirm_order.products['products'])
    return confirm_order
