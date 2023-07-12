from ..models import Order, Product, User, secret_string_saver
from django.core.mail import send_mail
from django.conf import settings
import random
import string


def email_sender(subject, message, recipient_list=[settings.RECIPIENT_ADDRESS]):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list
    )


class OrderEmail:
    def _get_optional_information(self):
        pickup_info = ''
        courier_info = '\n\tDestination address - {region}'.format(region=self.order_info.destination_region) + \
                       '{country}, {street}, house №{house}, apartment №{apartment}.'.format(
                           country=self.order_info.destination_country, street=self.order_info.destination_street,
                           house=self.order_info.destination_house, apartment=self.order_info.destination_apartment)
        delivery_service_info = '\n\tDestination delivery office - {region}'.format(
            region=self.order_info.destination_region) + \
                                '{country}, delivery office №{office}.'.format(
                                    country=self.order_info.destination_country,
                                    office=self.order_info.destination_delivery_service)

        order_optional_information = {
            Order.PICKUP: pickup_info,
            Order.STORE_COURIER: courier_info,
            Order.DELIVERY_SERVICE_1: delivery_service_info,
            Order.DELIVERY_SERVICE_2: delivery_service_info,
            Order.DELIVERY_SERVICE_3: delivery_service_info,
        }
        return order_optional_information[self.order_info.delivery_option]

    def _order_report_text(self):
        customer_text_header = 'Thank you, order №{order_id} accepted:'.format(order_id=self.order_info.id)
        admin_text_header = 'New order №{order_id}:'.format(order_id=self.order_info.id)
        product_text_list = ''

        id_quantity = self.order_info.products['products']
        products = Product.objects.filter(id__in=id_quantity)
        total_price = 0
        for prod_id in id_quantity:
            product = products.get(id=prod_id)
            product_quantity = id_quantity[prod_id]
            units_price = round(product.get_price() * product_quantity, 2)
            total_price += units_price
            line = '\n\t*\t{title} - {quantity} units - {price} ₴.'.format(title=product.title,
                                                                           quantity=product_quantity,
                                                                           price=units_price)
            product_text_list += line

        total_price_order_text = '\n\tTotal price - {total_price} ₴.'.format(total_price=total_price)
        product_text_list += total_price_order_text
        customer_text_footer = '\n\nOur manager will contact you shortly.'

        customer_email_text = customer_text_header + product_text_list + customer_text_footer

        admin_text_customer_name = '\n\tFull name - {first_name} {middle_name} {last_name};'.format(
            first_name=self.order_info.first_name, middle_name=self.order_info.middle_name,
            last_name=self.order_info.last_name)

        admin_text_customer_contacts = '\n\tContacts - {phone};  {email};'.format(phone=self.order_info.phone_number,
                                                                                  email=self.order_info.email)

        admin_text_customer_payment = '\n\tPayment option - {payment}.'.format(payment=self.order_info.payment_option)

        admin_text_customer_delivery = '\n\tDelivery option - {delivery}.'.format(
            delivery=self.order_info.delivery_option)

        admin_text_customer_address = self._get_optional_information()

        admin_email_text = admin_text_header + product_text_list + admin_text_customer_name + \
                           admin_text_customer_contacts + admin_text_customer_payment + admin_text_customer_delivery + \
                           admin_text_customer_address

        return {
            'customer_email_text': customer_email_text,
            'admin_email_text': admin_email_text
        }

    def _order_customer_email_subject(self):
        return "Order №{} in Web shop HHC".format(self.order_info.id)

    def _order_admin_email_subject(self):
        return "Order №{}".format(self.order_info.id)

    # def _sending_order_email(self):
    #     send_mail(
    #         subject=self.customer_email_subject,
    #         message=self.customer_email_text,
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[settings.RECIPIENT_ADDRESS]
    #     )
    #
    #     send_mail(
    #         subject=self.admin_email_subject,
    #         message=self.admin_email_text,
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[settings.RECIPIENT_ADDRESS]
    #     )

    # TODO: Change recipient_list to self.order.email

    def __init__(self, order_info):
        self.order_info = order_info
        email_text = self._order_report_text()
        self.customer_email_text = email_text['customer_email_text']
        self.admin_email_text = email_text['admin_email_text']
        self.customer_email_subject = self._order_customer_email_subject()
        self.admin_email_subject = self._order_admin_email_subject()
        email_sender(subject=self.customer_email_subject, message=self.customer_email_text)
        email_sender(subject=self.admin_email_subject, message=self.admin_email_text)


class RessetPasswordMail:
    def _get_customer(self):
        customer = User.objects.get(id=self.customer_id)
        return customer

    def _get_reset_link(self):
        count = 0
        first_link_part = ''
        for symbol in self.path:
            if symbol == '/':
                count += 1
            first_link_part += symbol
            if count == 3:
                break

        middle_link_part = 'reset_token/'

        last_link_part = (
            ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(30)))
        secret_string_saver(last_link_part, self.customer_id)

        reset_link = first_link_part + last_link_part
        return reset_link

    def _text_reset_password(self):
        text = "\tYou get this message for changing password in your account on Web-shop HHS." + \
               "\n\tFor changing password, click on the link below:" + \
               "\n\n\t {link} ".format(link=self.reset_link) + \
               "\n\n\tIf it was not you, ignore this massage"
        return text

    def _subject_reset_password(self):
        subject = 'Web shop HHS. Reset password!'
        return subject

    def __init__(self, customer_id, path):
        self.customer_id = customer_id
        self.customer = self._get_customer()
        self.path = path
        self.reset_link = self._get_reset_link()
        self.email_reset_text = self._text_reset_password()
        self.email_reset_subject = self._subject_reset_password()
        email_sender(subject=self.email_reset_subject, message=self.email_reset_text)
