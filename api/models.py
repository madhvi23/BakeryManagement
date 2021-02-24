from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Ingredients(models.Model):
    ingredientId = models.AutoField(primary_key=True)
    ingredientname = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    costprice = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.ingredientname


class BakeryItem(models.Model):
    bakeryitemId = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=100, blank=False, null=False)
    makingcharges = models.CharField(max_length=100)
    ingredientslist = models.JSONField()

    def __str__(self):
        return self.itemname


class CustomerRegsiteration(models.Model):
    customerId = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=8)
    mobileno = models.CharField(max_length=10, null=False, blank=False)
    countrycode = models.CharField(max_length=5, null=False, blank=False)
    role = models.CharField(max_length=10, default='Customer')

    def __str__(self):
        return self.user.username


class UserRole(models.Model):
    user = models.ForeignKey(CustomerRegsiteration, on_delete=models.CASCADE)
    role = models.CharField(choices=(('customer', 'Customer'), ('admin', 'Admin')),
                            max_length=8)


class Cart(models.Model):
    cartId = models.AutoField(primary_key=True)
    itemId = models.OneToOneField(BakeryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Cart Value is {self.itemId.costprice * self.quantity}"


class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    customerId = models.OneToOneField(CustomerRegsiteration, on_delete=models.CASCADE)
    cartId = models.OneToOneField(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.orderId


