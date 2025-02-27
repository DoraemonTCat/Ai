import hmac
import hashlib
import time
import json
import requests
import base64

# กำหนด API Key และ Secret Key
api_key = "AIzaSyDZWPTPjfbZbCzewYN04-zzW8dCuiTna_k"

# กำหนด payload สำหรับการยืนยันตัวตน
payload = {
    "request": "/v1/account",  # endpoint ที่ต้องการเรียก
    "nonce": int(time.time() * 1000)  # ค่า nonce (ต้องไม่ซ้ำ)
}

# เข้ารหัส payload ด้วย Base64
encoded_payload = base64.b64encode(json.dumps(payload).encode())

# สร้าง signature ด้วย HMAC และ SHA384

# กำหนด Header สำหรับคำขอ
headers = {
    "Content-Type": "text/plain",
    "Content-Length": "0",
    "X-GEMINI-APIKEY": api_key,
    "X-GEMINI-PAYLOAD": encoded_payload.decode()

}

# เรียกใช้ API
url = "https://api.gemini.com/v1/account"  # ใช้ URL Production หรือ Sandbox
response = requests.post(url, headers=headers)

# แสดงผลลัพธ์
print(response.json())
