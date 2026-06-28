from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Size(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Color(models.Model):
    name=models.CharField(max_length=100)
    color_code=models.CharField(max_length=7,unique=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey('Category', on_delete=models.PROTECT,related_name='products')
    sale = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],default=0)
    best_seller=models.BooleanField(default=False)
    def __str__(self):
        return self.name   
class ProductVariant(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='variants')
    size=models.ForeignKey('Size', on_delete=models.PROTECT,related_name='variants')
    color=models.ForeignKey('Color', on_delete=models.PROTECT,related_name='variants')
    quantity=models.PositiveIntegerField(default=0)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['product','size','color'],name='unique_product_variant')
        ]
    def __str__(self):
        return f"{self.product.name} {self.size.name} {self.color.name}"
class Media(models.Model):
    product_variant=models.ForeignKey(ProductVariant, on_delete=models.CASCADE,related_name='images',blank=True,null=True,default=1)
    media_url=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.product_variant.product.name} {self.product_variant.size.name} {self.product_variant.color.name} Image"
    