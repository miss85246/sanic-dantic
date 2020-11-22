from sanic import Sanic
from sanic.response import json

from sanic_dantic import parse_params, BaseModel

app = Sanic("SanicDanticExample")


class Person(BaseModel):
    name: str
    age: int


class Car(BaseModel):
    name: str
    speed: int


@app.route('/test', methods=['POST'])
@parse_params(form=Car, body=Person)
async def post_test(request, params):
    print(params)
    return json(params)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
