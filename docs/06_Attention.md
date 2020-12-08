# Attention

Although sanic-dantic can help you improve the inspection efficiency, it is not omnipotent.

## Don't use form with body

Both `form` and `json` use request.json to pass parameters, but their formats are completely different

```shell
form: name=test&age=12
json: {"name":"test", "age":12}
```

If you use form with body, It's will raise InvalidOperation:

```python
from sanic import Sanic

from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


@app.route('/body_and_form_test', methods=['POST'])
@parse_params(body=Person, form=Person)
async def body_and_form_test(request, params):
    pass


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```

## The same param name will be overwritten

sanic-dantic's type checking has a sequence, and if you use the same parameter name, some parameters will be overwritten

Their priorities are: `form` = `body` > `query` > `path`

```python
from sanic import Sanic
from sanic.response import json
from sanic_dantic import parse_params, BaseModel


class Person(BaseModel):
    name: str
    age: int


app = Sanic("SanicDanticExample")


@app.route('/overwritten_test', methods=['POST'])
@parse_params(body=Person, query=Person)
async def overwritten_test(request, params):
    return json({"params": params, "request.ctx.params": request.ctx.params})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```