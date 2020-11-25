# sanic-dantic
![Travis (.com)](https://img.shields.io/travis/com/miss85246/sanic-dantic?logo=travis)
![Codecov](https://img.shields.io/codecov/c/github/miss85246/sanic-dantic?color=33CC33&logo=codecov)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-dantic)
![PyPI](https://img.shields.io/pypi/v/sanic-dantic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sanic-dantic)
![PyPI - License](https://img.shields.io/pypi/l/sanic-dantic)
> sanic-dantic is a request parameter checking and parsing library based on pydantic under the sanic framework

sanic-dantic is a request parameter checking and parsing library based on pydantic under the sanic framework

It is based on pydantic, which can facilitate developers to quickly check and obtain request parameters

## Installation
```shell
pip install sanic-dantic
```

## Usage
Before writing all the examples, let's write a file `server.py` first. In other examples, we will focus on the use of views and no longer write extraneous peripheral code.
```python
from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel, validator

app = Sanic("sanic-dantic-example")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```
Before using, we need to use pydantic to create a class for format checking of request parameters
```python
class Person(BaseModel):
    name: str
    age: int
```
### Use in function-based views
In the function view, you can pass the pydantic model to different formal parameters in parse_params to check and parse the values of different types of request parameters

You can get all the parsed parameters by appending the formal parameter `params`, and get the value of the parameter through the attribute

```python
@app.route('/path_example/<name>/<age>/')
@parse_params(path=Person)
async def path_param_examples(request, name, age, params):
    print(params.name, params.age)
    return json({"message": f"hello {params.name} are you {params.age} years old ?"})
```
If you do not want to pass additional parameters in the form of `params` way to get the parameters of the resolution, you can also get them by` request.ctx.params`

```python
@app.route('/get_example/')
@parse_params(query=Person)
async def path_param_examples(request, params):
    print(params.name, params.age)
    print(request.ctx.params.name, request.ctx.params.age)
    return json({"message": f"hello {params.name} are you {params.age} years old ?"})
```

```python
@app.route('/post_example/')
@parse_params(body=Person)
async def path_param_examples(request, params):
    print(params.name, params.age)
    print(request.ctx.params.name, request.ctx.params.age)
    return json({"message": f"hello {params.name} are you {params.age} years old ?"})
```
### Use in class-based views
Of course, `sanic-dantic` not only supports function-based views, it also supports class-based views
```python
class SanicDanticExampleView(HTTPMethodView):
    @parse_params(query=Person)
    def get(self, request):
        name, age = request.ctx.params.values()
        return json({"message": f"hello {name} are you {age} years old ?"})

    @parse_params(body=Person)
    def put(self, request):
        name, age = request.ctx.params.values()
        return json({"message": f"hello {name} are you {age} years old ?"})

    @parse_params(body=Person)
    def put(self, request):
        name, age = request.ctx.params.values()
        return json({"message": f"hello {name} are you {age} years old ?"})
```
### Notice
If you need, you can even add inspection classes for path, query, and body at the same time
```python
@app.route('/get_example/')
@parse_params(query=Person, body=Person)
async def path_param_examples(request, params):
    print(params.name, params.age)
    print(request.ctx.params.name, request.ctx.params.age)
    return json({"message": f"hello {params.name} are you {params.age} years old ?"})
```
However, if the parameter names in different types of parameters are consistent, the original parameters may be overwritten

```shell
> curl 'http://localhost:8000/get_example/?name=Connor&age=10' -x POST -d '{"name":"Calvin", "age":20}'
{"message": "hello Calvin are you 20 years old ?"}
```
The priority of different parameters is `body` > `query` > `path`
### Other
`sanic-dantic` integrates most of the usage of `pydantic`, other more usage methods can refer to [pydantic](https://github.com/samuelcolvin/pydantic)
## Thanks
Thanks to the author [Eric Jolibois](https://github.com/PrettyWood) of [pydantic](https://github.com/samuelcolvin/pydantic) and the author [Ahmed Nafies](https://github.com/ahmednafies) of [sanic-pydantic](https://github.com/ahmednafies/sanic-pydantic).
 
Because of their open source, I have the inspiration to write sanic-dantic. Thank them very much
## License
I'm pleased to support the open source community by making sanic-dantic available.
Copyright (C) 2020, Connor Zhang.  All rights reserved.
If you have downloaded a copy of the sanic-dantic source code from here, please note that sanic-dantic source code is licensed under the MIT License.  Your integration of sanic-dantic into your own projects may require compliance with the MIT License.
A copy of the MIT License is included in this [file](https://github.com/misss85246/sanic-dantic/blob/main/LICENSE).
