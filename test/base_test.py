import unittest

from sanic_dantic.basic_definition import *


class TestBase(unittest.TestCase):
    class Person(BaseModel):
        name: str
        age: int

    class Car:
        speed: int

    def test_ParsedArgsObj(self):
        obj = ParsedArgsObj({"a": 1})
        self.assertEqual(obj.a, 1)
        obj.b = 2
        print(obj.get("a"))
        obj.update({"b": 2})
        self.assertEqual(obj.b, 2)

    def test_DanticModelObj(self):
        parsed = ParsedArgsObj(query=self.Person, path=self.Person, body=self.Person)
        try:
            DanticModelObj(query=self.Person, path=self.Person, body=self.Person, form=self.Person)
        except InvalidOperation as e:
            self.assertEqual(type(e), InvalidOperation)
        try:
            DanticModelObj(query=self.Car, path=self.Person, body=self.Person, )
        except TypeError as e:
            self.assertEqual(str(e), "param must type of pydantic.BaseModel")
        obj = DanticModelObj(query=self.Person, path=self.Person, body=self.Person)
        print(obj)
        self.assertEqual(obj.items.get('path'), parsed.get('path'))
