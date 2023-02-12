import pytest
import requests
import json

home = "http://localhost:4567"
api_path = "/todos"
headers = {"Content-Type": "application/json"}


@pytest.mark.to_get
class TestTodoPost:

    @pytest.fixture(autouse=True)
    def initialize(self):

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

        requests.post(home + "/categories", data=json.dumps({"title": "testCategory"}), headers=headers)

        requests.post(home + "/projects", data=json.dumps({"title": "testProject"}), headers=headers)

        pre_todos = requests.get(url=home + api_path).json()["todos"]
        catid = requests.get(url=home + "/categories?title=testCategory").json()["categories"][0]["id"]
        projid = requests.get(url=home + "/projects?title=testProject").json()["projects"][0]["id"]
        for cur in pre_todos:
            if (cur["title"] == "Test2" or cur["title"] == "Test3" or cur[
                "title"] == "Test4"):
                id = cur["id"]
                print("connect todo " + format(cur["title"]) + "with category testCategory. status code: " + format(
                    requests.post(home + api_path + "/" + format(id) + "/categories", headers=headers,
                                  data=json.dumps({"id": catid})).status_code))
                print("connect todo " + format(cur["title"]) + "with project testProject. status code: " + format(
                    requests.post(home + api_path + "/" + format(id) + "/tasksof", headers=headers,
                                  data=json.dumps({"id": projid})).status_code))

        yield

        request = requests.get(url=home + api_path)
        response = request.json()
        todos = response["todos"]
        print("")
        print("====================after each===================")
        for cur in todos:
            if (cur["title"] == "Test1" or cur["title"] == "Test2" or cur["title"] == "Test3" or cur[
                "title"] == "Test4" or cur["title"]=="Test6"):
                id = cur["id"]
                delRes = requests.delete(url=home + api_path + "/" + format(id))
                print("delete todo with id: " + id + ", status code: " + format(delRes.status_code))

        catrequest = requests.get(url=home + "/categories")
        catresponse = catrequest.json()
        categories = catresponse["categories"]
        for cur in categories:
            if (cur["title"] == "testCategory"):
                delRes = requests.delete(url=home + "/categories/" + format(cur["id"]))
                print("delete category with id: " + cur["id"] + ", status code: " + format(delRes.status_code))

        projrequest = requests.get(url=home + "/projects")
        projresponse = projrequest.json()
        projects = projresponse["projects"]
        for cur in projects:
            if (cur["title"] == "testProject"):
                delRes = requests.delete(url=home + "/projects/" + format(cur["id"]))
                print("delete project with id: " + cur["id"] + ", status code: " + format(delRes.status_code))
        print("=================================================")
        print("")

    # Success mode
    def test_head_all(self):
        response=requests.head(url=home+api_path)

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    def test_head_by_title(self):
        response = requests.head(url=home + api_path + "?title=file paperwork")

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200
    def test_head_by_id(self):
        response = requests.head(url=home+api_path+"/1")

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    def test_head_tasksof_all(self):
        response = requests.head(url=home + api_path + "/1/tasksof")

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    def test_head_tasksof(self):
        response = requests.head(url=home + api_path + "/1/tasksof",data=json.dumps({"id":1}),headers=headers)

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    def test_head_category_all(self):
        response = requests.head(url=home + api_path + "/1/categories")

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    def test_head_category(self):
        response = requests.head(url=home + api_path + "/1/categories", data=json.dumps({"id": 1}), headers=headers)

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    # Fail mode
    def test_head_id_not_exist(self):
        response = requests.head(url=home + api_path + "/114514")

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 404

    def test_head_title_not_exist(self):
        response = requests.head(url=home + api_path + "?title=notExist")

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 404

    def test_head_tasksof_all_id_not_exist(self):
        response = requests.head(url=home + api_path + "/114514")

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 404

    def test_head_tasksof_todo_not_exist(self):
        response = requests.head(url=home + api_path + "/114514",data=json.dumps({"id":1}),headers=headers)

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 404

    def test_head_tasksof_project_not_exist(self):
        response = requests.head(url=home + api_path + "/1", data=json.dumps({"id": 114514}), headers=headers)

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 404

    def test_head_category_all_id_not_exist(self):
        response = requests.head(url=home + api_path + "/114514")

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 404

    def test_head_category_todo_not_exist(self):
        response = requests.head(url=home + api_path + "/114514", data=json.dumps({"id": 1}), headers=headers)

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 404

    def test_head_category_not_exist(self):
        response = requests.head(url=home + api_path + "/1", data=json.dumps({"id": 114514}), headers=headers)

        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 404

