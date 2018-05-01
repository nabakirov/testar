### Save   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions***   
```javascript
request
    POST
        "text": "string" (Required)
        "correct_answers": ["string", "string", ..., ] (Required) //[array of strings]
        "incorrect_answers": ["string", "string", ..., ] (Required) //[array of strings]
response
    "question": {
        "created": "float" //[unix timestamp],
        "id": "int",
        "text": "string"
    } [dictionary],
    "answers": [
        {  
            "id": "int",
            "correct": "boolean",
            "text": "string"
        },
        ...,
    ] //array of dictionaries
    
    "message": "str",
    "status": "int"
```   
### Update   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions/<id>***   
```javascript
request
    PATCH
        "text": "string" (Required)
response
    "created": "float" //[unix timestamp],
    "id": "int",
    "text": "string"
    "message": "str",
    "status": "int"
```   
### Delete   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions/<id>***   
```javascript
request
    DELETE
response
    "question": {
        "created": "float" // unix timestamp,
        "id": "int",
        "text": "string"
    } // dictionary,
    "answers": [
        {  
            "id": "int",
            "correct": "boolean",
            "text": "string"
        },
        ...,
    ] //array of dictionaries
    "message": "str",
    "status": "int"
```   
### List   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions***   
```javascript
request
    GET
response
    "questions": [
        {
            "created": "float" //[unix timestamp],
            "id": "int",
            "text": "string"
        },
        ...,
    ] // array of dictionaries
    "message": "str",
    "status": "int"
```   
### One   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions/<id>***   
```javascript
request
    GET
response
    "created": "float" //[unix timestamp],
    "id": "int",
    "text": "string",
    "answers": [
        {  
            "id": "int",
            "correct": "boolean",
            "text": "string"
        },
        ...,
    ] //array of dictionaries
    "message": "str",
    "status": "int"
```   
