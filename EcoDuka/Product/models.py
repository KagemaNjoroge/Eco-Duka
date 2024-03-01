from django.db import models
from User.models import CustomUser


class MyException(Exception):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
        }


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.merchant.user_type != "MERCHANT":
            raise MyException("Only merchant can own product")
        else:
            super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "image": self.image.url,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category.name,
            "merchant": self.merchant.to_json(),
        }
