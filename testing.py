
import requests

domain = "localhost"
port = 8085
endpoint = "real"
url = f'http://{domain}:{port}/{endpoint}'
payload = {
    "message": "apa itu capd?",
    "sender": "user"
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())
