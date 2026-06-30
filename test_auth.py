import requests

url = "https://api-dev.wakilni.com/api/v2/third_party/auth_token"
body = {
    "key": "qFKKnobTtW",
    "secret": "LY1lw7Jy7NJ9J7XLijLCYsFkbf14voFrUeV"
}
headers = {
    "Accept": "application/json"
}
# Test with params
print("Testing with params...")
response1 = requests.get(url, params=body, headers=headers, timeout=10)
print("Status:", response1.status_code)
print("Body:", response1.text[:200])

# Test with json
print("\nTesting with json...")
response2 = requests.get(url, json=body, headers=headers, timeout=10)
print("Status:", response2.status_code)
print("Body:", response2.text[:200])
