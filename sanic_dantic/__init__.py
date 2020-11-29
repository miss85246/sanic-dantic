# -*- coding: utf-8 -*-
from pydantic import *

from .sanic_class_dantic import DanticView
from .sanic_function_dantic import parse_params

__author__ = "Connor Zhang"
__copyright__ = "Copyright 2020, Connor Zhang"
__license__ = "MIT"
__version__ = "1.1.4"
__all__ = [
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
    'Schema',
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
    'ConstrainedFloat',
    'confloat',
    'PositiveFloat',
    'NegativeFloat',
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
    'StrictInt',
    'StrictFloat',
    'PaymentCardNumber',
    'ByteSize',
    # sanic-dantic
    'parse_params',
    'DanticView'
]
