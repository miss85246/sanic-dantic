# -*- coding: utf-8 -*-
# import asyncio

from sanic.request import Request
from sanic.views import HTTPMethodView

from .basic_definition import DanticModelObj, validate


class DanticView(HTTPMethodView):
    """
    Simple view inherited from HTTPMethodView
    You should implement methods
    (get, post, put, patch, delete)
    for the class And should implement models
    (get_model, post_model, put_model, patch_model, delete_model)
    for the class to implement every HTTP request and request parameter
    type check that you want to support.

    For example:

        class Person(BaseModel):
            name:str
            age:int

        class DummyView(HTTPMethodView):
            def get(self, request, *args, **kwargs):
                return text('I am get method')
            def put(self, request, *args, **kwargs):
                return text('I am put method')
            def get_model(self):
                return self.DanticModel(query=Person)
            def post_model(self)
                return self.DanticModel(body=Person)
    etc.

    If someone tries to use a non-implemented method, there will be a
    405 response.

    If someone tries to use method, and you didn't give it method model,
    It will just like a common method

    Any other use method is the same as HTTPMethodView
    """

    DanticModel = DanticModelObj
    params = None

    def dispatch_request(self, request: Request, *args, **kwargs):
        """
        The DanticView dispatch method, It's inherit from HTTPMethodView

        The request.app.ctx namespace will be set to DanticView properties

        before into the method, it will check method_model and validate
        the request.

        other usage is the same as HTTPMethodView
        """

        for key, value in request.app.ctx.__dict__.items():
            setattr(self, key, value)

        method = request.method.lower()
        handler = getattr(self, method, None)
        model_handler = getattr(self, f'{method}_model', None)
        if model_handler:
            model_obj = model_handler()
            parsed_args = validate(request, **model_obj.items)
            request.ctx.params = parsed_args
            self.params = parsed_args
        return handler(request, *args, **kwargs)
