#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: cbv_test
Description:
Author: Connor Zhang
Email: chzhangyue@qq.com
CreateTime: 2022-05-08
"""
import unittest
from unittest import TestCase

from cbv_server import app


class CbvTest(TestCase):
    def setUp(self) -> None:
        self.app = app.test_client

    def test_cbv_query(self):
        params = {'name': 'Connor', 'age': '18'}
        _, resp = self.app.get("/person", params=params)
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_cbv_body(self):
        params = {'name': 'Connor', 'age': '18'}
        _, resp = self.app.post("/person", json=params)
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_cbv_header(self):
        params = {'name': 'Connor', 'age': '18'}
        _, resp = self.app.put("/person", headers=params)
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_cbv_form(self):
        params = {'name': 'Connor', 'age': '18'}
        _, resp = self.app.post("/dantic_person", data=params)
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_cbv_path(self):
        _, resp = self.app.get("/dantic_path_person/Connor/18")
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_cbv_error(self):
        params = {'name': '18', 'age': 'Connor'}
        _, resp = self.app.get("/dantic_person", params=params)
        print(resp.text, resp.status_code)
        self.assertEqual(resp.status_code, 500)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
