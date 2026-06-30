import requests
from django.conf import settings
from .models import OrderItem 
from urllib.parse import urljoin

def get_wakilni_token():
    url = urljoin(settings.WAKILNI_BASE_URL, "api/v2/third_party/auth_token")
    body = {
        "key": settings.WAKILNI_KEY,
        "secret": settings.WAKILNI_SECRET
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.get(url, params=body, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json().get('token')
def create_wakilni_order(order):
    address = order.address
    try:
        token = get_wakilni_token()
    except Exception as e:
        print(f"Request failed during authentication: {e}")
        return None
        
    order_items = []
    clean_phone_number = ''.join(filter(str.isdigit, str(address.receiver_phone_number)))
    clean_receiver_id = int(clean_phone_number)
    clean_secondary_phone_number = ''.join(filter(str.isdigit, str(address.receiver_secondary_phone_number)))
    db_items = OrderItem.objects.filter(order=order)
    for item in db_items:
        order_items.append({
            "quantity": item.quantity,
            "type_id": 57, 
            "name": item.product_variant.product.name,
            "sku": str(item.product_variant.product.id)
        })
        
    try:
        pickup_payload = {
            "location_id": 1, 
            "longitude": 35.5018,
            "latitude": 33.8938, 
            "floor": 1,
            "area": "Beirut"
        }
        headers = {
            'Authorization': f'Bearer {token}',
        }
        
        start_bulk = f"{settings.WAKILNI_BASE_URL}/api/v2/clients/start_bulk"
        response = requests.post(start_bulk, json=pickup_payload, headers=headers, timeout=10)
        response.raise_for_status()
        bulk_id = response.json().get('bulk_id')
        body = {
            "get_order_details": False,
            "get_barcode": True,
            "waybill": str(order.id),
            "receiver_id": clean_receiver_id,
            "receiver_first_name": address.receiver_first_name,
            "receiver_last_name": address.receiver_last_name,
            "receiver_phone_number": clean_phone_number,
            "receiver_gender": str(address.receiver_gender),
            "receiver_email": address.receiver_email,
            "receiver_secondary_phone_number": clean_secondary_phone_number,
            "receiver_location_id": address.id,
            "receiver_longitude": None,
            "receiver_latitude": None,
            "receiver_building": address.receiver_building,
            "receiver_floor": int(address.receiver_floor),
            "receiver_directions": address.receiver_directions,
            "receiver_area": address.receiver_area,
            "currency": 1,              
            "cash_collection_type_id": 52, 
            "collection_amount": float(order.total_price),
            "note": "",
            "car_needed": False,
            "packages": order_items
        }
        url = f"{settings.WAKILNI_BASE_URL}/api/v2/clients/add_delivery/{bulk_id}"
        final_response = requests.post(url, json=body, headers=headers, timeout=10)
        final_response.raise_for_status()
        end_bulk_url = f"{settings.WAKILNI_BASE_URL}/api/v2/clients/end_bulk/{bulk_id}"
        end_bulk_response = requests.post(end_bulk_url, headers=headers, timeout=10)
        end_bulk_response.raise_for_status()
        
        return final_response
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response data: {e.response.text}")
        return getattr(e, "response", None)
def cancel_wakilni_order(order_id,reason):
    try:
        token = get_wakilni_token()
    except Exception as e:
        print(f"Request failed during authentication: {e}")
        return None
    headers = {
        'Authorization': f'Bearer {token}',
    }
    body={
        "reason": reason
    }
    url = f"{settings.WAKILNI_BASE_URL}/api/v2/clients/orders/{order_id}/cancel"
    response = requests.post(url, json=body, headers=headers, timeout=10)
    response.raise_for_status()
    return response
def get_wakilni_areas():
    token = get_wakilni_token()
    if not token:
        raise ValueError("Could not retrieve a valid token from Wakilni.")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = f"{settings.WAKILNI_BASE_URL}/api/v2/areas?with_filter=false&with_pagination=false"
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    response.raise_for_status()
    return response.json()