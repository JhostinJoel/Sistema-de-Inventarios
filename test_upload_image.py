import requests
import os

# Configuration
BASE_URL = 'http://127.0.0.1:8000'
LOGIN_URL = f'{BASE_URL}/users/login/'
ADD_PRODUCT_URL = f'{BASE_URL}/inventory/products/add/'
IMAGE_PATH = r'C:\Users\jhost\.gemini\antigravity\brain\ddaa004b-f33f-4434-a2a6-b9d479bbd24a\uploaded_image_0_1765820850353.jpg'

# Create session
session = requests.Session()

# 1. Login
print("Logging in...")
response = session.get(LOGIN_URL)
csrftoken = session.cookies['csrftoken']
login_data = {
    'username': 'jhostin',
    'password': '12345678',
    'csrfmiddlewaretoken': csrftoken
}
response = session.post(LOGIN_URL, data=login_data, headers={'Referer': LOGIN_URL})
print(f"Login Status: {response.status_code}")

if response.status_code != 200:
    print("Login failed")
    exit()

# 2. Upload Product
print("Uploading product...")
response = session.get(ADD_PRODUCT_URL)
csrftoken = session.cookies['csrftoken']

product_data = {
    'code': 'TEST_IMG_01',
    'name': 'Test Product Image',
    'description': 'Test Description',
    'category': '1', # Assuming ID 1 exists (General)
    'price': '100',
    'cost': '50',
    'stock': '10',
    'min_stock': '5',
    'csrfmiddlewaretoken': csrftoken
}

files = {
    'image': open(IMAGE_PATH, 'rb')
}

response = session.post(ADD_PRODUCT_URL, data=product_data, files=files, headers={'Referer': ADD_PRODUCT_URL})
print(f"Upload Status: {response.status_code}")
print(f"Final URL: {response.url}")

if 'inventory/products/' in response.url:
    print("Upload successful (redirected to list)")
else:
    print("Upload failed (stayed on form?)")
    # print(response.text)
