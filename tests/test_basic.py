# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: test_basic.py
Description: 
Author: Connor Zhang
CreateTime:  2023-01-23
"""

from copy import deepcopy

import pytest
from sanic.exceptions import ServerError

from model import Person
from sanic_dantic import ParsedArgsObj, DanticModelObj


class TestBasic:

    def test_parse_args(self):
        obj = ParsedArgsObj()
        obj.name = 'Connor'
        obj.age = 18
        print(deepcopy(obj))
        assert obj.name == 'Connor'
        assert obj.age == 18
        assert obj == {'name': 'Connor', 'age': 18}

    def test_dantic_model(self):
        obj = DanticModelObj(
            header=Person, query=Person, path=Person, body=Person
        )
        assert obj.header == Person
        assert obj.query == Person
        assert obj.path == Person
        assert obj.body == Person

    def test_form_and_data(self):
        try:
            DanticModelObj(body=Person, form=Person)
        except Exception as e:
            assert isinstance(e, ServerError)

    def test_not_base_model(self):
        try:
            DanticModelObj(body=ServerError)
        except Exception as e:
            assert isinstance(e, ServerError)

    def test_not_callable(self):
        try:
            DanticModelObj(error='name')
        except Exception as e:
            assert isinstance(e, ServerError)


if __name__ == '__main__':
    pytest.main(['-s', 'test_basic.py'])
