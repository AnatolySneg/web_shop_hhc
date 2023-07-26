from ..models import UserBucketProducts, Order, Product
from ..forms import OrderSecondPickupCreationForm, OrderSecondCourierCreationForm, OrderSecondDeliveryCreationForm
from .text_message import OrderEmail


class Bucket:
    def _get_product_ids(self, user_id):
        try:
            personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
            self.product_ids = personal_bucket.user_bucket['products_in_bucket']
        except UserBucketProducts.DoesNotExist:
            self.product_ids = []

    def _get_product_prices(self, product_id, price):
        self.product_quantity_price[product_id] = price

    def _correction_available_ids(self, product_id, available):
        while self.product_ids.count(product_id) != available:
            self.product_ids.remove(product_id)

    def _get_possible_quantity(self):
        product_quantity = {}
        available_product_quantity = {}
        for id_number in self.product_ids:
            product_quantity[id_number] = self.product_ids.count(id_number)
        for id_value in product_quantity:
            product = Product.objects.get(id=id_value)
            available_quantity = product.available_quantity
            self._get_product_prices(product_id=id_value, price=product.get_price())
            if 0 < available_quantity < product_quantity[id_value]:
                available_product_quantity[id_value] = available_quantity
                self._correction_available_ids(product_id=id_value, available=available_quantity)
            elif 0 >= available_quantity:
                self._correction_available_ids(product_id=id_value, available=0)
            else:
                available_product_quantity[id_value] = product_quantity[id_value]

        return available_product_quantity

    def _update_user_bucket(self):
        try:
            personal_bucket = UserBucketProducts.objects.get(user_id=self.user_id)
            personal_bucket.user_bucket['products_in_bucket'] = self.product_ids
            personal_bucket.save()
        except UserBucketProducts.DoesNotExist:
            UserBucketProducts.objects.create(user_id=self.user_id,
                                              user_bucket={'products_in_bucket': self.product_ids})

    def _refresh_bucket_state(self):
        self.product_quantity = self._get_possible_quantity()
        if self.user_id:
            self._update_user_bucket()

    def _get_total_price(self):
        total_price = 0
        for product_id in self.product_quantity:
            total_price += self.product_quantity_price[product_id] * self.product_quantity[product_id]
        return total_price

    # TODO: refactor of data type, for saving products in bucket.
    """
    user_id - incoming integer data-type, if user is authenticate, or user=None type if else.
    session_products_ids - incoming list data-type, if bucket was updated at least once for current session, 
    or None type if else.
    """

    def __init__(self, user_id, session_products_ids):
        self.user_id = user_id
        if self.user_id:
            self._get_product_ids(self.user_id)
        else:
            self.product_ids = session_products_ids or []
        self.product_quantity_price = {}
        self.product_quantity = self._get_possible_quantity()
        self.product_quantity_total_price = self._get_total_price()

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
        return order.delivery_option

    def __init__(self, order_id):
        self.order_id = order_id
        self.delivery_option = self._get_delivery_option()

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
        OrderEmail(self.order)


class OrderHistory:

    def _get_orders(self):
        self.orders = Order.objects.filter(user_id=self.user_id)
        self._get_products_in_orders()

    def _get_products_in_orders(self):
        for order in self.orders:
            products_quantity = order.products['products']
            products_query = Product.objects.filter(id__in=products_quantity)
            order.products_query = products_query

    def __init__(self, user_id):
        self.user_id = user_id
        self._get_orders()
