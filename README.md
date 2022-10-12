# PAD

Repository for Programming Distribuited Applications course at university

# Gateway

# Routes

- /register

- /login

- /getUserVal
- /setUserVal
- /sendFriendRequest
- /getUserUpdates

- /sendMessage
- /getMessages

- /discover

# IO:

```
Route: /register
Input json format:
{
    "email":"string",
    "name":"string",
    "password":"string",
    "passwordConfirm":"string"
}
Output json format:

status == 200:
{
  "status": "success",
  "user": {
    "name": "string",
    "email": "string",
    "role": "user",
    "created_at": "2022-10-12T07:22:57.012000",
    "updated_at": "2022-10-12T07:22:57.012000",
    "id": "63466b5129b84965cfde61ba"
  }
}
else: 
{
  "detail": "Account already exist"
}
```

```
Route: /login
Input json format:
{
    "email":"string",
    "password":"password"
}
Output json format:

status == 200:
{
  "status": "success",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2MzQ2NmI1MTI5Yjg0OTY1Y2ZkZTYxYmEiLCJpYXQiOjE2NjU1NjI0NTYsIm5iZiI6MTY2NTU2MjQ1NiwianRpIjoiNGE4ODcxODEtYmU3My00ZmMwLThmZGYtMmM5ZjljMjJjNjA3IiwiZXhwIjoxNjY1NTYzMzU2LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlfQ.J9lOuF_fv-vqSa4vOQpT4qxtRFTvVV72MZajIuYQbGoJwzG7znPUpnrvlC_Qtlf4QDFFAH9W1NyI91w2uIAWag"
}
else: 
{
  "detail": "Incorrect Email or Password"
}
```

```
Route: /getUserVal
Input json format:
{
    "userId":"userId",
    "authToken":"authToken",
    "valId":"valId"
}
Output json format:
status == 200:
{
    "userId":"userId",
    "valId":"valId",
    "value":"value"
}
else: 
{
    "userId":"userId",
    "valId":"valId",
    "reason":"Invalid valId"
}
```

```
Route: /setUserVal
Input json format:
{
    "userId":"userId",
    "authToken":"authToken",
    "valId":"valId",
    "value":"value"
}
Output json format:
status == 200: no json output
else: 
{
    "userId":"userId",
    "valId":"valId",
    "reason":"Invalid valId"
}
```

```
Route: /sendMessage
Input json format:
{
    "userId":"userId",
    "authToken":"authToken",
    "receiverId":"receiverId",
    "message":"message"
}
Output json format
status == 200: 
{
    "messageId":"messageId"
}
else:
{
    "reason":"Invalid authToken"
}
```

```
Route: /getMessages
Input json format:
{
    "userId":"userId",
    "authToken":"authToken",
    "receiverId":"receiverId",
    "fromTimestamp":"fromTimestamp",
    "toTimestamp":"toTimestamp"
}
Output json format
status == 200: 
{
    "messages": [
        {
            "message1":"message1",
            "timestamp":"timestamp"
        },
        {
            "message1":"message1",
            "timestamp":"timestamp"
        }
    ]
}
else:
{
    "reason":"Invalid authToken"
}
```

```
Route: /getUserUpdates
Input json format:
{
    "userId":"userId",
    "authToken":"authToken",
    "fromTimestamp":"fromTimestamp",
}
Output json format
status == 200: 
{
    "message":"message"
}
else:
{
    "reason":"Invalid authToken"
}
```

```
Route: /discover
Input json format:
no json input

Output json format:
status == 200:
{
    "serviceIds":["serviceId1", "serviceId2"],
    "addresses":["address1", "address2"],
    "ports":["port1", "port2"],
}
else: no json output
```