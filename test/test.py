import unittest

from sanic import Sanic
from sanic.exceptions import ServerError, SanicException
from sanic.response import json
from sanic.views import HTTPMethodView

from sanic_dantic import BaseModel, DanticView, parse_params
from sanic_dantic.basic_definition import DanticModelObj

app = Sanic("SanicDanticExample")


# define class Person who inherited from pydantic.BaseModel
class Person(BaseModel):
    name: str
    age: int


# define class Car to test DanticModelObj TypeError
class Car:
    name: str
    age: int


# define error handler function
def error_handler(request, e):
    print(request.args, e)
    return SanicException(message="this is message in error_handler", status_code=403)


# --------------------------------------------- define function based views --------------------------------------------

@app.route('/path_test/<name>/<age>/', methods=['GET'])
@parse_params(path=Person)
async def path_test(request, name, age, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})


@app.route('/query_test', methods=['GET'])
@parse_params(query=Person, error=error_handler)
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


@app.route('/header_test', methods=['GET'])
@parse_params(header=Person)
async def strict_test(request, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})


# ------------------------------------------------ define class based views --------------------------------------------

class SanicDanticTestView(HTTPMethodView):
    decorators = [parse_params(methods=['POST'], body=Person), parse_params(query=Person)]

    async def get(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    async def post(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    @parse_params(body=Person)
    async def put(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})


# ------------------------------------------------ define class based views --------------------------------------------

class DanticTestView(DanticView):
    decorators = [parse_params(methods=['POST'], body=Person), parse_params(query=Person)]

    async def get(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    async def post(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    @parse_params(body=Person)
    async def put(self, request, params):
        return json({"params": params, "request.ctx.params": request.ctx.params})

    def get_model(self):
        return self.DanticModel(query=Person)


app.add_route(SanicDanticTestView.as_view(), '/cbv_test')
app.add_route(DanticTestView.as_view(), '/dtv_test')


# --------------------------------------------------- define test class ------------------------------------------------

class TestSanicDantic(unittest.TestCase):

    def setUp(self):
        self.data = {"name": "test", "age": 100}
        self.client = app.test_client
        self.expected_result = {"params": self.data, "request.ctx.params": self.data}

    # ------------------------------------------- -- function based view test -- ---------------------------------------

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

    def test_error_handler_test(self):
        url = '/query_test/'
        req, res = self.client.get(url, params={"name": "test"})
        self.assertEqual(403, res.status_code), res.status_code

    # ----------------------------------- -- class based view test for HTTPMethodView -- -------------------------------

    def test_cbv_get_test(self):
        url = '/cbv_test/'
        req, res = self.client.get(url, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_cbv_post_test(self):
        url = '/cbv_test/'
        req, res = self.client.post(url, json=self.data, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_cbv_put_test(self):
        url = '/cbv_test/'
        req, res = self.client.put(url, json=self.data, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    # ----------------------------------- -- class based view test for DanticView -- -------------------------------

    def test_dtv_get_test(self):
        url = '/dtv_test/'
        req, res = self.client.get(url, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_dtv_post_test(self):
        url = '/dtv_test/'
        req, res = self.client.post(url, json=self.data, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_dtv_put_test(self):
        url = '/dtv_test/'
        req, res = self.client.put(url, json=self.data, params=self.data)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    # -------------------------------------------------- -- error test -- ----------------------------------------------

    def test_dtv_invalid_usage(self):
        url = '/dtv_test/'
        req, res = self.client.get(url, params={"name": "test"})
        self.assertEqual(res.status_code, 400), res.status_code

    def test_body_and_form(self):
        url = "/body_and_form_test"
        req, res = self.client.post(url, json=self.data, data=self.data)
        self.assertEqual(res.status_code, 500), res.status_code

    def test_body_mismatching_method(self):
        url = "/body_mismatching_method_test"
        req, res = self.client.get(url, params=self.data)
        self.assertEqual(res.status_code, 500), res.status_code

    def test_invalid_usage(self):
        url = '/body_test/'
        req, res = self.client.post(url, json={"name": "test", "age": "abc"})
        self.assertEqual(res.status_code, 400), res.status_code

    def test_type_error(self):
        try:
            DanticModelObj(query=Person, form=Car)
        except ServerError as e:
            print(DanticModelObj(query=Person))
            self.assertEqual(type(e), ServerError)

    # ------------------------------------------------ -- header test -- -----------------------------------------------
    def test_close_strict(self):
        url = '/header_test'
        self.headers = {k: str(v) for k, v in self.data.items()}
        req, res = self.client.get(url, headers=self.headers)
        self.assertEqual(res.status_code, 200), res.status_code
        self.assertEqual(res.json, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"


if __name__ == '__main__':
    unittest.main()
