from django.db import models
from sqlalchemy import ForeignKey
from django.contrib.auth.models import User

# Create your models here.
class Region(models.Model):
    
    name = models.CharField(default='', max_length=40)

    class Meta:
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name


class District(models.Model):
    
    name = models.CharField(default='', max_length=40)
    region = models.ForeignKey(Region, on_delete=models.RESTRICT)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class TypeProduct(models.Model):

    name = models.CharField(default='', max_length=40)
    url = models.CharField(max_length=40, default='', null=True, blank=True)

    def save(self) -> None:
        self.url = self.name.replace(' ', '-')
        return super().save()

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class ProductOwner(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(default='', max_length=20)

    class Meta:
        ordering = ['phone']

    def __str__(self) -> str:
        return self.user.last_name + " " + self.user.first_name



class CustomUser(models.Model):
    phone_number = models.CharField(max_length=13)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user)


class Product(models.Model):

    name = models.CharField(default='', max_length=100)
    description = models.TextField(max_length=1000)
    price = models.FloatField(default=0)
    photo = models.ImageField(upload_to='product-images')
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, default=CustomUser.objects.first())
    district = models.ForeignKey(District, on_delete=models.RESTRICT)
    type = models.ForeignKey(TypeProduct, on_delete=models.RESTRICT)
    is_used = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name