from django.test import TestCase, Client
import unittest
from ..models import Product, Category, Type, Image, Comments, Rating, Customer, ShopContacts, ShopAddress, \
    UserBucketProducts, Order
from django.contrib.auth.models import User

client = Client()

# PRODUCT_VALID_DATA = {
#     "id": 1,
#     "title": 'Big Best Product',
#     "description": 'Description',
#     "price": 100.0,
#     "is_sale": False,
#     "discount": 0,
#     "available_quantity": 100,
# }
#
#
# class ProductModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         category = Category.objects.create(id=1, name="Main category")
#         type = Type.objects.create(id=1, name="First type", category=category)
#         Product.objects.create(**PRODUCT_VALID_DATA, type=type)
#
#     def test_product_fields(self):
#         product = Product.objects.get(id=1)
#         product_type = Type.objects.get(id=1)
#         category = Category.objects.get(id=1)
#
#         self.assertEqual(product.title, PRODUCT_VALID_DATA["title"])
#         self.assertEqual(product.description, PRODUCT_VALID_DATA["description"])
#         self.assertEqual(product.price, PRODUCT_VALID_DATA["price"])
#         self.assertEqual(product.is_sale, PRODUCT_VALID_DATA["is_sale"])
#         self.assertEqual(product.discount, PRODUCT_VALID_DATA["discount"])
#         self.assertEqual(product.available_quantity, PRODUCT_VALID_DATA["available_quantity"])
#
#         self.assertEqual(product.type, product_type)
#         self.assertEqual(product.type.category, category)
#
#     def test_product_get_price(self):
#         product = Product.objects.get(id=1)
#         self.assertEqual(product.get_price(), PRODUCT_VALID_DATA["price"])
#
#         product.is_sale = True
#         product.discount = 30
#         product.save()
#         self.assertEqual(product.get_price(), 70)
#
#
# class ImageModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         category = Category.objects.create(name="Main category")
#         type = Type.objects.create(name="First type", category=category)
#         product = Product.objects.create(**PRODUCT_VALID_DATA, type=type)
#         Image.objects.create(
#             id=1,
#             product=product,
#             title_image=True
#         )
#         Image.objects.create(
#             id=2,
#             product=product,
#             title_image=False
#         )
#
#     def test_image_save(self):
#         pass
#         # image_1 = Image.objects.get(id=1)
#         # image_2 = Image.objects.get(id=2)
#         #
#         # self.assertTrue(image_1.title_image)
#         # self.assertFalse(image_2.title_image)
#         #
#         # image_2.title_image = True
#         # image_2.save()
#         #
#         # self.assertTrue(image_2.title_image)
#         # self.assertFalse(image_1.title_image)
#
#     def test_image_delete(self):
#         pass


# CATEGORY = "product.category"
# TYPE = "product.type"
# PRODUCT = "product.product"
# IMAGE = "product.image"
# COMMENTS = "product.comments"
# RATING = "product.rating"
# CUSTOMER = "product.customer"
# SHOPCONTACTS = "product.shopcontacts"
# SHOPADDRESS = "product.shopaddress"
# USERBACKETPRODUCTS = "product.userbucketproducts"
# ORDER = "product.order"
#
# data_creation = {
#     CATEGORY: Category.objects.create,
#     TYPE: Type.objects.create,
#     PRODUCT: Product.objects.create,
#     IMAGE: Image.objects.create,
#     COMMENTS: Comments.objects.create,
#     RATING: Rating.objects.create,
#     CUSTOMER: Customer.objects.create,
#     SHOPCONTACTS: ShopContacts.objects.create,
#     SHOPADDRESS: ShopAddress.objects.create,
#     USERBACKETPRODUCTS: UserBucketProducts.objects.create,
#     ORDER: Order.objects.create,
# }

category_1 = {'id': 1, 'name': 'test_category_1'}
category_2 = {'id': 2, 'name': 'test_category_2'}

type_1 = {'id': 1, 'name': 'For hands', 'category_id': 1}
type_2 = {'id': 2, 'name': 'Flour', 'category_id': 2}
type_3 = {'id': 3, 'name': 'Soap', 'category_id': 1}
type_4 = {'id': 4, 'name': 'Hair care', 'category_id': 1}

product_1 = {'id': 1,
             'title': 'Soap 1',
             'description': 'Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION Soap 1 DESCRIPTION',
             'price': 100.0,
             'is_sale': False,
             'discount': None,
             'available_quantity': 1,
             'type_id': 3}
