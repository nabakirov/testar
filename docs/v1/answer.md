### Save   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions/<question_id>/answers***   
```javascript
request
    POST
        "text": "string" (Required)
        "correct": "boolean"
response
    "id": "int",
    "correct": "boolean",
    "text": "string",
    "message": "str",
    "status": "int"
```   
### Update   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions/<question_id>/answers/<answer_id>***   
```javascript
request
    PATCH
        "text": "string" (Optional),
        "correct": "boolean" (Optional)
response
    "id": "int",
    "correct": "boolean",
    "text": "string",
    "message": "str",
    "status": "int"
```   
### Delete   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions/<question_id>/answers/<answer_id>***   
```javascript
request
    DELETE
response
    "id": "int",
    "correct": "boolean",
    "text": "string",
    "message": "str",
    "status": "int"
```   
### List   
Authorization: Bearer <token> (given in login, registration)   
***/v1/questions/<question_id>/answers***   
```javascript
request
    GET
response
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
