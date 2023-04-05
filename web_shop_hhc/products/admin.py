from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import User
from .models import *


class ImageInline(admin.StackedInline):
    model = Image
    extra = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['id', 'title', 'available_quantity', 'price', 'is_sale', 'discount', ]


class CustomerInline(admin.StackedInline):
    model = Customer


class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline, )

    # pass


# admin.site.unregister(User)
# admin.site.register(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Image)
admin.site.register(Comments)
