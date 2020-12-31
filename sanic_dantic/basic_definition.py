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
    def __init__(self, header=None, path=None, query=None, form=None, body=None):
        """
        The param must be a BaseModel class or must inherit from BaseModel \n
        :param path: pydantic.BaseModel
        :param query: pydantic.BaseModel
        :param form: pydantic.BaseModel
        :param body: pydantic.BaseModel
        if list, the same model name's model will use strict mode
        """
        try:
            assert not (body and form), "sanic-dantic: body model cannot exist at the same time as form model"
            self.items = {"header": header, "path": path, "query": query, "form": form, "body": body}
            basemodel_check = [BaseModel in [_ for _ in getmro(model)] for model in self.items.values() if model]
            assert False not in basemodel_check, "sanic-dantic: model must inherited from Pydantic.BaseModel"
        except AssertionError as e:
            logger.error(e)
            raise ServerError(e)

    def __repr__(self):
        return str(self.items)


def validate(request, header=None, path=None, query=None, form=None, body=None):
    """
    When there are the same parameter name in the model, the parameter in ParsedArgsObj will be overwritten,
    The priorities is: body = form > query > path \n
    :param header: Pydantic model
    :param request: Pydantic model
    :param query: Pydantic model
    :param body: Pydantic model, cannot exist at the same time as form
    :param path: Pydantic model
    :param form: Pydantic model, cannot exist at the same time as body
    :return parsed_args: ParsedArgsObj
    """
    try:
        error_message = "sanic-dantic: body model must be used together with one of ['POST','PUT','PATCH','DELETE']"
        assert request.method in ["POST", "PUT", "PATCH", "DELETE"] if body else True, error_message
        models, parsed_args = [header, path, query] + [form or body], ParsedArgsObj()
        body_storage = {k: v[0] if len(v) == 1 else v for k, v in request.form.items()} if form else request.json
        params = {k: v[0] if len(v) == 1 else v for k, v in request.args.items()}
        storages = [request.headers, request.match_info, params, body_storage]
        models = [item for item in zip(models, storages) if item[0]]
        [parsed_args.update(model(**storage).dict()) for model, storage in models]
    except ValidationError as e:
        error_messages = e.errors()[0]
        message = f'{error_messages.get("loc")[0]} {error_messages.get("msg")}'
        logger.error(message)
        raise InvalidUsage(message)
    except AssertionError as e:
        logger.error(e)
        raise ServerError(e)
    
    return parsed_args
