import requests

r = requests.get("https://api.notion.com/v1/oauth/authorize?owner=user&client_id=463558a3-725e-4f37-b6d3-0889894f68de&redirect_uri=https%3A%2F%2Fexample.com%2Fauth%2Fnotion%2Fcallback&response_type=code", params = "{client_id:'c0881eda-977e-4f58-88ee-1558366971b7', response_type: 'code', owner: 'user'}")

print(r.text)