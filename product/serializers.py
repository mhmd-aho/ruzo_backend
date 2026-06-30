from rest_framework import serializers
from .models import Product,ProductVariant,Category,Color,Size,Media
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields='__all__'
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields='__all__'
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model=Product
        fields=['id','name','description','price','category','sale','best_seller']
class ProductVariantSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    size=SizeSerializer(read_only=True)
    color= ColorSerializer(read_only=True)
    class Meta:
        model=ProductVariant
        fields=['id','product','size','color','quantity']
class MediaSerializer(serializers.ModelSerializer):
    product_variant=ProductVariantSerializer(read_only=True)
    class Meta:
        model=Media
        fields=['id','product_variant','media_url']
