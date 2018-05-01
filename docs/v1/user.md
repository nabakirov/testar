### login
***/v1/login***   
```javascript
request
    POST
        "testar": string (Required) [email or username]
        "password": string (Required)
response
    "id": int [user id],
    "email": string,
    "jwt": string [JWT TOKEN],
    "message": str,
    "status": int
```   
### Registration   
***/v1/register***
```javascript
request
    POST
        "email": string (Required)
        "username": string (Required)
        "password": string (Required)
response
    "id": int [user id],
    "email": string,
    "jwt": string [JWT TOKEN],
    "message": str,
    "status": int
```   
### Update   
***/v1/me***   
Authorization: Bearer <token> (given in login, registration)   
```javascript
request
    POST
        "email": string (Optional)
        "username": string (Optional)
        "old_password": string (Optional*)
        "new_password": string (Optional*)
response
    "id": int [user id],
    "email": string,
    "jwt": string [JWT TOKEN],
    "message": str,
    "status": int
```   

