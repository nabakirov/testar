### Save   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/competitions***   
```javascript
request
    POST
        "title": "string" // (Required)
        "description": "string" // (Optional)
        "test": "int" // (Required)
        "start_date": "float" // (Required) Unix timestamp
        "end_date": "float" // (Required) Unix timestamp
response
    Competition (*)
    "message": "str"
    "status": "int"
```   
[Competition](/docs/v1/objects.md#competition)   
### List   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/competitions***   
```javascript
request
    GET
response
    "competitions": [
        Competition (*),
    ]
    "message": "str"
    "status": "int"
```   
[Competition](/docs/v1/objects.md#competition)   
### Update   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/competitions***   
```javascript
request
    PATCH
        "title": "string" // (Optional)
        "description": "string" // (Optional)
        "start_date": "float" // (Optional) Unix timestamp
        "end_date": "float" // (Optional) Unix timestamp
response
    Competition (*)
    "message": "str"
    "status": "int"
```   
[Competition](/docs/v1/objects.md#competition)   
### Detail   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/competitions/id***   
```javascript
request
    GET
response
    Competition (*)
    "participants": [
        User (*),
    ]
    "test": {
        Test (*)
        "questions":[
            {
                Question (*)
                "answers": [
                    Answer (*),
                    ...
                ]
            },
            ...
        ]
    }
    "message": "str"
    "status": "int"
```   
[Competition](/docs/v1/objects.md#competition)   
[User](/docs/v1/objects.md#user)   
[Test](/docs/v1/objects.md#test)   
[Question](/docs/v1/objects.md#question)   
[Answer](/docs/v1/objects.md#answer)   

### Get Test For Participant   
Authorization: Bearer *token* (given in login, registration)   
access role: ***public***   
***/v1/competitions/id/test***   
```javascript
request
    GET
response
    Competition (*)
    "test": {
        Test (*)
        "questions": [
            {
                "id": "int"
                "text": "string"
                "answers": [
                    {
                        "id": "int",
                        "text": "string"
                    },
                    ...
                ]
            },
            ...
        ]
    }
    "message": "str"
    "status": "int"
```   
[Competition](/docs/v1/objects.md#competition)   
[Test](/docs/v1/objects.md#test)   
### Submit Participant Test   
Authorization: Bearer *token* (given in login, registration)   
access role: ***admin***, ***manager***   
***/v1/competitions/id/submit***   
```javascript
request
    POST
        "questions":[
            {
                "question": "int"
                "answer": "int"
            },
            ...
        ]
response
    "corrects": "int" // count of correct unswered questions
    "total": "int" // total count of questions
    "message": "str"
    "status": "int"
```   