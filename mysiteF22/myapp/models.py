from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, null=True)

    # Added (null = True) so that it is possible to add
    # the warehouse field in the category because it was throwing an error

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(999)])
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self):
        self.stock += 100


class Client(User):
    PROVINCE_CHOICES = [('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ]
    company = models.CharField(max_length=50, null=True, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.username


class Order(models.Model):
    ORDERS = [(0, 'Order Cancelled'), (1, 'Order Placed'), (2, 'OrderShipped'), (3, 'Order Delivered')]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=ORDERS, default=1)
    status_date = models.DateField()

    def __str__(self):
        return self.client.first_name

    def total_cost(self):
        return self.num_units * self.product.price
