import unittest

import requests


class TestSanicDantic(unittest.TestCase):
    def setUp(self):
        self.session = requests.session()
        self.data = {"name": "test", "age": 100}
        self.expected_result = {"params": self.data, "request.ctx.params": self.data}

    def test_path_test(self):
        url = f'http://localhost:5000/path_test/{self.data["name"]}/{self.data["age"]}/'
        res = self.session.get(url).json()
        self.assertEqual(res, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_get_test(self):
        url = 'http://localhost:5000/query_test/'
        res = self.session.get(url, params=self.data).json()
        self.assertEqual(res, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_form_test(self):
        url = 'http://localhost:5000/form_test/'
        res = self.session.post(url, data=self.data).json()
        self.assertEqual(res, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_body_test(self):
        url = 'http://localhost:5000/body_test/'
        res = self.session.post(url, json=self.data).json()
        self.assertEqual(res, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_cbv_query_test(self):
        url = 'http://localhost:5000/cbv_test/'
        res = self.session.get(url, params=self.data).json()
        self.assertEqual(res, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_cbv_form_test(self):
        url = 'http://localhost:5000/cbv_test/'
        res = self.session.post(url, data=self.data).json()
        self.assertEqual(res, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def test_cbv_body_test(self):
        url = 'http://localhost:5000/cbv_test/'
        res = self.session.put(url, json=self.data).json()
        self.assertEqual(res, self.expected_result), f"response: {res} \n expected_result: {self.expected_result}"

    def tearDown(self):
        self.session.close()


if __name__ == '__main__':
    unittest.main()
