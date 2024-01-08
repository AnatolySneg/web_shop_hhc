from django.test import TestCase, TransactionTestCase, SimpleTestCase
from .models import Product, Category, Type, Image

PRODUCT_VALID_DATA = {
    "id": 1,
    "title": 'Big Best Product',
    "description": 'Description',
    "price": 100.0,
    "is_sale": False,
    "discount": 0,
    "available_quantity": 100,
}


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(id=1, name="Main category")
        type = Type.objects.create(id=1, name="First type", category=category)
        Product.objects.create(**PRODUCT_VALID_DATA, type=type)

    def test_product_fields(self):
        product = Product.objects.get(id=1)
        product_type = Type.objects.get(id=1)
        category = Category.objects.get(id=1)

        self.assertEqual(product.title, PRODUCT_VALID_DATA["title"])
        self.assertEqual(product.description, PRODUCT_VALID_DATA["description"])
        self.assertEqual(product.price, PRODUCT_VALID_DATA["price"])
        self.assertEqual(product.is_sale, PRODUCT_VALID_DATA["is_sale"])
        self.assertEqual(product.discount, PRODUCT_VALID_DATA["discount"])
        self.assertEqual(product.available_quantity, PRODUCT_VALID_DATA["available_quantity"])

        self.assertEqual(product.type, product_type)
        self.assertEqual(product.type.category, category)

    def test_product_get_price(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.get_price(), PRODUCT_VALID_DATA["price"])

        product.is_sale = True
        product.discount = 30
        product.save()
        self.assertEqual(product.get_price(), 70)


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Main category")
        type = Type.objects.create(name="First type", category=category)
        product = Product.objects.create(**PRODUCT_VALID_DATA, type=type)
        Image.objects.create(
            id=1,
            product=product,
            title_image=True
        )
        Image.objects.create(
            id=2,
            product=product,
            title_image=False
        )

    def test_image_save(self):
        pass
        # image_1 = Image.objects.get(id=1)
        # image_2 = Image.objects.get(id=2)
        #
        # self.assertTrue(image_1.title_image)
        # self.assertFalse(image_2.title_image)
        #
        # image_2.title_image = True
        # image_2.save()
        #
        # self.assertTrue(image_2.title_image)
        # self.assertFalse(image_1.title_image)

    def test_image_delete(self):
        pass
