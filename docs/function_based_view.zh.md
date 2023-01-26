---
hide:

- toc

---

# 基于函数视图的使用方法

sanic-dantic 提供了 `parse_params` 装饰器，它可以用来为函数视图添加参数检查。

```python
from sanic import Sanic
from sanic.response import json
from sanic_dantic import parse_params, BaseModel, Field

app = Sanic(__name__)
app.config.FALLBACK_ERROR_FORMAT = "json"


class Person(BaseModel):
    name: str = Field(description="name")
    age: int = Field(description="age")


@app.route("/person")
@parse_params(query=Person)
async def person(request, params):
    return json({"ctx": request.ctx.params, "params": params})


if __name__ == "__main__":
    app.run(host="localhost", port=8000, dev=True)
```

## 参数检查的顺序

越靠前的参数检查优先级越高，如果前面的参数检查失败，后面的参数检查将不会进行。

!!! note annotate "关于检查顺序"

    sanic-dantic 会按照以下顺序进行参数检查：

    `header` -> `path` -> `query` -> `form` -> `body`

    当您同时提供多个参数检查时，如果其中包含有同名的参数，优先级越靠后的参数
    检查将会覆盖优先级越靠前的参数。

!!! example annotate "冲突参数"

    form 和 body 参数检查只能有一个，如果同时提供了两个，会抛出异常。

