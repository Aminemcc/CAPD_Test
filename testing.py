
import requests

domain = "localhost"
port = 8085
endpoint = "real"

domain = "10.199.13.61"
port = 5009
endpoint = "webhooks/rest/webhook"

url = f'http://{domain}:{port}/{endpoint}'
payload = {
    "message": "apa itu capd?",
    "sender": "user"
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())
