import unittest

from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView

from sanic_dantic import parse_params, BaseModel

app = Sanic("SanicDanticExample")


class Person(BaseModel):
    name: str
    age: int


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


@app.route('/body_and_form_test', methods=['POST'])
@parse_params(body=Person, form=Person)
async def body_test(request, params):
    pass


@app.route('/body_mismatching_method_test', methods=['GET'])
@parse_params(body=Person)
async def body_test(request, params):
    pass


class SanicDanticTestView(HTTPMethodView):
    @parse_params(query=Person)
    async def get(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    @parse_params(form=Person)
    async def post(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    @parse_params(body=Person)
    async def put(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})


app.add_route(SanicDanticTestView.as_view(), '/cbv_test')


class TestSanicDantic(unittest.TestCase):

    def setUp(self):
        self.data = {"name": "test", "age": 100}
        self.client = app.test_client
        self.expected_result = {"params": self.data, "request.ctx.params": self.data}

    def test_path_test(self):
        url = f'/path_test/{self.data["name"]}/{self.data["age"]}/'
        req, res = self.client.get(url)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_get_test(self):
        url = '/query_test/'
        req, res = self.client.get(url, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_form_test(self):
        url = '/form_test/'
        req, res = self.client.post(url, data=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_body_test(self):
        url = '/body_test/'
        req, res = self.client.post(url, json=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_cbv_query_test(self):
        url = '/cbv_test/'
        req, res = self.client.get(url, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_cbv_form_test(self):
        url = '/cbv_test/'
        req, res = self.client.post(url, data=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_cbv_body_test(self):
        url = '/cbv_test/'
        req, res = self.client.put(url, json=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_body_and_form(self):
        url = "/body_and_form_test"
        req, res = self.client.post(url, json=self.data, data=self.data)
        self.assertEqual(res.status_code, 500), res.status_code

    def test_body_mismatching_method(self):
        url = "/body_mismatching_method_test"
        req, res = self.client.get(url, params=self.data)
        self.assertEqual(res.status_code, 500), res.status_code

    def test_invalid_usage(self):
        url = '/query_test/'
        req, res = self.client.get(url, params={"name": "test", "age": "abc"})
        self.assertEqual(res.status_code, 400), res.status_code


if __name__ == '__main__':
    unittest.main()
