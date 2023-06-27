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

    def _get_optional_information(self):
        pickup_info = ''
        courier_info = '\n\tDestination address - {region}'.format(region=self.order.destination_region) + \
                       '{country}, {street}, house №{house}, apartment №{apartment}.'.format(
                           country=self.order.destination_country, street=self.order.destination_street,
                           house=self.order.destination_house, apartment=self.order.destination_apartment)
        delivery_service_info = '\n\tDestination delivery office - {region}'.format(
            region=self.order.destination_region) + \
                                '{country}, delivery office №{office}.'.format(
                                    country=self.order.destination_country,
                                    office=self.order.destination_delivery_service)

        order_optional_information = {
            Order.PICKUP: pickup_info,
            Order.STORE_COURIER: courier_info,
            Order.DELIVERY_SERVICE_1: delivery_service_info,
            Order.DELIVERY_SERVICE_2: delivery_service_info,
            Order.DELIVERY_SERVICE_3: delivery_service_info,
        }
        return order_optional_information[self.order.delivery_option]

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
        customer_text = 'Thank you, order №{order_id} accepted:'.format(order_id=self.order_id)
        admin_text = 'New order №{order_id}:'.format(order_id=self.order_id)
        id_quantity = self.order.products['products']
        products = Product.objects.filter(id__in=id_quantity)
        total_price = 0
        for id in id_quantity:
            product = products.get(id=id)
            product_quantity = id_quantity[id]
            units_price = round(product.get_price() * product_quantity, 2)
            total_price += units_price
            text = '\n\t*\t{title} - {quantity} units - {price} ₴.'.format(title=product.title,
                                                                           quantity=product_quantity,
                                                                           price=units_price)
            customer_text += text
            admin_text += text
        total_price_text = '\n\tTotal price - {total_price} ₴.'.format(total_price=total_price)
        customer_text += total_price_text + '\n\nOur manager will contact you shortly.'
        admin_text += total_price_text + \
                      '\nCustomer information:' + \
                      '\n\tFull name - {first_name} {middle_name} {last_name};'.format(
                          first_name=self.order.first_name, middle_name=self.order.middle_name,
                          last_name=self.order.last_name) + \
                      '\n\tContacts - {phone};  {email};'.format(phone=self.order.phone_number,
                                                                  email=self.order.email) + \
                      '\n\tPayment option - {payment}.'.format(payment=self.order.payment_option) + \
                      '\n\tDelivery option - {delivery}.'.format(delivery=self.order.delivery_option) + \
                      self._get_optional_information()
        send_mail(
            subject="Order №{} in Web shop HHC".format(self.order_id),
            message=customer_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )
        send_mail(
            subject="Order №{}".format(self.order_id),
            message=admin_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )

        # TODO: Change recipient_list to self.order.email
