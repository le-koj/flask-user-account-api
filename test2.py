import requests

BASE = "http://127.0.0.1:5000/"


#user_id = input("input user ID: ")
response = requests.get(BASE + f"")
print(response.text)