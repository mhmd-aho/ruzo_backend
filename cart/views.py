from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from .models import Cart,CartItem
from .serializers import CartSerializer,CartItemSerializer
from product.models import ProductVariant

class CartView(APIView):
    def get(self,request):
        key = request.session.session_key
        if not key:
            return Response({'items':[],"cart_total":0})
        cart = Cart.objects.filter(session_key=key).first()
        if not cart:
            return Response({'items':[],"cart_total":0})
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        if not request.session.session_key:
            request.session.create()
        key=request.session.session_key
        variant_id = request.data.get('variant_id')
        quantity = request.data.get('quantity', 1)
        if not variant_id:
            return Response({"error":"variant_id is required"},status=status.HTTP_400_BAD_REQUEST)
        cart, _ = Cart.objects.get_or_create(session_key=key)
        cart_item,created = CartItem.objects.get_or_create(cart=cart,product_variant_id=variant_id)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return Response({"message":"Item added to cart"},status=status.HTTP_201_CREATED)
class CartItemDeleteView(generics.DestroyAPIView):
    queryset=CartItem.objects.all()
    serializer_class=CartItemSerializer
    lookup_field='id'
    def get_queryset(self):
        key=self.request.session.session_key
        return CartItem.objects.filter(cart__session_key=key)
