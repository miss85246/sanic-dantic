#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: cbv_server.py
Description:
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2022-05-08
"""

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.response import json
from sanic.views import HTTPMethodView

from dantic_model import Person
from sanic_dantic import DanticView, parse_params

app = Sanic("test_server")


class CustomException(SanicException):
    message = "This is Custom Exception"
    status_code = 500


class HttpPersonView(HTTPMethodView):
    decorators = [
        parse_params(query=Person, methods=["GET"]),
        parse_params(header=Person, methods=["PUT"])
    ]

    @staticmethod
    async def get(request, params):
        return json({
            "params1": request.ctx.params,
            "params2": params
        })

    @parse_params(body=Person)
    async def post(self, request, params):
        return json({
            "params1": request.ctx.params,
            "params2": params
        })

    @staticmethod
    async def put(request, params):
        return json({
            "params1": request.ctx.params,
            "params2": params
        })


class DanticPersonView(DanticView):

    async def post(self, request, params):
        return json({
            "params1": request.ctx.params,
            "params2": params,
            "params3": self.params
        })

    def post_model(self):
        return self.DanticModel(form=Person)

    async def get(self, request, params):
        return json({
            "params1": request.ctx.params,
            "params2": params,
            "params3": self.params
        })

    def get_model(self):
        return self.DanticModel(query=Person, error=CustomException)


class DanticPathPersonView(DanticView):
    async def get(self, request, name, age, params):
        return json({
            "params1": request.ctx.params,
            "params2": params,
            "params3": self.params
        })

    def get_model(self):
        return self.DanticModel(path=Person)


app.add_route(HttpPersonView.as_view(), "/person")
app.add_route(DanticPersonView.as_view(), "/dantic_person")
app.add_route(
    DanticPathPersonView.as_view(), "/dantic_path_person/<name>/<age>"
)
