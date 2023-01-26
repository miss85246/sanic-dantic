---
hide:

- toc

---

# 基于类视图的使用方法

## 使用 `HTTPMethodView` 来进行参数检查

您依旧可以像以前一样使用 `parse_params` 来为每个方法添加参数检查。

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

当然，`parse_params` 也可以添加到 `decorators` 的方式来进行使用。

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

## 使用 `DanticView` 来进行参数检查

除了使用 sanic 内置的 `HTTPMethodView` 之外，sanic-dantic 还提供了 `DanticView`
，它继承自 `HTTPMethodView` ，重写了 `dispatch_request` 方法，使其支持参数检查。

在继承 `DanticView` 时，需要定义对应的 `{method}_model`，例如 `get_model` 等。

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