---
hide:

- toc

---

# Why Use It

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