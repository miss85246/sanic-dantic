---
hide:

- toc

---

# QuickStart

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