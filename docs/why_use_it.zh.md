---
hide:

- toc

---

# 为什么要使用它？

在很多时候，我们需要对请求参数进行检查和解析，而 sanic 框架本身并没有提供，
所以我们需要自己实现。大部分情况下，您可能需要这样实现：

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

这样的代码看起来很简单，但是当您的参数变多的时候，您就会发现，您需要写很多。
这是一种糟糕的实现方式，因为它不是可维护的。所以我们需要一个更好的方式来实现。

sanic-dantic 可以帮助您快速的实现参数检查和解析。