from rest_framework import serializers
from .models import Order,OrderItem
from product.serializers import ProductVariantSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_variant=ProductVariantSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','order','product_variant','quantity']
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecieverAddress
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    address=AddressSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id','status','created_at','total_price','items','address','barcode']
