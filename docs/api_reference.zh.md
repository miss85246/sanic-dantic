---
hide:

- toc

---

# API 参考

## **class sanic_dantic.DanticModelObject**

### 说明

`DanticModelObject` 用于将 `pydantic` 模型进行统合，方便在 `validate` 时进行参数检查。

### 用法

#### `__init__(self, *args, **kwargs)`

- `headers` (Optional[pydantic.BaseModel]) – 用于检查请求头的模型
- `path` (Optional[pydantic.BaseModel]) – 用于检查路径参数的模型
- `query` (Optional[pydantic.BaseModel]) – 用于检查查询参数的模型
- `body` (Optional[pydantic.BaseModel]) – 用于检查请求体的模型
- `form` (Optional[pydantic.BaseModel]) – 用于检查表单数据的模型
- `error` (Optional[Callable]) – 用于自定义错误处理函数

## **class sanic_dantic.ParsedArgsObj**

### 说明

继承自 `dict` ，用于存储解析后的参数。支持通过 `.` 进行访问，支持进行 deepcopy。

### 用法

#### `__init__(self, *args, **kwargs)`

#### `__getattr__(self, name)`

#### `__setattr__(self, name, value)`

## **def validate(request: Request, dmo: DanticModelObj) -> Any**

### 说明

对请求进行参数检查，返回解析后的参数。

### 用法

#### `validate(request: Request, dmo: DanticModelObj) -> Any`

- `request` (Request) – 请求对象
- `dmo` (DanticModelObj) – 参数检查模型

## **class DanticView**

### 说明

继承自 `sanic.views.HTTPMethodView` ，重写了 `dispatch_request` 方法，使其支持参数检查。

### 用法

#### `dispatch_request(self, request, *args, **kwargs)`

- `request` (Request) – 请求对象
- `*args` – 位置参数
- `**kwargs` – 关键字参数

## **def parser_params(*args, **kwargs)**

### 说明

参数检查装饰器，用于对请求进行参数检查。

### 用法

#### `parser_params(*args, **kwargs)`

- `methods` (List[str]) – 请求方法列表，默认为 `None`, 表示所有方法
- `headers` (Optional[pydantic.BaseModel]) – 用于检查请求头的模型
- `path` (Optional[pydantic.BaseModel]) – 用于检查路径参数的模型
- `query` (Optional[pydantic.BaseModel]) – 用于检查查询参数的模型
- `body` (Optional[pydantic.BaseModel]) – 用于检查请求体的模型
- `form` (Optional[pydantic.BaseModel]) – 用于检查表单数据的模型
- `error` (Optional[Callable]) – 用于自定义错误处理函数

