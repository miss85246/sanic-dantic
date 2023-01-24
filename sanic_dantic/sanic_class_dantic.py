# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: sanic_class_dantic.py
Description:
Author: Connor Zhang
CreateTime:  2023-01-23
"""

from typing import Coroutine

from sanic.request import Request
from sanic.views import HTTPMethodView

from .basic_definition import DanticModelObj, validate


class DanticView(HTTPMethodView):
    """
    请求参数检查类视图基类，继承自 sanic.views.HTTPMethodView，有三种方式来定义参数检查：

    - 直接通过 `parse_params` 装饰器来为指定的请求方法添加参数检查。
    - 通过将检查参数放入到 `HTTPMethodView.decorators` 中来添加参数检查。
    - 通过定义对应的 `{method}_model` 方法来添加参数检查。[暂不支持 async 方法]

    parameter check class view base class, inherit from sanic.HTTPMethodView,
    there are three ways to define parameter check:

    - directly use `parse_params` decorator to add for specified request method.
    - add by putting check parameters into `HTTPMethodView.decorators`.
    - define `{method}_model` method to add. [not support async method]
    """

    DanticModel = DanticModelObj
    params = None

    def dispatch_request(self, request: Request, *args, **kwargs):
        """
        继承自 HTTPMethodView，重写了 dispatch_request 方法，添加了参数检查的逻辑。

        inherit from HTTPMethodView, rewrite dispatch_request method, add
        parameter check logic.
        """

        method = request.method.lower()
        handler = getattr(self, method, None)
        model_handler = getattr(self, f'{method}_model', None)

        if model_handler:
            model_obj = model_handler()
            parsed_args = validate(request, model_obj)
            if isinstance(parsed_args, Coroutine):
                return parsed_args
            request.ctx.params = parsed_args

            # remove path params from kwargs
            if model_obj.path:
                for key in model_obj.path.__fields__:
                    kwargs.pop(key)

            kwargs.update({"params": parsed_args})

        # set request.app.ctx to DanticView properties
        for key, val in request.app.ctx.__dict__.items():
            setattr(request.ctx, key, val)

        return handler(request, *args, **kwargs)
