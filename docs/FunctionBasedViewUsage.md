# Function-Based View Usage

## Overview
In FBV you can directly use the parse_params' method to check parameters:
```python
import unittest
from sanic import Sanic
from sanic.response import json
from sanic_dantic import parse_params, BaseModel

class Person(BaseModel):
    name:str
    age:int

app = Sanic("SanicDanticTest")

@app.route('/query_test', methods=['GET'])
@parse_params(query=Person)
async def query_test(request, params):
    assert params.name == request.ctx.params
     # {"params":{"name":"test", "age": 100}, "ctx.params":{"name":"test", "age": 100}}
    return json({"params":params, "ctx.params":request.ctx.params})

class SimpleTest(unittest.TestCase):
    def test_simple_usage(self):
        data = {"name":"test", "age": 100}
        req, res = app.test_client.get("/query_test", params=data)
        self.assertEqual(res.json, {"params":data, "ctx.params":data})
    
if __name__ == '__main__':
    unittest.main()
```

## Specify the inspection mode

In sanic-dantic, you can modify it to any inspection mode by specifying different models

`path`, `query`, `form`, `body` are four different inspection modes

* `path`: If you appoint it, sanic-dantic will help check path params. It applies to `GET`
* `query`: If you appoint it, sanic-dantic will help check url params. It applies to `GET`
* `form`: If you appoint it, sanic-dantic will help check data params. It applies to `GET`, `PUT`, `POST`
* `body`: If you appoint it, sanic-dantic will help check body params. It applies to `POST`, `PUT`, `PATCH`
* **Notice**: the applies is just suggest, It's not mean can't use with other method, you can try it

```python
from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


@app.route('/path_test/<name>/<age>/', methods=['GET'])
@parse_params(path=Person)
async def path_test(request, name, age, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})


@app.route('/query_test', methods=['GET'])
@parse_params(query=Person)
async def get_test(request, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})


@app.route('/form_test', methods=['GET', 'POST'])
@parse_params(form=Person)
async def path_test(request, params):
    params.__getattr__("name")
    params.__setattr__("age", params.age)
    return json({"params": params, "request.ctx.params": request.ctx.params})


@app.route('/body_test', methods=['POST', 'PUT', 'PATCH'])
@parse_params(body=Person)
async def body_test(request, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})
```

## Use multiple checks at the same time
sanic-dantic support use multiple checks at the same time. you can use it like this:

```python
from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


@app.route('/path_test/<name>/<age>/', methods=['GET'])
@parse_params(path=Person, body=Person, query=Person)
async def get_test(request, name, age, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})
```

