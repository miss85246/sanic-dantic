# -*- coding: utf-8 -*-
from functools import wraps
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage
from pydantic import ValidationError
from sanic.log import logger


class ParsedArgsObj(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.update({key: value})


class InvalidOperation(BaseException):
    pass


def validate(request, query, body, path):
    parsed_args = ParsedArgsObj()
    if body and request.method not in ["POST", "PUT", "PATCH"]:
        raise InvalidOperation(
            f"Http method '{request.method}' does not contain a payload,"
            "yet a `Pyndatic` model for body was supplied"
        )

    if path:
        parsed_args.update(path(**request.match_info).dict())

    if query:
        params = request.args
        params = {k: v[0] for k, v in params.items()}
        parsed_args.update(query(**params).dict())

    if body:
        parsed_args.update(body(**request.json).dict())

    return parsed_args


def parse_params(query=None, body=None, path=None):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                _request = args[0] if isinstance(request, HTTPMethodView) else request
                result = validate(_request, query, body, path)
            except ValidationError as e:
                error_messages = e.errors()[0]
                message = f'{error_messages.get("loc")[0]} {error_messages.get("msg")}'
                raise InvalidUsage(message)
            except InvalidOperation as e:
                logger.error(e)
                raise e
            kwargs.update({'params': result})
            _request.ctx.params = result
            _request["params"] = result
            response = await f(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator
