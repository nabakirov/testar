### Save   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/questions***   
```javascript
request
    POST
        "text": "string" // (Required)
        "correct_answers": ["string", "string", ..., ] // (Required) array of strings
        "incorrect_answers": ["string", "string", ..., ] // (Required) array of strings
response
    Question(*)
    "answers": [
        Answer (*)
        ...,
    ]
    "message": "str"
    "status": "int"
```
[Question](/docs/v1/objects.md#question)   
[Answer](/docs/v1/objects.md#answer)
### Update   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/questions/<id>***   
```javascript
request
    PATCH
        "text": "string" (Required)
response
    Question(*)
    "message": "str"
    "status": "int"
```
[Question](/docs/v1/objects.md#question)
### Delete   
Authorization: Bearer *token* (given in login, registration)    
access role: ***admin***, ***manager***   
***/v1/questions/<id>***   
```javascript
request
    DELETE
response
    Question(*)
    "answers": [
        Answer(*),
        ...
    ]
    "message": "str"
    "status": "int"
```
[Question](/docs/v1/objects.md#question)   
[Answer](/docs/v1/objects.md#answer)
### List   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/questions***   
```javascript
request
    GET
response
    "questions": [
        Question (*)
        ...,
    ]
    "message": "str"
    "status": "int"
```
[Question](/docs/v1/objects.md#question)
### One   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/questions/<id>***   
```javascript
request
    GET
response
    Question(*)
    "answers": [
        Answer(*),
        ...
    ]
    "message": "str",
    "status": "int"
```   
[Question](/docs/v1/objects.md#question)   
[Answer](/docs/v1/objects.md#answer)


