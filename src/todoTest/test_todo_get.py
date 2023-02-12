import urllib
from operator import itemgetter

import pytest
import requests
import json


home = "http://localhost:4567"
api_path = "/todos"
headers = {"Content-Type": "application/json"}

@pytest.mark.to_get
class TestTodoGet:

    @pytest.fixture(autouse=True)
    def initialize(self):
        # TODO: initialize test status

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
            if(cur["title"]=="Test1" or cur["title"]=="Test2" or cur["title"]=="Test3" or cur["title"]=="Test4"):
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
        assert len(todos) == 7

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

    def test_get_taskof(self):
        id = requests.get(url=home + api_path + "?title=scan paperwork").json()["todos"][0]["id"]
        request = requests.get(url=home+api_path+"/"+format(id)+"/tasksof")
        status_code=request.status_code
        print (format(request.json()["projects"][0])+ ", status code: " + format(status_code))

        received=request.json()["projects"][0]
        assert status_code==200
        assert received["title"]=="Office Work"
        assert received["completed"]=="false"
        assert received["active"]=="false"

    def test_get_categories(self):
        id = requests.get(url=home + api_path + "?title=scan paperwork").json()["todos"][0]["id"]
        request = requests.get(url=home + api_path + "/" + format(id) + "/categories")
        status_code = request.status_code
        print(format(request.json()["categories"][0]) + ", status code: " + format(status_code))

        received = request.json()["categories"][0]
        assert status_code == 200
        assert received["title"] == "Office"

    # Failed mode
    def test_get_by_id_not_exist(self):
        request=requests.get(url=home+api_path+"/114514")

        assert request.status_code==404
        assert request.json()["errorMessages"][0]=="Could not find an instance with todos/114514"

    def test_get_by_title_not_exist(self):
        request=requests.get(url=home+api_path+"?title==NonExist")

        assert request.status_code==200
        assert len(request.json()["todos"])==0

    def test_get_taskof_todo_non_exist(self):
        request = requests.get(url=home + api_path + "/114514/tasksof")

        assert request.status_code == 404
        assert request.json()["errorMessages"][0] == "Could not find an instance with todos/114514"