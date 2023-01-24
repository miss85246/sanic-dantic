# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: test_fbv.py
Description:
Author: Connor Zhang
CreateTime:  2023-01-23
"""

import pytest


@pytest.mark.usefixtures('test_client')
class TestFbv:
    def test_fbv_header(self, test_client):
        headers = {'name': 'Connor', 'age': '18'}
        request, response = test_client.get('/fbv_header_test', headers=headers)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_fbv_path(self, test_client):
        request, response = test_client.get('/fbv_path_test/Connor/18')
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_fbv_query(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.get('/fbv_query_test', params=params)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_fbv_form(self, test_client):
        data = {'name': 'Connor', 'age': '18'}
        request, response = test_client.post('/fbv_form_test', data=data)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_fbv_body(self, test_client):
        data = {'name': 'Connor', 'age': '18'}
        request, response = test_client.post('/fbv_body_test', json=data)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_fbv_delete(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.delete('/fbv_del_test', params=params)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_fbv_error(self, test_client):
        params = {'name': 'Connor', 'age': 'name'}
        request, response = test_client.put('/fbv_error_test', json=params)
        print(response.json)
        assert response.status == 400
        assert response.json['message'] == 'age value is not a valid integer'
        assert response.json['status_code'] == 400


if __name__ == '__main__':
    pytest.main(['-s', 'test_fbv.py'])
