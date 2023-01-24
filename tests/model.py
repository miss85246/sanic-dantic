# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: model.py
Description: 
Author: Connor Zhang
CreateTime:  2023-01-23
"""

from pydantic import BaseModel, Field


class Person(BaseModel):
    name: str = Field(description="name")
    age: int = Field(description="age")
