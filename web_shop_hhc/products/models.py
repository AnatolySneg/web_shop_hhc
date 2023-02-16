from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
    image = models.ImageField(upload_to='upload/')
    # https://www.youtube.com/watch?v=fsVY66QBhwM for finishing.
    available_quantity = models.IntegerField(default=0)
    type = models.ForeignKey(Type, default=None, on_delete=models.CASCADE)
    # Add Type field!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def __str__(self):
        return self.title


class Comments (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)
    author = models.CharField(default='DefaultAUTHOR', max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    # Change to Author from users model, when created!!!!!!!!
    comment = models.TextField(blank=True, max_length=1000) # Comments should be approved by moderator !!!!

# ADD USERS, COMMENTS, purchase history, product rating!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
