### List   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/groups***   
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
            "questions": [
                Question (*),
                ...
            ]
        },
        ...
    ]
    "questions": [
        Question (*),
        ...
    ]
    "message": "str"
    "status": "int"
```   
[Group](/docs/v1/objects.md#group)   
[Question](/docs/v1/objects.md#question)   
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
        "questions": ["int"] // (Optional) 
response
    
    Group (*)
    // If entry_id was send
    "entry_group": Group(*)
    // if questions was send
    "questions": [
        Question(*),
        ...
    ]
    "message": "str"
    "status": "int"
```   
[Group](/docs/v1/objects.md#group)   
