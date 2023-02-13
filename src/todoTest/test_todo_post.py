import pytest
import requests
import json

home = "http://localhost:4567"
api_path = "/todos"
headers = {"Content-Type": "application/json"}


# @pytest.mark.todo
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
    def test_post_new(self):

        data = {"title": "Test6", "doneStatus": False, "description": "sixth todo"}
        response = requests.post(url=home + api_path, data=json.dumps(data), headers=headers)
        resJson = response.json()
        status_code = response.status_code
        assert status_code == 201
        assert resJson["title"] == "Test6"
        assert resJson["doneStatus"] == "false"
        assert resJson["description"] == "sixth todo"

    def test_post_edit(self):
        data = {"description":"modified"}
        id=requests.get(url=home+api_path+"?title=Test1").json()["todos"][0]["id"]
        response = requests.post(url=home + api_path+"/"+format(id), data=json.dumps(data), headers=headers)
        resJson = response.json()
        status_code = response.status_code
        assert status_code == 200
        assert resJson["title"] == "Test1"
        assert resJson["doneStatus"] == "false"
        assert resJson["description"] == "modified"

    def test_post_add_taskof(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        projid = requests.get(url=home + "/projects?title=Office Work").json()["projects"][0]["id"]
        response = requests.post(url=home + api_path+"/"+format(id)+"/tasksof", data=json.dumps({"id":projid}), headers=headers)

        status_code = response.status_code
        assert status_code == 201
        assert requests.get(url=home+api_path+"/"+format(id)+"/tasksof").json()["projects"][0]["title"]=="Office Work"

    def test_post_add_category(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        catid = requests.get(url=home + "/categories?title=Office").json()["categories"][0]["id"]
        response = requests.post(url=home + api_path + "/" + format(id) + "/categories", data=json.dumps({"id": catid}),headers=headers)

        status_code = response.status_code
        assert status_code == 201
        assert requests.get(url=home + api_path + "/" + format(id) + "/categories").json()["categories"][0]["title"] == "Office"

    # Failed mode
    def test_post_new_unknown_field(self):
        data = {"title": "Test6", "doneStatus": False, "description": "sixth todo", "unknownField":"unknown"}
        response = requests.post(url=home + api_path, data=json.dumps(data), headers=headers)
        resJson = response.json()
        status_code = response.status_code
        assert status_code == 400
        assert resJson["errorMessages"] == ["Could not find field: unknownField"]

    def test_post_new_no_title(self):
        data = {"doneStatus": False, "description": "sixth todo"}
        response = requests.post(url=home + api_path, data=json.dumps(data), headers=headers)
        resJson = response.json()
        status_code = response.status_code
        assert status_code == 400
        assert resJson["errorMessages"] == ["title : field is mandatory"]

    def test_post_edit_unknown_field(self):
        data = {"unknownField": "modified"}
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        response = requests.post(url=home + api_path + "/" + format(id), data=json.dumps(data), headers=headers)
        resJson = response.json()
        status_code = response.status_code
        assert status_code == 400
        assert resJson["errorMessages"] == ["Could not find field: unknownField"]

    def test_post_edit_no_change(self):
        data = {}
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        response = requests.post(url=home + api_path + "/" + format(id), data=json.dumps(data), headers=headers)
        resJson = response.json()
        status_code = response.status_code
        assert status_code == 200
        assert resJson["title"] == "Test1"
        assert resJson["doneStatus"] == "false"
        assert resJson["description"] == "first todo"

    def test_post_edit_id_not_exist(self):
        data = {"description": "modified"}
        id = 114514
        response = requests.post(url=home + api_path + "/" + format(id), data=json.dumps(data), headers=headers)
        resJson = response.json()
        status_code = response.status_code
        assert status_code == 404
        assert resJson["errorMessages"] == ["No such todo entity instance with GUID or ID 114514 found"]

    def test_post_add_taskof_already_exist(self):
        id = requests.get(url=home + api_path + "?title=Test2").json()["todos"][0]["id"]
        projid = requests.get(url=home + api_path+"/"+format(id)+"/tasksof").json()["projects"][0]["id"]
        response = requests.post(url=home + api_path + "/" + format(id) + "/tasksof", data=json.dumps({"id": projid}),
                                 headers=headers)

        status_code = response.status_code
        assert status_code == 201
        assert requests.get(url=home + api_path + "/" + format(id) + "/tasksof").json()["projects"][0][
                   "title"] == "testProject"
    def test_post_add_tasksof_todo_not_exist(self):
        projid = requests.get(url=home + "/projects?title=Office Work").json()["projects"][0]["id"]
        response = requests.post(url=home + api_path + "/114514/tasksof", data=json.dumps({"id": projid}),headers=headers)

        status_code = response.status_code
        assert status_code == 404
        assert response.json()["errorMessages"]==["Could not find parent thing for relationship todos/114514/tasksof"]

    def test_post_add_tasksof_project_not_exist(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        response = requests.post(url=home + api_path + "/"+format(id)+"/tasksof", data=json.dumps({"id": 114514}),headers=headers)

        status_code = response.status_code
        assert status_code == 404
        assert response.json()["errorMessages"] == ["Could not find thing matching value for id"]

    def test_post_add_tasksof_project_unknown_field(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        # projid = requests.get(url=home + "/projects?title=Office Work").json()["projects"][0]["id"]
        response = requests.post(url=home + api_path + "/" + format(id) + "/tasksof", data=json.dumps({"unknownField": "unknown"}),
                                 headers=headers)

        status_code = response.status_code
        assert status_code == 400
        assert response.json()["errorMessages"] == ["Unknown field"]

    def test_post_add_category_todo_not_exist(self):
        catid = requests.get(url=home + "/categories?title=Office").json()["categories"][0]["id"]
        response = requests.post(url=home + api_path + "/114514/categories", data=json.dumps({"id": catid}), headers=headers)

        status_code = response.status_code
        assert status_code == 404
        assert response.json()["errorMessages"]==["Could not find parent thing for relationship todos/114514/categories"]

    def test_post_add_category_not_exist(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        #catid = requests.get(url=home + "/categories?title=Office").json()["categories"][0]["id"]
        response = requests.post(url=home + api_path + "/"+format(id)+"/categories", data=json.dumps({"id": 114514}),
                                 headers=headers)

        status_code = response.status_code
        assert status_code == 404
        assert response.json()["errorMessages"] == ["Could not find thing matching value for id"]

    def test_post_add_category_unknown_field(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        response = requests.post(url=home + api_path + "/" + format(id) + "/categories",
                                 data=json.dumps({"unknownField": "unknown"}),
                                 headers=headers)

        status_code = response.status_code
        assert status_code == 400
        assert response.json()["errorMessages"] == ["Unknown field"]

