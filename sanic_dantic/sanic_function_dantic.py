# -*- coding: utf-8 -*-
from functools import wraps
from typing import Type

from sanic.exceptions import SanicException
from sanic.request import Request

from .basic_definition import DanticModelObj, validate, BaseModel


def parse_params(methods: [str] = None, header: Type[BaseModel] = None, path: Type[BaseModel] = None,
                 query: Type[BaseModel] = None, form: Type[BaseModel] = None,
                 body: Type[BaseModel] = None, error: Type[SanicException] = None
                 ):
    """
    Sanic Dantic Function View type check decorator, you can use it for any view.

    It can be used in function-based view:

    - you can use it directly without **methods** param

    It's also can be used in Class-based view:

    - **methods** parameter is not required. it will be applicable to all view checks if you don't give
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            _request = [item for item in (request,) + args if isinstance(item, Request)][0]
            if (methods and _request.method.upper() in [_.upper() for _ in methods]) or not methods:
                model_obj = DanticModelObj(header=header, path=path, query=query, form=form, body=body, error=error)
                validate(_request, **model_obj.items)
            response = await f(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator
