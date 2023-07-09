import requests

url = 'http://localhost:5000/API/single'

#show error
data = {'key1': 'value1','key2': 'value2'}
response = requests.post(url, json=data)
print(response.text)

data = {'V':5,'K':8,'A':7}
response = requests.post(url, json=data)
print(response.text)

url = 'http://localhost:5000/API/multiple'
data = {'Datas':[{'V':5,'K':8,'A':7},{'V':5,'K':8,'A':9}]}
response = requests.post(url, json=data)
print(response.text)