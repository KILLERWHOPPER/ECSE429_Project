import urllib
from operator import itemgetter

import pytest
import requests
import json
from requests.auth import HTTPBasicAuth

home = "http://localhost:4567"
api_path = "/todos"


@pytest.mark.to_get
class TestTodoGet:

    @pytest.fixture(autouse=True)
    def initialize(self):
        # TODO: initialize test status
        headers = {"Content-Type": "application/json"}
        requests.delete(url=home + api_path + "?id=1")
        requests.delete(url=home + api_path + "?id=2")

        data1 = {"title": "Test1", "doneStatus": False, "description": "first todo"}
        data2 = {"title": "Test2", "doneStatus": True, "description": "second todo"}
        data3 = {"title": "Test3", "doneStatus": False, "description": "third todo"}
        data4 = {"title": "Test4", "doneStatus": True, "description": "fourth todo"}
        data5 = {"title": "Test4", "doneStatus": False, "description": "fifth todo"}

        requests.post(home + api_path, data=json.dumps(data1), headers=headers)
        requests.post(home + api_path, data=json.dumps(data2), headers=headers)
        requests.post(home + api_path, data=json.dumps(data3), headers=headers)
        requests.post(home + api_path, data=json.dumps(data4), headers=headers)
        requests.post(home + api_path, data=json.dumps(data5), headers=headers)

        yield

        request = requests.get(url=home + api_path)
        response = request.json()
        todos = response["todos"]
        print("")
        print("====================after each===================")
        for cur in todos:
            id = cur["id"]
            delRes = requests.delete(url=home + api_path + "/" + format(id))
            print("delete todo with id: " + id + ", status code: " + format(delRes.status_code))
        print("=================================================")
        print("")

    # Success mode
    def test_get_all(self):
        request = requests.get(url=home + api_path)
        response = request.json()
        todos = response["todos"]
        status_code = request.status_code
        print('')
        for cur in todos:
            print(format(cur) + ", status code: " + format(status_code))
        assert status_code == 200
        assert len(todos) == 5

    def test_get_by_title(self):
        request = requests.get(url=home + api_path + "?title=Test1")
        response = request.json()

        status_code = request.status_code
        print('n/')
        print(format(response["todos"]) + ", status code: " + format(status_code))
        assert status_code == 200
        todos = response["todos"]
        assert len(todos) != 0
        assert todos[0]["title"] == "Test1"
        assert todos[0]["doneStatus"] == "false"
        assert todos[0]["description"] == "first todo"

    def test_get_by_title_multi(self):
        request = requests.get(url=home + api_path + "?title=Test4")
        response = request.json()

        status_code = request.status_code
        print('')
        for cur in response["todos"]:
            print(format(cur) + ", status code: " + format(status_code))
        assert status_code == 200
        todos = response["todos"]
        assert len(todos) == 2

    def test_get_by_id(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        request = requests.get(url=home + api_path + "/" + format(id))
        response = request.json()

        status_code = request.status_code
        print(format(response["todos"][0]) + ", status code: " + format(status_code))
        assert status_code == 200
        todos = response["todos"]
        assert todos[0]["id"] == id
        assert todos[0]["title"] == "Test1"
        assert todos[0]["doneStatus"] == "false"
        assert todos[0]["description"] == "first todo"
