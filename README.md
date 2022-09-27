# PAD
Repository for Programming Distribuited Applications course at university

# Gateway
# Routes
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
Route: /login
Input json format:
{
    "login":"login",
    "password":"password"
}
Output json format:

status == 200:
{
    "userId":"userId",
    "authToken":"authToken"
}
else: no json output
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