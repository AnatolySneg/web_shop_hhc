from ..models import Product


#
#
# class NoSearchError(Exception):
#     def __init__(self, *args, **kwargs):
#         pass
#
#
# class NoSortingError(Exception):
#     def __init__(self, *args, **kwargs):
#         pass
#
#
# class NoFilterError(Exception):
#     def __init__(self, *args, **kwargs):
#         pass
#
#
# class NoTypeError(Exception):
#     def __init__(self, *args, **kwargs):
#         pass
#
#
# class NoCategoryError(Exception):
#     def __init__(self, *args, **kwargs):
#         pass
#

class ProductListing:

    def _get_product_search(self):
        available_product_list = Product.objects.filter(title__istartswith=self.search,
                                                        available_quantity__gte=1)
        unavailable_product_list = Product.objects.filter(title__istartswith=self.search,
                                                          available_quantity__lt=1)
        return available_product_list, unavailable_product_list

    def _get_product_type(self):
        available_product_list = Product.objects.filter(type_id=self.type_id, available_quantity__gte=1)
        unavailable_product_list = Product.objects.filter(type_id=self.type_id, available_quantity__lt=1)
        return available_product_list, unavailable_product_list

    def _get_product_category(self):
        available_product_list = Product.objects.filter(type__category_id=self.category_id, available_quantity__gte=1)
        unavailable_product_list = Product.objects.filter(type__category_id=self.category_id, available_quantity__lt=1)
        return available_product_list, unavailable_product_list

    def _get_product_all(self):
        available_product_list = Product.objects.filter(available_quantity__gte=1)
        unavailable_product_list = Product.objects.filter(available_quantity__lt=1)
        return available_product_list, unavailable_product_list

    def __init__(self, category_id, type_id, product_filtering, product_sorting, search):
        self.category_id = category_id
        self.type_id = type_id
        self.product_filtering = product_filtering
        self.product_sorting = product_sorting
        self.search = search
        if search:
            self.product_list = self._get_product_search()
        elif category_id:
            self.product_list = self._get_product_category()
        elif type_id:
            self.product_list = self._get_product_type()
        else:
            self.product_list = self._get_product_all()
        self.product_list_available = self.product_list[0]
        self.product_list_unavailable = self.product_list[1]
