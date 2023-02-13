#!/bin/bash

# Related Document: ExploratorySessionNotes3.pdf

# Command 1
curl --location --request GET 'http://localhost:4567/categories'

# Command 2
curl --location --head 'http://localhost:4567/categories'

# Command 3 - Create a new category
curl --location --request POST 'http://localhost:4567/categories' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Admin",
    "description": "admin"
}'

# Command 4 - Create a new category
curl --location --request POST 'http://localhost:4567/categories' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Fun",
    "description": "fun"
}'

# Command 5 - Create a new category including an ID
curl --location --request POST 'http://localhost:4567/categories' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": 5
    "title": "Fun",
    "description": "fun"
}'

# Command 6
curl --location --request GET 'http://localhost:4567/categories/3'

# Command 7
curl --location --request GET 'http://localhost:4567/categories/3'

# Command 8
curl --location --request GET 'http://localhost:4567/categories/3'

# Command 9
curl --location --head 'http://localhost:4567/categories/1'

# Command 10
curl --location --head 'http://localhost:4567/categories/1'

# Command 11 - Update category with defined title and description
curl --location --request POST 'http://localhost:4567/categories/3' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Admin",
    "description": "admin"
}'

# Command 12
curl --location --request GET 'http://localhost:4567/categories'

# Command 13 - Update category with inexistant ID
curl --location --request PUT 'http://localhost:4567/categories/5' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Admin",
    "description": "admin"
}'

# Command 14 - Update category with existant ID
curl --location --request PUT 'http://localhost:4567/categories/2' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Admin",
    "description": "admin"
}'

# Command 15
curl --location --request DELETE 'http://localhost:4567/categories/2'

# Command 16
curl --location --request GET 'http://localhost:4567/categories'

# Command 17
curl --location --request GET 'http://localhost:4567/categories/1/projects' 

# Command 18
curl --location --request GET 'http://localhost:4567/categories/2/projects' 

# Command 19
curl --location --request GET 'http://localhost:4567/categories/4/projects'

# Command 20
curl --location --head 'http://localhost:4567/categories/2/projects' 

# Command 21
curl --location --head 'http://localhost:4567/categories/5/projects' 

# Command 22 - Create a relationship between a category's instance and a project's instance
curl --location --request POST 'http://localhost:4567/categories/1/projects' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "1"
}'

# Command 23 - Create a relationship between a category's instance and a non-existant project's instance
curl --location --request POST 'http://localhost:4567/categories/2/projects' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "2"
}'

# Command 24
curl --location --request DELETE 'http://localhost:4567/categories/1/projects/1'

# Command 25
curl --location --request GET 'http://localhost:4567/categories/1/projects'

# Command 26
curl --location --request GET 'http://localhost:4567/categories/1/todos'

# Command 27
curl --location --request GET 'http://localhost:4567/categories/3/todos'

# Command 28
curl --location --head 'http://localhost:4567/categories/2/todos'

# Command 29
curl --location --head 'http://localhost:4567/categories/5/todos'

# Command 30 - Create a relationship between a category's instance and a todo's instance
curl --location --request POST 'http://localhost:4567/categories/1/todos' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "1"
}'

# Command 31 - Create a relationship between a category's instance and a non-existant todo's instance
curl --location --request POST 'http://localhost:4567/categories/2/todos' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "3"
}'

# Command 32
curl --location --request DELETE 'http://localhost:4567/categories/1/todos/1'

# Command 33
curl --location --request GET 'http://localhost:4567/categories/1/todos'