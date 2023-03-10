from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Comments)

