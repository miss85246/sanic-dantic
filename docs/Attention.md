# Attention
Although sanic-dantic can help you improve the inspection efficiency, it is not omnipotent.

## Don't use form with body
Both `form` and `json` use request.json to pass parameters, but their formats are completely different
```shell
form: name=test&age=12
json: {"name":"test", "age":12}
```
If you use form with body, It's will raise ServerError:
```python
import unittest
from sanic import Sanic

from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")

@app.route('/body_and_form_test', methods=['POST'])
@parse_params(body=Person, form=Person)
async def body_and_form_test(request, params):
    pass



class TestSanicDantic(unittest.TestCase):

    def setUp(self):
        self.data = {"name": "test", "age": 100}
        self.client = app.test_client
        self.expected_result = {"params": self.data, "request.ctx.params": self.data}
    
    def test_body_and_form(self):
        url = "/body_and_form_test"
        req, res = self.client.post(url, json=self.data, data=self.data)
        self.assertEqual(res.status_code, 500), res.status_code

if __name__ == '__main__':
    unittest.main()

```

## The same param name will be overwritten

sanic-dantic's type checking has a sequence, and if you use the same parameter name, some parameters may be overwritten

Their priorities are: `form` = `body` > `query` > `path`

```python
import unittest
from sanic import Sanic
from sanic.response import json
from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")

@app.route('/overwritten_test', methods=['POST'])
@parse_params(body=Person, query=Person)
async def overwritten_test(request, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})



class TestSanicDantic(unittest.TestCase):

    def setUp(self):
        self.data = {"name": "test", "age": 100}
        self.client = app.test_client
        self.expected_result = {"params": self.data, "request.ctx.params": self.data}
    
    def test_param_overwritten(self):
        url = "/overwritten_test"
        params = {"name":"test", "age":100}
        data = {"name":"test", "age":200}
        req, res = self.client.post(url, json=data, params=params)
        self.assertEqual(res.json, {"params":data, "ctx.params":data})

if __name__ == '__main__':
    unittest.main()
```