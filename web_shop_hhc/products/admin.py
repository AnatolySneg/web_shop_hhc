from django.contrib import admin
from .models import *


class ImageInline(admin.StackedInline):
    model = Image
    extra = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['title', 'id']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Image)
admin.site.register(Comments)
