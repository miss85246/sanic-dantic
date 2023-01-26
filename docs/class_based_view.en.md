---
hide:

- toc

---

# Class Based View Usage

## Using `HTTPMethodView` to check parameters

When using `HTTPMethodView` , you can also use `parse_params` to check
parameters for each method.

```python
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_dantic import parse_params, BaseModel, Field


class Person(BaseModel):
    name: str = Field(description="name")
    age: int = Field(description="age")


class MyView(HTTPMethodView):

    @parse_params(query=Person)
    async def get(self, request, params):
        return json({"ctx": request.ctx.params, "params": params})

```

of course, `parse_params` can also be added to the `decorators` attribute.

```python
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_dantic import parse_params, BaseModel, Field


class Person(BaseModel):
    name: str = Field(description="name")
    age: int = Field(description="age")


class MyView(HTTPMethodView):
    decorators = [parse_params(query=Person, methods=["GET"])]

    @staticmethod
    async def get(request, params):
        return json({"ctx": request.ctx.params, "params": params})

    @staticmethod
    async def post(request, params):
        return json({"ctx": request.ctx.params, "params": params})

```

## Using `DanticView` to check parameters

In addition to using the `HTTPMethodView` built into sanic , sanic-dantic also
provides `DanticView` , which inherits from `HTTPMethodView` and overrides the
`dispatch_request` method to support parameter checking.

When inheriting `DanticView` , you need to define the corresponding
`{method}_model` , such as `get_model` , etc.

```python
from sanic.response import json
from sanic_dantic import DanticView, Field


class MyView(DanticView):

    @staticmethod
    async def get(request, params):
        return json({"ctx": request.ctx.params, "params": params})

    def get_model(self):
        class Person:
            name: str = Field(description="name")
            age: int = Field(description="age")

        return self.DanticModel(query=Person)
```