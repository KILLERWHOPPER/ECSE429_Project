#!/bin/bash

# Related Document: ExploratorySessionNotes1.pdf

# Command 1
curl --location --request GET 'http://localhost:4567/todos'

# Command 2
curl --location --head 'http://localhost:4567/todos'

# Command 3
curl --location --request POST 'http://localhost:4567/todos' \
--header 'Content-Type: application/json' \
--data-raw '{
  "id": "6",
  "title": "ECSE427 Assignment 1",
  "doneStatus": true,
  "description": "interactive shell"
}
'

# Command 4
curl --location --request POST 'http://localhost:4567/todos' \
--header 'Content-Type: application/json' \
--data-raw '{
  "id": "3",
  "title": "ECSE427 Assignment 1",
  "doneStatus": true,
  "description": "interactive shell"
}
'

# Command 5
curl --location --request POST 'http://localhost:4567/todos' \
--header 'Content-Type: application/json' \
--data-raw '{
  "id": "4",
  "title": "ECSE428 AssignmentA",
  "doneStatus": true,
  "description": "Story tests and backlog entry"
}
'

# Command 6
curl --location --request POST 'http://localhost:4567/todos' \
--header 'Content-Type: application/json' \
--data-raw '{
  "id": "5",
  "title": "ECSE429 Project A",
  "doneStatus": true,
  "description": "testing the api"
}
'

# Command 7
curl --location --request GET 'http://localhost:4567/todos/4'

# Command 8
curl --location --request GET 'http://localhost:4567/todos/7'

# Command 9
curl --location --head 'http://localhost:4567/todos/1' 

# Command 10 
curl --location --head 'http://localhost:4567/todos/7'

# Command 11
curl --location --head 'http://localhost:4567/todos/9' \
--header 'heyyyyyy: hi' \
--header 'Content-Type: application/json' \
--data-raw '
'

# Command 12
curl --location --request POST 'http://localhost:4567/todos/3' \
--header 'Content-Type: application/json' \
--data-raw '{
  "title": "ECSE428 AssignmentB",
  "doneStatus": true,
  "description": "assignment description in mycourses"
}
'

# Command 13
curl --location --request GET 'http://localhost:4567/todos' \

# Command 14
curl --location --request PUT 'http://localhost:4567/todos/6' \
--header 'Content-Type: application/json' \
--data-raw '{
  "title": "ECSE316 Assignment 2832",
  "doneStatus": false,
  "description": "assignment"
}
'

# Command 15
curl --location --request PUT 'http://localhost:4567/todos/3' \
--header 'Content-Type: application/json' \
--data-raw '{
  "title": "ECSE316 Assignment 2832",
  "doneStatus": false,
  "description": "assignment"
}
'

# Command 16 
curl --location --request DELETE 'http://localhost:4567/todos/4' \
--header 'Content-Type: application/json' 


# Command 17
curl --location --request GET 'http://localhost:4567/todos' \

# Command 18
curl --location --request GET 'http://localhost:4567/todos/1/categories' 

# Command 19
curl --location --request GET 'http://localhost:4567/todos/2/categories'

# Command 20
curl --location --request GET 'http://localhost:4567/todos/5/categories'

# Command 21
curl --location --request GET 'http://localhost:4567/todos/6/categories'

# Command 22
curl --location --head 'http://localhost:4567/todos/2/categories'

# Command 23
curl --location --head 'http://localhost:4567/todos/5/categories'

# Command 24
curl --location --request POST 'http://localhost:4567/todos/2/categories' \
--header 'Content-Type: application/json' \
--data-raw '{
  "categories": [
    {
      "id": "1"
    }
  ]
}
'

# Command 25
curl --location --request POST 'http://localhost:4567/todos/2/categories' \
--header 'Content-Type: application/json' \
--data-raw '{
  "categories": [
    {
      "id": "2",
      "title": "Admin",
      "description": ""
    }
  ]
}
'

# Command 26
curl --location --request POST 'http://localhost:4567/todos/3/categories' \
--header 'Content-Type: application/json' \
--data-raw '{
  "categories": [
    {
      "id": "2",
      "title": "Admin",
      "description": ""
    }
  ]
}
'

# Command 27
curl --location --request DELETE 'http://localhost:4567/todos/1/categories/1' \
--header 'Content-Type: application/json' 

# Command 28
curl --location --request GET 'http://localhost:4567/todos/1/categories'