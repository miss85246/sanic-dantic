---
hide:

- toc

---

# 快速开始

sanic-dantic 先通过 pydantic 的方式定义参数检查模型，
然后再定义视图函数，并通过 `parse_params` 装饰器来进行参数检查和解析。

```python
from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel, Field


# 先通过 pydantic 的方式定义参数检查模型。
class Person(BaseModel):
    name: str = Field(description="name of person")
    age: int = Field(default=18, description="age of person")


app = Sanic("SanicDanticExample")


# 定义视图函数，并通过 `parse_params` 装饰器来进行参数检查和解析。
@app.route('/example')
@parse_params(path=Person)
async def path_param_examples(request, params):
    # request.ctx 和 params 都是解析后的参数

    print("ctx:", request.ctx.params)
    print("params:", params)
    print("name:", params.name)
    print("age:", params.age)

    return json({"ctx": request.ctx.params, "params": params})


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
```

现在，您可以通过 curl 进行测试：

```bash
curl -X GET "http://localhost:8000/example?name=Connor&age=18"
```

响应结果如下：

```json
{
  "ctx": {
    "name": "Connor",
    "age": 18
  },
  "params": {
    "name": "Connor",
    "age": 18
  }
}
```

控制台输出如下：

```bash
ctx: {'name': 'Connor', 'age': 18}
params: {'name': 'Connor', 'age': 18}
name: Connor
age: 18
```