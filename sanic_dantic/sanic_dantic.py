# -*- coding: utf-8 -*-
from functools import wraps

from pydantic import ValidationError
from sanic.exceptions import InvalidUsage, ServerError
from sanic.log import logger
from sanic.views import HTTPMethodView


class ParsedArgsObj(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.update({key: value})


class InvalidOperation(BaseException):
    pass


def validate(request, query, body, path, form):
    """
    :param request: Pydantic model
    :param query: Pydantic model
    :param body: Pydantic model, cannot exist at the same time as form
    :param path: Pydantic model
    :param form: Pydantic model, cannot exist at the same time as body
    :return: parsed_args: ParsedArgsObj
    When there are the same parameter name in the model,
    the parameter in ParsedArgsObj will be overwritten,
    The priorities is: body = form > query > path
    """
    parsed_args = ParsedArgsObj()
    if body and form:
        raise InvalidOperation("sanic-dantic: body model cannot exist at the same time as form model")
    if body and request.method not in ["POST", "PUT", "PATCH"]:
        raise InvalidOperation("sanic-dantic: body model must be used together with one of ['POST','PUT','PATCH']")

    if path:
        parsed_args.update(path(**request.match_info).dict())

    if query:
        params = {k: v[0] for k, v in request.args.items()}
        parsed_args.update(query(**params).dict())

    if form:
        forms = {k: v[0] for k, v in request.form.items()}
        parsed_args.update(form(**forms).dict())

    if body:
        parsed_args.update(body(**request.json).dict())

    return parsed_args


def parse_params(query=None, body=None, path=None, form=None):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                _request = args[0] if isinstance(request, HTTPMethodView) else request
                result = validate(_request, query, body, path, form)
            except ValidationError as e:
                error_messages = e.errors()[0]
                message = f'{error_messages.get("loc")[0]} {error_messages.get("msg")}'
                raise InvalidUsage(message)
            except InvalidOperation as e:
                logger.error(e)
                raise ServerError(e)
            kwargs.update({'params': result})
            _request.ctx.params = result
            response = await f(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator
