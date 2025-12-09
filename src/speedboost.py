import requests

url = "https://api.test.fiindo.com/api/v1/speedboost"
payload = {
    "first_name": "fionn",
    "last_name": "zak"
}

headers = {
    "Authorization": "Bearer fionn.zak"
}

resp = requests.post(url, json=payload, headers=headers)

print("STATUS:", resp.status_code)
print("RESPONSE:", resp.text)
