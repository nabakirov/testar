### List   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/user/groups***   
```javascript
request
    GET
response
    "groups":[
        Group (*),
        ...
    ]
    "message": "str"
    "status": "int"
```   
[Group](/docs/v1/objects.md#group)   
### Save   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/groups***   
```javascript
request
    POST
        "description": "string"
        "title": "string"
response
    Group (*)
    "message": "str"
    "status": "int"
```   
[Group](/docs/v1/objects.md#group)   
### detail (recursive)   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/groups/id***   
```javascript
request
    GET
response
    Group (*)
    "groups": [
        {
            Group(*),
            "groups": [
                ... // the same object like in first level json
            ]
            "users": [
                User (*),
                ...
            ]
        },
        ...
    ]
    "users": [
        User (*),
        ...
    ]
    "message": "str"
    "status": "int"
```   
[Group](/docs/v1/objects.md#group)   
[User](/docs/v1/objects.md#user)   
### Link   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/grouping***   
```javascript
request
    POST // to link
    DELETE // to unlink
        "group": "int" // (Required)
        // One of below
        "entry_group": "int" // (Optional)
        "users": ["int"] // (Optional) 
response
    
    Group (*)
    // If entry_id was send
    "entry_group": Group(*)
    // if questions was send
    "users": [
        User(*),
        ...
    ]
    "message": "str"
    "status": "int"
```   
[User](/docs/v1/objects.md#user)   
