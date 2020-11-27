# Simple Usage

You can get parameters quickly through `sanic-dantic`.

You just need give it a Pydantic Model and It's will auto help you check parameters and serialization.

Passed checked parameters will simultaneously transmitted to `request.ctx.params` and `params`.
```python
import unittest
from sanic import Sanic
from sanic.response import json
from sanic_dantic import parse_params, BaseModel

class Person(BaseModel):
    name:str
    age:int

app = Sanic("SanicDanticTest")

@app.route('/query_test', methods=['GET'])
@parse_params(query=Person)
async def query_test(request, params):
     # {"params":{"name":"test", "age": 100}, "ctx.params":{"name":"test", "age": 100}}
    return json({"params":params, "ctx.params":request.ctx.params})

class SimpleTest(unittest.TestCase):
    def test_simple_usage(self):
        data = {"name":"test", "age": 100}
        req, res = app.test_client.get("/query_test", params=data)
        self.assertEqual(res.json, {"params":data, "ctx.params":data})
    
if __name__ == '__main__':
    unittest.main()

```