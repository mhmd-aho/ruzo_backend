from rest_framework import serializers
from .models import Order,OrderItem
from product.serializers import ProductVariantSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_variant=ProductVariantSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','order','product_variant','quantity']
class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['id','user_fullname','user_number','user_email','order_status','created_at','total_price','items']