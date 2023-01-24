# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: app.py
Description:
Author: Connor Zhang
CreateTime:  2023-01-23
"""

from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView

from model import Person
from sanic_dantic import DanticView
from sanic_dantic import parse_params

app = Sanic(__name__)
app.config.FALLBACK_ERROR_FORMAT = "json"


# ------------------------ define exception handler-----------------------------

async def custom_exception_handler(request, message):
    return json(
        {
            "message": message,
            "status_code": 400,
            "request_id": str(request.id)
        },
        status=400
    )


# -------------------------- define function view ------------------------------

@app.route('/fbv_header_test', methods=['GET'])
@parse_params(header=Person)
async def fbv_header_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })


@app.route('/fbv_query_test', methods=['GET'])
@parse_params(query=Person)
async def fbv_query_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })


@app.route('/fbv_path_test/<name:str>/<age:int>', methods=['GET'])
@parse_params(path=Person)
async def fbv_path_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })


@app.route('/fbv_form_test', methods=['POST'])
@parse_params(form=Person)
async def fbv_form_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })


@app.route('/fbv_body_test', methods=['POST'])
@parse_params(body=Person)
async def fbv_body_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })


@app.route('/fbv_error_test', methods=['PUT'])
@parse_params(body=Person, error=custom_exception_handler)
async def fbv_error_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })


@app.route('/fbv_del_test', methods=['DELETE'])
@parse_params(query=Person)
async def fbv_delete_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })


# ---------------------------- define class view -------------------------------

class NormalView(HTTPMethodView):
    decorators = [
        parse_params(query=Person, error=custom_exception_handler)
    ]

    @staticmethod
    async def get(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })

    @staticmethod
    async def post(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })


class AppointView(HTTPMethodView):
    decorators = [
        parse_params(
            query=Person,
            error=custom_exception_handler,
            methods=['get']
        )
    ]

    @staticmethod
    async def get(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })

    @staticmethod
    async def post(request, *args, **kwargs):
        return json({"args": args, "kwargs": kwargs})


class SanicDanticView(DanticView):
    decorators = [
        parse_params(query=Person, error=custom_exception_handler)
    ]

    @staticmethod
    async def get(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })

    @staticmethod
    async def post(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })


class DanticAppointView(DanticView):
    decorators = [
        parse_params(
            query=Person,
            error=custom_exception_handler,
            methods=['get']
        )
    ]

    @staticmethod
    async def get(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })

    @staticmethod
    async def post(request, *args, **kwargs):
        return json({"args": args, "kwargs": kwargs})


class DanticDefModelView(DanticView):
    @staticmethod
    async def get(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })

    @staticmethod
    async def post(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })

    def get_model(self):
        return self.DanticModel(query=Person, error=custom_exception_handler)

    def post_model(self):
        return self.DanticModel(body=Person)


class DanticPathView(DanticView):

    @staticmethod
    @parse_params(path=Person)
    async def get(request, params):
        return json({
            "ctx.params": request.ctx.params,
            "params": params
        })


# ============================= register route =================================

app.add_route(NormalView.as_view(), '/normal_test')
app.add_route(AppointView.as_view(), '/appoint_test')
app.add_route(SanicDanticView.as_view(), '/dantic_test')
app.add_route(DanticAppointView.as_view(), '/dantic_appoint_test')
app.add_route(DanticDefModelView.as_view(), '/dantic_def_model_test')
app.add_route(
    DanticPathView.as_view(),
    '/dantic_path_test/<name:str>/<age:int>'
)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
