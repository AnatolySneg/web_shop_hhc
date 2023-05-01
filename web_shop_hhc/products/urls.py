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
    path('bucket/', bucket),
    path('add_to_bucket/<int:product_id>', add_to_bucket),
    path('more_to_bucket/<int:product_pk>', more_to_bucket),
    path('less_to_bucket/<int:product_pk>', less_to_bucket),
    path('remove_from_bucket/<int:product_pk>', remove_from_bucket),
]

urlpatterns += bucket_urls

order_urls = [
    path('order/', order),
    path('order/<int:order_id>', order_confirm),
    path('order_page/<int:confirm_order_id>', order_page),
    # path('add_to_user_bucket/<int:product_id>', add_to_user_bucket),
    # path('more_to_bucket/<int:product_pk>', more_to_bucket),
    # path('less_to_bucket/<int:product_pk>', less_to_bucket),
    # path('remove_from_bucket/<int:product_pk>', remove_from_bucket),
]


urlpatterns += order_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