product_2 = {'id': 2, 'title': 'Soap 2',
             'description': 'Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION Soap 2 DESCRIPTION',
             'price': 110.0, 'is_sale': False, 'discount': None, 'available_quantity': 14,
             'type_id': 3}
product_3 = {'id': 4, 'title': 'Soap 4',
             'description': 'Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION  Soap 4 DESCRIPTION',
             'price': 15.0, 'is_sale': False, 'discount': None, 'available_quantity': 0,
             'type_id': 3}
product_4 = {'id': 5, 'title': 'Soap 5',
             'description': 'Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION  Soap 5 DESCRIPTION',
             'price': 800.0,
             'is_sale': True,
             'discount': 20,
             'available_quantity': 0,
             'type_id': 3}
product_5 = {'id': 6, 'title': 'Floor cleaner 1',
             'description': 'Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION Floor cleaner 1 DESCRIPTION',
             'price': 80.0, 'is_sale': True, 'discount': 10, 'available_quantity': 89,
             'type_id': 4}
product_6 = {'id': 7, 'title': 'Floor cleaner 2',
             'description': '1000',
             'price': 40.0, 'is_sale': False, 'discount': None,
             'available_quantity': 12, 'type_id': 4}

comment_1 = {'products.comments': 1,
             'fields': {'id': 1, 'author': 7, 'published_date': '2023-07-18T15:01:50.421Z',
                        'comment': 'Good Shampoo, as for me.', 'product_id': 9}}
comment_2 = {'products.comments': 2,
             'fields': {'id': 2, 'author': 7, 'published_date': '2023-07-18T15:02:52.606Z',
                        'comment': 'I like this shampoo so much', 'product_id': 9}}
comment_3 = {'products.comments': 5,
             'fields': {'id': 5, 'author': 1, 'published_date': '2023-07-26T11:46:54.262Z',
                        'comment': '123 adfasd 131 41 qse qdasd', 'product_id': 7}}

rating_1 = {'products.rating': 29,
            'fields': {'id': 29, 'rate': 5, 'author': 16, 'product_id': 3}}
rating_2 = {'products.rating': 30,
            'fields': {'id': 30, 'rate': 5, 'author': 15, 'product_id': 3}}
rating_3 = {'products.rating': 31,
            'fields': {'id': 31, 'rate': 5, 'author': 1, 'product_id': 3}}
rating_4 = {'products.rating': 32,
            'fields': {'id': 32, 'rate': 4, 'author': 19, 'product_id': 3}}
rating_5 = {'products.rating': 33,
            'fields': {'id': 33, 'rate': 3, 'author': 16, 'product_id': 2}}
rating_6 = {'products.rating': 34,
            'fields': {'id': 34, 'rate': 4, 'author': 15, 'product_id': 2}}
rating_7 = {'products.rating': 35,
            'fields': {'id': 35, 'rate': 4, 'author': 16, 'product_id': 4}}

user_1 = {"id": 1, 'username': "username_1", "email": "example_1@example.com", 'password': "qwerty"}
user_2 = {"id": 2, 'username': "username_2", "email": "example_2@example.com", 'password': "qwerty"}
user_3 = {"id": 3, 'username': "username_3", "email": "example_3@example.com", 'password': "qwerty"}
user_4 = {"id": 4, 'username': "username_4", "email": "example_4@example.com", 'password': "qwerty"}
user_5 = {"id": 5, 'username': "username_5", "email": "example_5@example.com", 'password': "qwerty"}
user_6 = {"id": 6, 'username': "username_6", "email": "example_6@example.com", 'password': "qwerty"}

customer_1 = {'id': 1, 'phone_number': '+380441112233', 'user_id': 1}
customer_2 = {'id': 2, 'phone_number': '+380441212233', 'user_id': 2}
customer_3 = {'id': 3, 'phone_number': '+380441312233', 'user_id': 3}
customer_4 = {'id': 4, 'phone_number': '+380441412233', 'user_id': 4}
customer_5 = {'id': 5, 'phone_number': '+380441512233', 'user_id': 5}
customer_6 = {'id': 6, 'phone_number': '+380441612233', 'user_id': 6}



