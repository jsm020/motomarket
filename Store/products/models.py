from datetime import datetime

from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=21)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'categories'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Mahsulot nomi", max_length=50)
    photo = models.CharField(verbose_name="Rasm file_id", max_length=200, null=True)
    price = models.DecimalField(verbose_name="Narx", decimal_places=2, max_digits=12)
    description = models.TextField(verbose_name="Mahsulot haqida", max_length=3000, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"№{self.id} - {self.name}"

    class Meta:
        db_table = 'products'


#
# class Price(models.Model):
#     label = models.CharField(max_length=221)
#     price = models.DecimalField(decimal_places=2, max_digits=8)
#
#     def __str__(self):
#         return f"{self.label} - {self.price}"
#
#     class Meta:
#         db_table = "prices"
#
#
# class Product_orders(models.Model):
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     title = models.CharField(max_length=221)
#     description = models.TextField(null=True)
#     currency = models.CharField(max_length=3, null=True)
#     prices = models.ManyToManyField(Price, null=True)
#     start_parameter = models.CharField(max_length=221, null=True)
#     photo_url = models.CharField(max_length=500, null=True)
#     photo_width = models.IntegerField(null=True)
#     photo_height = models.IntegerField(null=True)
#     photo_size = models.IntegerField(null=True)
#     email = models.BooleanField(null=True, default=False)
#     shipping_address = models.BooleanField(null=True, default=False)
#     name = models.BooleanField(null=True, default=False)
#     phone_number = models.BooleanField(null=True, default=False)
#     provider = models.CharField(max_length=221, null=True)
#
#     @property
#     def created_time(self):
#         return datetime.now()
#
#     def __str__(self):
#         return f"({self.id}) {self.name}"
#
#     class Meta:
#         db_table = "Product_orders"


class Order(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    currency = models.CharField(max_length=221, null=True)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    invoice_payload = models.CharField(max_length=221, null=True)

    # order info
    user_name = models.CharField(max_length=221, null=True)
    phone_number = models.CharField(max_length=221, null=True)
    email = models.EmailField(null=True)

    # location
    state = models.CharField(max_length=221, null=True)
    city = models.CharField(max_length=221, null=True)

    created_time = models.DateTimeField(auto_now_add=True)

    # @property
    # def created_time(self):
    #     return datetime.now()

    def __str__(self):
        return f"({self.id}) {self.user_name}"

    class Meta:
        db_table = "orders"
