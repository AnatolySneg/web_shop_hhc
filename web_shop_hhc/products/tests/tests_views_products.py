from ..models import Product, Category, Type, Image, Comments, Rating, Customer, ShopContacts, ShopAddress, \
    UserBucketProducts, Order
from django.contrib.auth.models import User
from django.test import TestCase
from .tests_data_insert import client, EnyDataTesting
from .tests_data_insert import category_1, category_2, type_1, type_2, type_3, type_4
from .tests_data_insert import product_1, product_2, product_3, product_4, product_5, product_6


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
        client.force_login(User.objects.get(id=1))
        response = client.get("",
                              data={'type': '3', 'sorting': 'rating'})
        products = response.context["products"]
        out_of_stock = response.context["out_of_stock"]
        self.assertEqual(products[0].title, 'Soap 1')
        client.logout()
        self.assertEqual(products[1].title, 'Soap 2')
        self.assertEqual(out_of_stock[0].title, 'Soap 4')
        self.assertEqual(out_of_stock[1].title, 'Soap 5')


