from django.db import models

# Create your models here.
class RecieverAddress(models.Model):
    receiver_first_name=models.CharField(max_length=100)
    receiver_last_name=models.CharField(max_length=100)
    receiver_phone_number=models.CharField(max_length=15)
    receiver_gender=models.IntegerField(choices=[(1,'Male'),(2,'Female')])
    receiver_email=models.EmailField()
    receiver_secondary_phone_number=models.CharField(max_length=15)
    receiver_building=models.CharField(max_length=100)
    receiver_floor=models.IntegerField()
    receiver_directions=models.TextField()
    receiver_area=models.CharField(max_length=100)
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    ]
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    barcode=models.TextField(null=True)
    address = models.ForeignKey(RecieverAddress,on_delete=models.SET_NULL,related_name='orders',null=True)
    wakilni_id=models.CharField(max_length=100,null=True)
    def __str__(self):
        return f"order-#{self.id}"
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product_variant=models.ForeignKey('product.ProductVariant',on_delete=models.PROTECT,related_name='order_items')
    quantity=models.PositiveIntegerField(default=1)