class EnyDataTesting(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(**category_1)
        Category.objects.create(**category_2)

        Type.objects.create(**type_1)
        Type.objects.create(**type_2)
        Type.objects.create(**type_3)
        Type.objects.create(**type_4)

        Product.objects.create(**product_1)
        Product.objects.create(**product_2)
        Product.objects.create(**product_3)
        Product.objects.create(**product_4)
        Product.objects.create(**product_5)
        Product.objects.create(**product_6)

        User.objects.create_user(**user_1)
        User.objects.create_user(**user_2)
        User.objects.create_user(**user_3)
        User.objects.create_user(**user_4)
        User.objects.create_user(**user_5)
        User.objects.create_user(**user_6)

        Customer.objects.create(**customer_1)
        Customer.objects.create(**customer_2)
        Customer.objects.create(**customer_3)
        Customer.objects.create(**customer_4)
        Customer.objects.create(**customer_5)
        Customer.objects.create(**customer_6)

    def test_get_category(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.id, category_1["id"])
        category = Category.objects.get(name='test_category_2')
        self.assertEqual(category.id, category_2["id"])

    def test_get_type(self):
        type_prod = Type.objects.get(name='For hands')
        self.assertEqual(type_prod.id, type_1["id"])
        type_prod = Type.objects.get(name='Flour')
        self.assertEqual(type_prod.id, type_2["id"])

    def test_get_product(self):
        product = Product.objects.get(title='Soap 1')
        self.assertEqual(product.id, product_1["id"])
        product = Product.objects.get(title='Soap 2')
        self.assertEqual(product.id, product_2["id"])
        product = Product.objects.get(title='Soap 4')
        self.assertEqual(product.id, product_3["id"])
        product = Product.objects.get(title='Soap 5')
        self.assertEqual(product.id, product_4["id"])
        product = Product.objects.get(title='Floor cleaner 1')
        self.assertEqual(product.id, product_5["id"])
        product = Product.objects.get(title='Floor cleaner 2')
        self.assertEqual(product.id, product_6["id"])

    def test_get_product_else(self):
        product = Product.objects.get(id=7)
        self.assertEqual(product.description, '1000')

    def test_get_user(self):
        user_obj_1 = User.objects.get(id=1)
        self.assertEqual(user_obj_1.username, user_1["username"])
        user_obj_2 = User.objects.get(id=2)
        self.assertEqual(user_obj_2.username, user_2["username"])
        user_obj_3 = User.objects.get(id=3)
        self.assertEqual(user_obj_3.username, user_3["username"])
        user_obj_4 = User.objects.get(id=4)
        self.assertEqual(user_obj_4.username, user_4["username"])

    def test_get_customer(self):
        customer_obj_1 = Customer.objects.get(id=1)
        self.assertEqual(customer_obj_1.user.id, user_1["id"])
        customer_obj_2 = Customer.objects.get(id=2)
        self.assertEqual(customer_obj_2.user.id, user_2["id"])
        customer_obj_3 = Customer.objects.get(id=3)
        self.assertEqual(customer_obj_3.user.id, user_3["id"])
        customer_obj_4 = Customer.objects.get(id=4)
        self.assertEqual(customer_obj_4.user.id, user_4["id"])
        customer_obj_5 = Customer.objects.get(id=5)
        self.assertEqual(customer_obj_5.user.id, user_5["id"])
        customer_obj_6 = Customer.objects.get(id=6)
        self.assertEqual(customer_obj_6.user.id, user_6["id"])





# class RequestProductsTesting(EnyDataTesting):
#     def test_get_products(self):
#         response = client.get("")
#         self.assertEqual(response.status_code, 200)
#         products = response.context["products"]
#         out_of_stock = response.context["out_of_stock"]
#         self.assertEqual(len(products), 4)
#         self.assertEqual(len(out_of_stock), 2)
#         self.assertEqual(products.get(id=2).title, 'Soap 2')
#
#     def test_get_product_detail(self):
#         response = client.get("/product_detail/7/")
#         self.assertEqual(response.status_code, 200)
#         response = client.get("/product_detail/9999/")
#         self.assertEqual(response.status_code, 404)
#
#     def test_get_products_search(self):
#         response = client.get("",
#                               data={'search': 'soa', 'sorting': 'rating'})
#         products = response.context["products"]
#         out_of_stock = response.context["out_of_stock"]
#         self.assertEqual(products[0].title, 'Soap 1')
#         self.assertEqual(products[1].title, 'Soap 2')
#         self.assertEqual(out_of_stock[0].title, 'Soap 4')
#         self.assertEqual(out_of_stock[1].title, 'Soap 5')
#
#     def test_get_products_type(self):
#         response = client.get("",
#                               data={'type': '3', 'sorting': 'rating'})
#         products = response.context["products"]
#         out_of_stock = response.context["out_of_stock"]
#         self.assertEqual(products[0].title, 'Soap 1')
#         self.assertEqual(products[1].title, 'Soap 2')
#         self.assertEqual(out_of_stock[0].title, 'Soap 4')
#         self.assertEqual(out_of_stock[1].title, 'Soap 5')
