from django.db import models
# Create your models here.
class Cart(models.Model):
    session_key=models.CharField(max_length=100,unique=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.session_key
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product_variant=models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE,related_name='cart_items')
    quantity=models.PositiveIntegerField(default=1)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['cart','product_variant'],name='unique_cart_item')
        ]
