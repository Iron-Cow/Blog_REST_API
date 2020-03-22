Here is simple REST API for authenticated Posts creations and likes adding/removing.

# To do:
#### User block
- [x] models setup
- [x] serializers setup
- [x] urls + other setup
- [x] user signup
- [x] user login (JWT Token authentication and refresh)
---

#### Post block
- [x] models setup
- [x] serializers setup
- [x] urls + other setup
- [x] post creation
- [x] post like
- [x] post unlike
---

### Tests
- [x] Users tests
- [x] Post tests

----

# API Endpoint

**http://127.0.0.1:8000/api/v1/**

# Public data

### Get Posts list 

#### Path
**GET /posts**

#### Responses
**200 OK**

#### Response Example (200 OK)
    [
        {
            "id": 4,
            "title": "test post",
            "content": "Text of the post",
            "user": 31,
            "liked_users": [],
            "timestamp": "2020-03-22T23:36:20.634425+02:00"
        },
        
        {
            "id": 2,
            "title": "Admin post now",
            "content": "Edited by Admin",
            "user": 1,
            "liked_users": [
                31
            ],
            "timestamp": "2020-03-22T16:01:29.062520+02:00"
        }
    ]

### Retrieve post details 

#### Path
**GET /posts/{post_id}**

#### Request parameters
**post_id**: integer (in path)

#### Responses
**200 OK**

#### Response Example (200 OK)

    {
        "id": 2,
        "title": "Admin post now",
        "content": "Edited by Admin",
        "user": 1,
        "liked_users": [
            31
        ],
        "timestamp": "2020-03-22T16:01:29.062520+02:00"
    }

# Actions for authenticated user

### Register a new user

#### Path
**POST /users**

#### Request parameters
**username**: string (in body)

**email**: string (in body / 8+ symbols long)

**password**: string (in body / valid email to pass validation)

#### Responses
**201 Created**

####Response Example (201 Created)

    {
        "username": "User265",
        "email": "email@gmail.com",
        "password": "pbkdf2_sha256$182000$1jZ7R0w4dk1v$Jt7ZBVnE7AupR4UM4woWqc5oGvEOc0tGfwD1xz9pe7Y=",
        "email_check": "passed",
        "email_block": false,
        "email_accept_all": false
    }

### Get Access Token

#### Path
**POST /token**

#### Request parameters

**username**: string (in body)

**password**: string (in body)

#### Responses
**200 OK**

#### Response Example (200 OK)

    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTAwMDcwMCwianRpIjoiMzA5MWEyZDZmZTMwNGY0ZGI5MGU0MTVmMTk4ODBhNWEiLCJ1c2VyX2lkIjozMX0.pNh3zQ3fCxxzZgiAjFTJXzcWl7JATijwzcNG74TPZ6A",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0OTE0NjAwLCJqdGkiOiI3ZDFiNzIzYjIyYTg0ZWFlOTYyNThkZmMwY2EyOTE4ZiIsInVzZXJfaWQiOjMxfQ.Ii7ww-Ul38VxKWghDrMdr2gAlYU9LyX69uMY81_6o7E"
    }

### Refresh Access Token

#### Path
**POST /token/refresh**

#### Request parameters

**refresh**: string (in body)

#### Responses
**200 OK**

#### Response Example (200 OK)

    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0OTE1NjIxLCJqdGkiOiI1M2MxMzNjNDRmZjA0NGU5ODVkYmFlNzYzYjQzZjhjNiIsInVzZXJfaWQiOjMxfQ.k4h12Gb2vaFXzindYTivEva__3LzHj9aQN3pytXaUz4"
    }

### Create a new post

#### Path
**POST /posts/**

#### Request parameters

**_Authorization_**: 'Bearer ' + Token, string (in header)

**title**: string (in body)

**content**: string (in body)

#### Responses
**201 Created**

#### Response Example (200 OK)

    {
        "id": 9,
        "title": "New Title",
        "content": "New Text",
        "user": 31,
        "liked_users": [],
        "timestamp": "2020-03-23T00:24:25.427814+02:00"
    }
    
    
    
### Add like to the post

#### Path
**POST /posts/{post_id}/like**

#### Request parameters

**_Authorization_**: 'Bearer ' + Token, string (in header)

**post_id**: integer (in path)

#### Responses
**200 Created**

#### Response Example (200 OK)
    {
        "status": "your like added"
    }
   
### Remove like from the post

#### Path
**POST /posts/{post_id}/remove_like**

#### Request parameters

**_Authorization_**: 'Bearer ' + Token, string (in header)

**post_id**: integer (in path)

#### Responses
**200 OK**

#### Response Example (200 OK)
    {
        "status": "your like removed"
    }
    
# Actions for admin or postowner

### Edit post

#### Path
**PATCH /posts/{post_id}**

#### Request parameters

**_Authorization_**: 'Bearer ' + Token, string (in header)

**post_id**: integer (in path)

**title**: string (in body)

**content**: string (in body)

#### Responses
**200 OK**

#### Response Example (200 OK)
    {
        "id": 9,
        "title": "New Title Edited",
        "content": "New Text Edited",
        "user": 31,
        "liked_users": [],
        "timestamp": "2020-03-23T00:37:56.615808+02:00"
    }
    
    
### Delete post

#### Path
**DELETE /posts/{post_id}**

#### Request parameters

**_Authorization_**: 'Bearer ' + Token, string (in header)

**post_id**: integer (in path)


#### Responses
**204 No Content**

#### Response Example (204 No Content)
No data