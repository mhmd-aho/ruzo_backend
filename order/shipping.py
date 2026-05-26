import requests
from django.conf import settings
def create_wakilni_order(order):
    address=order.address
    order_items=[]
    clean_phone_number = ''.join(filter(str.isdigit, str(address.receiver_phone_number)))
    clean_receiver_id = int(clean_phone_number)
    clean_secondary_phone_number = ''.join(filter(str.isdigit, str(address.receiver_secondary_phone_number)))
    for item in order.items.all():
        order_items.append({
            "quantity": item.quantity,
            "type_id": 57,
            "name": item.product_variant.product.name,
            "sku": item.product_variant.product.id
        })
    url = 'https://api-dev.wakilni.com'
    headers = {
        'Authorization': f'Bearer {settings.WAKILNI_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    body = {
    "get_order_details": False,
    "get_barcode": True,
    "waybill": order.id,
    "receiver_id": clean_receiver_id,
    "receiver_first_name":address.receiver_first_name,
    "receiver_last_name": address.receiver_last_name,
    "receiver_phone_number": clean_phone_number,
    "receiver_gender": str(address.receiver_gender),
    "receiver_email": address.receiver_email,
    "receiver_secondary_phone_number": clean_secondary_phone_number,
    "receiver_location_id": address.id,
    "receiver_longitude": float(address.receiver_longitude),
    "receiver_latitude": float(address.receiver_latitude),
    "receiver_building": address.receiver_building,
    "receiver_floor": int(address.receiver_floor),
    "receiver_directions": address.receiver_directions,
    "receiver_area": address.receiver_area,
    "currency": 1,
    "cash_collection_type_id": 52,
    "collection_amount": float(order.total_price),
    "note": "",
    "car_needed": False,
    "packages":order_items
    }
    try:
        response= requests.post(url,json=body,headers=headers,timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    
