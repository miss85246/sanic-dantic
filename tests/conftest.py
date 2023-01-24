# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: conftest.py
Description: 
Author: Connor Zhang
CreateTime:  2023-01-23
"""

import pytest


@pytest.fixture
def test_client():
    from app import app
    return app.test_client
