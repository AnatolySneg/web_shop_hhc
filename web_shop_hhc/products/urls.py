from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', product_list),
    path('category_product_list/<int:category_id>', product_list),
    path('type_product_list/<int:type_id>', product_list),
    path('search_product_list/', product_list),
    path('about_us/', contacts_page),
    path('product_detail/<int:product_id>/', product_detail),
    path('product_detail/<int:product_id>/set_rating/', set_rating),
    path('product_detail/<int:product_id>/leave_a_comment/', leave_a_comment),
]

user_urls = [
    path('signup/', signup),
    path('login/', login_page, name='login'),
    path('logout/', logout),
    path('forgot_password/', forgot_password_page),
    path('get_reset_password_link/<int:customer_id>', get_reset_password_link),
    path('reset_token/<str:secret_string>/', reset_password),
    path('user/', user_page),
]

urlpatterns += user_urls

bucket_urls = [
    path('bucket/', bucket_page),
    path('add_to_bucket/<int:product_id>', add_to_bucket),
    path('more_to_bucket/<int:product_id>', more_to_bucket),
    path('less_to_bucket/<int:product_id>', less_to_bucket),
    path('remove_from_bucket/<int:product_id>', remove_from_bucket),
    path('clear_bucket/', clear_bucket),
]

urlpatterns += bucket_urls

order_urls = [
    path('order/', order_new),
    path('order/<int:order_id>', order_confirm),
    path('order_page/<int:confirm_order_id>', order_page),
]

urlpatterns += order_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
