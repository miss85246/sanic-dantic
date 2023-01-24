# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: test_cbv.py
Description:
Author: Connor Zhang
CreateTime:  2023-01-23
"""
import pytest


@pytest.mark.usefixtures('test_client')
class TestCbvNormalView:

    def test_normal_get(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.get('/normal_test', params=params)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_normal_post(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.post('/normal_test', params=params)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_normal_error(self, test_client):
        params = {'name': 'Connor', 'age': 'name'}
        request, response = test_client.post('/normal_test', params=params)
        print(response.json)
        assert response.status == 400
        assert response.json['message'] == 'age value is not a valid integer'
        assert response.json['status_code'] == 400

    def test_appoint_get(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.get('/appoint_test', params=params)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_appoint_post(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.post('/appoint_test', params=params)
        print(response.json)
        assert response.status == 200
        assert response.json == {'args': [], 'kwargs': {}}

    def test_dantic_get(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.get('/dantic_test/', params=params)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_dantic_post(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.post('/dantic_test', params=params)
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_dantic_error(self, test_client):
        params = {'name': 'Connor', 'age': 'name'}
        request, response = test_client.post('/dantic_test', params=params)
        print(response.json)
        assert response.status == 400
        assert response.json['message'] == 'age value is not a valid integer'
        assert response.json['status_code'] == 400

    def test_dantic_appoint_get(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.get(
            '/dantic_appoint_test',
            params=params
        )
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_dantic_appoint_post(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.post(
            '/dantic_appoint_test',
            params=params
        )
        print(response.json)
        assert response.status == 200
        assert response.json == {'args': [], 'kwargs': {}}

    def test_dantic_def_model_get(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.get(
            '/dantic_def_model_test',
            params=params
        )
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_dantic_def_model_post(self, test_client):
        params = {'name': 'Connor', 'age': '18'}
        request, response = test_client.post(
            '/dantic_def_model_test',
            json=params
        )
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}

    def test_dantic_def_model_error(self, test_client):
        params = {'name': 'Connor', 'age': 'name'}
        request, response = test_client.get(
            '/dantic_def_model_test',
            params=params
        )
        print(response.json)
        assert response.status == 400
        assert response.json['message'] == 'age value is not a valid integer'
        assert response.json['status_code'] == 400

    def test_dantic_path_get(self, test_client):
        request, response = test_client.get('/dantic_path_test/Connor/18')
        print(response.json)
        assert response.status == 200
        assert response.json['ctx.params'] == {'name': 'Connor', 'age': 18}
        assert response.json['params'] == {'name': 'Connor', 'age': 18}


if __name__ == '__main__':
    pytest.main(['-s', 'test_cbv.py'])
