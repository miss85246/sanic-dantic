# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: sanic_function_dantic.py
Description:
Author: Connor Zhang
CreateTime:  2023-01-23
"""

from functools import wraps
from typing import Callable, Coroutine
from typing import Type

from sanic.request import Request

from .basic_definition import BaseModel, DanticModelObj, validate


def parse_params(
        methods: [str] = None,
        header: Type[BaseModel] = None,
        path: Type[BaseModel] = None,
        query: Type[BaseModel] = None,
        form: Type[BaseModel] = None,
        body: Type[BaseModel] = None,
        error: Type[Callable] = None
):
    """
    parameter check decorator, can be used for function view and class view.
    if methods is None, it will check all request methods.

    参数检查装饰器，除了可以用于函数式视图，也可以用于类式视图。
    可以不指定 methods 参数，这样就会对所有请求方法都进行参数检查。

    :param methods: request methods
    :param header: pydantic model for header
    :param query: pydantic model for query
    :param path: pydantic model for path
    :param body: pydantic model for body
    :param form: pydantic model for form
    :param error: error handler function
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            _request = [
                item for item in (request,) + args
                if isinstance(item, Request)
            ][0]

            hit = None
            if methods:
                hit = _request.method.lower() in [_.lower() for _ in methods]
            if not methods or hit:
                model_obj = DanticModelObj(
                    header=header,
                    path=path,
                    query=query,
                    form=form,
                    body=body,
                    error=error
                )
                parsed_args = validate(_request, model_obj)
                if isinstance(parsed_args, Coroutine):
                    return await parsed_args
                if path:
                    for key in path.__fields__:
                        kwargs.pop(key)
                kwargs.update({"params": parsed_args})
                # set request.app.ctx to DanticView properties
            for key, val in request.app.ctx.__dict__.items():
                setattr(request.ctx, key, val)
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator
