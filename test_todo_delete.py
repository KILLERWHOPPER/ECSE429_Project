import pytest
import requests
import json

home = "http://localhost:4567"
api_path = "/todos"


@pytest.mark.to_get
class TestTodoDelete:

    # BeforeEach and AfterEach
    @pytest.fixture(autouse=True)
    def initialize(self):
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
    def test_delete(self):
        # TODO: finish delete one by id
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        request = requests.delete(url=home + api_path + "/"+format(id))

        assert request.status_code == 200
        checkRequest=requests.get(url=home + api_path + "?title=Test1")
        checkTodo=checkRequest.json()["todos"]
        assert len(checkTodo)==0
