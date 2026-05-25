from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order,OrderItem
from cart.models import Cart,CartItem
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import OrderSerializer,OrderItemSerializer
from django.db import transaction
# Create your views here.
class OrderView(APIView):
    def get_permissions(self):
        if self.request.method=='GET' or self.request.method=='DELETE':
            return [IsAdminUser()]
        return []
    def post(self,request):
        cart_id=request.session.session_key
        if not cart_id:
            return Response({"error":"your cart is empty"},status=status.HTTP_404_NOT_FOUND)
        cart=Cart.objects.filter(session_key=cart_id).first()
        if not cart or not cart.items.exists():
            return Response({"error":"your cart is empty"},status=status.HTTP_404_NOT_FOUND)
        fullname=request.data.get('user_fullname')
        email=request.data.get('user_email')
        number=request.data.get('user_number')
        if not fullname or not number or not email:
            return Response({"error":"fullname, email and number is required"},status=status.HTTP_400_BAD_REQUEST)
        cart_items=cart.items.all()
        total_price = 0
        for item in cart_items:
            total_price+=item.product_variant.product.price*item.quantity
        with transaction.atomic():
            order=Order.objects.create(user_fullname=fullname,user_email=email,user_number=number,total_price=total_price)
            order_items = []
            for item in cart_items:
                order_items.append(OrderItem(order=order,product_variant=item.product_variant,quantity=item.quantity))
            OrderItem.objects.bulk_create(order_items)
            cart.delete()
        return Response({"message":"Order created"},status=status.HTTP_201_CREATED)
            
    def get(self,request):
        orders=Order.objects.all().order_by('-created_at')
        serializer=OrderSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def delete(self,request,id):
        try:
            order = Order.objects.get(id=id)
            order.delete()
            return Response({"message":"order deleted"},status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error":"order not found"},status=status.HTTP_404_NOT_FOUND)
