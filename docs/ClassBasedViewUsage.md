# Class-Based View Usage

## Use like FBV
In class-based view, you can also use sanic-dantic like FBV:
```python
import unittest

from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView

from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


class HTTPMethodTestView(HTTPMethodView):

    @parse_params(query=Person)
    async def get(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})


app.add_route(HTTPMethodTestView.as_view(), '/http_test')


class TestSanicDantic(unittest.TestCase):

    def setUp(self):
        self.data = {"name": "test", "age": 100}
        self.client = app.test_client
        self.expected_result = {"params": self.data, "request.ctx.params": self.data}

    def test_http_method_view_get_test(self):
        url = f'/http_test'
        req, res = self.client.get(url, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

```
## Pass it to HTTPMethodView's decorators

You can also passed it to HTTPMethodView's decorators:

parameter `methods` is not required. it will be applicable to all view checks if don't give
```python
import unittest

from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView

from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


class HTTPMethodTestView(HTTPMethodView):
    decorators = [parse_params(methods=['POST'], body=Person)]

    async def post(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})


app.add_route(HTTPMethodTestView.as_view(), '/http_test')


class TestSanicDantic(unittest.TestCase):

    def setUp(self):
        self.data = {"name": "test", "age": 100}
        self.client = app.test_client
        self.expected_result = {"params": self.data, "request.ctx.params": self.data}

    def test_http_method_view_post_test(self):
        url = f'/http_test'
        req, res = self.client.post(url, json=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

```

## Use DanticView
If you don't like use decorator way, you can use `DanticView`.

`DanticView` is Inherited from `HTTPMethodView`, In here, you needn't to use a decorator to complete the type check.

You can define method model like define method function, sanic-dantic will be parsed and help you check it.


```python
import unittest
from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel, DanticView


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


class DanticTestView(DanticView):
    decorators = [parse_params(methods=['POST'], form=Person)]

    async def get(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    async def post(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    @parse_params(body=Person)
    async def put(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})
    
    # Format: method_model
    def get_model(self):    # You need define this function if you want check method
        return self.DanticModel(query=Person) # DanticModel is DanticView's Attribute


app.add_route(DanticTestView.as_view(), '/dantic_test')


class TestSanicDantic(unittest.TestCase):

    def setUp(self):
        self.data = {"name": "test", "age": 100}
        self.client = app.test_client
        self.expected_result = {"params": self.data, "request.ctx.params": self.data}

    def test_dantic_method_view_get_test(self):
        url = '/dantic_test'
        req, res = self.client.get(url, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_dantic_method_view_post_test(self):
        url = "/dantic_test"
        req, res = self.client.post(url, data=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_dantic_method_view_put_test(self):
        url = "/dantic_test"
        req, res = self.client.put(url, json=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"
```
DanticView inherits from HTTPMethodView, and it supports all usages in HTTPMethodView, including the usage of sanic-dantic in HTTPMethodView.