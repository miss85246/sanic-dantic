# sanic-dantic

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fmiss85246%2Fsanic-dantic%2Fbadge%3Fref%3Dmain&style=flat)](https://actions-badge.atrox.dev/miss85246/sanic-dantic/goto?ref=main)
[![Downloads](https://static.pepy.tech/personalized-badge/sanic-dantic?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/sanic-dantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![PyPI](https://img.shields.io/pypi/v/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![PyPI - License](https://img.shields.io/pypi/l/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![Docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://miss85246.github.io/sanic-dantic/)

当前为 sanic-dantic 的英文简介，如果您想阅读中文版本，请点击[这里](README_zh.md)。

## Introduction

sanic-dantic is a request parameter check and parsing library based on the sanic
framework. It is based on pydantic and can help developers quickly check and
get request parameters.

## Why sanic-dantic

In many cases, we need to check and parse request parameters, but the sanic
framework itself does not provide it, so we need to implement it ourselves.
In most cases, you may need to do this:

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

This code looks simple, but when your parameters become more and more, you will
find that you need to write a lot. This is a bad implementation because it is
not maintainable. So we need a better way to implement it.

sanic-dantic can help you quickly implement parameter checking and parsing.

## Installation

You can install sanic-dantic through pip:

```bash
pip install sanic-dantic
```

You can also install it through the source code:

```bash
pip install git+https://github.com/miss85246/sanic-dantic.git
```

### Requirements

sanic-dantic depends on sanic and pydantic, their specific versions are:

```bash
sanic >= 20.3.0
pydantic >= 1.7.3
```

## Simple Usage

First, define the parameter check model through pydantic,
then define the view function, and check and parse the parameters through the
`parse_params` decorator.

```python
from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel, Field


# define params check model by pydantic.
class Person(BaseModel):
    name: str = Field(description="name of person")
    age: int = Field(default=18, description="age of person")


app = Sanic("SanicDanticExample")


# view function and check and parse params by `parse_params` decorator.
@app.route('/example')
@parse_params(path=Person)
async def path_param_examples(request, params):
    # request.ctx and params are parsed parameters
    print("ctx:", request.ctx.params)
    print("params:", params)
    print("name:", params.name)
    print("age:", params.age)

    return json({"ctx": request.ctx.params, "params": params})


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
```

now you can test with curl:

```bash
curl -X GET "http://localhost:8000/example?name=Connor&age=18"
```

the response is:

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

and the console output is:

```bash
ctx: {'name': 'Connor', 'age': 18}
params: {'name': 'Connor', 'age': 18}
name: Connor
age: 18
```

more pydantic usage can see
[pydantic documentation](https://pydantic-docs.helpmanual.io/usage/models/)。

more sanic-dantic advanced usage can see
[sanic-dantic documentation]()。

## License

sanic-dantic is licensed under the GPL-3.0 License. If you want to use
sanic-dantic for secondary development or commercial use, please follow the
GPL-3.0 License.

