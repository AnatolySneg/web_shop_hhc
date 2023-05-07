from ..models import UserBucketProducts


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
    session_products_ids -  incoming list data-type, if bucket was updated at least once for current session, 
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
