import requests

BASE_URL = "http://localhost:5000/"

response = requests.put(BASE_URL+"video/1",{"likes":10})

print(response.json())