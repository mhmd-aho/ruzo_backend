from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order, OrderItem, RecieverAddress
from cart.models import Cart
from product.models import ProductVariant
from .shipping import create_wakilni_order
# Create your views here.

class CheckOutView(APIView):
    def post(self, request):
        cart_id = request.session.session_key
        if not cart_id:
            return Response({"error": "Your cart is empty"}, status=status.HTTP_404_NOT_FOUND)
            
        cart = Cart.objects.filter(session_key=cart_id).first()
        if not cart or not cart.items.exists():
            return Response({"error": "Your cart is empty"}, status=status.HTTP_404_NOT_FOUND)

        cart_items = cart.items.all()
        total_price = 0
        with transaction.atomic():
            address = RecieverAddress.objects.create(
                receiver_first_name=request.data.get('receiver_first_name'),
                receiver_last_name=request.data.get('receiver_last_name'),
                receiver_phone_number=request.data.get('receiver_phone_number'),
                receiver_gender=request.data.get('receiver_gender'),
                receiver_email=request.data.get('receiver_email'),
                receiver_secondary_phone_number=request.data.get('receiver_secondary_phone_number'),
                receiver_longitude=request.data.get('receiver_longitude'),
                receiver_latitude=request.data.get('receiver_latitude'),
                receiver_building=request.data.get('receiver_building'),
                receiver_floor=request.data.get('receiver_floor'),
                receiver_directions=request.data.get('receiver_directions'),
                receiver_area=request.data.get('receiver_area')
            )
            order = Order.objects.create(address=address, total_price=0, status='pending')
            order_items = []
            for item in cart_items:
                variant = ProductVariant.objects.select_for_update().get(id=item.product_variant_id)
                
                # Note: your model uses variant.quantity for stock tracking
                if variant.quantity < item.quantity:
                    return Response({"error": f"Product {variant.product.name} is out of stock"}, status=status.HTTP_400_BAD_REQUEST)
                
                variant.quantity -= item.quantity
                variant.save()

                total_price += variant.product.price * item.quantity
                order_items.append(OrderItem(order=order, product_variant=variant, quantity=item.quantity))

            OrderItem.objects.bulk_create(order_items)
            order.total_price = total_price
            order.save()
            response = create_wakilni_order(order)
            if response and response.status_code in [200, 201]:
                wakilni_data = response.json()
                order.status = 'shipped'
                order.barcode = wakilni_data.get('barcode')
                order.save()
                cart.delete()
                return Response({"message": "Order created and synced with Wakilni!", "order_id": order.id}, status=status.HTTP_201_CREATED)
            else:
                order.status = 'failed_to_ship'
                order.save()
                cart.delete()
                return Response({
                    "message": "Order saved locally, but failed to sync with Wakilni routing nodes.", 
                    "order_id": order.id
                }, status=status.HTTP_201_CREATED)
class OrderView(APIView):
    def get_permissions(self):
        if self.request.method=='GET' or self.request.method=='DELETE':
            return [IsAdminUser()]
        return []
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