### Save   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/questions/<question_id>/answers***   
```javascript
request
    POST
        "text": "string" // (Required)
        "correct": "boolean" // (Required)
response
    Answer (*)
    "message": "str"
    "status": "int"
```   
[Answer](/docs/v1/objects.md#answer)   
### Update   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/questions/<question_id>/answers/<answer_id>***   
```javascript
request
    PATCH
        "text": "string" (Optional),
        "correct": "boolean" (Optional)
response
    Answer (*)
    "message": "str"
    "status": "int"
```   
[Answer](/docs/v1/objects.md#answer)   
### Delete   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/questions/<question_id>/answers/<answer_id>***   
```javascript
request
    DELETE
response
    Answer (*)
    "message": "str"
    "status": "int"
```   
[Answer](/docs/v1/objects.md#answer)   
### List   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/questions/<question_id>/answers***   
```javascript
request
    GET
response
    "answers": [
        Answer (*)
        ...,
    ] //array of dictionaries
    "message": "str",
    "status": "int"
```   
[Answer](/docs/v1/objects.md#answer)   
