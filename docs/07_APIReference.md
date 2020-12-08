## sanic-dantic.basic_definition

### `class ParsedArgsObj(seq=None, **kwargs)`

**Based**: `dict`

This class is used to store the parsed request parameters

#### `def __getattr__(self, item)`

**parameter:**

- item - the name of the parameter to be obtained

**Return:** getattr(self, name)

#### `def__setattr__(self, key, value)`

**parameter:**

- key - the name of the attribute to be set -value-the value of the attribute to be set

**Return:** None

### `class InvalidOperation(BaseException)`

**Based**: `BaseException`

This error will be triggered when `sanic-dantic` is passed an abnormal parameter

### `class DanticModelObj(path=None, query=None, form=None, body=None):`

**Based:** `object`

This class is used to type check the incoming `pydantic` model

**parameter:**

- path - pydantic model, check with parameters
- query - pydantic model, check with parameters
- form - pydantic model, check with parameters
- body - pydantic model, check with parameters

**Attributes:**

- items - model parameters after checking will be assigned to items attribute

### `def validate(request, path=None, query=None, form=None, body=None) `

This function is used for the actual check of `request` parameters, here will be a parameter check for each model

**parameter:**

- request
- path - pydantic model, check with parameters
- query - pydantic model, check with parameters
- form - pydantic model, check with parameters
- body - pydantic model, check with parameters

**Return:** parsed_args-all parsed parameters will be placed under `parsed_args`

## sanic-dantic.sanic_class_dantic

### `class DanticView`

**Based:** `HTTPMethodViwe`

### `def dispatch_request(request, *args, **kwargs)`

## sanic-dantic.sanic_function_dantic

### `def parse_params(methods: [str] = None, path=None, query=None, form=None, body=None)`

**parameter:**

- methods - request method, multiple request parameters can exist at the same time - path - pydantic model, check with
  parameters
- query - pydantic model, check with parameters
- form - pydantic model, check with parameters
- body - pydantic model, check with parameters