from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ObjectDoesNotExist


class SignupError(Exception):
    "Raise when, during signing up, user entered data which already exists in database."
    pass


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
    available_quantity = models.IntegerField(default=0)
    type = models.ForeignKey(Type, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} | product id - {self.id}'

    def get_images(self):
        return Image.objects.filter(product=self)

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
    birth_date = models.DateField(null=True, blank=True)


class UserBucketProducts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_bucket = models.JSONField(null=True)

    def __str__(self):
        return "{}'s bucket".format(self.user.username)


# TODO: make below functions, UserBucketProducts methods also in view.
def bucket_updater(user_id, product_id):
    try:
        personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
        personal_bucket.user_bucket['products_in_bucket'].append(product_id)
        personal_bucket.save()
    except UserBucketProducts.DoesNotExist:
        UserBucketProducts.objects.create(user_id=user_id, user_bucket={'products_in_bucket': [product_id]})


def header_bucket_counter(request):
    user_id = request.session.get('_auth_user_id')
    if user_id:
        try:
            bucket_object = UserBucketProducts.objects.get(user_id=user_id)
            products_bucket_quantity = len(bucket_object.user_bucket['products_in_bucket'])
        except UserBucketProducts.DoesNotExist:
            products_bucket_quantity = 0
    else:
        try:
            products_bucket_quantity = len(request.session.get('products'))
        except Exception:
            products_bucket_quantity = 0
    return products_bucket_quantity



# class Order(models.Model):
#     status = []
#     order_date = ''
#     relation_user = ''
#     relation_product = ''
#     pass
