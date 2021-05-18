import requests

data = {"difficulty": "1", "category": "anime"}
url = "https://api-29-seconds.herokuapp.com/api/https://api-29-seconds.herokuapp.com/api"
response = requests.post(url, data)
print(response.text)