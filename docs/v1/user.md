### login   
Authorization: Bearer *token* (given in login, registration)    
access role: ***public***   
***/v1/login***   
```javascript
request
    POST
        "testar": "string" (Required) [email or username]
        "password": "string" (Required)
response
    User(*)
    "jwt": string [JWT TOKEN]
    "message": str
    "status": int
```   
[User](#user)   
### Registration   
Authorization: Bearer *token* (given in login, registration)  
access role: ***public***   
***/v1/register***
```javascript
request
    POST
        "email": "string" (Required)
        "username": "string" (Required)
        "password": "string" (Required)
        "first_name": "string" (Required)
        "last_name": "string" (Required)
response
    User(*)
    "jwt": "string" [JWT TOKEN]
    "message": "string"
    "status": "string"
```   
[User](#user)   
### Update   
Authorization: Bearer *token* (given in login, registration)    
access role: ***public***   
***/v1/me***   
```javascript
request
    POST
        "email": "string" (Optional)
        "username": "string" (Optional)
        "old_password": "string" (Optional, if changing password Required)
        "new_password": "string" (Optional, if changing password Required)
response
    User(*)
    "message": str
    "status": int
```   
[User](#user)    
### List   
Authorization: Bearer *token* (given in login, registration)    
access role: ***admin***, ***manager***   
***/v1/users***   
```javascript
request
    GET
response
    "users": "array of" - User(*)
    "message": str
    "status": int
```   
[User](#user)    

   
