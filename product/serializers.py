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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model=Product
        fields=['id','name','description','price','category','sale','best_seller']
class ProductVariantSerializer(serializers.ModelSerializer):
    product=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    size=serializers.PrimaryKeyRelatedField(queryset=Size.objects.all())
    color=serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())
    class Meta:
        model=ProductVariant
        fields=['id','product','size','color','quantity']
class MediaSerializer(serializers.ModelSerializer):
    product= serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model=Media
        fields=['id','product','media_url']
