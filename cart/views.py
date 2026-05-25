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
        quantity = int(request.data.get('quantity', 1))
        if not variant_id:
            return Response({"error":"variant_id is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            variant=ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return Response({"error":"product variant not found"},status=status.HTTP_404_NOT_FOUND)
        cart, _ = Cart.objects.get_or_create(session_key=key)
        cart_item,created = CartItem.objects.get_or_create(cart=cart,product_variant_id=variant_id)
        target_quantity = cart_item.quantity + quantity if not created else quantity
        if target_quantity > variant.quantity:
            if created:
                cart_item.delete()
            return Response({"error":"product out of stock"},status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity = target_quantity
        cart_item.save()
        return Response({"message":"Item added to cart"},status=status.HTTP_201_CREATED)
class CartItemDeleteView(generics.DestroyAPIView):
    queryset=CartItem.objects.all()
    serializer_class=CartItemSerializer
    lookup_field='id'
    def get_queryset(self):
        key=self.request.session.session_key
        return CartItem.objects.filter(cart__session_key=key)
class CartItemUpdateView(generics.UpdateAPIView): # or generics.RetrieveUpdateDestroyAPIView
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        action = request.query_params.get('action')

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
        else:
            new_quantity = request.data.get('quantity')
            if new_quantity is not None:
                cart_item.quantity = int(new_quantity)
        if cart_item.quantity <= 0:
            cart_item.delete()
            return Response({"message": "Item deleted from cart"}, status=status.HTTP_200_OK)
        if cart_item.quantity > cart_item.product_variant.quantity:
            return Response({"error": "Product out of stock"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response({
            "message": "Item quantity updated",
            "item": serializer.data
        }, status=status.HTTP_200_OK)