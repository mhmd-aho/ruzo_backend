import requests
from django.conf import settings
def get_wakilni_token():
    url = f"{settings.WAKILNI_BASE_URL}/api/v2/third_party/auth_token"
    body = {
        "key": settings.WAKILNI_KEY,
        "secret": settings.WAKILNI_SECRET
    }
    response = requests.get(url, json=body, timeout=10)
    response.raise_for_status()
    return response.json().get('token')
def create_wakilni_order(order):
    address=order.address
    try:
        token=get_wakilni_token()
    except Exception as e:
        print(f"Request failed: {e}")
        return None
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
    try:
        pickup_payload={
            "location_id": 1, 
            "longitude": 35.5018,
            "latitude": 33.8938, 
            "floor": 1,
            "area": "Beirut"
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        start_bluk = f"{settings.WAKILNI_BASE_URL}/api/v2/clients/start_bulk"
        response = requests.post(start_bluk, json=pickup_payload, headers=headers, timeout=10)
        response.raise_for_status()
        bulk_id = response.json().get('bulk_id')
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
        url = f"{settings.WAKILNI_BASE_URL}/api/v2/clients/add_delivery/{bulk_id}"
        final_response= requests.post(url,json=body,headers=headers,timeout=10)
        final_response.raise_for_status()
        data = final_response.json()
        end_bulk_url = f"{settings.WAKILNI_BASE_URL}/api/v2/clients/end_bulk/{bulk_id}"
        end_bulk_response = requests.post(end_bulk_url, headers=headers, timeout=10)
        end_bulk_response.raise_for_status()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text}")
        return None
    
