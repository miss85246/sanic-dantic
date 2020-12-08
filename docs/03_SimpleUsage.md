# Simple Usage

`sanic-dantic` is very simple and easy to use.

You can check the parameters by specifying the model of `pydantic`. After the check passes, the parameters will be
placed in the `params` parameter and the `request.ctx.params` parameter.

You can get your request parameters directly through attributes:

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
    print({"name": request.ctx.params.name, "age": request.ctx.params.age})
    return json({"name": params.name, "age": params.age})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```

This is just a simple usage of `sanic-dantic`, please
see [FunctionBasedViewUsage](https://miss85246.github.io/sanic-dantic/FunctionBasedViewUsage/)
and [ClassBasedViewUsage](https://miss85246.github.io/sanic-dantic/ClassBasedViewUsage/) for specific detailed usage. 
