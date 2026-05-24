from rest_framework import serializers
from .models import Cart,CartItem
from product.models import ProductVariant
from product.serializers import ProductVariantSerializer
class CartItemSerializer(serializers.ModelSerializer):
    product_variant=ProductVariantSerializer(read_only=True)
    item_total=serializers.SerializerMethodField()
    class Meta:
        model=CartItem
        fields=['id','cart','product_variant','quantity','item_total']
    def get_item_total(self,obj):
        return obj.product_variant.product.price*obj.quantity
class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    cart_total=serializers.SerializerMethodField()
    class Meta:
        model=Cart
        fields=['id','session_key','updated_at','items','cart_total']
    def get_cart_total(self,obj):
        return sum(item.product_variant.product.price*item.quantity for item in obj.items.all())