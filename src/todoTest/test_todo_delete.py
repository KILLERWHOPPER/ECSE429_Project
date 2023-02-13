import pytest
import requests
import json

home = "http://localhost:4567"
api_path = "/todos"
headers = {"Content-Type": "application/json"}
# @pytest.mark.todo
class TestTodoDelete:

    # BeforeEach and AfterEach
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

        requests.post(home+"/categories", data=json.dumps({"title":"testCategory"}),headers=headers)

        requests.post(home+"/projects", data=json.dumps({"title":"testProject"}),headers=headers)

        pre_todos = requests.get(url=home + api_path).json()["todos"]
        catid=requests.get(url=home+"/categories?title=testCategory").json()["categories"][0]["id"]
        projid=requests.get(url=home+"/projects?title=testProject").json()["projects"][0]["id"]
        for cur in pre_todos:
            if (cur["title"] == "Test1" or cur["title"] == "Test2" or cur["title"] == "Test3" or cur["title"] == "Test4"):
                id = cur["id"]
                print("connect todo "+format(cur["title"])+"with category testCategory. status code: "+format(requests.post(home + api_path + "/" + format(id)+"/categories", headers=headers, data=json.dumps({"id":catid})).status_code))
                print("connect todo " + format(cur["title"]) + "with project testProject. status code: " + format(requests.post(home + api_path + "/" + format(id) + "/tasksof", headers=headers,data=json.dumps({"id": projid})).status_code))

        yield

        request = requests.get(url=home + api_path)
        response = request.json()
        todos = response["todos"]
        print("")
        print("====================after each===================")
        for cur in todos:
            if (cur["title"] == "Test1" or cur["title"] == "Test2" or cur["title"] == "Test3" or cur[
                "title"] == "Test4"):
                id = cur["id"]
                delRes = requests.delete(url=home + api_path + "/" + format(id))
                print("delete todo with id: " + id + ", status code: " + format(delRes.status_code))

        catrequest =requests.get(url=home+"/categories")
        catresponse=catrequest.json()
        categories=catresponse["categories"]
        for cur in categories:
            if(cur["title"]=="testCategory"):
                delRes = requests.delete(url=home+"/categories/"+format(cur["id"]))
                print("delete category with id: "+cur["id"]+", status code: "+format(delRes.status_code))

        projrequest = requests.get(url=home + "/projects")
        projresponse = projrequest.json()
        projects = projresponse["projects"]
        for cur in projects:
            if(cur["title"]=="testProject"):
                delRes = requests.delete(url=home+"/projects/"+format(cur["id"]))
                print("delete project with id: "+cur["id"]+", status code: "+format(delRes.status_code))
        print("=================================================")
        print("")

    # Success mode
    def test_delete_by_id(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]
        request = requests.delete(url=home + api_path + "/"+format(id))

        assert request.status_code == 200
        checkRequest=requests.get(url=home + api_path + "?title=Test1")
        checkTodo=checkRequest.json()["todos"]
        assert len(checkTodo)==0

    def test_delete_relation_tasksof(self):
        projid=requests.get(url=home+"/projects?title=testProject").json()["projects"][0]["id"]
        id=requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]

        request = requests.delete(url=home + api_path + "/" + format(id) + "/tasksof/" + format(projid))

        assert request.status_code == 200
        checkTodo = requests.get(url=home + api_path + "/" + format(id) + "/tasksof")
        assert len(checkTodo.json()["projects"]) == 0

    def test_delete_relation_categories(self):
        catid=requests.get(url=home+"/categories?title=testCategory").json()["categories"][0]["id"]
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]

        request=requests.delete(url=home+api_path+"/"+format(id)+"/categories/"+format(catid))

        assert request.status_code==200
        checkTodo=requests.get(url=home+api_path+"/"+format(id)+"/categories")
        assert len(checkTodo.json()["categories"])==0

    # Failure mode

    def test_delete_by_id_non_exist(self):
        request = requests.delete(url=home + api_path + "/114514")

        assert request.status_code == 404
        assert request.json()["errorMessages"][0] == "Could not find any instances with todos/114514"

    def test_delete_relation_tasksof_todo_id_non_exist(self):
        projid = requests.get(url=home + "/projects?title=testProject").json()["projects"][0]["id"]

        request = requests.delete(url=home + api_path + "/114514" + "/tasksof/" + format(projid))

        assert request.status_code == 404 or 400
        assert request.json()["errorMessages"][0] == "Could not find any instances with todos/114514/"+format(projid)

    def test_delete_relation_tasksof_project_id_non_exist(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]

        request = requests.delete(url=home + api_path + format(id) + "/tasksof/114514")

        assert request.status_code == 404 or 400
        assert len(request.content)!=0

    def test_delete_relation_categories_todo_id_non_exist(self):
        catid = requests.get(url=home + "/categories?title=testCategory").json()["categories"][0]["id"]

        request = requests.delete(url=home + api_path + "/114514" + "/categories/" + format(catid))

        assert request.status_code == 404 or 400
        assert request.json()["errorMessages"][0] == "Could not find any instances with todos/114514"

    def test_delete_relation_categories_category_id_non_exist(self):
        id = requests.get(url=home + api_path + "?title=Test1").json()["todos"][0]["id"]

        request = requests.delete(url=home + api_path + format(id) + "/categories/114514")

        assert request.status_code == 404 or 400
        assert len(request.content)!=0
        assert request.json()["errorMessages"][0] == "Could not find any instances with todos/114514"