# sanic-dantic

![Travis (.com)](https://img.shields.io/travis/com/miss85246/sanic-dantic?logo=travis)
![Codecov](https://img.shields.io/codecov/c/github/miss85246/sanic-dantic?color=33CC33&logo=codecov)
[![Downloads](https://static.pepy.tech/personalized-badge/sanic-dantic?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/sanic-dantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![PyPI](https://img.shields.io/pypi/v/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![PyPI - License](https://img.shields.io/pypi/l/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![Docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://miss85246.github.io/sanic-dantic/)
> sanic-dantic is a request parameter checking and parsing library based on
> pydantic under the sanic framework

sanic-dantic is a request parameter checking and parsing library based on
pydantic under the sanic framework

It is based on pydantic, which can facilitate developers to quickly check and
obtain request parameters

## Documentation

If you want more usage, please
click [here](https://miss85246.github.io/sanic-dantic/)

## Installation

```shell
pip install sanic-dantic
```

## Why use it

Do you have to get the request parameters first every time you process them ?

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

How terrible, and there is no good experience for developers at all.

Therefore, sanic-dantic is to help you improve your development efficiency and
experience.

It allows you to skip the process of type checking and parameter acquisition.

## How to use

It is based on pydantic, which can facilitate developers to quickly check and
obtain request parameters

In sanic-dantic, you can pass the pydantic model to different formal parameters
in parse_params to check and parse the values of different types of request
parameters

You can get all the parsed parameters by appending the formal parameter , and
get the value of the parameter through the attribute `params`

```python
from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


@app.route('/example')
@parse_params(path=Person)
async def path_param_examples(request, params):
    print(params.ctx.name, params.ctx.age)
    return json(
        {"message": f"hello {params.name} are you {params.age} years old ?"})
```

Do you have a crush? Come and experience it!

more usage please read
the [documentation](https://miss85246.github.io/sanic-dantic/)

