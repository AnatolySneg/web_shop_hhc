from ..models import UserBucketProducts


class Bucket:
    def _get_bucket_ids(self, user_id):
        try:
            personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
            self.bucket_ids = personal_bucket.user_bucket['products_in_bucket']
        except UserBucketProducts.DoesNotExist:
            self.bucket_ids = []

    def _quantity(self):
        product_quantity = {}
        for id_number in self.bucket_ids:
            product_quantity[id_number] = self.bucket_ids.count(id_number)
        return product_quantity

    def __init__(self, user_id, session_products_ids):
        self.user_id = user_id
        if self.user_id:
            self._get_bucket_ids(self.user_id)
        else:
            if session_products_ids is None:
                self.bucket_ids = []
            else:
                self.bucket_ids = session_products_ids
        self.product_quantity = self._quantity()

    def _update_user_bucket(self):
        try:
            personal_bucket = UserBucketProducts.objects.get(user_id=self.user_id)
            personal_bucket.user_bucket['products_in_bucket'] = self.bucket_ids
            personal_bucket.save()
        except UserBucketProducts.DoesNotExist:
            UserBucketProducts.objects.create(user_id=self.user_id,
                                              user_bucket={'products_in_bucket': self.bucket_ids})

    def add_product(self, product_id):
        self.bucket_ids.append(product_id)
        self.product_quantity = self._quantity()
        if self.user_id:
            self._update_user_bucket()

    def remove_products(self, product_id):
        new_bucket_list = self.bucket_ids.copy()
        for bucket_id in self.bucket_ids:
            if bucket_id == product_id:
                new_bucket_list.remove(bucket_id)
        self.bucket_ids = new_bucket_list
        self.product_quantity = self._quantity()
        if self.user_id:
            self._update_user_bucket()

    def increase(self, product_id):
        self.bucket_ids.append(product_id)
        self.product_quantity = self._quantity()
        if self.user_id:
            self._update_user_bucket()

    def decrease(self, product_id):
        self.bucket_ids.remove(product_id)
        self.product_quantity = self._quantity()
        if self.user_id:
            self._update_user_bucket()
