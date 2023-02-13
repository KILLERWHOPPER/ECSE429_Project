# Related Document: ExploratorySessionNotes2.pdf

# Command 1
curl -L -X GET "http://localhost:4567/projects"

# Command 2
curl -L -I "http://localhost:4567/projects"

# Command 3 - Create project with Boolean as string as shown in docs
curl -L -X POST "http://localhost:4567/projects" -H "Content-Type: application/json" --data-raw "{
  \"title\": \"epteur sint occaecat\",
  \"completed\": \"true\",
  \"active\": \"true\",
  \"description\": \"e magna aliqua. Ut e\"
}"

# Command 4 - Create project with Boolean types
curl -L -X POST "http://localhost:4567/projects" -H "Content-Type: application/json" --data-raw "{
  \"title\": \"epteur sint occaecat\",
  \"completed\": true,
  \"active\": true,
  \"description\": \"e magna aliqua. Ut e\"
}"

# Command 5 - Create project with empty request body
curl -L -X POST "http://localhost:4567/projects" --data-raw ""

# Command 6 - Create project with an ID field in the JSON request body
curl --location --request POST 'http://localhost:4567/projects' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": 5,
    "title": "School",
    "completed": false,
    "active": true,
    "description": "schooool work"
}'

# Command 7 - Get a project with ID defined
curl --location --request GET 'http://localhost:4567/projects/3'

# Command 8 - Get a project with an unexistant ID 
curl --location --request GET 'http://localhost:4567/projects/5' \

# Command 9
curl --location --head 'http://localhost:4567/projects/2'

# Command 10
curl --location --head 'http://localhost:4567/projects/5'

# Command 11
curl --location --head 'http://localhost:4567/projects/6'

# Command 12
curl --location --request POST 'http://localhost:4567/projects/4'

# Command 13 - Update a project with non-existing ID
curl --location --request POST 'http://localhost:4567/projects/5' \
--header 'Content-Type: application/json' \

# Command 14
curl --location --request GET 'http://localhost:4567/projects'

# Command 15 - Update a project with given ID 
curl --location --request PUT 'http://localhost:4567/projects/3' \
--header 'Content-Type: application/json' \
--data-raw ' {
    "title": "taxes",
    "completed": false,
    "active": false,
    "description": "taxes"
 }'

# Command 16 - Update a project with given ID
curl --location --request PUT 'http://localhost:4567/projects/6' \
--header 'Content-Type: application/json' \
--data-raw ' {
    "title": "taxes",
    "completed": true,
    "active": true,
    "description": "taxes"
 }
'

# Command 17
curl --location --request DELETE 'http://localhost:4567/projects/2'

# Command 18
curl --location --request GET 'http://localhost:4567/projects'

# Command 19
curl --location --request GET 'http://localhost:4567/projects/1/categories' 

# Command 20
curl --location --request GET 'http://localhost:4567/projects/3/categories'

# Command 21
curl --location --request GET 'http://localhost:4567/projects/4/categories'

# Command 22
curl --location --head 'http://localhost:4567/projects/2/categories'

# Command 23
curl --location --head 'http://localhost:4567/projects/5/categories'

# Command 24 - Update a project's category
curl --location --request POST 'http://localhost:4567/projects/1/categories' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "2"
}'

# Command 25
curl --location --request DELETE 'http://localhost:4567/projects/1/categories/2' 

# Command 26
curl --location --request GET 'http://localhost:4567/projects/1/categories' 