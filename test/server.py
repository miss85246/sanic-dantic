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
    return json({"params": params, "request.ctx.params": request.ctx.params})


@app.route('/body_test', methods=['POST', 'PUT', 'PATCH'])
@parse_params(body=Person)
async def body_test(request, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})


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

if __name__ == '__main__':
    app.run(host='localhost', port=5000)