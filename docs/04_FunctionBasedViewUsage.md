# Function-Based View Usage

## Specify `pydantic` model

In the function-based view, you can specify the `pydantic` model for parameter checking, and you can submit the model to
the four parameters `path`, `query`, `form`, and `body`:

`path`, `query`, `form`, `body` are four different inspection modes

- `path:` If you appoint it, sanic-dantic will help check path params. It applies to `GET`
- `query:` If you appoint it, sanic-dantic will help check url params. It applies to `GET`
- `form:` If you appoint it, sanic-dantic will help check data params. It applies to `GET`, `PUT`, `POST`
- `body:` If you appoint it, sanic-dantic will help check body params. It applies to `POST`, `PUT`, `PATCH`
- **Notice**: the applies is just suggest, It's not mean can't use with other method, you can try it

```python
from sanic import Sanic
from sanic_dantic import BaseModel, parse_params
from sanic.response import json

app = Sanic("example")


class Person(BaseModel):
    name: str
    age: int


@app.route('/get_example', methods=['GET'])
@parse_params(query=Person)
async def example(request, params):
    print({"name": request.ctx.params.name, "age": request.ctx.params.age})
    return json({"name": params.name, "age": params.age})


@app.route('/post_example', methods=['POST'])
@parse_params(body=Person)
async def example(request, params):
    print({"name": request.ctx.params.name, "age": request.ctx.params.age})
    return json({"name": params.name, "age": params.age})


@app.route('/put_example', methods=['PUT'])
@parse_params(form=Person)
async def example(request, params):
    print({"name": request.ctx.params.name, "age": request.ctx.params.age})
    return json({"name": params.name, "age": params.age})


@app.route('/patch_example/<id>', methods=['PATCH'])
@parse_params(path=Person)
async def patch_example(request, params):
    print({"name": request.ctx.params.name, "age": request.ctx.params.age})
    return json({"name": params.name, "age": params.age})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```

## Specify multiple `pydantic` models at the same time

Sometimes, we may need more than one parameter check. There may be multiple combinations of `query` and `body`
.

`sanic-dantic` supports multiple parameter checks at the same time, like this:

```python
from sanic import Sanic
from sanic_dantic import BaseModel, parse_params
from sanic.response import json

app = Sanic("example")


class Person(BaseModel):
    name: str
    age: int


class Car(BaseModel):
    speed: int


@app.route('/example', methods=['POST'])
@parse_params(query=Person, body=Car)
async def example(request, params):
    print({
        "name": request.ctx.params.name,
        "age": request.ctx.params.age,
        "speed": request.ctx.params.speed
    })
    return json({"name": params.name, "age": params.age, "speed": params.speed})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
```
