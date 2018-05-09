### List   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/competitions/id/participants***   
```javascript
request
    GET
response
    "participants":[
        {
            User (*),
            "submission":[
                {
                    "answer": "int"
					"question": "int"
                },
                ...
            ]
        },
        ...
    ]
    "message": "str"
    "status": "int"
```   
[User](/docs/v1/objects.md#user)   
### Add to competition   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/competitions/id/participants***   
```javascript
request
    POST
        "users": [
            "string" // username, email, id
        ]
response
    "added": [
        User(*),
        ...
    ]
    "invited": [
        "string" // emails to be invited
    ]
    "unknown_ids": [
        "int"
    ]
    "unknown_usernames": [
        "string"
    ]
    "message": "str"
    "status": "int"
```   
[User](/docs/v1/objects.md#user)   