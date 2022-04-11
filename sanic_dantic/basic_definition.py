# -*- coding: utf-8 -*-
from inspect import getmro

from pydantic import BaseModel, ValidationError
from sanic.exceptions import InvalidUsage, ServerError
from sanic.log import logger
from sanic.request import Request


class ParsedArgsObj(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.update({key: value})


class DanticModelObj:
    def __init__(self, header=None, path=None, query=None, form=None, body=None):
        """
        The param must be a BaseModel class or must inherit from BaseModel \n
        :param path: pydantic.BaseModel
        :param query: pydantic.BaseModel
        :param form: pydantic.BaseModel
        :param body: pydantic.BaseModel
        if listed, the same model name's model will use strict mode
        """
        try:
            assert not (body and form), "sanic-dantic: body and form cannot be used at the same time."
            self.items = {"header": header, "path": path, "query": query, "form": form, "body": body}
            for model in [header, path, query, form, body]:
                if model and BaseModel not in getmro(model):
                    raise AssertionError("sanic-dantic: model must inherited from Pydantic.BaseModel")
        except AssertionError as e:
            logger.error(e)
            raise ServerError(e)

    def __repr__(self):
        return str(self.items)


def validate(request: Request, header=None, path=None, query=None, form=None, body=None, error=None):
    """
    When there are the same parameter name in the model, the parameter in ParsedArgsObj will be overwritten,
    The priorities is: body = form > query > path > header \n
    :param request: Request Obj
    :param header: Pydantic model
    :param path: Pydantic model
    :param query: Pydantic model
    :param form: Pydantic model, cannot exist at the same time as body
    :param body: Pydantic model, cannot exist at the same time as form
    :param error: custom error handler function, validate will pass the ValidationError to the function
    :return parsed_args: ParsedArgsObj
    """
    try:
        parsed_args = ParsedArgsObj()
        if header:
            parsed_args.update(header(**request.headers).dict())

        if path:
            parsed_args.update(path(**request.match_info).dict())

        if query:
            params = {key: val[0] if len(val) == 1 else val for key, val in request.args.items()}
            parsed_args.update(query(**params).dict())

        if form:
            form_data = {key: val[0] if len(val) == 1 else val for key, val in request.form.items()}
            parsed_args.update(form(**form_data).dict())

        elif body:
            parsed_args.update(body(**request.json).dict())

    except ValidationError as e:
        # Priority: error handler function of sanic_dantic  >  default InvalidUsage
        if error:
            raise error(request, e)
        else:
            error_messages = e.errors()[0]
            message = f'{error_messages.get("loc")[0]} {error_messages.get("msg")}'
            logger.error(message)
            raise InvalidUsage(message)
    except Exception as e:
        raise e

    return parsed_args
