from ..models import UserBucketProducts, bucket_updater


class Bucket:
    def _get_bucket_ids(self, user_id):
        try:
            personal_bucket = UserBucketProducts.objects.get(user_id=user_id)
            bucket_ids = personal_bucket.user_bucket['products_in_bucket']
        except UserBucketProducts.DoesNotExist:
            bucket_ids = {}
        return bucket_ids

    def __init__(self, user_id, session_products_ids=[], product_id=None):
        self.user_id = user_id
        if self.user_id:
            self.bucket_ids = self._get_bucket_ids(self.user_id)
        else:
            self.bucket_ids = session_products_ids
        self.product_id = product_id

    def add_product(self, user_id, product_id):
        if user_id:
            bucket_updater(user_id, product_id)
        else:
            return self.bucket_ids.append(product_id)


