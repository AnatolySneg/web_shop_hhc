from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', product_list),
    path('about_us/', contacts_page),
    path('login/', login_page, name='login'),
    path('signup/', signup),
    path('logout/', logout),
    path('user/', user_page),
    path('bucket/', bucket),
    path('product_detail/<int:product_pk>/', product_detail),
]

bucket_urls = [
    path('add_to_bucket/<int:product_id>', add_to_bucket),
]

urlpatterns += bucket_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
