from django.contrib import admin
from .models import Product,ProductVariant,Category,Color,Size,Media
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Media)
