# -*- coding: utf-8 -*-
from inspect import getmro
from typing import Type

from pydantic import BaseModel, ValidationError
from sanic.exceptions import InvalidUsage, ServerError, SanicException
from sanic.log import error_logger
from sanic.request import Request


class ParsedArgsObj(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.update({key: value})


class DanticModelObj:
    def __init__(
            self,
            header: Type[BaseModel] = None,
            query: Type[BaseModel] = None,
            path: Type[BaseModel] = None,
            body: Type[BaseModel] = None,
            form: Type[BaseModel] = None,
            error: Type[SanicException] = None,
    ) -> None:
        """
        The param must be a BaseModel class or must inherit from BaseModel \n
        if listed, the same model name's model will use strict mode
        """

        try:
            if body and form:
                raise AssertionError(
                    "sanic-dantic: " +
                    "body and form cannot be used at the same time."
                )

            self.items = {
                "header": header,
                "path": path,
                "query": query,
                "form": form,
                "body": body,
                "error": error
            }

            for model in [header, path, query, form, body]:
                if model and BaseModel not in getmro(model):
                    raise AssertionError(
                        "sanic-dantic: " +
                        "model must inherited from Pydantic.BaseModel"
                    )

            if error and SanicException not in getmro(error):
                raise AssertionError(
                    "sanic-dantic: " +
                    "error must inherited from SanicException"
                )

        except AssertionError as e:
            error_logger.error(e)
            raise ServerError(str(e))

    def __repr__(self):
        return str(self.items)


def validate(
        request: Request,
        header: Type[BaseModel] = None,
        query: Type[BaseModel] = None,
        path: Type[BaseModel] = None,
        body: Type[BaseModel] = None,
        form: Type[BaseModel] = None,
        error: Type[SanicException] = None
) -> ParsedArgsObj:
    """
    When there are the same parameter name in the model,
    the parameter in ParsedArgsObj will be overwritten,
    The priorities is: body = form > query > path > header
    """

    try:
        parsed_args = ParsedArgsObj()
        if header:
            parsed_args.update(header(**request.headers).dict())

        if path:
            parsed_args.update(path(**request.match_info).dict())

        if query:
            params = {
                key: val[0]
                if len(val) == 1 else val for key, val in request.args.items()
            }
            parsed_args.update(query(**params).dict())

        if form:
            form_data = {
                key: val[0]
                if len(val) == 1 else val
                for key, val in request.form.items()
            }
            parsed_args.update(form(**form_data).dict())

        elif body:
            parsed_args.update(body(**request.json).dict())

    except ValidationError as e:
        # error handler function of sanic_dantic  >  default InvalidUsage
        if error:
            error_msg = e.errors()[0]
            message = f'{error_msg.get("loc")[0]} {error_msg.get("msg")}'
            raise error(message)
        else:
            error_msg = e.errors()[0]
            message = f'{error_msg.get("loc")[0]} {error_msg.get("msg")}'
            error_logger.error(message)
            raise InvalidUsage(message)
    except Exception as e:
        raise e
    request.ctx.params = parsed_args
    return parsed_args
