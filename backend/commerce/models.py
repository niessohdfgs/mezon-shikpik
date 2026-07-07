from django.db import models
from django.conf import settings

from courses.models import Course
from patterns.models import Pattern


class Product(models.Model):

    TYPES = (
        ("course", "Course"),
        ("pattern", "Pattern"),
        ("bundle", "Bundle"),
    )

    title = models.CharField(
        max_length=255
    )

    type = models.CharField(
        max_length=20,
        choices=TYPES
    )

    price = models.PositiveIntegerField()

    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    pattern = models.ForeignKey(
        Pattern,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.title



class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def total_price(self):
        return sum(
            item.total_price()
            for item in self.items.all()
        )



class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )


    def total_price(self):
        return self.product.price * self.quantity



class Discount(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    percent = models.PositiveIntegerField()

    max_usage = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    used_count = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    start_date = models.DateTimeField(
        null=True,
        blank=True
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.code



class Order(models.Model):

    STATUS = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )

    total_price = models.PositiveIntegerField()


    discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"Order #{self.id}"



class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.PositiveIntegerField()



class Purchase(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        unique_together = (
            "user",
            "product"
        )


class Payment(models.Model):

    STATUS = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )


    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )


    amount = models.PositiveIntegerField()


    authority = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )


    ref_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"Payment {self.order.id}"