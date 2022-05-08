#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: dantic_model
Description:
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2022-05-08
"""

from sanic_dantic import BaseModel, Field


class Person(BaseModel):
    name: str = Field(description="name")
    age: int = Field(description="age")


class Car:
    name: str = Field(description="name")
    speed: int = Field(description="speed")
