import requests
parameters = {
    'collection': 'azuki-god',
    'limit': 1
}
r = requests.get("https://testnets-api.opensea.io/api/v1/assets", params = parameters)

print(r.json())
 