from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', product_list),
    path('about_us/', contacts_page),
    path('login/', login_page),
    path('signup/', signup),
    path('logout/', login_page),
    path('user/', user_page),
    path('bucket/', bucket),
    path('product_detail/<int:product_pk>/', product_detail),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
