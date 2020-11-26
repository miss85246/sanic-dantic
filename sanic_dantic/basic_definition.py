# -*- coding: utf-8 -*-
from inspect import getmro

from pydantic import BaseModel


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
        for item, model in items.items():
            if model is not None and BaseModel not in [_ for _ in getmro(model)]:
                raise TypeError("param must type of pydantic.BaseModel")
            self.__setattr__(item, model)
        self.items = items

    def __repr__(self):
        return str(self.items)


class InvalidOperation(BaseException):
    pass


def validate(request, query=None, body=None, path=None, form=None):
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
