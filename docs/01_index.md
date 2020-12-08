# sanic-dantic

![Travis (.com)](https://img.shields.io/travis/com/miss85246/sanic-dantic?logo=travis)
![Codecov](https://img.shields.io/codecov/c/github/miss85246/sanic-dantic?color=33CC33&logo=codecov)
[![Downloads](https://static.pepy.tech/personalized-badge/sanic-dantic?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/sanic-dantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![PyPI](https://img.shields.io/pypi/v/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![PyPI - License](https://img.shields.io/pypi/l/sanic-dantic)](https://pypi.org/project/sanic-dantic/)
[![Docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://miss85246.github.io/sanic-dantic/)
> Laziness is the source of progress.

`sanic-dantic` is a sanic request parameter check plugin based on pydantic. It supports you to use all the features
of `pydantic` to help you quickly check request parameters.

The purpose of this project is to help you quickly analyze and check parameters.

The project is published on [Github](https://github.com/miss85246/sanic-dantic) and is completely open source. Welcome
to communicate with the author and participate in the development.

## Installation

```shell
pip install sanic-dantic
```

## Why use it

I wonder whether you always need to take out request parameters from `request` when writing a program, and then check
the validity of the parameters? Like:

```python
from sanic import Sanic
from sanic.exceptions import InvalidUsage
from sanic.response import json

app = Sanic("Example")


@app.route('/example', methods=['GET'])
async def example(request):
    name = request.args.get("name")
    age = request.args.get("age")
    if not isinstance(name, str):
        raise InvalidUsage("name must be str")
    if not isinstance(age, int):
        raise InvalidUsage("age must be int")
    return json({"name": name, "age": age})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```

This is too bad, there is no development experience at all, this can be tolerated? So you should use `sanic-dantic`, it
can help you quickly check the legality of parameters, and help you parse them

## How to use

You just need to import `BaseModel` and `parse_params` to use it easily, like this:

```python
from sanic import Sanic
from sanic_dantic import BaseModel, parse_params
from sanic.response import json

app = Sanic("example")


class Person(BaseModel):
    name: str
    age: int


@app.route('/example', methods=['GET'])
@parse_params(query=Person)
async def example(request, params):
    return json({"name": params.name, "age": params.age})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```

Does it feel much more convenient? What are you waiting for, come use it!

more usage please read [Usage](https://miss85246.github.io/sanic-dantic/SimpleUsage/)