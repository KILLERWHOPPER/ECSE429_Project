import pytest
import requests
import json

url = "http://localhost:4567/categories"
NUMBER_OF_CATEGORIES = 5

def delete_all_categories():
    response = requests.get(url)
    request_data = response.json()
    categories = request_data["categories"]
    for category in categories:
        if category["title"]=="Home" or category["title"]=="Office" : continue
        id = category["id"]
        requests.delete(url + f"/{id}")

class TestCategoriesGet:
    @pytest.fixture(autouse=True)
    def initialize(self):
        delete_all_categories()
        for i in range(1, NUMBER_OF_CATEGORIES + 1):
            data = {"title": f"title{i}","description": f"description{i}"}
            requests.post(url, data=json.dumps(data))
        #assert len(requests.get(url).json()["categories"]) == NUMBER_OF_CATEGORIES

        yield # this is where the testing happens
        
        delete_all_categories()

    def test_get_all(self):
        response = requests.get(url)
        print(response.text)
        request_data = response.json()
        status_code = response.status_code
        print(request_data)
        assert status_code == 200
        assert "categories" in request_data

    def test_head_all_categories(self):
        response = requests.head(url)
        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    def test_post_create_category(self):
        data = {"title": "title","description": "test category"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("id") is not None
        assert request_data.get("title") == "title"
        assert request_data.get("description") == "test category"
        assert status_code == 201

    def test_post_create_category_with_id(self):
        data = {"id": 999,"title": "title","description": "test category"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("errorMessages") is not None
        assert status_code == 400

    def test_post_create_category_xml(self):
        data = {"title": "title", "description": "description"}
        response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/xml"})
        assert response.status_code == 201

    def test_post_create_category_content_type_plain(self):
        headers = {"Content-Type": "text/plain"}
        data = {"title": "title","description": "test category"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("id") is not None
        assert request_data.get("title") == "title"
        assert request_data.get("description") == "test category"
        assert status_code == 201
    
    def test_post_create_category_unknown_json_key(self):
        data = {"unknwon_key":"value", "title": "title","description": "test category"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("errorMessages") is not None
        assert status_code == 400
        
    def test_post_create_category_missing_description(self):
        data = {"title": "title"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("errorMessages") is None
        assert request_data.get("id") is not None
        assert request_data.get("description") == ""
        assert status_code == 201
    
    def test_post_create_category_empty_description(self):
        data = {"title": "title","description": ""}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("errorMessages") is None
        assert request_data.get("id") is not None
        assert request_data.get("description") == ""
        assert status_code == 201

    def test_post_create_category_missing_title(self):
        data = {"description": "description"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("errorMessages") is not None
        assert status_code == 400

    def test_post_create_category_empty_title(self):
        data = {"title": "","description": "description"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("errorMessages") is not None
        assert status_code == 400

    def test_post_create_category_with_id(self):
        data = {"id": 999,"title": "title","description": "test category"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        status_code = response.status_code
        assert request_data.get("errorMessages") is not None
        assert status_code == 400

    def test_get_category_by_id(self):
        data = {"title": "title","description": "test category"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        id = request_data["id"]
        response = requests.get(url + f"/{id}")
        request_data = response.json().get("categories")[0]
        assert response.status_code == 200
        assert request_data.get("id") is not None
        assert request_data.get("title") == "title"
        assert request_data.get("description") == "test category"

    def test_get_category_by_id_not_found(self):
        response = requests.get(url + "/999")
        request_data = response.json()
        assert response.status_code == 404
        assert request_data.get("errorMessages") is not None

    def test_get_category_by_id_invalid(self):
        response = requests.get(url + "/abc")
        request_data = response.json()
        assert response.status_code == 404
        assert request_data.get("errorMessages") is not None

    def test_get_category_by_title(self):
        new_title = "new_title"
        data = {"title": new_title,"description": "test category"}
        response = requests.post(url, data=json.dumps(data))
        response = requests.post(url, data=json.dumps(data))
        response = requests.get(url + f"?title={new_title}")
        request_data = response.json().get("categories")
        assert response.status_code == 200
        assert len(request_data) == 2

    def test_get_category_by_title_not_found(self):
        new_title = "new_title"
        response = requests.get(url + f"?title={new_title}")
        request_data = response.json().get("categories")
        status_code = response.status_code
        assert status_code == 404
        assert len(request_data) == 0
    
    def test_get_category_by_description(self):
        data = {"title": "title","description": "new_description"}
        response = requests.post(url, data=json.dumps(data))
        response = requests.post(url, data=json.dumps(data))
        response = requests.get(url + f"?description=new_description")
        request_data = response.json().get("categories")
        assert response.status_code == 200
        assert len(request_data) == 2

    def test_get_category_by_title_and_description(self):
        new_title = "new_title"
        new_description = "new_description"
        data = {"title": new_title,"description": new_description}
        response = requests.post(url, data=json.dumps(data))
        response = requests.post(url, data=json.dumps(data))
        data = {"title": new_title,"description": ""} # get response should ignore this category
        response = requests.post(url, data=json.dumps(data))
        response = requests.get(url + f"?title={new_title}&description={new_description}")
        request_data = response.json().get("categories")
        assert response.status_code == 200
        assert len(request_data) == 2

    def test_head_category_by_id(self):
        data = {"title": "title","description": "test category"}
        response = requests.post(url, data=json.dumps(data))
        request_data = response.json()
        id = request_data["id"]
        response = requests.head(url + f"/{id}")
        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    def test_head_category_by_id_non_existing(self):
        get_response = requests.get(url + f"/999")
        assert get_response.status_code == 404
        response = requests.head(url + f"/999")
        header_content_type = response.headers.get("Content-Type")
        assert header_content_type is None

    def test_head_category_by_title_and_description(self):
        new_title = "new_title"
        new_description = "new_description"
        data = {"title": new_title,"description": new_description}
        response = requests.post(url, data=json.dumps(data))
        response = requests.post(url, data=json.dumps(data))
        data = {"title": new_title,"description": ""} # get response should ignore this category
        response = requests.post(url, data=json.dumps(data))
        response = requests.head(url + f"?title={new_title}&description={new_description}")
        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200

    def test_put_update_category(self):
        title, description = "updated title", "updated description"
        data = {"title": title,"description": description}

        response = requests.get(url)
        request_data = response.json().get("categories")
        id = request_data[0]["id"]
        old_title = request_data[0]["title"]
        old_description = request_data[0]["description"]

        response = requests.put(url + f"/{id}", data=json.dumps(data))
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("id") is not None
        assert request_data.get("title") == title
        assert request_data.get("description") == description
        assert request_data.get("title") != old_title
        assert request_data.get("description") != old_description

    def test_put_update_category_not_found(self):
        title, description = "updated title", "updated description"
        data = {"title": title,"description": description}
        response = requests.put(url + "/999", data=json.dumps(data))
        request_data = response.json()
        assert response.status_code == 404
        assert request_data.get("errorMessages") is not None

    def test_put_update_category_empty_body(self):
        response = requests.get(url)
        request_data = response.json().get("categories")
        id = request_data[0]["id"]
        response = requests.put(url + f"/{id}")
        request_data = response.json()
        assert response.status_code == 400
        assert request_data.get("errorMessages") is not None

    def test_put_update_category_empty_title(self):
        title, description = "", "updated description"
        data = {"title": title,"description": description}
        response = requests.get(url)
        request_data = response.json().get("categories")
        id = request_data[0]["id"]
        response = requests.put(url + f"/{id}", data=json.dumps(data))
        request_data = response.json()
        assert response.status_code == 400
        assert request_data.get("errorMessages") is not None

    def test_put_update_category_empty_description(self):
        title, description = "updated title", ""
        data = {"title": title,"description": description}
        response = requests.get(url)
        request_data = response.json().get("categories")
        id = request_data[0]["id"]
        old_title = request_data[0]["title"]
        old_description = request_data[0]["description"]
        response = requests.put(url + f"/{id}", data=json.dumps(data))
        request_data = response.json()
        assert response.status_code == 200
        assert request_data.get("errorMessages") is None
        assert request_data.get("id") is not None
        assert request_data.get("title") == title
        assert request_data.get("description") == description
        assert request_data.get("title") != old_title
        assert request_data.get("description") != old_description

    def test_delete_category(self):
        response = requests.get(url)
        request_data = response.json().get("categories")
        id = request_data[0]["id"]
        response = requests.delete(url + f"/{id}")
        assert response.status_code == 200
        assert requests.get(url + f"/{id}").status_code == 404

    def test_delete_category_not_found(self):
        response = requests.delete(url + "/999")
        assert response.status_code == 404
        assert response.json().get("errorMessages") is not None
    
    def test_delete_category_empty_path(self):
        response = requests.delete(url)
        assert response.status_code == 405
        

if __name__ == "__main__":
    pytest.main()