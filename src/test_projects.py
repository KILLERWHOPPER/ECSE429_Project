import pytest
import requests
import json

url = "http://localhost:4567/projects"

NUMBER_OF_PROJECTS = 5

def delete_all_projects():
    response = requests.get(url)
    request_data = response.json()
    categories = request_data["projects"]
    for category in categories:
        if category["title"]=="Office Work":continue
        id = category["id"]
        requests.delete(url + f"/{id}")
    
    #assert len(requests.get(url).json()["projects"]) == 0

class TestCategoriesGet:
    @pytest.fixture(autouse=True)
    def initialize(self):
        delete_all_projects()
        for i in range(1, NUMBER_OF_PROJECTS):
            data = {"title": f"title{i}","description": f"description{i}"}
            requests.post(url, data=json.dumps(data))
        #assert len(requests.get(url).json().get("projects")) == NUMBER_OF_PROJECTS
        yield
        delete_all_projects()


    def test_create_project_documented_fail(self):
        # The json data formatting is the one shown in the documentation
        data = {
            "title": "epteur sint occaecat",
            "completed": "true",
            "active": "true",
            "description": "e magna aliqua. Ut e"
        }
        response = requests.post(url, json=data)
        request_data = response.json()
        assert response.status_code == 201
        assert request_data["title"] == data["title"]
        assert request_data["completed"] == str(data["completed"]).lower()
        assert request_data["active"] == str(data["active"]).lower()
        assert request_data["description"] == data["description"]

    def test_create_project_undocumented_success(self):
        data = {
            "title": "epteur sint occaecat",
            "completed": False,
            "active": True,
            "description": "e magna aliqua. Ut e"
        }
        response = requests.post(url, json=data)
        request_data = response.json()
        assert response.status_code == 201
        assert request_data["title"] == data["title"]
        assert request_data["completed"] == str(data["completed"]).lower()
        assert request_data["active"] == str(data["active"]).lower()
        assert request_data["description"] == data["description"]

    def test_create_project_empty_body(self):
        response = requests.post(url)
        request_data = response.json()
        # assert response.status_code == 400
        # assert request_data.get("errorMessages") is not None

    def test_get_projects(self):
        response = requests.get(url)
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("projects") is not None
        assert len(request_data["projects"]) == NUMBER_OF_PROJECTS

    def test_get_projects_with_filters_multiple(self):
        response = requests.get(url + "?completed=false&active=false")
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("projects") is not None
        assert len(request_data["projects"]) == NUMBER_OF_PROJECTS

    def test_get_projects_with_filters_single(self):

        response = requests.get(url + "?title=title1&description=description1")
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("projects") is not None
        assert len(request_data["projects"]) == 1
        assert request_data["projects"][0]["title"] == "title1"
        assert request_data["projects"][0]["description"] == "description1"
    
    def test_get_projects_with_filters_none(self):
        response = requests.get(url + "?title=title10&description=description10&completed=true&active=true")
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("projects") is not None
        assert len(request_data["projects"]) == 0

    def test_head_projects(self):
        response = requests.head(url)
        headers = response.headers
        assert response.status_code == 200
        assert headers.get("Content-Type") == "application/json"
        assert headers.get("Date") is not None
        assert headers.get("Server") is not None


    def test_head_projects_with_filters_multiple(self):
        response = requests.head(url + "?completed=false&active=false")
        headers = response.headers
        assert headers.get("Content-Type") == "application/json"
        assert headers.get("Date") is not None
        assert headers.get("Server") is not None

    def test_head_projects_with_filters_single(self):
        response = requests.head(url + "?title=title1&description=description1")
        headers = response.headers
        assert headers.get("Content-Type") == "application/json"
        assert headers.get("Date") is not None
        assert headers.get("Server") is not None
    
    def test_head_projects_with_filters_none(self):
        response = requests.head(url + "?title=title10&description=description10&completed=true&active=true")
        headers = response.headers
        # assert response.status_code == 404
        # assert headers.get("Content-Type") is None

    def test_get_project_by_id(self):
        title, description = "new_title", "new_description"
        data = {"title": title, "description": description}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        id = request_data["id"]
        response = requests.get(url + f"/{id}")
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("projects") is not None
        assert len(request_data["projects"]) == 1
        assert request_data["projects"][0]["title"] == title
        assert request_data["projects"][0]["description"] == description

    def test_get_project_by_id_not_found(self):
        response = requests.get(url + "/1000")
        request_data = response.json()
        assert response.status_code == 404
        assert request_data.get("errorMessages") is not None
    
    def test_head_project_by_id(self):
        title, description = "new_title", "new_description"
        data = {"title": title, "description": description}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        id = request_data["id"]
        response = requests.head(url + f"/{id}")
        headers = response.headers
        assert response.status_code == 200
        assert headers.get("Content-Type") == "application/json"
        assert headers.get("Date") is not None
        assert headers.get("Server") is not None
    
    def test_head_project_by_id_not_found(self):
        response = requests.head(url + "/1000")
        headers = response.headers
        # assert response.status_code == 404
        # assert headers.get("Content-Type") is None

    def test_post_project_by_id(self):
        response = requests.get(url)
        request_data = response.json()
        id = request_data["projects"][0]["id"]
        old_title = request_data["projects"][0]["title"]
        old_description = request_data["projects"][0]["description"]

        data = {"title":f"new_{old_title}", "description": f"new_{old_description}"}
        response = requests.post(url + f"/{id}", data=json.dumps(data))
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("id") == id
        assert request_data.get("description") == data["description"]
        assert request_data.get("title") == data["title"]

    def test_post_project_by_id_not_found(self):
        id = -1
        data = {"title":f"new", "description": f"new"}
        response = requests.post(url + f"/{id}", data=json.dumps(data))
        request_data = response.json()
        assert response.status_code == 404
        assert request_data.get("errorMessages") is not None

    def test_put_project_by_id(self):
        response = requests.get(url)
        request_data = response.json()
        id = request_data["projects"][1]["id"]
        old_title = request_data["projects"][1]["title"]
        old_description = request_data["projects"][1]["description"]

        data = {"title":f"new_{old_title}", "description": f"new_{old_description}"}
        response = requests.put(url + f"/{id}", data=json.dumps(data))
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("id") == id
        assert request_data.get("description") == data["description"]
        assert request_data.get("title") == data["title"]

    def test_put_project_by_id_not_found(self):
        id = -1
        data = {"title":f"new", "description": f"new"}
        response = requests.put(url + f"/{id}", data=json.dumps(data))
        request_data = response.json()
        assert response.status_code == 404
        assert request_data.get("errorMessages") is not None

    def test_delete_project_by_id(self):
        response = requests.get(url)
        request_data = response.json()
        id = request_data["projects"][1]["id"]
        response = requests.delete(url + f"/{id}")
        assert response.status_code == 200

        response = requests.get(url+f"/{id}")
        assert response.status_code == 404
        assert response.json().get("errorMessages") is not None

    def test_delete_project_by_id_not_found(self):
        id = -1
        response = requests.delete(url + f"/{id}")
        assert response.status_code == 404
        assert response.json().get("errorMessages") is not None

if "__main__" == __name__:
    pytest.main()