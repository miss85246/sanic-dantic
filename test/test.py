import requests

form_data = {'name': 'bwm', 'speed': 100}
body_data = {'name': 'connor', 'age': 13}
res = requests.post('http://localhost:5000/test', json=body_data, data=form_data, )
print(res.text)
