#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: fbv_test
Description:
Author: Connor Zhang
Email: chzhangyue@qq.com
CreateTime: 2022-05-08
"""
import unittest
from unittest import TestCase

from fbv_server import app


class FbvTest(TestCase):
    def setUp(self) -> None:
        self.app = app.test_client

    def test_fbv_query(self):
        params = {'name': 'Connor', 'age': '18'}
        _, resp = self.app.get("/fbv_query_test", params=params)
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_fbv_body(self):
        params = {'name': 'Connor', 'age': '18'}
        _, resp = self.app.post("/fbv_body_test", json=params)
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_fbv_form(self):
        params = {'name': 'Connor', 'age': '18'}
        _, resp = self.app.post("/fbv_form_test", data=params)
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_fbv_header(self):
        params = {'name': 'Connor', 'age': '18'}
        _, resp = self.app.get(
            "/fbv_header_test",
            headers={'name': 'Connor', 'age': '18'}
        )
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_fbv_path(self):
        _, resp = self.app.get("/fbv_path_test/Connor/18")
        print(resp.json)
        self.assertEqual(resp.status_code, 200)

    def test_fbv_error(self):
        params = {'name': '18', 'age': 'Connor'}
        _, resp = self.app.get("/fbv_error_test", params=params)
        print(resp.text, resp.status_code)
        self.assertEqual(resp.status_code, 500)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
