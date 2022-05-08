# -*- coding: utf-8 -*-
from pydantic import *

from .sanic_class_dantic import DanticView
from .sanic_function_dantic import parse_params

__author__ = "Connor Zhang"
__copyright__ = "Copyright 2020, Connor Zhang"
__license__ = "MIT"
__version__ = "1.2.0"
__all__ = [
    # annotated types utils
    'create_model_from_namedtuple',
    'create_model_from_typeddict',
    # dataclasses
    'dataclasses',
    # class_validators
    'root_validator',
    'validator',
    # decorator
    'validate_arguments',
    # env_settings
    'BaseSettings',
    # error_wrappers
    'ValidationError',
    # fields
    'Field',
    'Required',
    # main
    'BaseConfig',
    'BaseModel',
    'Extra',
    'compiled',
    'create_model',
    'validate_model',
    # network
    'AnyUrl',
    'AnyHttpUrl',
    'HttpUrl',
    'stricturl',
    'EmailStr',
    'NameEmail',
    'IPvAnyAddress',
    'IPvAnyInterface',
    'IPvAnyNetwork',
    'PostgresDsn',
    'RedisDsn',
    'validate_email',
    # parse
    'Protocol',
    # tools
    'parse_file_as',
    'parse_obj_as',
    'parse_raw_as',
    # types
    'NoneStr',
    'NoneBytes',
    'StrBytes',
    'NoneStrBytes',
    'StrictStr',
    'ConstrainedBytes',
    'conbytes',
    'ConstrainedList',
    'conlist',
    'ConstrainedSet',
    'conset',
    'ConstrainedStr',
    'constr',
    'PyObject',
    'ConstrainedInt',
    'conint',
    'PositiveInt',
    'NegativeInt',
    'NonNegativeInt',
    'NonPositiveInt',
    'ConstrainedFloat',
    'confloat',
    'PositiveFloat',
    'NegativeFloat',
    'NonNegativeFloat',
    'NonPositiveFloat',
    'ConstrainedDecimal',
    'condecimal',
    'UUID1',
    'UUID3',
    'UUID4',
    'UUID5',
    'FilePath',
    'DirectoryPath',
    'Json',
    'JsonWrapper',
    'SecretStr',
    'SecretBytes',
    'StrictBool',
    'StrictBytes',
    'StrictInt',
    'StrictFloat',
    'PaymentCardNumber',
    'PrivateAttr',
    'ByteSize',
    # sanic-dantic
    'parse_params',
    'DanticView'
]
