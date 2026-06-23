from django.shortcuts import render
from .models import Product,ProductVariant,Category,Color,Size,Media
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ProductSerializer,CategorySerializer,ColorSerializer,SizeSerializer,MediaSerializer,ProductVariantSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 12
class ProductsListView(generics.ListAPIView):
    serializer_class=ProductSerializer
    pagination_class=ProductPagination
    def get_queryset(self):
        queryset=Product.objects.all()
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset=queryset.filter(category_id=category_id)
        return queryset
class ProductRetrieveView(generics.RetrieveAPIView):
    def get_queryset(self):
        return Product.objects.get(id=self.kwargs['id'])
    serializer_class=ProductSerializer
    lookup_field='id'
class ProductCreateView(generics.CreateAPIView):
    permission_classes=[IsAdminUser]
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
class ProductModifyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='id'
class ProductVariantListView(generics.ListAPIView):
    def get_queryset(self):
        return ProductVariant.objects.filter(product=self.kwargs['product_id'])
    serializer_class=ProductVariantSerializer
class CategoryListView(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
class CategoryCreateView(generics.CreateAPIView):
    permission_classes=[IsAdminUser]
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
class CategoryModifyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    lookup_field='id'
class ColorListView(generics.ListAPIView):
    queryset=Color.objects.all()
    serializer_class=ColorSerializer
class ColorCreateView(generics.CreateAPIView):
    permission_classes=[IsAdminUser]
    queryset=Color.objects.all()
    serializer_class=ColorSerializer
class ColorModifyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=Color.objects.all()
    serializer_class=ColorSerializer
    lookup_field='id'
class SizeListView(generics.ListAPIView):
    queryset=Size.objects.all()
    serializer_class=SizeSerializer
class SizeCreateView(generics.CreateAPIView):
    permission_classes=[IsAdminUser]
    queryset=Size.objects.all()
    serializer_class=SizeSerializer
class SizeModifyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=Size.objects.all()
    serializer_class=SizeSerializer
    lookup_field='id'
class MediaListView(generics.ListAPIView):
    queryset=Media.objects.all()
    serializer_class=MediaSerializer
class ProductMediaListView(generics.ListAPIView):
    def get_queryset(self):
        return Media.objects.filter(product=self.kwargs['product_id'])
    serializer_class=MediaSerializer
class MediaCreateView(generics.CreateAPIView):
    permission_classes=[IsAdminUser]
    queryset=Media.objects.all()
    serializer_class=MediaSerializer
class MediaModifyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=Media.objects.all()
    serializer_class=MediaSerializer
    lookup_field='id'