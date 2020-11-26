import unittest

from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView

from sanic_dantic import parse_params, BaseModel, DanticView


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


class HTTPMethodTestView(HTTPMethodView):
    decorators = [parse_params(method=['POST'], body=Person)]

    @parse_params(query=Person)
    async def get(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    async def post(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    async def put(self, request, params):
        return json({"params": params, "request.ctx.params": request.json})


class DanticTestView(DanticView):
    decorators = [parse_params(method=['POST'], form=Person)]

    async def get(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    async def post(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    @parse_params(body=Person)
    async def put(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    def get_model(self):
        return self.DanticModel(query=Person)


app.add_route(HTTPMethodTestView.as_view(), '/http_test')
app.add_route(DanticTestView.as_view(), '/dantic_test')


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

    def test_http_method_view_post_test(self):
        url = f'/http_test'
        req, res = self.client.post(url, json=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_http_method_view_put_test(self):
        url = f'/http_test'
        req, res = self.client.put(url, json=self.data)
        self.assertEqual(res.status_code, 500), res.status_code

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
