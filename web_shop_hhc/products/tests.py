from django.test import TestCase, Client
import unittest
from .models import Product, Category, Type, Image, Comments, Rating, Customer, ShopContacts, ShopAddress, \
    UserBucketProducts, Order

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


class EnyDataTesting(TestCase):
    @classmethod
    def setUpTestData(cls):
        ctg_1 = Category(**category_1)
        ctg_1.save()
        ctg_2 = Category(**category_2)
        ctg_2.save()

        tp_1 = Type(**type_1)
        tp_1.save()
        tp_2 = Type(**type_2)
        tp_2.save()
        tp_3 = Type(**type_3)
        tp_3.save()
        tp_4 = Type(**type_4)
        tp_4.save()

        prd_1 = Product(**product_1)
        prd_1.save()
        prd_2 = Product(**product_2)
        prd_2.save()
        prd_3 = Product(**product_3)
        prd_3.save()
        prd_4 = Product(**product_4)
        prd_4.save()
        prd_5 = Product(**product_5)
        prd_5.save()
        prd_6 = Product(**product_6)
        prd_6.save()

        # Category.objects.create(**category_1)
        # Category.objects.create(**category_2)
        #
        # Type.objects.create(**type_1)
        # Type.objects.create(**type_2)
        # Type.objects.create(**type_3)
        # Type.objects.create(**type_4)
        #
        # Product.objects.create(**product_1)
        # Product.objects.create(**product_2)
        # Product.objects.create(**product_3)
        # Product.objects.create(**product_4)
        # Product.objects.create(**product_5)
        # Product.objects.create(**product_6)
        #
        #

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


class RequestProductsTesting(EnyDataTesting):
    def test_get_products(self):
        response = client.get("")
        self.assertEqual(response.status_code, 200)
        products = response.context["products"]
        out_of_stock = response.context["out_of_stock"]
        self.assertEqual(len(products), 4)
        self.assertEqual(len(out_of_stock), 2)
        self.assertEqual(products.get(id=2).title, 'Soap 2')

    def test_get_product_detail(self):
        response = client.get("/product_detail/7/")
        self.assertEqual(response.status_code, 200)
        response = client.get("/product_detail/9999/")
        self.assertEqual(response.status_code, 404)

    def test_get_products_search(self):
        response = client.get("",
                              data={'search': 'soa', 'sorting': 'rating'})
        products = response.context["products"]
        out_of_stock = response.context["out_of_stock"]
        self.assertEqual(products[0].title, 'Soap 1')
        self.assertEqual(products[1].title, 'Soap 2')
        self.assertEqual(out_of_stock[0].title, 'Soap 4')
        self.assertEqual(out_of_stock[1].title, 'Soap 5')

    def test_get_products_type(self):
        response = client.get("",
                              data={'type': '3', 'sorting': 'rating'})
        products = response.context["products"]
        out_of_stock = response.context["out_of_stock"]
        self.assertEqual(products[0].title, 'Soap 1')
        self.assertEqual(products[1].title, 'Soap 2')
        self.assertEqual(out_of_stock[0].title, 'Soap 4')
        self.assertEqual(out_of_stock[1].title, 'Soap 5')

