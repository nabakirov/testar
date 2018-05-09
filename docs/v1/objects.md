### User
```javascript
"email": "String"
"id": "int"
"first_name": "String"
"last_name": "String"
"scopes": "array" // of strings ("admin" and "manager" available)
"username": "String"
```

### Question
```javascript
"id": "int"
"text": "string"
"created": "float" // Unix Timestamp, date of creation
```

### Answer
```javascript
"id": "int"
"text": "string"
"correct": "boolean"
```

### Test
```javascript
"id": "int"
"title": "string"
"description": "string"
```

### Competition
```javascript
"id": "int"
"title": "string"
"description": "string"
"start_date": "float" // Unix Timestamp
"end_date": "float" // Unix Timestamp
"test_id": "int"
```

### Group
```javascript
"id": "int"
"title": "string"
"description": "string"
```