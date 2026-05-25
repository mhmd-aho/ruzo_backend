from django.db import models

# Create your models here.
class Order(models.Model):
    user_fullname=models.CharField(max_length=200)
    user_number=models.CharField(max_length=15)
    user_email=models.EmailField(blank=True,null=True)
    order_status=models.CharField(max_length=20,choices=[('pending','Pending'),('shipped','Shipped'),('delivered','Delivered')],default='pending')
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user_fullname
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product_variant=models.ForeignKey('product.ProductVariant',on_delete=models.PROTECT,related_name='order_items')
    quantity=models.PositiveIntegerField(default=1)

    