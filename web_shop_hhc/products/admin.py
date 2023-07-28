from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import User
from .models import *


class ImageInline(admin.StackedInline):
    model = Image
    extra = 5


class RatingInline(admin.StackedInline):
    model = Rating
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline, RatingInline]
    list_display = ['id', 'title', 'available_quantity', 'price', 'is_sale', 'discount', ]


# class ShopAddress(admin.ModelAdmin):
#     list_display = ['id', 'address']
#
#
# class ShopContacts(admin.ModelAdmin):
#     list_display = ['id', 'email', 'phone_number']


class CustomerInline(admin.StackedInline):
    model = Customer


class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline, )


# class UserBucketProductsAdmin(admin.ModelAdmin):
#     list_display = ['id', '__str__', 'quantity']



admin.site.unregister(User)
# admin.site.register(User)
admin.site.register(User, UserAdmin)
admin.site.register(Order)
admin.site.register(UserBucketProducts)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShopContacts)
admin.site.register(ShopAddress)
# admin.site.register(UserBucketProducts, UserBucketProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Image)
admin.site.register(Rating)
admin.site.register(Comments)
