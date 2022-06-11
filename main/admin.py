from django.contrib import admin
from .models import TypeProduct, Product, ProductOwner, District, Region, CustomUser

# Register your models here.
admin.site.register(TypeProduct)
admin.site.register(Product)
admin.site.register(ProductOwner)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(CustomUser)
