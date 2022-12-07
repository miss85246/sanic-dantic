#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: fbv_server.py
Description:
Author: Connor Zhang
Email: chzhangyue@qq.com
CreateTime: 2022-05-08
"""
from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.response import json

from dantic_model import Person
from sanic_dantic import parse_params

app = Sanic("test_server")


class CustomException(SanicException):
    message = "This is Custom Exception"
    status_code = 500


@app.route('/fbv_query_test', methods=['GET'])
@parse_params(query=Person)
async def fbv_query_test(request, params):
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


@app.route('/fbv_form_test', methods=['POST'])
@parse_params(form=Person)
async def fbv_form_test(request, params):
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


@app.route('/fbv_header_test', methods=['GET'])
@parse_params(header=Person)
async def fbv_header_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })


@app.route('/fbv_error_test', methods=['GET'])
@parse_params(query=Person, error=CustomException)
async def fbv_error_test(request, params):
    return json({
        "ctx.params": request.ctx.params,
        "params": params
    })
