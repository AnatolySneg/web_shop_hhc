from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    price = models.FloatField()
    is_sale = models.BooleanField(default=False)
    discount = models.IntegerField(blank=True, null=True)
    # TODO: Make positive integer field
    available_quantity = models.IntegerField(default=0)
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
        list_image_objects = Image.objects.filter(product=self.product)
        if self in list_image_objects or (self not in list_image_objects and self.title_image):
            for image in list_image_objects:
                image.title_image = False
                super(Image, image).save(args, **kwargs)
            self.title_image = True
            print("save method, {} is updating or creating new wis flag True".format(self))
        elif not list_image_objects:
            self.title_image = True
            print("save method, {} is creating as a first obj".format(self))
        else:
            self.title_image = False
            print("save method, {} is creating as another with False flag".format(self))
        super(Image, self).save(*args, **kwargs)
        print("hi from Save method", kwargs, self)

    def delete(self, *args, **kwargs):
        list_image_objects = Image.objects.filter(product=self.product)
        if len(list_image_objects) >= 1 and self.title_image:
            for image in list_image_objects:
                if image is not self:
                    image.title_image = True
                    super(Image, image).save()
                    print("super save {} in delete".format(image.id))
                    break
        super(Image, self).delete(args, kwargs)


class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)
    author = models.CharField(default='DefaultAUTHOR', max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    # TODO: Change to Author from users model, when created!!!!!!!!
    comment = models.TextField(blank=True, max_length=1000)  # Comments should be approved by moderator !!!!


# TODO: ADD USERS, COMMENTS, purchase history, product rating!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True, region="UA")


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
    return confirm_order
