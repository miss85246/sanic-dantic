---
hide:

- toc

---

# API Reference

## **class sanic_dantic.DanticModelObject**

### Description

`DanticModelObject` is used to unify `pydantic` models for easy parameter
checking during `validate`.

### Usage

#### `__init__(self, *args, **kwargs)`

- `headers` (Optional[pydantic.BaseModel]) – Model for checking request headers
- `path` (Optional[pydantic.BaseModel]) – Model for checking path parameters
- `query` (Optional[pydantic.BaseModel]) – Model for checking query parameters
- `body` (Optional[pydantic.BaseModel]) – Model for checking request body
- `form` (Optional[pydantic.BaseModel]) – Model for checking form data
- `error` (Optional[Callable]) – Custom error handling function

## **class sanic_dantic.ParsedArgsObj**

### Description

Inherited from `dict`, used to store parsed parameters. Supports access
through `.` and supports deepcopy.

### Usage

#### `__init__(self, *args, **kwargs)`

#### `__getattr__(self, name)`

#### `__setattr__(self, name, value)`

## **def validate(request: Request, dmo: DanticModelObj) -> Any**

### Description

Check the request parameters and return the parsed parameters.

### Usage

#### `validate(request: Request, dmo: DanticModelObj) -> Any`

- `request` (Request) – Request object
- `dmo` (DanticModelObj) – Parameter check model

## **class DanticView**

### Description

Inherited from `sanic.views.HTTPMethodView`, the `dispatch_request` method is
overwritten to support parameter checking.

### Usage

#### `dispatch_request(self, request, *args, **kwargs)`

- `request` (Request) – Request object
- `*args` – arguments
- `**kwargs` – keyword arguments

## **def parse_params(*args, \*\*kwargs)**

### Description

Decorator for `DanticView`, used to check request parameters.

### Usage

#### `parse_params(*args, \*\*kwargs)`

- `methods` (List[str]) – Request method list, default is `None`, which means
  all methods
- `headers` (Optional[pydantic.BaseModel]) – Model for checking request headers
- `path` (Optional[pydantic.BaseModel]) – Model for checking path parameters
- `query` (Optional[pydantic.BaseModel]) – Model for checking query parameters
- `body` (Optional[pydantic.BaseModel]) – Model for checking request body
- `form` (Optional[pydantic.BaseModel]) – Model for checking form data
- `error` (Optional[Callable]) – Custom error handling function



