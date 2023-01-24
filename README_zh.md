# sanic-dantic

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fmiss85246%2Fsanic-dantic%2Fbadge%3Fref%3Dmain&style=flat)](https://actions-badge.atrox.dev/miss85246/sanic-dantic/goto?ref=main)
[![Downloads](https://static.pepy.tech/personalized-badge/sanic-dantic?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/sanic-dantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![PyPI](https://img.shields.io/pypi/v/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![PyPI - License](https://img.shields.io/pypi/l/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![Docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://miss85246.github.io/sanic-dantic/)

This is the Chinese version of the README.md file. If you want to read the
English version, please click [here](README.md).

## 简介

sanic-dantic 是一个基于 sanic 框架下的请求参数检查和解析库。它基于
pydantic，可以帮助开发者快速检查和获取请求参数。

## 为什么要使用它？

在很多时候，我们需要对请求参数进行检查和解析，而 sanic 框架本身并没有提供，
所以我们需要自己实现。大部分情况下，您可能需要这样实现：

```python
from sanic import Sanic
from sanic.response import json

app = Sanic("SanicDanticExample")


@app.route('/example')
async def path_param_examples(request):
    name = request.get("name")
    age = request.get("age")
    if not isinstance(name, str) or not isinstance(age, int):
        return json({"error": "parameter type error"})
    return json({"message": f"hello {name} are you {age} years old ?"})
```

这样的代码看起来很简单，但是当您的参数变多的时候，您就会发现，您需要写很多。
这是一种糟糕的实现方式，因为它不是可维护的。所以我们需要一个更好的方式来实现。

sanic-dantic 可以帮助您快速的实现参数检查和解析。

## 安装

可以通过 pip 来进行安装：

```bash
pip install sanic-dantic
```

也可以通过源码进行安装：

```bash
pip install git+https://github.com/miss85246/sanic-dantic.git
```

### 依赖

sanic-dantic 依赖于 sanic 和 pydantic, 他们的具体版本为：

```bash
sanic >= 20.3.0
pydantic >= 1.7.3
```

## 简单示例

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

更多 pydantic 的使用方法可以参考
[pydantic 官方文档](https://pydantic-docs.helpmanual.io/usage/models/)。

更过 sanic-dantic 的使用方法可以参考
[sanic-dantic 文档](https://sanic-dantic.readthedocs.io/en/latest/)。

## 开源协议

sanic-dantic 使用 GPL-3.0 协议开源。如果您想使用 sanic-dantic 进行二次开发，或者商业使用，请您遵守
GPL-3.0 协议。