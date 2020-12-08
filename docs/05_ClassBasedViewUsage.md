# Class-Based View Usage

`sanic-dantic` not only supports [function-based view](https://miss85246.github.io/sanic-dantic/FunctionBasedViewUsage/)
, it also supports class-based views.

## Use like FBV

In class-based view, you can also use sanic-dantic like FBV:

```python
from sanic import Sanic
from sanic_dantic import BaseModel, parse_params
from sanic.views import HTTPMethodView
from sanic.response import json

app = Sanic("example")


class Person(BaseModel):
    name: str
    age: int


class ExampleView(HTTPMethodView):
    @parse_params(query=Person)
    async def get(self, request, params):
        print({"name": request.ctx.params.name, "age": request.ctx.params.age})
        return json({"name": params.name, "age": params.age})


app.add_route(ExampleView.as_view(), '/example')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```

## Pass it to HTTPMethodView's decorators

You can also pass it to HTTPMethodView's decorators:

parameter `methods` is not required. it will be applicable to all view checks if don't give

```python
from sanic import Sanic
from sanic_dantic import BaseModel, parse_params
from sanic.views import HTTPMethodView
from sanic.response import json

app = Sanic("example")


class Person(BaseModel)
    name: str
    age: int


class ExampleView(HTTPMethodView):
    decorators = [parse_params(methods=['GET'], query=Person)]

    async def get(self, request, params):
        print({"name": request.ctx.params.name, "age": request.ctx.params.age})
        return json({"name": params.name, "age": params.age})


app.add_route(ExampleView.as_view(), '/example')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```

## Use DanticView

If you don't like use decorator way, you can use `DanticView`.

`DanticView` is Inherited from `HTTPMethodView`, In here, you needn't use a decorator to complete the type check.

You can define method model like define method function, sanic-dantic will be parsing and help you check it.

```python
from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel, DanticView


class Person(BaseModel):
    name: str
    age: int


app = Sanic("example")


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
    def get_model(self):  # You need define this function if you want check method
        return self.DanticModel(query=Person)  # DanticModel is DanticView's Attribute


app.add_route(DanticTestView.as_view(), '/dantic_test')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```

#### Note

> method_model don't support define by async.

DanticView inherits from HTTPMethodView, and it supports all usages in HTTPMethodView, including the usage of
sanic-dantic in HTTPMethodView.