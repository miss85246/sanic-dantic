# -*- coding: utf-8 -*-
from inspect import getmro

from pydantic import BaseModel, ValidationError
from sanic.exceptions import InvalidUsage, ServerError
from sanic.log import logger


class ParsedArgsObj(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.update({key: value})


class DanticModelObj:
    def __init__(self, path=None, query=None, form=None, body=None):
        """
        The param must be a BaseModel class or must inherit from BaseModel \n
        :param path: pydantic.BaseModel
        :param query: pydantic.BaseModel
        :param form: pydantic.BaseModel
        :param body: pydantic.BaseModel
        """
        items = {'path': path, 'query': query, 'form': form, 'body': body}
        try:
            if body and form:
                raise InvalidOperation("sanic-dantic: body model cannot exist at the same time as form model")
            for item, model in items.items():
                if model is not None and BaseModel not in [_ for _ in getmro(model)]:
                    raise InvalidOperation("param must type of pydantic.BaseModel")
                self.__setattr__(item, model)
            self.items = items
        except InvalidOperation as e:
            logger.error(e)
            raise ServerError(e)

    def __repr__(self):
        return str(self.items)


class InvalidOperation(BaseException):
    pass


def validate(request, path=None, query=None, form=None, body=None):
    """
    When there are the same parameter name in the model, the parameter in ParsedArgsObj will be overwritten,
    The priorities is: body = form > query > path \n
    :param request: Pydantic model
    :param query: Pydantic model
    :param body: Pydantic model, cannot exist at the same time as form
    :param path: Pydantic model
    :param form: Pydantic model, cannot exist at the same time as body
    :return parsed_args: ParsedArgsObj
    """
    parsed_args = ParsedArgsObj()
    try:
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
    except ValidationError as e:
        error_messages = e.errors()[0]
        message = f'{error_messages.get("loc")[0]} {error_messages.get("msg")}'
        logger.error(message)
        raise InvalidUsage(message)
    except InvalidOperation as e:
        logger.error(e)
        raise ServerError(e)

    return parsed_args
