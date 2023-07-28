from ..models import Product


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

    def _rating_sorting(self):
        available_rating_sorted = sorted(self.product_list_available, key=lambda p: p.average_rating(),
                                         reverse=True)
        unavailable_rating_sorted = sorted(self.product_list_unavailable, key=lambda p: p.average_rating(),
                                           reverse=True)
        return available_rating_sorted, unavailable_rating_sorted

    def _price_ascending_sorting(self):
        available_price_ascending_sorted = sorted(self.product_list_available, key=lambda p: p.get_price())
        unavailable_price_ascending_sorted = sorted(self.product_list_unavailable,
                                                    key=lambda p: p.get_price())
        return available_price_ascending_sorted, unavailable_price_ascending_sorted

    def _price_descending_sorting(self):
        available_price_descending_sorted = sorted(self.product_list_available, key=lambda p: p.get_price(),
                                                   reverse=True)
        unavailable_price_descending_sorted = sorted(self.product_list_unavailable,
                                                     key=lambda p: p.get_price(), reverse=True)
        return available_price_descending_sorted, unavailable_price_descending_sorted

    def _sorting_products(self):
        return self.sorting_option[self.product_sorting]

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

        self.sorting_option = {
            "rating": self._rating_sorting(),
            "price_ascending": self._price_ascending_sorting(),
            "price_descending": self._price_descending_sorting()
        }

        if self.product_sorting:
            self.sorted_product_list = self._sorting_products()

            self.sorted_product_list_available = self.sorted_product_list[0]
            self.sorted_product_list_unavailable = self.sorted_product_list[1]
        else:
            self.sorted_product_list_available = self.product_list_available
            self.sorted_product_list_unavailable = self.product_list_unavailable
