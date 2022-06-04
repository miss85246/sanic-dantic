#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: other_test
Description:
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2022-06-04
"""

import unittest
from copy import deepcopy

from sanic_dantic import ParsedArgsObj


class OtherTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_deepcopy(self):
        args = ParsedArgsObj(name='Connor', age=18)
        print(args)
        copy_args = deepcopy(args)
        self.assertEqual(args, copy_args)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
