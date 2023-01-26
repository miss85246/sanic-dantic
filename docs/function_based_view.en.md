---
hide:

- toc

---

# Function Based View Usage

sanic-dantic supports the `parse_params` decorator, which can be used to add
parameter checking to function views.

```python
from sanic import Sanic
from sanic.response import json
from sanic_dantic import parse_params, BaseModel, Field

app = Sanic(__name__)
app.config.FALLBACK_ERROR_FORMAT = "json"


class Person(BaseModel):
    name: str = Field(description="name")
    age: int = Field(description="age")


@app.route("/person")
@parse_params(query=Person)
async def person(request, params):
    return json({"ctx": request.ctx.params, "params": params})


if __name__ == "__main__":
    app.run(host="localhost", port=8000, dev=True)
```

## Parameter Check Order

The parameter check with the highest priority is the one that comes first. If
the parameter check fails, the parameter check that comes later will not be
performed.

!!! note annotate "About the check order"

    sanic-dantic will check the parameters in the following order:

    `header` -> `path` -> `query` -> `form` -> `body`
 
    When you provide multiple parameter checks at the same time, if there are
    parameters with the same name, the parameter check with the higher priority
    will override the parameter check with the lower priority.

!!! example annotate "Conflict parameters"
form and body parameter checks can only have one, if both are provided, an
exception will be thrown。

