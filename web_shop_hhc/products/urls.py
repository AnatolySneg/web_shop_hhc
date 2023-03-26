from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', product_list),
    path('about_us/', contacts_page),
    path('login/', login_page),
    path('logout/', login_page),
    path('user/', user_page),
    path('bucket/', bucket),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
