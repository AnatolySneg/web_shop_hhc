from ..models import UserBucketProducts, Order, Product
from ..forms import OrderSecondPickupCreationForm, OrderSecondCourierCreationForm, OrderSecondDeliveryCreationForm
from django.core.mail import send_mail
from django.conf import settings


class Bucket:
    def _get_product_ids(self, user_id):
        try:
            personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
            self.product_ids = personal_bucket.user_bucket['products_in_bucket']
        except UserBucketProducts.DoesNotExist:
            self.product_ids = []

    def _quantity(self):
        product_quantity = {}
        for id_number in self.product_ids:
            product_quantity[id_number] = self.product_ids.count(id_number)
        return product_quantity

    def _update_user_bucket(self):
        try:
            personal_bucket = UserBucketProducts.objects.get(user_id=self.user_id)
            personal_bucket.user_bucket['products_in_bucket'] = self.product_ids
            personal_bucket.save()
        except UserBucketProducts.DoesNotExist:
            UserBucketProducts.objects.create(user_id=self.user_id,
                                              user_bucket={'products_in_bucket': self.product_ids})

    def _refresh_bucket_state(self):
        self.product_quantity = self._quantity()
        if self.user_id:
            self._update_user_bucket()

    # TODO: refactor of data type, for saving products in bucket.
    """
    user_id - incoming integer data-type, if user is authenticate, or None type if else.
    session_products_ids - incoming list data-type, if bucket was updated at least once for current session, 
    or None type if else.
    """

    def __init__(self, user_id, session_products_ids):
        self.user_id = user_id
        if self.user_id:
            self._get_product_ids(self.user_id)
        else:
            self.product_ids = session_products_ids or []
        self.product_quantity = self._quantity()

    def add_product(self, product_id):
        self.product_ids.append(product_id)
        self._refresh_bucket_state()

    def decrease_product(self, product_id):
        self.product_ids.remove(product_id)
        self._refresh_bucket_state()

    def remove_products(self, product_id):
        new_product_ids = [product for product in self.product_ids if product != product_id]
        self.product_ids = new_product_ids
        self._refresh_bucket_state()

    def clear(self):
        self.product_ids = []
        self._refresh_bucket_state()

    @staticmethod
    def header_bucket_counter(products_in_bucket):
        if products_in_bucket:
            return len(products_in_bucket)
        return 0


class Ordering:
    def _get_delivery_option(self):
        order = Order.objects.get(id=self.order_id)
        self.order = order
        self.delivery_option = order.delivery_option

    def __init__(self, order_id):
        self.order_id = order_id
        self._get_delivery_option()

    def get_optional_form(self):
        order_options = {
            Order.PICKUP: OrderSecondPickupCreationForm,
            Order.STORE_COURIER: OrderSecondCourierCreationForm,
            Order.DELIVERY_SERVICE_1: OrderSecondDeliveryCreationForm,
            Order.DELIVERY_SERVICE_2: OrderSecondDeliveryCreationForm,
            Order.DELIVERY_SERVICE_3: OrderSecondDeliveryCreationForm,
        }
        return order_options[self.delivery_option]

    def send_order_mail_report(self):
        text = 'Thank you, order №{order_id} accepted:'.format(order_id=self.order_id)
        id_quantity = self.order.products['products']
        products = Product.objects.filter(id__in=id_quantity)

        for id in id_quantity:
            product = products.get(id=id)
            text += '\n\t*\t{title} - {quantity} units.'.format(title=product.title, quantity=id_quantity[id])
        text += '\n\nOur manager will contact you shortly.'
        text += '\n\thttp://127.0.0.1:8000/about_us/'
        send_mail(
            subject="Order №{} in Web shop HHC".format(self.order_id),
            message=text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )
