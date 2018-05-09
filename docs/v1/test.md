### Save   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/tests***   
```javascript
request
    POST
        "title": "string" // (Required)
        "description": "string" // (Optional)
        "questions": [
            "int"
        ] // [1, 2, 3]
response
    Test (*)
    "message": "str"
    "status": "int"
```   
[Test](/docs/v1/objects.md#test)   

### List   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/tests***   
```javascript
request
    GET
response
    "tests": [
        Test (*),
    ]
    "message": "str"
    "status": "int"
```   
[Test](/docs/v1/objects.md#test)   

### Detail   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/tests/id***   
```javascript
request
    GET
response
    Test (*)
    "questions": [
        {
            Question (*),
            "answers": [
                Answer (*),
            ]
    ]
    "message": "str"
    "status": "int"
```   
[Question](/docs/v1/objects.md#question)   
[Answer](/docs/v1/objects.md#answer)   
[Test](/docs/v1/objects.md#test)  